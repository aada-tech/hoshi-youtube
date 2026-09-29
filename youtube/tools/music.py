"""Nappe musicale synthétisée pour les vidéos commentées (sans bruitages), à la durée voulue.

Reprend les timbres des vidéos promo (sources/*/promo/audio.py) dans un arrangement plus doux, fait pour passer sous une voix.
python3 music.py billot|tafat|nacre DUREE sortie.wav
"""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
rng = np.random.default_rng(7)


def tt(d): return np.arange(int(d * SR)) / SR
def hz(m): return 440. * 2 ** ((m - 69) / 12)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def noise(d): return rng.normal(0, 1, int(d * SR))


def ks(m, d=1.2, bright=.5, vel=1.):
    """corde pincée (Karplus-Strong)"""
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
            for k in range(1, 7):
                s += np.sin(2 * np.pi * hz(m) * (1 + det) * k * t + k * det * 400) / k
    e = np.minimum(1, t / .5) * np.where(t < d, 1, np.exp(-(t - d) * 5))
    return lp(s * e, cut) * vel / (len(ms) * 6)


def bass(m, d=.55, vel=1.):
    t = tt(d); f = hz(m)
    e = np.minimum(1, t / .004) * np.exp(-t * 3.2)
    return lp((np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * e, 500) * vel


def kick(vel=1.):
    t = tt(.4); ph = 2 * np.pi * np.cumsum(45 + 115 * np.exp(-t * 26)) / SR
    return np.sin(ph) * np.exp(-t * 8.5) * vel


def shaker(vel=1.):
    t = tt(.09); return bp(noise(.09), 4000, 11000) * np.sin(np.pi * np.clip(t / .09, 0, 1)) ** 2 * vel * .5


STYLES = {
    'billot': dict(bpm=100, lead='ks', prog=[([57, 64, 69, 72, 76, 72, 69, 64], [45, 52, 57, 60], 45), ([53, 60, 65, 69, 72, 69, 65, 60], [41, 48, 53, 57], 41),
                                            ([55, 60, 64, 67, 72, 67, 64, 60], [48, 55, 60, 64], 48), ([55, 59, 62, 67, 71, 67, 62, 59], [43, 50, 55, 59], 43)]),
    'tafat': dict(bpm=104, lead='marimba', prog=[([62, 65, 69, 74, 77, 74, 69, 65], [50, 57, 62, 65], 50), ([58, 62, 65, 70, 74, 70, 65, 62], [46, 53, 58, 62], 46),
                                                ([60, 65, 69, 72, 77, 72, 69, 65], [53, 60, 65, 69], 53), ([60, 64, 67, 72, 76, 72, 67, 64], [48, 55, 60, 64], 48)]),
    'nacre': dict(bpm=96, lead='bell', prog=[([65, 69, 72, 76, 77, 76, 72, 69], [41, 52, 57, 60, 64], 41), ([64, 67, 71, 74, 76, 74, 71, 67], [40, 50, 55, 59, 62], 40),
                                            ([62, 65, 69, 72, 74, 72, 69, 65], [38, 48, 53, 57, 60], 38), ([60, 64, 67, 71, 72, 71, 67, 64], [36, 47, 52, 55, 59], 36)]),
}


def bed(style, dur):
    """Stéréo (2, N) normalisée à −1 dBFS crête : nappe + arpège + basse et pulsation discrètes, fin sur l'accord de départ."""
    S = STYLES[style]
    beat = 60 / S['bpm']; bar = beat * 4
    N = int(SR * (dur + 3))
    music, send = np.zeros((2, N)), np.zeros((2, N))

    def place(bus, sig, t, pan=0., gain=1.):
        i = int(t * SR)
        if i >= N:
            return
        s = sig[:N - i] * gain
        bus[0, i:i + len(s)] += s * np.sqrt((1 - pan) / 2) * 1.414
        bus[1, i:i + len(s)] += s * np.sqrt((1 + pan) / 2) * 1.414

    bars = int(np.ceil((dur - 2.5) / bar))
    for b in range(bars):
        t0 = b * bar; arp, chord, root = S['prog'][b % 4]
        intro = b == 0
        for i, m in enumerate(arp):
            v = (1. if i % 4 == 0 else .7) * (.45 if intro else .6)
            if S['lead'] == 'ks':
                place(music, ks(m, 1.1, .4, v * .8), t0 + i * beat / 2, pan=(-.35 if i % 2 else .3))
            elif S['lead'] == 'marimba':
                place(music, marimba(m, v * .55, .8), t0 + i * beat / 2, pan=(-.35 if i % 2 else .3))
            else:
                place(music, bell(m + 12, v * .3, 1.6), t0 + i * beat / 2, pan=(-.4 if i % 2 else .4))
            place(send, (ks(m, 1.1, .4, v * .2) if S['lead'] == 'ks' else bell(m + 12, v * .2, 1.4)), t0 + i * beat / 2)
        place(music, pad(chord, bar, .5 if not intro else .4), t0)
        place(send, pad(chord, bar, .22), t0)
        if not intro:
            place(music, bass(root, .5, .7), t0)
            place(music, bass(root, .45, .5), t0 + 2 * beat)
            place(music, kick(.45), t0)
            place(music, kick(.32), t0 + 2 * beat)
            for k in range(8):
                place(music, shaker(.18 if k % 2 else .1), t0 + k * beat / 2 + .01, pan=.4)
    end = bars * bar
    fin = S['prog'][0][1]
    for i, m in enumerate(fin + [fin[-1] + 12]):
        v = marimba(m + 12, .5, 2.4) if S['lead'] != 'bell' else bell(m + 12, .38, 2.6)
        place(music, v, end + i * .04, pan=(i - 2) * .15); place(send, v * .5, end + i * .04)
    place(music, pad(fin, 2.2, .45), end)
    t = tt(1.8)
    ir = np.stack([lp(rng.normal(0, 1, len(t)), 6000) * np.exp(-t * 3.4) for _ in range(2)])
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    wet = np.stack([fftconvolve(send[c], ir[c])[:N] for c in range(2)])
    mix = (music * .55 + wet * .45)[:, :int(SR * dur)]
    fo = int(1.5 * SR)
    mix[:, -fo:] *= np.linspace(1, 0, fo) ** 1.5
    mix[:, :int(.05 * SR)] *= np.linspace(0, 1, int(.05 * SR))
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    return mix * (.89 / np.abs(mix).max())


def write_wav(path, stereo):
    pcm = (np.clip(stereo, -1, 1).T * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


if __name__ == '__main__':
    write_wav(sys.argv[3], bed(sys.argv[1], float(sys.argv[2])))
    print(sys.argv[3])
