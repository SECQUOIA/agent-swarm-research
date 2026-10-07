#!/usr/bin/env python3
"""Independent check (reviewer code) that each campaign .gms file encodes the
same model as the cached MINLPLib OSIL file.

For each instance, GAMS 54.3 CONVERT wrote osil.xml from the .gms file used by
the campaign (see conv.sh). This script parses both OSIL files with its own
parser and compares:
  * variables: names, order, types, bounds (exact float equality);
  * constraints: names, order, bounds, constants (exact);
  * objective: sense, constant;
  * linear coefficient maps (exact, informative only);
  * every row function and the objective function (linear + quadratic +
    nonlinear tree), evaluated in float64 at K random points within the
    variable bounds; agreement required to 1e-9 * (1 + |a| + |b|).
Floating-point evaluation is evidence of equality of the models, not a proof.

usage: python3 osil_compare.py CONVDIR [names...]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import math
import os
import sys
import xml.etree.ElementTree as ET

import numpy as np

sys.setrecursionlimit(100000)
CACHE = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
K = 4
RNG = np.random.default_rng(20261002)


def fl(s, default):
    if s is None:
        return default
    s = s.strip()
    if s in ("INF", "Infinity", "inf"):
        return math.inf
    if s in ("-INF", "-Infinity", "-inf"):
        return -math.inf
    return float(s)


def tagof(e):
    return e.tag.rsplit("}", 1)[-1]


def expand_ints(el):
    mult = int(el.get("mult", "1"))
    v = int(el.text.strip())
    inc = int(el.get("incr", "0"))
    return [v + k * inc for k in range(mult)]


def expand_floats(el):
    mult = int(el.get("mult", "1"))
    v = float(el.text.strip())
    inc = float(el.get("incr", "0"))
    return [v + k * inc for k in range(mult)]


def to_tree(e):
    t = tagof(e)
    if t == "number":
        return ("num", float(e.get("value", "0")))
    if t == "variable":
        kids = list(e)
        node = ("var", int(e.get("idx")), float(e.get("coef", "1")))
        if kids:
            raise ValueError("variable with child expression not supported")
        return node
    return (t, [to_tree(c) for c in e])


def parse(path):
    root = ET.parse(path).getroot()
    m = {"vars": [], "cons": [], "obj": None, "lin": {}, "quad": [], "nl": {}}
    for e in root.iter():
        t = tagof(e)
        if t == "var":
            for _ in range(int(e.get("mult", "1"))):
                m["vars"].append((e.get("name"), e.get("type", "C"), fl(e.get("lb"), 0.0), fl(e.get("ub"), math.inf)))
        elif t == "obj":
            coefs = {}
            for c in e:
                if tagof(c) == "coef":
                    coefs[int(c.get("idx"))] = coefs.get(int(c.get("idx")), 0.0) + float(c.text)
            m["obj"] = (e.get("maxOrMin", "min"), float(e.get("constant", "0")), coefs)
        elif t == "con":
            for _ in range(int(e.get("mult", "1"))):
                m["cons"].append((e.get("name"), fl(e.get("lb"), -math.inf), fl(e.get("ub"), math.inf),
                                  float(e.get("constant", "0"))))
        elif t == "linearConstraintCoefficients":
            starts, idx, val, major = [], [], [], None
            for c in e:
                ct = tagof(c)
                if ct == "start":
                    for el in c:
                        starts += expand_ints(el)
                elif ct in ("rowIdx", "colIdx"):
                    major = "col" if ct == "rowIdx" else "row"
                    for el in c:
                        idx += expand_ints(el)
                elif ct == "value":
                    for el in c:
                        val += expand_floats(el)
            for a in range(len(starts) - 1):
                for k in range(starts[a], starts[a + 1]):
                    key = (a, idx[k]) if major == "row" else (idx[k], a)
                    m["lin"][key] = m["lin"].get(key, 0.0) + val[k]
        elif t == "qTerm":
            m["quad"].append((int(e.get("idx")), int(e.get("idxOne")), int(e.get("idxTwo")), float(e.get("coef", "1"))))
        elif t == "nl":
            kids = list(e)
            assert len(kids) == 1, "nl with != 1 child"
            r = int(e.get("idx"))
            m["nl"].setdefault(r, []).append(to_tree(kids[0]))
    return m


def ev(node, X):
    t = node[0]
    if t == "num":
        return np.full(X.shape[1], node[1])
    if t == "var":
        return node[2] * X[node[1]]
    a = [ev(c, X) for c in node[1]]
    if t == "sum":
        return np.sum(a, axis=0) if a else np.zeros(X.shape[1])
    if t == "product":
        return np.prod(a, axis=0) if a else np.ones(X.shape[1])
    if t == "plus":
        return a[0] + a[1]
    if t == "minus":
        return a[0] - a[1]
    if t == "times":
        return a[0] * a[1]
    if t == "divide":
        return a[0] / a[1]
    if t == "power":
        return np.power(a[0], a[1])
    if t == "negate":
        return -a[0]
    if t == "square":
        return a[0] * a[0]
    if t == "sqrt":
        return np.sqrt(a[0])
    if t == "ln":
        return np.log(a[0])
    if t == "exp":
        return np.exp(a[0])
    if t == "sin":
        return np.sin(a[0])
    if t == "cos":
        return np.cos(a[0])
    if t == "tanh":
        return np.tanh(a[0])
    if t == "abs":
        return np.abs(a[0])
    raise ValueError(f"operator {t} not implemented")


def sample(vars_):
    X = np.empty((len(vars_), K))
    for j, (_, typ, lb, ub) in enumerate(vars_):
        lo, hi = max(lb, -5.0), min(ub, 5.0)
        if lo > hi:
            lo, hi = (lb, min(ub, lb + 5.0)) if lb > 5.0 else (max(lb, ub - 5.0), ub)
        if typ in ("B", "I"):
            X[j] = RNG.integers(math.ceil(lo), math.floor(hi) + 1, size=K)
        else:
            X[j] = RNG.uniform(lo, hi, size=K)
    return X


def row_values(m, X):
    """Value of every constraint body (rows 0..m-1) and of the objective (key -1)."""
    nrow = len(m["cons"])
    V = np.zeros((nrow + 1, X.shape[1]))  # last slot = objective
    for (r, c), v in m["lin"].items():
        V[r] += v * X[c]
    for r, i, j, c in m["quad"]:
        V[r if r >= 0 else nrow] += c * X[i] * X[j]
    for r, trees in m["nl"].items():
        for tr in trees:
            V[r if r >= 0 else nrow] += ev(tr, X)
    for r, con in enumerate(m["cons"]):
        V[r] += con[3]
    sense, const, coefs = m["obj"]
    V[nrow] += const
    for c, v in coefs.items():
        V[nrow] += v * X[c]
    return V


def compare(name, gen_path):
    a = parse(os.path.join(CACHE, name + ".osil"))
    b = parse(gen_path)
    out = []
    if [v[0] for v in a["vars"]] != [v[0] for v in b["vars"]]:
        out.append(f"variable names/order differ ({len(a['vars'])} vs {len(b['vars'])})")
        return out, None
    if [v[1:] for v in a["vars"]] != [v[1:] for v in b["vars"]]:
        d = [v[0] for v, w in zip(a["vars"], b["vars"]) if v[1:] != w[1:]]
        out.append(f"variable type/bounds differ for {len(d)} vars, e.g. {d[:5]}")
    if [c[0] for c in a["cons"]] != [c[0] for c in b["cons"]]:
        out.append(f"constraint names/order differ ({len(a['cons'])} vs {len(b['cons'])})")
        return out, None
    if [c[1:] for c in a["cons"]] != [c[1:] for c in b["cons"]]:
        d = [c[0] for c, e in zip(a["cons"], b["cons"]) if c[1:] != e[1:]]
        out.append(f"constraint bounds/constants differ for {len(d)} rows, e.g. {d[:5]}")
    if a["obj"][0] != b["obj"][0]:
        out.append(f"objective sense differs {a['obj'][0]} vs {b['obj'][0]}")
    lin_equal = ({k: v for k, v in a["lin"].items() if v != 0.0} == {k: v for k, v in b["lin"].items() if v != 0.0})
    X = sample(a["vars"])
    with np.errstate(all="ignore"):
        Va, Vb = row_values(a, X), row_values(b, X)
    nan_a, nan_b = ~np.isfinite(Va), ~np.isfinite(Vb)
    bad_nan = int(np.sum(nan_a != nan_b))
    both = np.isfinite(Va) & np.isfinite(Vb)
    err = np.abs(Va - Vb)
    tol = 1e-9 * (1 + np.abs(Va) + np.abs(Vb))
    bad = int(np.sum(both & (err > tol)))
    worst = float(np.max(np.where(both, err / (1 + np.abs(Va) + np.abs(Vb)), 0.0)))
    nonfinite = int(np.sum(nan_a & nan_b))
    if bad or bad_nan:
        rows = sorted(set(np.nonzero((both & (err > tol)) | (nan_a != nan_b))[0].tolist()))
        names = [a["cons"][r][0] if r < len(a["cons"]) else "objective" for r in rows[:5]]
        out.append(f"function values differ: {bad} finite mismatches, {bad_nan} finite/nonfinite mismatches; rows {names}")
    info = {"n": len(a["vars"]), "m": len(a["cons"]), "lin_maps_equal": lin_equal, "worst_scaled_err": worst,
            "nonfinite_both": nonfinite, "evals": int(Va.size)}
    return out, info


def main():
    conv = sys.argv[1]
    names = sys.argv[2:] or open(
        (_PUBLIC_REPO + '/research-20260929/publication/solver-runs/instances.txt')).read().split()
    nbad = 0
    for n in names:
        try:
            out, info = compare(n, os.path.join(conv, n, "osil.xml"))
        except Exception as e:  # report and continue
            out, info = [f"ERROR {e!r}"], None
        nbad += bool(out)
        print(f"{n:18s} {'OK ' if not out else 'BAD'} {info} {'; '.join(out)}", flush=True)
    print(f"{len(names)} instances, {nbad} with differences")


if __name__ == "__main__":
    main()
