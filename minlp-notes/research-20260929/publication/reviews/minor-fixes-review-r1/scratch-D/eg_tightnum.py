"""Group D: are tight_leaves.log leaf numbers chunk-concatenation positions? Check every listed leaf's margin."""
import glob, os, re
import numpy as np
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'eg-recheck'))
ok = bad = 0
for line in open(os.path.join(P, 'logs', 'tight_leaves.log')):
    m = re.match(r'part (\d) leaf (\d+) \(.*\): margin (\S+);', line)
    if not m: continue
    k, j, mg = int(m[1]), int(m[2]), float(m[3])
    Z = [np.load(f) for f in sorted(glob.glob(os.path.join(P, 'res', f'p{k}_c*.npz')))]
    cat = np.concatenate([z['mg'] for z in Z]); sel = np.concatenate([z['sel'] for z in Z])
    good_cat = abs(cat[j] - mg) <= 5e-4 * abs(mg)
    pos = np.flatnonzero(sel == j)
    good_idx = len(pos) and abs(cat[pos[0]] - mg) <= 5e-4 * abs(mg)
    ok += bool(good_cat); bad += (not good_cat)
    if not good_cat or good_idx: print('part', k, 'leaf', j, 'concat match', bool(good_cat), 'leaf-list-index match', bool(good_idx))
print('tight_leaves entries matching concatenation positions:', ok, 'not matching:', bad)
