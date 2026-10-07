#!/usr/bin/env python3
"""Read-only hash, schema, grouping, and arithmetic checks. Never invokes solvers."""
import collections
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE / "archive/research-20260928b/bb-complexity"
REJECT = {"nodelimit", "timelimit", "error"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(relative, fields, key):
    path = BASE / relative
    rows = []
    seen = set()
    for n, line in enumerate(path.read_text().splitlines(), 1):
        r = json.loads(line)
        require(isinstance(r, dict) and set(fields) <= set(r), f"schema: {relative}:{n}")
        identity = tuple(r.get(k) for k in key)
        require(identity not in seen, f"duplicate: {relative}:{n}: {identity}")
        seen.add(identity)
        if "nodes" in r:
            require(isinstance(r["nodes"], int) and r["nodes"] >= 0, f"nodes: {relative}:{n}")
        rows.append(r)
    return rows


def slope(rows, logy=True):
    if len(rows) < 3:
        return None
    x = [math.log10(1 / r["eps"]) for r in rows]
    if max(x) - min(x) < 0.99:
        return None
    y = [math.log10(r["nodes"]) if logy else float(r["nodes"]) for r in rows]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)


def fits(rows):
    grouped = collections.defaultdict(list)
    for r in rows:
        grouped[(r["inst"], r["setting"])].append(r)
    out = {}
    for (inst, setting), group in sorted(grouped.items()):
        group.sort(key=lambda r: r["eps"], reverse=True)
        good = [r for r in group if r["status"] not in REJECT]
        tail = [r for r in good if r["eps"] <= 1e-3 * 1.0001][-5:]
        wide = [r for r in good if r["eps"] <= 1e-2 * 1.0001]
        out[f"{inst}|{setting}"] = dict(tail=slope(tail), wide=slope(wide),
            nodes_per_decade=slope(tail, False),
            tail_window=[tail[0]["eps"], tail[-1]["eps"]] if tail else None)
    archived = json.loads((BASE / "solver-validation/results/runs_fits.json").read_text())
    require(set(archived) == set(out), "fit groups differ")
    for key, actual in out.items():
        for field, value in actual.items():
            expected = archived[key][field]
            if isinstance(value, float):
                require(math.isclose(value, expected, rel_tol=1e-10, abs_tol=1e-8), f"fit mismatch {key}.{field}")
            else:
                require(value == expected, f"fit mismatch {key}.{field}")
    return out


def inventory(rows):
    return dict(records=len(rows), instances=len({r["inst"] for r in rows}),
                statuses=dict(sorted(collections.Counter(r["status"] for r in rows).items())))


def node_ratios(rows, pairs, strict):
    grouped = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in rows:
        grouped[r["inst"]][r["setting"]][r["seed"]] = r
    result = {}
    for setting, baseline, expected_n, rounded_ratio in pairs:
        logs = []
        for inst in sorted(grouped):
            a, b = grouped[inst][setting], grouped[inst][baseline]
            require(set(a) == set(b) == {0, 1, 2}, f"seed completeness: {inst}/{setting}")
            if strict and any("nodes" not in r for r in list(a.values()) + list(b.values())):
                continue
            # First study retains the available node counts within a seed list;
            # robust study discards the paired instance if any seed lacks nodes.
            va = [r["nodes"] + 10 for r in a.values() if "nodes" in r]
            vb = [r["nodes"] + 10 for r in b.values() if "nodes" in r]
            logs.append(sum(map(math.log, va)) / len(va) - sum(map(math.log, vb)) / len(vb))
        ratio = math.exp(sum(logs) / len(logs))
        require(len(logs) == expected_n and f"{ratio:.3f}" == rounded_ratio,
                f"aggregate differs: {setting}/{baseline}: {len(logs)}, {ratio}")
        result[f"{setting}/{baseline}"] = dict(instances=len(logs), shifted_node_ratio=ratio)
    return result


