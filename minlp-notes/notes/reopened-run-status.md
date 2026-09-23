# Reopened run: status of work (updated 2026-09-05, evening)

## Final status: closed at the user's request

All started directions were reconciled with their proof and source records.
The [current closeout](research-continuation-closeout.md) supersedes every
historical active, pending, and unfinished label below. The final batch
completed the signed-polynomial inverse and fixed-resource bilevel
algorithms, two-quality pooling and contracted common-capacity algorithms,
energy maximization, and the weighted path-sign corollary. Independent
final-scope audits passed; existing ETR results received a closing audit.
Remaining questions are explicit unresolved boundaries, not asserted
results or active tasks. No further research directions were started.

The remainder is preserved as a chronological record.


## Existential-theory-of-the-reals results (2026-09-05, latest)

- [Pooling is `∃R`-complete](../results/pooling-existential-theory-of-reals.md):
  two full audits passed with corrections (applied), novelty audit found no
  prior statement for pooling or blending networks, bounded-data variant
  audited. Consequence: pooling is not in `NP` unless `NP = ∃R`; rational
  instances can require optimal flows of arbitrary algebraic degree.
  Open and recorded: one attribute with upper bounds only.
- [One pool with bypasses and many attributes](../results/pooling-one-pool-bypass-existential-reals.md):
  two audits passed with minor corrections (applied).
- [AC and resistive power flow](../results/ac-power-flow-existential-reals.md):
  three audits (the first two found and the third confirmed the fix of an
  angle-semantics flaw in Theorem 2); all corrections applied; novelty
  audit found no prior `∃R` statement for power flow.


## Latest vector, structural, and correlated-uncertainty results

The [one-input convex-vector curvature-rank theorem](../results/convex-vector-curvature-rank-precision.md)
gives a compact rational MILP with at most `p_conv+12+ceil(log2 r)` binaries.
Here r is the rank of normalized output polynomials modulo affine terms.
The [explicit unconditional polyhedral-body extension](../results/convex-vector-facet-curvature-rank-precision.md)
uses the rank of positive facet scalarizations and adds `13+ceil(log2 r)`;
weighted one-norm error gives constant overhead 13 regardless of output count.
For [arbitrary unconditional oracle bodies](../results/convex-vector-unconditional-compiled-precision.md),
a near-optimal product box gives `14+ceil(log2 m)` without putting the body's
oracle or nonlinear constraints into the final MILP. These have two complete
proof audits and qualified source comparisons.

The [bilevel leader-interaction boundary](../results/bilevel-leader-vertex-integrity-boundary.md)
gives exact polynomial optimization with fixed core and component size,
weak NP-completeness even on an interaction path, and exponential explicit
message size with identical constant-coefficient local factors. Both reviews
passed. Earlier PWL elimination and neural-network hardness are credited;
the precise structural boundary is retained with qualified priority.

The [correlated-cycle flow algorithm](../results/potential-flow-cycle-polytope-resistance-design.md)
permits a full rational resistance polytope within each cactus cycle. It
computes exact individual extrema and rational optimizing profiles, exact
capacity-feasible witnesses, and additive convex design. Cycles remain
independent and nominations fixed. Two full audits passed. The abstract
[monotone polynomial-root arithmetic lemma](monotone-polynomial-root-polytope-optimization.md)
has also passed two audits, including variable dense degree and fixed
piecewise-polynomial partitions. Its classical quasilinear and arithmetic
antecedents are explicit; it is supporting theory for further law extensions.


## Latest extension: all dense convex polynomials

The [compiled convex polynomial theorem](../results/convex-polynomial-compiled-integer-precision.md)
now removes both positive-coefficient and monotone-curvature assumptions.
It constructs a polynomial-size rational MILP with integer count at most
`p_conv+11` for a scalar graph, `p_conv+16r` for separable scalar sums,
and `p_conv+13r` for independent outputs. Both complete proof audits passed,
including certified integration with signed polynomial coefficients.
The algorithm combines known greedy chord segmentation with a succinct
curvature construction when explicit segmentation would be too long.
The comparison is against arbitrary convex lifts with general integers;
it does not make solving the resulting MILP polynomial time.


