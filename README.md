# Raquel Rocha Cerâmica: demonstração

Demonstração de site com reservas para o ateliê da Raquel Rocha ([@rrochaceramica](https://instagram.com/rrochaceramica)), oficinas de cerâmica em Cunha, SP. Feita pela Studio Digi.

No ar: https://dsalessales.github.io/ceramica/

| Página | Endereço | O que mostra |
|---|---|---|
| Home | `/ceramica/` | O ateliê, as quatro oficinas (Casal, Família, Infantil, Noturna), próximas vagas, perguntas frequentes |
| Reservas | `/ceramica/reservar/` | Escolha da oficina → dia → horário e pessoas → dados → sinal de 50% no Pix → confirmação. Também vale-presente (`#presente`) e turma fechada (`#grupo`) |
| Painel | `/ceramica/painel/` | O que a Raquel vê: reservas do dia, agenda da semana com bloqueios, preços e vagas por oficina, vales-presente |

É uma demonstração: o Pix é simulado (botão "Simular pagamento"), os preços e depoimentos são de exemplo, e as reservas ficam guardadas só no navegador de quem testa. Abra as reservas e o painel em duas abas: a reserva nova aparece no painel na hora.

## Regras do ateliê usadas na demo

- Oficinas de 1h30, início entre 10h e 17h, de 30 em 30 minutos, uma turma por vez.
- Fechado às segundas.
- Sinal de 50% no Pix, código válido por 15 minutos.
- Remarcação grátis até 48h antes. Vale-presente válido por 6 meses.

Tudo isso fica no objeto `CONFIG` de `demo/demo.js`, junto com os preços de exemplo de cada oficina.

## Rodar localmente

```bash
node server.js
```

Abra http://localhost:8080/ceramica/. Os scripts precisam de servidor: abrir o `index.html` com duplo clique não funciona.

## Estrutura

- `index.html`: a home (HTML + CSS exportados do Framer, com os textos da Raquel). Um script no fim do arquivo leva todo link interno para a página de reservas.
- `reservar/index.html`, `painel/index.html`: páginas da demo, em HTML/CSS/JS puro.
- `demo/demo.css`, `demo/demo.js`: visual e lógica compartilhados (agenda, vagas, vales, Pix simulado).
- `assets/framerusercontent.com/`: imagens, vídeo, fontes e scripts do Framer.
- `tools/raquel_textos.py`: aplica os textos da Raquel por cima do template (pode rodar de novo sem estragar nada).
- `tools/trocar_fotos.py`: troca as fotos do template pelas fotos do ateliê.

Todos os caminhos começam com `/ceramica/`, o endereço do site no GitHub Pages.

## Trocar as fotos

1. Crie a pasta `fotos/` e coloque as imagens com estes nomes: `raquel.jpg`, `casal.jpg`, `familia.jpg`, `infantil.jpg`, `noturna.jpg`, `atelie.jpg` e `insta-1.jpg` a `insta-6.jpg`.
2. Rode `python3 tools/trocar_fotos.py` (precisa do Pillow: `pip install pillow`).

Cada foto é recortada no formato certo e salva por cima da imagem do template, com o mesmo nome.

## Trocar um texto

O texto aparece no `index.html` e também nos `.mjs`, porque o Framer recria a página com JavaScript. Altere as duas ocorrências, ou acrescente a troca em `tools/raquel_textos.py` e rode o script.
