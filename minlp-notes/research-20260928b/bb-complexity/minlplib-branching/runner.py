"""Run jobs in parallel, one subprocess per SCIP run.

    python3 runner.py JOBFILE OUT.jsonl [--jobs 6]

JOBFILE lines: INSTANCE SETTING SEED TIMELIMIT [extra run_one.py flags].
Jobs whose (inst, setting, seed, tlim, traced) key is already in OUT.jsonl are
skipped, so an interrupted batch can be resumed. A run that crashes or
exceeds 2*TIMELIMIT+120 s of wall time is recorded with status "crash" or
"killed".
"""
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
lock = threading.Lock()


def key(inst, setting, seed, tlim, trace):
    return (inst, setting, int(seed), float(tlim), bool(trace))


def run(job, out):
    inst, setting, seed, tlim, *extra = job
    cmd = [sys.executable, os.path.join(HERE, "run_one.py"), inst, setting, seed, tlim, *extra]
    rec = None
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=ENV,
                           timeout=2 * float(tlim) + 120)
        lines = [ln for ln in p.stdout.splitlines() if ln.startswith("{")]
        if p.returncode == 0 and lines:
            rec = json.loads(lines[-1])
        else:
            rec = dict(status="crash", rc=p.returncode, err=(p.stderr or p.stdout)[-400:])
    except subprocess.TimeoutExpired:
        rec = dict(status="killed")
    rec.update(inst=inst, setting=setting, seed=int(seed), tlim=float(tlim), traced="--trace" in extra)
    with lock:
        with open(out, "a") as fh:
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
    return rec


def main():
    jobfile, out = sys.argv[1], sys.argv[2]
    nj = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 6
    assert nj <= 6
    done = set()
    if os.path.exists(out):
        for ln in open(out):
            r = json.loads(ln)
            done.add(key(r["inst"], r["setting"], r["seed"], r["tlim"], r.get("traced", False)))
    jobs = []
    for ln in open(jobfile):
        f = ln.split()
        if f and key(f[0], f[1], f[2], f[3], "--trace" in f) not in done:
            jobs.append(f)
    print(f"{len(jobs)} jobs to run ({len(done)} already done)", flush=True)
    n = 0
    with ThreadPoolExecutor(nj) as ex:
        for rec in ex.map(lambda j: run(j, out), jobs):
            n += 1
            if n % 20 == 0 or n == len(jobs):
                print(f"{n}/{len(jobs)} done", flush=True)


if __name__ == "__main__":
    main()
