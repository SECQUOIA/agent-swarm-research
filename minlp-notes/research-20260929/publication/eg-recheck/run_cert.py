"""Scheduler for the full re-certification of eg_disc2_s run G (all 8 parts).

Jobs per part k (eligible once logs/rec_disc2_p<k>.log has its final 'recorded' line):
  * the reviewer's verify_tree.py, unchanged, with sample fraction 0 (its coverage check plus
    its 2000 tightest closures) -> logs/verify_tree_p<k>.log
  * recheck_leaves.py chunk c of NCH[k] (every leaf of the part) -> res/p<k>_c<c>.npz, logs/cert_p<k>_c<c>.log
At most MAXP processes of this track run at once (the running record_run.py processes count).
"""
import os
import subprocess
import time

OUT = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(OUT, "..", "..", "reviews", "eg-retry-review-checks")
TH = "5.642100574331458"
MAXP = 12
NCH = {0: 4, 1: 5, 2: 6, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
           PYTHONDONTWRITEBYTECODE="1")

jobs = []
for k in (3, 4, 2, 5, 1, 0, 6, 7):          # largest parts first
    rec = os.path.join(OUT, "rec", f"rec_disc2_p{k}.npz")
    jobs.append((k, ["timeout", "7200", "python3", os.path.join(REV, "verify_tree.py"), rec, "eg_disc2_s", TH, "0.0", "0"],
                 os.path.join(OUT, "logs", f"verify_tree_p{k}.log")))
    for c in range(NCH[k]):
        jobs.append((k, ["timeout", "14400", "python3", os.path.join(OUT, "recheck_leaves.py"), rec, "eg_disc2_s", TH,
                         str(c), str(NCH[k]), os.path.join(OUT, "res", f"p{k}_c{c}.npz")],
                     os.path.join(OUT, "logs", f"cert_p{k}_c{c}.log")))


def recorded(k):
    try:
        return any(line.startswith("recorded") for line in open(os.path.join(OUT, "logs", f"rec_disc2_p{k}.log")))
    except OSError:
        return False


def n_recording():
    r = subprocess.run(["pgrep", "-f", "^python3 .*record_run.py eg_disc2_s"], capture_output=True, text=True)
    return len(r.stdout.split())


running = []
t0 = time.time()
while jobs or running:
    for p, cmd, log, ts in list(running):
        if p.poll() is not None:
            print(f"[{time.time() - t0:7.0f}s] done rc={p.returncode} {os.path.basename(log)} ({time.time() - ts:.0f}s)", flush=True)
            running.remove((p, cmd, log, ts))
    nrec = n_recording()
    for j in list(jobs):
        if len(running) + nrec >= MAXP:
            break
        k, cmd, log = j
        if recorded(k):
            p = subprocess.Popen(cmd, stdout=open(log, "w"), stderr=subprocess.STDOUT, env=ENV, cwd=OUT)
            running.append((p, cmd, log, time.time()))
            jobs.remove(j)
            print(f"[{time.time() - t0:7.0f}s] start pid {p.pid} {' '.join(cmd[3:])}", flush=True)
    time.sleep(10)
print(f"all jobs finished after {time.time() - t0:.0f}s", flush=True)
