"""Tables for face-exact-exponential.md from logs/bb_runs_v2.log (certified bounds) and the SCIP logs.

Usage: python3 summarize.py
"""
import glob
import math
import re
from collections import defaultdict

PAT = re.compile(r"^(\S+) (\S+) kappa=(\S+) (\S+) eps=(\S+) n=(\d+) nodes=(\d+) leaves=(\d+) (\S+)")
SPAT = re.compile(r"^(scip\S*) kappa=(\S+) (\S+) absgap=(\S+) n=(\d+) nodes=(\d+) (\S+)")


def lower_bound(n, eps=1e-4, b=0.8):
    return math.exp(-5 / 9 * (1 + eps / b)) * (5 / 3) ** n


def main():
    runs = {}
    for f in ["logs/bb_runs_v2.log"]:
        for line in open(f):
            m = PAT.match(line)
            if m:
                rel, rule, k, cm, e, n, nodes, leaves, st = m.groups()
                runs[(rel, rule, float(k), cm, float(e), int(n))] = (int(nodes), int(leaves), st)
    scip = {}
    for line in (l for f in ["logs/scip_runs.log"] + sorted(glob.glob("logs/scip_noprop_*.log")) + sorted(glob.glob("logs/scip_nominor_*.log")) for l in open(f)):
        m = SPAT.match(line)
        if m:
            tag, k, cm, e, n, nodes, st = m.groups()
            scip[(tag, float(k), cm, float(e), int(n))] = (int(nodes), st)

    print("A. leaves at eps = 1e-4 (toy B&B, exact node relaxations, certified bounds); last column: geometric-mean growth "
          "factor per added variable over the last four steps of n")
    ns = list(range(2, 11))
    print("config".ljust(34) + "".join(f"{n:>8d}" for n in ns) + "   growth")
    groups = defaultdict(dict)
    for (rel, rule, k, cm, e, n), (nodes, leaves, st) in runs.items():
        if e == 1e-4:
            groups[(rel, rule, k, cm)][n] = leaves if st == "done" else None
    for key in sorted(groups):
        row = groups[key]
        cells = "".join(f"{row[n]:>8d}" if row.get(n) else f"{'-':>8s}" for n in ns)
        avail = [n for n in ns if row.get(n)]
        g = ""
        if len(avail) >= 5:
            a, z = avail[-5], avail[-1]
            g = f"{(row[z] / row[a]) ** (1 / (z - a)):.2f}"
        rel, rule, k, cm = key
        print(f"{rel} {rule} kappa={k} {cm}".ljust(34) + cells + f"   {g}")
    print("Theorem 1 bound".ljust(34) + "".join(f"{lower_bound(n):>8.1f}" for n in ns))

    print("\nB. SCIP nodes (default settings, absgap 1e-4 unless stated)")
    for key in sorted(scip, key=lambda t: (t[0], t[1], t[2], t[3], t[4])):
        tag, k, cm, e, n = key
        nodes, st = scip[key]
        print(f"   {tag} kappa={k} {cm} absgap={e:.0e} n={n}: nodes={nodes} {st}")

    print("\nC. eps dependence (leaves)")
    eps_list = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    for (rel, rule, k, cm) in sorted({(a, b_, c, d) for (a, b_, c, d, e, n) in runs}):
        for n in (4, 6, 8):
            row = [runs.get((rel, rule, k, cm, e, n)) for e in eps_list]
            if sum(r is not None for r in row) >= 4:
                cells = "".join(f"{r[1]:>8d}" if r else f"{'-':>8s}" for r in row)
                print(f"   {rel} {rule} kappa={k} {cm} n={n}:".ljust(40) + cells)
    print("   (columns: eps = " + ", ".join(f"{e:.0e}" for e in eps_list) + ")")


if __name__ == "__main__":
    main()
