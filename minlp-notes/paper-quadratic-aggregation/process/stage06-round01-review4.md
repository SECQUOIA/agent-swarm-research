# Stage 6, round 1: independent review 4

Date: 2026-09-22. I read the complete new section, author/literature/snapshot
records, exact checker, bibliography addition, and coverage mapping. I checked
the transfer proof from its stated assumptions and inspected the relevant
primary BDS/BD statements. I did not read another current review, coordinate
findings, alter manuscript sources, or rerun Lean.

## Verdict

Accept stage 6. No valid major or minor issue identified. The transfer covers
every stated positive dimension and dependent originals, preserves strict
goodness in the limit, and supports the four-necessary and oriented-closure
conclusions. This verdict relies on the explicitly stated external BD theorem;
it is not an independent reproving of that theorem's topological arguments.

## External input and dimensions

I read the retrieved BD v1 primary text at its standing independence
assumption, Theorem 1.4, permissibility definition, Proposition 3.15 proof,
Proposition 8.7, and the final Theorem 1.4 proof. The external input retains
PDLC, independent matrices, nonempty interior, closure-of-interior regularity,
and no points at infinity. The final primary proof expressly separates
dimensions 1 and 2 from dimensions at least 3, so the present theorem does
not infer low-dimensional coverage merely from an omitted bound. The stated
input does not import the spectral smoothness assumption of other BD results.

The manuscript's versioned locators and comparison with BDS Corollary 2.20,
Example 2.21, Remark 2.19, and Example 2.23 match the actual BDS v2 text.
It acknowledges Dunbar's stronger dissertation statement without depending on
an uncertain missing hypothesis. The qualified priority claim is confined to
the full strict-system transfer and gives credit for both the four-bound and
the fixed-set negative-eigenvector antecedent.

## Inward approximation

The three displayed R matrices are positive definite and independent even
when n=1, where their size is two. Their leading blocks are positive definite.
Properness rules out a simultaneous strictly negative original leading
direction. Hence a nonzero direction satisfying all inward nonpositive leading
inequalities would contradict that fact. Normalizing an unbounded sequence
then proves boundedness of each inward closed system, independently of any
boundedness assumption on the original system.

The signed PDLC combination persists for small parameters by openness of
positive definiteness; the perturbation combination itself need not be PSD.
The chosen three-coordinate minor has a nonzero cubic leading coefficient,
so only finitely many perturbation parameters can fail independence.

The regular-level lemma is correct: a bad level produces a basic neighborhood
whose infimum equals that level, giving at most countably many possibilities.
Positive denominator quadratics correctly encode the inward systems by
`max_i f_i/w_i <= -epsilon`. The sequence avoids the exceptional **negative**
levels and the finite dependence parameters. Its selected systems have
nonempty interior and `C_k=cl(S_k)=cl(int(C_k))`. Every fixed finite subset
of the original strict S is eventually contained in S_k. No uniform compact
containment of all of S is asserted or needed.

## Strictification and limit

Globally nonpositive polynomials may indeed be discarded in a weak
description, and this deletion is necessary before making it strict. A
quadratic vanishing at an interior point of its weak sublevel has a zero
local maximum, hence zero gradient and negative semidefinite Hessian; its
exact Taylor formula makes it globally nonpositive. This proves the asserted
interior equality for each retained polynomial. Finite intersections commute
with taking interior, and the open convex hull equals the interior of its
closure. Boundedness guarantees that not all constraints are discarded.

Normalizing and, if necessary, duplicating retained multipliers gives one
compact four-tuple parameter space. The inward matrix error tends to zero.
Nonzero simplex limits remain strictly negative at the fixed feasible point
for the original system, so each limit has exactly one negative eigenvalue
rather than a possible zero matrix. The eigenvector subsequence can be chosen
once for all four matrices.

For a fixed original feasible x, eventual membership of both x and the
reference point in S_k and strict goodness on conv(S_k) force the same
negative-component orientation. After the limit, an orientation scalar cannot
vanish because the original aggregate is strictly negative at x. Thus all
feasible lifts lie in one convex negative component. Taking finite convex
combinations establishes strict validity on the **ordinary** hull. This step
does not incorrectly infer strict validity merely from a nonstrict limit.

The converse is also sound: finitely many strict limiting inequalities
persist at each fixed candidate point for sufficiently large k, placing the
point in conv(S_k), hence conv(S). There is no closure-intersection exchange.
The conic component formula covers singular matrices and a rank-one negative
semidefinite limit.

The optional dependent-triple reduction is valid: evaluation at a strict
feasible lift gives a bounded normalized slice of the finite cone; in span
dimension at most two it is a segment or point whose extreme rays come from
original generators. Nonzero nonnegative reconstruction preserves the strict
feasible set. The subsequent two-bound is appropriately attributed to the
classical result, not treated as new.

## Sharpness and SOC closure

I independently recalculated the PDLC identity, strict point, signs forcing
the original feasible s below -1, and the goodness of the four displayed
rays. A negative rho coefficient repeats at least twice for n>=3, proving
the necessary four-ray cone containment. The decomposition interval is
nonempty exactly under the stated nonnegative cone conditions.

All four witness slack vectors are correct, including the radical relations
for alpha and beta. At each witness every off-designated ray is strictly
negative, so any good multiplier not on the designated ray is strictly
negative as well. This proves indispensability; the established upper bound
then proves that precisely those four inequalities suffice. Sharpness is not
overclaimed in dimensions one and two.

The SOC formulas retain the selected orientation. Mixing a point satisfying
all weak oriented constraints with the common strict feasible point produces
strict slack for all finitely many norms and proves the closure formula.
The half-ball example verifies the separate failure of both naive quadratic
weakening and equality with the hull of the original weak system. Its added
negative-definite row genuinely enforces homogeneous PDLC without altering
the strict or weak feasible sets.

## Exact supplement and checks actually run

The script's radical arithmetic makes exact sign decisions in each stated
quadratic field; its comparisons square only after sign separation. It checks
the PDLC polynomial as a coefficient identity, all witness vectors, and the
cone-decomposition identity. It accurately excludes the quantified transfer
and external topological theorem from its finite checking claim.

Reads used `cat`, `tail`, `sed -n`, and targeted `rg -n` on the stage files,
the downloaded primary BDS/BD texts, and the recorded dissertation extraction.
From `paper-quadratic-aggregation/`:

```sh
python3 supplement/check_four_aggregation.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage06-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage06-review4/main.log /tmp/quadratic-stage06-review4/main.blg
```

The exact checks passed. The independent temporary-directory build passed
and produced 36 pages; final TeX/BibTeX scans found no matches. No project-wide
test, CI inspection, formal rerun, source modification, or subagent was used.
