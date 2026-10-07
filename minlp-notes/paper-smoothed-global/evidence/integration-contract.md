# Common mathematical and editorial contract

Use one main explanation: curvature-corrected refinement preserves global
optimizers; independent linear noise bounds expected retained states; exact
closure finishes the sampled problem; a base-selected finite law pays for an
exact fallback on the same draw.

Keep distinct the three structural routes: a small nonconvex auxiliary/core
dimension, sparse bags, and a small core with tractable conditional recourse.
They do not share the same parameter bound or the same noise model.

Every theorem must specify:

1. Rational input and its base bit length before sampling.
2. Which convexity, curvature, decomposition, and oracle assumptions are
   promises, supplied certificates, or algorithmically verified.
3. Fixed degree versus numerical/unary degree; expanded polynomial data versus
   circuit inputs.
4. Exact finite marginal law, independent coordinates, whether noise is aligned
   with a factor or applied to original coefficients, and the base-only sampler.
5. Output representation on ordinary and exceptional draws, its length, and
   arbitrary-precision evaluation when claimed.
6. Correctness on every draw, one sample with no retries, stopping depth,
   exceptional probability, fallback cost, and the resulting expectation.
7. Which numerical parameters enter outside bit length. Fixed-width polynomial
   bounds must not be described as fixed-parameter bounds in width.

An expectation bound for a adaptive list must be justified by comparison with a
deterministic full-grid count or another explicit dominating count. It must not
assume that the adaptively selected cells are independent of noise.

Global proof records, compact optimizer descriptors, and expanded algebraic
coordinates have different size contracts. An implicit exact minimizer defined
by a verified strongly convex subproblem is a valid exact representation only
when its uniqueness and global optimality are proved, and its evaluation
complexity is stated.

Include examples and special cases that explain the restrictions: a finite-law
atom needing fallback; sparse global-error retention preventing an FPT width
claim; recourse with changing feasibility; and the distinction between value
accuracy and distance to an optimizer. State the regret bound for using a
perturbed solution on the original objective.

The manuscript must contain proofs or explicit cited classical results for every
essential step. Repository notes, agent reviews, source paths, and internal
research dates do not belong in the scientific proof chain.

Do not force unresolved broader questions into the paper's theorem statements.
Complete missing arguments needed for the stated results; retain proved
obstructions and honest limitations. No experiment reruns and no fabricated
benchmarks. Position the contribution as mathematical guarantees and certificate
design; competitive practical performance is unestablished.
# Final prewriting audits

All three Sol audits are now complete and materialized. Authors must consult the
report corresponding to their sections:

- `reviews/prewrite-lowrank-sol.md`
- `reviews/prewrite-sparse-sol.md`
- `reviews/prewrite-recourse-sol.md`

Uniformly strong residual convexity admits a core-supported rank-at-most-k
quadratic convexifier by a Schur-complement bound. Its direct recourse theorem
preserves the original coordinate curvature factor L/sigma; do not claim that
this class has no small fixed-rank convexifier. The rank-separation example
belongs to the broader residual-convex class.

The focused two-negative-direction audit is being added at
`reviews/prewrite-two-inertia-sol.md`. The older k<=2 result has a distinct
linear numerical factor 1+nu S/sigma and is not entirely subsumed by the
broader closure bounds. Its deterministic retained-cell exponent is valid.
The supplemental report also supplies a finite Gaussian-like-law transfer;
no theorem should present an exact real Gaussian as a Turing input.

The first model draft has a root review at `reviews/root-model-early.md`.
Resolve its concrete scope and representation issues before finalizing
the front matter. In particular, strong-field and lattice-based methods do
not need a rare fallback, algebraic regret endpoints are not rational, and
the small-noise regret calibration does not apply to strong-field conditions.

That model review now also identifies the charted-output requirement for
explicit/implicit graph constraints. In particular, an implicit graph such
as y^2=2 may contain no rational full feasible point. Return a rational free
point with its exact algebraic lift, or a coordinate approximation without
claiming exact feasibility. Add a charted implicit output format; a box patch
in original coordinates is not sufficient for a nonaffine graph.

