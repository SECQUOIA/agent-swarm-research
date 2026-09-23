"""Independent numerical audit of the two-parameter finite harmonic certificate.

Quadrature is supporting evidence, not an exact or universal proof certificate.
The check varies the cutoff, unlike the repository's original rho=1 replay.
"""
import json
import math
from pathlib import Path

from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import lambertw

records = []
for degree in [2, 3, 8, 100, 10000, 100000000]:
    for multiplier in [1, 2, 10, 100]:
        cutoff = (degree - 1) * multiplier
        L = 1 + math.log(cutoff)
        rho = (degree - 1) / cutoff

        def curve(v):
            return 1.0 if v == 0 else -math.expm1(-(1 - rho*v)/(L*v))

        def integral(z):
            return quad(curve, z, 1, epsabs=1e-12, epsrel=1e-12)[0]

        zeta = brentq(lambda z: integral(z)-z, 0, 1, xtol=1e-14)
        slope = curve(zeta)
        minimum_slack = min((integral(z)+slope*z)/(1+slope)-zeta
                            for z in [0, zeta, 1] + [i/100 for i in range(101)])
        assert minimum_slack >= -1e-11
        w = float(lambertw(L*math.exp(-rho)).real)
        lower = (w-1/(2*w))/L if w >= 1 else None
        if lower is not None:
            assert lower <= zeta + 1e-11
        records.append(dict(degree=degree, cutoff=cutoff, rho=rho,
                            fixed_point=zeta, lambert_lower=lower,
                            minimum_tangent_slack=minimum_slack))

target = Path(__file__).with_suffix('.json')
target.write_text(json.dumps({'interpretation':'Numerical supporting evidence only',
                              'cases':records}, indent=2)+'\n')
print(f'PASS: {len(records)} cutoff cases; report {target}')
