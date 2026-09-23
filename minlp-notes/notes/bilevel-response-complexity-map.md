# Scope map for the bilevel response results

Updated: 2026-09-07 (UTC). This compares reviewed statements rather than proving
a new theorem. Independent agent review and publication-priority assessment
are separate; the linked files retain both records.

## Later continuation

The [continuation closeout](bilevel-reopened-closeout.md) records the completed
extensions, independent reviews, code, source comparison, and retained negative
findings. The older rows below keep their original scopes; they are not claims
that later extensions remain open.

The [classical positioning](bilevel-classical-positioning.md) compares fixed
follower and fixed structural dimensions, and separates XP-type guarantees
from formal FPT claims. The [paper scope](bilevel-paper-scope.md) selects a
primary model and keeps the semantics and output guarantees distinct.

| Additional structure or response semantics | Reviewed conclusion |
| --- | --- |
| Quadratic local blocks, fixed aggregate/resource dimensions, cost-near-optimal follower set, fixed measurement count per upper criterion | [Exact robust feasibility, infimum, attainment, and adversarial witnesses](../results/bilevel-near-optimal-response-robustness.md). Aggregate costs may be nonconvex; upper-criterion count may grow. Fixed normals plus convex aggregate costs ensure attainment. |
| Dense SPD box follower with a certified surrogate response cover | [Exact global recovery in at most `M*3^t` LPs](../results/bilevel-surrogate-screening-exact-optimization.md). An explicit perturbation radius gives `t<=(r+1)q` from bounded vertex transition multiplicity. No automatic small-ambiguity or good-surrogate promise. |
| Strictly convex dense polynomial local costs plus convex polynomial aggregate coupling | [Global approximation polynomial in accuracy bits](../results/bilevel-convex-aggregate-accuracy-bit-algorithm.md), with fixed leader, aggregate, and resource dimensions and exactly feasible rational leader output. |
| Explicit polynomial upper objectives and constraints in the polynomial-cost models | [Bicriteria approximation without regularity; exact rational feasible approximation under a tightening modulus](../results/bilevel-response-constraint-accuracy-bit-algorithm.md). Concrete sufficient conditions use convex reduced constraints and a strict anchor, or reserve controls with uniform headroom. |
| Scalar leader and supplied diagonal-plus-low-rank quadratic follower | [Exact certified response-path prototype](bilevel-reopened-quadratic-algorithm.md), with affine response constraints and tariff objectives. General numerical proposals can fail explicitly; a separate aligned rank-one sweep is complete and exact. |
| One aligned scalar tariff; diagonal local quadratics minus a rank-one quadratic aggregate | [Exact nonconvex global-response implementation](bilevel-nonconvex-scalar-algorithm.md), including every true tie, affine upper rows, optimistic optimization, and robust pessimistic supremum/attainment. Complete rational-input algorithm; output degree at most two. |

Two distinct boundaries remain important: exact quadratic near-optimal robustness
uses a fixed number of measurements per criterion, while polynomial-cost
approximation can handle arbitrary explicitly encoded polynomial upper criteria
with the stated error/margin guarantees. These conclusions must not be exchanged.

The leader dimension is fixed in the first table. Input and objective
coefficients are rational. Exact optimization, additive approximation,
and producing a rational near-optimal leader have different arithmetic
requirements.

