"""Driver of the exp/pow-audited rerun of route R (independent re-certification of every leaf)
for eg_int_s, eg_disc_s and eg_disc2_s.

    python3 run_audit.py [--workers 8] [--out DIR] [--only int,disc,disc2] [--dry-run]

What it runs (all code under this directory; nothing is run inside research-20260929/):
  record:int, record:disc_p0, record:disc_p1
      Regenerate the deleted recordings of runs C (eg_int_s) and E (eg_disc_s, 2 parts) with the
      reviewer's record_run.py.  It and the author's search code it replays are copied unchanged
      under record/research-20260929/ (same relative layout, so the copies import each other).
  cert:disc2_p<k>_c<c>   (38 jobs)
      cert/recheck_audit.py on the saved run-G recordings
      research-20260929/publication/eg-recheck/rec/rec_disc2_p<k>.npz, with exactly the chunking
      of the eg-recheck run (parts 0-7 in 4, 5, 6, 7, 7, 5, 3, 1 chunks), so every 64-box Taylor
      batch is the same as in the saved res/p<k>_c<c>.npz files.
  cert:int, cert:disc_p0, cert:disc_p1   (one chunk each, as the review's verify_tree.py runs)
      after the corresponding recording job.
  compare_audit.py at the end (bit-identity with the saved results, audit summary).

Outputs, only under DIR (default: eg-audit/out/):
  DIR/rec/rec_int.npz, rec_disc_p0.npz, rec_disc_p1.npz   regenerated recordings
  DIR/res/<job>.npz                                        per-leaf results with audit flags
  DIR/logs/<job>.log                                       one log per job
  DIR/run_audit.log                                        driver progress (also on stdout)
  DIR/compare.log                                          output of compare_audit.py
Restartable: a job is skipped when its output exists and its log has the final line; an
interrupted job is rerun from the start (its output is written atomically or checked).
Every job runs single-threaded (OMP/OPENBLAS/MKL threads = 1) with PYTHONDONTWRITEBYTECODE=1.
"""
import argparse
import heapq
import os
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.environ.get("EG_AUDIT_R") or os.path.normpath(os.path.join(HERE, "..", "..", "..", "research-20260929"))
REC_DISC2 = os.path.join(R, "publication", "eg-recheck", "rec")
RECORD = os.path.join(HERE, "record", "research-20260929", "reviews", "eg-retry-review-checks", "record_run.py")
RECHECK = os.path.join(HERE, "cert", "recheck_audit.py")
TH = {"eg_int_s": "6.4531031529331155", "eg_disc_s": "5.760539610694994", "eg_disc2_s": "5.642100574331458"}
NCH = {0: 4, 1: 5, 2: 6, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
# certified pieces per job (eg-recheck res/ files and the review's verify logs): cost estimates
PIECES_DISC2 = {0: 181859, 1: 213351, 2: 277737, 3: 348830, 4: 342813, 5: 232161, 6: 124909, 7: 48287}
PIECES = {"int": 38173, "disc_p0": 67139, "disc_p1": 58243}
REC_S = {"int": 170, "disc_p0": 200, "disc_p1": 180}     # recording s, measured on a quiet machine
MS_PER_PIECE = 5.5                                         # audited certification, measured (sample test)
ENV = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
           PYTHONDONTWRITEBYTECODE="1")


class Job:
    def __init__(self, name, cmd, out, final, cost, deps=()):
        self.name, self.cmd, self.out, self.final, self.cost, self.deps = name, cmd, out, final, cost, set(deps)

    def log(self, OUT):
        return os.path.join(OUT, "logs", self.name.replace(":", "_") + ".log")

    def done(self, OUT):
        if not os.path.exists(self.out):
            return False
        try:
            with open(self.log(OUT)) as f:
                return any(line.startswith(self.final) for line in f)
        except OSError:
            return False


def make_jobs(OUT, only):
    jobs = []
    rec = os.path.join(OUT, "rec")
    res = os.path.join(OUT, "res")
    if "int" in only:
        out = os.path.join(rec, "rec_int.npz")
        jobs.append(Job("record:int", ["python3", RECORD, "eg_int_s", "1e-9", "20000", out], out, "recorded", REC_S["int"]))
        o = os.path.join(res, "int.npz")
        jobs.append(Job("cert:int", ["python3", RECHECK, out, "eg_int_s", TH["eg_int_s"], "0", "1", o], o, "  saved ",
                        PIECES["int"] * MS_PER_PIECE / 1e3, deps=["record:int"]))
    if "disc" in only:
        for k in (0, 1):
            out = os.path.join(rec, f"rec_disc_p{k}.npz")
            jobs.append(Job(f"record:disc_p{k}", ["python3", RECORD, "eg_disc_s", "1e-9", "20000", out, str(k), "2"],
                            out, "recorded", REC_S[f"disc_p{k}"]))
            o = os.path.join(res, f"disc_p{k}.npz")
            jobs.append(Job(f"cert:disc_p{k}", ["python3", RECHECK, out, "eg_disc_s", TH["eg_disc_s"], "0", "1", o], o,
                            "  saved ", PIECES[f"disc_p{k}"] * MS_PER_PIECE / 1e3, deps=[f"record:disc_p{k}"]))
    if "disc2" in only:
        for k in range(8):
            src = os.path.join(REC_DISC2, f"rec_disc2_p{k}.npz")
            for c in range(NCH[k]):
                o = os.path.join(res, f"disc2_p{k}_c{c}.npz")
                jobs.append(Job(f"cert:disc2_p{k}_c{c}", ["python3", RECHECK, src, "eg_disc2_s", TH["eg_disc2_s"],
                                                          str(c), str(NCH[k]), o], o, "  saved ",
                                PIECES_DISC2[k] / NCH[k] * MS_PER_PIECE / 1e3))
    return jobs


