"""Outils communs aux sites : pages FR / EN / ES (et AR en option), sélecteur de langue, en-tête sécurisé, polices locales, chemins d'assets."""
import html, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import units  # noqa: E402

TOOLS = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(TOOLS), '_fonts')
LANGS = ('fr', 'en', 'es')          # langues par défaut ; un site peut passer langs=('fr', 'en', 'es', 'ar')
HREF = {'fr': './', 'en': 'en.html', 'es': 'es.html', 'ar': 'ar.html'}
OUT = {'fr': 'index.html', 'en': 'en.html', 'es': 'es.html', 'ar': 'ar.html'}
LANG_LABEL = {'fr': 'Langue', 'en': 'Language', 'es': 'Idioma', 'ar': 'اللغة'}
OG_LOCALE = {'fr': 'fr_FR', 'en': 'en_GB', 'es': 'es_ES', 'ar': 'ar_MA'}
RTL = ('ar',)

# Aucun script en ligne, aucune requête réseau, aucun cadre, aucun formulaire envoyé ailleurs.
# Les styles en ligne restent permis : le code pose des variables CSS dans des attributs style.
CSP = ("default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "font-src 'self'; media-src 'self'; connect-src 'none'; manifest-src 'self'; object-src 'none'; "
       "frame-src 'none'; worker-src 'none'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests")


def strip_dbg(js):
    """Retire les blocs /*DBG*/ … /*/DBG*/ (mode capture, réservé aux aperçus locaux)."""
    out = re.sub(r'[ \t]*/\*DBG\*/.*?/\*/DBG\*/\n?', '', js, flags=re.S)
    assert 'DBG' not in out
    return out


def switcher(lang, cls='lang-switch', tag='nav', langs=LANGS):
    links = ''.join(
        f'<a href="{HREF[l]}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else '') + f'>{l.upper()}</a>'
        for l in langs)
    role = ' role="group"' if tag != 'nav' else ''
    return f'<{tag} class="{cls}"{role} aria-label="{LANG_LABEL[lang]}">{links}</{tag}>'


def translate(src, table, lang):
    return src if lang == 'fr' else units.apply(src, table, lang)


def asset_paths(text):
    """img/… → assets/img/… dans le HTML et le JS (le CSS est traité à part)."""
    return re.sub(r'(?<=[\'"`(=])img/', 'assets/img/', text)


def fonts_css(name, prefix='../fonts/'):
    css = open(os.path.join(FONTS, name, 'fonts.css'), encoding='utf-8').read()
    return css.replace('../fonts/', prefix)


def font_files(name):
    d = os.path.join(FONTS, name)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith('.woff2'))


def esc(s):
    return html.escape(s, quote=True)


def page(lang, *, title, desc, base, body, scripts, brand, theme='#ffffff', preload_fonts=(), preload_img=(), head_extra='', langs=LANGS):
    url = base + ('' if lang == 'fr' else OUT[lang])
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{base}{"" if l == "fr" else OUT[l]}">\n' for l in langs)
    pre = ''.join(f'<link rel="preload" href="{f}" as="font" type="font/woff2" crossorigin>\n' for f in preload_fonts)
    pre += ''.join(f'<link rel="preload" href="{f}" as="image">\n' for f in preload_img)
    # une entrée (chemin, 'module') charge un module ES (type="module")
    js = ''.join(f'<script type="module" src="{s[0]}"></script>\n' if isinstance(s, tuple) else f'<script src="{s}"></script>\n' for s in scripts)
    return f"""<!doctype html>
<html lang="{lang}"{' dir="rtl"' if lang in RTL else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="same-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="{theme}">
<link rel="canonical" href="{url}">
{alt}<link rel="alternate" hreflang="x-default" href="{base}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(brand)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}assets/img/og-{lang}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
{pre}<link rel="stylesheet" href="assets/css/style.css">
{head_extra}</head>
<body>
{body}
{js}</body>
</html>
"""


