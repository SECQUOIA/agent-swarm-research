"""Re-derivation of the z = 1 specialization of the tilted SGFCI (17) of Lim, Linderoth, Luedtke (2018)
and comparison with the (F, T_1, T_2) selections of the note.

Part 1 (sympy): solve their system (7) with (a1,b1,a2,b2,l,u) = (1, mu-u_i, 0, 0, 0, u_i), build (17)
with N^- = C^- = empty and z = 1, and compare with
  (a) the display in the note (general capacities), and
  (b) the selection F, T_1 = N\\C, T_2 = C\\F for equal capacities, both for the equality row (Theorem 2)
      and, without using the row, for the <= row (Theorem 2(b)).
Part 2 (LP + exact vertex enumeration): the cover subfamily is strictly weaker than (RH).
"""
import itertools
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
from scipy.optimize import linprog


def part1():
    n, k = 5, 2
    C, F = [0, 1, 2], [0, 1]          # |C| = k+1
    w, r = sp.symbols("w r", positive=True)
    x = sp.symbols("x0:5")
    tau = sp.symbols("tau0:5")
    gm = sp.symbols("g0:5", positive=True)     # gamma_i(m_i)
    cs = sp.symbols("c0:5")                    # chord slopes: f_i(x) = c_i x + gamma_i(x), f_i(0) = 0
    d = k * w + r
    mu = (k + 1) * w - d
    assert sp.simplify(mu - (w - r)) == 0
    lam = {}
    for i in F:
        u_i = w
        m_i = u_i - mu                           # intersection of x + mu - u = 0*x + 0
        lx, lz, lt = sp.symbols("lx lz lt")
        f_l, f_m, f_u = 0, cs[i] * m_i + gm[i], cs[i] * u_i
        sol = sp.solve([0 * lx + lz + f_l * lt - 0,
                        m_i * lx + lz + f_m * lt - 0,
                        u_i * lx + lz + f_u * lt - (u_i + mu - u_i)], [lx, lz, lt], dict=True)[0]
        assert sol[lz] == 0
        lam[i] = (sol[lx], sol[lt])
    # (17) with z = 1:  sum_{C\F} (x_i - (u_i-mu)) + sum_F (lx x_i + lt t_i) <= d - sum_C (u_i - mu)
    t = [cs[i] * x[i] + tau[i] for i in range(n)]            # t_i = chord + tau_i
    lhs17 = sum(x[i] - (w - mu) for i in C if i not in F) + sum(lam[i][0] * x[i] + lam[i][1] * t[i] for i in F)
    rhs17 = d - sum(w - mu for i in C)
    viol17 = sp.simplify(lhs17 - rhs17)                      # valid iff <= 0
    # (a) note's display: sum_F tau/g * (mu m/u) >= sum_{C\F} x + sum_F (mu/u) x + sum_F m - d
    m_ = w - mu
    note = (sum(x[i] for i in C if i not in F) + sum(mu / w * x[i] for i in F) + sum(m_ for i in F) - d
            - sum(tau[i] / gm[i] * (mu * m_ / w) for i in F))   # valid iff <= 0
    print("(17) at z=1 minus the note's display:", sp.simplify(viol17 - note))
    # (b) selection (F, T1 = N\C, T2 = C\F)
    sel = (sum(tau[i] / gm[i] for i in F) + sum(x[i] / r for i in range(n) if i not in C)
           + sum((w - x[i]) / (w - r) for i in C if i not in F))
    # <= row, Theorem 2(b):  sel >= (sum x - k w)/r ;  violation form  (sum x - k w)/r - sel <= 0
    viol_b = (sum(x) - k * w) / r - sel
    print("2(b) selection minus  w/(r(w-r)) * (17):", sp.simplify(viol_b - w / (r * (w - r)) * viol17), " (0 = identical, no use of the row)")
    # equality row, Theorem 2: 1 - sel <= 0, compare after substituting the row
    viol_eq = 1 - sel
    diff = sp.simplify((viol_eq - w / (r * (w - r)) * viol17).subs(x[4], d - sum(x[:4])))
    print("Theorem 2 selection minus w/(r(w-r)) * (17), on the row:", diff)


def part2():
    # smallest case: n = 3, k = 1, w = 1, r = 1/2, delta = 1/4 each; objective sum tau_i / delta_i
    n, k = 3, 1
    w, r = Fr(1), Fr(1, 2)
    delta = [Fr(1, 4)] * n
    exact = None
    for j in range(n):
        for S in itertools.combinations([i for i in range(n) if i != j], k):
            val = Fr(1)       # tau_j/delta_j = 1 at the vertex, other tau = 0
            exact = val if exact is None else min(exact, val)
    out = {}
    for sub in (False, True):
        A, b = [], []
        for ch in itertools.product(range(3), repeat=n):
            Fset = [i for i in range(n) if ch[i] == 0]
            T2 = [i for i in range(n) if ch[i] == 2]
            if sub and len(Fset) + len(T2) != k + 1:
                continue
            row = [0.0] * (2 * n); const = 0.0
            for i in range(n):
                if ch[i] == 0:
                    row[n + i] = 1 / float(delta[i])
                elif ch[i] == 1:
                    row[i] = 1 / float(r)
                else:
                    row[i] = -1 / float(w - r); const += float(w / (w - r))
            A.append([-v for v in row]); b.append(const - 1.0)
        cost = [0.0] * n + [1 / float(dl) for dl in delta]
        res = linprog(cost, A_ub=A, b_ub=b, A_eq=[[1.0] * n + [0.0] * n], b_eq=[float(k * w + r)],
                      bounds=[(0, float(w))] * n + [(0, None)] * n, method="highs")
        out[sub] = (res.fun, res.x)
    print("n=3,k=1,w=1,r=1/2, min sum tau_i/delta_i: exact over vertices", exact,
          "| all selections", round(out[False][0], 9), "| cover subfamily only", round(out[True][0], 9))
    print("  subfamily optimizer (z, tau):", np.round(out[True][1], 6))


if __name__ == "__main__":
    part1()
    part2()
