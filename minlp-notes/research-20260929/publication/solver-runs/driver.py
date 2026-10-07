#!/usr/bin/env python3
"""Batch driver for the current-solver campaign (GAMS 54.3: BARON, GUROBI, SCIP).

Runs every (instance, solver) pair with the campaign settings
  <TYPE>=<SOLVER> reslim=R threads=1 optcr=1e-9 optca=1e-9
where TYPE is the model type the .gms file declares (NLP or MINLP here).
The counted attempt of each pair lives in OUT/runs/<instance>__<solver>/ with
gams.log, <inst>.lst, trace.trc, m_p.gdx (savepoint), stdout.txt, cmd.txt and
run.json. Instances are queued largest first (by nonzeros), all three solvers
per instance.

Admission. A run starts only if the 1-minute load average is at most
--max-load (30) and MemAvailable is at least --min-mem-gb (8); at most --jobs
(10) runs at once. Every wait is logged in driver.log: "wait" when it begins
or its reason changes and every 10 min while it lasts, "admit" when it ends.

Limits, checked by a monitor thread every 5 s:
  * hard wall-clock timeout reslim + --hard-extra-s (600 s);
  * memory cap: resident plus swapped memory of the run's process group above
    --mem-cap-gb (8);
  * low CPU share: the attempt can no longer reach the validity ratio (b)
    below, even if it got 1.02 CPU-seconds per second (GUROBI's helper threads
    give up to about 1.01) until its latest possible end, the hard timeout
    plus the SIGINT and SIGTERM graces; 10 s of slack covers CPU time that the
    5 s /proc samples can miss. Such an attempt is invalid anyway; stopping it
    early frees its slot and the machine.
On a limit the solver process (the process of the run's group with the most
CPU time: baron, or gmsgenux.out for GUROBI and SCIP) gets SIGINT. The solvers
treat it as a user interrupt (solver status 8) and GAMS still writes the final
bound, trace record and savepoint. SIGINT is not sent to the whole group: then
GAMS itself reacts too, and GUROBI runs interrupted after about 20 s or more
ended with solver/model status 13/13 and no solution (smoke2/sigsolver_*,
smoke2/gurobi_int). A solver may still ignore SIGINT for a while (SCIP on
optcdeg2 did for 120 s in driver 1). SIGTERM to the group follows 300 s after
SIGINT, SIGKILL 30 s after that.

Validity. The solvers are single-threaded, so an attempt counts (valid) only if
  (a) it ended by its own completion with a trace record, or by the hard
      timeout, and
  (b) CPU time of its process group / wall time >= --min-cpu-ratio (0.9).
Test (b) is not applied to attempts that completed on their own within
SHORT_RUN_S (60 s) and not at the solver's time limit (trace solver status
other than 3): GAMS start-up and file I/O dominate such short wall times, and
the CPU share cannot change how they end (BARON and SCIP reject
ann_cumene_tanh in under 1 s with cpu/wall 0.2-0.3).
An invalid attempt (low CPU share, memory cap, or an end without a trace record
that the driver did not cause) is moved to
OUT/runs_archive/attempts/<instance>__<solver>__a<k>/ and requeued at the end of
the queue, at most --max-retries (2) times. After the last attempt the best one
(proper end first, then a trace record, then the highest CPU/wall) is copied
back to runs/ with valid=false and kept_best=true; all attempts stay archived.

CPU time of an attempt: the larger of (a) wait4 resource usage of the gams
process (misses children that gams never reaped, e.g. after SIGTERM) and (b)
the sum over all processes of the group of their last /proc utime+stime sample
(misses at most the last 5 s of each process). Both are lower bounds.

Restart. A run whose run.json says finished=true is skipped. A run dir left
unfinished by a stopped or killed driver is deleted (after killing any of its
processes that are still alive) and rerun; it is not counted as an attempt.
Attempt numbers continue from runs_archive/attempts/.

Progress: OUT/progress.txt (every 30 s), events OUT/driver.log, machine load,
memory and swap every 60 s in OUT/machine_load.csv.

usage:
  python3 driver.py                                         # full campaign
  python3 driver.py --out smoke2/basic --reslim 30 --instances ex6_2_5 chain50
"""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from collect import parse_trace  # noqa: E402

