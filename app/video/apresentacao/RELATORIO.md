# Vídeo de apresentação do BK Gestão: relatório

**Com narração na voz "Gui" (clonada no Higgsfield).** As 15 falas usaram o modelo `qwen_audio_tts` em vez do `seed_audio` padrão. O motivo está em "O que não deu certo".

## Entrega
- `bk-gestao-apresentacao.mp4`: 1080x1920, 30 fps, H.264 + AAC 48 kHz mono, **91,9 s**, **9,1 MB**. Medidas do `ffprobe` no arquivo final. Volume integrado −16,2 LUFS e pico −1,4 dBFS, medidos com `ebur128`.
- `folha-de-quadros.jpg`: 18 quadros espaçados igualmente, com o tempo embaixo de cada um.
- Scripts nesta pasta. Tudo roda com um comando (ver "Como regravar").

## Estrutura do vídeo
1. **Abertura:** logo real da BK (`_coleta/logo.jpg`, invertida) e "BK GESTÃO". A fala 1 começa por cima.
2. **Dez blocos, na ordem pedida:** início do dia, estoque por tamanho, venda, baixa automática, pedido do site (com o selo "SIMULADO"), entrada de peças, peças paradas e oferta VIP, reposição, resumo e fechamento.
3. **Cartela final:** logo, "BK GESTÃO", "Feito para a BK Clothing" e a nota "Demonstração · números de exemplo".

Em cada bloco aparecem o ícone de traço fino desenhado em SVG, no mesmo estilo do objeto `I` de `js/app.js`, o número "NN / 10", o título em Bebas Neue, o aplicativo de verdade gravado com Playwright e a legenda da fala em Jost. A legenda acende palavra a palavra, sincronizada pelo tempo real de cada palavra do áudio (faster-whisper).

O que a fala cita recebe destaque: contorno areia com o resto da janela escurecido e, quando cabe, zoom de câmera de até 1,5x. Cada toque mostra um anel com uma onda.

## Falas
Texto final em `falas.py`, que é a fonte única. As mudanças em relação à missão:
- **02:** "peça esgotada, acabando ou parada", sem repetir "peça".
- **05:** "tu ajusta cada tamanho", mais curto.
- **09:** "Com o site ligado, o pedido de lá aparece aqui." O texto anterior afirmava que o site já está ligado, e a ligação ainda é simulada.
- **11:** "Peças paradas há mais de quarenta e cinco dias viram uma oferta pronta para o grupo VIP."
- **13:** "o lucro estimado". O app mostra "Lucro bruto estimado" e o custo é de exemplo.

`FALAS` em `_trabalho/gravar_narrado.py` foi atualizado com esses textos, e `video/roteiro-de-voz.md` foi regenerado.

## Áudios (em `video/voz/01.mp3` … `15.mp3`)
Modelo `qwen_audio_tts`, voz Gui (`1ef2b81a-5042-499e-9838-0c432f59113b`, element), `language: pt`, instrução "Português do Brasil, sotaque do sul do Brasil. Tom natural e conversado, como quem explica algo a um cliente. Ritmo tranquilo."

