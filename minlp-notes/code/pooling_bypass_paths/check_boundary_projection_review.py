"""Exact independent polygon-composition checks, using Fourier--Motzkin."""
from fractions import Fraction as F
from itertools import combinations
from random import Random


def require(ok):
    if not ok:
        raise RuntimeError("boundary projection check failed")


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    halves = []
    for seq in (points, list(reversed(points))):
        side = []
        for p in seq:
            while len(side) >= 2 and cross(side[-2], side[-1], p) <= 0:
                side.pop()
            side.append(p)
        halves.append(side[:-1])
    return halves[0]+halves[1]


def rows(vertices):
    xmin, xmax = min(x for x, y in vertices), max(x for x, y in vertices)
    ymin, ymax = min(y for x, y in vertices), max(y for x, y in vertices)
    result = [(F(1), F(0), xmax), (F(-1), F(0), -xmin),
              (F(0), F(1), ymax), (F(0), F(-1), -ymin)]
    for a, b in zip(vertices, vertices[1:]+vertices[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        result.append((dy, -dx, dy*a[0]-dx*a[1]))
    return list(set(result))


def vertices(H):
    points = []
    for (a, b, c), (d, e, f) in combinations(H, 2):
        det = a*e-b*d
        if det:
            x, y = (c*e-b*f)/det, (a*f-c*d)/det
            if all(u*x+v*y <= w for u, v, w in H):
                points.append((x, y))
    return hull(points)


def compose(P, Q):
    H = [(a, b, F(0), c) for a, b, c in P]
    H += [(F(0), a, b, c) for a, b, c in Q]
    result = [(a, c, d) for a, b, c, d in H if not b]
    for ap, bp, cp, dp in H:
        if bp <= 0:
            continue
        for an, bn, cn, dn in H:
            if bn < 0:
                result.append((-bn*ap+bp*an, -bn*cp+bp*cn, -bn*dp+bp*dn))
    return list(set(result))


def section(H, x):
    lo, hi = None, None
    for a, b, c in H:
        if not b:
            if a*x > c:
                return None
        elif b > 0:
            value = (c-a*x)/b
            hi = value if hi is None else min(hi, value)
        else:
            value = (c-a*x)/b
            lo = value if lo is None else max(lo, value)
    return (lo, hi) if lo <= hi else None


def run():
    rng = Random(91204)
    tests = sections = 0
    for trial in range(70):
        P = hull([(F(rng.randint(-4, 4)), F(rng.randint(-4, 4))) for _ in range(10)])
        Q = hull([(F(rng.randint(-4, 4)), F(rng.randint(-4, 4))) for _ in range(10)])
        if trial == 0:
            P = [(F(0), F(0)), (F(0), F(2))]
        if trial == 1:
            Q = [(F(1), F(-2)), (F(1), F(2))]
        if trial == 2:
            Q = [(F(0), F(0))]
        if trial == 3:
            P = [(F(0), F(0)), (F(2), F(2))]
        pr, qr = rows(P), rows(Q)
        result = compose(pr, qr)
        R = vertices(result)
        require(len(R) <= 8*(len(P)+len(Q)+4))
        if not R:
            continue
        domain = sorted(set(x for x, z in R))
        probes = domain + [(a+b)/2 for a, b in zip(domain, domain[1:])]
        qmin = min(z for y, z in Q)
        left = min(y for y, z in Q if z == qmin)
        right = max(y for y, z in Q if z == qmin)
        qlo, qhi = min(y for y, z in Q), max(y for y, z in Q)
        for x in probes:
            psection, rsection = section(pr, x), section(result, x)
            require(psection is not None and rsection is not None)
            lo, hi = max(psection[0], qlo), min(psection[1], qhi)
            require(lo <= hi)
            L = qmin if lo <= right else section(qr, lo)[0]
            D = qmin if hi >= left else section(qr, hi)[0]
            require(rsection[0] == max(L, D))
            candidates = [lo, hi]+[y for y, z in Q if lo <= y <= hi]
            require(rsection[0] == min(section(qr, y)[0] for y in candidates))
            require(rsection[1] == max(section(qr, y)[1] for y in candidates))
            sections += 1
        tests += 1
    print(f"PASS: {tests} exact polygon compositions; {sections} lower/upper "
          "section identities, including vertical and nonvertical segments and a point.")


if __name__ == "__main__":
    run()
