"""Independent exact re-evaluation (dossier check) of the stored powerflow certificates.
Rows come from a /tmp copy of pf_model.decode (+ leafcut planes for 0039 leaves); the
Lagrangian assembly, inner minimisation and PSD proof are written here.
PSD proof: exact rational LDL^T (natural order) of A + eps*I for the smallest eps in a
fine list; eps is the only rounding allowance."""
import json, sys, time
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/pfdossier/code")
import pf_model as pm
import leafcut as lc

def node_rows(M, info, box):
    (p1, p2), (q1, q2), (s1, s2) = box
    yb = dict(M["ybox"]); yb[info["Pg"]] = (p1, p2); yb[info["Qg"]] = (q1, q2)
    L = info["L"]
    extra = [dict(name="VBL", lin={}, Q={(2*L, 2*L): Fr(1), (2*L+1, 2*L+1): Fr(1)}, qy={}, lb=s1, ub=s2, kind="volt")]
    extra += lc.cut_rows3(info, box)
    return yb, list(M["rows"]) + extra

def lagrangian(M, rows, ybox, raw):
    assert len(rows) == len(raw)
    const = M["obj"]["const"]; kap = {y: Fr(0) for y in M["ys"]}; sig = {y: Fr(0) for y in M["ys"]}
    for y, c in M["obj"]["lin"].items(): kap[y] += c
    for y, c in M["obj"]["qy"].items(): sig[y] += c
    n2 = 2 * M["n"]; A = [[Fr(0)] * n2 for _ in range(n2)]
    stats = {}
    for r, rv in zip(rows, raw):
        if rv[0] == "eq":
            assert r["lb"] == r["ub"]
            w = Fr(rv[1]); const -= w * r["lb"]
        else:
            up = Fr(rv[1]) if rv[1] is not None and rv[1] > 0 else Fr(0)
            lo = Fr(rv[2]) if rv[2] is not None and rv[2] > 0 else Fr(0)
            if up: const -= up * r["ub"]
            if lo: const += lo * r["lb"]
            w = up - lo
        if w != 0:
            stats[r["kind"]] = stats.get(r["kind"], 0) + 1
        for y, c in r["lin"].items(): kap[y] += w * c
        for y, c in r["qy"].items(): sig[y] += w * c
        for (i, j), c in r["Q"].items():
            if i == j: A[i][i] += w * c
            else:
                A[i][j] += w * c / 2; A[j][i] += w * c / 2
    inner = Fr(0)
    for y in M["ys"]:
        s, k = sig[y], kap[y]
        assert s >= 0, ("sigma<0", y)
        if y in ybox:
            l, u = ybox[y]
            cands = [l, u] + ([min(max(-k / (2 * s), l), u)] if s > 0 else [])
            inner += min(s * t * t + k * t for t in cands)
        elif s > 0:
            inner -= k * k / (4 * s)
        else:
            assert k == 0, ("unbounded y", y, float(k))
    return const, inner, A, stats

def psd_ldl(A):
    """exact: True iff A is PSD (natural-order LDL^T with zero-pivot rule)."""
    n = len(A); A = [row[:] for row in A]
    for k in range(n):
        d = A[k][k]
        if d < 0: return False
        if d == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)): return False
            continue
        rk = A[k]
        nz = [j for j in range(k + 1, n) if rk[j] != 0]
        for i in nz:
            f = rk[i] / d; Ai = A[i]
            for j in nz:
                Ai[j] -= f * rk[j]
    return True

EPS = [Fr(0)] + [Fr(m, 10**e) for e in range(12, 4, -1) for m in (1, 2, 5)]

def certify(M, rows, ybox, raw):
    const, inner, A, stats = lagrangian(M, rows, ybox, raw)
    n2 = len(A); vm2 = sum(M["vmax2"])
    import numpy as np
    lam = float(np.linalg.eigvalsh(np.array([[float(a) for a in row] for row in A]))[0])
    cand = sorted(e for e in EPS if e == 0 or float(e) >= -lam * 1.01)
    for eps in cand:
        B = [[A[i][j] + (eps if i == j else 0) for j in range(n2)] for i in range(n2)]
        if psd_ldl(B):
            return const + inner - eps * vm2, eps, dict(stats, lam=lam), vm2
    return None, None, stats, vm2

def dec(x, d=12):
    q = x.numerator * 10**d // x.denominator
    s = str(q); return s[:-d] + "." + s[-d:]

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "root":
        for name in sys.argv[2:]:
            M = pm.decode(name)
            C = json.load(open(f"/tmp/pfdossier/data/{name}.sdpcert.json"))
            rows = M["rows"] if C["variant"] == "all rows" else [r for r in M["rows"] if r["kind"] != "angle"]
            t = time.time()
            b, eps, stats, vm2 = certify(M, rows, M["ybox"], C["raw"])
            print(f"{name}: rows {len(rows)} nonzero multipliers by kind {stats}; eps {eps}; bound floor(1e12) {dec(b)}; "
                  f"stored {dec(Fr(C['bound_exact']))}; diff {float(b - Fr(C['bound_exact'])):.3g}; sum vmax^2 {float(vm2)}; {time.time()-t:.1f}s")
    else:
        name, tag = sys.argv[2], sys.argv[3]
        M = pm.decode(name); info = lc.leaf_info(M)
        D = json.load(open(f"/tmp/pfdossier/data/{name}.{tag}.json"))
        mins = []
        for Lf in D["leaves"]:
            box = tuple((Fr(a), Fr(c)) for a, c in Lf["box"])
            yb, rows = node_rows(M, info, box)
            b, eps, stats, vm2 = certify(M, rows, yb, Lf["raw"])
            st = Fr(Lf["bound"])
            mins.append(b)
            cuts = [(r["name"], rv) for r, rv in zip(rows, Lf["raw"]) if r["kind"] == "cut"]
            cutw = sum(Fr(rv[1]) for _, rv in cuts if rv[1] and rv[1] > 0)
            print(f"  box {[[float(a), float(c)] for a, c in box]}: eps {eps}, own {dec(b)} stored {dec(st)} own-stored {float(b-st):.2e}; "
                  f"nonzero by kind {stats}; total cut multiplier {float(cutw):.4g}")
        print(f"{name}.{tag}: min over leaves {dec(min(mins), 14)}")
