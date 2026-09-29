"""Exact finite checks of the rational subset-order accuracy construction.

Checks all required subpolygons through ten leaves, the conservative perimeter
bound, original-space witness violation, and cost/mean bounds. Does not prove
the general geometry, scalar realization theorem, or literature novelty.
"""
from fractions import Fraction as F
from itertools import combinations

from verify_star_rational_uniform import polygon, rotate


def check(k):
    n = 2 * k
    ts = [F(2 * i - n + 1, 64 * (n - 1)) for i in range(n)]
    qs = [((1 - t*t)/(1 + t*t), 2*t/(1 + t*t)) for t in ts]
    ps, gs, perimeter = polygon(qs)
    loss = F(1, 11664 * (n - 1)**3)
    upper = perimeter - k * loss
    eta = (4 / perimeter + 4 / upper) / 2
    assert 4 <= upper < perimeter < 5
    assert 0 < eta < 1
    count = 0
    for size in range(1, k + 1):
        for indices in combinations(range(n), size):
            subperimeter = polygon([qs[i] for i in indices])[2]
            assert subperimeter <= upper
            assert eta * subperimeter < 4
            count += 1
    gap = eta * perimeter / 2 - 2
    assert gap == k * loss / upper
    assert gap >= F(1, 466560 * k*k)
    ps = [rotate(p) for p in ps]
    gs = [rotate(g) for g in gs]
    ws = [-g[1] for g in gs]
    cs = [g[0] for g in gs]
    bs = []
    for w in ws:
        b = F(1)
        while b*b >= 4*w:
            b /= 2
        while b*b < w:
            b *= 2
        bs.append(b)
    ds = [b*b/w for b, w in zip(bs, ws)]
    assert all(1 <= d < 4 for d in ds)
    assert sum(ws) == F(24, 13)
    assert all(abs(c) < 8*w for c, w in zip(cs, ws))
    zs = [(1 + eta*p[1])/2 for p in ps]
    ss = [eta*p[0]/2 for p in ps]
    rs = [(1 - eta*p[1])/2 for p in ps]
    ys = [-(w*s + z*c)/b for w, s, z, c, b in zip(ws, ss, zs, cs, bs)]
    assert all(F(11, 416) <= z < F(1, 2) for z in zs)
    assert sum(y*y for y in ys) <= F(486, 13)
    cost = F(25, 13) + sum(z*c*c/w - w*r for z, c, w, r in zip(zs, cs, ws, rs))
    true_upper = sum(d*y*y/z for d, y, z in zip(ds, ys, zs))
    assert cost >= F(1, 13)
    assert cost + gap <= true_upper < 122
    residual = cost + F(1, 13) + sum(
        2*d*c*y/b + (w + c*c/w)*z
        for d, c, y, b, w, z in zip(ds, cs, ys, bs, ws, zs)
    )
    assert residual == -gap
    assert gap / true_upper >= F(1, 56920320 * k*k)
    return count


if __name__ == '__main__':
    count = sum(check(k) for k in range(1, 6))
    print(f'PASS: five rational accuracy instances; {count} exact subpolygon checks; gap, mean, and cost bounds.')
