"""Scan MINLPLib OSiL files for ridge subexpressions sigma(a^T x + b), |supp(a)| >= 2.

Usage:  python scan_ridges.py [--jobs N] [--limit K] [name ...]
        python scan_ridges.py --report     (prints the markdown tables from the saved JSON)
Writes  ../minlplib-ridge-counts.csv   (one row per instance)
        ./minlplib-ridge-agg.json      (per-instance aggregated occurrence counters, used for the report)

Detection rules (all syntactic, on the OSiL expression trees; see the report for caveats):

  direct   A maximal nonlinear subtree T whose variable-containing maximal linear
           subtrees ("leaves") all share one direction a (up to scaling), with |supp(a)| >= 2.
           T is then a univariate function g of t = a^T x + b.  sigma label = the operator if T is
           op(L) (exp, ln, log10, sqrt, square, power p, k^t, signpower, abs, sin, cos, tan, tanh,
           erf, gamma, c/t); otherwise "comp[ops]" (e.g. 1/(1+exp(-t)), t*exp(t), (t)^2*(t)).
  quad     Quadratic terms of a row (qTerms plus top-level quadratic monomials in the nl tree) are
           split into connected components of the bilinear graph; a component with >= 2
           variables whose coefficient matrix has rank 1 is c*(v^T x)^2, i.e. an expanded
           (a^T x + b)^2.  Sums of several squares sharing variables are NOT decomposed.
  defined  A maximal univariate nonlinear subtree g(w) (or a lone quadratic term c*w^2) where w
           appears in a linear equality row with >= 3 variables (w = a^T x + b, |supp(a)| >= 2)
           and in no other purely linear row (an auxiliary-variable proxy).
  defined-loose  Same, but w also appears in other linear rows (e.g. a flow variable in several
           balance equations); the shortest linear equality is used as the "definition".  This
           fires on balance equations that are not meant as definitions, so it over-counts.

Curvature side needed (the task's simple rule):
  Top-level occurrence with coefficient c in a row: the row expression needs an underestimator
  if ub < inf or it is a minimized objective, an overestimator if lb > -inf or maximized.
  Underestimating c*g needs conv(g) if c>0 and conc(g) if c<0; overestimating symmetric.
  Nested occurrences (inside another nonlinear operator) need both sides (factorable aux var).
  The occurrence is "relevant" if it needs conv(g) and g is not convex on the interval of t,
  or needs conc(g) and g is not concave there.  The interval is computed from variable bounds
  (for defined variables: intersected with w's own bounds), clipped to sigma's natural domain.
  Curvature is analytic for the standard operators and numeric (second differences on a grid,
  infinite ends clipped) for composites.
  "bounded" means every variable of a^T x has finite bounds in the file.
"""
import sys, os, math, json, argparse
from collections import Counter, defaultdict
import numpy as np

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scouting", "minlplib-open-data"))
import osil  # noqa: E402

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
OUT_DIR = os.path.join(HERE, "..")
UNARY = {"exp", "ln", "log10", "sqrt", "square", "abs", "sin", "cos", "tan", "tanh", "erf", "gammaFn"}
INF = math.inf


# ---------------------------------------------------------------- tree helpers
def const_val(t):
    """numeric value of a variable-free subtree"""
    return float(ev(t, {}))


def linform(t):
    """(dict var->coef, const) if t is affine, else None"""
    op = t[0]
    if op == "num":
        return {}, t[1]
    if op == "var":
        return {t[1]: 1.0}, 0.0
    if op == "negate":
        r = linform(t[1])
        return None if r is None else ({k: -v for k, v in r[0].items()}, -r[1])
    if op == "sum":
        d, c = defaultdict(float), 0.0
        for ch in t[1:]:
            r = linform(ch)
            if r is None:
                return None
            for k, v in r[0].items():
                d[k] += v
            c += r[1]
        return dict(d), c
    if op == "times":
        nc = [ch for ch in t[1:] if osil.V(ch)]
        if len(nc) > 1:
            return None
        k = 1.0
        for ch in t[1:]:
            if not osil.V(ch):
                k *= const_val(ch)
        if not nc:
            return {}, k
        r = linform(nc[0])
        return None if r is None else ({v: k * a for v, a in r[0].items()}, k * r[1])
    if op == "divide" and not osil.V(t[2]):
        r = linform(t[1])
        k = const_val(t[2])
        return None if r is None else ({v: a / k for v, a in r[0].items()}, r[1] / k)
    if not osil.V(t):
        return {}, const_val(t)
    return None


