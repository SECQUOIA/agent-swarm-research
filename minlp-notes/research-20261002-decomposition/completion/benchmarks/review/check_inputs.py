"""Independent whole-polynomial comparison with retained QPLIB GAMS files."""
from collections import defaultdict
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
BENCHMARKS = HERE.parent
sys.path.insert(0, str(BENCHMARKS))
from corpus import cases


def check():
    models = cases()
    results = {}
    token = re.compile(r"([+-]?)(?:(\d+(?:\.\d+)?)\*)?(b\d+)(?:\*(b\d+))?")
    for code in ("3852", "5881"):
        folder = BENCHMARKS / "frozen" / "baseline" / "data"
        path = folder / f"QPLIB_{code}.gms"
        text = path.read_text()
        equation = re.search(r"e1\.\.(.*?)=E=\s*0\s*;", text, re.S).group(1)
        equation = re.sub(r"\s+", "", equation)
        assert equation.endswith("-objvar")
        equation = equation[:-len("-objvar")]
        coefficients = defaultdict(F)
        consumed = 0
        for term in token.finditer(equation):
            assert term.start() == consumed, equation[consumed:term.start()]
            sign, number, a, b = term.groups()
            coefficient = F(number or 1) * (-1 if sign == "-" else 1)
            indices = tuple(sorted(int(v[1:]) - 2 for v in (a, b) if v))
            coefficients[indices] += coefficient
            consumed = term.end()
        assert consumed == len(equation)
        model = models[f"QPLIB_{code}"]
        n = len(model.b)
        assert model.c == 0 and model.integers == set(range(n))
        assert model.bounds == [(F(0), F(1))] * n
        assert all(0 <= i < n for key in coefficients for i in key)
        for i in range(n):
            assert model.b[i] == -coefficients[(i,)]
            assert model.A[i][i] / 2 == -coefficients[(i, i)]
            for j in range(i):
                assert model.A[i][j] == model.A[j][i] == -coefficients[(j, i)]
        original = BENCHMARKS.parents[1] / "solver" / "extra-benchmarks" / "data"
        hashes = {}
        for extension in ("qplib", "gms", "sol"):
            file = folder / f"QPLIB_{code}.{extension}"
            assert file.read_bytes() == (original / file.name).read_bytes()
            hashes[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()
        results[model.name] = {"variables": n,
                              "quadratic_nonzero_terms": sum(bool(model.A[i][j]) for i in range(n) for j in range(i + 1)),
                              "gams_all_coefficients_match": True,
                              "archived_files_unchanged": True,
                              "sha256": hashes}
    audit = json.loads((BENCHMARKS / "data" / "continuous_input_audit.json").read_text())
    csvpath = BENCHMARKS / "data" / "instancedata.csv"
    assert hashlib.sha256(csvpath.read_bytes()).hexdigest() == audit["csv_sha256"]
    with csvpath.open() as stream:
        inputs = [row for row in csv.DictReader(stream)
                  if row["probtype"][0] in "QC" and row["probtype"][1:] == "CB"]
    assert set(row["name"] for row in inputs) == set(row["name"] for row in audit["continuous_bound_only_inputs"])
    results["metadata_screen"] = {"matching_rows": len(inputs), "csv_hash_matches": True}
    return results


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
