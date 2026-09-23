# Stage 3 author record

Authored 2026-09-22. This records author investigation, not acceptance by
the required five independent reviewers. No subagents were spawned by this
author. Stage 2 was accepted before this work began.

## Scope and files

Read the canonical aggregation certificate note, its corrective audit and
coverage map, stage 2 accepted statement/proof, the coordinator's investigation,
the September 12 application note and its corrected review, and the existing
example scripts. Added:

- `sections/03-consequences.tex`: closed-system consequence, three regimes
  with separate dimension restrictions, 2n+1 SDP objectives, the Shor
  projection and independent closure/whole-space proofs, two nonclosed
  projection examples including a compact strictly feasible variant.
- `sections/04-hypotheses-examples.tex`: stable convexity, two-/three-form
  sufficient conditions, A-block versus Q-block PDLC qualification, strict
  AHC-versus-HHC separation, both stable/HHC nonimplications, ordinary-HC
  four-/three-row counterexamples, closed-system counterexample and exact
  good-aggregation inertia obstruction, and the strip/Shor gap example.
- `appendices/application.tex`: complete certificate validity, exact DD
  selection LP and box support lifting, rational PSD identity, equality
  normalization, conditional rows, repaired exact example and optimum,
  activation interpretation, pure-bilinear and Shor limitations.
- `supplement/check_examples.py`: standard-library rational coefficient
  identities and exact witness checks. Polynomial identities are checked
  as coefficient dictionaries, not only on a grid. The manuscript supplies
  all universal proofs; finite witnesses do not establish general results.

Updated `main.tex`, bibliography, coverage and literature records, and the
stage plan at the coordinator's direction. The later frontier source expansion
is deferred to distinct stages 4--6, then synthesis and whole-paper review.

## Mathematical development and independent author checks

The SDP characterization uses trace(A) plus the 2n signed b coordinates,
reducing the canonical coordinate count without any complexity or numerical
certification claim. The spectrahedron's compactness guarantees attained
values when nonempty; common infeasibility is a separate branch.

The cone C=image(PSD)+orthant is not assumed closed. Its dual is the exact
nonnegative PSD multiplier cone. A strictly feasible point supplies an
interior cone point. Quadratic mixing with that point gives actual Shor
membership along the segment and proves closure equality. Extrapolating to
2x-x0 and taking the midpoint proves actual membership for every target x
when all certificates are trivial. This verifies the canonical result with
the precise cone-interior argument retained.

Independently checked both nonclosed projection formulas, including the
coordinator's compact extension. PSD of a 2x2 covariance with zero first
diagonal forces its cross entry zero; positive first variance permits any
fixed cross entry after increasing the second variance. The endpoint
formulas and strict feasible points follow exactly. The compact example
respects the global compactness convention in Kojima--Tuncel, avoiding an
unjustified comparison using only an unbounded original feasible set.

The AHC-not-HHC example has A1=I and so lies in the three-form stable class.
The restriction x3=t is the binary square cone, with a midpoint failing
y1^2=y2^2+y3^2. Thus the weaker hypothesis is demonstrably strict. Every
remaining boundary example has a complete algebraic proof, replacing
historical numerical inertia checks. The closed example has no good
multiplier, not merely no convex certificate, because its constant and
2x2 traceless block contribute two negative eigenvalues.

For the application, checked the estimator factorizations, DD range,
piecewise affine margin, increasing slopes, optimum, normalized comparison,
global tangent and activation witnesses. Equality weights must share the
normalization; equality-only certificates are allowed. Tangent separation
of an expansion point is distinguished from whole-box exclusion. No
selection-support, implementation, performance, or algorithm novelty claim
is made.

## Literature and concurrent formal work

Primary-source followups are recorded in `literature.md`, including Polyak's
author-uploaded text, the exact stable-convexity definition in the existing
Sheriff thesis extraction, Fujie--Kojima's closure theorem and Slater condition,
Berthold--Witzig's local source, and Dong's author manuscript and journal
metadata. Exact numbered BDS results use arXiv v2 throughout.
The coordinator independently investigated Kojima--Tuncel and erratum
availability; see `stage03-root-closure-audit.md`. The manuscript proves its
own needed closure statement and does not use KT Theorem 4.2's unqualified
equality. No broad historical-error or priority assertion is drawn.

Read the newly contributed `sections/91-formal-consequences.tex` and noted
its different finite-SDP coordinate count and additional scope. Per the
coordinator it is preserved but not yet input into the main manuscript.
Its actual source/interface verification and portable integration remain
for synthesis. In particular, the currently accepted main-proof formal
account is not silently extended to certify this stage's mathematics.

## Targeted verification

From `paper-quadratic-aggregation/`:

1. `python3 supplement/check_examples.py` passed, then was run again with
   output recorded in `build/stage03-exact-check.log` after final source edits.
2. `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
   passed during authoring (17-page PDF).
3. A fresh dedicated build used
   `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/stage03 main.tex`,
   with output in `build/stage03-author-build.log`. It passed with 17 pages.
   The final TeX log has zero warnings, undefined references, overfull boxes,
   or underfull boxes.
4. `pdftotext -layout build/stage03/main.pdf build/stage03-main.txt` passed;
   the extraction was inspected for the new section ordering and equations.

No project-wide checks, CI status, or CI logs were inspected. The existing
source notes, original scripts, accepted theorem source, and formal files
were not modified. The frozen source/PDF hashes are in
`stage03-author-snapshot.json`. This report completes authoring, not review.
