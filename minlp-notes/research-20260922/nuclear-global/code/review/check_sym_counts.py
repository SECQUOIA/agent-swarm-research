"""Exact automorphisms of (G, V, c, tie pairs) by backtracking, and pattern counts.
usage: check_sym_counts.py names..."""
import sys
from math import factorial, comb
from struct_nuc import analyze


def automorphisms(G, V, c, ties):
    N = len(G)
    tie = {}
    for i, j in ties: tie[i] = j; tie[j] = i
    inv = lambda i: (V[i], tuple(c[i]), G[i][i], tuple(sorted(G[i])), tuple(sorted(r[i] for r in G)), i in tie)
    cls = [inv(i) for i in range(N)]
    out = []

    def bt(perm, used):
        i = len(perm)
        if i == N: out.append(tuple(perm)); return
        for s in range(N):
            if s in used or cls[s] != cls[i]: continue
            if any(G[s][perm[j]] != G[i][j] or G[perm[j]][s] != G[j][i] for j in range(i)): continue
            if i in tie and tie[i] < i and perm[tie[i]] != tie.get(s): continue
            bt(perm + [s], used | {s})
    bt([], set())
    return out


for nm in sys.argv[1:]:
    S = analyze(nm)
    A = automorphisms(S.G, S.V, S.c, getattr(S, "ties", []))
    msg = f"{nm}: N={S.N} fam={S.fam} |Aut(G,V,c,ties)|={len(A)}"
    if S.fam == "F1":
        slots = S.N - len(S.ties); nch = len(S.chains)
        msg += f"; slots={slots} types={S.ntypes} chains={nch}; assignments={factorial(slots)}; patterns=slots!/chains!={factorial(slots)//factorial(nch)}"
    else:
        V = S.M["vars"]
        fr = [R for R in S.M["rows"] if R["lb"] is not None and R["lb"] == R["ub"] and R["lb"] > 1 and not R["quad"]
              and all(V[j]["type"] == "B" and v == 1 for j, v in R["lin"].items())]
        assert len(fr) == 1 and len(fr[0]["lin"]) == S.N; nf = int(fr[0]["lb"])
        msg += f"; nfresh={nf}; Lah L(N,nf)=C(N-1,nf-1) N!/nf! = {comb(S.N - 1, nf - 1) * factorial(S.N) // factorial(nf):.4e}"
    print(msg)
