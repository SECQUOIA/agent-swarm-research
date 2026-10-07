"""Independent verification of the ann_cumene_tanh claims (verifier's own code).

Parsing uses only the review reader osilx.py (decimal strings).  Decoding,
evaluation, interval enclosures and sampling are written here; nothing is
imported from open-instances-wave3/.

    python3 annv.py structure        # task 1: decode, identities, relaxation R
    python3 annv.py points           # task 3: p1 and wave3 points at 50 digits
    python3 annv.py boxes            # task 2: interval bounds + sampling on boxes
"""
import json
import os
import sys
import time
from fractions import Fraction as Fr

import mpmath
import numpy as np
from mpmath import iv, mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "open-instances-verification"))
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/ann_cumene_tanh.osil")
SOL = os.path.join(HERE, "..", "..", "..", "open-instances-wave3", "sol")
INPUT_NAMES = ["x723", "x724", "x725", "x726", "x727"]
# multipliers printed in the authors' log (any nonnegative values give a valid bound)
LAG = [("x647", "58.509053436320386", "-1"), ("x772", "20891.433722402617", ".999")]


def tvars(t):
    if t is None or t[0] == "num":
        return set()
    if t[0] == "var":
        return {t[1]}
    return set().union(*[tvars(s) for s in t[1:]])


def row_vars(c):
    return set(c["lin"]) | tvars(c["nl"]) | {a for a, _, _ in c["quad"]} | {b for _, b, _ in c["quad"]}


