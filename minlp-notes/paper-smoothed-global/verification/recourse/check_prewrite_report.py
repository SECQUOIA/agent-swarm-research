"""Check the recourse prewriting report's local document structure."""

from pathlib import Path
import re


paper_root = Path(__file__).resolve().parents[2]
report = paper_root / "evidence/reviews/prewrite-recourse-sol.md"
text = report.read_text()

assert not any(line.rstrip() != line for line in text.splitlines())
assert text.count(r"\(") == text.count(r"\)")
assert text.count(r"\[") == text.count(r"\]")
assert text.count(chr(96) * 3) % 2 == 0
links = re.findall(r"\]\(([^)]+)\)", text)
for target in links:
    assert (report.parent / target.split("#", 1)[0]).exists(), target
assert not any(control in text for control in ("\x0c", "\x08", "\x0b"))

print(
    f"PASS: report-only structure; {len(links)} local links, "
    f"{text.count(chr(92) + '(')} inline math pairs, "
    f"{text.count(chr(92) + '[')} display pairs."
)
