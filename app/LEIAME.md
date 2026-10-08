# BK Gestão — aplicativo de estoque e vendas (demonstração)

Feito em 07/10/2026 para a reunião com o Bruno. Objetivo: mostrar que dá para tirar das costas dele o controle de estoque e de vendas, num aplicativo que fica no celular. Ainda não sabemos a rotina exata dele; por isso é o padrão do mercado, com as peças da própria BK.

## Como abrir
- No computador: `python -m http.server 4178 --directory "C:/dev/bk clothing/app"` e abrir http://localhost:4178 (no preview do Claude é o servidor `bk-app`). Em tela larga o aplicativo aparece numa coluna do tamanho de um telefone.
- No celular, na mesma rede Wi-Fi do computador: com o servidor acima ligado, abrir `http://IP-DO-COMPUTADOR:4178` (em 07/10 o IP era 192.168.15.8). O Windows pode perguntar se libera o acesso na primeira vez.
- Pelo Claude, em qualquer aparelho: https://claude.ai/artifact/8qPQ1vHD2AZf35TjdkG9k2 (artefato privado, publicado em 08/10/2026; só abre logado na conta do Guilherme). A página publicada é `artefato.html`, que usa os mesmos `css/`, `js/` e `img/`. Para atualizar, publicar de novo esse arquivo com os arquivos que mudaram. Conferir antes com `python _trabalho/teste_embutido.py`.
- Para instalar de verdade no celular do Bruno (ícone na tela, abrir sem barra do navegador, funcionar sem internet) o aplicativo precisa estar num endereço https. **Ainda não foi publicado em lugar nenhum.**
- Vídeo: `video/bk-gestao-navegacao.mp4` (1080x1920, 1 min 40 s, sem som). Telas soltas: `telas/` (31 imagens e `prancha-celular.jpg` com seis lado a lado).

## O que o aplicativo faz
- **Início:** vendido hoje, gráfico dos 7 dias, e a lista do que precisa de atenção (pedidos do site, peças esgotadas, acabando, paradas).
- **Estoque:** as 135 peças do catálogo com a quantidade por tamanho na própria lista; busca por nome, marca ou cor; filtro por situação e categoria.
- **Peça:** estoque por tamanho com − e +, quanto tempo o estoque dura no ritmo de venda, preço, custo, margem, como está no site e o histórico de movimentações.
- **Vender:** toca na peça, escolhe o tamanho, cobra (Pix, crédito, débito, dinheiro; desconto; cliente opcional). O estoque baixa na hora e a tela avisa o que esgotou. Comprovante pronto para o WhatsApp.
- **Vendas:** histórico por dia, resumo do período (ticket médio, lucro bruto, forma de pagamento, mais vendidas, categoria) e pedidos do site para confirmar.
- **Mais:** entrada de peças por tamanho, lista de reposição para o fornecedor, peças paradas que viram oferta para o grupo VIP, clientes, fechamento do dia, cadastro de peça com foto da câmera, tema escuro.

## O que é real e o que é exemplo
- **Real:** nomes das peças, marcas, categorias, cores, preços e fotos, tudo do catálogo do site novo (`../site`).
- **De exemplo (inventado para a demonstração):** quantidades em estoque, custo de cada peça (logo, margem e lucro), clientes, todas as vendas passadas e os dois pedidos "do site". Os clientes são nomes fictícios, sem telefone.
- **Simulado:** a ligação com o site. Os pedidos que aparecem em Vendas > Pedidos e a linha "No site" da peça mostram como ficaria; o site da demo e o aplicativo ainda não conversam.
- **Não existe ainda:** login, mais de um usuário, dados na nuvem. O que a pessoa faz fica guardado só no aparelho dela (`localStorage`). "Mais > Reiniciar a demonstração" apaga isso.
- Os botões de WhatsApp abrem a conversa com o texto pronto e a pessoa escolhe para quem mandar. Nada é enviado sozinho.

## Como foi desenhado
- Antes de desenhar, fotografei as telas que Kyte, Loyverse, Shopify, Shopify POS, Zoho Inventory, SumUp e Lightspeed publicam no Google Play (`_trabalho/folha-referencias-1.jpg` e `-2.jpg`). O que se repete e foi seguido: barra de cinco abas embaixo; venda por grade de fotos com barra "Cobrar" fixa; lista de estoque com foto, quantidade e cor de alerta; variação por tamanho; botões grandes de forma de pagamento; início com o valor do dia e gráfico da semana; listas planas, quase sem enfeite.
- Identidade igual à do site: preto, off-white e areia; Bebas Neue nos títulos e números, Jost no texto. Linha fina, sem cartão arredondado e sem sombra. Nenhuma imagem gerada.

## Arquivos
- `index.html`, `css/app.css`, `js/app.js` (telas e toques), `js/base.js` (dados de exemplo, regras de estoque e venda), `js/catalogo.js` (gerado), `manifest.webmanifest` e `sw.js` (instalação e uso sem internet), `img/` (fotos e ícones).
- Sem build e sem dependência além das fontes do Google.
- `_trabalho/gerar_dados.py` refaz `catalogo.js`, as fotos e os ícones a partir do site. `_trabalho/capturas.py` refaz as telas. `_trabalho/gravar.py` regrava o vídeo (o roteiro e as frases estão na função `roteiro()`). `node _trabalho/numeros.js` mostra os números de exemplo. Tudo com custo zero.
- Para mudar os números de exemplo: em `js/base.js`, `CENA` é o estoque das peças com foto limpa, `PESO` são as peças que mais vendem e `vendasDoDia` define o movimento por dia da semana.

## Para virar produto (se o Bruno quiser)
1. Perguntar a rotina dele: quem lança venda, se usa maquininha, como recebe mercadoria, se tem numeração além de P a GG, se vende fiado, se quer leitor de código de barras.
2. Dados na nuvem com login (para ele e para quem atende), cópia de segurança e mais de um aparelho.
3. Ligar ao site novo: esgotou no estoque, sai do site; pedido da sacola entra aqui.
4. Estoque inicial: contagem real das peças e custo de cada uma.
5. Publicar em https para instalar no celular.
