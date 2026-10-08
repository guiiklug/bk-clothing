# Hermes — três entregas para a apresentação da BK Clothing

Escrito em 06/10/2026 para rodar sozinho na hora do almoço, com o Sonnet 5.5. O Guilherme não vai estar por perto para responder, então o que estiver em dúvida você decide pelo caminho mais simples e anota no relatório final.

## Para que serve

O Guilherme (freelancer) montou uma demo de site novo para a BK Clothing, loja de moda masculina de Joinville, e vai apresentá-la ao dono, o Bruno, ainda esta semana. A meta é fechar o projeto por volta de R$ 4 mil. O site já está pronto e aprovado por ele. Faltam três peças de apoio para a conversa:

1. Um vídeo de navegação pelo site no computador.
2. Um vídeo de navegação pelo site no celular.
3. Uma apresentação de negócio, em versão clara e em versão escura.

Os vídeos são para mandar no WhatsApp antes da visita e para rodar no notebook se a internet falhar. A apresentação é o que ele abre na frente do Bruno.

Leia primeiro `C:\dev\bk clothing\LEIAME.md`. Ele descreve o site, os dados da loja, o que é provisório e o gosto do Guilherme. Este arquivo aqui só acrescenta o que é específico destas três entregas.

## Limites

- **Zero crédito do Higgsfield.** Nada aqui precisa de imagem ou vídeo gerado por IA. Os vídeos são gravações do site de verdade e a apresentação usa prints do site e as fotos que já existem.
- **Gasto de tokens enxuto.** O Guilherme tem limite de uso e já se assustou com isso antes. Trabalhe sozinho, sem abrir subagentes nem workflows. Faça o trabalho por script e confira o resultado por amostra: para um vídeo, extraia seis ou oito quadros com o ffmpeg, junte numa folha só e olhe essa folha, em vez de abrir dezenas de imagens. Para a apresentação, olhe as páginas em miniatura numa folha e só amplie a que parecer errada.
- **Não altere o site.** A pasta `site/` está aprovada. Se precisar de um estado especial para gravar (animações já concluídas, tema, sacola vazia), injete isso pelo script de gravação, sem editar os arquivos.
- **Nada sai do computador.** Não publique, não envie nada ao Bruno, e não clique no botão final "Fechar pedido no WhatsApp" nem em nenhum link `wa.me` ou do grupo VIP durante a gravação: eles abrem o WhatsApp real da loja. O vídeo pode mostrar a sacola com o botão, e para ali.
- **Não invente fatos.** Números, preços e achados vêm de `diagnostico-bk-clothing.md`, do LEIAME principal e de `site/proposta.html`. Sem depoimentos, sem promessa de resultado, sem estatística de mercado.

## O que já existe na máquina

- Windows 11, Node 24, Python 3.12 com Pillow, e ffmpeg 9 no PATH. Playwright não está instalado; instale dentro de `hermes/` (`npm i playwright` e `npx playwright install chromium`), não globalmente.
- O site é estático. Suba um servidor próprio numa porta que não seja a 4173, que pode estar em uso: `python -m http.server 4174 --directory "C:\dev\bk clothing\site"`. Encerre o servidor ao terminar.
- Fontes: Bebas Neue (títulos) e Jost (texto), do Google Fonts. O site as carrega pela internet; espere `document.fonts.ready` antes de gravar ou tirar print, senão o primeiro quadro sai com fonte errada.

## Coisas do site que afetam a gravação

- **Tema:** `localStorage.bk_tema` vale `light` ou `dark`. Sem valor, o site abre escuro. O botão de sol e lua no cabeçalho alterna.
- **Arte do hero:** `localStorage.bk_arte` vale `a`, `b`, `c` ou `d`. Use a `a`, que é a aprovada. Não abra a página com `?arte` na URL, porque isso mostra um seletor de teste no rodapé da tela.
- **Sacola:** fica em `localStorage.bk_sacola`. Comece com ela vazia.
- **Entrada das seções:** os blocos com a classe `.rv` aparecem com uma transição quando entram na tela. Com rolagem contínua e devagar isso fica bonito; com saltos, fica piscando.
- **Imagens preguiçosas:** as fotos têm `loading="lazy"`. Antes de gravar, percorra a página uma vez até o fim e volte ao topo, para tudo já estar carregado na tomada de verdade.
- **Produto:** abre por cima da página ao clicar num card. Precisa escolher um tamanho antes de "Adicionar à sacola", senão aparece o aviso "Escolha um tamanho". Fechar: botão ✕ ou Esc.
- **Peças boas para mostrar:** as da "Seleção BK" logo abaixo do hero, que têm foto padronizada. Jaqueta bege `1914786`, moletom `1910184`, calça cargo `1679459`, mochila `1849734`.

