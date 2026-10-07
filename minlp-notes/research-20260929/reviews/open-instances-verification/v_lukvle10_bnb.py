"""lukvle10: own partial-Lagrangian bound with an own 2-D interval branch and bound.

Rows j < m = 994 dualized with multipliers lam (own KKT multipliers at p5; entries
30..960 replaced by the double value lam[495]); rows 994..997 kept exact.
  bound = sum_{i<497} min_{R^2} l_i + min_{R^2} tau + sum_{j<m} lam_j
  l_i(a,b) = f(a,b) + beta_{2i} a + q_{2i} a^2 + beta_{2i+1} b + q_{2i+1} b^2
  beta_k = -lam_k + 3 lam_{k-1} - 2 lam_{k-2},  q_k = -2 lam_{k-1}  (lam_j = 0 for j<0 or j>=m)
  tau(a,b) = f(a,b) + f(P(a,b)) + f(P^2(a,b)) + beta_994 a + q_994 a^2 + beta_995 b (+ q_995 b^2, q_995 = 0)
  P(a,b) = (c,d): c = (-a + 3b - 2b^2 + 1)/2, d = (-b + 3c - 2c^2 + 1)/2.
All bounding in mpmath interval arithmetic (iv, 64-bit mantissa, outward rounding).
Box reduction: f(a,b) >= phi(a) + phi(b), phi(t) = t^2 (|t|>=1) else 0.
"""
import json, sys, time, heapq
import numpy as np
import mpmath
from mpmath import iv, mp, mpf
from multiprocessing import Pool

iv.prec = 64
mp.prec = 64
M = 994
TOL = 1e-12


def lo(x):
    return mp.make_mpf(x._mpi_[0])


def hi(x):
    return mp.make_mpf(x._mpi_[1])


def I(v):
    return iv.mpf(v)


def sq(X):
    return X ** 2  # mpmath iv even power: tight, >= 0


def ppow(b, e):
    """enclosure of b^e for point mpf b >= 0, e >= 0"""
    if b == 0:
        return iv.mpf(0)
    return iv.exp(iv.mpf(e) * iv.log(iv.mpf(b)))


def pow_range(Bs, E):
    """range of base^e over base in Bs (subset [0,inf)), e in E (subset [1,inf)); exact up to rounding"""
    blo, bhi = max(lo(Bs), mpf(0)), hi(Bs)
    elo, ehi = lo(E), hi(E)
    assert elo >= 1
    if blo == 0:
        mn = mpf(0)
    elif blo >= 1:
        mn = lo(ppow(blo, elo))
    else:
        mn = lo(ppow(blo, ehi))
    if bhi >= 1:
        mx = hi(ppow(bhi, ehi))
    else:
        mx = hi(ppow(bhi, elo))
    return iv.mpf([mn, mx])


def f_range(X, Y):
    X2, Y2 = sq(X), sq(Y)
    return pow_range(X2, Y2 + 1) + pow_range(Y2, X2 + 1)


def f_point(x, y):
    """interval enclosure of f at point intervals (tiny) x, y"""
    return f_range(x, y)


def f_grad(X, Y):
    """interval enclosure of (df/dx, df/dy) over the box; None if X or Y contains 0"""
    if lo(X) <= 0 <= hi(X) or lo(Y) <= 0 <= hi(Y):
        return None
    X2, Y2 = sq(X), sq(Y)
    lX, lY = iv.log(X2), iv.log(Y2)
    T1 = iv.exp((Y2 + 1) * lX)
    T2 = iv.exp((X2 + 1) * lY)
    fx = 2 * X * ((Y2 + 1) * iv.exp(Y2 * lX) + T2 * lY)
    fy = 2 * Y * ((X2 + 1) * iv.exp(X2 * lY) + T1 * lX)
    return fx, fy


