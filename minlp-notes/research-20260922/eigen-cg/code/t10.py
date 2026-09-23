# re-run the two spurious hits with the complete separation
from fractions import Fraction as Fr
from bh import PBH
from perturb_milp import PerturbSearch
S = PerturbSearch(PBH(6, W0=1))
for a, b in [(11, 22), (8, 16)]:
    r = S.run([-2, -1, -1, 1, 1, 1], Fr(a), Fr(b), a)
    print(a, b, r if r is None else (r[0], r[1] if r[1] is None else r[1][0]))
