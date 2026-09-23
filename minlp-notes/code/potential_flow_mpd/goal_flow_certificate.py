"""Conservation-aware rational bounds for linear goals of passive network flows.

Verification, Hessian-certificate production, and demonstrations use only the
standard library. These are specialized convex-duality/error-bound certificates,
not claims of a new general duality principle. Run this file for demonstrations.
"""
from dataclasses import dataclass, replace
from fractions import Fraction as F

from envelope_rational_certificates import (
    energy, require, upward_root, verify_certificate, make_certificate,
)
from envelope_bregman_bounds import sharpen, verify_bounds


def _validate(edges, b, positive, negative, y, w):
    n, m = len(b), len(edges)
    require(n > 0 and m > 0, 'nonempty network')
    require(len(y) == len(w) == len(positive) == len(negative) == m,
            'goal vector dimensions')
    require(all(isinstance(x, F) for row in [b, positive, negative, y, w] for x in row),
            'rational goal problem data')
    require(all(c > 0 for c in positive + negative), 'positive goal coefficients')
    loads = [F(0)] * n
    for (u, v), x in zip(edges, y):
        require(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n and u != v,
                'valid loopless edge indices')
        loads[u] += x
        loads[v] -= x
    require(loads == b, 'exact goal flow conservation')


@dataclass
class SupportCertificate:
    multiplier: F
    potentials: list
    root_upper: list
    upper: F


def make_support(edges, b, positive, negative, y, w, multiplier, potentials, bits=100):
    """Any rational nonnegative multiplier/potentials give a bound if valid.

    At multiplier zero the goal must be a cut functional w=A.T@potentials.
    No numerical optimizer's termination status is trusted.
    """
    _validate(edges, b, positive, negative, y, w)
    multiplier = F(multiplier)
    potentials = list(map(F, potentials))
    require(len(potentials) == len(b) and multiplier >= 0, 'support dual dimensions and sign')
    residual = [we - potentials[u] + potentials[v] for we, (u, v) in zip(w, edges)]
    roots = []
    if multiplier > 0:
        for e, s in enumerate(residual):
            c = positive[e] if s >= 0 else negative[e]
            roots.append(upward_root(abs(s)**3 / (multiplier*c), 2, bits))
    else:
        require(all(s == 0 for s in residual), 'zero multiplier requires a cut goal')
    upper = multiplier*energy(y, positive, negative) + sum(p*bi for p, bi in zip(potentials, b)) + F(2, 3)*sum(roots)
    cert = SupportCertificate(multiplier, potentials, roots, upper)
    verify_support(edges, b, positive, negative, y, w, cert)
    return cert


def verify_support(edges, b, positive, negative, y, w, cert):
    _validate(edges, b, positive, negative, y, w)
    lam, p, roots = cert.multiplier, cert.potentials, cert.root_upper
    require(len(p) == len(b), 'support potential dimensions')
    require(all(isinstance(x, F) for x in [lam, cert.upper] + p + roots), 'rational support witness')
    require(lam >= 0, 'nonnegative support multiplier')
    require(len(roots) == (len(edges) if lam > 0 else 0), 'support root dimensions')
    for e, ((u, v), we) in enumerate(zip(edges, w)):
        s = we - p[u] + p[v]
        if lam == 0:
            require(s == 0, 'zero multiplier requires a cut goal')
        else:
            c = positive[e] if s >= 0 else negative[e]
            require(roots[e] >= 0 and roots[e]**2*lam*c >= abs(s)**3, 'support conjugate enclosure')
    expected = lam*energy(y, positive, negative) + sum(pv*bv for pv, bv in zip(p, b)) + F(2, 3)*sum(roots)
    require(cert.upper == expected, 'support bound identity')
    return True


def _linear_solve(matrix, rhs):
    """Rational RREF; choose free variables zero, reject inconsistent systems."""
    n = len(rhs)
    require(len(matrix) == n and all(len(row) == n for row in matrix), 'square linear system')
    rows = [list(map(F, row)) + [F(v)] for row, v in zip(matrix, rhs)]
    pivots = []
    for col in range(n):
        found = next((r for r in range(len(pivots), n) if rows[r][col]), None)
        if found is None:
            continue
        r = len(pivots)
        rows[r], rows[found] = rows[found], rows[r]
        divisor = rows[r][col]
        rows[r] = [x/divisor for x in rows[r]]
        for j in range(n):
            if j != r and rows[j][col]:
                scale = rows[j][col]
                rows[j] = [a-scale*b for a, b in zip(rows[j], rows[r])]
        pivots.append(col)
    require(all(any(row[:n]) or row[n] == 0 for row in rows),
            'goal must annihilate cycles supported entirely on zero-curvature edges')
    answer = [F(0)] * n
    for r, col in enumerate(pivots):
        answer[col] = rows[r][n]
    return answer


