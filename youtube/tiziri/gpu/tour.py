"""tools/tour.py pour Tiziri : le studio d'accueil est en WebGL (Three.js), et les mannequins marchent en vidéo.

Même interface que tools/tour.py, avec deux changements :
- Chrome dessine avec le GPU (--disable-gpu remplacé par le rendu Metal), comme youtube/lalla-warda/gpu/tour.py ;
- les vidéos de la page suivent le temps ralenti (playbackRate au même facteur que les horloges) : sinon, filmées
  image par image, elles passeraient environ sept fois trop vite et la cabine enchaînerait les pièces.
"""
import subprocess, sys
from pathlib import Path

YT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(YT / 'tools'))
sys.path.insert(0, str(YT.parent / '_tools'))
import check  # noqa: E402

GPU = ['--use-angle=metal', '--enable-gpu-rasterization', '--ignore-gpu-blocklist', '--force-color-profile=srgb']
_popen = subprocess.Popen


def popen(args, *a, **k):
    if args and args[0] == check.CHROME:
        args = [x for x in args if x != '--disable-gpu'] + GPU + ['--autoplay-policy=no-user-gesture-required']
    return _popen(args, *a, **k)


check.subprocess.Popen = popen
import tour  # noqa: E402

MEDIA = """(() => {
  const R = __RATE__;
  const slow = m => { if (m.playbackRate !== R) { m.defaultPlaybackRate = R; m.playbackRate = R; } };
  const play = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { slow(this); return play.call(this); };
  document.addEventListener('play', e => slow(e.target), true);
  document.addEventListener('ratechange', e => slow(e.target), true);
})();"""
tour.TIME_SCALE += MEDIA

if __name__ == '__main__':
    tour.main()
