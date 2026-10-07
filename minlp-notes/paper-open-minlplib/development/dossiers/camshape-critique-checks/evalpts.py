import sys
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/camcrit')
from mine import parse, structure
VN = {100: Fr('-4.2841471217467438034410071'), 200: Fr('-4.2785002329927222918988259'), 400: Fr('-4.2756884789255432151508246'), 800: Fr('-4.2742741419541941011244678')}
for n, p in ((100, 'p1'), (200, 'p1'), (400, 'p1'), (400, 'p2'), (800, 'p1'), (800, 'p2')):
    V, C, oc, lin, quad = parse(f'camshape{n}.osil')
    x = [Fr(0)] * len(V)
    for line in open(f'camshape{n}.{p}.sol'):
        a = line.split()
        if len(a) == 2 and a[0].startswith('x'): x[int(a[0][1:]) - 1] = Fr(a[1])
    viol = []
    for i, (nm, lb, ub) in enumerate(C):
        v = sum(k * x[j] for j, k in lin[i].items()) + sum(k * x[a] * x[b] for (a, b), k in quad[i].items())
        vi = max((v - ub) if ub is not None else 0, (lb - v) if lb is not None else 0, 0)
        viol.append((vi, nm))
    viol.sort(reverse=True)
    big = [(float(v), nm) for v, nm in viol if v > Fr(1, 10**12)]
    obj = sum(k * x[j] for j, k in oc.items())
    print(n, p, 'obj-vn', float(obj - VN[n]), 'rows>1e-12:', len(big), big[:4])