This note records what is finished and what is not in the run reopened on
2026-09-04. Update it whenever a pending item changes state. "Reviewed"
means checked by an independent research agent, not by a journal.

## Continuous research resumed on 2026-09-05

The user authorized continued research until interruption or usage limits.
The goal is active. The historical unfinished list below describes the prior
session; this section supersedes its statuses.

- **Shape-sensitive separable construction now verified:** the
  [new theorem](../results/separable-convex-graph-linear-dimension-precision.md)
  passed two final-scope audits and source comparison. Dense positive
  polynomial scalar sums admit `p_out<=p_conv+12r`; independent outputs
  admit `9r`. Its finite version covers arbitrary continuous convex
  summands with `7r` and `4r`, respectively, without a compactness claim.
  The [scalar algorithm](../results/compiled-curvature-quantile-precision.md)
  passed two full audits including certified curvature integration.
  The broader arbitrary-coefficient convex-polynomial construction is
  currently a candidate under review. A separate vector example explains
  why scalarization and uniform midpoint tests do not settle that scope.

- **Rational linear versus conic encoding:** the
  [new separation](../results/small-exponent-milp-soc-encoding-separation.md)
  passed two full audits, as did its tight rational-MILP lower/upper bound.
  At fixed graph error `1/16`, `x^(1/2^B)` requires `Theta(2^B)` total
  rational MILP encoding but has a polynomial-size rational MISOCP; four
  binaries suffice in both. The construction applies classical conic
  optimality and repeated squaring. Exact conic feasibility is required;
  no tolerance-stable numerical guarantee or new duality claim is made.

- **Pooling feasibility degree boundary:** the
  [endpoint-projection algorithm](../results/pooling-degree-two-boundary-projection.md)
  passed two full audits through exact reconstruction and fixed-support
  optimization. With one pool, two feeds/outlets, and input total degree
  at most two, feasibility is polynomial at output total degree two and
  strongly NP-complete at output degree three, even with fixed numerical
  alphabets. The hard side keeps exact positive flow contracts. Dense-profit
  optimization on degree-two bypasses remains unresolved.

- **Sparse exponent construction now verified:** the
  [rational-power theorem](../results/rational-power-compiled-integer-precision.md)
  passed two final-scope audits for all rational exponents greater than one,
  including exponents arbitrarily close to one. It gives `7r+1` binary
  overhead and polynomial size in the binary exponent encoding.
  The [sparse positive-mixture extension](../results/sparse-positive-polynomial-circuit-precision.md)
  also passed two audits, retaining its log-log degree count while removing
  numerical-degree dependence from construction size. Classical circuit
  compilation, interpolation, and base-two product encoding are explicitly
  credited. A separate small-exponent concave-power encoding obstruction
  remains under review.

- **Latest compact precision bounds:** two independent full audits passed
  the [pure-power theorem](../results/positive-pure-power-linear-dimension-precision.md),
  with `p_out<=p_conv+6.5r+1` independent of degree, and the
  [positive-mixture theorem](../results/positive-polynomial-loglog-degree-precision.md),
  with overhead `4.5r+sum_i ceil(log2(ceil(log2(D_i))+1))+1`.
  Both constructions have polynomial rational size in dense degrees and
  permit unconditional output-error bodies with strong separation and radii.
  The [certified positive rational approximation lemma](positive-rational-stieltjes-power-approximation.md)
  closes the pure-power construction's near-zero and bit-complexity issues;
  the approximation mechanism is credited to established resolvent quadrature.
  A twice-reviewed [benchmark obstruction](positive-polynomial-allocation-degree-gap.md)
  proves that coefficient-sum allocation can lose order `log log D` already
  in one dimension. It does not prove such an algorithmic overhead necessary.
  Reviewed [PSD block](../results/block-psd-unconditional-error-precision.md),
  [integer-feature](../results/independent-integer-feature-quadratic-precision.md),
  and [forest Laplacian](../results/forest-laplacian-quadratic-precision.md)
  refinements are also retained.

