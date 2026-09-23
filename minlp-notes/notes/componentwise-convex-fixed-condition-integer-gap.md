# Finite integer-count bounds for componentwise convex curves

Date: 2026-09-05. Status: main statements (1)--(3) and the final
simplex-band sharpenings independently reviewed; the linked root audit
includes the completed addendum.
Proof developed by potential_flow_review; binary_formulation_review supplied
the sharper level-cut refinement and the infinity-norm formulation.
The [root's full audit](review-componentwise-convex-fixed-condition-integer-gap-root.md)
passes the original main statements and proofs.

For one input and finitely many componentwise convex outputs, a fixed
condition number prevents an unbounded binary versus general-integer gap.
Every unconditional error body also has a dimension-only bound. These are
finite comparisons with unrestricted continuous formulation size and real
coefficients. They do not give a compact or polynomial-time construction.

Let `F=(f_1,...,f_m):[0,1]->R^m` have continuous convex components, with
`m>=1`. Let `K` be a compact convex error body with `0` in its interior.
An admissible formulation has projection containing every `(x,F(x))`,
has input projection exactly `[0,1]`, and admits only points with
`w-F(x) in K`. Write `p_conv` for the minimum number of general integer
variables in an arbitrary convex lift, and `p_bin` for the minimum number
of binary variables in a linear lift with arbitrary finite continuous
size and real coefficients. The results below show finiteness as well.

## A conditioning bound

If `r B_infinity subset K subset R B_infinity`, where `0<r<=R`, then

```
p_conv <= p_bin <= p_conv + ceil(log2(2ceil(2mR/r)-1)).       (1)
```

If instead `r B_2 subset K subset R B_2`, exactly the same bound (1) holds
with these Euclidean radii. In particular, fixed `m` and fixed `R/r` give
a constant additive difference independent of the functions.

### Parity supports and scalar chord gaps

Fix an admissible convex lift with `p` general integer variables. For each
of the at most `2^p` parity classes, collect the inputs whose exact graph
points have some witness in that class. Two such witnesses have an integer
midpoint. Convexity of the lifted set therefore implies

```
J(x,y) = (F(x)+F(y))/2 - F((x+y)/2) in K.
```

Each component of `J` is nonnegative. Put `h=sum_i f_i`. Under infinity
containment, its midpoint Jensen gap is at most `mR`. Under Euclidean
containment it is at most `sqrt(m)R`, by Cauchy--Schwarz.

Take the closed span of each nonempty parity support. Continuity extends
the midpoint inequality to the two endpoints of this span; no closedness
of the lifted set or existence of limiting witnesses is required. On an
interval `[a,b]`, the chord gap `g=chord(h)-h` is concave, nonnegative,
and zero at the endpoints. Its maximum is at most twice its value at the
midpoint: concavity between a maximizer and the farther endpoint proves
this inequality. Thus the span has maximum `h` chord gap at most

```
E = 2mR       (infinity containment),
E = 2sqrt(m)R (Euclidean containment).
```

The finitely many spans cover `[0,1]`. They can be trimmed to a partition
with at most `2^p` nondegenerate intervals, each contained in one span:
starting at the left endpoint, repeatedly choose a covering interval with
left endpoint no larger than the current point and farthest right endpoint.
If the endpoint has not reached 1, the finite covering property guarantees
a strictly advancing choice. No span is selected twice. Restricting a
chord interval cannot increase its maximum chord gap, because the smaller
chord lies below the restriction of the larger one.

### Level-cut refinement

If a continuous convex function has chord gap at most `E` on an interval,
then for any `t>0` it has a partition into at most

```
max(1, 2ceil(E/t)-1)
```

intervals with chord gap at most `t`.

To see this, let `H` be the actual maximum of the original concave gap
`g`. If `H<=t`, use one interval. Otherwise put `n=ceil(H/t)`. For each
level `jt`, `1<=j<=n-1`, cut at both boundary points of the superlevel
interval `{g>=jt}`. These points are ordered into at most `2n-1` pieces.
On each piece the range of `g` has length at most `t`: this follows from
the successive levels on the two sides and from `H-(n-1)t<=t` on the
middle piece. The new chord gap of the original function is `g` minus
the chord of `g` on that piece. It is nonnegative and at most the range
of `g`, hence at most `t`. Plateaus and coincident cuts only reduce the
number of pieces.

### A binary linear lift

In the infinity case set `t=r`; in the Euclidean case set `t=r/sqrt(m)`.
The ratio `E/t` is `2mR/r` in either case. Applying the refinement to all
parity-span intervals yields at most

```
2^p [2ceil(2mR/r)-1]
```

intervals. On each, let `T_i` be the component chord. The component gaps
`T_i-f_i` are nonnegative and sum to the `h` gap, so each is at most `t`.
Use the linear bands

```
T_i(x)-t <= w_i <= T_i(x),  i=1,...,m.
```

They contain the exact vector graph. Every admitted error has
`|w_i-f_i(x)|<=t`, so it belongs to `r B_infinity` in the first case and
to `r B_2` in the second. It therefore belongs to `K`.

The finite union of these bounded polyhedra has a linear formulation with
`ceil(log2(number of intervals))` binary variables. For completeness,
assign a distinct binary string to every interval, impose each polyhedron's
rows with a sufficiently large constant times the Hamming distance from
its string, and exclude unused strings. Global bounds on all input and
output variables make finite valid constants available. This proves (1).
The lower inequality follows since a binary linear lift is a convex lift
with the same number of general integer variables.

## Boxes and all unconditional bodies

For any positive coordinate tolerances `a_i`, the error box
`K=product_i[-a_i,a_i]` satisfies

```
p_bin <= p_conv + ceil(log2(4m-1)).                    (2)
```

Indeed, positive diagonal output scaling by `1/a_i` preserves component
convexity and both integer counts, while turning the error body into the
unit infinity ball. Apply (1) with `r=R=1`. For two outputs, the additive
bound is three binary variables. For one output it is two, agreeing with
the existing [scalar lemma](scalar-convex-graph-two-bit-gap.md).
The earlier [output-refinement note](positive-polynomial-vector-refinement-obstruction.md)
already proves the stronger box bound `ceil(log2(2m+1))` by overlaying
two cuts per component. Thus (2) is a corollary, not a box improvement.

More generally suppose `K` is unconditional: it is invariant under every
independent coordinate sign change. Put `a_i=max_{e in K}|e_i|>0`, and
scale coordinates by `1/a_i`. The resulting body `K'` satisfies

```
(1/m) B_infinity subset K' subset B_infinity.
```

The second inclusion is the definition of `a_i`. To prove the first,
choose a point attaining each coordinate maximum and average its sign
flips in all other coordinates. Convexity and unconditionality imply that
both positive and negative coordinate unit vectors belong to `K'`.
Their convex hull is the unit one-norm ball, which contains
`(1/m) B_infinity`. Applying (1) gives

```
p_bin <= p_conv + ceil(log2(4m^2-1)).                  (3)
```

Thus the [tilted-body gap](convex-vector-tilted-error-integer-gap.md) cannot
be reproduced in this one-input setting with any unconditional error body
at fixed output dimension, even if its coordinate scales vary arbitrarily.
The argument does not apply to several input variables, nonconvex output
components, or restrictions on total formulation size or rational encoding.
These bounds still grow with the number of outputs; they do not settle
whether a dimension-independent additive comparison holds for boxes or
unconditional bodies as `m` grows.
No independent novelty claim is made for the parity, chord, or finite
disjunction ingredients.

## Sharpening with simplex bands

The root reviewer suggested replacing the independent bands by one simplex
band. This yields two additional bounds with the same finite scope.

On an interval where the scalar chord gap satisfies `sum_i g_i<=s`, use

```
w=T-v,        v>=0,        sum_i v_i<=s.
```

This polyhedron contains the exact vector graph by choosing `v=g`.
Every admitted error is `g-v`, where both vectors are nonnegative and
have one-norm at most `s`. Consequently

```
||g-v||_2^2 <= ||g||_2^2+||v||_2^2 <= 2s^2,
||g-v||_1 <= 2s.
```

For Euclidean containment, choose `s=r/sqrt(2)`. Starting from
`E=2sqrt(m)R`, the same level-cut proof gives the sharper bound

```
p_bin <= p_conv + ceil(log2(2ceil(2sqrt(2m)R/r)-1)).       (4)
```

One may take the smaller of (1) and (4). For an unconditional body, use
the positive diagonal normalization above, so `B_1 subset K' subset
B_infinity`. Here `E=2m`. Taking `s=1/2` gives errors in `B_1 subset K'`
and therefore

```
p_bin <= p_conv + ceil(log2(8m-1)).                       (5)
```

This improves (3) when `m>2`, agrees with it at `m=2`, and is weaker at
`m=1`, where the scalar two-bit comparison applies. The simplex is
polyhedral even if the original unconditional body has infinitely many
supporting directions; no facet representation of that body is required.
