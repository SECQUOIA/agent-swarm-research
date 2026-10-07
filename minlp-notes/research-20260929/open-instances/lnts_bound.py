"""lnts (particle steering): structure check, primal solution, and a rigorous
Lagrangian dual bound.

Usage: python lnts_bound.py lnts50 [lnts100 ...]

Model (verified below from the OSIL rows, N = number of intervals):
  min  N*h
  s.t. px_{i+1} - px_i - h/2 (vx_i + vx_{i+1}) = 0          i = 0..N-1
       py_{i+1} - py_i - h/2 (vy_i + vy_{i+1}) = 0
       vx_{i+1} - vx_i - h/2 (a cos th_i + a cos th_{i+1}) = 0
       vy_{i+1} - vy_i - h/2 (a sin th_i + a sin th_{i+1}) = 0
       px_0 = py_0 = vx_0 = vy_0 = 0, py_N = 5, vx_N = 45, vy_N = 0, h >= 0.
Summing the recursions gives, for every feasible point,
  vx_N = a h sum_j w_j cos th_j,  vy_N = a h sum_j w_j sin th_j,
  py_N = a h^2 sum_j c_j sin th_j,
with trapezoid weights w (1/2 at both ends, 1 inside) and c_j = sum_k w_k W_{kj},
W_{kj} = ([j <= k-1] + [1 <= j <= k]) / 2.

Certificate: for mu, nu >= 0 and h2 > 0, if
  S(mu,nu) - nu*B(h2) < A(h2),   S = sum_j sqrt(w_j^2 + (mu w_j + nu c_j)^2),
  A(h) = 45/(a h), B(h) = 5/(a h^2),
then no feasible point has h <= h2 (proof in the report), so N*h2 is a valid
lower bound. The inequality is checked in mpmath interval arithmetic.
"""
import json
import math
import sys
from fractions import Fraction

import mpmath as mp

from osil_eval import check, load

mp.mp.dps = 60


def extract(name):
    I = load(name)
    names, lb, ub = I["names"], I["lb"], I["ub"]
    ncons = I["ncons"]
    N = ncons // 4
    assert ncons == 4 * N
    idx = {nm: j for j, nm in enumerate(names)}
    # variable blocks (OSIL order): th_0..th_N, px_0..px_N, py_0..py_N, vx_0..vx_N, vy_0..vy_N, h
    th = list(range(0, N + 1))
    px = list(range(N + 1, 2 * N + 2))
    py = list(range(2 * N + 2, 3 * N + 3))
    vx = list(range(3 * N + 3, 4 * N + 4))
    vy = list(range(4 * N + 4, 5 * N + 5))
    h = 5 * N + 5
    assert len(names) == 5 * N + 6
    obj = I["rows"][-1]
    assert obj["quad"] == [] and obj["nl"] is None and list(obj["lin"].items()) == [(h, float(N))], obj["lin"]
    fixed = {j: lb[j] for j in range(len(names)) if lb[j] == ub[j]}
    assert fixed == {px[0]: 0.0, py[0]: 0.0, py[N]: 5.0, vx[0]: 0.0, vx[N]: 45.0, vy[0]: 0.0, vy[N]: 0.0}, fixed
    assert lb[h] == 0.0 and math.isinf(ub[h])
    for j in th:
        assert lb[j] == -1.5707963267949 and ub[j] == 1.5707963267949
    for j in px[1:] + py[1:N] + vx[1:N] + vy[1:N]:
        assert math.isinf(lb[j]) and math.isinf(ub[j])
    a = None
    for i in range(N):
        for blk, (pos, vel) in enumerate([(px, vx), (py, vy)]):
            row = I["rows"][blk * N + i]
            assert row["lb"] == row["ub"] == 0.0 and row["nl"] is None
            assert row["lin"] == {pos[i]: -1.0, pos[i + 1]: 1.0}, row["lin"]
            assert sorted(row["quad"]) == sorted([(vel[i], h, -0.5), (vel[i + 1], h, -0.5)]), row["quad"]
        for blk, (vel, fn) in enumerate([(vx, "cos"), (vy, "sin")]):
            row = I["rows"][(2 + blk) * N + i]
            assert row["lb"] == row["ub"] == 0.0 and row["quad"] == []
            assert row["lin"] == {vel[i]: -1.0, vel[i + 1]: 1.0}, row["lin"]
            t = row["nl"]
            # ('times', ('sum', ('times', (fn, th_i), a), ('times', (fn, th_{i+1}), a)), ('num', -0.5), ('var', h))
            assert t[0] == "times" and t[2] == ("num", -0.5) and t[3] == ("var", h), t
            s = t[1]
            assert s[0] == "sum" and len(s) == 3
            for k, part in zip((i, i + 1), s[1:]):
                assert part[0] == "times" and part[1] == (fn, ("var", th[k])) and part[2][0] == "num", part
                a = part[2][1] if a is None else a
                assert part[2][1] == a
    return dict(I=I, N=N, a=a, th=th, px=px, py=py, vx=vx, vy=vy, h=h)


def weights(N):
    w = [Fraction(1, 2)] + [Fraction(1)] * (N - 1) + [Fraction(1, 2)]
    c = []
    for j in range(N + 1):
        s = Fraction(0)
        for k in range(1, N + 1):
            Wkj = Fraction((1 if j <= k - 1 else 0) + (1 if 1 <= j <= k else 0), 2)
            s += w[k] * Wkj
        c.append(s)
    return w, c


