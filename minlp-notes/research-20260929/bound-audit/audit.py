"""Audit driver: listed dual bounds versus listed points (MINLPLib).

Stages (run in order; each writes its output and can be re-run):
  screen    pages.json -> screen.json: every (solver dual, listed point) pair whose
            displayed values put the dual strictly on the wrong side of the point
            (min: d > p; max: d < p), for points with displayed infeas <= 1e-5.
  download  fetch sol/<name>.<p>.sol for the screened points (sequential, 1 s delay)
  evaluate  high-precision objective and violation of each screened point
            (audit_eval.py in a subprocess, timeout per point)
  verify    exact check / polish + Krawczyk for points with violation <= 1e-6
            (verify_one.py in a subprocess, timeout per point)
  classify  -> results.json, results.csv (one row per flagged pair)

Usage: python3 audit.py <stage> [--jobs N]
"""
import csv
import json
import math
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "minlp-notes bound audit (sequential, 1 req/s)"
VIOL_TOL = 1e-6
PAGE_INFEAS_MAX = 1e-5


def fnum(s):
    try:
        v = float(s)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def shown_slack(s):
    """Half a unit in the last digit shown (at most 10 significant digits are meaningful).
    This is the largest amount by which the listed value can differ from a value that was
    rounded to the digits shown."""
    v = float(s)
    t = s.lstrip("+-").lower()
    mant, _, ex = t.partition("e")
    dec = len(mant.split(".")[1]) if "." in mant else 0
    unit = 10.0 ** (-dec + (int(ex) if ex else 0))
    if v == 0:
        return 0.5e-8
    unit = max(unit, 10.0 ** (math.floor(math.log10(abs(v))) - 9))
    return unit / 2


def relgap(p, d):
    if p == d:
        return 0.0
    if p * d <= 0:
        return math.inf
    return abs(p - d) / min(abs(p), abs(d))


def load_pages():
    return json.load(open(os.path.join(HERE, "pages.json")))


def best_primal(r):
    sg = 1 if r["sense"] == "min" else -1
    pv = [fnum(p["value"]) for p in r["points"] if p["section"] == "primal" and fnum(p["value"]) is not None]
    return (min(pv, key=lambda v: sg * v) if pv else None)


def closing_solvers(r):
    """solvers whose listed dual is within MINLPLib's 1e-6 relative gap of the best listed primal"""
    p = best_primal(r)
    if p is None:
        return []
    out = []
    for d in r["duals"]:
        dv = fnum(d["value"])
        if dv is not None and relgap(p, dv) <= 1e-6:
            out.append(d["solver"])
    return out


# ---------------------------------------------------------------- screen
def screen():
    pairs, ties = [], []
    for r in load_pages():
        if r["sense"] not in ("min", "max"):
            continue
        sg = 1 if r["sense"] == "min" else -1
        for p in r["points"]:
            pv = fnum(p["value"])
            inf = fnum(p["infeas"])
            if pv is None or (inf is not None and inf > PAGE_INFEAS_MAX):
                continue
            for d in r["duals"]:
                dv = fnum(d["value"])
                if dv is None:
                    continue
                rec = dict(name=r["name"], point=p["point"], section=p["section"], p_listed=p["value"],
                           infeas_listed=p["infeas"], solver=d["solver"], d_listed=d["value"], d_date=d["date"])
                if sg * (dv - pv) > 0:
                    pairs.append(rec)
                elif dv == pv:
                    ties.append(rec)
    json.dump(dict(pairs=pairs, ties=ties), open(os.path.join(HERE, "screen.json"), "w"), indent=0)
    pts = sorted({(x["name"], x["point"]) for x in pairs})
    print(len(pairs), "pairs,", len(pts), "points,", len({x["name"] for x in pairs}), "instances;",
          len(ties), "display ties")


def screened_points():
    s = json.load(open(os.path.join(HERE, "screen.json")))
    return sorted({(x["name"], x["point"]) for x in s["pairs"]})


# ---------------------------------------------------------------- download
def download():
    os.makedirs(os.path.join(HERE, "sol"), exist_ok=True)
    for name, pt in screened_points():
        tag = f"{name}.{pt}"
        path = os.path.join(HERE, "sol", tag + ".sol")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        url = f"https://www.minlplib.org/sol/{tag}.sol"
        subprocess.run(["curl", "-s", "-f", "-m", "300", "-A", UA, "-o", path, url])
        print(tag, os.path.getsize(path) if os.path.exists(path) else "failed", flush=True)
        time.sleep(1.0)


