# Coupled convex polynomial outputs: precision controlled by curvature rank

Date: 2026-09-05. Status: independently reviewed result; two full audits passed. Author: `noncommutative_rank_review`. The scalar compiler is an independently reviewed dependency; the vector transfer below is new within this investigation. Literature priority remains qualified by a bounded source check.

## 1. Statements

Let `F=(F_1,...,F_m)` be continuous and componentwise convex on `[0,1]`, with positive component tolerances `epsilon_j`. Normalize `G_j=F_j/epsilon_j`. Let

```
r = dim span{G_1,...,G_m} modulo affine functions of x.
```

For polynomials this is the rank of the matrix of normalized coefficients of powers `x^2,x^3,...`, equivalently the dimension spanned by the component curvatures. Affine terms play no role in the rank. Write `p_conv` for the minimum integer dimension among arbitrary convex lifts containing the exact vector graph and admitting only component errors at most `epsilon_j`. Continuous size and general integer ranges are unrestricted. Let `p_bin` restrict integers to binary variables.

If `r=0`, the exact graph is affine and needs no integers. For `r>=1`, the finite real-coefficient statement is

```
p_bin <= p_conv + ceil(log2(4r-1)).                         (1)
```

The binary upper formulation can be linear. Thus the overhead depends on curvature rank rather than output count or degree.

For densely encoded rational polynomials convex on `[0,1]` and positive rational tolerances, there is a deterministic polynomial-time rational MILP construction with

```
p_out <= p_conv + ceil(log2 r) + 12.                        (2)
```

Its encoding length and construction time are polynomial in all polynomial coefficients and tolerance encodings, without fixing `r,m`, or degree. All outputs share one scalar grid index. This is a one-input vector theorem; it does not assert the same conclusion for arbitrary multivariate coupled outputs.

## 2. Scalar refinement at an arbitrary integer factor

Suppose a continuous convex scalar function has full-interval chord gap `g` satisfying `0<=g<=H*tau`, where `H>=1` is an integer. There is a partition into at most `2H-1` intervals with local chord error at most `tau`.

Indeed `g` is concave, nonnegative, and zero at the two endpoints. For every level `j*tau`, `j=1,...,H-1`, strictly below its maximum, take the two endpoints of the superlevel interval. Ignore levels above or equal to the maximum. These at most `2H-2` cuts form the partition. On either monotone side, each resulting interval has gap range of width at most `tau`. Its local chord gap is `g` minus the affine interpolant of its endpoint values, so it is at most that range width. The middle interval has equal endpoint gap `j*tau` at the highest retained level; its maximum gap is at most `(j+1)*tau`. Its local gap is therefore at most `tau`. If no level is retained, the original maximum is at most `tau`. Flat maximum intervals cause no difficulty.

This proves the factor `2H-1` directly, rather than by iterating the three-piece halving bound. The argument also covers a singleton interval with zero chord error.

## 3. A basis of original outputs controls every chord gap

Choose any coordinates for the `r`-dimensional quotient space and write the normalized outputs as row vectors there. Choose `r` rows maximizing the absolute determinant. Call the corresponding original normalized outputs `G_(i_1),...,G_(i_r)`.

Every normalized output has a representation

```
G_j(x) = alpha_j + beta_j*x + sum_(s=1)^r c_js G_(i_s)(x),
|c_js|<=1.                                                (3)
```

The coefficient bound follows from Cramer's rule: replacing one basis row by another row multiplies the determinant by that representation coefficient, so its magnitude cannot exceed one.

For any input interval, write `g_j` for its normalized component chord gap. All `g_j` are nonnegative by convexity, and affine terms cancel in (3). Define the convex scalar function

```
Psi=sum_(s=1)^r G_(i_s).
```

Then at every point of every interval,

```
0<=g_j=sum_s c_js g_(i_s)<=sum_s g_(i_s)=g_Psi.             (4)
```

Signed representation coefficients cause no problem because the basis consists of original convex outputs with nonnegative gaps. An arbitrary algebraic basis of the quotient need not have this property.

## 4. Compare with every convex integer lift

