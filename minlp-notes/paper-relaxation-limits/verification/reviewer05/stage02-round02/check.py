"""Independent exact finite checks; no optimization solver or universal claim."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
from math import comb, prod
from pathlib import Path
import json
import re
import subprocess
import sys

here = Path(__file__).resolve().parent
paper = here.parents[2]
frozen = paper / "process/snapshots/stage02-round02"
out = {}

# Replay all of the printed finite certificate, preserving the block boundary.
tex = (frozen / "sections/appendix-cubic-certificates.tex").read_text()
blocks = re.findall(r"\\begin\{verbatim\}\n(.*?)\\end\{verbatim\}", tex, re.S)
assert len(blocks) == 2
printed = "".join(blocks)
assert printed == (frozen / "verification/check_stage02_finite.py").read_text()
(here / "printed.py").write_text(printed)
run = subprocess.run([sys.executable, str(here / "printed.py")], check=True,
                     capture_output=True, text=True)
out["printed_exact_replay"] = run.stdout.splitlines()

# Reconstruct the dyadic law from the two resource profiles, and independently
# enumerate the prefixes produced by bit reversal. XOR translation preserves
# prefix equivalence, and each fixed failed label has one preimage at each target.
out["dyadic"] = []
for L in range(2, 11):
    m = 2**L
    weights = [Q(1, 2**(l+1)) if l < L else Q(1, m) for l in range(L+1)]
    B = lambda q: Q(L-q+2, 2**q)
    admissible = [s for s in range(1,L) if B(s+1) <= 1 <= B(s)]
    values = []
    for s in admissible:
        mix = (1-B(s+1))/(B(s)-B(s+1))
        resource = objective = Q(0)
        anchor = [Q(0)] * L
        for q, pq in [(s,mix), (s+1,1-mix)]:
            for l, pl in enumerate(weights):
                r = 0 if l < q else 2**(l-q+1)
                resource += pq*pl*r
                objective += pq*pl*sum(min(2**j,r) for j in range(1,l+1))
                for j in range(1,l+1):
                    anchor[j-1] += pq*pl
        expected = s + Q(L-s,2**s)
        assert resource == 1 and objective == expected
        assert anchor == [Q(1,2**j) for j in range(1,L+1)]
        for l in range(L+1):
            offset = 0 if l <= s else 2**(l-s+1)-2
            assert all(sum(min(2**j,r) for j in range(1,l+1)) <= s*r+offset
                       for r in range(m+1))
        values.append(expected)
    assert len(set(values)) == 1
    rev = [int(f"{r:0{L}b}"[::-1], 2) for r in range(m)]
    for j in range(1,L+1):
        prefixes = set()
        for r, leaf in enumerate(rev, 1):
            prefixes.add(leaf >> (L-j))
            assert len(prefixes) == min(2**j,r)
    if L <= 6:
        for r in range(m+1):
            counts = [0]*m
            for shift in range(m):
                for leaf in rev[:r]:
                    counts[leaf ^ shift] += 1
            assert counts == [r]*m
    assert sum(2**j for j in range(1,L+1)) == 2*m-2
    assert sum(2**j*(2**(L-j)+1) for j in range(1,L+1)) == L*m+2*m-2
    out["dyadic"].append({"L": L, "cutoffs": admissible, "H": str(values[0])})

# Directly integrate O and B from their distribution definitions, without using
# the manuscript's deficiency formulas or low-coordinate case proof.
def orientation(x):
    total = Q(0)
    for left in product([False,True], repeat=len(x)):
        lo = max([Q(0)] + [1-v for v,b in zip(x,left) if not b])
        hi = min([Q(1)] + [v for v,b in zip(x,left) if b])
        total += max(Q(0),hi-lo) / 2**len(x)
    return min(x)-total

def law_b(x):
    cuts = sorted({Q(0),Q(1)} | {v if v <= Q(1,2) else 2*(1-v) for v in x})
    joint = Q(0)
    means = [Q(0)] * len(x)
    for lo,hi in zip(cuts,cuts[1:]):
        t = (lo+hi)/2
        probabilities = [Q(t <= v) if v <= Q(1,2) else
                         (Q(1,2) if t <= 2*(1-v) else Q(1)) for v in x]
        joint += (hi-lo)*prod(probabilities)
        for j,p in enumerate(probabilities):
            means[j] += (hi-lo)*p
    assert means == list(x)
    return min(x)-joint

grid = [Q(i,12) for i in range(13)]
count = 0
for d in (2,3):
    for x in combinations_with_replacement(grid,d):
        gap = min(x)-max(Q(0),sum(x)-d+1)
        do, di, db = orientation(x), min(x)-prod(x), law_b(x)
        assert 18*do+6*di+7*db >= 12*gap
        assert do >= Q(2**(d-1)-1,(d-1)*2**(d-1))*gap
        count += 1
out["exact_direct_coupling_grid_cases"] = count

# Enumerate distinct supports in the explicit homogeneous 52-variable example.
supports = {tuple(sorted((u,w,v))) for u in range(16)
            for w in range(16,32) for v in range(w+1,32)}
supports |= {tuple(sorted((z,u,v))) for z in range(32,52)
             for u in range(16) for v in range(u+1,16)}
assert len(supports) == 4320 and all(len(set(e)) == 3 for e in supports)
x = [Q(1,2)]*16 + [Q(3,4)]*16 + [Q(999,1000)]*20
assert all(min(x[i] for i in e) == Q(1,2) and sum(x[i] for i in e) <= 2
           for e in supports)
assert Q(2160)/(2160-1088+Q(12,5)) == Q(2700,1343)
out["unit52_distinct_cubic_supports"] = len(supports)

(here / "results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
