"""Independent exact KKT and finite-regularization gap checks."""
from fractions import Fraction as F
from itertools import product
from random import Random

from exact_shadow_check import vertex
from exact_rank_one_slab_check import coefficients


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def main():
    rng = Random(124078)
    certificates = gaps = 0
    for n in range(1, 9):
        for _ in range(3):
            weights = [rng.randint(1, 12) for _ in range(n)]
            W = sum(weights)
            eps = F(1, 8*W)
            D = (8*W)**(n-1)
            separation = F(1, D*D)
            tau = separation/(2*n)
            c = coefficients(n, eps)
            vertices = {bits: vertex(bits, eps) for bits in product((0, 1), repeat=n)}
            items = list(vertices.items())
            for bits, v in items:
                lam = 2*v[-1]-1
                assert -1 <= lam <= 1
                p = c[:]
                p[-1] += lam
                # Normal cone KKT equation B^T mu=p-tau*v. Each active
                # row has diagonal sign2u-1 and predecessor coefficient eps.
                mu = [F(0)]*n
                for j in range(n-1, -1, -1):
                    tail = eps*mu[j+1] if j+1 < n else 0
                    mu[j] = (2*bits[j]-1)*(p[j]-tau*v[j]-tail)
                    assert mu[j] > 0
                for j in range(n):
                    normal = (2*bits[j]-1)*mu[j]
                    if j+1 < n:
                        normal += eps*mu[j+1]
                    assert normal == p[j]-tau*v[j]
                for _ in range(2):
                    chosen = [items[rng.randrange(len(items))] for _ in range(3)]
                    numerators = [rng.randint(1, 8) for _ in range(3)]
                    alphas = [F(a, sum(numerators)) for a in numerators]
                    z = [sum(a*u[j] for a, (_, u) in zip(alphas, chosen)) for j in range(n)]
                    off_mass = sum(a for a, (u_bits, _) in zip(alphas, chosen) if u_bits != bits)
                    actual_gap = tau*(dot(z,z)-dot(v,v))/2 - dot(p, [a-b for a,b in zip(z,v)])
                    assert actual_gap >= separation*off_mass/2
                    assert (actual_gap == 0) == (z == v)
                    gaps += 1
                certificates += 1
    print(f'PASS: {certificates} exact strictly positive KKT certificates for scalar-parameter diagonal QP responses.')
    print(f'PASS: {gaps} exact regularized objective-gap bounds on convex combinations.')


if __name__ == '__main__':
    main()
