"""Reviewer's independent exact checks for orbit-closure (review round 1).  Imports no stream code.

1. Lemma 16 (SDP) certificates of family (A): thm14_A, prop16_A, wcorner_A_A.  Instance data typed in
   from note.md.  Coverage of Delta = conv{0, e_j/lam_j} by an order-free reconstruction of the
   longest-edge bisection tree (pieces compared as vertex sets, every longest edge tried on ties)
   plus an exact volume sum.  Per piece: Y_j symmetric PSD, Y_j = 0 if lam_j = 0, R symmetric,
   Q(a) PSD with positive trace at the vertices.
2. Theorem 11(b): the integer certificate printed in the note.
3. Theorem 11(a): identities a_1 >= 7 + 6b/a and a_1 >= -6b/a (sympy), and the rational orbit set
   of logs/thm14_factor.log (p_1 recessive, alpha_2, alpha_3 >= 367/759).
4. Theorem 9(c) lower bound 2539/10000 for (BP): rational S and tau_j of logs/bp_lower.log.
5. Section 6.2: q > 0 on {lam >= 0 : w^T lam <= 649/2500}, w = (11/20, 10^-6, 9/20), by exact face
   enumeration with a Fraction linear solver; and the arithmetic of the factor 1.1166.
6. Arithmetic of Theorem 9 and Proposition 10 bounds.
"""
import json, itertools, sys
from fractions import Fraction as Fr
import sympy as sp

OK = True


def chk(msg, cond):
    global OK
    OK &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def M(s, h=Fr(1)):
    return [[s[2], s[0]], [s[1], h]]


def psd(A):
    return A[0][1] == A[1][0] and A[0][0] >= 0 and A[1][1] >= 0 and A[0][0] * A[1][1] - A[0][1] ** 2 >= 0


def sym(A):
    o = (A[0][1] + A[1][0]) / 2
    return [[A[0][0], o], [o, A[1][1]]]


F = Fr
THM14 = dict(sbar=[F(-9, 2), F(0), F(3, 2)], V=[[F(-1), F(-6), F(18)], [F(-5), F(6), F(-18)], [F(0), F(5, 2), F(5, 2)]])
PROP16 = dict(sbar=[F(-2), F(3), F(2)], V=[[F(0), F(0), F(0)], [F(6), F(-2), F(1, 4)], [F(1), F(-5, 2), F(1, 2)]])
for I in (THM14, PROP16):
    I['P'] = [[v[i] - I['sbar'][i] for i in range(3)] for v in I['V']]
WC = dict(sbar=[F(1), F(-1), F(1)], P=[[F(1), F(0), F(0)], [F(0), F(-1), F(0)], [F(0), F(0), F(1)], [F(0), F(0), F(-1)]])


# ------------------------------------------------------------------ 1. Lemma 16 certificates
def det3(Mx):
    return (Mx[0][0] * (Mx[1][1] * Mx[2][2] - Mx[1][2] * Mx[2][1]) - Mx[0][1] * (Mx[1][0] * Mx[2][2] - Mx[1][2] * Mx[2][0])
            + Mx[0][2] * (Mx[1][0] * Mx[2][1] - Mx[1][1] * Mx[2][0]))


def simplex_vol(vs, act):
    # vs: list of len(act)+1 points; |det| of edge vectors (up to the constant 1/k!)
    k = len(act)
    rows = [[vs[i][a] - vs[0][a] for a in act] for i in range(1, k + 1)]
    if k == 1:
        return abs(rows[0][0])
    if k == 3:
        return abs(det3(rows))
    if k == 2:
        return abs(rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0])
    raise ValueError


