"""Vidéo YouTube commentée de Maison Billot : visite du site en ligne, voix off Google, musique, sous-titres (FR, EN, ES, AR).

python3 make.py fr|en|es|ar [--test]      → out/maison-billot-visite-<langue>.mp4 et .srt
(la version arabe montre le site en français : le site n'a pas de version arabe)
"""
import json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent / 'tools'
sys.path.insert(0, str(TOOLS))
import narrate  # noqa: E402
import music  # noqa: E402
import visit  # noqa: E402

LANG = sys.argv[1]
TEST = '--test' in sys.argv
URL = {'fr': 'https://hoshuko.github.io/maison-billot/', 'en': 'https://hoshuko.github.io/maison-billot/en.html',
       'es': 'https://hoshuko.github.io/maison-billot/es.html', 'ar': 'https://hoshuko.github.io/maison-billot/'}[LANG]

# (texte affiché dans les sous-titres, texte prononcé si la prononciation du nom l'exige)
SCRIPT = {
    'fr': ["Maison Billot, boucherie artisanale à Lyon depuis 1987. Des bœufs Salers, Aubrac et Charolais, maturés sur l'os et découpés devant vous.",
           'Du collier à la queue, vingt-trois morceaux, tous issus de bêtes nées, élevées et abattues en France.',
           'Pour chaque pièce, le boucher vous dit tout : sa tendreté, comment la cuire, son conseil et le prix au kilo.',
           'Un barbecue, un pot-au-feu ? Dites ce que vous cuisinez, et on vous montre les bons morceaux.',
           "Merguez, saucisses et préparations sont faites maison chaque matin, sans rien cacher de ce qu'il y a dedans.",
           'En cave, nos côtes mûrissent de trois à huit semaines : plus elles attendent, plus elles gagnent en tendreté et en goût.',
           'Commandez votre colis en ligne et choisissez votre heure de retrait : il vous attend en boutique, et vous payez au poids réel.',
           'Maison Billot : choisi, maturé, découpé. Ce site de démonstration est gratuit et open source, en français, anglais et espagnol. Le lien est dans la description.'],
    'en': [('Maison Billot, an artisan butcher in Lyon since 1987. Salers, Aubrac and Charolais beef, aged on the bone and cut in front of you.',
            'Maison Bee-yo, an artisan butcher in Lyon since 1987. Salers, Aubrac and Charolais beef, aged on the bone and cut in front of you.'),
           'From neck to tail, twenty-three cuts, all from animals born, raised and slaughtered in France.',
           'For every cut, the butcher tells you everything: how tender it is, how to cook it, his tip and the price per kilo.',
           "A barbecue, a slow-cooked stew? Tell us what you're cooking, and we'll show you the right cuts.",
           'Merguez, sausages and ready-to-cook dishes are made in-house every morning, with nothing hidden about what goes in.',
           'In our ageing room, rib steaks mature for three to eight weeks: the longer they wait, the more tender and flavourful they get.',
           "Order your box online and choose your collection time: it's waiting for you in store, and you pay by actual weight.",
           ('Maison Billot: chosen, aged, cut. This demo website is free and open source, in French, English and Spanish. The link is in the description.',
            'Maison Bee-yo: chosen, aged, cut. This demo website is free and open source, in French, English and Spanish. The link is in the description.')],
    'es': [('Maison Billot, carnicería artesanal en Lyon desde 1987. Vacuno Salers, Aubrac y Charolais, madurado con hueso y cortado delante de ti.',
            'Maisón Biyó, carnicería artesanal en Lyon desde 1987. Vacuno Salers, Aubrac y Charolais, madurado con hueso y cortado delante de ti.'),
           'Del cuello al rabo, veintitrés piezas, todas de reses nacidas, criadas y sacrificadas en Francia.',
           'De cada pieza, el carnicero te lo cuenta todo: su terneza, cómo cocinarla, su consejo y el precio por kilo.',
           '¿Una barbacoa, un cocido? Dinos qué vas a cocinar y te enseñamos las piezas adecuadas.',
           'Las merguez, las salchichas y los preparados se hacen en casa cada mañana, sin ocultar nada de lo que llevan.',
           'En nuestra cámara, las chuletas maduran de tres a ocho semanas: cuanto más esperan, más tiernas y sabrosas son.',
           'Haz tu pedido en línea y elige la hora de recogida: te espera en la tienda y pagas por el peso real.',
           ('Maison Billot: elegido, madurado, cortado. Esta web de demostración es gratuita y de código abierto, en francés, inglés y español. El enlace está en la descripción.',
            'Maisón Biyó: elegido, madurado, cortado. Esta web de demostración es gratuita y de código abierto, en francés, inglés y español. El enlace está en la descripción.')],
    'ar': [('Maison Billot، محل جزارة حِرفي في ليون منذ عام 1987. لحوم أبقار سالير وأوبراك وشارولي، مُعتَّقة على العظم وتُقطَّع أمام عينيك.',
            'ميزون بييو، محل جزارة حِرفي في ليون منذ عام 1987. لحوم أبقار سالير وأوبراك وشارولي، مُعتَّقة على العظم وتُقطَّع أمام عينيك.'),
           'من الرقبة إلى الذيل، ثلاث وعشرون قطعة، كلها من أبقار وُلدت ورُبّيت وذُبحت في فرنسا.',
           'لكل قطعة، يخبرك الجزّار بكل شيء: طراوتها، وطريقة طهيها، ونصيحته، وسعر الكيلوغرام.',
           'شواء أم طبق مطهو على نار هادئة؟ أخبرنا بما ستطبخه، ونريك القطع المناسبة.',
           'المرقاز والنقانق والأطباق الجاهزة للطهي تُحضَّر في المحل كل صباح، دون إخفاء أي شيء مما بداخلها.',
           'في غرفة التعتيق، تنضج شرائح الضلع من ثلاثة إلى ثمانية أسابيع: كلما طال انتظارها، ازدادت طراوة ونكهة.',
           'اطلب طلبيتك عبر الإنترنت واختر موعد الاستلام: تنتظرك في المحل، وتدفع حسب الوزن الفعلي.',
           ('Maison Billot: اختيار وتعتيق وتقطيع. هذا الموقع التجريبي مجاني ومفتوح المصدر، بالفرنسية والإنجليزية والإسبانية. الرابط في الوصف.',
            'ميزون بييو: اختيار وتعتيق وتقطيع. هذا الموقع التجريبي مجاني ومفتوح المصدر، بالفرنسية والإنجليزية والإسبانية. الرابط في الوصف.')],
}
# voix Gemini : une par langue, en alternant voix d'homme et de femme
VOICE = {'fr': ('Charon', ''), 'en': ('Kore', ''),
         'es': ('Orus', ''), 'ar': ('Gacrux', '')}
