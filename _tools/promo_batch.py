"""Rend puis assemble les vidéos promo d'un projet, dans plusieurs langues et formats, trois rendus à la fois.

python3 promo_batch.py DOSSIER_PROMO PREFIXE fr,en,es 45,916,169
Sorties : PREFIXE-promo-4x5-fr.mp4, PREFIXE-promo-9x16-en.mp4, … (images H.264 + audio-voix-<langue>.wav, ou à défaut audio.wav, en AAC 192k).
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

d, prefix, langs, fmts = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4].split(',')
NAME = {'45': '4x5', '916': '9x16', '169': '16x9'}


def job(lang, fmt):
    log = open(os.path.join(d, f'render_{fmt}_{lang}.log'), 'w')
    r = subprocess.run([sys.executable, 'render.py', fmt, '--lang', lang], cwd=d, stdout=log, stderr=subprocess.STDOUT)
    if r.returncode:
        return f'ÉCHEC {fmt} {lang} (voir render_{fmt}_{lang}.log)'
    frames = os.path.join(d, f'frames_{fmt}.mp4' if lang == 'fr' else f'frames_{fmt}_{lang}.mp4')
    out = os.path.join(d, f'{prefix}-promo-{NAME[fmt]}-{lang}.mp4')
    # bande-son avec voix off dans la langue de la vidéo si elle existe (audio.py --voix <langue>), sinon musique seule
    voice = os.path.join(d, f'audio-voix-{lang}.wav')
    audio = voice if os.path.exists(voice) else os.path.join(d, 'audio.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', frames, '-i', audio, '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    return f'ok {os.path.basename(out)} {os.path.getsize(out) / 1e6:.1f} Mo'


with ThreadPoolExecutor(3) as ex:
    for res in ex.map(lambda a: job(*a), [(l, f) for l in langs for f in fmts]):
        print(res, flush=True)
print('TERMINÉ')
