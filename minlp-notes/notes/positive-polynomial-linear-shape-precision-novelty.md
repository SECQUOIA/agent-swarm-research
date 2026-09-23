# Source audit: linear-dimension integer precision for separable convex graphs

Date: 2026-09-05. Status: bounded primary-source novelty audit; mathematical review is separate.

The revised [candidate](positive-polynomial-linear-dimension-shape-precision.md)
has two distinct conclusions. For arbitrary continuous convex coordinate
functions, its scalar-sum graph has a finite binary formulation within `7r`
integers of every convex lift, and its independent-output graph has a gap
of `4r`. These finite statements permit real coefficients and unrestricted
continuous size. For dense rational positive polynomials, the construction
is polynomial in input and tolerance encoding, with respective gaps `12r`
and `9r`. No degree penalty occurs in either integer-count comparison.
Here `r` counts nonlinear coordinate functions, and the domain is the original
product box. The comparison is to arbitrary convex lifts with unrestricted
integer coordinates, not just to grid or piecewise-linear formulations.

I did not find a matching theorem in the primary sources examined. The most
plausible new contribution is this finite comparison to the minimum integer
dimension, together with the compact rational construction for the stated
polynomial class. Separable approximation, adaptive scalar knots, midpoint
obstructions, logarithmic disjunctions, and lattice-code packing are established
tools. The finite theorem is a short synthesis of those tools; it should not
be presented as a new general theory of convex approximation or coding.

## Simplification found during this audit

The original candidate used the positive-polynomial feature curve
`psi(x)=(sqrt(c_k) x^(k/2))_k` to compare Jensen gaps to squared Euclidean
distances. That remains a useful separate identity, but the final product
packing does not need it. For a twice continuously differentiable convex
function, integration twice gives the elementary tent-kernel formula

```
J_phi(a,b) = (phi(a)+phi(b))/2-phi((a+b)/2)
           = (1/2) integral_a^b min(t-a,b-t) phi''(t) dt.
```

For a partition `a=x_0<...<x_h=b`, the large tent dominates each smaller tent
on its support. Since curvature is nonnegative, this proves

```
J_phi(a,b) >= sum_j J_phi(x_(j-1),x_j).
```

The same conclusion holds for continuous convex functions by convex smoothing,
or their nonnegative second-derivative measure. Thus an ordered scalar packing
with adjacent Jensen gaps greater than `tau` has the stronger separation
`J_phi(x_j,x_k)>tau |j-k|`. The product argument at `tau=epsilon/r` needs
integer-index Manhattan distance greater than `r`, rather than `2r`.
The elementary bound

```
|{z in Z^r: ||z||_1<=r}|
  <= 2^r sum_(z in Z^r) 2^(-||z||_1) = 6^r
```

then gives the sharpened constants and the extension beyond positive
polynomials. The author incorporated this simplification after it was sent
for independent verification. No priority claim is made for the tent formula
or its immediate superadditivity consequence. Published superadditivity
results for Jensen functionals in their *weight vector* concern a different
operation and should not be cited as the exact interval statement without
checking their hypotheses.

## Closest primary sources and the distinctions

**Scalar adaptive approximation and interval packing.**
[Simchowitz, Jamieson, Suchow, and Griffiths (2018)](https://arxiv.org/pdf/1808.04523)
study adaptive convex regression using a local approximation modulus. Their
Lemma 2.1 gives the factor-two comparison between maximum chord error and
midpoint error used in the scalar packing step. Their Theorem 3.2 constructs
interval-based lower bounds for statistical sampling. This is relevant
precedent for local packing arguments, but its complexity is a sampling
quantity, not the integer dimension of an arbitrary convex lift.

[Fathabad, Cheng, Pan, and Yang](https://ira.lib.polyu.edu.hk/bitstream/10397/99199/1/Fathabad_Asymptotically_Tight_Conic.pdf),
Section 3.2, Lemma 5, Algorithm 1, and Theorem 2, prove optimal interpolation
point counts for their Gaussian-CDF approximation through sequential endpoint
selection. Their discussion extends the method to a broader monotone
convex/concave class. Thus minimum scalar segment counts are established
optimization targets. Enumerating all knots can take time exponential in
the accuracy encoding; this differs from the candidate's indexed compact
construction. See the [scalar source audit](compiled-curvature-quantile-precision-novelty.md)
for earlier minimax segmentation, certified quadrature, root isolation,
and computational-model distinctions.

**Jensen divergences and quadratic comparisons.**
[Kikianty, Dragomir, Dintoe, and Sherwell (2013)](https://vuir.vu.edu.au/40251/1/Approximations%20of%20Jensen.pdf)
define separable Jensen divergences in equation (1). Their Lemma 4 and
Theorems 6 and 9 give bounds and approximations through second derivatives
and power-function comparisons. This is a direct antecedent to treating
separable midpoint error as a divergence and comparing it with quadratic
quantities. It does not state the candidate's whole-formulation integer
comparison. Since the final proof bypasses the feature curve, no claim that
the square-root feature representation is unprecedented is needed.

**Product packing by integer codes.**
[Sok, Sole, and Tchamkerten (2014)](https://arxiv.org/pdf/1406.1055),
Section V, Lemma 3, record the exact cardinality of a Manhattan ball in
`Z^n`, including its generating function. Their Theorem 2 gives Gilbert
and Hamming bounds for their integer-code setting. The candidate's greedy
deletion of a radius-`r` ball from a rectangular product packing is the
standard Gilbert argument. Its elementary `6^r` bound needs no new coding
theorem. The metric here is Manhattan distance on integer indices; it is
not a cyclic Lee metric. The connection to summed convex Jensen gaps and
the subsequent comparison with general-integer lifts is the relevant step.

**Separable convex optimization.**
[Hochbaum and Shanthikumar (1990)](https://hochbaum.ieor.berkeley.edu/html/pub/Hochbaum-Shanthi-JACM90.pdf)
develop algorithms for separable convex optimization under linear constraints,
using proximity and scaling. Such algorithms optimize an objective over a
given feasible set. They do not provide a uniform two-sided outer
approximation of an entire nonlinear graph, nor do they minimize the number
of new integer variables in that approximation. A convex epigraph used
only for minimizing a convex objective is also a different modeling target.
This distinction matters because ordinary separable convex minimization
does not need graph-discretization integers in the first place.

**Formulation machinery.**
The midpoint/parity obstruction is inherited from mixed-integer convex
representability; logarithmic finite-disjunction encodings and Boolean-circuit
linearizations are established. The [compiler source audit](compiled-rational-knot-formulations-novelty.md)
documents the explicit predecessors, including continuous gate variables
forced Boolean by integral index bits. The candidate's polynomial-size
statement should cite those mechanisms rather than presenting circuit
compilation as new.

## Recommended claim and limits

A defensible statement is: the checked sources do not supply a finite
`O(r)` comparison between separable graph approximations and the minimum
integer dimension of arbitrary convex lifts, or the resulting polynomial
rational construction for dense positive polynomials. The candidate records
these comparisons, with classical ingredients explicitly credited.

The finite arbitrary-function result is not a polynomial-time oracle theorem.
The computational result does not cover sparse binary-encoded huge degrees,
arbitrary positive mixing across many outputs, or general coupled output
error bodies. It is an integer-count guarantee, not an assertion of ideal
continuous relaxations or a polynomial algorithm for solving every resulting
MINLP. Separate proof reviews must confirm the scalar construction and its
composition. The search was bounded: no matching result found is evidence
for a qualified novelty claim, not proof of priority.
