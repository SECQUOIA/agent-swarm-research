"""R8 check: acceptance threshold used by exact_output.py versus the paper.

Paper (eq:exact-constants): Delta = common denominator of H_ii/2, H_ij (i<j),
b, c and endpoints; P = Delta*H; R = Delta * prod_{i in I_C, H_ii>0} P_ii;
Omega = Delta*R^2.  Code (rational_heights): Delta' also clears H_ij/2;
det' = prod over continuous non-fixed i of max(1, sum_j |Delta' H_ij|)
(row Hadamard bound, Remark rem:heights); Omega' = Delta'*(Delta'*det')^2.
Report log2(Omega*W) and log2(Omega'*W) for the E4 instances (W = optimum's
denominator), i.e. the certified-gap bits each rule requires.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys, math, csv
from fractions import Fraction as F
from math import lcm
sys.path.insert(0, (_PUBLIC_REPO + '/paper-decomposition-aware/experiments'))
from instances import planted, random_small, tied_isolated, flat_segment
from exact_output import rational_heights

def paper_omega(p):
    n = len(p.b)
    dens = [p.constant.denominator] + [v.denominator for v in p.b]
    dens += [(p.A[i][i] / 2).denominator for i in range(n)]
    dens += [p.A[i][j].denominator for i in range(n) for j in range(i + 1, n)]
    dens += [v.denominator for pair in p.bounds for v in pair]
    D = lcm(*dens)
    R = D
    for i in range(n):
        lo, hi = p.bounds[i]
        if i not in p.integers and p.A[i][i] > 0:   # I_C^+ (paper: i in I_C with H_ii > 0)
            R *= int(D * p.A[i][i])
    return D * R * R

rows = {r['name']: r for r in csv.DictReader(open((_PUBLIC_REPO + '/paper-decomposition-aware/experiments/results/E4_exact.csv')))}
probs = []
seed = 4000
for n in (3, 4, 5, 6):
    for kind in ('path', 'tree', 'band2'):
        seed += 1
        probs.append(random_small(n, kind, 1 + (n >= 5), seed))
probs += [tied_isolated(s) for s in (1, 2, 3)]
for kind in ('path', 'tree', 'band2'):
    probs.append(planted(kind, 6, 4, 4100)[0])
for p in probs:
    r = rows[p.name]
    W = F(r['oracle_value']).denominator
    om_code = int(F(rational_heights(p)['value']))
    om_paper = paper_omega(p)
    print(f"{p.name:28s} stages={r['stages']:>4s} bits_code={math.log2(om_code*W):6.1f} "
          f"bits_paper={math.log2(om_paper*W):6.1f} csv_required_bits={float(r['required_gap_bits']):6.1f}")
