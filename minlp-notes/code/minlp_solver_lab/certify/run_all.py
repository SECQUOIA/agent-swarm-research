"""Run the certified-bound pipeline over MINLPLib convex instances.

For each instance: producer (OA + safe cuts + rational master), SCIP exact
with VIPR output, viprcomp, viprchk, independent checker. One JSON line per
instance in a new output file. Existing records and artifacts are refused;
use certify.recheck for resumable verification. Usage:
  uv run python -m certify.run_all --names names.txt --out results/cert_all.jsonl --par 3 --oa-time 300 --scip-time 600
"""
from __future__ import annotations
import argparse, json, os, re, shutil, signal, subprocess, sys, tempfile, time, traceback
from pathlib import Path
from flint import fmpq
from .rational_text import parse_rational_text

LAB = Path(__file__).resolve().parents[1]
os.environ.setdefault("OMP_NUM_THREADS", "1")


def _display_float(text):
    """Optional binary64 display; the exact rational string is authoritative."""
    try:
        return float(parse_rational_text(text))
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def canonicalize_fractions(path):
    """Rewrite every p/q token of a VIPR file in lowest terms (in place)."""
    def canon(match):
        # Proof coefficients can exceed Python's guarded decimal-int length.
        # FLINT parses and prints these rationals without changing that guard.
        return str(fmpq(match.group(0)))
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            with path.open() as source:
                for line in source:
                    output.write(re.sub(r"(?<!\S)(-?\d+)/(\d+)(?!\S)", canon, line))
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)



