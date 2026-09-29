"""Traduction des fragments HTML : repère les blocs de texte et les attributs lisibles, puis applique un fichier de traductions.

Format du fichier de traductions (entrées séparées par une ligne vide) :
    fr: <texte source tel qu'il apparaît dans le HTML, espaces normalisés>
    en: <traduction anglaise, HTML brut>
    es: <traduction espagnole, HTML brut>
    ar: <traduction arabe, HTML brut> (facultatif : seulement pour les sites en arabe)
"""
import re, sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
SKIP = {'script', 'style', 'svg', 'pre', 'textarea', 'template'}
ATTRS = ('alt', 'aria-label', 'placeholder', 'title', 'data-text', 'content', 'data-label', 'aria-valuetext')
LETTER = re.compile(r'[A-Za-zÀ-ÿ]')
norm = lambda s: re.sub(r'\s+', ' ', s).strip()


class Node:
    def __init__(self, tag, attrs, start, raw):
        self.tag, self.attrs, self.start, self.raw = tag, attrs, start, raw
        self.inner_start = start + len(raw)
        self.inner_end = None
        self.children, self.texts = [], []


class Tree(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=True)
        self.src = src
        self.lines = [0]
        for m in re.finditer('\n', src):
            self.lines.append(m.end())
        self.root = Node('#root', [], 0, '')
        self.stack = [self.root]
        self.feed(src)
        self.close()

    def off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.off(), self.get_starttag_text())
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs, self.off(), self.get_starttag_text()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                o = self.off()
                for n in self.stack[i:]:
                    n.inner_end = o
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].texts.append(data)


def collect(src):
    """Renvoie la liste des modifications possibles : (début, fin, texte source, genre)."""
    t = Tree(src)
    out = []

    def attrs_of(n):
        for name, val in n.attrs:
            if name in ATTRS and val and LETTER.search(val):
                if n.tag == 'meta' and name == 'content' and not any(a == 'name' or a == 'property' for a, _ in n.attrs):
                    continue
                m = re.search(r'\s' + re.escape(name) + r'\s*=\s*("([^"]*)"|\'([^\']*)\')', n.raw)
                if not m:
                    continue
                g = 2 if m.group(2) is not None else 3
                s = n.start + m.start(g)
                out.append((s, n.start + m.end(g), src[s:n.start + m.end(g)], 'attr'))

    def walk_svg(n):
        # dans un SVG, seuls les éléments <text> portent du texte lisible
        for c in n.children:
            if c.tag == 'text' and (any(LETTER.search(x) for x in c.texts) or any(LETTER.search(''.join(g.texts)) for g in c.children)):
                inner = src[c.inner_start:c.inner_end]
                out.append((c.inner_start, c.inner_end, inner, 'text'))
            elif c.tag not in VOID:
                walk_svg(c)

    def walk(n):
        for c in n.children:
            if c.tag == 'svg':
                attrs_of(c)
                walk_svg(c)
                continue
            if c.tag in SKIP:
                attrs_of(c)
                continue
            attrs_of(c)
            if c.tag in VOID:
                continue
            if any(LETTER.search(x) for x in c.texts):
                inner = src[c.inner_start:c.inner_end]
                lead = len(inner) - len(inner.lstrip())
                trail = len(inner) - len(inner.rstrip())
                out.append((c.inner_start + lead, c.inner_end - trail, inner.strip(), 'text'))
            else:
                walk(c)
    walk(t.root)
    return sorted(out)


def load(path):
    entries = {}
    block = {}
    for line in open(path, encoding='utf-8').read().split('\n') + ['']:
        if not line.strip():
            if block:
                if 'fr' not in block:
                    raise SystemExit(f'entrée sans fr: {block}')
                entries[norm(block['fr'])] = block
                block = {}
            continue
        m = re.match(r'^(fr|en|es|ar):\s?(.*)$', line)
        if not m:
            raise SystemExit(f'ligne illisible dans {path}: {line[:80]}')
        block[m.group(1)] = m.group(2)
    return entries


def tags(s):
    return re.findall(r'</?([a-z0-9]+)', s)


def apply(src, table, lang, strict=True):
    edits = collect(src)
    missing = []
    for s, e, text, kind in reversed(edits):
        k = norm(text)
        tr = table.get(k, {}).get(lang)
        if tr is None:
            missing.append(k)
            continue
        extra = list(tags(tr))
        for t in tags(text):
            if t in extra:
                extra.remove(t)
        if kind == 'text' and extra:
            print(f'  ! balises en trop ({lang}) {extra} : {k[:70]}', file=sys.stderr)
        if kind == 'attr' and re.search(r'[<>"]', tr):
            raise SystemExit(f'caractère interdit dans un attribut ({lang}) : {tr[:70]}')
        src = src[:s] + tr + src[e:]
    if missing and strict:
        raise SystemExit(f'{len(missing)} traductions manquantes ({lang}) :\n' + '\n'.join('  ' + m for m in missing[:40]))
    return src


if __name__ == '__main__':
    # python3 units.py list page.html [i18n.txt]  → affiche les textes à traduire (ceux absents du fichier)
    cmd, path = sys.argv[1], sys.argv[2]
    src = open(path, encoding='utf-8').read()
    have = load(sys.argv[3]) if len(sys.argv) > 3 else {}
    seen = set()
    for s, e, text, kind in collect(src):
        k = norm(text)
        if k in seen or k in have:
            continue
        seen.add(k)
        print('fr: ' + k + '\n')
