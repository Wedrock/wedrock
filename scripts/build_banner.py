#!/usr/bin/env python3
"""Gera dark.svg e light.svg (banner animado em estilo terminal).
Edite INFO / CONTATOS / CODIGO abaixo e rode:  python3 scripts/build_banner.py
"""
import html

TITLE_BAR = "Wedrock - % ./perfil.sh --live"
INFO = [
    ("Nome", "João Danjour"),
    ("Função", "Desenvolvedor Web"),
    ("Origem", "Brasil"),
    ("Formação", "Ensino Médio Técnico"),
    ("Status", "Aprendendo + Criando + Entregando"),
    ("Ferramentas", "VS Code, Git, GitHub"),
    ("Linguagens", "JavaScript, HTML, CSS"),
]
CONTATOS = [
    ("LinkedIn", "joão-danjour"),
    ("Instagram", "@joao.danjour"),
    ("GitHub", "@Wedrock"),
]
CODIGO = [
    ("const ", "dev", " = {"),
    ("  nome: ", '"João Danjour"', ","),
    ("  github: ", '"Wedrock"', ","),
    ("  foco: ", '["web", "e-commerce"]', ","),
    ("  status: ", '"em construção"', ","),
    ("};", "", ""),
    ("", "", ""),
    ("dev.", "build", "();"),
]

THEMES = {
    "dark": dict(BG1="#0A101F", BG2="#0C1426", BAR="#0B1222", OUT="#070B16", CYAN="#22D3EE", VIOLET="#A78BFA",
                 TEXT="#F8FAFC", MUTED="#94A3B8", DIM="#475569", DOT="rgba(148,163,184,0.35)",
                 LINE="rgba(255,255,255,0.10)", PILL="#4C1D95", PILLTX="#E9D5FF", STR="#10B981", KW="#A78BFA"),
    "light": dict(BG1="#F8FAFC", BG2="#FFFFFF", BAR="#F1F5F9", OUT="#E2E8F0", CYAN="#0891B2", VIOLET="#7C3AED",
                  TEXT="#0F172A", MUTED="#475569", DIM="#94A3B8", DOT="rgba(71,85,105,0.35)",
                  LINE="rgba(0,0,0,0.10)", PILL="#EDE9FE", PILLTX="#4C1D95", STR="#059669", KW="#7C3AED"),
}


def e(s):
    return html.escape(s, quote=False)


def row(t, y, begin, label, value):
    n = max(4, 78 - len(label) - len(value) - 2)
    return (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" values="-8 0;0 0" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
        f'<text x="470" y="{y}" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
        f'<tspan fill="{t["CYAN"]}">{e(label)} </tspan><tspan fill="{t["DOT"]}">{"." * n}</tspan>'
        f'<tspan fill="{t["TEXT"]}" font-weight="600"> {e(value)}</tspan></text></g>'
    )


