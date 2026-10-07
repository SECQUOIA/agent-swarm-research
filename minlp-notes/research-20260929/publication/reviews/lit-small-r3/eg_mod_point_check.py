"""Reviewer check (lit-small, round 3), independent of the author's eg_camino_gurobi.py.

Evaluates the rows of the MINLPLib AMPL .mod files of eg_disc2_s, eg_disc_s, eg_int_s at given
points with rigorous enclosures built from Python integers and fractions only (no mpmath):
  * the .mod text is tokenized and parsed by a small recursive-descent parser (+ - * / ^ exp, unary minus);
  * every decimal constant and every coordinate is the exact rational written in the file;
  * exp(t) is enclosed with a fixed-point Taylor series (2^-P grid, floor/ceil in each step,
    explicit remainder bound), range reduction t = 2^m u with u <= 1/2, outward-rounded squaring;
  * all other operations are exact on Fraction intervals.
Proves, for each point, bounds, integrality and every row (lower end of slack > 0 means proved).
Also: for the old GAMS World eg_int_s point, reports violated rows and the smallest objvar
satisfying rows e1..e24 (they have the form -(f_k(x)) + x8 >= c_k, checked textually).
Usage: python3 eg_mod_point_check.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import re
import sys
from fractions import Fraction as F
from pathlib import Path

P = 320
ONE = 1 << P
NTAYLOR = 70
TRACK = Path((_PUBLIC_REPO + '/research-20260929/publication/literature/small'))
MOD = TRACK / 'sources/eg/minlplib_mod'
SOL = Path((_PUBLIC_REPO + '/research-20260929/open-instances-wave3/eg/retry/sol'))


def floor_div(a, b):
    return a // b


def ceil_div(a, b):
    return -((-a) // b)


def exp_pos_fixed(t, up):
    """t: Fraction >= 0. Returns integer E with E/2^P <= exp(t) (up=False) or >= exp(t) (up=True)."""
    m = 0
    while t > F(1, 2) * (1 << m):
        m += 1
    u = t / (1 << m)  # 0 <= u <= 1/2, exact
    # fixed-point u, rounded in the needed direction
    uf = ceil_div(u.numerator * ONE, u.denominator) if up else floor_div(u.numerator * ONE, u.denominator)
    term = ONE
    s = ONE
    for k in range(1, NTAYLOR + 1):
        if up:
            term = ceil_div(term * uf, k * ONE)
        else:
            term = floor_div(term * uf, k * ONE)
        s += term
    if up:
        # remainder sum_{k>N} u^k/k! <= 2 u^{N+1}/(N+1)! for u <= 1/2; bound with u <= 1/2 crude:
        # term currently >= u^N/N!; next terms <= term*u/(N+1) * 1/(1-u/(N+2)) <= term * 2 / (N+1)
        s += ceil_div(2 * term, NTAYLOR + 1) + 1
    for _ in range(m):
        s = ceil_div(s * s, ONE) if up else floor_div(s * s, ONE)
    return s


def exp_iv(lo, hi):
    """Enclosure of exp over [lo, hi] (Fractions), as Fraction interval."""
    def one(t, up):
        if t >= 0:
            return F(exp_pos_fixed(t, up), ONE)
        # exp(t) = 1/exp(-t)
        e = exp_pos_fixed(-t, not up)
        return F(ONE, e)
    return one(lo, False), one(hi, True)


class Iv:
    __slots__ = ('a', 'b')

    def __init__(self, a, b=None):
        self.a = a
        self.b = a if b is None else b
        assert self.a <= self.b

    def __add__(self, o):
        return Iv(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return Iv(self.a - o.b, self.b - o.a)

    def __neg__(self):
        return Iv(-self.b, -self.a)

    def __mul__(self, o):
        p = [self.a * o.a, self.a * o.b, self.b * o.a, self.b * o.b]
        return Iv(min(p), max(p))

    def __truediv__(self, o):
        assert o.a > 0 or o.b < 0
        return self * Iv(1 / o.b, 1 / o.a)

    def ipow(self, n):
        assert n >= 0
        if n == 0:
            return Iv(F(1))
        if n % 2 == 1 or self.a >= 0:
            if self.a >= 0:
                return Iv(self.a ** n, self.b ** n)
            if n % 2 == 1:
                return Iv(self.a ** n, self.b ** n)
        if self.b <= 0:
            return Iv(self.b ** n, self.a ** n)
        return Iv(F(0), max(self.a ** n, self.b ** n))


TOK = re.compile(r'\s*(?:(\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)|([A-Za-z_]\w*)|(\S))')


def tokenize(s):
    out = []
    pos = 0
    s = s.strip()
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError('tokenize at ' + s[pos:pos + 30])
        num, name, op = m.groups()
        if num is not None:
            out.append(('num', F(num)))
        elif name is not None:
            out.append(('name', name))
        else:
            out.append(('op', op))
        pos = m.end()
    return out


class Parser:
    def __init__(self, toks, env):
        self.t = toks
        self.i = 0
        self.env = env
        self.nexp = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else ('end', None)

    def take(self, kind=None, val=None):
        tok = self.peek()
        if kind and tok[0] != kind or val is not None and tok[1] != val:
            raise ValueError(f'expected {kind} {val}, got {tok} at {self.i}')
        self.i += 1
        return tok

    def expr(self):
        v = self.term()
        while self.peek() in (('op', '+'), ('op', '-')):
            op = self.take()[1]
            w = self.term()
            v = v + w if op == '+' else v - w
        return v

    def term(self):
        v = self.unary()
        while self.peek() in (('op', '*'), ('op', '/')):
            op = self.take()[1]
            w = self.unary()
            v = v * w if op == '*' else v / w
        return v

    def unary(self):
        if self.peek() == ('op', '-'):
            self.take()
            return -self.unary()
        if self.peek() == ('op', '+'):
            self.take()
            return self.unary()
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == ('op', '^'):
            self.take()
            tok = self.take('num')
            n = tok[1]
            assert n.denominator == 1
            return base.ipow(int(n))
        return base

    def atom(self):
        tok = self.peek()
        if tok[0] == 'num':
            self.take()
            return Iv(tok[1])
        if tok[0] == 'name':
            self.take()
            if tok[1] == 'exp':
                self.take('op', '(')
                arg = self.expr()
                self.take('op', ')')
                self.nexp += 1
                lo, hi = exp_iv(arg.a, arg.b)
                return Iv(lo, hi)
            return self.env[tok[1]]
        if tok == ('op', '('):
            self.take()
            v = self.expr()
            self.take('op', ')')
            return v
        raise ValueError(f'bad atom {tok}')


def read_mod(path):
    text = path.read_text()
    vars_ = {}
    for m in re.finditer(r'^var (\w+)(.*?);', text, re.M):
        name, rest = m.group(1), m.group(2)
        integer = ' integer' in rest
        lb = re.search(r'>= (\S+?)(?:,|$)', rest)
        ub = re.search(r'<= (\S+?)(?:,|$)', rest)
        vars_[name] = (integer, F(lb.group(1)) if lb else None, F(ub.group(1)) if ub else None)
    body = text.split('subject to', 1)[1]
    rows = []
    for m in re.finditer(r'^(e\d+):(.*?);', body, re.S | re.M):
        rows.append((m.group(1), ' '.join(m.group(2).split())))
    return vars_, rows


def check_point(vars_, rows, point, label):
    print(f'== {label}')
    env = {}
    ok_b = True
    for name, (integer, lb, ub) in vars_.items():
        v = F(point[name])
        env[name] = Iv(v)
        if integer and v.denominator != 1:
            ok_b = False
            print('   not integral:', name, point[name])
        if lb is not None and v < lb or ub is not None and v > ub:
            ok_b = False
            print('   out of bounds:', name, point[name], lb, ub)
    print(f'   variables {len(vars_)}; all within bounds and integral (exact): {ok_b}')
    slacks = {}
    nexp = 0
    for rname, txt in rows:
        m = re.fullmatch(r'(.*) (>=|<=|=) (-?[\d.eE+-]+)', txt)
        lhs, sense, rhs = m.group(1), m.group(2), F(m.group(3))
        p = Parser(tokenize(lhs), env)
        val = p.expr()
        assert p.i == len(p.t), rname
        nexp += p.nexp
        if sense == '>=':
            slacks[rname] = val - Iv(rhs)
        elif sense == '<=':
            slacks[rname] = Iv(rhs) - val
        else:
            raise ValueError
    width = max(float(s.b - s.a) for s in slacks.values())
    bad = [r for r, s in slacks.items() if not s.a > 0]
    mn = min(slacks.items(), key=lambda kv: kv[1].a)
    print(f'   rows {len(rows)}, exp calls {nexp}, max enclosure width {width:.2e}')
    print(f'   rows not proved: {bad}; smallest slack row {mn[0]}: [{float(mn[1].a):.4e}, {float(mn[1].b):.4e}]')
    return slacks, bad


def main():
    import csv
    cam = TRACK / 'sources/eg/camino_benchmark'
    gur = {r['path'].removesuffix('.mod'): r for r in csv.DictReader(open(cam / 'noncvx_gurobi.csv'))}
    scip = {r['path'].removesuffix('.mod'): r for r in csv.DictReader(open(cam / 'noncvx_scip.csv'))}
    for name in ('eg_disc2_s', 'eg_disc_s', 'eg_int_s'):
        vars_, rows = read_mod(MOD / f'{name}.mod')
        senses = [re.fullmatch(r'.* (>=|<=|=) \S+', t).group(1) for _, t in rows]
        print(f'{name}: {len(vars_)} variables, {len(rows)} rows, senses >= {senses.count(">=")}, <= {senses.count("<=")}, = {senses.count("=")}')
        # rows e1..e24: -( ... ) + x8 >= c ; check textual form and that x8 appears nowhere else
        for rname, t in rows:
            k = int(rname[1:])
            if k <= 24:
                assert re.fullmatch(r'-\(.*\) \+ x8 >= \S+', t) and t.count('x8') == 1, rname
            else:
                assert 'x8' not in t, rname
        pt = {}
        for line in (SOL / f'{name}.retry.sol').read_text().split('\n'):
            if line.strip():
                k, v = line.split()
                pt['x8' if k == 'objvar' else k] = v
        slacks, bad = check_point(vars_, rows, pt, f'{name} recorded point')
        x8 = F(pt['x8'])
        g, s = gur[name], scip[name]
        gb, gobj = F(g['dual_obj']), F(g['obj'])
        print(f'   point objective x8 = {pt["x8"]}')
        print(f'   CAMINO Gurobi: obj {g["obj"]} bestbound {g["dual_obj"]} time {g["calc_time"]}; bound - x8 = {float(gb - x8):.9f} ({float((gb - x8) / x8) * 100:.2f}% of x8)')
        print(f'   CAMINO SCIP: obj {s["obj"]} bestbound {s["dual_obj"]} time {s["calc_time"]}; bound <= x8: {F(s["dual_obj"]) <= x8}')
    # old GAMS World point of eg_int_s
    inc = (TRACK / 'sources/gamsworld/MINLPLib_points_eg_int_s.inc').read_text()
    pt = {('x8' if k == 'objvar' else k): v for k, v in re.findall(r'(\w+)\.[Ll]\s*=\s*([-\d.eE+]+)', inc)}
    vars_, rows = read_mod(MOD / 'eg_int_s.mod')
    slacks, bad = check_point(vars_, rows, pt, 'eg_int_s old GAMS World point')
    for r in bad:
        print(f'   {r}: slack [{float(slacks[r].a):.6e}, {float(slacks[r].b):.6e}]')
    x8 = F(pt['x8'])
    need = max(x8 - slacks[f'e{k}'].a for k in range(1, 25))
    need_lo = max(x8 - slacks[f'e{k}'].b for k in range(1, 25))
    print(f'   smallest objvar satisfying e1..e24 at this x lies in [{float(need_lo):.13f}, {float(need):.13f}]')


if __name__ == '__main__':
    main()
