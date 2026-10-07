"""M4: exact checks for the overlap family
    D = (y-a-bx)^2 + (y-c-dz)^2 + b^2 x(1-x) + d^2 z(1-z),
x, z in [0,1], y in [l,u], A = {a, a+b}, C = {c, c+d} subsets of [l,u].

Checked (exact rationals / sympy):
  (F1) D_L = (y-a-bx)^2 + b^2 x(1-x) is affine in x with endpoint values
       (y-a)^2 and (y-a-b)^2, so min_x D_L = dist(y,A)^2.
  (F2) global minimum of D on the box is delta^2/2 (random instances).
  (F3) trichotomy of the lifted minimum over the glued pair hulls R:
         interleaving disjoint A, C   -> exact zero witness in R;
         other disjoint configurations -> explicit quadratic multiplier
                                         certifying lifted min >= delta^2/2.
  (F4) for every zero witness, the dense moment matrix of (1,x,y,z) has a
       unique PSD completion w = E[xz]; it violates exactly one McCormick
       inequality for xz; McCormick alone (without PSD) admits a value.
  (F5) the SOS + RLT identity
         D - delta^2/2 = (u+v)^2/2 + sum_ij F_ij l_ij(x,z)
                         + (b^2/2) x(1-x) + (d^2/2) z(1-z)
       with u = y-a-bx, v = y-c-dz, l_ij the four McCormick products and
       F_ij = ((C_j-A_i)^2 - delta^2)/2 >= 0; hence dense PSD + McCormick(xz)
       proves D >= delta^2/2 for every member of the family.
Run: .venv/bin/python M4_family.py
"""
from fractions import Fraction as F
import itertools
import random
import sympy as sp

x, y, z, a, b, c, d, dl = sp.symbols("x y z a b c d delta")

# ---- (F1) ------------------------------------------------------------------
DL = sp.expand((y - a - b * x) ** 2 + b**2 * x * (1 - x))
assert sp.Poly(DL, x).degree() <= 1
assert sp.expand(DL - ((y - a) ** 2 + b * x * (b - 2 * (y - a)))) == 0
assert sp.expand(DL.subs(x, 0) - (y - a) ** 2) == 0
assert sp.expand(DL.subs(x, 1) - (y - a - b) ** 2) == 0

# ---- (F5) symbolic identity -----------------------------------------------
u = y - a - b * x
v = y - c - d * z
D = (u**2 + v**2 + b**2 * x * (1 - x) + d**2 * z * (1 - z))
A0, A1, C0, C1 = a, a + b, c, c + d
Fij = {(i, j): ((Cj - Ai) ** 2 - dl**2) / 2
       for i, Ai in enumerate((A0, A1)) for j, Cj in enumerate((C0, C1))}
lij = {(0, 0): (1 - x) * (1 - z), (1, 0): x * (1 - z), (0, 1): (1 - x) * z, (1, 1): x * z}
cert = (u + v) ** 2 / 2 + sum(Fij[k] * lij[k] for k in lij) \
    + b**2 / 2 * x * (1 - x) + d**2 / 2 * z * (1 - z)
assert sp.expand(D - dl**2 / 2 - cert) == 0
# stronger penalties beta >= b^2, beta' >= d^2 (covers the 1/128 example D):
be, bp = sp.symbols("beta betap")
Dbeta = u**2 + v**2 + be * x * (1 - x) + bp * z * (1 - z)
assert sp.expand(Dbeta - dl**2 / 2 - cert - (be - b**2) * x * (1 - x) - (bp - d**2) * z * (1 - z)) == 0
assert sp.Poly(sp.expand(Dbeta), x).coeff_monomial(x**2) == b**2 - be      # <= 0: concave in x
# the xz terms of (u+v)^2/2 and (u-v)^2/2 cancel in D:
assert sp.Poly(sp.expand(D), x, z).coeff_monomial(x * z) == 0


# ---- exact helpers for numeric instances ----------------------------------
def dist2(t, S):
    return min((t - s) ** 2 for s in S)


