"""Driver for sim2d.c (revision after review): 10^6 runs per entry for the randomized clamps
(independent draws and draws keyed per (variable, interval)), one run for deterministic rules.
At most 4 processes.

    gcc -O2 -o sim2d sim2d.c -lm && python3 run_sim2d.py sim2d.jsonl
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

A = [1 / 6, 3 / 238, 0.1999, 0.25, 1 / 3, 0.010169169457068361, 0.8252065092537432, 0.2986398551995928]
EPS = [10.0 ** -k for k in range(2, 9)]
RULES = [("rclip", "0.1", "0.3"), ("rclip", "0.05", "0.35"), ("kvar", "0.1", "0.3"), ("kvar", "0.05", "0.35"),
         ("kshared", "0.1", "0.3"), ("clip", "0.2"), ("recenter", "0.2")]
jobs = []
for i, a in enumerate(A):
    for r in RULES:
        if r[0] == "kshared" and a not in (1 / 6, 3 / 238, 0.010169169457068361):
            continue
        for j, e in enumerate(EPS):
            n = "1" if r[0] in ("clip", "recenter") else "1000000"
            jobs.append(["./sim2d", repr(a), *r[:1], *r[1:], repr(e), n, str(1000 * i + 10 * j + len(r[0]))])


def run(cmd):
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)


with ThreadPoolExecutor(4) as ex, open(sys.argv[1], "w") as fh:
    for rec in ex.map(run, jobs):
        fh.write(json.dumps(rec) + "\n")
        fh.flush()
print(len(jobs), "entries")
