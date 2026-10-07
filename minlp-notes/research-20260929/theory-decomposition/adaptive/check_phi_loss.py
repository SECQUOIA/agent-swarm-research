"""Revision check for Proposition B.6 of extension-adaptive.md (added after review): the
sup-norm covering bound Phi loses a factor w^{Theta(w)}, and the Euclidean form Phi_2 does not,
on one flat bag and on the staircase family. All quantities are the closed-form bounds of the
proposition, evaluated in logarithms (no certificates are built here).

  python3 check_phi_loss.py

V_d = pi^{d/2}/Gamma(d/2+1) is the volume of the unit ball in R^d.
Flat bag (|T| = 1, F = 0 on [0,1]^d, relaxation -alpha q_B):
  N_dec >= (alpha/eps)^{d/2}/V_d                    (volume bound via Lemma 1.4)
  N_dec <= ceil(sqrt(alpha d/(4 eps)))^d            (uniform grid)
  sup Phi   <= 2^{-d} ceil(sqrt(alpha/(4 eps)))^d   (e = eps is admissible)
  sup Phi_2 >= 2^{-d} max(1, (alpha/eps)^{d/2}/V_d)
Staircase family (K bags, alpha <= 1, eps <= 1/2, P = alpha d/4 + 1):
  N_dec >= K (alpha/eps)^{d/2}/V_d
  N_dec <= K [ceil(sqrt(alpha d/(2 eps)))^d + 2 (J + 1)(4/theta)^d + 1] + 2 (K-1)   (Thm B.2(b)),
           J = max(0, ceil(log2(1/h0))) as in Lemma 3.1 of [D]
  sup Phi   <= K 2^{-(d+2)} (ceil(sqrt(alpha/(4 eps)))^d + 3)
  sup Phi   >= K 2^{-(d+2)} max(1, (alpha/(4 eps))^{d/2})
  sup Phi_2 >= K 2^{-(d+2)} max(1, (alpha/eps)^{d/2}/V_d)
Printed: lower bound on N_dec/sup Phi ("loss_Phi", which must grow like w^{Theta(w)}), and upper
bounds on N_dec/sup Phi and N_dec/sup Phi_2, also as per-dimension bases ratio^{1/(d+2)}.

Scan (added after the confirmation review): over a grid of (alpha, eps, K, d) with alpha <= 1,
eps <= 1/2, compare the upper bound on N_dec/sup Phi_2 (Thm B.2(b) size over K 2^{-(d+2)} M) with the
displayed constant of Proposition B.6(b), 4 (16 pi e)^{d/2} + 8 L (128 pi e)^{d/2} + 3 2^{d+2}, for
L = J + 1 (revised) and for L = log2(1/h0) + 2 (first revision; the term is dropped when L <= 0).
Also check L = J + 1 <= (1/2) log2(K d/(2 eps)) + 2.
"""
import math

LN2 = math.log(2.0)


def log_vd(d):
    return (d / 2) * math.log(math.pi) - math.lgamma(d / 2 + 1)


def log_ceil_pow(u, d):
    return d * math.log(math.ceil(u))


