"""Reviewer's structure detection for the nuclear* OSiL files (exact Fractions).

Every row is classified by its algebraic shape; the script asserts that each row gets exactly one role,
that the recovered data regenerate the row, and reports N, T, a, KF, V, c, the F1 fuel-type structure
(fresh types, predecessor chains, tie rows, copy rows) and the variable bounds by role.
"""
import sys
from collections import defaultdict, Counter
from fractions import Fraction as F
import osil


class Nuc:
    pass


def analyze(name, verbose=False):
    M = osil.read(name)
    V, rows = M["vars"], M["rows"]
    isB = lambda j: V[j]["type"] == "B"
    role = [None] * len(rows)

    def setrole(r, x):
        assert role[r] is None, (r, role[r], x); role[r] = x

    # --- burnup rows: c*k' - c*k + q*phi*k = 0, the quad pair shares k with the linear part
    nxt, phi_of, avals = {}, {}, set()
    for r, R in enumerate(rows):
        if R["lb"] == R["ub"] == 0 and len(R["lin"]) == 2 and len(R["quad"]) == 1 and not any(isB(j) for j in R["lin"]):
            (pr, q), = R["quad"].items()
            common = set(pr) & set(R["lin"])
            if len(common) != 1: continue
            (k,) = common; (kn,) = set(R["lin"]) - {k}; (ph,) = set(pr) - {k}
            ck, ckn = R["lin"][k], R["lin"][kn]
            assert ck == -ckn
            # row: ckn*kn + ck*k + q*ph*k = 0  ->  kn = k - (q/ckn) ph k
            avals.add(q / ckn)
            assert k not in nxt; nxt[k] = kn; phi_of[k] = ph
            setrole(r, "burn")
    assert len(avals) == 1; (a,) = avals; assert a > 0
    starts = set(nxt) - set(nxt.values())
    chains = []
    for s in sorted(starts):
        ch = [s]
        while ch[-1] in nxt: ch.append(nxt[ch[-1]])
        chains.append(ch)
    N = len(chains); T = len(chains[0]); assert all(len(ch) == T for ch in chains)
    # --- peaking rows: phi*k <= c (single quad term), gives phi_T for k_T
    peak = {}
    for r, R in enumerate(rows):
        if R["lb"] is None and R["ub"] is not None and not R["lin"] and len(R["quad"]) == 1:
            (pr, q), = R["quad"].items(); assert q == 1
            peak[pr] = R["ub"]; setrole(r, "peak")
    kset = {k for ch in chains for k in ch}
    for ch in chains:
        kT = ch[-1]
        cand = [pr for pr in peak if kT in pr]; assert len(cand) == 1
        (ph,) = set(cand[0]) - {kT}; phi_of[kT] = ph
    # node index = position in sorted chains; order nodes by the phi index of eigen rows later
    kvar = [[ch[t] for t in range(T)] for ch in chains]
    phivar = [[phi_of[ch[t]] for t in range(T)] for ch in chains]
    pair2 = {}
    for i in range(N):
        for t in range(T):
            pair2[tuple(sorted((phivar[i][t], kvar[i][t])))] = (i, t)
    c = [[peak[tuple(sorted((phivar[i][t], kvar[i][t])))] for t in range(T)] for i in range(N)]
    phiset = {phivar[i][t] for i in range(N) for t in range(T)}
    # --- normalization rows
    Vw = {}
    for r, R in enumerate(rows):
        if R["lb"] == R["ub"] == 1 and not R["lin"] and R["quad"]:
            ts = {pair2[pr][1] for pr in R["quad"]}; assert len(ts) == 1; (t,) = ts
            assert len(R["quad"]) == N
            w = {pair2[pr][0]: v for pr, v in R["quad"].items()}
            if Vw: assert w == Vw
            Vw = w; setrole(r, ("norm", t))
    Vv = [Vw[i] for i in range(N)]
    # --- eigen rows: -lam*phi_i + sum_j G_ij phi_j k_j = 0 (after scaling)
    G = {}; lam = {}
    for r, R in enumerate(rows):
        if role[r] is None and R["lb"] == R["ub"] == 0 and not R["lin"] and R["quad"]:
            other = [pr for pr in R["quad"] if pr not in pair2]
            if len(other) != 1: continue
            (lp,) = other; ph = [x for x in lp if x in phiset]; assert len(ph) == 1
            (lv,) = set(lp) - {ph[0]}
            s = -R["quad"][lp]
            i, t = [(ii, tt) for ii in range(N) for tt in range(T) if phivar[ii][tt] == ph[0]][0]
            if t in lam: assert lam[t] == lv
            lam[t] = lv
            for pr, v in R["quad"].items():
                if pr == lp: continue
                j, tj = pair2[pr]; assert tj == t
                g = v / s; assert g > 0
                if (i, j) in G: assert G[(i, j)] == g, "G differs between t"
                G[(i, j)] = g
            setrole(r, ("eigen", i, t))
    assert Counter(x[0] for x in role if isinstance(x, tuple)) == Counter({"eigen": N * T, "norm": T})
    Gm = [[G.get((i, j), F(0)) for j in range(N)] for i in range(N)]
    # objective
    assert M["obj"]["sense"] == "min" and M["obj"]["lin"] == {lam[T - 1]: -1}
    S = Nuc(); S.name = name; S.M = M; S.N, S.T, S.a, S.G, S.V, S.c = N, T, a, Gm, Vv, c
    S.k, S.phi, S.lam = kvar, phivar, [lam[t] for t in range(T)]
    S.role = role
    # --- reload rows
    k1 = {kvar[i][0]: i for i in range(N)}
    kT = {kvar[i][T - 1]: i for i in range(N)}
    rest = [r for r in range(len(rows)) if role[r] is None]
    k1row = {}
    for r in rest:
        R = rows[r]
        hits = [j for j in R["lin"] if j in k1]
        if hits:
            assert len(hits) == 1 and R["lin"][hits[0]] in (1, -1); k1row[k1[hits[0]]] = r
    assert len(k1row) == N
    fam = "F1"
    r0 = rows[k1row[0]]
    if any(any(x in kT for x in pr) for pr in r0["quad"]): fam = "F2"
    elif not r0["quad"]: fam = "F3"
    S.fam = fam
    if fam != "F1":
        return S
    # copy rows x - b = 0 (continuous copy of a binary) and tie rows b1 - b2 = 0
    alias, ties = {}, []
    for r in rest:
        R = rows[r]
        if R["lb"] == R["ub"] == 0 and not R["quad"] and len(R["lin"]) == 2 and sorted(R["lin"].values()) == [-1, 1]:
            x, y = R["lin"]
            if isB(x) and isB(y): ties.append((x, y)); setrole(r, "tie")
            elif isB(x) != isB(y):
                b, cc = (x, y) if isB(x) else (y, x); alias[cc] = b; setrole(r, "copy")
    canon = lambda j: alias.get(j, j)
    # k1 rows: k_i1 - KF*sum(fresh y) - sum y*kappa = 0
    KFs = set(); node_of = {}; kap_at = {}; fresh_bins = set()
    for i, r in k1row.items():
        R = rows[r]; s = R["lin"][kvar[i][0]]
        for j, v in R["lin"].items():
            if j == kvar[i][0]: continue
            assert isB(j); KFs.add(-v / s); node_of[j] = i; fresh_bins.add(j)
        for pr, v in R["quad"].items():
            assert v / s == -1
            yb = [x for x in pr if isB(canon(x))]; assert len(yb) == 1
            (kap,) = set(pr) - {yb[0]}
            node_of[canon(yb[0])] = i; kap_at[canon(yb[0])] = kap
        setrole(r, ("k1", i))
    assert len(KFs) == 1; (KF,) = KFs
    kappas = set(kap_at.values())
    # kappa rows
    kaprow = {}
    for r in rest:
        R = rows[r]
        if role[r] is None and len(R["lin"]) == 1 and next(iter(R["lin"])) in kappas and R["quad"] and R["lb"] == R["ub"] == 0:
            (kv, s), = R["lin"].items()
            terms = {}
            for pr, v in R["quad"].items():
                kk = [x for x in pr if x in kT]; assert len(kk) == 1
                (yb,) = set(pr) - {kk[0]}
                terms[canon(yb)] = (kT[kk[0]], -v / s)
            kaprow[kv] = terms; setrole(r, "kappa")
    assert set(kaprow) == kappas
    # node rows and type rows
    noderows, typerows = [], []
    for r in rest:
        R = rows[r]
        if role[r] is None and R["lb"] == R["ub"] == 1 and not R["quad"] and all(isB(j) for j in R["lin"]):
            nodes = {node_of[j] for j in R["lin"]}
            if len(nodes) == 1: noderows.append(r); setrole(r, "node")
            else: typerows.append(r); setrole(r, "type")
    assert all(x is not None for x in role), [rows[r] for r in range(len(rows)) if role[r] is None][:3]
    assert len(noderows) == N
    ng = len(typerows)
    y = [[None] * ng for _ in range(N)]
    for g, r in enumerate(typerows):
        R = rows[r]; assert len(R["lin"]) == N
        for j, v in R["lin"].items():
            i = node_of[j]; assert y[i][g] is None and v == Vv[i]; y[i][g] = j
    for r in noderows:
        R = rows[r]; assert set(R["lin"].values()) == {1} and len(R["lin"]) == ng
    gof = {y[i][g]: g for i in range(N) for g in range(ng)}
    fresh = [all(y[i][g] in fresh_bins for i in range(N)) for g in range(ng)]
    assert all(fresh[g] or not any(y[i][g] in fresh_bins for i in range(N)) for g in range(ng))
    kappa = [None] * ng; pred = [None] * ng
    for g in range(ng):
        if fresh[g]: continue
        ks = {kap_at[y[i][g]] for i in range(N)}; assert len(ks) == 1; kappa[g] = ks.pop()
        terms = kaprow[kappa[g]]
        ps = {gof[b] for b in terms}; assert len(ps) == 1; pred[g] = ps.pop()
        assert len(terms) == N
        for b, (j, w) in terms.items():
            assert node_of[b] == j and w == Vv[j]
    tiepairs = defaultdict(set)
    for (b1, b2) in ties:
        assert gof[b1] == gof[b2]
        tiepairs[tuple(sorted((node_of[b1], node_of[b2])))].add(gof[b1])
    assert all(v == set(range(ng)) for v in tiepairs.values())
    S.KF, S.ntypes, S.fresh, S.pred, S.y, S.kappa = KF, ng, fresh, pred, y, kappa
    S.ties = sorted(tiepairs); S.nties_rows = len(ties); S.alias = alias
    # chains / ages
    succ = {pred[g]: g for g in range(ng) if pred[g] is not None}
    assert len(succ) == sum(1 for g in range(ng) if pred[g] is not None)  # each type has <= 1 successor
    S.chains = []
    for g in range(ng):
        if fresh[g]:
            ch = [g]
            while ch[-1] in succ: ch.append(succ[ch[-1]])
            S.chains.append(ch)
    assert sorted(x for ch in S.chains for x in ch) == list(range(ng))
    S.age = {g: A for ch in S.chains for A, g in enumerate(ch)}
    # variable bounds by role
    rolev = {}
    for i in range(N):
        for t in range(T): rolev[kvar[i][t]] = "k"; rolev[phivar[i][t]] = "phi"
    for t in range(T): rolev[lam[t]] = "lam"
    for j in gof: rolev[j] = "bin"
    for j in alias: rolev[j] = "copy"
    for kv in kappas: rolev[kv] = "kappa"
    assert len(rolev) == len(V)
    bnd = defaultdict(set)
    for j, rr in rolev.items(): bnd[rr].add((V[j]["type"], str(V[j]["lb"]), str(V[j]["ub"])))
    S.bounds = dict(bnd)
    return S


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        S = analyze(nm)
        print(f"{nm}: fam={S.fam} N={S.N} T={S.T} a={S.a} rows={len(S.M['rows'])} vars={len(S.M['vars'])}")
        if S.fam == "F1":
            print(f"   KF={S.KF} types={S.ntypes} chains={len(S.chains)} lengths={sorted(set(map(len, S.chains)))} "
                  f"ties={S.ties} tie_rows={S.nties_rows} copy_rows={len(S.alias)}")
            print(f"   V={Counter(map(str, S.V))} c={Counter(str(x) for r in S.c for x in r)}")
            print(f"   bounds={S.bounds}")
