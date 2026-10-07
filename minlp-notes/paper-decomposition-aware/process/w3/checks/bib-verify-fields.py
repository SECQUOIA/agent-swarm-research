"""Verifier check: field-level diff of entries kept from the pre-W3 references.bib."""
import re

def entries(path):
    t = open(path, encoding='utf8').read()
    out = {}
    for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}', t, re.S):
        fields = {}
        for f in re.finditer(r'^\s*(\w+)\s*=\s*\{(.*)\},?\s*$', m.group(3), re.M):
            fields[f.group(1).lower()] = f.group(2)
        fields['@type'] = m.group(1).lower()
        out[m.group(2)] = fields
    return out

old = entries('process/w3/checks/bib-references-before-w3.bib')
new = entries('references.bib')
for k in sorted(set(old) & set(new), key=str.lower):
    o, n = old[k], new[k]
    diffs = [(f, o.get(f), n.get(f)) for f in sorted(set(o) | set(n)) if o.get(f) != n.get(f)]
    if diffs:
        print('==', k)
        for f, a, b in diffs:
            print(f'   {f}: {a!r}\n   {" " * len(f)}  -> {b!r}')
