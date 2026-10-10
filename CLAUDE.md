# BK Clothing — regras para qualquer sessão do Claude neste repositório

Duas pessoas editam este repositório, cada uma com o seu Claude: o Guilherme e o Carlos.
Leia primeiro o `LEIAME.md` (o que existe, como se refaz e os gostos do Guilherme) e o `RELATORIO.md` (o que mudou por último).

## Antes de começar
- Puxar o que o outro enviou: `git pull --rebase`.

## Ao terminar (regra do Guilherme, 10/10/2026)
Toda sessão que mexeu em arquivo termina com o GitHub atualizado e com o relatório escrito, **sem a pessoa precisar pedir**. O outro precisa conseguir ver tudo o que foi mexido.

1. Acrescentar no topo do `RELATORIO.md` uma entrada com a data e quem pediu: o que foi feito, em que pastas, o que o cliente ou o Guilherme decidiu, quanto custou no Higgsfield e o que ficou pendente. Escrever para quem não viu a conversa.
2. Atualizar o `LEIAME.md` se mudou o que existe ou o jeito de refazer.
3. Conferir o que vai subir (`git status`), depois `git add -A`, commit em português dizendo o que mudou, `git pull --rebase` e `git push` no ramo `main`.
4. Se o envio falhar ou der conflito, avisar a pessoa. Nunca forçar o envio por cima do trabalho do outro.

A sessão pode ser fechada a qualquer momento. Por isso, fazer os quatro passos ao fim de cada entrega grande, não só na despedida.

## O que não vai para o GitHub
O repositório é público.
- Fotos brutas da loja e do fornecedor (`peças/`, `drop-*/orig/`): têm pessoas aparecendo. Os recortes prontos (`cut/`, `pack/`) vão.
- Chave, token, senha e endereço assinado de envio. Conferir antes de cada commit.
- `sequencia-postagem/`: é cópia, refaz com `python organizar.py`.
- Sobras de gravação (quadros, páginas temporárias). O `.gitignore` já cobre.

## Como o Guilherme gosta do trabalho
Está no `LEIAME.md` e, para os criativos, no começo de `drop-verao/base.py`. Em resumo: sem cara de IA, peça real como maior elemento, frase normal no lugar de palavra solta gigante, sem preço nas artes, avisar o custo antes de gastar crédito.
