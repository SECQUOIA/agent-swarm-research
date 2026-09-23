# Independent review: all-product-contract pooling feasibility

Date: 2026-09-05. Reviewer: `pooling_degree_two`. Verdict: **PASS** for
[the candidate theorem](pooling-all-product-contracts-quasipolynomial.md)
with its exact flow/quality contracts and redundant common pool-capacity
assumption. Priority remains separate.

## Local and global equivalence

Exact supplies determine each intake as `a_i-sum_j z_ij`; exact demands
determine each outlet as `b_j-sum_i z_ij`. Missing pool arcs are fixed
to zero. These substitutions preserve every individual bound through
rows in at most two bypass coordinates. Exact output quality becomes
`sum_i(C_i-q)z_ij=b_j(B_j-q)`, with degree-one polynomial coefficients
in the common scalar parameter. The original input and output rows
therefore give exactly the stated bounded parametric path relations.

The total mass equality in (1) makes summed intake equal summed outlet.
Summing the exact output-quality equations and using the total attribute
equality in (1) gives the actual pool quality balance. This argument
works for every locally feasible assignment, independently of the choices
made inside different bypass components. It uses every product's exact
quality mass, rather than merely an upper or lower specification.

At zero throughput, all nonnegative intake and outlet flows vanish.
Every local quality equation then reduces to its bypass-only equation,
and any concentration in the allowed feed-quality interval is harmless.
At positive throughput the derived pool quality balance puts the chosen
concentration at the actual weighted average. A pool with no feed or no
outlet is correctly removed only after checking its forced-zero incident
arcs and retaining external contracts.

## Component elimination and common parameter

After local substitution, every bypass path is a scalar relation chain
with the required parameter-affine coefficients. A bypass cycle can be
cut at one arc variable, composed, and restricted to equal endpoint
coordinates. Adding that diagonal equality before the final minor-sign
refinement preserves boundedness and the polynomial-per-cell bound.
Isolated nodes give elementary univariate parameter conditions.

Each component's feasible parameter set can be made constant on each
refined open cell or isolated point using the candidate row intersections.
The extra determinant polynomials have polynomial degree and height,
and their number is polynomial per existing cell. Overlaying all component
partitions uses the union of their univariate breakpoints. It therefore
does not multiply their quasipolynomial cell counts. A common surviving
parameter exactly characterizes global feasibility by the conservation
identities above.

## Constructive encoding

The common parameter is either a rational interval sample of polynomial
bit length or an isolated algebraic root of a polynomial with polynomial
degree and height. Component endpoints can be chosen at vertices of
their bounded planar relations over this same field.

For a direct polynomial encoding bound on the lifted midpoint witness,
track each coordinate as a rational function of the common parameter.
Slice endpoints divide only by an evaluated nonzero row coefficient,
which is an explicitly encoded polynomial in that parameter. Each
reconstruction step uses a constant number of rational-function operations
on its parent endpoints. Balanced depth is logarithmic. Numerator and
denominator degrees and coefficient heights therefore remain polynomial,
by the same constant-factor recurrence as in the projection proof. Final
evaluation at the single selected algebraic parameter yields a
polynomial-size common-field representation. There is no need to form
a compositum of roots from different components.

The draft's separate Cramer observation is also correct for an original
component vertex at the fixed parameter. The rational-function tracking
argument directly covers the midpoint reconstruction actually proposed.

## Capacity and objective scope

The physical two-component capacity counterexample is exact. Its local
rows force `T=1/(q(2-q))` on `q in [1/2,3/2]`, so `T>=1`; they are
feasible at `q=1`, whereas an additional common pool cap `3/4` makes
the original network infeasible. Thus that cap cannot be dropped by the
global identities. This proves a limit of the elimination, not hardness
of the capped class.

All ordinary source and product throughputs are fixed, so standard
input-production and output-revenue profit is constant. Arbitrary arc
costs and nonconstant pool-throughput costs remain outside the result.
No polynomial-time or matching quasipolynomial lower-bound claim is made.

This is an independent symbolic proof audit. No additional numerical
experiment is claimed for the asymptotic bound; the underlying polygon
and conservation steps have separately documented checks.
