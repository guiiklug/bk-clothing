# Diagnóstico Digital — BK CLOTHING
**Data:** 02/10/2026 · Analisado: site, Instagram, Linktree, presença no Google
**Loja:** BK Clothing — moda masculina, Rua Santa Catarina 2348, Floresta, Joinville/SC · WhatsApp (47) 98820-4407

---

## Resumo executivo

| Área | Nota | Situação |
|---|---|---|
| Site/catálogo | 3/10 | Funciona, mas é template genérico sem marca, sem descrição de produto e com links quebrados |
| Instagram | 4/10 | Bio ok, mas feed parado desde 23/05/2026 (4+ meses) e crescimento via follow/unfollow |
| Linktree | 2/10 | Endereço ERRADO (placeholder do Canadá), plano grátis vazando tráfego pra outros perfis |
| Google (Maps/GMB) | 0/10 | A loja NÃO EXISTE no Google Maps — nenhum perfil de empresa encontrado |

A marca vende (139 produtos no catálogo, WhatsApp ativo, grupo VIP), mas o digital está rodando em cima de ferramenta genérica mal configurada. Tem muito ganho rápido barato antes de qualquer projeto grande.

---

## 1. Google — o buraco maior

**O que está ok:**
- O site rankeia em 1º pra busca "bk clothing" e o Google já gera AI Overview com endereço correto.
- Instagram aparece em 2º no resultado.

**O que está quebrado:**
- **Zero perfil no Google Maps / Perfil da Empresa (Google Business Profile).** Busquei pelo endereço: a Rua Santa Catarina 2348 retorna apenas "Vera Cruz Escritório Virtual e Coworking" (4,9★, 91 avaliações). BK Clothing não existe como estabelecimento. Quem busca "loja de roupa masculina Floresta Joinville" nunca encontra a BK.
- Sem GMB = sem avaliações, sem fotos, sem horário, sem botão de WhatsApp no Google, sem tráfego local gratuito.

**Atenção:** o endereço 2348 é o mesmo do coworking Vera Cruz. Confirmar com o dono se a loja física fica ali mesmo (sala no local) ou se é só endereço fiscal — isso muda como cadastrar o GMB (loja com vitrine vs. empresa de área de atendimento). Se tem loja física aberta ao público, o cadastro é direto e é o maior ganho gratuito de toda a lista.

## 2. Site (bkclothing.com.br) — frame por frame

**Plataforma:** catálogo SaaS genérico ("catalogoapp") — Bootstrap 5 + jQuery 2.1.1 (biblioteca de 2014). Checkout via carrinho → Asaas/PIX/cartão ou "a combinar pelo WhatsApp".

**Identidade/layout:**
- Título do site é literalmente "CATÁLOGO BK CLOTHING" — cara de link de atacadista, não de marca.
- Tema cinza padrão do template, zero identidade visual. A logo aparece pequena num círculo sobre uma foto do interior da loja usada como banner (cortada no mobile).
- Nenhuma seção institucional: sem "quem somos", sem política de troca, sem prazo de entrega, sem prova social. Pra quem "envia pra todo Brasil", isso mata conversão de quem não conhece a loja.

**Produtos (139 itens, 9 categorias):**
- Página de produto crua: nome + preço + foto + botão. **Sem descrição, sem grade de tamanhos, sem tecido/composição, sem medidas.** Ex.: "Jaqueta Tommy — R$ 299,00" e nada mais.
- Fotos: flat lay no chão de madeira, feitas com celular, iluminação inconsistente entre produtos. Serve pro grupo VIP, não pra vitrine pública.
- Nomes genéricos e duplicados ("Bermuda Diesel" aparece 5x sem distinção de cor/modelo).
- Faixa de preço: R$ 69,90 (bag) a R$ 299,90 (moletom/jaqueta).

**Bugs encontrados:**
- **Link do Instagram no rodapé está quebrado:** aponta pra `instagram.com/@bkclothiing` (o "@" na URL quebra o link → página de erro).
- **Link do Facebook quebrado:** aponta pra `facebook.com/BK%20CLOTHING` (nome com espaço, não é URL de página válida).
- **og:image com caminho relativo quebrado** (`catalogoapp/f1239464...jpeg`): quando alguém compartilha o link do catálogo no WhatsApp, **o preview sai sem imagem** — grave pra uma loja que vende via WhatsApp.
- Sem meta description própria (usa "CATÁLOGO BK CLOTHING" de novo) → o Google monta a descrição sozinho.

