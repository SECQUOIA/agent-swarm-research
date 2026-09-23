# Second independent review: pooling with controlled bypass structure

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the combined exact polynomial-time theorem passes this audit.**
I reviewed the complete candidate `/tmp/pooling-bypass-structure-algorithm.md`,
intended for `results/pooling-bypass-structure-algorithm.md`, including its
affine-quality compression and vertex-integrity decomposition. This audit is
independent of `benders_property`'s mapping review and builds on my earlier
[fixed-core theorem audit](review-fixed-core-block-optimization.md).

The parameters fixed here are the pool count `p`, affine rank `t` of input
quality vectors, and a bypass deletion bound `c` leaving components of size
at most `h`. Input, output, attribute, and arc counts can grow. All flow upper
bounds must be finite and explicitly supplied or validly derived. The model
has no pool-to-pool arcs. This is polynomial bit complexity for each fixed
parameter choice, not an FPT or practical runtime claim.

## Exact mapping

Rational Gaussian elimination supplies an affine basis and input coordinates
with polynomial coefficient bit lengths. Positive-throughput pool coordinates
are weighted averages of the input coordinates, hence lie in the stated
coordinate boxes. Pool mass balance plus the `t` coordinate-mass balances
imply every original attribute balance. Conversely basis independence gives
the coordinate balances from the original balances. Inactive pools have no
incoming or outgoing flow by nonnegativity and mass conservation, so arbitrary
boxed coordinates suffice there. Reconstructed pool attributes preserve the
physical model even when the original formulation leaves inactive qualities
unspecified.

The flow partition covers each arc exactly once. Covered-input pool arcs,
covered-output pool arcs, and cover-to-cover bypasses are core variables.
All remaining arcs belong to the component of their noncovered endpoint or,
for an internal bypass, their common remaining component. No bypass between
different remaining components exists. Thus every noncovered input/output
throughput and output-quality constraint is local. Missing arcs can be omitted
without changing any argument.

The pool mass equations, coordinate balances, pool capacities, and covered-input
capacities have the displayed signs and fixed aggregate count. Their dependence
on the core is of degree at most two. Individual arc bounds remain with their
owning variables, and every linear arc cost is counted once.

The covered-output totals are the essential step when the number of attributes
is unbounded. Introducing its throughput `T_j` and `t` coordinate masses `M_js`
uses only `t+1` defining aggregate equations. Every original upper/lower quality
constraint then becomes a core inequality, regardless of its specification
vector. Pool contribution `q_ells v_ellj`, cover-input bypass contribution, and
remaining-component bypass contribution are all present exactly once. The
constant affine offset multiplies total throughput, as required.

The bounds `|M_js| <= A_s H_j` are valid because all nonnegative incoming
flows carry coordinates in `[-A_s,A_s]`; `H_j` bounds their sum. Together
with finite flow bounds and coordinate boxes, these give a compact core.
Extra constraints may make it nonconvex or empty, which the fixed-core theorem
allows. Lower and upper aggregate inequalities can be converted to equalities
with bounded scalar slack blocks. Interval bounds on the polynomial residuals
have polynomial bit length, since core dimension, degree, and variable-box
descriptions satisfy the theorem's assumptions.

The stated parameter bounds are valid:
`r<=pt+pc+c^2+cJ(t+1)`, `d<=max(1,ph+ch+h^2)`, and
`k<=p(t+1)+cJ(t+1)+2p+2cI`, with degree at most two. Scalar slack blocks
do not violate the dimension bound. Enumerating deletion sets takes polynomial
time for fixed `c`; a failed structural search must not be reported as physical
infeasibility. Algebraic recovery of all original flow variables and attributes
uses the already reviewed common-field guarantee.

## Boundary cases and exact checks

With no inputs, every flow is zero and the remaining bounds are checked
directly; affine rank need not be defined. With no pools, the original problem
is a direct blending LP regardless of graph structure. At rank zero all inputs
have the same quality vector, so fixing every pool to it makes the original
problem an LP even with many pools and arbitrary bypasses. Inactive pools,
isolated graph vertices, no remaining components, and an entirely covered
graph introduce no missing division or empty-block issue.

I wrote an independent
[symbolic mapping checker](../code/pooling_bypass_copy/check_structure_mapping_review.py).
It passed 375 exact ownership and residual checks across 15 models: rank zero,
one, and two; a mixed input/output cover; input-only and output-only covers;
no cover; and all vertices covered. Each model uses four attributes, omitted
pool arcs, and the corresponding internal/covered bypass types. The checks
compare physical attribute-mass residuals with compressed balances, verify
the signs of partitioned equations and covered-output definitions, and assert
that every flow has exactly one owner while noncovered node constraints remain
within their component.

These symbolic checks target omission and sign errors. They do not implement
quantifier elimination or replace the theoretical complexity proof. Literature
priority remains separate from this correctness review.
