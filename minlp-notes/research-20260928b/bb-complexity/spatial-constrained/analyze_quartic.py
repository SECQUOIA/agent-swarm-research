"""Exponents and Theorem 4.5(i) lower bounds for the quartic circle instance S2_quart.

Lower bound on leaves: sqrt(alpha) int_0^{2pi} (sin^4 t + eps)^{-1/2} dt / (C_{2,1} * 4),
C_{2,1} = pi sqrt(2); a coordinate line meets the circle in <= 2 points, so sum_I M^I <= 4.
Usage: python3 analyze_quartic.py   (reads logs/sweep_quartic.jsonl)
"""
import json
import math
from scipy import integrate

rs = sorted([json.loads(l) for l in open("logs/sweep_quartic.jsonl")], key=lambda r: -r["eps"])
alpha, prev = 1.1, None
for r in rs:
    eps, nodes = r["eps"], r["nodes"]
    I = integrate.quad(lambda t: (math.sin(t) ** 4 + eps) ** -0.5, 0, 2 * math.pi,
                       points=[k * math.pi / 2 for k in range(1, 4)], limit=1000)[0]
    lb = alpha ** 0.5 * I / (math.pi * math.sqrt(2) * 4)
    ex = "" if prev is None else f" exponent {math.log(nodes / prev[1]) / math.log(prev[0] / eps):.2f}"
    print(f"eps={eps:.0e} nodes={nodes} leaves={(nodes + 1) / 2:.0f} ThmLB={lb:.2f} "
          f"leaves/LB={(nodes + 1) / 2 / lb:.1f}{ex}")
    prev = (eps, nodes)
