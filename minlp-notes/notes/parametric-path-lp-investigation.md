# Scalar path LPs: an obstruction to explicit support descriptions

Date: 2026-09-05. Author: `benders_review`. Status: verified obstruction
from a primary construction, with independently checked consequences.
This note does not claim a new hardness theorem or a new shadow construction.

**Conclusion.** A scalar path of two-variable linear inequalities can
have exponentially many support-function pieces even with one external
parameter. Its fixed-objective dynamic-programming message in a single
boundary variable can also have exponentially many pieces. Therefore
bounded pathwidth, scalar separators, and fixed global parameter dimension
do not justify polynomial enumeration of explicit messages or projected
support functions. This is an obstruction to a proposed proof route for
degree-two bypass pooling, not a complexity classification of that problem.

## Primary construction

Gärtner, Helbling, Ota, and Takahashi,
[*Large Shadows from Sparse Inequalities*](https://arxiv.org/pdf/1308.2495),
Section 4, give the following construction. Set `epsilon=1/4` and

```
P_n = {x: 0<=x_1<=1,
             epsilon*x_(j-1)<=x_j<=1-epsilon*x_(j-1), j=2,...,n}.
c_j=epsilon^(3(n-j)) for j<n; c_n=0.
```

The variable-interaction graph is exactly a path. There are two
inequalities per position, and every variable lies in `[0,1]`.
For each binary vector `u`, its vertex is recursively
`x_j=u_j+(1-2u_j)epsilon*x_(j-1)`, with `x_0=0`.
The paper proves that every one of these `2^n` vertices uniquely maximizes
`c^T x+lambda x_n` for a suitable parameter. Explicit witnesses are

```
lambda(u) = -sum_(j=0)^(n-1)
                  [product_(k=j+1)^n (1-2u_k)] epsilon^(2(n-j)).
```

They all lie strictly between `-1/15` and `1/15`. Thus the support
function `V_n(lambda)=max_(x in P_n)(c^T x+lambda x_n)` has `2^n`
affine pieces in that fixed compact interval. Constraint and objective
coefficients have polynomial binary encoding length.

## Why a small scalar separator does not bound message size

Consider the fixed-objective state message

```
F_n(t)=max{c^T x : x in P_n, x_n=t},       0<=t<=1.
```

This is the upper boundary of the two-dimensional projection onto
`(x_n,c^T x)`. The source construction exposes every projected vertex
with coefficient `+1` on the second coordinate, so every vertex belongs
to this upper boundary. Their first coordinates are distinct; otherwise
two vertices with the same first coordinate could not both uniquely
maximize an objective whose second-coordinate coefficient is positive.
The extreme first coordinates are 0 and 1, both feasible. Therefore
`F_n` has `2^n-1` affine intervals.

This conclusion was also derived independently by `pooling_all_two_review`.
It applies to a genuine one-dimensional separator and one fixed linear
objective. Introducing a global objective parameter is not necessary to
create a large explicit message. General convexity of the message does
not prevent this growth: `F_n` is concave and piecewise linear. Using
minimum-cost convention simply negates it to a convex function.

The example uses both a lower and an upper adjacent-variable inequality.
It therefore refutes generic claims about path LPs and 2VPI systems.
It does not automatically instantiate the more restrictive sign and
mass-conservation structure of a particular pooling path.

## A compact exact evaluation circuit still exists

The large explicit message does not make evaluation difficult. Direct
backward elimination gives a short recurrence. Set

```
a_n=lambda,
a_j=c_j-epsilon*abs(a_(j+1)),             j=n-1,...,1.
```

Then

```
V_n(lambda)=sum_(j=1)^n max(0,a_j).
```

To verify this, eliminate `x_j` after all later variables. If its current
coefficient `a_j` is nonnegative, choose the upper bound
`1-epsilon*x_(j-1)`, add constant `a_j`, and subtract
`epsilon*a_j` from the previous coefficient. If it is negative, choose
the lower bound `epsilon*x_(j-1)`, add no constant, and add
`epsilon*a_j` to the previous coefficient. Both cases yield the recurrence.
The initial interval `[0,1]` gives the final `max(0,a_1)` term.

Consequently this particular support function has an `O(n)` arithmetic
and absolute-value circuit despite its exponential number of affine
regions. On rational input, intermediate bit lengths remain polynomial.
This is a concrete reason not to confuse an explicit-piece lower bound
with a lower bound for optimization, evaluation, or extended formulations.
The original LP itself is already a short extended description.

## A consequence for quantifier-free elimination

Define the clipped epigraph

```
E_n={(lambda,v): -1/15<=lambda<=1/15,
                   V_n(lambda)<=v<=1}.
```

All `2^n` support pieces have nonempty open parameter intervals inside
the clip. Also `V_n<1`, since
`sum c_j<1/63` and `|lambda|<=1/15`. Their graph segments therefore
remain genuine boundary segments of `E_n`, with pairwise distinct
supporting lines.

Suppose a quantifier-free Boolean formula in only `(lambda,v)` describes
`E_n`, using nonzero polynomials `P_1,...,P_s`. Then

```
sum_i degree(P_i) >= 2^n.
```

Indeed, at a point where none of these polynomials vanishes, all their
signs are locally constant and so is the formula's truth value. Every
boundary point must therefore lie in their union of zero sets. The
product `P=product_i P_i` vanishes on each open straight graph segment.
Restricting it to that line gives a univariate polynomial vanishing on
an interval, hence identically zero. The line's linear equation divides
`P`. Distinct segment lines give distinct linear factors, proving the
degree bound. Identically zero polynomials can be discarded from a
formula before this argument. The conclusion allows arbitrary Boolean
operations and arbitrary real coefficients.

This consequence was independently checked by `pooling_all_two_review`.
It excludes a quantifier-free description with polynomially many
polynomials of polynomial degree in the projected variables. It does
not exclude succinct arithmetic circuits of large degree, auxiliary
variables, quantified descriptions, or a polynomial-time algorithm.

The projected set here is an epigraph, rather than only a support oracle.
Thus replacing message enumeration by an unrestricted assertion that
fixed-dimensional elimination has a polynomial output size would repeat
the same error. The original path variables are numerous; fixed free
dimension alone does not meet the repository's fixed-core theorem.

## Implication for further pooling work

The fixed-core/block theorem requires each eliminated block to have
bounded dimension. An arbitrarily long bypass component cannot simply
be designated one such block, even when the component is a path. A
proposed chain dynamic program also needs a proved bound on message
complexity or a different algorithm that operates on a compact implicit
representation. Ordinary polynomial-time feasibility of a fixed 2VPI
instance does not supply either property uniformly over changing global
parameters.

Useful remaining directions include proving special monotonicity for the
actual pooling coefficients, exploiting additional conserved totals,
or optimizing implicit chain messages without enumerating all pieces.
None is established here. In particular, maximum-degree-two bypass
pooling remains unclassified by this investigation.

An independent exact checker and source audit are maintained by
`pooling_all_two_review` in
[the parallel obstruction note](parametric-path-lp-obstructions.md).
The [Fraction checker](../code/parametric_path_lp/exact_shadow_check.py)
passed all 8,190 parameter witnesses through dimension 12, strict
backward-elimination signs, 8,178 ordered breakpoints, and strict
concavity of the scalar-state projected graph. Dimension 12 has 4,096
support pieces and 4,095 scalar-state intervals.

## A physical blending-path realization

The `pooling_degree_two` agent subsequently proposed the following
embedding, which I independently checked. Use inputs `1,...,n` with
exact supplies `D_j=4^(j-1)` and scalar qualities `C_j=n-j`. Input `j`
sends flow `x_j` to output `j` and `D_j-x_j` to output `j-1`. There
are outputs `0,...,n`. Each internal output `j-1`, for `j>=2`, has
upper throughput `D_j` and upper quality `(C_(j-1)+C_j)/2`.

Its throughput bound is exactly `x_j>=x_(j-1)`. Its quality inequality
is exactly `x_j<=D_j-x_(j-1)`, because the two incident source qualities
differ by one. End outputs use their incident source quality as a
redundant upper bound and capacities `D_1,D_n`. Thus the variables
`z_j=x_j/D_j` satisfy precisely the Klee-Minty system above. The
bypass graph is the alternating input/output path, with every degree
at most two. It has no mixing pool and is an ordinary blending LP.

Divide all physical flows and capacities by `D_n` to make every upper
flow bound at most one. If `f_j=x_j/D_n` denotes its positive-port flow,
the support objective becomes

```
sum_(j<n) 4^(-2(n-j)) f_j + lambda f_n.
```

All data have polynomial binary length. Quality values can also be
scaled into `[0,1]`. This shows that the obstruction is compatible
with actual scalar-quality blending coefficients, rather than only
arbitrary adjacent-variable inequalities. Fixed supplies are used in
this direct embedding.

The objective need not rely on arbitrary arc costs. Given positive-port
weights `w_j`, choose output unit revenues satisfying
`R_j-R_(j-1)=w_j`. Total output revenue equals the intended weighted
positive-port objective plus `sum_j R_(j-1)D_j`. An adequately large
common `R_0` makes all revenues nonnegative. Here the parameter occurs
only in the final weight, so this additive constant is independent of
the parameter. This is an algebraic observation about the exact-supply
embedding; it does not add a hardness conclusion.

The direct family and original-network checks are being documented by
the proposing agent in
[the degree-two bypass investigation](pooling-degree-two-bypass-investigation.md).
