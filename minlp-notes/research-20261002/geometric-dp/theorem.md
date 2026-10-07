# Certified geometric-grid dynamic programming under quadratic growth

Date: 2026-10-02. Status: core argument independently derived and
adversarially reviewed; prior-art investigation and extension review continue.
Statements below distinguish
the mathematical argument from unestablished originality and practical value.

## Main claim and scope

A mixed-integer box problem with a sparse factorization, bounded upper
coordinate curvature, and global quadratic growth around one minimizer can be
solved to accuracy `eps` by finite-state dynamic programs whose state counts
grow polynomially in `log(1/eps)`. The algorithm needs no minimizer, derivatives,
local solver, or multiplier estimates. A known upper curvature bound is needed;
the quadratic-growth constant can be unknown. For purely integer boxes the
same method reaches an exact optimum in finitely many stages, with logarithmic
dependence on the domain diameter and explicit dependence on conditioning.

The feasible set is a product of intervals and integer intervals. Arbitrary
nonlinear constraints are **not** covered. All complexity statements first
count exact factor evaluations, comparisons, and arithmetic operations. They
are not unconditional bit-complexity statements for arbitrary real functions.

This develops a different algorithm from the September 29 affine-message
certificate algorithms. It does not prove their branching-tree localization
conjecture. It uses globally shared coordinate grids, which remove copy drift,
and pays a power of a logarithm for product grids in each bag.

## 1. Assumptions and computation model

Let `X = product_i X_i`, where `X_i=[a_i,b_i]` or
`X_i=[a_i,b_i] intersect Z`. Integer endpoints are taken to be integers after
rounding inward; empty domains are rejected and fixed variables eliminated.
There are `n>=1` remaining variables and `s=max_i(b_i-a_i)>0`.

The objective is `F(x)=sum_t f_t(x_Vt)` on a supplied tree decomposition with
bags `V_t` of size at most `p=w+1`, satisfying running intersection. Each
factor is assigned to one bag containing its arguments. Write `N` for the
number of bags; factor-evaluation costs must also be counted if there are
many factors in a bag. Unary terms can be assigned to any containing bag.

Assume an extension of `F` to the continuous box has **upper coordinate
curvature at most `L>0`**: with other coordinates fixed, the function

`t -> F(x_1,...,t,...,x_n) - L t^2/2`

is concave on its interval. This is coordinate semiconcavity. In particular,
`partial_ii F <= L` suffices for a twice differentiable objective. If every
bag function has `M`-Lipschitz gradient and each variable occurs in at most
`k` bags, `L=kM` is valid. Full Hessian positivity, convexity, and smooth
conditional value functions are unnecessary.

Assume **global quadratic growth on the actual mixed domain**:

`F(x)-f* >= c ||x-x*||_2^2` for every `x in X`, with `c>0`.

Here `x*` is the unique global minimizer and `f*=F(x*)`. A boundary minimizer
is permitted. The constants may depend on the instance. In particular,
quadratic growth at an integer optimizer is not implied with the same
constant by strong convexity of a continuous extension. Nearly tied integer
solutions can make `c` arbitrarily small.

The exact-oracle model supplies factor values at grid points and exact
arithmetic/comparisons. Section 8 treats the limits of this model. The case
`L=0` is simpler: separate concavity makes a minimum attainable at a product
of interval endpoints, so one finite-state dynamic program is exact.

## 2. A valid lower bound from any shared coordinate grids

Choose finite grids `G_i subset X_i` containing both endpoints. For a grid
node `v`, let `ell_i(v)` be the largest length of an adjacent grid interval.
For an integer coordinate, ignore adjacent intervals of length one; put
`ell_i(v)=0` if none remain. Set

`d_i(v)=L ell_i(v)^2/8`, `D(y)=sum_i d_i(y_i)`,

`LB=min { F(y)-D(y) : y in product_i G_i }`.

**Lemma 1 (validity).** `LB <= f*`. If `y` minimizes the corrected grid
objective, then

`LB <= f* <= F(y)`, and `F(y)-LB = D(y)`.

**Proof.** For any `x in X`, independently round each coordinate to the two
endpoints of its containing grid interval, with probabilities chosen so
`E Y_i=x_i`. A coordinate already on its grid remains fixed. If the interval
has endpoints `u,v`, its rounding variance is `(x_i-u)(v-x_i)`.

Coordinate semiconcavity gives the one-coordinate inequality

`E F(x with coordinate i rounded) <= F(x)+(L/2) Var(Y_i)`.

Apply this successively to the coordinates. Independence keeps the same
variance at each step, hence

`E F(Y) <= F(x)+(L/2) sum_i Var(Y_i)`.

