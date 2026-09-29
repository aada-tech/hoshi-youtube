"""Rendu image par image de compo.html via Chrome (CDP sur les descripteurs 3/4), encodage ffmpeg.
usage : python3 render.py 45|916 [--stills t1,t2,...] [--fps 30]"""
import subprocess, os, sys, json, base64, time, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FFMPEG = '/opt/homebrew/bin/ffmpeg'

# remplacements appliqués aux versions traduites de compo.html
EXTRA = [('<span class="p">35 €</span>', '<span class="p">€35</span>', ('en',)), ('<span class="p">55 €</span>', '<span class="p">€55</span>', ('en',)),
         ('<span class="p">70 €</span>', '<span class="p">€70</span>', ('en',)),
         # arabe : les prix restent « 35 € » (sinon le bidi affiche « € 35 »)
         ('<span class="p">35 €</span>', '<span class="p" dir="ltr">35 €</span>', ('ar',)), ('<span class="p">55 €</span>', '<span class="p" dir="ltr">55 €</span>', ('ar',)),
         ('<span class="p">70 €</span>', '<span class="p" dir="ltr">70 €</span>', ('ar',))]

class CDP:
    def __init__(self):
        r1, w1 = os.pipe(); r2, w2 = os.pipe()
        def pre():
            os.dup2(r1, 3); os.dup2(w2, 4)
        self.tmp = tempfile.mkdtemp()
        self.p = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-pipe', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                                   '--no-first-run', '--no-default-browser-check', '--force-device-scale-factor=1', f'--user-data-dir={self.tmp}', 'about:blank'],
                                  pass_fds=(3, 4), preexec_fn=pre, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.close(r1); os.close(w2)
        self.w = os.fdopen(w1, 'wb', buffering=0); self.r = os.fdopen(r2, 'rb', buffering=0)
        self.buf = b''; self.n = 0; self.session = None
    def _read(self):
        while b'\0' not in self.buf:
            chunk = self.r.read(1 << 20)
            if not chunk: raise RuntimeError('chrome closed')
            self.buf += chunk
        msg, self.buf = self.buf.split(b'\0', 1)
        return json.loads(msg)
    def call(self, method, params=None, session=True):
        self.n += 1
        m = {'id': self.n, 'method': method, 'params': params or {}}
        if session and self.session: m['sessionId'] = self.session
        self.w.write(json.dumps(m).encode() + b'\0')
        while True:
            res = self._read()
            if res.get('id') == self.n:
                if 'error' in res: raise RuntimeError(f"{method}: {res['error']}")
                return res.get('result', {})
    def eval(self, expr):
        r = self.call('Runtime.evaluate', {'expression': expr, 'returnByValue': True, 'awaitPromise': True})
        return r.get('result', {}).get('value')
    def close(self):
        try: self.call('Browser.close', session=False)
        except Exception: pass
        self.p.wait(timeout=10)

def translated(lang):
    """compo.<lang>.html : textes traduits (i18n.txt), langue du document, remplacements propres au projet (EXTRA)."""
    import re
    from pathlib import Path
    root = next(p for p in Path(__file__).resolve().parents if (p / '_tools').is_dir())
    sys.path.insert(0, str(root / '_tools'))
    import units
    src = open(os.path.join(HERE, 'compo.html'), encoding='utf-8').read()
    src = units.apply(src, units.load(os.path.join(HERE, 'i18n.txt')), lang)
    src = re.sub(r'<html lang="fr">', f'<html lang="{lang}">', src, count=1)
    for item in EXTRA:  # (avant, après) ou (avant, après, langues concernées)
        a, b = item[0], item[1]
        if len(item) > 2 and lang not in item[2]:
            continue
        assert a in src, a
        src = src.replace(a, b.format(lang=lang))
    name = f'compo.{lang}.html'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(src)
    return name


def main():
    fmt = sys.argv[1] if len(sys.argv) > 1 else '45'
    W, H = {'916': (1080, 1920), '169': (1920, 1080)}.get(fmt, (1080, 1350))
    stills = None
    if '--stills' in sys.argv: stills = [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]
    fps = int(sys.argv[sys.argv.index('--fps') + 1]) if '--fps' in sys.argv else 30
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    c.call('Emulation.setDeviceMetricsOverride', {'width': W, 'height': H, 'deviceScaleFactor': 1, 'mobile': False})
    c.call('Page.enable')
    lang = sys.argv[sys.argv.index('--lang') + 1] if '--lang' in sys.argv else 'fr'
    page = 'compo.html' if lang == 'fr' else translated(lang)
    c.call('Page.navigate', {'url': 'file://' + os.path.join(HERE, page) + '?f=' + fmt})
    for _ in range(300):
        if c.eval('window.READY === true'): break
        time.sleep(.1)
    else: raise RuntimeError('page not ready')
    json.dump({'cues': c.eval('window.CUES'), 'meta': c.eval('window.META')}, open(os.path.join(HERE, 'cues.json' if lang == 'fr' else f'cues.{lang}.json'), 'w'))
    clip = {'x': 0, 'y': 0, 'width': W, 'height': H, 'scale': 1}
    def frame(t, q=90):
        c.eval(f'render({t:.5f})')
        return base64.b64decode(c.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': q, 'clip': clip})['data'])
    if stills:
        os.makedirs(os.path.join(HERE, 'stills'), exist_ok=True)
        for t in stills:
            open(os.path.join(HERE, 'stills', f'{fmt}_{lang}_{t:05.2f}.jpg'), 'wb').write(frame(t, 85))
        c.close(); print('stills', len(stills)); return
    out = os.path.join(HERE, f'frames_{fmt}.mp4' if lang == 'fr' else f'frames_{fmt}_{lang}.mp4')
    ff = subprocess.Popen([FFMPEG, '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    N = 60 * fps; t0 = time.time()
    for i in range(N):
        ff.stdin.write(frame(i / fps, 93))
        if i % 300 == 0: print(f'{fmt} {i}/{N} {time.time() - t0:.0f}s', flush=True)
    ff.stdin.close(); ff.wait(); c.close()
    print('video', out, f'{time.time() - t0:.0f}s')

if __name__ == '__main__':
    main()
