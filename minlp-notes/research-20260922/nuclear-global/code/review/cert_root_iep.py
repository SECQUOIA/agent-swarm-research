"""Reviewer's independent root IEP (B3) bound for F1 instances, made rigorous in exact rational arithmetic.

Root box: k_{i,1} in [KF - Amax a c (T-1), KF] for every node (no pattern information).
For t = 1..T-1:
  Ll_t <= rho(G diag kl_t)  : Collatz-Wielandt minimum ratio with a rational positive w (exact)
  Lh_t >= rho(G diag kh_t)  : Collatz-Wielandt maximum ratio (exact)
  Q_t = {V'p = 1, 0 <= p <= c, Ll p_i - kh_i (Gp)_i <= 0, kl_i (Gp)_i - Lh p_i <= 0}
  pl_i <= min_{Q_t} p_i, ph_i >= max_{Q_t} p_i : weak duality with float duals from HiGHS, evaluated exactly:
        for u free, mu >= 0:  p_i >= u + sum_j min(0, r_j) c_j,  r = e_i + A'mu - u V   (A p <= 0 rows)
  kl_{t+1} = kl_t - a ph_t (rounded down), kh_{t+1} = kh_t - a pl_t (rounded up)
Bound: lam_T <= rho(G diag kh_T) <= max_i (G diag(kh_T) w)_i / w_i   (B1 with IEP kh; exact).
Also prints the float values (numpy eigenvalues, HiGHS LP optima) for comparison with the author.
usage: cert_root_iep.py names..."""
import sys
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
from struct_nuc import analyze

DEN = 10 ** 18


