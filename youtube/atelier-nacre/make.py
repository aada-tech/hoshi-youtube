"""Vidéo YouTube commentée d'Atelier Nacre : visite du site en ligne, voix off Google, musique, sous-titres (FR, EN, ES, AR).

python3 make.py fr|en|es|ar [--test]    → out/atelier-nacre-visite-<langue>.mp4 et .srt
(la version arabe montre le site en français : le site n'a pas de version arabe)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import visit  # noqa: E402

LANG = sys.argv[1]
URL = {'fr': 'https://hoshuko.github.io/atelier-nacre/', 'en': 'https://hoshuko.github.io/atelier-nacre/en.html',
       'es': 'https://hoshuko.github.io/atelier-nacre/es.html', 'ar': 'https://hoshuko.github.io/atelier-nacre/'}[LANG]

SCRIPT = {
    'fr': ['Atelier Nacre, prothésiste ongulaire à Bordeaux : gel, semi-permanent et nail art, une cliente à la fois.',
           'Chaque pose se construit en six couches, de la préparation à la brillance, pour tenir trois à quatre semaines sans un éclat.',
           'Vous hésitez sur la couleur ? Essayez les teintes du nuancier sur une main, avant même de venir.',
           "Brillant, mat, chrome ou pailleté : c'est la finition qui fait la différence.",
           'Carré, amande ou stiletto : on vous conseille la forme qui va à vos mains.',
           'Laissez-vous inspirer par les poses de la semaine, et consultez la carte, avec le prix et la durée de chaque prestation.',
           "Réservez en ligne en quelques secondes, sans acompte, avec annulation gratuite jusqu'à vingt-quatre heures avant.",
           'Atelier Nacre, des ongles beaux et solides, pour longtemps. Ce site de démonstration est gratuit et open source, en français, anglais et espagnol. Le lien est dans la description.'],
    'en': ['Atelier Nacre, a nail studio in Bordeaux: gel, gel polish and nail art, one client at a time.',
           'Every set is built in six layers, from prep to shine, to last three to four weeks without a single chip.',
           "Can't decide on a colour? Try the shades from our colour chart on a hand, before you even come in.",
           'Gloss, matte, chrome or glitter: the finish makes all the difference.',
           "Square, almond or stiletto: we'll help you pick the shape that suits your hands.",
           "Get inspired by this week's sets, and check the menu, with the price and length of every service.",
           'Book online in seconds, with no deposit and free cancellation up to twenty-four hours before.',
           'Atelier Nacre: beautiful, strong nails that last. This demo website is free and open source, in French, English and Spanish. The link is in the description.'],
    'es': [('Atelier Nacre, estudio de uñas en Burdeos: gel, esmaltado semipermanente y nail art, una clienta cada vez.',
            'Atelié Nacre, estudio de uñas en Burdeos: gel, esmaltado semipermanente y nail art, una clienta cada vez.'),
           'Cada manicura se construye en seis capas, de la preparación al brillo, para durar de tres a cuatro semanas sin un desconchón.',
           '¿Dudas con el color? Prueba los tonos de la carta sobre una mano, antes incluso de venir.',
           'Brillo, mate, cromado o purpurina: el acabado marca la diferencia.',
           'Cuadrada, almendra o stiletto: te aconsejamos la forma que mejor va con tus manos.',
           'Inspírate con las manicuras de la semana y consulta la carta, con el precio y la duración de cada servicio.',
           'Reserva en línea en segundos, sin señal y con cancelación gratuita hasta veinticuatro horas antes.',
           ('Atelier Nacre: uñas bonitas y resistentes que duran. Esta web de demostración es gratuita y de código abierto, en francés, inglés y español. El enlace está en la descripción.',
            'Atelié Nacre: uñas bonitas y resistentes que duran. Esta web de demostración es gratuita y de código abierto, en francés, inglés y español. El enlace está en la descripción.')],
    'ar': [('Atelier Nacre، صالون لتجميل الأظافر في بوردو: جل، وطلاء شبه دائم، وفن الأظافر، لزبونة واحدة في كل مرة.',
            'أتولييه ناكر، صالون لتجميل الأظافر في بوردو: جل، وطلاء شبه دائم، وفن الأظافر، لزبونة واحدة في كل مرة.'),
           'يُبنى كل طلاء على ست طبقات، من التحضير إلى اللمعان، ليدوم من ثلاثة إلى أربعة أسابيع دون أي تقشّر.',
           'محتارة في اختيار اللون؟ جرّبي درجات الألوان على صورة يد، حتى قبل أن تأتي.',
           'لامع أو مطفأ أو كروم أو بالبريق: اللمسة النهائية تصنع الفرق.',
           'مربّع أو لوزي أو ستيليتو: ننصحك بالشكل الذي يناسب يديك.',
           'استلهمي من تصاميم الأسبوع، واطّلعي على قائمة الخدمات مع سعر كل خدمة ومدتها.',
           'احجزي عبر الإنترنت في ثوانٍ، دون عربون، مع إلغاء مجاني حتى أربع وعشرين ساعة قبل الموعد.',
           ('Atelier Nacre، أظافر جميلة وقوية تدوم طويلًا. هذا الموقع التجريبي مجاني ومفتوح المصدر، بالفرنسية والإنجليزية والإسبانية. الرابط في الوصف.',
            'أتولييه ناكر، أظافر جميلة وقوية تدوم طويلًا. هذا الموقع التجريبي مجاني ومفتوح المصدر، بالفرنسية والإنجليزية والإسبانية. الرابط في الوصف.')],
}
# voix Gemini : une par langue, en alternant voix d'homme et de femme
VOICE = {'fr': ('Vindemiatrix', ''), 'en': ('Puck', ''),
         'es': ('Despina', ''), 'ar': ('Rasalgethi', '')}
CARD = {'fr': ('Site gratuit · open source', 'Démo en ligne et code sur GitHub'), 'en': ('Free · open source', 'Live demo and code on GitHub'),
        'es': ('Web gratuita · código abierto', 'Demo en línea y código en GitHub'), 'ar': ('موقع مجاني · مفتوح المصدر', 'العرض والكود على GitHub')}


def endcard(lang):
    kicker, line = CARD[lang]
    ar = ' dir="rtl"' if lang == 'ar' else ''
    af = "font-family:'Geeza Pro','Noto Sans Arabic',sans-serif;text-align:left;letter-spacing:0;" if lang == 'ar' else ''
    return f"""<div style="position:absolute;inset:0;background:radial-gradient(120% 95% at 18% 32%,#FFFFFF 0%,#F6F2F1 55%,#EEE6E4 100%);color:#1F1418;display:flex;align-items:center;padding:0 0 0 130px">
