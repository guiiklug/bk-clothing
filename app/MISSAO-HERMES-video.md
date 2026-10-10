# Missão: vídeo de apresentação do BK Gestão

Hermes, quero um vídeo de apresentação da plataforma BK Gestão, feito por código em Python, para o cliente assistir no celular. Tem que explicar como a plataforma funciona, com legendas, ícones e a minha voz narrando. Quero resultado de agência, não esqueleto.

## 1. Estude o projeto antes de criar
Pasta: `C:\dev\bk clothing\app`
- Leia `LEIAME.md` inteiro: o que o aplicativo faz, o que é real e o que é exemplo.
- Abra o aplicativo e use: `python -m http.server 4178 --directory "C:/dev/bk clothing/app"` e http://localhost:4178 em tamanho de celular.
- Veja o que já existe: `telas/` (31 telas), `video/bk-gestao-navegacao.mp4` (navegação muda de 100 s), `video/roteiro-de-voz.md` (as 15 falas), `_trabalho/gravar.py` e `_trabalho/palco.html` (gravam o aplicativo de verdade com Playwright e ffmpeg) e `_trabalho/gravar_narrado.py` (a mesma gravação no tempo de cada fala; ainda não foi rodado).
- Contexto do cliente: `C:\dev\bk clothing\LEIAME.md` e `diagnostico-bk-clothing.md`. A BK Clothing é uma loja de moda masculina de Joinville; o dono é o Bruno. O vídeo é para ele.

## 2. O que entregar
`video/apresentacao/bk-gestao-apresentacao.mp4`
- Vertical, 1080x1920, 30 quadros por segundo, H.264 com áudio AAC. Entre 60 e 100 segundos. Leve o bastante para mandar por WhatsApp (mirar em até 20 MB).
- Abertura curta com a marca da BK, blocos que explicam cada parte e cartela final.
- Em cada bloco: ícone, título curto, o aplicativo de verdade funcionando e a legenda da fala.
- Blocos, nesta ordem: início do dia, estoque por tamanho, venda, estoque que baixa sozinho, pedido do site, entrada de mercadoria, peças paradas e oferta para o grupo VIP, reposição, resumo e fechamento.
- Legenda sincronizada com a voz, grande e legível no celular, dentro da zona segura (nada colado nas bordas nem embaixo demais).
- O que aparece do aplicativo tem que ser captura real dele rodando, não desenho imitando tela.

Junto com o vídeo:
- `video/apresentacao/folha-de-quadros.jpg`: 18 quadros espalhados pelo vídeo, para eu conferir sem assistir.
- `video/apresentacao/RELATORIO.md`: o que foi feito, o que não deu certo, créditos gastos e como regravar.
- Todos os scripts em `video/apresentacao/`, rodando com um comando.

## 3. Minha voz
Use o Higgsfield para gerar a narração com a minha voz clonada.
- nome: Gui
- voice_id: 1ef2b81a-5042-499e-9838-0c432f59113b
- voice_type: element
- Modelo: seed_audio (padrão). Se não estiver disponível, text2speech_v2.
- Português do Brasil, tom natural e conversado, como se eu estivesse falando com um cliente.

Antes de gerar:
1. Confirme que a voz "Gui" aparece na lista de vozes. Em 08/10 ela não apareceu na listagem feita pelo Claude Code; confira se o espaço de trabalho (workspace) selecionado é o certo e se a voz terminou de processar.
2. Veja o custo antes. Teto: 20 créditos para toda a narração. Se passar, pare e me avise.

Ao gerar:
- Um áudio por fala (são 15), salvos em `video/voz/01.mp3` até `15.mp3`. Assim cada cena dura o tempo da sua fala e a legenda sincroniza.
- Se der timeout, não reenvie: use o id do job que voltou e espere o resultado.
- Se a voz estiver "processing", espere e confira de novo antes de tentar.
- Se a voz não aparecer ou não der para gerar, **não troque por outra voz**. Entregue o vídeo com legenda e sem narração, e diga isso na primeira linha do relatório.
- No relatório, me mande o link ou o caminho de cada áudio.

