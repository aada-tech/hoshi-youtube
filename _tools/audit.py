"""Audit de sécurité et de confidentialité des dépôts avant publication.

python3 audit.py DIR [DIR…]
Signale : fichiers inattendus ou cachés, fichiers lourds, informations personnelles, secrets, e-mails, téléphones,
liens externes, scripts en ligne, liens target=_blank sans noopener, restes du mode capture, métadonnées des médias.
"""
import json, os, re, subprocess, sys

ALLOWED = ('.html', '.css', '.js', '.webp', '.jpg', '.png', '.svg', '.woff2', '.mp4', '.md', '.txt', '.xml')
ALLOWED_NAMES = {'LICENSE', '.gitignore', '.nojekyll'}
TEXT = ('.html', '.css', '.js', '.md', '.txt', '.xml', '.svg', '')
PERSONAL_FIXED = [r'/Users/', r'/home/', r'C:\\Users', r'gmail', r'icloud', r'hotmail', r'outlook\.', r'claude\.ai', r'anthropic', r'file://',
                  r'127\.0\.0\.1', r'scratchpad', r'hoshuko-github', r'vitrines-sources', r'nail-artiste', r'nettoyage-tigzirt', r'portfolio-vitrines']


def personal_patterns():
    """Motifs propres à cette machine, détectés à l'exécution : nom d'utilisateur, e-mail git global, autres comptes gh."""
    import getpass
    found = set()
    try:
        found.add(getpass.getuser())
    except Exception:
        pass
    try:
        mail = subprocess.run(['git', 'config', '--global', 'user.email'], capture_output=True, text=True).stdout.strip()
        if mail:
            found.update([mail, mail.split('@')[0]])
    except Exception:
        pass
    try:
        st = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        found.update(re.findall(r'account (\S+)', st.stdout + st.stderr))
    except Exception:
        pass
    found.discard('hoshuko')  # le compte de publication lui-même est public
    return PERSONAL_FIXED + [re.escape(x) for x in sorted(found) if len(x) >= 3]


SECRETS = [r'ghp_[A-Za-z0-9]{20,}', r'gho_[A-Za-z0-9]{20,}', r'github_pat_', r'\bsk-[A-Za-z0-9]{16,}', r'AKIA[0-9A-Z]{16}', r'AIza[0-9A-Za-z_-]{30,}',
           r'xox[baprs]-', r'-----BEGIN', r'(?i)api[_-]?key', r'(?i)secret', r'(?i)\btoken\b', r'(?i)password', r'(?i)bearer\s']
EMAIL = r'[\w.+-]+@[\w-]+\.[\w.-]+'
PHONE = r'(?<![\w-])(?:\+\d{2,3}[\s.]?)?0?\d(?:[\s.]?\d{2}){4}(?!\d)|\b0\d{3}(?:\s\d{2}){3}\b'
URL = r'https?://[^\s"\'<>)`\]]+'
META_BAD = ('GPS', 'Artist', 'Author', 'Creator', 'Copyright', 'OwnerName', 'SerialNumber', 'Make', 'Model', 'UserComment', 'XPAuthor', 'CameraOwnerName', 'LensModel', 'By-line', 'Credit', 'Rights')