def check_lemma16(path, inst, lam):
    d = json.load(open(path))
    sb, P = inst['sbar'], inst['P']
    n = len(P)
    ci = d['instance']
    same = [F(x) for x in ci['sbar']] == sb and [F(x) for x in ci['lam']] == lam
    if 'verts' in ci:
        same &= [[F(v[i]) - sb[i] for i in range(3)] for v in ci['verts']] == P
    else:
        same &= [[F(x) for x in p] for p in ci['rays']] == P
    chk('%s: certificate instance equals the note\'s corner and point' % path, same and d['family'] == 'A')
    act = [j for j in range(n) if lam[j] > 0]
    Mi = inv(M(sb))
    N = [mul(Mi, M(p, F(0))) for p in P]
    assert len(d['blocks']) == 1 and d['blocks'][0]['sector'] is None
    pieces = d['blocks'][0]['pieces']
    keys = {}
    for pc in pieces:
        vs = tuple(tuple(F(x) for x in v) for v in pc['vertices'])
        keys[frozenset(vs)] = pc
    root = frozenset([tuple(F(0) for _ in range(n))] + [tuple(1 / lam[j] if k == j else F(0) for k in range(n)) for j in act])
    memo = {}

    def resolve(node, depth):
        """set of pieces covering node via longest-edge bisection, or None"""
        if node in keys:
            return {node}
        if depth > 60:
            return None
        if node in memo:
            return memo[node]
        vs = list(node)
        best, edges = None, []
        for a, b in itertools.combinations(range(len(vs)), 2):
            L = sum((vs[a][m] - vs[b][m]) ** 2 for m in act)
            if best is None or L > best:
                best, edges = L, [(a, b)]
            elif L == best:
                edges.append((a, b))
        res = None
        for a, b in edges:
            mid = tuple((vs[a][m] + vs[b][m]) / 2 for m in range(n))
            c1 = frozenset(mid if i == a else v for i, v in enumerate(vs))
            c2 = frozenset(mid if i == b else v for i, v in enumerate(vs))
            r1 = resolve(c1, depth + 1)
            r2 = resolve(c2, depth + 1) if r1 is not None else None
            if r1 is not None and r2 is not None:
                res = r1 | r2
                break
        memo[node] = res
        return res

    used = resolve(root, 0)
    vol = sum(simplex_vol(list(k), act) for k in keys)
    chk('%s: bisection cover of Delta uses all %d pieces; volumes add up (%s vs %s)'
        % (path, len(keys), vol, simplex_vol(list(root), act)),
        used is not None and used == set(keys) and vol == simplex_vol(list(root), act))
    good = True
    for k, pc in keys.items():
        assert 'outside' not in pc
        Y = [[[F(x) for x in r] for r in Yj] for Yj in pc['Y']]
        for j in range(n):
            good &= psd(Y[j])
            if j not in act:
                good &= all(x == 0 for r in Y[j] for x in r)
        S = [[F(0)] * 2 for _ in range(2)]
        for j in range(n):
            T = mul(M(P[j], F(0)), Y[j])
            S = [[S[r][c] + T[r][c] for c in range(2)] for r in range(2)]
        R = mul(Mi, S)
        R = [[-x for x in r] for r in R]
        good &= R[0][1] == R[1][0]
        for a in k:
            Q = [[R[r][c] - sum(a[j] * Y[j][r][c] for j in range(n)) for c in range(2)] for r in range(2)]
            good &= psd(Q) and Q[0][0] + Q[1][1] > 0
    chk('%s: Lemma 16 conditions hold on every piece' % path, good)


check_lemma16('../logs/closure_cert_thm14_A.json', THM14, [F(3, 11), F(41, 99), F(10, 33)])
check_lemma16('../logs/closure_cert_prop16_A.json', PROP16, [F(24, 25), F(1, 100), F(29, 1000)])
check_lemma16('../logs/closure_cert_wcorner_A_A.json', WC, [F(20), F(20), F(20), F(0)])

# ------------------------------------------------------------------ 2. Theorem 11(b) integer certificate
Y = [[[F(141), F(-63)], [F(-63), F(29)]], [[F(4), F(67)], [F(67), F(1322)]], [[F(31), F(-132)], [F(-132), F(565)]],
     [[F(0)] * 2, [F(0)] * 2]]
Mi = inv(M(WC['sbar']))
S_ = [[F(0)] * 2 for _ in range(2)]
for j in range(4):
    T = mul(M(WC['P'][j], F(0)), Y[j])
    S_ = [[S_[r][c] + T[r][c] for c in range(2)] for r in range(2)]
