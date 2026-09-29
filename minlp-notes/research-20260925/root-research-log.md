# Root research and verification record

Date: 2026-09-25. This batch is finished; research is paused at the user's
request to finish the current ideas without starting new ones.

## Decisions and reassessment

The opening survey compared the existing repository with independent
investigations in convexification, parametric decomposition, integer
structure, and sparse quadratic hulls. Several attractive starting points
were downgraded after primary-source checks. The pooling edge reduction is
classical linear-plus-linear-fractional optimization. Fixed-rank quadratic
selection has close Gao--Li and Del Pia--Dey--Weismantel predecessors.
Three-variable SDP representability is already known from triangulation
and completely positive matrices of order four.

The penalty direction produced an independently reviewed, formally checked
encoding obstruction and a restricted calibration inapproximability
theorem. Independent significance review treats them as a focused milestone,
not sufficient reason to stop the research. Current continuations seek
positive penalty guarantees, structural limits and repairs of sparse
quadratic relaxations, and stronger implications of moment incompatibility
for tree indicator epigraphs.

## Independent root mathematical checks

The root rederived the one-binary projected native set, the cancellation of
an unrestricted multiplier using two opposing residual witnesses, the exact
dual value, and the factor-two penalty threshold. It separately derived the
general finite-mixture and scalar-sign characterizations in
[penalty geometry](penalty-geometry.md); a fresh reviewer accepted those
proofs.

The source's Example 13 was rechecked independently after the geometry
reviewer flagged it. Its residual is one-sided. For `t=lambda+rho>=1/2`,
the augmented value is `min(t-3/2,-1/(4t))`; its supremum is zero for every
penalty. The example has finite-multiplier nonattainment rather than a
positive optimized dual gap. The minimum switches branches at
`(3+sqrt(5))/4`, not `1/2`. See the review for the complete comparison.

For the three-variable quadratic

```
p=x²+y²+9z²+6xy-12xz-12yz-x-y+9z+1/4,
```

the root independently reconstructed all 27 localizing matrices from the
20 rational moments supplied by the investigating agent. Exact SymPy
determinants proved strict positive definiteness for every matrix. The
linearized objective is exactly `-1/40`; the smallest leading principal
minor is `154171/40000000000`.

The root also independently derived a simpler proof of true nonnegativity.
Writing `s=x+y` and `d=x-y`, use `|d|<=min(s,2-s)`. For `s<=3/4`,

```
p=(s-1/2)²+(s²-d²)+9z²+(9-12s)z.
```

For `3/4<=s<=1`,

```
p=9(z-2s/3+1/2)²+(s²-d²)+(1-s)(3s-2).
```

For `1<=s<=2`,

```
p=9(z-2s/3+1/2)²+((2-s)²-d²)+3(s-1)(2-s).
```

Each expression is nonnegative on its region. Exact polynomial expansion
checked all three identities. This proof and the independent rational
matrix check were sent to the author and reviewer for integration.

## Targeted commands actually run by the root

```
python research-20260925/check_parametric_penalty.py
python research-20260925/check_minimum_penalty_hardness.py
python research-20260925/check_treewidth_elimination.py
python research-20260925/checks/three_positive_gap_certificate.py
python research-20260925/verify_three_positive_disjoint_review.py
python research-20260925/verify_three_positive_family_review.py
python research-20260925/check_smoothed_penalty_review_second.py
python research-20260925/check_star_subset_accuracy.py
```

All passed: 72 exact penalty-envelope cases; 976 binary-box and 75 graph
penalty cases; the `K2,3` elimination counterexample and subdivided-complete
graph checks through eight branch vertices. These finite checks support,
but do not replace, the general proofs. The root's temporary SymPy script
for the three-variable moment witness and polynomial identities also
passed. Persistent reproductions are owned by the corresponding author
and independent reviewer.

Other agents' targeted commands and Lean builds are recorded in their own
verification files. No project-wide verification or CI inspection was run.

## Subsequent checks and direction reassessment

The root ran both persistent three-variable witness checkers. They confirm
the 27 strict matrix inequalities, all switched instances of the two
Anstreicher--Puges SOC families, the edge minima, and the five zero contacts.
The root inspected the primary source's SOC formulas before accepting the
comparison. A further independent symbolic calculation verified the full
five-parameter polynomial certificate, its proposed five-by-five matrix
expansion, and rank nine of the ten contact and edge-derivative equations
for the rational example. The matrix expansion is not by itself a proof of
the proposed conic equivalence; that equivalence has separate reviewers.

The effective penalty upper bound was revised after reviewers found a
superseded source and changed constants. The root independently inspected
the final Basu--Roy theorem statements: weak sign conditions suffice for
both the sparse KKT set and the reciprocal graph. The revised asymptotic
upper bound is a useful synthesis of existing theory, not the principal
originality claim. The fixed-number-of-quadratics case remains under
investigation and has a fresh adversarial reviewer.

