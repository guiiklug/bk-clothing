# BK Clothing — site novo (demonstração)

Passagem de bastão. Quem assumir (Hermes) começa por aqui. Atualizado em 06/10/2026.

## Contexto
- **Cliente em prospecção:** BK Clothing, moda masculina multimarca em Joinville/SC. Dono: Bruno.
- **Quem vende:** Guilherme (freelancer). Meta: fechar o site por volta de R$ 4 mil.
- **Situação:** demo pronta. Guilherme vai apresentar sem compromisso e visitar a loja esta semana. Nada foi publicado na internet e nada foi enviado ao Bruno ainda.
- **Se fechar:** completar as fotos das 111 peças restantes, trocar o que é provisório pelos dados reais do Bruno e publicar em bkclothing.com.br.
- Diagnóstico da presença digital atual: `diagnostico-bk-clothing.md`. Pedido antigo de segunda análise: `prompt-hermes.md`.

## Dados da loja
- Endereço: Rua Santa Catarina, 2348, Floresta, Joinville/SC (o diagnóstico alerta que o número é o mesmo de um coworking; confirmar com o Bruno se há loja aberta ao público ali)
- WhatsApp: (47) 98820-4407 → `5547988204407`
- Grupo VIP: https://chat.whatsapp.com/FCX9FvsBWBeACbsrjiNW62
- Instagram: @bkclothiing (com dois "i") · Linktree atual: linktr.ee/bkclothiing · Site atual: bkclothing.com.br
- Slogan: "vista estilo, vista bk clothing"

## Como abrir
- Duplo clique em `site/index.html`, ou
- `python -m http.server 4173 --directory site` e abrir http://localhost:4173
- O site é HTML, CSS e JS puros, sem build e sem dependência além das fontes do Google (Bebas Neue e Jost).

## O que existe em `site/`
- `index.html` — home, nesta ordem: hero com arte da logo, faixa de categorias, **Seleção BK** (16 peças com foto padronizada), categorias, lookbook Inverno 26 por sessão, como comprar, a loja, grupo VIP, dúvidas, rodapé
- `catalogo.html` — os 135 produtos, com filtro por categoria e marca, busca e ordenação. As 24 peças com foto limpa aparecem primeiro
- produto abre por cima da página (`#p=ID`): fotos, cor, tamanhos, guia de medidas, peças parecidas
- sacola lateral que monta o pedido e abre o WhatsApp da loja com a mensagem pronta (peça, cor, tamanho, total)
- `links.html` — página de links para a bio do Instagram, no lugar do Linktree
- `proposta.html` — proposta comercial para o Bruno. **Pendente:** trocar `SEU_NUMERO` pelo WhatsApp do Guilherme (aparece uma vez) e conferir os valores nos trechos `.preco` (hoje R$ 3.990, Google R$ 490, mensal a partir de R$ 690; fui eu que sugeri)
- `js/produtos.js` — dados dos produtos (gerado por `_coleta/build_data.py`) · `js/std.js` — lista das peças com foto padronizada · `js/app.js` — cabeçalho, tema, sacola, produto · `js/home.js` — home e artes da logo
- `css/style.css` — um arquivo só

## Decisões e gostos do Guilherme (respeitar)
- **Sem cara de IA.** Ele mandou tirar o vídeo e o modelo de IA do hero. O hero hoje é a logo desenhada em código.
- **Sem gíria nos títulos.** "Escolha seu corre" foi rejeitado; os títulos são neutros ("Compre por categoria", "Visite a loja", "Seleção BK").
- **Clean e premium:** preto, off-white e um tom areia de apoio; muito respiro; títulos grandes em caixa alta.
- **Fotos de produto no padrão packshot** (peça de frente, fundo cinza claro, sombra leve). Ele aprovou o resultado e quis essas peças logo abaixo do hero.
- **Gasto controlado:** avisar o custo antes de gastar créditos do Higgsfield ou de abrir vários agentes. Ele não quer gastar crédito antes do Bruno fechar.