def reset(out):
    """Vide le dossier de sortie (uniquement s'il s'agit bien d'un export généré) puis recrée l'arborescence."""
    if os.path.exists(out):
        assert os.path.isfile(os.path.join(out, 'index.html')) or not os.listdir(out), f'dossier inattendu : {out}'
        for n in os.listdir(out):
            if n in ('.git', 'README.md', 'README.fr.md', 'README.es.md', 'README.ar.md', 'LICENSE', 'CREDITS.md', 'SECURITY.md', '.github', 'media', '.nojekyll', '.gitignore'):
                continue  # documentation et historique du dépôt : gérés à part
            p = os.path.join(out, n)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for d in ('assets/css', 'assets/js', 'assets/img', 'assets/fonts'):
        os.makedirs(os.path.join(out, d), exist_ok=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def check_refs(out):
    """Chaque fichier d'image ou de police exporté doit être cité quelque part, et chaque référence locale doit exister."""
    texts = ''
    for root, _, files in os.walk(out):
        for f in files:
            if f.endswith(('.html', '.css', '.js')):
                texts += open(os.path.join(root, f), encoding='utf-8').read()
    unused = []
    for sub, exts in (('assets/img', ('.webp', '.png', '.jpg', '.svg')), ('assets/fonts', ('.woff2',))):
        for f in os.listdir(os.path.join(out, sub)):
            if not f.endswith(exts):
                continue
            stem = f.rsplit('.', 1)[0]
            if f not in texts and f"'{stem}'" not in texts and f'"{stem}"' not in texts and not f.startswith('og-'):
                unused.append(f'{sub}/{f}')
    missing = []
    for m in re.finditer(r'(?:src|href)="((?:assets/)[^"$`{]+)"|url\((\.\./[^)]+)\)', texts):
        ref = m.group(1) or m.group(2).replace('../', 'assets/', 1)
        if not os.path.exists(os.path.join(out, ref)):
            missing.append(ref)
    return unused, sorted(set(missing))


def finish(out):
    """Retire les images et polices qui ne sont citées nulle part, puis vérifie qu'aucune référence locale ne manque."""
    unused, missing = check_refs(out)
    for f in unused:
        os.remove(os.path.join(out, f))
    print('export :', out, '| retirés (non cités) :', unused or 'aucun', '| manquants :', missing or 'aucun')
    assert not missing, missing


LEGAL = os.path.join(os.path.dirname(TOOLS), '_legal')
FONT_FAMILIES = {
    'billot': [('Bodoni Moda', 'bodonimoda'), ('IBM Plex Mono', 'ibmplexmono'), ('Instrument Sans', 'instrumentsans')],
    'tafat': [('Bricolage Grotesque', 'bricolagegrotesque'), ('Figtree', 'figtree'), ('Noto Sans Tifinagh', 'notosanstifinagh')],
    'nacre': [('Gloock', 'gloock'), ('Hanken Grotesk', 'hankengrotesk'), ('DM Mono', 'dmmono')],
    'warda': [('Instrument Serif', 'instrumentserif'), ('Geist', 'geist'), ('Amiri', 'amiri'), ('IBM Plex Sans Arabic', 'ibmplexsansarabic')],
    'portfolio': [('Syne', 'syne'), ('Onest', 'onest'), ('JetBrains Mono', 'jetbrainsmono'),
                  ('Bodoni Moda', 'bodonimoda'), ('Bricolage Grotesque', 'bricolagegrotesque'), ('Gloock', 'gloock'),
                  ('Instrument Serif', 'instrumentserif')],
}


def fonts_license(out, name):
    """assets/fonts/OFL.txt : mentions de copyright de chaque famille, puis le texte de la licence SIL OFL 1.1 (obligatoire avec les fichiers de police)."""
    notices, body = [], None
    for family, slug in FONT_FAMILIES[name]:
        txt = open(os.path.join(LEGAL, f'ofl-{slug}.txt'), encoding='utf-8').read()
        head, rest = txt.split('This Font Software is licensed under the SIL Open Font License, Version 1.1.', 1)
        notices.append(f'{family}\n' + head.strip())
        body = body or 'This Font Software is licensed under the SIL Open Font License, Version 1.1.' + rest
    text = ('The fonts in this folder are distributed under the SIL Open Font License, Version 1.1.\n'
            'They are unmodified web subsets (WOFF2) as served by Google Fonts.\n\n' + '\n\n'.join(notices) + '\n\n' + body.strip() + '\n')
    write(os.path.join(out, 'assets/fonts/OFL.txt'), text)
