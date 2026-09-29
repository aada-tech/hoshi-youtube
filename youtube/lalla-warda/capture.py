"""Capture du moment fort de Lalla Warda pour la miniature (thumbs-work/warda.png), avec le GPU : le site est en WebGL.

python3 capture.py      puis   python3 ../tools/thumbs.py --no-capture   (ou thumbs.py, qui garde cette image)
"""
import sys, time
from pathlib import Path

YT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(YT.parent / 'sources' / 'cosmetiques-kenitra'))
from cdp import CDP  # noqa: E402  (Chrome avec le GPU)

c = CDP().attach(1920, 1080)
c.goto('https://hoshuko.github.io/lalla-warda/', ready="document.readyState === 'complete'", timeout=60)
time.sleep(3)
c.eval("document.documentElement.style.scrollBehavior = 'auto'")
c.eval("(() => { const s = document.querySelector('#accueil'); window.scrollTo(0, s.offsetTop + (s.offsetHeight - innerHeight)); })()")
time.sleep(5)
c.eval("document.head.insertAdjacentHTML('beforeend', '<style>#nav, #hero-end, #hero-labels, #hero-lines, #hero-copy, #scroll-hint { display: none !important }</style>')")
time.sleep(.6)
(YT / 'thumbs-work').mkdir(exist_ok=True)
c.shot(str(YT / 'thumbs-work' / 'warda.png'))
print('capture warda', *c.errors())
c.close()