def main():
    # The manifest intentionally excludes itself, avoiding a recursive hash.
    entries = (HERE / "SHA256SUMS").read_text().splitlines()
    listed = {line.split("  ", 1)[1] for line in entries}
    actual = {str(path.relative_to(HERE)) for path in HERE.rglob("*")
              if path.is_file() and path.name != "SHA256SUMS"}
    require(listed == actual, "manifest coverage differs from package contents")
    for line in entries:
        expected, name = line.split("  ", 1)
        path = HERE / name
        require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected,
                f"hash mismatch: {name}")
    source_inventory = json.loads((HERE / "SOURCE-INVENTORY.json").read_text())
    for item in source_inventory:
        path = HERE / item["copied_path"]
        require(path.stat().st_size == item["bytes"] and
                hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"],
                f"source copy mismatch: {item['original_path']}")
    solver = load("solver-validation/results/runs.jsonl", ("inst", "setting", "eps", "status", "nodes"),
                  ("inst", "setting", "eps"))
    require(len(solver) == 2134 and all(r["eps"] > 0 for r in solver), "solver inventory")
    computed_fits = fits(solver)
    bounds = json.loads((BASE / "solver-validation/results/thm_bounds.json").read_text())
    leaf_ratios = {}
    for inst, values in bounds.items():
        ratios = [(r.get("nodes_left", 0) + r.get("leaves_processed", 0)) / values[repr(r["eps"])]
                  for r in solver if r["inst"] == inst and r["setting"] == "model"
                  and r["status"] not in REJECT and repr(r["eps"]) in values]
        if ratios:
            leaf_ratios[inst] = dict(minimum=min(ratios), maximum=max(ratios), records=len(ratios))
    require(f"{leaf_ratios['qflat2a']['minimum']:.2f}" == "6.76" and
            f"{leaf_ratios['qflat2a']['maximum']:.2f}" == "9.41", "qflat2a leaf ratio")
    figure = json.loads((HERE / "presentation/figure-metadata.json").read_text())
    require(figure["source_sha256"] == hashlib.sha256(
        (BASE / "solver-validation/results/runs.jsonl").read_bytes()).hexdigest(), "figure source hash")
    displayed = 0
    for panel in figure["panels"]:
        for curve in panel["curves"]:
            expected = [r for r in solver if r["inst"] == curve["instance"] and
                        r["setting"] == curve["setting"] and r["status"] != "error"]
            require(len(expected) == len(curve["records"]), "figure record completeness")
            for record in curve["records"]:
                source = solver[record["source_line"] - 1]
                require(source["inst"] == curve["instance"] and source["setting"] == curve["setting"]
                        and all(record[key] == source[key] for key in ("eps", "nodes", "status")),
                        "figure grouping or record mismatch")
                displayed += 1
    first = load("minlplib-branching/results/runs.jsonl", ("inst", "setting", "seed", "status"),
                 ("inst", "setting", "seed"))
    core = [r for r in first if r["setting"] in {"default", "lp", "lp_noclamp", "mix_noclamp", "mid"}]
    optional = [r for r in first if r["setting"] in {"trig0", "couenne", "lp_c05"}]
    tolerance = [r for r in first if "@abs" in r["setting"]]
    require((len(first), len(core), len(optional), len(tolerance)) == (1254, 855, 171, 228), "first cohort counts")
    diagnostics = {}
    for name, n in [("screen", 486), ("trace", 171), ("trace2", 16)]:
        rows = load(f"minlplib-branching/results/{name}.jsonl", ("inst", "status"), ("inst", "setting", "seed"))
        require(len(rows) == n, f"diagnostic count {name}")
        diagnostics[name] = len(rows)
    robust = load("robust-branching-points/results/minlplib.jsonl", ("inst", "setting", "seed", "status"),
                  ("inst", "setting", "seed"))
    synthetic = load("robust-branching-points/results/synthetic.jsonl", ("inst", "setting", "seed", "eps", "status"),
                     ("inst", "setting", "seed", "eps"))
    require(len(robust) == 2052 and len(synthetic) == 3840, "robust cohort counts")
    require({r["seed"] for r in synthetic} == set(range(5)) and
            {r["eps"] for r in synthetic} == {1e-2, 1e-4, 1e-6, 1e-8}, "synthetic grid")
    rules = []
    for name in ("rule_p100_k6", "rule_p200_k8"):
        rules.extend(load(f"sparse-regression/data/{name}.jsonl",
                     ("p", "k", "alpha", "seed", "bad0", "bad1", "maxz", "maxfrac"),
                     ("p", "k", "alpha", "seed")))
    exceptions = [r for r in rules if r["bad0"] == 0 and r["bad1"] > 0]
    require(len(rules) == 72 and len(exceptions) == 3, "sparse removal/C1 exceptions")
    redecided = load("sparse-regression/data/c1_redecided.jsonl", ("p", "k", "seed", "status"),
                     ("p", "k", "n", "rule", "seed"))
    require(len(redecided) == 31 and sum(r["status"] == "C1" for r in redecided) == 30,
            "sparse revised C1 inventory")
    bls = load("binary-least-squares/data/c1.jsonl", ("N", "beta", "theta", "seed", "c1", "refuted"),
               ("N", "beta", "theta", "seed"))
    require(len(bls) == 330 and all(r["c1"] or r["refuted"] for r in bls), "BLS decisions")
    report = dict(verification="read-only; no experiment or solver invocation", hashes_checked=len(entries),
        original_files=len(source_inventory), solver=inventory(solver), fit_groups_checked=len(computed_fits),
        first_retained=inventory(first), first_core=inventory(core), first_optional=inventory(optional),
        first_tolerance=inventory(tolerance), first_other_batches=diagnostics,
        first_total_recorded=len(first) + sum(diagnostics.values()), robust=inventory(robust),
        robust_synthetic=inventory(synthetic),
        model_leaf_ratios=leaf_ratios, figure_records_checked=displayed,
        sparse_redecided=dict(records=len(redecided), C1=30, fails=1),
        sparse_rule_exceptions=[{k:r[k] for k in ("p", "k", "alpha", "seed", "bad0", "bad1", "maxz", "maxfrac")}
                                for r in exceptions], binary_least_squares_C1_records=len(bls),
        first_node_ratios=node_ratios(core, [("lp", "default", 57, "1.033"),
            ("lp_noclamp", "default", 57, "2.185"), ("mix_noclamp", "default", 57, "1.348"),
            ("mid", "default", 57, "1.150")], False),
        robust_node_ratios=node_ratios(robust, [("rclamp", "default", 56, "0.963"),
            ("lp", "default", 57, "1.010"), ("x_recenter", "x_lp", 56, "0.939"),
            ("x_noclamp", "x_lp", 56, "1.999")], True))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
