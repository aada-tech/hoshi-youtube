"""Chaîne commune des visites commentées : voix → plan de visite → capture du site → musique → mixage → MP4 et sous-titres.

Utilisé par youtube/<projet>/make.py (Tafat, Atelier Nacre).
"""
import functools, json, os, subprocess, sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import narrate  # noqa: E402
import music  # noqa: E402
import gemini_voice  # noqa: E402


def texts(script, lang):
    """Chaque phrase est soit un texte, soit (texte affiché, texte prononcé)."""
    shown = [x if isinstance(x, str) else x[0] for x in script[lang]]
    spoken = [x if isinstance(x, str) else x[1] for x in script[lang]]
    return shown, spoken


def use_voice(voice):
    """voice = (voix Gemini, consigne de jeu[, modèle]) ; sans clé GEMINI_API_KEY, la voix Google Traduction reste en place."""
    if voice and os.environ.get('GEMINI_API_KEY'):
        narrate.tts = functools.partial(gemini_voice.tts, voice=voice[0], style=voice[1], model=voice[2] if len(voice) > 2 else gemini_voice.MODEL)
        return voice[0]
    return 'Google Traduction'


def run(project, here, lang, url, script, plan_fn, style, holds, test=False, subtitle_langs=(), voice=None):
    here = Path(here)
    print('voix :', use_voice(voice), flush=True)
    out, work = here / 'out', here / 'work'
    out.mkdir(exist_ok=True); work.mkdir(exist_ok=True)
    shown, spoken = texts(script, lang)
    seg = narrate.timeline(spoken, lang, str(work), lead=.9, holds=holds)
    for s, t in zip(seg, shown):
        s['text'] = t
    plan = plan_fn(seg, lang)
    if test:
        plan['duration'] = min(plan['duration'], seg[2]['end'] + .5)
    plan_path = work / f'plan-{lang}.json'
    json.dump(plan, open(plan_path, 'w', encoding='utf-8'), ensure_ascii=False)
    narrate.save_timeline(seg, work / f'timeline-{lang}.json')
    stem = f'{project}-visite-{lang}' + ('-test' if test else '')
    video = work / f'{stem}-image.mp4'
    subprocess.run([sys.executable, str(TOOLS / 'tour.py'), url, str(plan_path), str(video)], check=True)
    bed = work / f'musique-{style}-{int(plan["duration"])}.wav'
    if not bed.exists():
        music.write_wav(str(bed), music.bed(style, plan['duration']))
    keep = [s for s in seg if s['start'] < plan['duration']]
    mixed = work / f'{stem}-son.wav'
    narrate.mix(keep, str(bed), plan['duration'], str(mixed))
    final = out / f'{stem}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(video), '-i', str(mixed), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                    '-map_metadata', '-1', str(final)], check=True)
    narrate.srt(keep, str(out / f'{stem}.srt'))
    # sous-titres dans d'autres langues, calés sur la voix de cette vidéo (utile pour la vidéo principale en français)
    for other in subtitle_langs:
        o_shown, _ = texts(script, other)
        narrate.srt([dict(s, text=o_shown[s['i']]) for s in keep], str(out / f'{stem}.{other}.srt'))
    json.dump([{k: v for k, v in s.items() if k != 'wav'} for s in seg], open(out / f'{stem}.timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('vidéo', final, round(plan['duration'], 1), 's')
    return final
