"""Selects the six minimizing-path records of certB and 14 random used records (seed 20261004)."""
import gzip, json, random, sys
rows = [json.loads(l) for l in gzip.open(sys.argv[1], 'rt')]
rec = [r for r in rows if r['kind'] == 'rec']
path = [52772, 52771, 52856, 53013, 52936, 53069]
random.seed(20261004)
samp = [r['rid'] for r in random.sample([r for r in rec if r['rid'] not in path], 14)]
json.dump([dict(key='r%d' % r, kind='rec', group='path' if i < 6 else 'sample', rid=r) for i, r in enumerate(path + samp)],
          open(sys.argv[2], 'w'))
