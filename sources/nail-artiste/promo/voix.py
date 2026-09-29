"""Voix off de la vidéo promo Atelier Nacre : Gemini TTS (modèle et appels de youtube/tools/gemini_voice.py,
clé lue dans la variable d'environnement GEMINI_API_KEY), voix « Despina » (femme, voix douce), une phrase par requête.

python3 voix.py [ar fr en es]   écrit voix/<langue>/NN.wav et voix/<langue>/voix.json (instant de départ de chaque phrase,
                                calé sur les scènes de compo.html, sans chevauchement) ; réponses gardées dans voix/cache.
Puis : python3 audio.py nacre --voix ar (etc.) : la musique baisse sous la voix ; promo_batch.py prend audio-voix-<langue>.wav.
"""
import json, os, sys, wave
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
# Instant (s) où chaque phrase commence, calé sur les scènes de compo.html (décalé si la phrase d'avant déborde) :
# 1 une pose · 2 la marque · 3 la couleur · 4 la forme · 5 la galerie · 6 l'hygiène · 7 la carte · 8 réservation.
T = [0.6, 5.0, 9.5, 19.9, 27.3, 38.0, 44.6, 52.1]
STYLE = 'Soft, warm and reassuring voice for a nail studio advert: unhurried, natural, with a clear pause between sentences; no laughter, no chuckles, no breaths between sentences.'
LIGNES = {
    'fr': ['Une pose, six couches.',
           'Atelier Nacre. Prothésiste ongulaire, à Bordeaux.',
           'Essayez chaque couleur, directement sur l’ongle.',
           'Carré, ovale, amande… choisissez la forme qui va à vos mains.',
           'Les poses de la semaine, pour vous inspirer.',
           'L’hygiène d’abord : instruments stérilisés, limes neuves pour chaque cliente.',
           'Une carte claire : gel, semi-permanent ou rallongement, prix affichés.',
           'Atelier Nacre. Réservez votre rendez-vous sur Planity.'],
    'en': ['One set, six layers.',
           'Atelier Nacre. Nail technician, in Bordeaux.',
           'Try every colour, right on the nail.',
           'Square, oval, almond… pick the shape that suits your hands.',
           'This week’s sets, for inspiration.',
           'Hygiene first: sterilised tools, and new files for every client.',
           'A clear price list: gel, semi-permanent or extensions, prices shown.',
           'Atelier Nacre. Book your appointment on Planity.'],
    'es': ['Una uña, seis capas.',
           'Atelier Nacre. Manicurista profesional, en Burdeos.',
           'Prueba cada color, directamente sobre la uña.',
           'Cuadrada, ovalada, almendra… elige la forma que va con tus manos.',
           'Los trabajos de la semana, para inspirarte.',
           'La higiene primero: instrumentos esterilizados y limas nuevas para cada clienta.',
           'Una carta clara: gel, semipermanente o extensión, con los precios a la vista.',
           'Atelier Nacre. Reserva tu cita en Planity.'],
    'ar': ['طلاءٌ واحد، ستُّ طبقات.',
           'أتيليه ناكر. خبيرة تجميل الأظافر، في بوردو.',
           'جرّبي كل لون، مباشرةً على الظفر.',
           'مربّع، بيضاوي، لوزي… اختاري الشكل الذي يناسب يديك.',
           'أعمال الأسبوع، لتستلهمي منها.',
           'النظافة أولًا: أدوات معقّمة، ومبارد جديدة لكل زبونة.',
           'قائمة واضحة: جل، أو شبه دائم، أو تطويل، والأسعار معلنة.',
           'أتيليه ناكر. احجزي موعدك على بلانيتي.'],
}

ROOT = next(p for p in Path(__file__).resolve().parents if (p / '_tools').is_dir())
sys.path.insert(0, str(ROOT / 'youtube' / 'tools'))
import gemini_voice  # noqa: E402

VOICE = 'Despina'
# Un modèle par vidéo (donc par langue). Consigne de jeu entre crochets : pas avec gemini-3.8-flash-lite-tts (débit ralenti).
MODEL = {'fr': 'gemini-3.8-flash-tts', 'en': 'gemini-3.8-flash-tts', 'es': 'gemini-3.8-flash-tts', 'ar': 'gemini-3.8-flash-tts'}
TAGS = {'fr': '', 'en': '', 'es': '', 'ar': ''}  # aucune consigne entre crochets : 3.8 Flash les lit parfois à voix haute


def duration(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def layout(lang, lignes, speed):
    """Écrit les phrases (à la vitesse donnée) et renvoie leur plan, ou None si la dernière finit après 59,2 s."""
    d = os.path.join(HERE, 'voix', lang)
    os.makedirs(d, exist_ok=True)
    plan, end = [], 0
    for i, (t, texte) in enumerate(zip(T, lignes), 1):
        out = os.path.join(d, f'{i:02d}.wav')
        gemini_voice.tts(texte, lang, out, os.path.join(HERE, 'voix', 'cache'), speed=speed, voice=VOICE, style=TAGS[lang], model=MODEL[lang])
        dur = duration(out)
        t = round(max(t, end + .3), 2)
        end = t + dur
        plan.append({'t': t, 'fichier': f'{i:02d}.wav', 'texte': texte, 'duree': round(dur, 2)})
    return plan if end < 59.2 else None


for lang in (sys.argv[1:] or LIGNES):
    lignes = LIGNES[lang]
    # si la voix déborde de la minute, on l'accélère un peu (les réponses sont en cache : aucune requête de plus)
    for speed in (1.0, 1.04, 1.08):
        plan = layout(lang, lignes, speed)
        if plan:
            break
    else:
        raise SystemExit(f'{lang} : la voix dépasse 59,2 s même à 1,08×')
    json.dump({'voix': f'Gemini TTS ({MODEL[lang]}), voix {VOICE}', 'consigne': TAGS[lang], 'style': STYLE, 'vitesse': speed, 'lignes': plan},
              open(os.path.join(HERE, 'voix', lang, 'voix.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, f'{speed}×', ' '.join(f"{p['t']}+{p['duree']}" for p in plan), flush=True)