def main():
    global PERSONAL
    PERSONAL = personal_patterns()
    total_issues = 0
    all_urls = {}
    for root in sys.argv[1:]:
        root = os.path.abspath(root)
        issues, media = [], []
        size = 0
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d != '.git']
            for fn in fns:
                p = os.path.join(dp, fn)
                rel = os.path.relpath(p, root)
                ext = os.path.splitext(fn)[1].lower()
                st = os.path.getsize(p)
                size += st
                if fn.startswith('.') and fn not in ALLOWED_NAMES:
                    issues.append(f'fichier caché : {rel}')
                if ext not in ALLOWED and fn not in ALLOWED_NAMES:
                    issues.append(f'extension inattendue : {rel}')
                if st > 10e6:
                    issues.append(f'fichier lourd ({st / 1e6:.1f} Mo) : {rel}')
                if os.path.islink(p):
                    issues.append(f'lien symbolique : {rel}')
                if ext in ('.webp', '.jpg', '.png', '.mp4', '.svg'):
                    media.append(p)
                if ext in TEXT and fn != 'OFL.txt' and not fn.endswith('.woff2'):
                    try:
                        s = open(p, encoding='utf-8').read()
                    except UnicodeDecodeError:
                        issues.append(f'texte illisible : {rel}')
                        continue
                    low_ok = fn == 'LICENSE'
                    for pat in PERSONAL:
                        for m in re.finditer(pat, s, flags=re.I):
                            ctx = s[max(0, m.start() - 30):m.end() + 30].replace('\n', ' ')
                            issues.append(f'info personnelle ? {rel} : «{pat}» … {ctx} …')
                    for pat in SECRETS:
                        if low_ok:
                            break
                        for m in re.finditer(pat, s):
                            ctx = s[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')
                            issues.append(f'secret ? {rel} : «{m.group(0)}» … {ctx} …')
                    for m in re.finditer(EMAIL, s):
                        if m.group(0).endswith(('.webp', '.jpg', '.png', '.woff2', '.svg')) or '@2x' in m.group(0):
                            continue
                        issues.append(f'adresse e-mail : {rel} : {m.group(0)}')
                    if ext in ('.html', '.js', '.md'):
                        for m in re.finditer(PHONE, s):
                            num = m.group(0).strip()
                            if re.fullmatch(r'[\d\s.+]+', num) and len(re.sub(r'\D', '', num)) >= 10:
                                all_urls.setdefault('☎ ' + num, set()).add(os.path.basename(root))
                    for m in re.finditer(URL, s):
                        u = m.group(0).rstrip('.,;:')
                        all_urls.setdefault(u, set()).add(os.path.basename(root))
                    if ext == '.html':
                        for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>', s):
                            issues.append(f'script en ligne : {rel}')
                        if re.search(r'\son[a-z]+\s*=\s*["\']', s):
                            issues.append(f'gestionnaire d’événement en ligne : {rel}')
                        for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', s):
                            if 'noopener' not in m.group(0):
                                issues.append(f'target=_blank sans noopener : {rel}')
                        if re.search(r'<iframe', s):
                            issues.append(f'iframe : {rel}')
                        if 'Content-Security-Policy' not in s:
                            issues.append(f'pas de CSP : {rel}')
                    if ext == '.js':
                        for pat in (r'DBG', r'dbg-', r'postMessage', r'eval\(', r'new Function', r'document\.write', r'innerHTML\s*=\s*[^;]*location'):
                            if re.search(pat, s):
                                issues.append(f'motif sensible dans le JS : {rel} : {pat}')
                        if re.search(r"target\s*=\s*'_blank'", s) and 'noopener' not in s:
                            issues.append(f'target=_blank sans noopener (JS) : {rel}')
                    if ext == '.svg' and re.search(r'<script|href="http|xlink:href="http', s):
                        issues.append(f'SVG actif ou externe : {rel}')
        # métadonnées des médias
        for i in range(0, len(media), 200):
            out = subprocess.run(['exiftool', '-json', '-G1', '-a', *media[i:i + 200]], capture_output=True, text=True).stdout
            for item in json.loads(out or '[]'):
                bad = {k: v for k, v in item.items() if any(b.lower() in k.lower() for b in META_BAD) and not k.startswith('File')}
                if bad:
                    issues.append(f'métadonnées : {os.path.relpath(item["SourceFile"], root)} : {bad}')
        print(f'\n=== {os.path.basename(root)} · {size / 1e6:.1f} Mo · ' + (f'{len(issues)} point(s) à examiner' if issues else 'aucun problème'))
        for x in issues:
            print('  - ' + x)
        total_issues += len(issues)
    print('\n=== liens externes et numéros (à relire)')
    for u in sorted(all_urls):
        print(f'  {u}   [{", ".join(sorted(all_urls[u]))}]')
    sys.exit(1 if total_issues else 0)


if __name__ == '__main__':
    main()
