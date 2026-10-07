"""R8 check: table sizes needed for the first stage on the two QPLIB inputs.

Binary QP: every coordinate grid is {0,1} with no correction, so stage 0 is
an exact DP. Report min-fill width and sum over bags of 2^|bag| (the stage-0
table-state count the implementation compares with its cap).
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import sys
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver'))
sys.path.insert(0, (_PUBLIC_REPO + '/research-20261002-decomposition/solver/extra-benchmarks'))
from corpus import read_qbn
from decomposition import decompose_qp
for code in ('3852', '5881'):
    p = read_qbn(code)
    A = p.A if hasattr(p, 'A') else p['A']
    d = decompose_qp(A)
    sizes = [len(b) for b in d['bags']]
    print(code, 'n =', len(A), 'max bag size =', max(sizes), 'width =', max(sizes) - 1,
          'stage-0 table states = %.3e' % sum(2 ** s for s in sizes))
