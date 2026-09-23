# Stage 1 author report

Status: authored and internally checked; ready for the required five independent reviewers. The stage is not self-approved.

## Files and scope

Created `main.tex`, `macros.tex`, `references.bib`, `README.md`,
`sections/01-foundations.tex`, and `sections/02-uniform-one-switch.tex`.
The current draft builds to eight pages. The author field is empty; no human
authorship has been invented. The abstract describes only the current stage
and must be expanded when later results are integrated.

Stage 1 contains:

- Measurable simplex controls, cumulative allocations, free initial activation,
  repeated modes, and a compact parameterization that includes zero-duration
  blocks and shorter schedules.
- Full and one-sided instance and minimax notation: `F_{n,s}(T)`,
  `G^-_{n,k}(T)` with `k=s+1`, grid variants, and unit-grid abbreviations.
- Endpoint monotonicity, cell averaging, compactness, attainment of inner and
  outer extrema, stability in the uniform cumulative norm, and scaling.
- The no-switch baseline for continuous and arbitrary-grid inputs.
- Exact uniform-input continuous formula for `0 <= s <= n-2`, exact unit-grid
  scalar recurrence, binary-search interval, and strict discretization gap.
- The exact three-term one-switch error identity (including two modes with an
  empty omitted maximum), the full continuous one-switch minimax for `n>=3`,
  matching extremizers, construction, and half-grid upper bound.
- Exact three-cell one-switch minimax, two explicit published-conjecture
  counterexamples, and the fixed-budget/many-mode obstruction.

No later-stage result is used in a stage 1 proof.

## Critical development beyond transcription

The manuscript proves compactness of the cumulative relaxed-input class by
recovering a measurable simplex derivative from every uniform limit. The
instance optimum is 1-Lipschitz in that topology, so both continuous minimax
suprema are maxima, not only the inner schedule infima. The schedule
parameterization is accompanied by an explicit uniform perturbation bound.

Endpoint monotonicity holds for measurable inputs even when an input changes
inside a grid cell. Averaging therefore preserves every grid schedule's
objective. In combination with the pointwise restriction inequality, this
proves `F_cont <= F_grid` and the analogous one-sided inequality. The differing
input classes do not leave that comparison unresolved. This consequence was
identified in discussion with the primary agent and explicitly proved here.

Boundary arguments were expanded for constant schedules, repeated modes in
the uniform lower bound, truncated recurrence iterates, the strict integer
rounding inequality, negative redundant terms in the three-term identity,
threshold equality and terminal-mass ties in the one-switch construction, and
fixed-horizon scaling of the conjecture counterexample.

## Sources inspected

Primary source: Sager and Zeile, *On mixed-integer optimal control with
constrained total variation of the integer control*, Computational Optimization
and Applications 78(2), 575–623 (2021), DOI `10.1007/s10589-020-00244-5`.
The manuscript references Conjecture 1 / equation (7.6) and Definition 10.
The local primary package is
`literature/papers/sager2020-on-mixed-integer-optimal-control/`.
The local `original.pdf` page 27 was rendered and visually checked; the formula
and its restrictions agree with the manuscript's statement. That rendering
is retained in `verification/stage01/source-conjecture-page27.png`.
Local manuscript page 6 contains Definition 10 (the free-initial-activation
convention). The manuscript bibliography uses the actual final publication
year, 2021; the local package slug records 2020.

Repository development sources read include
`results/cia-uniform-switching-obstruction.md`,
`results/cia-exact-three-mode-one-switch.md`, and the compactness/reduction
part of `results/cia-universal-heavy-mode-rounding.md`.
Literature positioning was checked against `notes/cia-novelty.md`,
`notes/cia-reopened-literature.md`, and the local primary package. No claim of
exhaustive novelty or priority is made. The three-mode arbitrary-grid-length
result is reserved for stage 4; later algorithms and related work are reserved
for their assigned stages.

## Verification performed

All arithmetic checks below use integers or Python `Fraction`.

1. `python code/cia_tv_conjecture/uniform_certificate.py`: passed; 60 exhaustive
   small schedule comparisons (including repeats), 31,200 continuous/discrete
   bounds, and exact counterexamples. Output: `verification/stage01/uniform.log`.
2. `python code/cia_tv_conjecture/one_switch_certificate.py`: passed; 2,080
   rational constructed schedules and half-grid bounds, plus 13 exact extremal
   constructions. Output: `verification/stage01/one-switch.log`.
3. Added `verification/stage01/check_boundaries.py`: passed; all 1,216 three-cell
   half-simplex profiles with 3 or 4 modes, including zeros/ties/equality cases;
   checked the three-term identity, construction and three-cell upper proof.
   Also checked 28 uniform three-cell extrema and 162 binary three-term
   identities with an empty omitted maximum.
4. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: passed;
   eight-page PDF with no warnings, undefined references, or over/underfull
   boxes in the final LaTeX log. Build output:
   `verification/stage01/build.log`. First page rendered for visual inspection.

These computations support, but do not replace, the analytic proofs over all
measurable inputs.

## Outstanding questions and limitations

No unresolved mathematical question is used or deferred within stage 1.
The draft requires the requested independent reviews before acceptance.
The current abstract and introduction are deliberately limited and await the
later complete-manuscript synthesis. This stage does not settle larger-budget
minimax questions or arbitrary-grid exact minimax formulas assigned elsewhere.
