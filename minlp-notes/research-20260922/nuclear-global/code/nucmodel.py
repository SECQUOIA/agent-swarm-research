"""Exact structured description of the MINLPLib nuclear* instances, and its exact verification.

load(name) -> Inst: data (G, V, c, a, KF, N, T, family) and OSiL variable indices by role.
verify(inst) regenerates every row and every variable bound of the OSiL file from the
structured description and compares them exactly (Fractions, rows up to multiplication by -1).
If verify() passes, the structured description IS the instance, so statements proved for the
structured model (e.g. the power-variable reformulation, see reform.py) hold for the file.

Row roles (0-based node i, time t = 0..T-1):
  eigen   -lam_t phi_it + sum_j G_ij phi_jt k_jt = 0
  burn    k_{i,t+1} - k_it + a phi_it k_it = 0            (t < T-1)
  norm    sum_i V_i phi_it k_it = 1
  peak    phi_it k_it <= c_it
  F1: tie    y_ig - y_jg = 0 for the tied half-node pairs (va-vf only);
      node   sum_g y_ig = 1 ;  type  sum_i V_i y_ig = 1 ;  copy  ycopy_ig - y_ig = 0 (14/25/49/104 only)
      k1     k_i0 - KF sum_{g fresh} y_ig - sum_{g old} Y_ig kappa_g = 0   (Y = copy if present)
      kappa  kappa_g - sum_j V_j k_{j,T-1} y_{j,pred g} = 0
  F2: k1     k_i0 - KF b0_i - sum_j b_ij k_{j,T-1} = 0 ; node b0_i + sum_j b_ij = 1 ;
      fuel   sum_i b_ij <= 1 ; fresh  sum_i b0_i = nfresh
  F3: k1     k_i0 - KF b0_i - sum_j z_ij = 0 ; z_ij - k_{j,T-1} <= 0 ; z_ij - KF b_ij <= 0 ; node, fuel, fresh as F2
  objective  min -lam_{T-1}
"""
import os, sys, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "../../benchmark-observations/code/review_nuclear"))
from parse import load as parse_load   # exact OSiL parser (Fractions), written by the reviewer
import nstruct                          # reviewer's role detection for phi, k, lam, G, V, peak

INF = "INF"; NINF = "-INF"


class Inst:
    pass


