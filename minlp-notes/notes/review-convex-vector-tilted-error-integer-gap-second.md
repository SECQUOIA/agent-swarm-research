# Independent second review: convex vector graph with tilted error body

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Candidate: [convex vector tilted-error gap](convex-vector-tilted-error-integer-gap.md).
Verdict: **PASS** for the stated growing family of rational error bodies.

The proof establishes an unbounded binary-versus-general-integer count gap
with one input and two componentwise convex polynomial outputs. It does
not establish such a gap for a fixed error body, a uniformly conditioned
family of bodies, or an unconditional body. This review checks the
mathematical construction and encoding; publication priority is separate.

## Scalar dependency and model

The source scalar family was independently checked in
[the nonconvex polynomial gap audit](review-nonconvex-polynomial-binary-integer-gap-second.md).
It provides a rational polynomial `q_M` satisfying
`0<=q_M<=1` and `|q_M-T_M|<=1/32` on `[0,1]`. Its rational MILP with
one bounded period integer and one orientation binary contains the entire
scalar graph and admits only scalar errors of magnitude at most `1/16`.
Every binary convex lift allowing error `1/4` needs at least
`ceil(log2 M)` binaries. Replacing the period by binary digits gives
an upper bound of `ceil(log2 M)+1`.

The distinction between models remains the same here: the general-integer
upper bound is already an ordinary rational MILP, while the binary lower
bound permits arbitrary convex continuous lifts and unlimited continuous
size. The orientation binary is counted as one of the two integers.

## Convexity and rational input length

Write `C=1+sum_(k>=2)k(k-1)|c_k|`. On `[0,1]`, the triangle inequality
gives `|q_M''(x)|<=C-1`. The two output second derivatives are therefore

```
(q_M+Cx²)'' = q_M''+2C >= C+1>0,
(Cx²)'' = 2C>0.
```

Thus both outputs are in fact strictly convex, including throughout the
closed domain in the stated polynomial sense. No positivity of the
monomial coefficients of `q_M` is assumed.

The dense monomial coefficients are rational. Forming the finite sum
defining `C`, and then adding it to a quadratic coefficient, uses
polynomial rational arithmetic. Numerator and denominator lengths remain
polynomial in the dense scalar input length. Summing through the stated
degree bound causes no problem: trailing coefficients are zero and may
be omitted. Even if the actual degree is smaller than that bound, the
scalar family's degree is at least `2M`, so `1024M²` is polynomial in
its actual dense degree. No compact encoding in `log M` is claimed.

## Error body and domain restrictions

The map `e -> (e_1-e_2,e_2)` is invertible and rational. Hence

```
K={e: |e_1-e_2|<=1/4, |e_2|<=C}
```

is a rational compact centrally symmetric parallelogram with nonempty
interior. Since `C>=1`, the point `(C,C)` belongs to `K`, but its
first-coordinate sign flip `(-C,C)` does not: the narrow-strip expression
has magnitude `2C>1/4`. Thus the lack of unconditionality is explicit.

The graph domain is exactly `[0,1]`; its restrictions are inherited from
the scalar period formulation. They are essential to the upper bound
because they imply `0<=Cx²<=C`. There is no assertion about inputs
outside this domain, or about merely checking the error on a subset of
a larger admitted input domain.

## General-integer formulation: both inclusions

Introduce continuous `w_2` with `0<=w_2<=C` and set `w_1=s+w_2`, where
`s` is the existing scalar approximate output. These are linear constraints,
so the resulting formulation is a rational MILP with the same two declared
integer variables. There is no constraint requiring the nonlinear identity
`w_2=Cx²`.

For exact graph containment, at each input choose the scalar witness with
`s=q_M(x)`, which exists by the scalar construction. Then choose the
permitted continuous value `w_2=Cx²`. This realizes exactly
`(w_1,w_2)=(q_M(x)+Cx²,Cx²)`. The nonlinear choice used to prove existence
does not need to be imposed as a formulation equation.

Conversely, every admitted point satisfies

```
e_1-e_2=s-q_M(x),
e_2=w_2-Cx².
```

The first has magnitude at most `1/16`, below the permitted `1/4`.
The second has magnitude at most `C` because both of its terms lie in
`[0,C]`. Thus every admitted vector error belongs to `K`. This proves
the full projection inclusions, not merely feasibility of selected graph
points, and establishes `p_conv<=2`.

The large permitted error along the common output direction is precisely
what makes a continuous interval sufficient for the convexifying output.
No hidden integer, nonlinear constraint, or unencoded coefficient is used.

## Binary lower bound and matching family upper bound

For any admissible binary convex lift of the vector graph, add the linear
output equation `s=w_1-w_2` and project onto `(x,s)`. Exact vector graph
containment gives exact scalar graph containment. For every admitted
vector error, the body's narrow strip gives
`|s-q_M(x)|=|e_1-e_2|<=1/4`. The linear map and projection preserve
convexity of the underlying lifted set and do not change the binary count.

The scalar binary lower bound therefore applies without modification:
`p_bin>=ceil(log2 M)`. It ultimately uses two peak witnesses with the
same full binary assignment and their entire chord, not merely equal
parity of general integer witnesses. Thus the existing two-general-integer
formulation creates no contradiction with the lower argument.

Conversely, replace the period variable in the explicit upper construction
by `ceil(log2 M)` binary digits and retain its period bound to exclude
unused codes. Together with the orientation bit and the same continuous
output interval, this gives `p_bin<=ceil(log2 M)+1`.
Consequently the vector family's binary optimum is determined within one
integer, while its general-integer optimum is at most two. In particular
the difference of the optima tends to infinity.

## Conditioning and its necessary growth in this construction

The body contains `(C,C)`, so its circumradius is at least `sqrt(2)C`.
Any Euclidean ball inside it has radius at most half the width of the
strip `|e_1-e_2|<=1/4`, namely `1/(4sqrt(2))`. Therefore the ratio of
circumradius to inradius is at least `8C`. The central symmetry makes
the origin a valid center for the usual radius comparison; the strip
bound also holds for balls with arbitrary centers.

The claimed growth of `C` can be made explicit. Take consecutive troughs
`a=j/M`, `b=(j+1)/M` and their midpoint peak `c=(a+b)/2`. The scalar
approximation guarantees imply

```
q_M(a)+q_M(b)-2q_M(c) <= -15/8.
```

The centered second-difference identity is

```
q_M(a)+q_M(b)-2q_M(c)
 = integral_a^b min(t-a,b-t) q_M''(t) dt.
```

The nonnegative kernel has integral `(b-a)^2/4=1/(4M²)`. Hence
`max |q_M''|>=(15/2)M²`, and the coefficient bound gives
`C>=1+(15/2)M²`. In particular the radius ratio is at least
`8+60M²`. This verifies that the growing anisotropy is mathematically
forced by this explicit convexification bound, not just left implicit
in a potentially constant parameter.

An invertible linear change of output coordinates can map the error body
to a box, but it then exposes `q_M` as one output, which is nonconvex.
It therefore does not transfer this example into a counterexample with
both componentwise convexity and box errors. The candidate correctly
leaves that stronger question open.

No mathematical correction was required by this independent review.
