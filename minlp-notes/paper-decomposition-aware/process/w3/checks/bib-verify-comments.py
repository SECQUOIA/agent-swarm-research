"""Verifier check: compare the comment above each references.bib entry with the comment
above the same key in the W1 sources (process/w1/lit-core.bib, lit-ext.bib) and in the
pre-W3 file. Prints entries whose current comment differs from every source comment."""
import re

def comments(path):
    lines = open(path, encoding='utf8').read().split('\n')
    out = {}
    for i, l in enumerate(lines):
        m = re.match(r'@\w+\{([^,]+),', l)
        if not m:
            continue
        j, com = i - 1, []
        while j >= 0 and lines[j].startswith('%') and not lines[j].startswith('% ---'):
            com.insert(0, lines[j].lstrip('% ').strip()); j -= 1
        out[m.group(1)] = ' '.join(com)
    return out

cur = comments('references.bib')
core = comments('process/w1/lit-core.bib')
ext = comments('process/w1/lit-ext.bib')
old = comments('process/w3/checks/bib-references-before-w3.bib')
n_same = 0
for k in sorted(cur, key=str.lower):
    srcs = [s for s in (core.get(k), ext.get(k)) if s is not None]
    if cur[k] in srcs:
        n_same += 1
        continue
    print(f'== {k}\n   now : {cur[k]}')
    for name, d in (('core', core), ('ext', ext), ('oldW3', old)):
        if k in d:
            print(f'   {name:5s}: {d[k]}')
print('entries with comment identical to a W1 source comment:', n_same, 'of', len(cur))
