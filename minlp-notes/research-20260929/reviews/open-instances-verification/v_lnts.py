"""Independent verification of the lnts dual bounds and primal points.

1. Parse the OSIL (own reader) and check every row and bound against the
   expected trapezoidal model exactly (string equality of constants).
2. Exact rationals w_j, c_j; identities vx_N, vy_N, py_N checked in exact
   rational arithmetic for random rational 'sin/cos' values.
3. Multipliers (mu, nu, h*) by Newton in 60 digits; certificate
   S(mu,nu) - nu*B(h2) < A(h2) checked with mpmath interval arithmetic.
4. Primal: tangent-law controls rounded to double, states by forward
   recursion, all rows/bounds evaluated in 60-digit arithmetic; also the
   authors' primal vector and MINLPLib p1 are evaluated.
"""
import os
import sys, json, random
from fractions import Fraction as Fr
import mpmath
from mpmath import mp, iv, mpf
import osilx

P = os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
AUTH = _REPO + '/research-20260929/open-instances/'


def layout(N):
    th = list(range(0, N + 1))
    px = list(range(N + 1, 2 * N + 2))
    py = list(range(2 * N + 2, 3 * N + 3))
    vx = list(range(3 * N + 3, 4 * N + 4))
    vy = list(range(4 * N + 4, 5 * N + 5))
    h = 5 * N + 5
    return th, px, py, vx, vy, h


def check_structure(I, N):
    th, px, py, vx, vy, h = layout(N)
    n = len(I['names'])
    assert n == 5 * N + 6, n
    assert len(I['cons']) == 4 * N
    o = I['obj']
    assert o['sense'] == 'min' and o['lin'] == {h: str(N)} and not o['quad'] and o['nl'] is None
    assert o['constant'] == '0' and o['weight'] == '1'
    TB = ('-1.5707963267949', '1.5707963267949')
    fixed = {px[0]: '0', py[0]: '0', py[N]: '5', vx[0]: '0', vx[N]: '45', vy[0]: '0', vy[N]: '0'}
    for j in range(n):
        b = (I['lb'][j], I['ub'][j])
        assert I['vt'][j] == 'C'
        if j in th:
            assert b == TB, (j, b)
        elif j == h:
            assert b == ('0', 'INF'), b
        elif j in fixed:
            assert b == (fixed[j], fixed[j]), (j, b)
        else:
            assert b == ('-INF', 'INF'), (j, b)
    for r, c in enumerate(I['cons']):
        assert c['lb'] == '0' and c['ub'] == '0' and c['constant'] == '0'
        k, i = divmod(r, N)
        if k in (0, 1):
            p, v = (px, vx) if k == 0 else (py, vy)
            assert c['lin'] == {p[i]: '-1', p[i + 1]: '1'}, (r, c['lin'])
            assert sorted(c['quad']) == sorted([(v[i], h, '-.5'), (v[i + 1], h, '-.5')]), (r, c['quad'])
            assert c['nl'] is None
        else:
            v, fn = (vx, 'cos') if k == 2 else (vy, 'sin')
            assert c['lin'] == {v[i]: '-1', v[i + 1]: '1'} and not c['quad']
            exp = ('product', ('sum', ('product', (fn, ('var', th[i], '1')), ('num', '100')),
                               ('product', (fn, ('var', th[i + 1], '1')), ('num', '100'))),
                   ('num', '-.5'), ('var', h, '1'))
            assert c['nl'] == exp, (r, c['nl'])
    return th, px, py, vx, vy, h


def weights(N):
    w = [Fr(1, 2)] + [Fr(1)] * (N - 1) + [Fr(1, 2)]
    # vy_k = a h sum_j W_kj s_j with W_kj = ([j<=k-1] + [1<=j<=k])/2
    c = [Fr(0)] * (N + 1)
    for k in range(N + 1):
        for j in range(N + 1):
            W = (Fr(1 if j <= k - 1 else 0) + Fr(1 if 1 <= j <= k else 0)) / 2
            c[j] += w[k] * W
    return w, c


