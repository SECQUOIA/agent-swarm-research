"""Small, auditable QCQP interchange and deterministic synthetic models.

All objectives remain in their original sense. No reference optimum or solution
is stored in the interchange format or passed to the solver.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import sparse


class Problem:
    def __init__(self, data):
        self.name = data["name"]
        self.n = len(data["lb"])
        self.m = len(data["rlo"])
        self.names = data["names"]
        self.vtype = np.asarray(data["vtype"])
        self.isint = np.isin(self.vtype, ["B", "I"])
        for attr in ("lb", "ub", "c", "rlo", "rhi"):
            setattr(self, attr, np.asarray(data[attr], dtype=float))
        self.c0 = data["c0"]
        self.sense = data["sense"]
        a = data["A"]
        self.A = sparse.coo_matrix((a["value"], (a["row"], a["col"])),
                                   shape=(self.m, self.n)).tocsr()
        self.oq = {(i, j): q for i, j, q in data["oq"]}
        self.rq = {int(r): {(i, j): q for i, j, q in terms}
                   for r, terms in data["rq"].items()}
        terms = set(self.oq)
        for d in self.rq.values():
            terms.update(d)
        self.terms = sorted(terms)
        self.nlvars = sorted({i for t in terms for i in t})

    def fmin(self, x):
        x = np.asarray(x)
        return float(self.sense * (self.c0 + self.c @ x +
                     sum(q * x[i] * x[j] for (i, j), q in self.oq.items())))

    def rows(self, x):
        x = np.asarray(x)
        values = self.A @ x
        for r, terms in self.rq.items():
            values[r] += sum(q * x[i] * x[j] for (i, j), q in terms.items())
        return values

    def validation(self, x):
        """Original rows/bounds/integrality, with absolute and scaled residuals."""
        x = np.asarray(x, dtype=float)
        if x.shape != (self.n,) or not np.all(np.isfinite(x)):
            return {"valid": False, "reason": "nonfinite or wrong-size incumbent"}
        rows = self.rows(x)
        row_viol = np.maximum(np.maximum(self.rlo - rows, rows - self.rhi), 0)
        bound_viol = np.maximum(np.maximum(self.lb - x, x - self.ub), 0)
        row_scale = 1 + abs(self.A) @ np.abs(x)
        for r, terms in self.rq.items():
            row_scale[r] += sum(abs(q * x[i] * x[j]) for (i, j), q in terms.items())
        finite_lo = np.where(np.isfinite(self.rlo), np.abs(self.rlo), 0)
        finite_hi = np.where(np.isfinite(self.rhi), np.abs(self.rhi), 0)
        row_scale = np.maximum(row_scale, np.maximum(finite_lo, finite_hi))
        integ = float(np.max(np.abs(x[self.isint] - np.rint(x[self.isint])), initial=0))
        absolute = max(float(np.max(row_viol, initial=0)),
                       float(np.max(bound_viol, initial=0)), integ)
        scaled = max(float(np.max(row_viol / row_scale, initial=0)),
                     float(np.max(bound_viol / (1 + np.abs(x)), initial=0)), integ)
        return {"valid": bool(scaled <= 1e-6), "max_absolute": absolute,
                "max_scaled": scaled, "integrality": integ,
                "objective_min": self.fmin(x), "tolerance": 1e-6}

    def violation(self, x):
        return self.validation(x).get("max_absolute", math.inf)


def as_data(p):
    a = p.A.tocoo()
    def numbers(values):
        return [float(x) if np.isfinite(x) else ("inf" if x > 0 else "-inf")
                for x in values]
    return {"name": p.name, "names": list(p.names), "vtype": list(p.vtype),
            "lb": numbers(p.lb), "ub": numbers(p.ub), "c": numbers(p.c),
            "c0": float(p.c0), "sense": int(p.sense),
            "rlo": numbers(p.rlo), "rhi": numbers(p.rhi),
            "A": {"row": a.row.tolist(), "col": a.col.tolist(), "value": a.data.tolist()},
            "oq": [[i, j, float(q)] for (i, j), q in sorted(p.oq.items())],
            "rq": {str(r): [[i, j, float(q)] for (i, j), q in sorted(terms.items())]
                   for r, terms in sorted(p.rq.items())}}


def write_problem(p, path):
    Path(path).write_text(json.dumps(as_data(p), sort_keys=True, indent=2) + "\n")


def read_problem(path):
    return Problem(json.loads(Path(path).read_text()))


def synthetic(family, size, seed):
    rng = np.random.default_rng(seed)
    rows, rlo, rhi, rq, oq = [], [], [], {}, {}
    n = size
    if family == "packing":
        n = 2 * size + 1
        lb, ub, c = np.zeros(n), np.ones(n), np.zeros(n)
        ub[-1], c[-1] = 2, -1
        for i in range(size):
            for j in range(i + 1, size):
                r = len(rows)
                rows.append({n - 1: 1})
                rlo.append(-math.inf)
                rhi.append(0)
                rq[r] = {(i, i): -1, (j, j): -1, (i, j): 2,
                         (size+i, size+i): -1, (size+j, size+j): -1,
                         (size+i, size+j): 2}
    elif family == "coupled_squares":
        lb, ub, c = -np.ones(n), np.ones(n), rng.uniform(-.2, .2, n)
        oq = {(i, i): float(rng.uniform(-1.5, -.5)) for i in range(n)}
        for i in range(n):
            j = (i+1) % n
            oq[tuple(sorted((i, j)))] = float(rng.uniform(-1, 1))
        for offset in (0, 1):
            r = len(rows)
            rows.append({})
            rlo.append(-math.inf)
            rhi.append(.3 * (n // 2))
            rq[r] = {(i, i): 1 for i in range(offset, n, 2)}
        rows.append({i: 1 for i in range(n)})
        rlo.append(-.25)
        rhi.append(.25)
    elif family == "bilinear_cycle":
        n = 2 * size
        lb, ub, c = np.zeros(n), np.ones(n), np.zeros(n)
        c[:size] = rng.uniform(-.6, .6, size)
        c[size:] = rng.uniform(-1.5, -.5, size)
        for i in range(size):
            j = (i + 1) % size
            r = len(rows)
            rows.append({size+i: 1})
            rlo.append(0)
            rhi.append(0)
            rq[r] = {tuple(sorted((i, j))): -1}
        rows.append({i: 1 for i in range(size)})
        rlo.append(.35 * size)
        rhi.append(.45 * size)
    elif family == "indefinite_qp":
        lb, ub, c = np.zeros(n), np.ones(n), rng.uniform(-.2, .2, n)
        for i in range(n):
            oq[i, i] = float(rng.uniform(-1, 1))
            for j in range(i + 1, n):
                if rng.random() < .2:
                    oq[i, j] = float(rng.uniform(-2, 2))
        for _ in range(max(2, n // 4)):
            a = rng.uniform(.25, 1, n)
            rows.append(dict(enumerate(a.tolist())))
            rlo.append(.3 * float(sum(a)))
            rhi.append(.6 * float(sum(a)))
    else:
        raise ValueError(family)
    ai, aj, av = [], [], []
    for r, row in enumerate(rows):
        for j, v in row.items():
            ai.append(r)
            aj.append(j)
            av.append(v)
    data = {"name": f"synthetic_{family}_{size}_{seed}",
            "names": [f"x{i}" for i in range(n)], "vtype": ["C"] * n,
            "lb": lb.tolist(), "ub": ub.tolist(), "c": c.tolist(), "c0": 0,
            "sense": 1, "rlo": rlo, "rhi": rhi,
            "A": {"row": ai, "col": aj, "value": av},
            "oq": [[i, j, q] for (i, j), q in oq.items()],
            "rq": {str(r): [[i, j, q] for (i, j), q in terms.items()]
                   for r, terms in rq.items()}}
    return Problem(data)
