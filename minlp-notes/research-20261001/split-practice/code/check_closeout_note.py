"""Check closeout sections, local links and headline counts; no experiments."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
note = (ROOT / "note.md").read_text()
assert not re.search(r"^pending\s*$", note, re.M)
assert '(Sections marked "pending"' not in note
assert "revised after review round 2; not re-reviewed" in note
for heading in (
    "## Summary", "## 8. Split separation at the stored points",
    "### 9.1 Optimal values of the two time-limited instances",
    "## 12. Conclusions for solvers", "## Checks actually run",
    "## Limits", "## Open questions", "## Revision after review round 1",
    "## Revision after review round 2",
):
    assert note.count(heading) == 1, heading
links = re.findall(r"\]\(([^)]+)\)", note)
for target in links:
    if "://" not in target:
        assert (ROOT / target.split("#")[0]).exists(), target
r = json.loads((ROOT / "logs/audit_closeout.json").read_text())
assert r["completeness"]["unique_points"] == 123
assert sum(g["complete"] for g in r["separation"].values()) == 103
assert sum(g["thm3"]["returned"] for g in r["separation"].values()) == 111
assert sum(g["thm3"]["q_near_quarter"] for g in r["separation"].values()) == 107
assert sum(g["thm3"]["bad_at_raw_point"] for g in r["separation"].values()) == 102
assert r["points"]["instances"] == 187 and len(r["points"]["face_failures"]) == 10
assert r["raw_ratio_check"]["meaningful_lost"] == []
assert r["hard"]["completed_enum"] == 80 and r["hard"]["first_run_enum_max_difference"] == 0
certificates = [json.loads(line) for line in (ROOT / "logs/ratio_certificates_r1.jsonl").read_text().splitlines()]
assert sum(c["certified"] and not c["finished"] for c in certificates) == 17
assert sum(c["certified"] or c["finished"] for c in certificates) == 120
rerun = [json.loads(line) for line in (ROOT / "logs/thm3_r1.jsonl").read_text().splitlines()]
assert len(rerun) == 113 and len({c["file"] for c in rerun}) == 113
assert all("error" not in c for c in rerun)
assert all(c["thm3"]["complete"] == (c["thm3"]["first_complete"] and c["thm3"]["second_complete"]) for c in rerun)
assert "120 of 123" in note
assert "| DM60 | 18 | 2/4/5 | 9.91 | 12 / 98.4 |" in note
assert "5168" in note and "2057 of 2688" in note
assert "being reconciled" not in note and "reconciled below" not in note
print("All required sections finalized; header status checked.")
print(f"All {len(links)} local Markdown links resolve.")
print("Historical audit checks and revised counts/flags agree with their saved records.")
print("No project-wide verification or CI checks were performed.")