def run_instance(name, outroot, oa_time, scip_time, threads, scip_bin=None, instances=None):
    from certify.driver import build_certificate, check_certificate
    if Path(name).name != name or name in (".", ".."):
        raise ValueError(f"invalid instance identifier: {name!r}")
    inst = str(Path(instances or LAB / "instances/py") / f"{name}.py")
    def executable(name):
        return str(Path(scip_bin) / name) if scip_bin else name
    outdir = os.path.join(outroot, name)
    rec = dict(instance=name)
    t0 = time.time()
    if os.path.isdir(outdir) and os.listdir(outdir):
        return dict(instance=name, status="output_exists", error="Choose a new artifact root; existing artifacts are preserved.")
    try:
        s = build_certificate(inst, outdir, time_limit=oa_time, threads=threads)
        rec["producer"] = {k: s[k] for k in s if k != "convexity"}
        rec["convex_certified"] = s.get("convexity", {}).get("certified")
        if s.get("status") != "master_written":
            rec["status"] = s.get("status"); rec["time"] = time.time() - t0
            return rec
    except Exception as e:
        rec["status"] = "producer_error"; rec["error"] = repr(e)[:300]; rec["trace"] = traceback.format_exc()[-1200:]
        rec["time"] = time.time() - t0
        return rec
    # SCIP exact: try default settings first, then a "safe" configuration
    # without cutting planes, presolving and propagation (SCIP 10's
    # certificate output for those components does not always verify).
    attempts = [
        ("default", ["set heuristics emphasis off"]),
        ("safe", ["set heuristics emphasis off", "set separating emphasis off", "set presolving emphasis off",
                  "set propagating maxrounds 0", "set propagating maxroundsroot 0"]),
    ]
    rec["scip_attempts"] = []
    verified = False
    checker_report = None
    checker_seconds = 0.0
    for label, settings in attempts:
        cmd = [executable("scip"), "-c", "set exact enable TRUE", "-c", f"set limits time {scip_time}",
               "-c", "set certificate filename master.vipr"]
        for st_ in settings:
            cmd += ["-c", st_]
        cmd += ["-c", "read master.lp", "-c", "optimize", "-c", "quit"]
        for stale in ("master.vipr", "master_complete.vipr"):
            Path(outdir, stale).unlink(missing_ok=True)
        attempt_start = time.time()
        try:
            out = subprocess.run(cmd, cwd=outdir, capture_output=True, text=True, timeout=scip_time + 120).stdout
        except subprocess.TimeoutExpired:
            rec["scip_attempts"].append(dict(label=label, status="timeout")); continue
        open(os.path.join(outdir, f"scip_{label}.log"), "w").write(out)
        m = re.search(r"Exact Dual Bound\s*:\s*(\S+)", out)
        st = re.search(r"SCIP Status\s*:\s*(.*)", out)
        att = dict(label=label, status=(st.group(1).strip() if st else "?"), time=time.time() - attempt_start)
        if m:
            att["exact_dual_bound"] = m.group(1)
        mp = re.search(r"Exact Primal Bound\s*:\s*(\S+)", out)
        if mp:
            att["exact_primal_bound"] = mp.group(1)
        # Complete and check the unchanged proof, including its solution section.
        t2 = time.time()
        try:
            subprocess.run([executable("viprcomp"), "master.vipr"], cwd=outdir, capture_output=True, text=True, timeout=scip_time + 600, check=True)
            # viprchk compares GMP rationals without canonicalizing them, so
            # non-reduced fractions printed by SCIP (e.g. -5/10) make exact
            # equality checks fail; rewrite every fraction in lowest terms
            # (value-preserving) before checking.
            canonicalize_fractions(os.path.join(outdir, "master_complete.vipr"))
            c2 = subprocess.run([executable("viprchk"), "master_complete.vipr"], cwd=outdir, capture_output=True, text=True, timeout=scip_time + 600)
            mm = re.search(r"Successfully verified optimal value range \[(\S+), (\S+?)[\]\)]", c2.stdout)
            ok = c2.returncode == 0 and bool(mm)
            att["viprchk_time"] = time.time() - t2
            att["viprchk"] = "OK" if ok else "FAIL"
            if mm:
                att["verified_range"] = [mm.group(1), mm.group(2)]
            else:
                att["viprchk_tail"] = c2.stdout[-300:]
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError) as error:
            att["viprchk"] = "timeout" if isinstance(error, subprocess.TimeoutExpired) else "error"
            att["viprchk_error"] = repr(error)[:300]
            ok = False
        if ok:
            check_start = time.time()
            try:
                checker_report = check_certificate(
                    inst, outdir, viprchk=executable("viprchk"), verbose=False,
                    vipr_path=os.path.join(outdir, "master_complete.vipr"), require_vipr=True)
                ok = checker_report["ok"]
                att["checker"] = "OK" if ok else "FAIL"
                att["checker_detail"] = [c for c in checker_report["checks"] if c[2] != "OK"]
            except Exception as error:
                ok = False
                checker_report = {"ok": False, "checks": [("checker", "", "FAIL", repr(error)[:300])]}
                att["checker"] = "error"
                att["checker_error"] = repr(error)[:300]
            att["checker_time"] = time.time() - check_start
            checker_seconds += att["checker_time"]
        rec["scip_attempts"].append(att)
        if ok:
            verified = True
            rec["scip_status"] = att["status"]; rec["scip_mode"] = label
            rec["scip_time"] = att["time"]; rec["viprchk_time"] = att["viprchk_time"]
            rec["verified_range"] = att["verified_range"]
            lo = att["verified_range"][0]
            rec["external_master_lb"] = _display_float(lo)
            rec["exact_dual_bound"] = att.get("exact_dual_bound")
            if rec["exact_dual_bound"]:
                rec["exact_dual_bound_float"] = _display_float(rec["exact_dual_bound"])
            os.replace(os.path.join(outdir, "master.vipr"), os.path.join(outdir, "master_verified_raw.vipr"))
            break
        else:
            try:
                os.replace(os.path.join(outdir, "master_complete.vipr"), os.path.join(outdir, f"master_complete_{label}_failed.vipr"))
            except FileNotFoundError:
                pass
    rec["viprchk"] = "OK" if any(a.get("viprchk") == "OK" for a in rec["scip_attempts"]) else "FAIL"
    # The authoritative checker runs inside each attempt, so a rejected default
    # proof can use the safe retry. Reuse its result instead of replaying twice.
    if checker_report is None:
        checker_report = {"ok": False, "checks": [("proof", "", "FAIL", "no completed externally accepted proof")]}
    rec["checker"] = "OK" if verified else "FAIL"
    rec["checker_detail"] = [c for c in checker_report["checks"] if c[2] != "OK"]
    rec["sense"] = checker_report.get("sense")
    rec["certified_bound_original_sense"] = checker_report.get("certified_bound_original_sense") if verified else None
    if rec["certified_bound_original_sense"] is not None:
        approximate = _display_float(rec["certified_bound_original_sense"])
        rec["certified_bound_original_sense_float"] = approximate
        rec["certified_lb"] = None if approximate is None else rec["sense"] * approximate
    rec["checker_time"] = checker_seconds
    rec["time"] = time.time() - t0
    rec["status"] = "verified" if verified else "rejected"
    # remove bulky files? keep vipr (needed as artifact) but drop the incomplete one
    try:
        os.remove(os.path.join(outdir, "master.vipr_ori"))
    except Exception:
        pass
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--outroot", default=str(LAB / "results/cert")); ap.add_argument("--par", type=int, default=3)
    ap.add_argument("--oa-time", type=float, default=300); ap.add_argument("--scip-time", type=float, default=600)
    ap.add_argument("--threads", type=int, default=4); ap.add_argument("--worker", default=None)
    ap.add_argument("--scip-bin", default=os.environ.get("SCIP_EXACT_BIN"), help="directory containing scip, viprcomp and viprchk; otherwise use PATH")
    ap.add_argument("--instances", default=str(LAB / "instances/py"))
    a = ap.parse_args()
    a.outroot = str(Path(a.outroot).resolve())
    a.instances = str(Path(a.instances).resolve())
    if a.scip_bin:
        a.scip_bin = str(Path(a.scip_bin).resolve())
    for tool in ("scip", "viprcomp", "viprchk"):
        if shutil.which(str(Path(a.scip_bin) / tool) if a.scip_bin else tool) is None:
            ap.error(f"executable not found: {tool}; set --scip-bin or PATH")
    if a.par < 1 or min(a.oa_time, a.scip_time, a.threads) <= 0:
        ap.error("parallelism, thread counts, and time limits must be positive")
    if a.worker:
        rec = run_instance(a.worker, a.outroot, a.oa_time, a.scip_time, a.threads, a.scip_bin, a.instances)
        print("RESULT " + json.dumps(rec, default=str)); return
    names = list(dict.fromkeys(l.strip() for l in open(a.names) if l.strip()))
    if any(Path(name).name != name or name in (".", "..") for name in names):
        ap.error("instance names must be plain identifiers without directory components")
    if Path(a.out).exists():
        ap.error("producer output must be new; use certify.recheck to resume certificate replay")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    jobs = names
    print(len(jobs), "jobs", flush=True)
    running = []
    out = open(a.out, "x")
    def launch(n):
        cmd = [sys.executable, "-m", "certify.run_all", "--names", a.names, "--out", "/dev/null", "--outroot", a.outroot,
               "--oa-time", str(a.oa_time), "--scip-time", str(a.scip_time), "--threads", str(a.threads), "--instances", a.instances, "--worker", n]
        if a.scip_bin:
            cmd += ["--scip-bin", a.scip_bin]
        stdout_log, stderr_log = tempfile.TemporaryFile(), tempfile.TemporaryFile()
        process = subprocess.Popen(cmd, stdout=stdout_log, stderr=stderr_log, start_new_session=True)
        return n, process, time.time(), stdout_log, stderr_log
    while jobs or running:
        while jobs and len(running) < a.par:
            running.append(launch(jobs.pop(0)))
        time.sleep(2)
        still = []
        for n, p, t0, stdout_log, stderr_log in running:
            if p.poll() is None:
                if time.time() - t0 > a.oa_time + 3 * a.scip_time + 1800:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    p.wait()
                    stdout_log.close()
                    stderr_log.close()
                    out.write(json.dumps(dict(instance=n, status="killed")) + "\n")
                    out.flush()
                    print("KILLED", n, flush=True)
                else:
                    still.append((n, p, t0, stdout_log, stderr_log))
                continue
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout_log.seek(0)
            rec = None
            for line in stdout_log:
                if line.startswith(b"RESULT "):
                    rec = json.loads(line[7:])
            if rec is None:
                stderr_log.seek(0, os.SEEK_END)
                stderr_log.seek(max(0, stderr_log.tell() - 1500))
                rec = dict(instance=n, status="crash", stderr=stderr_log.read().decode(errors="replace"))
            stdout_log.close()
            stderr_log.close()
            out.write(json.dumps(rec, default=str) + "\n"); out.flush()
            print(f"{n:28s} {rec.get('status'):14s} conv={rec.get('convex_certified')} oa_lb={rec.get('producer',{}).get('oa',{}).get('lb')} cert_lb={rec.get('certified_lb')} viprchk={rec.get('viprchk')} checker={rec.get('checker')} t={rec.get('time',0):.0f}", flush=True)
        running = still


if __name__ == "__main__":
    main()
