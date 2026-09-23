from fractions import Fraction as Fr
from verify import exact_bh_separation
from bh import bh_ineq
z = [Fr(3, 8), Fr(5, 8), Fr(3, 8), Fr(3, 8), Fr(3, 8), Fr(3, 8), Fr(1, 8), Fr(0), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 4), Fr(1, 8), Fr(1, 8), Fr(1, 8), Fr(1, 8), Fr(1, 8), Fr(1, 8)]
w, g = exact_bh_separation(6, z)
print(w, g)
a, c = bh_ineq(w[0], w[1:])
print(sum(Fr(ai)*zi for ai, zi in zip(a, z)) + c)
