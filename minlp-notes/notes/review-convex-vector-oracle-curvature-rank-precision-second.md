# Independent second audit: oracle-body curvature-rank precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.

**Status: PASS.** I independently checked the complete geometric and formulation argument in [the candidate](convex-vector-oracle-curvature-rank-precision.md). The finite bound `p_bin <= p_conv+ceil(log2(8r^2-1))` and the polynomial rational bound `p_out <= p_conv+17+2ceil(log2 r)` follow in the stated scope. The separately audited oracle primitive now has [two full passing reviews](review-rational-polar-spanner-oracle-second.md); its exact-feasibility and uniform bit guarantees match the main theorem's needs. This is a correctness audit, not a novelty certification.

## Nonlinear image and effective body

The space `S` is the span of deviations from the endpoint chord. For polynomials it equals the span of the coefficient columns of degrees at least two: the scalar functions `x^k-x`, for `k>=2`, are linearly independent. A full-column-rank rational basis `V` therefore gives an exact decomposition `F=a+bx+Vq`, where `q(0)=q(1)=0` and the values of `q` span `R^r`. Hence its coordinate functions are independent modulo affine functions. Computing the rational left inverse and dense coordinate coefficients has polynomial bit complexity.

The effective body `C={z:Vz in K}` is compact, centrally symmetric, and full dimensional in `R^r`. The claimed radii are valid: the coefficient-sum bound controls the operator norm of `V`; conversely `z=L(Vz)` and `||Vz||_2<=mR` give the displayed outer radius. Pulling a strong separator back by `V^T` is valid. A violated pulled-back normal cannot vanish because the origin belongs to `C`. No assertion that `C` is unconditional is needed or made.

## Positive scalarizations

The positive part of the polar is compact and has interior; its linear image under `V^T` spans `R^r`. Small positive coordinate-axis vectors give explicit spanning image seeds. Choosing a projected basis with feasible nonnegative preimages is sufficient, even though its image need not contain a ball about zero.

Each selected scalarization is convex. A representation in the projected basis leaves only an affine difference between scalar functions, so it exactly reconstructs chord gaps. Nonnegative selected gaps make signed reconstruction coefficients harmless: a coefficient bound `c` gives `0<=g_H<=c g_Psi`. The selected sum cannot be affine when `r>0`, since that would force all selected convex functions to be affine and contradict projected independence.

For a nonnegative error vector, the gauge of an unconditional body is the supremum over its positive polar. Taking absolute values of a polar normal preserves feasibility and does not decrease its pairing with a nonnegative vector. The vector chord gap is componentwise nonnegative by componentwise convexity. Thus the scalar domination controls its full `K` gauge. This is the precise use of unconditionality; no finite facet representation is silently assumed.

## Inner band and finite comparison

If the feasible columns of `B` form a `d`-spanner of `C`, central symmetry gives `B B_1^r subset C`, while the coefficient bound gives `C subset B[-d,d]^r`. Therefore `P=(1/r)VB[-1,1]^r` satisfies `P subset K intersect S subset drP`. The proposed band is the explicit continuous equation `w-y=VBu/(2r)`, `-1<=u_i<=1`. It is a polyhedron in the lifted variables and needs no body oracle or new integer variable.

Maximum absolute determinants in the compact spanning sets exist and are nonzero. Replacing a basis vector by any feasible point proves the coefficient bound one by Cramer's rule. Thus the finite choice has `c=d=1`.

For each parity class of exact graph contacts in an arbitrary admissible convex lift, take its interval hull. Approximating its two endpoints by contacts of the same parity gives feasible lifted midpoints; continuity and closedness of `K` then put the limiting Jensen vector in `K`. Each feasible selected polar normal has midpoint gap at most one. Their sum has midpoint gap at most `r`, hence full chord gap at most `2r` by concavity of the scalar chord gap. This argument does not assume bounded integer witnesses or closedness of the original lift projection.

