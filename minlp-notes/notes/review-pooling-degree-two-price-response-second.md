# Second review: upper-only blending-path price response

Date: 2026-09-05. Verdict: PASS for Sections 3–5 of
[the degree-two path note](pooling-degree-two-bypass-investigation.md),
together with the previously checked physical embedding. No hardness
claim is supported or made.

## One varying output price

After normalizing flows, source `j` has supply `s_j=4^(j-n)` and
rightward flow `t_j=s_j z_j`. Therefore the objective coefficient on
that physical flow is `c_j/s_j=16^(j-n)` for `j<n`, with coefficient
`lambda` on the last flow. Defining successive output prices by those
differences realizes the exact source objective.

Only `R_n` depends on the parameter. The constant contribution is
`C0=sum_j R_(j-1)s_j`, which excludes `R_n` and is therefore independent
of the parameter. The geometric sum of the fixed increments is less
than `1/15`; adding `lambda in [-1/15,1/15]` keeps every base price
strictly between zero and two. All input production costs may be zero.

## Uniform removal of source lower bounds

Use the `2n` actual arc flows as variables. The copy-only polytope here
is the entire exact-supply blending LP. It is nonempty by the previously
verified affine map from the Klee–Minty cube. Internal homogeneous upper
quality rows scale to `right_(j-1)-left_j<=0`; all other rows have
coefficients in `{-1,0,1}`. Source-contract coefficients are zero or one
and remain unscaled. The normalized supply right-hand sides are rational;
this causes no difficulty because the projection bound depends on row
coefficients, not right-hand-side denominators. The positive residuals of
the opposite contract rows are exactly the original supply deficits.

Thus the reviewed coefficient bound gives `H=N^N`, with `N=2n`.
Every unpenalized arc revenue is at most two throughout the entire
parameter interval. Repairing a relaxed point to the exact-supply
polytope loses at most `2H delta` in base revenue. The parameter-uniform
choice `M=2H+1` strictly dominates that loss.

Adding `M` to every output price rewards total physical throughput.
Every arc goes from an input to an output, so this is exactly `M` times
total input usage, including when contracts have not been filled. The
penalized offset is `M sum_j s_j`, independent of the parameter. Every
point with positive deficit is strictly inferior to its exact-supply
repair. The stated equality of value functions therefore holds on the
whole parameter interval, not merely at the exposing witnesses.

The modification adds no node, arc, or quality coordinate. All lower flow
bounds are zero, capacities are at most one, and only the terminal output
price varies. The positive revenue bonus has `O(n log n)` bits. The
physical graph remains a degree-two path with no pool. This is a response
curve example for a linear blending problem, not a pooling hardness
reduction.

## Quantifier-free degree bound

The graph and epigraph conclusions are both correct for formulas using
only the two free coordinates `(lambda,v)`. Discard zero polynomials.
At a boundary point where every remaining polynomial is nonzero, all
their signs are locally constant, so a Boolean formula in those signs
cannot define that boundary. Thus on every open affine graph segment at
least one polynomial vanishes at each point. The product of the finitely
many polynomials vanishes on the entire segment. Its restriction to the
supporting line is a univariate polynomial vanishing on an interval,
so the line is a factor. Distinct affine pieces here have distinct slopes
and hence distinct line factors. Total degree summed over the defining
polynomials must consequently be at least `2^n`.

This statement does not prohibit compact circuits, large-degree sparse
representations, auxiliary variables, or efficient pointwise algorithms.
The exact support recurrence already demonstrates efficient pointwise
evaluation.

## Independent exact certificates with the theoretical penalty

[exact_physical_penalty_check.py](../code/parametric_path_lp/exact_physical_penalty_check.py)
uses actual left/right arc variables and the proposed theoretical value
`M=2(2n)^(2n)+1`. It builds active source upper rows, output-capacity
rows, homogeneous upper quality rows, and endpoint nonnegativity rows.
It includes no source lower bounds or lower quality constraints.

For every exposing witness in dimensions two through seven, it checks
all physical inequalities and solves the transposed active-row system
exactly for dual multipliers. Every multiplier is strictly positive;
the active matrix is nonsingular and the primal and dual values agree.
These properties certify a unique global maximizer of the upper-only
physical LP. The full revenue and constant-offset identities are checked
in rational arithmetic as well.

All 252 exact primal/dual certificates passed. Unlike the earlier
moderate-penalty experiments, these checks use the actual theoretical
penalty, with no floating-point conditioning or cancellation issue.
The general proof above establishes the result for every dimension.

## Additional coordinate-projection obstruction

The later Section 7 also passes, with two scope qualifications: the
network contains only its standard physical feasibility constraints,
without an added global objective-threshold row or arbitrary side
constraints; and the contrasting degree-three universality statement
concerns bounded rational systems after the stated coordinate scaling.
Finite-capacity port variables cannot represent an unbounded feasible
set literally.

In a pool-free network of maximum degree two, every source flow bound,
output flow bound, and homogeneous output quality bound involves at
most two arc variables. Arc bounds involve one. Extra attributes and
lower specifications add rows of the same type. Eliminating one variable
by Fourier–Motzkin combines two rows, each of which has at most one
other variable, and therefore preserves this property. Rows not involving
the eliminated variable are retained. Repetition gives an exact finite
two-variables-per-inequality description of every coordinate projection.
It gives no polynomial bound on the number of rows.

The proposed simplex counterexample is valid. There is an especially
direct proof: the point `(1/2,1/2,1/2)` satisfies every inequality with
at most two nonzero coefficients that is valid for the simplex
`x>=0, sum x<=1`. For any chosen two coordinates, its pair of values
extends to a simplex point by setting the third coordinate to zero.
Yet the point itself is outside the simplex. Thus the simplex admits
no two-variable-per-inequality description, even with infinitely many
such valid rows. In particular it cannot be a designated-arc coordinate
projection of the stated degree-two network.

Arbitrary linear images are outside this argument, as are thresholded
feasible sets with a dense objective row. The exponential shadow result
is therefore consistent with the coordinate obstruction. The sufficiency
of degree three and insufficiency of degree two concern this precise
bounded-polytope representation property, not a pooling complexity
classification or a novel general elimination theorem.
