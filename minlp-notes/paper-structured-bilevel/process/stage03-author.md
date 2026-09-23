# Stage 3 author record

Date: 2026-09-07. Scope: near-optimal robustness and certified recovery of dense
quadratic responses using a structured surrogate. This is an author draft pending
five independent reviews. No stage 4 work was authored or delegated.

## Changes and coverage

`sections/03-robustness-screening.tex` contains the full assigned theorems, proofs,
examples, algorithms and limits. `main.tex` includes it. `references.bib` adds five
verified primary references; README identifies accepted stages 1/2 and pending
stage 3. `process/coverage.md` maps all stage 3 obligations to manuscript labels
without removing any subsequent-stage obligations. The accepted foundations,
exact-response section, and fixed-core appendix were not edited.

The robust result covers moving local/shared normals and nonlinear aggregate
costs, not only convex followers. The measurement dimension is fixed separately
for each criterion, while the number and combined rank of criteria may grow.
The nominal value is globally optimal, and adverse responses need not be
stationary in the original follower problem. The exact theorem distinguishes
feasibility, bounded infimum, attainment, and witness recovery. It does not merge
unrelated algebraic witnesses into one field. Bounded leader-controlled budgets,
irrational adverse output, convex attainment even at zero budgets, two strictly
positive-budget failures of attainment, and the growing-rank Max-Cut boundary
are included.

The screening result specifies the exact residual enclosure, sound whole-cell
labels, lower-dimensional closure handling, dense true-KKT reconstruction, and
M 3^t recovery LPs excluding preprocessing. The quantitative neighborhood is
computed from a vertex transition count and rational strict margins. Signed
inner/outer feasibility and objective bounds remain available when enumeration
is large. Full-assignment KKT checks, conservative ambiguity, shifted switches,
and the lack of a general practical superiority conclusion are explicit.

## Developments and proof obligations resolved

### Thresholded fibers avoid unnecessary nested global minimization

The nominal global value remains necessary. For each measurement, however,
existence of a feasible fiber KKT candidate under the nominal budget is both
necessary and sufficient for that measurement to occur at a near-optimal
response. Necessity follows by minimizing on the compact fiber. Sufficiency
uses only feasibility and the cost threshold. The manuscript proves both
implications and does not apply the original stationary predicate to arbitrary
near-optimal followers.

Each criterion is eliminated separately before robust feasibility is conjoined.
The resulting formulas share only the leader and one nominal value variable.
Only one original fiber candidate is reintroduced for each requested witness.
This closes the dimensional accounting when the criterion count grows.

### Constant local matrices give a stronger arithmetic conclusion

Root suggested the extension, independently checked during authorship. Constant
local Q, E and G make local KKT denominators constant even when shared normals
and criterion measurements depend polynomially on the leader. Those shared rows
enter the effective local linear cost, not its KKT matrix. The Basu–Pollack–Roy
degree bounds from the accepted exact-response section therefore extend to the
robust result: for fixed degree and structural dimensions, the output field
degree does not grow with N or row/criterion counts. The number of successive
elimination/sampling steps along each dependency chain is fixed; there are still
polynomially many independent criterion calls. No attainment or simultaneous
field bound for unrelated adversaries is asserted.

### A simplex cover suffices for transition control

The source uses a triangulation. The manuscript instead enumerates all affinely
independent subsets of at most r+1 vertices from each original surrogate cell.
Its affine dimension is at most r because projection to the leader is injective,
even when the aggregate lift has more coordinates. Carathéodory's reduction,
already proved in the fixed-core appendix, establishes that the resulting
simplices cover the cell. Overlaps are harmless. Each simplex involves at most
r+1 original vertices, so its union of transition coordinates is at most
(r+1)q. Outside that union the nominal label has a positive vertex margin,
preserved throughout the simplex. This supplies the same computable radius
without an additional triangulation construction or external theorem.

### Mathematical boundaries checked directly

- The measurement parameter box is bounded explicitly with polynomial-bit
  rational bounds; moving-normal compression applies on that compact domain.
- Closed follower graphs alone do not imply near-optimal lower continuity.
  The convex-attainment proof repairs feasible points with Hoffman, mixes with
  the unique nominal minimizer when the limiting budget is positive, and uses
  nominal responses when it is zero.
- The nonattainment example is checked through its polynomial factorization,
  derivative sign, and cost-level comparison; a positive budget alone does not
  eliminate the jump. Max-Cut uses the entire cube, not a spurious restriction
  of the continuous adversary to binary points without justification.
- Adding the two box VIs gives the stated ellipsoid with the correct sign.
  Applying its directional bound to Q times a coordinate vector gives the
  gradient center ghat + p/2, not ghat + p.
- Zero gradient is a valid F equation even at a bound. Weak sign certificates
  need strictness somewhere and relative-interior continuity; a bare nonstrict
  gradient does not certify a bound label.
- Every dense recovery LP imposes the true Hessian KKT signs. Certified free
  coordinates may be numerous; principal-submatrix inversion has polynomial
  rational bit complexity. Failed full-cell guesses are not discarded from
  recovery on smaller parts of the cell.
