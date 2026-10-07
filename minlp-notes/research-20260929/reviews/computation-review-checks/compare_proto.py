"""Compare the prototype's certified [LB, UB] (chain_bb.py, mode quad, unary_sub 16, as in the
study) with the independent rigorous bracket from indep_grid_dp.py on the same instances.

Validity requires proto_LB <= f* <= indep_UB, i.e. proto_LB - indep_UB <= 0, and
indep_LB <= f* <= proto_UB. Optimality of the prototype's point: proto_UB - indep_LB <= eps + loss.
"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../computation"))
import instances as I
import chain_bb as CB
import indep_grid_dp as G

K = int(sys.argv[1])
cases = json.loads(sys.argv[2])
for amp, n, seed in cases:
    c = I.coeffs(n, seed, amp)
    assert np.array_equal(c, G.coeffs(n, seed, amp))
    iLB, xg = G.grid_dp(c, K)
    _, iUB = G.polish(xg, c)
    iUB = min(iUB, G.F(xg, c))
    for eps in (1e-4, 1e-6):
        r = CB.chain_bb(I.Probe3Chain(c), eps, mode="quad", unary_sub=16, max_pairs_iter=30_000_000,
                        time_limit=300)
        print(json.dumps(dict(amp=amp, n=n, seed=seed, eps=eps, status=r["status"], proto_LB=r["LB"],
                              proto_UB=r["UB"], indep_LB=iLB, indep_UB=iUB,
                              protoLB_minus_indepUB=r["LB"] - iUB,
                              protoUB_minus_indepLB=r["UB"] - iLB,
                              protoUB_minus_indepUB=r["UB"] - iUB,
                              proto_x_at_bound=int((np.abs(r["x"]) > 1 - 1e-9).sum()))), flush=True)
