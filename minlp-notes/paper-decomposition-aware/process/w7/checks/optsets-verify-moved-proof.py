#!/usr/bin/env python3
"""Word-level comparison of the proof of thm:cells before and after W7.

Old: the proof block that follows \\label{thm:cells} in
process/w7/sections-before-w7/optsets.tex.
New: the block opened by \\begin{proof}[Proof of Theorem~\\ref{thm:cells}] in
sections/appendix-proximal.tex.
Prints the token counts and every differing token span (none expected).
"""
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "process/w7/sections-before-w7/optsets.tex"
NEW = ROOT / "sections/appendix-proximal.tex"


def proof_body(text, start_pattern):
    start = re.search(start_pattern, text)
    if not start:
        sys.exit(f"start pattern not found: {start_pattern}")
    begin = text.index("\\begin{proof}", start.start())
    body_start = text.index("\n", begin) + 1  # skip the \begin{proof}[...] line
    end = text.index("\\end{proof}", body_start)
    return text[body_start:end]


old = proof_body(OLD.read_text(), r"\\label\{thm:cells\}")
new = proof_body(NEW.read_text(), r"\\begin\{proof\}\[Proof of Theorem~\\ref\{thm:cells\}\]")

old_tokens, new_tokens = old.split(), new.split()
print(f"old tokens: {len(old_tokens)}, new tokens: {len(new_tokens)}")
diffs = [op for op in difflib.SequenceMatcher(a=old_tokens, b=new_tokens, autojunk=False).get_opcodes()
         if op[0] != "equal"]
for tag, i1, i2, j1, j2 in diffs:
    print(f"{tag}: old {' '.join(old_tokens[i1:i2])!r} -> new {' '.join(new_tokens[j1:j2])!r}")
print("IDENTICAL" if not diffs else f"{len(diffs)} differing span(s)")

# Labels and refs used by the moved proof, for the context check.
print("refs in moved proof:", sorted(set(re.findall(r"\\(?:eq)?ref\{([^}]*)\}", new))))
print("labels in moved proof:", re.findall(r"\\label\{([^}]*)\}", new))
