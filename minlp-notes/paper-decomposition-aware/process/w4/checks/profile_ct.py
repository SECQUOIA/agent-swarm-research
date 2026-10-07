"""Share of CT run time spent in fractions.Fraction (band n=8, bag 4, E5 settings)."""
import cProfile, pstats, sys, io
from fractions import Fraction as F
from pathlib import Path
EXP = Path(__file__).resolve().parents[3] / 'experiments'
sys.path.insert(0, str(EXP))
from instances import planted
from certified_grid import solve
p, info = planted('band3', 8, 4, 101)
pr = cProfile.Profile()
pr.enable()
cert = solve(p, epsilon=F(1, 1000000), max_stages=200, time_limit=60, max_table_states=200000,
             schedule='conditioning', convex_presolve=True)
pr.disable()
st = pstats.Stats(pr)
tot = st.total_tt
frac = sum(v[2] for k, v in st.stats.items() if 'fractions' in k[0])
print(cert['status'], 'total', round(tot, 2), 's; tottime inside fractions.py', round(frac, 2), f'({frac/tot:.0%})')
rows = sorted(st.stats.items(), key=lambda kv: -kv[1][2])[:12]
for k, v in rows:
    print(f'{v[2]:6.2f}s  {k[0].split("/")[-1]}:{k[2]}')
