"""Extract the eigenvalue structure of the MINLPLib nuclear* instances.

For the objective variable lam_T (objective: min -lam_T) every row containing a product with lam_T has
the form  sum_j G_ij * phi_j * k_j - phi_i * lam_T = 0  (verified below term by term).
Returns G (numpy, rows/cols = nodes), variable indices phi[i], k[i], lam, plus data for all time steps.
"""
import os, numpy as np
from osil_eval import Model

OS = os.path.expanduser("~/.cache/minlplib/minlplib/osil/")
NAMES = ("nuclearva nuclearvb nuclearvc nuclearvd nuclearve nuclearvf nuclear14 nuclear14a nuclear14b "
         "nuclear25 nuclear25a nuclear25b nuclear49 nuclear49a nuclear49b nuclear10a nuclear10b nuclear104").split()
LISTED = {}
import csv
for r in csv.DictReader(open(os.path.join(os.path.dirname(__file__), "../../scouting/minlplib-open-data/open.csv"))):
    if r["name"] in NAMES:
        LISTED[r["name"]] = (float(r["primalbound"]) if r["primalbound"] else None,
                             float(r["dualbound"]) if r["dualbound"] else None)


def eigen_rows(M, lam):
    """Rows with a (phi_i * lam) term. Returns dict node-> (row, phi_idx) and list of rows."""
    out = []
    for r, terms in M.quad.items():
        if r < 0: continue
        hit = [(i, j, c) for i, j, c in terms if lam in (i, j)]
        if hit:
            assert len(hit) == 1 and float(hit[0][2]) == -1.0, (r, hit)
            assert not M.lin[r] and r not in M.nl and M.clb[r] == M.cub[r] == "0", r
            i, j, _ = hit[0]
            out.append((r, j if i == lam else i))
    return out


def structure(name):
    M = Model(OS + name + ".osil")
    assert M.objsense == "min" and len(M.objlin) == 1
    (lamT, c), = M.objlin.items(); assert float(c) == -1.0
    # all lambda variables: every variable v such that some row has a -1 * phi * v term where phi is in
    # the T-rows' phi-set at the same position is hard to detect generically; use lam_T only for G.
    rows = eigen_rows(M, lamT)
    phi = [p for _, p in rows]
    node = {p: n for n, p in enumerate(phi)}
    N = len(phi)
    G = np.zeros((N, N)); kidx = [None] * N
    for n, (r, p) in enumerate(rows):
        for i, j, c in M.quad[r]:
            if lamT in (i, j): continue
            if i in node and j not in node: f, k = i, j
            elif j in node and i not in node: f, k = j, i
            else: raise ValueError(("ambiguous", r, i, j))
            m = node[f]
            assert kidx[m] in (None, k); kidx[m] = k
            G[n, m] += float(c)
    return M, lamT, phi, kidx, G


if __name__ == "__main__":
    for nm in NAMES:
        M, lam, phi, k, G = structure(nm)
        ev = np.linalg.eigvals(G); rho = max(abs(ev))
        # irreducibility: strong connectivity of the pattern of G
        from scipy.sparse.csgraph import connected_components
        irr = connected_components(G > 0, directed=True, connection="strong")[0] == 1
        print(f"{nm:11s} nodes={len(G):4d} G>=0:{(G>=0).all()} irreducible:{irr} rho(G)={rho:.6f} "
              f"maxrow={G.sum(1).max():.4f} maxcol={G.sum(0).max():.4f} 1.2*rho={1.2*rho:.6f} "
              f"listed primal/dual={LISTED[nm]}  phi lb={set(M.vlb[i] for i in phi)} k lb={set(M.vlb[i] for i in k)}")