## Entrega 1 — vídeo de navegação no computador

**Resultado esperado:** `entregas/bk-site-desktop.mp4`, 1920×1080, H.264, sem áudio, entre 40 e 60 segundos, abaixo de 16 MB para passar no WhatsApp.

O que "fluido" quer dizer aqui: a rolagem tem velocidade constante com aceleração e freio suaves, sem saltos; cada parada dura o bastante para ler o título da seção; o cursor aparece e se move em curva suave até o que vai clicar; nada pisca, nada carrega na frente da câmera.

Roteiro sugerido, no tema escuro:

1. Hero parado por uns três segundos, com os colchetes da logo se desenhando.
2. Rolagem até a Seleção BK; passa o cursor por dois cards (a foto troca para a foto real da peça).
3. Clica na jaqueta bege, o produto abre; rola um pouco as fotos; escolhe o tamanho M; adiciona à sacola.
4. A sacola abre com o item e o total. Segura dois segundos e fecha.
5. Rolagem pelas categorias e pelo lookbook; clica num filtro do lookbook (por exemplo "Conjuntos").
6. Clica no botão de tema: o site passa para o claro. Segura um instante.
7. Rolagem até "Visite a loja" e termina no rodapé "Vista BK."

O difícil é a qualidade. A gravação nativa do Playwright (`recordVideo`) é a mais simples e respeita as transições do site, mas sai com bitrate baixo e pode ficar lavada em 1080p. Comece por ela, gravando com o viewport em 1920×1080, e julgue por quadros extraídos. Se o texto pequeno estiver borrado, a alternativa é capturar quadro a quadro com `page.screenshot` enquanto o script controla a posição da rolagem, e montar a 30 ou 60 fps no ffmpeg. Fica nítido, mas as transições do site correm em tempo real e não no tempo do vídeo, então nesse modo deixe as seções já visíveis (classe `in` em todos os `.rv`) e use a gravação nativa só nos trechos de interação (abrir produto, sacola, troca de tema). Juntar os dois tipos de trecho no ffmpeg é aceitável.

O Playwright não grava o cursor. Injete um elemento que faz o papel dele (um círculo pequeno, na cor do texto, com leve transparência) e mova-o junto com o mouse real.

## Entrega 2 — vídeo de navegação no celular

**Resultado esperado:** `entregas/bk-site-celular.mp4`, vertical, 1080×1920, H.264, sem áudio, entre 30 e 45 segundos, abaixo de 16 MB.

Use um viewport de 360×640 com `deviceScaleFactor` 3, que dá exatamente 1080×1920, com `isMobile` e `hasTouch` ligados e user agent de celular. O site foi testado em 375 px; confira se em 360 não aparece rolagem lateral e, se aparecer, use 375×667 e ajuste a saída.

Sem moldura de aparelho: tela cheia, limpa. No lugar do cursor, um ponto que aparece e some onde o dedo toca.

Roteiro sugerido, no tema escuro: hero com a logo, rolagem pela Seleção BK, toca numa peça, desliza as fotos para o lado, escolhe tamanho, adiciona à sacola, fecha; abre o menu (três traços) e fecha; rolagem pelo lookbook; termina em "Visite a loja". Se sobrar tempo, encerre com a página `links.html`, que é a que vai na bio do Instagram.

## Entrega 3 — apresentação de negócio

O pedido do Guilherme, nas palavras dele: "apresentação de negócio clean e bonita, pode ser em PDF ou PowerPoint, vou querer uma opção clara e escura, clean, tipografia bonita, bem organizada, imagens e caixas de textos enquadradas".

**Resultado esperado:** `entregas/bk-apresentacao-escura.pdf` e `entregas/bk-apresentacao-clara.pdf`, formato 16:9, de 10 a 12 páginas, com o mesmo conteúdo e só as cores trocadas. Guarde também a fonte em HTML na pasta `apresentacao/`, para ele poder corrigir um texto e exportar de novo.

