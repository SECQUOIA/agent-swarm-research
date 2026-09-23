"""Enumerate all fresh-slot subsets (depth = #chains) of a va-vf instance and run the fresh-only float IEP
(partial_iep.iep_fresh logic) on each; count subsets proved infeasible. Each subset stands for
(#slots - #chains)! complete patterns.  usage: fresh_subsets.py name procs"""
import sys, itertools
import numpy as np
from multiprocessing import Pool
sys.argv = [sys.argv[0], sys.argv[1], "0", "0", sys.argv[2]]
exec(open("partial_iep.py").read().split("for q in range(npat):")[0])
procs = int(sys.argv[4])


def run(sub):
    fm = np.zeros(N, bool)
    for s in sub:
        fm[s] = True
        if s in partner: fm[partner[s]] = True
    return sub, iep_fresh(fm)


if __name__ == "__main__":
    C = len(d.S.chains)
    subs = list(itertools.combinations(slots, C))
    with Pool(procs) as P:
        res = P.map(run, subs, chunksize=4)
    inf = [s for s, r in res if r == "infeasible"]
    ubs = [float(r) for s, r in res if r != "infeasible"]
    from math import factorial
    per = factorial(len(slots) - C)
    print(f"{nm}: {len(subs)} fresh subsets; IEP-infeasible {len(inf)} ({len(inf)/len(subs):.3f}), "
          f"i.e. {len(inf)*per} of {len(subs)*per} patterns pruned at depth {C}; bound range on the rest [{min(ubs):.6f}, {max(ubs):.6f}]")
    print("infeasible subsets (0-based slot nodes):", inf)