Final scope decisions are recorded in `integration-decisions.md`. The complete
inventory has 69 in-scope entries, including tools and limitations. It is not
a count of independent original contributions.

The limitations/front-matter author should cover inventory X3 (the ambient
uniform count-surrogate barrier) and X4 (affine-feasibility hardness and the
diagonal TU local-count example), in addition to the global-error width barrier.
Both are central to the distinction between the proved structural routes and
unrestricted constrained optimization. Give self-contained proofs or an
explicit narrow citation for a previously published result; private notes
cannot be the proof dependency. Other small limitations can remain concise
worked examples or remarks at their natural theorem location.

The first continuous-recourse section has a root review at
`reviews/root-recourse-early.md`. Its empty-core certified mode needs a
separate positive accuracy allowance: E_j=0 cannot imply an exact incumbent
from an oracle called with width 4^{-j}. Resolve this edge case before final
review. Quadratic fallback should be described as rational on every draw.

The shared-tools section has a root review at `reviews/root-counting-early.md`.
A Sol supplement will provide the generic fallback's conversion from canonical
coordinate root isolators to one shared-root tuple within a base-only
exponential budget (`author-reports/fallback-shared-root-sol.md`). Another Sol
supplement extends pure-integer lattice closure from quartics to explicit
fixed-degree piecewise-polynomial convex unaries
(`author-reports/integer-lattice-generalization-sol.md`). Incorporate these
where they simplify the complete theorem contracts; treat their elementary
extensions as part of this work, without an unsupported priority claim.

TU feasible rounding is a proved preliminary lemma under integral, aligned
right-hand sides. It is not an unrestricted expected-time TU optimizer. A
fixed-instance chamber count with uncontrolled geometric constants does not
provide such a complexity bound.

The recourse report establishes three different sampling-bit contracts. General
nonlinear boundary flow/TU has parameter-dependent precision; interior and
bilinear versions have polynomial precision. The common-root component solver
supersedes the older algebraic primitive-element restriction. It does not
provide short expanded minimal polynomials or efficient general comparisons
for sums of independent component values.

# Additional early-review corrections

The shared-root fallback supplement is now complete at
`author-reports/fallback-shared-root-sol.md`, and the foundations reviewer
has checked its proof independently. Integrate its degree-versus-height
budget and tuple-selection step in Appendix A. A base-only bound B is an
exponential multiplier, not the entire output length when the added bit
length b is arbitrary: write B poly_d(I+b). Coordinate enclosures also need
an O(log n) precision allowance to meet the model's Euclidean q-bit contract.
The exact Gaussian Taylor construction has polynomial-length intermediate
numbers; the claim that every intermediate has O(b) bits is too strong.

The front/boundaries author must resolve
`reviews/early-boundaries-sol-r1.md`: assume delta >= 0 in the threshold
crossing proposition; state that sampled guarantees do not by themselves
give a polynomial-time original-threshold algorithm; and prove level-0
nonclosure before using the level-1 bag-local deletion example. Inventory X15
includes the direct Square Root Sum quartic reduction with width two and
bounded coefficients. Either retain that precise structural boundary with
its proof or record explicitly why the manuscript keeps only the indirect
PosSLP implication. Factor encodings use sparse variable/exponent pairs,
which is needed for the width example's stated input length.

The exact small-core solver already has a common root for its coordinates.
Give the optimal value as f(r(theta)) reduced modulo its root polynomial to
meet the model's common-root value contract; retain a separate value
polynomial only as an auxiliary representation for comparisons. Its
deformed stationary equations have the claimed leading monomials for
symbolic epsilon, or epsilon != 0, not at epsilon = 0.

The complete early foundations review is available at
`reviews/early-foundations-sol-r1.md`. Its Renegar statement also needs
positive block sizes, at least one free variable in the stated version,
and positive small-log conventions. Direct evaluation deals with a
zero-dimensional singleton before thresholds or elimination are invoked.

