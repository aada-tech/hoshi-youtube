"""tools/tour.py avec le GPU : Lalla Warda est en WebGL (Three.js), et Chrome sans GPU n'afficherait que les images de secours.

Même interface que tools/tour.py ; seul le lancement de Chrome change (--disable-gpu remplacé par le rendu Metal).
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
        args = [x for x in args if x != '--disable-gpu'] + GPU
    return _popen(args, *a, **k)


check.subprocess.Popen = popen

# profil Chrome jetable effacé à la fermeture (check.CDP le laisse dans $TMPDIR, ~150 Mo par rendu)
if 'rmtree' not in open(check.__file__, encoding='utf-8').read():
    import shutil
    _close = check.CDP.close

    def close(self):
        try:
            _close(self)
        finally:
            shutil.rmtree(self.tmp, ignore_errors=True)
    check.CDP.close = close
import tour  # noqa: E402

if __name__ == '__main__':
    tour.main()
