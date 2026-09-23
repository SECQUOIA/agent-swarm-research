# Stage 6 independent review 04

Recommendation: accept. I found no justified major or minor issue requiring a
stage 6 correction.

## Snapshot, scope and independence

I verified the SHA256.json digest
`b9c28c41440e7ea2e660731eac9023d900279ad1ebae7bf99866f32ffb3d4bc8`
and all 30 listed files in `process/snapshots/stage06-round01` before review.
I read the entire `sections/06-computation.tex`, all eight new Python files,
the three data tables, raw result structure and records, README, coverage
integration, new bibliography entries, and relevant accepted prerequisites.

I did not read another current stage 6 report, delegate, or modify manuscript
sources or official experiments. All builds and generated reviewer evidence
are under `verification/stage06-review04/`. The frozen scripts' repository-root
assumptions require adaptation after copying them deeper into the tree. I
changed only those dependency-root paths in isolated driver/helper copies;
solver copies remained byte-identical to the snapshot, and generated outputs
remained inside the reviewer directory. An initial incorrect relative-path
adaptation attempt failed before substantive checks; correcting the isolated
path resolved it.

The author report was used to locate evidence. Its completion and historical
PASS statements were not treated as proof or as verification of measurements.

## Mathematical review

**Convex certificates and sweep: Section 6 lines 29–111.** The free principal
system determines a rational affine response, and its box and gradient signs
are affine tests. Endpoint checks certify a closed interval, including a
singleton; complete interval coverage is separately necessary. Exhaustive weak
statuses cover every optimum. The small system is I+SH, in the displayed order,
and its determinant identity establishes invertibility without an inverse of H.
The implementation's dense SPD fallback is correctly excluded from the small
pattern operation count. The generic numerical proposal is never trusted for
optimality or coverage and can fail before or after its small-instance fallback;
the text supplies a separate complete exponential oracle.

For the aligned sweep, A1=-sum_free u_i^2/d_i gives derivative
(1-h*A1)/gamma. Positive definiteness makes this positive even for negative h;
signed and zero loadings and simultaneous events are handled. Constant tails
make the effective-price map onto the real line. The inverse and weighted-sum
updates match `quadratic_solver.py:339` onward. The implemented upper quadratic
has exactly the stated terms; interval endpoints and a feasible convex
stationary point give its rational minimum. The sweep is fused with the upper
solve, as the timing discussion says. I found no claim that the numerical
proposal mechanism has a polynomial worst-case path-construction guarantee.

**Fiber compression and complete candidates: lines 128–209.** Strict local
convexity gives a unique fiber minimizer even when the full Hessian is
indefinite. The multiplier clipping law is valid for either sign of a loading.
Its aggregate slope is a sum of squares, and zero slopes supply only singleton
aggregate images already covered by neighboring positive-slope pieces. Fixed
coordinates and a singleton aggregate are addressed explicitly. There are at
most 2N events and hence at most 2N-1 nondegenerate finite pieces.

Endpoints, valid stationary points of positive-curvature pieces, and complete
flat intervals at their single prices exhaust every scalar piece minimum.
Their original value comparisons therefore establish globality. All pairwise
crossings, domain boundaries and flat prices produce a polynomial partition.
On an open cell, identical winning value polynomials have derivatives gamma*w,
so the aggregate responses coincide; strict fiber convexity then identifies
the entire response. This is where gamma nonzero is essential.

**Upper semantics and arithmetic: lines 211–239.** Upper rows become affine
on each open response cell. Clipping retains a singleton strictly inside that
cell; excluded atlas endpoints are treated as limits. An interior sample is
needed to detect attainment of a constant revenue, and both implementations
include it. At a price with ties, optimism intersects each actual component
with upper rows, whereas pessimism checks every response component and uses
the least revenue. Affinity on each fiber piece makes its endpoint tests
sufficient, including a continuum of flat responses. Ties between a limit and
an attained value correctly prefer the attained value.

Quadratic algebraic cuts may belong to different fields, but the argument never
requires their full compositum as output. Rational interior samples prevent
unnecessary degree growth. Open-cell stationary points and row boundaries are
rational; flat prices are rational; remaining outputs use the field of one
quadratic cut. This proves the stated per-output degree-two guarantee, not a
single quadratic field for the entire atlas. Compactness proves optimistic
attainment; it does not prove pessimistic attainment.

