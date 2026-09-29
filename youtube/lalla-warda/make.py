"""Vidéo YouTube commentée de Lalla Warda : visite du site en ligne, voix off Gemini (GEMINI_API_KEY), musique, sous-titres (FR, EN, ES, AR).

python3 make.py fr|en|es|ar [--test]    → out/lalla-warda-visite-<langue>.mp4 et .srt
La visite passe par gpu/tour.py (Chrome avec le GPU) : les scènes du site sont en WebGL.
La voix off présente la marque, ses soins et ce qu'y gagne la cliente, pas les animations du site.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import visit  # noqa: E402

# voix Gemini (tools/gemini_voice.py), une par langue en alternant femme et homme ; un seul modèle par vidéo ;
# (famille 3.x : la consigne entre crochets n'est pas lue ; jamais gemini-2.5-pro-preview-tts)
MODEL = 'gemini-3.8-flash-tts'
VOICE = {'fr': ('Sulafat', '', MODEL),      # femme, voix chaude
         'en': ('Algieba', '', MODEL),      # homme, voix douce
         'es': ('Aoede', '', MODEL),     # femme, voix légère
         'ar': ('Achird', '', MODEL)}       # homme, voix posée

visit.TOOLS = HERE / 'gpu'  # tour.py avec le GPU ; narrate et music restent ceux de tools/

LANG = sys.argv[1]
BASE = 'https://hoshuko.github.io/lalla-warda/'
URL = {'fr': BASE, 'en': BASE + 'en.html', 'es': BASE + 'es.html', 'ar': BASE + 'ar.html'}[LANG]

SCRIPT = {
    'fr': ["Lalla Warda, c'est une marque de soins naturels née à Kénitra, autour de l'eau de rose que distillait la grand-mère de sa fondatrice.",
           "Chaque soin tient en quelques ingrédients du Maroc : l'argan du Souss, la rose de Kelâat M'Gouna, la figue de barbarie et la fleur d'oranger du Gharb.",
           "Une huile sèche qui pénètre en trente secondes, un baume fondant, une argile qui se rince toute seule : chaque texture a son moment.",
           "Pour le visage, un rituel simple : quatre gestes, dix minutes, avec le masque au ghassoul et quelques gouttes d'élixir de rose.",
           "Pour les cheveux, l'huile d'argan et de nigelle nourrit la fibre, referme les écailles et rend la brillance.",
           "Huit soins, de soixante-cinq à quatre cent vingt dirhams, sans silicone, avec la composition complète de chaque flacon.",
           "Vous hésitez ? Trois questions, et votre routine du matin et du soir est prête.",
           "La commande se fait sur WhatsApp, avec la livraison partout au Maroc et le paiement à la livraison.",
           "Lalla Warda, la douceur de la rose, du Maroc à votre peau. Ce site de démonstration est gratuit et open source, en français, anglais, espagnol et arabe. Le lien est dans la description."],
    'en': ["Lalla Warda is a natural skincare brand born in Kenitra, built around the rose water its founder's grandmother used to distil.",
           "Each product holds a few Moroccan ingredients: argan from the Souss, roses from Kelaat M'Gouna, prickly pear and orange blossom from the Gharb.",
           "A dry oil that sinks in within thirty seconds, a melting balm, a clay that rinses off on its own: every texture has its moment.",
           "For the face, a simple ritual: four steps, ten minutes, with the ghassoul mask and a few drops of rose elixir.",
           "For the hair, argan and nigella oil nourishes the fibre, smooths the scales and brings back the shine.",
           "Eight products, from sixty-five to four hundred and twenty dirhams, silicone-free, with the full ingredient list of every bottle.",
           "Not sure where to start? Three questions, and your morning and evening routine is ready.",
           "You order on WhatsApp, with delivery across Morocco and payment on delivery.",
           "Lalla Warda, the softness of the rose, from Morocco to your skin. This demo website is free and open source, in French, English, Spanish and Arabic. The link is in the description."],
    'es': ["Lalla Warda es una marca de cosmética natural nacida en Kenitra, en torno al agua de rosas que destilaba la abuela de su fundadora.",
           "Cada producto lleva unos pocos ingredientes de Marruecos: argán del Sus, rosa de Kelaat M'Gouna, higo chumbo y flor de azahar del Gharb.",
           "Un aceite seco que se absorbe en treinta segundos, un bálsamo fundente, una arcilla que se aclara sola: cada textura tiene su momento.",
           "Para el rostro, un ritual sencillo: cuatro gestos, diez minutos, con la mascarilla de ghassoul y unas gotas de elixir de rosa.",
           "Para el cabello, el aceite de argán y nigella nutre la fibra, cierra las escamas y devuelve el brillo.",
           "Ocho productos, de sesenta y cinco a cuatrocientos veinte dírhams, sin siliconas, con la composición completa de cada frasco.",
           "¿No sabes cuál elegir? Tres preguntas, y tu rutina de mañana y de noche está lista.",
           "El pedido se hace por WhatsApp, con envío a todo Marruecos y pago contra reembolso.",
           "Lalla Warda, la dulzura de la rosa, de Marruecos a tu piel. Esta web de demostración es gratuita y de código abierto, en francés, inglés, español y árabe. El enlace está en la descripción."],
    'ar': ["لالة وردة علامة لمستحضرات العناية الطبيعية وُلدت في القنيطرة، حول ماء الورد الذي كانت تقطّره جدّة مؤسِّستها.",
           "كل منتج يضم مكوّنات قليلة من المغرب: أركان سوس، وورد قلعة مكونة، والتين الشوكي، وزهر البرتقال من الغرب.",
           "زيت جاف يتشرّبه الجلد في ثلاثين ثانية، وبلسم ذائب، وطين يُشطف بسهولة: لكل قوام لحظته.",
           "للوجه طقس بسيط: أربع خطوات وعشر دقائق، مع قناع الغاسول وبضع قطرات من إكسير الورد.",
           "للشعر، زيت الأركان وحبة البركة يغذّي الليفة ويغلق القشور ويعيد اللمعان.",
           "ثمانية منتجات، من خمسة وستين إلى أربعمئة وعشرين درهماً، بلا سيليكون، مع التركيبة الكاملة لكل قارورة.",
           "محتارة؟ ثلاثة أسئلة، وروتينك للصباح والمساء جاهز.",
           ("يتم الطلب عبر WhatsApp، مع التوصيل إلى كل المغرب والدفع عند الاستلام.",
            "يتم الطلب عبر واتساب، مع التوصيل إلى كل المغرب والدفع عند الاستلام."),
           "لالة وردة، رقّة الورد، من المغرب إلى بشرتك. موقع العرض هذا مجاني ومفتوح المصدر، بالفرنسية والإنجليزية والإسبانية والعربية. الرابط في الوصف."],
}
CARD = {'fr': ('Site gratuit · open source', 'Démo en ligne et code sur GitHub'), 'en': ('Free · open source', 'Live demo and code on GitHub'),
        'es': ('Web gratuita · código abierto', 'Demo en línea y código en GitHub'), 'ar': ('موقع مجاني · مفتوح المصدر', 'العرض والكود على GitHub')}


def endcard(lang):
    kicker, line = CARD[lang]
    d = ' dir="rtl"' if lang == 'ar' else ''
    return f"""<div style="position:absolute;inset:0;background:radial-gradient(120% 95% at 18% 32%,#B23F66 0%,#6E1F3A 58%,#3A0F20 100%);color:#FBF3EF;display:flex;align-items:center;padding:0 0 0 130px">