def leaves(t, out):
    """maximal affine subtrees that contain variables; returns False if a variable occurs outside one"""
    if not osil.V(t):
        return True
    r = linform(t)
    if r is not None:
        a = {k: v for k, v in r[0].items() if v != 0.0}
        if a:
            out.append((t, a, r[1]))
        return True
    return all(leaves(ch, out) for ch in t[1:])


def direction(a):
    k0 = min(a)
    s = a[k0]
    return tuple(sorted((k, round(v / s, 9)) for k, v in a.items())), s


def interval(a, b, lb, ub):
    lo = hi = b
    for k, c in a.items():
        l, u = lb[k], ub[k]
        if c > 0:
            lo += c * l if l > -INF else -INF
            hi += c * u if u < INF else INF
        else:
            lo += c * u if u < INF else -INF
            hi += c * l if l > -INF else INF
    return lo, hi


# ---------------------------------------------------------------- numeric evaluation
_erf = np.vectorize(math.erf, otypes=[float])


def _gamma(x):
    return np.vectorize(lambda z: math.gamma(z) if z > 0 or z != int(z) else np.nan, otypes=[float])(x)


def ev(t, sub):
    """evaluate tree; sub maps id(node)->array (affine leaves replaced by functions of t)"""
    if id(t) in sub:
        return sub[id(t)]
    op = t[0]
    if op == "num":
        return t[1]
    if op == "var":
        raise ValueError("free variable")
    a = [ev(ch, sub) for ch in t[1:]]
    if op == "sum":
        return sum(a)
    if op == "negate":
        return -a[0]
    if op == "times":
        r = 1.0
        for x in a:
            r = r * x
        return r
    if op == "divide":
        return a[0] / a[1]
    if op == "power":
        return np.power(np.asarray(a[0], float), a[1])
    if op == "signpower":
        return np.sign(a[0]) * np.abs(a[0]) ** a[1]
    if op == "square":
        return a[0] * a[0]
    if op == "sqrt":
        return np.sqrt(a[0])
    if op == "exp":
        return np.exp(a[0])
    if op == "ln":
        return np.log(a[0])
    if op == "log10":
        return np.log10(a[0])
    if op in ("sin", "cos", "tan", "tanh", "abs"):
        return getattr(np, op)(a[0])
    if op == "erf":
        return _erf(a[0])
    if op == "gammaFn":
        return _gamma(a[0])
    if op == "min":
        return np.minimum.reduce(np.broadcast_arrays(*a))
    raise ValueError(op)


# ---------------------------------------------------------------- curvature of g on [L, U]
def _no_point_inside(L, U, off, per):
    """True if no point off + k*per lies strictly inside (L, U)"""
    k = math.floor((L - off) / per) + 1
    return off + k * per >= U


def curv(label, p, L, U):
    """(convex, concave) of the univariate function on [L, U] (already clipped to its domain)"""
    if L >= U:
        return True, True
    if label in ("exp", "kpow", "square"):
        return True, False
    if label in ("ln", "log10", "sqrt"):
        return False, True
    if label == "abs":
        return (True, True) if (L >= 0 or U <= 0) else (True, False)
    if label in ("tanh", "erf"):
        return (True, False) if U <= 0 else (False, True) if L >= 0 else (False, False)
    if label == "signpower":
        return (True, False) if L >= 0 else (False, True) if U <= 0 else (False, False)
    if label == "gammaFn":
        return (True, False) if L >= 0 else (False, False)
    if label == "inv":  # p = numerator constant
        if p == 0:
            return True, True
        if L >= 0:
            return (True, False) if p > 0 else (False, True)
        if U <= 0:
            return (False, True) if p > 0 else (True, False)
        return False, False
    if label == "power":
        if p in (0.0, 1.0):
            return True, True
        if p == int(p):
            pi = int(p)
            if pi > 0 and pi % 2 == 0:
                return True, False
            if pi > 0:
                return (True, False) if L >= 0 else (False, True) if U <= 0 else (False, False)
            if L >= 0:
                return True, False
            if U <= 0:
                return (True, False) if pi % 2 == 0 else (False, True)
            return False, False
        return (False, True) if 0 < p < 1 else (True, False)
    if label in ("sin", "cos", "tan"):
        if L == -INF or U == INF:
            return False, False
        if label == "tan" and not _no_point_inside(L, U, math.pi / 2, math.pi):
            return False, False
        off = 0.0 if label in ("sin", "tan") else math.pi / 2
        if not _no_point_inside(L, U, off, math.pi):
            return False, False
        m = 0.5 * (L + U)
        d2 = {"sin": -math.sin(m), "cos": -math.cos(m), "tan": math.tan(m)}[label]
        return (d2 >= 0, d2 <= 0)
    raise ValueError(label)


