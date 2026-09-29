"""For the best instance of a search log: omega, deficit, OPT_min, grid optimum (usage: python3 classify.py LOG)."""
import re, ast, sys
from fractions import Fraction as Fr
from search import coord_from_lines, evaluate
from sepexact import opt_min, run
line = [l for l in open(sys.argv[1]) if l.startswith('restart ')][-1]
eps = Fr(re.search(r'eps (\S+)', line).group(1))
L1 = [(Fr(a), Fr(b)) for a, b in ast.literal_eval(re.search(r'L1=(\[.*?\]) L2', line).group(1))]
L2 = [(Fr(a), Fr(b)) for a, b in ast.literal_eval(re.search(r'L2=(\[.*?\])$', line.strip()).group(1))]
c1, c2 = coord_from_lines(L1), coord_from_lines(L2)
print(sys.argv[1], "eps", eps, "omega", run([c1, c2], eps, "omega")['leaves'], "deficit", run([c1, c2], eps, "deficit")['leaves'],
      "OPT_min", opt_min(c1, c2, eps), "grid optimum", evaluate(L1, L2, eps, "omega")[2],
      "slice", max(len(c1.greedy(eps)) - 1, len(c2.greedy(eps)) - 1))