**Incremental contacts: lines 242–258 and compressed code 244–314.** Insertion
splits the current winner intervals at domain boundaries and all applicable
quadratic roots, including tangencies. Contacts are retained separately when
open intervals merge. Any final distinct tie must already meet the then-current
envelope when its later branch is inserted; a then-existing lower candidate
would contradict final globality. An identity of value polynomials gives the
same response and causes no missing distinct tie. Isolated-domain endpoints
and flat prices are also retained. Final point reconstruction rescans all
original candidates, so obsolete contacts do not create false responses.
The conservative polynomial counts and polynomial bit argument are compatible
with the implementation's acknowledged symbolic cost.

**Conjugacy and examples: lines 262–329.** The affine minorant proof gives
equality of tilted minimum values before and after convexification. An original
minimizer must also be at contact; a relaxed minimizer at contact is original.
The one-coordinate example correctly distinguishes two actual responses from
the whole convexified interval. The capacity example's three quadratics agree
at shared endpoints; at 17/20 their outer stationary points are 3/8 and 13/8,
both with value -9/320. The concave middle contributes no further minimum.
The comparison at that price correctly confines responses on either side,
and the low-piece revenue is decreasing on [17/20,1]. Thus 51/160 is an
optimistic maximum and an unattained pessimistic supremum. The replicated
two-type family scales this proof by m; it does not create additional events.
The figure matches the exact one-coordinate example and was visually inspected.

**Independent original-coordinate baseline: lines 337–395 and all of
`code/original_faces.py`.** Every nonempty principal determinant is actually
computed and checked. The positivity test uses Sylvester's leading-minor
criterion for the selected principal submatrix, with all needed smaller
determinants already available. A global minimizer on its minimal box face has
a positive semidefinite free Hessian; the nonzero determinant makes it positive
definite. Its unique stationary point is therefore enumerated. Fixed coordinates
need no gradient sign, and the code omits those signs. All retained candidates
are feasible, every global optimum is present, and original dense quadratic
value comparison removes nonglobal KKT points.

The baseline has independent rational parsing, original stationary solves,
value substitution, all-overlap crossing enumeration, tie comparison and upper
optimization. It imports no compressed solver. The minimal-face argument also
explains why the older fixed-price value oracle can move along a stationary
singular null direction to a smaller face without recovering the whole flat
set. The stronger new input restriction is checked rather than silently assumed.
The manuscript correctly describes the exponential minor/status enumeration
and limits its performance comparison to N<=6.

**Screening comparator: lines 542–555.** The two activity binaries correctly
encode lower, free and upper box KKT alternatives, including zero-gradient
bound cases. The explicit M_i bounds the gradient over the complete leader and
follower boxes. SPD makes this an exact real-arithmetic reformulation, while
the SciPy/HiGHS solve and its feasibility tolerances remain numerical. The
manuscript does not turn a zero reported MIP gap into an exact certificate.
The exact screening theorem's completeness, rather than a returned-point check
alone, supplies the exact global guarantee.

## Source coverage and attribution

I read the complete canonical quadratic-algorithm, nonconvex scalar-algorithm,
nonconvex source-positioning, nonconvex computation and reopened screening
computation notes, both implementation READMEs, and the nonconvex closeout.
I inspected the convex path/sweep and screening implementation portions used by
the new driver, the actual historical JSON records and their generators, and
the separate existing test families rerun below. The old full-pair compressed
atlas, fixed-price original-coordinate oracle, generic convex path proposal,
complete aligned convex sweep, complete nonconvex solver and new full-task
baseline remain distinct. Historical per-instance observations are not promoted
to new general results. Other reopened robustness/accuracy diagnostics belong
to the accepted Sections 3–4 and have an explicit disposition in coverage.md.
I found no unaccounted distinct stage 6 result; stage 7 synthesis is later work.

The primary sources support the narrowly stated credits:

- [Bemporad et al.](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf),
  printed pp.8 and 10, Theorems 2 and 4: active-region affine solutions and
  continuous piecewise-affine parametric optimizers. The current text does not
  import convexity of the original price-dependent value from their transformed
  problem.
