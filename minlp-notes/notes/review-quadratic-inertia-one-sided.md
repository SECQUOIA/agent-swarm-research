# Independent review: one-sided quadratic integer complexity

Date: 2026-09-05. Reviewer: `potential_flow_review`.

Reviewed result: [quadratic-inertia-one-sided-integer-complexity.md](../results/quadratic-inertia-one-sided-integer-complexity.md).

**Verdict: PASS.** The negative-inertia epigraph coefficient and positive-inertia hypograph coefficient follow from the stated lower and upper constructions. The proof covers the complete unbounded epigraph/hypograph and arbitrary convex lifts with unbounded integer coordinates. No substantive correction is needed. This review does not establish publication priority.

## Negative-curvature slice

Because the original box has interior, it contains a nondegenerate box in the negative eigenspace after translating to an interior point. More explicitly, if the minimum coordinate distance of `x_0` from the boundary is `d>0` and `T` has orthonormal columns, any `rho<d/sqrt(k)` works: for `t` in `[-rho,rho]^k`, `||Tt||_infinity<=||Tt||_2=||t||_2<=rho sqrt(k)<d`.

Restricting the original variables by `x=x_0+Tt` and `t` in that smaller box preserves convexity of every lifted set and introduces no integer variables. The restricted quadratic has Hessian `T^T H T<=-m I`, where `m` is the smallest absolute value among the strictly negative eigenvalues. Its affine terms do not affect midpoint gaps. The restricted relaxation contains its entire epigraph because the original relaxation contains all original epigraph points in the slice.

## Parity and the lower constant

For each parity vector, consider all restricted graph inputs with at least one feasible integer lift of that parity. These sets cover the full slice, even when a graph input has several different integer lifts. For any two points in one class, choose one corresponding lift each. Their convex midpoint remains in the lifted convex set, and its integer coordinates remain integers because their parities agree. The projected output is the average of the two exact graph outputs.

Strong concavity gives the one-sided gap

```
g((s+t)/2)-[g(s)+g(t)]/2 >= m||s-t||^2/8.
```

This midpoint lies **below** the graph, so it is exactly the direction controlled by epigraph undererror. The absence of any upper output bound is immaterial. The permitted error forces every parity class to have diameter at most `sqrt(8epsilon/m)`.

Taking closure within the compact slice preserves the pairwise diameter bound. The closures still cover the slice and are measurable compact sets, so no measurability of the original classes is needed. The Euclidean isodiametric inequality gives volume at most

```
omega_k (sqrt(8epsilon/m)/2)^k
= omega_k (2epsilon/m)^(k/2)
```

per class. At most `2^p` classes therefore imply

```
epsilon >= (m/2)[volume(D)/omega_k]^(2/k) 2^(-2p/k).
```

The displayed constant and logarithmic coefficient are correct. The proof depends only on parity, so neither bounded integer ranges nor a finite number of feasible integer assignments is assumed. Closedness of the original lifted set and the number of continuous auxiliaries are likewise irrelevant.

## Signed-square decomposition and one-sided construction

A real spectral decomposition has exactly `k_+` positive and `k_-` negative nonzero square terms. Each nonzero linear form has positive width over a full-dimensional box. Affine normalization to `[0,1]` preserves its sign and transfers only constants and linear terms into the affine part. Thus the normalized representation has the stated numbers of positive and negative coefficients, and its total coefficient magnitude `A` is independent of the original affine objective terms.

For a positive coefficient, the square auxiliary needs only a lower bound of the form `t>=y^2-delta_+`. For a negative coefficient, it needs only an upper bound `t<=y^2+delta_-`. Substitution into

```
w>=affine(x)+sum c_j t_j-sum d_j t_j
```

then gives a lower bound on `w`, with errors adding as positive magnitudes. There is no cancellation assumption. An unbounded positive-square auxiliary can only increase the right-hand side; an unbounded negative-square auxiliary in its permitted downward direction also increases it. Neither can create additional epigraph undererror.

The review independently checked Beach et al.'s [primary Part I paper](https://link.springer.com/article/10.1007/s10589-023-00543-7), Definition 6, equations (14)–(15), and its stated Proposition 2 bound. The zero-binary `Q_L` uses an unrestricted real square-output coordinate and only lower output inequalities. It therefore contains the entire square epigraph, with error `2^(-2L-4)`, and has linear size in depth. Its depth-zero case consists of the tangents at zero, one half, and one, and has error `1/16`, consistent with that formula.

