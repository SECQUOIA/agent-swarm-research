# Independent review of the all-scale core value oracle

Date: 2026-10-02. Verdict: **passed after an explicit formula-encoding
repair**. I read the actual [all-scale draft](../new-direction/all-scale-core-value-oracle.md),
the complete [two-dimensional predecessor](../new-direction/core-only-noise-value-oracle.md),
and the [finite-section interface](../new-direction/polynomial-finite-noise-tails.md).
The repair is now present in section 5 of the draft. No substantive
mathematical gap remains in this review. This is a correctness assessment,
not a prior-art or publication-priority claim.

## 1. The geometric proxy bounds actual generated work

The near-optimal set uses tolerance `k L h^2/2`, exactly the inherited
`4e_h` retained-corner tolerance. Compactness supplies residual optima
and makes this set compact. The padding gives a full-dimensional convex
body even for isolated or lower-dimensional optimal sets.

Both directions of the simplex-volume comparison are correct. A
maximizing simplex gives `D/k!<=volume`. Replacing each of its vertices
by an arbitrary point of the body bounds the absolute value of every
barycentric coordinate by one. The edge-coordinate parallelepiped
therefore contains the body and has volume `2^k D`.

Distinct grid nodes have disjoint interiors of their centered side-`h/2`
cubes, and all these cubes belong to the padded body. This proves the
node count without requiring padding to remain in the original feasible
box. Multiplying by corner incidence and the number of children gives
`16^k W` for generated cells. It is a bound on the actual candidate
lists before pruning, not merely on the eventual survivors. Approximate
recourse answers cannot defeat it because the predecessor proves the
true near-optimal witness property for every allowed oracle answer.

## 2. The measure and its local mass bound are well defined

The conjugate of the continuous box objective is finite and convex,
with subgradients in the unit box. Adding `||c||^2/(2L)` makes `H`
strongly convex and supercoercive. Thus `H*` is finite and continuously
differentiable, and its gradient is `L`-Lipschitz. The inverse relation
between its gradient and the subgradient of `H` holds on all of Euclidean
space, including nonsmooth points of `H`.

The measure is the pushforward of Lebesgue measure by that continuous
gradient. Preimages of Borel sets are measurable; countable additivity
does not depend on the gradient being injective. For a bounded coefficient
set its preimage is contained in the unit box plus that coefficient set
divided by `L`. This proves local finiteness. In particular it gives
the stated mass bound on the expanded noise cube. No assumption of
an almost-everywhere Hessian density is hidden in this definition.

At a near-optimal core point, the Fenchel residual is at most
`epsilon_h`. Strong convexity bounds the distance of its conjugate
gradient from the coefficient point by `sqrt(2L epsilon_h)`. The smooth
upper bound for the residual after padding has coefficient
`1/2+1/4+1/32=25/32` times `k L h^2`. Convexity of this residual extends
the bound to the padded convex hull. Every point of its translated body
therefore maps into the open ball of radius `4kLh`, strictly larger than
the required `sqrt(2k)Lh`. Translation preserves volume. This proves
the measure domination with the correct inclusion direction.

## 3. One covering argument controls all scales

For every coefficient with `A>T`, one positive scale witnesses the
strict inequality. The selected balls have uniformly bounded radii and
centers in the compact noise cube. The standard `5r` selection gives
countably many disjoint original balls whose enlargements cover all
centers. Every original ball lies in the expanded cube. Summing their
measure uses disjointness; only the enlarged balls are used for the
Lebesgue covering estimate. Open balls avoid any boundary-atom overlap
issue in the measure sum.

The resulting numerator is
`5^k v_k k! (4kL)^k (1+2sigma/L+8k)^k`. Division by the noise-cube
volume and `v_k<=2^k`, `k!<=k^k` are consistent with the deliberately
coarse constant `(180k^3)^k(1+L/sigma)^k`. The tail exponent is `1/T`
in every dimension. There is no union over dyadic levels or future
accuracy queries: the supremum was included before applying the covering
argument. The proof also covers an infinite value of the proxy.

## 4. The repaired finite-law formula has the claimed size

The first version displayed a determinant atom and described its
explicit polynomial encoding as polynomial size. Expanding a symbolic
`k`-by-`k` determinant has factorially many terms, so that assertion
needed repair for the stated polynomial-size formula argument. This
does not by itself refute the final section bound: `log(k!)` is polynomial
in the input, and the fixed-block bound can also accommodate suitable
exponential-size descriptions. The QR replacement gives the cleaner
polynomial-size description actually claimed.

The saved replacement is correct. It existentially introduces a square
orthogonal matrix and an upper-triangular matrix with positive diagonal
whose product is the simplex edge matrix. Orthogonality implies absolute
determinant one. The triangular diagonal product is therefore exactly
the absolute edge determinant. Conversely every nonsingular real edge
matrix has such a QR factorization; the strict positive threshold
ensures nonsingularity. Product-chain variables encode this product and
`h^k`. All equations have degree at most two and polynomially many
written monomials. Real witnesses suffice because this is an analysis
formula, not a rational online factorization algorithm.

Caratheodory representations use at most `k+1` points per simplex
vertex. Each point has a feasible residual witness, and its near-optimality
is expressed against one shared universally quantified global competitor.
Minimizing that competitor recovers exactly the intended near-optimal
set. Zero combination weights cause no problem because that set is
nonempty. The strict supremum event requires existence of some positive
scale, not attainment at zero.

Consequently there are just two quantified blocks, polynomially many
variables and atoms, and degree at most `max(d,2)`. The fixed-block
section theorem supplies a single exponential-in-polynomial component
bound uniformly over arbitrary fixed real thresholds and other noise
coordinates. This uniformity justifies replacing marginals one at a
time under mixed discrete and continuous conditioning. Singleton atoms
are counted. The finite-law error is additive `C_0/M`, independent of
the scale and query precision.

## 5. The cap pays for exceptional draws without changing their objective

The generated-count cap is checked before creating an oversized child
list. Its occurrence at any level implies `W>B`. At every completed
level the count is bounded both by the cap and by the geometric proxy,
giving the required truncated random work factor. Corner multiplicity
and the `2^k` calls per cell belong in the parameter factor; they are
not treated as dimension-independent constants.

Integration of the weak tail gives `1+a_k log B+beta B`, while
`B P(W>B)<=a_k+beta B` pays for the fallback's base exponential factor.
Choosing `M>=C_0 B` before sampling controls both expressions. The
fallback's sampled-height exponent remains fixed, and the repaired
section bound gives polynomial sampled bit length. Level coordinates
have only linear-in-level bit length. Thus the same random factor
bounds work at every requested accuracy, with a fixed polynomial in
`I+q`. No requirement that `M h` stay large reappears at fine scales.

The ordinary output remains a feasible rational point with certified
objective gap and an exact optimal-value Cauchy name. It does not give
a coordinate Cauchy name for a selected optimizer. Ties and degenerate
residuals are allowed. The rare branch uses the same sampled objective
and the independently established exact fallback. Zero curvature is
handled by endpoint recourse as stated. These distinctions are essential
to the scope of the theorem.

## Verification record

This review independently rederived the inclusions, constants, formula
size and cost accounting. I reread the saved QR repair before approving
it. I did not duplicate the author's planned geometric diagnostics or
the predecessor's grid/cap tests. A targeted local check of this review's
links, whitespace and control characters passed. No project-wide check,
CI inspection, index edit or new literature ingestion was performed.
