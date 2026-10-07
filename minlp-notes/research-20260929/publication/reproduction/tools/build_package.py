"""Inventory saved evidence and package ignored inputs; never run experiments."""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[4])

import gzip
import hashlib
import importlib.metadata
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile

from finish_paths import ROOT, RESEARCH, OUT, SCOPES
from rebuild_manifest import rebuild_manifest


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def relative(text):
    for prefix in ((_PUBLIC_REPO + '-clean/research-20260929'),
                   str(RESEARCH)):
        text = text.replace(prefix, "$R")
    text = text.replace((_PUBLIC_REPO + '-clean/scratch-repro-network'), "$SCRATCH")
    text = text.replace("/tmp/wa_scratch", "$SCRATCH")
    text = text.replace("/tmp/wa_tools", "$R/publication/reproduction/water-audit/tools")
    return text


def measured_seconds(path):
    if not path.exists():
        return None
    m = re.search(r"Elapsed \(wall clock\).*?:\s*([0-9:.]+)\s*$", path.read_text(), re.M)
    if not m:
        return None
    out = 0.0
    for part in m[1].split(":"):
        out = 60 * out + float(part)
    return out


def main():
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    evidence_scopes = SCOPES + ["open-instances-scout"]
    files = sorted({p for scope in evidence_scopes for p in (RESEARCH / scope).rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts and "singular" not in p.parts})
    files.extend([RESEARCH / "treewidth-census/census_merged.json", RESEARCH / "open-instances-summary.md"])
    # Keep only inputs that are absent from Git. All saved outputs remain in place.
    ignored = [p for p in files if str(p.relative_to(ROOT)) not in tracked
               and p.suffix in (".sol", ".osil", ".html")]
    inputs = []
    for p in ignored:
        rel = str(p.relative_to(ROOT))
        record = dict(path=rel, sha256=sha(p), bytes=p.stat().st_size)
        if p.suffix == ".sol" and ".center." not in p.name:
            record["source"] = "https://www.minlplib.org/sol/" + p.name
        elif p.suffix == ".osil":
            record["source"] = "https://www.minlplib.org/osil/" + p.name
        elif p.suffix == ".html":
            record["source"] = "https://www.minlplib.org/" + p.name
        inputs.append(record)
    data = OUT / "inputs"
    data.mkdir(exist_ok=True)
    with (data / "saved-inputs.tar.gz").open("wb") as f:
        with gzip.GzipFile(fileobj=f, mode="wb", mtime=0, filename="") as gz:
            with tarfile.open(fileobj=gz, mode="w|") as tar:
                for record in inputs:
                    p = ROOT / record["path"]
                    info = tarfile.TarInfo(record["path"])
                    info.size = p.stat().st_size
                    info.mode = 0o644
                    tar.addfile(info, io.BytesIO(p.read_bytes()))
    (data / "saved-inputs.json").write_text(json.dumps(inputs, indent=2) + "\n")
    names = {f"{family}{n}" for family, ns in
             [("lnts", [50, 100, 200, 400]), ("camshape", [100, 200, 400, 800]),
              ("chain", [50, 100, 200, 400]), ("catmix", [100, 200, 400, 800])]
             for n in ns}
    names.update(["dtoc5", "lukvle10", "optcdeg2", "hvycrash", "ex6_2_7", "ex6_2_5",
                  "etamac", "pricing050", "pindyck", "ann_cumene_tanh", "eg_int_s",
                  "eg_disc_s", "eg_disc2_s", "powerflow0030p", "powerflow0039p", "powerflow0039r",
                  "methanol50", "rocket100", "rocket200", "rocket400"])
    names.update(f"waterno2_{n:02d}" for n in [2, 3, 4, 6, 9, 12, 18, 24])
    names.update(f"kan_r{r}_h1_n{n}" for r, ns in [(3, [4, 5, 9]), (5, [3, 5, 8])] for n in ns)
    names.update(d["name"] for d in json.loads((RESEARCH / "bound-audit/screen.json").read_text())["pairs"])
    cache = Path("~/.cache/minlplib/minlplib/osil").expanduser()
    models = []
    for name in sorted(names):
        p = cache / (name + ".osil")
        models.append(dict(name=name, path="~/.cache/minlplib/minlplib/osil/" + p.name,
                           sha256=sha(p), bytes=p.stat().st_size,
                           source="https://www.minlplib.org/osil/" + p.name))
    (data / "osil-models.json").write_text(json.dumps(models, indent=2) + "\n")
    evidence_count = rebuild_manifest()
    packages = ["mpmath", "numpy", "scipy", "sympy", "pyscipopt", "cvxpy", "clarabel", "highspy"]
    env = dict(python=sys.version, packages={p: importlib.metadata.version(p) for p in packages})
    from pyscipopt import Model
    model = Model()
    env["scip"] = f"{model.getMajorVersion()}.{model.getMinorVersion()}.{model.getTechVersion()}"
    (OUT / "environment.json").write_text(json.dumps(env, indent=2) + "\n")
    (OUT / "requirements.txt").write_text("\n".join(f"{p}=={env['packages'][p]}" for p in packages) + "\n")
    runs = []
    for family in ["control", "network", "small", "cops"]:
        for p in sorted((OUT / family / "logs").glob("*.meta")):
            text = p.read_text()
            cwd = re.search(r"^cwd:\s*(.*)$", text, re.M)
            cmd = re.search(r"^cmd:\s*(.*)$", text, re.M)
            rc = re.search(r"^(?:exit|rc):\s*(.*)$", text, re.M)
            log = p.with_suffix(".out" if family in ("control", "small") else ".log")
            if not cmd or not cwd or not log.exists():
                continue
            runs.append(dict(id=family + "/" + p.stem, cwd=relative(cwd[1]),
                             command=relative(cmd[1]), exit=int(rc[1]) if rc else None,
                             wall_s=measured_seconds(p.with_suffix(".time")),
                             output=str(log.relative_to(OUT)), sha256=sha(log)))
    for line in (OUT / "water-audit/logs/runs.jsonl").read_text().splitlines():
        d = json.loads(line)
        p = OUT / "water-audit" / d["log"]
        runs.append(dict(id="water-audit/" + d["id"], cwd=relative(d["cwd"]),
                         command=relative(d["command"]), exit=d["exit"], wall_s=d["wall_s"],
                         output=str(p.relative_to(OUT)), sha256=sha(p)))
    (OUT / "commands.json").write_text(json.dumps(runs, indent=2) + "\n")
    audit = json.loads((RESEARCH / "bound-audit/summary.json").read_text())
    pages = json.loads((RESEARCH / "bound-audit/pages.json").read_text())
    count = dict(instances=len(pages), points=sum(len(p["points"]) for p in pages),
                 solver_bounds=sum(len(p["duals"]) for p in pages),
                 invalid_pairs=sum(p["cls"] == "i" for p in audit["pairs"]),
                 invalid_instances=len({p["name"] for p in audit["pairs"] if p["cls"] == "i"}))
    scout = json.loads((RESEARCH / "open-instances-scout/fetched.json").read_text())
    count["scout_candidates"] = len(scout)
    count["scout_open"] = sum(float(p["gap_best"]) > 1e-4 for p in scout)
    (OUT / "logs/saved-evidence-counts.json").write_text(json.dumps(count, indent=2) + "\n")
    print(json.dumps(dict(input_members=len(inputs), archive_bytes=(data / "saved-inputs.tar.gz").stat().st_size,
                          osil_models=len(models), evidence_files=evidence_count, saved_runs=len(runs), audit_counts=count), indent=2))


if __name__ == "__main__":
    main()
