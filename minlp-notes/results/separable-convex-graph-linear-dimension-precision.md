# Linear-dimension precision for separable convex sums and independent outputs

Date: 2026-09-05. Status: independently reviewed result; two full proof audits passed.

Shape-adapted scalar grids yield a polynomial rational construction within an
additive linear number of integers of every convex lift for two multivariate
positive-polynomial families. There is no degree-dependent additive term.
The scalar-sum case uses Jensen-gap superadditivity and a product packing
argument; it does not compare to the coefficient-sum allocation that has a
log-log degree gap.

## Statement

Let each coordinate polynomial be

```
phi_i(x)=sum_(k=2)^(D_i) c_ik x^k,       c_ik>=0,
i=1,...,r,
```

with rational dense input and at least one positive coefficient per coordinate.
All affine coefficients and tolerances are rational. Assume `r>=1`; when no
nonlinear coordinate is active, the exact graph is linear and needs no integers.
The domain is the original product box `[0,1]^r`. Extra affine-only coordinates
may be retained continuously. Consider either of the following graph models.

* Scalar sum: `f(x)=l^T x+b+sum_i phi_i(x_i)`, with positive rational absolute
  tolerance `epsilon` on its scalar output.
* Independent outputs: `f_i(x)=l_i^T x+b_i+phi_i(x_i)`, with positive rational
  componentwise tolerances `epsilon_i`.

A deterministic polynomial-time algorithm constructs a rational MILP of
polynomial size satisfying, respectively,

```
p_out<=p_conv+12r                 (scalar sum),
p_out<=p_conv+9r                  (independent outputs).             (1)
```

Here `p_conv` is the minimum number of general integer variables among all
convex lifts containing the exact graph and admitting only the stated errors.
The lower comparison does not restrict continuous lift size. The construction
is polynomial in dense polynomial input and tolerance encoding; sparse huge
degrees are not included in this theorem.

The two graph structures are explicit. This result does not claim the same
bound for arbitrary positive linear combinations in many outputs under a
general coupled error body. Arbitrary affine output terms are harmless because
they can be subtracted and restored by exact linear maps.

## 1. Scalar packing controls the shape-adapted grid count

For one continuous convex function `phi`, define its midpoint Jensen gap

```
J_phi(a,b)=[phi(a)+phi(b)]/2-phi((a+b)/2).
```

Fix a tolerance `tau>0`. Choose any finite maximal set of points
`x_1<...<x_P` such that every distinct pair has `J_phi(x_j,x_k)>tau`.
Such a finite maximal set exists. Uniform continuity makes sufficiently close
pairs compatible, which gives a finite packing bound; points can therefore
be added until no further addition is possible. This packing is used only
for the proof, not computed by the construction.

For a selected point `x_j`, the set of points compatible with it is a closed
interval `[a_j,b_j]` containing `x_j`. This uses monotonicity of midpoint gap
under interval enlargement. For a differentiable convex function it follows
from

```
partial_a J=(phi'(a)-phi'((a+b)/2))/2<=0,
partial_b J=(phi'(b)-phi'((a+b)/2))/2>=0,
```

and the continuous convex case follows by monotone secant slopes or smoothing.
Only smooth positive polynomials are needed for (1).

Maximality says these compatibility intervals cover `[0,1]`. Split each at
its selected point. The two intervals `[a_j,x_j]` and `[x_j,b_j]` have endpoint
midpoint gap at most `tau`, so their whole chord error is at most `2tau`.
A finite interval cover can be trimmed to a partition with at most the same
number of intervals. Consequently, if `N_(2tau)` is the optimal chord count,

```
N_(2tau)<=2P.                                                        (2)
```

Let `M_tau` denote the reviewed accuracy-dependent curvature mass for a
positive polynomial. Its finite theorem and scaling give

```
M_tau<=2M_(2tau)<=48N_(2tau)<=96P.                                   (3)
```

The reviewed [compiled curvature construction](../results/compiled-curvature-quantile-precision.md)
uses a rational upper estimate `U` with `M_tau<=U<=M_tau+1/256`, and
`L=max(0,ceil(log2((5/2)U)))` binaries. If `L>0`,

