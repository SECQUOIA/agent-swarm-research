"""A tiny one-quality pooling instance with all degrees at most two whose
optimal value is irrational: -(5 + sqrt(3))/2.

Inputs A (lambda 3/4, cap 1, arc cost 1), B (lambda 1/2, cap 2, cost 2),
C (lambda 0, cap 1, cost 1).  Pool P (cap 2) takes A and B; pool Q (cap 1)
takes C.  Output j2 (mu 1, cap 1) is fed by P at cost -4; output j1 (mu 1/4,
cap 1) is fed by P at cost -3 and by Q at cost -1.

Analysis: P takes a = 1 from A and b from B, sells 1 unit to j2 and b to j1,
where Q's clean flow 1-b dilutes it; the constraint at j1 is
(3/4 + b/2) b <= 1/4, i.e. b <= (sqrt(3)-1)/2, and each unit of b is worth
3 - 2 = 1, so the optimum is -3 - (sqrt(3)-1)/2 = -(5 + sqrt(3))/2.
The script solves the instance globally with Gurobi and compares.

Run: conda activate minlp-notes; python irrational_example.py
"""
import math

from random_degree_two import solve

inputs = {'A': (0.75, 1), 'B': (0.5, 2), 'C': (0.0, 1)}
pools = {'P': 2, 'Q': 1}
outputs = {'j1': (0.25, 1), 'j2': (1.0, 1)}
arcs_in = {('A', 'P'): 1, ('B', 'P'): 2, ('C', 'Q'): 1}
arcs_out = {('P', 'j2'): -4, ('P', 'j1'): -3, ('Q', 'j1'): -1}

opt, sol = solve(inputs, pools, outputs, arcs_in, arcs_out)
target = -(5 + math.sqrt(3)) / 2
print(f"gurobi optimum {opt:.9f}, predicted -(5+sqrt(3))/2 = {target:.9f}, diff {opt - target:.2e}")
print('pool (quality, throughput):', {l: (round(v[0], 9), round(v[1], 9)) for l, v in sol.items()})
print('b = (sqrt(3)-1)/2 =', (math.sqrt(3) - 1) / 2, ' predicted P quality',
      (0.75 + 0.5 * (math.sqrt(3) - 1) / 2) / (1 + (math.sqrt(3) - 1) / 2))
