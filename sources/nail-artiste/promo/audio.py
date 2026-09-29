"""Bande-son synthétisée (musique + bruitages calés sur cues.json). usage : python3 audio.py billot|nacre|tafat"""
import json, os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = sys.argv[1] if len(sys.argv) > 1 else 'billot'
SR, DUR = 48000, 60.0
N = int(SR * DUR)
rng = np.random.default_rng(5)
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
    """corde pincée (Karplus-Strong), traitée par blocs"""
    f = hz(m); P = max(2, int(round(SR / f))); n = int(d * SR)
    y = np.zeros(n + P); y[:P] = rng.uniform(-1, 1, P) * vel
    y[:P] = lp(y[:P], 1500 + 6000 * bright, 1)
    decay = .996 if m < 60 else .993
    for k in range(P, n + P, P):
        prev = y[k - P:k]; blk = .5 * (prev + np.roll(prev, 1)) * decay
        y[k:k + P] = blk[:len(y[k:k + P])]
    return y[P:] * np.minimum(1, tt(d) / .002)
def marimba(m, vel=1., d=.9):
    t = tt(d); f = hz(m)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 4.5) + .38 * np.sin(2 * np.pi * 3.98 * f * t) * np.exp(-t * 16)) * np.minimum(1, t / .002) * vel
def bell(m, vel=1., d=2.):
    t = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) + .45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4) + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 7)
    return s * np.minimum(1, t / .003) * vel
def pad(ms, d, vel=1., cut=1700):
    t = tt(d + .8); s = np.zeros_like(t)
    for m in ms:
        for det in (-.0028, .0031):
            for k in range(1, 7): s += np.sin(2 * np.pi * hz(m) * (1 + det) * k * t + k * det * 400) / k
    e = np.minimum(1, t / .5) * np.where(t < d, 1, np.exp(-(t - d) * 5))
    return lp(s * e, cut) * vel / (len(ms) * 6)
def bass(m, d=.55, vel=1.):
    t = tt(d); f = hz(m)
    return lp((np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * env(t, .004, 3.2), 500) * vel
def kick(vel=1.):
    t = tt(.4); ph = 2 * np.pi * np.cumsum(45 + 115 * np.exp(-t * 26)) / SR
    s = np.sin(ph) * np.exp(-t * 8.5); s[:150] += rng.normal(0, .25, 150) * np.linspace(1, 0, 150)
    return s * vel
def clap(vel=1.):
    t = tt(.28); s = np.zeros_like(t)
    for off in (0, .009, .019):
        i = int(off * SR); s[i:] += rng.normal(0, 1, len(t) - i) * np.exp(-np.arange(len(t) - i) / SR * (32 if off < .019 else 16))
    return bp(s, 900, 3200) * vel * .55
def snap(vel=1.):
    t = tt(.12); return (bp(noise(.12), 1800, 6000) * np.exp(-t * 60) + np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 90) * .3) * vel * .5
def hat(vel=1., d=.05):
    t = tt(d); return hp(rng.normal(0, 1, len(t)), 7000) * np.exp(-t * (60 if d < .1 else 18)) * vel * .5
def shaker(vel=1.):
    t = tt(.09); return bp(noise(.09), 4000, 11000) * np.sin(np.pi * np.clip(t / .09, 0, 1)) ** 2 * vel * .5