CARD = {
    'fr': ('Site gratuit · open source', 'Démo en ligne et code sur GitHub'),
    'en': ('Free · open source', 'Live demo and code on GitHub'),
    'es': ('Web gratuita · código abierto', 'Demo en línea y código en GitHub'),
    'ar': ('موقع مجاني · مفتوح المصدر', 'العرض والكود على GitHub'),
}


def endcard(lang):
    kicker, line = CARD[lang]
    ar = ' dir="rtl"' if lang == 'ar' else ''
    af = "font-family:'Geeza Pro','Noto Sans Arabic',sans-serif;text-align:left;letter-spacing:0;" if lang == 'ar' else ''
    return f"""<div style="position:absolute;inset:0;background:radial-gradient(120% 95% at 18% 32%,#1E473B 0%,#0F2922 58%,#0A1D18 100%);color:#F4EBDD;display:flex;align-items:center;padding:0 0 0 130px">
<div style="max-width:880px">
<p{ar} style="font:500 22px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#CDA85F;margin:0 0 30px;{af}">{kicker}</p>
<p style="font:italic 700 124px/1 var(--display);margin:0;color:#F4EBDD">Maison <span style="color:#E9D7AE">Billot</span></p>
<p{ar} style="font:400 32px/1.4 var(--sans);margin:34px 0 0;color:rgba(244,235,221,.82);{af}">{line}</p>
<p style="font:600 36px/1.55 var(--sans);margin:18px 0 0;color:#F4EBDD">hoshuko.github.io<br>github.com/hoshuko</p>
</div></div>"""