# ----------------------------------------------------------------------------- task 1
def decode(verbose=False):
    I = osilx.read(OSIL)
    N, cons = I["names"], I["cons"]
    idx = {n: j for j, n in enumerate(N)}
    out = []
    say = out.append
    assert I["obj"]["sense"] == "min" and I["obj"]["constant"] == "0"
    assert I["obj"]["lin"] == {idx["objvar"]: "1"} and not I["obj"]["quad"] and I["obj"]["nl"] is None
    assert all(c["constant"] == "0" for c in cons)
    assert all(t == "C" for t in I["vt"])
    eq = [k for k, c in enumerate(cons) if not osilx.isinf(c["lb"]) and not osilx.isinf(c["ub"]) and Fr(c["lb"]) == Fr(c["ub"])]
    ineq = [k for k in range(len(cons)) if k not in eq]
    say(f"rows {len(cons)}: equalities {len(eq)}, others {[cons[k]['name'] + ' ' + cons[k]['lb'] + '..' + cons[k]['ub'] for k in ineq]}")
    inputs = [idx[n] for n in INPUT_NAMES]
    known = set(inputs)
    ops, used = [], {}
    changed = True
    while changed:
        changed = False
        for k in eq:
            if k in used:
                continue
            c = cons[k]
            unk = row_vars(c) - known
            if len(unk) != 1:
                continue
            v = next(iter(unk))
            if v not in c["lin"] or v in tvars(c["nl"]) or any(v in (a, b) for a, b, _ in c["quad"]):
                continue
            cv = Fr(c["lin"][v])
            assert cv != 0
            if c["nl"] is None:
                assert not c["quad"]
                ops.append(("lin", v, cv, [(o, Fr(a)) for o, a in c["lin"].items() if o != v], Fr(c["lb"])))
            else:
                t = c["nl"]
                # row:  cv*v + (-(tanh(u))) = lb
                assert t[0] == "negate" and t[1][0] == "tanh" and len(t[1]) == 2 and t[1][1][0] == "var" and t[1][1][2] == "1", t
                assert set(c["lin"]) == {v} and cv == 1 and Fr(c["lb"]) == 0 and not c["quad"]
                ops.append(("tanh", v, t[1][1][1]))
            known.add(v)
            used[k] = v
            changed = True
    # rows that ended with no unknown but were not used would be extra constraints on R
    rest = [k for k in eq if k not in used]
    und = [j for j in range(len(N)) if j not in known]
    say(f"forward-determined {len(known) - len(inputs)} of {len(N)} (+{len(inputs)} inputs); "
        f"ops: {sum(o[0] == 'lin' for o in ops)} linear, {sum(o[0] == 'tanh' for o in ops)} tanh")
    say(f"undetermined: {[N[j] for j in und]}")
    say(f"unused equality rows: {[cons[k]['name'] for k in rest]}")
    for k in rest:
        say(f"   {cons[k]['name']}: unknowns {[N[j] for j in sorted(row_vars(cons[k]) - known)]}")
    # where the undetermined variables occur, and their bounds
    for j in und:
        rows = [cons[k]["name"] for k in range(len(cons)) if j in row_vars(cons[k])]
        say(f"   {N[j]} [{I['lb'][j]}, {I['ub'][j]}] occurs in {rows}")
    # inequality rows must involve determined variables only
    for k in ineq:
        assert row_vars(cons[k]) <= known, cons[k]["name"]
    # ---- objective as a function of determined variables
    byname = {c["name"]: c for c in cons}
    undset = set(und)
    prodrule = {}   # frozenset pair -> list of (p, r, coef) of determined vars
    for k in rest:
        c = cons[k]
        if c["lin"] or c["nl"] is not None:
            continue
        uq = [(a, b, Fr(cc)) for a, b, cc in c["quad"] if a in undset or b in undset]
        if len(uq) != 1:
            continue
        a, b, cc = uq[0]
        others = [(p, r, Fr(c2)) for p, r, c2 in c["quad"] if (p, r, Fr(c2)) != (a, b, cc)]
        assert all(p in known and r in known for p, r, _ in others) and Fr(c["lb"]) == 0
        prodrule[frozenset((a, b))] = [(p, r, -c2 / cc) for p, r, c2 in others]   # x_a x_b = sum
        say(f"   {c['name']}: {N[a]}*{N[b]} = " + " + ".join(f"({float(q):g})*{N[p]}*{N[r]}" for p, r, q in prodrule[frozenset((a, b))]))
    e788 = byname["e788"]
    assert e788["lin"] == {idx["x792"]: "1", idx["x793"]: "1"} and Fr(e788["lb"]) == 1 and not e788["quad"] and e788["nl"] is None
    e790 = byname["e790"]
    ob = idx["objvar"]
    assert Fr(e790["lin"][ob]) == -1 and e790["nl"] is None
    lin = {}
    bil = {}
    const = -Fr(e790["lb"])

    def addlin(j, a):
        lin[j] = lin.get(j, 0) + a

    def addbil(p, r, a):
        key = (min(p, r), max(p, r))
        bil[key] = bil.get(key, 0) + a
    for j, a in e790["lin"].items():
        if j != ob:
            assert j in known
            addlin(j, Fr(a))
    for a, b, cc in e790["quad"]:
        cc = Fr(cc)
        key = frozenset((a, b))
        if key in prodrule:
            for p, r, q in prodrule[key]:
                addbil(p, r, cc * q)
        elif key == frozenset((idx["x766"], idx["x793"])):
            # x766*x793 = x766*(1 - x792) = x766 - x766*x792  (e788 times x766)
            addlin(idx["x766"], cc)
            for p, r, q in prodrule[frozenset((idx["x766"], idx["x792"]))]:
                addbil(p, r, -cc * q)
        else:
            assert a in known and b in known, (N[a], N[b])
            addbil(a, b, cc)
    say(f"objective: const {float(const)!r}, {len(lin)} linear terms, {len(bil)} bilinear terms of determined vars")
    say("   f = %s + %s + %s" % (float(const), " + ".join(f"{float(a):g}*{N[j]}" for j, a in sorted(lin.items())),
                                 " + ".join(f"{float(a):g}*{N[p]}*{N[r]}" for (p, r), a in sorted(bil.items()))))
    # ---- constraints of R
    tanh_out = {o[1] for o in ops if o[0] == "tanh"}
    cb = []
    for j in sorted(known):
        if j in inputs:
            continue
        lo, hi = I["lb"][j], I["ub"][j]
        if not osilx.isinf(lo) or not osilx.isinf(hi):
            cb.append((j, None if osilx.isinf(lo) else Fr(lo), None if osilx.isinf(hi) else Fr(hi)))
    from collections import Counter
    kinds = Counter()
    for j, lo, hi in cb:
        kinds[("tanh-out" if j in tanh_out else "other", str(lo), str(hi))] += 1
    say(f"finite bounds of determined vars kept in R: {len(cb)}: {dict(kinds)}")
    for k in ineq:
        c = cons[k]
        assert set(c["lin"]) == {idx["x772"]} and Fr(c["lin"][idx["x772"]]) == -1 and osilx.isinf(c["lb"]) and not c["quad"] and c["nl"] is None
        cb.append((idx["x772"], -Fr(c["ub"]), None))   # -x772 <= ub  <=>  x772 >= -ub
    box = [(Fr(I["lb"][j]), Fr(I["ub"][j])) for j in inputs]
    say(f"input box: {[(N[j], I['lb'][j], I['ub'][j]) for j in inputs]}")
    if verbose:
        print("\n".join(out))
    return dict(I=I, N=N, idx=idx, inputs=inputs, ops=ops, const=const, lin=lin, bil=bil, cb=cb, box=box,
                used=used, rest=[cons[k]["name"] for k in rest], und=[N[j] for j in und], log=out, prodrule=prodrule)


