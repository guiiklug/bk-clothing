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

## Repositório no GitHub
- https://github.com/guiiklug/bk-clothing (privado). Colaborador: Carlaocod. `COMECE-AQUI.md` é o resumo para quem entra.
- Para o repositório não ficar pesado, ficam fora do Git (ver `.gitignore`): as 211 fotos originais do catálogo em `_coleta/img/` (só as 7 que os scripts usam foram mantidas; as outras se baixam de novo com `python _coleta/scrape.py`), `_coleta/ai/`, `_coleta/conf2/`, `_coleta/referencias/` e os vídeos de verão antes da troca de fundo. Esses arquivos continuam no computador do Guilherme.

## Vídeos de demonstração (pastas `video/` e `videos/`, 08/10/2026)
- Feitos com a skill `video-demonstracao`, igual à Perfect Hair: o script navega o site quadro a quadro, sem gravar a tela.
- `videos/apresentacao-completa.mp4` (deitado, 144 s): site2 no computador, no celular e o Instagram de verão, com cartelas. `apresentacao-site.mp4` (75 s) e `apresentacao-instagram.mp4` (em pé, 72 s) são os recortes. Os trechos brutos ficam na mesma pasta.
- `instagram/simulacao.html` é o perfil navegável para abrir ao vivo.
- Para regravar quando o site mudar: `python video/roteiro.py` (ou `computador`, `celular`, `instagram` para um trecho só). `video/preparar.py` refaz logo, capas e fonte.
- O botão do WhatsApp nunca é clicado no vídeo; o ponteiro chega nele e para.

## Drop de bermudas de basquete (pasta `drop-jordan/`, 10/10/2026)
- Feito com o Guilherme dentro da loja, a partir de 7 fotos de celular (em `orig/`), para mostrar ao Bruno como fica um drop novo. Três cores: preta, gelo e verde.
- `pack/` fotos padronizadas, `cut/` recortes, `feed/` 6 posts, `stories/` 2, `anuncio/` 3 formatos no estilo sóbrio, `video/bermuda-preta.mp4` (5 s). `python drop-jordan/gerar.py` refaz as artes; sem preço.
- Custo: cerca de 20 créditos (3 fotos, 1 quadro inicial e 1 vídeo). Foto de celular não tem endereço público, então sobe por `media_upload` e `curl -X PUT` com só o cabeçalho Content-Type (o urllib do Python dá 403).
- Pedido dele nesta rodada: ser fiel aos detalhes da peça. O que funcionou foi descrever no prompt cada detalhe (faixas do cós, losango lateral, cordão, logo nos dois lados) e conferir lado a lado com a foto original (`pack/_conf.jpg`).
- `criativo.py` grava `criativo/drop-bermudas.mp4`: vídeo de venda de 15 s por código, com corte no beat, sem crédito.
- `letras.py` gera `letras/A..E.jpg`: cinco letras para os criativos, cada uma em título e em marca d'água. **O Bruno escolheu a C, Big Shoulders Display 900.** O drop já está nela; site2 e artes antigas continuam em Archivo larga até ele pedir a troca.

