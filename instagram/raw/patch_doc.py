# Atualiza index.html para a versão 2 do feed (sem preço, uma ideia por linha, com vídeo). Roda uma vez.
from pathlib import Path
f = Path(__file__).resolve().parent.parent / 'index.html'
s = f.read_text(encoding='utf-8')


def sub(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)


def troca(ini, fim, novo):
    global s
    a = s.index(ini)
    b = s.index(fim, a)
    s = s[:a] + novo + s[b:]


# diagnóstico: sai a linha de preço
troca('      <tr><td><b>0</b>Nenhuma foto traz', '      <tr><td><b>3</b>Três vídeos', '')
sub('Falta um padrão para a foto da peça, uma ordem para a grade e uma rotina.', 'Falta um padrão para a foto da peça, uma ideia por trás da grade e uma rotina.')

# seção 03
troca('  <h2><small>03</small>A regra da grade</h2>', '  <div class="par">', '''  <h2><small>03</small>Uma ideia por linha</h2>
  <p class="lead">Cada linha de três posts conta uma coisa só. Nada de moldura repetida nem etiqueta em toda foto: o que dá unidade é a peça limpa, a letra grande e o mesmo punhado de tons.</p>
  <div class="regra">
    <div><span>Linha de cor</span><h3>A peça em close</h3><p>A mesma jaqueta nas três cores, enorme, com o nome da cor atrás. É a linha que para o dedo.</p></div>
    <div><span>Linha de vídeo</span><h3>A peça se mexendo</h3><p>Um vídeo curto da peça-chave, um detalhe de tecido de perto e a coleção em letra.</p></div>
    <div><span>Linha no corpo</span><h3>Gente e loja</h3><p>Foto real vestida, a frase da marca, a parede da loja. Sem texto em cima da foto.</p></div>
  </div>
''')

# seção 04
troca('  <h2><small>04</small>Como destacar cada peça</h2>', '</div></section>', '''  <h2><small>04</small>Como destacar cada peça</h2>
  <p class="lead">Peça importante vira um carrossel de quatro imagens. O valor fica para a conversa: quem quer saber chama, e a venda começa ali.</p>
  <div class="fila c4">
    <figure><img src="carrossel/1.jpg" alt=""><figcaption><b>1. Capa</b>A peça em close, com o nome da cor. É o que aparece na grade.</figcaption></figure>
    <figure><img src="carrossel/2.jpg" alt=""><figcaption><b>2. A peça de verdade</b>A foto que a loja já tira hoje, sem texto.</figcaption></figure>
    <figure><img src="carrossel/3.jpg" alt=""><figcaption><b>3. Detalhe</b>Gola, zíper, tecido. De perto.</figcaption></figure>
    <figure><img src="carrossel/4.jpg" alt=""><figcaption><b>4. Ficha</b>Cores, tamanhos e como pedir.</figcaption></figure>
  </div>
</div></section>

<section><div class="w">
  <h2><small>05</small>Vídeo de peça-chave</h2>
  <p class="lead">Três vídeos de cinco segundos, verticais, feitos a partir das fotos das peças. Entram no feed como reel e rodam em sequência nos stories.</p>
  <div class="fila c3 vids">
    <figure><video src="videos/bomber.mp4" poster="videos/bomber.jpg" autoplay muted loop playsinline controls></video><figcaption><b>Jaqueta bomber</b>A peça gira devagar. É o vídeo para fixar no topo do perfil.</figcaption></figure>
    <figure><video src="videos/mochila.mp4" poster="videos/mochila.jpg" autoplay muted loop playsinline controls></video><figcaption><b>Mochila</b>A câmera dá a volta na peça.</figcaption></figure>
    <figure><video src="videos/arara.mp4" poster="videos/arara.jpg" autoplay muted loop playsinline controls></video><figcaption><b>As três cores</b>As jaquetas na arara, como na loja.</figcaption></figure>
  </div>
''')
sub('<h2><small>05</small>Destaques</h2>', '<h2><small>06</small>Destaques</h2>')
sub('<p class="lead">Seis destaques com nome e capa próprios, na ordem em que o cliente novo faz as perguntas.</p>',
    '<p class="lead">Seis destaques com nome e capa próprios, na ordem em que o cliente novo faz as perguntas. As capas são recortes das próprias peças e da loja.</p>')