<div style="max-width:900px">
<p{d} style="font:600 22px/1 'Geist','IBM Plex Sans Arabic',sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#E4C998;margin:0 0 30px;text-align:left">{kicker}</p>
<p style="font:400 140px/1 'Instrument Serif',serif;margin:0;letter-spacing:-.01em">Lalla <i style="color:#F2D6D3">Warda</i> <span style="font:400 74px/1 'Amiri',serif;color:#E4C998;vertical-align:middle">لالة وردة</span></p>
<p{d} style="font:500 32px/1.4 'Geist','IBM Plex Sans Arabic',sans-serif;margin:34px 0 0;color:rgba(251,243,239,.84);text-align:left">{line}</p>
<p style="font:600 36px/1.55 'Geist',sans-serif;margin:18px 0 0">hoshuko.github.io<br>github.com/hoshuko</p>
</div></div>"""


def plan(seg, lang):
    s = lambda i: seg[i]['start']
    e = lambda i: seg[i]['end']
    st = []
    add = lambda **k: st.append(k)
    # 0-1 : la rose s'ouvre, le flacon sort de son cœur, puis les ingrédients se placent autour de lui
    add(t=s(0) + .2, d=e(0) - s(0), do='scroll', to={'sel': '#accueil', 'p': .5})
    add(t=s(1), d=e(1) - s(1) + .6, do='scroll', to={'sel': '#accueil', 'p': 1})
    # 2 : les textures, essayées sur la peau
    add(t=s(2) - .3, d=1.3, do='scroll', to={'sel': '#textures', 'offset': -10})
    k = (e(2) - s(2) - 1.2) / 2
    add(t=s(2) + 1.0 + k * .35, d=.45, do='cursor', sel='#tex-tabs .tex-tab:nth-child(2)')
    add(t=s(2) + 1.5 + k * .35, do='click', sel='#tex-tabs .tex-tab:nth-child(2)')
    add(t=s(2) + 1.0 + k * 1.2, d=.45, do='cursor', sel='#tex-tabs .tex-tab:nth-child(3)')
    add(t=s(2) + 1.5 + k * 1.2, do='click', sel='#tex-tabs .tex-tab:nth-child(3)')
    add(t=e(2), d=.4, do='hide')
    # 3 : le rituel visage, geste après geste
    add(t=s(3) - .3, d=e(3) - s(3) + .9, do='scroll', to={'sel': '#visage', 'p': .96})
    # 4 : le cheveu au microscope
    add(t=s(4) - .3, d=e(4) - s(4) + .8, do='scroll', to={'sel': '#micro', 'p': .95})
    # 5 : la collection, puis la fiche de l'élixir et sa composition
    add(t=s(5) - .3, d=1.2, do='scroll', to={'sel': '#collection', 'offset': 20})
    add(t=s(5) + 1.0, d=.5, do='cursor', sel='#products [data-sheet="elixir"]')
    add(t=s(5) + 1.6, do='click', sel='#products [data-sheet="elixir"]')
    add(t=s(5) + 2.6, d=.45, do='cursor', sel='#sheet-explode')
    add(t=s(5) + 3.1, do='click', sel='#sheet-explode')
    add(t=e(5) + .3, d=.4, do='cursor', sel='#sheet-close')
    add(t=e(5) + .75, do='click', sel='#sheet-close')
    # 6 : la routine en trois questions
    add(t=s(6) - .2, d=1.1, do='scroll', to={'sel': '#routine', 'offset': -10})
    for j in range(3):
        t = s(6) + 1.0 + j * max(.8, (e(6) - s(6) - 1.2) / 3)
        add(t=t, d=.4, do='cursor', sel='#quiz .quiz-choices button:first-child')
        add(t=t + .45, do='click', sel='#quiz .quiz-choices button:first-child')
    # 7 : la routine part au panier, la commande WhatsApp est prête
    add(t=s(7), d=.45, do='cursor', sel='#routine-add')
    add(t=s(7) + .5, do='click', sel='#routine-add')
    add(t=s(7) + 2.2, d=.6, do='cursor', sel='#cart-foot', off=[.5, .3])
    add(t=e(7) + .2, d=.4, do='cursor', sel='#cart-close')
    add(t=e(7) + .65, do='click', sel='#cart-close')
    # 8 : la route des fleurs, les quatre langues, puis la carte de fin
    add(t=s(8) - .1, d=1.3, do='hide')
    add(t=s(8) - .1, d=1.5, do='scroll', to={'sel': '#origines', 'offset': -10})
    k = s(8) + (e(8) - s(8)) * .5
    for j, l in enumerate(('en', 'es', 'ar')):
        add(t=k + j * .8, d=.6, do='cursor', sel=f'.lang-switch a[hreflang="{l}"]')
    tc = e(8) + .5
    add(t=tc, d=.7, do='card', html=endcard(lang))
    return {'duration': round(tc + .7 + 5.8, 2), 'steps': st}


if __name__ == '__main__':
    visit.run('lalla-warda', HERE, LANG, URL, SCRIPT, plan, 'nacre', {0: .6, 1: 1.2, 2: .8, 3: .8, 4: .6, 5: 1.2}, test='--test' in sys.argv,
              subtitle_langs=('en', 'es', 'ar') if LANG == 'fr' else (), voice=VOICE[LANG])
