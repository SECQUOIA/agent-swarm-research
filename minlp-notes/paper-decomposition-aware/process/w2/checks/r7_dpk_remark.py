"""R7 check: Remark lim:rem:dk numbers against Del Pia--Khajavirad Theorem 3 construction (20)-(24).

Builds Psi for the two-item Subset Sum instance a=(B,B-1), T=B in exact arithmetic and checks
(i) number of variables 5*ell+2 and ell = ceil(log2(2B)), D = 2^ell;
(ii) the encoding of (1,0) is a zero of Psi; (iii) the exact encoding of (0,1) has Psi = 1/D^2;
(iv) the largest diagonal entry of the Hessian of Psi is 10;
(v) ||y'-v*||^2 >= 2*ell for the two encodings;
(vi) the fractional choice (1/B, 1) has Psi = q/B with q = 1-1/B and all residual squares zero.
"""
from fractions import Fraction as Fr
import math, sys

def build(B):
    a = [B, B - 1]; T = B; U = sum(a)
    ell = math.ceil(math.log2(U + 1)); D = 2 ** ell
    bits = lambda v: [(v >> (r)) & 1 for r in range(ell)]  # b_{r+1} = bit r
    b = [bits(ai) for ai in a]; t = bits(T)
    n = 2
    names = [f"x{i}_{k}" for i in range(n) for k in range(ell)] + \
            [f"z{i}_{k}" for i in range(n) for k in range(ell)] + \
            [f"s{i}" for i in range(n)] + [f"w{k}" for k in range(ell)]
    idx = {nm: j for j, nm in enumerate(names)}
    # each term: (list of (coef,var or None const)) squared, or x(1-x)
    sq = []  # list of dict var->coef plus const
    conc = []  # vars with x(1-x)
    for i in range(n):
        conc.append(idx[f"x{i}_0"])
        for k in range(1, ell):
            sq.append(({idx[f"x{i}_{k}"]: 1, idx[f"x{i}_{k-1}"]: -1}, 0))
        for k in range(ell):
            d = {idx[f"z{i}_{k}"]: 2}
            if k > 0: d[idx[f"z{i}_{k-1}"]] = d.get(idx[f"z{i}_{k-1}"], 0) - 1
            if b[i][k]: d[idx[f"x{i}_{k}"]] = d.get(idx[f"x{i}_{k}"], 0) - b[i][k]
            sq.append((d, 0))
        d = {idx[f"s{i}"]: 1, idx[f"z{i}_{ell-1}"]: -1}
        if i > 0: d[idx[f"s{i-1}"]] = -1
        sq.append((d, 0))
    for k in range(ell):
        d = {idx[f"w{k}"]: 2}
        if k > 0: d[idx[f"w{k-1}"]] = -1
        sq.append((d, -t[k]))
    sq.append(({idx[f"s{n-1}"]: 1, idx[f"w{ell-1}"]: -1}, 0))
    return a, T, ell, D, names, idx, sq, conc, b, t

def psi(y, sq, conc):
    v = Fr(0)
    for d, c in sq:
        r = Fr(c) + sum(Fr(co) * y[j] for j, co in d.items()); v += r * r
    for j in conc: v += y[j] * (1 - y[j])
    return v

def encode(xbar, a, ell, D, names, idx, b, t, frac=None):
    y = [Fr(0)] * len(names); n = 2
    xs = frac if frac is not None else xbar
    for i in range(n):
        for k in range(ell): y[idx[f"x{i}_{k}"]] = Fr(xs[i])
        for k in range(ell):
            y[idx[f"z{i}_{k}"]] = Fr(xs[i]) / 2 ** (k + 1) * sum(b[i][r] * 2 ** r for r in range(k + 1))
    run = Fr(0)
    for i in range(n):
        run += Fr(a[i]) * Fr(xs[i]) / D; y[idx[f"s{i}"]] = run
    for k in range(ell):
        y[idx[f"w{k}"]] = Fr(1, 2 ** (k + 1)) * sum(t[r] * 2 ** r for r in range(k + 1))
    return y

def hess_diag(names, sq, conc):
    h = [Fr(0)] * len(names)
    for d, c in sq:
        for j, co in d.items(): h[j] += 2 * co * co
    for j in conc: h[j] -= 2
    return h

ok = True
for B in [3, 4, 5, 8, 16, 32]:
    a, T, ell, D, names, idx, sq, conc, b, t = build(B)
    assert ell == math.ceil(math.log2(2 * B)) and D >= 2 * B
    nv = len(names); ok &= nv == 5 * ell + 2
    vstar = encode([1, 0], a, ell, D, names, idx, b, t)
    yp = encode([0, 1], a, ell, D, names, idx, b, t)
    p0, p1 = psi(vstar, sq, conc), psi(yp, sq, conc)
    dist2 = sum((u - v) ** 2 for u, v in zip(vstar, yp))
    hd = max(hess_diag(names, sq, conc))
    q = 1 - Fr(1, B)
    yf = encode(None, a, ell, D, names, idx, b, t, frac=[Fr(1, B), 1])
    pf = psi(yf, sq, conc)
    inbox = all(0 <= v <= 1 for v in yf)
    res = (p0 == 0, p1 == Fr(1, D * D), dist2 >= 2 * ell, hd == 10, pf == q / B, inbox)
    ok &= all(res)
    extra = f" (B=2^m: 5m+7={5*int(math.log2(B))+7})" if B & (B - 1) == 0 else ""
    print(f"B={B} ell={ell} D={D} vars={nv}{extra} Psi(v*)={p0} Psi(y')={p1} dist2={dist2} maxdiag={hd} Psi(frac)={pf} q/B={q/B} inbox={inbox} -> {res}")
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
