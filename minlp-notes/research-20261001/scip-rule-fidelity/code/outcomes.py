"""Outcome statistics of all intersection-cut attempts from the dump index (logs/index/*.jsonl).

Prints, per test set (mc11, mc12, minlplib): attempts, outcome counts, numerics subreasons,
cases, inertia, root share; per MINLPLib instance a one-line summary; and checks against the
per-run counter lines (attempts / generated / added agree with the records).
Also checks the per-expression limit of Section 1.1: no attempt at depth > 0 with exprncuts >= 2
and none at the root with exprncuts >= 20.
Usage: python3 outcomes.py [INDEXDIR]"""
import sys, json, glob, os, collections
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '../logs/index')
sets = collections.defaultdict(list); counters = collections.defaultdict(dict)
for f in sorted(glob.glob(os.path.join(d, '*.jsonl'))):
    st, inst = os.path.basename(f)[:-6].split('__')
    for l in open(f):
        r = json.loads(l)
        if 'counters' in r:
            counters[st][inst] = r['counters']
        elif 'nlhdlrstats' in r:
            pass
        else:
            sets[st].append(r)
for st in ('mc11', 'mc12', 'minlplib'):
    R = sets[st]
    print('==', st, 'instances with records', len({r['inst'] for r in R}), 'attempts', len(R))
    oc = collections.Counter(r['outcome'] for r in R)
    print('  outcomes', dict(oc.most_common()))
    print('  numerics subreason', dict(collections.Counter(r.get('sub') for r in R if r['outcome'] == 'fail:numerics')))
    print('  case', dict(collections.Counter(r.get('case') for r in R)), ' root share %.3f' % (sum(r['depth'] == 0 for r in R) / len(R)))
    print('  n_+ (violated side)', dict(sorted(collections.Counter(r['npos'] for r in R).items())))
    bad1 = sum(1 for r in R if r['depth'] > 0 and r['exprncuts'] >= 2)
    bad2 = sum(1 for r in R if r['depth'] == 0 and r['exprncuts'] >= 20)
    print('  limit check: depth>0 with exprncuts>=2:', bad1, ' root with exprncuts>=20:', bad2,
          ' attempts at depth>0:', sum(r['depth'] > 0 for r in R))
    C = counters[st]
    tot = collections.Counter()
    for c in C.values():
        tot.update(c)
    print('  counters summed over runs:', dict(tot))
    mism = [i for i, c in C.items() if c['attempts'] != sum(1 for r in R if r['inst'] == i)]
    print('  runs whose counter attempts != records:', mism)
    if st == 'minlplib':
        byi = collections.defaultdict(list)
        for r in R:
            byi[r['inst']].append(r)
        print('  %-30s %6s %6s %6s %6s %6s %6s %6s %s' % ('instance', 'att', 'added', 'numer', 'zeros', 'clean', 'other', 'nzrt', 'cases/n+'))
        for i in sorted(byi):
            X = byi[i]; o = collections.Counter(r['outcome'] for r in X)
            oth = len(X) - o['added'] - o['fail:numerics'] - o['fail:zerostat'] - o['cleanup_fail']
            nz = sum(1 for r in X if r.get('nzerorate', 0) > 0)
            print('  %-30s %6d %6d %6d %6d %6d %6d %6d %s %s' % (i, len(X), o['added'], o['fail:numerics'], o['fail:zerostat'], o['cleanup_fail'], oth, nz,
                  dict(collections.Counter(r.get('case') for r in X)), dict(collections.Counter(r['npos'] for r in X).most_common(3))))
