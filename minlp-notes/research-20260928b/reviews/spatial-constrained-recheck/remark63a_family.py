"""Independent recheck of Remark 6.3a(ii) (single-scale characterization fails).

Instance: n = 1, X0 = F = [0,1], t = y - 1/2,
    f_K(t) = K^-2 (1 - cos(2 pi K t)) + K^-2 (1 - exp(-K^2 t^2)),
exact alphaBB f_B = f - alpha q_B with alpha = alpha' = 32, f* = 0.

Computes, for several K and eps:
  * min f'' (convexity requirement alpha >= -min f''/2);
  * N_opt(eps) exactly (up to floating point) by the greedy furthest-reach sweep.
    Greedy is optimal because LB is monotone under taking sub-intervals;
  * the single-scale covering number N_inf(E(eps), c sqrt(eps)) for c = 1/2, 1;
  * Phi_alpha(eps) = sup_eta N_inf(E(eta), 2 sqrt((eps+eta)/alpha)), over an eta grid;
  * |T_bis| (binary dyadic bisection, UBD = f*), and the Theorem 6.3 upper bound.
"""
import math
import sys
import numpy as np
from scipy.optimize import brentq

ALPHA = 32.0


def make(K):
    K = float(K)

    def f(t):
        return (1 - np.cos(2 * np.pi * K * t)) / K**2 + (1 - np.exp(-(K * t) ** 2)) / K**2

    def fp(t):
        return (2 * np.pi / K) * np.sin(2 * np.pi * K * t) + 2 * t * np.exp(-(K * t) ** 2)

    def fpp(t):
        u = K * t
        return 4 * np.pi**2 * np.cos(2 * np.pi * K * t) + (2 - 4 * u * u) * np.exp(-u * u)

    return f, fp, fpp


def lb_interval(f, fp, l, u, alpha=ALPHA):
    """LB([l,u]) = min_{t in [l,u]} f(t) - alpha (t-l)(u-t); objective is convex."""
    if u <= l:
        return float(f(l))
    g = lambda t: fp(t) - alpha * (u + l - 2 * t)  # derivative, increasing
    gl, gu = g(l), g(u)
    if gl >= 0:
        t = l
    elif gu <= 0:
        t = u
    else:
        t = brentq(g, l, u, xtol=1e-16, rtol=1e-15, maxiter=200)
    return float(f(t) - alpha * (t - l) * (u - t))


def greedy_nopt(f, fp, eps, lo=-0.5, hi=0.5, tol=1e-14):
    x = lo
    count = 0
    ends = [x]
    while x < hi:
        if lb_interval(f, fp, x, hi) >= -eps:
            count += 1
            ends.append(hi)
            break
        a, b = x, hi  # [x,a] valid, [x,b] invalid
        # initial a: tiny step is always valid for eps > 0 since f >= 0
        while b - a > tol:
            mid = 0.5 * (a + b)
            if lb_interval(f, fp, x, mid) >= -eps:
                a = mid
            else:
                b = mid
        if a <= x:
            raise RuntimeError("no progress")
        x = a
        count += 1
        ends.append(x)
        if count > 10**6:
            raise RuntimeError("too many")
    return count, ends


def sublevel_intervals(f, eta, K, lo=-0.5, hi=0.5, per_period=4000):
    """E(eta) = {t : f(t) <= eta} as a sorted list of closed intervals.

    Grid detection (per_period points per period 1/K, plus t = 0), then brentq
    refinement of every boundary crossing.
    """
    n = int(per_period * K) + 1
    t = np.union1d(np.linspace(lo, hi, n), np.array([0.0]))
    inside = (f(t) - eta) <= 0
    d = np.diff(inside.astype(np.int8))
    starts = list(np.nonzero(d == 1)[0] + 1)
    stops = list(np.nonzero(d == -1)[0])
    if inside[0]:
        starts = [0] + starts
    if inside[-1]:
        stops = stops + [len(t) - 1]
    g = lambda s: f(s) - eta
    ivs = []
    for i, j in zip(starts, stops):
        a = t[0] if i == 0 else brentq(g, t[i - 1], t[i], xtol=1e-16)
        b = t[-1] if j == len(t) - 1 else brentq(g, t[j], t[j + 1], xtol=1e-16)
        ivs.append((a, b))
    return ivs


