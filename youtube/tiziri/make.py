"""Tiziri : visite commentée du site en ligne → out/tiziri-visite-<langue>.mp4 et sous-titres .srt.

python3 youtube/tiziri/make.py fr [--test]
Voix Gemini (clé GEMINI_API_KEY), musique dans l'harmonie de la vidéo promo, capture avec le GPU (studio 3D)
et vidéos des mannequins ralenties au rythme de la page (gpu/tour.py).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import visit  # noqa: E402
import music  # noqa: E402

# voix Gemini (tools/gemini_voice.py), une par langue en alternant femme et homme ; un seul modèle par vidéo ;
# en français, Sulafat, la voix de la vidéo promo de Tiziri. La consigne entre crochets n'est pas lue ; avec
# gemini-3.8-flash-lite-tts, n'en mettre aucune : Lite la prend pour un débit lent (une pause après presque chaque mot).
# Toutes les langues en 3.8 Flash (clé payante) ; Flash Lite seulement en secours, sans consigne.
MODEL, LITE = 'gemini-3.8-flash-tts', 'gemini-3.8-flash-lite-tts'
VOICE = {'fr': ('Sulafat', '', MODEL),      # femme, voix chaude
         'en': ('Umbriel', '', MODEL),                  # homme, voix posée
         'es': ('Callirrhoe', '', MODEL),         # femme, voix souple
         'ar': ('Sadaltager', '', MODEL)}              # homme, voix claire

# la musique de la promo (sources/boutique-tigzirt/promo/audio.py) : la mineur harmonique, corde pincée comme une mandole
music.STYLES['tiziri'] = dict(bpm=96, lead='ks', prog=[([57, 64, 69, 72, 76, 72, 69, 64], [45, 52, 57, 60], 45),
                                                       ([53, 60, 65, 69, 72, 69, 65, 60], [41, 48, 53, 57], 41),
                                                       ([50, 57, 62, 65, 69, 65, 62, 57], [38, 45, 50, 53], 38),
                                                       ([52, 59, 64, 68, 71, 68, 64, 59], [40, 47, 52, 56], 40)])
visit.TOOLS = HERE / 'gpu'

LANG = sys.argv[1]
BASE = 'https://hoshuko.github.io/tiziri/'
URL = BASE if LANG == 'fr' else f'{BASE}{LANG}/'

SCRIPT = {
    'fr': ["Tiziri, c'est une boutique de mode à Tigzirt, en Kabylie, et toute sa garde-robe en ligne.",
           "Elle et Lui, nos mannequins en bois, portent chaque pièce.",
           "Chaque vêtement est photographié en boutique, puis détouré et mis en lumière, sans rien changer.",
           "Dans la cabine, vous choisissez une pièce : ils l'essaient, puis se mettent en marche.",
           "Autour, la mascotte garde une tenue de base écru, jamais vendue : la pièce reste la vedette.",
           "Au défilé, toute la boutique passe, pièce après pièce.",
           "La garde-robe se trie en un geste : robes, hauts, vestes, bas ou traditionnel.",
           "Glissez : photo brute ou mise en scène, c'est la même pièce, celle que vous trouvez en boutique.",
           "Une pièce vous plaît ? Un message sur WhatsApp : retrait en boutique, ou livraison dans les 58 wilayas, payée à la réception.",
           "Tiziri, la boutique prend vie. Ce site de démonstration est gratuit et open source, en français, en arabe, en anglais et en espagnol. Le lien est dans la description."],
    'en': ["Tiziri is a fashion boutique in Tigzirt, in Kabylie, with its whole wardrobe online.",
           "Elle and Lui, our wooden mannequins, wear every piece.",
           "Every garment is photographed in the shop, then cut out and set in the light, without changing a thing.",
           "In the fitting room, you pick a piece: they try it on, then start walking.",
           "Around it, the mascot keeps a plain ecru base outfit, never for sale: the piece stays the star.",
           "On the runway, the whole shop goes by, piece after piece.",
           "The wardrobe sorts itself in one tap: dresses, tops, jackets, bottoms or traditional.",
           "Slide: raw photo or staging, it's the same piece, the one you'll find in the shop.",
           "Like a piece? Send a WhatsApp message: pick it up in the shop, or get it delivered to any of the 58 provinces, and pay on delivery.",
           "Tiziri: the shop comes alive. This demo website is free and open source, in French, Arabic, English and Spanish. The link is in the description."],
    'es': ["Tiziri es una tienda de moda en Tigzirt, en Cabilia, con todo su armario en línea.",
           "Elle y Lui, nuestros maniquíes de madera, llevan cada prenda.",
           "Cada prenda se fotografía en la tienda, y luego se recorta y se pone bajo la luz, sin cambiar nada.",
           "En el probador, eliges una prenda: se la prueban y echan a andar.",
           "Alrededor, el maniquí lleva una ropa básica de color crudo, que no está a la venta: la protagonista es la prenda.",
           "En el desfile pasa toda la tienda, prenda tras prenda.",
           "El armario se ordena con un gesto: vestidos, tops, chaquetas, pantalones o tradicional.",
           "Desliza: foto original o puesta en escena, es la misma prenda, la que encuentras en la tienda.",
           "¿Te gusta una prenda? Escríbenos por WhatsApp: recógela en la tienda o te la enviamos a cualquiera de las 58 provincias, con pago contra reembolso.",
           "Tiziri: la tienda cobra vida. Esta web de demostración es gratuita y de código abierto, en francés, árabe, inglés y español. El enlace está en la descripción."],
    'ar': ["تيزيري محلّ أزياء في تيقزيرت، بمنطقة القبائل، وخزانة ملابسه كلّها على الإنترنت.",
           "«هي» و«هو»، عارضانا الخشبيان، يلبسان كل قطعة.",
           "كل قطعة تُصوَّر في المحل، ثم تُفصل عن الخلفية وتوضع تحت الضوء، دون أي تغيير.",
           "في غرفة القياس، تختارون قطعة: يجرّبانها، ثم ينطلقان في المشي.",
           "حولها، يرتدي المجسّم لباساً أساسياً بلون العاج، غير معروض للبيع: القطعة هي النجمة.",
           "في عرض الأزياء يمرّ المحل كلّه، قطعة بعد قطعة.",
           "خزانة الملابس تُفرز بلمسة واحدة: فساتين، قمصان، جاكيتات، سراويل أو تقليدي.",
           "مرّروا: الصورة الأصلية أو العرض، إنها القطعة نفسها، التي تجدونها في المحل.",
           ("أعجبتكم قطعة؟ رسالة على WhatsApp تكفي: استلموها من المحل، أو نوصلها إلى أي ولاية من الولايات الثماني والخمسين، والدفع عند الاستلام.",
            "أعجبتكم قطعة؟ رسالة على واتساب تكفي: استلموها من المحل، أو نوصلها إلى أي ولاية من الولايات الثماني والخمسين، والدفع عند الاستلام."),
           "تيزيري: المحل ينبض بالحياة. موقع العرض هذا مجاني ومفتوح المصدر، بالفرنسية والعربية والإنجليزية والإسبانية. الرابط في الوصف."],
}
CARD = {'fr': ('Site gratuit · open source', 'Démo en ligne et code sur GitHub'), 'en': ('Free · open source', 'Live demo and code on GitHub'),
        'es': ('Web gratuita · código abierto', 'Demo en línea y código en GitHub'), 'ar': ('موقع مجاني · مفتوح المصدر', 'العرض والكود على GitHub')}
PLACE = {'fr': 'Tigzirt · Kabylie', 'en': 'Tigzirt · Kabylie', 'es': 'Tigzirt · Cabilia', 'ar': 'تيقزيرت · القبائل'}


def endcard(lang):
    kicker, line = CARD[lang]
    d = ' dir="rtl"' if lang == 'ar' else ''
    # dir="ltr" : sur la page arabe (dir="rtl"), la carte garderait sinon son texte collé au bord droit
    return f"""<div dir="ltr" style="position:absolute;inset:0;background:radial-gradient(120% 95% at 18% 32%,#1D5A70 0%,#11394A 58%,#0A2430 100%);color:#EFE7DA;display:flex;align-items:center;padding:0 0 0 130px">
