"""Independent check of corner dumps written by the patched SCIP (nlhdlr/quadratic/dumpfile).

For every dumped corner (one root intersection cut) this script
  1. rebuilds the quadratic q(s) <= 0 over the constraint variables from the dumped quadratic data and checks that
     SCIP's eigendecomposition reproduces it (||x||^2 - ||y||^2 + w + kappa = q at random points);
  2. evaluates the Chmiela-Munoz-Serrano set C_lambda = {phi_lambda(yhat) <= lambda^T xhat} directly from its
     definition (Munoz-Serrano 2022, Proposition 5), for SCIP's lambda and for the chosen lambda, and computes
     every step length by bisection on the membership function (no use of SCIP's closed forms);
  3. compares these step lengths with the ones computed in C (search evaluation and final cut);
  4. checks S-freeness of C_lambda numerically: q > 0 at sampled interior points, and along every ray before its
     step length;
  5. for small corners, computes the corner bound z_K with research-20260928b/sfree/code/core.py (support
     enumeration up to rho(q) rays, Theorem 4) and checks the validity consequence z_C <= z_K (Theorem 1(2)).

Usage: python3 check_dump.py DUMPFILE [MAXCORNERS] [ZK_MAXRAYS]
"""
import sys, os, json, gzip
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'research-20260928b', 'sfree', 'code'))
from core import corner_bound   # noqa: E402

EPSZERO = 1e-9   # SCIP's default numerics/epsilon (SCIPisZero)


class Corner:
    def __init__(self, d):
        self.d = d
        nq, nl, aux = d['nquad'], d['nlin'], d['aux']
        self.nq, self.nl, self.aux = nq, nl, aux
        self.n = nq + nl + aux
        sf = d['sf']
        self.sf = sf
        Q = np.zeros((nq, nq))
        for i in range(nq):
            Q[i, i] = d['sqrcoef'][i]
        for i, j, c in d['bilin']:
            Q[i, j] += c / 2.0
            Q[j, i] += c / 2.0
        self.Qq = Q
        self.eig = np.array(d['eigval'])
        self.V = np.array(d['eigvec']).reshape(nq, nq)      # row i = eigenvector i
        # full quadratic over consvars (sidefactor applied): q(s) = s^T Qf s + bf^T s + cf
        Qf = np.zeros((self.n, self.n)); Qf[:nq, :nq] = sf * Q
        bf = np.zeros(self.n); bf[:nq] = sf * np.array(d['quadlin'])
        if nl:
            bf[nq:nq + nl] = sf * np.array(d['lincoef'])
        if aux:
            bf[-1] = -sf
        self.Qf, self.bf, self.cf = Qf, bf, d['constant']
        self.sbar = np.array(d['sbar'])
        P = np.zeros((self.n, len(d['rays'])))
        for j, ray in enumerate(d['rays']):
            for idx, v in ray:
                P[idx, j] = v
        self.P = P
        self.w = np.array(d['w'])
        th = sf * self.eig
        self.th = th
        self.vb = self.V @ (sf * np.array(d['quadlin']))
        self.Ip = [i for i in range(nq) if abs(self.eig[i]) > EPSZERO and th[i] > 0]
        self.Im = [i for i in range(nq) if abs(self.eig[i]) > EPSZERO and th[i] < 0]
        self.I0 = [i for i in range(nq) if abs(self.eig[i]) <= EPSZERO]
        kappa = self.cf - 0.25 * sum(self.vb[i] ** 2 / th[i] for i in self.Ip + self.Im)
        if abs(kappa) <= EPSZERO:
            kappa = 0.0
        self.kappa = kappa
        self.iscase4 = bool(d['iscase4'])

    def q(self, s):
        return float(s @ self.Qf @ s + self.bf @ s + self.cf)

    def xyw(self, s):
        sq = s[:self.nq]
        psi = self.V @ sq
        x = np.array([np.sqrt(self.th[i]) * (psi[i] + self.vb[i] / (2 * self.th[i])) for i in self.Ip])
        y = np.array([np.sqrt(-self.th[i]) * (psi[i] + self.vb[i] / (2 * self.th[i])) for i in self.Im])
        w = sum(self.vb[i] * psi[i] for i in self.I0)
        if self.nl:
            w += self.sf * float(np.array(self.d['lincoef']) @ s[self.nq:self.nq + self.nl])
        if self.aux:
            w -= self.sf * s[-1]
        return x, y, w

    def decomposition_error(self, rng, k=20):
        err = 0.0
        scale = 1.0 + np.abs(self.sbar).max()
        for _ in range(k):
            s = self.sbar + scale * rng.normal(size=self.n)
            x, y, w = self.xyw(s)
            lhs = x @ x - y @ y + w + self.kappa
            err = max(err, abs(lhs - self.q(s)) / (1 + abs(self.q(s))))
        return err

    def G(self, lam, s):
        """gauge-type function of C_lambda: C = {G <= 0}"""
        x, y, w = self.xyw(s)
        if not self.iscase4:
            if self.kappa > 0:
                return np.linalg.norm(y) - lam @ np.append(x, np.sqrt(self.kappa))
            if self.kappa < 0:
                return np.linalg.norm(np.append(y, np.sqrt(-self.kappa))) - lam @ x
            return np.linalg.norm(y) - lam @ x
        r = np.sqrt(1 + self.kappa ** 2); sr = np.sqrt(r)
        xh = np.append(x, (w + self.kappa + r) / (2 * sr))
        yh = np.append(y, (w + self.kappa - r) / (2 * sr))
        ll = lam[-1]
        ny = np.linalg.norm(yh)
        if -ll * ny + yh[-1] <= 0:
            phi = ny
        else:
            phi = np.sqrt(max(0.0, (1 - ll ** 2) * (ny ** 2 - yh[-1] ** 2))) + ll * yh[-1]
        return phi - lam @ xh

    def step(self, lam, p, amax=1e12):
        g = lambda t: self.G(lam, self.sbar + t * p)
        if np.linalg.norm(p) == 0:
            return np.inf
        if g(amax) <= 0:
            return np.inf
        lo, hi = 0.0, 1e-8
        while g(hi) <= 0:
            lo, hi = hi, hi * 2
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if g(mid) <= 0:
                lo = mid
            else:
                hi = mid
            if hi - lo <= 1e-14 * hi:
                break
        return 0.5 * (lo + hi)