def cover_count(ivs, delta):
    """Least number of closed intervals of length delta covering a sorted union of
    closed intervals (greedy: each new interval starts at the leftmost uncovered point)."""
    cnt = 0
    reach = -np.inf
    for a, b in ivs:
        if b <= reach:
            continue
        if a > reach:  # a is uncovered
            k = max(1, math.ceil((b - a) / delta - 1e-12))
            reach = a + k * delta
        else:
            k = math.ceil((b - reach) / delta - 1e-12)
            reach = reach + k * delta
        cnt += k
    return cnt


def check_partition(f, ends, eps, alpha=ALPHA, pts=4001):
    """Independent dense-grid evaluation of LB on each greedy interval."""
    worst = np.inf
    maxdiff = 0.0
    for l, u in zip(ends[:-1], ends[1:]):
        t = np.linspace(l, u, pts)
        g = f(t) - alpha * (t - l) * (u - t)
        worst = min(worst, g.min() + eps)
    return worst


def phi_alpha(f, K, eps, alpha=ALPHA, n_eta=160):
    fmax = float(np.max(f(np.linspace(-0.5, 0.5, 20001))))
    etas = np.geomspace(eps * 1e-3, fmax * 1.01, n_eta)
    best = 0
    best_eta = None
    psi_run = 0  # sup_{eta >= eps} psi(eta)
    for eta in etas:
        ivs = sublevel_intervals(f, eta, K)
        c = cover_count(ivs, 2 * math.sqrt((eps + eta) / alpha))
        if c > best:
            best, best_eta = c, eta
        if eta >= eps:
            psi = cover_count(ivs, 2 * math.sqrt(eta / alpha))
            psi_run = max(psi_run, psi)
    return best, best_eta, psi_run


def bisection_nodes(f, fp, eps, alpha=ALPHA):
    """Binary dyadic bisection of [-1/2,1/2], UBD = f* = 0; count processed nodes."""
    nodes = 0
    stack = [(-0.5, 0.5)]
    while stack:
        l, u = stack.pop()
        nodes += 1
        if lb_interval(f, fp, l, u, alpha) >= -eps:
            continue
        m = 0.5 * (l + u)
        stack.append((l, m))
        stack.append((m, u))
        if nodes > 5 * 10**6:
            raise RuntimeError("bisection too large")
    return nodes


