# Grupo VIP do WhatsApp: o que fazer com 181 pessoas

Escrito em 10/10/2026 para o Guilherme levar ao Bruno. As artes estão em `foto-grupo/` e `posts/`; a descrição nova está em `descricao.txt`.

## O que o grupo tem hoje
- 182 membros, só admin posta, criado em dezembro de 2024. Dezoito meses sem nenhuma mídia, link ou documento salvo ("Mídia, links e docs: 0"). Ou o grupo nunca recebeu post, ou tudo foi apagado. Em qualquer caso, quem entra hoje vê um grupo vazio.
- Foto: a logo em fundo branco, a mesma do site. Descrição em caixa alta, com emoji e o endereço do catálogo.
- 181 pessoas que pediram para entrar são o ativo digital mais valioso da BK. É mais que o alcance real de um post no Instagram com 1.400 seguidores, e chega direto na tela do cliente.

## Trocar agora (custo zero, dez minutos)
1. **Foto do grupo:** `foto-grupo/A-azul.jpg` (recomendada) ou `D-vip.jpg`. É a logo atual na paleta que o Bruno aprovou. O WhatsApp corta em círculo; as artes já respeitam isso.
2. **Descrição:** colar `descricao.txt`. Sai a caixa alta e entra o passo a passo de como comprar, que é o que a pessoa nova procura.
3. **Mensagem fixada:** mandar `posts/01-bem-vindo.jpg` e `posts/02-como-funciona.jpg` e fixar a segunda. Grupo de loja sem regra de compra vira confusão de "quanto é" e "tem no M".
4. **Continuar com "só admins podem enviar".** Com 181 pessoas, grupo aberto vira ruído e as pessoas saem. A conversa acontece no privado.
5. **Trocar o link de convite** se o atual estiver em sites públicos: o grupo é "VIP" e tem que parecer fechado.

## O que postar: cinco tipos, uma vez cada por semana

| Dia | Tipo | Arte | Como usar |
|---|---|---|---|
| Segunda | Chegou hoje | `03-chegou-hoje` | Foto da peça nova real (ou a arte com a peça recortada) + tamanhos disponíveis. Pede "responda QUERO no privado". |
| Quarta | Qual leva? | `05-qual-leva` | Três peças numeradas. A pessoa responde 1, 2 ou 3. É o post que mais gera resposta e mostra para o Bruno o que vende. |
| Quinta | Só no grupo | `07-so-no-grupo` | Uma condição que não vai para o Instagram: peça separada por 24 h, frete por conta da loja acima de X, brinde. Com prazo (até domingo). Sem isso o grupo não tem motivo para existir. |
| Sexta | Últimas peças | `04-ultimas` | Peças com um ou dois tamanhos sobrando. Mostra a grade com o que acabou riscado. Cria urgência sem desconto. |
| Sábado | Quem usa | `08-quem-usa` | Foto de cliente com a peça (pedir no privado quando entregar). Prova social e o cliente se sente parte. |

Quinzenal ou mensal: `06-nova-colecao` quando entra lote grande, `09-loja` e `10-todo-brasil` para quem entrou há pouco e não sabe que existe loja física e envio.

## Regras que fazem o grupo funcionar
- **Um a dois posts por dia, no máximo.** Grupo que manda cinco fotos seguidas às 23 h é silenciado. Horários bons: 12 h e 19 h.
- **Toda foto vai com texto curto:** nome da peça, tamanhos, como pedir. Sem preço na arte; o preço vai no texto da mensagem ou no privado, como o Bruno preferir. Isso deixa a arte reaproveitável.
- **Vídeo curto de 5 a 10 segundos** da peça na mão ou na arara vende mais que foto. O celular resolve; não precisa produção.
- **Áudio do Bruno** de vez em quando ("chegou a Diesel que vocês pediram") humaniza e é o formato que mais se vê no grupo de loja que vende.
- **Nunca mandar lista de preços em PDF** nem catálogo inteiro de uma vez: a pessoa salva e nunca mais abre.
- **Enquete nativa do WhatsApp** uma vez por semana ("qual cor você quer ver primeiro?"). Gera interação sem abrir o grupo.
- **Responder no privado em até uma hora** no dia do post. O grupo cria o desejo; a venda fecha no privado.

## Como crescer de 181 para 500
- Link do grupo no destaque "VIP" do Instagram, na página de links e no site (`site2` já tem a seção "Grupo VIP").
- Etiqueta na sacola ou cartão na entrega com o QR do grupo: "ofertas antes de todo mundo".
- Pedir no caixa: "quer entrar no grupo? Chega primeiro aqui".
- Uma vez por mês, uma condição só para quem indicar alguém que entrou.

## Medir
Toda semana anotar: quantas pessoas entraram e saíram, quantas responderam QUERO ou número, quantas vendas vieram do grupo. Em um mês dá para ver qual tipo de post vende e cortar o resto.

## Como gerar as artes de novo
`python gerar.py` nesta pasta. Peça, cor e texto ficam nas listas no topo do arquivo. Para trocar a peça de um post, o recorte precisa existir em `instagram/verao/cut/`.
