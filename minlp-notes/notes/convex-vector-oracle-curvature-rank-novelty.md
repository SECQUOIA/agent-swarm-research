# Curvature-rank graph formulations with oracle error bodies: source assessment

Date: 2026-09-05. Bounded primary-source assessment by `joint_flow_novelty`.
The complete [main theorem](convex-vector-oracle-curvature-rank-precision.md)
and [rational spanner lemma](rational-polar-spanner-oracle.md) were read.
The separate mathematical audits are not replaced by this assessment.

No matching whole-formulation guarantee was located in the primary sources
checked. The defensible candidate contribution is a polynomial-time rational
MILP construction for a one-input, componentwise convex polynomial vector,
with an unconditional error body supplied by a strong separation oracle,
whose integer count satisfies

```
p_out <= p_conv + 17 + 2 ceil(log2 r).
```

Here `r` is the dimension of the nonlinear output image, after removing the
common input's affine contribution. The comparator permits arbitrary convex
lifts, unrestricted continuous size, and general integers. The companion
finite real-coefficient theorem has overhead `ceil(log2(8r^2-1))`.

The oracle and spanner mechanisms have close direct predecessors, including
positive-polar oracle access and approximate optimization inside a spanner
algorithm. These should remain supporting tools, rather than independent
broad novelty claims.

## Barycentric spanners are direct prior

Awerbuch and Kleinberg, *Adaptive Routing with End-to-End Feedback:
Distributed Learning and Geometric Approaches*,
[primary author manuscript](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf),
Section 2.3, PDF pp.4–5, supplies the exact construction used here.
Proposition 2.2 chooses a maximum-absolute-determinant basis of a compact
spanning set. Cramer's rule bounds all representation coefficients by one.
Observation 2.3 relates local determinant replacement bounds to approximate
spanners. Proposition 2.4 obtains a constant-approximation spanner through
linear optimization and determinant-increasing exchanges. Its stated oracle
count is `O(d^2 log_C d)`. These propositions and their exchange argument
were read directly.

Comparison: both finite maximum-volume bases and determinant doubling in
the candidate belong to this established mechanism. Applying it to a linear
image, retaining feasible preimages, and using a basis to sandwich a symmetric
body between a crosspolytope and a parallelotope are natural geometric
consequences. The candidate's running-time proof starts from explicit rational
seeds and tracks conditioning and bit length; it should not inherit the
source's oracle count without its different initialization argument.