The most promising current geometric continuations are a compact SDP for
the missing three-variable inequality family and a quantitative accuracy
barrier for the explicitly defined subset moment relaxation on uniformly
conditioned stars. Neither is being promoted to a broader formulation or
algorithmic limitation without a proof covering that broader class.

## Completion of the existing ideas

After the user's finish-only instruction, work was limited to the ideas
already underway, their independent reviews and documentation. New review
agents completed the fixed-quadratic-count proof audit, the quadratic-family
priority comparison, and the quantitative star proof audit. Outstanding
extensions were recorded as unresolved, including symmetry-complete
three-variable cuts and unrestricted four-variable star exactness.

The completed fixed-count theorem gives penalty bit length `N^{O(k+1)}`.
The root independently checked the affine-face reduction, regularized
stationarity elimination, two-block limit formula, and multiplier recovery.
The final source comparison also examines the later quadratic-map paper's
few-variable formulas and algebraic-representation theorem, avoiding an
originality claim based only on an older missing proof.

The root completed the already proposed rational star accuracy refinement.
Repeated opposite-pair deletions bound every `k`-subset perimeter when
there are `2k` leaves. The resulting rational data have fixed spectral
bounds, polynomial encoding and gap at least `1/(466560 k^2)`.
A fresh reviewer checked the complete written proof and normalization.
The targeted rational checker passed five instances and 852 exact subset
perimeters, together with the cut violation, mean bounds and cost bounds.
This computation is finite corroboration, not the all-order proof.

The additional root checks of the family identity passed. The smoothed
penalty checker passed 363 penalty cases, 150 grid/tube cases and 1,216
optimized-penalty sharpness cases, all in exact arithmetic. Earlier Lean
checks were performed by the author and independent reviewer; the root did
not rerun a redundant build. Their coverage note states the formal limits.

A separate documentation audit checked local links and found one malformed
fraction caused by a form-feed character. It was corrected. Both indexes
now distinguish completed reviewed results, classical consequences and open
questions. No project-wide verification or CI inspection was performed.

The final targeted documentation scan passed for all 56 Markdown files in
this batch: local link targets exist and no unexpected raw control
characters remain. A scoped `git diff --check` also passed for tracked
changes; untracked research files were covered by the separate scan, not
implicitly by that Git command.

## Publication preparation completed

The user subsequently authorized finishing the current work for potential
publication, without writing manuscripts. This pass covered this September
25 batch and did not reopen unrelated repository projects or pursue new
research directions. The final handoff is
[publication-readiness.md](publication-readiness.md).

Fresh agents assessed the penalty, quadratic, indicator-star, and supporting
packages. Separate adversarial agents checked important proofs and closest
prior results. A final independent reviewer compared the package assessments
with the mathematical notes and the central handoff. No unresolved proof
blocker was found in the accepted scope. These are research-agent reviews,
not external peer review or guarantees of correctness or novelty.

The strongest new source correction concerns the treewidth preprint. The
root independently opened the August 19, 2026 arXiv revision and read its
Theorem 1, Corollary 1, and Section 2.3. The main theorem now assumes torso
width directly. The false elimination lemmas still support the corollary.
The corrected source-specific account was incorporated and independently
rechecked. No claim that the current main theorem is refuted remains.

The root also independently reread the newly integrated full-parent
indicator-star hull argument. Bounded objective sublevels give bounded
parent blocks; deleting a zero-mass positive second moment decreases the
objective by at least the positive Schur complement times that moment.
Thus optimal parents have finite scalar-law realizations. Coercivity and
continuity at interior masses also pass the lower bound to the closed hull
when original means vary. This is a supporting characterization, not a
compact formulation claim.

Literature comparisons now include the explicit Kamminga–Rudolph QCQP
application, Burer–Dong complete three-variable separation, and additional
quantum compatibility and indicator-quadratic precedents. Their effect is
to narrow the proposed contributions, not to promote every retained result
to a standalone novelty. Source versions with inconsistent displayed dates
are retained separately and compared by the formulas actually used.

The result agents' targeted arithmetic runs are recorded in their package
assessments. New persistent supporting checks cover exact local star parent
matrices and integer-structure identities. The reproduction agent checked
the final manifest's 31 source records and 61 artifacts, including every
hash and byte count. The unchanged Lean source still matches its previously
reviewed hash; this preparation did not repeat its successful compilations.
The root did not rerun unchanged mathematical suites merely to duplicate
these checks. Numerical discovery searches remain archived as exploration.

The root updated both indexes and the central handoff. A targeted inline
Python command checked local Markdown targets, raw controls, final newlines,
and whitespace across this batch, the main README, and its three supporting
notes outside the batch. It passed for 79 Markdown files and 580 local link
targets. `git diff --check -- README.md` also passed; the inline check is
what covered untracked files. No project-wide suite or CI inspection was
performed.

The final reviewer suggested distinguishing constructed parent moment
matrices from explicit scalar atom locations. The handoff now states that
the checker verifies the former and the two-atom realization proof supplies
the latter. This precision change affects no theorem. Publication preparation
is complete on the documented scope; open extensions remain inactive.