| Fala | Link |
|---|---|
| 01 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_014843_827c5586-ceaf-4a06-aa7e-ec211dc5cbb5.mp3 |
| 02 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_012233_3bd2907d-ac8f-4294-9880-9711acca06ca.mp3 |
| 03 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_014914_87cbc286-1f4e-4176-b3ad-572c57c122d5.mp3 |
| 04 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_014936_f0d91f50-d4b5-40a7-9d1d-79c9230932a5.mp3 |
| 05 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_012255_084aa256-cdab-4fc7-a41a-16009df1851f.mp3 |
| 06 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_014951_adf287d5-952c-4ccc-b991-16c69e3c777d.mp3 |
| 07 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015005_8f1edceb-fae2-497f-b04b-d3d733e55545.mp3 |
| 08 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015103_f4fd05a9-ac62-4c63-85bc-474a233a2892.mp3 |
| 09 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015121_b359cac6-8d06-49c4-9ed3-ea4e17bf2760.mp3 |
| 10 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015137_3d81b6bd-7aa8-484a-8530-6a25a2afb797.mp3 |
| 11 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015152_a0f1b485-6b87-4524-84ff-1cc079bbe9f3.mp3 |
| 12 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015207_5b27f915-3e86-45a8-b2f1-13b5e44bcb38.mp3 |
| 13 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015223_36b3a5e1-ffe9-4074-b507-127f20555ecc.mp3 |
| 14 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015238_90bdd2ca-338c-4096-becb-4b0d6943d68a.mp3 |
| 15 | https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261009_015254_eb6c5658-1394-4dbf-91f5-7f9e65ed27b9.mp3 |

Conferi as 15 transcrevendo cada uma com o Whisper `medium`. Todas dizem o texto de `falas.py`. Em duas a transcrição sai diferente, mas o áudio está certo: o Whisper escreve "BK" como "becar" e "quarenta e cinco" como "45". **Eu não ouvi os áudios.** A conferência foi só por transcrição, então vale escutar antes de mandar ao Bruno, principalmente o sotaque.

A primeira geração, com `seed_audio`, ficou guardada em `video/voz/_seed_audio_v1/`.

## Créditos do Higgsfield (teto: 20)
| Rodada | Modelo | Créditos |
|---|---|---|
| Narração 1 (15 falas) | seed_audio | 8,3 |
| Teste A–D | text2speech_v2 (seed_speech falhou e foi reembolsado; elevenlabs ok) | 0,6 |
| Teste E–F | qwen_audio_tts | 0,1 |
| Refação de 5 falas, 2 variações cada | seed_audio | 5,6 |
| Narração final (13 falas; a 02 e a 05 vieram do teste E–F) | qwen_audio_tts | 0,46 |
| **Total** | | **≈ 15,1** |

A soma vem do saldo antes e depois de cada rodada e das transações. Nenhuma imagem e nenhum vídeo foram gerados.

O saldo também mostra uma entrada de +40 "Voice Element" (reembolso da criação da voz) às 01:15 UTC. Não foi coisa minha e não sei explicar.

## O que não deu certo
1. **seed_audio com a voz clonada.** As falas saíram trocadas, com pedaços da gravação de referência da voz. A 02 começava com "Bruno, esse é o BK…" e dizia o texto antigo. A 05 também tinha o texto antigo. A 15 dizia "as duas peças". As 10 variações de refação tiveram o mesmo problema.
   - Pelos parâmetros dos jobs, o `seed_audio` usa o áudio da voz como referência (`voice_as_reference`), e essa referência é a própria gravação do roteiro antigo.
   - Também pelos parâmetros, a voz Gui não lista `seed_audio` entre os modelos suportados, só `elevenlabs`, `minimax`, `seed_speech` e `qwen_audio`.
   - Por isso troquei para `qwen_audio_tts`: mesma voz, com idioma `pt`. Não usei nenhuma outra voz.
2. **text2speech_v2 com seed_speech.** Os dois jobs falharam sem mensagem de erro e foram reembolsados.
3. **text2speech_v2 com elevenlabs.** Funcionou, mas trocou "tu ajusta" por "estou a ajustar" e "você ajusta". Descartei.
4. **Lote de geração.** Duas falas foram recusadas com `429 rate_limit_reached`. Gerei de novo uma por vez, sem cobrança dobrada.