def reduced(c):
    """Affine coordinates t = (x(s), y(s), [w(s)]) in which q = ||x||^2 - ||y||^2 [+ w] + kappa.  Returns
    (Q', b', c', tbar, P') for core.corner_bound.  The corner set {lam >= 0 : q(sbar + P lam) <= 0} is the same."""
    def coords(s):
        x, y, w = c.xyw(s)
        return np.concatenate([x, y, [w]]) if c.iscase4 else np.concatenate([x, y])
    t0 = coords(np.zeros(c.n))
    T = np.array([coords(np.eye(c.n)[i]) - t0 for i in range(c.n)]).T     # affine: coords(s) = t0 + T s
    k = len(t0); npos, nneg = len(c.Ip), len(c.Im)
    Qr = np.diag([1.0] * npos + [-1.0] * nneg + ([0.0] if c.iscase4 else []))
    br = np.zeros(k)
    if c.iscase4:
        br[-1] = 1.0
    return Qr, br, c.kappa, t0 + T @ c.sbar, T @ c.P


def rho(c):
    """rho(q) of Theorem 4 in the reduced coordinates: n_+ + n_0 + 1 - [b not in range Q]."""
    return len(c.Ip) + 1 if c.iscase4 else len(c.Ip) + 1


def fin_used(fin):
    return fin is not None and bool(fin.get('usedlambda'))


