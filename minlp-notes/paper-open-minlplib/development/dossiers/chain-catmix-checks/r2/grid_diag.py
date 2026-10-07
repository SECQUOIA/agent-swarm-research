"""Float diagnostic (dossier): authors' per-stage grids for catmix100 (final settings).
Where does the transported 401-ray window sit, how wide is it, and what is the largest ray
spacing inside [0.0685, 0.0725] (the band) at each stage?"""
import numpy as np
import catmix_bound as A
import catmix_model as cmx
N = 100
m, K = cmx.extract(N)
A.BAND = (0.0685, 0.0725, 1e-6)
ustar = np.load('catmix100_u.npy')
grids, thstar, J = A.make_grids(N, K, ustar, 1e-5, 200, 1e-7)
worst = []
for i, g in enumerate(grids):
    sel = g[(g >= 0.0685) & (g <= 0.0725)]
    gaps = np.diff(sel) if len(sel) > 1 else np.array([np.nan])
    # spacing at the primal theta
    k = np.searchsorted(g, thstar[i]) if i < len(thstar) else None
    loc = g[k] - g[k - 1] if k is not None and 0 < k < len(g) else np.nan
    worst.append((i, len(g), np.nanmax(gaps), loc, thstar[i]))
arr = np.array(worst)
print('stages', len(grids), ' max band spacing over stages: %.3e  (median %.3e)' % (np.nanmax(arr[:, 2]), np.nanmedian(arr[:, 2])))
for row in worst[::10]:
    print('stage %3d rays %5d  max spacing in [0.0685,0.0725] %.2e  spacing at primal theta %.2e  theta* %.5f' % row)
