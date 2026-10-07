import sys, json
from fractions import Fraction as Fr
import mpmath as mp
sys.path.insert(0, '/tmp/camcrit')
from qplib import to_model
from mine import enclosure, digits, structure
eta = Fr(1, 10**14)
for name, n, src in (('QPLIB_3177', 800, 'q'), ('QPLIB_2738', 100, 'q'), ('camshape800', 800, 'osil'), ('camshape100', 100, 'osil')):
    K = to_model(f'/tmp/camcrit/q/{name}.gms', n)[0] if src == 'q' else structure(f'/tmp/camcrit/{name}.osil', n)
    Klo = dict(K, c=K['c'] - eta, ub1=K['ub1'] + eta, alpha=K['alpha'] + eta)
    c = Klo['c']; U = [Fr(1), c]
    while len(U) < n: U.append(c * U[-1] - U[-2])
    assert all(u >= 0 for u in U)
    slo, shi, _, _ = enclosure(Klo, n)
    low = -(K['c0'] + eta) * shi
    Khi = dict(K, c=K['c'] + eta, ub1=K['ub1'] - eta, alpha=K['alpha'] - eta)
    slo2, shi2, Elo, Ehi = enclosure(Khi, n)
    upv = -(K['c0'] - eta) * slo2
    print(name, 'low', digits(low, 16), 'up', digits(upv, 16, True))
