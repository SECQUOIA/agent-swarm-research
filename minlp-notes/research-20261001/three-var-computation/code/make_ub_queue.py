"""Write the queue of ub_local.py runs (start 0 = B point from sparse_audit) for every audited JSON instance."""
import glob, json, os
ub = []
for f in sorted(glob.glob('../logs/sparse_audit/*.json')):
    t = os.path.basename(f)[:-5]
    n = json.load(open(f))['n']
    ns = 40 if n <= 300 else (8 if n <= 1000 else 4)
    if not os.path.exists('../logs/ub2/%s.json' % t) or os.path.getsize('../logs/ub2/%s.json' % t) == 0:
        ub.append('timeout 3600 python ub_local.py ../data/{t}.json {ns} 1 ../logs/sparse_audit/{t}.json.base.npz > ../logs/ub2/{t}.json 2>&1'.format(t=t, ns=ns))
open('../data/tmp/queue_ub.txt', 'w').write('\n'.join(ub) + '\n')
print(len(ub))
