# Independent review of the sparse bag-cell noise argument

Date: 2026-10-02. Scope: proof review of
[the complete author draft](sparse-bag-cell-smoothed-qp.md), with emphasis
on conditional counting, the finite perturbation law, strict margins,
and exact completion. A small exact-arithmetic counting diagnostic is
recorded below. No external searches or CI checks were run.

**Conclusion.** The expected exact-solver bound is supported by the
argument. The algorithm is correct on every draw; probability controls
its work. The stated dependence is polynomial for fixed bag size and
polynomially bounded numerical ratios, and is not FPT in bag size.
The author applied the two wording clarifications identified below.

## 1. Conditional counting and clipped grids

Conditioning on all noise outside a fixed bag leaves its noise
coordinates independent. The value function in the draft's (10) uses
the original complementary box, which is essential: it is independent
of all in-bag coefficients. Subtracting `L v_i^2/2` gives an infimum
of concave coordinate restrictions, so its upper coordinate curvature
is at most `L`.

For a fixed deterministic tuple `v`, an epsilon-near-optimal value
implies, at a regular node in coordinate `i`,

```
[V_B(v)-V_B(v+h e_i)-epsilon]/h <= gamma_i
 <= [V_B(v-h e_i)-V_B(v)+epsilon]/h.
```

The interval has width at most `Lh+2epsilon/h`. Its endpoints depend
only on `v` and the outside noise; all other in-bag linear terms cancel.
Thus the joint conditional probability is bounded by a product of
one-dimensional interval probabilities. Adaptively chosen witnesses
cause no independence problem because the count sums over the entire
deterministic bag grid.

On the clipped physical grid, the left endpoint, last full-step node,
and clipped upper endpoint are the only possible exceptions. Coincident
nodes are counted only once. There are at most three exceptional nodes
and at most `w_i/h` regular nodes. The clipping creates neither extra
neighbors nor extra incidence: a node belongs to at most `2^|B|` bag
cells, and halving the step creates at most `2^|B|` children per cell.

The rounding and min-marginal argument supplies an actual full feasible
grid witness for every retained cell, with gap at most
`2E_j=nLh_j^2/4`. Consequently `epsilon=2E_j` gives interval width
`(1+n/2)Lh_j`. For uniform noise on `N` equally spaced points of
`[-sigma,sigma]`, an interval of length `a` has probability at most
`a/(2sigma)+1/N`. This proves the draft's product bound (13), including
its constants. It also gives the stated continuous-density variant.

The sparse DP is consistent with this count: corner rows use exact
separator keys, and min-marginals are minima over complete consistent
assignments. The rounding proof retains any specified containing bag
cell, even where different bags meet on grid boundaries. Thus neither
the witness nor the pruning step assumes independent local choices.

## 2. The finite noise law and margin probabilities

The atomic term is controlled through the deterministic terminal level:
`h_j=s 2^(-j)`, `w_i<=s`, and `N>=2^J` imply
`w_i/(N h_j)<=1` for every processed level. A fixed arbitrary coarse
noise grid would not give a level-independent count. The draft properly
chooses its law before sampling, from a level cap depending only on the
base data.

With `B=3^n`, `rho=1/(4B)`, and
`C_tail=8(B+1)^2`, the cited finite-grid growth theorem gives

```
Pr{g_*<g_0} <= rho/2 + 2n C_tail/N <= rho,
g_0=rho sigma/(2W).
```

For a face with nonsingular free Hessian, its free stationary vector
depends only on noise in its free coordinates. An active gradient is
therefore `gamma_i` plus an affine function independent of `gamma_i`.
The conditional probability that its magnitude is at most `tau` is
at most `tau/sigma+1/N`. Counting all face-coordinate pairs, including
infeasible candidates, only enlarges the bad event; `K=nB` is valid.
The choices `tau=rho sigma/(2K)` and `N>=2K/rho` make the union bound
at most `rho`.

Positive point growth implies uniqueness. At a unique optimizer, the
free Hessian of its smallest box face is positive definite: second-order
optimality gives PSD, and a null direction would yield nearby distinct
optima. The optimizer's active gradients are therefore among the
hyperplanes just counted. The combined bad-event probability is at
most `2rho=1/(2B)`.

## 3. Unconditional exact closure and its stopping level

The coordinate hull contains every original optimizer by the pruning
invariant. If a gradient component is strictly positive throughout
that hull, first-order optimality on the original box forces every
optimizer to its original lower endpoint; the negative case forces
its original upper endpoint. These equations are valid without a
growth estimate and without a feasible path through retained cells.