## Hero: quatro artes da logo
- Abrir `index.html?arte=a` mostra um seletor A, B, C, D no rodapé da tela; a escolha fica salva no navegador. Sem `?arte` o seletor não aparece.
- A (padrão): logo inteira com colchetes · B: padrão de mini-logos · C: foto da parede da loja dentro dos colchetes · D: "BK" gigante em contorno
- Guilherme viu a A e gostou; não disse se quer manter outra opção.

## Tema claro e escuro
- Botão de sol/lua no cabeçalho e na página de links; a escolha fica salva. O escuro é o padrão. A proposta só existe no escuro.
- Tokens em `css/style.css`: `--bg`, `--fg`, `--mute`, `--accent`, `--ph`, `--panel`, `--line`. A classe `.alt` é a superfície alternada. Os componentes só leem esses nomes; a única cor fixa é o texto sobre foto, sempre claro.
- Os tamanhos estão em `rem`, e a base cresce em telas acima de 1500 px de largura (regra no `html`), para o layout manter a proporção em monitores muito largos. Não voltar para `px`.

## Fotos padronizadas
- 20 peças têm foto nova em `site/img/std/`; outras 4 já tinham foto limpa. Faltam **111 peças**.
- No produto, a foto padrão vem primeiro e as fotos reais originais seguem depois.
- **Custo medido:** 2,75 créditos por foto no Higgsfield (`gpt_image_2_5`, quality high, resolution 2k, 4:5). As 111 restantes dão cerca de 305 créditos. **Só rodar se o Bruno fechar e o Guilherme autorizar.** Até aqui foram gastos cerca de 77 créditos na demo inteira.
- **Como fazer mais:** importar a foto original por URL com `media_import_url` (as URLs estão em `_coleta/produtos.json`), gerar com a foto como `image_references`, pôr o id e o trecho da URL do resultado em `_coleta/baixa_std.py` e rodar esse script e depois `_coleta/patch_std.py`.
- **Prompt que funcionou:** "Turn this exact [peça] from the reference photo into a clean e-commerce catalog packshot. Keep the garment itself unchanged: same colours, fabric, cut, trims, prints and logo placement exactly as in the reference; do not add pockets, seams, logos or text that are not there. Show it front-facing, laid perfectly flat and symmetrical, fully visible and centred with even margin. Seamless plain light grey studio background (#ececec), soft even lighting, faint soft shadow underneath. Remove floor, hangers, hang tags, people and props." Para foto de lote, pedir uma cor só; para peça clara, fundo `#e6e6e6`.
- **Conferir sempre:** a IA redesenha a peça e pode inventar detalhe. Folhas de antes e depois em `_coleta/piloto/conferencia_*.jpg`. Pontos em aberto para o Bruno validar: bolsos laterais nas três jaquetas bomber e a cor da mochila (original azul-marinho, a nova saiu quase preta).

## O que é provisório na demo (trocar pelos dados do Bruno)
- Tamanhos (P/M/G/GG em tudo) e a tabela do guia de medidas são de exemplo
- Textos de troca (7 dias), envio e pagamento são padrão, não a regra dele
- Cores foram preenchidas olhando as fotos; "Várias cores" onde a foto mostra um lote
- Nomes repetidos (17 "Bermuda Nike"): falta nomear por modelo
- Horário de funcionamento não aparece porque não foi encontrado
- Duas fotos do lookbook são de IA com modelo (`img/look1.webp`, `img/look2.webp`). Guilherme não respondeu se quer tirar; pelo gosto dele, o provável é tirar
- As fotos do Instagram no lookbook estão em 640 px (o máximo sem login); pedir os originais
- Falta a seção "Quem usa" (prova social): depende das fotos dos destaques do Instagram
- `og:image` aponta para https://bkclothing.com.br/img/og.jpg e só funciona depois de publicar no domínio
- O catálogo é revenda de marcas de terceiros; ver o alerta sobre anúncios pagos no diagnóstico

