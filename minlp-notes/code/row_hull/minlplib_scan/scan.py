"""Structural scan of MINLPLib (OSiL) for rows where the row hull could apply.

For every instance: list the additive univariate nonlinear terms g(x_k) with certified
curvature on the declared bounds, then test every purely linear row for
  (i)   >= 2 "secant items" (non-binary variables that carry a convex or concave term),
  (ii)  finite bounds on all row variables (declared, or one round of row-activity inference),
  (iii) nondegeneracy (no subset of the widths sums to B); equality rows only.
Output: one JSON line per instance.  The counts are a structural upper bound on
applicability, not a measurement of benefit.  See notes/row-hull-minlplib-scan.md.

Usage: python scan.py OSIL_DIR OUT.jsonl [--timeout SECONDS] [--only NAME ...]
One worker process does all the work; the parent only enforces the per-file timeout.
"""
from __future__ import annotations

import argparse
from collections import Counter
import glob
import json
import math
import multiprocessing as mp
import os
import signal
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "univariate_envelopes"))

INF = 1e20          # bounds at or beyond this magnitude count as infinite
TOL = 1e-9
SUBSET_MAX_ITEMS = 25
EXPR_TIMEOUT = 5    # seconds per curvature certification
MAX_LISTED = 200    # terms listed individually per instance; all terms are counted in term_shapes


# ---------------------------------------------------------------- additive terms
def const_value(t):
    """Value of a variable-free tree, or None."""
    op = t[0]
    if op == "num":
        return t[1]
    if op == "var":
        return None
    k = [const_value(c) for c in t[1:]]
    if any(v is None for v in k):
        return None
    try:
        if op == "sum":
            return sum(k)
        if op == "times":
            return math.prod(k)
        if op == "negate":
            return -k[0]
        if op == "divide":
            return k[0] / k[1]
        if op == "power":
            return k[0] ** k[1]
        if op == "square":
            return k[0] ** 2
        return {"log": math.log, "exp": math.exp, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                "abs": abs}[op](k[0])
    except (ValueError, ZeroDivisionError, OverflowError, KeyError):
        return None


def additive_terms(t, coef, out):
    """Flatten the top-level sum of ``t`` into (constant coefficient, subtree) pairs."""
    op = t[0]
    if op == "num":
        return
    if op == "sum":
        for c in t[1:]:
            additive_terms(c, coef, out)
    elif op == "negate":
        additive_terms(t[1], -coef, out)
    elif op == "times":
        c, rest = 1.0, []
        for ch in t[1:]:
            v = const_value(ch)
            if v is None:
                rest.append(ch)
            else:
                c *= v
        if not rest or c == 0.0:
            return
        if len(rest) == 1:
            additive_terms(rest[0], coef * c, out)
        else:
            out.append((coef * c, ("times", *rest)))
    elif op == "divide" and const_value(t[2]) not in (None, 0.0):
        additive_terms(t[1], coef / const_value(t[2]), out)
    else:
        out.append((coef, t))


def show(t, names):
    op = t[0]
    if op == "num":
        return f"{t[1]:g}"
    if op == "var":
        return "x"
    k = [show(c, names) for c in t[1:]]
    if op == "sum":
        return "(" + "+".join(k) + ")"
    if op == "times":
        return "*".join(k)
    if op == "negate":
        return "-" + k[0]
    if op == "divide":
        return f"({k[0]})/({k[1]})"
    if op == "power":
        return f"({k[0]})^({k[1]})"
    if op == "square":
        return f"({k[0]})^2"
    return f"{op}({k[0]})"


# ---------------------------------------------------------------- curvature
class _Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise _Timeout()


_CURV: dict = {}


def _flip(c):
    return {"convex": "concave", "concave": "convex"}.get(c, c)