**SEO:** o site só rankeia pela marca. Nenhuma estrutura pra capturar busca de produto ("jaqueta masculina joinville", "moletom oversized") — sem textos, sem headings, sem URLs amigáveis por categoria.

## 3. Instagram (@bkclothiing)

- **1.433 seguidores / 1.226 seguindo** — ratio quase 1:1, perfil cresceu via follow/unfollow. Pra quem chega no perfil, isso passa imagem de loja pequena/insegura.
- **Feed parado desde 23/05/2026** — mais de 4 meses sem post público. E os posts visíveis foram todos publicados em lote no MESMO dia (23/05): despejo de fotos de produto de uma vez, sem legenda estratégica, sem reels.
- Bio razoável: "vista estilo, vista bkclothing." + endereço + "Enviamos para todo Brasil" + link. É o melhor ativo digital deles hoje.
- Destaques: "ENDEREÇO" + 7 destaques "Quem usa?" (prova social de cliente — ótimo conteúdo, mal organizado: 7 destaques iguais sem capa padronizada).
- O que claramente sustenta a venda é story + grupo VIP do WhatsApp — o feed é vitrine morta.

## 4. Linktree (linktr.ee/bkclothiing)

- **ERRO GRAVE: o bloco de endereço mostra "172 Main St W, Listowel"** — endereço placeholder de uma cidade no Canadá que ninguém trocou. O botão "COMO CHEGAR?" aponta pro Google Maps via link de busca gigante e frágil.
- Plano grátis: rodapé com "Explore other Linktrees" e perfis de celebridades — **vaza o clique pra fora da marca**.
- Links atuais: WhatsApp, Catálogo, Grupo VIP 🥇, Como chegar.
- Sem pixel/UTM — impossível medir o que converte.

---

## Plano de ação priorizado

### Quick wins (1 dia de trabalho, custo zero)
1. Corrigir links de Instagram e Facebook no rodapé do site (config do catalogoapp).
2. Consertar og:image → preview bonito no WhatsApp (logo ou foto da loja).
3. Matar o Linktree: trocar por página própria `bkclothing.com.br/links` (mesmo domínio, com pixel, sem propaganda de terceiro) — ou no mínimo corrigir o endereço do Canadá hoje.
4. Consolidar os 7 destaques "Quem usa?" em 1–2 com capas padronizadas.
5. Título e meta description do site: "BK Clothing — Moda Masculina em Joinville | Envio para todo Brasil".

### Projeto principal (o que vale dinheiro)
6. **Google Business Profile completo**: cadastro, fotos da loja, horário, WhatsApp, posts semanais, pedir avaliação no grupo VIP (meta: 30+ avaliações em 60 dias). Maior ROI de toda a lista.
7. **Site novo com cara de marca** (landing + catálogo): hero forte, prova social ("Quem usa"), política de troca/envio, categorias navegáveis, grade de tamanho nos produtos. Manter o checkout WhatsApp que já funciona — o site não precisa ser e-commerce completo, precisa ser vitrine que gera confiança e manda pro WhatsApp.
8. **Padrão de foto de produto**: fundo único, luz consistente, 3 fotos por peça (frente, detalhe, vestida). É o que mais muda a percepção de valor.
9. **Rotina de feed**: 3 posts/semana reaproveitando o conteúdo de story que eles já produzem + reels de "chegou hoje".

### Risco a mapear antes de propor tráfego pago
O catálogo é revenda multimarca (Tommy, Boss, Diesel, Armani, Jordan, High). Antes de prometer anúncio no Google Shopping/Meta, confirmar a procedência/nota das peças — anúncio de produto de marca de terceiro sem autorização derruba conta. Orgânico + GMB + WhatsApp não têm esse risco.

---

## Ângulo comercial (pra tua proposta)

- **Pacote 1 — "Arrumação" (quick wins + GMB):** 1 semana. Referência de preço em Joinville: R$ 800–1.500.
- **Pacote 2 — Site novo + identidade do catálogo:** 2–3 semanas. R$ 1.800–3.500 (amigo: ancora no valor, não na hora).
- **Pacote 3 — Recorrente:** gestão GMB + feed (12 posts/mês) + relatório: R$ 600–1.200/mês.

O argumento de venda pro teu amigo é um só: *"tu já vende bem no WhatsApp sem vitrine nenhuma. Hoje quem te procura no Google Maps não te encontra, quem compartilha teu catálogo manda um link sem foto, e teu Linktree diz que a loja fica no Canadá. Imagina com isso arrumado."*
