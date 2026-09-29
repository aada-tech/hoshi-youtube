"""Vérifie avant un rendu que chaque élément visé par le plan de visite existe sur le site en ligne (et a une taille).

python3 preflight.py ../tafat fr     (dossier du projet, langue)
"""
import importlib.util, inspect, json, sys, time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import tour  # noqa: E402
import narrate, visit  # noqa: E402

project, lang = Path(sys.argv[1]).resolve(), sys.argv[2]
sys.argv = ['make.py', lang]
spec = importlib.util.spec_from_file_location('make', project / 'make.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

shown, spoken = visit.texts(mod.SCRIPT, lang)
seg = narrate.timeline(spoken, lang, str(project / 'work'), lead=.9)
plan = mod.plan(seg, lang) if len(inspect.signature(mod.plan).parameters) > 1 else mod.plan(seg)
sels = []
for st in plan['steps']:
    s = st.get('sel') or (st.get('to') or {}).get('sel')
    if s and s not in sels:
        sels.append(s)

c = tour.CDP()
tid = [t for t in c.call('Target.getTargets', session=False)['targetInfos'] if t['type'] == 'page'][0]['targetId']
c.session = c.call('Target.attachToTarget', {'targetId': tid, 'flatten': True}, session=False)['sessionId']
c.call('Runtime.enable')
c.call('Emulation.setDeviceMetricsOverride', {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1, 'mobile': False})
c.call('Page.navigate', {'url': mod.URL})
for _ in range(300):
    if c.eval("document.readyState === 'complete'"):
        break
    time.sleep(.1)
time.sleep(1)
bad = 0
for s in sels:
    r = c.eval(f"(() => {{ const e = document.querySelector({json.dumps(s)}); if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.width), Math.round(b.height)]; }})()")
    ok = r is not None and r[0] > 0 and r[1] > 0
    bad += not ok
    print('ok ' if ok else 'MANQUE', s, r if r else '')
c.close()
print(f"{project.name} {lang} : {len(sels) - bad}/{len(sels)} éléments trouvés")
sys.exit(1 if bad else 0)