GAMS = (_PUBLIC_HOME + '/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams')
SOLVERS = ["BARON", "GUROBI", "SCIP"]
OPTCR = "1e-9"
OPTCA = "1e-9"
INT_GRACE_S = 300
TERM_GRACE_S = 30
SHORT_RUN_S = 60
ADMIT_POLL_S = 15
WAIT_LOG_EVERY_S = 600
PAGE_KB = os.sysconf("SC_PAGE_SIZE") // 1024
CLK_TCK = os.sysconf("SC_CLK_TCK")
CHILD_ENV = {**os.environ, "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1"}


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def declared(gms):
    text = Path(gms).read_text(errors="replace")
    m = re.search(r"^Solve\s+m\s+using\s+%(\w+)%\s+(minimizing|maximizing)\s+objvar", text, re.M)
    return m.group(1), ("min" if m.group(2) == "minimizing" else "max")


def write_json(path, obj):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, indent=1) + "\n")
    tmp.replace(path)


def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def sample_groups(pgids):
    """Per process group: resident and swapped memory (MB) summed over its
    processes, and CPU seconds so far (utime+stime) per process, keyed by
    (pid, start time) so that a reused pid is not confused with an old one."""
    res = {g: {"rss": 0.0, "swap": 0.0, "cpu": {}} for g in pgids}
    for p in os.listdir("/proc"):
        if not p.isdigit():
            continue
        try:
            with open(f"/proc/{p}/stat") as f:
                st = f.read()
        except OSError:
            continue
        fields = st[st.rfind(")") + 2:].split()
        r = res.get(int(fields[2]))
        if r is None:
            continue
        r["cpu"][(int(p), fields[19])] = (int(fields[11]) + int(fields[12])) / CLK_TCK
        r["rss"] += int(fields[21]) * PAGE_KB / 1024
        try:
            with open(f"/proc/{p}/status") as f:
                for ln in f:
                    if ln.startswith("VmSwap:"):
                        r["swap"] += int(ln.split()[1]) / 1024
                        break
        except OSError:
            pass
    return res


def meminfo_gb():
    """MemAvailable and swap in use (GB) from /proc/meminfo."""
    v = {}
    with open("/proc/meminfo") as f:
        for ln in f:
            k, rest = ln.split(":", 1)
            v[k] = int(rest.split()[0]) / 2**20
    return v["MemAvailable"], v["SwapTotal"] - v["SwapFree"]


def best_key(meta):
    """Order of attempts for keeping the best: proper end, then a trace record, then CPU/wall."""
    return (meta.get("end_kind") in ("completed", "hard timeout"), bool(meta.get("has_trace")),
            meta.get("cpu_over_wall") or 0.0)


