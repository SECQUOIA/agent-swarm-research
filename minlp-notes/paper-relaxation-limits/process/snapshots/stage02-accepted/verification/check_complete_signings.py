"""Exhaustive K_2,...,K_7 center optima using exact Python integers.

Run with Python 3.10+: python verification/check_complete_signings.py
No external packages or optimization solvers are required. The output includes
one center witness for every size and an explicit worst-face witness for K_7.
Switching makes all edges incident to vertex 0 positive. The remaining negative
edge masks enumerate every switching class exactly once; cuts fix vertex 0 on
side zero. Integer cut ranges determine the ratios without rounding.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def enumerate_center(n):
    edges = list(combinations(range(n), 2))
    free = [(i, j) for i, j in edges if i != 0]
    cuts = []
    for side in range(1 << (n - 1)):
        side <<= 1
        crosses = lambda i, j: ((side >> i) ^ (side >> j)) & 1
        size = sum(crosses(i, j) for i, j in edges)
        mask = sum(crosses(i, j) << k for k, (i, j) in enumerate(free))
        cuts.append((size, mask))
    best, witness = len(edges) + 1, None
    histogram = Counter()
    for negative in range(1 << len(free)):
        values = [size - 2 * (negative & mask).bit_count()
                  for size, mask in cuts]
        width = max(values) - min(values)
        histogram[width] += 1
        if width < best:
            best, witness = width, negative
    negative_edges = [edge for k, edge in enumerate(free) if (witness >> k) & 1]
    return {
        "n": n,
        "switching_representatives": 1 << len(free),
        "cut_representatives": len(cuts),
        "min_cut_range": best,
        "max_center_ratio": str(Fraction(len(edges), best)),
        "negative_edges": negative_edges,
        "cut_range_histogram": dict(sorted(histogram.items())),
    }


def direct_witness(n, negative_edges):
    """Independent scalar evaluation of Q, also on every induced face."""
    edges = list(combinations(range(n), 2))
    negative = {tuple(edge) for edge in negative_edges}
    assert negative <= set(edges)
    face_best, face_witness = Fraction(0), None
    center = None
    for face in range(1 << n):
        vertices = [i for i in range(n) if (face >> i) & 1]
        if len(vertices) < 2:
            continue
        local = list(combinations(vertices, 2))
        values = [sum((-1 if (i, j) in negative else 1)
                      * (-1 if ((signs >> i) ^ (signs >> j)) & 1 else 1)
                      for i, j in local)
                  for signs in range(1 << n) if signs & ~face == 0]
        ratio = Fraction(2 * len(local), max(values) - min(values))
        if face == (1 << n) - 1:
            center = {"min_Q": min(values), "max_Q": max(values),
                      "ratio": str(ratio)}
        if ratio > face_best:
            face_best, face_witness = ratio, vertices
    return {"center": center, "max_face_ratio": str(face_best),
            "maximizing_face": face_witness}


def main():
    expected_ranges = [1, 2, 4, 4, 5, 8]
    expected_faces = ["1", "3/2", "3/2", "5/2", "3", "3"]
    rows = []
    face_best = Fraction(0)
    for n, expected_range, expected_face in zip(range(2, 8), expected_ranges, expected_faces):
        row = enumerate_center(n)
        assert row["min_cut_range"] == expected_range
        assert sum(row["cut_range_histogram"].values()) == row["switching_representatives"]
        witness = direct_witness(n, row["negative_edges"])
        assert witness["center"]["ratio"] == row["max_center_ratio"]
        face_best = max(face_best, Fraction(row["max_center_ratio"]))
        row["max_full_signing_face_ratio"] = str(face_best)
        assert str(face_best) == expected_face
        assert Fraction(witness["max_face_ratio"]) <= face_best
        row["witness_check"] = witness
        rows.append(row)
    # Add vertex 6 to the K_6 witness with all new incident edges positive.
    extended = {"n": 7, "negative_edges": rows[-2]["negative_edges"]}
    extended.update(direct_witness(7, extended["negative_edges"]))
    assert extended["max_face_ratio"] == "3"
    assert extended["maximizing_face"] == list(range(6))
    report = {"arithmetic": "Exact unbounded Python integers and Fraction",
              "rows": rows, "extended_K6_face_witness": extended}
    output = Path(__file__).with_name("complete_signings.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
