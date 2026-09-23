# Stage 6 author report

Date: 2026-09-22. Status: authored, ready for the required five independent
reviews. No subagents were used by this author. Existing research-note
reviews supplied context but do not replace this stage's manuscript reviews.

## Mathematical development

`sections/08-four-aggregation.tex` proves the four-aggregation bound for
every positive dimension, under nonempty proper strict feasibility and
signed homogeneous PDLC. Linear independence of the original matrices is
not required. The section gives the entire transfer proof, with BD's
topological theorem explicitly identified as the external input and all
its hypotheses stated.

The proof uses three independent positive definite perturbations. A cubic
coordinate minor controls exceptional dependence parameters. Properness
excludes a common strictly negative leading direction, which makes every
positive inward nonstrict system bounded and free of points at infinity
in the original affine chart. Ratios by the positive perturbation
quadratics encode the systems as sublevels of a continuous function;
the elementary countable-base lemma selects regular levels. No original
boundedness, regularity, initial good aggregation, projective chart, or
spectral smoothness is assumed.

The strictification lemma deletes globally nonpositive quadratics before
taking interiors. Its proof explains why a retained quadratic cannot vanish
at an interior point of its nonpositive sublevel. The main limit normalizes
four multipliers in the simplex and then controls their negative
eigenvectors. Eventual inclusion of each fixed original feasible point,
strict negativity of every simplex limit at that point, and convexity of
the selected homogeneous component establish strict validity on the
ordinary hull. The converse uses finitely many strict limiting slacks,
with no closure interchange. The conic component formula handles singular
matrices, including a rank-one negative semidefinite limit.

An optional remark credits and proves the known two-generator reduction
for dependent triples, then invokes Yildiran's classical two-bound. The
four-necessary BDS example has a self-contained witness proof: every good
multiplier belongs to the four-ray cone by repeated negative eigenvalues,
and each of four explicit witnesses can be excluded only by its designated
ray. Combining necessity with the new upper bound gives the exact displayed
description. Sharpness is claimed only for n>=3.

The SOC corollary keeps the negative-component orientations. A common
strict feasible point proves the closed formula by convex mixing. The
PDLC half-ball counterexample distinguishes that closure from naive
nonstrict quadratic replacement and from the hull of the original weak
system. Its source locator is corrected to BDS **v2 Example 2.23**.

The root's preliminary reading identified two wording issues before
freeze; both are fixed: a finite subset is *contained in* the inward set,
and it is the levels **-epsilon_k** that avoid the exceptional levels of
the continuous function. These authoring checks are not the five formal
manuscript reviews required next.

## Literature and contribution boundary

`stage06-literature.md` records the independent primary-source checks,
including BD's low-dimensional proof, BDS v2 numbering, and the dissertation.
The four-bound, sharpness construction, dependent cone reduction, conic
representation principle, and fixed-set eigenvector limit have explicit
antecedent credit. The narrowly qualified originality statement concerns
the full transfer to arbitrary strict systems. Dunbar's stronger regular
nonstrict theorem statement is acknowledged; the proof relies only on the
fully qualified published theorem. Retrieval and proof-dependency limits
are kept in the process record rather than turned into an allegation in
the manuscript. No search non-discovery is treated as proof of priority.

## Exact supplement and targeted checks actually run

From the repository root:

```sh
python3 paper-quadratic-aggregation/supplement/check_four_aggregation.py
```

Passed. This standalone standard-library script verifies the PDLC
polynomial identity, a strict feasible point, all four witness slack
vectors and radical signs, and the four-ray decomposition as a coefficient
identity. Arithmetic is exact in the rational fields extended by sqrt(2)
and sqrt(5); no floating-point sign threshold is used. It verifies finite
algebraic identities, not the quantified transfer theorem or novelty.

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/stage06 main.tex
```

Passed after final source and reference changes. The final author PDF has
36 pages at `build/stage06/main.pdf`; build output is captured in
`build/stage06-author-build.log`. Searches of final `main.log` and
`main.blg` for Warning, Overfull, Underfull, and undefined returned no
matches. The section's extracted PDF text was read, and rendered pages
25 and 29 were visually inspected for equation and table layout. An
initial optional renderer attempt using PyMuPDF failed because `fitz` is
not installed; `pdftoppm` rendered the pages successfully instead. No
dependency was installed. UTF-8, terminal-newline, and trailing-whitespace
checks accompany the SHA-256 source snapshot.

No project-wide verification, CI inspection, solver experiment, or Lean
rerun was performed. Concurrent formal fragments and source files were
preserved; their integration and packaging remain stage 7.

## Files and remaining workflow

Added section 08, `supplement/check_four_aggregation.py`, the author and
literature records, and the source snapshot. Updated `main.tex`, the
bibliography with the Dunbar dissertation, the supplement README, coverage,
literature index, and process status. Other topics were not changed.
The five independent stage reviews must precede acceptance. Synthesis,
portable formal supplements, final packaging, and whole-paper review remain
stages 7–8.
