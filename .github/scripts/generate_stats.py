#!/usr/bin/env python3
"""
Generate the contribution stats card (stats.svg / stats-light.svg).

Uses the same contribution calendar GitHub draws on the profile page (GraphQL
contributionCalendar, last 12 months), so the numbers match the profile:
total contributions, active days, current streak and longest streak.
Private contributions are included when "Private contributions" is turned on
in the profile's Contribution settings.

Usage:
  GITHUB_TOKEN=... python3 generate_stats.py <user> <outdir>
  python3 generate_stats.py --from-json calendar.json <outdir>   # offline test
"""
import json, os, sys, urllib.request
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_projects as gp  # reuse themes + font so the look matches

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def fetch_calendar(login):
    token = os.environ.get("GITHUB_TOKEN", "")
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "stats-card",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def compute(cal):
    days = sorted(
        (date.fromisoformat(d["date"]), d["contributionCount"])
        for w in cal["weeks"] for d in w["contributionDays"]
    )
    active = sum(1 for _, c in days if c > 0)

    # longest streak
    best = (0, None, None)
    run, start = 0, None
    for d, c in days:
        if c > 0:
            if run == 0:
                start = d
            run += 1
            if run > best[0]:
                best = (run, start, d)
        else:
            run = 0

    # current streak: today may still be empty without breaking it
    cur, cur_start, cur_end = 0, None, None
    i = len(days) - 1
    if i >= 0 and days[i][1] == 0:
        i -= 1
    while i >= 0 and days[i][1] > 0:
        cur += 1
        cur_start = days[i][0]
        cur_end = cur_end or days[i][0]
        i -= 1

    return {
        "total": cal["totalContributions"],
        "active": active,
        "span": len(days),
        "first": days[0][0] if days else None,
        "last": days[-1][0] if days else None,
        "current": (cur, cur_start, cur_end),
        "longest": best,
    }


def fmt(d):
    return f"{d.day:02d} {MESES[d.month - 1]} {d.year}" if d else ""


def rng(a, b):
    if not a:
        return "—"
    return fmt(a) if a == b else f"{fmt(a)} → {fmt(b)}"


def plural(n, one, many):
    return one if n == 1 else many


def build(s, theme):
    gp.set_theme(theme)
    T = gp.THEMES[theme]
    W, H, M = gp.W, 150, gp.MARGIN
    gid = f"st_{theme}"
    cur_n, cur_a, cur_b = s["current"]
    lon_n, lon_a, lon_b = s["longest"]
    tiles = [
        ("CONTRIBUIÇÕES", f"{s['total']:,}".replace(",", "."), "no último ano", rng(s["first"], s["last"]), T["CYAN"]),
        ("DIAS ATIVOS", str(s["active"]), f"de {s['span']} dias", f"{s['active'] * 100 // max(s['span'], 1)}% dos dias", T["VIOLET"]),
        ("SEQUÊNCIA ATUAL", str(cur_n), plural(cur_n, "dia", "dias"), rng(cur_a, cur_b), T["EMERALD"]),
        ("MAIOR SEQUÊNCIA", str(lon_n), plural(lon_n, "dia", "dias"), rng(lon_a, lon_b), T["CYAN"]),
    ]
    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{gp.FONT}" role="img" aria-label="Estatísticas de contribuições">')
    a(f'<rect width="{W}" height="{H}" fill="{T["BG"]}"/>')
    a(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{T["VIOLET2"]}"><animate attributeName="stop-color" values="{T["VIOLET2"]};{T["CYAN"]};{T["EMERALD"]};{T["VIOLET2"]}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{T["EMERALD"]}"><animate attributeName="stop-color" values="{T["EMERALD"]};{T["VIOLET2"]};{T["CYAN"]};{T["EMERALD"]}" dur="10s" repeatCount="indefinite"/></stop>'
      '</linearGradient></defs>')
    a(f'<text x="{M+2}" y="18" font-size="11" letter-spacing="2" fill="{T["CYAN"]}">CONTRIB.STATS</text>')
    a(f'<text x="{M+130}" y="18" font-size="10" fill="{T["DIM"]}">./stats.sh --last-year</text>')
    a(f'<line x1="{M}" y1="28" x2="{W-M}" y2="28" stroke="url(#{gid})" stroke-width="1.5" opacity="0.7"/>')

    gap = 14
    tw = (W - 2 * M - 3 * gap) / 4
    th = 100
    y = 42
    for i, (label, big, unit, sub, color) in enumerate(tiles):
        x = M + i * (tw + gap)
        a(f'<g transform="translate({x:.1f},{y})">')
        a(f'<rect width="{tw:.1f}" height="{th}" rx="8" fill="{T["PANEL"]}" stroke="{T["STROKE"]}"/>')
        a(f'<circle cx="16" cy="18" r="3" fill="{color}"><animate attributeName="opacity" values="1;0.3;1" dur="2.4s" begin="{i*0.4}s" repeatCount="indefinite"/></circle>')
        a(f'<text x="26" y="22" font-size="10" letter-spacing="1.5" fill="{T["MUTED"]}">{gp.esc(label)}</text>')
        a(f'<text x="16" y="64" font-size="30" font-weight="700" fill="{T["TEXT"]}">{gp.esc(big)}'
          f'<tspan dx="8" font-size="12" font-weight="400" fill="{color}">{gp.esc(unit)}</tspan></text>')
        a(f'<text x="16" y="86" font-size="10" fill="{T["DIM"]}">{gp.esc(sub)}</text>')
        a('</g>')
    a('</svg>')
    return "".join(out)


def main():
    args = sys.argv[1:]
    if args and args[0] == "--from-json":
        with open(args[1]) as f:
            cal = json.load(f)
        outdir = args[2] if len(args) > 2 else "."
    else:
        login = args[0] if args else os.environ.get("GITHUB_REPOSITORY_OWNER", "")
        outdir = args[1] if len(args) > 1 else "."
        cal = fetch_calendar(login)
    s = compute(cal)
    os.makedirs(outdir, exist_ok=True)
    for theme, fname in (("dark", "stats.svg"), ("light", "stats-light.svg")):
        path = os.path.join(outdir, fname)
        with open(path, "w") as f:
            f.write(build(s, theme))
        print(f"wrote {path}")
    print(f"total={s['total']} active={s['active']} current={s['current'][0]} longest={s['longest'][0]}")


if __name__ == "__main__":
    main()
