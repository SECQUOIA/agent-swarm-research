"""Index stored eg_disc2_s evidence without running scientific scripts."""
import hashlib
import json
import re

from finish_paths import RESEARCH, OUT

TRACK = "publication/eg-recheck"
REVIEW = "publication/reviews/eg-recheck-r1"
CERTIFIER = "reviews/eg-retry-review-checks"
OSIL = "~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil"
PRODUCER = "open-instances-wave3/eg/retry"
RECORD_INPUTS = [OSIL, "open-instances-wave3/sol/eg_disc2_s.p1.sol",
                 "open-instances-wave2/small/ev.py"]
RECORD_INPUTS += [f"{PRODUCER}/{name}.py" for name in ("egbb", "egfast", "egtm", "egdata")]
RECORD_INPUTS += ["open-instances-wave3/kan/kan_iv.py",
                  "open-instances-wave3/eg/eg_model.py",
                  "reviews/open-instances-verification/osilx.py"]
NCH = (4, 5, 6, 7, 7, 5, 3, 1)
THETA = "5.642100574331458"
EXPECTED = dict(threshold=THETA, leaves=1114361, certified=1114361,
                failures=0, processed_boxes=1152830, parts=8, chunks=38,
                all_leaf_assumptions=["A1", "A2"],
                coverage="exact guillotine proof over all eight parts and the OSIL domain",
                interval_sample_leaves=10404, interval_sample_failures=0,
                interval_sample_scope="parts 0 and 2–7; includes the 300 tightest per part; no libm assumption")


def evidence_paths():
    scripts = [f"{TRACK}/{name}.py" for name in
               ("recheck_leaves", "margin_cert", "summarize", "check_copy", "check_independence")]
    scripts += [f"{CERTIFIER}/{name}.py" for name in ("indep_cert", "gms_model", "record_run")]
    scripts += [f"{REVIEW}/{name}.py" for name in
                ("own_bookkeeping", "own_cover", "own_model", "cmp_model", "own_sample", "own_ia", "indep_repro")]
    inputs = [f"{CERTIFIER}/data/eg_disc2_s.gms"] + RECORD_INPUTS
    inputs += [f"{REVIEW}/minF_p{k}.npy" for k in (0, 2, 3, 4, 5, 6, 7)]
    inputs += [f"{TRACK}/rec/rec_disc2_p{k}.npz" for k in range(8)]
    inputs += [f"{REVIEW}/leaves_p{k}.npz" for k in range(8)]
    outputs = [f"{TRACK}/res/p{k}_c{c}.npz" for k, n in enumerate(NCH) for c in range(n)]
    outputs += [f"{TRACK}/logs/cert_p{k}_c{c}.log" for k, n in enumerate(NCH) for c in range(n)]
    outputs += [f"{TRACK}/logs/{name}.log" for name in ("summarize", "compare_logs", "check_copy", "check_independence")]
    outputs += [f"{REVIEW}/logs/{name}.log" for name in
                ("own_bookkeeping", "own_cover", "cmp_model", "indep_repro", "own_sample_A", "own_sample_B", "own_sample_C")]
    outputs += [str(p.relative_to(RESEARCH)) for label in "ABC"
                for p in sorted((RESEARCH / REVIEW).glob(f"sample_{label}_p*.npz"))]
    outputs += [f"{TRACK}/report.md", "publication/reviews/eg-recheck-review-r1.md"]
    return scripts, inputs, outputs