- The radius uses induced infinity norms of symmetric matrices, including the
  inverse, and R = ceil(sqrt(N)). Both response and gradient errors are at most
  sigma/2. The dense residual can have arbitrary rank and signs.
- Inner LPs give genuinely feasible leaders, while outer LPs only bound the
  objective. Equalities can defeat inner feasibility; only the actual finite
  bound gap is an accuracy certificate.

## Sources and attribution

Read the full canonical `results/bilevel-near-optimal-response-robustness.md`
and `results/bilevel-surrogate-screening-exact-optimization.md`, their reopened
notes and literature audit, and the accepted foundations/exact-response section.
Historical PASS labels were not treated as proofs. The root's independent
reading led to minor wording and LaTeX corrections, all applied during authorship.

Read `literature/AGENTS.md`; no generated literature metadata or originals were
changed or copied. Actual primary sources consulted and cited include:

- Besançon, Anjos and Brotcorne (2021), *Complexity of near-optimal robust
  versions of multilevel optimization problems*, Optimization Letters 15,
  2597–2610, DOI 10.1007/s11590-021-01754-9. Checked the publisher's full text and
  arXiv:2011.00824, including conditional complexity membership and the
  objective-robust variant. The model is not presented as new here.
  https://link.springer.com/article/10.1007/s11590-021-01754-9
- Besançon, Anjos and Brotcorne (2024), the near-optimal robust model and separate
  upper-row adversaries. The repository literature audit flags a reversed margin
  direction in its printed Corollary 2; that statement is not imported. Our
  screening bounds are independently derived from the VIs.
- Dantas and Gribonval (2019), *Stable Safe Screening and Structured Dictionaries
  for Faster l1 Regularization*, IEEE TSP 67(14), 3756–3769, DOI
  10.1109/TSP.2019.2919404. Checked arXiv:1812.06635v3, especially Remark 2 and
  the approximate-dictionary screening construction. It is a direct precedent
  for certified use of structured approximations, not merely generic screening.
  https://arxiv.org/abs/1812.06635v3
- Liu, Zhao, Wang and Ye (2014), ICML/PMLR 32(2), 289–297. Checked the primary
  proceedings record and PDF Sections 2.2/2.3 on VI enclosures and directional
  screening. https://proceedings.mlr.press/v32/liuc14.html
- Arnström and Axehill (2020), arXiv:2003.07605v2. Checked the author preprint,
  including Section IV/Algorithm 2's parameter-region partition. The cited
  version is identified explicitly. https://arxiv.org/abs/2003.07605v2
- Garey, Johnson and Stockmeyer (1976), TCS 1(3), 237–267, DOI
  10.1016/0304-3975(76)90059-1. Verified the primary publisher record and its
  explicit simple unweighted Max-Cut NP-completeness statement. Our reduction
  from Max-Cut is written in full.
  https://www.sciencedirect.com/science/article/pii/0304397576900591

No unsupported claim of priority, exhaustive novelty, or solver superiority is
made. The bounded-degree corollary and simplex-cover refinement are proved
without describing standard elimination or convexity tools as new.

## Actual verification

Logs are under `verification/stage03-author/`. Both diagnostic commands were run
from the repository root and completed with exit code 0.

| Command | Distinct result |
| --- | --- |
| `python code/bilevel_reopened/nearoptimal_second_review.py` | 24,603 exact fiber-identity points over 35 measurement models; 5,421 cube points over 75 Max-Cut graphs; two nonstationary worst-response checks; the positive-budget polynomial identity and 2,048 sampled exclusions. Actual JSON is `nearoptimal.txt`. |
| `python code/bilevel_reopened/screening_review_checks.py` | 24 exact random cases, 61 cells, 112 certified statuses, 549 screened recovery assignments versus 3,213 full assignments, and 918 directional checks. Singleton/zero-residual and weak-closure cases passed. The dense eight-coordinate transition case has q=1, theorem bound 2, observed ambiguity 2, residual infinity norm 51/100000 and margin 1/10. Actual JSON is `screening.txt`. |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` from the paper folder | PASS. Combined draft has 27 pages. The final log has no warnings, undefined references/citations, or overfull/underfull boxes. Actual transcript is `build.txt`. |

These finite diagnostics verify distinct boundary/certificate cases. They do not
implement fixed-dimensional general quantifier elimination, prove the general
complexity bounds, or constitute runtime experiments for this paper. No numerical
or experimental superiority is inferred from the assignment counts.

The first build found a missing closing equation environment in the new section;
it was corrected before the final clean build. A multi-label eqref and a missing
quad were also corrected. `manifest.json` records artifact/input hashes, command
outcomes, and preservation of accepted mathematical section files.

## Remaining scope

All assigned stage 3 obligations are written, with no unresolved proof dependency
identified by the author. This does not bypass the five independent reviews.
Accuracy algorithms, other hardness/structural boundaries, implementation and
experimental comparisons, synthesis, and final integrated review remain in
stages 4–7 as already assigned. No source file outside the new paper folder was
modified.