Texto a ser falado:
1. Bruno, esse é o BK Gestão: o estoque e as vendas da loja, no teu celular.
2. Abriu, tu já vê quanto vendeu hoje e o que precisa de atenção: peça esgotada, peça acabando e peça parada.
3. No estoque, cada peça mostra a quantidade por tamanho. O que está faltando aparece em vermelho.
4. Para achar uma peça, é só digitar o nome, a marca ou a cor.
5. Dentro da peça, tu ajusta o estoque de cada tamanho, vê a margem e quanto tempo esse estoque dura no ritmo de venda.
6. Para vender, toca na peça, escolhe o tamanho e cobra.
7. Vendeu, o estoque baixa sozinho. E o aplicativo avisa quando um tamanho esgota.
8. O comprovante já sai pronto para mandar no WhatsApp do cliente.
9. O pedido que chega pelo site aparece aqui. Confirmou o pagamento, virou venda.
10. Chegou mercadoria? Tu dá entrada por tamanho, em poucos toques.
11. O aplicativo mostra as peças paradas há mais de quarenta e cinco dias e monta a oferta para o grupo VIP.
12. A lista do que pedir ao fornecedor se monta sozinha, com base no que mais vende.
13. No resumo, tu acompanha as vendas, o lucro e as formas de pagamento do período.
14. E no fim do dia, o fechamento sai em um toque.
15. Tudo isso feito para a BK, com as tuas peças, no teu celular.

Pode melhorar o texto se ficar mais claro ou mais natural de falar, mantendo estas regras: falar com o Bruno, tratando por "tu"; sem gíria; sem prometer o que o aplicativo não faz (não emite nota fiscal; a ligação com o site ainda é simulada); sem número de venda ou de estoque, porque os da demo são de exemplo. Se mudar alguma fala, atualize `FALAS` em `_trabalho/gravar_narrado.py`.

## 4. Visual (regras minhas, não negociar)
- Identidade do aplicativo e do site: preto `#0b0b0b`, off-white `#f3f0ea`, areia `#c8b89a`; Bebas Neue nos títulos e Jost no texto.
- Sem cara de IA: nenhuma imagem ou vídeo gerado, nada de letra com serifa em fundo creme, nada de cartão arredondado com sombra, nada de emoji no lugar de ícone, nada de brilho ou degradê roxo.
- Ícones de traço fino desenhados por código (SVG), no mesmo estilo dos ícones do próprio aplicativo (`js/app.js`, objeto `I`).
- Movimento com intenção: entrada dos títulos, destaque do que a fala cita, ponto mostrando o toque. Sem efeito por efeito.
- Marca da BK: a logo real está em `C:\dev\bk clothing\_coleta\logo.jpg` e os ícones prontos em `img/`.

## 5. Time de agentes
Use agentes para chegar ao melhor resultado, com no máximo três e tarefa curta para cada um, sempre com entrega em arquivo:
1. Direção: estuda o projeto e escreve o plano de cenas (tempo, ícone, título, o que aparece do aplicativo, legenda).
2. Montagem: grava as cenas e monta o vídeo em Python.
3. Revisão: assiste pela folha de quadros, compara com o plano e com as regras da seção 4, e lista o que corrigir. Uma rodada de correção.
Não use agente para abrir dezenas de imagens uma a uma.

## 6. Limites
- Não altere o aplicativo (`index.html`, `artefato.html`, `css/`, `js/`, `img/`). Trabalhe só em `video/apresentacao/` e `video/voz/`.
- Não publique nada em lugar nenhum.
- Crédito do Higgsfield: só a voz, até 20. Zero imagem e zero vídeo gerado.
- Python 3.12, Playwright (com `channel="chrome"`), Pillow e ffmpeg já estão instalados. Não escreva script por heredoc no terminal, porque corrompe as barras invertidas: grave o arquivo e rode com `python arquivo.py`.

## 7. Só diga que terminou quando
- O arquivo do vídeo existir, abrir, tiver áudio (ou o relatório disser por que não tem) e durar entre 60 e 100 segundos. Confira com `ffprobe`.
- A folha de quadros mostrar legenda legível, ícone e o aplicativo real em todos os blocos.
- O relatório disser o que ficou de fora, sem inventar horário nem resultado.