def rdown(x): return F((x.numerator * DEN) // x.denominator, DEN)
def rup(x): return -rdown(-x)


def ratw(v):
    return [F(float(max(z, 1e-300))).limit_denominator(10 ** 15) for z in v]


def cw(Gq, k, w, which):
    N = len(k)
    r = [sum(Gq[i][j] * k[j] * w[j] for j in range(N)) / w[i] for i in range(N)]
    return min(r) if which == "min" else max(r)


def perron_w(Gf, kf):
    M = Gf * kf[None, :]
    ev, W = np.linalg.eig(M); m = np.argmax(ev.real)
    return ev[m].real, np.abs(W[:, m].real)


def main(nm):
    S = analyze(nm); N, T = S.N, S.T
    Gq, Vq, a, KF = S.G, S.V, S.a, S.KF
    cs = {x for r in S.c for x in r}; assert len(cs) == 1; c = cs.pop()
    Amax = max(S.age.values())
    Gf = np.array([[float(x) for x in r] for r in Gq]); Vf = np.array([float(x) for x in Vq]); cf = float(c)
    kl = [KF - Amax * a * c * (T - 1)] * N; kh = [KF] * N
    klf = np.array([float(x) for x in kl]); khf = klf * 0 + float(KF)
    for t in range(T - 1):
        # float reference (author-style): eigenvalues and LP optima in floating point
        Llf, _ = perron_w(Gf, klf); Lhf, _ = perron_w(Gf, khf)
        # rigorous eigenvalue enclosure
        _, wl = perron_w(Gf, np.array([float(x) for x in kl])); _, wh = perron_w(Gf, np.array([float(x) for x in kh]))
        Ll = cw(Gq, kl, ratw(wl), "min"); Lh = cw(Gq, kh, ratw(wh), "max")
        assert float(Ll) <= Llf + 1e-12 and float(Lh) >= Lhf - 1e-12
        # LP data (A p <= 0)
        Aq = []
        for i in range(N):
            Aq.append([(Ll if j == i else 0) - kh[i] * Gq[i][j] for j in range(N)])
        for i in range(N):
            Aq.append([kl[i] * Gq[i][j] - (Lh if j == i else 0) for j in range(N)])
        Af = np.array([[float(x) for x in r] for r in Aq])
        # float Q_t with float Ll, Lh (the author's construction)
        Aff = np.vstack([np.diag(np.full(N, Llf)) - khf[:, None] * Gf, klf[:, None] * Gf - np.diag(np.full(N, Lhf))])
        pl, ph, plf, phf = [], [], [], []
        for i in range(N):
            for sgn in (1, -1):
                e = np.zeros(N); e[i] = sgn
                rf = linprog(e, A_ub=Aff, b_ub=np.zeros(2 * N), A_eq=Vf[None, :], b_eq=[1], bounds=[(0, cf)] * N, method="highs")
                assert rf.status == 0
                (plf if sgn == 1 else phf).append(sgn * rf.fun)
                res = linprog(e, A_ub=Af, b_ub=np.zeros(2 * N), A_eq=Vf[None, :], b_eq=[1], bounds=[(0, cf)] * N, method="highs")
                assert res.status == 0
                best = None
                for s2 in (1, -1):
                    mu = [F(float(max(0.0, s2 * z))) for z in res.ineqlin.marginals]
                    for s3 in (1, -1):
                        u = F(float(s3 * res.eqlin.marginals[0]))
                        ei = [F(sgn) if j == i else F(0) for j in range(N)]
                        r = [ei[j] + sum(Aq[q][j] * mu[q] for q in range(2 * N) if mu[q]) - u * Vq[j] for j in range(N)]
                        lb = u + sum(min(F(0), r[j]) * c for j in range(N))   # rigorous lower bound on sgn*p_i
                        best = lb if best is None or lb > best else best
                if sgn == 1:
                    pl.append(max(F(0), best))
                else:
                    ph.append(min(c, -best))
        kl = [rdown(kl[i] - a * ph[i]) for i in range(N)]
        kh = [rup(kh[i] - a * pl[i]) for i in range(N)]
        klf = klf - float(a) * np.array(phf); khf = khf - float(a) * np.array(plf)
        gap_l = max(float(pl[i]) - plf[i] for i in range(N)); gap_h = max(phf[i] - float(ph[i]) for i in range(N))
        print(f"  t={t+1}: Lam=[{float(Ll):.9f},{float(Lh):.9f}] min pl={float(min(pl)):.6f} max ph={float(max(ph)):.6f} "
              f"(rigorous minus float LP: pl {gap_l:.1e}, ph {-gap_h:.1e})", flush=True)
    rhof, wT = perron_w(Gf, khf)
    ub = cw(Gq, kh, ratw(perron_w(Gf, np.array([float(x) for x in kh]))[1]), "max")
    print(f"{nm}: float B1(IEP kh_T) = {rhof:.9f};  certified upper bound (exact CW on rigorous kh_T) = {float(rup(ub)):.9f}"
          f"  [{rup(ub)}]; min kh_T = {float(min(kh)):.6f}", flush=True)
    return kh, S, c


def knap(d, V, c, sense="max"):
    """Exact optimum and optimizer of d'p over P = {V'p = 1, 0 <= p <= c} (fractional knapsack)."""
    N = len(d); order = sorted(range(N), key=lambda j: d[j] / V[j], reverse=(sense == "max"))
    p = [F(0)] * N; rem = F(1)
    for j in order:
        take = min(c, rem / V[j]); p[j] = take; rem -= V[j] * take
        if rem == 0: break
    assert rem == 0
    return sum(d[j] * p[j] for j in range(N)), p


def cert_b2(Gq, Vq, c, kh):
    """B2: lam_T <= max_{p in P} y'Gp / sum_i y_i p_i / kh_i, y from float LP bisection, value by exact Dinkelbach."""
    N = len(kh); Gf = np.array([[float(x) for x in r] for r in Gq]); Vf = np.array([float(x) for x in Vq])
    khf = np.array([float(x) for x in kh]); cf = float(c)
    lo, hi = 0.0, 2.0; yb = None
    for _ in range(50):
        beta = (lo + hi) / 2
        # vars: y (N), mu (1), nu (N);  min mu + c sum nu  s.t.  (G'y)_j - beta y_j/kh_j - V_j mu - nu_j <= 0, sum y = 1
        A = np.hstack([Gf.T - np.diag(beta / khf), -Vf[:, None], -np.eye(N)])
        cost = np.concatenate([np.zeros(N), [1.0], np.full(N, cf)])
        r = linprog(cost, A_ub=A, b_ub=np.zeros(N), A_eq=np.concatenate([np.ones(N), [0], np.zeros(N)])[None, :], b_eq=[1],
                    bounds=[(0, None)] * N + [(None, None)] + [(0, None)] * N, method="highs")
        if r.status == 0 and r.fun <= 1e-12: hi = beta; yb = r.x[:N]
        else: lo = beta
    y = [F(float(max(z, 0.0))).limit_denominator(10 ** 12) for z in yb]
    den = [y[i] / kh[i] for i in range(N)]
    mden, _ = knap(den, Vq, c, "min"); assert mden > 0      # sum_i y_i p_i / kh_i > 0 on P
    num = [sum(y[i] * Gq[i][j] for i in range(N)) for j in range(N)]
    _, p = knap(num, Vq, c, "max")
    beta = sum(num[j] * p[j] for j in range(N)) / sum(den[j] * p[j] for j in range(N))
    for _ in range(100):   # Dinkelbach, exact
        val, p = knap([num[j] - beta * den[j] for j in range(N)], Vq, c, "max")
        if val <= 0: break
        beta = sum(num[j] * p[j] for j in range(N)) / sum(den[j] * p[j] for j in range(N))
    else:
        raise RuntimeError("Dinkelbach did not terminate")
    return hi, beta


def main2(nm):
    kh, S, c = main(nm)
    fl, b = cert_b2(S.G, S.V, c, kh)
    print(f"{nm}: B2 (peaking) with rigorous kh_T: float bisection {fl:.9f}; certified (exact Dinkelbach) {float(rup(b)):.9f}", flush=True)


for nm in sys.argv[1:]:
    main2(nm)
