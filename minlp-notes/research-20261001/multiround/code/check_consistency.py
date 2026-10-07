"""Validity check of stored loop runs: every (rule, instance) trajectory that occurs in more than
one record file must be identical (the diag/choice/swap/new runs were made with later code
versions than some main runs; identical trajectories show that the later edits did not change
the rules).  Reads .jsonl and .jsonl.gz files (code/recio.py).  Usage: python3 check_consistency.py"""
import re, json, collections
import recio
F = collections.defaultdict(list)
for f in recio.files('../logs/main/*.jsonl') + recio.files('../logs/diag/*.jsonl') + recio.files('../logs/new/*.jsonl') + recio.files('../logs/rev1/*.jsonl') + recio.files('../logs/rev2/*.jsonl'):
    size = re.search(r'_(\d+x\d+)', f.split('/')[-1]).group(1)
    for line in recio.lines(f):
        r = json.loads(line)
        F[(size, r['rule'], r['inst'])].append((f, r['closed']))
n = bad = 0
for k, L in F.items():
    if len(L) < 2:
        continue
    for f, c in L[1:]:
        n += 1
        d = max(abs(a - b) for a, b in zip(L[0][1], c))
        if d > 1e-12:
            bad += 1; print('DIFFERS', k, L[0][0], f, d)
print('pairs of duplicate trajectories compared: %d, differing: %d' % (n, bad))
if n == 0:
    raise SystemExit('check_consistency: no duplicate trajectories found; are the record files present?')