def load(name):
    Vv, C, O, rep, S = nstruct.analyze(name)
    I = Inst(); I.name = name; I.vars = Vv; I.rows = C; I.obj = O
    N, T = S["N"], S["T"]; I.N, I.T = N, T
    I.k = [[S["kvar"][(i, t)] for t in range(T)] for i in range(N)]
    I.phi = [[S["phi"][(i, t)] for t in range(T)] for i in range(N)]
    I.lam = [S["lam"][t] for t in range(T)]
    I.G = [[S["G"].get((i, j), F(0)) for j in range(N)] for i in range(N)]
    I.V = [S["Vw"][i] for i in range(N)]
    I.c = [[S["peak"][(i, t)] for t in range(T)] for i in range(N)]
    (I.a,) = rep["alpha"]
    isB = lambda j: Vv[j]["type"] == "B"
    # k1 row of node i: the only row with coefficient +1 on k_{i,0}
    k1row = []
    for i in range(N):
        rr = [r for r, c in enumerate(C) if c["lin"].get(I.k[i][0]) == 1]
        assert len(rr) == 1; k1row.append(rr[0])
    kT = {I.k[j][T - 1]: j for j in range(N)}
    alias = {}
    for c in C:
        if c["lb"] == c["ub"] == 0 and not c["quad"] and len(c["lin"]) == 2 and sorted(c["lin"].values()) == [-1, 1]:
            a, b = c["lin"]
            if isB(a) and not isB(b): alias[b] = a
            if isB(b) and not isB(a): alias[a] = b
    r0 = C[k1row[0]]
    KFs = {-v for j, v in r0["lin"].items() if isB(j)}
    assert len(KFs) == 1; I.KF = KFs.pop()
    if r0["quad"] and all((a in kT) != (b in kT) for a, b in r0["quad"]):
        I.fam = "F2"
    elif r0["quad"]:
        I.fam = "F1"
    else:
        I.fam = "F3"
    if I.fam in ("F2", "F3"):
        I.b0 = [None] * N; I.b = [[None] * N for _ in range(N)]; I.z = [[None] * N for _ in range(N)]
        for i in range(N):
            c = C[k1row[i]]
            (I.b0[i],) = [j for j, v in c["lin"].items() if isB(j)]
            if I.fam == "F2":
                for (a, b) in c["quad"]:
                    bb, kk = (a, b) if b in kT else (b, a)
                    I.b[i][kT[kk]] = bb
            else:
                for zz in [j for j, v in c["lin"].items() if v == -1]:
                    r1 = [cc for cc in C if cc["lb"] == NINF and cc["ub"] == 0 and not cc["quad"] and cc["lin"].get(zz) == 1]
                    js = [kT[j] for cc in r1 for j in cc["lin"] if j in kT]
                    bs = [j for cc in r1 for j in cc["lin"] if isB(j)]
                    assert len(js) == 1 and len(bs) == 1
                    I.z[i][js[0]] = zz; I.b[i][js[0]] = bs[0]
        fr = [c for c in C if c["lb"] == c["ub"] and set(c["lin"]) == set(I.b0)]
        assert len(fr) == 1; I.nfresh = fr[0]["lb"]
    else:
        canon = lambda j: alias.get(j, j)
        node_of, kap_of, fresh_bins = {}, {}, set()
        for i in range(N):
            c = C[k1row[i]]
            for j in c["lin"]:
                if j != I.k[i][0]: node_of[j] = i; fresh_bins.add(j)
            for (a, b) in c["quad"]:
                y, kap = (a, b) if isB(canon(a)) else (b, a)
                node_of[canon(y)] = i; kap_of[canon(y)] = kap
        typerows = [c for c in C if c["lb"] == c["ub"] == 1 and not c["quad"] and all(j in node_of for j in c["lin"])
                    and len({node_of[j] for j in c["lin"]}) == N == len(c["lin"])]
        ng = len(typerows); I.ntypes = ng
        I.y = [[None] * ng for _ in range(N)]
        I.ycopy = [[None] * ng for _ in range(N)]
        I.fresh = [None] * ng; I.kappa = [None] * ng; I.pred = [None] * ng
        for g, c in enumerate(typerows):
            for j in c["lin"]:
                I.y[node_of[j]][g] = j
            I.fresh[g] = all(j in fresh_bins for j in c["lin"])
            if not I.fresh[g]:
                ks = {kap_of[j] for j in c["lin"]}; assert len(ks) == 1; I.kappa[g] = ks.pop()
        inv = {v: k for k, v in alias.items()}
        for i in range(N):
            for g in range(ng):
                I.ycopy[i][g] = inv.get(I.y[i][g])
        gofbin = {I.y[i][g]: g for i in range(N) for g in range(ng)}
        gofkap = {I.kappa[g]: g for g in range(ng) if I.kappa[g] is not None}
        for c in C:
            if len(c["lin"]) == 1 and next(iter(c["lin"])) in gofkap and c["quad"]:
                g = gofkap[next(iter(c["lin"]))]
                ps = set()
                for (a, b) in c["quad"]:
                    y = a if canon(a) in gofbin else b
                    ps.add(gofbin[canon(y)])
                assert len(ps) == 1; I.pred[g] = ps.pop()
                # which variable (binary or copy) the kappa row uses
                I.kapuse_copy = any(a in alias or b in alias for (a, b) in c["quad"])
        assert all(I.fresh[g] or I.pred[g] is not None for g in range(ng))
        # tie rows y_ig - y_jg = 0 (va-vf: the two pairs of diagonal half-nodes carry the same type)
        ties = collections.defaultdict(set)
        for c in C:
            if c["lb"] == c["ub"] == 0 and not c["quad"] and len(c["lin"]) == 2 and all(j in gofbin for j in c["lin"]):
                a, b = c["lin"]; assert gofbin[a] == gofbin[b] and sorted(c["lin"].values()) == [-1, 1]
                ties[tuple(sorted((node_of[a], node_of[b])))].add(gofbin[a])
        assert all(v == set(range(ng)) for v in ties.values())
        I.ties = sorted(ties)
    return I


def regenerate(I):
    """All rows of the structured model as (lb, ub, lin, quad) with Fraction data."""
    N, T, rows = I.N, I.T, []
    q = lambda a, b: (min(a, b), max(a, b))
    for t in range(T):
        for i in range(N):
            Q = {q(I.lam[t], I.phi[i][t]): F(-1)}
            for j in range(N):
                if I.G[i][j]: Q[q(I.phi[j][t], I.k[j][t])] = Q.get(q(I.phi[j][t], I.k[j][t]), 0) + I.G[i][j]
            rows.append((0, 0, {}, Q))
            if t < T - 1:
                rows.append((0, 0, {I.k[i][t + 1]: F(1), I.k[i][t]: F(-1)}, {q(I.phi[i][t], I.k[i][t]): I.a}))
            rows.append((NINF, I.c[i][t], {}, {q(I.phi[i][t], I.k[i][t]): F(1)}))
        rows.append((1, 1, {}, {q(I.phi[i][t], I.k[i][t]): I.V[i] for i in range(N)}))
    kT = [I.k[j][T - 1] for j in range(N)]
    if I.fam == "F1":
        ng = I.ntypes
        Y = lambda i, g: I.ycopy[i][g] if I.ycopy[i][g] is not None else I.y[i][g]
        for i in range(N):
            rows.append((1, 1, {I.y[i][g]: F(1) for g in range(ng)}, {}))
            lin = {I.k[i][0]: F(1)}; Q = {}
            for g in range(ng):
                if I.fresh[g]: lin[I.y[i][g]] = -I.KF
                else: Q[q(Y(i, g), I.kappa[g])] = F(-1)
            rows.append((0, 0, lin, Q))
            for g in range(ng):
                if I.ycopy[i][g] is not None:
                    rows.append((0, 0, {I.ycopy[i][g]: F(1), I.y[i][g]: F(-1)}, {}))
        for (i, j) in I.ties:
            for g in range(ng):
                rows.append((0, 0, {I.y[i][g]: F(1), I.y[j][g]: F(-1)}, {}))
        for g in range(ng):
            rows.append((1, 1, {I.y[i][g]: I.V[i] for i in range(N)}, {}))
            if not I.fresh[g]:
                pg = I.pred[g]
                yy = (lambda j: Y(j, pg)) if I.kapuse_copy else (lambda j: I.y[j][pg])
                rows.append((0, 0, {I.kappa[g]: F(1)}, {q(yy(j), kT[j]): -I.V[j] for j in range(N)}))
    else:
        for i in range(N):
            rows.append((1, 1, {I.b0[i]: F(1), **{I.b[i][j]: F(1) for j in range(N)}}, {}))
            if I.fam == "F2":
                rows.append((0, 0, {I.k[i][0]: F(1), I.b0[i]: -I.KF}, {q(I.b[i][j], kT[j]): F(-1) for j in range(N)}))
            else:
                rows.append((0, 0, {I.k[i][0]: F(1), I.b0[i]: -I.KF, **{I.z[i][j]: F(-1) for j in range(N)}}, {}))
                for j in range(N):
                    rows.append((NINF, 0, {I.z[i][j]: F(1), kT[j]: F(-1)}, {}))
                    rows.append((NINF, 0, {I.z[i][j]: F(1), I.b[i][j]: -I.KF}, {}))
        for j in range(N):
            rows.append((NINF, 1, {I.b[i][j]: F(1) for i in range(N)}, {}))
        rows.append((I.nfresh, I.nfresh, {I.b0[i]: F(1) for i in range(N)}, {}))
    return rows