def curvature(positive, negative, intervals):
    return [2*cp*lo if lo > 0 else -2*cm*hi if hi < 0 else F(0)
            for cp, cm, (lo, hi) in zip(positive, negative, intervals)]


def optimal_goal_potentials(edges, n, w, h):
    """Exact constrained weighted Laplacian solve; singular gauges are allowed.

    This dense rational implementation is intended for modest certificate sizes.
    A sparse numerical solve followed by rational rounding is possible when all
    curvatures are positive, but is not implemented here.
    """
    zeros = [e for e, he in enumerate(h) if he == 0]
    size = n + len(zeros)
    matrix = [[F(0)]*size for _ in range(size)]
    rhs = [F(0)]*size
    for e, ((u, v), we, he) in enumerate(zip(edges, w, h)):
        if he > 0:
            for i, si in [(u, 1), (v, -1)]:
                rhs[i] += si*we/he
                for j, sj in [(u, 1), (v, -1)]:
                    matrix[i][j] += F(si*sj)/he
    for k, e in enumerate(zeros, n):
        u, v = edges[e]
        matrix[u][k] = matrix[k][u] = F(1)
        matrix[v][k] = matrix[k][v] = F(-1)
        rhs[k] = w[e]
    return _linear_solve(matrix, rhs)[:n]


@dataclass
class HessianCertificate:
    intervals: list
    potentials: list
    factor: F
    radius: F


def make_hessian(edges, b, positive, negative, base, w, bits=100):
    verify_certificate(edges, b, positive, negative, base)
    _validate(edges, b, positive, negative, base.flow, w)
    intervals = sharpen(positive, negative, base)
    if base.gap == 0:
        cert = HessianCertificate(intervals, [F(0)]*len(b), F(0), F(0))
        verify_hessian(edges, b, positive, negative, base, w, cert)
        return cert
    h = curvature(positive, negative, intervals)
    p = optimal_goal_potentials(edges, len(b), w, h)
    factor = sum(((we-p[u]+p[v])**2/he for (u, v), we, he in zip(edges, w, h) if he > 0), F(0))
    cert = HessianCertificate(intervals, p, factor, upward_root(2*base.gap*factor, 2, bits))
    verify_hessian(edges, b, positive, negative, base, w, cert)
    return cert


def verify_hessian(edges, b, positive, negative, base, w, cert):
    verify_certificate(edges, b, positive, negative, base)
    _validate(edges, b, positive, negative, base.flow, w)
    verify_bounds(positive, negative, base, cert.intervals)
    require(len(cert.potentials) == len(b), 'Hessian potential dimensions')
    require(all(isinstance(x, F) for x in cert.potentials + [cert.factor, cert.radius]),
            'rational Hessian witness')
    if base.gap == 0:
        require(cert.factor == 0 and cert.radius == 0, "zero-gap exact goal")
        return True
    h = curvature(positive, negative, cert.intervals)
    factor = F(0)
    for (u, v), we, he in zip(edges, w, h):
        s = we-cert.potentials[u]+cert.potentials[v]
        if he == 0:
            require(s == 0, 'zero-curvature goal residual')
        else:
            factor += s*s/he
    require(cert.factor == factor, 'Hessian factor identity')
    require(cert.radius >= 0 and cert.radius**2 >= 2*base.gap*factor, 'Hessian radius bound')
    return True


