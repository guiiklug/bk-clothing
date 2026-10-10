"""Monta a pasta sequencia-postagem/: tudo o que o Bruno posta, copiado e numerado na ordem, um dia por subpasta.

Uso:  python organizar.py
A pasta é apagada e refeita a cada vez (são cópias; os originais ficam em drop-verao/ e drop-pecas/).
Dentro de cada dia os arquivos já estão na ordem de postar. No feed, cada fileira vai de trás para frente
(o terceiro, o segundo, o primeiro) para aparecer inteira e na ordem certa no perfil.
COMO-POSTAR.txt, na raiz da pasta, repete a ordem com a legenda de cada post.
"""
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
V, P = RAIZ / 'drop-verao', RAIZ / 'drop-pecas'
SAIDA = RAIZ / 'sequencia-postagem'
FECHO = 'Vista estilo, vista BK Clothing. Chama no direct ou passa na loja: Rua Santa Catarina, 2348, Floresta, Joinville.'
GRUPO = 'https://chat.whatsapp.com/FCX9FvsBWBeACbsrjiNW62'
ZAP_DROP = ('Chegou o drop de verão, e vocês estão vendo primeiro.\n\n'
            'Bermudas da Jordan em cinco cores\nBermuda cargo e short da Nike, em preto\n'
            'Shorts de praia Brooksfield em azul e verde-água\nShorts Tommy Hilfiger em off-white, preto e marinho\n\n'
            'Quer garantir? Responda aqui com a peça e o tamanho que a gente separa.')
ZAP_CONVITE = ('Grupo VIP da BK Clothing.\nQuem está no grupo recebe o drop antes de ir para o Instagram e reserva o tamanho antes de acabar.\n'
               f'Entre aqui: {GRUPO}')
VIP = 'Quem está no grupo VIP recebe o drop antes do Instagram e reserva o tamanho antes de acabar. Link na bio.'

