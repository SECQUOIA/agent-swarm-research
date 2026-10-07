# Independent review of the mixed sparse noise argument

Date: 2026-10-02. Status: completed independent proof review of
[the full mixed author draft](sparse-bag-cell-smoothed-miqp.md).
The conditional counts, margin probabilities, exact closure, and bit
accounting check out. This review concerns a mixed product box and
independent noise in every remaining linear coefficient. No tests,
external searches, or CI checks were run for this mixed extension.

## 1. Mixed grids and the conditional count

First round integer bounds inward, reject an empty domain, and remove
fixed coordinates. Choose an integer power of two `s` at least every
remaining width and at least one, and put `h_j=s 2^(-j)`. While
`h_j>=1`, the integer grid step is the integer `h_j`, anchored at
the integer lower bound and clipped at the integer upper bound.
At `h_j<1`, integer cells are singletons at integer points.

The transition from spacing one to singletons preserves the mixed
physical domain: an integer cell with endpoints `z,z+1` contains only
those two feasible integer points. It creates at most two children.
Later refinement leaves a singleton unchanged. Continuous intervals
and coarse integer intervals also split into at most two children.
Thus every bag cell has at most `2^|B|` children throughout.

Mean-preserving rounding of an integer point in a coarse interval
uses integer endpoints, so it remains feasible. At fine levels each
integer point is fixed. Independent coordinate rounding therefore has
the same safe objective error `E_j=nLh_j^2/8`. The variance contribution
from fine integer coordinates is actually zero; retaining the displayed
upper bound is harmless. The consistent witness and pruning arguments
of the continuous theorem consequently retain every original optimizer.

For the noise count, condition on noise outside a bag and minimize over
the original outside mixed box. Extend the resulting value function to
real values of the bag's integer coordinates by the same minimization
formula. The outside feasible set is fixed, and the quadratic is defined
at those real arguments. After subtracting `L t^2/2`, every coordinate
restriction is an infimum of concave functions. This proves the needed
semiconcavity even though actual bag feasibility requires integer values.

Use comparison step `a_i=h_j` for continuous coordinates and
`a_i=max(1,h_j)` for integer coordinates. Both neighbors of a regular
integer node remain integers. An epsilon-near-optimal node gives a noise
interval of length at most `L a_i+2epsilon/a_i`. Substituting
`epsilon=2E_j` gives

```
L a_i+4E_j/a_i <= (1+n/2)L a_i.
```

For continuous and coarse integer coordinates this is equality in the
upper estimate. For fine integers it follows from `h_j^2<=1` and
`a_i=1`. There are at most three exceptional nodes and at most
`w_i/a_i` regular nodes. Finite-grid interval probabilities therefore
give the conditional product bound

```
product_(i in B) [3+(1+n/2)Lw_i/(2sigma)+w_i/(N a_i)].
```

The necessary comparison intervals depend only on the deterministic
bag tuple and outside noise, so the in-bag probabilities multiply.
The original mixed domain, rather than a random restricted domain,
must be used in this argument.

Since `a_i>=h_j`, `w_i<=s`, and `N>=2^J`, every atomic term through
level `J` is at most one. The resulting bag bound is exactly

```
H_B=product_(i in B) [4+(1+n/2)Lw_i/(2sigma)].
```

Corner incidence, child generation, and sparse separator-key DP then
give the same constant-to-the-bag-size overhead as in the continuous
case. There is no product of adjacent random table sizes.

## 2. Mixed growth and continuous margin events

Let `n_c` be the number of continuous coordinates and put

```
F=3^n_c product_(i integer)(w_i+1),
B=F,       C_tail=8(F+1)^2,       K=max(1,n_c F),
rho=1/(4B),
g_0=rho sigma/(2W),               tau=rho sigma/(2K).
```

The supplied finite-grid growth theorem counts continuous faces
separately at each integer assignment, so `F` is the correct face
bound. With `N>=4n C_tail/rho`, its bad-growth probability is at most
`rho`. On the complementary event, point growth is at least `g_0`
and the complete mixed optimizer is unique.

For a fixed integer assignment and a continuous face with nonsingular
free Hessian, free stationarity depends only on noise in its free
continuous coordinates. An active continuous gradient has coefficient
exactly one on its own noise coordinate. The other noise coefficients
are independent of that coordinate, including all integer coefficients.
The event that this gradient has magnitude at most `tau` therefore has
probability at most `tau/sigma+1/N`.

There are at most `n_c F` such face-coordinate pairs. Choosing
`N>=2K/rho` bounds their union by `rho`. For a unique mixed optimizer,
the free continuous Hessian of its smallest continuous face in its
integer slice is positive definite. Thus the true active continuous
gradients are among the candidates counted. When `n_c=0`, the margin
event is empty; using the safe `K=1` only enlarges the schedule.

