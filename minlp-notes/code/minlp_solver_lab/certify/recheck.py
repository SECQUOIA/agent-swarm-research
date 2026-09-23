"""Read-only, resumable replay of every historical certificate record.

Run from any directory with the package on PYTHONPATH. The output is a new
JSONL file, accompanied by a pinned environment/input manifest. Historical
records and certificate artifacts are never rewritten. A timeout includes
both the Python checker and any external checker it launches.
"""
from __future__ import annotations

import argparse
import concurrent.futures
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from .rational_text import parse_rational_text

LAB = Path(__file__).resolve().parents[1]


def fingerprint(path):
    """Hash large proof artifacts with bounded memory."""
    path = Path(path)
    if not path.is_file():
        return {"path": str(path.resolve()), "missing": True}
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"path": str(path.resolve()), "bytes": path.stat().st_size,
            "sha256": digest.hexdigest()}


def exact_comparison(previous, current):
    if previous is None or current is None:
        return "unavailable"
    try:
        before, after = parse_rational_text(str(previous)), parse_rational_text(str(current))
    except (ValueError, ZeroDivisionError):
        return "unavailable"
    return "equal" if before == after else "changed"


def read_results(stream):
    """Recover only an interrupted final JSON line; reject interior damage."""
    stream.seek(0)
    results = {}
    while True:
        start = stream.tell()
        line = stream.readline()
        if not line:
            break
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            if stream.read() or line.endswith("\n"):
                raise ValueError("replay output contains a corrupt complete record")
            stream.seek(start)
            stream.truncate()
            break
        key = record["record_index"]
        if key in results:
            raise ValueError(f"duplicate replay record index {key}")
        results[key] = record
        if not line.endswith("\n"):
            stream.write("\n")
    stream.seek(0, os.SEEK_END)
    return results