def identity_check(N, w, c):
    # exact rational simulation of the recursions with arbitrary rational s_j, k_j
    rnd = random.Random(1)
    a, h = Fr(100), Fr(rnd.randint(1, 999), 1000)
    s = [Fr(rnd.randint(-999, 999), 1000) for _ in range(N + 1)]
    k = [Fr(rnd.randint(-999, 999), 1000) for _ in range(N + 1)]
    vx, vy, py = [Fr(0)], [Fr(0)], [Fr(0)]
    for i in range(N):
        vx.append(vx[i] + h / 2 * (a * k[i] + a * k[i + 1]))
        vy.append(vy[i] + h / 2 * (a * s[i] + a * s[i + 1]))
        py.append(py[i] + h / 2 * (vy[i] + vy[i + 1]))
    assert vx[N] == a * h * sum(wj * kj for wj, kj in zip(w, k))
    assert vy[N] == a * h * sum(wj * sj for wj, sj in zip(w, s))
    assert py[N] == a * h * h * sum(cj * sj for cj, sj in zip(c, s))


def solve_primal_system(N, w, c, guess):
    mp.dps = 60
    wm = [mpf(x.numerator) / x.denominator for x in w]
    cm = [mpf(x.numerator) / x.denominator for x in c]

    def F(mu, nu, h):
        s1 = s2 = s3 = mpf(0)
        for wj, cj in zip(wm, cm):
            t = mu + nu * cj / wj
            r = mpmath.sqrt(1 + t * t)
            s1 += wj / r
            s2 += wj * t / r
            s3 += cj * t / r
        return [s1 - mpf(45) / (100 * h), s2, s3 - mpf(5) / (100 * h * h)]
    sol = mpmath.findroot(F, guess, tol=mpf(10) ** -50)
    return [sol[0], sol[1], sol[2]]


def certificate(N, w, c, mu, nu, h2):
    """sup of S(mu,nu) - nu B(h2) - A(h2) in interval arithmetic."""
    iv.dps = 50
    S = iv.mpf(0)
    MU, NU, H = iv.mpf(mu), iv.mpf(nu), iv.mpf(h2)
    for wj, cj in zip(w, c):
        W = iv.mpf(wj.numerator) / wj.denominator
        Cc = iv.mpf(cj.numerator) / cj.denominator
        b = MU * W + NU * Cc
        S += iv.sqrt(W * W + b * b)
    A = iv.mpf(45) / (iv.mpf(100) * H)
    B = iv.mpf(5) / (iv.mpf(100) * H * H)
    val = S - NU * B - A
    return val


def build_point(N, lay, mu, nu, h, w, c):
    """tangent-law controls rounded to double, states by forward recursion (in doubles
    of the 60-digit exact recursion), h rounded to double."""
    th, px, py, vx, vy, hi = lay
    mp.dps = 60
    x = [mpf(0)] * (5 * N + 6)
    hd = float(h)
    for j in range(N + 1):
        t = mu + nu * (mpf(c[j].numerator) / c[j].denominator) / (mpf(w[j].numerator) / w[j].denominator)
        x[th[j]] = mpf(float(mpmath.atan(t)))
    x[hi] = mpf(hd)
    H = x[hi]
    X = {k: [mpf(0)] for k in 'xyuv'}
    for i in range(N):
        X['u'].append(X['u'][i] + H / 2 * (100 * mpmath.cos(x[th[i]]) + 100 * mpmath.cos(x[th[i + 1]])))
        X['v'].append(X['v'][i] + H / 2 * (100 * mpmath.sin(x[th[i]]) + 100 * mpmath.sin(x[th[i + 1]])))
        X['x'].append(X['x'][i] + H / 2 * (X['u'][i] + X['u'][i + 1]))
        X['y'].append(X['y'][i] + H / 2 * (X['v'][i] + X['v'][i + 1]))
    for i in range(N + 1):
        x[px[i]] = mpf(float(X['x'][i]))
        x[py[i]] = mpf(float(X['y'][i]))
        x[vx[i]] = mpf(float(X['u'][i]))
        x[vy[i]] = mpf(float(X['v'][i]))
    # fixed variables take their fixed values
    x[py[N]] = mpf(5); x[vx[N]] = mpf(45); x[vy[N]] = mpf(0)
    return x


