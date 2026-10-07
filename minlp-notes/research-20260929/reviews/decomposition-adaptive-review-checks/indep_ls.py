"""Independent re-implementation (reviewer) of algorithm LS of extension-adaptive.md, Section A.2,
for the path family F(x) = sum_i phi(x_i) + b sum_i x_i x_{i+1} + sum_i c_i x_i on [-1,1]^n,
phi(t) = t^2 - kappa t^4, bags V_t = {t, t+1} (t = 0..n-2), root bag 0, S_t = {t} (t >= 1).
Unary factors exact, bilinear factor by alphaBB with alpha = |b|/2 on the leaf box.

Written from the note's text, not from ls_lib.py. Differences on purpose:
  * bag subproblems: golden-section search in z1 with the inner z2 solved in closed form
    (non-last bags) or by safeguarded Newton (last bag); ls_lib uses nested bisection;
  * leaves are kept sorted lexicographically, so ties in argmin are broken differently;
  * interval intersection and DP are coded separately.
Floating point; illustrations only.
"""
import math
import numpy as np

B, KAPPA = 0.8, 0.1
AL = abs(B) / 2
GR = (math.sqrt(5.0) - 1.0) / 2.0
NGOLD = 90
NNEWT = 40


def phi(t):
    t2 = t * t
    return t2 - KAPPA * t2 * t2


def dphi(t):
    return t * (2.0 - 4.0 * KAPPA * t * t)


def ddphi(t):
    return 2.0 - 12.0 * KAPPA * t * t


def Fval(x, c):
    return float(np.sum(phi(x)) + B * np.sum(x[:-1] * x[1:]) + np.dot(c, x))


def slopes(x, c):
    n = len(x)
    lam = np.zeros(n)
    lam[1:n - 1] = dphi(x[1:n - 1]) + c[1:n - 1] + B * x[2:n]
    return lam


def _inner(z1, l2, u2, lin2, last, cz2):
    if not last:
        return np.clip((AL * (l2 + u2) - B * z1 - lin2) / (2 * AL), l2, u2)

    def g(z):
        return dphi(z) + cz2 + B * z1 + AL * (2 * z - l2 - u2) + lin2
    lo, hi = l2.copy(), u2.copy()
    glo, ghi = g(lo), g(hi)
    z = 0.5 * (lo + hi)
    for _ in range(NNEWT):
        gz = g(z)
        lo = np.where(gz < 0, z, lo)
        hi = np.where(gz > 0, z, hi)
        zn = z - gz / (ddphi(z) + 2 * AL)
        bad = ~((zn >= lo) & (zn <= hi))      # closed bracket: a converged step is kept
        z = np.where(gz == 0, z, np.where(bad, 0.5 * (lo + hi), zn))
    z = np.where(glo >= 0, l2, z)
    z = np.where(ghi <= 0, u2, z)
    return z


def _obj(z1, z2, l1, u1, l2, u2, lin1, lin2, last, cz2):
    v = (phi(z1) + lin1 * z1 + B * z1 * z2
         - AL * ((z1 - l1) * (u1 - z1) + (z2 - l2) * (u2 - z2)) + lin2 * z2)
    if last:
        v = v + phi(z2) + cz2 * z2
    return v


def bagmin(l1, u1, l2, u2, L1, U1, lin1, lin2, last, cz2):
    """min over z1 in [L1,U1], z2 in [l2,u2] of the relaxed, slope-shifted bag function
    (relaxation on the leaf [l1,u1]x[l2,u2]). Golden section in z1 (convex after
    partial minimization in z2). Returns (value, z1, z2)."""
    def h(z1):
        z2 = _inner(z1, l2, u2, lin2, last, cz2)
        return _obj(z1, z2, l1, u1, l2, u2, lin1, lin2, last, cz2), z2
    a, bb = L1.copy(), U1.copy()
    for _ in range(NGOLD):
        x1 = bb - GR * (bb - a)
        x2 = a + GR * (bb - a)
        f1, _ = h(x1)
        f2, _ = h(x2)
        left = f1 <= f2
        bb = np.where(left, x2, bb)
        a = np.where(left, a, x1)
    zc = 0.5 * (a + bb)
    best, z2b = h(zc)
    z1b = zc
    for zz in (L1, U1):
        v, z2 = h(zz)
        better = v < best
        best = np.where(better, v, best)
        z1b = np.where(better, zz, z1b)
        z2b = np.where(better, z2, z2b)
    return best, z1b, z2b