<div style="max-width:880px">
<p{ar} style="font:500 22px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#5B0E22;margin:0 0 30px;{af}">{kicker}</p>
<p style="font:400 128px/1 var(--display);margin:0">Atelier <span style="color:#5B0E22">Nacre</span></p>
<p{ar} style="font:400 32px/1.4 var(--sans);margin:34px 0 0;color:#5C4C52;{af}">{line}</p>
<p style="font:600 36px/1.55 var(--sans);margin:18px 0 0">hoshuko.github.io<br>github.com/hoshuko</p>
</div></div>"""


def plan(seg, lang):
    s = lambda i: seg[i]['start']
    e = lambda i: seg[i]['end']
    st = []
    add = lambda **k: st.append(k)
    add(t=s(1) - .3, d=e(1) + 1.3 - (s(1) - .3), do='scroll', to={'sel': '#accueil', 'p': .9})
    add(t=s(2) - .3, d=1.3, do='scroll', to={'sel': '#essai', 'offset': -20})
    add(t=s(2) + 1.1, d=.5, do='cursor', sel='#swatches .sw[data-ref="R-06"]')
    add(t=s(2) + 1.7, do='click', sel='#swatches .sw[data-ref="R-06"]')
    k = s(2) + 1.7 + (e(2) - s(2) - 1.7) * .55
    add(t=k, d=.45, do='cursor', sel='#swatches .sw[data-ref="C-10"]')
    add(t=k + .55, do='click', sel='#swatches .sw[data-ref="C-10"]')
    add(t=s(3) + .1, d=.5, do='cursor', sel='#finishes .fin[data-id="chrome"]')
    add(t=s(3) + .7, do='click', sel='#finishes .fin[data-id="chrome"]')
    add(t=s(4) - .3, d=1.2, do='scroll', to={'sel': '#formes', 'offset': -20})
    add(t=s(4) + 1.0, d=.45, do='cursor', sel='#shape-carre')
    add(t=s(4) + 1.55, do='click', sel='#shape-carre')
    k = s(4) + 1.55 + (e(4) - s(4) - 1.55) * .5
    add(t=k, d=.45, do='cursor', sel='#shape-stiletto')
    add(t=k + .55, do='click', sel='#shape-stiletto')
    add(t=s(5) - .3, d=1.2, do='scroll', to={'sel': '#galerie', 'offset': -20})
    add(t=s(5) + 1.0, d=.45, do='cursor', sel='#gal-chips .chip[data-f="chrome"]')
    add(t=s(5) + 1.55, do='click', sel='#gal-chips .chip[data-f="chrome"]')
    add(t=s(5) + 2.4, d=e(5) + .3 - (s(5) + 2.4), do='scroll', to={'sel': '#tarifs', 'offset': -20})
    add(t=s(6) + .3, d=.5, do='cursor', sel='#tarifs-book')
    add(t=s(6) + .95, do='click', sel='#tarifs-book')
    add(t=s(7) + .1, d=.8, do='cursor', sel='.lang-switch a[hreflang="en"]')
    add(t=s(7) + 1.5, d=.6, do='cursor', sel='.lang-switch a[hreflang="es"]')
    tc = e(7) + .5
    add(t=tc, d=.7, do='card', html=endcard(lang))
    return {'duration': round(tc + .7 + 5.8, 2), 'steps': st}


if __name__ == '__main__':
    visit.run('atelier-nacre', HERE, LANG, URL, SCRIPT, plan, 'nacre', {1: 1.2, 5: .4}, test='--test' in sys.argv,
              subtitle_langs=('en', 'es', 'ar') if LANG == 'fr' else (), voice=VOICE[LANG])