For a genuinely rounded coordinate with interval length `Delta`, both
endpoints have `ell_i >= Delta`. Thus
`E d_i(Y_i) >= L Delta^2/8 >= (L/2) Var(Y_i)`.
For an integer coordinate, a feasible integer cannot lie strictly inside a
unit interval; ignoring those intervals is therefore valid. For a coordinate
already at a grid point the variance is zero and its penalty is nonnegative.
It follows that `E[F(Y)-D(Y)] <= F(x)`. The minimum of the corrected grid
objective is no larger than this expectation. Take `x=x*`. The remaining
claims follow from feasibility of `y`. QED.

The interpolation inequality and finite-state dynamic programming are
classical ingredients. The proposed contribution is the conditioning-dependent
global algorithm and its accuracy bound, subject to the literature audit.

The corrected grid objective has the same factorization as `F`, plus unary
penalties. Exact min-sum dynamic programming on the supplied decomposition
computes `LB` and a minimizing `y` in

`O((N+number of factors) q^p)` table work,

where `q=max_i |G_i|`, with a factor depending on `p` for index operations.
Shared coordinate values enforce exact separator consistency. Children can
be accumulated one at a time, so arbitrary branching of the tree does not
introduce a product of the numbers of child states.

## 3. Geometric grids centered at a feasible point

Fix `z in X`, `h>0`, and `0<theta<=1/2`. Include `z_i` in each grid and build
outward on both sides, clipping the final step at the domain endpoint.

For a continuous coordinate, at distance `t` from `z_i` take a step
`h+theta t`. Before clipping, the successive distances are

`t_j = h ((1+theta)^j-1)/theta`.

For an integer coordinate, take the integer step

`max{1, floor(h+theta t)}`.

The center is integral on integer coordinates, so all such nodes are feasible.

**Lemma 2 (mesh bound and count).** For every grid node `v`,

`ell_i(v) <= h+theta |v-z_i|`.

For continuous coordinates the number of outward steps on either side is
at most

`1+ceil(log(1+theta s/h)/log(1+theta))`.

For integer coordinates replace the denominator by `log(1+theta/3)` and
`h` inside the numerator by `H=max{h,1}`. Consequently, for `h=s 2^{-j}`,
every coordinate has at most `C theta^{-1}(j+1)` grid nodes for a universal
constant `C`.

**Proof.** Any adjacent interval with nonzero penalty has length no larger
than `h+theta t`, where `t` is the distance of its nearer endpoint to the
center. For an integer interval of length at least two this follows because
its untruncated step is `floor(h+theta t)`. Clipping cannot increase it.
Both endpoints have distance at least `t`, which proves the mesh bound.

The continuous count follows from the explicit distance formula. For the
integer count, each nonfinal step satisfies

`max{1,floor(h+theta t)} >= (H+theta t)/3`.

If `h>=1`, the stronger factor `1/2` follows from `floor(u)>=u/2` for
`u>=1`. If `h<1` and `theta t<2`, a step of at least one suffices. If
`theta t>=2`, use `floor(h+theta t)>=theta t/2 >=(1+theta t)/3`.
Therefore `t+H/theta` grows by at least `1+theta/3` at every nonfinal step.
The counts and the final asymptotic estimate follow. QED.

The full coordinate grid is retained. It is not a trust region and does not
discard remote global minimizers. Its coarse remote intervals have larger
corrections, which the quadratic-growth argument controls.

## 4. One global contraction step

Form these grids around `z`, minimize `F-D` exactly, and call a minimizer `y`.
Put `Eold=||z-x*||^2` and `Enew=||y-x*||^2`.

**Lemma 3.** If

`theta^2 <= min{1/4, c/(8L)}`,

then

`Enew <= (4L/(15c)) n h^2 + Eold/15`.                     (1)

**Proof.** The mesh bound gives

`D(y) <= (L/8) sum_i (h+theta |y_i-z_i|)^2`
`     <= (L/4)[n h^2+theta^2 ||y-z||^2]`
`     <= L n h^2/4 + (L theta^2/2)(Enew+Eold)`.

By Lemma 1 and quadratic growth,
`c Enew <= F(y)-f* <= D(y)`. Move the `Enew` term to the left. Since
`L theta^2/2 <= c/16`, the coefficient on the left is at least `15c/16`.
This gives (1). QED.

This is an aggregate squared-distance estimate. No bound on every bag's
individual error, decay of graph sensitivities, or path structure is used.

## 5. Algorithm and accuracy theorem

