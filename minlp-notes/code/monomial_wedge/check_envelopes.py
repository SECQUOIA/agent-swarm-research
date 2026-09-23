"""Numerical check of the n = 2 wedge envelope classification for real exponents.

f(x1, x2) = x1^a1 * x2^a2 on W = {x > 0 : p x1 <= x2 <= q x1}, D = {x in W : l <= f(x) <= u}.
Predicted envelopes (conv(D), lower E_L, upper E_U) by regime:
  I.1  a1,a2>0, beta>=1 : conv(D)={f>=l, phi<=u};  E_L=max(l,phi),  E_U=min(u,H)
  I.2  a1,a2>0, beta<=1 : conv(D)={f>=l, phi<=u};  E_L=max(l,L),    E_U=min(u,f)
  II   a1,a2<0           : conv(D)={f<=u, phi>=l};  E_L=max(f,l),    E_U=min(u,L)
  IIIA mixed, kappa<1    : conv(D)={f>=l, phi<=u};  E_L=max(l,phi),  E_U=min(u,H)
  IIIB1 mixed,kappa>1,beta>=1: conv(D)={f<=u, phi>=l}; E_L=max(f,l), E_U=min(u,L)
  IIIB2 mixed,kappa>1,0<beta<1: conv(D)={f<=u, phi>=l}; E_L=max(l,H), E_U=min(u,phi)
where phi = (s/sigma)^beta (constant on parallel level-curve chords, exact on the rays),
H = z0 + c f^{1/beta} (affine on rays, exact on the level curves l, u), L affine through the
four corner points, s a linear form positive on W.
Envelopes are compared against LP envelopes of a dense sample of graph points over D.
Run: conda run -n minlp-notes python code/monomial_wedge/check_envelopes.py
"""
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(7)


def setup(a1, a2, p, q, l, u):
    beta = a1 + a2
    if beta == 0:
        raise ValueError("The chord/ray formulas require a1 + a2 != 0")
    if not (0 < p < q and 0 < l < u):
        raise ValueError("Expected 0 < p < q and 0 < l < u")
    f = lambda x: x[..., 0] ** a1 * x[..., 1] ** a2
    # level-1 endpoints on rays x2 = p x1 and x2 = q x1: x1 = r^{-a2/beta}
    def endpoint(r, xi=1.0):
        x1 = (xi / r ** a2) ** (1.0 / beta)
        return np.array([x1, r * x1])
    v = endpoint(q) - endpoint(p)          # chord direction (level independent)
    # linear form s vanishing on v, positive on W
    s_coef = np.array([v[1], -v[0]])       # s(x) = v2 x1 - v1 x2
    if s_coef @ endpoint(p) < 0:
        s_coef = -s_coef
    s = lambda x: x[..., 0] * s_coef[0] + x[..., 1] * s_coef[1]
    sigma = s(endpoint(p))
    assert abs(sigma - s(endpoint(q))) < 1e-9 * abs(sigma)
    phi = lambda x: (s(x) / sigma) ** beta
    c = (u - l) / (u ** (1 / beta) - l ** (1 / beta))
    z0 = l - c * l ** (1 / beta)
    H = lambda x: z0 + c * f(x) ** (1 / beta)
    s_l, s_u = sigma * l ** (1 / beta), sigma * u ** (1 / beta)
    zeta = (u - l) / (s_u - s_l)
    L = lambda x: l + zeta * (s(x) - s_l)
    corners = [endpoint(p, l), endpoint(q, l), endpoint(p, u), endpoint(q, u)]
    return dict(beta=beta, f=f, s=s, phi=phi, H=H, L=L, corners=np.array(corners), endpoint=endpoint)


def regime(a1, a2):
    beta = a1 + a2
    if beta == 0:
        raise ValueError("Degree-zero cases are checked separately")
    if a1 == 0 or a2 == 0:
        return "U.conv" if beta < 0 or beta >= 1 else "U.conc"
    if a1 > 0 and a2 > 0:
        return "I.1" if beta >= 1 else "I.2"
    if a1 < 0 and a2 < 0:
        return "II"
    pos, neg = (a1, a2) if a1 > 0 else (a2, a1)
    kappa = pos / abs(neg)
    if kappa < 1:
        return "IIIA"
    return "IIIB1" if beta >= 1 else "IIIB2"


def predicted(reg, S, x):
    f, phi, H, L = S["f"], S["phi"], S["H"], S["L"]
    l, u = S["l"], S["u"]
    if reg in ("I.1", "IIIA"):
        return np.maximum(l, phi(x)), np.minimum(u, H(x))
    if reg in ("I.2", "U.conc"):
        return np.maximum(l, L(x)), np.minimum(u, f(x))
    if reg in ("II", "IIIB1", "U.conv"):
        return np.maximum(f(x), l), np.minimum(u, L(x))
    if reg == "IIIB2":
        return np.maximum(l, H(x)), np.minimum(u, phi(x))
    raise ValueError(f"Unknown regime: {reg}")