# ---------------------------------------------------------------- evaluate / verify
def run_many(script, tags, outdir, jobs, timeout):
    os.makedirs(os.path.join(HERE, "logs", outdir), exist_ok=True)

    def one(tag):
        out = os.path.join(HERE, "logs", outdir, tag + ".json")
        if os.path.exists(out):
            return
        env = dict(os.environ, OMP_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2", MKL_NUM_THREADS="2")
        try:
            p = subprocess.run(["nice", "-n", "5", sys.executable, os.path.join(HERE, script), tag],
                               capture_output=True, text=True, timeout=timeout, env=env, cwd=HERE)
            print(p.stdout.strip()[-400:], p.stderr.strip()[-400:], flush=True)
            if not os.path.exists(out):
                json.dump(dict(error="no output", stderr=p.stderr[-2000:]), open(out, "w"))
        except subprocess.TimeoutExpired:
            json.dump(dict(error=f"timeout {timeout} s"), open(out, "w"))
            print(tag, "timeout", flush=True)

    with ThreadPoolExecutor(jobs) as ex:
        list(ex.map(one, tags))


def evaluate(jobs):
    tags = [f"{n}.{p}" for n, p in screened_points()
            if os.path.exists(os.path.join(HERE, "sol", f"{n}.{p}.sol"))]
    run_many("audit_eval.py", tags, "eval", jobs, 1800)


def load_eval(tag):
    p = os.path.join(HERE, "logs", "eval", tag + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


def small_viol(e, x):
    """violation small enough to flag: ours <= 1e-6, or MINLPLib's listed infeas <= 1e-6
    (the listed value is a double-precision evaluation, which can hide cancellation)"""
    li = fnum(x["infeas_listed"])
    return e["max_viol"] <= VIOL_TOL or (li is not None and li <= VIOL_TOL)


def flagged_points():
    s = json.load(open(os.path.join(HERE, "screen.json")))
    out = set()
    for x in s["pairs"]:
        e = load_eval(f"{x['name']}.{x['point']}")
        if not e or "error" in e or e.get("obj") is None or not small_viol(e, x):
            continue
        sg = 1 if e["sense"] == "min" else -1
        if sg * (Fraction(x["d_listed"]) - Fraction(e["obj"])) > 0:
            out.add(f"{x['name']}.{x['point']}")
    return sorted(out)


def has_cert(tag):
    """points handled by a dedicated exact certificate script (see the report)"""
    name = tag.rsplit(".", 1)[0]
    return any(os.path.exists(os.path.join(HERE, "logs", f)) for f in
               (f"cert_linear_{tag}.json", f"cert_ndnetgen_{tag}.json", f"cert_socp_{name}.json",
                f"cert_topopt_{tag}.json"))


BIG = {"topopt-cantilever_60x40_50"}  # run separately: verify_one.py --max-n 8000 --route-c-only


def verify(jobs):
    tags = [t for t in flagged_points() if not has_cert(t) and t.rsplit(".", 1)[0] not in BIG]
    run_many("verify_one.py", tags, "verify", jobs, 3600)


# ---------------------------------------------------------------- classify
def classify():
    pages = {r["name"]: r for r in load_pages()}
    s = json.load(open(os.path.join(HERE, "screen.json")))
    rows = []
    for x in s["pairs"]:
        tag = f"{x['name']}.{x['point']}"
        r = pages[x["name"]]
        sg = 1 if r["sense"] == "min" else -1
        e = load_eval(tag)
        rec = dict(x, sense=r["sense"], type=r["type"], solved=r["solved"], convex=r["convex"],
                   closing=x["solver"] in closing_solvers(r), n_closing=len(closing_solvers(r)))
        d = Fraction(x["d_listed"])
        rho = shown_slack(x["d_listed"])
        rec["d_slack"] = rho
        if not e or "error" in e or e.get("obj") is None:
            rec.update(cls="not evaluated", note=(e or {}).get("error", "no .sol"))
            rows.append(rec)
            continue
        rec.update(obj_eval=e["obj"], viol_eval=e["max_viol"], worst=e.get("worst_row"))
        if not small_viol(e, x):
            rec.update(cls="excluded: violation > 1e-6")
            rows.append(rec)
            continue
        if sg * (d - Fraction(e["obj"])) <= 0:
            rec.update(cls="not flagged: exact objective not beyond the dual")
            rows.append(rec)
            continue
        rec["margin_eval"] = float(sg * (d - Fraction(e["obj"])))
        vp = os.path.join(HERE, "logs", "verify", tag + ".json")
        v = json.load(open(vp)) if os.path.exists(vp) else None
        cpt = os.path.join(HERE, "logs", f"cert_topopt_{tag}.json")  # Krawczyk + exact checks
        if os.path.exists(cpt):
            c = json.load(open(cpt))
            if c.get("status") == "proved":
                v = dict(status="proved", obj_lo=c["obj_lo"].strip("'"), obj_hi=c["obj_hi"].strip("'"),
                         attempt="linear Krawczyk + exact checks (cert_topopt.py)")
        for script in ("cert_linear", "cert_ndnetgen"):  # exact rational repairs override
            cp_ = os.path.join(HERE, "logs", f"{script}_{tag}.json")
            if os.path.exists(cp_):
                c = json.load(open(cp_))
                if c.get("status") == "proved":
                    digits = c["objective_exact_30"].replace("e-30", "")  # floor(10^30 f)
                    lo = digits[:-30] + "." + digits[-30:]
                    hi = str(Fraction(lo) + Fraction(1, 10 ** 30))
                    hi = (digits[:-30] + "." + str(int(digits[-30:]) + 1).zfill(30)) if int(digits[-30:]) + 1 < 10 ** 30 else hi
                    v = dict(status="proved", obj_lo=lo, obj_hi=hi, attempt=f"exact rational repair ({script}.py)")
        cs_ = os.path.join(HERE, "logs", f"cert_socp_{x['name']}.json")
        if os.path.exists(cs_):
            c = json.load(open(cs_))
            digits = c["lower_bound_30_digits_rounded_down"].replace("e-30", "")  # floor(10^30 L)
            L = Fraction(digits) / 10 ** 30
            # stored as the exact rounded-down decimal (float(L) rounds to nearest and can exceed L)
            rec["rigorous_opt_lower"] = digits[:-30] + "." + digits[-30:]
            rec["repaired_obj"] = c.get("repaired_" + tag)
            if sg == 1 and d <= L:
                rec["route"] = "cert_socp.py (weak duality, exact)"
                rec["cls"] = "(ii) tolerance effect (proven)"
                rec["note"] = "listed dual <= rigorous lower bound on the exact optimum"
                rows.append(rec)
                continue
        if not v:
            rec.update(cls="(iii) undecided", note="not verified")
            rows.append(rec)
            continue
        rec["route"] = v.get("attempt") or v.get("route")
        if v.get("status") == "proved":
            lo, hi = Fraction(str(v["obj_lo"])), Fraction(str(v["obj_hi"]))
            rec.update(obj_lo=v["obj_lo"], obj_hi=v["obj_hi"])
            worst = hi if sg == 1 else lo
            best = lo if sg == 1 else hi
            margin = sg * (d - worst)  # > 0: exactly feasible point strictly beyond the dual
            rec["margin_proved"] = float(margin)
            # margin relative to |d| (the listed dual); all class (i) duals here have |d| >= 0.008
            rec["rel_margin"] = float(margin) / abs(float(d)) if d != 0 else float("inf")
            if margin > rho:
                rec["cls"] = "(i) proven invalid"
                # gross error vs exact-arithmetic violation within the 1e-6 relative convention
                rec["i_group"] = "gross" if rec["rel_margin"] > 1e-6 else "tolerance-scale"
            elif margin > 0:
                rec["cls"] = "(i-r) invalid as listed, within rounding of shown digits"
            elif sg * (d - best) <= 0:
                rec["cls"] = "(ii) tolerance effect"
                rec["note"] = "exactly feasible repair is not beyond the dual"
            else:
                rec["cls"] = "(iii) undecided"
                rec["note"] = "objective enclosure contains the dual"
        else:
            po = v.get("polished_obj")
            rec["note"] = v.get("reason", "")[:200]
            if po is not None and sg * (float(d) - po) <= 0:
                rec["cls"] = "(ii) tolerance effect (numerical)"
                rec["polished_obj"] = po
            else:
                rec["cls"] = "(iii) undecided"
                if po is not None:
                    rec["polished_obj"] = po
        rows.append(rec)
    json.dump(rows, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    cols = ["name", "type", "sense", "solved", "convex", "point", "section", "p_listed", "infeas_listed",
            "solver", "d_listed", "d_date", "closing", "obj_eval", "viol_eval", "margin_eval", "route",
            "obj_lo", "obj_hi", "margin_proved", "rel_margin", "d_slack", "polished_obj", "cls", "i_group", "note"]
    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for rec in rows:
            w.writerow([rec.get(k, "") for k in cols])
    from collections import Counter
    print(Counter(r["cls"] for r in rows))


if __name__ == "__main__":
    st = sys.argv[1]
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
    dict(screen=screen, download=download, classify=classify)[st]() if st in ("screen", "download", "classify") \
        else dict(evaluate=evaluate, verify=verify)[st](jobs)