| Follower structure and upper model | Reviewed conclusion |
| --- | --- |
| Positive diagonal quadratic local costs, fixed resource and aggregate dimensions; polynomial aggregate cost may be nonconvex | [Exact optimistic optimization is polynomial](../results/bilevel-fixed-aggregate-response-algorithm.md). Global follower optimality is verified through compressed responses, rather than inferred from stationarity. |
| Fixed-dimensional positive-definite quadratic local blocks, fixed aggregate dimension | [Exact polynomial optimization](../results/bilevel-fixed-block-response-algorithm.md), with arbitrary many local polyhedral rows. |
| Supplied diagonal-plus-fixed-rank quadratic coupling; box follower | [Exact rational LP-cell optimization](bilevel-fixed-rank-quadratic-corollary.md). This is an attributed structural corollary, not a new decomposition algorithm. |
| Diagonal box follower with local costs z_i^(p_i+1)/(p_i+1), positive rational scaling, affine leader dependence and affine upper objective; no response-dependent upper constraints | [Rational additive optimization is polynomial in input bits, accuracy bits, and numerical P=max p_i](../results/bilevel-bounded-power-accuracy-bit-algorithm.md). Only leader dimension is fixed. Unary or dense powers are covered; exact common-field follower/value output is not asserted. |
| Separable strictly convex dense polynomial local costs, one signed resource equality, affine upper objective; no response-dependent upper constraints | [Rational additive optimization is polynomial in input bits, numerical degree, and accuracy bits](../results/bilevel-one-resource-accuracy-bit-algorithm.md). A scalar monotonicity identity converts balance residual directly to weighted response error; arbitrary signed marginal coefficients are covered. |
| Separable strictly convex dense polynomial local costs, fixed number of rational resource inequalities/equalities, affine upper objective; no response-dependent upper constraints | [The same accuracy-bit guarantee holds for fixed leader and resource dimensions](../results/bilevel-fixed-resource-accuracy-bit-algorithm.md). The resource matrix is independent of the leader. Exact leader feasibility, bounded multipliers, Hoffman repair, and a degree-dependent convexity modulus cover degenerate faces and interior zeros of marginal derivatives. |
| Dense fixed SPD quadratic box follower; one leader, affine upper objective, no upper constraints | [Exact threshold is NP-complete](../results/bilevel-well-conditioned-box-exact-hardness.md), even with coefficient magnitudes at most two and condition number below two. Coupling can be arbitrarily close to the identity. The gap is exponentially small. |
| SPD quadratic box follower, affine upper objective, fixed leader dimension | [Additive error epsilon times the follower-objective one-norm is achievable in polynomial time in input size, condition number, and 1/epsilon](../results/bilevel-conditioned-box-additive-algorithm.md). This does not give polynomial dependence on accuracy bits. |

For the power-cost algorithm, a dyadic arrangement controls clipped root
arguments. Rational polynomial approximations can then be optimized in the
fixed leader dimension. Approximation within a cell and rational recovery
preserve exact leader feasibility without an exact sum-of-radicals oracle.
Its source comparison credits earlier algebraic-function approximation,
including Vigneron's bit-model discussion; the dependence on accuracy bits
in this restricted model is the candidate distinction.

The resource extensions remove the restriction to independent follower coordinates and positive marginal coefficients. The [general inverse lemma](certified-monotone-polynomial-inverse-approximation.md) supplies rational polynomial approximations even when a strictly increasing marginal has interior derivative zeros. With fixed resource dimension, the exact feasible-leader set has a polynomial-size rational description. Approximate dual feasibility and complementarity then control the entire follower response through polynomial-bit error bounds, while the final rounding preserves exact leader feasibility. The one-equality identity is sharper; the general fixed-resource proof does not assume that identity survives for multiple rows.

These are global additive approximation results for the induced signed upper objective. The [source comparison](bilevel-resource-accuracy-bit-novelty.md) explicitly credits earlier logarithmic-accuracy resource-allocation algorithms and algebraic-sum approximation, as well as the established Hoffman and KKT tools. No matching combined theorem was found in the checked sources; this remains a qualified novelty assessment. Both resource proofs and their signed-marginal extensions passed two independent audits.

If p is supplied only in sparse binary encoding, two power responses
x^(1/p) and x^(2/p) give a fixed-error objective whose near-optimal rational
leaders need Omega(p) bits. This is an output-length obstruction, not a
claim that every compressed algebraic output model is hard. Dense local
quadratic coupling has a separate combinatorial obstruction even though
its coefficient magnitudes and condition number are controlled.

## When the number of leaders grows

The [leader-interaction theorem](../results/bilevel-leader-vertex-integrity-boundary.md)
uses a supplied fixed-size core whose deletion leaves components of fixed
size. It gives exact rational optimization for the stated diagonal box
follower and affine upper objective. Fixed treewidth alone does not provide
the same result: an interaction path already supports weak NP-completeness.
That reduction has a normalized gap inversely proportional to the encoded
subset-sum scale; it does not prove strong hardness.

The same note gives an unconditional representation obstruction: identical
constant-coefficient local factors along a path generate an exact
elimination message with 2^(n+1)-1 affine pieces. This concerns explicit
piecewise-linear messages and does not exclude compressed representations
or contradict the established closure of piecewise-linear functions under
elimination.

## Semantics that must remain explicit

The [full compressed-response framework](../results/bilevel-compressed-response-infimum-semantics.md)
distinguishes infima from attained minima and permits its stated pessimistic
follower semantics. Those guarantees should not be silently imported into
the simpler approximation models above. Additional response-dependent
upper equalities can create exact algebraic feasibility questions that
uniform response approximation does not solve.