- **Conditioning boundary now verified:** two full audits passed both
  [the additive algorithm](../results/bilevel-conditioned-box-additive-algorithm.md)
  and [near-identity-Hessian exact hardness](../results/bilevel-well-conditioned-box-exact-hardness.md).
  With fixed leader dimension, a unit-box positive-definite quadratic
  follower and affine upper objective admit `epsilon*||a||_1` approximation
  in time polynomial in input bits, condition number, and `1/epsilon`,
  independently of the numerical magnitudes of the affine follower costs
  or direct leader costs. Exact optimization is nevertheless NP-complete
  with a scalar leader, no upper constraints, condition number below two,
  and all coefficient magnitudes bounded by two. The exponentially small
  reduction gap rules out polynomial dependence on accuracy bits, while
  remaining compatible with the positive approximation theorem.

- **Scalar-leader quadratic bilevel hardness:** the
  [new NP-completeness result](../results/bilevel-scalar-leader-spd-box-np-completeness.md)
  passed two final-scope audits. It has no upper constraints, an affine
  upper objective, and a unique follower optimum over a fixed unit box
  with fixed positive-definite Hessian. A jointly convex sum-of-squares
  lower objective is available when its leader-only quadratic term is
  retained. The reduction gives a zero-versus-two upper objective gap;
  it does not establish strong hardness or a well-conditioned boundary.

- **Weighted potential boundaries:** the
  [fixed-nomination one-cycle hardness theorem](../results/potential-flow-weighted-potential-cycle-hardness.md)
  and [fixed-resistance tree nomination boundary](../results/potential-flow-weighted-tree-np-completeness.md)
  passed two audits and source comparisons. The former uses discrete
  resistance choices and a three-terminal objective; the latter uses growing
  objective support. Resistance scaling amplifies potential gaps and gives
  the stated fixed absolute-error barriers; it leaves flows unchanged and
  does not imply a constant-error arc-flow barrier.
  The [fixed-support tree algorithm](../results/potential-flow-fixed-support-weighted-tree.md)
  and [fixed-global-rank extension](../results/potential-flow-fixed-support-global-rank.md)
  have now passed two full audits and source comparisons. The first returns
  rational optima and permits finite resistance sets; the second returns
  algebraic optima and requires continuous resistance intervals.
  General tree threshold NP membership also passed independent review,
  extending the hardness boundary to NP/coNP-completeness of the full class.

- **Structured nonconvex bilevel optimization:** the
  [new algorithm](../results/bilevel-fixed-aggregate-response-algorithm.md)
  passed two full audits, an independent degree/common-field audit, and
  a source assessment. Fixed leader, resource, and aggregate dimensions
  suffice despite many follower variables and a nonconvex aggregate
  follower objective. Polynomial moving bounds and aggregate matrices
  are allowed; constraint normals stay fixed for the attainment theorem.
  The algorithm selects global follower responses by quantified comparison
  and returns an exact algebraic optimal pair. Only structural dimensions
  are fixed; dense or unary-encoded polynomial degrees may grow.
  The [fixed-dimensional local-block extension](../results/bilevel-fixed-block-response-algorithm.md)
  has also passed two full audits and permits arbitrarily many local
  inequalities per positive-definite quadratic block.
  The [infimum and pessimistic-semantics extension](../results/bilevel-compressed-response-infimum-semantics.md)
  passed two final-scope audits, including polynomial local normals with
  changing rank. It computes exact infima, decides attainment, and handles
  upper constraints imposed on all globally optimal follower responses.

- **Strong one-pool hardness with fixed numerical alphabets:**
  [new theorem](../results/pooling-constant-data-two-feed-np-completeness.md)
  passed two full audits. One pool with exactly two feeds and two outlets,
  one scalar upper quality, zero lower flows, input out-degree two and
  output in-degree three suffice. Every physical coefficient lies in a
  fixed finite set and the threshold is linear in network size. Independent
  checks solve the compiled physical network, without imposing the
  intended signal identities as extra equations. The proof also yields a
  supporting LP representation lemma using bounded-degree blending
  circuits. A dedicated novelty assessment is running; no approximation
  or perturbation-robustness lower bound follows from the exact threshold.

