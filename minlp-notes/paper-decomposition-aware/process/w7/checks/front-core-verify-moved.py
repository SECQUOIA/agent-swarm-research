#!/usr/bin/env python3
"""Word-level comparison of the proofs moved in W7 (F-referee-1(a)).

For each label, take the first proof after \\label{label} in the pre-W7 main-text
file and the proof headed "[Proof of <Type>~\\ref{label}]" in the current
appendix file, and print the word-level differences.  Also check that the
statement in the main text is now followed by the pointer sentence.
"""
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "process/w7/sections-before-w7"
NEW = ROOT / "sections"

MOVES = [
    ("thm:cv", "recourse-convex.tex", "appendix-recourse-convex.tex"),
    ("thm:cr-oracle", "recourse-cuts.tex", "appendix-recourse-cuts.tex"),
    ("thm:cr-search", "recourse-cuts.tex", "appendix-recourse-cuts.tex"),
    ("prop:cr-growth", "recourse-cuts.tex", "appendix-recourse-cuts.tex"),
    ("prop:tu-sound", "constraints.tex", "appendix-tu.tex"),
    ("thm:tu-states", "constraints.tex", "appendix-tu.tex"),
    ("thm:tu-approx", "constraints.tex", "appendix-tu.tex"),
    ("thm:cells", "optsets.tex", "appendix-proximal.tex"),
]


def proof_body(text, start):
    """Return the body of the first proof environment at or after start."""
    b = text.index(r"\begin{proof}", start)
    depth, i = 0, b
    pat = re.compile(r"\\(begin|end)\{proof\}")
    for m in pat.finditer(text, b):
        depth += 1 if m.group(1) == "begin" else -1
        if depth == 0:
            body = text[b:m.end()]
            break
    else:
        raise ValueError("unterminated proof")
    # Drop the \begin{proof}[...] header and \end{proof}.
    body = re.sub(r"^\\begin\{proof\}(\[[^\n]*?\])?", "", body)
    body = body[: -len(r"\end{proof}")]
    return body, b


def words(s):
    return s.split()


status = 0
for label, old_file, new_file in MOVES:
    old = (OLD / old_file).read_text()
    new_main = (NEW / old_file).read_text()
    new_app = (NEW / new_file).read_text()
    lab = old.index(r"\label{%s}" % label)
    old_body, _ = proof_body(old, lab)

    hdr = re.search(r"\\begin\{proof\}\[Proof of [A-Za-z]+~\\ref\{%s\}\]" % re.escape(label), new_app)
    if not hdr:
        print(f"== {label}: NO appendix proof header found in {new_file}")
        status = 1
        continue
    new_body, _ = proof_body(new_app, hdr.start())

    # Main text: statement kept, followed by a pointer sentence, no proof.
    nlab = new_main.index(r"\label{%s}" % label)
    env_end = re.compile(r"\\end\{(theorem|proposition|lemma|corollary)\}").search(new_main, nlab)
    after = new_main[env_end.end(): env_end.end() + 200].strip()
    pointer_ok = after.startswith("The proof is in Appendix~\\ref{")
    proof_left = after.startswith(r"\begin{proof}")

    ow, nw = words(old_body), words(new_body)
    sm = difflib.SequenceMatcher(a=ow, b=nw, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print(f"== {label}: {old_file} -> {new_file}: {len(ow)} old words, {len(nw)} new words, "
          f"{len(diffs)} differing spans; header: {hdr.group(0)}")
    print(f"   main text after statement: {after[:90]!r}")
    if not pointer_ok or proof_left:
        print("   !! pointer sentence missing or proof still in the main text")
        status = 1
    for tag, i1, i2, j1, j2 in diffs:
        print(f"   {tag}: OLD[{' '.join(ow[i1:i2])}]  NEW[{' '.join(nw[j1:j2])}]")
sys.exit(status)
