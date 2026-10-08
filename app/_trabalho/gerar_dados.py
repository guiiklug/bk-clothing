"""Monta os dados e as imagens do aplicativo a partir do catálogo do site novo.

Lê ../../site/js/produtos.json e as fotos de ../../site/img, copia uma foto pequena e uma grande de cada peça
para ../img e escreve ../js/catalogo.js. Também gera os ícones do aplicativo a partir da logo real.
Pode rodar de novo quando o catálogo mudar. Custo zero.
"""
import json
import re
import shutil
from pathlib import Path
from PIL import Image, ImageOps

AQUI = Path(__file__).resolve().parent
APP = AQUI.parent
SITE = APP.parent / "site"
COLETA = APP.parent / "_coleta"

prods = json.loads((SITE / "js" / "produtos.json").read_text(encoding="utf-8"))
std_js = (SITE / "js" / "std.js").read_text(encoding="utf-8")
STD = set(re.findall(r"'(\d+)'", std_js.split("BK_LIMPAS")[0]))
LIMPAS = set(re.findall(r"'(\d+)'", std_js.split("BK_LIMPAS")[1]))

(APP / "img" / "t").mkdir(parents=True, exist_ok=True)
(APP / "img" / "g").mkdir(parents=True, exist_ok=True)
(APP / "js").mkdir(exist_ok=True)

saida = []
for p in prods:
    i = p["id"]
    if i in STD:
        peq, gde = SITE / "img" / "std" / f"{i}_t.webp", SITE / "img" / "std" / f"{i}.webp"
    else:
        peq, gde = SITE / "img" / "p" / f"{i}_0_t.webp", SITE / "img" / "p" / f"{i}_0.webp"
    shutil.copyfile(peq, APP / "img" / "t" / f"{i}.webp")
    shutil.copyfile(gde, APP / "img" / "g" / f"{i}.webp")
    saida.append({"id": i, "n": p["n"], "b": p["b"], "c": p["c"], "cor": p["cor"], "p": p["p"], "s": p["s"],
                  "std": 1 if (i in STD or i in LIMPAS) else 0})

txt = "/* gerado por _trabalho/gerar_dados.py a partir do catálogo do site: não editar à mão */\nwindow.BK_CATALOGO=" \
      + json.dumps(saida, ensure_ascii=False, separators=(",", ":")) + ";\n"
(APP / "js" / "catalogo.js").write_text(txt, encoding="utf-8")
print("produtos", len(saida), "| com foto limpa", sum(x["std"] for x in saida))

# ícones: a logo real, clara sobre preto, com margem para o recorte arredondado do celular
logo = ImageOps.invert(Image.open(COLETA / "logo.jpg").convert("RGB"))
fundo = logo.getpixel((4, 4))
for nome, lado, ocupa in (("icone-512.png", 512, .70), ("icone-192.png", 192, .70), ("icone-apple.png", 180, .78)):
    tela = Image.new("RGB", (lado, lado), fundo)
    l = logo.resize((round(lado * ocupa),) * 2, Image.LANCZOS)
    tela.paste(l, ((lado - l.width) // 2, (lado - l.height) // 2))
    tela.save(APP / "img" / nome)
print("ícones ok, fundo", fundo)