- **Latest formulation refinement:** the
  [input-rank theorem](../results/quadratic-nonlinear-input-rank-precision.md)
  passed two distinct independent audits. For rational quadratic systems
  and symmetric output-error bodies with strong separation and known radii,
  polynomial construction uses at most `O(r log(r+1))` more binaries than
  the minimum unrestricted-integer convex-lift dimension. Here `r` is
  stacked-Hessian rank. Common-kernel quotienting and zonotope methods are
  credited as established ingredients; the integer-count guarantee carries
  the candidate contribution.
  The [diagonal convex-quadratic refinement](../results/diagonal-psd-quadratic-linear-dimension-precision.md)
  also passed two audits and a source assessment: componentwise tolerances
  admit polynomial rational construction with `p_out<=p_conv+5r+1`.
  The [positive separable polynomial theorem](../results/positive-separable-polynomial-integer-precision.md)
  has since passed two audits and source comparison. It gives
  `p_out<=p_conv+2 sum_i log2(D_i)+4r+1`, including growing dense degrees.
- **Discrete flow capacity boundary:** the
  [rank-three hardness theorem](../results/potential-flow-discrete-arc-capacity-hardness.md)
  and [series-parallel validation theorem](../results/potential-flow-series-parallel-arc-validation.md)
  each passed two audits. Exact robust arc validation with independent
  discrete resistance uncertainty is polynomial at block cycle rank at
  most two and coNP-complete already at rank three. The positive result
  does not assert polynomial time for unbounded-rank series-parallel graphs
  with uncertain nominations. Older nonlinear tolerance literature remains
  a priority caveat.
  The subsequent [single-envelope algorithm](../results/potential-flow-series-parallel-envelope-optimization.md)
  handles fixed nominations on arbitrary series-parallel graphs in
  polynomial additive bit time. Its [exact-arithmetic companion](../results/potential-flow-series-parallel-exact-arc-barrier.md)
  and [uncertain-nomination hardness companion](../results/potential-flow-series-parallel-nomination-hardness.md)
  also passed two audits. The [scope map](potential-flow-complexity-map.md)
  records their distinct assumptions and inequality conventions.

- **All-degree-two pooling:** [new result](../results/pooling-all-degrees-two.md)
  passed two independent reviews and extensive numerical checks. Strong
  NP-hardness holds with all four degrees exactly two, unit capacities,
  and bounded costs; the profit version has no PTAS. Positive-purity-tolerance
  robustness is reviewed in its linked extension.
- **Bilinear graph integer dimension:**
  [new result](../results/bilinear-graph-binary-complexity.md) passed two
  independent reviews, including its rational preprocessing guarantee.
  The leading accuracy coefficient is fractional vertex cover, even for
  arbitrary convex lifts and unrestricted integers. Weighted accuracy LP
  bounds and compact constructions are included. The
  [scalar quadratic rank extension](../results/quadratic-rank-integer-complexity.md)
  also passed independent review: the leading coefficient is half the
  Hessian rank, independently of signature.
- **Spatial B&B:** the original result passed a second review, with the
  infimum and objective-bound-tightening scope corrected. Its
  [SDP–RLT strengthening](../results/spatial-bb-sdp-rlt-exponential-lower-bound.md)
  passed an independent review. The
  [higher-order result](../results/spatial-bb-higher-sos-exponential-lower-bound.md)
  also passed independent review, including its unique-minimizer perturbation.
  Product-domain, local polynomial auxiliary, and relative-tolerance
  direct-product extensions passed review and are promoted. A known clique
  inequality closes these particular instances. The stronger
  [sparse-XOR construction](../results/spatial-bb-quadratic-cut-exponential-lower-bound.md)
  and [monomial-lift extension](../results/spatial-bb-monomial-lift-exponential-lower-bound.md)
  passed two proof audits and are promoted; they survive all quadratic
  inequalities of the node box, under the stated hierarchy and cover model.
- **Scalar binary-count draft:** now independently reviewed, corrected, and
  retained in [its result file](../results/mip-relaxation-binary-lower-bounds.md).
