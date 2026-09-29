"""Vidéo YouTube commentée de Tafat : visite du site en ligne, voix off Google, musique, sous-titres (FR, EN, ES, AR).

python3 make.py fr|en|es|ar [--test]    → out/tafat-visite-<langue>.mp4 et .srt
(la version arabe montre le site en français : le site n'a pas de version arabe)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'tools'))
import visit  # noqa: E402

LANG = sys.argv[1]
URL = {'fr': 'https://hoshuko.github.io/tafat/', 'en': 'https://hoshuko.github.io/tafat/en.html',
       'es': 'https://hoshuko.github.io/tafat/es.html', 'ar': 'https://hoshuko.github.io/tafat/'}[LANG]

SCRIPT = {
    'fr': ['Tafat, « la lumière » en kabyle : une équipe de femmes de Tigzirt qui fait le ménage à domicile.',
           'On arrive, on nettoie à fond, et la lumière revient chez vous : des vitres claires, une maison qui respire.',
           "Ménage de la semaine, grand ménage de l'Aïd, maison d'été ou lendemain de fête : chaque prestation commence par une estimation claire.",
           "Vous n'avez rien à acheter : l'équipe apporte tout, avec des produits simples, vinaigre blanc, bicarbonate, citron et savon à l'huile d'olive.",
           'Pièce par pièce, vous savez ce qui est nettoyé, avec une microfibre de couleur par zone, pour ne jamais mélanger cuisine et toilettes.',
           "Votre prix en trente secondes : choisissez, et le message WhatsApp s'écrit tout seul. L'équipe répond dans l'heure.",
           "Vous vivez loin ? On ouvre, on aère, on nettoie et on vous envoie les photos : vous n'avez plus qu'à poser les valises.",
           'Tafat, votre maison entre de bonnes mains. Ce site de démonstration est gratuit et open source, en français, anglais et espagnol. Le lien est dans la description.'],
    'en': ['Tafat means “light” in Kabyle: a team of women from Tigzirt who clean homes.',
           'We arrive, clean thoroughly, and the light comes back into your home: clear windows, a house that breathes.',
           'Weekly cleaning, the big clean before Eid, summer homes or the day after a party: every job starts with a clear estimate.',
           "You don't need to buy anything: the team brings it all, with simple products like white vinegar, baking soda, lemon and olive oil soap.",
           'Room by room, you know exactly what gets cleaned, with one colour of microfibre cloth per area, so the kitchen and the toilet never mix.',
           'Your price in thirty seconds: make your choices and the WhatsApp message writes itself. The team replies within the hour.',
           'Live far away? We open up, air the house, clean it and send you photos: all you have to do is drop your bags.',
           'Tafat: your home in good hands. This demo website is free and open source, in French, English and Spanish. The link is in the description.'],
    'es': ['Tafat significa «luz» en cabilio: un equipo de mujeres de Tigzirt que limpia casas.',
           'Llegamos, limpiamos a fondo y la luz vuelve a tu casa: cristales limpios, una casa que respira.',
           'Limpieza semanal, la gran limpieza del Aid, casas de verano o el día después de una fiesta: cada servicio empieza con un presupuesto claro.',
           'No tienes que comprar nada: el equipo lo trae todo, con productos sencillos como vinagre blanco, bicarbonato, limón y jabón de aceite de oliva.',
           'Estancia por estancia, sabes qué se limpia, con una microfibra de un color por zona, para no mezclar nunca la cocina y el baño.',
           'Tu precio en treinta segundos: elige y el mensaje de WhatsApp se escribe solo. El equipo responde en menos de una hora.',
           '¿Vives lejos? Abrimos, ventilamos, limpiamos y te enviamos las fotos: solo tienes que dejar las maletas.',
           'Tafat: tu casa en buenas manos. Esta web de demostración es gratuita y de código abierto, en francés, inglés y español. El enlace está en la descripción.'],
    'ar': ['تافات تعني «النور» بالقبائلية: فريق من نساء تيقزيرت يقدّم خدمات التنظيف المنزلي.',
           'نصل، وننظّف بعمق، فيعود النور إلى بيتك: نوافذ صافية وبيت يتنفّس.',
           'تنظيف أسبوعي، أو تنظيف شامل قبل العيد، أو منزل الصيف، أو ما بعد الحفلات: كل خدمة تبدأ بتقدير واضح للسعر.',
           'لا تحتاج إلى شراء أي شيء: يحضر الفريق كل شيء، بمنتجات بسيطة كالخل الأبيض والبيكربونات والليمون وصابون زيت الزيتون.',
           'غرفة بعد غرفة، تعرف ما يُنظَّف بالضبط، مع قطعة ميكروفايبر بلون مختلف لكل منطقة، حتى لا تختلط أدوات المطبخ بأدوات المرحاض.',
           'سعرك في ثلاثين ثانية: اختر، فتُكتب رسالة واتساب تلقائيًا. ويردّ الفريق خلال ساعة.',
           'تعيش بعيدًا؟ نفتح البيت ونهوّيه وننظّفه ونرسل إليك الصور: ما عليك إلا أن تضع حقائبك.',
           'تافات، بيتك بين أيادٍ أمينة. هذا الموقع التجريبي مجاني ومفتوح المصدر، بالفرنسية والإنجليزية والإسبانية. الرابط في الوصف.'],
}
# voix Gemini : une par langue, en alternant voix d'homme et de femme
VOICE = {'fr': ('Laomedeia', ''), 'en': ('Iapetus', ''),
         'es': ('Autonoe', ''), 'ar': ('Schedar', '')}
CARD = {'fr': ('Site gratuit · open source', 'Démo en ligne et code sur GitHub'), 'en': ('Free · open source', 'Live demo and code on GitHub'),
        'es': ('Web gratuita · código abierto', 'Demo en línea y código en GitHub'), 'ar': ('موقع مجاني · مفتوح المصدر', 'العرض والكود على GitHub')}


def endcard(lang):
    kicker, line = CARD[lang]
    rtl = lang == 'ar'
    ar = "font-family:'Geeza Pro','Noto Sans Arabic',sans-serif;text-align:left;letter-spacing:0;" if rtl else ''
    d = ' dir="rtl"' if rtl else ''
    return f"""<div style="position:absolute;inset:0;background:radial-gradient(120% 95% at 18% 32%,#146272 0%,#0E4A57 55%,#072830 100%);color:#FFFFFF;display:flex;align-items:center;padding:0 0 0 130px">
