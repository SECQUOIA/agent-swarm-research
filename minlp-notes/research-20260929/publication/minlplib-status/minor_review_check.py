"""Recheck the four minor round-2 findings using stored evidence only."""

import collections
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
from fractions import Fraction


TRACK = Path(__file__).resolve().parent
REVIEW = TRACK.parent / "reviews/minlplib-status-r2"


def run(*args, cwd=None):
    print("Command:", " ".join(map(str, args)), flush=True)
    return subprocess.check_output(args, cwd=cwd, text=True)


def main():
    # Children inherit this limit. All checks run sequentially.
    os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:2])
    print("CPU affinity:", sorted(os.sched_getaffinity(0)))

    print("\nIssue 1: stored Last-Modified counts")
    print(run(sys.executable, str(REVIEW / "code/spotchecks.py")), end="")
    instances = json.loads((TRACK / "data/part_a.json").read_text())["instances"]
    counts = collections.Counter(v["osil"]["last_modified"] for v in instances.values())
    assert len(instances) == 69
    assert sum(n for date, n in counts.items() if "25 Jun 2019" in date) == 61

    print("\nIssue 2: MINLPLib.jl first commit")
    repo = TRACK / "pages/sources/MINLPLib.jl"
    commits = run("git", "log", "--reverse", "--format=%h %ad %s", "--date=short", cwd=repo)
    print(commits.splitlines()[0])
    assert commits.splitlines()[0].startswith("d2ba96c 2017-11-21 ")
    tree = run("git", "ls-tree", "--name-only", "d2ba96c", "instances/", cwd=repo)
    print(tree, end="")
    assert len(tree.splitlines()) == 15
    assert all(f"instances/{name}" in tree.splitlines() for name in ("global", "minlp", "prince"))
    assert "instances/minlp2" not in tree.splitlines()

    print("\nIssue 3: hvycrash bound multisets")
    # Load the reviewer's parser without creating files in the review directory.
    with contextlib.redirect_stdout(io.StringIO()) as output:
        evidence = runpy.run_path(str(REVIEW / "code/hvy_bounds.py"))
    print(output.getvalue(), end="")
    current = TRACK / "pages/models/gms/hvycrash.gms"
    assert current.read_bytes() == Path(evidence["C"]).read_bytes()
    old = evidence["bounds"](evidence["P"])
    new = evidence["bounds"](current)
    assert (len(old), len(new)) == (203, 202)
    before = collections.Counter(tuple(v) for v in old.values())
    after = collections.Counter(tuple(v) for v in new.values())
    assert before - after == {("0.005", "0.005"): 1, ("0.005", "6.2881854"): 51}
    assert after - before == {("0", "6.2831854"): 51}
    shift = Fraction("0.005")
    assert Fraction("6.2881854") - Fraction("6.2831854") == shift
    assert Fraction("0.005") - Fraction("0") == shift
    print("Both endpoints shift by exactly 0.005; one extra variable is fixed at 0.005.")
    print("Equivalence was not checked.")

    print("\nIssue 4: listing equality")
    files = sorted((TRACK / "pages/wayback/instpages").glob("*.full.html"))
    assert len(files) == 30
    result = run(sys.executable, str(REVIEW / "code/listing_check.py"), *map(str, files))
    records = [json.loads(line) for line in result.splitlines()]
    complete = [r for r in records if r["complete"]]
    cut = [r for r in records if not r["complete"]]
    assert len(complete) == 29 and len(cut) == 1
    for r in complete:
        assert not r["identical_exact"] and r["identical_mod_trailing_ws"]
        assert r["listing_lines"] == r["gms_lines"] + 1
        current = TRACK / "pages/models/gms" / (r["name"] + ".gms")
        reviewer_copy = REVIEW.parent / "minlplib-status-r1/dl/gms" / current.name
        assert current.read_bytes() == reviewer_copy.read_bytes()
    assert cut[0]["cut_text_is_prefix"]
    assert (cut[0]["complete_lines"], cut[0]["complete_chars_incl_newlines"]) == (23479, 1039259)
    print("29 complete listings equal the current GMS apart from boundary newlines;")
    print("each has one extra trailing newline. The cut capture is a matching prefix.")

    print("\nIssue 4: stored faclay75 CDX entries")
    rows = [line.split() for line in (REVIEW / "dl/cdx_domain_to2018.txt").read_text().splitlines()]
    rows = sorted(r for r in rows if len(r) >= 3 and r[2] == "200" and "faclay75" in r[1])
    for row in rows:
        print(" ".join(row))
    for suffix, timestamp in (("/faclay75.html", "20180526153903"),
                              ("/lp/faclay75.lp", "20180529055921"),
                              ("/pip/faclay75.pip", "20180529055947"),
                              ("/gms/faclay75.gms", "20180529060121")):
        assert any(r[0] == timestamp and r[1].endswith(suffix) for r in rows)
    print("\nAll four minor findings confirmed. No disagreement with round 2.")


if __name__ == "__main__":
    main()
