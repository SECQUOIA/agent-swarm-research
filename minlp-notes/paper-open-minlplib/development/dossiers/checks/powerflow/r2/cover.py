"""Exact coverage check: every elementary grid cell of the root box lies in exactly one leaf box."""
import json, itertools
from fractions import Fraction as Fr
root = ((Fr(0), Fr(52, 5)), (Fr(7, 5), Fr(4)), (Fr(2209, 2500), Fr(2809, 2500)))
for n in ["powerflow0039p", "powerflow0039r"]:
    B = [tuple((Fr(a), Fr(c)) for a, c in l["box"]) for l in json.load(open(f"data/{n}.bb3t.json"))["leaves"]]
    assert all(root[d][0] <= b[d][0] < b[d][1] <= root[d][1] for b in B for d in range(3))
    cuts = [sorted({root[d][0], root[d][1]} | {b[d][k] for b in B for k in (0, 1)}) for d in range(3)]
    cells = 0
    for idx in itertools.product(*[range(len(c) - 1) for c in cuts]):
        mid = [(cuts[d][i] + cuts[d][i + 1]) / 2 for d, i in enumerate(idx)]
        k = sum(all(b[d][0] < mid[d] < b[d][1] for d in range(3)) for b in B)
        assert k == 1, (n, idx, k)
        cells += 1
    vol = lambda b: (b[0][1]-b[0][0])*(b[1][1]-b[1][0])*(b[2][1]-b[2][0])
    print(f"{n}: {len(B)} leaves, {cells} grid cells each inside exactly one leaf; volume sum == root volume: {sum(map(vol, B)) == vol(root)}")