def _fast(t, lo, hi):
    """Curvature of the most common atoms on [lo, hi] without sympy; None if not covered."""
    op = t[0]
    if op == "square" and t[1][0] == "var":
        return "convex"
    if op == "exp" and t[1][0] == "var":
        return "convex"
    if op in ("log", "sqrt") and t[1][0] == "var":
        ok = lo > 0 if op == "log" else lo >= 0
        return "concave" if ok else "unknown"
    if op == "power" and t[1][0] == "var" and t[2][0] == "num":
        p = t[2][1]
        if p in (0.0, 1.0):
            return "linear"
        if lo >= 0:
            if p < 0:
                return "convex" if lo > 0 else "unknown"
            return "concave" if p < 1 else "convex"     # x^p, 0<p<1, is continuous at 0
        if p != int(p):
            return "unknown"
        if p < 0 and hi >= 0:
            return "unknown"
        if int(p) % 2 == 0:
            return "convex"
        if hi <= 0:
            return "concave"
        return "neither"
    return None


def _certified(expr, lo, hi):
    import sympy as sp
    from uenv.curvature import X, certify_pieces, compile_ball
    from flint import arb
    if not expr.has(X):
        return "linear"
    d2e = sp.diff(expr, X, 2)
    if d2e == 0:
        return "linear"
    # Cheap certified refutation: g'' strictly negative at one point and strictly positive at another.
    try:
        d2 = compile_ball(d2e)
        neg = pos = False
        for k in range(1, 10):
            try:
                v = d2(arb(lo + (hi - lo) * k / 10))
            except (ZeroDivisionError, ValueError):
                continue
            neg, pos = neg or bool(v < 0), pos or bool(v > 0)
        if neg and pos:
            return "neither"
    except NotImplementedError:
        return "unknown"
    pieces = certify_pieces(expr, lo, hi)
    # An undecided sliver at an end point where g is finite (x**0.6 at 0) is accepted by continuity.
    if len(pieces) > 1 and pieces[0].label == "unknown":
        pieces = pieces[1:]
    if len(pieces) > 1 and pieces[-1].label == "unknown":
        pieces = pieces[:-1]
    labels = {p.label for p in pieces}
    if {"convex", "concave"} <= labels:
        return "neither"
    if "unknown" in labels:
        return "unknown"
    return labels.pop()


def curvature_tree(t, lo, hi):
    key = (t, lo, hi)
    if key in _CURV:
        return _CURV[key]
    res = _fast(t, lo, hi)
    if res is None:
        from uenv.curvature import X
        from uenv.osil import to_sympy
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(EXPR_TIMEOUT)
        try:
            res = _certified(to_sympy(t, X), lo, hi)
        except _Timeout:
            res = "unknown"
        except Exception:
            res = "unknown"
        finally:
            signal.alarm(0)
    _CURV[key] = res
    return res


def group_curvature(terms, lo, hi):
    """Curvature of sum_k c_k g_k(x) on [lo, hi]; terms = [(c_k, tree_k)]."""
    each = []
    for c, t in terms:
        cv = curvature_tree(t, lo, hi)
        each.append(cv if c > 0 else _flip(cv))
    kinds = {c for c in each if c != "linear"}
    if not kinds:
        return "linear"
    if len(kinds) == 1:
        return kinds.pop()
    if "unknown" in kinds and len(terms) == 1:
        return "unknown"
    # Mixed signs: certify the sum itself.
    tree = ("sum", *[("times", ("num", c), t) for c, t in terms])
    return curvature_tree(tree, lo, hi)


# ---------------------------------------------------------------- rows
def finite(v):
    return abs(v) < INF


