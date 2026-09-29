"""Visite guidée filmée d'un site en ligne : défilement, curseur, clics et carte de fin, rendus image par image.

Le temps de la page est ralenti (horloges JavaScript, minuteries et animations CSS au même facteur) : Chrome a tout
le temps de dessiner chaque image, et la vidéo garde la vitesse réelle des animations.

python3 tour.py URL plan.json sortie.mp4 [--rate .15] [--size 1920x1080] [--fps 30]
plan.json : {"duration": secondes, "steps": [...], "mascot": {...} facultatif} (voir youtube/<projet>/make.py et uko.py)
"""
import base64, json, os, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / '_tools').is_dir())
sys.path.insert(0, str(ROOT / '_tools'))
from check import CDP  # noqa: E402

# horloges ralenties, installées avant tout script de la page
TIME_SCALE = """(() => {
  const R = __RATE__;
  const pNow = performance.now.bind(performance), p0 = pNow();
  const vnow = () => p0 + (pNow() - p0) * R;
  performance.now = vnow;
  const dNow = Date.now, d0 = dNow();
  Date.now = () => d0 + (dNow() - d0) * R;
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = cb => raf(() => cb(vnow()));
  const st = window.setTimeout.bind(window), si = window.setInterval.bind(window);
  window.setTimeout = (fn, ms, ...a) => st(fn, (ms || 0) / R, ...a);
  window.setInterval = (fn, ms, ...a) => si(fn, (ms || 0) / R, ...a);
  window.__vnow = vnow;
})();"""