Start from any feasible center `z_-1`. At stage `j=0,1,...`, put
`h_j=s 2^{-j}`, build the grids around `z_(j-1)`, and compute an exact
minimizer `z_j` of their corrected objective. Retain the lower bound and
feasible value; stop when their difference is at most `eps`.

**Theorem 4 (known growth constant).** Choose `theta` as in Lemma 3 and set

`B=max{1,4L/(11c)}`.

For every stage,

`||z_j-x*||^2 <= B n h_j^2`,

`F(z_j)-LB_j = D_j(z_j) <= (7L/8) n h_j^2`.              (2)

Thus it suffices to reach

`J=max{0,ceil( (1/2) log2(7 L n s^2/(8 eps)) )}`.

Total table work through stage `J` is at most

`C^p (N+number of factors) theta^{-p} (J+1)^(p+1)`.       (3)

In particular the accuracy dependence is polynomial in `log(1/eps)` for
fixed width and conditioning. There are no nonlinear local optimization
subproblems in this oracle model.

**Proof.** The initial center has squared distance at most `n s^2`.
For stage zero, (1) gives
`E_0 <= (4L/(15c)+1/15)n s^2 <= B n s^2`.
For later stages, induction and `h_(j-1)=2h_j` give

`E_j <= [4L/(15c)+4B/15] n h_j^2 <= B n h_j^2`.

For the gap, `E_(j-1)<=4B n h_j^2` also holds at stage zero using the
initial bound. The proof of Lemma 3 gives

`D_j <= (L/4)[1+10 theta^2 B] n h_j^2`.

If `B=1`, then `theta^2 B<=1/4`. Otherwise
`theta^2 B <= (c/(8L))(4L/(11c))=1/22`. Hence in all cases
`theta^2 B<=1/4`, yielding `D_j<=7L n h_j^2/8`.
Lemma 2 bounds each coordinate grid by `C theta^-1(j+1)` states. Sum the
per-stage finite-state DP bounds. QED.

Compared with the earlier path algorithm, (3) has a higher logarithmic
power but applies to arbitrary supplied tree decompositions and boundary
minima. With `L=kM` and `theta` chosen within a constant factor of the largest
permitted value, its conditioning factor is of order
`max{1,sqrt(kM/c)}^p`, before factor evaluation costs. This comparison is
about different algorithms and certificate representations, not dominance
of one particular implementation.

## 6. The growth constant need not be supplied

The lower bound is valid for every `theta`; only the complexity guarantee
uses `c`. Compute `J` from the known `L,n,s,eps` in Theorem 4. Try
`theta_m=2^(-m-1)`, `m=0,1,...`. For each trial run stages `0,...,J`, starting
from a fixed feasible center. Stop whenever a verified gap is at most `eps`.

**Corollary 5.** If global quadratic growth holds for some unknown `c>0`,
this procedure terminates. If `m*` is the first trial meeting Lemma 3's
threshold, total table work is bounded by the form (3) with
`theta=theta_m*`, times a universal geometric-series constant.

**Proof.** Trial `m*` must succeed by Theorem 4. For earlier trials validity
does not depend on the failed threshold. The per-trial upper work bounds are
proportional to `theta_m^-p=2^((m+1)p)` with the same `J`; their sum is at
most `1/(1-2^-p)` times the last such bound. QED.

This is a guarantee under an unknown assumption, not a procedure for proving
the assumption. A valid final lower-bound certificate does not require
trusting a guessed growth constant.

In fact, epsilon termination needs no quadratic-growth assumption. At the
fixed final stage, the mesh estimate alone gives
`D(y)<=Ln(h_J+theta s)^2/8`, regardless of the center. Our choice of `J`
ensures `Ln h_J^2/8<=eps/7`, including the case `J=0`. For sufficiently
small `theta`, the displayed bound is less than `eps`. Thus the search over
`theta` is a globally convergent approximation method on the stated
semiconcave product domains. Quadratic growth supplies the much faster
conditioning-dependent bound; without it the search may approach a dense
uniform grid.

## 7. Purely integer optimization can stop exactly

**Corollary 6 (known-constant exact stopping).** Suppose every coordinate
is integer. With `theta` satisfying Lemma 3, once `B n h_j^2<1`, the stage
minimizer equals `x*`. At the next stage it again equals `x*`; if that
stage's `h` is less than two, its correction vanishes and
`LB=F(x*)=f*` exactly.

**Proof.** Two distinct integer vectors have squared distance at least one,
so the first claim follows from (2). It applies again at the next stage.
The next grids are centered at `x*`. Every existing interval immediately
adjacent to the center then has length one, since its first step is
`max{1,floor(h)}` with `h<2`. Integer unit intervals contribute zero
correction. Lemma 1 gives the exact equality. QED.