sub('<h2><small>06</small>Stories</h2>', '<h2><small>07</small>Stories</h2>')
sub('<h2><small>07</small>A semana</h2>', '<h2><small>08</small>A semana</h2>')
sub('<h2><small>08</small>Para vender mais</h2>', '<h2><small>09</small>Para vender mais</h2>')
sub('<h2><small>09</small>O que é demonstração</h2>', '<h2><small>10</small>O que é demonstração</h2>')
sub('<b>Chegou hoje</b>A peça nova, com preço. Quem responde QUERO já entra na conversa.', '<b>Chegou</b>A peça nova. Quem responde QUERO já entra na conversa.')
sub('<b>Última unidade.</b> Uma peça, um tamanho, um preço.', '<b>Última unidade.</b> Uma peça, um tamanho.')
sub('<td>Coluna da peça: carrossel de quatro imagens</td>', '<td>A peça: carrossel de quatro imagens</td>')
sub('<td>Coluna do meio: marca, coleção, aviso ou vídeo da loja</td>', '<td>Vídeo de peça-chave ou da loja</td>')
sub('<td>Coluna do corpo: foto vestida ou vídeo curto</td>', '<td>No corpo: foto vestida ou provador</td>')
sub('Três posts por semana, um de cada coluna, e stories todos os dias.', 'Três posts por semana, que fecham uma linha da grade, e stories todos os dias.')
sub('<li><span><b>Preço na imagem.</b> Tira a primeira pergunta do caminho.</span></li>',
    '<li><span><b>Vídeo no topo.</b> O vídeo da peça-chave fica fixado. É a primeira coisa que o visitante vê se mexer.</span></li>')
sub('Publicar os seis primeiros posts, duas linhas completas da grade.', 'Publicar as duas primeiras linhas da grade: as três cores e a linha do vídeo.')
sub('As fotos de peça usam o padrão já feito para o site, redesenhado a partir das fotos da loja; cada uma precisa ser conferida com a peça real antes de publicar.',
    'As fotos de peça usam o padrão já feito para o site, redesenhado a partir das fotos da loja; cada uma precisa ser conferida com a peça real antes de publicar. Os três vídeos foram gerados a partir dessas fotos e servem para mostrar a ideia: o definitivo é filmar a peça real na loja, no mesmo enquadramento.')

# estilos novos
sub('.fila.c4{grid-template-columns:repeat(4,1fr)}', '.fila.c3{grid-template-columns:repeat(3,1fr);max-width:62rem}\n.vids video{width:100%;aspect-ratio:9/16;object-fit:cover;background:#111;display:block}\n.fone .gr video{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}\n.fila.c4{grid-template-columns:repeat(4,1fr)}')
sub('.fila.c4{grid-template-columns:repeat(2,1fr)}.fila.c6', '.fila.c4{grid-template-columns:repeat(2,1fr)}.fila.c3{grid-template-columns:1fr}.fila.c6')

# grade nova, com vídeo nas três casas
a = s.index("const posts=[")
b = s.index("document.getElementById('gr-hoje')", a)
s = s[:a] + """const posts=['01-preta','02-marinho','03-bege','04-video-bomber','05-detalhe-gola','06-inverno','07-mochila','08-video-mochila','09-detalhe-mochila','10-no-corpo-1','11-slogan','12-no-corpo-2','13-cargo','14-video-arara','15-conjunto','16-loja','17-logo','18-no-corpo-3'];
document.getElementById('gr-novo').innerHTML=posts.map(p=>{const v=p.match(/video-(.+)$/);return v?`<video src="videos/${v[1]}.mp4" poster="feed/${p}.jpg" autoplay muted loop playsinline></video>`:`<img src="feed/${p}.jpg" alt="">`}).join('');
""" + s[b:]
f.write_text(s, encoding='utf-8')
print('ok')
