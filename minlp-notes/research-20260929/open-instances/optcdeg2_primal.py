"""optcdeg2 primal: bang-bang control u = -0.2 (t < k1), +0.2 (k1 < t < k2), -0.2 (t > k2),
with fractional values at the two switching steps. For given (k1, f1) the second switch
(k2, f2) is found by bisection on the (monotone) map s -> v_N, s = k2 + fractional part,
so that v_N = 0; then (k1, f1) is optimized by a scan. States are simulated exactly
from the controls, so all equality rows hold up to rounding."""
import json, numpy as np
from optcdeg2_common import N, h, to_osil
from osil_eval import check, load

def simulate(u):
    y = np.empty(N + 1); v = np.empty(N + 1); y[0] = 10.0; v[0] = 0.0
    for t in range(N):
        y[t + 1] = y[t] + h * v[t]
        v[t + 1] = v[t] + h * (u[t] - 0.02 * y[t] - 0.2 * v[t] ** 2)
    return y, v

def controls(s1, s2):
    """s = switch position in steps (float): u_t = -0.2 for t < floor(s), fractional at floor(s)."""
    u = np.full(N, -0.2)
    k1, f1 = int(s1), s1 - int(s1); k2, f2 = int(s2), s2 - int(s2)
    u[k1 + 1:k2] = 0.2
    u[k1] = -0.2 + 0.4 * (1 - f1)          # f1 = 0 -> +0.2 at k1 (switch at k1)
    u[k2] = 0.2 - 0.4 * (1 - f2) if k2 > k1 else u[k2]
    return u

def vN(s1, s2):
    return simulate(controls(s1, s2))[1][N]

def solve_s2(s1, lo=46000.0, hi=48500.0):
    flo, fhi = vN(s1, lo), vN(s1, hi)
    assert flo * fhi < 0, (flo, fhi)
    for _ in range(60):
        mid = 0.5 * (lo + hi); fm = vN(s1, mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return 0.5 * (lo + hi)

def cost(s1):
    s2 = solve_s2(s1); u = controls(s1, s2); y, v = simulate(u)
    return h / 2 * np.sum(y ** 2), s2, u, y, v

if __name__ == "__main__":
    best = None
    for s1 in np.arange(3080.0, 3100.0, 1.0):
        c = cost(s1)
        print(s1, c[0], c[1], flush=True)
        if best is None or c[0] < best[0][0]: best = (c, s1)
    # golden-section refine around the best integer
    a, b = best[1] - 1.0, best[1] + 1.0
    g = (5 ** 0.5 - 1) / 2
    x1, x2 = b - g * (b - a), a + g * (b - a); f1, f2 = cost(x1)[0], cost(x2)[0]
    for _ in range(30):
        if f1 < f2: b, x2, f2 = x2, x1, f1; x1 = b - g * (b - a); f1 = cost(x1)[0]
        else: a, x1, f1 = x1, x2, f2; x2 = a + g * (b - a); f2 = cost(x2)[0]
    s1 = 0.5 * (a + b); c, s2, u, y, v = cost(s1)
    v = v.copy(); v[N] = 0.0  # fixed variable takes its exact value; residual reported by the check
    chk = check("optcdeg2", to_osil(u, y, v))
    rec = dict(s1=s1, s2=s2, cost_float=c, obj=chk["obj"], cons_viol=chk["cons_viol"], bound_viol=chk["bound_viol"], worst_row=chk["worst_row"])
    print(json.dumps(rec))
    json.dump(rec, open("logs/optcdeg2_primal.json", "w"), indent=1)
    np.save("logs/optcdeg2_primal_u.npy", u)
