"""Instance list for the root seed-variation runs: instances of logs/testset_root.txt whose seed-0 root runs
(logs/root.json) finished without time limit or error in all seven settings."""
import json, os
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
R = defaultdict(dict)
for r in json.load(open(os.path.join(HERE, '..', 'logs', 'root.json'))):
    R[r['inst']][r['setting']] = r
ok = sorted(i for i in R if len(R[i]) == 7 and all(r.get('status') and 'time limit' not in r['status'] and not r.get('error')
                                                  and r.get('returncode') == '0' for r in R[i].values()))
open(os.path.join(HERE, '..', 'logs', 'testset_rootseeds.txt'), 'w').write('\n'.join(ok) + '\n')
print(len(ok))