def evaluate(I, x):
    mp.dps = 60
    num = lambda s: mpf(s)
    fns = {'cos': mpmath.cos, 'sin': mpmath.sin}
    rv = mpf(0)
    for c in I['cons']:
        v = osilx.ev_row(c, x, num, fns)
        lo = -mpmath.inf if osilx.isinf(c['lb']) else mpf(c['lb'])
        hi = mpmath.inf if osilx.isinf(c['ub']) else mpf(c['ub'])
        rv = max(rv, lo - v, v - hi)
    bv = mpf(0)
    for j in range(len(x)):
        lo = -mpmath.inf if osilx.isinf(I['lb'][j]) else mpf(I['lb'][j])
        hi = mpmath.inf if osilx.isinf(I['ub'][j]) else mpf(I['ub'][j])
        bv = max(bv, lo - x[j], x[j] - hi)
    obj = osilx.ev_row(dict(I['obj'], constant=I['obj']['constant']), x, num, fns)
    return obj, rv, bv


def read_sol(I, path):
    idx = {nm: j for j, nm in enumerate(I['names'])}
    x = [mpf(0)] * len(I['names'])
    seen = set()
    for line in open(path):
        nm, val = line.split()
        if nm == 'objvar':
            continue
        x[idx[nm]] = mpf(val); seen.add(nm)
    return x, len(I['names']) - len(seen)


def main(N):
    name = f'lnts{N}'
    I = osilx.read(P + name + '.osil')
    lay = check_structure(I, N)
    w, c = weights(N)
    identity_check(N, w, c)
    mu, nu, h = solve_primal_system(N, w, c, [mpf(-1.41), mpf(0.0564), mpf('0.5546') / N])
    out = dict(name=name, mu=float(mu), nu=float(nu), h_star=mpmath.nstr(h, 25),
               N_h_star=mpmath.nstr(N * h, 25))
    assert nu > 0
    for rel in ['1e-10', '1e-12']:
        mp.dps = 60
        h2 = h * (1 - mpf(rel))
        val = certificate(N, w, c, mu, nu, h2)
        out['cert_' + rel] = dict(h2=mpmath.nstr(h2, 20), sup_margin=mpmath.nstr(val.b, 5),
                                  ok=bool(val.b < 0), bound=mpmath.nstr(N * h2, 16))
    x = build_point(N, lay, mu, nu, h, w, c)
    o, rv, bv = evaluate(I, x)
    out['own_primal'] = dict(obj=mpmath.nstr(o, 16), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3))
    # authors' primal vector
    xa = [mpf(line.strip()) for line in open(AUTH + f'logs/lnts_{name}_primal.txt')]
    o, rv, bv = evaluate(I, xa)
    out['authors_primal'] = dict(obj=mpmath.nstr(o, 16), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3))
    try:
        xs, miss = read_sol(I, AUTH + f'minlplib_sol/{name}.p1.sol')
        o, rv, bv = evaluate(I, xs)
        out['minlplib_p1'] = dict(obj=mpmath.nstr(o, 16), rowviol=mpmath.nstr(rv, 3), bndviol=mpmath.nstr(bv, 3), missing=miss)
    except FileNotFoundError:
        pass
    print(json.dumps(out, indent=1))
    return out


if __name__ == '__main__':
    res = [main(int(a)) for a in sys.argv[1:]]
    json.dump(res, open('logs/lnts_verify.json', 'w'), indent=1)
