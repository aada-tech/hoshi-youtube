"""Miniatures de Tiziri : la cabine d'essayage capturée avec le GPU (le pull léopard porté, l'étiquette « La pièce »,
la tenue de base adoucie), puis composées par tools/thumbs.py → out/tiziri-miniature-<langue>.jpg.

python3 youtube/tiziri/capture.py      (ne refait que les miniatures de Tiziri)
"""
import shutil, sys, time
from pathlib import Path

YT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(YT.parent / 'sources' / 'cosmetiques-kenitra'))
sys.path.insert(0, str(YT / 'tools'))
from cdp import CDP  # noqa: E402  (Chrome avec le GPU)
import thumbs  # noqa: E402

c = CDP().attach(1920, 1080)
c.goto('https://hoshuko.github.io/tiziri/', ready="document.readyState === 'complete'", timeout=60)
time.sleep(4)
c.eval("document.documentElement.style.scrollBehavior = 'auto'")
c.eval("(() => { const e = document.querySelector('[data-cabin]'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 6); })()")
time.sleep(1.5)
c.eval("document.querySelector('[data-cabin-pick=\"1\"]').click()")  # le pull léopard
# balayage, la pièce se dépose, le mannequin marche, puis reprend ses poses : on s'arrête sur la pose détendue
DETENTE = """(() => { const look = document.querySelector('[data-cabin-piece="1"]'), poses = look.querySelectorAll('[data-pose]');
  return look.classList.contains('is-active') && poses[3].classList.contains('is-on') && !look.querySelector('video.is-playing'); })()"""
for _ in range(120):
    time.sleep(.25)
    if c.eval(DETENTE):
        break
c.eval("document.querySelector('[data-cabin-pause]').click()")
time.sleep(1.2)
c.eval("document.head.insertAdjacentHTML('beforeend', '<style>[data-header], #essayage .gutter > div:first-child, [data-cabin-status],"
       " [data-cabin-pose], [data-cabin-pause], .tenue-note { visibility: hidden !important }</style>')")
time.sleep(.6)
thumbs.WORK.mkdir(parents=True, exist_ok=True)
c.shot(str(thumbs.WORK / 'tiziri.png'))
print('capture tiziri', *c.errors())
c.close()

# composition, pour Tiziri seulement : les autres miniatures restent telles quelles
(thumbs.WORK / 'fonts').mkdir(exist_ok=True)
for f in (thumbs.ROOT / '_fonts' / thumbs.STYLE['tiziri']['fonts']).glob('*.woff2'):
    shutil.copy2(f, thumbs.WORK / 'fonts' / f.name)
thumbs.TEXT = {'tiziri': thumbs.TEXT['tiziri']}
thumbs.render()
