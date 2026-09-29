"""Run the eps sweeps: python3 sweep.py [OUT.jsonl] [--workers 4] [--phase2].

Each (instance, setting) pair is one sequence over EPS in decreasing order,
run sequentially; a sequence stops after its first run that hits the node or
time limit (smaller eps would only hit it again). Up to --workers sequences
run in parallel, each run in its own subprocess. Finished runs are skipped
on restart.
"""
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = [10 ** (-k / 2) for k in range(2, 15)]          # 1e-1 ... 1e-7, half decades

CORE = ["iso2", "isofbbt2", "linediag2", "lineaxis2", "ring2", "qflat2a",
        "mccaxis2", "mccdiag2", "conexp2"]
FULL = ["default", "nopresolve", "noprop", "nocutoffprop", "obbtoff", "obbtall",
        "lppoint", "midpoint", "widestbisect", "model", "modelnoprop", "toy"]
REST = ["iso3", "iso4", "iso2c", "qflat1", "qflat2b", "qflat3", "sphere3", "plane3",
        "conexp4", "condisk2", "condisk2soc"]
REDUCED = ["default", "noprop", "model", "toy"]
EXTRA = [("ring2", "noexpand"), ("mccaxis2", "withlocks"), ("condisk2", "noexpand")]

TASKS = [(i, s) for i in CORE for s in FULL] + [(i, s) for i in REST for s in REDUCED] + EXTRA
# second phase, added after the cutoff-in-presolve finding
TASKS2 = [(i, "noweakdual") for i in CORE] + [("mccaxis2", s) for s in
                                                ("xprio", "xpriomidpoint", "xpriolppoint")] \
    + [(i, "smallstreps") for i in ("mccaxis2", "isofbbt2", "mccdiag2")] \
    + [("condisk2soc", s) for s in ("noweakdual", "nocutoffprop", "nonlprop")] \
    + [("mccaxis2", "xpriotoy"), ("mccaxis2", "exttoy"), ("mccaxis2", "xprioexttoy")]

LOCK = threading.Lock()


def done_keys(path):
    keys = set()
    if os.path.exists(path):
        with open(path) as fh:
            for line in fh:
                r = json.loads(line)
                keys.add((r["inst"], r["setting"], r["eps"], r["status"]))
    return keys


def sequence(inst, setting, out, done):
    for eps in EPS:
        prev = [k for k in done if k[:3] == (inst, setting, eps)]
        if prev:
            if prev[0][3] in ("nodelimit", "timelimit"):
                return
            continue
        cmd = [sys.executable, os.path.join(HERE, "run_one.py"), inst, setting, repr(eps)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        lines = [ln for ln in p.stdout.splitlines() if ln.startswith("{")]
        if p.returncode != 0 or not lines:
            r = dict(inst=inst, setting=setting, eps=eps, status="error",
                     stderr=p.stderr[-500:], stdout=p.stdout[-500:])
        else:
            r = json.loads(lines[-1])
        with LOCK:
            with open(out, "a") as fh:
                fh.write(json.dumps(r, separators=(",", ":")) + "\n")
            print(f"{inst:12s} {setting:13s} eps={eps:.1e} {r['status']:9s} "
                  f"nodes={r.get('nodes')} t={r.get('time')}", flush=True)
        if r["status"] in ("nodelimit", "timelimit", "error"):
            return


def main():
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") \
        else os.path.join(HERE, "results", "runs.jsonl")
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    os.makedirs(os.path.dirname(out), exist_ok=True)
    done = done_keys(out)
    tasks = TASKS2 if "--phase2" in sys.argv else TASKS
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in [ex.submit(sequence, i, s, out, done) for i, s in tasks]:
            f.result()


if __name__ == "__main__":
    main()