R = [[-x for x in r] for r in mul(Mi, S_)]
chk('Thm 11(b): R = %s equals [[14, 18], [18, 85]]' % R, R == [[14, 18], [18, 85]])
chk('Thm 11(b): Y_1..Y_3 PSD', all(psd(Y[j]) for j in range(3)))
verts = [[F(0)] * 4] + [[F(1, 20) if k == j else F(0) for k in range(4)] for j in range(3)]
chk('Thm 11(b): Q(a) PSD, trace > 0 at the vertices of {20(a1+a2+a3) <= 1}',
    all(psd(Q) and Q[0][0] + Q[1][1] > 0 for Q in
        [[[R[r][c] - sum(a[j] * Y[j][r][c] for j in range(4)) for c in range(2)] for r in range(2)] for a in verts]))

# ------------------------------------------------------------------ 3. Theorem 11(a)
a, b, c = sp.symbols('a b c', real=True)
Ss = sp.Matrix([[a, b], [b, c]])
sb = THM14['sbar']; P = THM14['P']
Ms = sp.Matrix([[sp.Rational(str(x)) for x in r] for r in M(sb)])
FT = Ss * Ms.inv()
E = sp.Matrix([[1, 0], [0, 0]])
M0 = [sp.Matrix([[sp.Rational(str(x)) for x in r] for r in M(p, F(0))]) for p in P]
e1 = sp.Matrix([1, 0])
chk('Thm 11(a): e_1 kept: e1^T F^T E e1 = 2a/3', sp.simplify((e1.T * FT * E * e1)[0] - 2 * a / 3) == 0)
chk('Thm 11(a): -e1^T F^T M0(p1) e1 = 7a + 6b and e1^T F^T M(sbar) e1 = a',
    sp.expand(-(e1.T * FT * M0[0] * e1)[0] - 7 * a - 6 * b) == 0 and sp.expand((e1.T * FT * Ms * e1)[0] - a) == 0)
J = sp.Matrix([[0, 1], [-1, 0]])
m = Ms.inv() * e1
u = J * Ss * m
chk('Thm 11(a): u = JSm kept, -u^T F^T M0(p1) u = det(S)(-8b/3), u^T S u = det(S) 4a/9',
    sp.expand((u.T * FT * E * u)[0]) == 0 and sp.expand(-(u.T * FT * M0[0] * u)[0] - (a * c - b ** 2) * (-8 * b / 3)) == 0
    and sp.expand((u.T * Ss * u)[0] - (a * c - b ** 2) * 4 * a / 9) == 0)
rho = sp.symbols('rho', real=True)
chk('Thm 11(a): max(7 + 6 rho, -6 rho) >= 7/2 (crossing at rho = -7/12, value 7/2)',
    sp.solve(sp.Eq(7 + 6 * rho, -6 * rho), rho) == [sp.Rational(-7, 12)] and 7 + 6 * sp.Rational(-7, 12) == sp.Rational(7, 2))
X = [[F(658069, 904895), F(-152131921313, 178878074790)], [F(2319980473, 178878074790), F(246826, 904895)]]
Msb = M(sb)
FTx = mul(X, inv(Msb))
A0 = sym(X)
Aj = [sym(mul(FTx, M(p, F(0)))) for p in P]
z0 = F(367, 759)
chk('Thm 11(a): log orbit set: sym(X) > 0, det X > 0',
    A0[0][0] > 0 and A0[0][0] * A0[1][1] - A0[0][1] ** 2 > 0 and X[0][0] * X[1][1] - X[0][1] * X[1][0] > 0)
chk('Thm 11(a): sym(F^T M0(p1)) PSD (p1 recessive)', psd(Aj[0]))
chk('Thm 11(a): sym(F^T M(sbar + z0 p_j)) PSD for j = 2, 3',
    all(psd([[A0[r][cc] + z0 * Aj[j][r][cc] for cc in range(2)] for r in range(2)]) for j in (1, 2)))

