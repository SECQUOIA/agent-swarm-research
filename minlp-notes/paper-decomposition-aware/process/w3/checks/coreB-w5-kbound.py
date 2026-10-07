"""W5 coreB: check the numeric bound moved to Appendix A (Lemma lem:states).

1 + 2*ceil((4/theta) ln(5/4 + 4 sqrt(2m))) <= 10/theta * ceil(log2(m+2))
    for theta = 2^-mu, mu = 2..12, and m = 1..10^5 (direct check),
    and phi(1) < 16.3, phi(2) < 18.6, phi'(m) <= 4/m, d/dm 10 log2(m+2) >= 7.2/m.
"""
import math

def phi(m):
    return 0.75 + 8 * math.log(1.25 + 4 * math.sqrt(2 * m))

assert phi(1) < 16.3 <= 10 * math.ceil(math.log2(3)), phi(1)
assert phi(2) < 18.6 <= 10 * math.log2(4), phi(2)
bad = 0
for m in range(1, 100001):
    if m >= 2:
        dphi = 8 * (4 * math.sqrt(2) / (2 * math.sqrt(m))) / (1.25 + 4 * math.sqrt(2 * m))
        assert dphi <= 4 / m + 1e-15
        assert 10 / ((m + 2) * math.log(2)) >= 7.2 / m
    assert phi(m) <= 10 * math.ceil(math.log2(m + 2)) + 1e-12
    for mu in range(2, 13):
        th = 2.0 ** -mu
        lhs = 1 + 2 * math.ceil((4 / th) * math.log(1.25 + 4 * math.sqrt(2 * m)))
        rhs = 10 / th * math.ceil(math.log2(m + 2))
        if lhs > rhs:
            bad += 1
print("phi(1)=%.4f phi(2)=%.4f violations=%d" % (phi(1), phi(2), bad))
assert bad == 0
print("OK")
