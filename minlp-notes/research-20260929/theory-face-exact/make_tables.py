"""Markdown tables of Section 7 of face-exact-exponential.md, generated from the certified logs.

Reads logs/bb_runs_v2.log (toy B&B, certified bounds), logs/grid_dp_n*_*.log and the SCIP logs.
Usage: python3 make_tables.py > logs/tables.md
"""
import glob
import math
import re

PAT = re.compile(r"^(\S+) (\S+) kappa=(\S+) (\S+) eps=(\S+) n=(\d+) nodes=(\d+) leaves=(\d+) (\S+)")
STAT = re.compile(r"refined=(\d+) undecided=(\d+) solver-too-high=(\d+)")


def load():
    runs = {}
    for line in (l for f in ("logs/bb_runs_v2.log", "logs/bb_runs_v3_mc.log") for l in open(f)):   # v3 overrides v2
        m = PAT.match(line)
        if m:
            rel, rule, k, cm, e, n, nodes, leaves, st = m.groups()
            s = STAT.search(line)
            runs[(rel, rule, float(k), cm, float(e), int(n))] = (int(leaves), st, tuple(map(int, s.groups())) if s else None)
    return runs


def growth(row, ns):
    avail = [n for n in ns if row.get(n)]
    if len(avail) < 5:
        return ""
    a, z = avail[-5], avail[-1]
    return f"{(row[z] / row[a]) ** (1 / (z - a)):.2f}"


def main():
    runs = load()
    ns = list(range(2, 11))
    print("### leaf table (eps = 1e-4)\n")
    print("| relaxation, rule, instance | " + " | ".join(f"n={n}" if n == 2 else str(n) for n in ns) + " | growth |")
    print("|---|" + "---|" * (len(ns) + 1))
    rows = [("mc", "bisect", 0.0, "zero", "`mc` bisect, `kappa=0`, `c=0`"),
            ("mc", "bisect", 0.1, "seed0", "`mc` bisect, seed 0"),
            ("mc", "oracle", 0.1, "seed0", "`mc` oracle, seed 0"),
            ("mc", "viol", 0.1, "seed0", "`mc` viol, seed 0"),
            ("mc", "vw", 0.1, "seed0", "`mc` vw, seed 0"),
            ("mcx", "bisect", 0.1, "seed0", "`mcx` bisect, seed 0"),
            ("mcx", "oracle", 0.1, "seed0", "`mcx` oracle, seed 0"),
            ("mcx", "vw", 0.1, "seed0", "`mcx` vw, seed 0"),
            ("mcx", "vw", 0.1, "seed1", "`mcx` vw, seed 1"),
            ("mcx", "vw", 0.1, "zero", "`mcx` vw, `c=0`"),
            ("abb", "bisect", 0.0, "zero", "`abb` bisect, `kappa=0`, `c=0`"),
            ("abb", "viol", 0.0, "zero", "`abb` viol, `kappa=0`, `c=0`"),
            ("abbU", "bisect", 0.1, "zero", "`abbU` bisect, `c=0` (PROGRAM factorization)"),
            ("abbS", "bisect", 0.1, "zero", "`abbS` bisect, `c=0` (balanced split)")]
    for rel, rule, k, cm, name in rows:
        row = {n: runs[(rel, rule, k, cm, 1e-4, n)][0] for n in ns
               if (rel, rule, k, cm, 1e-4, n) in runs and runs[(rel, rule, k, cm, 1e-4, n)][1] == "done"}
        print(f"| {name} | " + " | ".join(str(row[n]) if n in row else "" for n in ns) + f" | {growth(row, ns)} |")
    tb = {n: math.exp(-5 / 9 * (1 + 1e-4 / 0.8)) * (5 / 3) ** n for n in ns}
    print("| Theorem 1 lower bound | " + " | ".join(f"{tb[n]:.1f}" for n in ns) + " | 1.67 |")

    print("\n### eps table\n")
    eps = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    print("| relaxation, rule, instance | n | " + " | ".join(f"`{e:.0e}`" for e in eps) + " |")
    print("|---|---|" + "---|" * len(eps))
    for rel, rule, k, cm, name, nlist in [("mcx", "bisect", 0.1, "seed0", "`mcx` bisect, seed 0", (4, 6, 8)),
                                          ("mcx", "vw", 0.1, "seed0", "`mcx` vw, seed 0", (4, 6, 8)),
                                          ("mc", "bisect", 0.0, "zero", "`mc` bisect, `kappa=0`, `c=0`", (4, 6, 8)),
                                          ("mc", "viol", 0.1, "seed0", "`mc` viol, seed 0", (8,))]:
        for j, n in enumerate(nlist):
            cells = [runs.get((rel, rule, k, cm, e, n)) for e in eps]
            print(f"| {name if j == 0 else ''} | {n} | " + " | ".join(str(c[0]) if c else "" for c in cells) + " |")

    print("\n### certified-bound statistics (nodes refined by dual ascent / undecided / solver value too high)\n")
    tot = [0, 0, 0]
    for key, (lv, st, s) in sorted(runs.items()):
        if s:
            for i in range(3):
                tot[i] += s[i]
    print(f"totals over all {len(runs)} runs: refined={tot[0]}, undecided={tot[1]}, solver-too-high={tot[2]}")
    und = [(k, s) for k, (lv, st, s) in runs.items() if s and s[1] > 0]
    print("runs with undecided nodes:", und if und else "none")

    print("\n### grid DP\n")
    for f in sorted(glob.glob("logs/grid_dp_n*_*.log")):
        for line in open(f):
            if line.startswith("grid DP"):
                print("   ", line.strip())


if __name__ == "__main__":
    main()
