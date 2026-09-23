# Stage 4, round 1 — reviewer 09

Major findings: 0
Minor findings: 0

I found no concrete mathematical, scope, coverage or attribution defect requiring a correction in this frozen stage. The positive-power obstruction preserves the distinction between separately easy scalarizations and a difficult joint graph. Neither that family nor its cap-set strengthening is presented as resolving the remaining one-input binary/general-integer gap. This verdict is bounded by the coverage and implementation limits below.

## Coverage

I read the complete 1,297-line `sections/04-vector.tex`, all of `abstract.tex`, `sections/00-introduction.tex` and `sections/05-conclusion.tex`, the stage task/lenses and process/protocol, the stage-4 coverage inventory, the bibliography and manuscript inclusion/notation files. All eleven snapshot hashes matched and were rechecked when finalizing this report.

I compared all ten canonical stage-4 result files and all eleven explicitly substantive stage-4 supporting files listed in `coverage.md`, reading the original mathematical text rather than relying on its audit status. This includes the full positive-power refinement obstruction, its source-scope note, the cap-set and three-witness notes, the general rational-polar-spanner note, the hinge/Bernstein precursor, the finite separable companion, the conditioning/simplex refinements and the lattice investigation. The promoted nonconvex precursor is only a pointer and supplies no additional theorem. The manuscript preserves the distinct direct maximum-product transfer despite the later rank bounds.

Accepted stages 1–3 were checked as dependencies, using my earlier full-stage reviews as context. I reread the indexed compiler, corrected rational-tolerance statement, hybrid scalar cell-count proof and Jensen-superadditivity interface in stage 3, and the rational log-determinant allocation oracle in stage 2. The parity-contact and finite-disjunction interfaces in stage 1 remain applicable. I did not reopen every proof in these accepted stages during this review.

## Full-stage proof reconstruction

- **Refinement and overlays, lines 19–161.** The level-cut argument handles exact level maxima and plateaus. Restricting a finite interval cover gives the claimed partition count. A shared deterministic mass-bisection tree orders its returned knots without assuming monotonicity of the approximate mass oracle. The common denominator has polynomial bit length because only polynomially many piece endpoints contribute. Multiset order statistics preserve multiplicity; source-cell recovery works on positive cells and can select any containing source cell on duplicate endpoints. The common interpolation weight and directed bands preserve the complete vector graph.
- **Box/facet ranks and direct allocation, lines 165–330.** An original-output spanner preserves nonnegative selected chord gaps despite signed representation coefficients. The rational exchange count and coefficient lengths are polynomial. The factors $4r-1$, $8r-1$, $2^{12}r$ and $2^{13}r$ follow from the stated refinements and hybrid bound. Compact nonnegative-facet bodies force every original component to be affine when facet rank is zero. The half-body band is needed for coupled budgets. The approximate-product argument gives the displayed $7m$ bound, including $m=1$; it does not assume approximate first-order optimality.
- **Oracle interfaces and effective-image bands, lines 338–577.** The effective body has the supplied rational balls and a nonzero pulled-back separator at exterior queries. The generic spanner has uniform inverse/objective bounds from its seed determinant. A fixed grid and central-ball repair give exact feasibility with additive objective loss at most $1/4$ and prevent denominator growth across exchanges. The positive-polar procedure gives either a valid separator or a distance certificate, rather than treating approximate support as exact membership. Its seeds are feasible and span the required image. The one-dimensional product-body workaround respects the imported optimization theorem's dimension convention. Both spanners are obtained from the original oracle. Rounding effective coordinates keeps the output error in the nonlinear image, and the final explicit parallelotope band has the stated $49/64$ error factor.
- **Separable vectors, lines 579–740.** One concatenated output basis supplies the same coefficients across all coordinate blocks. Ordered Jensen gaps and the integer lattice-ball estimate compare the product packing with the original vector lift. I recomputed all six finite/compiled constants, including $5832\cdot219=1277208<2^{21}$. Every coordinate has one shared interpolation weight across its outputs. Inactive-coordinate removal and the common effective image are valid.
- **Separations and boundaries, lines 742–1297.** I reconstructed the positive-power and cap-set arguments in detail, as described below. For the fixed-degree product example I checked the rational inequalities defining the boxes and the entire middle integer section, not merely the initially labeled sets. Oriented thirds prove the general-integer lower bound, while full convexity of fixed binary sections proves the stronger binary lower bound. The hinge precursor and Bernstein thickening preserve their margins. The triangular-wave polynomial construction has the claimed dense encoding and uniform error; its peak/trough lower bound concerns optimum binary dimensions. The arbitrary polynomial overlay preserves source-cell signs, bracket bands, invalid-code exclusions and exact graph containment. The tilted-body lift absorbs the common quadratic and retains the scalar obstruction; its condition ratio grows by at least $8+60M^2$. Both conditioning comparisons and the simplex improvement follow from the stated ball assumptions, including nonsymmetric permitted-error sets. Strict upper-violation sets are convex, but their union need not be; the manuscript correctly declines to infer a simultaneous covering result from Helly or Radon arguments.