Recomendo PDF feito a partir de HTML e exportado com o `page.pdf` do Playwright (página de 1920×1080 px, fundo impresso, uma seção por página). É o mesmo ferramental dos vídeos, garante as fontes certas e deixa as duas versões idênticas. Um tema por variável CSS resolve a versão clara e a escura com um arquivo só.

**Identidade:** a mesma do site, para parecer uma coisa só. Preto `#0b0b0b`, off-white `#f3f0ea`, cinza de apoio `#8f8a80` no escuro e `#666056` no claro, acento areia `#c8b89a` no escuro e `#75654a` no claro, linhas finas a 14% de opacidade. Bebas Neue em caixa alta nos títulos, Jost 300 e 400 no texto. A logo é desenhada em código (colchetes, "BK" fino, "CLOTHING" em Bebas); copie o desenho de `site/js/home.js`, arte `a`.

**O que "enquadrado" significa:** uma grade fixa com as mesmas margens em todas as páginas; toda imagem dentro de uma moldura de proporção definida, cortada com `object-fit`, alinhada à grade; todo bloco de texto com largura máxima e alinhado às mesmas linhas. Nenhum elemento solto ou torto, nada encostando na borda, nenhum texto cortado ou saindo da caixa. Muito respiro, uma ideia por página, numeração discreta. Sem ícones de biblioteca, sem gradiente colorido, sem cantos arredondados genéricos, sem emoji.

**Estrutura sugerida:**

1. Capa: logo, "Proposta de novo site", Joinville, outubro de 2026.
2. Ponto de partida: a loja já vende bem pelo WhatsApp e pelo grupo VIP; o digital ainda não está à altura.
3. O que encontrei: quatro ou cinco achados do diagnóstico, cada um com a consequência prática.
4. Hoje: print do site atual (bkclothing.com.br) enquadrado.
5. O novo site: print da home nova, no computador e no celular lado a lado.
6. Fotos padronizadas: antes e depois de quatro a seis peças. As originais estão em `_coleta/img/` e as novas em `_coleta/piloto/`.
7. Como o cliente compra: catálogo, sacola, pedido pronto no WhatsApp, com prints.
8. O que mais vem junto: página de links própria, lookbook, tema claro e escuro, políticas de troca e envio.
9. O que está incluso: a lista do escopo.
10. Investimento e prazo.
11. Próximo passo.

Texto em português do Brasil, direto, de parceiro para dono de loja, tratando por "você". Frases curtas. Sem tom de crítica ao que o Bruno construiu, sem jargão de marketing e sem travessão longo. O texto de `site/proposta.html` já está nesse tom e pode ser reaproveitado.

**Prints:** tire com o Playwright, do site local, depois de as fontes carregarem. Para o site atual, um print de bkclothing.com.br; se a página não carregar, use `_coleta/home.html` como referência do que existe e diga isso no relatório.

**Dois pontos que são do Guilherme e não seus:** os valores (hoje R$ 3.990 pelo site, R$ 490 pelo perfil no Google e mensal a partir de R$ 690) foram sugeridos e ele ainda não confirmou; e o WhatsApp dele ainda não foi informado. Use os valores como estão e deixe o contato como um campo fácil de achar no HTML, com o texto `SEU_NUMERO`. Liste os dois no relatório como pendência.

## Como entregar

Tudo dentro de `C:\dev\bk clothing\hermes\`:

- `entregas/` com os dois vídeos e os dois PDFs.
- `apresentacao/` com o HTML e as imagens usadas.
- `scripts/` com os scripts de gravação e de exportação, para poder regravar se o site mudar.
- `RELATORIO.md`, curto: o que ficou pronto, o que você conferiu e como, o que não deu certo, o que decidiu sozinho e as pendências que dependem do Guilherme. Se alguma entrega ficou pela metade, diga isso com todas as letras em vez de entregar algo que parece pronto e não está.

Considere pronto quando os dois vídeos tocam do começo ao fim sem quadro quebrado, sem fonte errada e sem seletor de teste na tela; quando os dois PDFs abrem com o número certo de páginas e nenhuma tem texto cortado ou imagem fora da moldura; e quando o relatório existe. Se o tempo ou o orçamento apertar, a ordem de prioridade é: apresentação, vídeo no computador, vídeo no celular.
