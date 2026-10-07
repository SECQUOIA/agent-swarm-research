"""M-limits checks for Prop prop:lbproduct (appendix-lbproduct.tex): encoding, values,
uniqueness, Hessian diagonal, decomposition, and the isolation lemma on small cases."""
from itertools import product, combinations
from math import comb
import random
import sympy as sp

random.seed(7)
ok = True


def check(c, msg):
    global ok
    if not c:
        ok = False
        print("FAIL:", msg)


def pair_table(Ecd, N0, W0, w):
    """For each (xc,xd) compute min over pair variables of W0*Phi_cd + sum w zeta,
    the number of minimizers, and the min of Phi_cd."""
    m = len(Ecd)
    res = {}
    choices = list(product([0, 1], [0, 1], range(N0 + 1), range(N0 + 1)))
    for xc in range(1, N0 + 1):
        for xd in range(1, N0 + 1):
            best = None
            nbest = 0
            minphi = None
            for tup in product(choices, repeat=m):
                sig0 = y0 = yp0 = 0
                phi = 0
                lin = 0
                for l, (zeta, sig, y, yp) in enumerate(tup):
                    a, b = Ecd[l]
                    phi += (sig - sig0 - zeta) ** 2 + (y - y0 - a * zeta) ** 2 + (yp - yp0 - b * zeta) ** 2
                    lin += w[(a, b)] * zeta
                    sig0, y0, yp0 = sig, y, yp
                phi += (sig0 - 1) ** 2 + (y0 - xc) ** 2 + (yp0 - xd) ** 2
                val = W0 * phi + lin
                if minphi is None or phi < minphi:
                    minphi = phi
                if best is None or val < best:
                    best, nbest = val, 1
                elif val == best:
                    nbest += 1
            res[(xc, xd)] = (best, nbest, minphi)
    return res


def run(k, N0, E):
    Etot = sum(len(v) for v in E.values())
    W0 = 1 + comb(k, 2) * 2 * Etot
    w = {}
    for cd in E:
        for e in E[cd]:
            w[(cd, e)] = random.randint(1, 2 * Etot)
    tables = {}
    for cd in E:
        wl = {e: w[(cd, e)] for e in E[cd]}
        tables[cd] = pair_table(E[cd], N0, W0, wl)
    # Phi=0 iff (xc,xd) in E_cd
    for cd in E:
        for (xc, xd), (best, nb, minphi) in tables[cd].items():
            check((minphi == 0) == ((xc, xd) in E[cd]), "Phi_cd=0 iff edge")
            if (xc, xd) in E[cd]:
                check(nb == 1, "encoding of an edge not unique")
                check(best == w[(cd, (xc, xd))], "value at encoding")
            else:
                check(best >= W0, "Phi>=1 gives >=W0")
    # global minimum over x
    vals = []
    for x in product(range(1, N0 + 1), repeat=k):
        tot = 0
        nmin = 1
        for (c, d) in E:
            best, nb, _ = tables[(c, d)][(x[c], x[d])]
            tot += best
            nmin *= nb
        vals.append((tot, nmin, x))
    vals.sort()
    opt = vals[0][0]
    cliques = [x for x in product(range(1, N0 + 1), repeat=k)
               if all((x[c], x[d]) in E[(c, d)] for (c, d) in E)]
    if cliques:
        check(opt <= W0 - 1, "OPT <= W0-1 when clique exists")
        cw = sorted(sum(w[((c, d), (x[c], x[d]))] for (c, d) in E) for x in cliques)
        uniq = len(cw) == 1 or cw[0] < cw[1]
        nopt = sum(v[1] for v in vals if v[0] == opt)
        check((nopt == 1) == uniq, "unique minimizer iff unique min-weight clique")
        return True, uniq
    else:
        check(opt >= W0, "no clique: OPT >= W0")
        return False, None


stats = {"yes": 0, "uniq": 0, "no": 0}
for trial in range(25):
    k = random.choice([2, 3])
    N0 = 2
    E = {}
    for c, d in combinations(range(k), 2):
        allp = [(a, b) for a in range(1, N0 + 1) for b in range(1, N0 + 1)]
        mcd = random.randint(1, 2 if k == 3 else 3)
        E[(c, d)] = random.sample(allp, mcd)
    yes, u = run(k, N0, E)
    if yes:
        stats["yes"] += 1
        stats["uniq"] += bool(u)
    else:
        stats["no"] += 1
print("lbproduct encoding:", stats)

# Hessian diagonal bound and variable count (symbolic) for a random k=3 instance
k, N0 = 4, 3
E = {}
for c, d in combinations(range(k), 2):
    allp = [(a, b) for a in range(1, N0 + 1) for b in range(1, N0 + 1)]
    E[(c, d)] = random.sample(allp, random.randint(1, 5))
Etot = sum(len(v) for v in E.values())
W0 = 1 + comb(k, 2) * 2 * Etot
xs = sp.symbols(f'x0:{k}')
Phi = 0
nvars = k
bags = [set(f'x{c}' for c in range(k))]
for (c, d), lst in E.items():
    mm = len(lst)
    z = sp.symbols(f'z{c}{d}_1:{mm + 1}')
    s = sp.symbols(f's{c}{d}_1:{mm + 1}')
    y = sp.symbols(f'y{c}{d}_1:{mm + 1}')
    yp = sp.symbols(f'yp{c}{d}_1:{mm + 1}')
    nvars += 4 * mm
    s0 = y0 = yp0 = 0
    for l, (a, b) in enumerate(lst):
        Phi += (s[l] - s0 - z[l]) ** 2 + (y[l] - y0 - a * z[l]) ** 2 + (yp[l] - yp0 - b * z[l]) ** 2
        s0, y0, yp0 = s[l], y[l], yp[l]
    Phi += (s0 - 1) ** 2 + (y0 - xs[c]) ** 2 + (yp0 - xs[d]) ** 2
Psi = W0 * Phi
allv = sorted(Psi.free_symbols, key=str)
maxdiag = max(sp.diff(Psi, v, 2) for v in allv)
check(maxdiag <= W0 * (2 + 4 * N0 ** 2 + 2 * k), "Hessian diagonal bound")
check(nvars <= k + 2 * k * k * N0 * N0, "variable count bound")
print("lbproduct: max diag =", maxdiag, "bound =", W0 * (2 + 4 * N0 ** 2 + 2 * k), "n =", nvars)

# isolation lemma exact probability on a tiny family
U = list(range(4))
fam = [frozenset(s) for s in [(0, 1), (1, 2), (2, 3), (0, 3), (0, 2)]]
rho = 8
good = 0
tot = 0
for wv in product(range(1, rho + 1), repeat=len(U)):
    vals = sorted(sum(wv[e] for e in Z) for Z in fam)
    tot += 1
    good += vals[0] < vals[1]
check(good / tot >= 1 - len(U) / rho, "isolation bound")
print("isolation: Pr[unique] =", good / tot, ">=", 1 - len(U) / rho)

# psi' construction of the last claim: p/psi'(p) >= max(a(p), C) for p >= C
import math
for C in [1, 2, 5]:
    for psi in [lambda p: max(1.0, math.log2(p + 1)), lambda p: max(1.0, p ** 0.5)]:
        for p in range(C, 200):
            psip = max(1.0, min(psi(p), p / C))
            check(p / psip >= max(p / psi(p), C) - 1e-9, "psi' bound")
print("ALL OK" if ok else "SOME FAILURES")