The abstract, introduction and conclusion agree with these scopes. Finite real existence, rational construction, numerical degree, binary exponent encoding, total formulation length and optimization time are not conflated. The synthesis identifies the increasing-input product separation, increasing-degree nonconvex separation, and changing-error-body separation separately.

## Primary lens: positive powers and repeated convexification

For $j<k$, the scale separation gives $x_k^{D_j}\ge15/16$. A thirds mixture weighted toward the larger input has input at most $1-64/(3D_j)$, so its selected component power is at most $3/67$. The resulting error lower bound is exactly $2177/2144>1$. Equal integer residues modulo three therefore fail, whereas equal binary assignments fail under every real convex weight. The midpoint bound remains strictly below $7/8$ for every pair of graph points, not only the selected contacts.

For arbitrary signed normalized scalarization weights, the increasing function $\sum_j|\lambda_j|F_j$ bounds the scalar range variation. Splitting its height at $7/8$ gives two valid rectangles, with the correct induced unit tolerance. Each scalarization may select its own split. The vector half-height overlay instead uses $M+1$ intervals. The thirds obstruction also proves that each unit-error chord interval contains at most one selected input; thus the refinement failure is about simultaneous chord count, not a claimed unbounded optimum binary/general-integer gap.

A zero-sum triple of distinct residues produces an integral uniform barycenter and the same forbidden component error. Over $\mathbb F_3$, a zero-sum triple with two equal entries has all three equal, so the residue set satisfies the exact cap-set hypothesis. The generating-function bound and minimizer equation $4t^2+t-2=0$ are correct. For three outputs, the direct proof handles arbitrary label magnitudes and orderings: a separation of at least three yields an integer point at a weight in $[2/3,4/5]$; otherwise distinct labels are consecutive, and repeated convexification inside the middle integer section produces the forbidden uniform barycenter. No pairwise midpoint assumption is silently strengthened.

## Primary-source checks

After reading `literature/AGENTS.md`, I inspected the cached primary texts. Ellenberg–Gijswijt, Theorem 4, gives the monomial-count bound used here, with the stated specialization to $\mathbb F_3$. GLS Definition (5) and Theorem (3.1) compare the returned objective with all points of the exact body and provide the distance-to-body convention required by the repair proof; Corollaries (3.4)–(3.5) support the polar/anti-blocker credit. Lyu–Hicks–Huchette Section 3, Proposition 1, explicitly combines breakpoint lists and uses shared SOS2 weights. Plevrakis–Hazan Section 3.2 discusses approximate optimization in spanner construction. Kelly–Maulloo–Tan Section 2 states the proportional-fairness relation. Averkov–Weismantel Theorem 1.1 contains the mixed Helly identity cited in the open-boundary discussion.

I checked the manuscript's mathematical spanner proof directly. I did not separately retrieve Awerbuch–Kleinberg's original article during this round or certify every bibliography metadata field. No exhaustive external-priority search is claimed.

## Executed checks

All completed successfully:

- `python code/positive_vector_obstruction/check_first_review.py`: 120 rational witness pairs, 15 actual-power gaps and 306 residue combinations.
- `python code/positive_vector_obstruction/check_box_gap_root.py`: 72 middle-slice vertices, 2,048 exact integer-slice mixtures and 390 product-contact pair obstructions.
- `python code/quadratic_rank/check_implicit_knot_overlay.py`: 2,304 ordered-search checks, 60 exact order statistics, 180 source-cell containments, eight large implicit-grid rank queries and 99 directed-band checks.
- `python code/quadratic_rank/check_rational_polar_spanner_second.py`: 16 generic systems, 93 repaired optimizer calls, 11 exchanges, 120 full-image vertex checks and 347 positive-polar cases.
- **Independent checker:** `python paper-integer-dimension/verification/check_stage4_reviewer09.py`: 66 rational scale checks, 990 arbitrary-label orderings, exhaustive checks that cap(1)=2 and cap(2)=4, 31 exact monomial-count bounds, 84 high-precision pair violations and 56 triple violations. The exact tests use rational/integer arithmetic; actual huge powers use 100-digit arithmetic and are supplemental numerical evidence.

## Limits and disposition

No numbered findings remain. I did not run a LaTeX build or perform a PDF-layout review. I did not generate complete MILPs or implement the inherited certified quadrature, root-isolation and black-box optimization routines. Their use received a proof and interface review. Existing and independent finite checks support, but do not replace, the general arguments. Historical audits outside the explicitly substantive coverage set were not exhaustively reread. Whole-paper verification remains a separate gate.

## Verified snapshot SHA-256 hashes

```text
abstract.tex
db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3
coverage.md
d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf
macros.tex
3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f
main.tex
026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c
references.bib
60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693
sections/00-introduction.tex
6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16
sections/01-foundations.tex
3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e
sections/02-quadratic-finite.tex
0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3
sections/03-scalar-nonlinear.tex
8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803
sections/04-vector.tex
d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d
sections/05-conclusion.tex
2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e
```
