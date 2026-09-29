"""Prépare les éléments de la vidéo promo à partir du site (garde-robe, décor, polices) et du site exporté (captures).

python3 prep.py EXPORT [--site ../site] [--captures-only | --data-only]
  EXPORT : le dépôt public exporté (ex. ../../../publication/tiziri), servi en local sous /tiziri/ pour les captures.
Sorties (dossiers non suivis, recréés à la demande) :
  img/   photos habillées, photos prises en boutique, détourage, mannequin invisible, décor, mannequin nu
  vid/   vidéos des mannequins en marche, ré-encodées image par image (rendu déterministe au 1/30 s)
  fonts/ Instrument Serif et Geist (WOFF2)
  site/  captures du vrai site, téléphone et ordinateur, en FR, EN et ES (et l'accueil et une fiche en arabe)
"""
import base64, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '_tools').is_dir())
sys.path.insert(0, str(ROOT / '_tools'))
from check import CDP, serve  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith('--')]
EXPORT = Path(args[0]).resolve()
SITE = Path(sys.argv[sys.argv.index('--site') + 1] if '--site' in sys.argv else HERE.parent / 'site').resolve()
ITEMS = SITE / 'wardrobe/items'
# Les quatre vraies pièces de la boutique d'abord, puis les pièces de démonstration du site.
PIECES = ['pull-leopard', 'robe-maille-grise', 'gilet-long-beige', 'pantalon-gris',
          'robe-brodee-velours', 'blouson-cuir-marron', 'bomber-terracotta', 'veste-laine-brune',
          'perfecto-noir', 'chemise-blanche', 'robe-bustier-blanche', 'top-noir-sans-manches']
# La pièce qui montre le passage de la photo prise en boutique au détourage.
HERO = 'pull-leopard'


def ff(*a):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], check=True)


def assets():
    for d in ('img', 'vid', 'fonts'):
        if d == 'fonts' and not (SITE / 'node_modules').is_dir():  # polices déjà là (node_modules absent)
            continue
        shutil.rmtree(HERE / d, ignore_errors=True)
        (HERE / d).mkdir()
    for pid in PIECES:
        shutil.copy(ITEMS / pid / 'porte-face.jpg', HERE / 'img' / f'{pid}.jpg')
        # Une image clé par image : la composition se place à n'importe quel instant sans décoder ce qui précède.
        ff('-i', str(ITEMS / pid / 'video.mp4'), '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-g', '1',
           '-pix_fmt', 'yuv420p', '-map_metadata', '-1', str(HERE / 'vid' / f'{pid}.mp4'))
    shutil.copy(ITEMS / HERO / 'raw.jpg', HERE / 'img/photo-boutique.jpg')
    shutil.copy(ITEMS / HERO / 'cutout.png', HERE / 'img/detourage.png')
    for pid in PIECES[:4]:  # les vraies pièces : photo prise en boutique, mannequin invisible, pose de fin de marche
        shutil.copy(ITEMS / pid / 'raw.jpg', HERE / 'img' / f'{pid}-photo.jpg')
        shutil.copy(ITEMS / pid / 'ghost.jpg', HERE / 'img' / f'{pid}-ghost.jpg')
        end = ITEMS / pid / 'porte-hanche.jpg'  # Elle finit sa marche la main sur la hanche (comme sur le site)
        shutil.copy(end if end.exists() else ITEMS / pid / 'porte-face.jpg', HERE / 'img' / f'{pid}-fin.jpg')
    for f in ('studio-hero-large.jpg', 'studio-hero-tall.jpg', 'wall-portrait.jpg', 'wall-square.jpg'):
        shutil.copy(SITE / 'src/assets/decor' / f, HERE / 'img' / f)
    shutil.copy(SITE / 'wardrobe/brand/mannequins/elle-face.jpg', HERE / 'img/elle-face.jpg')
    shutil.copy(SITE / 'wardrobe/brand/mannequins/studio-vide.jpg', HERE / 'img/studio-vide.jpg')
    data()
    fonts = SITE / 'node_modules'
    for f in () if not fonts.is_dir() else ('@fontsource/instrument-serif/files/instrument-serif-latin-400-normal.woff2',
              '@fontsource/instrument-serif/files/instrument-serif-latin-ext-400-normal.woff2',
              '@fontsource/instrument-serif/files/instrument-serif-latin-400-italic.woff2',
              '@fontsource/instrument-serif/files/instrument-serif-latin-ext-400-italic.woff2',
              '@fontsource-variable/geist/files/geist-latin-wght-normal.woff2',
              '@fontsource-variable/geist/files/geist-latin-ext-wght-normal.woff2',
              '@fontsource/ibm-plex-sans-arabic/files/ibm-plex-sans-arabic-arabic-500-normal.woff2',
              '@fontsource/amiri/files/amiri-arabic-400-normal.woff2'):
        shutil.copy(fonts / f, HERE / 'fonts' / Path(f).name)