def update_command_index():
    """Preserve other historical commands; replace this track's records on rebuild."""
    path = OUT / "commands.json"
    runs = [r for r in json.loads(path.read_text()) if not r["id"].startswith("eg-recheck/")]

    def add(tag, cwd, command, log, inputs, results, expected, historical=False):
        output = "$R/" + log
        runs.append(dict(id="eg-recheck/" + tag, cwd="$R/" + cwd, command=command,
                         output=output, sha256=hashlib.sha256((RESEARCH / log).read_bytes()).hexdigest(),
                         inputs=[p if p.startswith("~/") else "$R/" + p for p in inputs],
                         result_files=["$R/" + p for p in results], expected=expected,
                         execution="historical expensive command; do not repeat for packaging" if historical
                         else "saved-evidence check; run only in a disposable copy"))

    for k, n in enumerate(NCH):
        rec = f"{TRACK}/rec/rec_disc2_p{k}.npz"
        add(f"record-p{k}", CERTIFIER,
            f"python3 record_run.py eg_disc2_s 1e-9 25000 ../../{TRACK}/rec/rec_disc2_p{k}.npz {k} 8",
            f"{TRACK}/logs/rec_disc2_p{k}.log", RECORD_INPUTS, [rec],
            "Recorded run G tree; processed-box counts match the original logs", True)
        for c in range(n):
            log = f"{TRACK}/logs/cert_p{k}_c{c}.log"
            text = (RESEARCH / log).read_text()
            match = re.search(r"certified (\d+)/(\d+); failures (\d+)", text)
            assert match and match[1] == match[2] and match[3] == "0", log
            add(f"cert-p{k}-c{c}", TRACK,
                f"python3 recheck_leaves.py rec/rec_disc2_p{k}.npz eg_disc2_s {THETA} {c} {n} res/p{k}_c{c}.npz",
                log, [rec, f"{CERTIFIER}/data/eg_disc2_s.gms"], [f"{TRACK}/res/p{k}_c{c}.npz"],
                dict(certified=int(match[1]), failures=0, threshold=THETA, assumptions=["A1", "A2"]), True)
    chunks = [f"{TRACK}/res/p{k}_c{c}.npz" for k, n in enumerate(NCH) for c in range(n)]
    add("summarize", TRACK, "python3 summarize.py", f"{TRACK}/logs/summarize.log",
        chunks + ["~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil"], [], EXPECTED)
    add("bookkeeping", REVIEW, "python3 own_bookkeeping.py", f"{REVIEW}/logs/own_bookkeeping.log",
        chunks + [f"{TRACK}/rec/rec_disc2_p{k}.npz" for k in range(8)],
        [f"{REVIEW}/leaves_p{k}.npz" for k in range(8)], "ALL GOOD; boxes and chunk indices agree exactly")
    add("coverage", REVIEW, "python3 own_cover.py", f"{REVIEW}/logs/own_cover.log",
        [f"{REVIEW}/leaves_p{k}.npz" for k in range(8)] + ["~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil"],
        [], "COVERAGE PROVED: all eight parts and the OSIL domain")
    add("model", REVIEW, "python3 cmp_model.py", f"{REVIEW}/logs/cmp_model.log",
        [f"{CERTIFIER}/data/eg_disc2_s.gms", "~/.cache/minlplib/minlplib/osil/eg_disc2_s.osil"],
        [], "MODEL DATA IDENTICAL")
    add("reproduce", REVIEW, "python3 indep_repro.py 100", f"{REVIEW}/logs/indep_repro.log",
        [f"{REVIEW}/leaves_p{k}.npz" for k in range(8)], [],
        "800/800 certified; 502 row margins identical", True)
    for label, args in [("A", "0,2,3 300 1000 0 20000 A"),
                        ("B", "4,5,6,7 300 1000 0 20000 B"),
                        ("C", "0,2,3,4,5,6,7 0 0 200 20000 C")]:
        results = [str(p.relative_to(RESEARCH)) for p in sorted((RESEARCH / REVIEW).glob(f"sample_{label}_p*.npz"))]
        parts = [int(p) for p in args.split()[0].split(",")]
        inputs = [OSIL] + [f"{REVIEW}/leaves_p{k}.npz" for k in parts]
        if label == "C":
            inputs += [f"{REVIEW}/minF_p{k}.npy" for k in parts]
        add("interval-sample-" + label, REVIEW, "python3 own_sample.py " + args,
            f"{REVIEW}/logs/own_sample_{label}.log", inputs,
            results, "Union of A/B/C: 10,404 distinct leaves; zero failures; no libm assumption", True)
    path.write_text(json.dumps(runs, indent=2) + "\n")
    return sum(r["id"].startswith("eg-recheck/") for r in runs)


def check_command_index(result_map):
    row = next(r for r in result_map if r["instance"] == "eg_disc2_s")
    assert row["all_leaf_recheck"]["expected"] == EXPECTED
    mapped = {r["path"] for key in ("scripts", "saved_inputs", "outputs") for r in row[key]}
    assert all(path in mapped for paths in evidence_paths() for path in paths)
    commands = [r for r in json.loads((OUT / "commands.json").read_text())
                if r["id"].startswith("eg-recheck/")]
    assert len(commands) == 54 and len({r["id"] for r in commands}) == 54
    for run in commands:
        output = RESEARCH / run["output"].removeprefix("$R/")
        assert hashlib.sha256(output.read_bytes()).hexdigest() == run["sha256"]
        for path in run["inputs"] + run["result_files"]:
            if path.startswith("$R/"):
                assert (RESEARCH / path.removeprefix("$R/")).is_file(), path
            elif path.startswith("~/"):
                from pathlib import Path
                assert Path(path).expanduser().is_file(), path
    return len(commands)