Orestis Plevrakis and Elad Hazan, *Geometric Exploration for Online Control*,
[primary preprint](https://arxiv.org/pdf/2010.13178), Section 3.0.1,
Theorem 5, PDF p.5, imports the spanner theorem. Section 3.2, PDF pp.8–9,
explicitly combines convex-body separation, the ellipsoid method, approximate
function information, and an approximate optimization oracle to compute a
constant-approximation spanner. It states that the exchange proof continues
with a sufficiently accurate optimization oracle. Section 4.2, Theorem 13,
PDF p.10, gives an affine-spanner extension. These sections were read; the
control/regret proof was not audited. The institutional PDF endpoint failed
in this retrieval, but the open arXiv copy was readable.

Comparison: replacing exact optimization by an approximate oracle is already
explicit in primary literature. This source does not supply the candidate's
fixed rational denominator, exact-feasible repair, or positive-polar
formulation application. Those details are useful for a self-contained bit
complexity argument; their absence here is not evidence of a new general
spanner algorithm.

## Polar and positive-polar oracle access are also established

Grötschel, Lovász and Schrijver, *The ellipsoid method and its consequences
in combinatorial optimization*,
[primary paper](https://ir.cwi.nl/pub/10046/10046D.pdf), Definition (5),
printed p.172, states weak optimization with rational output near the body
and objective comparison against every exact feasible point. Theorem (3.1),
p.177, establishes weak optimization/separation equivalence with explicit
inner and outer balls. Lemma (3.2) and Corollary (3.4), p.178, address polar
oracle equivalence. Corollary (3.5), pp.178–179, treats the anti-blocker of a
convex downward-closed set in the nonnegative orthant. These definitions,
statements, and polar proof were read. The subsequent discussion emphasizes
that knowledge of an interior ball cannot simply be omitted.

Comparison: for unconditional `K`, the set `K intersect R_+^m` is
downward-closed, and its anti-blocker is exactly
`{lambda>=0: h_K(lambda)<=1}`. Thus the source directly covers the underlying
positive-polar access principle, not merely a distant general optimization
theorem. The candidate's explicit support-based weak separator and rational
central-ball repair give an implementation with the particular certificates
needed later. They do not furnish a strong polar oracle or exact support
optimization. The fixed grid addresses accumulated denominator growth across
exchanges, rather than improving the general oracle equivalence.

The two uses of geometry should be distinguished. Positive polar weights
preserve convexity of the selected scalar functions; a symmetric basis in
the effective primal body gives a finite rational inner band. Neither use
requires the effective body itself to remain unconditional after the change
of coordinates. Unconditionality is used in the original output coordinates
to evaluate nonnegative chord errors through positive polar directions.

## Minimum integer dimension and the midpoint obstruction have prior definitions

Lubin, Vielma and Zadik, *Mixed-integer convex representability*,
[primary manuscript](https://arxiv.org/pdf/1706.05135), Definition 4.3,
PDF p.11, defines MICP rank as the smallest number of integer variables in
an arbitrary convex lift. Lemma 4.1, PDF p.12, gives the midpoint obstruction:
a set containing `w` pairwise midpoint-incompatible points requires at least
`ceil(log2 w)` integer variables. The proof explicitly partitions integer
witnesses into parity classes. Corollary 4.2, PDF pp.13–14, applies this to
subsets of the binary hypercube and explains why unbounded integers do not
improve the binary lower count there. These definitions and proofs were read.

Comparison: minimizing integer dimension over general convex lifts, and
using parity to control possible midpoint errors, are established. The
candidate applies that obstruction to every admissible set between a graph
and its error tube, then constructs a rational graph-containing band with a
rank-dependent additive comparison. That particular approximation theorem
was not found in the cited representability paper. The nonlinear output
rank `r` and the comparator's MICP rank are different quantities and should
never share an unexplained use of the word “rank.”

## Shared vector interpolation and circuit compilation are inherited tools

The [previous vector-overlay source assessment](compiled-polynomial-vector-overlay-novelty.md)
records a particularly close finite formulation predecessor: Lyu, Hicks and
Huchette, [Section 3, Proposition 1 and Equation (4)](https://arxiv.org/pdf/2304.14542),
explicitly merge breakpoints of several outputs with the same scalar input
and use one SOS2 weight vector and one logarithmic interval encoding.
Shared output selection and a shared interpolation weight are therefore
established. That source reading is reused here, rather than claiming a
fresh full-paper review.

The [compiler assessment](compiled-rational-knot-formulations-novelty.md)
likewise documents prior continuous Boolean gate extensions, compilation
of algorithms into linear formulations, logarithmic discrete-function
encodings, and circuit-specified interpolation. The rank theorem does not
create a new compiler. Its scalar approximation dependency must retain the
already reviewed uniform dense-polynomial accuracy and encoding guarantees.

The distinction from the earlier explicit shared-breakpoint construction is
the complete guarantee: a polynomial-size rational output formulation can
use a scalarization selected from an implicit error body, approximate all
outputs within that body, and stay within the displayed overhead of the
unrestricted convex-lift benchmark. The final formulation contains a rational
parallelotope band; it does not attempt to encode the whole nonpolyhedral
body exactly.

## Scope and recommended positioning

The useful structural refinement is dependence on the dimension of the
nonlinear output image instead of an explicit facet count or total output
count. Positive scalarizations control all chord errors; a second basis
preserves a rational band inside the allowed body. This combination allows
the construction to exploit redundant nonlinear outputs while restoring
their affine parts exactly.

Several qualifications belong with the theorem:

* Output dimension, dense polynomial degree, coefficient lengths, oracle
  complexity, and radius encodings still affect total running time and MILP
  size. Their absence concerns the additive integer-count overhead only.
* The minimum comparator count can itself depend on the degree and error
  budget. The theorem does not bound it by a function of `r` alone.
* The bound is proved sufficient. This assessment found no matching lower
  bound requiring a `2 log r` penalty or the constant 17.
* The assumptions retain one scalar input, componentwise convexity, an
  unconditional body, and the stated oracle and radius promises. The theorem
  is not an arbitrary multivariate graph-approximation result.
* The algorithm need not compute the comparator or its minimum count. It
  also does not establish ideality, small practical constants, or polynomial
  time for solving the resulting MILP.

A suitable novelty statement is: “Combining established barycentric-spanner,
convex-body oracle, parity, and compilation tools yields a uniform rational
formulation theorem whose integer-count overhead depends only logarithmically
on the nonlinear output dimension. No matching whole-formulation guarantee
was located in the primary sources checked.”

Fresh searches covered barycentric spanners with approximate oracles,
positive polar and anti-blocker computation, MICP rank and midpoint bounds,
vector PWL approximation, and integer-efficient graph formulations. The
bounded search supports this qualified positioning; it does not establish
exhaustive priority. The supporting oracle lemma is best presented as an
explicit implementation of established machinery, with the combined graph
precision theorem carrying the substantive candidate contribution.
