"""Lower bounds on single-tree certificate sizes for the path family (face-exact-exponential.md).

Family:  f(x) = sum_i (x_i^2 - kappa x_i^4 + c_i x_i) + b sum_{i<n} x_i x_{i+1}  on [-1,1]^n.
Constants used by the bounds: D = sup g_i'' = 2, coupling b, cube radius r around x*.

Bounds evaluated (all are floating-point evaluations of closed forms or 1-D quadratures):
  T1   Theorem 1 (termwise McCormick, center-volume):  exp(-lam (1 + eps/(b r^2))) * theta^-n
  T1L  Theorem 1, general Lagrangian form (numerically minimised over mu)
  T1E  Theorem 2 (per-factor convex envelopes), Lagrangian over (sigma, mu)
  ABBV per-factor alphaBB, same center-volume argument (Proposition 5.1)
  ABBI per-factor alphaBB, repository Theorem 3.1 (anisotropic integral bound)
  SL   matching-slice bound (face-exact note, Theorem 3.4), has a log(1/eps) factor
Usage: python3 bounds.py
"""
import math
import numpy as np
from scipy import integrate, optimize


def closed_form(D, b):
    rho = D / (2 * b)
    S = math.sqrt(1 + rho)
    theta = S / (1 + S)
    lam = (1 + S) / (2 * S * S)
    ok = (S <= 2) and (lam >= math.log(1 + 1 / S))
    return rho, S, theta, lam, ok


def smax():
    """Largest S with (1+S)/(2S^2) >= log(1+1/S) (condition of Corollary 1)."""
    F = lambda S: (1 + S) / (2 * S * S) - math.log(1 + 1 / S)
    return optimize.brentq(F, 1.5, 2.0, xtol=1e-14)


def upper_max(k, lo=0.0, hi=1.0, N=400001):
    """Upper bound for max_{s in [lo, hi)} k(s): dense grid + Lipschitz slack on [lo, 1-delta],
    where the tail [1-delta, 1) is handled by the caller's choice of k (it tends to -inf)."""
    s = np.linspace(lo, hi, N, endpoint=False)
    v = k(s)
    i = int(np.argmax(v))
    # local refinement (the grid max is within one step of a local max)
    a, c = s[max(i - 1, 0)], s[min(i + 1, N - 1)]
    res = optimize.minimize_scalar(lambda t: -k(np.array([t]))[0], bounds=(a, c), method="bounded",
                                   options={"xatol": 1e-13})
    return max(v[i], -res.fun)


SG = np.linspace(0.0, 1.0, 10001, endpoint=False)      # coarse grid used only to choose multipliers
_CACHE = {}


def psi_table(kfun, mus, key=None):
    """max over the coarse s-grid of kfun(s, mu), vectorised over mu (used to pick mu); cached by key."""
    if key is not None and key in _CACHE:
        return _CACHE[key]
    out = np.empty(len(mus))
    for j in range(0, len(mus), 200):
        out[j:j + 200] = np.max(kfun(SG[None, :], mus[j:j + 200, None]), axis=1)
    if key is not None:
        _CACHE[key] = out
    return out


def k_mc(D, b):
    rho = D / (2 * b)
    return lambda s, mu: np.log1p(-s) + mu * (rho * s * s + 2 * s - 1)


def best_mc(D, b, n, epsp, mus=np.linspace(1e-3, 5, 1000)):
    """Theorem 1, Lagrangian form: log volume fraction <= n Psi(mu) + mu (1 + eps'/b)."""
    kf = k_mc(D, b)
    tab = n * psi_table(kf, mus, ('mc', D, b)) + mus * (1 + epsp / b)
    mu = mus[int(np.argmin(tab))]
    val = n * upper_max(lambda s: kf(s, mu)) + mu * (1 + epsp / b)
    return val, mu


def k_env(D, b, sigma):
    phi = lambda s: 2 * b * sigma * s + (b * (1 - sigma) + D / 2) * s * s + (D * sigma * sigma / 2) * (1 - s) ** 2
    return lambda s, mu: np.log1p(-s) + mu * (phi(s) - b * sigma)