## Pasta `_coleta/` (material bruto e scripts)
- `produtos.json` — os 135 produtos como estão no site atual (id, nome, preço, URLs das fotos, categoria, descrição)
- `img/` — 211 fotos originais · `logo.jpg` · `capa.jpg` (parede da loja)
- `insta/` — 12 posts do feed · `linktree.html` e `page*.html` — páginas baixadas do site e do Linktree atuais
- `ai/` — fotos editoriais e o vídeo de hero gerados no Higgsfield (o vídeo e a foto do hero não são mais usados)
- `piloto/` — as 20 fotos padronizadas em PNG original e as folhas de conferência
- `scrape.py` — refaz a coleta do site atual · `build_data.py` — gera `site/js/produtos.js` e as imagens otimizadas (pode rodar de novo)
- `baixa_std.py` e `patch_std.py` — baixam e ligam as fotos padronizadas (podem rodar de novo)
- `patch_tema.py` — foi aplicado uma vez e **não deve rodar de novo** (falha de propósito se o site já estiver alterado)

## Próximos passos
1. Guilherme: trocar `SEU_NUMERO` na proposta e decidir os valores.
2. Publicar a demo num endereço temporário para o Bruno abrir no celular (Guilherme ainda não autorizou publicar).
3. Depois da conversa com o Bruno: tamanhos reais, regras de troca e envio, horário, fotos originais e fotos de clientes.
4. Se fechar: padronizar as 111 fotos restantes, renomear produtos, apontar o domínio e corrigir os links quebrados do site atual.

## Aplicativo de estoque e vendas (pasta `app/`, 07/10/2026)
- Demonstração de um aplicativo de celular para o Bruno controlar estoque e vendas ("BK Gestão"), feita para a reunião. Usa as peças, preços e fotos deste catálogo; quantidades, custos, clientes e vendas são de exemplo.
- Tudo o que importa está em `app/LEIAME.md`: como abrir, o que é real e o que é exemplo, vídeo de navegação (`app/video/`), telas (`app/telas/`) e o que falta para virar produto.
- Não foi publicado. O preço desse serviço ainda não foi definido e não está na proposta.

## Instagram (pasta `instagram/`, versão 2 de 07/10/2026)
- `instagram/index.html` — diagnóstico do perfil @bkclothiing e proposta de feed, vídeos, destaques e stories. Abre com duplo clique.
- **Versão 1 foi rejeitada pelo Guilherme**: três colunas fixas com faixa de nome e preço em toda foto. Ele achou engessado e clichê e mandou tirar o preço das artes.
- **Versão 2 (atual):** uma ideia por linha da grade, sem preço e sem etiqueta. Linha de cor (a jaqueta em close nas três cores com o nome da cor atrás), linha de vídeo, detalhes de tecido, foto real no corpo, loja.
- Artes exportadas: `feed/` (18 posts 1080x1350), `carrossel/` (4), `destaques/` (6 capas), `stories/` (6 modelos 1080x1920), `videos/` (3 vídeos verticais de 5 s: bomber, mochila, arara), `apresentacao/` (perfil hoje, perfil proposto, seções de 9).
- Para trocar texto ou peça: editar as listas no topo de `gerar.py`, rodar `python gerar.py` e depois `python exportar.py`. Custo zero.
- Vídeos: quadro inicial com `gpt_image_2_5` 9:16 a partir da foto padronizada (2,75 créditos) e animação no `kling3_0` modo pro, 5 s, sem som. Cerca de 34 créditos pelos três, de um teto de 70 dado pelo Guilherme. Originais em `instagram/raw/`.
- Base do diagnóstico: 60 posts mais recentes vistos com login, destaques abertos, Guadalupe Store e Cartel 011 como referência. Sem acesso às estatísticas do perfil.
- As fotos com modelo em `instagram/raw/` vieram do próprio feed da BK (campanha da Comp Supply), em 635 px; para publicar, usar os arquivos originais do Bruno.

