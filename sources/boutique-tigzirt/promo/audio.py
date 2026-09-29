"""Bande-son de la vidéo Tiziri : musique synthétisée (100 BPM, la mineur harmonique, corde pincée et darbouka)
et bruitages calés sur cues.json (écrit par render.py).

python3 audio.py                 → audio.wav (musique et bruitages)
python3 audio.py --voix fr       → audio-voix-fr.wav : la même bande, baissée sous la voix de voix/fr/*.wav
Sorties : 48 kHz, stéréo, 16 bits. Aucun échantillon, aucun son sous droits.
"""
import json, os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__))
SR, DUR = 48000, 60.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
BEAT = .6; BAR = BEAT * 4
music, send, sfx = (np.zeros((2, N)) for _ in range(3))


def place(bus, sig, t, pan=0., gain=1.):
    i = int(round(t * SR))
    if i >= N: return
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i); a = (pan + 1) * np.pi / 4
    bus[0, i:i + n] += sig[:n] * np.cos(a) * gain; bus[1, i:i + n] += sig[:n] * np.sin(a) * gain
def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440. * 2 ** ((m - 69) / 12)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def env(t, a, dec): return np.minimum(1, t / a) * np.exp(-t * dec)
def noise(d): return rng.normal(0, 1, int(d * SR))


# ---------- timbres ----------
def ks(m, d=1.2, bright=.5, vel=1.):
    """corde pincée (Karplus-Strong) : une mandole discrète"""
    f = hz(m); P = max(2, int(round(SR / f))); n = int(d * SR)
    y = np.zeros(n + P); y[:P] = rng.uniform(-1, 1, P) * vel
    y[:P] = lp(y[:P], 1500 + 6000 * bright, 1)
    decay = .996 if m < 60 else .993
    for k in range(P, n + P, P):
        prev = y[k - P:k]; blk = .5 * (prev + np.roll(prev, 1)) * decay
        y[k:k + P] = blk[:len(y[k:k + P])]
    return y[P:] * np.minimum(1, tt(d) / .002)
def bell(m, vel=1., d=2.):
    t = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + .45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 7)
    return s * np.minimum(1, t / .003) * vel
def pad(ms, d, vel=1., cut=1600):
    t = tt(d + .8); s = np.zeros_like(t)
    for m in ms:
        for det in (-.0028, .0031):
            for k in range(1, 7): s += np.sin(2 * np.pi * hz(m) * (1 + det) * k * t + k * det * 400) / k
    e = np.minimum(1, t / .6) * np.where(t < d, 1, np.exp(-(t - d) * 5))
    return lp(s * e, cut) * vel / (len(ms) * 6)
