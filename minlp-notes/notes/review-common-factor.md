# Independent audit of the common-factor investigation

Date: 2026-09-04. Reviewer: independent common-factor audit agent.

Scope: mathematical correctness of `notes/common-factor-investigation.md`, rather than publication novelty. The fixed-linking-row theorem and reciprocal-anchor PSD cut pass this audit under their stated assumptions. Two additional hull observations below are proved here, but require another independent review before promotion to a result file. No novelty claim is made for them.

## 1. Fixed-linking-row theorem

The bounded-variable basis enumeration is sound. In particular:

- Adding bounded slacks preserves the feasible set and makes the equality matrix have full row rank for every scalar value. A negative interval-arithmetic slack upper bound can safely be replaced by any positive upper bound: either bound is only an auxiliary bound, and every feasible slack is nonnegative.
- The lexicographic reduced cost of a nonbasic variable can never vanish as a formal polynomial in the perturbation parameter: its own perturbation coefficient is one and no basic coefficient has that index. This holds pointwise wherever the basis is nonsingular, not merely as a rational-function identity. Tied original costs are therefore covered.
- A primal-dual optimal bounded-variable basis exists for a nonempty bounded LP of full row rank, including degenerate vertices and fixed variables. This is the needed coverage fact. An arbitrary basis at an optimal vertex need not work.
- Multiplication by the basis determinant produces reduced-cost coefficient polynomials of degree at most `k+1`. For basic coordinates, multiplication by `x D(x)` produces numerator degree at most `k+1`. Comparison with a bound `r+s/x` therefore still has degree at most `k+1`. The objective numerator has degree at most `k+2`, and the derivative numerator has degree at most `2k+2`.
- The union of the finitely many partition endpoints must be processed explicitly. This captures isolated feasible scalar values, determinant roots, and the case `a=b`. Compactness makes every limit along a feasible candidate interval feasible.
- For fixed `k`, all scalar endpoint and stationary-point degrees are bounded by a function of `k`, and coefficient heights have polynomial bit length. Conditional LPs at endpoints can alternatively be solved by the same finite basis enumeration over the endpoint's fixed-degree algebraic field, avoiding any need to invoke a general algebraic-input LP algorithm. Every endpoint has some nonsingular basis because of the slack identity columns.
- For `k=0`, the single empty basis has determinant one. The proof reduces to separately choosing interval endpoints for each leaf and minimizing piecewise expressions of the form `A x+B+C/x`. The claimed algebraic degree and complexity conclusions remain true.
- Negative leaf bounds and product bounds cause no problem. Only division by the positive common factor is used. A zero or sign-changing common-factor interval is outside the stated theorem.

One presentation correction is needed in the variable-total knapsack discussion: partition at cost-zero crossings as well as pairwise cost-order crossings. A fixed total uses only pairwise order; an interval of permitted totals also needs to know where each marginal cost changes sign.

Follow-up audit: the author has applied this correction and the endpoint-enumeration clarification. Corollaries 1a and 1b also pass review. For integer common factors, derivative-root partitioning makes each candidate objective monotone or constant, and only the first/last permitted integer of each open interval plus integral partition endpoints are needed. For signed common factors, substitution on the negative branch and explicit processing of zero suffice. The positive branch touching zero need not be compact: bounded rational candidate coordinates have finite limits at zero, and these limits belong to the original compact feasible set.

The existing example showing failure without lexicographic perturbation uses a one-row equality directly. If the equality is represented as two linking inequalities, the example still illustrates the underlying bounded-variable LP defect; it should not be read as a claim about every possible slack basis of the expanded two-row system.

## 2. Reciprocal-anchor PSD cut

The moment proof is correct. The stated family of rotated second-order-cone cuts is equivalent to the PSD condition for `m>0`: taking the Schur complement of its last diagonal entry gives a two-dimensional quadratic form tested by all vectors `(1,-s)` and the limiting direction `(0,1)`.

The equality implication `mt=1 => w=my` is correct. It follows either from the PSD kernel condition or from equality in strict Jensen for the reciprocal function on a positive interval.

## 3. Additional results found during the audit

The full proofs have moved to [Reciprocal-anchor hulls and a joint separating inequality](../results/common-factor-reciprocal-anchor-hulls.md). They give an exact two-SOC formulation for one unrestricted box-bounded leaf, a rational two-leaf counterexample to intersecting these exact individual hulls, and an explicit rational separating inequality for that counterexample. The result note records the separate independent-review and novelty status.
