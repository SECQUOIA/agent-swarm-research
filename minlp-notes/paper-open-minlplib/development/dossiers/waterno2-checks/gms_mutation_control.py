"""Negative control for gms_vs_osil.py: one perturbed coefficient and one perturbed bound must be detected."""
import re
g = open('waterno2_09.gms').read()
print('GAMS equations in waterno2_09.gms:', len(re.findall(r'^(e\d+)\.\.', g, re.M)), '(OSIL rows + objective row e1)')
g2 = g.replace('63.61644904', '63.61644905', 1); assert g2 != g
open('mut_coef_09.gms', 'w').write(g2)
m = re.search(r'(x\d+)\.up = ([0-9.]+);', g); s = m.group(0)
g3 = g.replace(s, s.replace(m.group(2), m.group(2) + '1'), 1); assert g3 != g
open('mut_bound_09.gms', 'w').write(g3); print('perturbed bound:', s)
