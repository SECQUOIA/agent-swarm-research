"""Recount Tables 6.1-6.3 of phase-transition.md from the stored run files (own aggregation) and
compare every printed cell with the note.  Capped runs take the status of c1_redecided.jsonl.
usage: python3 tables_check.py"""
import json, re, collections
import numpy as np

D = '../../bb-complexity/sparse-regression/data/'
NOTE = '../../bb-complexity/sparse-regression/phase-transition.md'


def rows(files, keep=lambda r: True):
    seen, out = set(), []
    for fn in files:
        for l in open(D + fn):
            r = json.loads(l)
            key = (r['p'], r['k'], r['n'], r['rule'], r['seed'])
            if key in seen or not keep(r):
                continue
            seen.add(key); out.append(r)
    return out


red = {}
for l in open(D + 'c1_redecided.jsonl'):
    r = json.loads(l)
    red[(r['p'], r['k'], r['n'], r['rule'], r['seed'])] = r['status']


def c1(r):
    if r['c1'] == 'capped':
        return red[(r['p'], r['k'], r['n'], r['rule'], r['seed'])] == 'C1'
    return r['c1'] is True


def recount(rs):
    cells = collections.defaultdict(list)
    for r in rs:
        cells[(r['p'], r['k'], r['n'])].append(r)
    out = {}
    for key, v in cells.items():
        out[key] = (len(v), sum(r['pwe'] for r in v), sum(r['wit'] for r in v), sum(c1(r) for r in v),
                    round(float(np.mean([r['tau'] ** 2 for r in v])), 2), round(float(np.mean([r['gap'] for r in v])), 3))
    return out


def printed(title):
    txt = open(NOTE).read()
    i = txt.index(title)
    out = {}
    for line in txt[i:].split('\n')[1:]:
        if line.startswith('| ') and re.match(r'\| \d', line):
            c = [x.strip() for x in line.strip('|').split('|')]
            out[(int(c[0]), int(c[1]), int(c[3]))] = (int(c[5]), int(c[6]), int(c[7]), int(c[8]), float(c[9]), float(c[12]))
        elif out and not line.startswith('|'):
            break
    return out


t61 = rows(['c1_p200_k8_t1.5.jsonl', 'c1_scaleP_1600_a2.jsonl', 'c1_scaleP_1600_hi.jsonl', 'c1_scaleP_k8_t1.5.jsonl'])
t62 = rows(['c1_gamma_half_full.jsonl']) + rows(['c1_gamma_half.jsonl'], keep=lambda r: r['n'] > 180 and r['p'] == 400 and r['k'] == 20)
t63 = rows(['c1_sqrtn_k5.jsonl'])
nred = sum(1 for r in t61 + t62 + t63 if r['c1'] == 'capped')
print("capped runs in the tabulated data: %d (redecided file has %d rows)" % (nred, len(red)))
for name, rs in [('Table 6.1 (', t61), ('Table 6.2 (', t62), ('Table 6.3 (', t63)]:
    mine, note = recount(rs), printed(name)
    bad = [(k, mine.get(k), note.get(k)) for k in sorted(set(mine) | set(note)) if mine.get(k) != note.get(k)]
    print("%s: %d cells printed, %d recounted, mismatches: %s" % (name.strip(' ('), len(note), len(mine), bad if bad else 'none'))