# ----------------------------------------------------------------------------- evaluation
def forward_mp(D, u):
    """determined variables at inputs u (mp numbers, current mp.dps)."""
    x = {}
    for i, j in enumerate(D["inputs"]):
        x[j] = mp.mpf(u[i])
    q = lambda F: mp.mpf(F.numerator) / F.denominator
    for op in D["ops"]:
        if op[0] == "lin":
            _, v, cv, terms, rhs = op
            s = q(rhs)
            for o, a in terms:
                s -= q(a) * x[o]
            x[v] = s / q(cv)
        else:
            x[op[1]] = mp.tanh(x[op[2]])
    return x


def fobj(D, x, num):
    f = num(D["const"])
    for j, a in D["lin"].items():
        f = f + num(a) * x[j]
    for (p, r), a in D["bil"].items():
        f = f + num(a) * x[p] * x[r]
    return f


def ev_osil_point(I, x, dps=50):
    """objective, max row violation, max bound violation of a full OSIL point (x: list of decimal strings)."""
    with mp.workdps(dps):
        X = [mp.mpf(v) for v in x]
        fns = {"tanh": mp.tanh}
        rv, worst = mp.mpf(0), None
        for c in I["cons"]:
            val = osilx.ev_row(c, X, mp.mpf, fns)
            v = mp.mpf(0)
            if not osilx.isinf(c["lb"]):
                v = max(v, mp.mpf(c["lb"]) - val)
            if not osilx.isinf(c["ub"]):
                v = max(v, val - mp.mpf(c["ub"]))
            if v > rv:
                rv, worst = v, c["name"]
        bv, wb = mp.mpf(0), None
        for j in range(len(X)):
            v = mp.mpf(0)
            if not osilx.isinf(I["lb"][j]):
                v = max(v, mp.mpf(I["lb"][j]) - X[j])
            if not osilx.isinf(I["ub"][j]):
                v = max(v, X[j] - mp.mpf(I["ub"][j]))
            if v > bv:
                bv, wb = v, I["names"][j]
        o = I["obj"]
        obj = mp.mpf(o["constant"]) + sum(mp.mpf(a) * X[j] for j, a in o["lin"].items())
        return obj, rv, worst, bv, wb


def read_sol(path):
    d = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2:
            d[p[0]] = p[1]
    return d


# ----------------------------------------------------------------------------- intervals (mpmath iv)
iv.prec = 80


def ivq(F):
    return iv.mpf(F.numerator) / iv.mpf(F.denominator)


def iv_tanh_pt(z):
    """rigorous enclosure of tanh at an mpf point z via iv.exp."""
    Z = iv.mpf(z)
    if z >= 0:
        return 1 - 2 / (iv.exp(2 * Z) + 1)
    return 2 / (iv.exp(-2 * Z) + 1) - 1


def iv_tanh(X):
    lo = iv_tanh_pt(X.a).a
    hi = iv_tanh_pt(X.b).b
    lo = max(lo, mpmath.mpf(-1))
    hi = min(hi, mpmath.mpf(1))
    return iv.mpf([lo, hi])


def iv_sq(X):
    a, b = X.a, X.b
    if a >= 0:
        return iv.mpf([(iv.mpf(a) * a).a, (iv.mpf(b) * b).b])
    if b <= 0:
        return iv.mpf([(iv.mpf(b) * b).a, (iv.mpf(a) * a).b])
    m = max(-a, b)
    return iv.mpf([0, (iv.mpf(m) * m).b])


def meet(X, lo, hi):
    a, b = X.a, X.b
    if lo is not None:
        a = max(a, ivq(lo).a)
    if hi is not None:
        b = min(b, ivq(hi).b)
    if a > b:
        return None
    return iv.mpf([a, b])


