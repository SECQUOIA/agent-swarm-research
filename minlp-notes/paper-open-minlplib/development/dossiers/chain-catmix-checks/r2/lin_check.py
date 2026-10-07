"""Check catmix linear coefficients exactly (xml.etree, OSiL column-major start/rowIdx/value with mult/incr)."""
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction as F
NS = '{os.optimizationservices.org}'
def expand(parent, cast):
    out = []
    for el in parent.findall(NS + 'el'):
        m = int(el.get('mult', '1')); inc = el.get('incr'); v = el.text
        for t in range(m):
            out.append(cast(v) + (t * cast(inc) if inc else 0))
    return out
for N in [int(v) for v in sys.argv[1:]]:
    inst = ET.parse('catmix%d.osil' % N).getroot().find(NS + 'instanceData')
    lcc = inst.find(NS + 'linearConstraintCoefficients')
    start = expand(lcc.find(NS + 'start'), int)
    rowcol = lcc.find(NS + 'rowIdx'); colIdx = lcc.find(NS + 'colIdx')
    vals = expand(lcc.find(NS + 'value'), F)
    if rowcol is not None:   # column-major: start over columns, rowIdx
        idx = expand(rowcol, int); major = 'col'
    else:
        idx = expand(colIdx, int); major = 'row'
    ent = {}
    for j in range(len(start) - 1):
        for k in range(start[j], start[j + 1]):
            r, c = (idx[k], j) if major == 'col' else (j, idx[k])
            ent[(r, c)] = ent.get((r, c), 0) + vals[k]
    a = F(1, 2 * N)
    X1, X2 = (lambda i: N + 1 + i), (lambda i: 2 * N + 2 + i)
    exp = {}
    for i in range(N):
        exp[(i, X1(i))] = F(-1); exp[(i, X1(i + 1))] = F(1)
        exp[(N + i, X2(i))] = -(1 - a); exp[(N + i, X2(i + 1))] = 1 + a
    assert ent == exp, (N, len(ent), len(exp))
    print('catmix%d: %d linear coefficients, all equal to the expected exact values (-1, 1, -(1-a), 1+a); major=%s' % (N, len(ent), major))