- **Geoffrion:** [reviewed result](../results/geoffrion-property-p-conjecture.md)
  disproves the unrestricted exact P-prime implication. The informal
  computational Property P conjecture remains unresolved by this example.
- **Cactus potential comparison:** the single-entry/single-exit exact
  Square-Root-Sum equivalence passed independent proof review and a separate
  novelty audit; see the
  [result](../results/potential-flow-cactus-square-root-sum.md).
  The [multi-entry additive algorithm](../results/potential-flow-cactus-additive-optimization.md)
  passed two proof audits and a separate novelty audit. It returns a rational
  feasible nomination and value interval in polynomial bit time and requested
  precision. The [bounded block cycle-rank extension](../results/potential-flow-bounded-block-rank.md)
  also passed two proof audits and a separate source audit.
  [Joint resistance uncertainty](../results/potential-flow-joint-resistance.md)
  and [exact arc-capacity validation](../results/potential-flow-exact-arc-capacity.md)
  each passed two proof audits. The joint model itself is prior work; a
  dedicated source audit of the exact arc-capacity guarantee is running.
- **Fixed-core constructive optimization:**
  [theorem and pooling corollaries](../results/fixed-core-block-polyhedral-optimization.md)
  passed two full proof reviews.
  The fixed-input/fixed-pool class allows unrestricted qualities and bypasses.
  The fixed-pool/fixed-quality class allows unrestricted inputs and outputs
  but excludes arbitrary bypasses. The final 2016 primary source resolves
  the apparent conflict with an unproved 2014 abstract and explicitly lists
  these combinations as open. The [fixed-terminal portion is NP-hard](../results/pooling-two-pools-two-outputs-hardness.md)
  already with two pools and two outputs; two independent audits passed.
  Separate bounded novelty audits found no matching later results.
- **General quadratic systems:** the [noncommutative-rank law](../results/quadratic-system-noncommutative-rank-complexity.md)
  extends the graph and scalar integer-precision theorems. Two full proof
  reviews and a separate novelty audit passed. The cross-product example
  separates the answer from the maximum
  rank of an ordinary scalar Hessian combination.
- **Facial quality structure:** the [universal integrality characterization](../results/pooling-facial-quality-integrality.md)
  passed independent review. It also yields a fixed-pool, fixed-quality
  algorithm with arbitrary bypasses when output specifications cut out faces
  of the input-quality convex hull.

The research log records subsequent changes. No bounded novelty search is
treated as proof of publication priority.

### Further verified generalizations

- [Rational quadratic construction](../results/quadratic-ncrank-rational-construction.md):
  reviewed deterministic polynomial bit-time construction with uniform
  polynomial input-size overhead around the noncommutative-rank law.
- [Smooth-map local rank](../results/smooth-map-local-rank-integer-complexity.md):
  two audits passed. A classical mixed-Hessian oscillatory estimate gives
  the local lower bound; fixed-degree polynomial maps have compact upper
  formulations. The [constant scalar Hessian-rank theorem](../results/constant-hessian-rank-smooth-precision.md)
  and [positive perspective transfer](../results/perspective-integer-precision.md)
  also passed independent review.
- [Finite unequal-accuracy quadratic law](../results/quadratic-weighted-covariance-precision.md):
  two audits passed. Maximum determinant under covariance-energy bounds
  characterizes integer dimension within a dimension-only additive term.
  The [polynomial bit-time construction](../results/quadratic-weighted-precision-polynomial-construction.md)
  also passed two audits and is promoted. It uses only a dimension-only
  additive number of binaries above the arbitrary-convex-lift optimum.
- [One-pool bypass NP-completeness](../results/pooling-one-pool-bypass-np-completeness.md)
  and its [NP-membership lemma](../results/fixed-parameter-linear-fibers-np-membership.md)
  each passed two audits. Exact supply/demand contracts are essential to
  that earlier construction. The stronger
  [upper-bounds-only theorem](../results/pooling-one-pool-upper-bounds-np-completeness.md)
  now passed two audits: one scalar upper quality, zero lower flows, input
  out-degree at most two, output in-degree at most three, and upper flow
  bounds at most four. An explicit polynomial-bit exact penalty removes
  the contracts. The fixed-pool/fixed-terminal theorem is also upgraded to
  NP-completeness using the reviewed split-fraction NP certificate.
