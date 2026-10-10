# Relatório de sessões

O que cada sessão fez, para quem não viu a conversa. A entrada mais nova fica em cima.
A regra de atualizar este arquivo e enviar ao GitHub no fim de toda sessão está no `CLAUDE.md`. O que existe no projeto e como se refaz está no `LEIAME.md`.

---

## 10/10/2026 — Guilherme, na loja com o Bruno

Dia inteiro dentro da BK Clothing, produzindo material de drop com o Bruno do lado e ajustando conforme ele reagia.

### O que foi feito

**Drop das bermudas de basquete (`drop-jordan/`)**
- Três cores (preta, gelo, verde) a partir de fotos de celular: fotos padronizadas, 6 posts, 2 stories, anúncio em 3 formatos e um vídeo curto da preta girando.
- `criativo.py`: vídeo de venda de 15 s feito por código, com corte no beat.
- `letras.py`: cinco letras para os criativos. **O Bruno escolheu a C, Big Shoulders Display.** Vale para os criativos; o site continua em Archivo.

**Drop de verão (`drop-verao/`)**
- 12 peças de quatro marcas: Jordan (5 bermudas), Nike (cargo e short), Brooksfield (2 shorts de praia), Tommy Hilfiger (3 shorts).
- `feed/` 18 posts, `stories/` 7, `whatsapp/` 2 artes do grupo VIP, `videos/` 6 vídeos, `textos.md` com legendas e ordem.
- `grade.jpg` mostra como o feed fica no perfil.
- `marcas/` e `marcas.py`: símbolos das quatro marcas.

**Vídeos do grupo, das básicas e dos conjuntos (`drop-pecas/`)**
- `videos/grupo.mp4` (convite para o grupo VIP com as melhores peças), `basicas.mp4` e `conjuntos-bermudas.mp4`.
- As básicas (camiseta, camiseta texturizada, polo, camisa) foram tratadas no Higgsfield, várias cores por imagem (`pack/`).

**Pasta para postar**
- `python organizar.py` monta `sequencia-postagem/`: nove dias, tudo numerado na ordem, com `COMO-POSTAR.txt`. A pasta não vai para o GitHub por ser cópia; rodar o script para tê-la.

**Regra nova**
- `CLAUDE.md`: toda sessão termina com este relatório atualizado e o envio ao GitHub.

### O que o Bruno e o Guilherme decidiram
- Letra dos criativos: Big Shoulders Display.
- Palavra solta gigante ("Praia", "Quadra", "Rua", "Basquete", "Listra") foi rejeitada duas vezes como brega. Ficou: frase normal na abertura de cada marca, peça grande com nome pequeno no resto.
- Bordão da loja: "Vista estilo, vista BK Clothing". Frase de verão: "Seu verão começa na BK."
- Ordem de importância: Jordan, Nike, Brooksfield, Tommy, com mais espaço para a Jordan.
- Pode escrever as marcas e usar os símbolos.
- Grupo VIP: a vantagem é ver e reservar antes, sem prometer desconto.
- Nos stories, as opções vão em letra grande entre dois fios; a caixa preta imitando enquete não agradou.
- Vídeo não leva foto tirada de qualquer jeito na loja nem foto de modelo do fornecedor: só a peça tratada.
- Vídeo começa devagar, para dar tempo de ler, e depois acelera.

As mesmas decisões estão no começo de `drop-verao/base.py`, que é de onde os scripts tiram frases e ordem.

### Custo no Higgsfield
Cerca de 38 créditos no dia: 20 nas bermudas de basquete (inclui um vídeo), 8,25 no drop de verão (3 peças) e 9,75 nas básicas (14 peças em 3 imagens). Posts, stories e os outros vídeos saíram por código.

### Pendente
- Marca de dois conjuntos de jaqueta e short, de um par de shorts e das básicas: o Guilherme ficou de passar.
- Short bege da foto da camisa: não se sabe se é conjunto; ficou fora.
- Símbolo da Brooksfield veio de imagem pequena; trocar se o Bruno tiver o arquivo maior.
- Básicas e conjuntos só têm vídeo, sem post de feed nem story.
- Os seis vídeos de `drop-verao/videos/` ainda têm o começo rápido; o Guilherme não pediu para mexer.
- Nenhum vídeo foi ouvido com som: a conferência foi por folha de quadros.
- Vídeos reais para o Bruno gravar na semana: a lista foi passada ao Guilherme (chegada do drop, detalhe na mão, peça no corpo, look no balcão, loja, pedido do grupo).

### O que não está no GitHub
As fotos brutas (`peças/` e as pastas `orig/` dos drops) ficam só no computador do Guilherme: têm pessoas aparecendo e o repositório é público. Os recortes prontos estão em `cut/` e `pack/`, então dá para refazer artes e vídeos sem elas. Só `recortar.py` precisa das originais.

---

## 08 e 09/10/2026 — enviado só agora

Trabalho anterior que estava no computador do Guilherme e não tinha subido.

- **Vídeos de demonstração (`videos/`, `video/`)**: o site no computador e no celular e o Instagram, com apresentação montada. `python video/roteiro.py` regrava. Feito em 08/10.
- **`instagram/simulacao.html`**: perfil do Instagram navegável, usado nesses vídeos.
- **Vídeo de apresentação do aplicativo BK Gestão (`app/video/`)**: feito por outra sessão, com narração. O relatório dela está em `app/video/apresentacao/RELATORIO.md`. A pasta de rascunho `app/video/apresentacao/_trabalho/` não foi enviada.
