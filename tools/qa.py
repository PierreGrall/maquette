#!/usr/bin/env python3
"""Contrôle qualité d'une maquette Grall Studio, en un seul appel.

Usage : python3 tools/qa.py <slug> [--feature "#id-de-la-feature"] [--click "sélecteur"]...
Sortie : erreurs de console (hors images externes) + UNE planche JPEG compacte
         /tmp/qa-<slug>.jpg (à ouvrir avec Read : une seule image, ~1 500 tokens).
Planche : 1440 px (ouverture, en-tête après défilement, feature, avis/FAQ, section Grall Studio)
          + 390 px (ouverture, feature, section Grall Studio) + 1440 px sans aucune image externe.
"""
import sys, os, threading, http.server, functools, argparse, io
from playwright.sync_api import sync_playwright
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('slug')
ap.add_argument('--feature', default='#estimateur')
ap.add_argument('--click', action='append', default=[])
a = ap.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
http.server.SimpleHTTPRequestHandler.log_message = lambda *x: None
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{srv.server_address[1]}/{a.slug}/'

ARGS = ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader']
errors, shots = [], []

def scroll_to(p, sel):
    p.evaluate("""s=>{const e=document.querySelector(s);if(!e)return;const y=e.getBoundingClientRect().top+scrollY-80;
      if(window.lenis&&window.lenis.scrollTo)window.lenis.scrollTo(y,{immediate:true});else scrollTo(0,y);}""", sel)
    p.wait_for_timeout(1200)

def snap(p, label):
    img = Image.open(io.BytesIO(p.screenshot(type='jpeg', quality=70)))
    shots.append((label, img))

def run(br, w, h, block=False, plan=()):
    ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
    p = ctx.new_page()
    if block:
        p.route('**/*', lambda r: r.abort() if r.request.resource_type in ('image',) and not r.request.url.startswith('http://127.0.0.1') else r.continue_())
    else:
        def con(m):
            t = m.text
            if m.type == 'error' and 'Failed to load resource' not in t and 'net::' not in t:
                errors.append(f'[{w}px] {t[:300]}')
        p.on('console', con)
        p.on('pageerror', lambda e: errors.append(f'[{w}px] pageerror: {str(e)[:300]}'))
    p.goto(URL, wait_until='load')
    p.wait_for_timeout(2600)
    for label, sel in plan:
        if sel == 'TOP':
            pass
        elif sel == 'HDR':
            p.evaluate("window.lenis&&window.lenis.scrollTo?window.lenis.scrollTo(900,{immediate:true}):scrollTo(0,900)")
            p.wait_for_timeout(900)
        else:
            scroll_to(p, sel)
            if sel == a.feature and not block:
                for c in a.click:
                    try: p.click(c, timeout=1500); p.wait_for_timeout(500)
                    except Exception as e: errors.append(f'[{w}px] clic impossible {c}')
        snap(p, f'{w}px {label}' + (' SANS IMAGES' if block else ''))
    ctx.close()

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=ARGS)
    run(br, 1440, 900, plan=[('ouverture', 'TOP'), ('en-tete', 'HDR'), ('feature', a.feature),
                             ('avis/faq', '.faq, #avis, .reviews'), ('grall-studio', '#grall-studio')])
    run(br, 390, 844, plan=[('ouverture', 'TOP'), ('feature', a.feature), ('grall-studio', '#grall-studio')])
    run(br, 1440, 900, block=True, plan=[('ouverture', 'TOP'), ('milieu', 'HDR')])
    br.close()

# planche : vignettes de 300 px de haut, rangées de 1440 px max
from PIL import ImageDraw
TH, MAXW = 300, 1440
th = [(l, im.resize((int(im.width * TH / im.height), TH))) for l, im in shots]
rows, cur, w = [], [], 0
for l, t in th:
    if cur and w + t.width > MAXW: rows.append(cur); cur, w = [], 0
    cur.append((l, t)); w += t.width
rows.append(cur)
sheet = Image.new('RGB', (MAXW, len(rows) * (TH + 16)), 'white')
d = ImageDraw.Draw(sheet)
for r, row in enumerate(rows):
    x = 0
    for l, t in row:
        sheet.paste(t, (x, r * (TH + 16) + 16)); d.text((x + 4, r * (TH + 16) + 2), l, fill='black'); x += t.width
out = f'/tmp/qa-{a.slug}.jpg'
sheet.save(out, quality=72)
print('ERREURS :', len(errors)); [print(' ', e) for e in errors[:15]]
print('PLANCHE :', out, sheet.size)
