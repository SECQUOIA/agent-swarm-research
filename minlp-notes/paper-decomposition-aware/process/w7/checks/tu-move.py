"""W7 group tu: move the proofs of prop:tu-sound, thm:tu-states and
thm:tu-approx from constraints.tex to a new subsection of appendix-tu.tex.

The proof blocks are moved word for word; only the proof headers and the
pointer "the tree computation above" change. Run once from the paper root.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[3]
main = root / "sections/constraints.tex"
app = root / "sections/appendix-tu.tex"
src = main.read_text()
apx = app.read_text()

POINTER = "The proof is in Appendix~\\ref{app:tu-proofs}."


def cut(text, label, env_end):
    """Return (text without the proof after `label`, proof body)."""
    i = text.index("\\label{" + label + "}")
    i = text.index(env_end, i) + len(env_end)
    j = text.index("\\begin{proof}\n", i)
    assert text[i:j] == "\n\n", repr(text[i:j])
    k = text.index("\\end{proof}\n", j) + len("\\end{proof}\n")
    body = text[j + len("\\begin{proof}\n"):k]
    # join the pointer with the paragraph that follows the proof
    assert text[k] == "\n", repr(text[k:k + 20])
    return text[:j] + POINTER + " " + text[k + 1:], body


src, sound = cut(src, "prop:tu-sound", "\\end{proposition}")
src, states = cut(src, "thm:tu-states", "\\end{theorem}")
src, approx = cut(src, "thm:tu-approx", "\\end{theorem}")

old = "The table count is the tree computation above, summed over levels;"
new = ("The table count is the tree computation of Section~\\ref{sec:tu-filter},\n"
       "summed over levels;")
assert approx.count(old) == 1
approx = approx.replace(old, new)

block = (
    "\\subsection{Proofs for Sections~\\ref{sec:tu-filter}--\\ref{sec:tu-complexity}}"
    "\\label{app:tu-proofs}\n\n"
    "\\begin{proof}[Proof of Proposition~\\ref{prop:tu-sound}]\n" + sound + "\n"
    "\\begin{proof}[Proof of Theorem~\\ref{thm:tu-states}]\n" + states + "\n"
    "\\begin{proof}[Proof of Theorem~\\ref{thm:tu-approx}]\n" + approx + "\n"
)
anchor = "\\subsection{Union versus hull filtering}\\label{app:tu-union}"
assert apx.count(anchor) == 1
apx = apx.replace(anchor, block + anchor)

old_intro = "This appendix gives the checks of the model of Section~\\ref{sec:tu-model}, an\n"
new_intro = ("This appendix gives the checks of the model of Section~\\ref{sec:tu-model},\n"
             "the proofs of Proposition~\\ref{prop:tu-sound} and\n"
             "Theorems~\\ref{thm:tu-states} and~\\ref{thm:tu-approx}, an\n")
assert apx.count(old_intro) == 1
apx = apx.replace(old_intro, new_intro)

main.write_text(src)
app.write_text(apx)
print("moved", len(sound.splitlines()), len(states.splitlines()),
      len(approx.splitlines()), "lines")