def logsumexp(*xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def flat(d, alpha, eps):
    lb_n = (d / 2) * math.log(alpha / eps) - log_vd(d)
    ub_n = log_ceil_pow(math.sqrt(alpha * d / (4 * eps)), d)
    ub_phi = -d * LN2 + log_ceil_pow(math.sqrt(alpha / (4 * eps)), d)
    lb_phi = -d * LN2 + max(0.0, (d / 2) * math.log(alpha / (4 * eps)))
    lb_phi2 = -d * LN2 + max(0.0, lb_n)
    return lb_n - ub_phi, ub_n - lb_phi, ub_n - lb_phi2


def shell_levels(d, alpha, eps, K):
    """h0 of Thm B.2(b) and the level count J + 1 of Lemma 3.1 of [D] (s0 = 1)."""
    h0 = math.sqrt(2 * eps / (K * d * alpha ** 2))
    return h0, max(0, math.ceil(math.log2(1 / h0))) + 1


def staircase_size(d, alpha, eps, K):
    """log of the size bound of Thm B.2(b)."""
    _, levels = shell_levels(d, alpha, eps, K)
    mu = max(0, math.ceil(math.log2(math.sqrt(alpha * d) / 2)))
    theta = 2.0 ** -mu
    per_bag = logsumexp(log_ceil_pow(math.sqrt(alpha * d / (2 * eps)), d),
                        math.log(2 * levels) + d * math.log(4 / theta), 0.0)
    return logsumexp(math.log(K) + per_bag, math.log(2 * (K - 1)))


def staircase(d, alpha, eps, K):
    lb_n = math.log(K) + (d / 2) * math.log(alpha / eps) - log_vd(d)
    ub_n = staircase_size(d, alpha, eps, K)
    ub_phi = math.log(K) - (d + 2) * LN2 + math.log(math.ceil(math.sqrt(alpha / (4 * eps))) ** d + 3.0)
    lb_phi = math.log(K) - (d + 2) * LN2 + max(0.0, (d / 2) * math.log(alpha / (4 * eps)))
    lb_phi2 = math.log(K) - (d + 2) * LN2 + max(0.0, (d / 2) * math.log(alpha / eps) - log_vd(d))
    return lb_n - ub_phi, ub_n - lb_phi, ub_n - lb_phi2


def main():
    alpha, K = 1.0, 1024
    ds = (1, 2, 4, 8, 12, 16, 24, 32, 48, 64)
    for eps in (1e-2, 1e-6):
        print("staircase, alpha=%.0f K=%d eps=%.0e; limit of loss_Phi as eps->0 is 4*4^d/V_d" % (alpha, K, eps))
        print("  d | loss_Phi (lower bd) | /4^(d+2) | limit    | base^(1/(d+2)) | /sqrt(d) || "
              "N/Phi upper: base | /sqrt(d) || N/Phi_2 upper: base")
        for d in ds:
            l1, u1, u2 = staircase(d, alpha, eps, K)
            lim = math.log(4.0) + d * math.log(4.0) - log_vd(d)
            b1, bu1, bu2 = (math.exp(x / (d + 2)) for x in (l1, u1, u2))
            print("%3d | %19.3e | %8.2e | %8.2e | %14.3f | %8.3f || %17.3f | %8.3f || %17.3f" % (
                d, math.exp(l1), math.exp(l1 - (d + 2) * math.log(4.0)), math.exp(lim), b1,
                b1 / math.sqrt(d), bu1, bu1 / math.sqrt(d), bu2))
    for eps in (1e-2, 1e-6):
        print("flat bag, alpha=%.0f eps=%.0e; limit of loss_Phi as eps->0 is 4^d/V_d" % (alpha, eps))
        print("  d | loss_Phi (lower bd) | limit    | base^(1/d) | /sqrt(d) || N/Phi upper: base || "
              "N/Phi_2 upper: base")
        for d in ds:
            l1, u1, u2 = flat(d, alpha, eps)
            lim = d * math.log(4.0) - log_vd(d)
            b1, bu1, bu2 = (math.exp(x / d) for x in (l1, u1, u2))
            print("%3d | %19.3e | %8.2e | %10.3f | %8.3f || %17.3f || %19.3f" % (
                d, math.exp(l1), math.exp(lim), b1, b1 / math.sqrt(d), bu1, bu2))
    scan()


def displayed_const(d, L):
    """log of 4 (16 pi e)^{d/2} + 8 L (128 pi e)^{d/2} + 3 2^{d+2} (L-term dropped if L <= 0)."""
    terms = [math.log(4.0) + (d / 2) * math.log(16 * math.pi * math.e), math.log(3.0) + (d + 2) * LN2]
    if L > 0:
        terms.append(math.log(8 * L) + (d / 2) * math.log(128 * math.pi * math.e))
    return logsumexp(*terms)


def scan():
    n = bad_new = bad_old = bad_L = 0
    worst_new, worst_old, hmin_old = -1e300, -1e300, math.inf
    for alpha in (1.0, 0.5, 0.25, 0.1, 0.03, 0.01, 1e-3, 1e-4):
        for eps in (0.5, 0.25, 0.1, 1e-2, 1e-4, 1e-6):
            for K in (2, 3, 4, 16, 64, 1024):
                for d in (1, 2, 3, 4, 6, 8, 12, 16, 32, 64):
                    n += 1
                    h0, levels = shell_levels(d, alpha, eps, K)
                    lb_phi2 = math.log(K) - (d + 2) * LN2 + max(0.0, (d / 2) * math.log(alpha / eps) - log_vd(d))
                    ratio = staircase_size(d, alpha, eps, K) - lb_phi2
                    r_new = ratio - displayed_const(d, levels)
                    r_old = ratio - displayed_const(d, math.log2(1 / h0) + 2)
                    worst_new, worst_old = max(worst_new, r_new), max(worst_old, r_old)
                    bad_new += r_new > 1e-12
                    if r_old > 1e-12:
                        bad_old += 1
                        hmin_old = min(hmin_old, h0)
                    bad_L += levels > 0.5 * math.log2(K * d / (2 * eps)) + 2 + 1e-12
    print("scan of Proposition B.6(b), %d cases (alpha 1..1e-4, eps 0.5..1e-6, K 2..1024, d 1..64):" % n)
    print("  L = J + 1:          bound exceeds displayed constant in %d cases; max ratio/const = %.3f" % (
        bad_new, math.exp(worst_new)))
    print("  L = log2(1/h0) + 2: bound exceeds displayed constant in %d cases; max ratio/const = %.3f; "
          "smallest h0 among them = %.3g" % (bad_old, math.exp(worst_old), hmin_old))
    print("  cases with J + 1 > (1/2) log2(K d/(2 eps)) + 2: %d" % bad_L)


if __name__ == "__main__":
    main()