def build(name):
    t = THEMES[name]
    o = []
    a = o.append
    a('<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" '
      'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,\'Liberation Mono\',monospace" role="img" '
      'aria-label="João Danjour — perfil.sh --live">')
    a('<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
      '<stop offset="0" stop-color="#7C3AED"><animate attributeName="stop-color" values="#7C3AED;#22D3EE;#10B981;#7C3AED" dur="10s" repeatCount="indefinite"/></stop>'
      '<stop offset="0.5" stop-color="#22D3EE"><animate attributeName="stop-color" values="#22D3EE;#10B981;#7C3AED;#22D3EE" dur="10s" repeatCount="indefinite"/></stop>'
      '<stop offset="1" stop-color="#10B981"><animate attributeName="stop-color" values="#10B981;#7C3AED;#22D3EE;#10B981" dur="10s" repeatCount="indefinite"/></stop></linearGradient>'
      f'<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["BG1"]}"/><stop offset="1" stop-color="{t["BG2"]}"/></linearGradient>'
      '<filter id="glow8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>'
      '<filter id="glow3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>'
      '<clipPath id="winClip"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath></defs>')
    a(f'<rect x="2" y="2" width="1176" height="606" rx="18" fill="{t["OUT"]}"/><g clip-path="url(#winClip)">')
    a(f'<rect x="2" y="2" width="1176" height="606" fill="url(#panelGrad)"/><rect x="2" y="2" width="1176" height="46" fill="{t["BAR"]}"/>')
    a(f'<line x1="2" y1="48" x2="1178" y2="48" stroke="{t["LINE"]}"/>')
    for cx, c in ((30, "#ff5f56"), (50, "#ffbd2e"), (70, "#27c93f")):
        a(f'<circle cx="{cx}" cy="25" r="5.5" fill="{c}"/>')
    a(f'<text x="590" y="29" text-anchor="middle" font-size="12" fill="{t["MUTED"]}">{e(TITLE_BAR)}</text>')
    a(f'<text x="38" y="74" font-size="10" letter-spacing="3" fill="{t["DIM"]}">CODE.MAP</text>')

    # painel de código (esquerda)
    a(f'<rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{t["CYAN"]}" stroke-width="2" opacity="0.45" filter="url(#glow3)"/>')
    a(f'<rect x="36" y="84" width="400" height="492" rx="10" fill="{t["BG1"]}" stroke="{t["CYAN"]}" stroke-opacity="0.35"/>')
    y0, b0 = 130, 0.4
    for i, (p1, p2, p3) in enumerate(CODIGO):
        if p1 or p2 or p3:
            a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{b0 + i * 0.35:.2f}s" fill="freeze"/>'
              f'<text x="56" y="{y0 + i * 34}" font-size="15" xml:space="preserve">'
              f'<tspan fill="{t["KW"]}">{e(p1)}</tspan><tspan fill="{t["STR"]}">{e(p2)}</tspan>'
              f'<tspan fill="{t["MUTED"]}">{e(p3)}</tspan></text></g>')
    ycur = y0 + len(CODIGO) * 34
    a(f'<text x="56" y="{ycur}" font-size="15" fill="{t["CYAN"]}">&#9608;'
      '<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></text>')
    a(f'<path d="M 50 576 L 36 576 L 36 562" fill="none" stroke="{t["CYAN"]}" stroke-width="2" opacity="0.8"/>')
    a(f'<path d="M 422 576 L 436 576 L 436 562" fill="none" stroke="{t["CYAN"]}" stroke-width="2" opacity="0.8"/>')

    # painel de informações (direita)
    a(f'<text x="470" y="106" font-size="13" letter-spacing="2" fill="{t["CYAN"]}">SYSTEM.INFO</text>')
    a(f'<line x1="566" y1="102" x2="1061" y2="102" stroke="{t["LINE"]}"/>')
    a('<text x="1125" y="106" text-anchor="end" font-size="12" fill="#F87171" font-weight="700"><tspan>&#9679;</tspan> LIVE'
      '<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></text>')
    a('<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.6s" fill="freeze"/>'
      f'<rect x="470" y="122" width="200" height="20" rx="4" fill="{t["PILL"]}"/>'
      f'<text x="479" y="136" font-size="14" font-weight="700" fill="{t["PILLTX"]}">Wedrock@github</text>'
      f'<line x1="680" y1="130" x2="1125" y2="130" stroke="{t["LINE"]}"/></g>')
    y, b = 162, 0.9
    for lab, val in INFO:
        a(row(t, y, b, lab, val))
        y += 32
        b += 0.12
    y += 12
    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{b:.2f}s" fill="freeze"/>'
      f'<text x="470" y="{y}" font-size="14" textLength="655" lengthAdjust="spacingAndGlyphs" xml:space="preserve">'
      f'<tspan fill="{t["MUTED"]}">- Contato </tspan><tspan fill="{t["DOT"]}">{"-" * 69}</tspan></text></g>')
    y += 32
    b += 0.12
    for lab, val in CONTATOS:
        a(row(t, y, b, "Grid." + lab, val))
        y += 32
        b += 0.12
    a(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{b + 0.3:.2f}s" fill="freeze"/>'
      f'<text x="470" y="577" font-size="14" fill="{t["MUTED"]}">&#9656; Mais sobre mim e projetos abaixo no README &#8595; '
      f'<tspan fill="{t["CYAN"]}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text></g>')
    a('</g>')
    a('<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.55" filter="url(#glow8)"/>')
    a('<rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="1.6"/></svg>')
    return "\n".join(o)


if __name__ == "__main__":
    for n in THEMES:
        with open(f"{n}.svg", "w", encoding="utf-8") as f:
            f.write(build(n))
        print("ok", n + ".svg")
