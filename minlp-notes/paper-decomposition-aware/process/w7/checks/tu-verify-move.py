"""W7 group tu: check that the proofs moved to Appendix E equal the pre-W7
proofs in constraints.tex up to whitespace, except the one pointer change
("the tree computation above" -> "... of Section~\\ref{sec:tu-filter}"),
and that the main text keeps every label and has the pointer sentences."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[3]
old = (root / "process/w7/sections-before-w7/constraints.tex").read_text()
new_main = (root / "sections/constraints.tex").read_text()
new_app = (root / "sections/appendix-tu.tex").read_text()


def norm(s):
    return " ".join(s.split())


def proof_after(text, label):
    i = text.index("\\label{" + label + "}")
    j = text.index("\\begin{proof}", i)
    j = text.index("\n", j) + 1
    return text[j:text.index("\\end{proof}", j)]


def moved(label, kind):
    head = "\\begin{proof}[Proof of " + kind + "~\\ref{" + label + "}]\n"
    j = new_app.index(head) + len(head)
    return new_app[j:new_app.index("\\end{proof}", j)]


pairs = [("prop:tu-sound", "Proposition"), ("thm:tu-states", "Theorem"),
         ("thm:tu-approx", "Theorem")]
for label, kind in pairs:
    a, b = norm(proof_after(old, label)), norm(moved(label, kind))
    if label == "thm:tu-approx":
        a = a.replace("tree computation above,",
                      "tree computation of Section~\\ref{sec:tu-filter},")
    assert a == b, label
    print(label, "moved verbatim,", len(a.split()), "words")

# every label of the old file still in constraints.tex, none duplicated
labels = re.findall(r"\\label\{([^}]*)\}", old)
for lab in labels:
    assert new_main.count("\\label{" + lab + "}") == 1, lab
print(len(labels), "labels kept in constraints.tex")
assert new_main.count("The proof is in Appendix~\\ref{app:tu-proofs}.") == 3
assert "\\begin{proof}" in new_main  # lem:tu-round, lem:tu-allow stay
assert new_main.count("\\begin{proof}") == 2
print("3 pointers; 2 proofs (lem:tu-round, lem:tu-allow) remain in main text")
