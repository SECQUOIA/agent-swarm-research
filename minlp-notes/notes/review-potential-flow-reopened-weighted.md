# Independent review of fixed-factor weighted cactus optimization

Date: 2026-09-06. Reviewer: independent `review_weighted` agent. Scope: the theorem and exact local-constraint extension in [the reopened weighted investigation](potential-flow-reopened-weighted-investigation.md), including mathematical bit complexity and feasible recovery.

**Verdict: pass after three small scope/completeness corrections, which the author applied.** I found no remaining mathematical obstruction to the stated fixed-dimensional affine-nomination theorem or its closed local-constraint extension. This is an internal proof review. It does not establish literature priority or practical runtime of the real-algebraic optimizer.

The corrections were to include bridge zero-flow hyperplanes in the global decomposition, specify `0<epsilon<=1` or reduce larger tolerances to one, and restrict the capacity extension's general local constraints to closed sets when claiming compact feasible sets and attained extrema. The first correction is necessary even for a tree: without bridge sign information its objective need not be a single polynomial on a selected parameter region.

## Cycle formulas and branch domains

A cactus has an edge-disjoint cycle basis. After orienting a cycle consistently and swapping asymmetric coefficients where necessary, its edge flows are `q+ell_e(z)` with rational affine `ell_e`. A sign region in the `d+1` variables `(z,q)` yields a quadratic cycle equation `Aq^2+B(z)q+C(z)=0`. The number of realized sign patterns is polynomial for fixed `d`; enumerating all formal sign vectors would be incorrect.

At a physical root the polynomial derivative is exactly

```
2Aq+B = 2 sum_e beta_e^{sign(x_e)} |x_e| >= 0.
```

Thus the plus-square-root formula is correct for negative as well as positive `A`. When the derivative vanishes, every edge flow is zero. This covers the repeated quadratic root and proves that an `A=0, B=0` physical stratum has no hidden nonzero-flow solution. When `A=0` and the flows are not all zero, `B>0`; the linear-root denominator is therefore strictly positive on its physical domain.

Substitution of the quadratic root into any quadratic weighted drop produces a rational polynomial plus a rational affine coefficient times one square root of a quadratic polynomial. Since `A` is a fixed nonzero rational constant on the local chart, division by `A` or `A^2` has polynomial bit cost. Its magnitude may be large, but its bit length is controlled. This is the specific point that would require a new argument with variable resistance coefficients.

The proposed one-variable elimination keeps `d+1` total variables and bounded starting degree. It gives exact domain formulas with rational coefficients. Cell sign inequalities, the derivative selection condition, and all-zero strata are enough; no informal root selection is being smuggled into the algorithm.

## Polynomial common decomposition

Collect every polynomial appearing in the exact projected local-domain formulas, the bridge zero-flow hyperplanes, and the defining inequalities of the rational parameter polytope. Add the square-root panel-boundary polynomials later. For fixed `d`, a sign-invariant decomposition has polynomial total size. One can equivalently enumerate realized sign conditions; disconnected realizations are harmless because formula membership is determined by the Boolean formula of signs. It is unnecessary to enumerate the Cartesian product of the cycles' local charts.

For each realized parameter stratum and each cycle, at least one physical chart is valid throughout the stratum. Choose one. At a boundary, several charts may apply; their exact drops coincide by physical uniqueness. Panel approximants may differ on a shared endpoint, but either remains within the certified error. The global surrogate can therefore be discontinuous without invalidating any claim.