# ---------- styles ----------
S = {
  'billot': dict(prog=[('Am', [57, 64, 69, 72, 76, 72, 69, 64], [45, 52, 57, 60], 45), ('F', [53, 60, 65, 69, 72, 69, 65, 60], [41, 48, 53, 57], 41),
                       ('C', [55, 60, 64, 67, 72, 67, 64, 60], [48, 55, 60, 64], 48), ('G', [55, 59, 62, 67, 71, 67, 62, 59], [43, 50, 55, 59], 43)],
                 lead='ks', breakdown=(15, 17), drums='stomp'),
  'nacre': dict(prog=[('Fmaj7', [65, 69, 72, 76, 77, 76, 72, 69], [41, 52, 57, 60, 64], 41), ('Em7', [64, 67, 71, 74, 76, 74, 71, 67], [40, 50, 55, 59, 62], 40),
                      ('Dm7', [62, 65, 69, 72, 74, 72, 69, 65], [38, 48, 53, 57, 60], 38), ('Cmaj7', [60, 64, 67, 71, 72, 71, 67, 64], [36, 47, 52, 55, 59], 36)],
                lead='bell', breakdown=(15, 17), drums='soft'),
}[STYLE]
for b in range(25):
    t0 = b * BAR; name, arp, chord, root = S['prog'][b % 4] if b < 24 else S['prog'][0]
    brk = S['breakdown'][0] <= b <= S['breakdown'][1]; intro = b <= 1; outro = b == 24
    if not outro:
        for i, m in enumerate(arp):
            v = (1. if i % 4 == 0 else .72) * (.55 if intro else .5 if brk else .8)
            if S['lead'] == 'ks':
                place(music, ks(m, 1.1, .45, v * .9), t0 + i * BEAT / 2, pan=(-.35 if i % 2 else .3)); place(send, ks(m, 1.1, .45, v * .25), t0 + i * BEAT / 2)
            else:
                if i % 2 == 0 or b >= 4:
                    place(music, bell(m + 12, v * .38, 1.6), t0 + i * BEAT / 2, pan=(-.4 if i % 2 else .4)); place(send, bell(m + 12, v * .3, 1.6), t0 + i * BEAT / 2)
    place(music, pad(chord, BAR if not outro else 2.2, (.8 if brk else .5 if not intro else .42) * (1.25 if S['lead'] == 'bell' else 1), 1500 if S['lead'] == 'bell' else 1700), t0)
    place(send, pad(chord, BAR, .25), t0)
    if not intro and not outro:
        for i, off in enumerate([0, 2 * BEAT, 3.5 * BEAT] if not brk else [0]):
            place(music, bass(root, .5, .95 if i == 0 else .75), t0 + off)
    if b >= 2 and not outro:
        if S['drums'] == 'stomp':
            for k in range(4):
                if not brk and k in (0, 2): place(music, kick(1.), t0 + k * BEAT)
                if not brk and k in (1, 3): place(music, clap(.75), t0 + k * BEAT, pan=.05); place(send, clap(.3), t0 + k * BEAT)
            for k in range(8): place(music, shaker(.35 if k % 2 else .22), t0 + k * BEAT / 2 + .01, pan=.4)
        else:
            if not brk: place(music, kick(.75), t0); place(music, kick(.55), t0 + 2.5 * BEAT)
            if not brk: place(music, snap(.8), t0 + 2 * BEAT, pan=.1); place(send, snap(.4), t0 + 2 * BEAT)
            for k in range(8): place(music, hat(.13 if k % 2 == 0 else .2), t0 + k * BEAT / 2 + .012, pan=.35)
fin = S['prog'][0][2]
for i, m in enumerate(fin + [fin[-1] + 12]):
    v = marimba(m + 12, .6, 2.4) if S['lead'] == 'ks' else bell(m + 12, .45, 2.6)
    place(music, v, 57.6 + i * .04, pan=(i - 2) * .15); place(send, v * .5, 57.6 + i * .04)
place(music, kick(1.), 57.6)

# ---------- bruitages ----------
def swish(d, g=1.):
    t = tt(d); return (bp(noise(d), 2200, 7500) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * .9) * g
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
        place(sfx, ting(f) * .11 * g, t0 + j * .045 + rng.uniform(0, .02), pan=rng.uniform(-.7, .7)); place(send, ting(f) * .09 * g, t0 + j * .045)
def pop(g=1.):
    t = tt(.09); f0 = 1100 * rng.uniform(.9, 1.12); ph = 2 * np.pi * np.cumsum(380 + (f0 - 380) * np.exp(-t * 55)) / SR
    return np.sin(ph) * env(t, .001, 38) * g
def thud(g=1.):
    t = tt(.35); ph = 2 * np.pi * np.cumsum(55 + 70 * np.exp(-t * 20)) / SR
    return (np.sin(ph) * np.exp(-t * 11) + lp(noise(.35), 300) * np.exp(-t * 30) * .6) * g
def click(g=1.):
    t = tt(.05); return (np.sin(2 * np.pi * 1600 * t) * np.exp(-t * 120) + hp(noise(.05), 3000) * np.exp(-t * 200) * .5) * g
def knife(t0, g=1.):
    d = .5; t = tt(d)
    shing = (np.sin(2 * np.pi * (5200 - 1600 * t / d) * t) * .5 + np.sin(2 * np.pi * 7300 * t) * .25) * env(t, .01, 7)
    scrape = bp(noise(d), 3500, 9000) * np.sin(np.pi * np.clip(t / .22, 0, 1)) * .6
    place(sfx, (shing + scrape) * g, t0, pan=.2); place(sfx, whoosh(.35, 800, 5000, .25 * g), t0 - .05, pan=-.2); place(send, shing * .3 * g, t0)