def environment_manifest(args):
    paths = sorted((LAB / "certify").glob("*.py")) + sorted((LAB / "lbesh").glob("*.py"))
    paths += [LAB / "pyproject.toml", LAB / "uv.lock"]
    versions = {}
    for package in ("pyomo", "python-flint", "mpmath", "numpy", "sympy"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return {
        "schema": 1, "records": fingerprint(args.records),
        "record_count": sum(bool(line.strip()) for line in args.records.read_text().splitlines()),
        "artifact_root": str(args.outroot.resolve()), "instance_root": str(args.instances.resolve()),
        "python": sys.version, "python_executable": fingerprint(sys.executable),
        "platform": platform.platform(), "package_versions": versions,
        "checker_sources": [fingerprint(path) for path in paths],
        "external_checker": fingerprint(args.viprchk) if args.viprchk else None,
        "timeout_seconds": args.timeout,
    }


def worker(args):
    from certify.driver import check_certificate
    report = check_certificate(str(args.instance), str(args.certdir),
                               viprchk=args.viprchk, verbose=False,
                               vipr_path=str(args.certdir / "master_complete.vipr"),
                               require_vipr=True)
    args.report.write_text(json.dumps(report, default=str))


def replay(index, historical, args, previous):
    start = time.monotonic()
    name = historical["instance"]
    if Path(name).name != name or name in (".", ".."):
        raise ValueError(f"invalid instance identifier: {name!r}")
    certdir = args.outroot / name
    instance = args.instances / f"{name}.py"
    paths = {"instance": instance, "lemma": certdir / "lemma.json",
             "master": certdir / "master.lp", "proof": certdir / "master_complete.vipr"}
    artifacts = {key: fingerprint(path) for key, path in paths.items()}
    if previous is not None:
        if previous["artifacts"] != artifacts:
            raise ValueError(f"artifacts changed since replay of {name}; use a new output")
        return None
    result = {
        "schema": 1, "record_index": index, "instance": name,
        "historical_status": historical.get("status"),
        "historical_checker": historical.get("checker"),
        "historical_viprchk": historical.get("viprchk"),
        "historical_bound": historical.get("certified_bound_original_sense"),
        "artifacts": artifacts, "artifact_bytes": sum(x.get("bytes", 0) for x in artifacts.values()),
        "hash_seconds": time.monotonic() - start,
        "started_utc": datetime.now(timezone.utc).isoformat(),
    }
    missing = [key for key, info in artifacts.items() if info.get("missing")]
    report = {}
    check_start = time.monotonic()
    if missing:
        result.update(status="missing_artifacts", missing=missing)
    else:
        with tempfile.TemporaryDirectory(prefix="minlp-replay-") as temp:
            report_path = Path(temp) / "report.json"
            cmd = [sys.executable, "-m", "certify.recheck", "--worker",
                   "--instance", str(instance), "--certdir", str(certdir), "--report", str(report_path)]
            if args.viprchk:
                cmd += ["--viprchk", args.viprchk]
            env = os.environ.copy()
            env["PYTHONPATH"] = str(LAB) + os.pathsep + env.get("PYTHONPATH", "")
            with (Path(temp) / "worker.log").open("w+") as log:
                process = subprocess.Popen(cmd, cwd=LAB, stdout=log, stderr=log, env=env, start_new_session=True)
                try:
                    returncode = process.wait(timeout=args.timeout)
                    if returncode == 0 and report_path.is_file():
                        report = json.loads(report_path.read_text())
                        result["status"] = "verified" if report.get("ok") else "rejected"
                    else:
                        result.update(status="checker_error", returncode=returncode)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait()
                    result["status"] = "timeout"
                finally:
                    # Also stop descendants left behind by an abnormal worker exit.
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                if result["status"] in ("checker_error", "timeout"):
                    log.seek(0, os.SEEK_END)
                    log.seek(max(0, log.tell() - 4000))
                    result["diagnostic_tail"] = log.read()
    result["checker_seconds"] = time.monotonic() - check_start
    if not missing:
        postcheck_start = time.monotonic()
        after = {key: fingerprint(path) for key, path in paths.items()}
        result["postcheck_hash_seconds"] = time.monotonic() - postcheck_start
        if after != artifacts:
            result["status"] = "artifacts_changed"
            result["artifacts_after"] = after
    result["elapsed_seconds"] = time.monotonic() - start
    result["report"] = report
    bound = report.get("certified_bound_original_sense") if result["status"] == "verified" else None
    result["certified_bound_original_sense"] = bound
    result["sense"] = report.get("sense")
    result["bound_comparison"] = exact_comparison(result["historical_bound"], bound)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=LAB / "results/cert_all.jsonl")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--outroot", type=Path, default=LAB / "results/cert")
    parser.add_argument("--instances", type=Path, default=LAB / "instances/py")
    parser.add_argument("--viprchk", help="optional corroborating external checker executable")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=1200)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    for option in ("instance", "certdir", "report"):
        parser.add_argument(f"--{option}", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(args)
        return
    if args.out is None or args.jobs < 1 or args.timeout <= 0:
        parser.error("--out is required, and --jobs and --timeout must be positive")
    for name in ("records", "out", "outroot", "instances"):
        setattr(args, name, getattr(args, name).resolve())
    if args.out == args.records or (args.out.exists() and os.path.samefile(args.out, args.records)):
        parser.error("output must differ from the historical input")
    if args.viprchk:
        executable = shutil.which(args.viprchk)
        if executable is None:
            parser.error("external checker executable was not found")
        args.viprchk = str(Path(executable).resolve())
    historical = [json.loads(line) for line in args.records.read_text().splitlines() if line.strip()]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = args.out.with_suffix(args.out.suffix + ".manifest.json")
    with args.out.open("a+") as output:
        fcntl.flock(output, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = environment_manifest(args)
        if manifest_path.exists():
            if json.loads(manifest_path.read_text()) != manifest:
                parser.error("replay inputs, code, environment, or settings changed; use a new output")
        else:
            if args.out.stat().st_size:
                parser.error("existing output has no manifest; use a new output")
            with tempfile.NamedTemporaryFile(mode="w", dir=manifest_path.parent, delete=False) as temporary:
                temporary.write(json.dumps(manifest, indent=2) + "\n")
                temporary.flush()
                os.fsync(temporary.fileno())
            os.replace(temporary.name, manifest_path)
        previous = read_results(output)
        if any(index < 0 or index >= len(historical) for index in previous):
            parser.error("output contains a record index outside the historical input")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(replay, index, record, args, previous.get(index))
                       for index, record in enumerate(historical)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is None:
                    continue
                output.write(json.dumps(result, default=str, sort_keys=True) + "\n")
                output.flush()
                os.fsync(output.fileno())
                print(f"{result['instance']}: {result['status']} ({result['elapsed_seconds']:.2f}s)", flush=True)
        print(f"Replay complete: {len(historical)} historical records; {args.out}", flush=True)


if __name__ == "__main__":
    main()