def solve_primal(N, a, w, c):
    """Linear tangent law th_j = atan((mu w_j + nu c_j)/w_j); solve the three
    terminal equations for (mu, nu, h) by Newton in mpmath."""
    wm = [mp.mpf(x.numerator) / x.denominator for x in w]
    cm = [mp.mpf(x.numerator) / x.denominator for x in c]
    A = mp.mpf(a)

    def F(mu, nu, h):
        th = [mp.atan((mu * wj + nu * cj) / wj) for wj, cj in zip(wm, cm)]
        f1 = mp.fsum(wj * mp.sin(t) for wj, t in zip(wm, th))
        f2 = A * h * mp.fsum(wj * mp.cos(t) for wj, t in zip(wm, th)) - 45
        f3 = A * h * h * mp.fsum(cj * mp.sin(t) for cj, t in zip(cm, th)) - 5
        return [f1, f2, f3]

    mu, nu, h = mp.findroot(F, (mp.mpf(-0.6), mp.mpf(2.0 / N), mp.mpf(0.555 / N)))
    return mu, nu, h


def states(N, a, th, h):
    """Forward recursion in mpmath for all state variables."""
    A = mp.mpf(a)
    px, py, vx, vy = [mp.mpf(0)], [mp.mpf(0)], [mp.mpf(0)], [mp.mpf(0)]
    for i in range(N):
        vx.append(vx[i] + h / 2 * (A * mp.cos(th[i]) + A * mp.cos(th[i + 1])))
        vy.append(vy[i] + h / 2 * (A * mp.sin(th[i]) + A * mp.sin(th[i + 1])))
        px.append(px[i] + h / 2 * (vx[i] + vx[i + 1]))
        py.append(py[i] + h / 2 * (vy[i] + vy[i + 1]))
    return px, py, vx, vy


def certify(N, a, w, c, mu, nu, h2):
    """Interval check of S(mu,nu) - nu B(h2) - A(h2) < 0 with mu, nu, h2 given as
    exact binary floats (converted exactly to intervals)."""
    iv = mp.iv
    iv.dps = 60
    mu_i, nu_i, h_i = iv.mpf(mu), iv.mpf(nu), iv.mpf(h2)
    S = iv.mpf(0)
    for wj, cj in zip(w, c):
        wi = iv.mpf(wj.numerator) / wj.denominator
        ci = iv.mpf(cj.numerator) / cj.denominator
        S += iv.sqrt(wi * wi + (mu_i * wi + nu_i * ci) ** 2)
    Ai = iv.mpf(45) / (iv.mpf(a) * h_i)
    Bi = iv.mpf(5) / (iv.mpf(a) * h_i * h_i)
    margin = S - nu_i * Bi - Ai
    return margin


def main(name):
    d = extract(name)
    N, a = d["N"], d["a"]
    w, c = weights(N)
    mu, nu, h = solve_primal(N, a, w, c)
    th = [mp.atan((mu * (mp.mpf(wj.numerator) / wj.denominator) + nu * (mp.mpf(cj.numerator) / cj.denominator))
                  / (mp.mpf(wj.numerator) / wj.denominator)) for wj, cj in zip(w, c)]
    px, py, vx, vy = states(N, a, th, h)
    x = [0.0] * len(d["I"]["names"])
    for k in range(N + 1):
        x[d["th"][k]] = float(th[k])
        x[d["px"][k]], x[d["py"][k]], x[d["vx"][k]], x[d["vy"][k]] = float(px[k]), float(py[k]), float(vx[k]), float(vy[k])
    for j, v in [(d["py"][0], 0.0), (d["py"][N], 5.0), (d["vx"][0], 0.0), (d["vx"][N], 45.0),
                 (d["vy"][0], 0.0), (d["vy"][N], 0.0), (d["px"][0], 0.0)]:
        x[j] = v  # fixed variables take their exact fixed values
    x[d["h"]] = float(h)
    chk = check(name, x, d["I"])
    # dual certificate: exact binary floats for mu, nu; h2 slightly below h*
    mu_f, nu_f = float(mu), float(nu)
    h2 = float(h * (1 - mp.mpf("1e-10")))
    margin = certify(N, a, w, c, mu_f, nu_f, h2)
    ok = bool(margin.b < 0) and nu_f >= 0  # the argument needs nu >= 0
    dual = N * h2  # N*h2 computed in float; recheck as interval below
    dual_iv = mp.iv.mpf(N) * mp.iv.mpf(h2)
    dual_report = float(mp.mpf(dual_iv.a))  # lower end of the exact product
    rec = dict(name=name, N=N, a=a, mu=mu_f, nu=nu_f, h_star=float(h), primal_obj=chk["obj"],
               primal_bound_viol=chk["bound_viol"], primal_cons_viol=chk["cons_viol"], worst_row=chk["worst_row"],
               h2=h2, certificate_margin_upper=float(margin.b), certificate_ok=bool(ok),
               dual_bound=dual_report if ok else None)
    print(json.dumps(rec))
    with open(f"logs/lnts_{name}.json", "w") as f:
        json.dump(rec, f, indent=1)
    with open(f"logs/lnts_{name}_primal.txt", "w") as f:
        f.write("\n".join(repr(v) for v in x) + "\n")
    return rec


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        main(nm)