def quad_lower(q, beta, A):
    """lower bound of q t^2 + beta t over interval A (q, beta intervals)"""
    a, b = iv.mpf(lo(A)), iv.mpf(hi(A))
    cands = [lo(q * a * a + beta * a), lo(q * b * b + beta * b)]
    if hi(q) > 0:
        if lo(q) <= 0:
            return lo(q * A * A + beta * A)
        v = -beta / (2 * q)
        if not (hi(v) < lo(A) or lo(v) > hi(A)):
            cands.append(lo(-(beta * beta) / (4 * q)))
    return min(cands)


class Pair:
    def __init__(self, ba, qa, bb, qb):
        self.ba, self.qa, self.bb, self.qb = ba, qa, bb, qb

    def point(self, a, b):
        A, B = iv.mpf(a), iv.mpf(b)
        return f_point(A, B) + self.qa * A * A + self.ba * A + self.qb * B * B + self.bb * B

    def lower(self, A, B):
        nat = lo(f_range(A, B)) + quad_lower(self.qa, self.ba, A) + quad_lower(self.qb, self.bb, B)
        g = f_grad(A, B)
        ca, cb = mpf(lo(A) + hi(A)) / 2, mpf(lo(B) + hi(B)) / 2
        Fc = self.point(ca, cb)
        if g is None:
            return nat, hi(Fc), (ca, cb)
        ga = g[0] + 2 * self.qa * A + self.ba
        gb = g[1] + 2 * self.qb * B + self.bb
        mv = lo(Fc + ga * (A - ca) + gb * (B - cb))
        return max(nat, mv), hi(Fc), (ca, cb)


class Tail:
    """tau(a,b) = f(a,b) + f(c,d) + f(e,g) + ba a + qa a^2 + bb b ; (c,d)=P(a,b), (e,g)=P(c,d)"""
    def __init__(self, ba, qa, bb):
        self.ba, self.qa, self.bb = ba, qa, bb

    @staticmethod
    def step(a, b):
        c = (-a + 3 * b - 2 * b * b + 1) / 2
        return c

    def maps(self, A, B):
        C = self.step(A, B)
        D = self.step(B, C)
        E = self.step(C, D)
        G = self.step(D, E)
        return C, D, E, G

    def point(self, a, b):
        A, B = iv.mpf(a), iv.mpf(b)
        C, D, E, G = self.maps(A, B)
        return f_point(A, B) + f_point(C, D) + f_point(E, G) + self.qa * A * A + self.ba * A + self.bb * B

    def lower(self, A, B):
        C, D, E, G = self.maps(A, B)
        nat = (lo(f_range(A, B)) + lo(f_range(C, D)) + lo(f_range(E, G)) + quad_lower(self.qa, self.ba, A)
               + lo(self.bb * B))
        ca, cb = mpf(lo(A) + hi(A)) / 2, mpf(lo(B) + hi(B)) / 2
        Fc = self.point(ca, cb)
        g0, g1, g2 = f_grad(A, B), f_grad(C, D), f_grad(E, G)
        if g0 is None or g1 is None or g2 is None:
            return nat, hi(Fc), (ca, cb)
        # forward-mode derivatives of the maps: d(new)/d(a,b) with new = (-x + 3y - 2y^2 + 1)/2
        one, zero = iv.mpf(1), iv.mpf(0)
        dA, dB = (one, zero), (zero, one)

        def dstep(dx, Y, dy):
            k = (3 - 4 * Y) / 2
            return (-dx[0] / 2 + k * dy[0], -dx[1] / 2 + k * dy[1])
        dC = dstep(dA, B, dB)
        dD = dstep(dB, C, dC)
        dE = dstep(dC, D, dD)
        dG = dstep(dD, E, dE)
        grad = []
        for k in range(2):
            s = g0[0] * dA[k] + g0[1] * dB[k] + g1[0] * dC[k] + g1[1] * dD[k] + g2[0] * dE[k] + g2[1] * dG[k]
            grad.append(s)
        grad[0] = grad[0] + 2 * self.qa * A + self.ba
        grad[1] = grad[1] + self.bb
        mv = lo(Fc + grad[0] * (A - ca) + grad[1] * (B - cb))
        return max(nat, mv), hi(Fc), (ca, cb)