The needed elimination and sampling bounds are established, rather than assumptions about a value oracle. [Basu's real-algebraic geometry survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf), Theorem 2.18, provides bounds on formula size, degree, and integer coefficient sizes for elimination. With all variable counts fixed, these are polynomial also when polynomial degrees grow with requested precision. Theorem 2.15 supplies sampling of realized sign conditions. These results support both local projection and final threshold decisions; they do not promise a practically fast implementation.

## Approximation and coefficient encodings

The square-root approximation proof is sound. On the specified panel, `u=x/a_j-1` lies in `[-5/9,7/9]`. The absolutely convergent binomial series has coefficients of magnitude at most one, and its tail is bounded by `(9/2)(7/9)^(K+1)`. The all-zero panel gives error at most `2^-J`. Rational square-root centers avoid adjoining any algebraic coefficients.

For precision exponent `p`, both the panel count and degree are `O(p)` after incorporating the polynomial-bit scale bound `S`. Expanded coefficients can have bit length proportional to products such as `jK`; this is quadratic in precision, hence still polynomial. Substitution of a quadratic discriminant doubles polynomial degree. A dense polynomial in fixed `d` variables and polynomial degree has polynomially many monomials. Consequently actual coefficient expansion, not merely an arithmetic-circuit representation, is polynomial.

The affine radical multipliers have explicit polynomial-bit absolute bounds on the rational parameter box. Summing these bounds over all local charts remains polynomial in representation size. The error budget therefore controls cancellation in the full weighted sum without any algebraic separation assumption.

The linear-root charts retain their rational terms exactly. A product of the squared affine denominators has degree at most twice the number of terms. Coefficient bits grow polynomially under this product and under numerator summation. Denominators may tend to zero at a boundary: no polynomial approximation is applied to their reciprocal, and exact threshold decisions retain the nonzero constraints. The exact physical objective is bounded, and its uniformly accurate surrogate is bounded as well, even if a displayed rational formula has individually large intermediate terms.

## Suprema, optimal-value intervals, and witnesses

Individual chart strata can be open. Bisection must concern their suprema, not assume a maximizer exists in each chart. Testing strict threshold feasibility and then sampling at a strictly lower threshold produces a witness arbitrarily close to any finite supremum. This needs no separation from a branch boundary.

Here is one explicit error allocation. Let each surrogate differ from the physical objective by at most `r=epsilon/16`. Let `[L,U]` contain the global surrogate supremum with `U-L<=epsilon/8`. Then `[L-r,U+r]` is a certified interval for the true maximum, of width at most `epsilon/4`. Sample a point in a stratum with surrogate value greater than `L-epsilon/16`. Its true objective is within `5epsilon/16` of the true maximum. A further rational rounding loss at most `epsilon/4` leaves total loss below `epsilon`. Using a threshold strictly below `L` avoids the possibility that an unattained supremum equals the requested sampling threshold.

The objective has a polynomial-bit bound because every physical edge flow is bounded by total positive nomination. Nomination bounds follow by rational linear programming over the compact parameter polytope. Thus the number of bisection steps is polynomial in the input bit length and `log(1/epsilon)`. Fixed-dimensional sampling returns an algebraic parameter representation of polynomial degree and coefficient size. Coordinate isolation to any polynomially specified number of bits is therefore also polynomial.

## Global Lipschitz estimate and exact rational recovery

The difference-flow argument is particularly useful and correct for general connected passive networks. For two physical states, strict monotonicity makes every nonzero difference flow point downhill in the difference potential. That directed support is acyclic. Its path decomposition has total mass `||b-b'||_1/2`; hence every difference edge flow has absolute value at most that number. This is independent of flow signs and does not require strictly positive derivative at zero.

On a common flow bound `B`, an asymmetric quadratic law is Lipschitz with constant `2 beta_max B`, including across zero. Summing drop changes along a spanning-tree path gives the stated objective Lipschitz constant. Multiplication by the entrywise absolute sum of `H` gives a valid parameter-space constant.

The algebraic witness belongs to the original rational polytope. A rational coordinate-isolation box containing it has nonempty intersection with that polytope. Rational linear programming therefore returns a rational feasible parameter of polynomial bit length, including in a lower-dimensional polytope. Its distance to the algebraic witness is at most the box width in each coordinate. No rational point in the selected semialgebraic chart is required: the global physical Lipschitz bound controls the objective after crossing a chart boundary. This also resolves the singular-denominator recovery issue.

## Exact local operating constraints

The additional extension is sound for a polynomial-size list of bounded-degree rational closed semialgebraic constraints, each involving the parameters and flow variables of only one cycle or bridge. Substitute the affine local flow representation before elimination; the total variable dimension stays fixed even when a cycle is long. Intersecting the resulting projected domains determines exact global feasibility in fixed parameter dimension. The feasible subset of the compact parameter polytope is compact by continuity of the physical flow and closedness of the constraints. The same objective approximation gives an algebraic feasible near-optimizer.

The four-cycle counterexample correctly excludes a general rational feasible-output claim. In the author's example, capacities on `q` and `q-2` force `q=1`. The remaining loop equation on `t in[1,2]` is exactly `t^2-2=0`, and the other capacities hold. Computing successive flow differences yields precisely the stated balanced nomination vector `(t+1,-t-1,2,-2)`. Thus the only feasible parameter is irrational although every input coefficient and positive capacity is rational.

The added capacity-slack recovery statement also passes review. A parameter perturbation of sup-norm at most `delta` changes every physical edge flow by at most `(sum_ij |H_ij|) delta/2`. Starting from the nonempty problem with capacities tightened by a supplied rational `sigma>0`, the prescribed rational LP rounding therefore preserves the original capacities. Its objective guarantee is relative to the tightened optimum only; no unjustified continuity of the optimum as capacity slack disappears is asserted. The rounding construction uses only `P`, so this statement applies to capacity constraints, not to preserving arbitrary additional local semialgebraic constraints.

These local constraints do not include arbitrary potential bounds coupling drops from arbitrarily many cycles. Their exact treatment could reintroduce radical-sum comparison. The theorem does not claim otherwise.

## Independent reproducible checks

I wrote [an independent review script](../code/potential_flow_mpd/check_reopened_weighted_review.py) without using the author's checker. Running `python code/potential_flow_mpd/check_reopened_weighted_review.py` passed:

- 55 exact rational checks of square-root panel error, including panel endpoints and 40-bit accuracy;
- five exact linear-root cases with denominators tending to zero, down to scale `2^-1000`;
- 240 cycle computations at 100 decimal digits, including 119 negative-`A`, 113 positive-`A`, and eight zero-`A` cases;
- 240 independent checks of the difference-flow bound.

The exact vanishing-denominator family is `x=(q+t,q+2t,q-t,q-3t)`, with unit coefficients, `t>0`, and `q=5t/14`. Its loop polynomial has `A=0`, `B=14t`, and `C=-5t^2`. At `t=0` the separate all-zero stratum applies. This specifically exercises the branch case where a uniform denominator lower bound would fail.

The script checks distinct vulnerable mechanisms; it is not a global optimizer and cannot substitute for the proof of the real-algebraic complexity claim.
