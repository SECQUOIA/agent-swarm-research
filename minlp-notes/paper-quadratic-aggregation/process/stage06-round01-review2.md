# Stage 6, round 1, independent review 2

Verdict: **pass; no major or minor correction requested**.

I independently reviewed the complete four-aggregation section, the author
report and snapshot, the stage literature record, relevant bibliography and
supplement changes, and the standalone exact checker. I checked the earlier
negative-direction lemma as a dependency. I did not read other current
review reports. The only repository file I authored is this report.

## External input and scope

The input at `sections/08-four-aggregation.tex:58` states the relevant
independence, signed PDLC, regularity, nonempty-interior, and infinity
hypotheses. The primary BD preprint's final proof of Theorem 1.4 explicitly
handles dimensions one and two through Proposition 8.7, and the other cases
through Propositions 8.6 and 8.10. Thus the all-positive-dimensions use here
is supported. The manuscript does not silently use a smooth spectral curve
or the stronger dissertation statement.

The four-bound is an external topological theorem. The manuscript correctly
identifies its own development as the transfer to arbitrary strict systems,
including dependent original triples, and distinguishes the original weak
feasible set from the regular inward approximants.

## Perturbation and regular levels

The regular-level lemma at line 81 is valid: any exceptional real level is
the infimum of the function over a member of a countable base. Continuity
gives the other inclusion. This also works when the function is unbounded;
the exceptional infima under consideration equal actual finite levels.

The three displayed positive definite perturbations are independent already
in homogeneous dimension two. The off-diagonal entry separates the third
matrix, and the two diagonal entries separate the remaining two. Their
leading principal blocks are positive definite for every stated dimension.

Properness excludes a common strictly negative leading direction. Any
nonzero common nonpositive direction of the perturbed leading forms would
give precisely such a direction for the original forms. The normalization
argument consequently proves boundedness, not merely absence of an obvious
recession ray. Closedness gives compactness.

The same signed PDLC certificate and one fixed strict feasible point survive
all sufficiently small perturbations. The chosen coordinate determinant has
a nonzero cubic leading coefficient, so independence fails at only finitely
many parameters even when the original matrices are dependent. The ratio
function uses strictly positive denominators, and its levels are correctly
identified as `-epsilon`. Avoiding the countable exceptional levels and the
finite dependence set gives all external hypotheses simultaneously. Every
fixed finite subset of the original strict set is eventually contained in
the inward sets; no unsupported uniform exhaustion assertion is needed.

## Strictification and limiting goodness

The strictification lemma at line 176 deletes exactly the potentially
troublesome globally nonpositive quadratics. A quadratic vanishing at an
interior point of its nonpositive set has a zero local maximum, vanishing
gradient, and negative semidefinite Hessian, hence is globally nonpositive.
For every retained quadratic the interior of its weak sublevel is therefore
its strict sublevel. Finite intersections commute with taking interiors,
and a nonempty open convex set equals the interior of its closure. At least
one inequality remains because the hull is bounded in positive dimension.

The limit proof at line 214 establishes strict validity rather than only
weak validity. Simplex normalization keeps every limiting multiplier
nonzero. Strict evaluation at the fixed feasible point and continuity of
ordered eigenvalues give exactly one negative eigenvalue in every limit.
Unit negative eigenvectors have a common convergent subsequence and retain
their negative eigenvector equations.

For each original feasible point, eventual membership in the inward system
puts its lift and the fixed feasible lift on a strictly negative segment.
Their oriented eigenvector scalar products have the same sign. In the
limit, strict negativity of the original nonnegative aggregate excludes a
zero scalar product. Every original lift therefore belongs to the same
convex negative component. Convex combinations remain strictly in that
component. The displayed component formula also handles singular limits
and the rank-one negative semidefinite case.

