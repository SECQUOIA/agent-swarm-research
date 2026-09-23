"""Exact integral-flow checks for adjacent-repeat rounding.

For an allocation matrix with unit column sums, this tests whether prefix error
at most one is compatible with selecting a specified mode in two adjacent slots.
The max-flow computation and all prefix bounds use exact integer arithmetic.
The existential property is proved separately by prefix uncrossing. The stronger
largest-mode property explored by this search remains unproved.
"""
from collections import deque
from fractions import Fraction as F
from random import Random


class Flow:
    def __init__(self, n):
        self.edges = [[] for _ in range(n)]

    def add(self, u, v, capacity):
        forward = [v, len(self.edges[v]), capacity]
        backward = [u, len(self.edges[u]), 0]
        self.edges[u].append(forward)
        self.edges[v].append(backward)
        return forward

    def maximum(self, source, sink):
        total = 0
        while True:
            parent = [None] * len(self.edges)
            parent[source] = (-1, -1)
            queue = deque([source])
            while queue and parent[sink] is None:
                u = queue.popleft()
                for j, (v, _, capacity) in enumerate(self.edges[u]):
                    if capacity and parent[v] is None:
                        parent[v] = (u, j)
                        queue.append(v)
            if parent[sink] is None:
                return total
            amount = 10**9
            v = sink
            while v != source:
                u, j = parent[v]
                amount = min(amount, self.edges[u][j][2])
                v = u
            v = sink
            while v != source:
                u, j = parent[v]
                edge = self.edges[u][j]
                edge[2] -= amount
                self.edges[v][edge[1]][2] += amount
                v = u
            total += amount


def rounded(a, mode, first=None, *, repeat=False):
    """Return a verified word with a forced pair, or tight-prefix repeated mode.

    repeat=True uses floor/ceiling bounds and requires final count of mode>=2.
    Otherwise first specifies the first slot of the forced adjacent pair.
    """
    n, M = len(a), len(a[0])
    assert 0 <= mode < n
    assert (repeat and first is None) or (not repeat and first is not None and 0 <= first < M-1)
    assert all(sum(a[i][j] for i in range(n)) == 1 for j in range(M))
    source, sink = 0, 1
    slot = lambda j: 2+j
    chain = lambda i,j: 2+M+i*M+j
    extra_source, extra_sink = 2+M+n*M, 3+M+n*M
    flow = Flow(extra_sink+1)
    balance = [0]*(extra_sink+1)

    def bounded(u,v,lower,upper):
        assert 0 <= lower <= upper
        balance[u] -= lower
        balance[v] += lower
        return flow.add(u,v,upper-lower)

    assignment = {}
    for j in range(M):
        bounded(source,slot(j),1,1)
        for i in range(n):
            if first is not None and j in (first,first+1) and i != mode:
                continue
            assignment[i,j] = bounded(slot(j),chain(i,j),0,1)
    for i,row in enumerate(a):
        cumulative = F(0)
        for j,value in enumerate(row):
            cumulative += value
            if repeat:
                lower = cumulative.numerator//cumulative.denominator
                upper = -(-cumulative.numerator//cumulative.denominator)
                if i == mode and j == M-1:
                    lower = max(2,lower)
                if lower > upper:
                    return None
            else:
                lower = max(0,-(-(cumulative-1).numerator//(cumulative-1).denominator))
                upper = (cumulative+1).numerator//(cumulative+1).denominator
            target = chain(i,j+1) if j+1<M else sink
            bounded(chain(i,j),target,lower,upper)
    bounded(sink,source,0,M)
    demand = 0
    for v,b in enumerate(balance):
        if b > 0:
            flow.add(extra_source,v,b)
            demand += b
        elif b < 0:
            flow.add(v,extra_sink,-b)
    if flow.maximum(extra_source,extra_sink) != demand:
        return None
    word = [next(i for i in range(n) if (i,j) in assignment and assignment[i,j][2] == 0)
            for j in range(M)]
    if first is not None:
        assert word[first] == word[first+1] == mode
    if repeat:
        assert word.count(mode) >= 2
    counts = [0]*n
    cumulative = [F(0)]*n
    for j,chosen in enumerate(word):
        counts[chosen] += 1
        for i in range(n):
            cumulative[i] += a[i][j]
            assert abs(counts[i]-cumulative[i]) <= 1
    return word


def verify():
    rng = Random(845209)
    profiles = modes = forced = 0
    for M in range(3,13):
        for trial in range(500):
            n = rng.randint(3,12)
            columns = []
            for _ in range(M):
                weights = [rng.randrange(8) for _ in range(n)]
                if trial%3:
                    weights[0] += 20
                if trial%3 == 2:
                    weights[1] += 20
                if not sum(weights):
                    weights[0] = 1
                columns.append([F(w,sum(weights)) for w in weights])
            a = [list(row) for row in zip(*columns)]
            heavy = sorted([i for i,row in enumerate(a) if sum(row,F(0)) > 1], key=lambda i: sum(a[i],F(0)), reverse=True)
            if not heavy:
                continue
            profiles += 1
            found = False
            for position,i in enumerate(heavy):
                modes += 1
                for j in range(M-1):
                    forced += 1
                    if rounded(a,i,j) is not None:
                        found = True
                        break
                if found:
                    break
                if position == 0:
                    print('COUNTEREXAMPLE TO LARGEST-HEAVY-MODE VERSION',M,n,i)
                    print([[str(x) for x in row] for row in a])
            if not found:
                print('COUNTEREXAMPLE TO EXISTENTIAL ADJACENT-REPEAT VERSION',M,n)
                print([[str(x) for x in row] for row in a])
                return
    print(f'No counterexample: {profiles} profiles, {modes} heavy-mode candidates, {forced} exact integral-flow tests.')
    print('This is finite experimental evidence, not a proof of the universal property.')


def verify_counterexamples():
    a = [[F(7,15),F(0),F(0),F(0)],
         [F(2,15),F(1,2),F(0),F(4,5)],
         [F(2,5),F(1,2),F(1),F(1,5)]]
    assert all(rounded(a,1,j) is None for j in range(3))
    assert rounded(a,2,1) is not None
    b = [[F(3,5),F(0),F(1,10),F(2,5),F(1)],
         [F(3,10),F(3,5),F(11,20),F(3,5),F(0)],
         [F(1,10),F(2,5),F(7,20),F(0),F(0)]]
    assert sum(b[0]) > max(sum(b[1]),sum(b[2]))
    assert all(rounded(b,0,j) is None for j in range(3))
    assert rounded(b,0,3) is not None
    print('Both false-strengthening counterexamples verified by exact integer flow.')


def verify_exhaustive():
    from itertools import product
    for denominator,M in ((3,4),(2,5),(2,6)):
        columns = [(F(i,denominator),F(j,denominator),F(denominator-i-j,denominator))
                   for i in range(denominator+1) for j in range(denominator-i+1)]
        count = 0
        for selected in product(columns,repeat=M):
            a = [list(row) for row in zip(*selected)]
            q = max(range(3),key=lambda i:sum(a[i]))
            assert sum(a[q]) > 1
            assert any(rounded(a,q,j) is not None for j in range(M-1)), a
            count += 1
        print(f'Exhaustive pass: three modes, M={M}, denominator={denominator}, {count} matrices.')


if __name__ == '__main__':
    import sys
    verify_counterexamples()
    if '--exhaustive' in sys.argv:
        verify_exhaustive()
    else:
        verify()