def radius(q, beta, mother, U):
    """R >= 1 with (1+q) R^2 - |beta| R + mother > U + 1 and R >= |beta|/(2(1+q)); checked in intervals"""
    qq = float(lo(q)); bb = float(max(abs(lo(beta)), abs(hi(beta))))
    k = 1 + qq
    assert k > 0
    rhs = float(hi(U)) + 1 - float(lo(mother))
    R = max(1.0, bb / (2 * k), (bb + np.sqrt(bb * bb + 4 * k * max(rhs, 0))) / (2 * k)) * (1 + 1e-6) + 1e-9
    Rv = iv.mpf(R)
    val = (1 + q) * Rv * Rv - iv.mpf(bb) * Rv + mother
    assert lo(val) > hi(U) + 1 and R >= bb / (2 * k)
    return mpf(R)


def psi_min_lower(q, beta):
    """lower bound of min_t phi(t) + q t^2 + beta t"""
    babs = iv.mpf(max(abs(lo(beta)), abs(hi(beta))))
    qabs = iv.mpf(max(abs(lo(q)), abs(hi(q))))
    in1 = lo(-qabs - babs)
    out1 = lo(-(babs * babs) / (4 * (1 + q)))
    return iv.mpf(min(in1, out1))


def bnb(prob, box, x0, tol, maxboxes=400000):
    A0, B0 = box
    U = hi(prob.point(x0[0], x0[1]))
    lb0, u0, _ = prob.lower(A0, B0)
    U = min(U, u0)
    heap = [(lb0, 0, A0, B0)]
    cnt = 1; nb = 1
    while heap:
        lb, _, A, B = heapq.heappop(heap)
        if U - lb <= tol:
            return dict(LB=min(lb, U), UB=U, boxes=nb, open=len(heap) + 1)
        if nb > maxboxes:
            return dict(LB=lb, UB=U, boxes=nb, open=len(heap) + 1, incomplete=True)
        wa, wb = hi(A) - lo(A), hi(B) - lo(B)
        if wa >= wb:
            m = (lo(A) + hi(A)) / 2
            kids = [(iv.mpf([lo(A), m]), B), (iv.mpf([m, hi(A)]), B)]
        else:
            m = (lo(B) + hi(B)) / 2
            kids = [(A, iv.mpf([lo(B), m])), (A, iv.mpf([m, hi(B)]))]
        for (Ak, Bk) in kids:
            l, u, _ = prob.lower(Ak, Bk)
            nb += 1
            if u < U:
                U = u
            if l <= U:
                cnt += 1
                heapq.heappush(heap, (l, cnt, Ak, Bk))
    return dict(LB=U, UB=U, boxes=nb, open=0)


def coeffs(lam):
    """beta_k, q_k as intervals for k = 0..995 from double multipliers (lam_j = 0 outside [0, M))"""
    L = lambda j: iv.mpf(float(lam[j])) if 0 <= j < M else iv.mpf(0)
    beta = [-L(k) + 3 * L(k - 1) - 2 * L(k - 2) for k in range(996)]
    q = [-2 * L(k - 1) for k in range(996)]
    return beta, q


def solve_pair(args):
    key, i, lamw, x0 = args
    t0 = time.time()
    iv.prec = 64; mp.prec = 64
    Lw = [iv.mpf(float(v)) for v in lamw]  # lam_{2i-2}, lam_{2i-1}, lam_{2i}, lam_{2i+1}
    ba = -Lw[2] + 3 * Lw[1] - 2 * Lw[0]
    qa = -2 * Lw[1]
    bb = -Lw[3] + 3 * Lw[2] - 2 * Lw[1]
    qb = -2 * Lw[2]
    prob = Pair(ba, qa, bb, qb)
    U = prob.point(x0[0], x0[1])
    Ra = radius(qa, ba, psi_min_lower(qb, bb), U)
    Rb = radius(qb, bb, psi_min_lower(qa, ba), U)
    res = bnb(prob, (iv.mpf([-Ra, Ra]), iv.mpf([-Rb, Rb])), x0, TOL)
    res.update(key=key, first_pair=i, R=[float(Ra), float(Rb)], seconds=time.time() - t0)
    res['LB'] = mpmath.nstr(res['LB'], 20); res['UB'] = mpmath.nstr(res['UB'], 20)
    return res