## 3. Integer identification and exact closure

On the good event, each retained cell has a feasible full witness whose
distance from the unique optimizer is at most
`h_j sqrt(nL/g_0)/2`. Cell widths add at most `h_j` coordinatewise;
fine integer cells add zero. Thus the safe radius is

```
r_j<=A h_j,       A=2+nL/g_0.
```

Impose `h_J<=1/(4A)`, as in the author draft. Since `A>=2`, this
already gives `h_J<1` and `A h_J<=1/4`. Every retained integer
projection is then a singleton at an integer within distance `1/4`
of the optimal integer value. It must equal that value. Consequently
all integer coordinate hulls are singletons.

Independently of the good event, a singleton integer hull fixes that
coordinate in every original optimizer, by the pruning invariant.
After all integer hulls are singletons, the continuous interval-gradient
tests may force original continuous endpoints by box KKT conditions.
If the remaining continuous principal Hessian is PSD, exact convex QP
solution on this fixed integer slice and original continuous face
returns the original global optimum. These are sound deterministic
tests; no growth estimate is accepted as a certificate.

For `M=max(1,max_i sum_k |H_ik|)`, the additional condition
`h_J<=tau/(2MA)` makes gradient variation on the retained hull at most
`tau/2`. All active continuous coordinates are therefore identified
on the good event. Their removal leaves the positive-definite free
continuous Hessian, so exact closure succeeds by `J`. An empty
continuous free set is included.

## 4. Noise encoding, fallback, and scope

All integer widths are integers after preprocessing, and

```
log F=n_c log 3+sum_(i integer) log(w_i+1)
```

has polynomial binary-input length. So do `log(1/g_0)`,
`log(1/tau)`, and the least terminal level satisfying the two
conditions above. Choosing a power of two

```
N>=max{2,2^J,4n C_tail/rho,2K/rho}
```

therefore uses polynomially many bits. This choice depends only on
the base input; it does not depend on sampled coefficient denominators
or a subsequent rational reconstruction precision.

Enumerating all integer assignments and all continuous faces costs
`F` times a polynomial in the base and sampled encoding lengths.
A minimum-dimensional optimal continuous face at an optimal integer
assignment has positive-definite free Hessian, or is a vertex. Hence
the stationary-candidate fallback is exact on every draw, including
ties. Its invocation probability is at most `2rho=1/(2F)`, making
its expected contribution polynomial without resampling.

The expected search work retains the numerical factors `Lw_i/sigma`.
Arbitrarily many integer coordinates are permitted, but this is not a
claim of polynomial work in binary width length alone. The factor
`(1+n/2)^|B|` likewise prevents an FPT conclusion in bag size with a
dimension-free noise ratio. The result concerns the chosen fine finite
noise law and a product mixed box, not arbitrary atomic laws or
coupled mixed constraints.

## 5. Full-draft checks of singleton handling and arithmetic

At fine integer levels the conceptual complete coordinate grid has
`w_i+1` nodes, with at most `w_i` regular nodes and two endpoint
exceptions. A distinct integer singleton has one corner and one child
at every subsequent level. At the transition, shared endpoints may
produce duplicate singleton descriptions; treating each whitelist as
a set removes them. Even if such descriptions are retained, their
multiplicity is at most two per integer coordinate and arises only
once, so the constant-to-the-bag-size bounds still apply. The draft's
corner-row deduplication independently prevents duplicate DP states.

The actual search creates singleton children only from retained unit
intervals. It does not enumerate the complete integer grid when the
spacing reaches one. The complete grid is used solely to bound the
expected number of retained states. This distinction makes the
binary-width complexity statement valid.

For arithmetic, an integer label has at most the input endpoint bit
length, and a continuous grid coordinate has polynomial bit length
in `I+j`. The sampled noise adds polynomially many bits since
`log N` is polynomial in `I`. Each DP value is a minimum of sums of
original factor values; there are only polynomially many factors.
Using a common denominator, or reducing rational sums exactly, gives
polynomial message bit length. The logarithm of even a full bag table
is bounded by the sum of the coordinate grid-count logarithms, hence
is polynomial in `I+J`. Sorting sparse lists therefore adds only a
polynomial factor, without requiring their full deterministic size
to be polynomial. Integer substitution in the fallback or convex
closure also preserves polynomial coefficient bit length.

The draft correctly requires every integer coordinate to be fixed
before invoking continuous convex closure. PSD of a continuous block
alone would not justify minimizing over unresolved integer choices.
No such relaxation is used in the stated algorithm.
