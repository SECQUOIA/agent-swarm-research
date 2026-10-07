"""Verify the counts in finding C-writing-2 and compare with corrected replacements."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
lines = (ROOT / "sections" / "intro.tex").read_text().splitlines()

def stats(text):
    return (len(text.split()), len(re.findall(r"\\ref\{", text)), len(re.findall(r"\\cite", text)))

ranges = {"thus": (194, 217), "recourse": (219, 246), "tu": (248, 268), "several": (270, 294)}
orig = {k: "\n".join(lines[a - 1:b]) for k, (a, b) in ranges.items()}
for k, t in orig.items():
    print("original", k, "words/refs/cites =", stats(t))

s = " ".join(lines[193:217])
seg = s[s.find("Section~\\ref{sec:limits} also shows"):s.find("As far as we know")]
print("long sentence words:", len(seg.split()))
print("messages duplicate:", "lim:prop:messages" in " ".join(lines[151:158]),
      "pieces at bag size three" in " ".join(lines[200:206]))

prop = (ROOT / "process" / "w4" / "checks" / "verify-C-writing-2-proposed.tex")
if prop.exists():
    parts = prop.read_text().split("%%%")
    tot = 0
    for p in parts:
        if p.strip():
            print("proposed", p.strip().splitlines()[0][:40], stats(p))
            tot += stats(p)[0]
    print("total words original:", sum(stats(t)[0] for t in orig.values()), "proposed:", tot)