Take any admissible convex lift with `p` general integer variables. For each exact graph point choose one lifted witness. Group its input by the parity of the integer vector. There are at most `2^p` groups. Take the closure and interval hull of every nonempty group.

For endpoints `a,b` of one such hull, approximate them by inputs from that parity group. The midpoint of the corresponding lifted witnesses has an integer vector and belongs to the convex lifted set. Passing to limits only in the projected error inequalities, using continuity of `F`, gives

```
0 <= [G_j(a)+G_j(b)]/2-G_j((a+b)/2) <= 1.
```

No closedness or measurability of the lift, nor boundedness of its integer coordinates, is used. Hence the midpoint gap of `Psi` is at most `r`. Every nonnegative concave gap vanishing at the endpoints has maximum at most twice its midpoint value, so its full-interval maximum is at most `2r`.

Apply section 2 with `H=2r,tau=1`. Each parity hull splits into at most `4r-1` intervals whose `Psi` chord error is at most one. Equation (4) gives the same bound for every normalized component. On one interval, with normalized component chords `T_j`, the polyhedral band

```
T_j(x)-1 <= w_j <= T_j(x),   j=1,...,m,
```

contains the exact normalized graph and admits only normalized errors in `[-1,1]^m`. Rescale each output by `epsilon_j`.

The parity hulls cover the input domain. Their refined intervals produce at most `(4r-1)2^p` bands. A finite binary disjunction gives (1). This part permits real knot and row coefficients and makes no algorithmic claim about finding the original lift.

We will also use the chord-count consequence. Any finite cover by intervals of scalar chord error at most `tau` can be replaced by a partition with no more intervals: repeatedly choose a covering interval extending farthest to the right from the current covered endpoint and restrict it to the new partition piece. Restriction preserves a convex function's chord-error bound. Thus such a cover bounds the minimum scalar partition count `N_tau` as well.

## 5. A polynomial rational approximate barycentric spanner

For polynomial inputs, form the rational matrix `A` of normalized coefficients of degrees at least two, padding degrees with zeros. Its size is polynomial in the dense input. Select `r` independent columns by rational elimination and call the resulting `m by r` full-rank matrix `V`.

Start with any nonsingular `r by r` row submatrix `V_I`. Compute all representation coefficients `V_j V_I^{-1}`. If an entry has magnitude greater than two, replace its corresponding basis row by row `j`. Repeat until none does. Each replacement increases the absolute determinant by a factor greater than two. At termination,

```
G_j = affine_j + sum_s c_js G_(i_s),   |c_js|<=2.            (5)
```

This algorithm has polynomial bit complexity even when `r` varies. To see termination quantitatively, let `L` bound the full binary encoding length of `V`. Every entry has magnitude at most `2^L`. Let `q` be the product of all its positive denominators, so `q<=2^L`. A nonzero row-minor determinant has magnitude at least `q^(-r)>=2^(-rL)`, while every row-minor determinant has magnitude at most `r! 2^(rL)`. There are therefore at most `2rL+log2(r!)+1` determinant-doubling steps. Each basis is a submatrix of the original rational matrix, and all its determinants, inverses, and representation coefficients have polynomial bit length. Rational elimination and all comparisons are consequently polynomial time. Fixed independent columns suffice because they span the column space, so agreement on those columns implies the same relation for the full coefficient rows.

No maximum-determinant optimization oracle is needed for the constructive theorem. The exact maximum-volume basis is used only for the sharper finite constant in (1).

With the polynomial basis, define `Psi` as the sum of its selected normalized original outputs. It is convex and nonaffine when `r>=1`. The gap inequality becomes

```
0<=g_j<=2g_Psi.                                           (6)
```

For every original parity hull, the same midpoint argument gives `g_Psi<=2r` on that hull. Refining with `H=4r,tau=1/2` and using the cover-to-partition observation yields

```
N_(1/2)(Psi) <= (8r-1)2^p.                                (7)
```

## 6. Compile one scalar grid for the whole vector

Apply [the reviewed dense convex scalar compiler](convex-polynomial-compiled-integer-precision.md) to `Psi` at tolerance `tau=1/2`. Its proof gives a random-access rational polygonal path with actual cell count

