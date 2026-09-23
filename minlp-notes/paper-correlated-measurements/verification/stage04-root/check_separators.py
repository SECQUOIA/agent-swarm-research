"""Independent exact checks of separator elimination and mixture ordering."""
from itertools import combinations
from pathlib import Path
import json
import sympy as s

Q = s.Rational
n, p = 5, 2
T = s.eye(n)
transitions = [Q(-2, 3), Q(1, 2), Q(3, 5), Q(-1, 4)]
for i in range(1, n):
    for j in range(i):
        T[i, j] = transitions[i-1]*T[i-1, j]
K = T*s.diag(Q(2), Q(1, 3), Q(2, 5), Q(3, 7), Q(1, 2))*T.T
R = K+s.diag(Q(1, 2), Q(2, 3), Q(1), Q(3, 4), Q(4, 5))
F = s.Matrix([[1, -2], [2, 1], [-1, 3], [Q(1, 3), -1], [1, 2]])
J0 = s.Matrix([[2, Q(1, 3)], [Q(1, 3), 1]])

def principal(M, ix):
    return M.extract(ix, ix)

def psd(M):
    assert M == M.T
    for k in range(1, M.rows+1):
        for ix in combinations(range(M.rows), k):
            assert principal(M, ix).det() >= 0

def eliminate(M, kept):
    gone = [i for i in range(M.rows) if i not in kept]
    if not gone:
        return principal(M, kept)
    C = principal(M, gone)
    B = M.extract(kept, gone)
    return principal(M, kept)-B*C.inv()*B.T

def augmented(anchors, selected):
    if anchors:
        KA = principal(K, anchors)
        H = K.extract(range(n), anchors)*KA.inv()
        D = R-H*KA*H.T
        base = s.diag(J0, KA.inv())
    else:
        H = s.zeros(n, 0)
        D = R
        base = J0
    if not selected:
        return base
    V = F.row_join(H).extract(selected, range(p+len(anchors)))
    return base+V.T*principal(D, selected).inv()*V

subsets = [list(ix) for k in range(n+1) for ix in combinations(range(n), k)]
anchor_pairs = [([], [1, 3]), ([1], [1, 3]), ([3], [1, 3]),
                ([0, 3], [0, 2, 3, 4]), ([], list(range(n)))]
counts = {'exact_eliminations': 0, 'mixture_orderings': 0, 'quadratic_supports': 0}
for aa, bb in anchor_pairs:
    small = [augmented(aa, ix) for ix in subsets]
    big = [augmented(bb, ix) for ix in subsets]
    kept = list(range(p))+[p+bb.index(a) for a in aa]
    for ix, ma, mb in zip(subsets, small, big):
        assert ma == eliminate(mb, kept)
        j = J0 if not ix else J0+F.extract(ix, range(p)).T*principal(R, ix).inv()*F.extract(ix, range(p))
        assert eliminate(ma, list(range(p))) == j
        counts['exact_eliminations'] += 1
    for t in range(8):
        indices = [(t+3)%32, (3*t+7)%32, (5*t+11)%32]
        weights = [Q(1, 5), Q(1, 3), Q(7, 15)]
        ma = sum((w*small[i] for w, i in zip(weights, indices)), s.zeros(p+len(aa)))
        mb = sum((w*big[i] for w, i in zip(weights, indices)), s.zeros(p+len(bb)))
        psd(eliminate(mb, kept)-ma)
        ja, jb = eliminate(ma, list(range(p))), eliminate(mb, list(range(p)))
        psd(jb-ja)
        assert jb.det() >= ja.det()
        counts['mixture_orderings'] += 1
        G = s.Matrix(len(bb), p, lambda i,j: Q((-1)**(i+j)*(i+j+1), 7))
        E = s.eye(p).col_join(G)
        for i in indices:
            psd(E.T*big[i]*E-eliminate(big[i], list(range(p))))
            counts['quadratic_supports'] += 1
result = {'status': 'PASS', 'arithmetic': 'exact rational', 'counts': counts,
          'scope': 'Finite checks supplement the manuscript proofs; no performance claim.'}
Path(__file__).with_name('separator-results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result))