The resulting original box face contains every optimizer. If its free
principal Hessian is PSD, exact convex box-QP solution gives the
original global optimum. This is a valid certificate on all draws.
In particular, the algorithm does not accept a guessed growth modulus
or a likely strict-complementarity event as a certificate.

On the good event, each retained cell's witness is within
`h_j sqrt(nL/g_0)/2` of the unique optimizer. Adding the cell width
bounds every retained projection, and hence the coordinate hull, by

```
r_j=h_j[1+sqrt(nL/g_0)/2] <= (2+nL/g_0)h_j
```

in each coordinate. With `M>=max_i sum_k |H_ik|`, gradient variation
is at most `M r_j`. The terminal condition in (17) makes this at most
`tau/2`, so every active coordinate is correctly forced. The remaining
free Hessian is positive definite, and closure succeeds. An empty free
set is covered by the vacuous PSD test.

The fallback also covers tied and degenerate draws. A global optimum
on a minimum-dimensional optimal face has positive-definite free
Hessian, since a null direction could be followed to a smaller optimal
face. Thus enumerating all `3^n` faces, including vertices, and taking
the best feasible stationary candidate is exact.

## 4. Bit work and scope

The logarithms of `1/g_0`, `1/tau`, and the required `N` have polynomial
base-input length. Therefore `J`, grid-coordinate bit lengths, and
sampled coefficient bit lengths are polynomially bounded. Choosing
`J` before `N` avoids a circular requirement involving the sampled
denominators and a rational reconstruction precision.

The fallback costs `B` times a polynomial and is invoked with
probability at most `1/(2B)`. Its expected contribution is polynomial.
For the search, bounded tree degree and separator-key lookup avoid
products of random adjacent table sizes. Logarithmic sorting overhead
is bounded by the logarithm of the full deterministic grid size, hence
by a polynomial in the base input and level. Standard exact rational
arithmetic, PSD testing, and convex QP solution then give the stated
expected bit bound.

The factor `(1+n/2)^|B|` remains. The result is an expected
width-dependent polynomial bound, not FPT in `p` with a dimension-free
noise parameter. It concerns the specified fine finite perturbation
law and continuous box variables. It does not establish the
deterministic sparse `nu/g` target or an integer analogue.

## 5. Wording clarifications and targeted diagnostic

- The draft now states that `L` is rational and included in the input
  length. This makes the binary-length assertions unambiguous.
- The draft now defines `Q_j` by intersecting coordinate projection
  hulls and states that it contains every optimizer. That intersection
  need not contain every retained cell projection, and the proof does
  not require it to do so.

The targeted command

```
python research-20261002/new-direction/check_sparse_bag_noise.py
```

passed. The [diagnostic](check_sparse_bag_noise.py) uses exact fractions
for a two-coordinate bag and one private variable. Minimizing over the
private variable gives a minimum of two quadratic branches, with a
downward kink. It exhaustively checks all 64 in-bag noise draws on an
eight-point grid, two conditioned outside coefficients, and four mesh
levels. The unequal coordinate widths include clipped terminal cells.
All eight cases and 238 tuples satisfy the comparison-rectangle
containment, finite-grid rectangle probability bound, and expected
count bound. The cases include 45 empty comparison intervals. This
diagnostic checks the counting argument independently of the separate
DP checker; it does not replace the proof.

## 6. Checked hardness compatibility calculation

I also checked the calculation in the
[noise-scale hardness note](sparse-smoothed-hardness-sanity.md), using
the reduction equations recorded in the earlier local hardness review.
For `r>=1`, the NO instance with items `2^r,2^r+2` and target `2^r+1`
has a feasible reduction trajectory of value `delta=2^(-2r-4)` and
at least one coordinate equal to one. Compactness and the reduction's
zero-value equivalence imply a strictly positive original optimum.
Conditioning on the noise coefficient of that unit coordinate bounds
the density of `Z=gamma'y` by `1/(2sigma)`. For symmetric finite-grid
noise, the exact identity
`Pr{Z<-delta}=(1-Pr{|Z|<=delta})/2` retains all central and endpoint
atoms. The displayed bound
`1/2-delta/(2sigma)-1/(2N_noise)` for crossing the original NO
threshold follows. This checks threshold instability for that family;
it does not exclude other robust reductions or more elaborate use of
perturbed outputs. No additional test or source search was run for
this algebraic check.
