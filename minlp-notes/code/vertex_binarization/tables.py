"""Markdown tables from sweep JSON lines: python3 tables.py <file.jsonl> [...]"""
import json
import sys
from collections import defaultdict

for path in sys.argv[1:]:
    rows = [json.loads(l) for l in open(path)]
    best = defaultdict(lambda: float("inf"))
    for r in rows:
        if "true_obj" in r:
            best[(r["family"], r["n"], r["m"], r["seed"])] = min(best[(r["family"], r["n"], r["m"], r["seed"])], r["true_obj"])
    by = defaultdict(dict)
    for r in rows:
        by[(r["family"], r["n"], r["m"], r["seed"])][(r["solver"], r["form"])] = r
    solvers = sorted({r["solver"] for r in rows})
    forms = sorted({r["form"] for r in rows})
    print(f"\n`{path}` (time limit {rows[0]['tl']:.0f} s; cell = seconds, or `TL gap%` with the gap between the "
          "dual bound and the best known value; `!` marks a returned point worse than the best known by more than 1e-4)\n")
    head = ["family", "n", "m", "seed"] + [f"{s} {f}" for s in solvers for f in forms]
    print("| " + " | ".join(head) + " |\n|" + "---|" * len(head))
    for k in sorted(by):
        cells = []
        for s in solvers:
            for f in forms:
                r = by[k].get((s, f))
                if r is None or "time" not in r:
                    cells.append("–"); continue
                bk = best[k]
                gap = 100 * abs(bk - r["dual"]) / max(1e-9, abs(bk))
                bad = "!" if r.get("true_obj", bk) > bk + 1e-4 * max(1, abs(bk)) else ""
                done = r["status"] in ("optimal", "gaplimit")
                cells.append((f"{r['time']:.1f}" if done else f"TL {gap:.1f}%") + bad)
        print("| " + " | ".join(map(str, k)) + " | " + " | ".join(cells) + " |")