Since `B>=1` and `n>=1`, the condition `B n h_j^2<1` already implies
`h_j<1`, hence the next-stage requirement automatically holds. The operation
bound has the form (3) with
`J=O(1+log_+(s sqrt(Bn)))`. This is an exact-oracle result; exact comparison
of arbitrary transcendental objective values can be a separate obstruction.

For unknown `c`, [the extensions, Section 2](extensions.md), give an explicit
exact algorithm: try `theta_m=2^(-m-1)`, refine each trial until
`n h_j^2<=theta_m^2`, and take one additional stage. Stop when the certified
gap is zero. The first admissible trial succeeds, and preceding trial costs
sum geometrically. This needs neither a supplied growth constant nor an
objective-gap bound.

## 8. What the result establishes and does not establish

- **Proved by the candidate argument:** valid global bounds from finite
  tables; contraction under the stated global growth and curvature bounds;
  polylogarithmic accuracy dependence at fixed treewidth and conditioning;
  exact stopping on pure integer boxes with suitable parameters.
- **Potential solver capability:** a component solver for sparse box
  optimization that certifies a solution without a full-dimensional spatial
  branch-and-bound tree. It could also serve as a bound for an outer MINLP
  method when dropping constraints leaves a subproblem of this form.
- **Not yet demonstrated:** competitive performance, useful constants on
  real instances, adaptive reuse of tables, certified floating-point
  evaluation, or a general constrained-MINLP algorithm.
- **Material limitations:** global quadratic growth around one point can be
  very weak when minima are nearly tied. A fixed-width decomposition must be
  supplied. The method enumerates product grids in each bag, giving a power
  of the logarithm that grows with width. The curvature bound must be valid
  on the entire continuous extension, including between integer points.
- **Arithmetic:** rational-polynomial factors and rational choices of grid
  parameters permit rational evaluation.
  [The extensions](extensions.md) provide an explicit bit bound and a
  finite-precision table-error budget; their independent review is in
  progress. The polynomial bit bound counts degree numerically, and does not
  hold for arbitrarily large binary-encoded exponents. Arbitrary real factor
  oracles do not supply these arithmetic guarantees.
- **Certificates:** a checker can verify factor tables, unary corrections,
  and the finite DP recurrence. It must also verify or be supplied a valid
  coordinate-curvature bound. It does not need the growth constant to check
  the resulting lower bound.

## 9. Prior work and verification record

The closest local predecessors are
[decomposition certificates](../../research-20260929/theory-decomposition/decomposition-certificates.md),
[the path algorithm](../../research-20260929/theory-decomposition/adaptive-matching.md),
and [the earlier literature audit](../../research-20260929/literature/decomposition-bb-prior.md).
The present construction replaces affine separator functions by shared finite
coordinate grids and explicit second-order rounding corrections. Whether the
full conditioned complexity guarantee already appears under adaptive dynamic
programming, continuous graphical models, or related terminology is under
investigation. No priority claim follows from this draft.

The [independent derivation](independent-derivation.md) and
[adversarial proof review](../reviews/geometric-dp-adversary.md) support the
core theorem. The review checked its constants, mixed-integer rounding,
large-domain grid count, boundary scope, and exact integer stopping. Its
counterexamples show why the continuous-extension curvature bound and an
appropriate mesh parameter are necessary.

The [extensions](extensions.md) also cover fixed-feasible-set private
recourse and fully enumerated finite-state variables. For the latter,
quadratic growth is needed only in the gridded coordinates; discrete optimal
states can be nonunique. The recourse cost and feasibility reconstruction
remain explicit obligations, and parameter-dependent private feasible sets
do not automatically preserve the curvature assumption.

The [targeted checks](checks/README.txt) record the commands actually run:

- `python3 research-20261002/geometric-dp/checks/exact_checks.py` passed:
  six analytic families, 42 stages, 142,348 exhaustive corrected-grid
  assignments, and 294 independent rounding laws, with exact fractions.
- `python3 research-20261002/geometric-dp/checks/grid_geometry_checks.py`
  passed: 250 grids, 1,883 vertices, and 36 parameter cases.
- `python3 research-20261002/geometric-dp/checks/float_scale.py` ran a timing
  prototype on 16, 64, and 128 variables. Its ordinary floating-point bounds
  are explicitly not certificates.

The large integer test obtains an exact certificate with 143 retained values
per coordinate out of 20,001 feasible integers. These tests check finite
examples with known analytic optima; they do not prove the general theorem,
test arbitrary treewidth, establish novelty, or show superiority to a general
solver. No Lean verification or project-wide/CI verification is claimed.
