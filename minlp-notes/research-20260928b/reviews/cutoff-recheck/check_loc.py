"""Recheck of Proposition 5.1a (two-sided localization).

For a point y, with N = {y}: D0' = min_i (D_i(y) - |d_i f(y)|); K0 from the
second partials d_ii t_j on the segments y + s e_i, |s| <= rho (sampled);
rho' = min(rho, D0'/(4 K0)); theta' = D0' rho'/4. Only points with
m(y) + eps < theta' are used, so the hypotheses hold (up to sampling of K0).
Claim: if propagation at cutoff f* - eps removes y from C, then every face of
C is within r = 4(m(y)+eps)/D0' of y.

(A) Random boxes (four faces log-uniform in r*[1e-3, 10^0.5]).
(B) Adversarial: all faces at 1e-4 r except one; bisection for the largest
    distance of that face at which y is still removed (removal is monotone in
    the box, Lemma 1.2(a)); report distance / r.
Instances: cnd1 = (s-1)^2 (s^2+1) in monomial form (1D, CND at s = 1) and
linediag = h(x - y) in expanded form (2D, CND on t in [0.2, 1.1] of the line).
Run: python3 check_loc.py > logs/check_loc.log
"""
import random
import numpy as np
import sympy as sp
import iprop as P
import inst as I

rng = random.Random(51)
RHO = 0.05


def setup(J):
    syms = J['syms']
    Pl = sp.Poly(sp.expand(J['f']), *syms)
    terms = [coef * sp.prod([v ** e for v, e in zip(syms, mon)]) for mon, coef in Pl.terms()
             if any(mon)]
    n = len(syms)
    g = [[sp.lambdify(syms, sp.diff(t, v)) for v in syms] for t in terms]
    h = [[sp.lambdify(syms, sp.diff(t, v, 2)) for v in syms] for t in terms]
    F = sp.lambdify(syms, J['f'])
    return dict(n=n, g=g, h=h, F=F, dag=J['dag'], fstar=J['fstar'])


def constants(S, y):
    n = S['n']
    Dp = np.inf
    K0 = 0.0
    for i in range(n):
        gi = np.array([float(gt[i](*y)) for gt in S['g']])
        Di = np.abs(gi).sum() - 2 * np.abs(gi).max()
        Dp = min(Dp, Di - abs(gi.sum()))
        H = np.zeros(len(S['h']))
        for s in np.linspace(-RHO, RHO, 101):
            z = list(y)
            z[i] += s
            H = np.maximum(H, [abs(float(ht[i](*z))) for ht in S['h']])
        K0 = max(K0, 1.001 * (H.sum() / 2 + H.max()))
    rho_p = min(RHO, Dp / (4 * K0))
    return Dp, K0, rho_p, Dp * rho_p / 4


def removed(S, y, box, eps):
    st, Z, _ = P.fixpoint(S['dag'], box, S['fstar'] - eps, max_rounds=50000)
    if st == 'empty':
        return True
    xb = P.xbox(S['dag'], Z)
    return not all(xb[i][0] - 1e-13 <= y[i] <= xb[i][1] + 1e-13 for i in range(len(y)))


def sample_point(name):
    if name == 'cnd1':
        return [1.0 + rng.uniform(-0.02, 0.02)]
    t = rng.uniform(0.2, 1.1)
    return [t + 1 + rng.uniform(-0.008, 0.008), t]


def run(name, J, npts, nbox, nadv):
    S = setup(J)
    tried = rem = viol = 0
    worst = 0.0
    adv = []
    usable = 0
    for _ in range(npts):
        y = sample_point(name)
        eps = 10 ** rng.uniform(-7, -3)
        m = float(S['F'](*y)) - S['fstar']
        Dp, K0, rho_p, theta_p = constants(S, y)
        if not (Dp > 0 and m + eps < theta_p):
            continue
        usable += 1
        r = 4 * (m + eps) / Dp
        for _ in range(nbox):
            dist = [[r * 10 ** rng.uniform(-3, 0.5) for _ in range(2)] for _ in y]
            box = [(y[i] - dist[i][0], y[i] + dist[i][1]) for i in range(len(y))]
            tried += 1
            if removed(S, y, box, eps):
                rem += 1
                ratio = max(max(d) for d in dist) / r
                worst = max(worst, ratio)
                if ratio >= 1:
                    viol += 1
        if len(adv) < nadv:
            for i in range(len(y)):
                for side in (0, 1):
                    def box_of(d):
                        dist = [[1e-4 * r, 1e-4 * r] for _ in y]
                        dist[i][side] = d
                        return [(y[k] - dist[k][0], y[k] + dist[k][1]) for k in range(len(y))]
                    if not removed(S, y, box_of(1e-4 * r), eps):
                        continue
                    lo, hi = 1e-4 * r, 4 * r
                    if removed(S, y, box_of(hi), eps):
                        adv.append(np.inf)
                        continue
                    for _ in range(30):
                        mid = 0.5 * (lo + hi)
                        if removed(S, y, box_of(mid), eps):
                            lo = mid
                        else:
                            hi = mid
                    adv.append(lo / r)
    print(f'{name}: {usable} points satisfying the hypotheses (rho = {RHO}); '
          f'(A) {tried} random boxes, {rem} removals of y, {viol} with a face beyond r; '
          f'max farthest-face/r over removals = {worst:.3f}')
    a = np.array(adv)
    print(f'    (B) adversarial single-face search, {len(a)} faces: largest removal distance / r: '
          f'max {a.max():.3f}, median {np.median(a):.3f}, min {a.min():.3f} (claim: < 1)')


if __name__ == '__main__':
    S = setup(I.cnd1())
    Dp, K0, rp, tp = constants(S, [1.0])
    print(f'cnd1 at s = 1: D0\' = {Dp:.4f}, K0 = {K0:.3f}, rho\' = {rp:.5f}, theta\' = {tp:.5f}')
    S = setup(I.linediag('exp'))
    for t in (0.2, 0.5, 1.0):
        Dp, K0, rp, tp = constants(S, [t + 1, t])
        print(f'linediag at t = {t}: D0\' = {Dp:.4f}, K0 = {K0:.2f}, rho\' = {rp:.5f}, theta\' = {tp:.2e}')
    run('cnd1', I.cnd1(), 60, 20, 60)
    run('linediag', I.linediag('exp'), 60, 20, 30)
