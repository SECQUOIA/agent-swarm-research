"""Which candidate set the selection rules (eff, oracle_seq, sumstep, ...) choose.
Usage: python3 analyze_choice.py 'GLOB'  (diag records of mrloop.py)"""
import sys, glob, json, collections
import recio
BUCK = [(0, 0), (1, 2), (3, 5), (6, 10), (11, 19)]
C = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for f in recio.files(sys.argv[1]):
    for line in recio.lines(f):
        r = json.loads(line)
        for c in r.get('cuts', []):
            b = [i for i, (a, z) in enumerate(BUCK) if a <= c['r'] <= z][0]
            C[r['rule']][b][c['set']] += 1
for rule, D in C.items():
    print('rule', rule)
    for b, cnt in sorted(D.items()):
        tot = sum(cnt.values())
        print('  r%d-%d  n=%4d  ' % (BUCK[b][0], BUCK[b][1], tot) + '  '.join('%s %.2f' % (k, v / tot) for k, v in cnt.most_common()))