def infer_bounds(inst, linear_rows):
    """One round of row-activity bound inference from the declared bounds; fills infinite bounds only."""
    lb, ub = list(inst.var_lb), list(inst.var_ub)
    new_lb, new_ub = list(lb), list(ub)
    for r in linear_rows:
        row = inst.rows[r + 1]
        lin = row["lin"]
        if all(finite(lb[j]) and finite(ub[j]) for j in lin):
            continue
        mn = mx = 0.0
        mn_inf, mx_inf = [], []
        for j, a in lin.items():
            lo_c, hi_c = (a * lb[j], a * ub[j]) if a > 0 else (a * ub[j], a * lb[j])
            if finite(lo_c):
                mn += lo_c
            else:
                mn_inf.append(j)
            if finite(hi_c):
                mx += hi_c
            else:
                mx_inf.append(j)
        for j, a in lin.items():
            if finite(lb[j]) and finite(ub[j]):
                continue
            lo_c, hi_c = (a * lb[j], a * ub[j]) if a > 0 else (a * ub[j], a * lb[j])
            # a*x_j <= row ub - min activity of the others
            if finite(row["ub"]) and (not mn_inf or mn_inf == [j]):
                rhs = (row["ub"] - (mn - (lo_c if finite(lo_c) else 0.0))) / a
                if a > 0:
                    new_ub[j] = min(new_ub[j], rhs)
                else:
                    new_lb[j] = max(new_lb[j], rhs)
            # a*x_j >= row lb - max activity of the others
            if finite(row["lb"]) and (not mx_inf or mx_inf == [j]):
                rhs = (row["lb"] - (mx - (hi_c if finite(hi_c) else 0.0))) / a
                if a > 0:
                    new_lb[j] = max(new_lb[j], rhs)
                else:
                    new_ub[j] = min(new_ub[j], rhs)
    out_lb = [l if finite(l) else n for l, n in zip(lb, new_lb)]
    out_ub = [u if finite(u) else n for u, n in zip(ub, new_ub)]
    return out_lb, out_ub