- [Structured bypass pooling algorithm](../results/pooling-bypass-structure-algorithm.md):
  two audits passed. Fixed pool count, affine quality rank, and bypass
  vertex integrity suffice for exact polynomial bit-time optimization.
  This subsumes both earlier pooling corollaries.
- [Fractional-power exact arc barrier](../results/potential-flow-fractional-power-arc-barrier.md):
  proof and source audits are complete. A fixed fractional-power law makes
  exact capacity comparison Square-Root-Sum-hard on one cycle, including
  every fixed reduced exponent greater than one with even denominator.
  This does not imply an additive-approximation barrier.
- [Discrete resistance uncertainty](../results/potential-flow-discrete-resistance-hardness.md):
  two audits and a separate source comparison passed. Independent two-point
  choices make high-precision pressure optimization NP-hard on one rank-two
  theta block with a bridge and maximum degree three. The gap is not a
  strong-hardness or fixed-accuracy obstruction.

The [dense piecewise-polynomial affine-law extension](../results/potential-flow-polynomial-law-uncertainty.md)
has passed two audits and is promoted.
[Fractional-power additive optimization](../results/potential-flow-fractional-additive-optimization.md)
has also passed two proof audits and is promoted, including a fixed finite
family of exponents in `(1,3)`. Research continues; none of
these milestones closes the user's active goal.

## Finished and verified

- **One-quality pooling with degree-two pools is strongly NP-hard**
  ([result](../results/pooling-one-quality-degree-two-hardness.md)).
  Answers open problems 2 and 3 of Boland, Kalinowski, Rigterink (2017).
  Theorems 1–2 passed two independent reviews (one with corrections,
  applied); the degree-three refinement (Lemma 2, Theorem 3) passed a third
  review with minor corrections (applied). Gurobi and exact-LP cross-checks,
  an exhaustive small-instance checker, and a brute-force gadget check all
  passed. Novelty audit in [the companion note](pooling-degree-two-novelty.md).
  The all-four-degree-two pattern was subsequently resolved in the
  continuation recorded above.
- **Exponential lower bound for spatial branch-and-bound with separable
  relaxations** ([result](../results/spatial-bb-exponential-lower-bound.md)).
  One independent review passed with corrections (a `max`/`min` error in the
  theorem statement, the scope `k, n-k = Θ(n)`, and a Remark 3 condition;
  all applied). Numerical checks passed. A novelty search found no prior
  spatial-B&B tree-size lower bound of this kind; the related work is listed
  in the result. A second independent review was completed in the
  continuation above, with minor scope corrections applied.

## Started but not finished (agents were still running when usage limits
## approached)

- **Geoffrion (1972) Property (P) conjecture without compactness**: an agent
  was asked to verify a candidate counterexample and prove a positive
  sufficient condition, writing `results/geoffrion-property-p-conjecture.md`
  and `code/geoffrion_property_p/`. If the file exists it has NOT been
  independently reviewed unless a review note is linked from it.
- **Lower bounds on the number of binaries in MIP relaxations of `x^2` and
  `xy`** (sawtooth optimality): agent writing
  `results/mip-relaxation-binary-lower-bounds.md` and
  `code/mip_relaxation_binaries/`. Unreviewed unless a review is linked.
- **Pooling with all degrees at most two**: exploratory agent writing
  `notes/pooling-all-degrees-two-investigation.md`; any theorem would be in
  `results/pooling-all-degrees-two.md`. Unreviewed.
- **Maximum potential difference on cactus graphs** (open in the 2026
  survey of Pfetsch, Schmidt, Skutella, Thürauf): exploratory agent writing
  `notes/potential-flow-mpd-cactus-investigation.md`. Unreviewed.

Any of these files present in the repository without a linked review should
be treated as unverified drafts. Candidate directions not started are listed
in the [research log](log.md) entry for this session.
