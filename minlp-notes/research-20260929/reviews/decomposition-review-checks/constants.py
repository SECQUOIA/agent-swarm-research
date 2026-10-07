"""Referee checks of the constants in decomposition-certificates.md (Sections 2.1, 4, 5.4).

Independent of the note's scripts: scipy quadrature in log variables instead of mpmath.
Path family F_n = sum (x_i^2 - kappa x_i^4) + b sum x_i x_{i+1} on [-1,1]^n, b = 0.8, kappa = 0.1.
"""
import math
import numpy as np
from scipy import integrate, optimize, special

B, KAPPA = 0.8, 0.1


def log_detH(n, b):
    # tridiag(b, 2, b): D_k = 2 D_{k-1} - b^2 D_{k-2}; work with ratios to avoid overflow
    lg, r_prev, r = 0.0, None, 2.0          # r = D_k / D_{k-1}
    lg = math.log(2.0)
    for _ in range(2, n + 1):
        r_new = 2.0 - b * b / r
        lg += math.log(r_new)
        r = r_new
    return lg


def log_Jn(n, T):
    # J_n(T) = int_0^T t^{n-1} (1+t^2)^{-n/2} dt = int_{-inf}^{log T} exp(n u - (n/2) log(1+e^{2u})) du
    f = lambda u: math.exp(n * u - 0.5 * n * math.log1p(math.exp(2 * u)))
    lo = min(-40.0 / n, math.log(T) - 60)
    val, _ = integrate.quad(f, lo, math.log(T), limit=400, epsabs=0, epsrel=1e-11)
    return math.log(val)


def log_L(n, eps, logprod_alpha, lam_min, b=B):
    R2 = lam_min / 2.0
    T = math.sqrt(R2 / eps)
    return (math.log(2) + 0.5 * n * math.log(2 * n / math.pi) + 0.5 * (logprod_alpha - log_detH(n, b))
            - special.gammaln(n / 2) + log_Jn(n, T))


def lam_min_H(n, b=B):
    return 2 - 2 * abs(b) * math.cos(math.pi / (n + 1))


def weights_from_factor_alphas(fa):
    """per-variable weights alpha_j = sum of alpha of factors (i, i+1) containing j"""
    n = len(fa) + 1
    w = np.zeros(n)
    w[:-1] += fa
    w[1:] += fa
    return w


def lmin2(p, q, b=B):
    return (p + q) / 2 - math.sqrt(((p - q) / 2) ** 2 + b * b)


