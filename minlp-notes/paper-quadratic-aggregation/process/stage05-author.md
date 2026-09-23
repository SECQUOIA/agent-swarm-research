# Stage 5 author report

Date: 2026-09-22. Status: authored, ready for the required five independent
reviews. No subagents were used by this author. Earlier source-note reviews
were read as context and do not replace this stage's reviews.

## Deliverables and independent development

`sections/07-approximation.tex` gives the complete finite-approximation
analysis and the exact aggregation for one nonzero prescribed objective.
It defines the extended Euclidean Hausdorff objective over arbitrary good
multiplier families, including interior multipliers, rescaling, empty or
unbounded relaxations, and no attainment assumption for the infimum.

The angle-mesh proof establishes the operator bound 5/2, second derivative
bound 10, defect 5 Delta^2/4, and a radial correction valid for every point
of the relaxation. Both coordinate rays are included; N=2 is covered.
Only nonnegative directions of the slack matrix are constrained; no false
positive-semidefiniteness assertion is used. Integer meshes preserve the
good-cone boundary exactly, have 2m+1 distinct rays, and give O(log N) bits
per multiplier entry. Explicit epsilon-to-cut-count bounds use the actual
mesh construction rather than attainment of an infimum.

The lower proof was developed further after the concurrent formal-accuracy
contribution appeared. It now uses N+1 equally spaced rational parameters,
eta=1/(400 N^2), and a finite pigeonhole argument. Two exclusions by one
cut imply, by adding inequalities and AM–GM,
`(tau-sigma)^2 < 16*((1+10*eta)^2-1) < 1/N^2`.
Zero-coordinate and interior good multipliers are covered. Exact Gram
realization bounds work in r=2 and embed in every r>=2. The manuscript's
Lipschitz constant 5 sqrt(2) gives the strengthened lower constant
**sqrt(2)/2000**, replacing the older sqrt(2)*(log 2)^2/1600. The upper
constant remains 5 sqrt(2) pi^2/16 with denominator (N-1)^2. The constants
are uniform in r and not claimed optimal.

The support-function equality is proved directly by nearest-point
projection. The one-objective proposition has a full order-convex epigraph
separation proof, including interior of the separation set, boundary
support without assuming that set closed, the correct dual cone signs,
strict negativity of every nonzero good aggregate at the origin, nonzero
objective multiplier, complementarity, and common attainment. The origin
is a strict point for the hull description, not the original system.
The result is explicitly classical convex duality, with no selection-cost
or iteration claim.

The proof remains restricted to good cuts; the preceding qualitative
obstruction for arbitrary quadratics is not promoted to a quantitative
rate. `process/stage05-literature.md` records the primary-source review,
including the closer Rote antecedent and the local Bronshteyn–Ivanov PDF.

## Figure and reproducible checks

`figures/finite-aggregation-slice.pdf` is a standalone vector figure of
the plane u=x e1, v=y e2. It shows the exact quartic hull and N=3,5,9
angle-mesh outer boundaries, with a magnified boundary panel. It uses
analytic radial formulas, not optimization or external data. The caption
explicitly distinguishes the illustration from a full-dimensional
Hausdorff computation. A PNG preview is also included.

`supplement/plot_aggregation_slice.py` regenerates both formats using
NumPy and Matplotlib. It checks the formulas numerically on 8,001
directions. `supplement/check_approximation.py` uses only the standard
library and exact fractions to check 64 integer meshes, 606 Gram
witnesses, finite-grid constants, and radial identities. Finite checks do
not prove the universal mathematical statements.

## Targeted checks actually run

From the repository root:

```sh
python3 paper-quadratic-aggregation/supplement/check_approximation.py
python3 paper-quadratic-aggregation/supplement/plot_aggregation_slice.py
```

Both passed. The exact script was rerun after replacing the logarithmic
construction with the finite-grid development and passed again.

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/stage05 main.tex
```

Passed after the final mathematical/literature changes. The 30-page
stage-5 PDF is `build/stage05/main.pdf`; the captured build output is
`build/stage05-author-build.log`. Final `main.log` and `main.blg` were
searched for Warning, Overfull, Underfull, and undefined, with no matches.
The PDF figure preview and rendered manuscript pages 22–23 were visually
inspected; the figure, equations, labels, and surrounding text are legible
with no layout defect found. The author also read the extracted section
text to check symbol consistency and theorem placement.
Targeted UTF-8, terminal-newline, and trailing-whitespace checks on the
stage source/provenance files also passed when writing the 20-file
SHA-256 snapshot in `stage05-author-snapshot.json`.

No project-wide verification, CI inspection, solver experiment, or Lean
rerun was performed. Concurrent formal sections 93–94 were preserved and
not integrated. Their actual verification and packaging remain stage 7.
The main stronger lower constant sqrt(2)/2000 is not claimed to be covered
by the formal package's reported constant 1/2000.

## Files and remaining workflow

The stage adds section 07, its two Python scripts, figure PDF/PNG,
literature/author records, and a source snapshot. It updates `main.tex`,
`macros.tex` (graphicx), `references.bib`, the supplement README, coverage,
literature, and process status. Other repository topics and concurrent
formal source files were not changed. Stages 6–8 are outside this author
task and remain outstanding. Stage 5 requires the coordinator's five
independent manuscript reviews before acceptance.