def subset_sum_hits(widths, B):
    """True / False / "unknown": does some subset of ``widths`` sum to B (tolerance TOL, relative to scale)?"""
    import numpy as np
    W = sum(widths)
    tol = TOL * max(1.0, W, abs(B))
    if B < -tol or B > W + tol:
        return "infeasible"
    if B <= tol or B >= W - tol:
        return True
    if max(widths) - min(widths) <= tol:                       # equal widths: B/w integer?
        q = B / widths[0]
        return abs(q - round(q)) * widths[0] <= tol
    n = len(widths)
    if n <= SUBSET_MAX_ITEMS:
        def sums(ws):
            s = np.zeros(1)
            for w in ws:
                s = np.concatenate([s, s + w])
            return s
        s1, s2 = sums(widths[: n // 2]), np.sort(sums(widths[n // 2:]))
        need = B - s1
        i = np.searchsorted(s2, need - tol)
        i = np.minimum(i, len(s2) - 1)
        return bool(np.any(np.abs(s2[i] - need) <= tol))
    # Integer data: exact bitset dynamic program when it is small enough.
    ints = [round(w) for w in widths]
    if all(abs(w - k) <= TOL for w, k in zip(widths, ints)) and abs(B - round(B)) <= TOL and n * W <= 4e9:
        bits = 1
        for k in ints:
            bits |= bits << k
        return bool((bits >> round(B)) & 1)
    return "unknown"


def analyse(path):
    from uenv.osil import nonlinear_ops, read_osil, variables
    t0 = time.time()
    inst = read_osil(path)
    nvars, nrows = len(inst.var_lb), len(inst.rows) - 1
    lb, ub, vt = inst.var_lb, inst.var_ub, inst.var_type

    def is_binary(j):
        return vt[j] == "B" or (vt[j] == "I" and lb[j] >= 0 and ub[j] <= 1)

    # --- additive univariate terms, grouped per (row, variable)
    shapes = Counter()               # (curvature, secant needed, vtype, declared bounds, in multivariate term, shape) -> count
    terms = []                       # [row, var, curvature, secant side needed, vtype, declared bounds, in multivariate term, text]
    counts = {"convex": 0, "concave": 0, "neither": 0, "unknown": 0, "linear": 0, "unbounded_var": 0,
              "fixed_var": 0}
    sec_loose, sec_strict, sec_binary = set(), set(), set()
    sec_sep = set()                  # strict, and the variable is in no multivariate term of that row
    sec_inferred = set()             # secant items whose interval needed bound inference
    linear_rows, nl_only_linear = [], 0
    row_groups = []
    for ridx, row in enumerate(inst.rows):
        r = ridx - 1                 # -1 is the objective
        flat = []
        for i, j, c in row["quad"]:
            if i == j and c != 0.0:
                flat.append((c, ("square", ("var", i))))
        if row["nl"] is not None:
            additive_terms(row["nl"], 1.0, flat)
        groups: dict[int, list] = {}
        has_nonlinear = any(i != j for i, j, _ in row["quad"])
        mixed = {v for i, j, _ in row["quad"] if i != j for v in (i, j)}   # variables in multivariate terms
        for c, sub in flat:
            vs = variables(sub)
            if len(vs) == 1 and nonlinear_ops(sub) >= 1:
                groups.setdefault(next(iter(vs)), []).append((c, sub))
                has_nonlinear = True
            elif sub[0] != "var":
                has_nonlinear = True
                mixed |= vs
        if r >= 0 and not has_nonlinear:
            if row["nl"] is not None:
                nl_only_linear += 1  # linear terms hidden in the expression tree: row is not analysed
            elif row["lin"]:
                linear_rows.append(r)
        if groups:
            row_groups.append((r, row, groups, mixed))

    ilb, iub = infer_bounds(inst, linear_rows)
    for r, row, groups, mixed in row_groups:
        for j, g in groups.items():
            declared = finite(lb[j]) and finite(ub[j])
            if not (finite(ilb[j]) and finite(iub[j])):
                counts["unbounded_var"] += 1
                continue
            if iub[j] <= ilb[j]:
                counts["fixed_var"] += 1
                continue
            cv = group_curvature(g, ilb[j], iub[j])
            counts[cv if declared else "inferred_" + cv] = counts.get(cv if declared else "inferred_" + cv, 0) + 1
            need = False
            if cv in ("convex", "concave"):
                if r == -1:
                    need = cv == ("concave" if inst.obj_sense == "min" else "convex")
                else:
                    need = (cv == "concave" and finite(row["ub"])) or (cv == "convex" and finite(row["lb"]))
                if is_binary(j):
                    sec_binary.add(j)
                else:
                    (sec_loose if declared else sec_inferred).add(j)
                    if need:
                        sec_strict.add(j)
                        if j not in mixed:
                            sec_sep.add(j)
            if len(terms) < MAX_LISTED:
                text = "+".join(f"{c:g}*{show(t, None)}" for c, t in g)[:80]
                terms.append([r, j, cv, int(need), vt[j], int(declared), int(j in mixed), text])
            shape = "+".join(sorted({("-" if c < 0 else "") + show(t, None) for c, t in g}))[:80]
            shapes[(cv, int(need), vt[j], int(declared), int(j in mixed), shape)] += 1
    sec_inferred -= sec_loose

    # --- linear rows
    row_classes = {}
    n_lin_with_sec = 0
    for r in linear_rows:
        row = inst.rows[r + 1]
        lin = {j: a for j, a in row["lin"].items() if a != 0.0}
        sec_decl = [j for j in lin if j in sec_loose]
        sec = sec_decl + [j for j in lin if j in sec_inferred]
        if sec:
            n_lin_with_sec += 1
        if len(sec) < 2:
            continue
        rlb, rub = row["lb"], row["ub"]
        if not (finite(rlb) or finite(rub)):
            continue
        sense = "E" if rlb == rub else "R" if finite(rlb) and finite(rub) else "L" if finite(rub) else "G"
        if all(finite(lb[j]) and finite(ub[j]) for j in lin):
            bounded = "declared"
        elif all(finite(ilb[j]) and finite(iub[j]) for j in lin):
            bounded = "inferred"
        else:
            bounded = "no"
        rec = {"row": r, "sense": sense, "size": len(lin), "n_sec": len(sec_decl), "n_sec_inf": len(sec),
               "n_sec_strict": sum(j in sec_strict for j in sec),
               "n_sec_sep": sum(j in sec_sep for j in sec), "bounded": bounded,
               "n_int": sum(vt[j] != "C" for j in lin)}
        if bounded != "no":
            widths = [abs(a) * (iub[j] - ilb[j]) for j, a in lin.items()]
            base = sum(a * (ilb[j] if a > 0 else iub[j]) for j, a in lin.items())
            pos = [w for w in widths if w > TOL * max(1.0, max(widths))]
            rec["n_items"] = len(pos)
            rec["equal_widths"] = bool(pos) and max(pos) - min(pos) <= TOL * max(1.0, max(pos))
            secw = [abs(lin[j]) * (iub[j] - ilb[j]) for j in sec]
            rec["equal_secant_widths"] = max(secw) - min(secw) <= TOL * max(1.0, max(secw))
            W = sum(pos)
            if sense == "E":
                rec["degenerate"] = subset_sum_hits(pos, rlb - base) if pos else True
            else:
                # can the row be tight without forcing every variable to a bound?  0 < B < W
                tol = TOL * max(1.0, W)
                tight = []
                if finite(rub):
                    tight.append(tol < rub - base < W - tol)
                if finite(rlb):
                    tight.append(tol < rlb - base < W - tol)
                rec["can_be_tight"] = any(tight)
        first_row = rec.pop("row")
        key = json.dumps(rec, sort_keys=True)
        if key in row_classes:                       # identical rows are stored once, with a count
            row_classes[key]["count"] += 1
        else:
            row_classes[key] = {"first_row": first_row, "count": 1, **rec}
    rows_out = list(row_classes.values())

    return {"name": inst.name, "status": "ok", "nvars": nvars, "nrows": nrows,
            "n_linear_rows": len(linear_rows), "n_rows_linear_in_nl_tree": nl_only_linear,
            "n_linear_rows_with_secant_item": n_lin_with_sec,
            "term_counts": counts, "n_secant_vars": len(sec_loose), "n_secant_vars_inferred_bounds": len(sec_inferred),
            "n_secant_vars_strict": len(sec_strict), "n_secant_vars_separable": len(sec_sep),
            "n_secant_vars_binary_excluded": len(sec_binary),
            "rows": rows_out,
            "term_shapes": [[*k, n] for k, n in shapes.most_common(MAX_LISTED)], "terms_first": terms, "seconds": round(time.time() - t0, 2)}


# ---------------------------------------------------------------- driver
def worker(conn):
    sys.setrecursionlimit(100000)
    while True:
        path = conn.recv()
        if path is None:
            return
        name = os.path.basename(path)[:-5]
        try:
            conn.send(analyse(path))
        except NotImplementedError as e:
            conn.send({"name": name, "status": f"unsupported operator: {e}"})
        except Exception as e:                      # keep the scan going; the status is reported
            conn.send({"name": name, "status": f"error: {type(e).__name__}: {e}"[:300]})


def start():
    parent, child = mp.Pipe()
    p = mp.Process(target=worker, args=(child,), daemon=True)
    p.start()
    return p, parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("osil_dir")
    ap.add_argument("out")
    ap.add_argument("--timeout", type=float, default=300.0)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    files = sorted(glob.glob(os.path.join(args.osil_dir, "*.osil")))
    if args.only:
        files = [f for f in files if os.path.basename(f)[:-5] in set(args.only)]
    done = set()
    if os.path.exists(args.out):                    # resume
        done = {json.loads(line)["name"] for line in open(args.out)}
    proc, conn = start()
    with open(args.out, "a") as out:
        for k, f in enumerate(files):
            name = os.path.basename(f)[:-5]
            if name in done:
                continue
            conn.send(f)
            if conn.poll(args.timeout):
                try:
                    rec = conn.recv()
                except EOFError:
                    rec = {"name": name, "status": "worker died"}
                    proc, conn = start()
            else:
                proc.kill()
                proc.join()
                proc, conn = start()
                rec = {"name": name, "status": "timeout", "size_bytes": os.path.getsize(f)}
            out.write(json.dumps(rec) + "\n")
            out.flush()
            if rec["status"] != "ok" or rec.get("seconds", 0) > 30:
                print(k, name, rec["status"], rec.get("seconds"), flush=True)
    conn.send(None)


if __name__ == "__main__":
    main()
