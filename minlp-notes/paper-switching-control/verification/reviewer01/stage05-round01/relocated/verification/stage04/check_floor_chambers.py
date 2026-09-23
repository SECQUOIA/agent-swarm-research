"""Exact floor-graph coverage, five/six/seven-cell theorems, and witnesses.

No external packages, numerical solver, or saved certificate is used. Run with
ordinary Python: the explicit optimization guard prevents disabled assertions.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product, permutations

if not __debug__:
    raise RuntimeError('Exact checks require Python without -O.')


def offset(sigma, node):
    return tuple(int(i == node) if sigma == 1 else int(i != node)
                 for i in range(3))


def transitions(sigma):
    for next_sigma in (1, 2):
        for delta in product((0, 1), repeat=3):
            if sum(delta) == 1 + sigma - next_sigma:
                yield next_sigma, delta


def edges(sigma, next_sigma, delta):
    result = []
    for u, v in product(range(3), repeat=2):
        change = tuple(delta[i] + offset(next_sigma, v)[i]
                       - offset(sigma, u)[i] for i in range(3))
        if sorted(change) == [0, 0, 1]:
            result.append((u, v, change.index(1)))
    assert {u for u, v, a in result} == {0, 1, 2}
    assert {v for u, v, a in result} == {0, 1, 2}
    return result


def advance(cost, sigma, next_sigma, delta):
    result = [[None] * 3 for _ in range(3)]
    for u, v, b in edges(sigma, next_sigma, delta):
        for a in range(3):
            if cost[u][a] is not None:
                candidate = cost[u][a] + (a != b)
                if result[v][b] is None or candidate < result[v][b]:
                    result[v][b] = candidate
    return result


def minimum(cost):
    return min(c for row in cost for c in row if c is not None)


def initial():
    return [[0 if u == a else None for a in range(3)] for u in range(3)]


def all_histories(N):
    def visit(history, sigma, cost):
        if len(history) == N:
            yield history, cost
        else:
            for next_sigma, delta in transitions(sigma):
                floor = tuple(history[-1][i] + delta[i] for i in range(3))
                yield from visit(history + (floor,), next_sigma,
                                 advance(cost, sigma, next_sigma, delta))
    yield from visit(((0, 0, 0),), 1, initial())


def prefixes(word):
    counts = [0, 0, 0]
    result = []
    for a in word:
        counts[a] += 1
        result.append(tuple(counts))
    return tuple(result)


def switches(word):
    return sum(a != b for a, b in zip(word, word[1:]))


def error(cumulative, word):
    return max(abs(a - w) for A, W in zip(cumulative, prefixes(word))
               for a, w in zip(A, W))


def floor_history(cumulative):
    return tuple(tuple(x.numerator // x.denominator for x in A)
                 for A in cumulative)


def run():
    expected_totals = (1, 4, 18, 84, 396, 1872, 8856)
    distributions = {}
    bad = []
    for N, total in enumerate(expected_totals, 1):
        histories = list(all_histories(N))
        assert len(histories) == total
        assert len({h for h, c in histories}) == total
        dist = Counter(minimum(c) for h, c in histories)
        distributions[N] = dict(sorted(dist.items()))
        if N == 5:
            assert dist == {0: 3, 1: 138, 2: 255}
        if N == 6:
            assert max(dist) == 3
        if N == 7:
            assert dist == {0: 3, 1: 414, 2: 4542, 3: 3891, 4: 6}
            bad = [h for h, c in histories if minimum(c) == 4]
    triples = ((1,1,1),(4,1,1),(4,4,1),(4,4,4),
               (7,4,4),(8,5,5),(8,5,8))
    cumulative = tuple(tuple(Q(x,3) for x in row) for row in triples)
    canonical = floor_history(cumulative)
    orbit = {tuple(tuple(row[p[i]] for i in range(3)) for row in canonical)
             for p in permutations(range(3))}
    assert len(orbit) == 6 and set(bad) == orbit
    matrices = [initial()]
    for j in range(1, 7):
        sigma = j - sum(canonical[j-1])
        next_sigma = j+1 - sum(canonical[j])
        delta = tuple(b-a for a,b in zip(canonical[j-1],canonical[j]))
        matrices.append(advance(matrices[-1],sigma,next_sigma,delta))
    expected_matrices = [
        [[0,None,None],[None,0,None],[None,None,0]],
        [[0,None,None],[1,1,None],[1,None,1]],
        [[1,1,None],[None,1,None],[None,2,2]],
        [[3,None,2],[None,2,2],[None,None,2]],
        [[3,None,None],[3,3,None],[3,None,2]],
        [[None,3,4],[3,None,4],[3,4,None]],
        [[None,None,4],[None,None,4],[4,4,4]],
    ]
    assert matrices == expected_matrices
    repairs = ((1,2,0,0,0,2,2),(0,0,2,1,1,2,2),(0,0,1,1,2,2,0))
    for mode, word in enumerate(repairs):
        assert switches(word) <= 3
        violations = [(j,i,W[i]) for j,(f,W) in enumerate(zip(canonical,prefixes(word)))
                      for i in range(3) if not f[i] <= W[i] <= f[i]+1]
        assert violations == [(mode+1,mode,0)], violations
    feasible = []
    all_words = tuple(product(range(3),repeat=7))
    for word in all_words:
        if all(f[i] <= W[i] <= f[i]+1
               for f,W in zip(canonical,prefixes(word)) for i in range(3)):
            feasible.append(word)
    assert len(feasible) == 104 and min(map(switches,feasible)) == 4
    assert min(error(cumulative,w) for w in all_words if switches(w)<=3) == Q(4,3)
    witness_word = (0,0,1,1,0,2,2)
    assert switches(witness_word) == 3 and error(cumulative,witness_word) == Q(4,3)
    for N,budget in ((5,2),(6,3)):
        target = prefixes(tuple(j%2 for j in range(N)))
        assert min(error(target,w) for w in product(range(3),repeat=N)
                   if switches(w)<=budget) == 1
    target = prefixes((0,1,2,0,1))
    assert error(target,(0,0,1,1,2)) == 1
    print('Exact distributions by minimum chamber switch count:', distributions)
    print('Seven-cell exceptional histories: six mode permutations; all three repair words verified.')
    print('Seven-cell witness: 2187 words, 104 chamber words, grid OPT_3 = 4/3.')
    print('Five/six-cell lower witnesses and continuous two-switch witness verified.')
    return distributions


if __name__ == '__main__':
    run()
