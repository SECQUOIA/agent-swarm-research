#!/usr/bin/env python3
"""Exact checks: conditioning of the Del Pia--Khajavirad treewidth-two reduction.

Builds the objective (20)-(24) of arXiv:2609.35595v1 (Theorem 3) for the
two-item Subset Sum instance a=(B,B-1), T=B, assembles the dense Hessian
independently by expanding every square, and verifies
  * max Hessian diagonal = 10 (so L=10 is the exact coordinate curvature),
  * unique zero v* (binary solution (1,0) only),
  * binary witness (0,1): Psi = 1/D^2, ||y'-v*||^2 >= 2 ell  => kappa >= 20 ell D^2,
  * fractional witness (1/B,1): Psi = c q/B, d^T H d = -2c(q^2+1)  => nu/g >= 2B(q+1/q) >= 4B.
"""
from fractions import Fraction as Fr


def instance(a, T):
    n = len(a)
    U = sum(a)
    ell = (U + 1 - 1).bit_length() if U > 0 else 1
    # ell = ceil(log2(U+1))
    ell = 0
    while 2 ** ell < U + 1:
        ell += 1
    D = 2 ** ell
    bits = [[(ai >> k) & 1 for k in range(ell)] for ai in a]
    tb = [(T >> k) & 1 for k in range(ell)]
    names = []
    for i in range(n):
        names += [f'x{i}_{k}' for k in range(ell)]
    for i in range(n):
        names += [f'z{i}_{k}' for k in range(ell)]
    names += [f's{i}' for i in range(n)] + [f'w{k}' for k in range(ell)]
    idx = {nm: j for j, nm in enumerate(names)}
    squares = []  # (dict var->coef, const)

    def V(nm):
        return nm
    for i in range(n):
        for k in range(1, ell):
            squares.append(({f'x{i}_{k}': 1, f'x{i}_{k-1}': -1}, 0))
        for k in range(ell):
            d = {f'z{i}_{k}': 2}
            if k > 0:
                d[f'z{i}_{k-1}'] = d.get(f'z{i}_{k-1}', 0) - 1
            if bits[i][k]:
                d[f'x{i}_{k}'] = d.get(f'x{i}_{k}', 0) - 1
            squares.append((d, 0))
        d = {f's{i}': 1, f'z{i}_{ell-1}': -1}
        if i > 0:
            d[f's{i-1}'] = -1
        squares.append((d, 0))
    for k in range(ell):
        d = {f'w{k}': 2}
        if k > 0:
            d[f'w{k-1}'] = -1
        squares.append((d, -tb[k]))
    squares.append(({f's{n-1}': 1, f'w{ell-1}': -1}, 0))
    pen = [f'x{i}_0' for i in range(n)]  # endpoint penalties x_{i1}(1-x_{i1})
    return dict(n=n, ell=ell, D=D, names=names, idx=idx, squares=squares, pen=pen, bits=bits, tb=tb)


def hessian(inst, c=Fr(1)):
    N = len(inst['names'])
    H = [[Fr(0)] * N for _ in range(N)]
    for d, _ in inst['squares']:
        items = [(inst['idx'][k], Fr(v)) for k, v in d.items()]
        for i, ai in items:
            for j, aj in items:
                H[i][j] += 2 * ai * aj
    for nm in inst['pen']:
        j = inst['idx'][nm]
        H[j][j] += -2 * c
    return H


def value(inst, y, c=Fr(1)):
    tot = Fr(0)
    for d, const in inst['squares']:
        r = sum(Fr(v) * y[k] for k, v in d.items()) + const
        tot += r * r
    for nm in inst['pen']:
        tot += c * y[nm] * (1 - y[nm])
    return tot


def point(inst, a, choices):
    n, ell, D = inst['n'], inst['ell'], inst['D']
    y = {}
    for i in range(n):
        for k in range(ell):
            y[f'x{i}_{k}'] = Fr(choices[i])
        prev = Fr(0)
        for k in range(ell):
            prev = (prev + inst['bits'][i][k] * Fr(choices[i])) / 2
            y[f'z{i}_{k}'] = prev
    acc = Fr(0)
    for i in range(n):
        acc += Fr(a[i]) * Fr(choices[i]) / D
        y[f's{i}'] = acc
    prev = Fr(0)
    for k in range(ell):
        prev = (prev + inst['tb'][k]) / 2
        y[f'w{k}'] = prev
    return y


def main():
    Bs = list(range(3, 40)) + [2 ** m for m in range(2, 13)] + [2 ** 30, 2 ** 64 + 5]
    count = 0
    for B in Bs:
        a, T = [B, B - 1], B
        inst = instance(a, T)
        ell, D = inst['ell'], inst['D']
        assert 2 ** ell >= 2 * B and 2 ** (ell - 1) < 2 * B  # ell = ceil(log2(2B))
        dense = B <= 2 ** 12
        H = hessian(inst) if dense else None
        if dense:
            diag = [H[j][j] for j in range(len(H))]
            assert max(diag) == 10, (B, max(diag))
        vstar = point(inst, a, [1, 0])
        assert value(inst, vstar) == 0
        assert all(0 <= x <= 1 for x in vstar.values())
        # binary solutions of B u1 + (B-1) u2 = B
        assert [(u1, u2) for u1 in (0, 1) for u2 in (0, 1) if B * u1 + (B - 1) * u2 == B] == [(1, 0)]
        # binary witness (0,1): only the final square is nonzero
        yb = point(inst, a, [0, 1])
        assert value(inst, yb) == Fr(1, D * D)
        Rb = sum((yb[k] - vstar[k]) ** 2 for k in vstar)
        assert Rb >= 2 * ell
        g_upper_b = Fr(1, D * D) / Rb
        assert 10 / g_upper_b >= 20 * ell * D * D
        # fractional witness (1/B, 1)
        yf = point(inst, a, [Fr(1, B), 1])
        assert all(0 <= x <= 1 for x in yf.values())
        q = Fr(B - 1, B)
        for c in (Fr(1), Fr(1, 7), Fr(13)):
            assert value(inst, yf, c) == c * q / B
            d = {k: yf[k] - vstar[k] for k in vstar}
            R = sum(x * x for x in d.values())
            assert R >= ell * (q * q + 1)
            if dense:
                Hc = hessian(inst, c)
                names = inst['names']
                dv = [d[nm] for nm in names]
                quad = sum(dv[i] * Hc[i][j] * dv[j] for i in range(len(dv)) for j in range(len(dv)) if Hc[i][j])
            else:  # residual representation (all affine residuals vanish along d)
                quad = -2 * c * (d['x0_0'] ** 2 + d['x1_0'] ** 2)
            assert quad == -2 * c * (q * q + 1)
            g_up = c * q / B / R
            nu_low = -quad / R
            assert nu_low / g_up == 2 * B * (q * q + 1) / q >= 4 * B
            count += 1
    print(f'PASS: {len(Bs)} instances (dense Hessian for B<=4096), {count} weight cases; '
          f'max diag 10; kappa >= 20 ell D^2; nu/g >= 4B')


if __name__ == '__main__':
    main()