For the negative square terms, the usual binary tent-map graph encoding makes the depth-`L` expression exactly the dyadic square interpolant. That interpolant is above the square with maximum difference `2^(-2L-2)`. Keeping only `t<=interpolant` therefore contains the **entire** square hypograph. No lower bound on this auxiliary is imposed or needed.

At an exact original graph point choose every `t_j=y_j^2`; the required square lifts exist. The final inequality then admits every `w>=f(x)`, not only `w=f(x)`. Increasing `w` alone always preserves feasibility. This directly verifies complete unbounded-epigraph containment.

## Accuracy and dimensions

The upper construction's total undererror is bounded by

```
sum c_j 2^(-2L-4)+sum d_j 2^(-2L-2)
<= A 2^(-2L-2).
```

For `L=max(0,ceil[(1/2)log2(A/(4epsilon))])`, this is at most `epsilon`. If the untruncated expression is nonpositive, `L=0` and `A/4<=epsilon`; if it is positive, the ceiling gives the desired bound directly. Thus the accuracy split and the depth formula also cover coarse accuracies.

Only negative square terms require binaries, yielding exactly `k_- L` binary variables in the proposed formulation. The continuous auxiliaries and inequalities number `O(n+(k_++k_-)(L+1))`, which is the stated logarithmic size for fixed data as accuracy tends to zero. Coefficients may be real, as explicitly allowed; no rational spectral-decomposition claim is being made.

Every binary linear lift is an admissible convex integer lift, so

```
p_epi,conv <= p_epi,bin <= k_- L.
```

Applying the parity lower bound to both classes proves both asymptotic formulas. The additive constants depend on `H` and the box, while the affine part does not influence either error or integer count.

## Convex cases, hypographs, and scope

If `k_-=0`, positive square epigraph approximations provide a finite LP outer approximation of every positive accuracy with zero binaries. The exact epigraph is convex, so zero integer coordinates also suffice exactly when arbitrary convex lifted constraints are allowed. This does not assert an exact finite LP representation of a curved convex epigraph.

The map `(x,w)->(x,-w)` converts a hypograph of `f` and its permitted overerror into an epigraph of `-f` and its permitted undererror. The negative inertia of `-H` is the positive inertia of `H`, proving every hypograph statement with the correct sign and unbounded output direction.

The lower bound concerns uniform representation of a whole epigraph block over a full-dimensional box. Additional constraints restricting the original feasible domain can remove the negative slice, and optimal-value approximation of a single constrained instance need not satisfy this formulation lower bound. The result states this limitation correctly. The signed-square upper construction and parity mechanism are established ingredients; this audit certifies their proposed quantitative combination without certifying novelty.

## Addendum: exact bilinear convex-lift constant

The author's proposed corollary for `f(x,y)=xy` on the unit square also **passes**. With at most `p` arbitrary integer coordinates in a convex lift, the smallest achievable epigraph undererror is exactly `2^(-2p-2)`.

For the lower bound, restrict to `y=1-x`. The restricted function is `g(x)=x-x^2`, and two graph points from one parity class have midpoint gap `(s-t)^2/4`. Thus each closed parity class has diameter at most `2sqrt(epsilon)`. Their interval hulls cover `[0,1]`, so `1<=2^p 2sqrt(epsilon)`, proving the sharp lower bound.

For the upper bound, put `u=(x+y)/2` and `v=(x-y+1)/2`, so both normalized variables lie in `[0,1]` and

```
xy = u^2-v^2+v-1/4.
```

Use the exact convex inequality `t_plus>=u^2`, the depth-`p` binary interpolant hypograph `t_minus<=F_p(v)`, and `w>=t_plus-t_minus+v-1/4`. This convex integer lift contains the complete bilinear epigraph and has undererror at most `F_p(v)-v^2<=2^(-2p-2)`. The upper error is attained in the projected relaxation: choose `u=1/2`, choose `v` at a dyadic cell midpoint, and set both auxiliary inequalities and the final inequality to equality. These `u,v` values correspond to original points with `x+y=1` in the unit square.

The transformation `y'=1-y`, `w'=x-w` converts a bilinear hypograph into a bilinear epigraph with exactly the same error. Hence the same exact constant holds for hypograph overerror.

This proof attains the constant with a convex quadratic constraint; it does not prove exact optimal-error attainment by finite MILP formulations for every `p`. It also does not imply nonattainment: at `p=0`, the ordinary McCormick epigraph already attains error `1/4`.
