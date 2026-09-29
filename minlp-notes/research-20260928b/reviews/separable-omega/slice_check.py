"""Slice bounds N_z(eps), N_x(eps) for the note's sharp x quadratic instance, and omega/slice
with omega's leaf counts from the note's Section 5 table (reproduced in sharpquad_grid.log)."""
from fractions import Fraction as Fr
from selection_check import quad_knots
from sepcore import sharp

cz = quad_knots(Fr(29, 70), 1, rmin=Fr(1, 10 ** 8), sel="knots")
cx = sharp(Fr(1, 3), 2, sel="knots")
om = {3: 10, 4: 14, 5: 18, 6: 24, 7: 28, 8: 32, 9: 36, 10: 38, 11: 44}
for k in range(3, 12):
    e = Fr(1, 10 ** k)
    nz, nx = cz.ncert(e), cx.ncert(e)
    print(f"eps=1e-{k}: slice N_z={nz} N_x={nx}; omega/slice = {om[k]}/{nz} = {om[k] / nz:.3f}")