def in_conv_pred(reg, S, x):
    f, phi = S["f"], S["phi"]
    l, u = S["l"], S["u"]
    if reg in ("I.1", "I.2", "IIIA"):
        return (f(x) >= l - 1e-9) & (phi(x) <= u + 1e-9)
    return (f(x) <= u + 1e-9) & (phi(x) >= l - 1e-9)


def lp_envelope(pts, vals, x, sense):
    """min/max sum mu_k vals_k s.t. sum mu_k pts_k = x, sum mu = 1, mu >= 0."""
    n = len(pts)
    A_eq = np.vstack([pts.T, np.ones(n)])
    b_eq = np.array([x[0], x[1], 1.0])
    cvec = vals if sense == "min" else -vals
    res = linprog(cvec, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method="highs")
    if res.status == 2:
        return None
    if res.status != 0:
        raise RuntimeError(f"LP did not finish successfully: {res.message}")
    return res.fun if sense == "min" else -res.fun


def sample_D(a1, a2, p, q, l, u, n=4000):
    beta = a1 + a2
    rs = np.exp(rng.uniform(np.log(p), np.log(q), n))
    xis = np.exp(rng.uniform(np.log(l), np.log(u), n))
    x1 = (xis / rs ** a2) ** (1.0 / beta)
    pts = np.stack([x1, rs * x1], axis=1)
    # add boundary: rays and level curves densely
    rr = np.exp(np.linspace(np.log(p), np.log(q), 200))
    for xi in (l, u):
        x1b = (xi / rr ** a2) ** (1.0 / beta)
        pts = np.vstack([pts, np.stack([x1b, rr * x1b], axis=1)])
    xx = np.exp(np.linspace(np.log(l), np.log(u), 200))
    for r in (p, q):
        x1b = (xx / r ** a2) ** (1.0 / beta)
        pts = np.vstack([pts, np.stack([x1b, r * x1b], axis=1)])
    return pts


def run_instance(a1, a2, p, q, l, u, ntest=60):
    reg = regime(a1, a2)
    S = setup(a1, a2, p, q, l, u); S["l"], S["u"] = l, u
    f = S["f"]
    pts = sample_D(a1, a2, p, q, l, u)
    vals = f(pts)
    assert np.all(vals >= l - 1e-9) and np.all(vals <= u + 1e-9)
    sample_lower, sample_upper = predicted(reg, S, pts)
    assert np.all(sample_lower <= vals + 1e-9 * u)
    assert np.all(sample_upper >= vals - 1e-9 * u)
    # sanity: phi exact on rays, H exact on level curves, L exact on corners; minorant/majorant relations on D
    for r in (p, q):
        x = S["endpoint"](r, np.exp(rng.uniform(np.log(l), np.log(u))))
        assert abs(S["phi"](x) - f(x)) < 1e-8 * f(x)
    for xi in (l, u):
        x = S["endpoint"](np.exp(rng.uniform(np.log(p), np.log(q))), xi)
        assert abs(S["H"](x) - f(x)) < 1e-8 * f(x)
    for cpt in S["corners"]:
        assert abs(S["L"](cpt) - f(cpt)) < 1e-8 * f(cpt)
    # test points: random convex combinations of sample points (inside conv(D))
    worst_l = worst_u = 0.0
    worst_dom = 0.0
    for _ in range(ntest):
        k = rng.integers(2, 5)
        idx = rng.choice(len(pts), k, replace=False)
        w = rng.dirichlet(np.ones(k))
        x = w @ pts[idx]
        assert in_conv_pred(reg, S, x[None, :])[0], (reg, x)
        el = lp_envelope(pts, vals, x, "min"); eu = lp_envelope(pts, vals, x, "max")
        assert el is not None and eu is not None, "A sampled convex combination must be feasible"
        pl, pu = predicted(reg, S, x[None, :])
        # LP envelope over a finite sample is >= true lower envelope and <= true upper envelope
        worst_l = max(worst_l, (pl[0] - el) / u)   # predicted lower must not exceed LP lower
        worst_u = max(worst_u, (eu - pu[0]) / u)   # predicted upper must not be below LP upper
        # and they should be close (sampling density)
        worst_dom = max(worst_dom, abs(pl[0] - el) / u, abs(eu - pu[0]) / u)
    # points outside predicted conv(D) but in the wedge must be unreachable: test by LP feasibility
    bad = 0
    for _ in range(20):
        r = np.exp(rng.uniform(np.log(p), np.log(q)))
        xi = np.exp(rng.uniform(np.log(l) - 1.0, np.log(u) + 1.0))
        x1 = (xi / r ** a2) ** (1.0 / S["beta"]); x = np.array([x1, r * x1])
        inside = in_conv_pred(reg, S, x[None, :])[0]
        feas = lp_envelope(pts, vals, x, "min") is not None
        if feas and not inside:
            bad += 1
    return reg, worst_l, worst_u, worst_dom, bad


