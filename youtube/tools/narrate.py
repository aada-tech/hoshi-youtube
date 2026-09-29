"""Voix off (synthèse vocale de Google), minutage, sous-titres SRT et mixage voix + musique.

Utilisé par les scripts youtube/<projet>/make.py.
"""
import hashlib, json, os, re, subprocess, urllib.parse, urllib.request, wave
import numpy as np

SR = 48000
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36'}
# domaine Google par langue : l'accent suit le domaine (anglais américain, espagnol d'Espagne, arabe standard)
TLD = {'fr': 'fr', 'en': 'com', 'es': 'es', 'ar': 'com'}


def _chunks(text, limit=180):
    """Découpe aux ponctuations pour rester sous la limite du service (≈ 200 caractères par requête)."""
    parts, cur = [], ''
    for piece in re.split(r'(?<=[.!?;:,])\s+', text.strip()):
        if len(cur) + len(piece) + 1 <= limit:
            cur = (cur + ' ' + piece).strip()
        else:
            if cur:
                parts.append(cur)
            cur = piece
    if cur:
        parts.append(cur)
    return parts


def tts(text, lang, out_wav, cache, speed=1.04):
    """Texte → WAV 48 kHz mono, silences de début et de fin retirés."""
    os.makedirs(cache, exist_ok=True)
    mp3s = []
    for c in _chunks(text):
        key = hashlib.sha1(f'{lang}|{TLD[lang]}|{c}'.encode()).hexdigest()[:16]
        p = os.path.join(cache, f'{lang}-{key}.mp3')
        if not os.path.exists(p):
            url = f'https://translate.google.{TLD[lang]}/translate_tts?' + urllib.parse.urlencode({'ie': 'UTF-8', 'q': c, 'tl': lang, 'client': 'tw-ob'})
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
            assert len(data) > 1000, f'réponse vide pour « {c} »'
            open(p, 'wb').write(data)
        mp3s.append(p)
    lst = out_wav + '.txt'
    # chemins absolus : ffmpeg lit les chemins relatifs d'une liste par rapport au dossier de la liste
    open(lst, 'w').write(''.join(f"file '{os.path.abspath(m)}'\n" for m in mp3s))
    trim = 'silenceremove=start_periods=1:start_threshold=-48dB'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-af', f'{trim},areverse,{trim},areverse,atempo={speed},aresample={SR}', '-ac', '1', out_wav], check=True)
    os.remove(lst)
    return out_wav


def duration(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


def timeline(texts, lang, work, lead=.7, gap=.45, holds=None, speed=1.04):
    """Génère chaque phrase et renvoie [{'i', 'text', 'wav', 'start', 'end'}], avec des pauses optionnelles (holds[i] secondes après la phrase i)."""
    holds = holds or {}
    t, out = lead, []
    for i, text in enumerate(texts):
        wav = tts(text, lang, os.path.join(work, f'voice-{lang}-{i:02d}.wav'), os.path.join(work, 'cache'), speed)
        d = duration(wav)
        out.append({'i': i, 'text': text, 'wav': wav, 'start': round(t, 3), 'end': round(t + d, 3)})
        t += d + gap + holds.get(i, 0)
    return out


def _ts(s):
    ms = int(round(s * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def _balanced(words, n):
    """Répartit les mots en n groupes de longueurs voisines."""
    total = sum(len(w) + 1 for w in words)
    groups, cur, acc = [], [], 0
    for w in words:
        if cur and len(groups) < n - 1 and acc + (len(w) + 1) / 2 > total * (len(groups) + 1) / n:
            groups.append(cur); cur = []
        cur.append(w); acc += len(w) + 1
    groups.append(cur)
    return groups


def srt(segments, path, width=42):
    """Sous-titres : chaque phrase en blocs de deux lignes équilibrées (42 caractères au plus), durées au prorata du texte."""
    import math
    out, n = [], 1
    for s in segments:
        words = s['text'].split()
        blocks = _balanced(words, max(1, math.ceil(len(s['text']) / (2 * width - 4))))
        total = sum(len(' '.join(b)) for b in blocks)
        t = s['start']
        for b in blocks:
            lines = _balanced(b, 2) if len(' '.join(b)) > width else [b]
            share = (s['end'] - s['start']) * len(' '.join(b)) / total
            out.append(f'{n}\n{_ts(t)} --> {_ts(t + share)}\n' + '\n'.join(' '.join(l) for l in lines) + '\n')
            n += 1; t += share
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    return path


def _read(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
        return a.reshape(-1, w.getnchannels()).T


def mix(segments, music_wav, dur, out_wav):
    """Voix au centre, musique abaissée pendant qu'elle parle (attaque 120 ms, retour 600 ms)."""
    N = int(dur * SR)
    voice = np.zeros(N, np.float32)
    for s in segments:
        a = _read(s['wav'])[0]
        a = a / (np.abs(a).max() + 1e-9) * .82
        i = int(s['start'] * SR)
        voice[i:i + len(a)] += a[:max(0, N - i)]
    music = _read(music_wav)[:, :N]
    if music.shape[1] < N:
        music = np.pad(music, ((0, 0), (0, N - music.shape[1])))
    # enveloppe de la voix → gain de la musique
    env = np.convolve(np.abs(voice), np.ones(int(.05 * SR)) / int(.05 * SR), 'same')
    target = np.where(env > .01, .16, .5).astype(np.float32)
    gain = np.empty(N, np.float32); g = .5
    up, down = 1 - np.exp(-1 / (.6 * SR)), 1 - np.exp(-1 / (.12 * SR))
    for k in range(0, N, 480):  # par blocs de 10 ms
        tgt = target[k]
        g += (tgt - g) * (1 - (1 - (down if tgt < g else up)) ** 480)
        gain[k:k + 480] = g
    out = music * gain + voice
    out /= max(1.0, np.abs(out).max() / .95)
    pcm = (out.T * 32767).astype('<i2')
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return out_wav


def mouth(segments, dur, fps=30):
    """Ouverture de la bouche d'une mascotte (0 à 1) à chaque image, d'après l'énergie de la voix : syllabes marquées, silences fermés."""
    n = int(dur * fps) + 1
    env = np.zeros(n, np.float32)
    hop = SR // fps
    for s in segments:
        a = _read(s['wav'])[0]
        k0 = int(round(s['start'] * fps))
        for k in range(len(a) // hop):
            if 0 <= k0 + k < n:
                env[k0 + k] = max(env[k0 + k], float(np.sqrt(np.mean(a[k * hop:(k + 1) * hop] ** 2))))
    ref = np.percentile(env[env > 0], 90) if (env > 0).any() else 1
    env = np.clip(env / (ref + 1e-9), 0, 1) ** .8
    env[env < .12] = 0
    out, v = [], 0.0
    for x in env:  # ouverture immédiate, fermeture en ~2 images
        v = x if x > v else v * .45 + x * .55
        out.append(round(float(v), 3))
    return out


def save_timeline(segments, path):
    json.dump([{k: v for k, v in s.items() if k != 'wav'} for s in segments], open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
