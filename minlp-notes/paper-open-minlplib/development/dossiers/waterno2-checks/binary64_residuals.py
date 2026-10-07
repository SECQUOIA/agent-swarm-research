"""Sign of the binary64 rounding residuals of the off-station identities (dossier check).
Decimal data satisfy w^2 = sq and w^3 = cu exactly; a binary64 reading of the same data may not."""
from fractions import Fraction as F
for st, w, sq, cu in [('A', '.6', '.36', '.216'), ('B1', '.8', '.64', '.512'), ('B2', '.85', '.7225', '.614125'), ('D', '.7', '.49', '.343')]:
    fw = F(float(w))
    assert F(w)**2 == F(sq) and F(w)**3 == F(cu)
    r2 = fw**2 - F(float(sq)); r3 = fw**3 - F(float(cu))
    print(f'station {st}: speed lb {w}: fl(w)^2 - fl({sq}) = {float(r2):+.4g}; fl(w)^3 - fl({cu}) = {float(r3):+.4g}; '
          f'off station infeasible under binary64 reading: {r2 < 0 or r3 < 0}')
