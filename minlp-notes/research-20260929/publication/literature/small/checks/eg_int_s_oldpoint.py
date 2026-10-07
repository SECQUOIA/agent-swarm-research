"""Evaluate the old GAMS World MINLPLib point of eg_int_s (sources/gamsworld/MINLPLib_points_eg_int_s.inc,
objvar.L = 6.4531031527) on the rows of the current MINLPLib .mod file, in outward-rounded interval
arithmetic (same parser and evaluator as eg_camino_gurobi.py). Reports bounds, integrality and every
row with a negative slack. Usage: python3 checks/eg_int_s_oldpoint.py
"""
import re
from pathlib import Path

from eg_camino_gurobi import MOD, evaluate, parse_mod

INC = Path(__file__).resolve().parent.parent / 'sources/gamsworld/MINLPLib_points_eg_int_s.inc'
point = {('x8' if k == 'objvar' else k): v for k, v in re.findall(r'(\w+)\.L\s*=\s*([-\d.eE+]+)', INC.read_text())}
variables, rows = parse_mod(MOD / 'eg_int_s.mod')
ok, slacks = evaluate(variables, rows, point)
print('point', point)
print('within bounds and integral:', ok)
bad = [(r, float(sl.a), float(sl.b)) for r, sl in slacks if sl.a <= 0]
print('rows not proved to hold:', len(bad))
for r, lo, hi in bad:
    print(f'   {r}: slack in [{lo:.4e}, {hi:.4e}]')
# rows e1..e24 have the form x8 - f_k(x) >= c_k: the smallest objvar feasible for them at this x is objvar - min slack
x8_rows = [sl for r, sl in slacks if int(r[1:]) <= 24]
print(f"smallest objvar meeting rows e1..e24 at this x: {float(6.4531031527 - min(sl.b for sl in x8_rows)):.13f} (lower end)")
