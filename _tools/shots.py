"""Captures d'écran en série de sites exportés, servis en local.

python3 shots.py LISTE.json
LISTE : [{"dir": "...", "page": "en.html", "w": 1440, "h": 900, "dpr": 1, "out": ".../x.webp", "wait": 3, "scroll": 0}, …]
Le format de sortie suit l'extension (.webp, .jpg, .png).
"""
import base64, io, json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import CDP, serve  # noqa: E402


def main():
    jobs = json.load(open(sys.argv[1]))
    servers = {}
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    c.call('Page.enable'); c.call('Runtime.enable')
    for j in jobs:
        if j['dir'] not in servers:
            servers[j['dir']] = serve(j['dir'])
        origin = servers[j['dir']][1]
        c.call('Emulation.setDeviceMetricsOverride', {'width': j['w'], 'height': j['h'], 'deviceScaleFactor': j.get('dpr', 1), 'mobile': j['w'] < 700})
        if j.get('locale'):
            ua = c.call('Browser.getVersion', session=False)['userAgent'].replace('Headless', '')
            c.call('Emulation.setUserAgentOverride', {'userAgent': ua, 'acceptLanguage': j['locale']})
        c.call('Page.navigate', {'url': origin + j['page']})
        c.pump(j.get('wait', 3))
        if j.get('scroll'):
            c.eval(f"window.scrollTo(0, {j['scroll']})")
            c.pump(1.5)
        if j.get('js'):
            c.eval(j['js'])
            c.pump(0.8)
        data = base64.b64decode(c.call('Page.captureScreenshot', {'format': 'png'})['data'])
        im = Image.open(io.BytesIO(data)).convert('RGB')
        out = j['out']
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if out.endswith('.webp'):
            im.save(out, 'WEBP', quality=j.get('q', 80), method=6)
        elif out.endswith('.jpg'):
            im.save(out, 'JPEG', quality=j.get('q', 84), optimize=True, progressive=True)
        else:
            im.save(out, optimize=True)
        print(os.path.basename(out), im.size, os.path.getsize(out) // 1024, 'Ko', flush=True)
    c.close()
    for s, _ in servers.values():
        s.shutdown()


if __name__ == '__main__':
    main()