class IvModel:
    def __init__(self, D):
        self.D = D
        self.ops = []
        for op in D["ops"]:
            if op[0] == "lin":
                _, v, cv, terms, rhs = op
                self.ops.append(("lin", v, [(o, ivq(-a / cv)) for o, a in terms], ivq(rhs / cv)))
            else:
                self.ops.append(op)
        self.cb = {}
        for j, lo, hi in D["cb"]:
            plo, phi = self.cb.get(j, (None, None))
            if lo is not None:
                plo = lo if plo is None else max(plo, lo)
            if hi is not None:
                phi = hi if phi is None else min(phi, hi)
            self.cb[j] = (plo, phi)
        self.lin = [(j, ivq(a)) for j, a in D["lin"].items()]
        self.bil = [(p, r, ivq(a)) for (p, r), a in D["bil"].items()]
        self.const = ivq(D["const"])
        idx = D["idx"]
        self.lag = [(idx[n], iv.mpf(l), iv.mpf(b)) for n, l, b in LAG]

    def forward(self, box, grad=False, clip=False):
        """box: list of 5 (lo, hi) mpf/str; returns dict values, dict grads, infeasible flag."""
        d = len(box)
        X, G = {}, {}
        zero = [iv.mpf(0)] * d
        for i, j in enumerate(self.D["inputs"]):
            X[j] = iv.mpf([box[i][0], box[i][1]])
            if grad:
                g = list(zero)
                g[i] = iv.mpf(1)
                G[j] = g
        infeas = False
        for op in self.ops:
            if op[0] == "lin":
                _, v, terms, b = op
                s = b
                for o, w in terms:
                    s = s + w * X[o]
                X[v] = s
                if grad:
                    g = list(zero)
                    for o, w in terms:
                        go = G[o]
                        g = [g[i] + w * go[i] for i in range(d)]
                    G[v] = g
            else:
                _, v, u = op
                T = iv_tanh(X[u])
                X[v] = T
                if grad:
                    dT = 1 - iv_sq(T)
                    G[v] = [dT * gi for gi in G[u]]
            if v in self.cb:
                lo, hi = self.cb[v]
                m = meet(X[v], lo, hi)
                if m is None:
                    infeas = True
                    if clip:
                        return X, G, True
                elif clip:
                    X[v] = m
        return X, G, infeas

    def f(self, X, G=None, d=5):
        f = self.const
        g = [iv.mpf(0)] * d if G is not None else None
        for j, a in self.lin:
            f = f + a * X[j]
            if G is not None:
                g = [g[i] + a * G[j][i] for i in range(d)]
        for p, r, a in self.bil:
            f = f + a * (iv_sq(X[p]) if p == r else X[p] * X[r])
            if G is not None:
                if p == r:
                    g = [g[i] + a * 2 * X[p] * G[p][i] for i in range(d)]
                else:
                    g = [g[i] + a * (G[p][i] * X[r] + X[p] * G[r][i]) for i in range(d)]
        return f, g

    def lagr(self, X, f, G=None, g=None, d=5):
        L = f
        Lg = list(g) if g is not None else None
        for j, lam, b in self.lag:
            L = L - lam * (X[j] - b)
            if G is not None:
                Lg = [Lg[i] - lam * G[j][i] for i in range(d)]
        return L, Lg

    def bound(self, box):
        """lower bound of f over box ∩ R: (lb, parts) with parts = natural, MV f, MV Lagrangian, infeasible."""
        d = len(box)
        c = [(mpmath.mpf(a) + mpmath.mpf(b)) / 2 for a, b in box]       # any point in the box works
        Xc, _, _ = self.forward([(ci, ci) for ci in c])
        fc, _ = self.f(Xc)
        Lc, _ = self.lagr(Xc, fc)
        X, G, inf1 = self.forward(box, grad=True)
        f, g = self.f(X, G)
        Dd = [iv.mpf([a, b]) - ci for (a, b), ci in zip(box, c)]
        mvf, mvL = fc, Lc
        _, Lg = self.lagr(X, f, G, g)
        for i in range(d):
            mvf = mvf + g[i] * Dd[i]
            mvL = mvL + Lg[i] * Dd[i]
        # mean-value enclosure of constrained variables
        inf2 = False
        for j, (lo, hi) in self.cb.items():
            m = Xc[j]
            for i in range(d):
                m = m + G[j][i] * Dd[i]
            if meet(m, lo, hi) is None:
                inf2 = True
        Xn, _, inf3 = self.forward(box, clip=True)
        nat = self.f(Xn)[0] if not inf3 else None
        infeas = inf1 or inf2 or inf3
        parts = dict(nat=None if nat is None else float(nat.a), mvf=float(mvf.a), mvL=float(mvL.a),
                     infeasible=infeas, nat_unclipped=float(f.a))
        if infeas:
            return mpmath.inf, parts
        return max(nat.a, mvf.a, mvL.a), parts


