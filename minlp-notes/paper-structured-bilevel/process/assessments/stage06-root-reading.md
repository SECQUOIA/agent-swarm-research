# Stage 6 — root source and implementation reading

Stage 6 began only after stage 5's five reviews, separate corrections, root
verification and acceptance. Root assigned one author and is independently
reading the sources and checking the new development.

## Existing scalar and convex algorithms

Root read the complete nonconvex scalar algorithm note, computation report,
closeout and source-positioning note; the full scalar_solver.py; the original
benchmark face oracle; the convex quadratic prototype algorithm note; and the
screening-versus-MILP report. The nonconvex algorithm maximizes revenue, with
pessimistic least revenue and universal upper feasibility. The convex API
minimizes its specified quadratic upper expression. This sign difference must
remain explicit.

The convex fiber minimizer is unique, including signed/zero aggregate weights
and fixed boxes. Multiplier events cover every attainable aggregate; positive
slope pieces invert affinely. Scalar endpoints, positive-curvature stationary
branches and zero-curvature flat intervals give every global response. Negative
curvature contributes endpoints only. Comparing actual costs, not stationarity,
establishes globality. On an open price interval, equal winning value
polynomials have equal derivatives gamma*w; nonzero gamma and fiber uniqueness
therefore give one actual response. Point strata must retain all distinct ties
and flat intervals. The incremental envelope's retained contacts and final
all-branch scans preserve these isolated responses even after cell merging.

Root checked the code's open-cell upper-row clipping and endpoint inclusion:
upper rows have rational affine coefficients; a feasible interior singleton
is rational and retained, while a limit at an excluded response-cell boundary
is not an attained optimizer. Rational interior samples avoid joining the
quadratic fields of two different endpoints. At a fixed price, upper rows and
revenue are affine in a flat aggregate interval; endpoint checks handle robust
feasibility and least revenue. The selected price's field contains the complete
returned response and value, of degree at most two.

The old original-coordinate face enumerator computes a global VALUE despite
singular free Hessians by moving a minimizer along a null direction to a
smaller face. This does not enumerate all flat global minimizers. The newly
assigned full-bilevel baseline must instead certify its explicit nonsingular-
principal-matrix restriction, compare all original stationary-face values over
the entire price interval, and optimize the same upper task independently.

Root identified two concrete profile targets without prescribing a rewrite:
the existing fiber construction rescans all coordinates per multiplier interval
and stores every response vector, and its branch processing repeatedly performs
symbolic substitution/cancellation. The author should choose only a measured,
justified improvement preserving exact contacts and all response semantics.

Historical timing distinctions were read directly: heterogeneous N=48 is
expensive; N=1000 has only two repeated types; the convex N=10000 sweep is a
different model/family. The screening prototype loses the four historical
MILP comparisons, including formulation/preprocessing. The N=8 default MILP
objective discrepancy comes with a primal violation and a separately reported
tighter-tolerance follow-up; zero numerical MIP gap is not an exact certificate.

## Independent primary-source access

Root opened the Gardiner–Lucet publisher abstract,
https://link.springer.com/article/10.1007/s11228-010-0157-5.
It directly confirms quadratic and linear operation algorithms for univariate
piecewise-quadratic convex envelopes. Root did not access the subscription
full text or import an unverified bit-complexity/contact-reconstruction theorem.

Root accessed the published Moehle–Gindi–Boyd–Kochenderfer article at
https://web.stanford.edu/~boyd/papers/pdf/portf_constr_lcso.pdf,
Optimization and Engineering 24 (2023), 1667–1687,
DOI 10.1007/s11081-022-09748-x. Read Section 6.3 and Appendix B; printed
1686–1687 were rendered locally after the web screenshot cache failed.
Original and renderings are under verification/stage06-root/.
This establishes the broad constructive envelope antecedent. The published
appendix has apparent formula errors: equation (25) repeats q1 where q2
belongs; the finite endpoint chord's beta has the wrong sign for alpha*x+beta;
the stated endpoint derivative inequalities appear reversed. The author was
alerted. Our direct branch and contact arguments must remain self-contained;
these detailed source formulas are not used as proof or executable authority.

The Kiwiel repository PDF failed via the web tool; the actual Springer record
was accessible at https://link.springer.com/article/10.1007/s10107-006-0050-z.
Further exact source/proof inspection remains ongoing. External source access
limits are recorded rather than silently replacing primary texts with summaries.

## Complete convex-code and primary-resource check

Root read all of quadratic_solver.py, including exact symmetric elimination,
small active systems, segment/coverage verification, proposal failure paths,
exhaustive enumeration, quadratic upper interval optimization and the aligned
rank-one weighted event sweep. The small system is I+SH, so singular H causes
no inversion problem. The sweep requires gamma>0 in its implemented API;
signed/zero u and either sign of h subject to SPD are supported. Its weighted
updates avoid storing a full response at every price cell. Negative h uses
the full rank-one SPD inequality to prove every free-set price slope positive.

