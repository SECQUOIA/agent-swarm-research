"""Exact algebra and sampled checks for Stage 05; not substitutes for proofs."""
from pathlib import Path
import json
import mpmath as mp
import sympy as sp

mp.mp.dps = 70
y = sp.symbols('y', real=True)
p = y * (1-y)**2 * (1+2*y)
checks = {
    'polynomial_pde_residual': str(sp.simplify(sp.diff(p, y)+y**2*(9-8*y)-1)),
    'half_profile_mass_polynomial': str(sp.integrate(p, (y, 0, 1))),
    'dimensionless_inside_source': str(2*sp.integrate(9-8*y, (y, 0, 1))),
    'dimensionless_inside_reaction': str(2*sp.integrate(y**2*(9-8*y)**2, (y, 0, 1))),
    'dimensionless_derivative_energy': str(16*sp.integrate(p, (y, 0, 1))),
}
assert checks['polynomial_pde_residual'] == '0'
assert checks['half_profile_mass_polynomial'] == '3/20'
assert checks['dimensionless_inside_source'] == '10'
assert checks['dimensionless_inside_reaction'] == '38/5'
assert checks['dimensionless_derivative_energy'] == '12/5'
# The exterior reaction integral equals its source integral, namely 2.
c0 = mp.pi * mp.gamma(mp.mpf(1)/4)/(2*mp.gamma(mp.mpf(3)/4))
cpl = 12*(mp.mpf(3)/80)**(mp.mpf(1)/5)
kobs = 2**(mp.mpf(6)/5)*cpl*mp.beta(mp.mpf(1)/2,mp.mpf(1)/5)/4
k1 = c0*(2*mp.beta(mp.mpf(3)/10,mp.mpf(1)/2))**(mp.mpf(5)/4)/4
checks['constants'] = {name: mp.nstr(val, 40) for name,val in
                      [('Cpl',cpl),('Kobs',kobs),('K1',k1),('oracle_blind_factor',kobs/k1)]}
# Sample the single explicit policy's sufficient support and potential bounds.
L = mp.mpf(10000)
max_radius_to_delta = mp.mpf(0)
min_potential_ratio = mp.inf
sample_count = 0
for exponent in [20,30,40,50]:
    mass = mp.mpf(10)**(-exponent)
    tmin = L*mass**(mp.mpf(2)/7)
    for t in [tmin,2*tmin,10*tmin,mp.sqrt(tmin),mp.mpf('0.5'),mp.mpf(1)]:
        if t > 1 or t < tmin:
            continue
        for sign in [-1,1]:
            c = sign*(1-t)
            a = 1-c*c
            z = mass/a**(mp.mpf(7)/2)
            eta = z**(mp.mpf(1)/10)
            b = a*(1-eta)
            delta = eta*mp.sqrt(a)/2
            radius = (40*mass/(3*b))**(mp.mpf(1)/5)
            max_radius_to_delta = max(max_radius_to_delta,radius/delta)
            assert eta <= mp.mpf('0.5') and radius <= delta/2
            root = mp.acos(-c)
            for j in range(-20,21):
                if j == 0:
                    continue
                x = delta*j/20
                ratio = (c+mp.cos(root+x))**2/(b*x*x)
                min_potential_ratio = min(min_potential_ratio, ratio)
                assert ratio >= 1
                sample_count += 1
checks['sampled_policy'] = {
    'fixed_L': str(L),
    'potential_samples': sample_count,
    'largest_R_over_delta': mp.nstr(max_radius_to_delta,30),
    'smallest_k_over_bx2': mp.nstr(min_potential_ratio,30),
    'scope': 'sampled check only; manuscript proves bounds for all small M and admissible c',
}
source = Path(__file__).resolve().parents[2]
files = ['main.tex','references.bib','notation.md','claims-map.md','sections/05-exact-observation.tex']
for name in files:
    data = (source/name).read_bytes()
    assert not any(c<32 and c not in (9,10) for c in data), name
    assert all(line.rstrip()==line for line in data.decode().splitlines()), name
checks['source_control_characters_and_trailing_whitespace'] = 'pass'
out = Path(__file__).with_suffix('.json')
out.write_text(json.dumps(checks, indent=2)+'\n')
print(json.dumps(checks, indent=2))
