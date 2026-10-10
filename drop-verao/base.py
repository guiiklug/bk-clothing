"""O que os posts e os vídeos do drop de verão têm em comum: paleta, peças, marcas e frases.

Decisões do Guilherme e do Bruno em 10/10/2026 (sessão de perguntas na loja):
- nada de palavra solta gigante ("Quadra", "Rua", "Basquete", "Listra" foram rejeitadas como bregas): frase normal ou só a peça;
- a abertura de cada marca leva uma frase; os posts de cor mostram só a peça, com o nome pequeno;
- pode escrever as quatro marcas e usar o símbolo delas (marcas.py);
- o bordão "Vista estilo, vista BK Clothing" é a frase principal da capa;
- o verão entra como "Seu verão começa na BK.";
- ordem de importância: Jordan, Nike, Brooksfield, Tommy, com mais ênfase na Jordan;
- grupo VIP: a vantagem é ver e reservar antes (sem prometer desconto).
"""
import shutil
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
A1, A2, S, K, W = '#dce8ef', '#c5d6e1', '#e6dfd0', '#0b0b0b', '#f3f0ea'
LGI = '<b>BK</b><i>CLOTHING</i>'
BORDAO = 'Vista estilo,|vista BK Clothing.'
VERAO = 'Seu verão|começa na BK.'
VIP = 'Quem está no grupo VIP|vê primeiro.'
VANTAGENS = ['Recebe o drop antes de ir para o Instagram', 'Reserva o tamanho antes de acabar']
ORDEM = ['jordan', 'nike', 'brooksfield', 'tommy']

# as três cores do drop anterior de bermudas entram junto com as novas
for novo, antigo in {'basquete-preta': 'preta', 'basquete-gelo': 'cinza', 'basquete-verde': 'verde'}.items():
    if not (AQUI / 'cut' / f'{novo}.png').exists():
        shutil.copy(AQUI.parent / 'drop-jordan' / 'cut' / f'{antigo}.png', AQUI / 'cut' / f'{novo}.png')
RAZAO = {f.stem: (lambda i: i.width / i.height)(Image.open(f)) for f in (AQUI / 'cut').glob('*.png')}

# marca -> (frase de abertura, resumo curto, peças na ordem em que aparecem)
MARCAS = {
    'jordan': ('Bermudas da Jordan.|Cinco cores na loja.', 'Bermudas · cinco cores',
               ['basquete-preta', 'basquete-menta', 'basquete-creme', 'basquete-gelo', 'basquete-verde']),
    'nike': ('Cargo e short da Nike.|Os dois em preto.', 'Cargo e short · preto', ['cargo-preta', 'vivo-preta']),
    'brooksfield': ('Shorts Brooksfield.|Azul e verde-água.', 'Shorts de praia · duas cores', ['praia-azul', 'praia-agua']),
    'tommy': ('Shorts Tommy Hilfiger.|Três cores na loja.', 'Shorts · três cores', ['listra-offwhite', 'listra-preta', 'listra-marinho']),
}
# peça -> (marca, nome, cor)
PECAS = {
    'basquete-preta': ('jordan', 'Bermuda Jordan', 'Preta com azul-claro'),
    'basquete-menta': ('jordan', 'Bermuda Jordan', 'Preta com verde-menta'),
    'basquete-creme': ('jordan', 'Bermuda Jordan', 'Creme com preto'),
    'basquete-gelo': ('jordan', 'Bermuda Jordan', 'Gelo com branco'),
    'basquete-verde': ('jordan', 'Bermuda Jordan', 'Verde com off-white'),
    'cargo-preta': ('nike', 'Bermuda cargo Nike', 'Preta, com bolso de fivela'),
    'vivo-preta': ('nike', 'Short Nike', 'Preto com vivo branco'),
    'praia-azul': ('brooksfield', 'Short de praia Brooksfield', 'Azul'),
    'praia-agua': ('brooksfield', 'Short de praia Brooksfield', 'Verde-água'),
    'listra-offwhite': ('tommy', 'Short Tommy Hilfiger', 'Off-white com marinho'),
    'listra-preta': ('tommy', 'Short Tommy Hilfiger', 'Preto com azul-claro'),
    'listra-marinho': ('tommy', 'Short Tommy Hilfiger', 'Marinho com branco'),
}


def tinta(fundo):
    """Cor do texto sobre um fundo."""
    return W if fundo == K else K