def canon_row(lb, ub, lin, quad, const=0):
    """Canonical key; rows equal up to multiplication by -1 get the same key."""
    lin = {j: F(v) for j, v in lin.items() if v != 0}; quad = {k: F(v) for k, v in quad.items() if v != 0}
    lb = lb if lb == NINF else F(lb) - const; ub = ub if ub == INF else F(ub) - const
    terms = sorted([(("L", j), v) for j, v in lin.items()] + [(("Q",) + k, v) for k, v in quad.items()])
    if terms[0][1] < 0:
        terms = [(k, -v) for k, v in terms]
        lb, ub = (NINF if ub == INF else -ub), (INF if lb == NINF else -lb)
    return (str(lb), str(ub), tuple((k, str(v)) for k, v in terms))


def verify(I):
    file_rows = collections.Counter(canon_row(c["lb"], c["ub"], c["lin"], c["quad"], c["const"]) for c in I.rows)
    gen_rows = collections.Counter(canon_row(*r) for r in regenerate(I))
    assert file_rows == gen_rows, ("row mismatch", len(file_rows - gen_rows), len(gen_rows - file_rows))
    # objective
    assert I.obj["sense"] == "min" and I.obj["lin"] == {I.lam[I.T - 1]: -1} and not I.obj.get("quad") and I.obj["const"] == 0
    # variable roles cover all variables exactly once; record bounds by role
    N, T = I.N, I.T
    roles = {}
    def put(j, r):
        assert j not in roles, (j, r, roles.get(j)); roles[j] = r
    for i in range(N):
        for t in range(T):
            put(I.phi[i][t], "phi"); put(I.k[i][t], "k")
    for t in range(T): put(I.lam[t], "lam")
    if I.fam == "F1":
        for i in range(N):
            for g in range(I.ntypes):
                put(I.y[i][g], "bin")
                if I.ycopy[i][g] is not None: put(I.ycopy[i][g], "copy")
        for g in range(I.ntypes):
            if I.kappa[g] is not None: put(I.kappa[g], "kappa")
    else:
        for i in range(N):
            put(I.b0[i], "bin")
            for j in range(N):
                put(I.b[i][j], "bin")
                if I.fam == "F3": put(I.z[i][j], "z")
    assert len(roles) == len(I.vars)
    bnd = collections.defaultdict(set)
    for j, r in roles.items():
        v = I.vars[j]; bnd[r].add((v["type"], str(v["lb"]), str(v["ub"])))
    assert bnd["bin"] == {("B", "0", "1")}
    assert all(t == "C" for r in bnd if r != "bin" for t, _, _ in bnd[r])
    return {r: sorted(s) for r, s in bnd.items()}


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        I = load(nm); b = verify(I)
        extra = (f" types={I.ntypes} fresh={sum(I.fresh)} ties={I.ties} kappa_uses_copy={I.kapuse_copy}" if I.fam == "F1"
                 else f" nfresh={I.nfresh}")
        print(f"{nm}: {len(I.rows)} rows regenerated exactly; fam={I.fam} N={I.N} T={I.T} a={I.a} KF={I.KF} "
              f"V={sorted(set(map(str, I.V)))} c={sorted(set(str(x) for r in I.c for x in r))}{extra}")
        print("   variable bounds by role:", {r: [(lb[:14], ub) for _, lb, ub in s] for r, s in b.items()})