def meets(lo, hi, l, u):
    """pairs (k, D): closed interval [l_k, u_k] meets cell [lo_D, hi_D]. Cells tile [-1,1]."""
    o = np.argsort(lo, kind="stable")
    slo, shi = lo[o], hi[o]
    first = np.searchsorted(shi, l, side="left")        # shi[first] >= l
    last = np.searchsorted(slo, u, side="right") - 1    # slo[last] <= u
    cnt = np.maximum(last - first + 1, 0)
    k = np.repeat(np.arange(len(l)), cnt)
    start = np.repeat(first, cnt)
    off = np.arange(cnt.sum()) - np.repeat(np.cumsum(cnt) - cnt, cnt)
    return k, o[start + off]


def segmin(vals, grp, ng):
    out = np.full(ng, np.inf)
    np.minimum.at(out, grp, vals)
    # argmin: first index attaining the min
    arg = np.full(ng, -1)
    hit = vals <= out[grp]
    idx = np.nonzero(hit)[0]
    # keep the first index per group
    g = grp[idx]
    uniq, pos = np.unique(g, return_index=True)
    arg[uniq] = idx[pos]
    return out, arg


class Part:
    def __init__(self, n):
        self.n = n
        self.L = [dict(l1=np.array([-1.0]), u1=np.array([1.0]), l2=np.array([-1.0]),
                       u2=np.array([1.0]), lev=np.array([0])) for _ in range(n - 1)]
        self.C = [None] + [dict(lo=np.array([-1.0]), hi=np.array([1.0]), lev=np.array([0]))
                           for _ in range(1, n - 1)]

    def counts(self):
        return (sum(len(d["l1"]) for d in self.L), sum(len(d["lo"]) for d in self.C[1:]))

    def split(self, t, lm, cm):
        d = self.L[t]
        if lm.any():
            keep = {k: v[~lm] for k, v in d.items()}
            l1, u1, l2, u2, lv = d["l1"][lm], d["u1"][lm], d["l2"][lm], d["u2"][lm], d["lev"][lm]
            m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
            parts = [keep]
            for a1, b1 in ((l1, m1), (m1, u1)):
                for a2, b2 in ((l2, m2), (m2, u2)):
                    parts.append(dict(l1=a1, u1=b1, l2=a2, u2=b2, lev=lv + 1))
            new = {k: np.concatenate([p[k] for p in parts]) for k in d}
            o = np.lexsort((new["l2"], new["l1"]))       # canonical order
            self.L[t] = {k: v[o] for k, v in new.items()}
        if cm is not None and cm.any():
            e = self.C[t]
            lo, hi, lv = e["lo"][cm], e["hi"][cm], e["lev"][cm]
            mid = 0.5 * (lo + hi)
            nlo = np.concatenate([e["lo"][~cm], lo, mid])
            nhi = np.concatenate([e["hi"][~cm], mid, hi])
            nlv = np.concatenate([e["lev"][~cm], lv + 1, lv + 1])
            o = np.argsort(nlo, kind="stable")
            self.C[t] = dict(lo=nlo[o], hi=nhi[o], lev=nlv[o])