### Instagram, segunda identidade: Verão 27 (pasta `instagram/verao/`)
- O Guilherme aprovou a versão 2 do feed de inverno ("ficou ótimo") e pediu a mesma qualidade com outras peças e outra estética.
- `instagram/verao/index.html` — apresentação da identidade de verão, com o perfil ao lado do de inverno.
- Estética: blocos de cor tirados das peças (vermelho #e2372b, azul #a9d8e6, areia #d9cdb6, preto, off-white), peça recortada em diagonal com sombra, palavra enorme atrás, tipografia Archivo larga e pesada. A linha do topo é a palavra VERÃO atravessando três posts.
- `recortar.py` recorta as peças com rembg (pasta `cut/`); `gerar.py` monta e exporta tudo (`feed/` 18 posts, `stories/` 4, `destaques/` 6, `apresentacao/perfil-verao.jpg`). Custo zero.
- Dois vídeos em `videos/` (camiseta sobre vermelho, conjunto sobre azul), mesma receita dos de inverno. Cerca de 23 créditos; somados aos de inverno, perto de 58 dos 70 autorizados.

### Vídeo de navegação no Instagram (pasta `instagram/navegacao/`)
- `navegacao-verao.mp4` e `navegacao-inverno.mp4`: 1080x1920, 26 s, simulando o celular (rolagem, toque em foto com curtida e deslize, dois vídeos em tela cheia, cartela final).
- `app.html` é o perfil simulado; `gravar.py verao|inverno` grava quadro a quadro com o Playwright e junta com `beat.wav`; `beat.py` sintetiza o beat (trap, 140 BPM) por código, sem sample. Custo zero.
- Os tempos de cada ação ficam no objeto `T` dentro de `app.html`; o que é aberto em cada identidade fica em `CFGS`.

### Retorno do Bruno sobre as identidades (07/10/2026, por WhatsApp com o Guilherme)
- Sobre a versão com cor: "não gostei muito", "poderia até ser com cor, porém não achei que azul e vermelho fazem parte da identidade". Pediu "um azulzinho mais esbranquiçado". Ele respondeu "gostei mais dessa pegada" a um dos vídeos, sem ficar claro qual; o Guilherme perguntou se o layout das peças agradou e a resposta não apareceu na conversa que eu vi.
- Verão 27 foi refeito na paleta dele: azul esbranquiçado em dois tons (#dce8ef e #c5d6e1), areia clara (#e6dfd0), preto e off-white. Sem vermelho. O layout não mudou.
- Fundo dos vídeos trocado por código, sem crédito: `verao/recolorir.py` (recorte quadro a quadro, usado na camiseta) e curva de cor no ffmpeg (usada no conjunto, porque o recorte confundia a listra azul clara com o fundo). Originais guardados em `verao/raw/*-cor-antiga.mp4`.

## Site versão 2 (pasta `site2/`, feito em 07/10/2026)
- Refeito do zero na paleta que o Bruno aprovou para o Instagram: azul esbranquiçado (#dce8ef e #c5d6e1), areia clara (#e6dfd0), preto e off-white. Letra Archivo larga e pesada nos títulos, Archivo normal no texto. O site anterior continua intacto em `site/`.
- Home: abertura em mosaico de blocos de cor com peças recortadas (a peça acompanha o mouse), faixa de avisos, Seleção (16 peças recortadas sobre cor), categorias em lista grande com a peça aparecendo no hover, três vídeos, fotos no corpo, como comprar, loja, grupo VIP, dúvidas.
- Catálogo, produto, sacola e pedido no WhatsApp são os mesmos do site 1, com o visual novo. Peça com recorte aparece solta sobre bloco de cor; as outras seguem com a foto.
- Tema claro é o padrão; o botão de sol/lua troca para o escuro (chave `bk_tema2` no navegador).
- Recortes em `site2/img/cut/` (24 peças, lista em `site2/js/cut.js`), feitos por `_coleta/recortar_site.py` com rembg. Para recortar mais peças, elas precisam primeiro da foto padronizada.
- Referência usada antes de desenhar: primeira tela de Guadalupe, Your ID, OStore, Kith, Aimé Leon Dore, Stüssy, Pace e Piet (`_coleta/referencias/_folha.jpg`). O padrão que se repete: cabeçalho fino, abertura com imagem grande e poucas palavras, e logo abaixo uma grade uniforme de produto em fundo limpo.
- Conferência por prints: `python _coleta/confere_site2.py` (várias larguras, seções, catálogo, produto, tema escuro, celular). Preview: servidor `bk-site2` no `launch.json` de `C:\devgui16.09`.
- **Atualização de 08/10/2026 (ideias da Maze, a pedido do Guilherme):** barra preta de avisos fixa no topo (só fatos da loja: envio, pagamento, retirada, grupo VIP; sem frete grátis, cupom ou parcelamento, que dependem do Bruno); primeiro item do menu em destaque ("Drops"); categorias viraram grade 3x3 de peças recortadas ao lado de um banner com a palavra em pé; quatro vitrines por categoria (Jaquetas, Camisetas, Bermudas, Acessórios) com banner lateral e carrossel com setas. Saíram a faixa rolante, a lista grande de categorias e a seção "Em movimento" (os vídeos foram para os banners).
- Cuidado: a classe `.ft` é do rodapé. Não usar em imagem (usei `fo` nos banners por causa disso).
- Opções de letra para os títulos em `_coleta/letras/letras.jpg`; o Guilherme ainda não escolheu, o site segue com Archivo larga.

## Criativos de exemplo para Google Ads (pasta `anuncios/`, versão 2 de 08/10/2026)
- **Versão 1 rejeitada pelo Guilherme como "brega"** (palavra gigante, botão preto, etiqueta pendurada, fundo colorido). Guardada em `anuncios/_v1-rejeitada/`.
- **Versão 2 (atual), sóbria:** uma peça ou uma foto, muito espaço vazio, letra pequena (Jost), sem botão. Quatro conceitos em paisagem 1200x628, quadrado 1200x1200 e retrato 960x1200: `1-peca` (jaqueta sozinha), `2-cores` (as três cores em fila com o nome), `3-corpo` (foto real com modelo), `4-loja` (parede da loja com endereço). `1-peca/animado.mp4` é o primeiro em vídeo de 6 s, sem som.
- `anuncios/index.html` apresenta tudo; `gerar.py` monta, exporta e grava. Custo zero, sem imagem gerada.
- Pendências antes de anunciar de verdade: o Google reprova anúncio com marca registrada de terceiros (ver alerta no diagnóstico) e exige página de destino no ar.

## Explorações de logo (pasta `logo/`, 08/10/2026)
- O Guilherme pediu para "brincar com a logo". `logo/logos.jpg` tem a logo atual e oito direções desenhadas em SVG por código (`logo/gerar.py`): A Espelho (B de costas para o K na mesma haste), B Vertical, C Bloco, D Selo, E Corte, F Alta, G Sobreposta, H Clássica. Uma imagem por opção em `logo/opcoes/`.
- É estudo, não proposta fechada: a loja tem letreiro físico com a logo atual, e trocar logo é decisão do Bruno. Nenhuma foi aplicada ao site.

## Grupo VIP do WhatsApp (pasta `whatsapp/`, 10/10/2026)
- O grupo tem 182 membros, só admin posta e nenhuma mídia guardada; foto é a logo em fundo branco e a descrição em caixa alta.
- `gerar.py` monta, na identidade de verão (azul esbranquiçado, areia, preto, off-white, Archivo), quatro opções de foto do grupo (`foto-grupo/`, já pensadas para o corte em círculo), dez modelos de post 1080x1350 (`posts/`: bem-vindo, como funciona, chegou hoje, últimas peças, qual leva, nova coleção, só no grupo, quem usa, loja, todo Brasil) e `index.html` para apresentar. Custo zero.
- `descricao.txt` é a descrição nova do grupo. `ideias.md` tem o diagnóstico do grupo, o que trocar agora, o calendário semanal de posts, regras de uso e como crescer de 181 para 500.
- Recomendação: foto `A-azul`, fixar `02-como-funciona`, manter o grupo só para admins.

## Repositório no GitHub
- https://github.com/guiiklug/bk-clothing (privado). Colaborador: Carlaocod. `COMECE-AQUI.md` é o resumo para quem entra.
- Para o repositório não ficar pesado, ficam fora do Git (ver `.gitignore`): as 211 fotos originais do catálogo em `_coleta/img/` (só as 7 que os scripts usam foram mantidas; as outras se baixam de novo com `python _coleta/scrape.py`), `_coleta/ai/`, `_coleta/conf2/`, `_coleta/referencias/` e os vídeos de verão antes da troca de fundo. Esses arquivos continuam no computador do Guilherme.