def global_min(a_, b_, c_, d_, l_, u_):
    """Exact min of D over the box: leaves binary (affine in each leaf),
    then a convex quadratic 2y^2+... in y on [l,u]."""
    best = None
    for xv, zv in itertools.product((0, 1), repeat=2):
        s, t = a_ + b_ * xv, c_ + d_ * zv
        ymid = (s + t) / 2
        ycand = min(max(ymid, l_), u_)
        val = (ycand - s) ** 2 + (ycand - t) ** 2
        best = val if best is None or val < best else best
    return best


def classify(Aset, Cset):
    A_, C_ = sorted(set(Aset)), sorted(set(Cset))
    if set(A_) & set(C_):
        return "share"
    if len(A_) == 2 and len(C_) == 2:
        if A_[0] < C_[0] < A_[1] < C_[1] or C_[0] < A_[0] < C_[1] < A_[1]:
            return "interleave"
    if max(A_) < min(C_) or max(C_) < min(A_):
        return "separated"
    return "nested"


def zero_witness(a_, b_, c_, d_):
    """Solve p b - q d = c - a and p(A1^2-A0^2) - q(C1^2-C0^2) = C0^2-A0^2."""
    A0_, A1_, C0_, C1_ = a_, a_ + b_, c_, c_ + d_
    m11, m12, r1 = b_, -d_, c_ - a_
    m21, m22, r2 = A1_**2 - A0_**2, -(C1_**2 - C0_**2), C0_**2 - A0_**2
    det = m11 * m22 - m12 * m21
    p = (r1 * m22 - m12 * r2) / det
    q = (m11 * r2 - m21 * r1) / det
    return p, q


def principal_minors_nonneg(Mx):
    n = Mx.shape[0]
    for r in range(1, n + 1):
        for idx in itertools.combinations(range(n), r):
            if Mx.extract(list(idx), list(idx)).det() < 0:
                return False
    return True


def multiplier_bound(Aset, Cset):
    """Explicit quadratic multiplier for disjoint non-interleaving A, C.
    Returns kappa1 + kappa2, a certified lower bound on the lifted minimum."""
    A_, C_ = sorted(set(Aset)), sorted(set(Cset))
    delta2 = min((s - t) ** 2 for s in A_ for t in C_)
    kind = classify(A_, C_)
    if kind == "separated":
        if max(A_) < min(C_):
            lo, hi, S1, S2 = max(A_), min(C_), A_, C_
        else:
            lo, hi, S1, S2 = max(C_), min(A_), C_, A_
        lam, m0 = hi - lo, (hi + lo) / 2
        # p(y) = lam (y - m0); min_y (y-s)^2 - p = -lam^2/4 - lam (s - m0)
        k1 = min(-lam**2 / 4 - lam * (s - m0) for s in S1)
        k2 = min(-lam**2 / 4 + lam * (t - m0) for t in S2)
        return k1 + k2, delta2
    assert kind == "nested"
    # inner set: the one contained in a gap of the other
    if min(A_) < min(C_) and max(C_) < max(A_):
        outer, inner = A_, C_
    else:
        outer, inner = C_, A_
    m = (min(inner) + max(inner)) / 2
    R = (max(inner) - min(inner)) / 2
    r = min(abs(s - m) for s in outer)
    assert r ** 2 >= delta2 and (r - R) ** 2 == delta2, (outer, inner, r, R)
    gam = (r - R) / (r + R)
    # p(y) = -gam (y-m)^2 placed on the outer side:
    # min_y (y-s)^2 + gam (y-m)^2 = gam/(1+gam) (s-m)^2
    k1 = min(gam / (1 + gam) * (s - m) ** 2 for s in outer)
    if R == 0:
        k2 = F(0)                       # gam = 1 and (y-m)^2 - (y-m)^2 = 0
    else:
        k2 = min(-gam / (1 - gam) * (t - m) ** 2 for t in inner)
    return k1 + k2, delta2


