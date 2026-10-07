"""Run scip_run.py jobs in parallel (at most 6), appending one JSON line per run.

    python3 runner.py JOBFILE OUT.jsonl [--jobs 6]

JOBFILE lines: INSTANCE SETTING SEED TIMELIMIT [--eps EPS].  Jobs whose
(inst, setting, seed, tlim, eps) key is already in OUT.jsonl are skipped, so a batch
can be resumed.  A crash or a wall time above 2*TIMELIMIT+120 s is recorded as
status "crash" or "killed".
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


def key(inst, setting, seed, tlim, eps):
    return (inst, setting, int(seed), float(tlim), None if eps is None else float(eps))


def parse_job(f):
    eps = f[f.index("--eps") + 1] if "--eps" in f else None
    return f[0], f[1], f[2], f[3], eps


def run(job, out):
    inst, setting, seed, tlim, eps = parse_job(job)
    cmd = [sys.executable, os.path.join(HERE, "scip_run.py"), inst, setting, seed, tlim]
    if eps is not None:
        cmd += ["--eps", eps]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=2 * float(tlim) + 120)
        lines = [ln for ln in p.stdout.splitlines() if ln.startswith("{")]
        if p.returncode == 0 and lines:
            rec = json.loads(lines[-1])
        else:
            rec = dict(status="crash", rc=p.returncode, err=(p.stderr or p.stdout)[-400:])
    except subprocess.TimeoutExpired:
        rec = dict(status="killed")
    rec.update(inst=inst, setting=setting, seed=int(seed), tlim=float(tlim),
               eps=None if eps is None else float(eps))
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
            done.add(key(r["inst"], r["setting"], r["seed"], r["tlim"], r.get("eps")))
    jobs = [f for f in (ln.split() for ln in open(jobfile)) if f and key(*parse_job(f)) not in done]
    print(f"{len(jobs)} jobs to run ({len(done)} already done)", flush=True)
    n = 0
    with ThreadPoolExecutor(nj) as ex:
        for _ in ex.map(lambda j: run(j, out), jobs):
            n += 1
            if n % 50 == 0 or n == len(jobs):
                print(f"{n}/{len(jobs)} done", flush=True)


if __name__ == "__main__":
    main()
