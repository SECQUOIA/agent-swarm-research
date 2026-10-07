"""Delta-debugging minimization of a wrong-'optimal' SCIP reproducer.

The model is a spec (models/<key>.json, from export_models.py); the witness
is an exactly feasible point (witness/<key>.json).  A candidate model is
obtained by (a) keeping a subset of the rows and (b) shrinking the bounds of
some variables to a small decimal box around the witness (binaries: fixed to
the witness value).  Both operations keep the witness exactly feasible, so
its objective value w stays an upper bound on the true optimum.

A candidate is "interesting" if SCIP (PySCIPOpt, given settings) reports
status optimal with dual bound > w + THR for at least NEED of the given
random seed shifts.  Phases: ddmin over rows; fix binaries; ddmin over the
set of variables left free; ddmin over rows again.

usage: python3 minimize.py KEY SETTINGS_JSON SEEDS NEED OUTPREFIX [THR] [DIGITS]
e.g.   python3 minimize.py pair2236 '{}' 7 1 min/pair2236_s7
"""
import json
import math
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from export_models import write_cip  # noqa: E402
import exact_check  # noqa: E402

KEY = sys.argv[1]
SETTINGS = json.loads(sys.argv[2])
SEEDS = [int(s) for s in sys.argv[3].split(",")]
NEED = int(sys.argv[4])
OUTP = sys.argv[5]
THR = float(sys.argv[6]) if len(sys.argv) > 6 else 0.01
DIGITS = int(sys.argv[7]) if len(sys.argv) > 7 else 7
WORKERS = int(os.environ.get("WORKERS", "2"))
TL = 120.0

SPEC = json.load(open(os.path.join(HERE, "models", f"{KEY}.json")))
WIT = {k: F(v) for k, v in json.load(open(os.path.join(HERE, "witness", f"{KEY}.json"))).items()}
OBJ = {n: F(a) for n, a in SPEC["obj"]}
WVAL = sum(a * WIT[n] for n, a in OBJ.items())
VARS = {v["name"]: v for v in SPEC["vars"]}
LOG = open(OUTP + ".log", "a")
CACHE = {}
NTEST = [0]


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


def dec_floor(x, d):
    return F(math.floor(x * 10 ** d), 10 ** d)


def dec_ceil(x, d):
    return F(math.ceil(x * 10 ** d), 10 ** d)


def fmt(q):
    """exact decimal string of a rational with power-of-10 denominator"""
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    s = format(Decimal(q.numerator) / Decimal(q.denominator), "f")
    assert F(s) == q
    return s


def box_of(name):
    v = VARS[name]
    w = WIT[name]
    if v["type"] == "B":
        return (str(int(w)), str(int(w)))
    lo, hi = dec_floor(w, DIGITS), dec_ceil(w, DIGITS)
    if v["lb"] is not None:
        lo = max(lo, F(v["lb"]))
    if v["ub"] is not None:
        hi = min(hi, F(v["ub"]))
    assert lo <= w <= hi
    return (fmt(lo), fmt(hi))


def build(rows, fixed):
    """spec with the given row indices and the given variables boxed;
    variables in no kept row and without objective coefficient are dropped."""
    used = set(OBJ)
    for i in rows:
        for a, ns in SPEC["rows"][i]["terms"]:
            used.update(ns)
    vars_ = []
    for v in SPEC["vars"]:
        if v["name"] not in used:
            continue
        v = dict(v)
        if v["name"] in fixed:
            v["lb"], v["ub"] = box_of(v["name"])
        vars_.append(v)
    return dict(name=SPEC["name"] + "_reduced", vars=vars_, rows=[SPEC["rows"][i] for i in sorted(rows)],
                obj=[[n, a] for n, a in SPEC["obj"] if n in used])


ORACLE = os.environ.get("ORACLE", "pyscipopt")  # or a version of run_binary.py (10.0.2, 10.0.3, 10.1.0)


def run_one(path, seed):
    prm = dict(SETTINGS)
    prm["randomization/randomseedshift"] = seed
    if ORACLE != "pyscipopt":
        import run_binary
        try:
            r = run_binary.run(ORACLE, path, prm, timelimit=TL)
        except subprocess.TimeoutExpired:
            return dict(status="hang", dual=None)
        st = "optimal" if r["status"].startswith("problem is solved [optimal") else r["status"]
        return dict(status=st, dual=r["dual"])
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, "scip_worker.py"), path, json.dumps(prm), str(TL)],
                           capture_output=True, text=True, timeout=TL + 60, env=dict(os.environ, OMP_NUM_THREADS="1"))
        line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
        if p.returncode != 0 or not line.startswith("{"):
            return dict(status=f"crash{p.returncode}", dual=None)
        return json.loads(line)
    except subprocess.TimeoutExpired:
        return dict(status="hang", dual=None)


