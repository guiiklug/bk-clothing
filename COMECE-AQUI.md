# BK Clothing — comece por aqui

Relatório para quem está entrando no projeto. Escrito em 08/10/2026.

## O que é
A BK Clothing é uma loja de moda masculina multimarca de Joinville/SC. O dono é o Bruno. O Guilherme está apresentando a ele, sem compromisso, um pacote de presença digital: site novo, Instagram, anúncios e logo. A meta é fechar o site por volta de R$ 3.500 a R$ 4.000 e oferecer um serviço mensal depois.

Nada foi publicado na internet e nada é definitivo: tudo aqui é demonstração.

## Em que pé está

| Frente | Pasta | Situação |
|---|---|---|
| Site, primeira versão | `site/` | Pronta. Escura, letra estreita. O Guilherme gostou, mas foi superada pela segunda. |
| Site, segunda versão | `site2/` | Pronta e é a atual. Paleta azul esbranquiçado, areia, preto e off-white; peças recortadas sobre blocos de cor; barra de avisos, vitrines com carrossel. |
| Instagram, identidade neutra | `instagram/` | Pronta. Feed de 18 posts, carrossel, destaques, stories e 3 vídeos. |
| Instagram, identidade com cor | `instagram/verao/` | Pronta, já na paleta que o Bruno pediu. 2 vídeos. |
| Vídeos de navegação no Instagram | `instagram/navegacao/` | Prontos, com beat feito por código. |
| Anúncios para Google | `anuncios/` | Segunda versão, sóbria. A primeira foi rejeitada e está em `_v1-rejeitada/`. |
| Estudos de logo | `logo/` | Oito direções desenhadas. O Guilherme ainda não escolheu. |
| Opções de letra para o site | `_coleta/letras/` | Nove opções. O Guilherme ainda não escolheu. |
| Material bruto e scripts | `_coleta/` | Catálogo atual da loja (135 produtos, 211 fotos) e os scripts que geram tudo. |
| Outras frentes | `app/`, `hermes/` | Feitas em outras sessões. Cada uma tem o próprio LEIAME. |

O detalhe de cada frente está no `LEIAME.md` da raiz. Leia antes de mexer.

## O que o Bruno já disse
- Não gostou de vermelho nem de azul forte: "não fazem parte da identidade".
- Pediu um azul mais esbranquiçado. Foi atendido no Instagram de verão e no `site2`.
- Não ficou claro qual das duas identidades de Instagram ele preferiu.

## Como o Guilherme gosta do trabalho
Estas regras valem para tudo e já custaram refação quando foram ignoradas.

- **Sem cara de IA.** Nada de vídeo ou modelo gerado no site. Usar foto real da loja e das peças sempre que existir.
- **Sem gíria nos títulos.** "Escolha seu corre" foi rejeitado.
- **Sem preço nas artes de Instagram e de anúncio.** No site o preço fica.
- **Nada engessado.** Moldura ou etiqueta repetida em toda foto foi rejeitada como clichê.
- **Anúncio é sóbrio.** Palavra gigante, botão e enfeite juntos foram chamados de brega.
- **Olhar referência antes de inventar.** Ele confia mais em "é assim que as lojas grandes fazem" do que em conceito autoral.
- **Avisar o custo antes de gastar.** Vale para créditos do Higgsfield e para o limite de uso do Claude.
- **Tela muito larga.** O monitor dele tem perto de 3.800 px. Layout só testado em 1.440 px chega para ele com letra minúscula. O site usa medidas em `rem` com base que cresce com a janela; não voltar para `px`.

## O que ainda é provisório
- Tamanhos (P/M/G/GG em tudo), guia de medidas e textos de troca e envio são de exemplo.
- Só 24 das 135 peças têm foto padronizada e recorte. As outras 111 custam cerca de 305 créditos no Higgsfield e só devem ser feitas se o Bruno fechar.
- O `site2` não tem painel de cadastro: os produtos ficam num arquivo de código. Falta decidir como o Bruno vai cadastrar peça nova.
- Na proposta (`site/proposta.html`) falta o WhatsApp do Guilherme e a confirmação dos valores.
- O catálogo revende marcas de terceiros. O Google reprova anúncio com marca registrada sem autorização; conversar com o Bruno antes de vender tráfego pago.

## Para trabalhar no projeto

### Instalar uma vez
1. Git, GitHub CLI e Claude Code.
2. Python 3.12 com as bibliotecas dos scripts:

```bash
pip install playwright pillow rembg onnxruntime numpy
```

3. O ffmpeg, para os vídeos.
4. O Google Chrome, que os scripts usam para tirar os prints.

### Baixar

```bash
gh auth login
```

```bash
gh repo clone guiiklug/bk-clothing
```

Depois é abrir a pasta `bk-clothing` no Claude Code.

### Ver o site

```bash
python -m http.server 4179 --directory site2
```

E abrir http://localhost:4179 no navegador. Também funciona com duplo clique em `site2/index.html`.

### Rotina de quem divide o projeto
- **Antes de começar:** pedir ao Claude para puxar as atualizações do GitHub.
- **Ao terminar:** pedir para salvar e enviar.
- **Combinar quem mexe em quê.** Texto e código o Git junta sozinho; imagem e vídeo não, e a versão de um substitui a do outro.

## O que não vem com o repositório
- **Conta do Higgsfield.** Foto e vídeo gerados saem da conta do Guilherme. Quem não tem conta deixa esse trabalho para ele.
- **Memória do Claude do Guilherme.** As preferências dele estão resumidas acima; o resto se aprende conversando com ele.
- **Ambiente Python do Hermes** (`hermes/.venv`). Recriar se for usar aquela pasta.

## Onde está cada coisa para mostrar
- Site atual: `site2/index.html`
- Instagram neutro: `instagram/index.html`
- Instagram com cor: `instagram/verao/index.html`
- Vídeos de navegação: `instagram/navegacao/navegacao-verao.mp4` e `navegacao-inverno.mp4`
- Anúncios: `anuncios/index.html`
- Logos: `logo/logos.jpg`
- Letras: `_coleta/letras/letras.jpg`
- Proposta comercial: `site/proposta.html`