## Drop de verão (pasta `drop-verao/`, 10/10/2026)
- Também feito com o Guilherme na loja, a partir de 18 fotos (`orig/`). Pedido: organizar por hierarquia de peça, falar de verão, posts e vídeos para o Instagram, post do grupo VIP, gastando o mínimo de crédito.
- Doze peças de quatro marcas, na ordem de importância que ele definiu: **Jordan** (bermuda em cinco cores, com mais espaço), **Nike** (bermuda cargo e short preto), **Brooksfield** (short de praia azul e verde-água), **Tommy Hilfiger** (short com listra lateral em três cores).
- Custo: 8,25 créditos. Só as três peças fotografadas em cima da mesa (cargo e as bermudas creme e menta) passaram pelo Higgsfield (`pack/`). As seis com foto limpa foram recortadas direto da foto real com `python recortar.py`, que também endireita a peça e tira a etiqueta de tamanho. Preta, gelo e verde vêm do drop anterior. Ele aprovou as fotos.
- **Duas versões de texto foram rejeitadas antes desta:** palavra solta gigante ("Praia", "Quadra", "Rua", depois "Basquete", "Listra") ele achou brega e grande demais. O que ficou, decidido por perguntas na loja, está no cabeçalho de `base.py`: frase normal na abertura de cada marca, peça grande com o nome pequeno no resto, bordão "Vista estilo, vista BK Clothing" na capa, "Seu verão começa na BK.", marcas escritas e com símbolo.
- `marcas.py` e a pasta `marcas/` guardam os símbolos (Jordan da Wikipédia em inglês, Nike e Tommy do Wikimedia Commons, Brooksfield enviado por ele). São marcas de terceiros, usadas só ao lado das peças delas.
- `python gerar.py` → `feed/` 18 posts (`grade.jpg` mostra o perfil), `stories/` 7, `whatsapp/` convite do grupo VIP e aviso do drop para postar dentro do grupo.
- `python video.py` → `videos/`: `verao.mp4` (campanha, 24 s, só com as peças tratadas: as fotos de celular da loja ele mandou tirar), `jordan.mp4`, `nike.mp4`, `brooksfield.mp4`, `tommy.mp4` e `grupo-vip.mp4`. `python video.py --roteiro verao` mostra um quadro por cena antes de gravar. Tudo por código; o beat é `beat.wav` (`python beat.py 34`, cópia do de `instagram/navegacao/`).
- `textos.md` tem legendas, ordem de postagem e as mensagens do WhatsApp.
- Grupo VIP: a vantagem combinada é ver e reservar antes, sem promessa de desconto. Tamanhos e preços não entraram em nada.
- Nos stories, as opções de "Qual você leva?" vão em letra grande entre dois fios. A caixa preta que imitava a figurinha de enquete ele não gostou.

## Vídeos do grupo, das básicas e dos conjuntos (pasta `drop-pecas/`, 10/10/2026)
- Pedido dele, ainda na loja: um vídeo para as pessoas entrarem no grupo VIP com as melhores peças, um apresentando as básicas e outro com os conjuntos e as bermudas. Tudo por código, Higgsfield só para tratar peça. Custo: **9,75 créditos**, só nas básicas.
- As fotos vieram em sete zips em `peças/` (11 de básicas, 21 de conjuntos e bermudas) e estão em `drop-pecas/orig/` como `b01..b11` e `c01..c21` (`python preparar.py`).
- `python recortar.py` recorta os conjuntos e as bermudas direto da foto (peça estendida no chão), em `cut/`. As básicas vieram como foto de modelo do fornecedor; a primeira versão do vídeo usou essas fotos e ele rejeitou ("não quero foto com modelo"). Agora o Higgsfield gera três imagens com várias cores cada (`pack/camisetas.png` com seis, `texturizadas.png` com quatro, `polos.png` com três polos e a camisa), em grade de células iguais, e o mesmo `recortar.py` separa cada célula num recorte. Pedir várias cores numa imagem só saiu por 9,75 créditos em vez de uns 38.
- `python video.py` → `videos/grupo.mp4` (22 s, mistura as peças do drop de verão, do site e as novas), `basicas.mp4` (23 s) e `conjuntos-bermudas.mp4` (22 s). O começo é lento de propósito: ele achou que passava rápido demais para ler, então cada frase fica dois tempos parada e as primeiras peças ficam dois tempos antes de os cortes acelerarem. O catálogo de peças com nome, marca e fundo está no começo do script; `--roteiro` mostra um quadro por cena.
- Marcas escritas só quando estão legíveis na peça ou na etiqueta: Nike, High, Thug Nine, Hurley, além das do site (Lacoste, Diesel). Dois conjuntos de jaqueta e short (`c01`, `c04`) e um par de shorts (`c09`) ficaram sem marca porque o patch não dá para ler. A marca das básicas ele não informou.
- Ficaram de fora: `c03` (foto de uma pessoa na rua, sem saber de quem é) e `c11` (boné).

## Pasta para postar (`sequencia-postagem/`, 10/10/2026)
- `python organizar.py` apaga e refaz a pasta: nove dias, um por subpasta, com as artes e os vídeos copiados e numerados na ordem de postar (abertura, Jordan em dois dias, Nike, Brooksfield, Tommy, básicas, conjuntos e bermudas, grupo VIP). `COMO-POSTAR.txt` repete a ordem com a legenda de cada item.
- São cópias, fora do git. Se uma arte ou um vídeo mudar, rodar o script de novo. A sequência e as legendas ficam na lista `SEQ` do script.
- Básicas e conjuntos têm só o vídeo (Reels): não há post de feed nem story dessas duas linhas.
