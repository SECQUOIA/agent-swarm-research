"""Confirmation check (independent of adaptive/check_phi_loss.py) for Proposition B.6 of
extension-adaptive.md.

1. Recompute, from the formulas stated in the note, the numbers quoted after Proposition B.6
   (staircase and flat bag, alpha = 1, K = 1024) and the review's loss/4^(d+2) values.
2. Check the elementary inequalities used in the proof, for d = 1..400:
     Gamma(d/2+1) >= (d/(2e))^{d/2};
     (4 pi d)^{d/2}/Gamma(d/2+1) <= (8 pi e)^{d/2};
     4 (8 pi d)^{d/2}/Gamma(d/2+1) <= 4 (16 pi e)^{d/2};
     8 (64 pi d eps)^{d/2}/Gamma(d/2+1) <= 8 (128 pi e)^{d/2} for eps <= 1/2.
3. Scan (alpha, eps, K, d) and compare the exact ratio
     [size bound of Theorem B.2(b)] / [K 2^{-(d+2)} max(1, (alpha/eps)^{d/2}/V_d)]
   with the displayed constant 4 (16 pi e)^{d/2} + 8 L (128 pi e)^{d/2} + 3 2^{d+2},
   L = log2(1/h0) + 2. The shell count uses Lemma 3.1 of [D] exactly:
   (J+1)(4/theta)^d with J = max(0, ceil(log2(1/h0))).
All in logarithms; floating point.
"""
import math
from scipy.special import gammaln

LOG2 = math.log(2.0)


def logVd(d):
    return 0.5 * d * math.log(math.pi) - gammaln(d / 2 + 1)


