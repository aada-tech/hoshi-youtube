"""Planche contact d'un site exporté : une capture par section, animation déployée.

python3 sheet.py DIR PAGE WxH OUT.jpg [--cols 4] [--scale .35] [--at .9]
"""
import base64, io, sys, time
from PIL import Image
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from check import CDP, serve, opt  # noqa: E402


def main():
    root, page, size, out = sys.argv[1:5]
    W, H = map(int, size.split('x'))
    cols, scale, at = int(opt('--cols', '4')), float(opt('--scale', '.35')), float(opt('--at', '.9'))
    srv, origin = serve(root)
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    c.call('Page.enable'); c.call('Runtime.enable')
    c.call('Emulation.setDeviceMetricsOverride', {'width': W, 'height': H, 'deviceScaleFactor': 1, 'mobile': W < 700})
    c.call('Page.navigate', {'url': origin + page})
    c.pump(3.5)
    ys = c.eval(f"""[...document.querySelectorAll('main > section, main > div, body > footer, main > footer')]
        .filter(s => s.offsetHeight > 120)
        .map(s => {{ const r = s.getBoundingClientRect(), top = r.top + scrollY, extra = Math.max(0, s.offsetHeight - innerHeight);
                    return Math.round(top + (extra ? extra * {at} : Math.min(80, s.offsetHeight / 4))); }})""")
    shots = []
    for y in ys:
        c.eval(f'window.scrollTo(0, {y})')
        c.pump(1.6)
        data = c.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 80})['data']
        im = Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB')
        shots.append(im.resize((int(W * scale), int(H * scale))))
    c.close(); srv.shutdown()
    w, h = shots[0].size
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * w + (cols + 1) * 8, rows * h + (rows + 1) * 8), '#888')
    for i, im in enumerate(shots):
        sheet.paste(im, (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
    sheet.save(out, quality=82)
    print(out, len(shots), 'sections')


if __name__ == '__main__':
    main()
