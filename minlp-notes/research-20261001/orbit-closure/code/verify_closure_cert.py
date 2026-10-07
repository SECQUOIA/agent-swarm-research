"""Separate exact verification of a closure-point certificate written by
certify_closure_point.py.

Checks, in exact rational arithmetic:
  0. lam_hat has exactly one nonnegative entry per ray;
  1. covering: starting from Delta = conv{0, e_j / lam_j (lam_j > 0)}, recursive bisection of the
     longest edge (exact squared lengths over the coordinates with lam_j > 0, first pair in
     lexicographic order on ties) reaches exactly the listed pieces, so the pieces cover Delta;
  2. for every SDP piece: Y_j symmetric PSD (Y_j = 0 if lam_j = 0), R = -M(sbar)^{-1} sum_j M0(p_j) Y_j
     symmetric, Q(a) = R - sum_j a_j Y_j PSD with positive trace at every vertex, and (family B)
     u . (X_11, X_12) >= 0 for both sector directions u and every X in {Y_j} and {Q(vertex)};
  3. for every piece marked 'outside': the listed point x is in X (x >= 0, q(sbar + P x) <= 0) and
     x_j = 0 when lam_j = 0, and a^T x < 1 at every vertex (so the piece,
     including its unbounded inactive coordinates, contains no cut vector valid for X);
  4. family B: the sectors are consecutive closed cones of angle < pi covering the closed half-plane
     {f : f . (1, -sbar_y) >= 0} of first rows of F.
Usage: python3 verify_closure_cert.py CERT.json
"""
import sys, json, itertools
from fractions import Fraction as Fr

ok_all = True


def check(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name, flush=True)


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def psd(X):
    return X[0][1] == X[1][0] and X[0][0] >= 0 and X[1][1] >= 0 and X[0][0] * X[1][1] - X[0][1] * X[1][0] >= 0