def ding(t0, g=1.):
    s = bell(88, .5, 1.8) + bell(95, .25, 1.8)
    place(sfx, s * .35 * g, t0); place(send, s * .2 * g, t0)
def brush(d=.6, g=1.):
    t = tt(d); return bp(noise(d), 1500, 5500) * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2 * .7 * g
cues = json.load(open(os.path.join(HERE, 'cues.json')))['cues']
side = 1
for t0, kind, arg in cues:
    if kind == 'swish': place(sfx, swish(.9, .18), t0)
    elif kind == 'burst':
        place(sfx, thud(.5), t0); place(sfx, whoosh(.6, 500, 4000, .3), t0 - .05)
        for j in range(12): place(sfx, pop(.08), t0 + .05 + j * .06, pan=rng.uniform(-.6, .6))
    elif kind == 'sparkle': sparkle(t0)
    elif kind == 'slash': knife(t0)
    elif kind == 'thud': place(sfx, thud(.42), t0)
    elif kind == 'pop': place(sfx, pop(.2), t0, pan=rng.uniform(-.25, .25))
    elif kind == 'click': place(sfx, click(.22), t0)
    elif kind == 'whoosh': place(sfx, whoosh(.55, 300, 3200, .28), t0 - .05)
    elif kind == 'tick':
        k = 0
        while k * .15 < (arg or 1): place(sfx, click(.07 + .03 * (k % 2)), t0 + k * .15, pan=.15); k += 1
    elif kind == 'ding': ding(t0)
    elif kind == 'brush': side = -side; place(sfx, brush(arg or .6, .22), t0, pan=.3 * side)
    elif kind == 'impact':
        place(sfx, kick(1.1), t0); t = tt(2.2); cr = hp(noise(2.2), 3500) * np.exp(-t * 2.4) * .2; place(sfx, cr, t0); place(send, cr * .6, t0)
t = tt(1.8)
ir = np.stack([lp(rng.normal(0, 1, len(t)), 6000) * np.exp(-t * 3.4) for _ in range(2)]); ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
wet = np.stack([fftconvolve(send[c], ir[c])[:N] for c in range(2)])
mix = music * .5 + wet * .5 + sfx * .95
fade = np.ones(N); fade[:int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR)); fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
mix = np.tanh(mix * fade * 1.7) / np.tanh(1.7); mix *= .89 / np.abs(mix).max()
def write(mix, name):
    pcm = (mix.T * 32767).astype('<i2')
    with wave.open(os.path.join(HERE, name), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return 20 * np.log10(np.sqrt((mix ** 2).mean()))


if '--voix' in sys.argv:
    # La voix off (voix.py) : phrases posées aux instants de voix/<langue>/voix.json, la musique baisse dessous (−11 dB, lissé).
    lang = sys.argv[sys.argv.index('--voix') + 1]
    d = os.path.join(HERE, 'voix', lang)
    plan = json.load(open(os.path.join(d, 'voix.json'), encoding='utf-8'))
    voice = np.zeros(N)
    for line in plan['lignes']:
        with wave.open(os.path.join(d, line['fichier'])) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768
            if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(axis=1)
            assert w.getframerate() == SR, line['fichier']
        x = hp(x, 80) / (np.abs(x).max() + 1e-9) * .9
        i = int(line['t'] * SR); n = min(len(x), N - i); voice[i:i + n] += x[:n]
    active = np.convolve(np.abs(voice) > .02, np.ones(int(.25 * SR)), 'same') > 0
    duck = lp(np.where(active, 10 ** (-11 / 20), 1.), 3, 1)
    bed = np.tanh((music * .5 + wet * .5 + sfx * .95) * fade * 1.7) / np.tanh(1.7); bed *= .89 / np.abs(bed).max()
    out = bed * duck + np.stack([voice, voice]) * .62
    out *= min(1, .95 / np.abs(out).max())
    print(f'audio-voix-{lang}.wav rms {write(out, f"audio-voix-{lang}.wav"):.1f} dBFS, {len(plan["lignes"])} phrases')
else:
    print(f'audio.wav {STYLE} rms {write(mix, "audio.wav"):.1f} dBFS cues {len(cues)}')