- [Kiwiel's technical report](https://rcin.org.pl/Content/139441/PDF/RB-2002-77.pdf),
  printed pp.1–2, equation (2.1), Fact 2.1 and introductory breakpoint discussion:
  clipped multipliers and earlier sorting of 2N breakpoints. Web text extraction
  did not locate the formulas; downloading the open PDF and extracting locally
  did. The local copy/text are in this review's verification directory.
- [Gardiner–Lucet publisher abstract](https://link.springer.com/article/10.1007/s11228-010-0157-5):
  piecewise-quadratic convex-envelope algorithms with quadratic and linear
  complexity. I did not inspect its subscription full text or import a bit
  theorem from the abstract.
- [Moehle et al.](https://web.stanford.edu/~boyd/papers/pdf/portf_constr_lcso.pdf),
  Section 6.3 and Appendix B: recursive piecewise-quadratic convex-envelope
  construction. The manuscript supplies its own contact and original-response
  proof and relies on no external tangent formula for correctness.

These were bounded source checks, not a new exhaustive publication-priority audit.

## Experimental evidence and provenance

All 11 input hashes recorded in `data/stage06-results.json` verify. The two
wrapper hashes match `measured-run-experiments.py` and
`measured-check-full-task.py` in the author verification directory. I inspected
their diffs against the frozen final wrappers: changes add directory creation,
input archival outside the timed workers, and hash-list entries. Solver logic
and timed regions are unchanged. The compressed solver's diff against the
repository version contains only the stated rational sign/midpoint fast paths
and explanatory text.

The raw file has 60 distinct worker keys in 20 three-repetition groups, all
with exit code zero. I checked repeated exact outputs and attainment flags,
not just record counts. Three tables regenerate byte-for-byte. Both prepared
input archives regenerate exactly from their specified generators. The fresh
results, historical records, documented partial-run transport failure and
untimed archival changes are kept distinguishable. The old pairwise compressed
implementation's historical times are not represented as reproducible by its
replacement.

The full-task comparison solves the same follower graph, capacity row and both
upper semantics with each method. The baseline's validation belongs to its
build time. Neither method wins uniformly in the tested instances. Larger
baseline sizes were unattempted, not presumed timeouts. Three-run medians and
shared-machine limitations are stated; independently taking medians for each
column explains why displayed component medians need not sum to the total
median. Profiled timing is separated from ordinary timing. The N1000 population
uses only two types, the N48 case has many distinct events, and the N10000
convex sweep measures a separate subclass.

For screening, preprocessing and exact final verification are included in the
proper total columns. The default N8 numerical infeasibility/objective
discrepancy is retained in every repetition, along with its tighter-tolerance
follow-up; follow-up times do not replace the default solve column. All actual
exact certificate booleans were checked individually. The numerical comparator
remains faster on the stated archived and fresh cases; the manuscript draws no
unsupported superiority conclusion from the M*3^t recovery count.

## Independent checks and limits

The isolated LaTeX build succeeded with 73 pages and no undefined references,
citations, overfull/underfull warnings or other LaTeX warnings. All five
diagnostic groups passed in the isolated harness: the 18 full-task examples,
convex certificate/failure checks, 86 nonconvex adversarial checks, the separate
350 value/72 atlas/30 envelope/11 edge-case families, and scalar examples.
Their commands and logs are under the review directory's nested
`verification/stage06-author/`; this name is inherited from the copied wrapper
and does not refer to or overwrite official author outputs.

My additional `check_review04.py` generated 16 different small rational instances
with signed/zero loadings, either sign of gamma, fixed or nonunit boxes, negative
prices and affine upper rows. Three singular-minor draws were explicitly
rejected. The remaining instances passed 156 exact response-set comparisons
at every cut and an interior sample of every cell in the union of the two
independently constructed atlas partitions. Both upper semantics agreed, and
attained witnesses were checked against original-coordinate values and rows.

I separately reran the fresh N6 heterogeneous compressed/face worker pair,
the N100 convex worker, and the N8 screening worker serially in isolation.
The N6 outputs agree exactly, including the quadratic irrational switch and
optimistic/pessimistic attainment distinction. The convex point passed exact
KKT and service-floor checks. Screening reproduced the exact value
4810519997/235205877942 and the documented numerical follow-up behavior.
These rerun timings are not used as a new performance comparison.

I did not rerun all 60 benchmark workers, implement a new general QE backend,
or claim that finite tests prove arbitrary-input correctness. The acceptance
recommendation rests on the source/code/proof review together with the stated
targeted checks. No optional editorial preference needs to block this stage.
