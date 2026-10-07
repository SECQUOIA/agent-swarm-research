"""Check new import paths and the manifest builder only in the disposable smoke copy."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from finish_paths import ROOT, RESEARCH, OUT
from rebuild_manifest import EXTRA_FILES


def main():
    before = (OUT / "manifest.json").read_bytes()
    tree = Path(json.loads((OUT / "logs/smoke-results.json").read_text())["tree"])
    paths = ["open-instances-scout/hvycrash_check.py", "open-instances-scout/structure.py",
             "treewidth-census/census.py"]
    for path in [RESEARCH / rel for rel in paths] + list((OUT / "tools").glob("*.py")):
        dst = tree / path.relative_to(ROOT)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)
    # The copied Git index and detached HEAD let the inventory query Git without
    # copying objects, committing anything, or accessing the hidden source tree.
    subprocess.run(["git", "init", "-q", str(tree)], check=True)
    index = subprocess.check_output(["git", "rev-parse", "--git-path", "index"], cwd=ROOT, text=True).strip()
    shutil.copy2(ROOT / index, tree / ".git/index")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    (tree / ".git/HEAD").write_text(head + "\n")
    cache = Path("~/.cache/minlplib/minlplib/osil").expanduser()
    sandbox = ["bwrap", "--dev-bind", "/", "/", "--tmpfs", str(ROOT)]
    old = ROOT.with_name("minlp-notes-clean")
    if old.exists():
        sandbox += ["--tmpfs", str(old)]
    sandbox += ["--tmpfs", str(cache.parent), "--ro-bind", str(tree / "osil-cache"), str(cache)]
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"):
        sandbox += ["--setenv", key, "1"]
    sandbox += ["--setenv", "PYTHONDONTWRITEBYTECODE", "1", "--", sys.executable, "-B"]
    research = tree / "research-20260929"
    commands = [
        [str(research / paths[0])],
        ["-c", "import sys; from pathlib import Path; sys.path.insert(0, sys.argv[1]); "
         "import structure, census, osil; assert Path(osil.__file__).resolve() == Path(sys.argv[2]); "
         "assert Path(census.__file__).resolve() == Path(sys.argv[3]); print('relocated imports passed')",
         str(research / "open-instances-scout"), str(tree / EXTRA_FILES[0]),
         str(research / "treewidth-census/census.py")],
        [str(research / "publication/reproduction/tools/rebuild_manifest.py")],
    ]
    records = []
    for args in commands:
        command = sandbox + args
        result = subprocess.run(command, capture_output=True, text=True)
        records.append(dict(argv=command, exit=result.returncode, stdout=result.stdout, stderr=result.stderr))
        assert result.returncode == 0, result.stderr
    manifest = json.loads((research / "publication/reproduction/manifest.json").read_text())
    files = {r["path"]: r for r in manifest["files"]}
    for rel in EXTRA_FILES + ["research-20260929/" + rel for rel in paths]:
        assert files[rel]["sha256"] == hashlib.sha256((tree / rel).read_bytes()).hexdigest(), rel
    assert (OUT / "manifest.json").read_bytes() == before, "Main manifest changed"
    (OUT / "logs/review-r1-relocated-paths.json").write_text(json.dumps(records, indent=2) + "\n")
    print("Relocated hvycrash, scout/census imports and manifest builder passed; main manifest unchanged")


if __name__ == "__main__":
    main()
