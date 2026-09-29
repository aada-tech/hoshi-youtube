"""Voix off Gemini TTS (API Gemini, clé lue dans la variable d'environnement GEMINI_API_KEY, jamais écrite nulle part).

Même signature que narrate.tts, plus la voix et la consigne de jeu :
    narrate.tts = functools.partial(gemini_voice.tts, voice='Charon', style='[warm] [confident]')
Les réponses sont mises en cache (PCM) : un texte déjà dit n'est pas redemandé.
Offre gratuite : 100 requêtes par jour et par modèle ; une vidéo garde le même modèle du début à la fin.
"""
import base64, hashlib, json, os, subprocess, time, urllib.error, urllib.request

MODEL = 'gemini-3.8-flash-tts'
SR = 48000
_last = [0.0]


def _call(text, voice, model=MODEL):
    key = os.environ['GEMINI_API_KEY']
    body = {'contents': [{'parts': [{'text': text}]}],
            'generationConfig': {'responseModalities': ['AUDIO'],
                                 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voice}}}}}
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
    for attempt in range(8):
        wait = 6.5 - (time.time() - _last[0])  # offre gratuite : 10 requêtes par minute
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        # la clé passe dans un en-tête, jamais dans l'adresse (qui peut finir dans des journaux)
        req = urllib.request.Request(url, json.dumps(body).encode(), {'Content-Type': 'application/json', 'x-goog-api-key': key})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
            return base64.b64decode(r['candidates'][0]['content']['parts'][0]['inlineData']['data'])
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, IndexError, TimeoutError) as e:
            if attempt == 7:
                raise RuntimeError(f'Gemini TTS : échec ({getattr(e, "code", type(e).__name__)})') from None
            time.sleep(20 * (attempt + 1) if getattr(e, 'code', 0) == 429 else 4)


def _pcm(data):
    """La réponse est du PCM 16 bits 24 kHz, parfois enveloppé dans un WAV : ne garder que l'audio."""
    if data[:4] != b'RIFF':
        return data
    i = 12
    while i + 8 <= len(data):
        cid, n = data[i:i + 4], int.from_bytes(data[i + 4:i + 8], 'little')
        if cid == b'data':
            return data[i + 8:i + 8 + n]
        i += 8 + n + (n & 1)
    raise ValueError('WAV sans audio')


def tts(text, lang, out_wav, cache, speed=1.0, voice='Charon', style='', model=MODEL):
    """Texte → WAV 48 kHz mono, silences de début et de fin retirés (la consigne entre crochets n'est pas lue)."""
    os.makedirs(cache, exist_ok=True)
    key = hashlib.sha1(json.dumps([model, voice, style, text], ensure_ascii=False).encode()).hexdigest()[:16]
    raw = os.path.join(cache, f'gemini-{lang}-{key}.pcm')
    if not os.path.exists(raw):
        pcm = _pcm(_call(f'{style} {text}'.strip(), voice, model))
        assert len(pcm) > 24000, f'réponse vide pour « {text[:40]} »'
        open(raw, 'wb').write(pcm)
    trim = 'silenceremove=start_periods=1:start_threshold=-50dB'
    tempo = f',atempo={speed}' if speed != 1 else ''
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', raw,
                    '-af', f'{trim},areverse,{trim},areverse{tempo},aresample={SR}', '-ac', '1', out_wav], check=True)
    return out_wav