def best_env(D, b, n, epsp, sigmas=np.linspace(0.05, 1.0, 39), mus=np.linspace(1e-3, 10, 1000)):
    """Theorem 2 (per-factor envelopes): log fraction <= n Psi(sigma, mu) + mu (b sigma + eps')."""
    best = (math.inf, None, None)
    for sg in sigmas:
        tab = n * psi_table(k_env(D, b, sg), mus, ('env', D, b, sg)) + mus * (b * sg + epsp)
        i = int(np.argmin(tab))
        if tab[i] < best[0]:
            best = (tab[i], sg, mus[i])
    _, sg, mu = best
    kf = k_env(D, b, sg)
    val = n * upper_max(lambda s: kf(s, mu)) + mu * (b * sg + epsp)
    return val, sg, mu


def k_abb(D, b, a):
    K = D / 2 + b
    return lambda s, mu: np.log1p(-s) + mu * (K * s * s - a * (1 - s) ** 2)


def best_abb(D, b, alphas, epsp, mus=np.linspace(1e-3, 30, 1500)):
    """alphaBB center-volume: sum_i alpha_i (1-s_i)^2 <= (D/2+b) sum s_i^2 + eps'."""
    vals = sorted(set(alphas))
    cnt = {a: alphas.count(a) for a in vals}
    tab = mus * epsp
    for a in vals:
        tab = tab + cnt[a] * psi_table(k_abb(D, b, a), mus, ('abb', D, b, a))
    mu = mus[int(np.argmin(tab))]
    val = mu * epsp + sum(cnt[a] * upper_max(lambda s, a=a: k_abb(D, b, a)(s, mu)) for a in vals)
    return val, mu


def radial(k, R, eps):
    """int_0^R rho^(k-1) (rho^2/2 + eps)^(-k/2) d rho, computed in log-space variable."""
    f = lambda t: math.exp(k * t) * (math.exp(2 * t) / 2 + eps) ** (-k / 2)   # rho = e^t, d rho = rho dt
    lo = math.log(R) - 60
    val, err = integrate.quad(f, lo, math.log(R), limit=500, epsabs=0, epsrel=1e-10)
    return val


def sphere_area(k):
    return 2 * math.pi ** (k / 2) / math.gamma(k / 2)


def path_adj(k):
    A = np.zeros((k, k))
    for i in range(k - 1):
        A[i, i + 1] = A[i + 1, i] = 1
    return A


def slice_bound(D, b, n, eps, r):
    """face-exact Theorem 3.4 with the matching (1,2),(3,4),...; integral restricted to the ellipsoid
    {t' M t <= lam_min(M) r^2}, which lies in the cube [-r,r]^k."""
    k = n // 2
    M = 2 * (D - b) * np.eye(k) - b * path_adj(k)
    ev = np.linalg.eigvalsh(M)
    I = radial(k, r * math.sqrt(ev[0]), eps) * sphere_area(k) / math.sqrt(np.prod(ev))
    return (k * b / math.pi ** 2) ** (k / 2) * I


def abb_integral_bound(D, b, alphas, eps, r):
    """Repository Theorem 3.1, anisotropic form: |P| >= (n/pi^2)^(n/2) prod alpha_i^(1/2) int (m+eps)^(-n/2),
    with m <= y'Hy/2, H = D I + b A, integral restricted to {y'Hy <= lam_min(H) r^2}."""
    n = len(alphas)
    H = D * np.eye(n) + b * path_adj(n)
    ev = np.linalg.eigvalsh(H)
    I = radial(n, r * math.sqrt(ev[0]), eps) * sphere_area(n) / math.sqrt(np.prod(ev))
    return (n / math.pi ** 2) ** (n / 2) * math.prod(math.sqrt(a) for a in alphas) * I


