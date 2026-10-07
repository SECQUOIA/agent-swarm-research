"""W7 verifier checks for group exact-comp.

1. The table environment with \\label{tab:chain} moved from computation.tex to
   appendix-computation.tex is word-for-word identical to the old one.
2. Every \\label in the group's files before W7 is still defined exactly once
   in the group's files after W7, and no new label appears twice.
3. Word-level diff of every changed file (old vs new), for reading.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import difflib
import re
from collections import Counter
from pathlib import Path

ROOT = Path((_PUBLIC_REPO + '/paper-decomposition-aware'))
OLD = ROOT / 'process/w7/sections-before-w7'
NEW = ROOT / 'sections'
FILES = ['exact', 'exact-localized', 'appendix-localized', 'appendix-boundary',
         'computation', 'appendix-computation']


def text(d, f):
    return (d / f'{f}.tex').read_text()


def table_with_label(src, label):
    for m in re.finditer(r'\\begin\{table\}.*?\\end\{table\}', src, re.S):
        if f'\\label{{{label}}}' in m.group(0):
            return m.group(0)
    return None


def words(s):
    return s.split()


ok = True
old_tab = table_with_label(text(OLD, 'computation'), 'tab:chain')
new_tab = table_with_label(text(NEW, 'appendix-computation'), 'tab:chain')
left = table_with_label(text(NEW, 'computation'), 'tab:chain')
if old_tab is None or new_tab is None:
    print('FAIL: tab:chain not found', old_tab is None, new_tab is None)
    ok = False
elif words(old_tab) != words(new_tab):
    print('FAIL: tab:chain differs')
    ok = False
else:
    print('OK: tab:chain moved word for word', len(words(new_tab)), 'words')
if left is not None:
    print('FAIL: tab:chain still in computation.tex')
    ok = False

lab = re.compile(r'\\label\{([^}]*)\}')
old_labels = Counter(l for f in FILES for l in lab.findall(text(OLD, f)))
new_labels = Counter(l for f in FILES for l in lab.findall(text(NEW, f)))
lost = sorted(set(old_labels) - set(new_labels))
dup = sorted(l for l, c in new_labels.items() if c > 1)
added = sorted(set(new_labels) - set(old_labels))
print('labels before', sum(old_labels.values()), 'after', sum(new_labels.values()))
print('lost', lost, 'duplicated', dup, 'added', added)
ok = ok and not lost and not dup

for f in FILES:
    a, b = words(text(OLD, f)), words(text(NEW, f))
    if a == b:
        continue
    print(f'\n=== {f}.tex: word-level changes')
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        old = ' '.join(a[i1:i2])
        new = ' '.join(b[j1:j2])
        if f in ('computation', 'appendix-computation') and 'tab:chain' in old + new \
                and len(old + new) > 400:
            print(f'  [{op}] table block ({len(a[i1:i2])} -> {len(b[j1:j2])} words)')
            continue
        print(f'  [{op}] -{old!r}\n         +{new!r}')

print('\nRESULT:', 'PASS' if ok else 'FAIL')