The current draft's citation keys are collected in
`current-citation-requests.txt`. Final bibliography identity, theorem scope,
and all exact source locators must be checked by the Luna literature owner;
keys copied from source notes are not yet a completed literature audit.

The early integer interface review is being written at
`reviews/early-integer-interfaces-sol.md`. Two explanatory statements need
correction: a leading characteristic coefficient can retain a bounded
projection of a pole branch, so its roots describe finite vector limits
only after a good-form qualification and the required degree/divisibility
checks; and an affine distance-to-zero-set bound requires a nonempty zero
set. Nonzero constants and empty zero sets need a separate rational
vertex-value bound. The TU transfer theorem must explicitly carry the
fixed-degree rational cost model and core-curvature premise from its flow
antecedent, rather than relying only on the informal surrounding transfer.

The quadratic instance definition currently assumes its rational polyhedral
relaxation is nonempty, but this does not imply that the mixed feasible set
is nonempty. Require X != empty, or explicitly detect integer infeasibility
before promising an attaining optimizer. A relaxation consisting only of
x=1/2 with x native integer is the simplest allowed counterexample to the
current definition. This is a feasibility-contract correction, not a
limitation of the conditional exact algorithms.

The draft coverage audit found three gaps; decisions 10-11 in
`integration-decisions.md` now require precise coverage of B10's short
conditional-recourse count, X16's deterministic flow-core error bound, and
the direct width-two, bounded-coefficient Square Root Sum boundary from
the exact-arithmetic companion. The latter needs self-contained construction
and explicit overlap attribution, not a claim of novelty here. The PosSLP
construction has different structural scope and must remain separate.

Final front matter must identify the related unpublished companions by
precise bibliography entries and distinguish what is re-proved, overlapped,
and new to this manuscript. A generic unnamed companion paragraph is not
a relation-to-prior-work account. Literature audit owns the exact source
comparison. Do not claim the finite-law model itself is new merely because
we carry its output and bit contracts through these route-specific results.

The first introduction has a root review at
`reviews/root-introduction-early.md`. Resolve its dependence, scale
calibration, output, attribution, and section-reference issues before
finalizing the abstract and introduction.

Further early route findings (read the full upcoming reports):

- In `thm:qp:two`, choose the least sufficient Gaussian accuracy b, impose
  b <= poly(I), or retain its bit cost in the work bound. An arbitrary b
  with only a lower bound cannot have a work bound independent of b.
- The general-k growth-conditioned work bound can retain its dimension-free
  c^k(1+sqrt(kappa))^k form only with the Euclidean-volume packing argument.
  It does not follow from the displayed coarse coordinate-box count. The
  early low-rank reviewer has supplied the missing packing derivation.
- The deterministic growth-conditioned foundation should also state its
  mixed-integer version, with the convex-MIQP oracle factor f(n_z), as in
  inventory A0. The same growth transfer, rational reconstruction and
  polishing apply; this is a supported extension of the shared proof, not
  a separate new smoothing claim.
- In the actuator corollary, L_q cannot be an arbitrary possibly negative
  upper second-derivative bound if L=1+L_q+Lambda G_2 is used. Require a
  nonnegative L_q (the source bounds the absolute derivatives), or replace
  the final enclosure by max{1,L_q+Lambda G_2}.
- Inventory X8's generic threshold bound should be tied to the explicit
  Del Pia--Khajavirad NO family with gap 2^(-2r-4) and a deterministic
  witness coordinate equal to one. Give the short worked relation and
  precise source attribution, rather than leaving the connection implicit.

The blanket universal-law limitation/open question in the first discussion
is being examined in `author-reports/universal-law-budget-sol.md`. Uniform
worst-case bounds by input length may already give a common sampling budget
for polynomial-bit routes. Do not freeze this as an unresolved question
without considering that report and its parameter-dependent-flow caveat.

