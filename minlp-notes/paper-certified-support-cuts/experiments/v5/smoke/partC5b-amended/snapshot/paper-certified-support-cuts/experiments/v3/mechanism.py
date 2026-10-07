"""Interleaved path family of mechanism-protocol.md, as exact case data.

The random draw for instance (n, seed) is, triple by triple (i = 1..n), with a
single ``random.Random(1000*n + seed)``:

    ks = rng.sample(range(49), 4)            # four distinct k in 0..48
    t1 < t2 < t3 < t4 = sorted(k/64)
    A, C = ({t1,t3}, {t2,t4}) if rng.random() < 0.5 else ({t2,t4}, {t1,t3})
    (a1, a2) = A in increasing order, reversed if rng.random() < 0.5
    (c1, c2) = C in increasing order, reversed if rng.random() < 0.5

Variables are ordered x_i, y_i, z_i, t_i for i = 1..n (index 4(i-1)+k).
Row 0 is the objective sum_i t_i; rows 1..n are D_i - t_i <= 0 with the
constant a1^2 + c1^2 of D_i moved to the right-hand side; row n+1 is
sum_i y_i <= 0.8 n. Every coefficient is dyadic and exact in binary64.
"""
from __future__ import annotations

from fractions import Fraction as Q
import math
import random

NS = (10, 20, 40, 80)
SEEDS = (0, 1, 2, 3, 4)


def draw_triples(n, seed):
    rng = random.Random(1000 * n + seed)
    triples = []
    for _ in range(n):
        t1, t2, t3, t4 = sorted(Q(k, 64) for k in rng.sample(range(49), 4))
        a, c = ([t1, t3], [t2, t4]) if rng.random() < 0.5 else ([t2, t4], [t1, t3])
        if rng.random() < 0.5:
            a.reverse()
        if rng.random() < 0.5:
            c.reverse()
        triples.append((tuple(a), tuple(c)))
    return triples


def expand(a, c):
    """Exact coefficients of D in (x, y, z): linear, quadratic and constant."""
    (a1, a2), (c1, c2) = a, c
    p, q = a2 - a1, c2 - c1
    linear = {"x": 2 * a1 * p + 1, "y": -2 * (a1 + c1), "z": 2 * c1 * q + 1}
    quadratic = {("x", "x"): p * p - 1, ("y", "y"): Q(2), ("z", "z"): q * q - 1,
                 ("x", "y"): -2 * p, ("y", "z"): -2 * q}
    return linear, quadratic, a1 * a1 + c1 * c1


def evaluate(a, c, x, y, z):
    (a1, a2), (c1, c2) = a, c
    return ((y - a1 - (a2 - a1) * x) ** 2 + (y - c1 - (c2 - c1) * z) ** 2
            + x * (1 - x) + z * (1 - z))


def closest_pair(a, c):
    """Minimizing (s, t) in A x C and the vertex (x, z) that selects it."""
    s, t = min(((s, t) for s in a for t in c), key=lambda st: (abs(st[0] - st[1]), st))
    return s, t, (0 if s == a[0] else 1), (0 if t == c[0] else 1)


def binary64(value):
    result = float(value)
    if Q(result) != value:
        raise ValueError(f"{value} is not exactly representable in binary64")
    return result


def instance(n, seed):
    """Return (Instance dict, exact optimum, exact witness, triple records)."""
    triples = draw_triples(n, seed)
    index = {"x": 0, "y": 1, "z": 2, "t": 3}
    rows = [{"nl": None, "lin": {4 * i + 3: 1.0 for i in range(n)}, "quad": [],
             "lb": -math.inf, "ub": math.inf}]
    optimum, witness, records = Q(0), [], []
    for i, (a, c) in enumerate(triples):
        linear, quadratic, constant = expand(a, c)
        lin = {4 * i + index[v]: binary64(k) for v, k in linear.items() if k}
        lin[4 * i + 3] = -1.0
        quad = [(4 * i + index[u], 4 * i + index[v], binary64(k))
                for (u, v), k in quadratic.items() if k]
        rows.append({"nl": None, "lin": dict(sorted(lin.items())), "quad": quad,
                     "lb": -math.inf, "ub": binary64(-constant)})
        s, t, x, z = closest_pair(a, c)
        delta = abs(s - t)
        value = delta * delta / 2
        y = (s + t) / 2
        if evaluate(a, c, Q(x), y, Q(z)) != value or not 0 <= y <= Q(3, 4):
            raise AssertionError("witness does not attain delta^2/2")
        optimum += value
        witness += [Q(x), y, Q(z), value]
        records.append({"a": [str(v) for v in a], "c": [str(v) for v in c],
                        "delta": str(delta), "witness_pair": [str(s), str(t)]})
    rows.append({"nl": None, "lin": {4 * i + 1: 1.0 for i in range(n)}, "quad": [],
                 "lb": -math.inf, "ub": binary64(Q(4 * n, 5))})
    names = [f"{v}_{i + 1}" for i in range(n) for v in "xyzt"]
    model = {"name": case_name(n, seed), "var_lb": [0.0, 0.0, 0.0, -10.0] * n,
             "var_ub": [1.0, 1.0, 1.0, 10.0] * n, "var_type": ["C"] * (4 * n),
             "obj_sense": "min", "obj_const": 0.0, "rows": rows, "var_names": names}
    if sum(witness[4 * i + 1] for i in range(n)) > Q(4 * n, 5):
        raise AssertionError("witness violates the coupling row")
    return model, optimum, witness, records


def case_name(n, seed):
    return f"interleaved_path_n{n}_s{seed}"


def case(n, seed, exact_json):
    """Case descriptor in the campaign-v2 synthetic format (see worker.load_model)."""
    model, optimum, witness, records = instance(n, seed)
    return {"name": model["name"], "suite": "mechanism",
            "stratum": "interleaved path family (mechanism-protocol.md)",
            "known_optimum": binary64(optimum), "known_optimum_exact": str(optimum),
            "known_witness": [binary64(v) for v in witness],
            "known_witness_exact": [str(v) for v in witness],
            "mechanism": {"n": n, "seed": seed, "rng": f"random.Random({1000 * n + seed})",
                          "triples": records},
            "model": exact_json(model)}
