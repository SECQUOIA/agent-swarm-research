"""Independent direct-OSiL checks for this frozen quadratic cohort.

This deliberately does not import the historical QCQP parser. It evaluates XML
terms directly, checks interchange semantics at deterministic probes, and can
check every public incumbent in a completed campaign. Numerical checks do not
certify exact feasibility or global optimality.
"""
from __future__ import annotations

import argparse
import gzip
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

import numpy as np

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent / "experiments"
sys.path.insert(0, str(EXPERIMENTS))
from models import read_problem


def tag(element):
    return element.tag.rsplit("}", 1)[-1]


def numbers(element, cast):
    result = []
    for item in element:
        base = cast(item.text)
        increment = cast(item.get("incr", "0"))
        result.extend(base + i * increment for i in range(int(item.get("mult", "1"))))
    return result


class DirectSource:
    def __init__(self, content):
        root = ET.fromstring(content)
        data = next(e for e in root if tag(e) == "instanceData")
        self.sections = {tag(e): e for e in data}
        assert "nonlinearExpressions" not in self.sections
        self.variables = list(self.sections["variables"])
        self.constraints = list(self.sections["constraints"])
        self.objective = list(self.sections["objectives"])[0]
        self.n = len(self.variables)
        self.m = len(self.constraints)
        assert all("mult" not in e.attrib for e in self.variables + self.constraints)
        self.lb = np.array([float(v.get("lb", "0")) for v in self.variables])
        self.ub = np.array([float(v.get("ub", "inf")) for v in self.variables])
        self.vtype = [v.get("type", "C") for v in self.variables]
        for i, typ in enumerate(self.vtype):
            if typ == "B":
                self.lb[i], self.ub[i] = max(0, self.lb[i]), min(1, self.ub[i])
        self.rlo = np.array([float(c.get("lb", "-inf")) for c in self.constraints])
        self.rhi = np.array([float(c.get("ub", "inf")) for c in self.constraints])
        self.constants = np.array([float(c.get("constant", "0")) for c in self.constraints])
        self.linear_terms = [[] for _ in self.constraints]
        section = self.sections.get("linearConstraintCoefficients")
        if section is not None:
            coeffs = {tag(e): e for e in section}
            start = numbers(coeffs["start"], int)
            values = numbers(coeffs["value"], float)
            byrow = "colIdx" in coeffs
            indices = numbers(coeffs["colIdx" if byrow else "rowIdx"], int)
            assert len(values) == len(indices) == start[-1]
            assert len(start) == (self.m if byrow else self.n) + 1
            for major in range(len(start) - 1):
                for k in range(start[major], start[major + 1]):
                    row, col = (major, indices[k]) if byrow else (indices[k], major)
                    self.linear_terms[row].append((col, values[k]))
        self.quadratic_terms = [[] for _ in range(self.m + 1)]
        section = self.sections.get("quadraticCoefficients")
        if section is not None:
            for q in section:
                row = int(q.get("idx"))
                assert -1 <= row < self.m
                self.quadratic_terms[row + 1].append((int(q.get("idxOne")),
                    int(q.get("idxTwo")), float(q.get("coef"))))
        self.sense = -1 if self.objective.get("maxOrMin", "min") == "max" else 1

    def evaluate(self, x):
        rows = []
        for r in range(self.m):
            terms = [self.constants[r]]
            terms.extend(q * x[i] for i, q in self.linear_terms[r])
            terms.extend(q * x[i] * x[j] for i, j, q in self.quadratic_terms[r + 1])
            rows.append(math.fsum(terms))
        exact = Fraction(float(self.objective.get("constant", "0")))
        exact += sum((Fraction(float(c.text)) * Fraction(float(x[int(c.get("idx"))]))
                      for c in self.objective), Fraction(0))
        exact += sum((Fraction(q) * Fraction(float(x[i])) * Fraction(float(x[j]))
                      for i, j, q in self.quadratic_terms[0]), Fraction(0))
        return float(self.sense * exact), np.array(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign")
    args = ap.parse_args()
    manifest = json.loads((EXPERIMENTS / "frozen/manifest.json").read_text())
    sources = {}
    for model in manifest["models"]:
        path = EXPERIMENTS / "frozen" / model["model"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == model["model_sha256"]
        if model["kind"] != "public":
            continue
        content = gzip.decompress((EXPERIMENTS / "frozen/osil" / (model["name"] + ".osil.gz")).read_bytes())
        assert hashlib.sha256(content).hexdigest() == model["source_sha256"]
        source = DirectSource(content)
        problem = read_problem(path)
        assert source.vtype == problem.vtype.tolist()
        assert [v.get("name") for v in source.variables] == problem.names
        np.testing.assert_array_equal(source.lb, problem.lb)
        np.testing.assert_array_equal(source.ub, problem.ub)
        np.testing.assert_array_equal(source.rlo - source.constants, problem.rlo)
        np.testing.assert_array_equal(source.rhi - source.constants, problem.rhi)
        rng = np.random.default_rng(20261004)
        # Probes need not be feasible: polynomial semantics hold everywhere.
        for x in (np.zeros(problem.n), np.ones(problem.n), -np.ones(problem.n),
                  rng.uniform(-3, 3, problem.n), rng.uniform(-100, 100, problem.n)):
            obj, rows = source.evaluate(x)
            np.testing.assert_allclose(problem.objective_exact_float(x), obj, rtol=1e-12, atol=1e-8)
            np.testing.assert_allclose(problem.rows(x) + source.constants, rows, rtol=1e-12, atol=1e-8)
        sources[model["name"]] = source, problem
    count = 0
    if args.campaign:
        campaign = EXPERIMENTS / "runs" / args.campaign
        config = json.loads((campaign / "campaign.json").read_text())
        for filename, digest in config["source_sha256"].items():
            assert hashlib.sha256((campaign / "source" / filename).read_bytes()).hexdigest() == digest
        for task in config["tasks"]:
            result = json.loads((campaign / "raw" / (task["key"] + ".json")).read_text())
            assert result["process_complete"]
            point = result.get("outcome", {}).get("solution")
            if task["name"] not in sources or point is None:
                continue
            source, problem = sources[task["name"]]
            x = np.array(point)
            obj, rows = source.evaluate(x)
            np.testing.assert_allclose(obj, problem.objective_exact_float(x), rtol=1e-12, atol=1e-7)
            np.testing.assert_allclose(rows, problem.rows(x) + source.constants, rtol=1e-12, atol=1e-7)
            count += 1
    print(json.dumps({"public_models_checked": len(sources), "probes_per_model": 5,
                      "public_incumbents_checked": count, "result": "passed"}, sort_keys=True))


if __name__ == "__main__":
    main()
