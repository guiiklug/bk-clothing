# Troca a paleta do Verão 27 para o pedido do Bruno (azul esbranquiçado, sem vermelho). Roda uma vez.
from pathlib import Path
f = Path(__file__).resolve().parent / 'gerar.py'
s = f.read_text(encoding='utf-8')


def sub(a, b):
    global s
    assert a in s, a[:60]
    s = s.replace(a, b)


sub("R, B, S, K, W = '#e2372b', '#a9d8e6', '#d9cdb6', '#0b0b0b', '#f3f0ea'",
    "# paleta pedida pelo Bruno em 07/10/2026: azul esbranquiçado em dois tons, sem vermelho nem azul forte\n"
    "# (R e B ficaram como nomes das duas casas de cor; R é o azul um tom acima, B o mais claro)\n"
    "R, B, S, K, W = '#c5d6e1', '#dce8ef', '#e6dfd0', '#0b0b0b', '#f3f0ea'")
sub("('13-regata', R, wd('Rega|ta', 268, 50, 54, W)", "('13-regata', K, wd('Rega|ta', 268, 50, 54, W)")
sub("('16-pochete', K, pc('pochete', 980, 540, 690, 12))", "('16-pochete', R, pc('pochete', 980, 540, 690, 12))")
sub('<p class="lead">A mesma loja, outra identidade. Bloco de cor forte, peça recortada por cima da letra e uma tipografia larga e pesada. Feita para a coleção de calor: camisetas, bermudas, regata e acessórios.</p>',
    '<p class="lead">A mesma loja, outra identidade. Bloco de cor clara, peça recortada por cima da letra e uma tipografia larga e pesada. Feita para a coleção de calor: camisetas, bermudas, regata e acessórios.</p>')
sub('Esta grita: cor chapada, peça jogada em diagonal com sombra, palavra enorme atrás.',
    'Esta é mais solta: cor chapada clara, peça jogada em diagonal com sombra, palavra enorme atrás.')
sub('<h3>De onde vêm as cores</h3><p>Das próprias peças. O vermelho é o do desenho da camiseta preta, o azul é o da listra do conjunto, a areia é a da pochete. Preto e off-white seguram o resto.</p>',
    '<h3>As cores</h3><p>Um azul esbranquiçado em dois tons, como o Bruno pediu, mais areia clara. Preto e off-white seguram o resto. A primeira versão usava vermelho e azul forte e saiu por não ser a cara da marca.</p>')
sub('''<div style="background:{R}">Vermelho</div><div style="background:{B}">Azul</div>''', '''<div style="background:{R}">Azul</div><div style="background:{B}">Azul claro</div>''')
sub('cada peça girando sobre a cor dela.', 'cada peça girando sobre um fundo da paleta.')
sub('<figcaption>Camiseta preta sobre o vermelho do próprio desenho.</figcaption>', '<figcaption>Camiseta preta sobre o azul claro.</figcaption>')
sub('<figcaption>Conjunto sobre o azul da listra.</figcaption>', '<figcaption>Conjunto sobre a areia.</figcaption>')
sub('o definitivo é filmar a peça real sobre um fundo de papel colorido.', 'o definitivo é filmar a peça real sobre um fundo de papel na cor da paleta. O fundo dos vídeos foi trocado por código, quadro a quadro.')
f.write_text(s, encoding='utf-8')
print('ok')