# ----------------------------------------------------------------------------- float model (sampling)
class FloatModel:
    def __init__(self, D):
        self.D = D
        self.ops = []
        for op in D["ops"]:
            if op[0] == "lin":
                _, v, cv, terms, rhs = op
                self.ops.append(("lin", v, [(o, float(-a / cv)) for o, a in terms], float(rhs / cv)))
            else:
                self.ops.append(op)
        self.cb = [(j, -np.inf if lo is None else float(lo), np.inf if hi is None else float(hi)) for j, lo, hi in D["cb"]]
        self.lin = [(j, float(a)) for j, a in D["lin"].items()]
        self.bil = [(p, r, float(a)) for (p, r), a in D["bil"].items()]
        self.const = float(D["const"])
        self.tanh_out = {op[1] for op in D["ops"] if op[0] == "tanh"}

    def eval(self, U):
        """U (n,5) -> f (n,), min slack over constraints of R (n,)."""
        X = {}
        for i, j in enumerate(self.D["inputs"]):
            X[j] = U[:, i]
        for op in self.ops:
            if op[0] == "lin":
                _, v, terms, b = op
                s = np.full(U.shape[0], b)
                for o, w in terms:
                    s = s + w * X[o]
                X[v] = s
            else:
                X[op[1]] = np.tanh(X[op[2]])
        f = np.full(U.shape[0], self.const)
        for j, a in self.lin:
            f = f + a * X[j]
        for p, r, a in self.bil:
            f = f + a * X[p] * X[r]
        slack = np.full(U.shape[0], np.inf)
        for j, lo, hi in self.cb:
            if j in self.tanh_out:      # tanh(z) lies in (-1, 1): these bounds always hold exactly
                continue
            slack = np.minimum(slack, np.minimum(X[j] - lo, hi - X[j]))
        return f, slack, X

    def slacks(self, u):
        """per-constraint slacks at one point: non-tanh bounds individually, the rest as one min."""
        _, s, X = self.eval(u[None, :])
        tanh_out = {op[1] for op in self.ops if op[0] == "tanh"}
        out, rest = [], np.inf
        for j, lo, hi in self.cb:
            if j in tanh_out or max(abs(lo), abs(hi)) >= 1e5 and not (np.isinf(lo) or np.isinf(hi)):
                rest = min(rest, X[j][0] - lo, hi - X[j][0])
                continue
            if np.isfinite(lo):
                out.append(X[j][0] - lo)
            if np.isfinite(hi):
                out.append(hi - X[j][0])
        out.append(rest)
        return np.array(out)