def main():
    path = sys.argv[1]
    maxc = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    zk_maxrays = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    rng = np.random.default_rng(1)
    op = gzip.open if path.endswith('.gz') else open
    # the final record of a cut computed with SCIP's own lambda in Case 2 can contain uninitialized entries for
    # rays handled by monoidal strengthening (printed as nan); json accepts NaN
    lines = [json.loads(l.replace('-nan', 'NaN').replace('nan', 'NaN')) for l in op(path, 'rt') if l.strip()]
    stats = dict(corners=0, decomp_max=0.0, alpha0_maxrel=0.0, alpha_maxrel=0.0, final_maxrel=0.0, overshoot=0,
                 sfree_viol=0, ray_viol=0, zk_checked=0, zk_viol=0, crit_mismatch=0, changed=0, rel_gain=[],
                 zC_over_zK_scip=[], zC_over_zK_sel=[], qbar_nonpos=0, rays_compared=0, rays_short10=0, zk_spurious=0)
    k = 0
    while k < len(lines) and stats['corners'] < maxc:
        d = lines[k]
        fin = lines[k + 1] if k + 1 < len(lines) and lines[k + 1]['type'] == 'final' else None
        k += 2 if fin is not None else 1
        if d['type'] != 'corner':
            continue
        c = Corner(d)
        stats['corners'] += 1
        if c.q(c.sbar) <= 0:
            stats['qbar_nonpos'] += 1
        stats['decomp_max'] = max(stats['decomp_max'], c.decomposition_error(rng))
        lam0 = np.array(d['lam0']); lam = np.array(d['lam'])
        N = c.P.shape[1]
        ref0 = np.array([c.step(lam0, c.P[:, j]) for j in range(N)])
        ref = np.array([c.step(lam, c.P[:, j]) for j in range(N)]) if d['changed'] else ref0

        def cmp(alC, alR, count_short=False):
            m = 0.0; over = 0
            for a, b in zip(alC, alR):
                a = np.inf if a < 0 else a
                if np.isinf(a) and np.isinf(b):
                    continue
                if np.isinf(a) != np.isinf(b):
                    # a step of 1e12+ counts as infinite in the reference; SCIP's infinity is 1e20
                    big = a if np.isinf(b) else b
                    if big > 1e9:
                        continue
                    m = max(m, 1.0); over += np.isinf(a)
                    continue
                m = max(m, abs(a - b) / max(1.0, abs(b)))
                if a > b * (1 + 1e-7) + 1e-9 and b < 1e9:
                    over += 1
                if count_short:
                    stats['rays_compared'] += 1
                    if np.isfinite(b) and a < 0.9 * b:
                        stats['rays_short10'] += 1
            return m, over
        m0, o0 = cmp(d['alpha0'], ref0)
        m1, o1 = cmp(d['alpha'], ref)
        stats['alpha0_maxrel'] = max(stats['alpha0_maxrel'], m0)
        stats['alpha_maxrel'] = max(stats['alpha_maxrel'], m1)
        stats['overshoot'] += o0 + o1
        monoidal_possible = (not c.iscase4) and c.kappa > 0 and not fin_used(fin)
        if fin is not None and fin['success'] and not monoidal_possible:
            mf, of = cmp(fin['alpha'], ref, count_short=True)
            stats['final_maxrel'] = max(stats['final_maxrel'], mf)
            stats['overshoot'] += of
        # S-freeness of C_lambda (chosen lambda): q > 0 inside
        for _ in range(30):
            dvec = rng.normal(size=c.n)
            t = c.step(lam, dvec)
            tt = min(t, 1e6) if np.isfinite(t) else 1e6
            for u in (0.25, 0.5, 0.9, 0.999):
                s = c.sbar + u * tt * dvec
                if c.G(lam, s) < 0 and c.q(s) < -1e-7 * (1 + abs(c.q(c.sbar))):
                    stats['sfree_viol'] += 1
        for j in range(N):
            t = ref[j]
            tt = min(t, 1e6) if np.isfinite(t) else 1e6
            for u in np.linspace(0.05, 0.999, 12):
                if c.q(c.sbar + u * tt * c.P[:, j]) < -1e-7 * (1 + abs(c.q(c.sbar))):
                    stats['ray_viol'] += 1
                    break
        wt = np.maximum(c.w, 1e-6 * max(c.w.max(), 1e-9))
        zC0 = min([wt[j] * ref0[j] for j in range(N) if np.isfinite(ref0[j])], default=np.inf)
        zC = min([wt[j] * ref[j] for j in range(N) if np.isfinite(ref[j])], default=np.inf)
        if d['rule'] == 1 and np.isfinite(zC):
            if abs(zC - d['critbest']) > 1e-5 * max(1e-12, abs(zC)) + 1e-12:
                stats['crit_mismatch'] += 1
        if d['changed']:
            stats['changed'] += 1
            if d['crit0'] > 0:
                stats['rel_gain'].append(d['critbest'] / d['crit0'])
        rh = rho(c)
        if (rh <= 2 and N <= 2 * zk_maxrays) or (rh <= 4 and N <= zk_maxrays // 2):
            if True:
                Qr, br, cr, tbar, Pr = reduced(c)
                assert abs(float(tbar @ Qr @ tbar + br @ tbar + cr) - c.q(c.sbar)) <= 1e-8 * (1 + abs(c.q(c.sbar)))
                zk, lamk = corner_bound(Qr, br, cr, tbar, Pr, wt, max_support=min(rh, np.linalg.matrix_rank(Pr)),
                                        return_point=True)
                if np.isfinite(zk):
                    tk = tbar + Pr @ lamk
                    if float(tk @ Qr @ tk + br @ tk + cr) > 1e-6 * (1 + abs(c.q(c.sbar))):
                        # core.two_ray does not check feasibility of its point; near-constant rays with tiny floored
                        # weights can give a spurious finite value (see note, Section 4.2)
                        stats['zk_spurious'] += 1
                        zk = np.nan
                stats['zk_checked'] += 1
                if np.isfinite(zk):
                    tol = 1e-6 * max(1.0, abs(zk))
                    if zC0 > zk + tol or zC > zk + tol:
                        stats['zk_viol'] += 1
                        print('ZK VIOLATION', stats['corners'], zC0, zC, zk, flush=True)
                    if zk > 0:
                        stats['zC_over_zK_scip'].append(min(zC0, zk) / zk)
                        stats['zC_over_zK_sel'].append(min(zC, zk) / zk)
    out = {k_: v for k_, v in stats.items() if not isinstance(v, list)}
    for key in ('rel_gain', 'zC_over_zK_scip', 'zC_over_zK_sel'):
        v = np.array(stats[key])
        out[key] = dict(n=len(v), mean=float(v.mean()) if len(v) else None, median=float(np.median(v)) if len(v) else None,
                        min=float(v.min()) if len(v) else None)
    v1, v0 = np.array(stats['zC_over_zK_sel']), np.array(stats['zC_over_zK_scip'])
    if len(v1):
        out['reach_zK_scip'] = int((v0 > 0.9999).sum()); out['reach_zK_sel'] = int((v1 > 0.9999).sum())
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
