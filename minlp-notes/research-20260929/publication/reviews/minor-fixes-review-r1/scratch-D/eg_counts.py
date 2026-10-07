"""Group D independent recount of eg-recheck saved leaf results."""
import glob, os, collections
import numpy as np
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
E = os.path.join(P, 'eg-recheck', 'res')
tot = 0; inf_by_how = collections.Counter(); how_all = collections.Counter(); nproc = {}; okall = True
part_leaves = {}
for k in range(8):
    files = sorted(glob.glob(os.path.join(E, f'p{k}_c*.npz')), key=lambda f: int(f.split('_c')[1].split('.')[0]))
    sels = []
    for f in files:
        z = np.load(f)
        sels.append(z['sel']); okall &= bool(z['ok'].all())
        mg, how = z['mg'], z['how']
        for h in np.unique(how):
            how_all[int(h)] += int((how == h).sum())
            inf_by_how[int(h)] += int(((how == h) & np.isposinf(mg)).sum())
        nproc.setdefault(k, set()).add(int(z['n_proc']))
        nl = int(z['n_leaves'])
    s = np.concatenate(sels)
    assert len(s) == nl and len(np.unique(s)) == nl and s.min() == 0 and s.max() == nl - 1, k
    part_leaves[k] = nl; tot += len(s)
    print('part', k, 'leaves', nl, 'n_proc', nproc[k], 'chunks', len(files))
print('total leaves', tot, 'all ok', okall)
print('how counts (all leaves)', dict(how_all))
print('+inf margin leaves by how', dict(inf_by_how), 'sum', sum(inf_by_how.values()))
print('sum n_proc', sum(next(iter(v)) for v in nproc.values()))
print('parts 0,2-7 leaves', tot - part_leaves[1], 'part 1', part_leaves[1])
# leaf numbering: position 69407 in chunk concatenation of part 5
files = sorted(glob.glob(os.path.join(E, 'p5_c*.npz')), key=lambda f: int(f.split('_c')[1].split('.')[0]))
Z = [np.load(f) for f in files]
cat = lambda key: np.concatenate([z[key] for z in Z])
sel, lo, hi, mg = cat('sel'), cat('lo'), cat('hi'), cat('mg')
j = 69407
print('pos 69407: sel', int(sel[j]), 'mg', mg[j], 'lo', lo[j].tolist(), 'hi', hi[j].tolist())
fin = np.isfinite(mg)
print('argmin finite mg in part 5 position', int(np.argmin(np.where(fin, mg, np.inf))), 'min', np.min(mg[fin]))
# compare with the reviewer's derived leaf list (built from rec/ per verify_tree convention)
L = np.load(os.path.join(P, 'reviews', 'eg-recheck-r1', 'leaves_p5.npz'))
i = int(sel[j])
print('reviewer leaves_p5[%d] equal box:' % i, bool((L['lo'][i] == lo[j]).all() and (L['hi'][i] == hi[j]).all()), 'mg', L['mg'][i])
# is the glob order also the sorted order (inspect_leaf uses sorted(glob))?
print('sorted glob order', [os.path.basename(f) for f in sorted(glob.glob(os.path.join(E, 'p5_c*.npz')))])