<div style="max-width:880px">
<p{d} style="font:700 22px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:#FFC53D;margin:0 0 30px;{ar}">{kicker}</p>
<p style="font:800 128px/1 var(--display);margin:0;letter-spacing:-.02em">Tafat <span style="font:400 64px/1 var(--tfn);color:#FFC53D;vertical-align:middle">ⵜⴰⴼⴰⵜ</span></p>
<p{d} style="font:500 32px/1.4 var(--sans);margin:34px 0 0;color:rgba(255,255,255,.82);{ar}">{line}</p>
<p style="font:700 36px/1.55 var(--sans);margin:18px 0 0">hoshuko.github.io<br>github.com/hoshuko</p>
</div></div>"""


def plan(seg, lang):
    s = lambda i: seg[i]['start']
    e = lambda i: seg[i]['end']
    st = []
    add = lambda **k: st.append(k)
    add(t=s(1) - .3, d=e(1) + 1.2 - (s(1) - .3), do='scroll', to={'sel': '#accueil', 'p': .95})
    add(t=s(2) - .3, d=1.3, do='scroll', to={'sel': '#prestations', 'offset': -30})
    add(t=s(2) + 1.3, d=e(2) - s(2) - 1.1, do='scroll', to={'sel': '#svc-grid', 'offset': -120})
    add(t=s(3) - .3, d=e(3) + .8 - (s(3) - .3), do='scroll', to={'sel': '#kit', 'p': .95})
    add(t=s(4) - .3, d=1.2, do='scroll', to={'sel': '#pieces', 'offset': -20})
    add(t=s(4) + 1.0, d=.5, do='cursor', sel='#tab-sdb')
    add(t=s(4) + 1.6, do='click', sel='#tab-sdb')
    k = s(4) + 1.6 + (e(4) - s(4) - 1.6) * .5
    add(t=k, d=.45, do='cursor', sel='#tab-salon')
    add(t=k + .55, do='click', sel='#tab-salon')
    add(t=s(5) - .3, d=1.2, do='scroll', to={'sel': '#devis', 'offset': -20})
    add(t=s(5) + 1.0, d=.45, do='cursor', sel='#q-logement .chip[data-id="f4"]')
    add(t=s(5) + 1.55, do='click', sel='#q-logement .chip[data-id="f4"]')
    add(t=s(5) + 2.2, d=.45, do='cursor', sel='#q-prestation .chip[data-id="ete"]')
    add(t=s(5) + 2.75, do='click', sel='#q-prestation .chip[data-id="ete"]')
    add(t=s(5) + 3.3, d=.5, do='cursor', sel='#wa-msg', off=[.5, .4])
    add(t=s(6) - .3, d=1.3, do='hide')
    add(t=s(6) - .3, d=1.3, do='scroll', to={'sel': '#ete', 'offset': -20})
    add(t=s(7) + .1, d=.8, do='cursor', sel='.lang-switch a[hreflang="en"]')
    add(t=s(7) + 1.5, d=.6, do='cursor', sel='.lang-switch a[hreflang="es"]')
    tc = e(7) + .5
    add(t=tc, d=.7, do='card', html=endcard(lang))
    return {'duration': round(tc + .7 + 5.8, 2), 'steps': st}


if __name__ == '__main__':
    visit.run('tafat', HERE, LANG, URL, SCRIPT, plan, 'tafat', {1: 1.0, 3: .6, 5: .9}, test='--test' in sys.argv,
              subtitle_langs=('en', 'es', 'ar') if LANG == 'fr' else (), voice=VOICE[LANG])