def main(path):
    global ok_all
    ok_all = True
    d = json.load(open(path))
    inst, fam = d['instance'], d['family']
    sb = [Fr(v) for v in inst['sbar']]
    if 'verts' in inst:
        P = [[Fr(v[i]) - sb[i] for i in range(3)] for v in inst['verts']]
    else:
        P = [[Fr(x) for x in p] for p in inst['rays']]
    n = len(P)
    lam = [Fr(v) for v in inst['lam']]
    check('lam_hat has exactly one entry per ray', len(lam) == n)
    check('lam_hat is nonnegative', all(v >= 0 for v in lam))
    if not ok_all:
        print('SOME CHECK FAILED')
        return 1
    act = [j for j in range(n) if lam[j] > 0]
    Ms = [[sb[2], sb[0]], [sb[1], Fr(1)]]
    det = Ms[0][0] * Ms[1][1] - Ms[0][1] * Ms[1][0]
    Msi = [[Ms[1][1] / det, -Ms[0][1] / det], [-Ms[1][0] / det, Ms[0][0] / det]]
    N = [mm(Msi, [[p[2], p[0]], [p[1], Fr(0)]]) for p in P]
    q = lambda s: s[2] - s[0] * s[1]
    check('q(sbar) = %s > 0' % q(sb), q(sb) > 0)
    print('lam_hat = %s, sum = %s' % ([str(v) for v in lam], sum(lam)))
    xpts = [[Fr(v) for v in x] for x in inst.get('xpoints', [])]
    points_ok = True
    for x in xpts:
        if len(x) != n:
            points_ok = False
            continue
        s = [sb[i] + sum(x[j] * P[j][i] for j in range(n)) for i in range(3)]
        points_ok &= all(v >= 0 for v in x) and q(s) <= 0
    if xpts:
        check('all %d pruning points lie in X' % len(xpts), points_ok)
        if not points_ok:
            print('SOME CHECK FAILED')
            return 1

    def split(piece):
        best = None
        for i, k in itertools.combinations(range(len(piece)), 2):
            dd = sum((piece[i][m] - piece[k][m]) ** 2 for m in act)
            if best is None or dd > best[0]:
                best = (dd, i, k)
        _, i, k = best
        mid = tuple((piece[i][m] + piece[k][m]) / 2 for m in range(n))
        return (tuple(v if idx != i else mid for idx, v in enumerate(piece)),
                tuple(v if idx != k else mid for idx, v in enumerate(piece)))

    if fam == 'B':
        secs = [[[Fr(v) for v in u] for u in blk['sector']] for blk in d['blocks']]
        if d.get('sector_ids') is None:
            nrm = (Fr(1), -sb[1])
            dot = lambda u, v: u[0] * v[0] + u[1] * v[1]
            cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
            good = True
            good &= dot(secs[0][0], nrm) == 0 and cross(nrm, secs[0][0]) < 0     # starts on the boundary, clockwise side
            good &= dot(secs[-1][1], nrm) == 0 and cross(nrm, secs[-1][1]) > 0
            for i, (u, v) in enumerate(secs):
                good &= cross(u, v) > 0                                         # angle in (0, pi)
                if i + 1 < len(secs):
                    good &= secs[i + 1][0] == v                                  # consecutive
            check('sectors are consecutive and cover the half-plane f.(1, -sbar_y) >= 0', good)
        else:
            print('note: partial sector set %s (other sectors in other files)' % d['sector_ids'])
    for blk in d['blocks']:
        sec = None if blk['sector'] is None else [[Fr(v) for v in u] for u in blk['sector']]
        pieces = {}
        for pc in blk['pieces']:
            key = tuple(tuple(Fr(v) for v in a) for a in pc['vertices'])
            pieces[key] = pc
        # 1. covering by reconstruction of the bisection tree
        root = tuple([tuple(Fr(0) for _ in range(n))] + [tuple(Fr(1) / lam[j] if k == j else Fr(0) for k in range(n)) for j in act])
        stack = [(root, 0)]
        found = set(); bad = False
        while stack:
            pc, depth = stack.pop()
            if pc in pieces:
                found.add(pc)
                continue
            if depth > 60:
                bad = True
                break
            a, b = split(pc)
            stack += [(a, depth + 1), (b, depth + 1)]
        check('block %s: bisection tree reaches exactly the %d listed pieces (covering of Delta)'
              % (blk['sector'], len(pieces)), (not bad) and found == set(pieces))
        # 2./3. piece certificates
        nsdp = nout = 0; good = True
        for key, pc in pieces.items():
            if 'outside' in pc:
                nout += 1
                x = xpts[pc['outside']]
                good &= all(x[j] == 0 for j in range(n) if j not in act)
                good &= all(sum(a[j] * x[j] for j in range(n)) < 1 for a in key)
                continue
            nsdp += 1
            Y = [[[Fr(v) for v in row] for row in Yj] for Yj in pc['Y']]
            for j in range(n):
                if j not in act:
                    good &= all(v == 0 for row in Y[j] for v in row)
                good &= psd(Y[j])
            R = [[Fr(0), Fr(0)], [Fr(0), Fr(0)]]
            for j in range(n):
                NY = mm(N[j], Y[j])
                R = [[R[i][k] - NY[i][k] for k in range(2)] for i in range(2)]
            good &= R[0][1] == R[1][0]
            mats = [Y[j] for j in act]
            for a in key:
                Q = [[R[i][k] - sum(a[j] * Y[j][i][k] for j in range(n)) for k in range(2)] for i in range(2)]
                good &= psd(Q) and Q[0][0] + Q[1][1] > 0
                mats.append(Q)
            if sec is not None:
                for u in sec:
                    for X in mats:
                        good &= u[0] * X[0][0] + u[1] * X[0][1] >= 0
        check('block %s: %d SDP certificates and %d pruned pieces verified' % (blk['sector'], nsdp, nout), good)
    print('ALL PASS' if ok_all else 'SOME CHECK FAILED')
    return 0 if ok_all else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