def bass(m, d=.55, vel=1.):
    t = tt(d); f = hz(m)
    return lp((np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * env(t, .004, 3.2), 500) * vel
def kick(vel=1.):
    t = tt(.4); ph = 2 * np.pi * np.cumsum(45 + 115 * np.exp(-t * 26)) / SR
    s = np.sin(ph) * np.exp(-t * 8.5); s[:150] += rng.normal(0, .25, 150) * np.linspace(1, 0, 150)
    return s * vel
def doum(vel=1.):
    """darbouka, frappe grave au centre de la peau"""
    t = tt(.5); ph = 2 * np.pi * np.cumsum(78 + 60 * np.exp(-t * 30)) / SR
    return (np.sin(ph) * np.exp(-t * 7) + lp(noise(.5), 500) * np.exp(-t * 40) * .25) * vel
def tek(vel=1., bright=1.):
    """darbouka, frappe claire sur le bord"""
    t = tt(.12)
    return (bp(noise(.12), 1800 * bright, 6500) * np.exp(-t * 55) + np.sin(2 * np.pi * 620 * t) * np.exp(-t * 70) * .5) * vel * .55
def shaker(vel=1.):
    t = tt(.09); return bp(noise(.09), 4000, 11000) * np.sin(np.pi * np.clip(t / .09, 0, 1)) ** 2 * vel * .5


# ---------- musique : la mineur harmonique (Am, F, Dm, E7) ----------
PROG = [([57, 64, 69, 72, 76, 72, 69, 64], [57, 60, 64, 69], 45), ([53, 60, 65, 69, 72, 69, 65, 60], [53, 57, 60, 65], 41),
        ([50, 57, 62, 65, 69, 65, 62, 57], [50, 53, 57, 62], 38), ([52, 59, 64, 68, 71, 68, 64, 59], [52, 56, 59, 62], 40)]
BREAK = (8, 9)          # 19,2 – 24 s : la marque, la musique se pose
for b in range(25):
    t0 = b * BAR; arp, chord, root = PROG[b % 4] if b < 24 else PROG[0]
    brk = BREAK[0] <= b <= BREAK[1]; intro = b <= 1; outro = b == 24
    if not outro:
        for i, m in enumerate(arp):
            if intro and i % 2: continue
            v = (1. if i % 4 == 0 else .7) * (.55 if intro else .45 if brk else .8)
            place(music, ks(m, 1.1, .45, v * .85), t0 + i * BEAT / 2, pan=(-.35 if i % 2 else .3)); place(send, ks(m, 1.1, .45, v * .25), t0 + i * BEAT / 2)
            if brk and i % 2 == 0:
                place(music, bell(m + 12, v * .3, 1.8), t0 + i * BEAT / 2, pan=(-.4 if i % 4 else .4)); place(send, bell(m + 12, v * .3, 1.8), t0 + i * BEAT / 2)
    place(music, pad(chord, BAR if not outro else 2.2, (.85 if brk else .5 if not intro else .45)), t0)
    place(send, pad(chord, BAR, .25), t0)
    if not intro and not outro and not brk:
        for i, off in enumerate([0, 1.5 * BEAT, 2 * BEAT, 3.5 * BEAT]):
            place(music, bass(root if i != 2 else root + 12 if b % 2 else root, .5, .95 if i == 0 else .7), t0 + off)
    if b >= 2 and not outro and not brk:
        # maqsoum : doum, tek, ·, tek, doum, ·, tek, · (en croches), et des frappes fantômes
        for k, hit in enumerate('DT.TD.T.'):
            at = t0 + k * BEAT / 2 + (.012 if k % 2 else 0)
            if hit == 'D': place(music, doum(.9), at, pan=-.1)
            elif hit == 'T': place(music, tek(.55), at, pan=.25); place(send, tek(.2), at)
            elif b >= 4: place(music, tek(.14, 1.3), at, pan=.35)
        place(music, kick(.55), t0)
        if b >= 10:
            for k in range(8): place(music, shaker(.28 if k % 2 else .18), t0 + k * BEAT / 2 + .01, pan=.45)
fin = PROG[0][1]
for i, m in enumerate(fin + [fin[-1] + 12]):
    v = bell(m + 12, .45, 2.6)
    place(music, v, 57.6 + i * .04, pan=(i - 2) * .15); place(send, v * .5, 57.6 + i * .04)
place(music, doum(1.), 57.6); place(music, kick(.8), 57.6)


# ---------- bruitages ----------
def whoosh(d=.55, lo=300, hi=3200, g=1.):
    n = int(d * SR); x = noise(d); out = np.zeros(n); seg = 16; L = n // seg
    for k in range(seg):
        fc = lo * (hi / lo) ** (k / (seg - 1)); y = bp(x, fc * .7, min(fc * 1.4, SR / 2 - 100))
        w = np.zeros(n); a, b = max(0, (k - 1) * L), min(n, (k + 2) * L); w[a:b] = np.hanning(b - a); out += y * w
    return out * np.sin(np.pi * np.arange(n) / SR / d) ** 2 * g
def ting(f, d=.9):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 8)) * env(t, .002, 7.5)
def sparkle(t0, g=1.):
    for j in range(6):
        f = [2637, 3136, 3520, 3951, 4699, 5274][rng.integers(0, 6)]
        place(sfx, ting(f) * .1 * g, t0 + j * .045 + rng.uniform(0, .02), pan=rng.uniform(-.7, .7)); place(send, ting(f) * .08 * g, t0 + j * .045)
def pop(g=1.):
    t = tt(.09); f0 = 1100 * rng.uniform(.9, 1.12); ph = 2 * np.pi * np.cumsum(380 + (f0 - 380) * np.exp(-t * 55)) / SR
    return np.sin(ph) * env(t, .001, 38) * g
def click(g=1., f=1600):
    t = tt(.05); return (np.sin(2 * np.pi * f * t) * np.exp(-t * 120) + hp(noise(.05), 3000) * np.exp(-t * 200) * .5) * g
def shutter(t0):
    """déclencheur d'appareil photo : deux claquements mécaniques"""
    for off, g in ((0, .5), (.075, .38)):
        t = tt(.06); s = bp(noise(.06), 1200, 7000) * np.exp(-t * 90) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 60) * .4
        place(sfx, s * g, t0 + off, pan=.1)