<div style="max-width:900px">
<p{d} style="font:600 22px/1 'Geist Variable','IBM Plex Sans Arabic',sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#FFD79C;margin:0 0 30px;text-align:left">{kicker}</p>
<p style="font:400 150px/1 'Instrument Serif',serif;margin:0;letter-spacing:-.01em">Tiziri <span style="font:400 76px/1 'Amiri',serif;color:#FFD79C;vertical-align:middle">تيزيري</span></p>
<p{d} style="font:{"400 40px/1.3 'Amiri'" if lang == 'ar' else "italic 400 44px/1.2 'Instrument Serif'"},serif;margin:18px 0 0;color:#D9794F;text-align:left">{PLACE[lang]}</p>
<p{d} style="font:500 32px/1.4 'Geist Variable','IBM Plex Sans Arabic',sans-serif;margin:34px 0 0;color:rgba(239,231,218,.84);text-align:left">{line}</p>
<p style="font:600 36px/1.55 'Geist Variable',sans-serif;margin:18px 0 0">hoshuko.github.io<br>github.com/hoshuko</p>
</div></div>"""


PIECE = '[data-cabin-pick="1"]'            # le pull léopard : porté avec la tenue de base écru
DEFILE = '.pin-spacer:has(> #defile)'      # la section épinglée et toute sa course horizontale
COMPARE = 'section:has(> [data-compare])'


def plan(seg, lang):
    s = lambda i: seg[i]['start']
    e = lambda i: seg[i]['end']
    st = []
    add = lambda **k: st.append(k)
    # 0 : le studio 3D ; on laisse la caméra finir son entrée sur le grain du bois
    # 1 : la caméra s'approche d'Elle et Lui
    add(t=s(1) - .2, d=e(1) - s(1) + .4, do='scroll', to={'sel': '#accueil', 'p': 1})
    # 2 : la métamorphose, en trois temps comme la phrase : la photo prise en boutique (01), détourée (02),
    # puis mise en lumière (03) ; p = part du parcours épinglé où chaque étape est terminée
    L = e(2) - s(2)
    add(t=s(2) - .4, d=.38 * L + .4, do='scroll', to={'sel': '#metamorphose', 'p': .12})
    add(t=s(2) + .38 * L, d=.3 * L, do='scroll', to={'sel': '#metamorphose', 'p': .53})
    add(t=s(2) + .68 * L, d=.32 * L + .9, do='scroll', to={'sel': '#metamorphose', 'p': 1})
    # 3-4 : la cabine ; on choisit le pull léopard : balayage, la pièce se dépose, le mannequin marche,
    # puis reprend ses poses avec l'étiquette « La pièce » et la tenue de base adoucie
    add(t=s(3) - .5, d=1.2, do='scroll', to={'sel': '[data-cabin]', 'offset': -6})
    add(t=s(3) + .6, d=.5, do='cursor', sel=PIECE)
    add(t=s(3) + 1.15, do='click', sel=PIECE)
    add(t=s(3) + 2.2, d=.4, do='hide')
    # 5 : le défilé : la rangée glisse pendant que chaque mannequin se met en marche (jusqu'à l'étape suivante)
    add(t=s(5) - .4, d=1.0, do='scroll', to={'sel': DEFILE, 'offset': 0})
    add(t=s(5) + .7, d=s(6) - s(5) - 1.1, do='scroll', to={'sel': DEFILE, 'p': 1})
    # 6 : la garde-robe et ses filtres ; entre deux filtres, la grille a le temps de se vider puis de se remplir
    add(t=s(6) - .3, d=1.2, do='scroll', to={'sel': '#garde-robe', 'offset': 0})
    gap = min(2.0, max(1.4, (s(7) - s(6) - 2.7) / 2))
    for j, f in enumerate(('robes', 'vestes', '*')):
        t = s(6) + .9 + j * gap
        add(t=t, d=.45, do='cursor', sel=f'[data-filter="{f}"]')
        add(t=t + .5, do='click', sel=f'[data-filter="{f}"]')
    add(t=t + 1.2, d=.4, do='hide')
    # 7 : avant / après ; en arrivant, le site fait lui-même un aller-retour (3,4 s) pour montrer qu'on peut glisser,
    # puis on reprend la poignée (au rythme du temps qui reste) : la pièce ne change pas
    add(t=s(7) - .3, d=1.2, do='scroll', to={'sel': COMPARE, 'offset': -52})
    t = s(7) + 3.4
    add(t=t, d=.5, do='cursor', sel='[data-compare]', off=[.5, .55])
    t += .6
    k = max(.6, min(1, (s(8) - .4 - t) / 3.3))
    for a, b, x, d in ((50, 22, .22, .9), (22, 78, .78, 1.2), (78, 50, .5, .7)):
        add(t=t, d=d * k, do='range', sel='[data-compare] input[type=range]', **{'from': a, 'to': b})
        add(t=t, d=d * k, do='cursor', sel='[data-compare]', off=[x, .55])
        t += (d + .25) * k
    # 8 : commander sur WhatsApp
    add(t=s(8) - .3, d=1.3, do='scroll', to={'sel': '#commander', 'offset': -40})
    add(t=s(8) + 1.2, d=.6, do='cursor', sel='#commander .btn-wa')
    # 9 : retour au studio (« la boutique prend vie »), les quatre langues, puis la carte de fin
    add(t=s(9) - .2, d=.3, do='hide')
    add(t=s(9) - .1, d=0, do='scroll', to={'y': 0})
    k = s(9) + (e(9) - s(9)) * .45
    for j, l in enumerate(('ar', 'en', 'es')):
        add(t=k + j * .8, d=.6, do='cursor', sel=f'header a.lang[hreflang="{l}"]')
    tc = e(9) + .5
    add(t=tc, d=.7, do='card', html=endcard(lang))
    return {'duration': round(tc + .7 + 5.8, 2), 'steps': st}


if __name__ == '__main__':
    visit.run('tiziri', HERE, LANG, URL, SCRIPT, plan, 'tiziri', {0: .9, 1: .3, 2: .6, 3: 1.2, 4: 1.2, 5: 2.0, 6: 1.0, 7: 1.3},
              test='--test' in sys.argv, subtitle_langs=('en', 'es', 'ar') if LANG == 'fr' else (), voice=VOICE[LANG])
