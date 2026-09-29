"""Scratch check: principal-ideal testing in a pure cubic field as a
3-variable integer cubic minimization over a rational polyhedral cone.

For K=Q(theta), theta^3=m with Z[theta] the maximal order (checked), identify
y=(a,b,c) with a+b*theta+c*theta^2.  N(y)=a^3+m b^3+m^2 c^3-3m abc is the
norm form.  Q is a rational pointed cone around the real direction where the
complex embedding sigma2 vanishes; its extreme rays are checked to satisfy
sigma1>0, so N=sigma1*|sigma2|^2>0 on lattice points of Q minus 0.
For an ideal I, min{N(y): y in I cap Q, y != 0} equals Norm(I) iff I is
principal (unit multiples of a generator eventually enter Q).
The script enumerates all lattice points of I in Q with 1<=c<=Cmax.
Membership in I uses the integer HNF basis H: y in I iff adj(H) y = 0 mod det H.
"""
import itertools
from fractions import Fraction as F
import numpy as np
import cypari2

pari = cypari2.Pari()


def cone_rows(m, den=10**6):
    th = m ** (1.0 / 3)
    s3 = 3 ** 0.5
    r = lambda v: F(round(v * den), den)
    s1 = [F(1), r(th), r(th * th)]
    re = [F(1), r(-th / 2), r(-th * th / 2)]
    im = [F(0), r(s3 * th / 2), r(-s3 * th * th / 2)]
    rows = []  # g.y >= 0
    for e1, e2 in itertools.product([1, -1], repeat=2):
        g = [s1[i] - 2 * (e1 * re[i] + e2 * im[i]) for i in range(3)]
        L = 1
        for x in g:
            L = L * x.denominator // np.gcd(L, x.denominator)
        rows.append([int(x * L) for x in g])  # integer rows, same cone
    return rows, th


def extreme_rays(rows):
    rays = []
    for g, h in itertools.combinations(rows, 2):
        v = np.cross(np.array(g, dtype=float), np.array(h, dtype=float))
        for s in (1, -1):
            w = s * v
            if all(np.dot(r, w) >= -1e-6 * np.linalg.norm(w) * np.linalg.norm(r) for r in rows):
                rays.append(w / np.linalg.norm(w))
    return rays


def run(m, ideals, Cmax):
    rows, th = cone_rows(m)
    rays = extreme_rays(rows)
    s1 = lambda y: y[0] + th * y[1] + th * th * y[2]
    assert rays and all(s1(r) > 0 for r in rays), "cone not inside sigma1>0"
    assert all(r[2] > 0 for r in rays), "c>=1 must exclude only the origin"
    bnf = pari(f'bnfinit(x^3-{m},1)')
    assert [str(t) for t in pari('(b)->b.zk')(bnf)] == ['1', 'x', 'x^2']
    R = np.array(rows, dtype=np.int64)
    for name, I in ideals:
        Ip = pari(I) if not isinstance(I, str) or not I.startswith('bnf') else pari(I)
        H = pari('(b,I)->idealhnf(b,I)')(bnf, Ip)
        Hm = [[int(H[i, j]) for j in range(3)] for i in range(3)]
        det = int(pari('matdet')(H))
        adj = [[int(pari('(M)->matadjoint(M)')(H)[i, j]) for j in range(3)] for i in range(3)]
        nI = int(pari('(b,I)->idealnorm(b,I)')(bnf, Ip))
        cls = [int(t) for t in pari('(b,I)->bnfisprincipal(b,I,0)')(bnf, Ip)]
        principal = all(t == 0 for t in cls)
        best, arg = None, None
        nr = [r / r[2] for r in rays]
        amin, amax = min(r[0] for r in nr), max(r[0] for r in nr)
        bmin, bmax = min(r[1] for r in nr), max(r[1] for r in nr)
        for c in range(1, Cmax + 1):
            bs = np.arange(int(np.floor(bmin * c)) - 1, int(np.ceil(bmax * c)) + 2, dtype=np.int64)
            as_ = np.arange(int(np.floor(amin * c)) - 1, int(np.ceil(amax * c)) + 2, dtype=np.int64)
            A, Bv = np.meshgrid(as_, bs, indexing='ij')
            A = A.ravel(); Bv = Bv.ravel(); C = np.full_like(A, c)
            ok = np.ones(A.shape, dtype=bool)
            for r in rows:
                ok &= (r[0] * A + r[1] * Bv + r[2] * C) >= 0
            A, Bv, C = A[ok], Bv[ok], C[ok]
            memb = np.ones(A.shape, dtype=bool)
            for i in range(3):
                memb &= ((adj[i][0] * A + adj[i][1] * Bv + adj[i][2] * C) % det) == 0
            A, Bv, C = A[memb], Bv[memb], C[memb]
            if A.size == 0:
                continue
            assert np.abs(A).max() < 10**5 and np.abs(Bv).max() < 10**5 and c < 10**4
            Nv = A**3 + m * Bv**3 + m * m * C**3 - 3 * m * A * Bv * C
            assert (Nv > 0).all() and (Nv % nI == 0).all()
            k = int(np.argmin(Nv))
            if best is None or int(Nv[k]) < best:
                best, arg = int(Nv[k]), (int(A[k]), int(Bv[k]), c)
        print(f'm={m} ideal={name} Norm(I)={nI} class={cls} principal={principal} '
              f'min N on I cap Q (1<=c<={Cmax}) = {best} at {arg}', flush=True)
        if principal:
            assert best == nI, 'principal: generator not reached in window'
        else:
            assert best is None or best > nI


if __name__ == '__main__':
    run(2, [('O_K', '1'), ('(3+x^2)', 'Mod(3+x^2,x^3-2)')], Cmax=30)
    b11 = 'bnfinit(x^3-11,1)'
    run(11, [('O_K', '1'), ('(2+x)', 'Mod(2+x,x^3-11)'),
             ('P2', f'idealprimedec({b11},2)[1]'),
             ('P3', f'idealprimedec({b11},3)[1]'),
             ('P5a', f'idealprimedec({b11},5)[1]'),
             ('P2^2', f'idealpow({b11},idealprimedec({b11},2)[1],2)')], Cmax=120)
