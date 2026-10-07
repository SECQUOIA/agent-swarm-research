"""W7 verifier for group tu: word-level comparison of the pre-W7 and current
constraints.tex and appendix-tu.tex.

1. Prints every word-level difference between old and new constraints.tex and
   between old and new appendix-tu.tex, so that no unintended change is hidden.
2. Compares the three proof bodies removed from constraints.tex with the proof
   bodies inserted in appendix-tu.tex, word by word, and prints every
   difference.
3. Checks that every \\label of both old files is still defined exactly once in
   the same file, and that every \\ref/\\eqref target used in the moved proofs
   is defined somewhere in the paper sources.
"""
import difflib
import re
from pathlib import Path

root = Path(__file__).resolve().parents[3]
old_dir = root / "process/w7/sections-before-w7"
new_dir = root / "sections"


def words(s):
    return s.split()


def show_diff(name, a, b):
    wa, wb = words(a), words(b)
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    print(f"== word diff {name}: {len(wa)} -> {len(wb)} words")
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old = " ".join(wa[i1:i2])
        new = " ".join(wb[j1:j2])
        if len(old) > 200:
            old = old[:90] + f" ...[{i2 - i1} words]... " + old[-90:]
        if len(new) > 200:
            new = new[:90] + f" ...[{j2 - j1} words]... " + new[-90:]
        print(f"  {tag}: OLD<<{old}>>\n        NEW<<{new}>>")


def proof_after_label(text, label):
    i = text.index("\\label{" + label + "}")
    j = text.index("\\begin{proof}", i)
    k = text.index("\\end{proof}", j)
    # body without the \begin{proof} line
    return text[text.index("\n", j) + 1:k]


def moved_proof(text, label):
    head = re.search(r"\\begin\{proof\}\[Proof of (Proposition|Theorem|Lemma)~\\ref\{"
                     + re.escape(label) + r"\}\]\n", text)
    assert head, label
    k = text.index("\\end{proof}", head.end())
    return text[head.end():k]


old_c = (old_dir / "constraints.tex").read_text()
new_c = (new_dir / "constraints.tex").read_text()
old_a = (old_dir / "appendix-tu.tex").read_text()
new_a = (new_dir / "appendix-tu.tex").read_text()

show_diff("constraints.tex", old_c, new_c)
show_diff("appendix-tu.tex", old_a, new_a)

print("== moved proofs")
for label in ["prop:tu-sound", "thm:tu-states", "thm:tu-approx"]:
    a = proof_after_label(old_c, label)
    b = moved_proof(new_a, label)
    wa, wb = words(a), words(b)
    if wa == wb:
        print(f"  {label}: identical ({len(wa)} words)")
    else:
        show_diff(label, a, b)

print("== labels")
for name, old, new in [("constraints.tex", old_c, new_c),
                       ("appendix-tu.tex", old_a, new_a)]:
    labs = re.findall(r"\\label\{([^}]*)\}", old)
    for lab in labs:
        n = new.count("\\label{" + lab + "}")
        assert n == 1, (name, lab, n)
    print(f"  {name}: all {len(labs)} old labels present once")

all_src = "".join(p.read_text() for p in sorted(new_dir.glob("*.tex")))
all_src += (root / "main.tex").read_text()
defined = set(re.findall(r"\\label\{([^}]*)\}", all_src))
for lab in ["app:tu-proofs"]:
    assert lab in defined
print("== references in moved proofs")
for label in ["prop:tu-sound", "thm:tu-states", "thm:tu-approx"]:
    b = moved_proof(new_a, label)
    refs = re.findall(r"\\(?:eq)?ref\{([^}]*)\}", b)
    missing = [r for r in refs if r not in defined]
    print(f"  {label}: refs {sorted(set(refs))}; undefined: {missing}")