# ----------------------------------------------------------------------------- commands
def cmd_structure():
    D = decode(verbose=True)
    I, N, idx = D["I"], D["N"], D["idx"]
    # identities at the wave3 full point and at p1: objvar vs f(forward vars of the same point)
    for tag in ["p1", "wave3"]:
        s = read_sol(os.path.join(SOL, f"ann_cumene_tanh.{tag}.sol"))
        with mp.workdps(50):
            xs = {j: mp.mpf(s[N[j]]) for j in range(len(N))}
            fpt = fobj(D, xs, lambda q: mp.mpf(q.numerator) / q.denominator)      # f on the point's own values
            u = [s[n] for n in INPUT_NAMES]
            xf = forward_mp(D, u)
            ffw = fobj(D, xf, lambda q: mp.mpf(q.numerator) / q.denominator)      # f of forward propagation from u
            dev = max(abs(xf[j] - xs[j]) for j in xf)
            print(f"[{tag}] objvar {mp.nstr(xs[idx['objvar']], 20)}  f(point vars) {mp.nstr(fpt, 20)}  "
                  f"f(forward(u)) {mp.nstr(ffw, 20)}  max |forward - point| {mp.nstr(dev, 3)}")
            # the product identities at the point
            for key, rule in D["prodrule"].items():
                a, b = sorted(key)
                lhs = xs[a] * xs[b]
                rhs = sum(mp.mpf(q.numerator) / q.denominator * xs[p] * xs[r] for p, r, q in rule)
                print(f"    {N[a]}*{N[b]} - RHS = {mp.nstr(lhs - rhs, 3)}")
            print(f"    x746 {mp.nstr(xs[idx['x746']], 12)}  x766 {mp.nstr(xs[idx['x766']], 12)}  x753 {mp.nstr(xs[idx['x753']], 12)}")
    # range of x746, x766, x753 over the whole input box (natural interval enclosure, sign information)
    M = IvModel(D)
    X, _, _ = M.forward([(str(a), str(b)) for a, b in [(float(p), float(q)) for p, q in D["box"]]], clip=False)
    for n in ["x746", "x766", "x753", "x647", "x772"]:
        print(f"natural enclosure over the full input box (unclipped): {n} in [{mpmath.nstr(X[idx[n]].a, 8)}, {mpmath.nstr(X[idx[n]].b, 8)}]")


def cmd_points():
    D = decode()
    I, N = D["I"], D["N"]
    for tag in ["p1", "wave3"]:
        s = read_sol(os.path.join(SOL, f"ann_cumene_tanh.{tag}.sol"))
        x = [s[n] for n in N]
        obj, rv, wr, bv, wb = ev_osil_point(I, x, 50)
        print(f"[{tag}] objvar {mp.nstr(obj, 20)}  max row viol {mp.nstr(rv, 3)} ({wr})  max bound viol {mp.nstr(bv, 3)} ({wb})")
        with mp.workdps(50):
            xf = forward_mp(D, [s[n] for n in INPUT_NAMES])
            ff = fobj(D, xf, lambda q: mp.mpf(q.numerator) / q.denominator)
            slack = min(min((xf[j] - mp.mpf(lo.numerator) / lo.denominator) if lo is not None else mp.inf,
                            (mp.mpf(hi.numerator) / hi.denominator - xf[j]) if hi is not None else mp.inf) for j, lo, hi in D["cb"])
            print(f"      f(u) by forward propagation (reduced model) {mp.nstr(ff, 20)}  min slack of R constraints {mp.nstr(slack, 3)}")


def local_min(FM, lo, hi, u0):
    from scipy.optimize import minimize

    def fun(u):
        f, s, _ = FM.eval(u[None, :])
        return f[0]

    def con(u):
        return FM.slacks(u)
    r = minimize(fun, u0, bounds=list(zip(lo, hi)), method="SLSQP",
                 constraints=[dict(type="ineq", fun=con)], options=dict(maxiter=300, ftol=1e-12))
    u = np.clip(r.x, lo, hi)
    f, s, _ = FM.eval(u[None, :])
    return f[0], s[0], u


def make_boxes(D, rng):
    lo0 = np.array([float(a) for a, b in D["box"]])
    hi0 = np.array([float(b) for a, b in D["box"]])
    W = hi0 - lo0
    ustar = np.array([370.9280572920674, 0.7863373968889928, 1.620252679906157, 0.9494678019619749, 0.734065236105183])
    boxes = [("full", lo0, hi0)]
    for frac in [0.5, 0.25, 0.125, 0.0625]:
        for t in range(2):
            w = W * frac
            a = lo0 + rng.random(5) * (W - w)
            boxes.append((f"rand{frac:g}-{t}", a, a + w))
    for h in [1e-2, 1e-3, 1e-4, 1e-5]:
        a = np.maximum(lo0, ustar - h * W)
        b = np.minimum(hi0, ustar + h * W)
        boxes.append((f"u*±{h:g}W", a, b))
    return boxes, ustar