DOMAIN = {"ln": (0, INF), "log10": (0, INF), "sqrt": (0, INF), "gammaFn": (0, INF)}


def curv_numeric(T, lvs, L, U):
    """numeric curvature of composite T(t), t = first leaf; returns (convex, concave)"""
    if L == -INF and U == INF:
        L, U = -100.0, 100.0
    elif L == -INF:
        L = U - 200.0
    elif U == INF:
        U = L + 200.0
    if U - L < 1e-12:
        return True, True
    t = np.linspace(L, U, 401)
    (_, a0, b0) = lvs[0]
    d0, s0 = direction(a0)
    sub = {}
    for node, a, b in lvs:
        d, s = direction(a)
        mu = s / s0  # leaf = mu * (t - b0) + b
        sub[id(node)] = mu * (t - b0) + b
    with np.errstate(all="ignore"):
        try:
            g = np.asarray(ev(T, sub), float) * np.ones_like(t)
        except (ValueError, OverflowError, ZeroDivisionError):
            return False, False
    ok = np.isfinite(g)
    if ok.sum() < 5:
        return False, False
    g = g[ok]
    d2 = g[2:] - 2 * g[1:-1] + g[:-2]
    tol = 1e-9 * (np.abs(g).max() + 1.0)
    return bool((d2 >= -tol).all()), bool((d2 <= tol).all())


def classify(T, lvs, lead_iv):
    """label, parameter, and effective interval of the (single) leaf for standard ops"""
    op = T[0]
    if op in UNARY and len(lvs) == 1 and lvs[0][0] is T[1]:
        return op, None
    if op == "power" and not osil.V(T[2]) and lvs[0][0] is T[1]:
        return "power", const_val(T[2])
    if op == "power" and not osil.V(T[1]) and lvs[0][0] is T[2]:
        k = const_val(T[1])
        return ("kpow", k) if k > 0 else ("comp[power]", None)
    if op == "signpower" and not osil.V(T[2]) and lvs[0][0] is T[1]:
        return "signpower", const_val(T[2])
    if op == "divide" and not osil.V(T[1]) and lvs[0][0] is T[2]:
        return "inv", const_val(T[1])
    ops = set()

    def walk(u):
        if u[0] in ("num", "var") or linform(u) is not None:
            return
        if u[0] not in ("sum", "negate", "times", "divide") or (u[0] == "times" and sum(1 for c in u[1:] if osil.V(c)) > 1) \
                or (u[0] == "divide" and osil.V(u[2])):
            ops.add({"times": "prod", "divide": "div"}.get(u[0], u[0]))
        for c in u[1:]:
            walk(c)
    walk(T)
    return "comp[" + ",".join(sorted(ops)) + "]", None


# ---------------------------------------------------------------- per-instance scan
def size_bin(n):
    return "2" if n == 2 else "3-5" if n <= 5 else "6-10" if n <= 10 else "11-100" if n <= 100 else ">100"


