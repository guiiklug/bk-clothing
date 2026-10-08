import json,os,re
from PIL import Image,ImageOps,ImageFilter
import concurrent.futures as cf
SITE='../site'; os.makedirs(SITE+'/img/p',exist_ok=True); os.makedirs(SITE+'/img/look',exist_ok=True); os.makedirs(SITE+'/js',exist_ok=True)
P=json.load(open('produtos.json',encoding='utf-8'))
V='Várias cores'
cores="""Preto;Azul-marinho;Bege;Preto;Preto;Preto;Vermelho;Bege;Preto
Azul-marinho;Verde-água;Azul-marinho;Azul-marinho;Off-white;Vermelho;Preto;Azul-marinho;Preto
Preto;Color block;Jeans claro;Jeans destroyed;Jeans médio;Jeans preto;V;Verde;Preto
Azul-claro;Cinza-claro;Preto;Azul-marinho;Preto;V;Bege;Preto;Branco
Marrom;Preto;Caramelo;Off-white;Bege;Verde-militar;Off-white;Cinza-claro;Verde-militar
V;Grafite;V;V;V;V;Caqui;Preto;Branco
Preto;V;V;V;V;V;Branco;Preto;Preto
Preto;Branco;Branco;Preto;Preto;Preto;Preto;Off-white;Preto
Preto;Preto;Preto;Preto;Preto;Preto;V;V;V
V;V;V;V;Branco;Branco;V;V;V
V;V;V;V;V;V;Azul-marinho;V;V
V;V;V;V;Azul-marinho;Azul-marinho;V;Cinza;Preto
Cinza;Branco;Preto;Cinza;V;V;V;V;V
Preto;Azul-marinho;Preto e branco;Preto e branco;Preto e branco;Preto e branco;Azul-marinho;Preto;Off-white
Branco;Preto;Preto;Cinza;Preto;Cinza;V;V;V"""
C=[c for l in cores.split('\n') for c in l.split(';')]
assert len(C)==len(P),(len(C),len(P))
BR=['Tommy','Hugo Boss','Boss','Armani','Diesel','High','Jordan','Lacoste','Nike SB','Nike','Calvin Klein','Comp','EFFEL','Adidas','Casa Blanca','Palm Angels','Ralph Lauren','MR BUNNY','NY']
def cat(n):
    l=n.lower()
    if l.startswith(('jaqueta','moletom')): return 'Jaquetas & Moletons'
    if 'oversized' in l or l=='camiseta comp': return 'Oversized'
    if 'polo' in l: return 'Polos'
    if l.startswith('camiseta'): return 'Camisetas'
    if l.startswith(('bermuda','short')): return 'Bermudas & Shorts'
    if l.startswith('calça'): return 'Calças'
    if l.startswith('conjunto'): return 'Conjuntos'
    if l.startswith('regata'): return 'Regatas'
    return 'Acessórios'
out=[]
for p,c in zip(P,C):
    n=p['name'].replace('�','ç').replace('Sort ','Short ').replace('Camiseta Comp','Camiseta Oversized Comp').replace('Moletom Comp','Moletom Comp Supply')
    b=next((x for x in BR if re.search(r'\b'+re.escape(x)+r'\b',n,re.I)),'')
    b={'Boss':'Hugo Boss','Comp':'Comp Supply','Tommy':'Tommy Hilfiger','NY':'','MR BUNNY':'Mr Bunny'}.get(b,b)
    k=cat(n); l=n.lower()
    if k=='Acessórios':
        sizes=['39 ao 43'] if 'meia' in l else (['P','M','G','GG'] if 'cueca' in l else ['Único'])
    else: sizes=['P','M','G','GG']
    if p['desc'].startswith('Tamanho:'): sizes=['M','G']
    price=float(p['price'].replace('.','').replace(',','.')) if p['price'] else None
    out.append(dict(id=p['id'],n=n,b=b,c=k,cor=(V if c=='V' else c),p=price,i=len(p['imgs']),s=sizes,d=('1 par, branco ou preto.' if 'meia' in l else '')))
json.dump(out,open(SITE+'/js/produtos.json','w',encoding='utf-8'),ensure_ascii=False)
open(SITE+'/js/produtos.js','w',encoding='utf-8').write('window.BK_PRODUTOS='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';')
def conv(a):
    src,dst,w=a
    if os.path.exists(dst): return
    im=ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.save(dst,'WEBP',quality=80,method=4)
jobs=[]
for p in P:
    for k in range(len(p['imgs'])):
        s=f"img/{p['id']}_{k}.jpg"
        jobs.append((s,f"{SITE}/img/p/{p['id']}_{k}.webp",1200)); jobs.append((s,f"{SITE}/img/p/{p['id']}_{k}_t.webp",560))
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(conv,jobs))
for i in range(1,13):
    im=Image.open(f'insta/ig{i}.jpg').convert('RGB'); im=im.resize((im.width*2,im.height*2),Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2,60,2))
    im.save(f'{SITE}/img/look/ig{i}.webp','WEBP',quality=84)
im=Image.open('capa.jpg').convert('RGB'); im.save(SITE+'/img/loja.webp','WEBP',quality=86)
from collections import Counter
print(Counter(o['c'] for o in out)); print(Counter(o['b'] for o in out))
