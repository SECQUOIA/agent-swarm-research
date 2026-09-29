# Count distinct depth-D itineraries (L/R words) of a fixed point x* under
# alpha-splitting (child boxes [l, l+a(u-l)] and [l+a(u-l), u]) as alpha varies.
# Exact via sympy-free approach: breakpoints are alphas where x* equals a node endpoint.
import numpy as np, sys
from fractions import Fraction

def itinerary(x, a, D):
    w = []
    for _ in range(D):
        if x < a:
            w.append('L'); x = x / a
        else:
            w.append('R'); x = (x - a) / (1 - a)
    return ''.join(w)

xstar = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3141592653589793
a_lo, a_hi = 0.2, 0.8
grid = np.linspace(a_lo, a_hi, 2_000_001)
for D in range(1, 21):
    words = [itinerary(xstar, a, D) for a in grid[::1]] if D <= 20 else None
    changes = sum(1 for i in range(1, len(words)) if words[i] != words[i-1])
    print(D, 'distinct', len(set(words)), 'pieces', changes + 1, flush=True)
