"""Maison Billot présenté par Uko, la mascotte hoshuko : Uko entre sur la page, parle (bouche calée sur la voix Google),
regarde ce qu'il montre, se déplace vers les zones libres et fête la réservation. Même visite que make.py.

python3 uko.py fr [--test]    → out/maison-billot-uko-fr.mp4 et .srt
Le moteur d'Uko est celui du site officiel (uko-mascot.pages.dev), piloté image par image.
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent / 'tools'
sys.path.insert(0, str(TOOLS))
import music, narrate, visit  # noqa: E402

LANG = sys.argv[1]
TEST = '--test' in sys.argv
sys.argv = ['make.py', LANG]
spec = importlib.util.spec_from_file_location('billot', HERE / 'make.py')
billot = importlib.util.module_from_spec(spec); spec.loader.exec_module(billot)

ENGINE = 'https://uko-mascot.pages.dev/js/uko-mascot-engine.js'
SCRIPT = {
    'fr': ["Salut, moi c'est Uko ! Je t'emmène chez Maison Billot, boucher artisan à Lyon depuis 1987 : des bœufs maturés sur l'os et découpés devant toi.",
           'Regarde : du collier à la queue, vingt-trois morceaux, tous issus de bêtes nées, élevées et abattues en France.',
           'Pour chaque pièce, le boucher te dit tout : sa tendreté, comment la cuire, son conseil et le prix au kilo.',
           'Un barbecue, un pot-au-feu ? Dis ce que tu cuisines, et il te montre les bons morceaux.',
           "Merguez et saucisses sont faites maison chaque matin, sans rien cacher de ce qu'il y a dedans.",
           'En cave, les côtes mûrissent de trois à huit semaines : plus elles attendent, plus elles sont tendres et goûteuses.',
           'Et pour finir, tu commandes ton colis en ligne, tu choisis ton heure, et tu paies en boutique, au poids réel.',
           'Ce site de démonstration est gratuit et open source, en français, anglais et espagnol. Le lien est dans la description.',
           'Abonne-toi pour découvrir les prochains commerces. À bientôt !'],
}
VOICE = {'fr': ('Fenrir', '[cheerful] [playful] [energetic]')}   # voix Gemini d'Uko
HOLDS = {1: 1.1, 5: .2, 6: .9, 7: .8}
H, GROUND = 500, 1050          # hauteur de la boîte d'Uko et ligne des pieds (px, image 1920×1080)


def uko_steps(seg, tc):
    s = lambda i: seg[i]['start']
    e = lambda i: seg[i]['end']
    st = []
    u = lambda t, act, **k: st.append({'t': round(t, 3), 'do': 'uko', 'act': act, **k})
    # arrivée par la droite, puis coucou en disant bonjour
    u(.1, 'walk', x=1640, speed=2.4)
    u(s(0), 'state', pose='welcome')
    # la bête se découpe : Uko la regarde, puis se place à gauche du volet qui va s'ouvrir
    u(s(1) + .2, 'look', sel='.piece[data-id="onglet"]')
    u(s(1) + 2.6, 'walk', x=1130, speed=2)
    u(s(2) - .2, 'look', sel='.piece[data-id="onglet"]')
    u(s(2) + 1.2, 'look', xy=[1620, 430])
    # guide : Uko file vers la marge droite, puis regarde la bête qui s'allume
    u(e(2) - .2, 'look', xy=None)
    u(s(3) - .2, 'walk', x=1760, speed=2.4)
    u(s(3) + 3.2, 'look', xy=[700, 620])
    # fait maison : l'infographie occupe la droite, Uko passe sous le texte, à gauche
    u(s(4) - .4, 'walk', x=820, speed=2.6)
    u(s(4) + 3.9, 'look', xy=[1600, 520])
    # cave : retour dans la marge droite, les yeux sur le curseur
    u(s(5) - .3, 'walk', x=1750, speed=2.6)
    u(s(5) + 4.1, 'look', sel='#age-range')
    # colis : il suit les clics, puis saute de joie quand la réservation est prête
    u(s(6) + 1.0, 'look', sel='#presets .preset')
    u(s(6) + 3.3, 'look', sel='#colis-go')
    u(s(6) + 4.2, 'look', xy=None)
    u(s(6) + 4.25, 'state', pose='success')
    # langues : il regarde le sélecteur, puis la caméra
    u(s(7) + .1, 'look', sel='.lang-switch a[hreflang="en"]')
    u(s(7) + 2.7, 'look', xy=None)
    u(s(7) + 2.8, 'walk', x=1180, speed=2.4)
    # carte de fin : couleurs claires sur le vert, Uko se place à droite du texte et salue
    u(tc, 'theme', theme='dark')
    u(tc, 'brand', color='#2E6A55')
    u(s(8) + .1, 'state', pose='welcome')
    return st


def main():
    out, work = HERE / 'out', HERE / 'work'
    out.mkdir(exist_ok=True); work.mkdir(exist_ok=True)
    print('voix :', visit.use_voice(VOICE[LANG]), flush=True)
    seg = narrate.timeline(SCRIPT[LANG], LANG, str(work), lead=3.0, holds=HOLDS)
    p = billot.plan(seg)
    tc = seg[7]['end'] + .5
    p['duration'] = round(max(p['duration'], seg[8]['end'] + 1.6), 2)
    if TEST:
        p['duration'] = min(p['duration'], seg[2]['end'] + .5)
    keep = [s for s in seg if s['start'] < p['duration']]
    p['steps'] += uko_steps(seg, tc)
    p['mascot'] = {'engine': ENGINE, 'height': H, 'ground': GROUND, 'x': 2100, 'hair': 'original',
                   'mouth': narrate.mouth(keep, p['duration'])}
    stem = f'maison-billot-uko-{LANG}' + ('-test' if TEST else '')
    plan_path = work / f'plan-uko-{LANG}.json'
    json.dump(p, open(plan_path, 'w', encoding='utf-8'), ensure_ascii=False)
    video = work / f'{stem}-image.mp4'
    subprocess.run([sys.executable, str(TOOLS / 'tour.py'), billot.URL, str(plan_path), str(video)], check=True)
    bed = work / f'musique-{int(p["duration"])}.wav'
    if not bed.exists():
        music.write_wav(str(bed), music.bed('billot', p['duration']))
    mixed = work / f'{stem}-son.wav'
    narrate.mix(keep, str(bed), p['duration'], str(mixed))
    final = out / f'{stem}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(video), '-i', str(mixed), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                    '-map_metadata', '-1', str(final)], check=True)
    narrate.srt(keep, str(out / f'{stem}.srt'))
    print('vidéo', final, round(p['duration'], 1), 's')


if __name__ == '__main__':
    main()