def cmd_boxes(nsamp=20000, nloc=8):
    D = decode()
    M = IvModel(D)
    FM = FloatModel(D)
    rng = np.random.default_rng(20260930)
    boxes, ustar = make_boxes(D, rng)
    fs, ss, _ = FM.eval(ustar[None, :])
    print(f"float check at u*: f {fs[0]!r} slack {ss[0]:.3e}")
    res = []
    CLAIM = -4024.4949777104284
    for name, lo, hi in boxes:
        t0 = time.time()
        lb, parts = M.bound([(mpmath.mpf(float(a)), mpmath.mpf(float(b))) for a, b in zip(lo, hi)])
        tb = time.time() - t0
        U = lo + (hi - lo) * rng.random((nsamp, 5))
        f, s, _ = FM.eval(U)
        feas = s >= 0
        smin = float(f[feas].min()) if feas.any() else np.inf
        best = (smin, None)
        for k in range(nloc):
            u0 = U[rng.integers(nsamp)] if not feas.any() or k % 2 else U[feas][np.argmin(f[feas])]
            fl, sl, ul = local_min(FM, lo, hi, u0)
            if sl >= -1e-9 and fl < best[0]:
                best = (float(fl), ul)
        row = dict(box=name, lo=lo.tolist(), hi=hi.tolist(), lb=float(lb), parts=parts, nfeas=int(feas.sum()),
                   sampled_min=smin, local_min=best[0], t_bound=tb)
        res.append(row)
        ok = (not np.isfinite(best[0])) or float(lb) <= best[0] + 1e-6
        print(f"{name:14s} lb {float(lb):14.6f} (nat {parts['nat']}, mvf {parts['mvf']:.6g}, mvL {parts['mvL']:.6g}, "
              f"infeas {parts['infeasible']}) feasible samples {int(feas.sum())}/{nsamp} sampled min {smin:.6f} "
              f"local min {best[0]:.6f} lb<=min {ok} below-claim {best[0] < CLAIM} ({tb:.1f}s)", flush=True)
    json.dump(res, open(os.path.join(HERE, "boxes_verifier.json"), "w"), indent=1)


def cmd_boxes2(nbox=1200, per_box=200):
    """many small boxes that each contain a feasible point (so min over box ∩ R <= f(point));
    records the verifier's rigorous lb, f at the known feasible point and sampled feasible min."""
    D = decode()
    M = IvModel(D)
    FM = FloatModel(D)
    rng = np.random.default_rng(11)
    lo0 = np.array([float(a) for a, b in D["box"]])
    hi0 = np.array([float(b) for a, b in D["box"]])
    W = hi0 - lo0
    U = lo0 + W * rng.random((400000, 5))
    f, s, _ = FM.eval(U)
    ok = s > 1e-9
    Uf, ff = U[ok], f[ok]
    order = np.argsort(ff)
    pick = np.concatenate([order[:nbox // 2], rng.choice(len(ff), nbox - nbox // 2, replace=False)])
    print(f"{ok.sum()} strictly feasible of {len(U)} samples; best sampled f {ff[order[0]]:.6f}", flush=True)
    rows = []
    t0 = time.time()
    for n, i in enumerate(pick):
        c = Uf[i]
        w = W * 2.0 ** -rng.uniform(3, 20, 5)
        r = rng.random(5)
        lo = np.maximum(lo0, c - r * w)
        hi = np.minimum(hi0, c + (1 - r) * w)
        lb, parts = M.bound([(mpmath.mpf(float(a)), mpmath.mpf(float(b))) for a, b in zip(lo, hi)])
        V = lo + (hi - lo) * rng.random((per_box, 5))
        fv, sv, _ = FM.eval(V)
        smin = float(fv[sv >= 0].min()) if (sv >= 0).any() else np.inf
        rows.append(dict(lo=lo.tolist(), hi=hi.tolist(), center=c.tolist(), f_center=float(ff[i]),
                         sampled_min=min(smin, float(ff[i])), lb=float(lb), infeasible=parts["infeasible"]))
        if n % 200 == 0:
            print(f"  {n} boxes, {time.time() - t0:.0f}s", flush=True)
    json.dump(rows, open(os.path.join(HERE, "boxes2_verifier.json"), "w"))
    lbs = np.array([r["lb"] for r in rows])
    fm = np.array([r["sampled_min"] for r in rows])
    print(f"verifier: {len(rows)} boxes; infeasible-flagged {sum(r['infeasible'] for r in rows)} (must be 0); "
          f"max(lb - best feasible f in box) = {np.max(lbs - fm):.3e} (must be <= ~1e-8)")


if __name__ == "__main__":
    cmd = sys.argv[1]
    dict(structure=cmd_structure, points=cmd_points, boxes=cmd_boxes, boxes2=cmd_boxes2)[cmd]()
