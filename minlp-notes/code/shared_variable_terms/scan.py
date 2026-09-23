"""How often does one variable carry several DISTINCT univariate nonlinear subexpressions?
For every MINLPLib OSiL file: all maximal univariate nonlinear subtrees g(x_k) anywhere in the model
(also nested inside multivariate expressions), plus pure squares from the quadratic section.
Shapes are canonical strings with the variable replaced by 'x'; constant factors at the top are dropped."""
import glob, json, os, sys, signal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
from uenv.osil import read_osil

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def vars_of(t, acc):
    if t[0] == "var": acc.add(t[1])
    elif t[0] != "num":
        for c in t[1:]: vars_of(c, acc)
    return acc


def is_lin(t):
    if t[0] in ("num", "var"): return True
    if t[0] in ("sum", "negate"): return all(is_lin(c) for c in t[1:])
    if t[0] == "times":
        nonconst = [c for c in t[1:] if vars_of(c, set())]
        return len(nonconst) <= 1 and all(is_lin(c) for c in nonconst)
    if t[0] == "divide": return is_lin(t[1]) and not vars_of(t[2], set())
    return False


def shape(t):
    if t[0] == "num": return f"{t[1]:.6g}"
    if t[0] == "var": return "x"
    return t[0] + "(" + ",".join(shape(c) for c in t[1:]) + ")"


def strip(t):
    """drop constant factors / negation / constant summands at the top"""
    while True:
        if t[0] == "negate": t = t[1]; continue
        if t[0] == "times":
            nc = [c for c in t[1:] if vars_of(c, set())]
            if len(nc) == 1: t = nc[0]; continue
        if t[0] == "divide" and not vars_of(t[2], set()): t = t[1]; continue
        return t


def collect(t, out):
    vs = vars_of(t, set())
    if len(vs) == 1 and not is_lin(t):
        if t[0] == "sum":                      # a univariate sum: its summands are separate terms
            for c in t[1:]: collect(c, out)
        else:
            s = strip(t)
            if not is_lin(s): out.setdefault(next(iter(vs)), set()).add(shape(s))
        return
    if t[0] not in ("num", "var"):
        for c in t[1:]: collect(c, out)


def handler(signum, frame): raise TimeoutError


signal.signal(signal.SIGALRM, handler)
with open(sys.argv[1], "w") as fh:
    for path in sorted(glob.glob(f"{OSIL}/*.osil")):
        name = Path(path).stem
        if os.path.getsize(path) > 30_000_000: continue
        signal.alarm(120)
        try:
            ins = read_osil(path)
            out = {}
            for r in ins.rows:
                if r["nl"] is not None: collect(r["nl"], out)
                for i, j, c in r["quad"]:
                    if i == j: out.setdefault(i, set()).add("square(x)")
            multi = {k: sorted(v) for k, v in out.items() if len(v) >= 2}
            rec = {"name": name, "nvars": len(ins.var_lb), "vars_with_term": len(out), "vars_with_2plus": len(multi),
                   "examples": [v for v in list(multi.values())[:3]]}
        except TimeoutError:
            rec = {"name": name, "status": "timeout"}
        except Exception as e:  # noqa: BLE001
            rec = {"name": name, "status": "error " + type(e).__name__}
        signal.alarm(0)
        fh.write(json.dumps(rec) + "\n")