# moteur de visite : étapes datées en secondes de vidéo
ENGINE = r"""window.__tour = (() => {
  const vnow = window.__vnow;
  const ease = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
  const q = s => document.querySelector(s);
  let t0 = 0, steps = [], cur = null, ring = null, card = null, pos = [innerWidth * .62, innerHeight * .7], clickAt = -9;
  // mascotte Uko (optionnelle) : moteur en pause, avancé image par image sur le temps de la vidéo
  let uko = null, host = null, mc = null, hx = 0, feet = 0, lastT = 0, walk = null;
  function mascot(cfg) {
    mc = cfg;
    host = document.createElement('div'); host.id = 'tour-uko';
    Object.assign(host.style, { position: 'fixed', left: '0', top: '0', width: cfg.height * 2 / 3 + 'px', height: cfg.height + 'px', zIndex: 2147483646, pointerEvents: 'none' });
    document.body.append(host);
    uko = UkoMascot.create('#tour-uko', { character: cfg.character || 'uko', state: 'idle', hairStyle: cfg.hair || 'original', interactive: false, follow: 'none', oneShotMode: 'return' });
    uko.pause(); uko.step(0);
    if (cfg.theme) uko.setTheme(cfg.theme);
    const p = uko.getPose(), f = k => (p[k + '_center'] || p[k.replace('foot', 'ankle')])[1];
    feet = (Math.max(f('foot_L'), f('foot_R')) + 22) / 1536 * cfg.height;
    hx = cfg.x; place();
  }
  function place() { host.style.transform = `translate(${hx - mc.height / 3}px, ${mc.ground - feet}px)`; }
  function talk(a) {
    // bouche ouverte selon la voix : remplace le trait de la bouche (dernier élément du visage) par une bouche ronde
    if (a < .06) return;
    const svg = uko.getSvgElement(), mark = svg.querySelector('.blush') || svg.querySelector('.eye');
    const m = mark && mark.parentNode.lastElementChild;
    if (!m || m.getAttribute('class') !== 'faceStroke') return;
    const b = m.getBBox(), e = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
    e.setAttribute('class', 'faceOpenMouth');
    e.setAttribute('cx', b.x + b.width / 2); e.setAttribute('cy', b.y + b.height / 2 + 3);
    e.setAttribute('rx', Math.max(18, Math.min(38, b.width * .45)) * (.85 + .25 * a)); e.setAttribute('ry', 6 + 22 * a);
    m.replaceWith(e);
  }
  function ukoInit(s) {
    if (s.act === 'walk') { s.dir = Math.sign(s.x - hx) || 1; uko.startWalk(s.dir, s.speed || 1.8); walk = s; }
    else if (s.act === 'look') uko.lookAt(s.sel ? q(s.sel) : s.xy ? { x: s.xy[0], y: s.xy[1] } : null);
    else if (s.act === 'state') { if (walk) { uko.stopWalk(); walk = null; } uko.setState(s.pose); }
    else if (s.act === 'poke') uko.poke(s.zone || 'body', s.reaction);
    else if (s.act === 'turn') uko.setOrientation(s.yaw || 0);
    else if (s.act === 'theme') uko.setTheme(s.theme);
    else if (s.act === 'brand') uko.setBrandColor(s.color);
  }
  function ukoFrame(t) {
    const dt = Math.max(0, t - lastT); lastT = t;
    if (walk) {
      hx += uko.getWalkVelocity() * mc.height / 1536 * dt;
      if ((walk.dir > 0 && hx >= walk.x) || (walk.dir < 0 && hx <= walk.x)) { hx = walk.x; uko.stopWalk(); walk = null; }
    }
    place();
    uko.step(dt * 1000);
    const mo = mc.mouth || [];
    talk(mo[Math.min(mo.length - 1, Math.floor(t * 30))] || 0);
  }
  const time = () => (vnow() - t0) / 1000;
  function y(spec) {
    if (spec.y != null) return spec.y;
    const el = q(spec.sel), top = el.getBoundingClientRect().top + scrollY;
    if (spec.p != null) return top + spec.p * Math.max(0, el.offsetHeight - innerHeight);
    return top + (spec.offset || 0);
  }
  function center(sel, off) {
    const r = q(sel).getBoundingClientRect();
    return [r.left + r.width * (off ? off[0] : .5), r.top + r.height * (off ? off[1] : .5)];
  }
  function overlay() {
    cur = document.createElement('div');
    cur.innerHTML = '<svg width="30" height="38" viewBox="0 0 30 38"><path d="M3 2 L3 31 L10.5 24.5 L15.5 35.5 L20.5 33.3 L15.6 22.6 L25.5 22.2 Z" fill="#fff" stroke="#111" stroke-width="2.2" stroke-linejoin="round"/></svg>';
    Object.assign(cur.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, pointerEvents: 'none', filter: 'drop-shadow(0 3px 6px rgba(0,0,0,.35))', opacity: '0', willChange: 'transform' });
    ring = document.createElement('div');
    Object.assign(ring.style, { position: 'fixed', left: '0', top: '0', width: '46px', height: '46px', marginLeft: '-23px', marginTop: '-23px', borderRadius: '50%',
      border: '3px solid rgba(255,255,255,.95)', boxShadow: '0 0 0 2px rgba(0,0,0,.25)', zIndex: 2147483646, pointerEvents: 'none', opacity: '0' });
    document.body.append(ring, cur);
  }
  function draw() {
    cur.style.transform = `translate(${pos[0] - 3}px, ${pos[1] - 2}px)`;
    const k = time() - clickAt;
    if (k >= 0 && k < .6) { const e = k / .6; ring.style.opacity = String(1 - e); ring.style.transform = `translate(${pos[0]}px, ${pos[1]}px) scale(${.4 + e * 1.2})`; }
    else ring.style.opacity = '0';
  }
  function init(s) {
    if (s.do === 'scroll') { s.y0 = scrollY; s.y1 = y(s.to); }
    else if (s.do === 'cursor') { s.p0 = pos.slice(); s.p1 = s.sel ? center(s.sel, s.off) : s.xy; cur.style.opacity = '1'; }
    else if (s.do === 'hide') cur.style.opacity = '0';
    else if (s.do === 'click') { const el = q(s.sel); if (el) { pos = center(s.sel, s.off); clickAt = time(); el.click(); } }
    else if (s.do === 'range') { s.el = q(s.sel); }
    else if (s.do === 'uko' && uko) ukoInit(s);
    else if (s.do === 'card') {
      card = document.createElement('div'); card.innerHTML = s.html;
      Object.assign(card.style, { position: 'fixed', inset: '0', zIndex: 2147483645, opacity: '0' });
      document.body.append(card); cur.style.opacity = '0';
    }
  }
  function apply(s, e) {
    if (s.do === 'scroll') window.scrollTo(0, s.y0 + (s.y1 - s.y0) * e);
    else if (s.do === 'cursor') pos = [s.p0[0] + (s.p1[0] - s.p0[0]) * e, s.p0[1] + (s.p1[1] - s.p0[1]) * e];
    else if (s.do === 'range' && s.el) {
      const v = Math.round(s.from + (s.to - s.from) * e);
      if (String(v) !== s.el.value) { s.el.value = v; s.el.dispatchEvent(new Event('input', { bubbles: true })); }
    }
    else if (s.do === 'card' && card) card.style.opacity = String(e);
  }
  function tick() {
    const t = time();
    for (const s of steps) {
      if (t < s.t || s.state === 'done') continue;
      if (!s.state) { s.state = 'run'; init(s); }
      const k = s.d ? Math.min(1, (t - s.t) / s.d) : 1;
      apply(s, ease(k));
      if (k >= 1) s.state = 'done';
    }
    if (uko) ukoFrame(t);
    draw();
    requestAnimationFrame(tick);
  }
  return {
    start(plan) {
      document.documentElement.style.scrollBehavior = 'auto';
      window.scrollTo(0, 0);
      overlay();
      if (plan.mascot) mascot(plan.mascot);
      steps = plan.steps.slice().sort((a, b) => a.t - b.t);
      t0 = vnow();
      requestAnimationFrame(tick);
      return true;
    },
    time
  };
})();"""


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    url, plan_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rate = float(opt('--rate', '.15'))
    W, H = map(int, opt('--size', '1920x1080').split('x'))
    fps = int(opt('--fps', '30'))
    plan = json.load(open(plan_path, encoding='utf-8'))
    dur = plan['duration']
    c = CDP()
    tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
    c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
    for d in ('Page', 'Runtime', 'Animation'):
        c.call(f'{d}.enable')
    c.call('Page.setBypassCSP', {'enabled': True})
    c.call('Emulation.setDeviceMetricsOverride', {'width': W, 'height': H, 'deviceScaleFactor': 1, 'mobile': False})
    c.call('Page.addScriptToEvaluateOnNewDocument', {'source': TIME_SCALE.replace('__RATE__', str(rate))})
    c.call('Page.navigate', {'url': url})
    for _ in range(300):
        if c.eval("document.readyState === 'complete'"):
            break
        time.sleep(.1)
    c.eval('document.fonts.ready.then(() => true)')
    c.eval("Promise.all([...document.images].filter(i => i.loading !== 'lazy').map(i => i.decode().catch(() => {}))).then(() => true)")
    c.call('Animation.setPlaybackRate', {'playbackRate': rate})
    time.sleep(1.5)
    if plan.get('mascot'):
        src = plan['mascot']['engine']
        code = (urllib.request.urlopen(urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8')
                if src.startswith('https://') else open(src, encoding='utf-8').read())
        c.eval(code + ';true')
    c.eval(ENGINE)
    assert c.eval(f'__tour.start({json.dumps(plan)})') is True
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    n, prev, grabs, t_real = 0, None, 0, time.time()
    total = int(dur * fps)
    while n < total:
        t = c.eval('__tour.time()')
        img = base64.b64decode(c.call('Page.captureScreenshot', {'format': 'jpeg', 'quality': 90})['data'])
        grabs += 1
        # chaque image de sortie reçoit la dernière capture prise avant son instant
        while prev is not None and n < total and n / fps < t:
            ff.stdin.write(prev); n += 1
        prev = img
        if grabs % 150 == 0:
            print(f'{os.path.basename(out)} {n}/{total} images · {grabs} captures · {time.time() - t_real:.0f} s', flush=True)
    ff.stdin.close(); ff.wait(); c.close()
    if getattr(c, 'tmp', None):  # profil Chrome temporaire de ce rendu (≈ 150 Mo)
        shutil.rmtree(c.tmp, ignore_errors=True)
    print(f'{out} · {total} images · {grabs} captures ({grabs / max(1, total):.1f} par image) · {time.time() - t_real:.0f} s')


if __name__ == '__main__':
    main()