def plan(seg):
    s = lambda i: seg[i]['start']
    e = lambda i: seg[i]['end']
    st = []
    add = lambda **k: st.append(k)
    # 1. la bête se découpe
    add(t=s(1) - .3, d=e(1) + 1.3 - (s(1) - .3), do='scroll', to={'sel': '#decoupe', 'p': .86})
    # 2. fiche d'un morceau
    piece = '.piece[data-id="onglet"]'
    add(t=s(2) - .1, d=.8, do='cursor', sel=piece)
    add(t=s(2) + .85, do='click', sel=piece)
    add(t=e(2) - 1.05, d=.5, do='cursor', sel='#d-close')
    add(t=e(2) - .4, do='click', sel='#d-close')
    # 3. guide des morceaux
    add(t=s(3) - .3, d=1.4, do='scroll', to={'sel': '#guide', 'offset': -30})
    add(t=s(3) + 1.25, d=.55, do='cursor', sel='#usage-chips [data-u="barbecue"]')
    add(t=s(3) + 1.9, do='click', sel='#usage-chips [data-u="barbecue"]')
    k = s(3) + 1.9 + (e(3) - s(3) - 1.9) * .5
    add(t=k, d=.5, do='cursor', sel='#usage-chips [data-u="potaufeu"]')
    add(t=k + .6, do='click', sel='#usage-chips [data-u="potaufeu"]')
    # 4. merguez en vue éclatée
    add(t=s(4) - .2, do='hide')
    add(t=s(4) - .3, d=e(4) + .7 - (s(4) - .3), do='scroll', to={'sel': '#maison', 'p': .92})
    # 5. cave de maturation
    add(t=s(5) - .3, d=1.2, do='scroll', to={'sel': '#cave', 'offset': -20})
    add(t=s(5) + .95, d=.45, do='cursor', sel='#age-range', off=[.5, .5])
    add(t=s(5) + 1.45, d=.7, do='range', sel='#age-range', **{'from': 30, 'to': 0})
    add(t=s(5) + 1.45, d=.7, do='cursor', sel='#age-range', off=[0, .5])
    t6 = s(5) + 2.3
    add(t=t6, d=e(5) + .3 - t6, do='range', sel='#age-range', **{'from': 0, 'to': 60})
    add(t=t6, d=e(5) + .3 - t6, do='cursor', sel='#age-range', off=[1, .5])
    # 6. colis et retrait
    add(t=s(6) - .3, d=1.3, do='scroll', to={'sel': '#colis', 'offset': -20})
    add(t=s(6) + 1.1, d=.5, do='cursor', sel='#presets .preset')
    add(t=s(6) + 1.7, do='click', sel='#presets .preset')
    add(t=s(6) + 2.4, d=.45, do='cursor', sel='#slot-list .chip')
    add(t=s(6) + 2.95, do='click', sel='#slot-list .chip')
    add(t=s(6) + 3.4, d=.45, do='cursor', sel='#colis-go')
    add(t=s(6) + 3.95, do='click', sel='#colis-go')
    # pas de défilement vers #recap : le récapitulatif de réservation est un bloc technique sous la caisse ; la caméra reste
    # sur la caisse en bois (elle se remplit, le prix s'anime, le créneau est choisi), comme sur le vrai site
    # 7. langues, puis carte de fin
    add(t=s(7) + .1, d=.8, do='cursor', sel='.lang-switch a[hreflang="en"]')
    add(t=s(7) + 1.5, d=.6, do='cursor', sel='.lang-switch a[hreflang="es"]')
    tc = e(7) + .5
    add(t=tc, d=.7, do='card', html=endcard(LANG))
    return {'duration': round(tc + .7 + 5.8, 2), 'steps': st}


def main():
    out = HERE / 'out'
    work = HERE / 'work'
    out.mkdir(exist_ok=True); work.mkdir(exist_ok=True)
    print('voix :', visit.use_voice(VOICE[LANG]), flush=True)
    texts = [x if isinstance(x, str) else x[1] for x in SCRIPT[LANG]]
    shown = [x if isinstance(x, str) else x[0] for x in SCRIPT[LANG]]
    seg = narrate.timeline(texts, LANG, str(work), lead=.9, holds={1: 1.1, 5: .2, 6: .9})
    for sg, txt in zip(seg, shown):
        sg['text'] = txt
    p = plan(seg)
    if TEST:
        p['duration'] = min(p['duration'], seg[2]['end'] + .5)
    plan_path = work / f'plan-{LANG}.json'
    json.dump(p, open(plan_path, 'w', encoding='utf-8'), ensure_ascii=False)
    narrate.save_timeline(seg, work / f'timeline-{LANG}.json')
    stem = f'maison-billot-visite-{LANG}' + ('-test' if TEST else '')
    video = work / f'{stem}-image.mp4'
    subprocess.run([sys.executable, str(TOOLS / 'tour.py'), URL, str(plan_path), str(video)], check=True)
    bed = work / f'musique-{int(p["duration"])}.wav'
    if not bed.exists():
        music.write_wav(str(bed), music.bed('billot', p['duration']))
    mixed = work / f'{stem}-son.wav'
    narrate.mix([s for s in seg if s['start'] < p['duration']], str(bed), p['duration'], str(mixed))
    final = out / f'{stem}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(video), '-i', str(mixed), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                    '-map_metadata', '-1', str(final)], check=True)
    narrate.srt([s for s in seg if s['start'] < p['duration']], str(out / f'{stem}.srt'))
    if LANG == 'fr':
        for other in ('en', 'es', 'ar'):
            o_shown = [x if isinstance(x, str) else x[0] for x in SCRIPT[other]]
            narrate.srt([dict(s, text=o_shown[s['i']]) for s in seg if s['start'] < p['duration']], str(out / f'{stem}.{other}.srt'))
    print('vidéo', final, round(p['duration'], 1), 's')


if __name__ == '__main__':
    main()