```
2^L<=5U<=480P+5/256<=481P.
```

If `L=0`, the same last bound is immediate from `P>=1`. Thus every coordinate's
actual computed binary count satisfies

```
2^(L_i)<=481P_i.                                                     (4)
```

The construction at tolerance `tau` has actual absolute error at most
`15tau/16`, contains the whole exact scalar graph, and has polynomial rational
size and construction time for dense positive-polynomial input.

## 2. Independent outputs: product parity packing

For the independent-output model, apply (2)--(4) at tolerance `tau_i=epsilon_i`.
Take the Cartesian product of the selected point sets. It has `product_i P_i`
points. Two distinct product points differ in some coordinate `i`, whose
midpoint gap exceeds `epsilon_i`. Their exact graph midpoint therefore violates
that output's tolerance. The restored affine output terms cancel in this gap.

All these product graph points are pairwise parity-incompatible in every convex
integer lift. Hence

```
2^(p_conv)>=product_i P_i.
```

Compose the independent scalar compiled formulations and restore their affine
outputs. The graph containment and error guarantees hold componentwise. By (4),

```
p_out=sum_i L_i
 <=sum_i log2 P_i+r log2(481)
 <=p_conv+9r,
```

because `481<512`. This proves the second line of (1).

## 3. Midpoint Jensen gaps are superadditive along an interval

For a twice continuously differentiable convex function,

```
J_phi(a,b)=(1/2)integral_a^b min(t-a,b-t) phi''(t)dt.
```

Given `a=x_0<...<x_h=b`, the long interval's tent kernel dominates the
corresponding kernel on each subinterval, and those subinterval interiors
are disjoint. Since `phi''>=0`,

```
J_phi(a,b)>=sum_(j=0)^(h-1) J_phi(x_j,x_(j+1)).         (5)
```

The same inequality holds for every continuous convex function. First check
it for a convex piecewise-linear function, represented as an affine function
plus a nonnegative sum of hinges `(x-t)_+`. A hinge's midpoint gap is one
half of the same tent value at its kink, so the kernel argument is identical.
Uniform piecewise-linear interpolants of a continuous convex function remain
convex and converge uniformly. Pass to the limit in the finite inequality.
This establishes (5) without any smoothness or curvature-monotonicity assumption.

## 4. Scalar sum: a product code preserves enough incompatible points

Set the same local tolerance `tau=epsilon/r` for every coordinate, and take the
maximal packing sets from Section 1. Adjacent selected points have midpoint
gap strictly greater than `tau`. By (5), an index separation of `h>0` implies
midpoint gap strictly greater than `tau h`.

For two product points with index vectors `u,v`, the scalar sum's midpoint gap
is the sum of its coordinate gaps. Consequently,

```
J_f(x(u),x(v))>tau sum_i |u_i-v_i|
```

whenever the points differ. In particular, index distance greater than `r`
forces `J_f>epsilon`.

The full product grid may contain close index neighbors, so select a separated
subcollection greedily, deleting after each selection all index points with
`ell_1` distance at most `r` from it. An integer lattice ball of that radius
in `r` dimensions has at most `6^r` points. Indeed,

```
#{z in Z^r: sum_i |z_i|<=r}
 <=2^r sum_(z in Z^r)2^(-sum_i |z_i|)
 =2^r [1+2sum_(k>=1)2^(-k)]^r
 =6^r.
```

The finite product boundaries can only reduce that number. The separated
subcollection thus has at least `product_i P_i/6^r` points, all pairwise
midpoint-incompatible. Parity gives

```
2^(p_conv)>=product_i P_i/6^r.                         (6)
```

The code is only a lower-bound existence argument. Neither its construction
nor enumeration of the product grid is part of the polynomial-time algorithm.

## 5. Compact scalar-sum construction and count

Run the reviewed compiled scalar curvature construction on `phi_i` at tolerance
`epsilon/r`, independently in every coordinate. Introduce their scalar outputs
`q_i` and set the final output exactly to