def main():
    print("Remark 6.3a(ii) recheck, alpha = alpha' = 32, n = 1")
    print()
    # convexity requirement
    print("min f'' (grid of 2e6 points) vs termwise bound -4 pi^2 - 4 e^(-3/2) and the note's bound -4 pi^2 - 2")
    for K in [1, 2, 5, 16, 64, 256]:
        f, fp, fpp = make(K)
        t = np.linspace(-0.5, 0.5, 2_000_001)
        print(f"  K={K:4d}: min f'' = {fpp(t).min():.6f}; -4pi^2-4e^-1.5 = {-4*np.pi**2-4*math.exp(-1.5):.6f};"
              f" -4pi^2-2 = {-4*np.pi**2-2:.6f}; required alpha >= {-fpp(t).min()/2:.4f}")
    print("  (the second derivative of 1 - exp(-u^2) in u is (2-4u^2)e^(-u^2) >= -4e^(-3/2) = -0.8925)")
    print()
    # growth claims
    print("growth claims: m >= 8 t^2 on |t| <= 1/(2K); m >= 0.22 K^-2 on |t| >= 1/(2K)")
    for K in [2, 5, 16, 64, 256]:
        f, fp, fpp = make(K)
        t = np.linspace(-0.5, 0.5, 4_000_001)
        inner = np.abs(t) <= 1 / (2 * K)
        tt = t[inner & (t != 0)]
        r1 = np.min(f(tt) / (8 * tt**2))
        r2 = np.min(f(t[~inner])) * K**2
        print(f"  K={K:4d}: min m/(8t^2) inner = {r1:.6f} (>= 1 claimed); min K^2 m outer = {r2:.6f} (>= {1-math.exp(-0.25):.6f})")
    print()

    header = ("K", "eps*K^2", "N_opt", "(K-1)/2", "Nsingle(c=.5)", "Nsingle(c=1)",
              "Phi", "sup_{eta>=eps}psi", "|T_bis|", "Thm6.3 UB", "N_opt/(log(1/eps)*Ns(c=1))")
    print(" | ".join(header))
    Ks = [int(a) for a in sys.argv[1:]] or [4, 8, 16, 32, 64, 128, 256]
    rows = []
    for K in Ks:
        f, fp, fpp = make(K)
        for ek in [0.2, 0.02, 0.002]:
            eps = ek / K**2
            nopt, ends = greedy_nopt(f, fp, eps)
            # robustness: perturb eps slightly
            n_lo, _ = greedy_nopt(f, fp, eps * (1 - 1e-7))
            n_hi, _ = greedy_nopt(f, fp, eps * (1 + 1e-7))
            slack = check_partition(f, ends, eps)
            assert slack >= -1e-12 * eps, ("greedy interval invalid on grid", slack)
            ivs = sublevel_intervals(f, eps, K)
            ns5 = cover_count(ivs, 0.5 * math.sqrt(eps))
            ns1 = cover_count(ivs, 1.0 * math.sqrt(eps))
            Phi, eta_star, psirun = phi_alpha(f, K, eps)
            tb = bisection_nodes(f, fp, eps) if K <= 128 else -1
            Lam = 8.0  # tau = alpha' n/4, kappa = 0
            J = max(0, math.ceil(math.log2(math.sqrt(Lam / eps))))
            ub = 1 + 2 * (1 + 15 * max(1, math.ceil(2 * math.sqrt(Lam / ALPHA))) * J * Phi)
            ratio = nopt / (math.log(1 / eps) * ns1)
            flag = "" if n_lo == nopt == n_hi else f" (eps-perturbed: {n_lo},{n_hi})"
            print(f"{K} | {ek} | {nopt}{flag} | {(K-1)/2:.1f} | {ns5} | {ns1} | {Phi} (eta*={eta_star*K**2:.3g}/K^2) | {psirun} | {tb} | {ub} | {ratio:.3f}")
            # consistency checks
            assert nopt >= (K - 1) / 2 or ek > 0.2
            assert Phi / 2 <= nopt + 1e-9, "Theorem 4.6 lower bound violated?"
            if tb > 0:
                assert nopt <= tb <= ub
    print()
    print("fixed K, eps -> 0: N_opt grows only additively (single-scale bound holds with a K-dependent constant)")
    for K in [8, 32]:
        f, fp, fpp = make(K)
        out = []
        for eps in [1e-4, 1e-6, 1e-8, 1e-10, 1e-12]:
            if eps > 0.2 / K**2:
                continue
            nopt, _ = greedy_nopt(f, fp, eps)
            ns1 = cover_count(sublevel_intervals(f, eps, K), math.sqrt(eps))
            out.append(f"eps={eps:.0e}: N_opt={nopt}, Nsingle(c=1)={ns1}")
        print(f"  K={K}: " + "; ".join(out))
    print()
    print("checks asserted on every row: greedy intervals valid on a 4001-point grid;"
          " N_opt >= Phi/2 (Thm 4.6 / 6.3 lower bound); N_opt <= |T_bis| <= Thm 6.3 UB (K <= 128)")


if __name__ == "__main__":
    main()
