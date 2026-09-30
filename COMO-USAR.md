# Como colocar no ar

1. No GitHub, crie um repositório **público** chamado exatamente `Wedrock` (igual ao seu usuário) e marque "Add a README".
2. Envie todos os arquivos desta pasta (inclusive `.github/`) para a branch `main`.
3. Em **Settings > Actions > General > Workflow permissions**, marque **Read and write permissions**.
4. Na aba **Actions**, rode manualmente "Generate Snake Animation" e "Generate Projects Panel" (Run workflow). Isso cria as branches `output` (cobrinha) e `projects` (painel).
5. Abra `github.com/Wedrock` e confira.

## Personalizar
- **Banner:** edite `INFO`, `CONTATOS` e `CODIGO` em `scripts/build_banner.py` e rode `python3 scripts/build_banner.py` (gera `dark.svg` e `light.svg`).
- **Projetos:** edite `projects.json`. Troque `NOME-DO-REPO` pelo nome real de cada repositório (precisa ser público). Para usar logo, coloque a imagem em `logos/` e preencha `"logo": "arquivo.png"`; sem logo, aparece um monograma.