def critical(job, by_name, memo):
    """cost of the longest chain that starts with job (for scheduling priority)."""
    if job.name not in memo:
        succ = [j for j in by_name.values() if job.name in j.deps]
        memo[job.name] = job.cost + max((critical(j, by_name, memo) for j in succ), default=0.0)
    return memo[job.name]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--only", default="int,disc,disc2")
    ap.add_argument("--timeout", type=int, default=6 * 3600, help="per-job timeout (s)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for sig in (signal.SIGTERM, signal.SIGHUP):          # run the cleanup below (kill the jobs) on these
        signal.signal(sig, lambda s, f: sys.exit(128 + s))
    OUT = os.path.abspath(a.out)
    for sub in ("rec", "res", "logs"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    flog = open(os.path.join(OUT, "run_audit.log"), "a")
    t0 = time.time()

    def say(msg):
        line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')} +{time.time() - t0:7.0f}s] {msg}"
        print(line, flush=True)
        flog.write(line + "\n")
        flog.flush()

    jobs = make_jobs(OUT, set(a.only.split(",")))
    by_name = {j.name: j for j in jobs}
    memo = {}
    prio = {j.name: critical(j, by_name, memo) for j in jobs}
    done = {j.name for j in jobs if j.done(OUT)}
    pending = [j for j in jobs if j.name not in done]
    say(f"start: {len(jobs)} jobs, {len(done)} already done, {len(pending)} to run, workers {a.workers}, out {OUT}")
    say(f"estimated CPU of the remaining jobs: {sum(j.cost for j in pending) / 3600:.2f} h")
    if a.dry_run:
        for j in sorted(pending, key=lambda j: -prio[j.name]):
            print(f"  {j.name:22s} est {j.cost:6.0f}s  deps {sorted(j.deps)}  {' '.join(j.cmd)}")
        return 0
    running = {}
    failed = set()
    last = 0.0
    try:
        while pending or running:
            for name, (p, j, ts, fh) in list(running.items()):
                rc = p.poll()
                if rc is None:
                    continue
                fh.close()
                del running[name]
                ok = rc == 0 and j.done(OUT)
                (done if ok else failed).add(name)
                say(f"{'done  ' if ok else 'FAILED'} {name} rc={rc} {time.time() - ts:.0f}s")
            ready = [j for j in pending if j.deps <= done]
            blocked = [j for j in pending if j.deps & failed]
            for j in blocked:
                pending.remove(j)
                failed.add(j.name)
                say(f"skip   {j.name}: a dependency failed")
            heap = [(-prio[j.name], j.name) for j in ready]
            heapq.heapify(heap)
            while heap and len(running) < a.workers:
                _, name = heapq.heappop(heap)
                j = by_name[name]
                pending.remove(j)
                fh = open(j.log(OUT), "w")
                p = subprocess.Popen(["timeout", str(a.timeout)] + j.cmd, stdout=fh, stderr=subprocess.STDOUT,
                                     env=ENV, cwd=OUT, start_new_session=True)
                running[name] = (p, j, time.time(), fh)
                say(f"start  {name} (pid {p.pid}, est {j.cost:.0f}s)")
            if time.time() - last > 300:
                last = time.time()
                rem = sum(j.cost for j in pending) + sum(max(0.0, j.cost - (time.time() - ts))
                                                         for p, j, ts, fh in running.values())
                say(f"status: done {len(done)}/{len(jobs)}, running {len(running)}, pending {len(pending)}, "
                    f"failed {len(failed)}; remaining CPU est {rem / 3600:.2f} h (~{rem / max(1, a.workers) / 60:.0f} min wall)")
            time.sleep(5)
    finally:
        for p, j, ts, fh in running.values():
            os.killpg(p.pid, signal.SIGTERM)
            say(f"killed {j.name} (driver exit)")
    say(f"all jobs finished: {len(done)} done, {len(failed)} failed: {sorted(failed)}")
    cmp_log = os.path.join(OUT, "compare.log")
    with open(cmp_log, "w") as fh:
        rc = subprocess.call(["python3", os.path.join(HERE, "compare_audit.py"), "--out", OUT],
                             stdout=fh, stderr=subprocess.STDOUT, env=ENV, cwd=OUT)
    say(f"compare_audit.py rc={rc}; see {cmp_log}")
    with open(cmp_log) as fh:
        tail = fh.read().strip().splitlines()[-3:]
    for line in tail:
        say("  " + line)
    return 1 if failed or rc else 0


if __name__ == "__main__":
    sys.exit(main())