def run():
    """Exact solutions and distinct malformed-witness checks, no solver needed."""
    for length in [2, 8, 32]:
        # Two length-L paths from source 0 to sink 1. Exact physical flows = 1.
        edges = []
        paths = []
        next_node = 2
        for _ in range(2):
            nodes = [0] + list(range(next_node, next_node+length-1)) + [1]
            next_node += length-1
            paths.append(nodes)
            edges.extend(zip(nodes[:-1], nodes[1:]))
        b = [F(0)]*next_node
        b[0], b[1] = F(2), F(-2)
        positive = negative = [F(1)]*len(edges)
        eps = F(1, 1000)
        y = [1+eps]*length + [1-eps]*length
        p = [F(0)]*next_node
        for nodes in paths:
            for j, node in enumerate(nodes):
                p[node] = F(length-j)
        base = make_certificate(edges, b, positive, negative, y, p)
        w = [F(1)] + [F(0)]*(len(edges)-1)
        hcert = make_hessian(edges, b, positive, negative, base, w)
        require(abs(sum(we*(F(1)-ye) for we, ye in zip(w, y))) <= hcert.radius,
                'known physical goal enclosed')
        old_width = hcert.intervals[0][1] - hcert.intervals[0][0]
        # Exact support optimum is 1+eps. Recover its dual rationally by KKT.
        lam = F(1)/(4*length*eps)
        v = [F(0)]*next_node
        for path_id, nodes in enumerate(paths):
            x = 1+eps if path_id == 0 else 1-eps
            for j, (u, dest) in enumerate(zip(nodes[:-1], nodes[1:])):
                we = F(1) if path_id == 0 and j == 0 else F(0)
                v[dest] = v[u] - we + lam*x*x
        support = make_support(edges, b, positive, negative, y, w, lam, v)
        require(support.upper >= 1+eps and support.upper-(1+eps) < F(1, 10**20), 'sharp support bound')
        print(f'two paths length {length}: edgewise width {float(old_width):.9g}; '
              f'Hessian width {float(2*hcert.radius):.9g}; '
              f'exact support width {float(2*eps):.9g}; '
              f'edgewise/Hessian ratio {float(old_width/(2*hcert.radius)):.4g}')
        for bad in [replace(support, upper=support.upper-F(1)),
                    replace(support, multiplier=-lam),
                    replace(support, root_upper=[F(0)]*len(edges))]:
            try:
                verify_support(edges, b, positive, negative, y, w, bad)
            except ValueError:
                pass
            else:
                raise RuntimeError('malformed support accepted')
        for bad in [replace(hcert, radius=F(0)), replace(hcert, factor=hcert.factor+1)]:
            try:
                verify_hessian(edges, b, positive, negative, base, w, bad)
            except ValueError:
                pass
            else:
                raise RuntimeError('malformed Hessian certificate accepted')
    # Zero-flow bridge: curvature vanishes, but its flow is exactly fixed by b.
    edges, b, y, w = [(0, 1)], [F(0), F(0)], [F(0)], [F(1)]
    c = [F(1)]
    base = make_certificate(edges, b, c, c, y, [F(0), F(0)])
    hc = make_hessian(edges, b, c, c, base, w)
    sc = make_support(edges, b, c, c, y, w, F(0), [F(1), F(0)])
    require(hc.radius == sc.upper == 0, 'zero-curvature bridge is exact')
    # A zero-curvature cycle goal cannot be controlled by this Hessian modulus.
    try:
        optimal_goal_potentials([(0, 1), (1, 2), (2, 0)], 3,
                                [F(1), F(0), F(0)], [F(0)]*3)
    except ValueError:
        pass
    else:
        raise RuntimeError('uncontrolled zero-curvature cycle accepted')
    print('Exact bridge, zero-curvature obstruction, and 15 corrupted-certificate rejections passed.')


def compare_file(path):
    """Apply the Laplacian certificate to every edge of a saved base witness."""
    import json
    from envelope_rational_certificates import Certificate
    with open(path) as stream:
        payload = json.load(stream)
    b, cp, cm = (list(map(F, payload[key])) for key in ['b', 'positive', 'negative'])
    base = Certificate(list(map(F, payload['flow'])), list(map(F, payload['potentials'])),
                       list(map(F, payload['root_upper'])), F(payload['gap']), F(payload['radius']))
    for e in range(len(payload['edges'])):
        w = [F(int(j == e)) for j in range(len(payload['edges']))]
        cert = make_hessian(payload['edges'], b, cp, cm, base, w)
        old = cert.intervals[e][1]-cert.intervals[e][0]
        print(f'edge {e}: edgewise width {float(old):.9g}; '
              f'Laplacian width {float(2*cert.radius):.9g}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', metavar='JSON')
    args = parser.parse_args()
    if args.certificate:
        compare_file(args.certificate)
    else:
        run()
