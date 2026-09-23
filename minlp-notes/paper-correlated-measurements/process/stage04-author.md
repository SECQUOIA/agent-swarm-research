# Stage 4 author handoff

Status: author complete, ready for five independent reviews. No claim of
submission readiness before the remaining staged gates.

Files written: `sections/04-certification.tex`, `appendices/certification.tex`,
new bibliography entries, main includes, Stage4 coverage/literature records,
and self-contained `verification/stage04/check.py` with `results.json`.
Stages1–3 manuscript source was not changed. No historical results, literature
packages, or unrelated manuscript were edited.

All mapped Stage4 mathematics is written and proved: prior-aware support and
trace certificates; rational SPD/log/signed interval arithmetic; established
VN scalar/diagonal boundary formulas and continuous certificate bounds;
structured tridiagonal and covariance/reverse-adjoint oracle; every scalar
and diagonal split barriers; finite-scenario raw/standardized robust bounds
and fixed-qp spectral corollary with sharp a-squared limitation; exact latent
separator representation, arbitrary W/G support, full cross-prior elimination
proof of nested-anchor ordering, singleton baseline and signed bridges.

Author-phase coordinator comments corrected before completion: strict k/G
ceiling-loss boundary at k=0; two literal `quad` typos; row/column orientation
of interval quadratic; empty diagonal-support convention; determinant
normalizer wording; rational-log arithmetic bit-cost scope; redundant
irrational no-anchor gap example replaced by one rational example. No result
was invalidated. All critique was useful local clarification, not a substitute
for the requested five-reviewer gate.

Primary literature is credited precisely. Especially direct precedents now
explicitly include Burclová–Pázman normalized criterion support, Maus AR1
maximin relative efficiency, Chowdhary etal robust exact-budget correlated
selection, Harman–Trnovská grouped PSD information, and Sagnol–Harman subsystem
conic design. Kim's final title was corrected against publisher metadata.
Generic convexity, filtering, exact arithmetic, nuisance Schur, pattern
atomization, and mixture methods are not novelty claims. A qualified novelty
sentence concerns only the precise nested Markov-anchor hierarchy in the
inspected predecessors.

Validation: `code/research_20260912/.venv/bin/python
paper-correlated-measurements/verification/stage04/check.py` returns PASS for
1,537 exact rational checks: 180 filter information and 180 reverse-row
identities; 756 binary log tangents using independent rational enclosures;
20 diagonal toy barriers and 20 convex lower tangents; 10 rational dual
repairs; 256 selected-subset separator identities; four signed bridge checks;
100 signed interval comparisons; robust representative/tie/factor checks;
and exact toy information/gradient/dual. No floating tolerance or historical
helper import is used. These bounded checks supplement mathematical proofs,
not a broad solver benchmark or proof-assistant formalization.

The coordinator separately supplied independent nested-anchor/Loewner/G
checks and read the main and appendix proofs during authoring. Stage5 owns
all empirical tables, exact historical certificate replay, matched new
experiments, and final supplement integration. The Stage4 checker is already
standalone apart from its declared SymPy dependency.

Build: latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
from this folder succeeds. Combined manuscript is 50 pages at handoff; final
log has no undefined references/citations or underfull/overfull boxes.
