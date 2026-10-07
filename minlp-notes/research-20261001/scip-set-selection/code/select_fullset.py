"""Select the full-solve test set: a random sample (seed 20261001) of 60 instances among those whose root
screening run with SCIP's rule (logs/screen.json) applied at least one intersection cut, was not solved in
the root node, and took less than 30 CPU seconds.  Uses only information from SCIP's own rule."""
import json, random, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, '..', 'logs', 'screen.json')))
pool = sorted(r['inst'] for r in R if (r.get('rootapplied') or 0) > 0 and 'optimal' not in (r['status'] or '')
              and r['time'] < 30)
sel = sorted(random.Random(20261001).sample(pool, 60))
open(os.path.join(HERE, '..', 'logs', 'testset_full.txt'), 'w').write('\n'.join(sel) + '\n')
print(len(pool), len(sel))
