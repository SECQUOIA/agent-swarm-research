"""Araya-Trombettoni-Neveu (2010) example: x^2 - 3x + y = 0 on [4,10] x [-80,14],
propagated to the fixed point on the DAG (terms x^2, x, y), root fixed to [0,0]."""
from ifbbt import DAG
d = DAG(2); p = d.pow(0, 2); d.sum([p, 0, 1], [1.0, -3.0, 1.0])
Z = d.forward_box([(4.0, 10.0), (-80.0, 14.0)]); Z[-1] = (0.0, 0.0)
st, Z, r = d.propagate(None, 0.0, start=Z)
print(st, r, 'x-box', d.xbox(Z), '(true hull of y: [-70, -4])')