def scan(path):
    name = os.path.basename(path)[:-5]
    I = osil.read(path)
    lb, ub, vt, rows = I["lb"], I["ub"], I["vt"], I["rows"]
    # linear equality rows usable as definitions w = a^T x + b
    defrow = {}
    nlinrows = Counter()  # number of purely linear rows each variable appears in
    for r, row in rows.items():
        if r < 0 or row["quad"] or row["nl"] is not None:
            continue
        lin = {k: v for k, v in row["lin"].items() if v != 0.0}
        nlinrows.update(lin)
        if row["lb"] != row["ub"]:
            continue
        if len(lin) < 3:
            continue
        for k in lin:
            if k not in defrow or len(lin) < len(defrow[k][0]):
                defrow[k] = (lin, row["lb"])
    agg = Counter()
    examples = {}

    argsets = defaultdict(set)  # kind -> distinct relevant ridge arguments (directions / defined vars)

    def record(kind, label, nv, bounded, ctx, need, cvx, ccv, row_r, text, arg):
        need_conv, need_conc = need
        rel = (need_conv and not cvx) or (need_conc and not ccv)
        lab = label
        agg[(kind, lab, size_bin(nv), int(bounded), ctx, int(rel))] += 1
        if rel:
            argsets[kind].add(arg)
        key = (kind, lab)
        if rel and key not in examples:
            examples[key] = f"{text} [n={nv}, {'bounded' if bounded else 'unbounded'}, {ctx}, row {row_r}]"

    def ctx_need(r, c, nested):
        row = rows[r]
        if r < 0:
            under, over, ctx = I["sense"] == "min", I["sense"] == "max", "obj"
        else:
            under, over = row["ub"] < INF, row["lb"] > -INF
            ctx = "eq" if row["lb"] == row["ub"] else "ineq"
        if nested:
            return ctx + "-nested", (True, True)
        return ctx, ((under and c > 0) or (over and c < 0), (under and c < 0) or (over and c > 0))

    def def_interval(w):
        lin, rhs = defrow[w]
        aw = lin[w]
        a = {k: -v / aw for k, v in lin.items() if k != w}
        lo, hi = interval(a, rhs / aw, lb, ub)
        bnd = all(lb[k] > -INF and ub[k] < INF for k in a)
        return max(lo, lb[w]), min(hi, ub[w]), len(a), bnd

    def handle_ridge(T, lvs, r, c, nested, text_hint=""):
        """T is a maximal subtree depending on one direction only"""
        d, _ = direction(lvs[0][1])
        nvars = len(d)
        node0, a0, b0 = lvs[0]
        if nvars >= 2:
            kind = "direct"
            L, U = interval(a0, b0, lb, ub)
            bounded = all(lb[k] > -INF and ub[k] < INF for k in a0)
        else:
            w = d[0][0]
            if w not in defrow:
                return
            kind = "defined" if nlinrows[w] == 1 else "defined-loose"
            wl, wu, nvars, bounded = def_interval(w)
            L, U = interval({0: a0[w]}, b0, [wl], [wu])
        label, p = classify(T, lvs, (L, U))
        if label.startswith("comp["):
            cvx, ccv = curv_numeric(T, lvs, L, U)
        else:
            dl, du = DOMAIN.get(label, (-INF, INF))
            if label == "power" and p != int(p):
                dl = 0.0
            cvx, ccv = curv(label, p, max(L, dl), min(U, du))
        ctx, need = ctx_need(r, c, nested)
        record(kind, label, nvars, bounded, ctx, need, cvx, ccv, r,
               f"{label}{'' if p is None else '(p=%g)' % p} on t in [{L:.3g},{U:.3g}]",
               d if kind == "direct" else w)

    def visit(t, r, c, nested):
        """t is a nonlinear subtree (not affine)"""
        lvs = []
        if leaves(t, lvs) and lvs and len({direction(a)[0] for _, a, _ in lvs}) == 1:
            handle_ridge(t, lvs, r, c, nested)
            return
        for ch in t[1:]:
            if osil.V(ch) and linform(ch) is None:
                visit(ch, r, c, True)

    def atoms(t, c, out):
        """top-level nonlinear atoms with their constant coefficient"""
        if linform(t) is not None:
            return
        op = t[0]
        if op == "sum":
            for ch in t[1:]:
                atoms(ch, c, out)
        elif op == "negate":
            atoms(t[1], -c, out)
        elif op == "times" and sum(1 for ch in t[1:] if osil.V(ch)) == 1:
            k = 1.0
            for ch in t[1:]:
                if not osil.V(ch):
                    k *= const_val(ch)
            atoms([ch for ch in t[1:] if osil.V(ch)][0], c * k, out)
        elif op == "divide" and not osil.V(t[2]):
            atoms(t[1], c / const_val(t[2]), out)
        else:
            out.append((t, c))

    def quad_monomial(t, c):
        """c*t as list of (i, j, coef) if t is (a w + d)^2 or (a v + d)(b w + e); else None"""
        if t[0] in ("square", "power"):
            if t[0] == "power" and (osil.V(t[2]) or const_val(t[2]) != 2.0):
                return None
            r = linform(t[1])
            if r is None or len(r[0]) != 1:
                return None
            (k, a), = r[0].items()
            return [(k, k, c * a * a)]
        if t[0] == "times":
            nc = [ch for ch in t[1:] if osil.V(ch)]
            if len(nc) != 2:
                return None
            for ch in t[1:]:
                if not osil.V(ch):
                    c *= const_val(ch)
            r1, r2 = linform(nc[0]), linform(nc[1])
            if r1 is None or r2 is None or len(r1[0]) != 1 or len(r2[0]) != 1:
                return None
            (i, a), = r1[0].items()
            (j, b), = r2[0].items()
            return [(i, j, c * a * b)]
        return None

    for r, row in rows.items():
        quad = list(row["quad"])
        if row["nl"] is not None:
            out = []
            atoms(row["nl"], 1.0, out)
            for t, c in out:
                q = quad_monomial(t, c)
                if q is not None:
                    quad += q
                else:
                    visit(t, r, c, False)
        if not quad:
            continue
        # quadratic part: rank-1 components
        par = {}

        def find(x):
            while par.setdefault(x, x) != x:
                par[x] = par[par[x]]
                x = par[x]
            return x
        Q = defaultdict(float)
        for i, j, c in quad:
            i, j = min(i, j), max(i, j)
            Q[(i, j)] += c
            par[find(i)] = find(j)
        comp = defaultdict(list)
        for (i, j), c in Q.items():
            if c != 0.0:
                comp[find(i)].append((i, j, c))
        for terms in comp.values():
            vs = sorted({v for i, j, _ in terms for v in (i, j)})
            n = len(vs)
            if n == 1:
                w = vs[0]
                if w in defrow:
                    c = terms[0][2]
                    wl, wu, nv, bnd = def_interval(w)
                    ctx, need = ctx_need(r, c, False)
                    record("defined" if nlinrows[w] == 1 else "defined-loose", "square", nv, bnd, ctx, need, True, wl == wu, r, "square of defined var", w)
                continue
            if n > 400 or len([1 for i, j, _ in terms if i != j]) != n * (n - 1) // 2:
                continue  # not dense, cannot be rank 1
            pos = {v: k for k, v in enumerate(vs)}
            M = np.zeros((n, n))
            for i, j, c in terms:
                if i == j:
                    M[pos[i], pos[i]] += c
                else:
                    M[pos[i], pos[j]] += c / 2
                    M[pos[j], pos[i]] += c / 2
            e, U_ = np.linalg.eigh(M)
            order = np.argsort(-np.abs(e))
            if abs(e[order[1]]) > 1e-8 * abs(e[order[0]]):
                continue
            mu = e[order[0]]
            v = U_[:, order[0]]
            a = {vs[k]: v[k] for k in range(n)}
            bnd = all(lb[k] > -INF and ub[k] < INF for k in a)
            ctx, need = ctx_need(r, mu, False)
            record("quad", "square", n, bnd, ctx, need, True, False, r, "expanded (a^T x)^2",
                   direction({k: round(float(x), 6) for k, x in a.items()})[0])
    distinct = {k: len(v) for k, v in argsets.items()}
    distinct["direct+quad"] = len(argsets["direct"] | argsets["quad"])
    return name, agg, examples, dict(nvars=len(vt), ncons=I["ncons"], distinct_relevant_args=distinct)


