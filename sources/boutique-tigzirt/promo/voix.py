"""Voix off de la vidéo promo : Gemini TTS (API Gemini, modèle et appels de youtube/tools/gemini_voice.py,
clé lue dans la variable d'environnement GEMINI_API_KEY), voix « Sulafat », une phrase par requête.

python3 voix.py            écrit voix/<langue>/NN.wav et voix/<langue>/voix.json (instant de départ de chaque phrase,
                           calé sur les scènes de compo.html, sans chevauchement) ; les réponses sont gardées dans voix/cache.
Puis : python3 audio.py --voix fr (etc.) : la musique baisse sous la voix ; promo_batch.py prend audio-voix-<langue>.wav.
"""
import json, os, sys, wave
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
# Instant (s) où chaque phrase commence, calé sur les scènes de compo.html (décalé si la phrase d'avant déborde).
T = [0.5, 5.1, 10.4, 19.7, 24.5, 34.1, 43.3, 47.0, 53.6]
STYLE = 'Warm, elegant and confident voice for a premium fashion boutique advert: smooth, natural and unhurried, with a clear pause between sentences; no laughter, no chuckles, no breaths between sentences.'
LIGNES = {
    'fr': ['Une photo, prise en boutique.',
           'On détoure la pièce, sans rien changer.',
           'Puis Elle, notre mannequin en bois, la porte… et la pièce prend vie.',
           'Tiziri. Votre boutique de mode à Tigzirt, en ligne.',
           'Chaque pièce de la boutique est présentée en mouvement.',
           'Sur le site : l’essayage, le défilé, et chaque pièce sous tous les angles.',
           'En français, en arabe, en anglais et en espagnol.',
           'Une pièce vous plaît ? Écrivez-nous sur WhatsApp : retrait en boutique ou livraison.',
           'Tiziri. Ce que vous voyez, vous le trouvez en boutique.'],
    'en': ['One photo, taken in the shop.',
           'We cut the piece out, changing nothing.',
           'Then Elle, our wooden mannequin, wears it… and the piece comes to life.',
           'Tiziri. Your fashion boutique in Tigzirt, online.',
           'Every piece in the shop is shown in motion.',
           'On the website: the fitting room, the runway, and every piece from every angle.',
           'In French, Arabic, English and Spanish.',
           'Like a piece? Message us on WhatsApp: collect it in store, or get it delivered.',
           'Tiziri. What you see here, you’ll find in the shop.'],
    'es': ['Una foto, hecha en la tienda.',
           'Recortamos la prenda, sin cambiar nada.',
           'Luego Elle, nuestra maniquí de madera, se la pone… y la prenda cobra vida.',
           'Tiziri. Tu tienda de moda en Tigzirt, en línea.',
           'Cada prenda de la tienda se presenta en movimiento.',
           'En la web: el probador, el desfile y cada prenda desde todos los ángulos.',
           'En francés, árabe, inglés y español.',
           '¿Te gusta una prenda? Escríbenos por WhatsApp: recógela en la tienda o te la enviamos.',
           'Tiziri. Lo que ves aquí, lo encuentras en la tienda.'],
    'ar': ['صورة واحدة، التُقطت في المتجر.',
           'نفرّغ القطعة، دون أن نغيّر فيها شيئًا.',
           'ثم ترتديها «إيل»، دميتنا الخشبية… فتنبض القطعة بالحياة.',
           'تيزيري. متجر الأزياء الخاص بكم في تيقزيرت، على الإنترنت.',
           'كل قطعة في المتجر تُعرض وهي في حركة.',
           'على الموقع: غرفة القياس، والعرض، وكل قطعة من جميع الزوايا.',
           'بالفرنسية والعربية والإنجليزية والإسبانية.',
           'أعجبتكم قطعة؟ راسلونا على واتساب: استلموها من المتجر أو نوصلها إليكم.',
           'تيزيري. ما ترونه هنا، تجدونه في المتجر.'],
}


ROOT = next(p for p in Path(__file__).resolve().parents if (p / '_tools').is_dir())
sys.path.insert(0, str(ROOT / 'youtube' / 'tools'))
import gemini_voice  # noqa: E402

VOICE = 'Sulafat'
# Un modèle par vidéo (donc par langue) ; l'offre gratuite compte 100 requêtes par jour et par modèle.
MODEL = {'fr': 'gemini-3.8-flash-tts', 'en': 'gemini-3.8-flash-tts', 'es': 'gemini-3.8-flash-tts', 'ar': 'gemini-3.8-flash-tts'}
# Consigne de jeu (non lue). Avec gemini-3.8-flash-lite-tts, n'en mettre aucune : Lite la prend pour un débit lent
# (une pause après presque chaque mot, 6 s au lieu de 2,2 s pour « One photo, taken in the shop. »).
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


for lang, lignes in LIGNES.items():
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