The reverse inclusion uses the finitely many strict limiting slacks to
obtain eventual membership in the exact inward hull. It is valid pointwise
and does not exchange a limit with an intersection or replace the ordinary
hull by its closure. These arguments establish the claimed upper bound.

## Dependence, sharpness, and closure

The optional dependent-triple reduction at line 279 is sound. Evaluation at
a feasible lift makes a compact base of the pointed generated cone. In a
span of dimension at most two this base is a segment or point whose extreme
points come from original generators. Consequently at most two original
inequalities define the same strict set. Yildiran's two-constraint theorem,
with its opposite sign convention, supplies the stated optional bound; it
is not an input to the general perturbation proof.

For the example at line 300, I checked the PDLC identity, strict feasible
point, the negative component selected by the first inequality, and the
goodness of both sums. The repeated transverse eigenvalues show that every
good multiplier satisfies `c <= a+b` when `n >= 3`. The four-ray cone
decomposition has nonnegative coefficients for the displayed interval of
choices of `t`.

Each witness has exactly one zero designated slack and three strictly
negative slacks. Hence every nonzero good multiplier excluding that witness
must belong to its designated ray. Each witness is outside the ordinary
hull because the designated inequality is good and strict there. Every
exact family must therefore contain all four rays, and the established
upper bound gives the exact four-ray representation. No sufficiency claim
for every multiplier in the larger cone is needed. Sharpness is explicitly
limited to `n >= 3`.

The oriented SOC formula at line 365 follows from the correct negative
components. Mixing a point satisfying all closed conic inequalities with a
common strict feasible point gives simultaneous strict slack and proves the
closure identity, including degenerate matrices. The half-ball example
does satisfy PDLC after adding the redundant negative definite form, and
its naive weak replacement adds the isolated point `e1`. It correctly
distinguishes both possible closed-set confusions.

## Literature and checks actually performed

- Read the local primary BD preprint extraction, including its theorem,
  standing setup, fixed-set eigenvector limit, and final low-dimensional
  proof. Also opened the [primary v1 text](https://arxiv.org/html/2405.18282v1).
  The preprint Section 8 locators are not presented as journal locators.
- Checked the BDS v2 source for Corollary 2.20, Example 2.21, Conjecture 3.2,
  Remark 2.19, the dependent-generator observation, and Example 2.23. The
  claims and versioned locators agree with the manuscript.
- Read the available dissertation extraction and checked the official
  [Emory record](https://etd.library.emory.edu/concern/etds/vq27zq10w) and
  search-indexed primary dissertation metadata. Its stronger Theorem 5.0.5
  statement is acknowledged. I did not visually inspect a freshly retrieved
  dissertation PDF, and do not infer a definitive error from the damaged
  extraction or its proof-dependency discrepancy.
- Inspected the accepted author text of Yildiran's paper for the strict
  sign convention and theorem setup. The optional application does not
  introduce an unsupported dimensional restriction or omit nonemptiness.
- Additional targeted searches for strict four-aggregation results and the
  dissertation did not establish an earlier complete arbitrary-strict
  transfer. This is bounded search evidence, not proof of priority. The
  manuscript's qualified and narrowly stated novelty claim is appropriate;
  the four-bound, sharpness example, and conic principle receive credit.
- Read and ran
  `python3 paper-quadratic-aggregation/supplement/check_four_aggregation.py`.
  It passed the exact PDLC identity, strict point, radical/rational witness
  slacks, and ray decomposition checks. Its radical arithmetic and exact
  sign comparisons are consistent with those finite checks. It does not
  purport to verify the quantified transfer theorem.
- Compared the relevant frozen snapshot hashes for the new section,
  bibliography, standalone checker, and historical checker source: they
  matched. Searched the dedicated stage 6 LaTeX and BibTeX logs for warnings,
  undefined references, and overfull/underfull boxes: no matches.
- No new build, Lean rerun, project-wide verification, CI inspection, or
  subagent was used. This review does not certify later synthesis work.