def main():
    print("# 1. Corollary 2.1 closed-form constant")
    c0 = 2 * math.sqrt(3 / 16) / math.sqrt(4 * math.pi) * math.exp(-0.5) / 2
    print("   2 sqrt(3/16) (4pi)^-1/2 e^-1/2 / 2 = %.5f ; times e^{-1/12} = %.5f (note: 0.0741, 0.068)" % (c0, c0 * math.exp(-1 / 12)))
    print("   (2e/pi)^(1/2) = %.5f ; pi/(4e) = %.5f" % (math.sqrt(2 * math.e / math.pi), math.pi / (4 * math.e)))
    thr = optimize.brentq(lambda bb: bb / (1 + math.sqrt(1 - bb * bb)) - math.pi / (4 * math.e), 0.1, 0.99)
    print("   growth threshold |b| = %.5f (note 0.53334)" % thr)
    print("   det H <= (4/3) 1.6^n check (n=10,40): ", [round(math.exp(log_detH(n, B)) / (4 / 3 * 1.6 ** n), 6) for n in (10, 40)])

    print("# 2. Exact integral bound L_n(eps), note's split (alpha_j = |b| interior, |b|/2 ends)")
    fa_note = np.full(1, 0.0)
    for eps in (1e-4, 1e-6, 1e-8):
        row = []
        for n in (4, 10, 20, 40, 60, 80):
            fa = np.full(n - 1, abs(B) / 2)
            lp = float(np.sum(np.log(weights_from_factor_alphas(fa))))
            row.append("n=%d:%.3e" % (n, math.exp(log_L(n, eps, lp, lam_min_H(n)))))
        print("   eps=%.0e " % eps + " ".join(row))
    print("   closed form at eps = 0.2/n is 0 (log 1 = 0); exact L_n(0.2/n):",
          " ".join("n=%d:%.3e" % (n, math.exp(log_L(n, 0.2 / n, float(np.sum(np.log(weights_from_factor_alphas(np.full(n - 1, 0.4))))), lam_min_H(n)))) for n in (10, 40)))

    print("# 3. Theorem 4.1(b) constants")
    Ma, w, k, cg, ap, A, K1, Dl = 2.8, 1, 2, 1 - KAPPA - B, 0.4, 2, 1, 1
    Q = Ma ** 2 * w * k / cg + Ma * w / 2 + ap * A
    th = math.sqrt(cg / 2 / (k * (48 * K1 * (1 + Dl) * Q + ap * A)))
    Z = 768 * K1 * Q + 3 * ap * A
    print("   Q = %.2f, theta_max(T2) = %.3e (2^-10 = %.3e), Z = 768Q+3a'A = %.4e, 4Z = %.4e, 2*4096^2 = %.4e"
          % (Q, th, 2 ** -10, Z, 4 * Z, 2 * 4096 ** 2))
    # M_a: spectral norm of [[p, b],[b, 0]] and [[p, b],[b, q]], p,q in [0.8, 2]
    Hn = max(max(abs(e) for e in np.linalg.eigvalsh(np.array([[p, B], [B, q]]))) for p in np.linspace(0.8, 2, 13) for q in [0.0] + list(np.linspace(0.8, 2, 13)))
    print("   max spectral norm of bag Hessians = %.4f (note M_a = 2.8)" % Hn)
    c_c = abs(B) / math.pi ** 2 * 2 * math.pi / math.sqrt(4 - B * B)
    print("   (c) constant (|b|/pi^2)(2pi/sqrt(4-b^2)) = %.5f (note 0.2778); R^2 = (2-|b|)/2 = %.2f" % (c_c, (2 - B) / 2))

    print("# 4. Factorization dependence: Corollary 2.1 base sqrt(4e/pi * alpha_geo/lambda_geo), lambda_geo = 1.6")
    lg = 1 + math.sqrt(1 - B * B)
    def base(ag):
        return math.sqrt(4 * math.e / math.pi * ag / lg)
    a_note = abs(B) / 2
    a_prog_root = -lmin2(2 - 12 * KAPPA, 0.0) / 2         # [[g''min, b],[b, 0]], g''min = 0.8 on [-1,1]
    a_prog_x0 = -lmin2(2.0, 0.0) / 2                       # g'' = 2 near 0
    a_bal_root = max(0.0, -lmin2((2 - 12 * KAPPA) / 2, (2 - 12 * KAPPA) / 2) / 2)
    a_bal_x0 = max(0.0, -lmin2(1.0, 1.0) / 2)
    for name, a in [("note: bilinear alone, alphaBB", a_note), ("PROGRAM split g_i+bx_ix_{i+1}, root-box alpha", a_prog_root),
                    ("PROGRAM split, alpha on boxes near x*=0", a_prog_x0), ("balanced split g_i/2+g_{i+1}/2+b.., root-box alpha", a_bal_root),
                    ("balanced split, alpha on boxes near x*=0", a_bal_x0)]:
        print("   %-52s alpha_c = %.4f, interior weight %.4f, base %s" % (name, a, 2 * a, "%.4f" % base(2 * a) if a > 0 else "none (gap 0)"))
    r_cvx = math.sqrt((1 - B) / (6 * KAPPA))
    print("   balanced interior factor convex on |x|_inf <= sqrt((1-b)/(6 kappa)) = %.4f" % r_cvx)
    # exact finite-n L_n for the balanced split with root-box alpha (end factors carry the whole g_1, g_n)
    for n in (10, 40, 80):
        fa = np.full(n - 1, a_bal_root)
        a_end = max(0.0, -lmin2(2 - 12 * KAPPA, (2 - 12 * KAPPA) / 2) / 2)
        fa[0] = fa[-1] = a_end
        lp = float(np.sum(np.log(weights_from_factor_alphas(fa))))
        print("   balanced root-alpha L_n(1e-6), n=%d: %.3e   (note split: %.3e)" % (
            n, math.exp(log_L(n, 1e-6, lp, lam_min_H(n))),
            math.exp(log_L(n, 1e-6, float(np.sum(np.log(weights_from_factor_alphas(np.full(n - 1, 0.4))))), lam_min_H(n)))))

    print("# 5. Face-exact Theorem 1 applied to the note's relaxation")
    rng = np.random.default_rng(1)
    worst = np.inf
    for _ in range(200000):
        l = rng.uniform(-1, 1, 2); u = rng.uniform(-1, 1, 2); l, u = np.minimum(l, u), np.maximum(l, u)
        y = rng.uniform(l, u)
        a = (y - l) * (u - y); d = np.minimum(y - l, u - y)
        worst = min(worst, (abs(B) / 2) * a.sum() - abs(B) * d[0] * d[1])
    print("   min over 2e5 random boxes/points of alphaBB gap - b d_i d_{i+1} = %.3e (>= 0 means (M_b) holds)" % worst)
    S = math.sqrt(1 + 2 / (2 * B)); lam = (1 + S) / (2 * S * S)
    fe = lambda n, eps: (1 + 1 / S) ** n * math.exp(-lam * (1 + eps / B))
    print("   S = %.4f, base 1+1/S = %.4f, lambda = %.4f; bound at n=20,40: %.3e, %.3e (eps=1e-6)" % (S, 1 + 1 / S, lam, fe(20, 1e-6), fe(40, 1e-6)))
    # crossover with computed certificate sizes (note Section 5.4: size/(n-1) at the h reaching eps)
    per_bag = {1e-4: 27937.0, 1e-6: 37248.0, 1e-8: 46551.0}
    for eps, pb in per_bag.items():
        n_fe = next(n for n in range(3, 400) if fe(n, eps) >= pb * (n - 1))
        n_c = next(n for n in range(3, 400) if math.exp(log_L(n, eps, float(np.sum(np.log(weights_from_factor_alphas(np.full(n - 1, 0.4))))), lam_min_H(n))) >= pb * (n - 1))
        print("   eps=%.0e: computed certificate ~%.0f (n-1); first n where the bound exceeds it: Cor 2.1 exact n=%d, face-exact Thm 1 n=%d" % (eps, pb, n_c, n_fe))
    # counting convex programs: pairs/leaves = 4.47 at theta = 1/16, h = 2^-12 (pairs_theta16.log)
    pb = 37248.0 * 4.47
    n_fe = next(n for n in range(3, 400) if fe(n, 1e-6) >= pb * (n - 1))
    n_c = next(n for n in range(3, 400) if math.exp(log_L(n, 1e-6, float(np.sum(np.log(weights_from_factor_alphas(np.full(n - 1, 0.4))))), lam_min_H(n))) >= pb * (n - 1))
    print("   eps=1e-06, counting (leaf, cell) convex programs (x4.47): Cor 2.1 exact n=%d, face-exact Thm 1 n=%d" % (n_c, n_fe))

    print("# 6. Proven versus proven: Theorem 4.1(b) upper bound against the single-tree lower bounds")
    dec = lambda n, eps: 3.36e7 * (n - 1) * (0.5 * math.log2(1.96e6 * (n - 1) / eps) + 2)
    for eps in (1e-4, 1e-6, 1e-8):
        n_cf = next(n for n in range(3, 1000) if 0.2 / (n * eps) > 1 and 0.068 * math.sqrt(n) * (2 * math.e / math.pi) ** (n / 2) * math.log(0.2 / (n * eps)) >= dec(n, eps))
        n_fe = next(n for n in range(3, 1000) if fe(n, eps) >= dec(n, eps))
        print("   eps=%.0e: closed form (Cor 2.1) exceeds (b) from n=%d; face-exact Thm 1 exceeds (b) from n=%d" % (eps, n_cf, n_fe))


if __name__ == "__main__":
    main()