The Kiwiel technical report was subsequently downloaded successfully via curl
and its actual printed pages 1–2 were read. Equation (2.1), Fact 2.1 and the
signed/zero-weight reduction support the narrow local-fiber attribution. The
introduction explicitly credits earlier sorting methods; the clipping sweep
and O(N log N) operation bound are not new.

## Original-coordinate baseline and measured improvement

Root read the complete new original_faces.py and check_full_task.py during
authoring. Every principal minor is checked; Sylvester's criterion rejects
nonpositive-definite free submatrices. Every global minimizer's minimal face
has positive-semidefinite free Hessian, and the nonsingularity restriction
therefore makes it positive definite. Its stationary affine solution is
enumerated. Fixed-coordinate rows correctly impose no one-sided gradient
restriction. Direct original quadratic substitution gives the three correct
price-polynomial coefficients; all overlapping-domain pair intersections and
pointwise ties are retained. The independent upper solver handles open-cell
limits, interior row singletons, stationary revenue points and point-stratum
worst revenue. Shared rational instance data are its only connection to the
compressed implementation. No code-level correctness defect was found in this
reading. Root requested direct validation of every returned optimizer witness,
in addition to equality of values/attainment and response sets.

A focused root cProfile of the unchanged heterogeneous N=8, seed17 atlas
recorded 4.93 profiled seconds, with 3.64 seconds in sign and 2.92 in repeated
cancel calls. These are profiler costs, not benchmark times. The author
independently found the same bottleneck at N=12 and introduced only an exact
rational sign shortcut and a rational-endpoint midpoint shortcut in a paper
copy. Root checked the complete diff and requested the resulting docstring
change from “dyadic” to “rational.” Both changes preserve exact signs and
interior samples; the algebraic fallback and contact selection are unchanged.
Fresh timed comparisons should warm both methods and vary execution order to
limit cache bias, with individual times retained.

## Independent capacity-example derivation

For d=(1,1), c=(-1,-1/2), u=(1,1), h=3/5, the reduced untariffed cost is
w^2/5-w on [0,1/2], -w^2/20-3w/4-1/16 on [1/2,3/2], and
w^2/5-3w/2+1/2 on [3/2,2]. At price 17/20 the only global minimizers are
3/8 and 13/8, both with follower value -9/320; the middle piece is concave
and its endpoints have the larger value -1/40. For lower prices, comparison
with the larger contact excludes every aggregate <=1. For higher prices,
comparison with the smaller contact puts all optima in [0,3/8], where direct
minimization gives w=(5/2)(1-x). Its revenue decreases on [17/20,1]. Thus
capacity w<=1 gives optimistic maximum 51/160 and the same pessimistic
unattained supremum. Root supplied these exact calculations to the author.

## Completed draft and fresh protocol inspection

Root read the complete mathematical Section 6 and its empirical subsection,
all of the new original-coordinate baseline, direct returned-witness tests,
experiment driver, table generator, diagnostic runner and figure generator.
The overly broad initial common-field wording was corrected during authoring:
each selected optimizer or limit pair and value share one quadratic field;
the entire atlas need not. Two missing TeX backslashes and the rational-sample
docstring were also corrected. These are pre-freeze authoring checks, not a
substitute for the independent five-reviewer gate.

The fresh protocol uses separate cold processes, clears the SymPy cache, and
alternates paired execution order. An initial native-solver stdout collision
broke JSON transport after 18 successful workers; those successes and the
failed transport log were retained. The repaired harness uses a separate JSON
file and captures native stdout/stderr; only remaining workers were resumed.
The final record contains 60 successful workers, all three repetitions.
Root checked that internal totals include validation, construction and both
upper solves, whereas worker wall times additionally include startup/imports.
The independent face validation cost is included in its construction.
Individual samples support the quoted medians and show mixed small-instance
winners. The source provenance now includes the convex generator and shared
rational-data helper.

Root accessed the actual Bemporad–Morari–Dua–Pistikopoulos 2002 PDF at
https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf.
Theorem 2 (printed p8) proves affine optimizer/multipliers on an independent
active region; Theorem 4 (printed p10) proves continuous piecewise-affine
optimizers. Their convex-value assertion is for the transformed objective
without the removed parameter-only term and is not imported for arbitrary
original parameter-dependent quadratic costs.

## Frozen-stage root verification

The sole author completed and stopped before root froze stage06-round01:
30 inputs, manifest SHA256
`b9c28c41440e7ea2e660731eac9023d900279ad1ebae7bf99866f32ffb3d4bc8`.
Root verified every frozen/live hash and the complete final source-input,
artifact and measured-version manifests: no mismatches after applying the
explicit measured-source mapping. All previously accepted mathematical inputs
(Sections 1–5 and four appendices) are unchanged. The live 73-page PDF is current
and its log has no warnings or unresolved references. Root visually rendered
the contact figure and found its labels and plotted sets clear and faithful.

Root reread the entire Section 6 after freeze, including the generic failure
contract, signed/negative-rank-one sweep, singleton aggregate case, all-pair
and incremental globality proofs, all upper endpoint/attainment cases, exact
examples, baseline minimal-face proof and all empirical qualifications. Root
found no further substantive proof defect in this reading. The five independent
reviewers have separate full-stage assignments; their findings remain pending.
