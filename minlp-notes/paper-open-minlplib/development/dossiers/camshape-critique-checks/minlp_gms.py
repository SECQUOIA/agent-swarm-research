import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/camcrit')
from qplib import parse_gms
from mine import structure
for n in (100, 200, 400, 800):
    eqs, lo, up = parse_gms(f'/tmp/camcrit/q/camshape{n}.gms')
    assert len(eqs) == 2 * n + 1
    r = [None] + [f'x{j}' for j in range(1, n + 1)]; d = [None] + [f'x{n + i}' for i in range(1, n)]
    lin, quad, s, rhs = eqs['e1']; assert s == 'E' and rhs == 0 and quad == {} and lin['objvar'] in (1, -1)
    # objective row: (sign) * objvar + sum(-c0 x) = 0
    sg = lin['objvar']; c0s = {-lin[r[j]] * (-sg) for j in range(1, n + 1)}
    K = structure(f'camshape{n}.osil', n)
    ok = {}
    c = K['c']
    for j in range(2, n):
        want = ({}, {tuple(sorted((r[j-1], r[j+1]))): c, tuple(sorted((r[j-1], r[j]))): -1, tuple(sorted((r[j], r[j+1]))): -1}, 'L', 0)
        assert eqs[f'e{j}'] == want, j
    assert eqs[f'e{n}'] == ({r[1]: -1, r[2]: c}, {(r[1], r[2]): -1}, 'L', 0)
    assert eqs[f'e{n+1}'] == ({r[n-1]: K['c2'], r[n]: -2}, {tuple(sorted((r[n-1], r[n]))): -1}, 'L', 0)
    assert eqs[f'e{n+2}'] == ({r[n]: -4}, {(r[n], r[n]): c}, 'L', 0)
    for i in range(1, n):
        assert eqs[f'e{n+2+i}'] == ({r[i]: 1, r[i+1]: -1, d[i]: 1}, {}, 'E', 0)
    assert up[r[1]] == K['ub1'] and lo[r[n]] == K['lbn'] and up[d[2]] == K['alpha'] and lo[d[2]] == -K['alpha']
    for i in range(2, n): assert lo[d[i]] == -K['alpha'] and up[d[i]] == K['alpha']
    for j in range(2, n): assert lo[r[j]] == 1 and up[r[j]] == 2
    assert d[1] not in lo and d[1] not in up and set(lo) == set(r[1:]) | set(d[2:]) == set(up)
    print(n, 'objvar sign', sg, 'c0 set', [str(x) for x in c0s], 'osil c0', str(K['c0']), 'gms==osil OK')