def interesting(rows, fixed):
    key = (frozenset(rows), frozenset(fixed))
    if key in CACHE:
        return CACHE[key]
    spec = build(rows, fixed)
    fd, path = tempfile.mkstemp(suffix=".cip", dir=os.path.join(HERE, "tmp"))
    os.close(fd)
    write_cip(spec, path)
    hits, res = 0, []
    for s in SEEDS:
        r = run_one(path, s)
        res.append((s, r["status"], r["dual"]))
        if r["status"] == "optimal" and r["dual"] is not None and r["dual"] > float(WVAL) + THR:
            hits += 1
        if hits >= NEED or hits + (len(SEEDS) - len(res)) < NEED:
            break
    os.unlink(path)
    ok = hits >= NEED
    NTEST[0] += 1
    CACHE[key] = ok
    return ok


def ddmin(items, test):
    """Classic ddmin (complements only, plus subsets at n = 2), testing up to
    WORKERS candidates in parallel; accepts the first success in order."""
    items = list(items)
    n = 2
    with ThreadPoolExecutor(WORKERS) as ex:
        while len(items) >= 2:
            k = len(items)
            chunks = [items[i * k // n:(i + 1) * k // n] for i in range(n)]
            cands = [[x for x in items if x not in set(c)] for c in chunks]
            if n == 2:
                cands = chunks + cands
            found = None
            for j in range(0, len(cands), WORKERS):
                batch = cands[j:j + WORKERS]
                oks = list(ex.map(test, batch))
                for c, ok in zip(batch, oks):
                    if ok:
                        found = c
                        break
                if found is not None:
                    break
            if found is not None:
                items = found
                n = max(n - 1, 2)
                log(f"  -> {len(items)} items (tests so far {NTEST[0]})")
            else:
                if n >= len(items):
                    break
                n = min(2 * n, len(items))
    if len(items) == 1 and test([]):
        items = []
    return items


def main():
    os.makedirs(os.path.join(HERE, "tmp"), exist_ok=True)
    tic = time.time()
    log(f"# minimize {KEY} oracle={ORACLE} settings={SETTINGS} seeds={SEEDS} need={NEED} thr={THR} digits={DIGITS}; "
        f"witness value {float(WVAL):.12f}")
    allrows = list(range(len(SPEC["rows"])))
    assert interesting(allrows, set()), "full model is not a reproducer under these settings"
    # phase 1: rows
    rows = ddmin(allrows, lambda R: interesting(R, set()))
    log(f"phase 1 (rows): {len(rows)} rows left, {time.time() - tic:.0f}s")
    # phase 2: fix binaries (all at once, else one by one)
    used = {n for i in rows for a, ns in SPEC["rows"][i]["terms"] for n in ns} | set(OBJ)
    bins = [n for n in used if VARS[n]["type"] == "B"]
    fixed = set()
    if interesting(rows, set(bins)):
        fixed = set(bins)
    else:
        for b in bins:
            if interesting(rows, fixed | {b}):
                fixed.add(b)
    log(f"phase 2 (binaries): fixed {sorted(fixed)}")
    # phase 3: ddmin over the set of free (unboxed) continuous variables
    conts = sorted(n for n in used if VARS[n]["type"] == "C" and n not in fixed)
    free = ddmin(conts, lambda Fr: interesting(rows, fixed | (set(conts) - set(Fr))))
    fixed |= set(conts) - set(free)
    log(f"phase 3 (variables): {len(free)} continuous variables left free: {free}")
    # phase 4: rows again
    rows = ddmin(rows, lambda R: interesting(R, fixed))
    log(f"phase 4 (rows): {len(rows)} rows left")
    spec = build(rows, fixed)
    write_cip(spec, OUTP + ".cip")
    json.dump(spec, open(OUTP + ".json", "w"), indent=0)
    json.dump({n: str(WIT[n]) for n in (v["name"] for v in spec["vars"])}, open(OUTP + ".witness.json", "w"), indent=0)
    log(f"final: {len(spec['vars'])} variables, {len(spec['rows'])} rows; tests {NTEST[0]}; {time.time() - tic:.0f}s")
    exact_check.check(OUTP + ".cip", {n: str(WIT[n]) for n in (v["name"] for v in spec["vars"])})


if __name__ == "__main__":
    main()