## Limites que ficaram (o que não está perfeito)
- **Fala 11 (peças paradas):** quando a voz chega em "grupo VIP", a tela já mostrou a oferta montada (67–68 s) e volta ao menu "Mais" a caminho da reposição. Os últimos cerca de 0,6 s da frase caem sobre o menu.
- **Fala 13 (resumo):** sem zoom. Com zoom, o total e os nomes das formas de pagamento ficavam cortados. Durante "formas de pagamento", o contorno às vezes continua no lucro.
- **Fala 02:** sem zoom, pelo mesmo motivo (os números 2, 3, 17 e 32 eram cortados). Os itens "esgotada" e "acabando" se acendem um de cada vez. O "parada" não ficou visível nos quadros que conferi.
- **Fala 05:** no instante "e quanto tempo o estoque dura", o título grande da peça aparece meio escondido sob o cabeçalho fixo do próprio app. Isso é rolagem do app, não algo da montagem.
- **Rolagem:** seis momentos têm um intervalo de 120 a 400 ms entre quadros da gravação (30,2 s, 55,5 s, 57,8 s, 69,1 s, 81,0 s e 81,7 s). O vídeo repete o quadro anterior, e isso pode parecer um engasgo curto.
- **Duração:** 91,9 s, dentro do limite de 60 a 100 s.
- **Legenda na abertura:** a fala 01 começa sobre a logo, antes de a janela do app entrar.

## Como foi feito
Seguindo a seção 5 da missão, trabalhei com três agentes (Claude Code em modo `-p`), cada um com uma entrega em arquivo dentro de `_trabalho/`:
1. **Direção:** `plano-de-cenas.md`.
2. **Montagem:** os scripts, `montagem-relatorio.md` e uma rodada de correção.
3. **Revisão:** `revisao.md`, com 15 itens, em uma rodada.

A voz também saiu por sessões curtas do Claude Code, porque o Higgsfield só está conectado lá. Os briefings e os relatórios de cada rodada estão em `_trabalho/briefing-*.md` e `voz-*.md`.

Depois da rodada de correção, eu (Hermes) fiz três ajustes direto em `montar.py`, conferindo os quadros a cada um:
- o zoom só aproxima até o trecho citado caber inteiro;
- sem zoom nas falas 02 e 13;
- o cabeçalho troca em sequência, sem os dois títulos aparecerem sobrepostos.

O aplicativo (`index.html`, `css/`, `js/`, `img/`) não foi alterado. Fora de `video/apresentacao/` e `video/voz/`, só mexi em `_trabalho/gravar_narrado.py` (o `FALAS`, como a missão pede) e em `video/roteiro-de-voz.md`, que é gerado por ele.

## Como regravar
```
cd "C:/dev/bk clothing/app/video/apresentacao"
py -3.12 fazer.py              # tudo do zero: ícones, alinhamento das falas, gravação do app (~1,5 min) e montagem (~2 min)
py -3.12 fazer.py --so-montar  # só a montagem, reaproveitando a gravação em _trabalho/gravacao/
```
- **Versão com música e sem narração:** `py -3.12 fazer.py --so-montar --trilha "caminho/da/musica.mp3"`. O arquivo sai em `bk-gestao-apresentacao-trilha.mp4` e a versão narrada continua igual. A música se repete se for curta, entra em 1 s, sai em 2,5 s e fica normalizada em −16 LUFS. As cenas e as legendas mantêm o ritmo das falas.
- **Mudar uma fala:** edite `falas.py` (`|` quebra a linha da legenda, `||` troca de página), gere de novo só aquele `video/voz/NN.mp3` com a voz Gui e rode `fazer.py` sem `--so-montar`. O tempo de cada cena segue a duração do áudio.
- **Visual** (posições, cores, zoom): constantes no topo de `montar.py`.
- **Ações no app:** `gravar.py`, com os toques e destaques de cada fala, ancorados nas palavras.
- Precisa de Python 3.12 com Playwright (Chrome), Pillow, numpy e faster-whisper, e de ffmpeg. As fontes Bebas Neue e Jost estão em `fontes/`.
- `_trabalho/quadros_finais/` (cerca de 500 MB) é recriado a cada montagem e pode ser apagado.