class Driver:
    def __init__(self, a):
        self.a = a
        self.out = (HERE / a.out).resolve()
        self.runs = self.out / "runs"
        self.archive = self.out / "runs_archive" / "attempts"
        self.runs.mkdir(parents=True, exist_ok=True)
        self.archive.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.admit_lock = threading.Lock()
        self.active = {}      # pgid -> dict(name, t0, stage, t_stage, reason, memory and CPU samples)
        self.waiting = None   # (name, monotonic start, reason) of the run waiting for admission
        self.pending = []     # tasks taken from the queue by a worker, not started yet (admission)
        self.done = []        # names that ended in this driver session (any outcome)
        self.stop = threading.Event()
        self.finished_all = threading.Event()
        self.tasks = self.build_tasks()
        self.total = len(self.tasks)

    def log(self, msg):
        line = f"{utc()} {msg}"
        with self.lock:
            with open(self.out / "driver.log", "a") as f:
                f.write(line + "\n")

    def build_tasks(self):
        names = self.a.instances or (HERE / "instances.txt").read_text().split()
        mpath = HERE / "gms_manifest.json"
        size = {r["instance"]: r["gms_nz"] for r in json.loads(mpath.read_text())} if mpath.exists() else {}
        names = sorted(names, key=lambda n: -size.get(n, 0))
        return [(n, s) for n in names for s in self.a.solvers]

    def attempts(self, name):
        """Archived attempt dirs of a run, in attempt order."""
        return sorted(self.archive.glob(f"{name}__a*"), key=lambda p: int(p.name.rsplit("__a", 1)[1]))

    # ---------------------------------------------------------------- admission
    def admit(self, name):
        """Block until load and memory allow a start; return the admission record or None on stop."""
        with self.admit_lock:
            t0 = time.monotonic()
            last_kinds, last_log = None, 0.0
            while not self.stop.is_set():
                load1 = os.getloadavg()[0]
                avail, _ = meminfo_gb()
                why = []
                if load1 > self.a.max_load:
                    why.append(f"load1 {load1:.1f} > {self.a.max_load:g}")
                if avail < self.a.min_mem_gb:
                    why.append(f"MemAvailable {avail:.1f} GB < {self.a.min_mem_gb:g} GB")
                now = time.monotonic()
                if not why:
                    waited = now - t0
                    if last_kinds is not None:
                        self.log(f"admit {name} after waiting {waited:.0f} s (load1 {load1:.1f}, "
                                 f"MemAvailable {avail:.1f} GB)")
                    with self.lock:
                        self.waiting = None
                    return {"admission_wait_s": round(waited, 1), "load1_at_admission": round(load1, 2),
                            "mem_available_gb_at_admission": round(avail, 2)}
                kinds = tuple(w.split()[0] for w in why)
                if kinds != last_kinds or now - last_log >= WAIT_LOG_EVERY_S:
                    self.log(f"wait {name} (waiting {now - t0:.0f} s): " + "; ".join(why))
                    last_kinds, last_log = kinds, now
                with self.lock:
                    self.waiting = (name, t0, "; ".join(why))
                self.stop.wait(ADMIT_POLL_S)
            with self.lock:
                self.waiting = None
            return None

    # ---------------------------------------------------------------- one attempt
    def run_one(self, inst, solver, adm):
        name = f"{inst}__{solver}"
        d = self.runs / name
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        k = len(self.attempts(name)) + 1
        gms = HERE / "gms" / f"{inst}.gms"
        mtype, sense = declared(gms)
        cmd = [GAMS, str(gms), f"{mtype}={solver}", f"reslim={self.a.reslim}", "threads=1",
               f"optcr={OPTCR}", f"optca={OPTCA}", "lo=2", "logfile=gams.log", f"o={inst}.lst",
               "savepoint=1", "trace=trace.trc", "traceopt=3"]
        (d / "cmd.txt").write_text(
            "cd " + str(d) + "\nOMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 "
            + " ".join(cmd) + "\n")
        meta = {"instance": inst, "solver": solver, "model_type": mtype, "sense": sense,
                "reslim": self.a.reslim, "threads": 1, "optcr": OPTCR, "optca": OPTCA,
                "hard_timeout_s": self.a.reslim + self.a.hard_extra_s, "int_grace_s": INT_GRACE_S,
                "mem_cap_gb": self.a.mem_cap_gb, "min_cpu_ratio": self.a.min_cpu_ratio,
                "max_retries": self.a.max_retries, "attempt": k, "cmd": cmd, **adm,
                "start_utc": utc(), "loadavg_start": os.getloadavg(), "finished": False,
                "driver_pid": os.getpid()}
        t0 = time.monotonic()
        with open(d / "stdout.txt", "wb") as so:
            p = subprocess.Popen(cmd, cwd=d, stdout=so, stderr=subprocess.STDOUT,
                                 start_new_session=True, env=CHILD_ENV)
        meta["pgid"] = p.pid
        write_json(d / "run.json", meta)
        info = {"name": name, "attempt": k, "t0": t0, "stage": 0, "t_stage": None, "reason": None,
                "rss": 0.0, "swap": 0.0, "peak": 0.0, "peak_rss": 0.0, "peak_swap": 0.0, "cpu": {},
                "load_sum": 0.0, "n_samples": 0, "machine_swap_max": 0.0, "avail_min": None}
        with self.lock:
            self.active[p.pid] = info
        self.log(f"start {name} attempt {k} pid {p.pid}")
        _, status, ru = os.wait4(p.pid, 0)
        p.returncode = os.waitstatus_to_exitcode(status)
        wall = time.monotonic() - t0
        with self.lock:  # the monitor updates info only while holding the lock
            self.active.pop(p.pid, None)
            cpu_proc = sum(info["cpu"].values())
        try:
            os.killpg(p.pid, signal.SIGKILL)  # leftovers of the group, if any
        except ProcessLookupError:
            pass
        for s in d.iterdir():  # GAMS scratch dirs left behind by an interrupted job
            if s.is_dir() and re.fullmatch(r"225[a-z]+", s.name):
                shutil.rmtree(s, ignore_errors=True)
        with self.lock:
            self.done.append(name)
        if info["reason"] == "driver stop":
            self.log(f"abandon {name} attempt {k} (driver stopping; not counted, rerun on restart)")
            return

        cpu_wait4 = ru.ru_utime + ru.ru_stime
        cpu = max(cpu_wait4, cpu_proc)
        ratio = cpu / wall if wall > 0 else 0.0
        tr = parse_trace(d / "trace.trc")
        reason = info["reason"]
        if reason is None:
            end = "completed" if tr else "ended without trace record"
        elif reason.startswith("hard timeout"):
            end = "hard timeout"
        else:
            end = reason
        if end not in ("completed", "hard timeout"):
            valid, why = False, f"end: {end}"
        elif end == "completed" and wall < SHORT_RUN_S and tr.get("SolverStatus", "").strip() != "3":
            valid, why = True, (f"completed within {SHORT_RUN_S} s (wall {wall:.1f} s) before the time limit: "
                                f"cpu/wall {ratio:.3f} not tested")
        elif ratio >= self.a.min_cpu_ratio:
            valid, why = True, f"cpu/wall {ratio:.3f} >= {self.a.min_cpu_ratio:g}"
        else:
            valid, why = False, f"cpu/wall {ratio:.3f} < {self.a.min_cpu_ratio:g}"
        n = info["n_samples"]
        meta.update({"end_utc": utc(), "wall_s": round(wall, 2), "cpu_s": round(cpu, 2),
                     "cpu_s_wait4": round(cpu_wait4, 2), "cpu_s_proc": round(cpu_proc, 2),
                     "cpu_over_wall": round(ratio, 4),
                     "return_code": p.returncode, "kill_reason": reason, "kill_stage": info["stage"],
                     "end_kind": end, "has_trace": bool(tr), "valid": valid, "validity": why,
                     "peak_group_rss_mb": round(info["peak_rss"], 1),
                     "peak_group_swap_mb": round(info["peak_swap"], 1),
                     "peak_group_rss_plus_swap_mb": round(info["peak"], 1),
                     "max_single_process_rss_mb": round(ru.ru_maxrss / 1024, 1),
                     "load1_mean": round(info["load_sum"] / n, 1) if n else None,
                     "machine_swap_used_max_gb": round(info["machine_swap_max"], 2),
                     "machine_mem_available_min_gb": None if info["avail_min"] is None
                     else round(info["avail_min"], 2),
                     "loadavg_end": os.getloadavg()})
        self.log(f"end {name} attempt {k} rc {p.returncode} wall {wall:.0f}s cpu/wall {ratio:.3f} "
                 f"ms {tr.get('ModelStatus')} ss {tr.get('SolverStatus')} obj {tr.get('ObjectiveValue')} "
                 f"objest {tr.get('ObjectiveValueEstimate')} end {end!r} valid {valid} ({why})")
        if valid:
            meta.update({"finished": True, "attempts_total": k, "kept_best": False})
            write_json(d / "run.json", meta)
            return
        write_json(d / "run.json", meta)  # finished stays false until archived or kept
        self.archive_attempt(d, name, k)
        if k <= self.a.max_retries:
            with self.lock:
                self.queue.append((inst, solver))
            self.log(f"requeue {name} for attempt {k + 1} of {self.a.max_retries + 1}")
        else:
            self.keep_best(name)

    def archive_attempt(self, d, name, k):
        dest = self.archive / f"{name}__a{k}"
        shutil.move(str(d), str(dest))
        self.log(f"archive {name} attempt {k} -> {dest.relative_to(self.out)}")

    def keep_best(self, name):
        """All attempts used: copy the best archived attempt back to runs/ and mark it."""
        atts = [(read_json(p / "run.json"), p) for p in self.attempts(name)]
        meta, src = max(atts, key=lambda x: best_key(x[0]))
        d = self.runs / name
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(src, d)
        meta.update({"finished": True, "attempts_total": len(atts), "kept_best": True,
                     "validity": f"INVALID after {len(atts)} attempts; kept attempt {meta.get('attempt')} "
                                 f"({meta.get('validity')})"})
        write_json(d / "run.json", meta)
        self.log(f"keep {name}: {meta['validity']}")

    # ---------------------------------------------------------------- monitor
    def cannot_reach_ratio(self, cpu, el):
        """True if CPU/wall stays below --min-cpu-ratio whatever happens from now on (see Limits)."""
        w_max = self.a.reslim + self.a.hard_extra_s + INT_GRACE_S + TERM_GRACE_S
        return (cpu + 10 + 1.02 * max(0.0, w_max - el)) / w_max < self.a.min_cpu_ratio

    def signal_group(self, pgid, info, sig, reason=None, pid=None):
        """Send sig to the run's process group, or only to process pid if given."""
        target = f"pgid {pgid}"
        try:
            if pid:
                target += f", only pid {pid} ({Path(f'/proc/{pid}/comm').read_text().strip()})"
                os.kill(pid, sig)
            else:
                os.killpg(pgid, sig)
        except (ProcessLookupError, FileNotFoundError):
            return  # gone since the sample; the next monitor pass decides again
        if reason and info["reason"] is None:
            info["reason"] = reason
        info["stage"] += 1
        info["t_stage"] = time.monotonic()
        self.log(f"signal {signal.Signals(sig).name} to {info['name']} ({target}): {info['reason']}")

    def monitor(self):
        last_progress = 0.0
        last_load = -1e9
        lp = self.out / "machine_load.csv"
        if not lp.exists():
            lp.write_text("utc,load1,load5,load15,mem_available_gb,swap_used_gb,our_running_runs,"
                          "our_rss_gb,our_swap_gb\n")
        while True:
            now = time.monotonic()
            with self.lock:
                act = dict(self.active)
            smp = sample_groups(list(act))
            avail, swap_used = meminfo_gb()
            load1 = os.getloadavg()[0]
            with self.lock:
                for g, info in act.items():
                    s = smp[g]
                    info["rss"], info["swap"] = s["rss"], s["swap"]
                    info["cpu"].update(s["cpu"])
                    info["peak_rss"] = max(info["peak_rss"], s["rss"])
                    info["peak_swap"] = max(info["peak_swap"], s["swap"])
                    info["peak"] = max(info["peak"], s["rss"] + s["swap"])
                    info["load_sum"] += load1
                    info["n_samples"] += 1
                    info["machine_swap_max"] = max(info["machine_swap_max"], swap_used)
                    info["avail_min"] = avail if info["avail_min"] is None else min(info["avail_min"], avail)
            for g, info in act.items():
                el = now - info["t0"]
                cpu_now = smp[g]["cpu"]
                solver = max(cpu_now, key=cpu_now.get)[0] if cpu_now else None  # busiest live process
                if info["stage"] == 0:
                    if self.stop.is_set():
                        self.signal_group(g, info, signal.SIGKILL, "driver stop")
                    elif el > self.a.reslim + self.a.hard_extra_s:
                        self.signal_group(g, info, signal.SIGINT, pid=solver,
                                          reason=f"hard timeout {self.a.reslim + self.a.hard_extra_s} s")
                    elif info["rss"] + info["swap"] > self.a.mem_cap_gb * 1024:
                        self.signal_group(g, info, signal.SIGINT, pid=solver,
                                          reason=f"memory cap: group RSS+swap {info['rss'] + info['swap']:.0f} MB "
                                          f"> {self.a.mem_cap_gb:g} GB")
                    elif self.cannot_reach_ratio(cpu := sum(info["cpu"].values()), el):
                        self.signal_group(g, info, signal.SIGINT, pid=solver,
                                          reason=f"low cpu share: cpu {cpu:.0f} s at wall {el:.0f} s, cpu/wall cannot "
                                          f"reach {self.a.min_cpu_ratio:g}")
                elif info["stage"] == 1 and now - info["t_stage"] > INT_GRACE_S:
                    self.signal_group(g, info, signal.SIGTERM)
                elif info["stage"] == 2 and now - info["t_stage"] > TERM_GRACE_S:
                    self.signal_group(g, info, signal.SIGKILL)
            if now - last_progress > 30:
                self.write_progress(act, avail, swap_used)
                if now - last_load > 60:
                    with open(lp, "a") as f:
                        la = os.getloadavg()
                        f.write(f"{utc()},{la[0]:.2f},{la[1]:.2f},{la[2]:.2f},{avail:.2f},{swap_used:.2f},"
                                f"{len(act)},{sum(i['rss'] for i in act.values()) / 1024:.2f},"
                                f"{sum(i['swap'] for i in act.values()) / 1024:.2f}\n")
                    last_load = now
                last_progress = now
            if self.finished_all.is_set() and not act:
                self.write_progress({}, avail, swap_used)
                return
            time.sleep(5)

    def write_progress(self, act, avail, swap_used):
        now = time.monotonic()
        with self.lock:
            queued = list(self.queue) + list(self.pending)
            waiting = self.waiting
        fin = [d.name for d in sorted(self.runs.iterdir()) if d.is_dir() and read_json(d / "run.json").get("finished")]
        R, H = self.a.reslim, self.a.reslim + self.a.hard_extra_s
        exp_s, worst_s = R + 30, H + INT_GRACE_S + TERM_GRACE_S
        exp_left = len(queued) * exp_s + sum(max(0.0, exp_s - (now - i["t0"])) for i in act.values())
        worst_left = len(queued) * worst_s + sum(max(0.0, worst_s - (now - i["t0"])) for i in act.values())
        n_arch = len(list(self.archive.iterdir()))
        L = [f"updated {utc()}  driver pid {os.getpid()}  out {self.out}",
             f"total {self.total}  finished {len(fin)}  running {len(act)}  queued {len(queued)} "
             f"(of which waiting for admission {len(queued) - len(self.queue)})  archived invalid attempts {n_arch}",
             f"settings: jobs {self.a.jobs}, reslim {R} s, hard timeout {H} s, min cpu/wall "
             f"{self.a.min_cpu_ratio:g}, max retries {self.a.max_retries}, admission load1 <= "
             f"{self.a.max_load:g} and MemAvailable >= {self.a.min_mem_gb:g} GB",
             f"machine MemAvailable {avail:.1f} GB  swap used {swap_used:.1f} GB  "
             f"loadavg {tuple(round(x, 2) for x in os.getloadavg())}",
             f"rough remaining time without retries or admission waits: expected "
             f"{exp_left / self.a.jobs / 3600:.1f} h (every run to reslim + 30 s), worst case "
             f"{worst_left / self.a.jobs / 3600:.1f} h (every run to the hard timeout and full escalation)",
             ("admission: " + (f"{waiting[0]} waiting {now - waiting[1]:.0f} s ({waiting[2]})" if waiting
                               else "not waiting")),
             "", "running:"]
        for g, i in sorted(act.items(), key=lambda x: x[1]["t0"]):
            el = now - i["t0"]
            cpu = sum(i["cpu"].values())
            L.append(f"  {i['name']:28s} a{i['attempt']} pgid {g:7d}  elapsed {el:7.0f} s  cpu {cpu:7.0f} s "
                     f"({cpu / el if el > 0 else 0:4.2f})  rss {i['rss'] / 1024:5.2f} GB  "
                     f"swap {i['swap'] / 1024:5.2f} GB  peak rss+swap {i['peak'] / 1024:5.2f} GB"
                     + (f"  INTERRUPTING ({i['reason']})" if i["stage"] else ""))
        L += ["", "finished (all sessions):"]
        for n in fin:
            m = read_json(self.runs / n / "run.json")
            tr = parse_trace(self.runs / n / "trace.trc")
            L.append(f"  {n:28s} a{m.get('attempt', '?')}/{m.get('attempts_total', '?')} "
                     f"{'valid  ' if m.get('valid') else 'INVALID'} wall {m.get('wall_s', 0):6.0f} s "
                     f"cpu/wall {m.get('cpu_over_wall') or 0:5.3f}  ms {tr.get('ModelStatus', '-'):>2s} "
                     f"ss {tr.get('SolverStatus', '-'):>2s}  obj {tr.get('ObjectiveValue', '-'):>20s}  "
                     f"objest {tr.get('ObjectiveValueEstimate', '-'):>20s}"
                     + (f"  kill: {m['kill_reason']}" if m.get("kill_reason") else ""))
        tmp = self.out / "progress.tmp"
        tmp.write_text("\n".join(L) + "\n")
        tmp.replace(self.out / "progress.txt")

    # ---------------------------------------------------------------- queue and restart
    def worker(self):
        while not self.stop.is_set():
            with self.lock:
                if not self.queue:
                    return
                task = self.queue.pop(0)
                self.pending.append(task)
            inst, solver = task
            adm = self.admit(f"{inst}__{solver}")
            with self.lock:
                self.pending.remove(task)
            if adm is None:
                return
            try:
                self.run_one(inst, solver, adm)
            except Exception as e:  # keep the batch going; the run stays unfinished
                self.log(f"ERROR {inst}__{solver}: {e!r}")

    def kill_leftovers(self, d, meta):
        """Kill processes of an unfinished run that survived a killed driver (same group, cwd in d)."""
        g = meta.get("pgid")
        if not g:
            return
        for p in os.listdir("/proc"):
            if not p.isdigit():
                continue
            try:
                with open(f"/proc/{p}/stat") as f:
                    st = f.read()
                pgrp = int(st[st.rfind(")") + 2:].split()[2])
                cwd = os.readlink(f"/proc/{p}/cwd")
            except OSError:
                continue
            if pgrp == g and cwd.startswith(str(d)):
                os.killpg(g, signal.SIGKILL)
                self.log(f"killed leftover process group {g} of {d.name} (driver had been killed)")
                time.sleep(1)
                return

    def main(self):
        self.queue = []
        skipped = 0
        for inst, solver in self.tasks:
            name = f"{inst}__{solver}"
            d = self.runs / name
            meta = read_json(d / "run.json")
            if meta.get("finished"):
                skipped += 1
                continue
            if d.exists():
                self.kill_leftovers(d, meta)
                if meta.get("end_utc") and meta.get("attempt"):  # ended invalid, archiving interrupted
                    self.archive_attempt(d, name, meta["attempt"])
                else:
                    shutil.rmtree(d)
                    self.log(f"removed unfinished {name} (stopped by a driver stop; not counted)")
            if len(self.attempts(name)) > self.a.max_retries:
                self.keep_best(name)
                skipped += 1
                continue
            self.queue.append((inst, solver))
        (self.out / "driver.pid").write_text(f"{os.getpid()}\n")
        self.log(f"driver start pid {os.getpid()} tasks {self.total} queued {len(self.queue)} skipped(finished) "
                 f"{skipped} jobs {self.a.jobs} reslim {self.a.reslim} hard timeout "
                 f"{self.a.reslim + self.a.hard_extra_s} s int grace {INT_GRACE_S} s mem_cap(rss+swap) "
                 f"{self.a.mem_cap_gb:g} GB min cpu/wall {self.a.min_cpu_ratio:g} (not tested for runs that end "
                 f"before the time limit within {SHORT_RUN_S} s) "
                 f"max retries {self.a.max_retries} admission load1 <= {self.a.max_load:g}, MemAvailable >= "
                 f"{self.a.min_mem_gb:g} GB")

        def on_signal(sig, _frame):
            self.log(f"driver got {signal.Signals(sig).name}; stopping, active runs are killed and stay unfinished")
            self.stop.set()
        signal.signal(signal.SIGTERM, on_signal)
        signal.signal(signal.SIGINT, on_signal)
        mon = threading.Thread(target=self.monitor, daemon=True)
        mon.start()
        ws = [threading.Thread(target=self.worker) for _ in range(self.a.jobs)]
        for w in ws:
            w.start()
        for w in ws:
            while w.is_alive():
                w.join(timeout=1)
        self.finished_all.set()
        mon.join(timeout=60)
        self.log(f"driver end; attempts ended this session: {len(self.done)}; stop requested: {self.stop.is_set()}")


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=".", help="output folder relative to this script (runs/ go inside)")
    ap.add_argument("--instances", nargs="*", help="subset of instances (default: instances.txt)")
    ap.add_argument("--solvers", nargs="*", default=SOLVERS, choices=SOLVERS)
    ap.add_argument("--reslim", type=int, default=3600)
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--mem-cap-gb", type=float, default=8.0, help="cap on a run's resident + swapped memory")
    ap.add_argument("--hard-extra-s", type=int, default=600,
                    help="hard wall-clock timeout is reslim + this (only lowered for testing the guard)")
    ap.add_argument("--min-cpu-ratio", type=float, default=0.9, help="validity: CPU time / wall time")
    ap.add_argument("--max-retries", type=int, default=2, help="reruns of an invalid attempt")
    ap.add_argument("--max-load", type=float, default=30.0, help="admission: 1-minute load average at most this")
    ap.add_argument("--min-mem-gb", type=float, default=8.0, help="admission: MemAvailable at least this")
    return ap.parse_args()


if __name__ == "__main__":
    Driver(parse_args()).main()
