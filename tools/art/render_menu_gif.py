import re, sys, io
sys.path.insert(0,'/home/claude/gen')
from illo import svg
from PIL import Image
from playwright.sync_api import sync_playwright
h=open('/home/claude/menu/project/Main.dc.html').read()
body=h[h.index('</helmet>')+9:h.index('</x-dc>')].replace('{{accent}}','#F2B632')
F='/home/claude/fonts/node_modules/@fontsource'
ff=f'''
@font-face{{font-family:'Fraunces';font-weight:500;font-style:normal;src:url(file://{F}/fraunces/files/fraunces-latin-500-normal.woff2)}}
@font-face{{font-family:'Fraunces';font-weight:700;font-style:normal;src:url(file://{F}/fraunces/files/fraunces-latin-700-normal.woff2)}}
@font-face{{font-family:'Fraunces';font-weight:500;font-style:italic;src:url(file://{F}/fraunces/files/fraunces-latin-500-italic.woff2)}}
@font-face{{font-family:'Fraunces';font-weight:700;font-style:italic;src:url(file://{F}/fraunces/files/fraunces-latin-700-italic.woff2)}}
@font-face{{font-family:'DM Sans';font-weight:400;src:url(file://{F}/dm-sans/files/dm-sans-latin-400-normal.woff2)}}
@font-face{{font-family:'DM Sans';font-weight:500;src:url(file://{F}/dm-sans/files/dm-sans-latin-500-normal.woff2)}}
@font-face{{font-family:'DM Sans';font-weight:700;src:url(file://{F}/dm-sans/files/dm-sans-latin-700-normal.woff2)}}
@font-face{{font-family:'Noto Serif Malayalam';font-weight:600;src:url(file://{F}/noto-serif-malayalam/files/noto-serif-malayalam-malayalam-600-normal.woff2)}}
body{{margin:0;background:#173A2B}}'''
html=f'<!doctype html><html><head><meta charset="utf-8"><style>{ff}</style></head><body>{body}</body></html>'
open('/home/claude/gen/menu.html','w').write(html)
N=24; frames=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=b.new_page(viewport={'width':800,'height':1620}, device_scale_factor=1)
    pg.goto('file:///home/claude/gen/menu.html'); pg.wait_for_timeout(800)
    pg.evaluate("document.fonts.ready")
    for i in range(N):
        s=svg('frame', i/N, 800, 223).replace(' xmlns="http://www.w3.org/2000/svg"','')
        pg.evaluate("s=>{const o=document.querySelector('svg[role=img]'); const t=document.createElement('div'); t.innerHTML=s; o.replaceWith(t.firstElementChild);}", s)
        frames.append(Image.open(io.BytesIO(pg.screenshot(clip={'x':0,'y':0,'width':800,'height':1620}))).convert('RGB'))
    b.close()
pal=frames[0].quantize(colors=192, method=Image.MEDIANCUT)
q=[f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
q[0].save('/home/claude/gen/pass-the-papadam-menu.gif', save_all=True, append_images=q[1:], duration=83, loop=0, optimize=True)
frames[0].resize((400,810)).save('/home/claude/gen/preview_full.png')