```
w=l^T x+b+sum_i q_i.
```

Each exact coordinate graph point is admitted, so the whole scalar-sum graph
is admitted. The total error is at most
`sum_i (15/16)(epsilon/r)=15epsilon/16`.
All component constructions have polynomial rational size and construction time;
replacing the tolerance by `epsilon/r` adds only `O(log r)` encoding bits.

Using (4) and (6),

```
p_out=sum_i L_i
 <=sum_i log2 P_i+r log2(481)
 <=p_conv+r log2(6*481)
 <p_conv+12r,
```

because `6*481=2886<4096`. This proves the first line of (1).

## 6. Finite linear gaps for arbitrary continuous convex summands

Replace the positive polynomials by arbitrary continuous convex functions
`phi_i` on `[0,1]`. The same graph models have finite comparisons

```
p_bin<=p_conv+7r                 (scalar sum),
p_bin<=p_conv+4r                 (independent outputs).             (7)
```

These bounds allow real coefficients and unrestricted continuous size; no
polynomial construction claim is made for arbitrary functions. Affine-only
coordinates may still be retained exactly.

The [scalar two-bit lemma](../notes/scalar-convex-graph-two-bit-gap.md) proves
`N_tau<=3N_(2tau)`. Combining with (2),

```
N_tau<=6P.
```

The finite chord-band encoding at tolerance `tau` therefore uses
`L=ceil(log2 N_tau)` binaries, with `2^L<=2N_tau<=12P`. Its exact graph
containment and error bound require no derivative assumptions.

For independent outputs, use each local tolerance `epsilon_i` and the full
product packing from Section 2. This gives
`p_bin<=p_conv+r log2(12)<p_conv+4r`. For a scalar sum, use local tolerances
`epsilon/r` and the product code (6), valid by the continuous-convex version
of (5). Summing local approximation errors gives the prescribed total error,
and the count is

```
p_bin<=p_conv+r log2(6*12)<p_conv+7r.
```

This proves (7). It is a finite geometric guarantee, independent of whether
the functions have rational descriptions or efficiently accessible knots.
The positive-polynomial construction in (1) adds a uniform computational
guarantee under its stated input assumptions.

## Scope and source boundary

The density theorem, compiled scalar quadrature algorithm, parity obstruction,
and finite interval-cover argument are supporting ingredients. The Jensen-gap
superadditivity and integer-lattice counting bound are elementary supporting
ingredients. The separate [feature-curve identities](../notes/positive-polynomial-feature-curve-geometry.md)
remain useful but are not needed for the sharpened proof.
The potentially new conclusions are the finite `O(r)` comparison for arbitrary
continuous convex separable sums and independent outputs, and its polynomial
rational construction for dense positive polynomials, without a degree penalty.

The coefficient-sum benchmark's log-log degree obstruction is consistent with
this result: the construction now adapts to each coordinate polynomial's shape
through an accuracy-dependent measure. It does not try to improve that inadequate
benchmark by changing only its constants.


## Verification and literature review

Two independent full audits passed for both the polynomial construction and the
finite continuous-convex extension:

* [First proof audit](../notes/review-positive-polynomial-linear-shape-precision.md).
* [Second proof audit](../notes/review-positive-polynomial-linear-shape-precision-second.md).
* [Focused primary-source and novelty review](../notes/positive-polynomial-linear-shape-precision-novelty.md).

The [exact arithmetic checker](../code/quadratic_rank/check_positive_polynomial_shape_geometry_review.py)
passes 1,973 feature comparisons, 1,973 squared-secant inequalities, 1,973 direct
Jensen-superadditivity inequalities, and 40 integer-lattice ball bounds. These
checks supplement the proofs; they do not implement or certify the full
polynomial-time quadrature algorithm, whose analytic justification is linked
through the scalar construction.


The [general convex-polynomial construction](convex-polynomial-compiled-integer-precision.md)
removes coefficient-sign and curvature-monotonicity assumptions for dense
polynomials. It gives an eleven-integer scalar comparison and separable
comparisons of `16r` for sums and `13r` for independent outputs.