def ding(t0, g=1.):
    """notification de message : deux notes rondes"""
    for off, m in ((0, 84), (.11, 91)):
        s = bell(m, .5, 1.2); place(sfx, s * .28 * g, t0 + off); place(send, s * .12 * g, t0 + off)


cues = json.load(open(os.path.join(HERE, 'cues.json')))['cues']
for t0, kind, arg in cues:
    if kind == 'shutter': shutter(t0)
    elif kind == 'scan': place(sfx, whoosh(1.3, 400, 6000, .22), t0); sparkle(t0 + 1.2, .8)
    elif kind == 'pop': place(sfx, pop(.2), t0, pan=rng.uniform(-.25, .25))
    elif kind == 'blip': place(sfx, pop(.12), t0, pan=-.2)
    elif kind == 'whoosh': place(sfx, whoosh(.9, 250, 2500, .2), t0 - .05)
    elif kind == 'glow':
        sparkle(t0, 1.1)
        for j, m in enumerate((81, 88, 93)): place(sfx, bell(m, .16, 2.2), t0 + j * .05, pan=(j - 1) * .3); place(send, bell(m, .18, 2.2), t0 + j * .05)
    elif kind == 'sweep': place(sfx, whoosh(.75, 250, 4200, .3), t0 - .05); place(send, whoosh(.75, 800, 5000, .1), t0)
    elif kind == 'sparkle': sparkle(t0)
    elif kind == 'swipe': place(sfx, whoosh(.38, 600, 4000, .16), t0, pan=.2)
    elif kind == 'tap': place(sfx, click(.16), t0, pan=.1)
    elif kind == 'key': place(sfx, click(.045 + .02 * rng.random(), 1300 + 700 * rng.random()), t0 + rng.uniform(0, .03), pan=.15)
    elif kind == 'send': place(sfx, pop(.22), t0, pan=.2); place(sfx, whoosh(.3, 900, 5000, .12), t0, pan=.3)
    elif kind == 'ding': ding(t0)
    elif kind == 'impact':
        place(sfx, doum(.9), t0); place(sfx, kick(.7), t0)
        t = tt(2.2); cr = hp(noise(2.2), 3500) * np.exp(-t * 2.4) * .16; place(sfx, cr, t0); place(send, cr * .6, t0)

t = tt(1.8)
ir = np.stack([lp(rng.normal(0, 1, len(t)), 6000) * np.exp(-t * 3.4) for _ in range(2)]); ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
wet = np.stack([fftconvolve(send[c], ir[c])[:N] for c in range(2)])
bed = music * .5 + wet * .5 + sfx * .95


def master(mix, path):
    fade = np.ones(N); fade[:int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR)); fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
    mix = np.tanh(mix * fade * 1.7) / np.tanh(1.7); mix *= .89 / np.abs(mix).max()
    pcm = (mix.T * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return 20 * np.log10(np.sqrt((mix ** 2).mean()))


def read_wav(path):
    """WAV mono ou stéréo, 16 bits, rééchantillonné à 48 kHz, en mono."""
    with wave.open(path) as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), '<i2').astype(float) / 32768
    x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        x = np.interp(np.arange(int(len(x) * SR / sr)) / SR, np.arange(len(x)) / sr, x)
    return x


if '--voix' in sys.argv:
    # La voix off : phrases posées aux instants de voix/<langue>/voix.json, la musique baisse dessous (−11 dB, lissé).
    lang = sys.argv[sys.argv.index('--voix') + 1]
    d = os.path.join(HERE, 'voix', lang)
    plan = json.load(open(os.path.join(d, 'voix.json'), encoding='utf-8'))
    voice = np.zeros(N)
    for line in plan['lignes']:
        x = read_wav(os.path.join(d, line['fichier']))
        x = hp(x, 80) / (np.abs(x).max() + 1e-9) * .9
        i = int(line['t'] * SR); n = min(len(x), N - i); voice[i:i + n] += x[:n]
    active = np.convolve(np.abs(voice) > .02, np.ones(int(.25 * SR)), 'same') > 0
    duck = lp(np.where(active, 10 ** (-11 / 20), 1.), 3, 1)
    mix = bed * duck + np.stack([voice, voice]) * .62
    db = master(mix, os.path.join(HERE, f'audio-voix-{lang}.wav'))
    print(f'audio-voix-{lang}.wav rms {db:.1f} dBFS, {len(plan["lignes"])} phrases')
else:
    db = master(bed, os.path.join(HERE, 'audio.wav'))
    print(f'audio.wav rms {db:.1f} dBFS cues {len(cues)}')
