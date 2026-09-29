"""Sum over omega phases of the Phase-Lemma certificate size N_A(b') (b' = eps + m_j(h)),
compared with omega's internal nodes and the grid optimum.  usage: python3 exp6.py FAMILY"""
import sys
from fractions import Fraction as Fr
from sepexact import run, guill_grid
import fam
from exp1 import family

if __name__ == "__main__":
    name = sys.argv[1]
    for k in (3, 4, 5, 6, 7, 8):
        eps = Fr(1, 10 ** k)
        c = family(name, eps)
        ro = run(list(c), eps, "omega", record=True)
        seen = {}
        for box, y, i, ph in ro["internal"]:
            if ph not in seen:
                j = 1 - i
                bprime = eps + c[j].m(y[j])
                seen[ph] = len(c[i].greedy(bprime, box[i][0], box[i][1])) - 1
        tot = sum(seen.values())
        print(f"{name} eps=1e-{k} omega_internal={len(ro['internal'])} phases={len(seen)} "
              f"sum_P N_A(b')={tot} max_P={max(seen.values())}", flush=True)
