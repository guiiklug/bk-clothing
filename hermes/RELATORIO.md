# Relatório — entregas para a apresentação da BK Clothing

06/10/2026. Zero crédito Higgsfield, sem subagentes, `site/` não foi alterado, nada publicado nem enviado.

## Pronto

| Arquivo | Especificação | Medido |
|---|---|---|
| `entregas/bk-site-desktop.mp4` | 1920×1080, H.264, sem áudio, 40–60 s, < 16 MB | 1920×1080, 30 fps, 44,3 s, 10,2 MB |
| `entregas/bk-site-celular.mp4` | 1080×1920, H.264, sem áudio, 30–45 s, < 16 MB | 1080×1920, 30 fps, 38,8 s, 6,9 MB |
| `entregas/bk-apresentacao-escura.pdf` | 16:9, 10–12 páginas | 11 páginas, 1920×1080, 2,0 MB |
| `entregas/bk-apresentacao-clara.pdf` | idem, mesmo conteúdo | 11 páginas, 2,0 MB |
| `apresentacao/apresentacao.html` + `img/` | fonte editável | tema claro com `?tema=claro` |
| `scripts/` | regravar e reexportar | ver abaixo |

## Como conferi
- **Vídeos:** extraí 16 quadros de cada um, em folha única, e olhei a folha. Sequência certa nos dois (hero → Seleção BK → jaqueta → tamanho M → sacola → categorias/lookbook → tema claro → loja → rodapé; no celular: fotos deslizando, menu, links.html no fim). Sem quadro em branco, sem seletor `?arte`, fontes Bebas Neue/Jost corretas, cursor/ponto do dedo visíveis. Os colchetes da logo aparecem se desenhando do 0 ao 2 s. Celular: sem rolagem lateral em 360 px (medido: 0 px).
- **Texto nítido:** conferi um quadro 1080p em tamanho cheio; sem faixas de cor.
- **PDFs:** 11 páginas cada, contadas no arquivo. Um script mede em cada página texto que estoura a caixa, elemento fora da área útil e imagem quebrada: resultado zero problemas nas duas versões. Vi as 11 páginas em miniatura e ampliei as que pareciam erradas (5, 7, 8), corrigi e revi.
- **Nenhum clique em `wa.me`, grupo VIP ou "Fechar pedido no WhatsApp"**: a gravação para na sacola.

## Decisões minhas
- **Gravação quadro a quadro, não `recordVideo`.** O `recordVideo` saiu com bitrate baixo e faixas nos tons lisos, e a captura por screencast saiu com ritmo irregular. Fiz uma biblioteca (`gravacao_lib.py`) que pausa as animações do navegador e avança 1/30 s por quadro, capturando JPEG. Resultado: 30 fps exatos, sem salto, e a transição de seções do site corre no tempo do vídeo. Custo: a gravação leva uns 5–8 min por vídeo.
- **Ritmo:** o roteiro sugerido cabia em 44 s no computador; mantive. No celular, 39 s.
- **Apresentação:** 11 páginas seguindo a estrutura sugerida (capa, ponto de partida, achados, site de hoje, site novo, antes e depois, como compra, o que mais vem junto, incluso, investimento e prazo, próximo passo). Investimento e prazo dividem uma página.
- **Antes e depois:** 6 peças (jaqueta Tommy, bermuda Nike, regata Nike, bermuda jeans, bag High, conjunto Nike). Escolhi pares em que a foto nova é fiel à original. Não usei a mochila (cor mudou) nem as jaquetas bomber com bolsos em aberto no LEIAME.
- **Site atual:** o print de bkclothing.com.br carregou normalmente (título "CATÁLOGO BK CLOTHING"), então usei o print real, não o `home.html`.
- **Textos:** reaproveitei os de `proposta.html` e o diagnóstico (96 de 135 produtos com uma foto, 135 produtos, achados 1–5). Sem depoimentos nem estatística.
- Nomes de arquivos temporários e quadros foram apagados; ficaram só entregas, apresentação e scripts.

## Pendências que dependem do Guilherme
1. **WhatsApp dele:** a página 11 mostra `SEU_NUMERO` (único lugar, id `contato` em `apresentacao.html`). Trocar e rodar `exportar_pdf.py`.
2. **Valores:** R$ 3.990, PIX R$ 3.790,50, 3x R$ 1.330, Google R$ 490, mensal a partir de R$ 690 estão como sugeridos, ainda não confirmados. Estão nos `<span class="preco">` da página 10.
3. Mostrar o vídeo e a apresentação só depois de decidir sobre as duas fotos de lookbook com modelo de IA (`look1.webp`, `look2.webp`): elas aparecem no vídeo do computador (Inverno 26) e na miniatura do lookbook da página 8.
4. Os vídeos mostram os dados provisórios do site (tamanhos P/M/G/GG, guia de medidas, texto de troca de 7 dias). A página de produto da apresentação também. Avisar o Bruno que são exemplo.
5. A página 8 diz "Trocas e envio... escritas com as suas regras": é o que a proposta promete; hoje o texto é padrão.

## Limitações
- O 5.º achado e o antes/depois citam fatos do diagnóstico de 02/10; não reverifiquei Instagram nem Linktree hoje.
- O print do site atual é de hoje. Se o catálogo mudar, rodar `scripts/prints.py`.

## Como refazer (na pasta `hermes/`, com o servidor do site na porta 4174)
```
python -m http.server 4174 --directory "C:\dev\bk clothing\site"
.venv\Scripts\python scripts\prints.py          # prints do site novo e do atual
.venv\Scripts\python scripts\prep_imagens.py    # antes/depois e recortes
.venv\Scripts\python scripts\exportar_pdf.py    # os dois PDFs + checagem de estouro
.venv\Scripts\python scripts\gravar_desktop.py  # vídeo do computador
.venv\Scripts\python scripts\gravar_celular.py  # vídeo do celular
```
(`.venv` e `scripts/folha.py` — folha de conferência — ficam em `hermes/`; o `.venv` pode ser apagado e recriado com `pip install playwright pillow` + `playwright install chromium`.)