The moment-obstruction remark in the first quadratic draft has an incorrect
lower integration limit. If Pr(Z>t) >= a_0/t only for t >= a_0, raising Z
to k/2 moves the valid lower limit to max{1,a_0^(k/2)}, not a_0. Use that
limit with the nonempty-range qualification, or simply choose a_0=1 for
the example. The existing quadratic reviewer gives a concrete counterexample
to the uncorrected displayed bound in `reviews/early-quadratic-sol.md`.

For quadratic mixed-label closure, the current gap-to-gradient lemma assumes
h <= 1. Enforce h_J <= 1 in the terminal schedule; then its C_gap and
C_bad are independent of the Gaussian support radius. The old loop bound
J(t) <= J(0)+2t is safe; the reviewer also derives the sharper +t bound.
The conditioned algorithm must remove singleton auxiliary range coordinates
before invoking positive-width mesh formulas, while retaining their fixed
values in the inner problem.

The preliminary universal-law development is positive: polynomial-bit
routes admit one resolution M_d(I)=2^{P_d(I)} (or Gaussian accuracy b_d(I)),
scaled by the supplied sigma and keeping the perturbation model unchanged.
Uniformize effective base-only bounds, not the numerical count parameters.
For nonlinear boundary flow/TU a supplied k <= K gives a common
M_d(I,K)=2^{F_d(K)P_d(I)}; maxing over all k <= I need not preserve the
small-k bound. Wait for the complete report before replacing the discussion
claim, but do not describe uniform resolution for the polynomial-bit routes
as an open question.

The complete early sparse/domain review is at
`reviews/early-sparse-domain-sol.md`; besides the actuator correction, its
uniform-family lemma needs polynomial coefficient length and production
cost, rather than a literal I+b bound after substitutions. Align the common
descriptor with sound singleton-hull continuous fixing. Order transport
replaces the fixed-outside-feasibility step; it does not satisfy that
box-only premise literally. Handle all-fixed instances before maxima and
division by width budgets. Read the complete early integer interface report
for its marginal-cost bit premise, infeasible restriction +infinity
convention, zero-rank lattice branch, and joint component distance/value
refinement contract.

The full uniform-resolution report is complete at
`author-reports/universal-law-budget-sol.md`. Incorporate its concise
routewise corollary with proof and replace the broad limitation/open
question. Preserve its geometric-domain and oracle qualifications, the
Gaussian support/precision calculation, and the nonlinear-flow K-bound
qualification. Strong-field q_i(M) are not monotone under grid refinement;
recompute the actual beta, or use the uniform sufficient strong-noise
regime. The corollary is an elementary consequence, not a priority claim.

A first typesetting pass of the immutable complete-proof snapshot succeeded
(145 pages, no bibliography yet). It found eight overfull lines, mostly in
Appendix E's long formulas. The root will supply exact locations in
`reviews/root-typesetting-early.md` and verify final layout after references
and all scientific revisions are integrated. This first pass is not a
submission-quality build.

The complete constrained-domain reviewer found a substantive simplex-margin
statement error in frozen Appendix D: equality-budget multipliers are
unrestricted and must not be included among nonnegative active-margin
variables. Margin and closure premises must count active inequalities only:
zero-coordinate inequalities and tight resource inequalities. Exclude an
original equality-simplex budget multiplier throughout the statements and
proof, including the active-event definition and any sentence asserting
all multipliers are nonnegative. For F0=0 on x1+x2=1, x>=0, with positive
unequal coefficient draws, the equality multiplier is -min(gamma1,gamma2)
while growth is positive; demanding it exceed tau would cause frequent
fallback and defeat the expectation proof. The actual inequality-margin
argument is the intended valid one. Full finding is in
`reviews/complete-sparse-domain-sol-r1.md` when materialized.

The early quadratic report is complete at `reviews/early-quadratic-sol.md`.
Its reconstruction step must be guarded by successful value reconstruction;
remove singleton auxiliary ranges only from the search, retaining their
fixed coordinates and all rows in the full PSD inner model. Its concavity
proof uses a minimum over a compact family of affine functions, not
necessarily a finite minimum.

