# Cerâmica — demonstrativo da home

Cópia da página inicial de [handsel.framer.website](https://handsel.framer.website/), para servir de base para ajustes.

Só a home foi copiada. Os links do menu e dos cards apontam para páginas que ainda não existem neste repositório.

## Rodar localmente

```bash
node server.js
```

Abra http://localhost:8080/ceramica/

Os scripts do Framer (animações, menu, carrosséis) precisam de um servidor: abrir o `index.html` com duplo clique não funciona.

## Estrutura

- `index.html`: a página, já renderizada (HTML + CSS do Framer)
- `assets/framerusercontent.com/images/`: imagens, convertidas para WebP com até 1600 px
- `assets/framerusercontent.com/assets/`: vídeo do topo e fontes
- `assets/framerusercontent.com/sites/…/*.mjs`: scripts do Framer, que recriam a página e fazem as animações
- `assets/fonts.gstatic.com/`: fontes do Google
- `server.js`: servidor local sem dependências

Todos os caminhos começam com `/ceramica/`, que é o endereço do site no GitHub Pages (`dsalessales.github.io/ceramica`).

## Como fazer ajustes

- **Trocar uma imagem:** substitua o arquivo em `assets/framerusercontent.com/images/` mantendo o mesmo nome.
- **Trocar um texto:** o texto aparece no `index.html` e também nos `.mjs`, porque o Framer recria a página com JavaScript. Use a busca do editor na pasta toda e altere todas as ocorrências.
- **Cores e fontes:** ficam nas variáveis CSS do `<head>` do `index.html` (`--token-…`).