def mccormick(mx, mz, w):
    return {"w>=0": w >= 0, "w>=mx+mz-1": w >= mx + mz - 1, "w<=mx": w <= mx, "w<=mz": w <= mz}


# ---- random instances -------------------------------------------------------
random.seed(20261003)
counts = {"share": 0, "interleave": 0, "separated": 0, "nested": 0}
violated_names = {}


def rnd():
    return F(random.randint(-12, 12), random.choice([1, 2, 3, 4, 8]))


for trial in range(4000):
    a_, b_, c_, d_ = rnd(), rnd(), rnd(), rnd()
    if trial % 7 == 0:
        b_ = F(0)
    if trial % 11 == 0:
        d_ = F(0)
    pts = [a_, a_ + b_, c_, c_ + d_]
    l_, u_ = min(pts) - F(random.randint(0, 3)), max(pts) + F(random.randint(0, 3))
    Aset, Cset = {a_, a_ + b_}, {c_, c_ + d_}
    delta2 = min((s - t) ** 2 for s in Aset for t in Cset)
    # (F2)
    assert global_min(a_, b_, c_, d_, l_, u_) == delta2 / 2
    kind = classify(Aset, Cset)
    counts[kind] += 1
    if kind == "share":
        continue
    if kind == "interleave":
        assert b_ != 0 and d_ != 0
        p, q = zero_witness(a_, b_, c_, d_)
        assert 0 < p < 1 and 0 < q < 1
        my = a_ + p * b_
        sy = (1 - p) * a_**2 + p * (a_ + b_) ** 2
        assert my == c_ + q * d_ and sy == (1 - q) * c_**2 + q * (c_ + d_) ** 2
        mx, sx, cxy = p, p, p * (a_ + b_)
        mz, sz, cyz = q, q, q * (c_ + d_)
        # lifted D_L, D_R vanish
        liftDL = sy + a_**2 + b_**2 * sx - 2 * a_ * my - 2 * b_ * cxy + 2 * a_ * b_ * mx + b_**2 * (mx - sx)
        liftDR = sy + c_**2 + d_**2 * sz - 2 * c_ * my - 2 * d_ * cyz + 2 * c_ * d_ * mz + d_**2 * (mz - sz)
        assert liftDL == 0 and liftDR == 0
        # uniqueness of the witness: the linear system is nonsingular (checked by solve)
        # (F4) forced completion
        wL = (cyz - a_ * mz) / b_
        wR = (cxy - c_ * mx) / d_
        assert wL == wR
        w = wL
        Mx = sp.Matrix([[1, mx, my, mz], [mx, sx, cxy, w], [my, cxy, sy, cyz], [mz, w, cyz, sz]])
        Mx = Mx.applyfunc(lambda e: sp.Rational(e.numerator, e.denominator) if isinstance(e, F) else e)
        if trial % 10 == 0:            # exact minors are slowish; sample
            assert principal_minors_nonneg(Mx)
        mc = mccormick(mx, mz, w)
        bad = [k for k, ok in mc.items() if not ok]
        assert len(bad) == 1, (a_, b_, c_, d_, mc)
        if b_ > 0 and d_ > 0:
            # rule: the set owning the overall largest point loses its upper bound
            assert bad[0] == ("w<=mx" if max(Aset) > max(Cset) else "w<=mz")
        key = (b_ > 0, d_ > 0, bad[0])
        violated_names[key] = violated_names.get(key, 0) + 1
        # McCormick range alone is nonempty (so PSD is needed)
        assert max(F(0), mx + mz - 1) <= min(mx, mz)
    else:
        lb, d2 = multiplier_bound(Aset, Cset)
        assert lb == d2 / 2, (Aset, Cset, lb, d2)

print("instance counts:", counts)
print("violated McCormick inequality by orientation (b>0, d>0, name): count")
for k_, v_ in sorted(violated_names.items()):
    print("   ", k_, v_)
print("M4_family: all exact checks passed.")