def data():
    """data.js : nom, couleurs, prix et cadrage de la vidéo de chaque pièce, lus dans la garde-robe."""
    from PIL import Image
    out = {}
    for pid in PIECES:
        it = json.load(open(ITEMS / pid / 'item.json', encoding='utf-8'))
        out[pid] = {'name': {k: it['name'][k] for k in ('fr', 'en', 'es', 'ar')}, 'price': it['price'],
                    'colors': [c['hex'] for c in it['colors']], 'box': it['video']['box'], 'duration': it['video']['duration'],
                    'still': list(Image.open(ITEMS / pid / 'porte-face.jpg').size),
                    'crop': it['pipeline']['crop'], 'raw': [it['pipeline']['rawSize']['width'], it['pipeline']['rawSize']['height']]}
    (HERE / 'data.js').write_text('// Écrit par prep.py à partir de la garde-robe du site.\nwindow.PIECES = ' + json.dumps(out, ensure_ascii=False) + ';\n', encoding='utf-8')


# Vues du site : (nom, page, section à amener à l'écran, décalage en px, attente en s)
MOBILE = [('hero', '', None, 0, 4), ('cabine', '', '[data-cabin]', -90, 6), ('defile', '', '#defile', 'pin', 5),
          ('garde-robe', '', '#garde-robe', 40, 3.5), ('piece', f'piece/{HERO}/', None, 0, 5.5), ('commander', '', '#commander', 0, 3)]
DESKTOP = [('hero', '', None, 0, 4), ('cabine', '', '[data-cabin-section]', 0, 6), ('defile', '', '#defile', 'pin', 5),
           ('piece', f'piece/{HERO}/', None, 0, 5.5)]
PREFIX = {'fr': '', 'en': 'en/', 'es': 'es/', 'ar': 'ar/'}
ONLY = {}  # toutes les vues dans les quatre langues (la promo arabe reprend toute la visite)


def captures():
    out = HERE / 'site'
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    tmp = Path(tempfile.mkdtemp())
    os.symlink(EXPORT, tmp / 'tiziri')  # le site vit sous /tiziri/, comme sur GitHub Pages
    srv, origin = serve(str(tmp))
    for kind, views, (W, H, dpr, mobile) in (('m', MOBILE, (390, 844, 2, True)), ('d', DESKTOP, (1440, 900, 1, False))):
        c = CDP()
        tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
        c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
        c.call('Emulation.setDeviceMetricsOverride', {'width': W, 'height': H, 'deviceScaleFactor': dpr, 'mobile': mobile})
        if mobile:
            c.call('Emulation.setTouchEmulationEnabled', {'enabled': True})
        for lang, pre in PREFIX.items():
            for name, page, sel, off, wait in views:
                if lang in ONLY and name not in ONLY[lang]:
                    continue
                c.call('Page.navigate', {'url': f'{origin}tiziri/{pre}{page}'})
                time.sleep(2.5)
                if sel:
                    if off == 'pin':  # au milieu du défilé épinglé
                        c.eval(f"(() => {{ const s = document.querySelector('{sel}'); const top = s.getBoundingClientRect().top + scrollY; const sp = s.parentElement; const dist = sp.classList.contains('pin-spacer') ? sp.offsetHeight - s.offsetHeight : 0; window.scrollTo(0, top + dist * .35); }})()")
                    else:
                        c.eval(f"window.scrollTo(0, document.querySelector('{sel}').getBoundingClientRect().top + scrollY + ({off}))")
                time.sleep(wait)
                data = c.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})['data']
                (out / f'{lang}-{kind}-{name}.jpg').write_bytes(base64.b64decode(data))
                print('capture', lang, kind, name, flush=True)
        c.close()
    srv.shutdown()
    shutil.rmtree(tmp)


if __name__ == '__main__':
    if '--data-only' in sys.argv:
        shutil.copy(SITE / 'wardrobe/brand/mannequins/studio-vide.jpg', HERE / 'img/studio-vide.jpg')
        data()
        sys.exit()
    if '--captures-only' not in sys.argv:
        assets()
    captures()
