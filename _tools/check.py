"""Contrôle d'un site exporté, servi en local : erreurs JS, violations CSP, requêtes en échec, requêtes vers l'extérieur, captures.

python3 check.py DIR|URL PAGE [PAGE…] [--size 1440x900,390x844] [--scroll 0,1200] [--shots PREFIX] [--wait 3] [--js EXPR]
"""
import base64, functools, http.server, json, os, shutil, socketserver, subprocess, sys, tempfile, threading, time

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


class CDP:
    def __init__(self):
        r1, w1 = os.pipe(); r2, w2 = os.pipe()

        def pre():
            os.dup2(r1, 3); os.dup2(w2, 4)
        self.tmp = tempfile.mkdtemp()
        self.p = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-pipe', '--disable-gpu', '--hide-scrollbars',
                                   '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--force-device-scale-factor=1',
                                   f'--user-data-dir={self.tmp}', 'about:blank'],
                                  pass_fds=(3, 4), preexec_fn=pre, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.close(r1); os.close(w2)
        self.w = os.fdopen(w1, 'wb', buffering=0); self.r = os.fdopen(r2, 'rb', buffering=0)
        self.buf = b''; self.n = 0; self.session = None; self.events = []

    def _read(self):
        while b'\0' not in self.buf:
            chunk = self.r.read(1 << 20)
            if not chunk:
                raise RuntimeError('chrome closed')
            self.buf += chunk
        msg, self.buf = self.buf.split(b'\0', 1)
        return json.loads(msg)

    def call(self, method, params=None, session=True):
        self.n += 1
        m = {'id': self.n, 'method': method, 'params': params or {}}
        if session and self.session:
            m['sessionId'] = self.session
        self.w.write(json.dumps(m).encode() + b'\0')
        while True:
            res = self._read()
            if res.get('id') == self.n:
                if 'error' in res:
                    raise RuntimeError(f"{method}: {res['error']}")
                return res.get('result', {})
            if 'method' in res:
                self.events.append(res)

    def pump(self, seconds):
        """Laisse tourner la page en collectant les événements."""
        end = time.time() + seconds
        while time.time() < end:
            self.call('Runtime.evaluate', {'expression': '1'})
            time.sleep(0.1)

    def eval(self, expr):
        r = self.call('Runtime.evaluate', {'expression': expr, 'returnByValue': True, 'awaitPromise': True})
        return r.get('result', {}).get('value')

    def close(self):
        try:
            self.call('Browser.close', session=False)
        except Exception:
            pass
        self.p.wait(timeout=10)
        # le profil Chrome temporaire (~150 Mo de caches) : sans ce ménage, chaque capture en laissait un dans $TMPDIR
        shutil.rmtree(self.tmp, ignore_errors=True)


def serve(root):
    handler = functools.partial(type('Quiet', (http.server.SimpleHTTPRequestHandler,), {'log_message': lambda *a: None}), directory=root)
    srv = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f'http://127.0.0.1:{srv.server_address[1]}/'


def opt(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith('--') and not sys.argv[i - 1].startswith('--')]
    root, pages = args[0], args[1:]
    live = root.startswith(('http://', 'https://'))
    root = root if live else os.path.abspath(root)
    sizes = [tuple(map(int, s.split('x'))) for s in opt('--size', '1440x900').split(',')]
    scrolls = [int(y) for y in opt('--scroll', '0').split(',')]
    shots, wait, js = opt('--shots'), float(opt('--wait', '3')), opt('--js')
    srv, origin = (None, root if root.endswith('/') else root + '/') if live else serve(root)
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    for d in ('Page', 'Runtime', 'Log', 'Network'):
        c.call(f'{d}.enable')
    if opt('--locale'):
        ua = c.call('Browser.getVersion', session=False)['userAgent'].replace('Headless', '')
        c.call('Emulation.setUserAgentOverride', {'userAgent': ua, 'acceptLanguage': opt('--locale')})
    problems = 0
    for page in pages:
        for (W, H) in sizes:
            c.events.clear()
            c.call('Emulation.setDeviceMetricsOverride', {'width': W, 'height': H, 'deviceScaleFactor': 1, 'mobile': W < 700})
            c.call('Page.navigate', {'url': origin + page})
            c.pump(wait)
            if js:
                print(f'  js → {c.eval(js)}')
            print(f'  url → {c.eval("location.pathname")}')
            for y in scrolls:
                if y:
                    c.eval(f'window.scrollTo(0, {y})')
                    c.pump(1.5)
                if shots:
                    data = c.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 82})['data']
                    name = f"{shots}-{page.replace('/', '_').replace('.html', '') or 'index'}-{W}x{H}-{y}.jpg"
                    open(name, 'wb').write(base64.b64decode(data))
            issues = []
            over = c.eval('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if over and over > 1:
                wide = c.eval("[...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1).slice(0, 4).map(e => e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '')).join(', ')")
                issues.append(f'débordement horizontal : {over} px ({wide})')
            for e in c.events:
                m, p = e['method'], e.get('params', {})
                if m == 'Runtime.exceptionThrown':
                    d = p['exceptionDetails']
                    issues.append('exception : ' + (d.get('exception', {}).get('description') or d.get('text', ''))[:300])
                elif m == 'Runtime.consoleAPICalled' and p['type'] in ('error', 'warning', 'assert'):
                    issues.append(f"console.{p['type']} : " + ' '.join(str(a.get('value', a.get('description', ''))) for a in p['args'])[:300])
                elif m == 'Log.entryAdded' and p['entry']['level'] in ('error', 'warning'):
                    issues.append(f"log {p['entry']['source']} : {p['entry']['text'][:300]}")
                elif m == 'Network.requestWillBeSent':
                    u = p['request']['url']
                    if not (u.startswith(origin) or u.startswith('data:') or u.startswith('blob:')):
                        issues.append('requête externe : ' + u[:200])
                elif m == 'Network.loadingFailed' and not p.get('canceled'):
                    issues.append(f"échec réseau : {p.get('errorText')} {p.get('blockedReason', '')}")
                elif m == 'Network.responseReceived' and p['response']['status'] >= 400:
                    issues.append(f"HTTP {p['response']['status']} : {p['response']['url'][:200]}")
            problems += len(issues)
            print(f"{page or 'index'} {W}x{H} : " + ('OK' if not issues else f'{len(issues)} problème(s)'))
            for i in dict.fromkeys(issues):
                print('   · ' + i)
    c.close()
    if srv:
        srv.shutdown()
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
