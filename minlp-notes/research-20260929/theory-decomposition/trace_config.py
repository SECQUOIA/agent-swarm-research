"""Trace the minimizing configuration of the fixed-slope DP (debugging aid for Section 5)."""
import sys
import numpy as np
from dp_certificate import shells, min_subbox, dphi, phi

def argmin_subbox(l1, u1, l2, u2, L1, U1, lin1, lin2, b, kappa, last, cz2):
    # brute force on a fine grid inside each sub-box to locate the minimizer (for tracing only)
    best = []
    for i in range(len(l1)):
        a = np.linspace(L1[i], U1[i], 201)[:, None]
        c = np.linspace(l2[i], u2[i], 201)[None, :]
        ab = abs(b)
        v = phi(a, kappa) + lin1[i] * a + b * a * c - (ab / 2) * ((a - l1[i]) * (u1[i] - a) + (c - l2[i]) * (u2[i] - c)) + lin2[i] * c
        if last:
            v = v + phi(c, kappa) + cz2 * c
        k = np.unravel_index(np.argmin(v), v.shape)
        best.append((float(a[k[0], 0]), float(c[0, k[1]])))
    return best

def trace(n, b, kappa, h, mu):
    c = np.zeros(n); xs = np.zeros(n); lam = np.zeros(n)
    info = {}
    child = None
    for t in range(n - 2, -1, -1):
        last = (t == n - 2)
        L, U = shells(xs[t:t + 2], h, mu, 2)
        l1, u1, l2, u2 = L[:, 0], U[:, 0], L[:, 1], U[:, 1]
        if child is not None:
            clo, chi, cbeta = child
            meet = (clo[None, :] <= u2[:, None]) & (chi[None, :] >= l2[:, None])
            offm = np.where(meet, cbeta[None, :], np.inf)
            off = offm.min(axis=1); offarg = offm.argmin(axis=1)
        else:
            off = np.zeros(len(L)); offarg = np.full(len(L), -1)
        lin2 = np.zeros(len(L))
        if t == 0:
            vals = min_subbox(l1, u1, l2, u2, l1.copy(), u1.copy(), np.zeros(len(L)), lin2, b, kappa, last, 0.0) + off
            i = int(np.argmin(vals))
            info[0] = dict(leaf=(L[i], U[i]), val=float(vals[i]), childcell=int(offarg[i]), off=float(off[i]))
            return info
        Pl, Pu = shells(xs[t:t + 1], h, mu, 1)
        plo, phi_ = Pl[:, 0], Pu[:, 0]
        meet = (plo[None, :] <= u1[:, None]) & (phi_[None, :] >= l1[:, None])
        bi, di = np.nonzero(meet)
        L1 = np.maximum(l1[bi], plo[di]); U1 = np.minimum(u1[bi], phi_[di])
        vals = min_subbox(l1[bi], u1[bi], l2[bi], u2[bi], L1, U1, np.zeros(len(bi)), lin2[bi], b, kappa, last, 0.0) + off[bi]
        beta = np.full(len(plo), np.inf); arg = np.full(len(plo), -1)
        for q in range(len(bi)):
            if vals[q] < beta[di[q]]:
                beta[di[q]] = vals[q]; arg[di[q]] = q
        info[t] = dict(cells=(plo, phi_), beta=beta, arg=arg, bi=bi, L=L, U=U, L1=L1, U1=U1, offarg=offarg, off=off)
        child = (plo, phi_, beta)

n = int(sys.argv[1]); mu = int(sys.argv[2]); h = 2.0 ** -int(sys.argv[3])
b, kappa = 0.8, 0.1
info = trace(n, b, kappa, h, mu)
r = info[0]
print("root value %.4e leaf %s-%s child cell %d" % (r['val'], r['leaf'][0], r['leaf'][1], r['childcell']))
cell = r['childcell']
for t in range(1, n - 1):
    it = info[t]
    q = it['arg'][cell]
    bi = it['bi'][q]
    lo, hi = it['L'][bi], it['U'][bi]
    pr = it['cells'][0][cell], it['cells'][1][cell]
    last = (t == n - 2)
    z = argmin_subbox(lo[:1], hi[:1], lo[1:], hi[1:], it['L1'][q:q+1], it['U1'][q:q+1], np.zeros(1), np.zeros(1), b, kappa, last, 0.0)[0]
    nxt = it['offarg'][bi] if not last else -1
    print("t=%2d cell [% .4f,% .4f] beta=% .4e leaf [% .4f,% .4f]x[% .4f,% .4f] z=(% .4f,% .4f) next cell %d" % (
        t, pr[0], pr[1], it['beta'][cell], lo[0], hi[0], lo[1], hi[1], z[0], z[1], nxt))
    cell = nxt
