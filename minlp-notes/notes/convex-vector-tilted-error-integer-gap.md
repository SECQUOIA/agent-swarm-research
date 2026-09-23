# Convex vector graphs can have an integer-count gap for tilted error bodies

Date: 2026-09-05. Status: independently reviewed supporting consequence.
The [first audit](review-convex-vector-tilted-error-integer-gap.md) and
[second audit](review-convex-vector-tilted-error-integer-gap-second.md) passed.

With one input and two componentwise convex rational polynomial outputs,
binary formulations can require arbitrarily more integer variables than
general-integer formulations if the error body need not be unconditional.
The error bodies below are rational centrally symmetric parallelograms.
Their conditioning grows with the family; this is not a fixed-error-body
result. The [reviewed finite box bound](positive-polynomial-vector-refinement-obstruction.md)
already rules out such a gap with a
fixed number of convex outputs. The output-independent comparison for box
errors when the number of outputs grows remains open.

## Construction

Use the rational polynomial `q_M`, triangular wave `T_M`, and fixed tolerance
from the [nonconvex scalar gap construction](nonconvex-polynomial-binary-integer-gap.md):

```
M>=2,    degree(q_M)<=N=1024M^2,
0<=q_M<=1,    |q_M-T_M|<=1/32.
```

The scalar construction gives a rational MILP with two general integer
variables whose projection contains every `(x,q_M(x))` and permits only
scalar error at most `1/16`. Every binary convex lift at scalar error `1/4`
requires at least `ceil(log2 M)` binaries, by the separated peaks and troughs.

Write the dense monomial coefficients as `q_M(x)=sum c_k x^k`. Set

```
C_M=1+sum_(k=2)^N k(k-1)|c_k|,
F_M(x)=(q_M(x)+C_M x^2, C_M x^2),     0<=x<=1,
K_M={e in R^2: |e_1-e_2|<=1/4, |e_2|<=C_M}.
```

All data are rational with encoding length polynomial in the dense scalar
input. Since `|q_M''(x)|<=C_M-1`, both components of `F_M` are convex.
The set `K_M` is compact, centrally symmetric, and has nonempty interior.
For example, `(C_M,C_M)` belongs to `K_M`, while its first-coordinate sign
flip does not. Thus `K_M` is not unconditional.

## General-integer upper bound

Take the scalar two-integer lift with scalar output `s`. Introduce two output
variables `w_1,w_2` and impose only

```
0<=w_2<=C_M,          w_1=s+w_2.
```

Every exact vector graph point is admitted by choosing `s=q_M(x)` and
`w_2=C_M x^2`. Conversely, for the error `e=w-F_M(x)`,

```
|e_1-e_2|=|s-q_M(x)|<=1/16,
|e_2|=|w_2-C_M x^2|<=C_M.
```

Hence the entire projection lies in the prescribed graph error body, and

```
p_conv(F_M,K_M)<=2.
```

This upper bound is already a rational MILP. It uses the large allowed error
along the common output direction to absorb the convexifying quadratic.

## Binary lower bound

Given any binary convex lift for `(F_M,K_M)`, apply the linear output map
`s=w_1-w_2`. Its projection contains the complete scalar graph of `q_M` and
permits scalar error at most `1/4`, with exactly the same binary variables.
The scalar lower bound therefore gives

```
p_bin(F_M,K_M)>=ceil(log2 M).
```

Replacing the scalar period index by binary digits in the explicit upper
construction also gives `p_bin<=ceil(log2 M)+1`. Thus the vector family's
binary count is determined within one integer.

## Error geometry and source boundary

The Euclidean circumradius of `K_M` is at least `sqrt(2) C_M`, while its
Euclidean inradius is at most `1/(4 sqrt(2))`, owing to the narrow strip
`|e_1-e_2|<=1/4`. Their ratio is therefore at least `8 C_M`. In particular,
the growing anisotropy is part of the construction, not hidden in a claim
about a uniformly conditioned or fixed norm. More explicitly, at a peak
`a` and its adjacent troughs `a+-h`, with `h=1/(2M)`,
`q_M(a-h)-2q_M(a)+q_M(a+h)<=-15/8`. The centered second-difference identity
therefore gives `max |q_M''|>=(15/2)M^2`, so
`C_M>=1+(15/2)M^2` and the radius ratio is at least `8+60M^2`.

Adding a sufficiently large quadratic to convexify a smooth function is a
standard difference-of-convex construction; the general decomposition
framework long predates this application, as in
[Hartman (1959), *On functions representable as a difference of convex functions*](https://msp.org/pjm/1959/9-3/pjm-v9-n3-p09-p.pdf).
Linear output transformations
and the inherited scalar graph encoding are established mechanisms. The
supporting conclusion is the explicit failure of a dimension-only binary
versus general-integer comparison under coordinatewise convexity when the
allowed norm is arbitrary. No novelty is claimed for the convexification
step. This does not resolve the output-independent comparison for box or
unconditional errors when the number of outputs grows.

The [bounded primary-source audit](convex-vector-gap-and-overlay-source-audit.md)
confirms these attribution limits and did not locate the precise resulting
integer-count separation. This is not an exhaustive priority claim.
