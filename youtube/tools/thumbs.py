"""Miniatures YouTube (1280 × 720) : capture du moment fort de chaque site en ligne, puis composition typographique.

python3 thumbs.py                → youtube/<projet>/out/<projet>-miniature-<langue>.jpg
"""
import base64, json, os, shutil, sys, time
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / '_tools').is_dir())
sys.path.insert(0, str(ROOT / '_tools'))
from check import CDP, serve  # noqa: E402

YT = ROOT / 'youtube'
WORK = YT / 'thumbs-work'
BASE = 'https://hoshuko.github.io/'

# moment fort de chaque site : page, position de défilement (fraction du parcours épinglé), délai
SHOTS = {
    'billot': ('maison-billot/', "(() => { const s = document.querySelector('#decoupe'); window.scrollTo(0, s.offsetTop + .86 * (s.offsetHeight - innerHeight)); })()"),
    'tafat': ('tafat/', "(() => { const s = document.querySelector('#accueil'); window.scrollTo(0, s.offsetTop + .17 * (s.offsetHeight - innerHeight)); })()"),
    'nacre': ('atelier-nacre/', "(() => { const s = document.querySelector('#accueil'); window.scrollTo(0, s.offsetTop + .85 * (s.offsetHeight - innerHeight)); })()"),
}

TEXT = {
    'billot': {'fr': ('23', 'morceaux', 'Site gratuit · open source'), 'en': ('23', 'cuts', 'Free website · open source'),
               'es': ('23', 'piezas', 'Web gratis · código abierto'), 'ar': ('23', 'قطعة', 'موقع مجاني · مفتوح المصدر')},
    'tafat': {'fr': ('', 'Un site qui nettoie', 'Site gratuit · open source'), 'en': ('', 'A site that cleans', 'Free website · open source'),
              'es': ('', 'Una web que limpia', 'Web gratis · código abierto'), 'ar': ('', 'موقع يُنظّف', 'موقع مجاني · مفتوح المصدر')},
    'nacre': {'fr': ('6', 'couches', 'Site gratuit · open source'), 'en': ('6', 'layers', 'Free website · open source'),
              'es': ('6', 'capas', 'Web gratis · código abierto'), 'ar': ('6', 'طبقات', 'موقع مجاني · مفتوح المصدر')},
    'warda': {'fr': ('', 'Née d’une rose', 'Site gratuit · open source'), 'en': ('', 'Born of a rose', 'Free website · open source'),
              'es': ('', 'Nacida de una rosa', 'Web gratis · código abierto'), 'ar': ('', 'وُلدت من وردة', 'موقع مجاني · مفتوح المصدر')},
    'tiziri': {'fr': ('', 'La boutique<br><i style="color:#B4532F">prend vie</i>', 'Site gratuit · open source'), 'en': ('', 'The shop<br><i style="color:#B4532F">comes alive</i>', 'Free website · open source'),
               'es': ('', 'La tienda<br><i style="color:#B4532F">cobra vida</i>', 'Web gratis · código abierto'), 'ar': ('', 'المحل ينبض بالحياة', 'موقع مجاني · مفتوح المصدر')},
}
STYLE = {
    'billot': dict(brand='Maison <i>Billot</i>', display="'Bodoni Moda'", font_brand="italic 700", accent='#B01F2E', ink='#1E1516', paper='#FBF9F8',
                   fonts='billot', big_style='italic 900', side='left', bg='1280px auto', pos='330px 0', shade=(30, 50)),
    'tafat': dict(brand='Tafat <span style="font-family:\'Noto Sans Tifinagh\'">ⵜⴰⴼⴰⵜ</span>', display="'Bricolage Grotesque'", font_brand="800", accent='#FFC53D',
                  ink='#FFFFFF', paper='#0E4A57', fonts='tafat', big_style='800', side='left', bg='1400px auto', pos='-140px -34px', shade=(30, 52)),
    'nacre': dict(brand='Atelier <b>Nacre</b>', display="'Gloock'", font_brand="400", accent='#5B0E22', ink='#1F1418', paper='#F6F2F1',
                  fonts='nacre', big_style='400', side='right', bg='175% auto', pos='14% 44%', shade=(40, 66)),
}
# Lalla Warda est en WebGL : sa capture (thumbs-work/warda.png) vient de youtube/lalla-warda/capture.py, avec le GPU
STYLE['warda'] = dict(brand='Lalla <i>Warda</i>', display="'Instrument Serif'", font_brand="400", accent='#B23F66', ink='#2E1620', paper='#FBF3EF',
                      fonts='warda', big_style='400', side='left', bg='1380px auto', pos='170px -20px', shade=(30, 54))
# Tiziri : même chose (studio 3D) ; sa capture vient de youtube/tiziri/capture.py, qui compose aussi ses miniatures.
# Mêmes polices que Lalla Warda (Instrument Serif, Geist, Amiri, IBM Plex Sans Arabic).
STYLE['tiziri'] = dict(brand='Tiziri <span style="font-family:\'Amiri\';font-size:40px">تيزيري</span>', display="'Instrument Serif'", font_brand="400",
                       accent='#B4532F', ink='#1C1714', paper='#EFE7DA', fonts='warda', big_style='400', side='left', bg='1824px auto',
                       pos='-455px -40px', shade=(45, 61))