def dp(P, lam, c):
    """beta (bottom-up), min-marginals (top-down), a minimizing configuration."""
    n = P.n
    info = [None] * (n - 1)
    npairs = 0
    childmin = np.zeros(0)
    for t in range(n - 2, -1, -1):
        d = P.L[t]
        nl = len(d["l1"])
        last = t == n - 2
        if last:
            mch = np.zeros(nl)
            mcharg = np.full(nl, -1)
            ck = cD = None
            lin2 = 0.0
        else:
            e = P.C[t + 1]
            ck, cD = meets(e["lo"], e["hi"], d["l2"], d["u2"])
            mch, a = segmin(info[t + 1]["beta"][cD], ck, nl)
            mcharg = cD[a]
            lin2 = lam[t + 1]
        if t == 0:
            v, z1, z2 = bagmin(d["l1"], d["u1"], d["l2"], d["u2"], d["l1"], d["u1"],
                               np.full(nl, c[0]), np.full(nl, lin2), last, c[n - 1])
            info[0] = dict(g=v, z1=z1, z2=z2, mch=mch, mcharg=mcharg, ck=ck, cD=cD)
            npairs += nl
            break
        e = P.C[t]
        bi, di = meets(e["lo"], e["hi"], d["l1"], d["u1"])
        npairs += len(bi)
        L1 = np.maximum(d["l1"][bi], e["lo"][di])
        U1 = np.minimum(d["u1"][bi], e["hi"][di])
        v, z1, z2 = bagmin(d["l1"][bi], d["u1"][bi], d["l2"][bi], d["u2"][bi], L1, U1,
                           np.full(len(bi), c[t] - lam[t]), np.full(len(bi), lin2), last, c[n - 1])
        beta, barg = segmin(v + mch[bi], di, len(e["lo"]))
        info[t] = dict(g=v, z1=z1, z2=z2, bi=bi, di=di, mch=mch, mcharg=mcharg, ck=ck, cD=cD,
                       beta=beta, barg=barg)
    rootv = info[0]["g"] + info[0]["mch"]
    lr = float(rootv.min())
    MML = [None] * (n - 1)
    MMC = [None] * (n - 1)
    o = info[0]["g"].copy()
    MML[0] = o + info[0]["mch"]
    for t in range(1, n - 1):
        ck, cD = info[t - 1]["ck"], info[t - 1]["cD"]
        out = np.full(len(P.C[t]["lo"]), np.inf)
        np.minimum.at(out, cD, o[ck])
        MMC[t] = out + info[t]["beta"]
        bi, di = info[t]["bi"], info[t]["di"]
        on = np.full(len(P.L[t]["l1"]), np.inf)
        np.minimum.at(on, bi, out[di] + info[t]["g"])
        o = on
        MML[t] = o + info[t]["mch"]
    # minimizing configuration: first argmin in the canonical order
    k = int(np.argmin(rootv))
    x = np.zeros(n)
    x[0], x[1] = info[0]["z1"][k], info[0]["z2"][k]
    val = info[0]["g"][k]
    D = info[0]["mcharg"][k]
    for t in range(1, n - 1):
        q = info[t]["barg"][D]
        leaf = info[t]["bi"][q]
        val += info[t]["g"][q]
        x[t + 1] = info[t]["z2"][q]
        D = info[t]["mcharg"][leaf]
    return dict(lr=lr, MML=MML, MMC=MMC, x=x, confval=float(val), npairs=npairs)


