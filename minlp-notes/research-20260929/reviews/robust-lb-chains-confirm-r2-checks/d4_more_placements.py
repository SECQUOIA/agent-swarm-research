"""Referee check: further placements not in the note (floating point, Clarabel), using d2_sdp.build.
  oneL / oneR : both linear bounds 1 -/+ x_i in the same clique, (i-1, i) resp. (i, i+1) (ends: the only clique)
  also with Lasserre's ball M = 1.5 and M = 2.
Usage: python3 d4_more_placements.py n1 n2 ...
"""
import sys, json, warnings
warnings.filterwarnings("ignore")
import d2_sdp as D
for n in [int(v) for v in sys.argv[1:]] or [5, 8]:
    for place, ball in (("oneL", None), ("oneR", None), ("oneR", 1.5), ("oneR", 2.0), ("opp", 1.5), ("opp", 1.7)):
        prob, _ = D.build(n, place, ball)
        prob.solve(solver="CLARABEL")
        print(json.dumps(dict(n=n, place=place, ball=ball, CLARABEL=[prob.status, float(f"{prob.value:.7g}")])), flush=True)
