"""Exact original-blending-network certificates for the path shadow.

The active rows are physical input supplies and output cap/quality rows;
no Klee--Minty inequalities are inserted into the network certificate.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import sympy as sp


def vector(n, values):
    row = [F(0)]*(2*n)
    for j, v in values:
        row[j] = F(v)
    return row


def network(n):
    # Coordinates are left_j, right_j. Normalized supplies and qualities.
    supply = [F(4)**(j-n+1) for j in range(n)]
    quality = [F(n-j-1, n-1) for j in range(n)] if n > 1 else [F(0)]
    eq = [vector(n, [(2*j, 1), (2*j+1, 1)]) for j in range(n)]
    rows, rhs = [], []
    for k in range(2*n):
        rows.append(vector(n, [(k, -1)])); rhs.append(F(0))
        rows.append(vector(n, [(k, 1)])); rhs.append(supply[k//2])
    # End outputs have redundant quality and their physical upper caps.
    rows += [vector(n, [(0, 1)]), vector(n, [(2*n-1, 1)])]
    rhs += [supply[0], supply[-1]]
    active_pairs = []
    for j in range(1, n):
        cap = vector(n, [(2*j-1, 1), (2*j, 1)])
        bound = (quality[j-1]+quality[j])/2
        qual = vector(n, [(2*j-1, quality[j-1]-bound),
                           (2*j, quality[j]-bound)])
        rows += [cap, qual]; rhs += [supply[j], F(0)]
        active_pairs.append(((cap, supply[j]), (qual, F(0))))
    return supply, eq, rows, rhs, active_pairs


def exposing_parameter(bits):
    n = len(bits)
    return -sum((F(-1)**sum(bits[j:]))*F(1, 4)**(2*(n-j))
                for j in range(n))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=6)
    args = parser.parse_args()
    checked = 0
    for n in range(1, args.max_n+1):
        supply, eq, rows, rhs, pairs = network(n)
        slopes = set()
        for bits in product([0, 1], repeat=n):
            lam = exposing_parameter(bits)
            assert abs(lam) <= F(1, 15)
            active = [(vector(n, [(1 if bits[0] == 0 else 0, -1)]), F(0))]
            active += [pairs[j-1][bits[j]] for j in range(1, n)]
            B = sp.Matrix(eq+[r for r, _ in active])
            d = sp.Matrix(supply+[b for _, b in active])
            flow = B.inv()*d
            assert all(sum(sp.Rational(a)*v for a, v in zip(row, flow)) <= bound
                       for row, bound in zip(rows, rhs))
            weights = [F(16)**(j-n+1) for j in range(n-1)]+[lam]
            reward = sp.Matrix([0 if k % 2 == 0 else weights[k//2]
                                for k in range(2*n)])
            dual = B.T.inv()*reward
            assert all(v > 0 for v in dual[n:])
            assert (dual.T*d)[0] == (reward.T*flow)[0]
            # Strict positive physical-row multipliers and full rank certify
            # this flow is the unique maximizer for the actual network LP.
            slopes.add(flow[-1])
            revenues = [F(1)]
            for weight in weights:
                revenues.append(revenues[-1]+weight)
            assert all(F(0) <= r <= F(2) for r in revenues)
            actual_revenue = sum(revenues[j]*flow[2*j]+revenues[j+1]*flow[2*j+1]
                                 for j in range(n))
            constant = sum(revenues[j]*supply[j] for j in range(n))
            assert actual_revenue == constant+(reward.T*flow)[0]
            checked += 1
        assert len(slopes) == 2**n
        print(f'n={n}: {len(slopes)} distinct uniquely exposed original-network flows', flush=True)
    print(f'PASS {checked} exact primal/dual network certificates and price identities')


if __name__ == '__main__':
    main()