def ls(n, c, eps, x0, pmax=30, fixed_lam=None, xstar=None, fstar=None, log=None):
    """Algorithm LS (Section A.2). fixed_lam: one pass with these slopes, no restarts."""
    UBD = Fval(x0, c)
    xbest = x0.copy()
    xprev = x0.copy()
    processed = 0
    recs = []
    start = {}
    passes = [None] if fixed_lam is not None else range(pmax + 1)
    for p in passes:
        lam = fixed_lam if fixed_lam is not None else slopes(xprev, c)
        P = Part(n)
        start = dict(lam=lam.copy(), UBD=UBD, xbest=xbest.copy())
        top = pmax if fixed_lam is not None else p
        for i in range(top + 1):
            nl, nc = P.counts()
            processed += nl + nc
            R = dp(P, lam, c)
            fx = Fval(R["x"], c)
            if fx < UBD:
                UBD, xbest = fx, R["x"].copy()
            thr = UBD - eps
            viol = 0
            live = []
            for t in range(n - 1):
                lev = P.L[t]["lev"]
                viol += int(np.sum((lev < i) & (R["MML"][t] < thr - 1e-12)))
                live.append(int(np.sum((lev == i) & (R["MML"][t] < thr))))
                if t >= 1:
                    viol += int(np.sum((P.C[t]["lev"] < i) & (R["MMC"][t] < thr - 1e-12)))
            s = 2.0 * 2.0 ** (-i)
            rec = dict(p=p, i=i, leaves=nl, cells=nc, lr=R["lr"], UBD=UBD, viol=viol,
                       live_mean=float(np.mean(live)), live_max=max(live), npairs=R["npairs"],
                       mmcheck=min(float(np.min(m)) for m in R["MML"]) - R["lr"],
                       conf_err=abs(R["confval"] - R["lr"]))
            if xstar is not None:
                # sup-distance (units of s_i) from x*_{V_t} of the farthest live (to-be-split) leaf
                far = 0.0
                for t in range(n - 1):
                    d = P.L[t]
                    m = (d["lev"] == i) & (R["MML"][t] < thr)
                    if m.any():
                        dx = np.maximum(np.maximum(d["l1"][m] - xstar[t], xstar[t] - d["u1"][m]), 0)
                        dy = np.maximum(np.maximum(d["l2"][m] - xstar[t + 1], xstar[t + 1] - d["u2"][m]), 0)
                        far = max(far, float(np.maximum(dx, dy).max()))
                rec["far_s"] = far / s
                rec["dx2_s"] = float(np.linalg.norm(R["x"] - xstar)) / s
                rec["dxinf_s"] = float(np.abs(R["x"] - xstar).max()) / s
                rec["nu"] = float(np.linalg.norm(lam - slopes(xstar, c)))
            if fstar is not None:
                rec["gap"] = fstar - R["lr"]
            recs.append(rec)
            if log:
                log(rec)
            if R["lr"] >= thr:
                return dict(done=True, p=p, i=i, size=nl + nc, leaves=nl, cells=nc, lr=R["lr"],
                            UBD=UBD, processed=processed, npairs=R["npairs"], start=start), recs
            if i < top:
                for t in range(n - 1):
                    lm = (P.L[t]["lev"] == i) & (R["MML"][t] < thr)
                    cm = ((P.C[t]["lev"] == i) & (R["MMC"][t] < thr)) if t >= 1 else None
                    P.split(t, lm, cm)
        xprev = R["x"]
    return dict(done=False, processed=processed), recs


def global_min_indep(n, c, G=2001):
    """Grid DP over the path (G points) followed by Newton polishing (interior minimizer)."""
    y = np.linspace(-1, 1, G)
    V = phi(y) + c[n - 1] * y
    args = []
    for i in range(n - 2, -1, -1):
        M = (phi(y) + c[i] * y)[:, None] + B * y[:, None] * y[None, :] + V[None, :]
        a = M.argmin(axis=1)
        args.append(a)
        V = M[np.arange(G), a]
    args = args[::-1]
    j = int(V.argmin())
    idx = [j]
    for i in range(n - 1):
        idx.append(int(args[i][idx[-1]]))
    x = y[idx].copy()
    for _ in range(50):
        g = dphi(x) + c
        g[:-1] += B * x[1:]
        g[1:] += B * x[:-1]
        H = np.diag(ddphi(x)) + B * (np.eye(n, k=1) + np.eye(n, k=-1))
        x = x - np.linalg.solve(H, g)
    g = dphi(x) + c
    g[:-1] += B * x[1:]
    g[1:] += B * x[:-1]
    return x, Fval(x, c), float(np.abs(g).max())