def main():
    D, b, eps, r = 2.0, 0.8, 1e-4, 1.0
    rho, S, theta, lam, ok = closed_form(D, b)
    print(f"S_max = {smax():.6f}, rho_max = {smax()**2 - 1:.6f}")
    print(f"D={D} b={b}: rho={rho} S={S} theta={theta:.6f} 1/theta={1/theta:.6f} lam={lam:.6f} "
          f"closed-form condition holds: {ok}")
    # per-factor alphaBB constant: smallest alpha valid on every box (bilinear part with h''<=2)
    af = (math.sqrt(D * D + 4 * b * b) - D) / 4
    af_root = (math.sqrt(0.8 ** 2 + 4 * b * b) - 0.8) / 4      # kappa = 0.1 root box, h'' >= 0.8
    print(f"per-factor alphaBB: alpha_f >= {af:.6f} on every box (root-box value for kappa=0.1: {af_root:.6f})")
    # asymptotic bases
    eb = best_env(D, b, 200, 0.0)
    print(f"asymptotic base per variable: McCormick T1 {1/theta:.4f}; envelope T1E "
          f"{math.exp(-eb[0]/200):.4f} (sigma={eb[1]:.3f}, mu={eb[2]:.3f})")
    ab = best_abb(D, b, [2 * af] * 200, 0.0)
    print(f"  alphaBB center-volume (alpha_eff = 2 alpha_f = {2*af:.4f}): {math.exp(-ab[0]/200):.4f}")
    Mlam = (D - b) + math.sqrt((D - b) ** 2 - b ** 2)
    Hlam = (D + math.sqrt(D * D - 4 * b * b)) / 2
    print(f"  slice (log-factor) base per variable: {(4*math.e*b/(math.pi*Mlam))**0.25:.4f} "
          f"(lambda_geo(M)={Mlam:.4f});  alphaBB Thm 3.1 base: {(4*math.e*2*af/(math.pi*Hlam))**0.5:.4f} "
          f"(lambda_geo(H)={Hlam:.4f})")
    print()
    print(f"eps={eps}, r={r}: lower bounds on the number of leaves")
    print(" n   T1(closed)   T1L(opt)   T1E(env)   ABBV      ABBI       SL(slice)")
    for n in range(2, 21):
        t1 = math.exp(-lam * (1 + eps / (b * r * r))) * theta ** (-n) if ok else float("nan")
        t1l = math.exp(-best_mc(D, b, n, eps / r ** 2)[0])
        t1e = math.exp(-best_env(D, b, n, eps / r ** 2)[0])
        alphas = [af] + [2 * af] * (n - 2) + [af]
        abv = math.exp(-best_abb(D, b, alphas, eps / r ** 2)[0])
        abi = abb_integral_bound(D, b, alphas, eps, r)
        sl = slice_bound(D, b, n, eps, r) if n >= 2 else float("nan")
        print(f"{n:2d} {t1:11.3f} {t1l:10.3f} {t1e:10.3f} {abv:9.3f} {abi:10.4g} {sl:10.4g}")
    print()
    print("eps dependence at n = 10 (r = 1):")
    for e in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8):
        t1 = math.exp(-lam * (1 + e / b)) * theta ** (-10)
        print(f"  eps={e:.0e}: T1={t1:.2f}  SL={slice_bound(D, b, 10, e, 1.0):.3f}  "
              f"ABBI={abb_integral_bound(D, b, [af]+[2*af]*8+[af], e, 1.0):.4g}")


if __name__ == "__main__":
    main()


def upper_bisection(n, eps, b=0.8, kappa=0.1, secant=False):
    """Proposition 5.4: leaves of the uniform 2^n-ary dyadic tree on [-1,1]^n, c = 0, UBD = f*."""
    mu0 = 1 - kappa - b
    tau = b * (n - 1) / 4 + (1.5 * kappa * n if secant else 0.0)
    J = sum(1 for j in range(200) if tau * (2.0 ** (1 - j)) ** 2 > eps)
    Vn = math.pi ** (n / 2) / math.gamma(n / 2 + 1)
    per_level = Vn * (math.sqrt(tau / mu0) + math.sqrt(n)) ** n
    return 1 + (2 ** n - 1) * J * per_level, J, per_level


if __name__ == "__main__" and len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "upper":
    for n in range(2, 21, 2):
        ub, J, pl = upper_bisection(n, 1e-4)
        ub0, _, _ = upper_bisection(n, 1e-4, kappa=0.0)
        print(f"n={n:2d}: exact-g kappa=0.1: levels={J} per-level<={pl:.3g} leaves<={ub:.3g} "
              f"(per-variable {ub ** (1 / n):.1f});  kappa=0: leaves<={ub0:.3g} (per-variable {ub0 ** (1 / n):.1f})")
