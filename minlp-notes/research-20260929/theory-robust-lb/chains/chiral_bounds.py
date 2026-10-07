"""Lower-bound constants for the chiral chain (Section C.4 of robust-chains.md).

Windows of k consecutive variables separated by single variables pinned at x* = 0 (Lemma B.1); a
pinned window is the k-chain f_k itself.  For class P_D (D = 1: fixed balanced split; D = 2: class (a)):

  gamma_k(theta) = -(fooling value of the k-chain on K_theta = [-theta, theta]^k)  (primal LP family,
                   an S-consistent family, so V(K_theta) <= -gamma_k(theta));
  Lambda_j      = sum over the factors e containing j of max_{[-1,1]^2} |d_j f_e|  (exact polynomial max);
  analytic base (transport, Section 4.3(a) of the robust note): Phi(mu) <= exp(-mu gamma_k(1)) for
                   2 mu Lambda_j <= 1, base per variable exp(gamma_k(1) / (2 max_j Lambda_j (k+1)));
  computed base (cores + point masses, Section 4.3(b) of the robust note): with the separable bound
                   f_k(p) <= sum_j c_j p_j^2 on [-1,1]^k (c_j = a+b+g interior, a+(b+g)/2 at the ends),
                   Phi(mu) <= max{ e^{-mu gamma(1)}, max_i ((1+theta_{i+1})/2) e^{-mu max(gamma(theta_i),0)}, Psi(mu) },
                   Psi(mu) <= max_{j0} H'_{j0} prod_{j != j0} H_j,  H_j = max(1, sup_d ((1-d)/2) e^{mu c_j d^2}),
                   H'_j = max((1+theta_1)/2, sup_d ((1-d)/2) e^{mu c_j d^2});
  ceiling: mu0 = smallest mu at which a corner box B = prod_j [s_j, 1] or [-1, -s_j] (sign pattern sigma)
                   has (vol/2^k) e^{mu V(B)} >= 1, with V(B) >= the column-generation lower bound; the
                   tilted-volume base is then at most exp(mu0 gamma_k(1)) per window.
Usage: python3 chiral_bounds.py B G EV D k1 k2 ...
Floating point; the LP fooling values are not interval-certified.
"""
import sys
import json
import numpy as np
from numpy.polynomial import polynomial as P
from polychain import RelaxPoly, poly_class, min_bivar, _dx, _dy, add_x, add_y
from chiral import chain


def lambdas(ch):
    n = ch.n
    L = np.zeros(n)
    for e in range(n - 1):
        C = ch.factor(e)
        for j, D in ((e, _dx(C)), (e + 1, _dy(C))):
            mx = max(-min_bivar(D, -1, 1, -1, 1)[0], -min_bivar(-D, -1, 1, -1, 1)[0])
            L[j] += mx
    return L


def gamma_theta(ch, d, theta, maxit=200):
    n = ch.n
    rel = RelaxPoly(ch, poly_class(d), K=7)
    lo, up, _ = rel.bound(np.full(n, -theta), np.full(n, theta), None, maxit=maxit, tol=1e-10)
    return -up, -lo  # gap lower bound (from fooling family), gap upper bound (from split)


def sup_corner(mu, c, grid=np.linspace(0, 1, 2001)):
    return float(np.max((1 - grid[1:]) / 2 * np.exp(mu * c * grid[1:] ** 2)))


def computed_base(gam, thetas, cvec, mu):
    terms = [np.exp(-mu * gam[-1])]
    for i in range(len(thetas) - 1):
        terms.append((1 + thetas[i + 1]) / 2 * np.exp(-mu * max(gam[i], 0.0)))
    th1 = thetas[0]
    H = [max(1.0, sup_corner(mu, c)) for c in cvec]
    Hp = [max((1 + th1) / 2, sup_corner(mu, c)) for c in cvec]
    psi = max(Hp[j0] * np.prod([H[j] for j in range(len(cvec)) if j != j0]) for j0 in range(len(cvec)))
    terms.append(psi)
    return max(terms)


def corner_mu0(ch, d, k, gam1, rng, ntrial=60):
    """Smallest mu found at which some corner box has (vol/2^k) e^{mu V(B)} >= 1 (V from the dual bound)."""
    best = np.inf; bestbox = None
    rel = RelaxPoly(ch, poly_class(d), K=5)
    for t in range(ntrial):
        sig = rng.choice([-1.0, 1.0], size=k)
        s = rng.uniform(0.2, 0.95, size=k)
        l = np.where(sig > 0, s, -1.0); u = np.where(sig > 0, 1.0, -s)
        lo, up, _ = rel.bound(l, u, None, maxit=60, tol=1e-8)
        logvol = np.sum(np.log((u - l) / 2))
        if lo > 0:
            mu = -logvol / lo
            if mu < best:
                best, bestbox = mu, (l.round(3).tolist(), u.round(3).tolist(), lo)
    return best, bestbox


if __name__ == "__main__":
    b, g, ev = map(float, sys.argv[1:4]); d = int(sys.argv[4])
    a = b + ev
    rng = np.random.default_rng(0)
    thetas = np.round(np.arange(0.2, 1.0001, 0.05), 4)
    for k in map(int, sys.argv[5:]):
        ch = chain(k, b, g, ev)
        L = lambdas(ch)
        gam = []
        for th in thetas:
            glo, ghi = gamma_theta(ch, d, th)
            gam.append(glo)
        gam = np.array(gam)
        g1 = gam[-1]
        an = np.exp(g1 / (2 * L.max() * (k + 1)))
        cvec = np.array([a + (b + g) / 2] + [a + b + g] * (k - 2) + [a + (b + g) / 2])
        best = (np.inf, None)
        for mu in np.linspace(0.05, 4.0, 160):
            # use all cores with gamma >= 0 from the smallest theta upwards; also try dropping small cores
            for start in range(len(thetas) - 1):
                phi = computed_base(gam[start:], thetas[start:], cvec, mu)
                if phi < best[0]:
                    best = (phi, (round(mu, 3), float(thetas[start])))
        comp = best[0] ** (-1.0 / (k + 1))
        mu0, box = corner_mu0(ch, d, k, g1, rng)
        ceil = np.exp(mu0 * g1 / (k + 1)) if np.isfinite(mu0) else None
        print(json.dumps(dict(b=b, g=g, ev=ev, cls=f"P{d}", k=k, Lambda=L.round(4).tolist(), gamma_theta=dict(zip(thetas.tolist(), gam.round(5).tolist())),
                              analytic_base_per_var=round(float(an), 5), computed_Phi=round(float(best[0]), 5), computed_at=best[1],
                              computed_base_per_var=round(float(comp), 5), corner_mu0=round(float(mu0), 4), corner_box=box,
                              ceiling_per_var=None if ceil is None else round(float(ceil), 5))), flush=True)