```
K<=486N_(1/2)(Psi),
```

and exact scalar chord error at most `13tau/16=13/32` on every cell. By (6), every normalized output has exact chord error at most `13/16` on those same cells. Consecutive compiled knots need not be monotone; the chord inequality holds on their unoriented interval, and the scalar path covers the full domain.

Use the scalar compiler's one global binary index and rational knot circuit. At each of the two selected knots, evaluate all original normalized output polynomials and round downward with error at most `1/8`. These evaluations are polynomial-time rational computations with polynomial bit length. With `y_j` the interpolation of the rounded endpoint values, impose

```
y_j-13/16 <= w_j <= y_j+1/8.                              (8)
```

If `T_j` is the exact chord, then `0<=T_j-y_j<=1/8` and `0<=T_j-G_j<=13/16`. Thus (8) contains the exact component graph, and every admitted point differs from it by at most `15/16<1`. All components use the same interpolation weight and input segment, so this proves vector graph containment and componentwise accuracy simultaneously. Finally output `epsilon_j w_j`.

The reviewed circuit-to-MILP compiler uses only the input index bits as declared integer variables. Internal gate wires are continuous and forced to Boolean values by their exact gate constraints once the index bits are fixed. Products with the continuous interpolation weight use exact binary-product hulls. Evaluating more output polynomials adds continuous wires and rows, not integer variables. Invalid index codes are excluded by the same binary comparison used in the scalar compiler.

By (7),

```
K <= 486(8r-1)2^p < 3888r 2^p < 4096r 2^p.
```

Therefore `ceil(log2 K)<=p+ceil(log2 r)+12`. Apply this to a lift attaining the minimum integer dimension to obtain (2). The algorithm never needs that lift, its integer dimension, or an optimal chord partition. All quantities it computes come from the input polynomials, tolerances, basis exchanges, and the reviewed scalar compiler.

## 7. Scope and significance

This result handles genuinely shared one-input vector outputs, not independent input coordinates. It resolves the output-count dependence when many outputs lie in a low-dimensional curvature space, even if their affine parts, tolerances, signs of polynomial coefficients, and degrees differ. Rank one recovers a uniform constant-overhead guarantee for arbitrarily many outputs.

The [positive-power refinement obstruction](../notes/positive-polynomial-vector-refinement-obstruction.md) has curvature rank equal to its number of distinct powers. It therefore remains compatible with both bounds. Its failure of every fixed normalized scalarization does not contradict the present proof: the selected sum has total error budget `r` under the original lift, and the explicit scalar refinement factor is charged as `O(log r)` extra bits.

Neither theorem proves that an unbounded binary-versus-general-integer gap occurs at growing rank, nor that the logarithmic rank overhead is necessary. The general multivariate coupled-convex case also remains open here. No minimum-rank nonlinear decomposition is assumed: the rank in this statement is computed by ordinary rational linear algebra on the given normalized polynomial coefficients.

Maximum-volume bases, determinant-exchange methods, scalar chord refinement, parity obstructions, and Boolean circuit compilation are established ingredients. In particular, the bases in sections 3 and 5 are barycentric spanners and 2-approximate barycentric spanners. Awerbuch and Kleinberg's *Adaptive Routing with End-to-End Feedback: Distributed Learning and Geometric Approaches*, section 2.3, Proposition 2.2, Observation 2.3, and Proposition 2.4, gives the maximum-determinant coefficient argument and determinant-exchange construction. These passages were checked directly in the [primary author manuscript](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf). Neither basis selection nor its exchange mechanism is new here.

The proposed contribution is the uniform curvature-rank comparison with every convex integer lift and its polynomial-size rational construction. The [bounded source assessment](../notes/convex-vector-curvature-rank-novelty.md) did not locate that complete conclusion; it does not prove exhaustive priority.

Both full audits passed without required corrections: [first audit](../notes/review-convex-vector-curvature-rank-precision.md) and [second audit](../notes/review-convex-vector-curvature-rank-precision-second.md). The first reviewer independently checked 24 rational convex-output basis systems, 936 exact chord identities and domination inequalities, and 120 concave level refinements. Its report records the test scope.
