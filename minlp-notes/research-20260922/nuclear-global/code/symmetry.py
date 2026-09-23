"""Automorphisms of the core geometry: node permutations pi with G[pi i, pi j] = G[i, j] (exact Fractions),
V[pi i] = V[i], c preserved, tied half-node pairs mapped to tied pairs.  Backtracking with row-multiset refinement.
Also prints the number of distinct loading patterns.
usage: symmetry.py names..."""
import sys, math
from fractions import Fraction as F
import nucmodel


def automorphisms(I):
    N = I.N; G = I.G
    inv = lambda i: (I.V[i], tuple(sorted(G[i])), tuple(sorted(G[j][i] for j in range(N))), G[i][i],
                     tuple(sorted(str(x) for x in I.c[i])))
    cls = [inv(i) for i in range(N)]
    tie = {}
    for a, b in getattr(I, "ties", []): tie[a] = b; tie[b] = a
    out = []
    def bt(pi):
        i = len(pi)
        if i == N: out.append(tuple(pi)); return
        for j in range(N):
            if j in pi or cls[j] != cls[i]: continue
            if (i in tie) != (j in tie): continue
            if i in tie and tie[i] < i and pi[tie[i]] != tie[j]: continue
            if all(G[i][m] == G[j][pi[m]] and G[m][i] == G[pi[m]][j] for m in range(i)):
                bt(pi + [j])
    bt([])
    return out


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        I = nucmodel.load(nm)
        A = automorphisms(I)
        nontriv = [p for p in A if any(p[i] != i for i in range(I.N))]
        if I.fam == "F1":
            nslots = I.N - len(I.ties); nch = sum(I.fresh)
            count = math.factorial(nslots) // math.factorial(nch)
            desc = f"F1: {nslots} slots, {I.ntypes} types in {nch} chains; patterns = {nslots}!/{nch}! = {count:.4e}"
        else:
            nf = int(I.nfresh); N = I.N
            # sets of nf vertex-disjoint directed paths covering N labelled nodes: Lah number L(N, nf)
            lah = math.comb(N - 1, nf - 1) * math.factorial(N) // math.factorial(nf)
            desc = f"{I.fam}: {N} nodes, {nf} fresh; reload patterns (path covers) = L({N},{nf}) = {lah:.4e}"
        print(f"{nm}: |Aut(G)| = {len(A)}; nontrivial: {nontriv[:3]}; {desc}; per automorphism class {count / len(A) if I.fam == 'F1' else lah / len(A):.3e}")
