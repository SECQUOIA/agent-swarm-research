# Independent audit of rational positive-polar and primal spanner oracles

Date: 2026-09-05. Reviewer: `quadratic_weighted_precision`.
Status: PASS after a full independent read of
[the supporting oracle](rational-polar-spanner-oracle.md).

The generic projected spanner computation has explicit uniform conditioning.
The image-entry bound `W`, the determinant lower bound `Delta_0`, and the
cofactor estimate bound every basis inverse throughout the algorithm. The
stated `L` is a valid common bound on the l1 norms of every signed objective
`V B^(-1)e_i`; its conservative factors do not omit a rank or dimension term.
All these bounds have polynomial binary encoding even when rank grows.

The fixed-grid feasibility repair is exact. Weak-optimization error `n delta`
and coordinate snapping contribute at most `2n delta` distance to the body.
The convex combination with the known interior center places the returned
point inside the body, as shown by the explicit inner-ball witness. Condition
(C) bounds the total objective loss, including weak optimization, snapping,
and repair, by `1/4`. The same rational grid and repair weight apply to every
call. Thus every returned vector has a common polynomial-bit denominator and
uniformly bounded numerator; including the seed denominators covers every
possible basis. This resolves the potential recursive bit-growth issue.

An exchange only occurs when the returned representation coefficient has
magnitude greater than two, so each exchange more than doubles the determinant.
The determinant upper bound `r! W^r` then gives polynomially many exchanges.
When all signed objectives fail to produce an exchange, the true extrema are
at most `2+1/4`, which establishes the claimed spanner factor. Exact-feasible
returned points, rather than approximate points outside the body, are used as
basis vectors. Exact inverses and subsequent objectives retain uniformly
polynomial encoding because of the common output denominator.

The support optimizer on the original strongly separated body also repairs
feasibility exactly: scaling the weak output by `rho/(rho+eta)` uses the
origin-centered inner ball. Its objective loss is bounded by the displayed
expression, so the pair of certified bounds in (F) is valid. Arbitrarily
small requested support error costs polynomial precision bits, not an inverse
error iteration count, under the stated GLS import.

The positive-polar weak separator is sound in each branch. Coordinate
constraints `0<=lambda_i<=1/rho` are valid. Inside that box, the certified
feasible support point either supplies an exact valid polar separating
inequality, or the support upper bound proves that `lambda/(1+tau)` is
feasible and within the requested distance. The normal is nonzero in the
separation branch because its pairing with the query exceeds one. Rescaling
both the normal and its right-hand side meets the weak-oracle normalization
without changing validity. No exact boundary-membership decision or strong
polar oracle is assumed.

The positive center `a*1`, radius `a/2`, and outer radius `1/rho+ma` are valid
for the positive polar. The chosen dyadic bound gives ample support margin
and positivity throughout the inner ball. The axis seeds `2a e_j` are exactly
feasible, and independent rows of `V` give a nonzero projected determinant.
The projected family need not contain a ball at zero: optimization is performed
in the full-dimensional original positive-polar body, with the seed only
certifying image rank.

The effective primal body has the stated inner/outer radii under the linear
map and its rational left inverse. Strong separation pulls back through `V`;
a violated normal cannot vanish because zero is feasible. Coordinate-axis
seeds lie in its inner ball. The same generic theorem thus applies directly,
and central symmetry gives the claimed contained crosspolytope and outer
parallelotope.

The main application supplies an outer coordinate radius; replacing it by
`mR` gives the Euclidean radius required here with polynomial encoding. The
weak-separation/weak-optimization theorem and known-ball assumptions match the
previously reviewed GLS interface. No mathematical or bit-complexity defect
was found. Priority and primary-source attribution remain separate from this
proof audit; the note correctly credits the classical spanner mechanism.
