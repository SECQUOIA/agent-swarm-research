"""Extra exact crossing boundary checks; not a proof of the general theorem."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import sys
sys.dont_write_bytecode = True
root = Path(__file__).resolve().parents[3]
path = root / "paper-power-flow/process/snapshots/stage02-round01/checks/check_ac_exact.py"
spec = importlib.util.spec_from_file_location("frozen_ac", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
eps = F(1, 10**100)
points = [(F(x),F(y)) for x,y in [(1,0),(-1,0),(0,1),(0,-1)]]
points += [(F(x), y) for x in [-1,1] for y in [-eps,eps]]
points += [(x,F(y)) for x in [-eps,eps] for y in [-1,1]]
count=0
for a in points:
    for b in points:
        if not m.admissible(a,b):
            continue
        for ra,rb in [(F(1),F(1)), (eps,1/eps), (1/eps,eps)]:
            a1,b1=m.scale(a,ra),m.scale(b,rb)
            assert m.crossing(a1,b1)==m.chord_crossing(a1,b1)
            assert m.crossing(a1,b1)==-m.crossing(b1,a1)
            count += 1
print(f"PASS: {count} exact near-axis and near-antipodal pairs; radii span 10^-100 to 10^100.")
