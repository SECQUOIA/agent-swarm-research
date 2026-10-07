"""How many cuts reported as added (SCIPaddRow) are later found in the LP?

From the dump index: a cut added for expression e, side s, at LP number L of node n is 'seen in the
LP' if a later attempt record of e at node n lists [s, L] in 'lpcuts'.  Cuts with no later attempt
record of e at node n cannot be checked ('unknown').
Usage: python3 lp_entry.py SET [SET ...]"""
import sys, os, json, glob, collections
idxdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/index')
for st in sys.argv[1:]:
    tot = collections.Counter()
    for f in glob.glob(os.path.join(idxdir, st + '__*.jsonl')):
        X = [json.loads(l) for l in open(f)]
        X = [x for x in X if 'outcome' in x and 'lp' in x]
        for k, x in enumerate(X):
            if x['outcome'] != 'added':
                continue
            later = [y for y in X[k + 1:] if y['node'] == x['node'] and y['expr'] == x['expr'] and y['lp'] > x['lp']]
            if not later:
                tot['unknown'] += 1
            elif any([x['over'], x['lp']] in (y.get('lpcuts') or []) for y in later):
                tot['seen_in_LP'] += 1
            else:
                tot['never_seen'] += 1
    known = tot['seen_in_LP'] + tot['never_seen']
    print(st, dict(tot), 'fraction seen among checkable %.3f' % (tot['seen_in_LP'] / known if known else float('nan')))
