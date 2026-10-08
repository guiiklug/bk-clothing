# Baixa as fotos padronizadas do Higgsfield, converte para o site e monta a folha de conferência antes/depois
import os, urllib.request
from PIL import Image, ImageOps, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
B = 'https://d8j0ntlcm91z4.cloudfront.net/user_3GlkoJPiGWn8VbUyzLemqFrq3OW/hf_20261006_'
J = {
    '1914784': '130102_15d7e950-1fb3-4252-98b7-1fade416a831', '1914785': '130103_7bdedb9a-adf0-47bb-8eb7-d1792af512a0',
    '1910185': '130103_a7a64c89-e175-40d8-a4f0-c79106950084', '1849694': '130105_c554724c-7523-498e-b798-863fdf792346',
    '1703189': '130105_5c3c52d3-cb7c-4270-ab3a-01c4f3010cd1', '1679459': '130104_0cfb0c18-a207-4a51-be2b-71e35f9ea222',
    '1910182': '130104_8fce3d36-aded-4a48-9c62-51ed417505b1', '1849734': '130102_3bf09dd8-0297-463c-a484-ac19c1746506',
    '1703193': '130102_02970abc-a1a9-4a4f-a905-2b6c04d55543', '1703192': '130101_e4fde4c3-5a26-44d0-93fa-600112dda7d5',
    '1703197': '130104_33dd90c5-a92f-43be-8ce6-de06d014bbca', '1688196': '130102_b0b9f4ea-4ba4-4a3b-8788-cc25b9c4f165',
    '1678831': '130109_163aa0b7-8a55-444a-b874-b03929b0129f', '1703184': '130110_c7496d9d-f904-4dc7-857e-836d3db5e10d',
    '1690115': '130110_59119d4c-2d32-48f3-8392-4f5d80217bf5', '1849982': '130109_93d85702-9ee7-436c-a1c1-f332c366185f',
}
os.makedirs('piloto', exist_ok=True)
os.makedirs('../site/img/std', exist_ok=True)
for k, v in J.items():
    f = f'piloto/{k}.png'
    if not os.path.exists(f):
        urllib.request.urlretrieve(B + v + '.png', f)
ids = sorted(f[:-4] for f in os.listdir('piloto') if f.endswith('.png'))
for k in ids:
    im = Image.open(f'piloto/{k}.png').convert('RGB')
    im.resize((1200, 1500), Image.LANCZOS).save(f'../site/img/std/{k}.webp', 'WEBP', quality=84)
    im.resize((560, 700), Image.LANCZOS).save(f'../site/img/std/{k}_t.webp', 'WEBP', quality=82)
# folha de conferência: original em cima, padronizada embaixo
t = 300
for n in range(0, len(ids), 10):
    part = ids[n:n + 10]
    S = Image.new('RGB', (len(part) * t, t + int(t * 1.25)), 'white')
    d = ImageDraw.Draw(S)
    for i, k in enumerate(part):
        a = ImageOps.fit(ImageOps.exif_transpose(Image.open(f'img/{k}_0.jpg')).convert('RGB'), (t, t))
        S.paste(a, (i * t, 0))
        S.paste(ImageOps.fit(Image.open(f'piloto/{k}.png').convert('RGB'), (t, int(t * 1.25))), (i * t, t))
        d.text((i * t + 5, 5), k, fill='yellow')
    S.save(f'piloto/conferencia_{n // 10 + 1}.jpg', quality=85)
print(len(ids), ids)