def work(path):
    try:
        name, agg, ex, info = scan(path)
        return dict(name=name, agg=[[list(k), v] for k, v in agg.items()],
                    examples={"|".join(k): v for k, v in ex.items()}, **info)
    except Exception as e:  # noqa: BLE001
        return dict(name=os.path.basename(path)[:-5], err=f"{type(e).__name__}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("names", nargs="*")
    args = ap.parse_args()
    if args.names:
        paths = [os.path.join(OSIL_DIR, n + ".osil") for n in args.names]
    else:
        paths = sorted((os.path.join(OSIL_DIR, f) for f in os.listdir(OSIL_DIR) if f.endswith(".osil")),
                       key=os.path.getsize, reverse=True)
    if args.limit:
        paths = paths[-args.limit:]
    import multiprocessing as mp
    res = []
    with mp.Pool(args.jobs, maxtasksperchild=20) as pool:
        for k, r in enumerate(pool.imap_unordered(work, paths, chunksize=1)):
            res.append(r)
            if "err" in r:
                print("ERR", r["name"], r["err"], file=sys.stderr, flush=True)
            if k % 100 == 0:
                print(k, r["name"], file=sys.stderr, flush=True)
    res.sort(key=lambda r: r["name"])
    if args.names or args.limit:
        for r in res:
            print(json.dumps(r)[:3000])
        return
    with open(os.path.join(HERE, "minlplib-ridge-agg.json"), "w") as f:
        json.dump(res, f)
    write_csv(res)


def ndistinct(r):
    """distinct relevant ridge arguments (direct/quad directions plus strictly defined variables)"""
    d = r.get("distinct_relevant_args", {})
    return d.get("direct+quad", 0) + d.get("defined", 0)


STRICT = ("direct", "quad", "defined")  # kinds counted in the headline numbers
OPEN_CSV = os.path.join(HERE, "..", "..", "scouting", "minlplib-open-data", "open.csv")


def write_csv(res):
    """one row per instance; totals and breakdowns count direct+quad+defined (not defined-loose)"""
    import csv
    gap = {r["name"]: r["gap"] for r in csv.DictReader(open(OPEN_CSV))}
    with open(os.path.join(OUT_DIR, "minlplib-ridge-counts.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "open", "gap", "nvars", "ncons", "error",
                    "ridge_total", "ridge_relevant", "ridge_relevant_bounded", "ridge_relevant_toplevel",
                    "direct_relevant", "quad_relevant", "defined_relevant", "defined_loose_relevant",
                    "distinct_relevant_args",
                    "relevant_by_sigma", "relevant_by_argsize", "relevant_by_context"])
        for r in res:
            head = [r["name"], int(r["name"] in gap), gap.get(r["name"], "")]
            if "err" in r:
                w.writerow(head + ["", "", r["err"]] + [""] * 12)
                continue
            tot = rel = relb = relt = 0
            kind, sig, size, ctx = Counter(), Counter(), Counter(), Counter()
            for (k, lab, sb, bnd, cx, rl), v in r["agg"]:
                if rl:
                    kind[k] += v
                if k not in STRICT:
                    continue
                tot += v
                if rl:
                    rel += v
                    relb += v * bnd
                    relt += v * ("nested" not in cx)
                    sig[lab] += v
                    size[sb] += v
                    ctx[cx] += v
            fmt = lambda C: ";".join(f"{a}:{b}" for a, b in C.most_common())  # noqa: E731
            w.writerow(head + [r["nvars"], r["ncons"], "", tot, rel, relb, relt,
                               kind["direct"], kind["quad"], kind["defined"], kind["defined-loose"], ndistinct(r),
                               fmt(sig), fmt(size), fmt(ctx)])




def report():
    """print the markdown tables used in ../minlplib-ridge-scan.md"""
    import csv
    res = json.load(open(os.path.join(HERE, "minlplib-ridge-agg.json")))
    opn = {r["name"]: r for r in csv.DictReader(open(OPEN_CSV))}
    ok = [r for r in res if "err" not in r]
    print(f"scanned {len(res)}, errors {len(res) - len(ok)}: {[r['name'] for r in res if 'err' in r]}\n")
    for r in ok:
        r["occ"] = [(tuple(k), v) for k, v in r["agg"]]

    def tab(title, keyf, kinds=STRICT, rel_only=True):
        occ, inst, occb = Counter(), defaultdict(set), Counter()
        for r in ok:
            for (k, lab, sb, bnd, cx, rl), v in r["occ"]:
                if k in kinds and (rl or not rel_only):
                    key = keyf(k, lab, sb, bnd, cx)
                    occ[key] += v
                    occb[key] += v * bnd
                    inst[key].add(r["name"])
        print(f"| {title} | occurrences | of which bounded | instances | open instances |")
        print("|---|---:|---:|---:|---:|")
        for key, v in occ.most_common():
            print(f"| {key} | {v} | {occb[key]} | {len(inst[key])} | {sum(1 for n in inst[key] if n in opn)} |")
        print()

    # headline
    print("| subset | instances with >=1 | open among them | occurrences |")
    print("|---|---:|---:|---:|")
    for label, kinds, relf, bf in [
            ("any ridge, direct+quad", ("direct", "quad"), False, False),
            ("any ridge, direct+quad+defined", STRICT, False, False),
            ("relevant, direct+quad", ("direct", "quad"), True, False),
            ("relevant, direct+quad+defined", STRICT, True, False),
            ("relevant and bounded, direct+quad+defined", STRICT, True, True),
            ("relevant, top-level only (not nested), direct+quad+defined", STRICT, True, "top"),
            ("relevant, defined-loose only", ("defined-loose",), True, False)]:
        names, tot = set(), 0
        for r in ok:
            c = sum(v for (k, lab, sb, bnd, cx, rl), v in r["occ"] if k in kinds and (rl or not relf)
                    and (bf is False or (bf is True and bnd) or (bf == "top" and "nested" not in cx)))
            if c:
                names.add(r["name"])
                tot += c
        print(f"| {label} | {len(names)} | {sum(1 for n in names if n in opn)} | {tot} |")
    print(f"\ndistinct relevant ridge arguments (direct+quad+defined): {sum(ndistinct(r) for r in ok)}")
    print(f"\nopen instances scanned: {sum(1 for r in ok if r['name'] in opn)}; solved: {sum(1 for r in ok if r['name'] not in opn)}\n")
    tab("kind (relevant)", lambda k, lab, sb, bnd, cx: k, kinds=STRICT + ("defined-loose",))
    tab("sigma (relevant; direct+quad+defined)", lambda k, lab, sb, bnd, cx: lab)
    tab("sigma x kind (relevant)", lambda k, lab, sb, bnd, cx: f"{lab} / {k}")
    tab("sigma (all ridge occurrences incl. convex-side; direct+quad+defined)", lambda k, lab, sb, bnd, cx: lab, rel_only=False)
    tab("argument size |supp(a)| (relevant)", lambda k, lab, sb, bnd, cx: sb)
    tab("context (relevant)", lambda k, lab, sb, bnd, cx: cx)
    # top 40
    rows = []
    for r in ok:
        rel = Counter(); relb = 0; sz = Counter(); cxs = Counter(); kd = Counter()
        loose = 0
        for (k, lab, sb, bnd, cx, rl), v in r["occ"]:
            if not rl:
                continue
            if k == "defined-loose":
                loose += v
                continue
            rel[lab] += v; relb += v * bnd; sz[sb] += v; cxs[cx] += v; kd[k] += v
        n = sum(rel.values())
        if n:
            rows.append((n, r, rel, relb, sz, cxs, kd, loose))
    rows.sort(key=lambda x: -x[0])
    print("| # | instance | open (gap) | relevant | distinct args | bounded | kinds | sigma | arg sizes | contexts | nvars |")
    print("|---:|---|---|---:|---:|---:|---|---|---|---|---:|")
    f = lambda C: ", ".join(f"{a} {b}" for a, b in C.most_common(4))  # noqa: E731
    for i, (n, r, rel, relb, sz, cxs, kd, loose) in enumerate(rows[:40], 1):
        o = opn.get(r["name"])
        og = f"open ({float(o['gap']):.3g})" if o else "solved"
        print(f"| {i} | {r['name']} | {og} | {n} | {ndistinct(r)} | {relb} | {f(kd)} | {f(rel)} | {f(sz)} | {f(cxs)} | {r['nvars']} |")
    print("\nexamples:")
    for n, r, *_ in rows[:40]:
        print(r["name"], "::", " || ".join(v for k, v in r["examples"].items() if not k.startswith("defined-loose"))[:400])


if __name__ == "__main__":
    if sys.argv[1:] == ["--report"]:
        report()
    else:
        main()