The complete constrained review also requires explicit coarse simplex
vertices when h>1: C intersect (h Z)^b is empty for an equality simplex at
that coarse level. Use the original simplex vertices there and the bounded
fine-cell indices once h<=1. Skip zero-dimensional inequality blocks before
the center formula divides by sum_i(u_i-l_i). Every evaluator must have a
direct point-patch branch, including implicit graphs whose exact dependent
roots still need evaluation; GLS is not invoked on a zero-dimensional body.

The integer-flow model must expressly assume its residual feasible set is
nonempty (or run one feasibility solve and return infeasibility before
optimization); the all-optimal-cores-interior premise is otherwise vacuous.
The marginal-cycle necessity proof must include two-cycles on different
parallel arcs, and self-loops if the model allows them, using the same
feasible one-unit negative-cycle augmentation argument.

Original-objective approximation retains all numerical parameters. Fixed
structure alone does not make its work polynomial in I and 1/epsilon if
binary-encoded L, widths, supplied concave curvature or coupling-derived
curvature can be exponentially large. State the resulting bound after
substituting sigma, and say polynomial in 1/epsilon with other numerical
parameters fixed; polynomial in I and 1/epsilon needs polynomially bounded
numerical factors. Apply this qualification consistently in model,
introduction, abstract and discussion. Gaussian calibration includes its
actual (b+20) sigma support and aligned calibration the projected widths.

The integrated introduction must scope rational quadratic outputs to the rational
polyhedral/box classes. A quadratic objective on an implicit graph can have an
irrational algebraic lift (for example y^2=2). The phrase "all three routes
need a fixed feasible set independent of search coordinates" also overstates
the common premise: graph/chart and order-transport results replace that
literal box premise with their proved curvature and noise-comparison
invariants. State the direct recourse premise and these replacements plainly.

The complete front/boundary Sol review additionally requires mu_0>0 in
lem:lim:amplifier; the actual positive-modulus reduction instantiations are
valid. Del Pia--Khajavirad's nonnegative construction combines binary
penalties x(1-x) and squared residuals, so describe it accordingly rather
than calling every summand an affine-residual square.

Complete boundary review corrections also scope width-two/bounded-coefficient
point hardness to Square Root Sum, not the unrestricted PosSLP construction,
in every summary table and prior-work paragraph. The width barriers rule out
the analyzed retention/local-substitution rules; conditional values are one
sufficient improvement, not a proved necessary ingredient of every width-FPT
algorithm. Uniform-resolution proofs bound logarithms of algebraic format
counts: native-label disjunctions can have exponentially many atoms.

Shared-tools finite-law motivation must say bounded worst-case random bits
force finite support; a Turing machine can sample countably infinite-support
rational distributions. Discussion independence is in the coordinates of
each perturbation model, not every original coefficient under aligned noise.
The prescribed-small-epsilon original-objective consequence uses routes
valid at arbitrary positive sigma; strong-field lower-scale conditions do
not permit that calibration in general.

Original-objective calibration uses W_noise for the chosen model throughout,
not original coordinate widths in the aligned recipe. Handle W_noise=0
separately. Dyadic Gaussian calibration may choose t>=0 and
R=max{1,W_noise/epsilon}; use positive logarithms and retain the bound
1/sigma<=R poly(I0+log R), including the exact (b+20)sigma support.
A least adequate t is computed with the effective polynomial bit envelope.

The Opus editorial interim findings P1--P5 are adjudicated in
review-disposition-editorial-r1.md. The exact-arithmetic companion already
contains the noisy-core quartic point obstruction and also has a positive
residual-convex cubic theorem; do not overlook this degree distinction or
claim the core-only consequence as new. The decomposition-aware companion's
growth-conditioned graded-grid FPT result and sparse-indicator companion's
indicator-only grid noise require precise comparisons. FPT summaries must
include numerical ratios in the parameter, not merely call them polynomial
in input length. Application analogies require the actual law and fixed
residual feasibility. The nonquadratic strong-field sufficient scale is
severe, but there is no evidence for a practical impossibility verdict.