DIR = {'billot': 'maison-billot', 'tafat': 'tafat', 'nacre': 'atelier-nacre', 'warda': 'lalla-warda', 'tiziri': 'tiziri'}


def capture():
    """Capture 1920 × 1080 du moment fort de chaque site (version française : le texte du site y est court)."""
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    c.call('Page.enable'); c.call('Runtime.enable')
    c.call('Emulation.setDeviceMetricsOverride', {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1, 'mobile': False})
    for pid, (page, js) in SHOTS.items():
        c.call('Page.navigate', {'url': BASE + page})
        c.pump(4)
        c.eval("document.documentElement.style.scrollBehavior = 'auto'")
        c.eval(js)
        c.pump(3.5)
        c.eval("document.querySelectorAll('.nav, header.nav, #nav, .scroll-hint, .hero-copy, .hero-hint, .ana-hint, .ana-total, .anat-head').forEach(e => e.style.visibility = 'hidden')")
        c.pump(.5)
        data = base64.b64decode(c.call('Page.captureScreenshot', {'format': 'png'})['data'])
        open(WORK / f'{pid}.png', 'wb').write(data)
        print('capture', pid)
    c.close()


def html(pid, lang):
    big, word, pill = TEXT[pid][lang]
    s = STYLE[pid]
    rtl = lang == 'ar'
    fonts = open(ROOT / '_fonts' / s['fonts'] / 'fonts.css', encoding='utf-8').read().replace('../fonts/', 'fonts/')
    side = 'right' if (s['side'] == 'right') else 'left'
    shade = f"linear-gradient({'270deg' if side == 'right' else '90deg'}, {s['paper']} 0%, {s['paper']}F5 {s['shade'][0]}%, {s['paper']}00 {s['shade'][1]}%)"
    big_html = f'<div class="big">{big}</div>' if big else ''
    arabic = "font-family:'Noto Sans Arabic','Geeza Pro',sans-serif;" if rtl else ''
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
* {{ margin:0; box-sizing:border-box }}
body {{ width:1280px; height:720px; overflow:hidden; background:{s['paper']}; font-family:{s['display']},serif }}
.bg {{ position:absolute; inset:0; background:url({pid}.png) no-repeat; background-size:{s['bg']}; background-position:{s['pos']} }}
.shade {{ position:absolute; inset:0; background:{shade} }}
.txt {{ position:absolute; top:0; bottom:0; {side}:64px; width:{'470px' if rtl and side == 'left' else '600px'}; display:flex; flex-direction:column; justify-content:center; {'align-items:flex-end;text-align:right;' if side == 'right' else ''} }}
.pill {{ align-self:{'flex-end' if side == 'right' else 'flex-start'}; font:700 26px/1 system-ui,sans-serif; letter-spacing:.04em; text-transform:uppercase; color:#fff; background:{s['accent'] if pid != 'tafat' else '#0A3842'};
  {'color:#0A3842;background:#FFC53D;' if pid == 'tafat' else ''} padding:14px 22px; border-radius:999px; margin-bottom:26px; {arabic} }}
.big {{ font:{s['big_style']} 300px/.8 {s['display']},serif; color:{s['accent'] if pid != 'tafat' else '#FFC53D'}; letter-spacing:-.04em }}
.word {{ font:{s['big_style']} {'130px' if big else '112px'}/.92 {s['display']},serif; color:{s['ink']}; text-transform:{'uppercase' if pid == 'billot' else 'none'}; letter-spacing:-.02em; {arabic} {'font-weight:800;' if rtl else ''}
  {'text-shadow:0 4px 30px rgba(0,0,0,.35);' if pid == 'tafat' else ''} }}
.brand {{ margin-top:30px; font:{s['font_brand']} 46px/1 {s['display']},serif; color:{s['ink']}; opacity:.92 }}
</style></head><body{' dir="rtl"' if rtl else ''}><div class="bg"></div><div class="shade"></div>
<div class="txt"><div class="pill">{pill}</div>{big_html}<div class="word">{word}</div><div class="brand">{s['brand']}</div></div></body></html>"""


def render():
    srv, origin = serve(str(WORK))
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    c.call('Page.enable'); c.call('Runtime.enable')
    c.call('Emulation.setDeviceMetricsOverride', {'width': 1280, 'height': 720, 'deviceScaleFactor': 1, 'mobile': False})
    for pid, langs in TEXT.items():
        for lang in langs:
            name = f'{pid}-{lang}.html'
            (WORK / name).write_text(html(pid, lang), encoding='utf-8')
            c.call('Page.navigate', {'url': origin + name})
            c.pump(1.5)
            c.eval('document.fonts.ready.then(() => true)')
            data = base64.b64decode(c.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 92})['data'])
            out = YT / DIR[pid] / 'out'
            out.mkdir(parents=True, exist_ok=True)
            path = out / f'{DIR[pid]}-miniature-{lang}.jpg'
            path.write_bytes(data)
            print(path.name, len(data) // 1024, 'Ko')
    c.close(); srv.shutdown()


if __name__ == '__main__':
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / 'fonts').mkdir(exist_ok=True)
    for name in ('billot', 'tafat', 'nacre', 'warda'):
        for f in (ROOT / '_fonts' / name).glob('*.woff2'):
            shutil.copy2(f, WORK / 'fonts' / f.name)
    if '--no-capture' not in sys.argv:
        capture()
    render()
