"""Run only cheap checks in a relocated copy with the source trees/cache hidden.

Requires Linux bubblewrap and strace. Sequential, one BLAS thread, 90 s per check.
No long experiment is included. Logs and file-open traces are retained.
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import argparse
import difflib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

from finish_paths import ROOT, RESEARCH, OUT

# id, research-relative cwd, arguments, prior saved output
CHECKS = [
    ("lnts50", "open-instances", ["lnts_bound.py", "lnts50"], "control/logs/lnts_bound.out"),
    ("dtoc5", "open-instances", ["dtoc5_bound.py"], "control/logs/dtoc5_bound.out"),
    ("camshape100", "open-instances", ["camshape_bound.py", "100"], "control/logs/camshape_bound.out"),
    ("optcdeg2", "theory-bangbang", ["optcdeg2_qcal_recheck.py"], "control/logs/bb_qcal_recheck.out"),
    ("lukvle10", "reviews/open-instances-verification", ["v_lukvle10_prep.py"], "control/logs/oiv_v_lukvle10_prep.out"),
    ("chain50", "open-instances-wave2/cops", ["chain_bound.py", "1e-14", "50"], "cops/logs/a_chain_bound_50.log"),
    ("catmix800-primal", "open-instances-wave2/cops/explore", ["catmix_primal_snap_eval.py", "800"], "cops/logs/a_catmix_primal_snap_eval_800.log"),
    ("hvycrash", "open-instances-wave2/small", ["hvycrash.py"], "small/logs/A02_hvycrash_cert.out"),
    ("ex6_2_7", "reviews/wave2-small-verification", ["gibbs_bound.py", "ex6_2_7", "0=logs/ex6_2_7_bb_type0_tau6e-15.json"], "small/logs/A16_v_gibbs_bound_ex6_2_7.out"),
    ("ex6_2_5", "reviews/wave2-small-verification", ["gibbs_bound.py", "ex6_2_5", "0=logs/ex6_2_5_bb_type0_tau1e-17.json"], "small/logs/A17_v_gibbs_bound_ex6_2_5.out"),
    ("etamac", "open-instances-wave2/small", ["etamac.py"], "small/logs/A06_etamac_cert.out"),
    ("pricing050", "open-instances-wave2/small", ["pricing050.py"], "small/logs/A08_pricing050_cert.out"),
    ("pindyck", "reviews/pindyck-review-checks", ["final_bound.py"], "small/logs/A28_pr_final_bound.out"),
    ("eg_int_s-primal", "open-instances-wave3/eg/retry", ["verify_primal.py", "eg_int_s", "logs/int9_final.npz"], "small/logs/A35_eg_int_primal.out"),
    ("eg_disc_s-primal", "open-instances-wave3/eg/retry", ["verify_primal.py", "eg_disc_s", "logs/disc9_p1.npz"], "small/logs/A36_eg_disc_primal.out"),
    ("kan_r3_h1_n4", "open-instances-wave3/kan", ["run_kan.py", "kan_r3_h1_n4", "1e-10", "1800"], "network/logs/kan.run_kan.kan_r3_h1_n4.log"),
    ("kan_r3_h1_n4-infeasible", "reviews/wave3-verification", ["kan_infeas_cert.py", "kan_r3_h1_n4"], "network/logs/kan.verifier_infeas.kan_r3_h1_n4.log"),
    ("powerflow0030p", "open-instances-wave3/powerflow", ["pf_cert.py", "powerflow0030p"], "network/logs/pf.pf_cert.powerflow0030p.log"),
    ("ann-primal", "reviews/wave3-verification/ann", ["annv.py", "points"], "network/logs/ann.verifier_points.log"),
    ("waterno2_06-sum", "reviews/waterno2-verification", ["vsum.py", "6"], "water-audit/logs/wall_vsum.log"),
    ("waterno2_06-cellslopes", "reviews/waterno2-cellslopes-review-checks", ["ind_verify_cs.py", "../../open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz", "logs/repro_ind_verify_certB.json", "../../open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json"], "water-audit/logs/w06_ind_verify_certB.log"),
    ("audit-ghg_3veh", "reviews/bound-audit-verification", ["run_kraw.py", "ghg_3veh.p2"], "water-audit/logs/auditv_kraw_ghg_3veh.p2.log"),
    ("audit-sssd22", "reviews/bound-audit-recheck", ["sssd_exact.py", "sssd22-08persp.p4=508748.972"], "water-audit/logs/auditr_sssd_exact.log"),
    ("lnts50-tight", "reviews/open-instances-verification", ["v_lnts.py", "50"], "control/logs/oiv_v_lnts.out"),
    ("powerflow0030p-stored", "reviews/wave3-verification/powerflow", ["run_root.py", "powerflow0030p"], "network/logs/pf.verifier_root_stored.powerflow0030p.log"),
]


# Explicit slices of historical batch logs, using 1-based inclusive line numbers.
# These commands check one instance. Every line in its selected record is required.
REFERENCE_LINES = {
    "lnts50": (1, 1),
    "camshape100": (1, 1),
    "waterno2_06-sum": (1, 1),
    "audit-sssd22": (7, 12),
    "lnts50-tight": (1, 35),
}


def normalize(text, tree):
    # Rebase historical checkout paths for the relocated command.
    for prefix in (str(tree / "research-20260929"), str(RESEARCH),
                   (_PUBLIC_REPO + '-clean/research-20260929')):
        text = text.replace(prefix, "$R")
    # Ignore only named timing values, preserving the fields and all other text.
    keys = "seconds|seconds_bound|seconds_total|sec|time|time_encl|elapsed|wall_s|cpu_s"
    text = re.sub(r"([\"'](?:" + keys + r")[\"']:\s*)[-+0-9.eE]+", r"\1<time>", text)
    text = re.sub(r"\b(?:seconds|elapsed|wall_s)\s*[=:]\s*[-+0-9.eE]+",
                  lambda m: re.sub(r"[-+0-9.eE]+$", "<time>", m[0]), text)
    text = re.sub(r"\b\d+(?:\.\d+)?\s*s\b", "<seconds>", text)
    return text.splitlines()


def compare_output(name, output, reference, tree):
    actual = normalize(output, tree)
    expected = normalize(reference, tree)
    if name in REFERENCE_LINES:
        first, last = REFERENCE_LINES[name]
        expected = expected[first - 1:last]
        assert len(expected) == last - first + 1, f"Short reference for {name}"
    matched = bool(output.strip()) and actual == expected
    return matched, "".join(difflib.unified_diff(
        [line + "\n" for line in expected], [line + "\n" for line in actual],
        fromfile="saved reference", tofile="relocated output"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", type=Path, help="Continue the saved smoke copy without repeating completed checks")
    args = parser.parse_args()
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:4])
    tree = args.resume or Path(tempfile.mkdtemp(prefix="repro-smoke-"))
    manifest = json.loads((OUT / "manifest.json").read_text())
    paths = {r["path"] for r in manifest["files"]}
    paths.update(subprocess.check_output(["git", "ls-files", "research-20260922/scouting/minlplib-open-data"], cwd=ROOT, text=True).splitlines())
    paths.update(str(p.relative_to(ROOT)) for p in OUT.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for rel in sorted(paths) if not args.resume else []:
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    cache = Path(os.path.expanduser("~/.cache/minlplib/minlplib/osil"))
    isolated = tree / "osil-cache"
    isolated.mkdir(exist_ok=True)
    for record in json.loads((OUT / "inputs/osil-models.json").read_text()) if not args.resume else []:
        shutil.copy2(cache / (record["name"] + ".osil"), isolated / (record["name"] + ".osil"))
    r = tree / "research-20260929"
    sandbox = ["bwrap", "--dev-bind", "/", "/", "--tmpfs", str(ROOT)]
    old = ROOT.with_name("minlp-notes-clean")
    if old.exists():
        sandbox += ["--tmpfs", str(old)]
    sandbox += ["--tmpfs", str(cache.parent), "--ro-bind", str(isolated), str(cache)]
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
        sandbox += ["--setenv", key, "1"]
    sandbox += ["--setenv", "PYTHONDONTWRITEBYTECODE", "1"]
    setup = subprocess.run(sandbox + ["--", sys_executable(), str(r / "publication/reproduction/tools/prepare_inputs.py")], capture_output=True, text=True)
    (OUT / "logs/smoke-prepare.log").write_text(setup.stdout + setup.stderr)
    if setup.returncode:
        raise RuntimeError("input restoration failed; see logs/smoke-prepare.log")
    logdir = OUT / "logs/smoke"
    logdir.mkdir(exist_ok=True)
    previous = json.loads((OUT / "logs/smoke-results.json").read_text()) if args.resume else None
    assert previous is None or previous["tree"] == str(tree)
    results = previous["checks"] if previous else []
    progress = json.loads((OUT / "PROGRESS.json").read_text())
    progress["smoke_tree"] = str(tree)
    for name, cwd, args, reference in CHECKS:
        if any(record["id"] == name for record in results):
            continue
        if name == "powerflow0030p-stored":
            # The earlier fresh SDP smoke solve overwrites its certificate.
            # Restore the published multipliers before checking the published bound.
            rel = "open-instances-wave3/logs/powerflow0030p.sdpcert.json"
            shutil.copy2(RESEARCH / rel, r / rel)
        ref = OUT / reference
        if not ref.exists():
            raise FileNotFoundError(ref)
        trace = logdir / (name + ".strace")
        command = sandbox + ["--chdir", str(r / cwd), "--", "strace", "-f", "-yy",
                             "-e", "trace=openat,open", "-o", str(trace),
                             "timeout", "90", sys_executable(), "-u"] + args
        # strace writes into the copy, because the original log directory is hidden.
        local_trace = tree / (name + ".strace")
        command[command.index(str(trace))] = str(local_trace)
        start = time.monotonic()
        completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        wall = time.monotonic() - start
        output = completed.stdout
        (logdir / (name + ".log")).write_text(output)
        shutil.copy2(local_trace, trace)
        successful_main = [line for line in trace.read_text().splitlines()
                           if any(prefix in line for prefix in (str(ROOT), str(old)))
                           and re.search(r"= [0-9]+(?:<|$)", line)]
        matched, difference = compare_output(name, output, ref.read_text(), tree)
        (logdir / (name + ".diff")).write_text(difference)
        record = dict(id=name, cwd="$R/" + cwd, command="python3 -u " + " ".join(args),
                      exit=completed.returncode, wall_s=round(wall, 2),
                      reference=reference, reference_lines=REFERENCE_LINES.get(name), normalized_match=matched,
                      successful_main_tree_opens=len(successful_main),
                      output="logs/smoke/" + name + ".log", trace="logs/smoke/" + name + ".strace")
        results.append(record)
        print(json.dumps(record), flush=True)
        (OUT / "logs/smoke-results.json").write_text(json.dumps(dict(tree=str(tree), checks=results), indent=2) + "\n")
        progress["smoke_completed"] = [d["id"] for d in results]
        progress["background_jobs"] = []
        (OUT / "PROGRESS.json").write_text(json.dumps(progress, indent=2) + "\n")
    # Recheck every saved line on resume without executing completed checks again.
    for record in results:
        matched, difference = compare_output(record["id"], (OUT / record["output"]).read_text(),
                                             (OUT / record["reference"]).read_text(), tree)
        record["normalized_match"] = matched
        (logdir / (record["id"] + ".diff")).write_text(difference)
    (OUT / "logs/smoke-results.json").write_text(json.dumps(dict(tree=str(tree), checks=results), indent=2) + "\n")
    assert len(results) == len(CHECKS)
    if not all(d["exit"] == 0 and d["normalized_match"] and d["successful_main_tree_opens"] == 0
               for d in results):
        raise RuntimeError("Smoke checks failed; see logs/smoke-results.json and logs/smoke/*.diff")


def sys_executable():
    import sys
    return sys.executable


if __name__ == "__main__":
    main()