def check_degree_zero_examples():
    """Exact rational examples for the nonclosed degree-zero graph hull.

    These check the construction and boundary distinctions in Remark 2;
    they do not certify the general set equality proved in the note.
    """
    F = Fraction

    def ratio_interval(k, p, q, l, u):
        # The examples use k = +/-1 so every calculation remains rational.
        assert k in (-1, 1)
        ends = (l, u) if k == 1 else (1 / u, 1 / l)
        lo, hi = max(p, ends[0]), min(q, ends[1])
        return None if lo > hi else (lo, hi)

    def interior_witness(a, b, k, s, r, z):
        theta = (r - a) / (b - a)
        weight = (z - a**k) / (b**k - a**k)
        assert 0 < theta < 1 and 0 < weight < 1
        t_a = s * (1 - theta) / (1 - weight)
        t_b = s * theta / weight
        point_a, point_b = (t_a, a * t_a, a**k), (t_b, b * t_b, b**k)
        assert t_a > 0 and t_b > 0
        mixture = tuple((1 - weight) * x + weight * y for x, y in zip(point_a, point_b))
        assert mixture == (s, s * r, z)

    p, q = F(1), F(2)
    assert ratio_interval(1, p, q, F(1, 2), F(3)) == (p, q)  # Loose bounds: actual values [1,2].
    assert ratio_interval(1, p, q, F(2), F(3)) == (q, q)     # A single graph ray.
    assert ratio_interval(1, p, q, F(3), F(4)) is None      # Empty domain.
    assert ratio_interval(-1, p, q, F(1, 2), F(1)) == (p, q)
    interior_witness(p, q, 1, F(3), F(4, 3), F(7, 4))
    interior_witness(p, q, -1, F(3), F(4, 3), F(3, 4))
    # On r = p, nonnegative x_2 - p*x_1 forces every contributing graph
    # point onto r = p, hence z = p^k. In particular (1,1,2) is excluded.
    assert p != q and p**1 != F(2)
    # Interior hull points approach that excluded boundary point. Their
    # exact two-point decompositions verify membership before taking limits.
    for n in (3, 10, 100):
        r, z = p + F(1, n), q - F(1, n)
        interior_witness(p, q, 1, F(1), r, z)
        assert abs(r - p) == F(1, n) and abs(z - q) == F(1, n)
    # Degree-zero with k = 0 is the constant graph z = 1, when feasible.
    for l, u, feasible in ((F(1, 2), F(2), True), (F(2), F(3), False)):
        assert (l <= 1 <= u) == feasible
    for a1, a2 in ((1, -1), (0, 0)):
        try:
            setup(a1, a2, 0.4, 2.5, 0.7, 3.1)
        except ValueError:
            pass
        else:
            raise AssertionError("Nonzero-degree formulas accepted degree-zero input")


if __name__ == "__main__":
    check_degree_zero_examples()
    print("degree-zero exact rational examples consistent", flush=True)
    cases = [
        (1.7, 1.5), (0.6, 0.2), (0.5, 0.5), (1.0, 1.0),      # I.1, I.2, beta=1, I.1
        (-0.8, -1.3), (-0.3, -0.4),                            # II
        (0.5, -1.2), (1.0, -3.0), (0.2, -0.5),                 # IIIA (kappa<1)
        (2.0, -0.7), (3.0, -1.0), (1.4, -0.4),                 # IIIB1 and near beta=1 in floating point
        (1.5, -1.0), (0.9, -0.5), (1.2, -0.9),                 # IIIB2 (kappa>1, 0<beta<1)
        (-1.2, 0.5), (-0.5, 0.9), (-1.0, 2.0),                # swapped mixed signs; exact beta=1
        (2.0, 0.0), (0.0, 2.0), (0.5, 0.0), (0.0, 0.5),      # univariate convex/concave
        (-1.0, 0.0), (0.0, -1.0), (1.0, 0.0), (0.0, 1.0),    # univariate negative/linear
    ]
    ok = True
    for a1, a2 in cases:
        p, q = 0.4, 2.5
        l, u = 0.7, 3.1
        reg, wl, wu, wd, bad = run_instance(a1, a2, p, q, l, u)
        # Signed violations test validity; the two-sided discrepancy tests only
        # agreement with this finite sample, not an exact-envelope certificate.
        flag = (wl <= 1e-7) and (wu <= 1e-7) and (wd <= 2e-3) and (bad == 0)
        ok &= flag
        print(f"a=({a1:+.2f},{a2:+.2f}) regime {reg:6s}  pred_lower - LP_lower <= {wl:.1e}  LP_upper - pred_upper <= {wu:.1e}  max|diff| {wd:.1e}  outside-but-feasible {bad}  {'ok' if flag else 'FAIL'}", flush=True)
    print("all regimes consistent" if ok else "INCONSISTENCY FOUND")
    raise SystemExit(0 if ok else 1)
