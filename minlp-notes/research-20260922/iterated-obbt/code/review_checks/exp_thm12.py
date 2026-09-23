"""Independent spot check of Theorem 12's E-recursion (products, exp, scaling)
against a direct composite McCormick implementation (MCB 2009 rules)."""
import numpy as np
rng = np.random.default_rng(7)

# expression DAG: list of ops; ('x',i) ('mul',a,b) ('exp',a) ('scale',c,a) ('add',a,b)
def mccormick(expr, lo, hi, x):
    V = []   # (value, L, U, cv, cc)
    for op in expr:
        if op[0] == 'x':
            i = op[1]; V.append((x[i], lo[i], hi[i], x[i], x[i]))
        elif op[0] == 'add':
            A, B = V[op[1]], V[op[2]]; V.append(tuple(A[k] + B[k] for k in range(5)))
        elif op[0] == 'scale':
            c, A = op[1], V[op[2]]
            V.append((c*A[0], min(c*A[1], c*A[2]), max(c*A[1], c*A[2]),
                      c*A[3] if c >= 0 else c*A[4], c*A[4] if c >= 0 else c*A[3]))
        elif op[0] == 'exp':
            a, aL, aU, acv, acc = V[op[1]]
            L, U = np.exp(aL), np.exp(aU)
            cv = np.exp(max(acv, aL))            # mid(cv, cc, zmin = aL); exp increasing & convex
            m = min(acc, aU)                      # mid(cv, cc, zmax = aU)
            sec = L if aU == aL else L + (U - L) * (m - aL) / (aU - aL)
            V.append((np.exp(a), L, U, cv, sec))
        elif op[0] == 'mul':
            a, aL, aU, acv, acc = V[op[1]]; b, bL, bU, bcv, bcc = V[op[2]]
            P = [aL*bL, aL*bU, aU*bL, aU*bU]
            al1 = min(bL*acv, bL*acc); al2 = min(aL*bcv, aL*bcc)
            be1 = min(bU*acv, bU*acc); be2 = min(aU*bcv, aU*bcc)
            ga1 = max(bL*acv, bL*acc); ga2 = max(aU*bcv, aU*bcc)
            de1 = max(bU*acv, bU*acc); de2 = max(aL*bcv, aL*bcc)
            cv = max(al1 + al2 - aL*bL, be1 + be2 - aU*bU)
            cc = min(ga1 + ga2 - aU*bL, de1 + de2 - aL*bU)
            V.append((a*b, min(P), max(P), cv, cc))
    return V

def tangent(expr, xs, dm, dp, xi):
    """recursion of A.1: returns per factor (v*, grad, p, ellL, ellU, Ecv, Ecc)"""
    n = len(xs); T = []
    pos = lambda t: max(t, 0.0); neg = lambda t: max(-t, 0.0)
    for op in expr:
        if op[0] == 'x':
            i = op[1]; g = np.eye(n)[i]; T.append((xs[i], g, xi[i], -dm[i], dp[i], 0.0, 0.0))
        elif op[0] == 'add':
            A, B = T[op[1]], T[op[2]]
            T.append((A[0]+B[0], A[1]+B[1], A[2]+B[2], A[3]+B[3], A[4]+B[4], A[5]+B[5], A[6]+B[6]))
        elif op[0] == 'scale':
            c, A = op[1], T[op[2]]
            if c >= 0: T.append((c*A[0], c*A[1], c*A[2], c*A[3], c*A[4], c*A[5], c*A[6]))
            else: T.append((c*A[0], c*A[1], c*A[2], c*A[4], c*A[3], -c*A[6], -c*A[5]))
        elif op[0] == 'exp':
            A = T[op[1]]; h1 = h2 = np.exp(A[0])
            sa = (A[2] - A[3]) * (A[4] - A[2])
            T.append((np.exp(A[0]), h1*A[1], h1*A[2], h1*A[3], h1*A[4],
                      neg(h2)/2*sa + pos(h1)*A[5] + neg(h1)*A[6],
                      pos(h2)/2*sa + pos(h1)*A[6] + neg(h1)*A[5]))
        elif op[0] == 'mul':
            A, B = T[op[1]], T[op[2]]; a, b = A[0], B[0]
            ell = sorted([b*A[3], b*A[4]]); ell2 = sorted([a*B[3], a*B[4]])
            Ecv = (pos(b)*A[5] + neg(b)*A[6] + pos(a)*B[5] + neg(a)*B[6]
                   + min((A[2]-A[3])*(B[2]-B[3]), (A[4]-A[2])*(B[4]-B[2])))
            Ecc = (pos(b)*A[6] + neg(b)*A[5] + pos(a)*B[6] + neg(a)*B[5]
                   + min((A[4]-A[2])*(B[2]-B[3]), (A[2]-A[3])*(B[4]-B[2])))
            T.append((a*b, b*A[1] + a*B[1], b*A[2] + a*B[2], ell[0]+ell2[0], ell[1]+ell2[1], Ecv, Ecc))
    return T

X, Y, Z = ('x', 0), ('x', 1), ('x', 2)
cases = {
  "exp(x)*y": ([X, Y, ('exp', 0), ('mul', 2, 1)], [(0.3, -0.4), (0.3, 0.0), (0.0, 0.0)]),
  "x*y*z": ([X, Y, Z, ('mul', 0, 1), ('mul', 3, 2)], [(0.5, -0.7, 1.2), (0.0, 0.0, 1.0)]),
  "exp(-x*y)*z": ([X, Y, Z, ('mul', 0, 1), ('scale', -1.0, 3), ('exp', 4), ('mul', 5, 2)],
                  [(0.6, 0.8, -1.1), (0.0, 0.5, 0.0)]),
  "exp(exp(x)*y - x)": ([X, Y, ('exp', 0), ('mul', 2, 1), ('scale', -1.0, 0), ('add', 3, 4), ('exp', 5)],
                  [(0.2, 0.7), (-0.3, -1.0)]),
}
for name, (expr, pts) in cases.items():
    for xs in pts:
        xs = np.array(xs, float); n = len(xs)
        errs = []
        for w in [1e-1, 1e-2, 1e-3]:
            e = 0.0
            for _ in range(300):
                dm = rng.uniform(0, 2, n) * (rng.random(n) > 0.1); dp = rng.uniform(0, 2, n) * (rng.random(n) > 0.1)
                xi = -dm + (dm + dp) * rng.random(n)
                face = rng.random(n) < 0.3; xi[face] = np.where(rng.random(face.sum()) < 0.5, -dm[face], dp[face])
                V = mccormick(expr, xs - w*dm, xs + w*dp, xs + w*xi)
                T = tangent(expr, xs, dm, dp, xi)
                for Vk, Tk in zip(V, T):
                    e = max(e, abs((Vk[3] - Vk[0])/w**2 + Tk[5]), abs((Vk[4] - Vk[0])/w**2 - Tk[6]))
            errs.append(e)
        print(f"{name:20s} x*={tuple(xs)}  max err w=1e-1,1e-2,1e-3: " + ", ".join(f"{v:.2e}" for v in errs))