def lse(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def theta_of(alpha, d):
    # largest power of 1/2 with theta <= min(1, 2/sqrt(alpha d))
    t = 1.0
    while t > min(1.0, 2.0 / math.sqrt(alpha * d)):
        t /= 2
    return t


def stair_size_log(K, d, alpha, eps, lemma31=True):
    h0 = math.sqrt(2 * eps / (K * d * alpha ** 2))
    th = theta_of(alpha, d)
    if lemma31:
        J = max(0, math.ceil(math.log2(1 / h0)))
        levels = J + 1
    else:
        levels = math.log2(1 / h0) + 2        # as written in Theorem B.2(b)
    G = math.ceil(math.sqrt(alpha * d / (2 * eps)))
    parts = [d * math.log(G), 0.0]
    if levels > 0:
        parts.append(math.log(2 * levels) + d * math.log(4 / th))
    per_bag = lse(parts)
    return lse([math.log(K) + per_bag, math.log(2 * (K - 1))]), h0, levels


def main():
    alpha, K = 1.0, 1024
    print("== 1. numbers quoted after Proposition B.6 ==")
    for eps in (1e-2, 1e-6):
        print("staircase eps=%g" % eps)
        for d in (4, 12, 16, 24, 32, 64):
            lbN = math.log(K) + 0.5 * d * math.log(alpha / eps) - logVd(d)
            ubPhi = math.log(K) - (d + 2) * LOG2 + math.log(math.ceil(math.sqrt(alpha / (4 * eps))) ** d + 3)
            loss = lbN - ubPhi
            sz, _, _ = stair_size_log(K, d, alpha, eps)
            lbPhi2 = math.log(K) - (d + 2) * LOG2 + max(0.0, 0.5 * d * math.log(alpha / eps) - logVd(d))
            print("  d=%2d loss^(1/(d+2))=%.3f loss/4^(d+2)=%.3g  (N/Phi_2 upper)^(1/(d+2))=%.3f" % (
                d, math.exp(loss / (d + 2)), math.exp(loss - (d + 2) * math.log(4)),
                math.exp((sz - lbPhi2) / (d + 2))))
    for eps in (1e-6,):
        print("flat bag eps=%g" % eps)
        for d in (4, 16, 32, 64):
            lbN = 0.5 * d * math.log(alpha / eps) - logVd(d)
            ubPhi = -d * LOG2 + d * math.log(math.ceil(math.sqrt(alpha / (4 * eps))))
            ubN = d * math.log(math.ceil(math.sqrt(alpha * d / (4 * eps))))
            lbPhi2 = -d * LOG2 + max(0.0, lbN)
            print("  d=%2d loss^(1/d)=%.3f (N/Phi_2 upper)^(1/d)=%.3f" % (
                d, math.exp((lbN - ubPhi) / d), math.exp((ubN - lbPhi2) / d)))

    print("== 2. elementary inequalities, d = 1..400 ==")
    worst = [-1e9] * 4
    for d in range(1, 401):
        g = gammaln(d / 2 + 1)
        worst[0] = max(worst[0], 0.5 * d * math.log(d / (2 * math.e)) - g)
        worst[1] = max(worst[1], 0.5 * d * math.log(4 * math.pi * d) - g - 0.5 * d * math.log(8 * math.pi * math.e))
        worst[2] = max(worst[2], 0.5 * d * math.log(8 * math.pi * d) - g - 0.5 * d * math.log(16 * math.pi * math.e))
        worst[3] = max(worst[3], 0.5 * d * math.log(64 * math.pi * d * 0.5) - g - 0.5 * d * math.log(128 * math.pi * math.e))
    print("  max over d of log(lhs/rhs) (must be <= 0):", ["%.3f" % w for w in worst])

    print("== 3. scan of the displayed constant in Proposition B.6(b) ==")
    bad = []
    n = 0
    for alpha in (1.0, 0.5, 0.25, 0.1, 0.03, 0.01, 1e-3):
        for eps in (0.5, 0.1, 1e-2, 1e-4, 1e-6):
            for K in (2, 4, 64, 1024):
                for d in (1, 2, 3, 4, 8, 16, 32, 64):
                    n += 1
                    sz, h0, levels = stair_size_log(K, d, alpha, eps, lemma31=True)
                    lbPhi2 = math.log(K) - (d + 2) * LOG2 + max(0.0, 0.5 * d * math.log(alpha / eps) - logVd(d))
                    ratio = sz - lbPhi2
                    L = math.log2(1 / h0) + 2
                    terms = [math.log(4) + 0.5 * d * math.log(16 * math.pi * math.e),
                             math.log(3) + (d + 2) * LOG2]
                    if L > 0:
                        terms.append(math.log(8 * L) + 0.5 * d * math.log(128 * math.pi * math.e))
                    const = lse(terms)
                    if ratio > const + 1e-9 or L < 1:
                        bad.append((alpha, eps, K, d, h0, L, levels, math.exp(ratio - const)))
    print("  cases:", n, " cases with L < 1 or ratio > displayed constant:", len(bad))
    for b in bad[:12]:
        print("   alpha=%g eps=%g K=%d d=%d h0=%.3g L=%.3f levels(Lemma 3.1)=%d ratio/const=%.3g" % b)
    viol = [b for b in bad if b[7] > 1]
    print("  of these, ratio exceeds the displayed constant in", len(viol), "cases")


if __name__ == "__main__":
    main()


def violations():
    """List the cases where the exact ratio exceeds the displayed constant, and re-test them with
    L replaced by J + 1 = max(0, ceil(log2(1/h0))) + 1 (the level count of Lemma 3.1 of [D])."""
    out = []
    for alpha in (1.0, 0.5, 0.25, 0.1, 0.03, 0.01, 1e-3):
        for eps in (0.5, 0.1, 1e-2, 1e-4, 1e-6):
            for K in (2, 4, 64, 1024):
                for d in (1, 2, 3, 4, 8, 16, 32, 64):
                    sz, h0, levels = stair_size_log(K, d, alpha, eps, lemma31=True)
                    lbPhi2 = math.log(K) - (d + 2) * LOG2 + max(0.0, 0.5 * d * math.log(alpha / eps) - logVd(d))
                    ratio = sz - lbPhi2
                    L = math.log2(1 / h0) + 2
                    base = [math.log(4) + 0.5 * d * math.log(16 * math.pi * math.e), math.log(3) + (d + 2) * LOG2]
                    disp = lse(base + ([math.log(8 * L) + 0.5 * d * math.log(128 * math.pi * math.e)] if L > 0 else []))
                    fixed = lse(base + [math.log(8 * levels) + 0.5 * d * math.log(128 * math.pi * math.e)])
                    if ratio > disp + 1e-9:
                        out.append((alpha, eps, K, d, h0, L, ratio - disp, ratio - fixed))
    print("== 4. violations of the displayed constant ==")
    print("  count:", len(out), "; all have h0 > 2:", all(o[4] > 2 for o in out),
          "; min alpha^2 K d/eps among them: %.3g" % min(o[0] ** 2 * o[2] * o[3] / o[1] for o in out))
    print("  largest log(ratio/displayed): %.3f ; with L -> J+1 (Lemma 3.1), largest log(ratio/const): %.3f"
          % (max(o[6] for o in out), max(o[7] for o in out)))


if __name__ == "__main__":
    violations()
