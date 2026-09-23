"""Independent exact checks of the positive-vector obstruction constants."""
from fractions import Fraction as F
from itertools import product


def main():
    margin = F(7, 4) * (F(2, 3) * F(15, 16) - F(3, 67))
    assert margin == F(2177, 2144) > 1
    D = [128 * 1024 ** j for j in range(16)]
    x = [1 - F(64, d) for d in D]
    pairs = 0
    for j in range(16):
        assert D[j] == 2 ** (10 * (j + 1) - 3)
        assert F(1, 2) <= x[j] < 1
        for ell in range(j + 1, 16):
            assert 1 - F(64 * D[j], D[ell]) >= F(15, 16)
            xi = (x[j] + 2 * x[ell]) / 3
            assert xi <= 1 - F(64, 3 * D[j])
            pairs += 1
    # Actual powers, independently of the analytic estimates, in component 1.
    for ell in range(1, 16):
        xi = (x[0] + 2 * x[ell]) / 3
        actual = F(7, 4) * ((x[0] ** D[0] + 2 * x[ell] ** D[0]) / 3 - xi ** D[0])
        assert actual >= margin
    residues = 0
    for p in (1, 2):
        vectors = list(product(range(-3, 4), repeat=p))
        for a in vectors:
            for b in vectors:
                if all((ai - bi) % 3 == 0 for ai, bi in zip(a, b)):
                    assert all((ai + 2 * bi) % 3 == 0 for ai, bi in zip(a, b))
                    residues += 1
    print(f'PASS: {pairs} rational witness pairs; 15 actual-power gaps; {residues} residue combinations')


if __name__ == '__main__':
    main()
