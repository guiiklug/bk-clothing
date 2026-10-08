import re,json,html,os,urllib.request,concurrent.futures as cf
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get(u):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read()
        except Exception as e: err=e
    print('FAIL',u,err); return b''
ids={}
for p in range(1,7):
    s=open(f'page{p}.html','rb').read().decode('utf-8','replace')
    for i,slug in re.findall(r'product\?code=(\d+)-([^"]+)"',s): ids[i]=slug
print(len(ids))
def prod(i):
    s=get(f'https://bkclothing.com.br/product?code={i}-{ids[i]}').decode('utf-8','replace')
    name=re.search(r'<h1 class="h4">([^<]*)',s)
    price=re.search(r'class="fs-1">\s*R\$\s*([\d.,]+)',s)
    imgs=list(dict.fromkeys(re.findall(r'<img src="([^"]+)" class="d-block w-100"',s)))
    cat=re.search(r'<h4>Categorias</h4>(.*?)</table>',s,flags=re.S)
    cats=[html.unescape(c).strip() for c in re.findall(r'<td>([^<]*)</td>',cat.group(1))] if cat else []
    desc=re.search(r'<p class="lead">(.*?)</p>',s,flags=re.S)
    comb=re.search(r'id="formWithVariantCombinations" value="([^"]*)"',s)
    return dict(id=i,slug=ids[i],name=html.unescape(name.group(1)).strip() if name else '',price=price.group(1) if price else '',imgs=imgs,cats=cats,desc=html.unescape(desc.group(1)).strip() if desc else '',variants=html.unescape(comb.group(1)) if comb else '')
with cf.ThreadPoolExecutor(8) as ex: out=list(ex.map(prod,ids))
json.dump(out,open('produtos.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
os.makedirs('img',exist_ok=True)
jobs=[]
for p in out:
    for k,u in enumerate(p['imgs']): jobs.append((u,f"img/{p['id']}_{k}.jpg"))
def dl(j):
    u,f=j
    if not os.path.exists(f):
        b=get(u)
        if b: open(f,'wb').write(b)
with cf.ThreadPoolExecutor(10) as ex: list(ex.map(dl,jobs))
for u,f in [('https://supliutech.nyc3.cdn.digitaloceanspaces.com/covers/e61dea88-7f3c-433c-a4e5-49f0fb7e2bc9.jpeg','capa.jpg'),('https://supliutech.nyc3.cdn.digitaloceanspaces.com/catalogoapp/f1239464-ddfa-483d-85aa-9f29a26c4fe6.jpeg','logo.jpg')]: dl((u,f))
from collections import Counter
print(len(out),len(jobs),len(os.listdir('img')))
print(Counter(c for p in out for c in p['cats']))
print(Counter(len(p['imgs']) for p in out))
print([p for p in out if p['desc'] or p['variants'] not in('null','')][:5])
print([p['name'] for p in out if not p['price'] or not p['imgs']])
