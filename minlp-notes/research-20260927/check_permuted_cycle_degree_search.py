"""Exact finite search over assignments of squares to a neighbor cycle.

The search supports the investigation. Its finite range does not prove
the all-dimension bound obtained from the interlace polynomial.
"""

import argparse
from itertools import combinations_with_replacement, product
from math import gcd

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form


def determinant_integer(matrix):
    """Fraction-free elimination with exact integer pivoting."""
    a = [list(row) for row in matrix]
    previous, sign = 1, 1
    for k in range(len(a) - 1):
        if a[k][k] == 0:
            other = next((j for j in range(k + 1, len(a)) if a[j][k]), None)
            if other is None:
                return 0
            a[k], a[other] = a[other], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        for i in range(k + 1, len(a)):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def admissible_permutations(size):
    def recurse(row, used, prefix):
        if row == size:
            yield tuple(prefix)
            return
        for column in range(size):
            if used >> column & 1 or column in (row, (row + 1) % size):
                continue
            prefix.append(column)
            yield from recurse(row + 1, used | (1 << column), prefix)
            prefix.pop()

    return recurse(0, 0, [])


def grounded_matrix(permutation):
    size = len(permutation)
    return [
        [2 * (permutation[i] == j) - (i == j) - ((i + 1) % size == j)
         for j in range(1, size)]
        for i in range(1, size)
    ]


def search(size):
    maximum, count, witness = 0, 0, None
    for permutation in admissible_permutations(size):
        matrix = grounded_matrix(permutation)
        cofactor = abs(determinant_integer(matrix))
        # Distinct implementation check on every smaller matrix.
        if size <= 6:
            assert cofactor == abs(int(sp.Matrix(matrix).det()))
        assert cofactor > 0 and cofactor % 2 == 1
        count += 1
        if cofactor > maximum:
            maximum, witness = cofactor, permutation
    expected = (2 ** size - (-1) ** size) // 3
    assert maximum == expected
    smith = smith_normal_form(sp.Matrix(grounded_matrix(witness)), domain=sp.ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(size - 1)]
    assert diagonal == [1] * (size - 2) + [maximum]
    return size, count, maximum, witness


def check_small_networks(size):
    """All two-out multigraphs, including loops and repeated arcs."""
    neighbor_pairs = list(combinations_with_replacement(range(size), 2))
    count, odd_count, maximum_odd_index = 0, 0, 0
    for pairs in product(neighbor_pairs, repeat=size):
        adjacency = [[0] * size for _ in range(size)]
        for row, pair in enumerate(pairs):
            for column in pair:
                adjacency[row][column] += 1

        def reachable(reverse=False):
            seen, stack = {0}, [0]
            while stack:
                vertex = stack.pop()
                for other in range(size):
                    present = adjacency[other][vertex] if reverse else adjacency[vertex][other]
                    if present and other not in seen:
                        seen.add(other)
                        stack.append(other)
            return len(seen) == size

        if not reachable() or not reachable(reverse=True):
            continue
        count += 1
        laplacian = [[2 * (i == j) - adjacency[i][j] for j in range(size)] for i in range(size)]
        trees = [determinant_integer([
            [laplacian[i][j] for j in range(size) if j != root]
            for i in range(size) if i != root
        ]) for root in range(size)]
        assert all(0 < value <= 2 ** (size - 1) for value in trees)
        index = gcd(*trees)
        eulerian = all(sum(adjacency[i][j] for i in range(size)) == 2 for j in range(size))
        if not eulerian:
            assert max(value // index for value in trees) >= 2
            assert index <= 2 ** (size - 2)
        else:
            assert all(value == index for value in trees)
        if index % 2:
            odd_count += 1
            maximum_odd_index = max(maximum_odd_index, index)
            assert index <= (2 ** size - (-1) ** size) // 3
    return size, count, odd_count, maximum_odd_index


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', type=int, default=10)
    args = parser.parse_args()
    assert 3 <= args.max_size <= 12
    for size in range(3, args.max_size + 1):
        print(search(size), flush=True)
    example = (2, 0, 1, 5, 3, 4)
    smith = smith_normal_form(sp.Matrix(grounded_matrix(example)), domain=sp.ZZ)
    assert [abs(int(smith[i, i])) for i in range(5)] == [1, 1, 1, 3, 3]
    print('Passed: all tested maxima equal Jacobsthal; maximizing witnesses have cyclic torsion.')
    print('Confirmed noncyclic example at size 6: permutation (2,0,1,5,3,4), torsion Z/3 + Z/3.')
    for size in (3, 4):
        print('All two-out multigraphs (size, strongly connected, odd index, maximum odd index):',
              check_small_networks(size))
