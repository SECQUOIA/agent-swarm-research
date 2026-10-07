"""Per-part +inf counts and side/Farkas counts; union of r1 interval samples (A,B,C)."""
import glob, os
import numpy as np
P = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
for k in range(8):
    inf = side = fk = 0
    for f in glob.glob(os.path.join(P, 'eg-recheck', 'res', f'p{k}_c*.npz')):
        z = np.load(f); m = np.isposinf(z['mg'])
        inf += int(m.sum()); side += int((z['how'] == 1).sum()); fk += int((z['how'] == 3).sum())
    print('part', k, '+inf', inf, 'side', side, 'farkas', fk)
R = os.path.join(P, 'reviews', 'eg-recheck-r1')
tot = 0; allcert = True
for k in [0, 2, 3, 4, 5, 6, 7]:
    s = set(); 
    for f in glob.glob(os.path.join(R, f'sample_[ABC]_p{k}.npz')):
        z = np.load(f); s |= set(z['sel'].tolist())
        allcert &= bool((z['st'] == z['st'].max()).all()) if False else True
        print(os.path.basename(f), 'n', len(z['sel']), 'st values', np.unique(z['st']).tolist(), 'tight', len(z['tight']))
    print('part', k, 'distinct', len(s)); tot += len(s)
print('distinct sampled leaves parts 0,2-7:', tot)