# dia -> lista de (onde postar, arquivo de origem, legenda ou observação)
SEQ = [
    ('dia-1-abertura', [
        ('whatsapp-grupo', V / 'whatsapp/drop-no-grupo.jpg', 'Antes de tudo, dentro do grupo VIP, com esta mensagem:\n' + ZAP_DROP),
        ('story', V / 'stories/1-capa.jpg', ''),
        ('feed', V / 'feed/02-vip.jpg', VIP),
        ('feed', V / 'feed/01-verao.jpg', 'O drop de verão inteiro numa imagem. Qual é o seu?'),
        ('feed', V / 'feed/00-capa.jpg', 'Seu verão começa na BK. Bermudas da Jordan, cargo e short da Nike, shorts de praia Brooksfield '
                                          'e shorts Tommy Hilfiger, tudo novo na loja.'),
        ('reels', V / 'videos/verao.mp4', 'A mesma legenda do post da capa.'),
    ]),
    ('dia-2-jordan', [
        ('story', V / 'stories/2-jordan.jpg', ''),
        ('story', V / 'stories/3-jordan-novas.jpg', ''),
        ('feed', V / 'feed/12-jordan-menta.jpg', 'Bermuda Jordan preta com verde-menta.'),
        ('feed', V / 'feed/11-jordan-preta.jpg', 'Bermuda Jordan preta com azul-claro.'),
        ('feed', V / 'feed/10-jordan.jpg', 'Bermudas da Jordan em cinco cores. Já na loja.'),
        ('reels', V / 'videos/jordan.mp4', 'Bermudas da Jordan em cinco cores. Já na loja.'),
    ]),
    ('dia-3-jordan', [
        ('feed', V / 'feed/15-jordan-verde.jpg', 'Bermuda Jordan verde com off-white.'),
        ('feed', V / 'feed/14-jordan-gelo.jpg', 'Bermuda Jordan gelo com branco.'),
        ('feed', V / 'feed/13-jordan-creme.jpg', 'Bermuda Jordan creme com preto.'),
    ]),
    ('dia-4-nike', [
        ('story', V / 'stories/4-nike.jpg', ''),
        ('feed', V / 'feed/22-nike-short.jpg', 'Short Nike preto com vivo branco.'),
        ('feed', V / 'feed/21-nike-cargo.jpg', 'Bermuda cargo Nike preta, com bolso de fivela de um lado e de zíper do outro.'),
        ('feed', V / 'feed/20-nike.jpg', 'Bermuda cargo e short da Nike, os dois em preto.'),
        ('reels', V / 'videos/nike.mp4', 'Bermuda cargo e short da Nike, os dois em preto.'),
    ]),
    ('dia-5-brooksfield', [
        ('story', V / 'stories/5-brooksfield.jpg', ''),
        ('feed', V / 'feed/32-brooksfield-agua.jpg', 'Short de praia Brooksfield verde-água.'),
        ('feed', V / 'feed/31-brooksfield-azul.jpg', 'Short de praia Brooksfield azul.'),
        ('feed', V / 'feed/30-brooksfield.jpg', 'Shorts de praia Brooksfield em azul e verde-água.'),
        ('reels', V / 'videos/brooksfield.mp4', 'Shorts de praia Brooksfield em azul e verde-água.'),
    ]),
    ('dia-6-tommy', [
        ('story', V / 'stories/6-tommy.jpg', ''),
        ('feed', V / 'feed/42-tommy-marinho.jpg', 'Short Tommy Hilfiger marinho com branco.'),
        ('feed', V / 'feed/41-tommy-offwhite.jpg', 'Short Tommy Hilfiger off-white com marinho.'),
        ('feed', V / 'feed/40-tommy.jpg', 'Shorts Tommy Hilfiger com listra lateral, em três cores: off-white, preto e marinho.'),
        ('reels', V / 'videos/tommy.mp4', 'Shorts Tommy Hilfiger com listra lateral, em três cores.'),
    ]),
    ('dia-7-basicas', [
        ('reels', P / 'videos/basicas.mp4', 'Peças básicas para o dia a dia: camiseta básica em seis cores, camiseta texturizada em quatro, '
                                            'polo de malha em três e camisa bege. Qual é a sua?'),
    ]),
    ('dia-8-conjuntos-e-bermudas', [
        ('reels', P / 'videos/conjuntos-bermudas.mp4', 'Conjuntos e bermudas, novidade na loja: Nike, High, Thug Nine, Hurley e as bermudas da Jordan. '
                                                       'Qual você leva?'),
    ]),
    ('dia-9-grupo-vip', [
        ('story', V / 'stories/7-vip.jpg', 'Colocar a figurinha de link do grupo logo abaixo de "Toque no link e entre".'),
        ('reels', P / 'videos/grupo.mp4', VIP),
        ('whatsapp-status', V / 'whatsapp/convite-vip.jpg', 'No status do WhatsApp e para mandar no direct, com esta mensagem:\n' + ZAP_CONVITE),
        ('whatsapp-status', V / 'videos/grupo-vip.mp4', 'Versão curta do convite, para o status.'),
    ]),
]
ONDE = {'feed': 'FEED', 'story': 'STORY', 'reels': 'REELS', 'whatsapp-grupo': 'WHATSAPP, DENTRO DO GRUPO', 'whatsapp-status': 'WHATSAPP, STATUS'}

shutil.rmtree(SAIDA, ignore_errors=True)
SAIDA.mkdir()
txt = ['SEQUÊNCIA DE POSTAGEM — BK CLOTHING', '',
       'Cada pasta é um dia. Dentro dela os arquivos já estão numerados na ordem de postar.',
       'No feed, cada fileira vai de trás para frente (o terceiro, o segundo, o primeiro): assim ela aparece inteira no perfil.',
       'Reels: desmarcar a opção de mostrar na grade do perfil, senão o vídeo ocupa um quadrado e desalinha as fileiras.',
       'Stories 4, 5 e 6: se quiser voto de verdade, colocar a figurinha de enquete do Instagram logo abaixo das opções.',
       'Fecho para colar no fim de toda legenda de feed e de Reels:', FECHO, '']
total = 0
for dia, itens in SEQ:
    (SAIDA / dia).mkdir()
    txt += ['', '=' * 60, dia.upper().replace('-', ' '), '=' * 60]
    for k, (onde, origem, legenda) in enumerate(itens, 1):
        if not origem.exists():
            raise SystemExit(f'falta o arquivo {origem}')
        nome = f'{k}-{onde}_{origem.name}'
        shutil.copy2(origem, SAIDA / dia / nome)
        total += 1
        txt += ['', f'{k}. {ONDE[onde]} — {nome}']
        if legenda:
            txt += [('Legenda: ' if onde in ('feed', 'reels') and not legenda.startswith('A mesma') else '') + legenda]
(SAIDA / 'COMO-POSTAR.txt').write_text('\n'.join(txt) + '\n', encoding='utf-8')
print('ok', total, 'arquivos em', len(SEQ), 'dias ->', SAIDA)
