#!/usr/bin/env python3
"""W7 recourse verifier: word-level checks of the moved proofs and of all
other changes in the recourse group's files.

1. For each moved proof, extract the old proof body (pre-W7 main text) and
   the new proof body (appendix), compare word by word, and print every
   difference.
2. For each owned file, print a word-level diff between the pre-W7 and the
   current version with the moved blocks removed from both sides, so that
   every remaining change is visible.
3. Check that every \\label of the pre-W7 owned files still exists exactly
   once in the current owned files, in the same file.
"""
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "process/w7/sections-before-w7"
NEW = ROOT / "sections"
FILES = [
    "recourse.tex", "recourse-valuefn.tex", "recourse-local.tex",
    "recourse-convex.tex", "recourse-cuts.tex", "recourse-mixed.tex",
    "recourse-balanced.tex", "appendix-recourse-convex.tex",
    "appendix-recourse-cuts.tex",
]

# (label, old file, new file, new proof opener)
MOVES = [
    ("thm:cv", "recourse-convex.tex", "appendix-recourse-convex.tex",
     r"\begin{proof}[Proof of Theorem~\ref{thm:cv}]"),
    ("thm:cr-oracle", "recourse-cuts.tex", "appendix-recourse-cuts.tex",
     r"\begin{proof}[Proof of Theorem~\ref{thm:cr-oracle}]"),
    ("thm:cr-search", "recourse-cuts.tex", "appendix-recourse-cuts.tex",
     r"\begin{proof}[Proof of Theorem~\ref{thm:cr-search}]"),
    ("prop:cr-growth", "recourse-cuts.tex", "appendix-recourse-cuts.tex",
     r"\begin{proof}[Proof of Proposition~\ref{prop:cr-growth}]"),
]


def read(p):
    return p.read_text(encoding="utf-8")


def old_proof_span(text, label):
    """Span of the first proof environment after the statement with label."""
    i = text.index(r"\label{" + label + "}")
    b = text.index(r"\begin{proof}", i)
    e = text.index(r"\end{proof}", b) + len(r"\end{proof}")
    return b, e


def new_proof_span(text, opener):
    b = text.index(opener)
    assert text.count(opener) == 1, opener
    e = text.index(r"\end{proof}", b) + len(r"\end{proof}")
    return b, e


def words(s):
    return s.split()


def show_diff(a, b, ctx=6):
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        n += 1
        pre = " ".join(a[max(0, i1 - ctx):i1])
        post = " ".join(a[i2:i2 + ctx])
        print(f"  [{tag}] ...{pre} <<OLD: {' '.join(a[i1:i2])} | NEW: "
              f"{' '.join(b[j1:j2])}>> {post}...")
    return n


def main():
    ok = True
    old_text = {f: read(OLD / f) for f in FILES}
    new_text = {f: read(NEW / f) for f in FILES}
    old_cut = dict(old_text)
    new_cut = dict(new_text)

    print("== 1. Moved proofs (body after the \\begin{proof} line)")
    for label, of, nf, opener in MOVES:
        ob, oe = old_proof_span(old_text[of], label)
        nb, ne = new_proof_span(new_text[nf], opener)
        old_block = old_text[of][ob:oe]
        new_block = new_text[nf][nb:ne]
        old_body = old_block[len(r"\begin{proof}"):]
        new_body = new_block[len(opener):]
        assert old_block.startswith(r"\begin{proof}" + "\n"), label
        print(f"-- {label}: old {len(words(old_body))} words, "
              f"new {len(words(new_body))} words")
        n = show_diff(words(old_body), words(new_body))
        print(f"   differences: {n}")
        # remove the blocks for the per-file comparison
        old_cut[of] = old_cut[of].replace(old_block, "@@MOVED-" + label + "@@")
        new_cut[nf] = new_cut[nf].replace(new_block, "@@MOVED-" + label + "@@")

    print("\n== 2. Remaining word-level changes per file (moved blocks masked)")
    for f in FILES:
        a, b = words(old_cut[f]), words(new_cut[f])
        if a == b:
            print(f"-- {f}: unchanged")
            continue
        print(f"-- {f}:")
        show_diff(a, b)

    print("\n== 3. Labels")
    lab = re.compile(r"\\label\{([^}]*)\}")
    for f in FILES:
        for l in lab.findall(old_text[f]):
            cnt_same = len(re.findall(r"\\label\{" + re.escape(l) + r"\}",
                                      new_text[f]))
            cnt_all = sum(len(re.findall(r"\\label\{" + re.escape(l) + r"\}",
                                         new_text[g])) for g in FILES)
            if cnt_same != 1 or cnt_all != 1:
                ok = False
                print(f"   LABEL PROBLEM {l}: in {f} {cnt_same}x, "
                      f"in owned files {cnt_all}x")
    old_labels = {l for f in FILES for l in lab.findall(old_text[f])}
    new_labels = {l for f in FILES for l in lab.findall(new_text[f])}
    print(f"   old labels {len(old_labels)}, new labels {len(new_labels)}, "
          f"added {sorted(new_labels - old_labels)}, "
          f"lost {sorted(old_labels - new_labels)}")
    if old_labels - new_labels:
        ok = False

    print("\n== 4. Statement environments per file (count old -> new)")
    env = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|"
                     r"definition|example|remark|algorithm|proof)\}")
    for f in FILES:
        co = len(env.findall(old_text[f]))
        cn = len(env.findall(new_text[f]))
        print(f"   {f}: {co} -> {cn}")
    print("\nRESULT:", "OK" if ok else "PROBLEMS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
