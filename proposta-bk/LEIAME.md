# Proposta para o Bruno (página para o celular)

Feita em 08/10/2026 pelo Carlos. Página única, sem build: abre com duplo clique em `index.html` (as fontes vêm do Google, então precisa de internet). Nada foi publicado.

## O que tem
1. Abertura: a logo; ao rolar, os colchetes se abrem e entra o título.
2. Hoje e a proposta: comparador de arrastar com 10 exemplos reais (site: início, produto, links; Instagram: perfil, grade, post; 4 fotos de peça).
3. Site novo: telas do `site2` e recursos.
4. Site e app ligados: simulação em que vender no site baixa o estoque do app e vender na loja atualiza o site.
5. BK Gestão: um dia na loja com 13 telas do `app/` e a tabela sem sistema × com o app.
6. Loja e marca: Google Maps, fotos, Instagram, links, acompanhamento.
7. Investimento: configurador com os dois pacotes; o total muda na hora.
8. Prazos e botão "Quero fechar", que abre o WhatsApp com a escolha pronta.

## Onde editar valores, prazos e WhatsApp
Tudo fica no bloco `CONFIG`, no topo do `index.html`:
- `pacotes.presenca`: R$ 3.500 de implantação + R$ 500/mês.
- `pacotes.gestao`: R$ 4.000 de implantação + R$ 200/mês.
- `prazos` e `prazoTotal`: hoje `null`, que aparece como "a definir".
- `whatsapp`: vazio. Enquanto estiver vazio, o botão mostra o aviso "número não configurado". Use 55 + DDD + número.
- `validade`: opcional.

## Pendente
- Prazos, número do WhatsApp e validade.
- Confirmar o escopo do BK Gestão listado no configurador (ligação com o site, estoque inicial, treinamento).
- Publicar num endereço https para o Bruno abrir no celular.

## Imagens (`img/`)
- `hoje-*`: prints do site, do Linktree e do Instagram atuais, tirados em 08/10/2026 em tela de celular.
- `novo-*`: prints do `site2` e do Instagram proposto.
- `antes-*` e `depois-*`: fotos de peça, vindas de `hermes/apresentacao/img`.
- `app-*`: telas de `app/telas`.
- `cut-*`: recortes de `site2/img/cut`.
- `loja.webp`: foto da parede da loja.

Todas em WebP para carregar rápido no celular (cerca de 2,5 MB no total).