# ------------------------------------------------------------------ 4. BP lower bound 2539/10000
S = [[F(1), F(-392, 621)], [F(-392, 621), F(47753, 99290)]]
FTs = mul(S, inv(Msb))
Z = sym(mul(FTs, [[F(1), F(0)], [F(0), F(0)]]))
mu = F(2539, 10000)
taus = [F(0), F(0), F(227, 64)]
good = S[0][0] > 0 and S[0][0] * S[1][1] - S[0][1] ** 2 > 0
for j in range(3):
    A = sym(mul(FTs, M([sb[i] + mu * P[j][i] for i in range(3)])))
    good &= taus[j] >= 0 and psd([[A[r][cc] - taus[j] * Z[r][cc] for cc in range(2)] for r in range(2)])
chk('Thm 9(c): BP set S of bp_lower.log has sbar + (2539/10000) p_j - tau_j e_w in C_F for all j', good)


# ------------------------------------------------------------------ 5. z_K lower bound of Section 6.2
def solve(A, bvec):
    n = len(A)
    Mx = [list(A[i]) + [bvec[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if Mx[r][col] != 0), None)
        if piv is None:
            return None
        Mx[col], Mx[piv] = Mx[piv], Mx[col]
        for r in range(n):
            if r != col and Mx[r][col] != 0:
                f = Mx[r][col] / Mx[col][col]
                Mx[r] = [x - f * y for x, y in zip(Mx[r], Mx[col])]
    return [Mx[i][n] / Mx[i][i] for i in range(n)]


w = [F(11, 20), F(1, 10 ** 6), F(9, 20)]
z0 = F(649, 2500)
V4 = [list(sb)] + [[sb[i] + z0 / w[j] * P[j][i] for i in range(3)] for j in range(3)]


def qv(s):
    return s[2] - s[0] * s[1]


best = None
for k in range(1, 5):
    for face in itertools.combinations(range(4), k):
        pts = [V4[i] for i in face]
        # q(sum t_i p_i) = sum_i t_i p_i,w - (sum t_i p_i,x)(sum t_i p_i,y); gradient_i = p_i,w - p_i,x Y - p_i,y X
        # stationarity on {sum t = 1}: grad_i - mu = 0; unknowns t (k), mu
        A = []
        rhs = []
        for i in range(k):
            row = [-(pts[i][0] * pts[l][1] + pts[i][1] * pts[l][0]) for l in range(k)] + [F(-1)]
            A.append(row); rhs.append(-pts[i][2])
        A.append([F(1)] * k + [F(0)]); rhs.append(F(1))
        sol = solve(A, rhs)
        if sol is None:
            continue          # singular: stationary set empty or affine; its values are attained on subfaces
        t = sol[:k]
        if all(x >= 0 for x in t):
            s = [sum(t[i] * pts[i][cc] for i in range(k)) for cc in range(3)]
            val = qv(s)
            best = val if best is None or val < best else best
chk('Sec 6.2: min q over T_{649/2500} = %s > 0 (stream: 6480592821/4840070400112)' % best,
    best > 0 and best == F(6480592821, 4840070400112))
lamw = [F(2211, 10000), F(8805, 10000), F(2464, 10000)]
zcl = sum(x * y for x, y in zip(w, lamw))
chk('Sec 6.2: w^T lam = %s = %.7f, ratio z0/that = %.5f >= 1.1166' % (zcl, float(zcl), float(z0 / zcl)), z0 / zcl >= F(11166, 10000))

# ------------------------------------------------------------------ 6. arithmetic
chk('Thm 9: sums 49/50, 98/99, 136/525, 11/30',
    sum([F(67, 250), F(41, 100), F(151, 500)]) == F(49, 50) and sum([F(3, 11), F(41, 99), F(10, 33)]) == F(98, 99)
    and F(51, 350) + F(17, 150) == F(136, 525) and F(1, 5) + F(1, 6) == F(11, 30))
chk('Prop 10: (24/25, 1/100, 29/1000) sums to 999/1000', F(24, 25) + F(1, 100) + F(29, 1000) == F(999, 1000))
print('ALL PASS' if OK else 'SOME CHECK FAILED')
sys.exit(0 if OK else 1)