def solve_tail(args):
    lam_tail, x0, tol = args
    t0 = time.time()
    iv.prec = 64; mp.prec = 64
    l992, l993 = iv.mpf(float(lam_tail[0])), iv.mpf(float(lam_tail[1]))
    ba = 3 * l993 - 2 * l992
    qa = -2 * l993
    bb = -2 * l993
    prob = Tail(ba, qa, bb)
    U = prob.point(x0[0], x0[1])
    zero = iv.mpf(0)
    Ra = radius(qa, ba, psi_min_lower(zero, bb), U)
    Rb = radius(zero, bb, psi_min_lower(qa, ba), U)
    res = bnb(prob, (iv.mpf([-Ra, Ra]), iv.mpf([-Rb, Rb])), x0, tol, maxboxes=3000000)
    res.update(tail=True, R=[float(Ra), float(Rb)], seconds=time.time() - t0)
    res['LB'] = mpmath.nstr(res['LB'], 20); res['UB'] = mpmath.nstr(res['UB'], 20)
    return res


def main(nproc=8):
    lam = np.load('logs/lukvle10_lam_kkt.npy').copy()
    x5 = np.load('logs/lukvle10_x5.npy')
    LC = lam[495]
    lam[30:961] = LC
    # pair problems, grouped by the four multipliers they use
    groups = {}
    for i in range(497):
        w = tuple(float(lam[j]) if 0 <= j < M else 0.0 for j in (2 * i - 2, 2 * i - 1, 2 * i, 2 * i + 1))
        groups.setdefault(w, []).append(i)
    tasks = [(k, v[0], k, (float(x5[2 * v[0]]), float(x5[2 * v[0] + 1]))) for k, v in groups.items()]
    t0 = time.time()
    with Pool(nproc) as pool:
        tail_async = pool.apply_async(solve_tail, (((lam[992], lam[993]), (float(x5[994]), float(x5[995])), 1e-9),))
        res = pool.map(solve_pair, tasks, chunksize=1)
        tail = tail_async.get()
    out = dict(n_groups=len(groups), LC=float(LC), groups=[])
    for r in res:
        cnt = len(groups[r['key']])
        out['groups'].append(dict(first_pair=r['first_pair'], count=cnt, R=r['R'], LB=r['LB'], UB=r['UB'],
                                  boxes=r['boxes'], open=r['open'], seconds=round(r['seconds'], 1),
                                  incomplete=r.get('incomplete', False)))
    out['tail'] = tail
    print(json.dumps(out['tail']), flush=True)
    # certified sum: use exact lower ends (LB strings are nstr-rounded -> subtract 1e-18 relative safety)
    tot = iv.mpf(0)
    for g in out['groups']:
        tot += g['count'] * (iv.mpf(g['LB']) - iv.mpf('1e-18'))
    tot += iv.mpf(tail['LB']) - iv.mpf('1e-18')
    s = iv.mpf(0)
    for j in range(M):
        s += iv.mpf(float(lam[j]))
    bound = tot + s
    ub = iv.mpf(0)
    for g in out['groups']:
        ub += g['count'] * iv.mpf(g['UB'])
    ub += iv.mpf(tail['UB'])
    out['sum_lam'] = mpmath.nstr(lo(s), 20)
    out['dual_bound'] = mpmath.nstr(lo(bound), 16)
    out['sum_of_upper_ends'] = mpmath.nstr(hi(ub + s), 16)
    out['seconds'] = time.time() - t0
    print(json.dumps({k: v for k, v in out.items() if k != 'groups'}, indent=1))
    json.dump(out, open('logs/lukvle10_bnb.json', 'w'), indent=1)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