The direct level refinement lemma, with ratio `(2r)/(1/(2r))=4r^2`, uses at most `8r^2-1` subintervals. The refined vector chord gap is in `(1/(2r))K intersect S`, hence in `P/2`. The exact vector chord center with its symmetric `P/2` band therefore contains the graph and stays inside its `K` tube. Parity hulls cover the input; singleton hulls cause no difficulty. A finite binary disjunction gives the stated bound. Errors of the comparator lift outside `S` do not affect this argument, since its exact-contact Jensen vectors lie in `S` automatically.

## Oracle interface and rational construction

I read the oracle lemma and checked its interface against this application; its internal weak-optimization proof has separate independent audits. The main theorem supplies all required data: a full-rank rational image, explicit rational inner and outer radii, exact feasible spanning seeds, and strong separation of the original body. Its coordinate outer bound is converted to the Euclidean bound `mR`. The lemma returns exactly feasible positive polar weights and exactly feasible primal basis columns with coefficient bound `9/4<3`, with one uniform polynomial bit bound. Positive-polar access uses weak separation derived from certified support optimization and exact repair; it does not require exact polar membership. The dimension-one case is covered by the lemma's explicit padding argument.

Using the conservative constants `c=d=3`, let `tau=1/(36r)`. The parity comparison remains a full scalar gap of at most `2r`, because each selected polar weight is exactly feasible. Level refinement gives `N_tau <= (144r^2-1)2^p`. Converting an interval cover into a partition does not increase this count: repeatedly take a covering interval that extends farthest to the right and restrict to the uncovered suffix; convex chord error decreases under restriction.

The reviewed dense scalar compiler supplies actual cell count at most `486N_tau` and exact scalar chord gap at most `13tau/16`. Gap domination gives vector gap in `(13/(192r))K intersect S`; the inner-band comparison then puts it in `(13/64)P`. Both multiplications and the rank factors are correct.

Round the coordinate vector `q`, not the original output vector, with coordinate error at most `delta=1/(16rL_B)`, where `L_B=1+sum|B^{-1}_{ij}|`. Applying `B^{-1}` bounds the infinity norm of each endpoint rounding error by `1/(16r)`, so the error belongs to `P_0/16`. Common interpolation preserves this set. Restoring `a+bx` exactly therefore yields center error in `(17/64)P`. The `P/2` band contains the graph, since `17/64<1/2`, and every admitted error belongs to `(49/64)P subset K`.

This coordinate rounding is essential: it keeps the error exactly in `S` even when that space is a proper subspace of the output space. Every output uses the same scalar input and interpolation weight. The coordinate polynomials need not themselves be convex, since they are used only for exact evaluation and controlled rounding; the scalar knot compiler is applied to the convex function `Psi`.

The scalar compiler's common input denominator and signed output offsets extend to all coordinate evaluations with polynomial encoding. Polynomial-bit rational bases have polynomial-bit inverses; hence the required rounding accuracy has polynomial encoding as well. Gate wires are continuous but forced Boolean by the global index bits, and binary-times-interpolation products have exact linear descriptions. The affine output restoration and band equation add only continuous variables and rational rows. No nonpolyhedral constraint survives in the final MILP.

Finally, `486(144r^2-1)<69984r^2<2^17 r^2`. Taking the ceiling of the logarithm proves the stated integer count. The algorithm computes neither the comparator lift nor its optimum integer dimension.

## Verification and scope

I reran [the exact rational band checker](../code/quadratic_rank/check_oracle_curvature_rank_bands.py):

```
PASS: 289 inner-parallelotope checks; 576 exact vector-chord comparisons; 9216 inner-band errors
```

It checks a rank-two nonlinear image in three outputs and includes signed coordinate rounding and band corners. Its scope is the geometric transfer, not an implementation of the body oracle or the GLS theorem. The proof above checks the general constants independently.

The result concerns one input, componentwise convex outputs, compact unconditional error bodies with interior, and dense rational polynomial data for the algorithmic statement. Polynomial time is relative to the stated rational strong-oracle model and radius encodings. It does not imply the same bound for tilted non-unconditional bodies, multiple coupled input variables, or sparse enormous degrees. No unresolved issue remains within these assumptions.
