"""k=2 gadget: midpoint-graph clique/chromatic numbers vs the hypergraph partition
number, at eps ~ 0 and eps = 0.9*delta (companion to thm3_gadget.py)."""
import itertools, numpy as np
from thm3_gadget import closed_forms, check_partition_k2, ghat, TH, S, LAM
g00, g10, g11, gh, delta = closed_forms()
k = 2; OPT = k * g10
pts = [np.array(p, float) for p in itertools.product([0, 1], repeat=2 * k) if sum(p) <= k]
def g(z):
    return sum(ghat(z[2*j], z[2*j+1]) for j in range(k))
for eps in (1e-6, 0.9 * delta):
    m = len(pts)
    adj = [[i != j and g((pts[i] + pts[j]) / 2) < OPT - eps for j in range(m)] for i in range(m)]
    best_clique = max(len(c) for r in range(1, m + 1) for c in itertools.combinations(range(m), r)
                      if all(adj[a][b] for a, b in itertools.combinations(c, 2)))
    # chromatic number by brute force
    chi = next(q for q in range(1, m + 1) if any(
        all(not adj[a][b] or col[a] != col[b] for a, b in itertools.combinations(range(m), 2))
        for col in itertools.product(range(q), repeat=m)) ) if m <= 11 else None
    print("eps=%.4g: omega_mid=%d chi_mid=%d" % (eps, best_clique, chi))
    check_partition_k2(eps)
