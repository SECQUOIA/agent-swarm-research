# Independent adversarial review of the RHS-smoothed penalty bound

Date: 2026-09-25. Scope: the theorem supplied by the author, the completed
[geometry note](smoothed-penalty-geometry.md), and the proposed optimized
penalty lower-tail examples. The main note was still being drafted when
this review began; the completed main draft was subsequently inspected.
This review independently reconstructed the deterministic argument, checked
the probability constants, delegated a second audit of the geometry, and
tested exact finite examples.

**Assessment.** The proposed theorem is correct with the assumptions and
qualifications below. No proof-breaking gap was found. It is a quantitative
smoothed exact-penalty result, not a polynomial-time optimization result.
The novelty assessment remains provisional; the underlying distance-to-
ill-posedness method and convex-boundary probability bounds have strong
precedents.

## Deterministic proof reconstructed

Let the finitely many nonempty native sets `X_z` be compact and convex.
Let `r_z` be affine and `f_z` continuous and convex on `X_z`, with a common
bound `L<=f_z<=U`. Put `M=U-L` and `C_z=r_z(X_z)`. All boundaries are ambient
boundaries. Assume

```
min_z dist_inf(b,boundary C_z) > d > 0.
```

If `b in C_z`, it is an interior point and `b+[-d,d]^m subset C_z`.
For native `x`, write `r=||r_z(x)-b||inf`. If `r>0`, choose `x' in X_z`
with image

```
r_z(x') = b - d(r_z(x)-b)/r.
```

The point `y=(d*x+r*x')/(d+r)` is feasible. With `V_z(b)` the slice value,
convexity gives

```
V_z(b) <= f_z(y) <= [d*f_z(x)+r*U]/(d+r),
f_z(x) >= V_z(b) - (U-V_z(b))*r/d
          >= V_z(b) - M*r/d.
```

This also holds for `r=0`. If `b outside C_z`, compactness implies its
closest image point is on the boundary, so `r>d` for every native point.
Let `p` be the finite global feasible optimum. Then `p<=U`, and for
`rho=M/d` every native point in an infeasible slice has penalized cost
at least `L+M*r/d>=U>=p`. For `M>0`, the first inequality is strict.
Together with the feasible-slice estimate this proves exact optimal value.
For `rho>M/d`, any native point with nonzero residual has penalized cost
strictly above `p`. The minimizer sets therefore agree.

The degenerate case `M=0` is harmless: `rho=0` gives the correct value,
but can leave infeasible minimizers; every `rho>0` excludes them. The
strict-penalty conclusion must not be weakened to equality without an
extra argument.

The norm and boundary distance must agree. In particular, separation in
Euclidean distance by `d` does not supply an infinity ball of radius `d`.
Use infinity distance with infinity norm, or Euclidean distance with
Euclidean norm. The same geometric probability estimate is available for
either choice. A norm dominating the infinity norm also works with
infinity separation.

## Geometry and rational grid

The independent geometry audit agrees with the coordinate-section proof.
For `Q=[-1,1]^m` and `s>d`, the closed boundary tube is contained in

```
(C+sQ) outside (C erosion sQ).
```

Successive coordinate expansions add at most `2s` to every clipped fiber;
successive erosions remove at most `2s`. Summing each of the `m` changes
and dividing by the cube volume gives `2ms/sigma`; letting `s` decrease
to `d` proves the bound `2md/sigma`. The use of `s>d` avoids an incorrect
identity at closed tube endpoints. Lower-dimensional sets, empty erosion
sets, and clipped fibers are covered by this proof.

For `N` centered cell midpoints on each coordinate, independent jitter
of infinity radius `sigma/N` is exactly uniform on the original cube.
The distance function is 1-Lipschitz, giving the single-set estimate

```
Pr[dist_inf(G,boundary C)<=d] <= 2m(d/sigma+1/N).
```

The sets must be fixed independently of the sampled perturbation. With
at most `K` sets, `d=sigma*epsilon/(4mK)` and `N>=4mK/epsilon`, the union
bound is at most `epsilon`. No independence of boundary events is needed.
For an endpoint grid, the jitter is uniform on a slightly enlarged cube;
it must not be described as uniform on the original cube.

These statements use a finite number of random bits if `N` is a power of
two. A claim of polynomial ordinary encoding additionally requires rational
bounds `L,U`, rational `sigma,epsilon,b0`, and polynomial encoding of
`log K` and these quantities. Compactness alone supplies no such encoding
bounds. Even when `K` is exponential, the sufficient penalty has only
`O(log K)` digits contributed by this factor; its numerical magnitude can
still be exponential.

## Feasibility and practical limits

The unconditional event is

```
perturbed problem is infeasible OR the stated penalty is exact.
```

If feasible perturbations have probability `q>0`, the direct conditional
failure bound is `epsilon/q`, capped at one. A perturbation cube inside one
native residual image is a sufficient robust-feasibility anchor. Without
an anchor or another feasibility estimate, the result can be vacuous:
if all residual images are lower-dimensional, a continuously sampled RHS
is almost surely infeasible.

The theorem gives no approximation guarantee for the optimum or solutions
at the original RHS. It also supplies neither an efficient native
optimization oracle nor a polynomial bound on branch-and-bound work.
The common objective range is material. Its computation and its encoding
must be accounted for in an algorithmic application.

## Integration and the local-stability consequence

The completed main draft uses infinity distance and infinity penalty
consistently. Its repair lemma, coefficient `4mKM/(sigma*epsilon)`, grid
resolution, and local stability statement agree with this review.

For completeness, if every boundary distance at `b` exceeds `d`, every
point in `b+[-d/2,d/2]^m` has boundary distance greater than `d/2`.
Membership in each convex residual image cannot change within this smaller
cube without meeting its boundary. Thus the feasible integer assignments
are fixed. Apply the deterministic value estimate at two points `u,v` in
this cube, using a slice optimizer at `v` as the native test point at `u`.
This gives `V_z(v)>=V_z(u)-(2M/d)||v-u||inf`. Reversing `u,v` proves the
slice Lipschitz bound. The minimum over the common nonempty finite set of
feasible slices has the same bound. The uniform exact penalty `2M/d`
follows from the deterministic lemma at each center. No gap was found in
this corollary.

One wording correction was sent to the author: the multiatom sharpness
argument needs `b in (0,1)` outside the atoms to choose an anchor point
with residual of the opposite sign. Its endpoints are null events, so
this does not alter the probability bound. The two-slice exact formula
in the main draft already has the correct open-interval restriction.

## Optimized-multiplier sharpness

Consider one anchor slice with residual image `[0,1]` and objective zero,
and `K-1` singleton slices at `a_j=j/K`, each with objective `-1`.
For `b in (0,1)` outside these atoms, the primal optimum is zero. The
anchor contains residuals of both signs arbitrarily close to zero. For
zero dual gap with a scalar multiplier `lambda`, it therefore requires

```
-rho <= lambda <= rho.
```

An atom at distance `t` then requires `2*rho*t>=1`. This necessity also
follows from a zero-mean convex combination of the atom and an anchor
point on the opposite side, so it remains valid even if the optimized
dual is expressed as a supremum rather than an attained maximum.

For `T>=K`, the `K-1` open intervals of radius `1/(2T)` around the atoms
are disjoint and contained in `[0,1]`. Except for their centers, all their
points have least optimized exact penalty greater than `T`. Thus

```
Pr[rho_star > T] >= (K-1)/T.
```

This independently validates the claimed order in `K/epsilon` for the
one-dimensional continuous-noise model. It does not establish sharpness
of the dimension factor or every finite-grid constant.

A more precise check is possible. Write `t_left` and `t_right` for the
nearest atom distance on each existing side, and set the corresponding
reciprocal to zero if that side has no atom. Then

```
rho_star = (1/t_left + 1/t_right)/2,
lambda = (1/t_right - 1/t_left)/2.
```

These formulas satisfy all atom inequalities and the anchor condition.

For anchor `[-1,1]` and a single cost-`-1` atom at zero,

```
rho_star(b) = 1/(2|b|),     0<|b|<1,
```

attained with `lambda=-rho_star*sign(b)`. At `b=0`, the atom is feasible
and `rho_star=0`. At `b=+1` or `-1`, the anchor has residuals of only one
sign, and a sufficiently large multiplier gives `rho_star=0` even with
zero penalty. These endpoint exceptions have probability zero under
continuous uniform noise. The integral of `1/(2|b|)` diverges, proving
that no finite expected numerical penalty follows from the high-probability
bound. This does not contradict a finite expectation for a logarithmic
magnitude, and a real-valued continuous draw has no ordinary finite
rational encoding without discretization.

## Prior-work comparison and search limits

Two primary sources were examined independently:

- Dunagan, Spielman, and Teng, *Smoothed Analysis of Condition Numbers and
  Complexity Implications for Linear Programming*,
  [author manuscript](https://www.cs.yale.edu/homes/spielman/Research/lpcond.pdf).
  Their Gaussian perturbation analysis controls condition numbers measuring
  inverse distance to ill-posedness and yields complexity consequences for
  linear programming. This establishes the broad conditioning mechanism;
  it is not a finite union of convex native slices with a finite rational
  RHS grid.
- Bürgisser and Amelunxen, *Robust Smoothed Analysis of a Condition Number
  for Linear Programming*, [version 3](https://arxiv.org/pdf/0803.0925v3).
  Theorem 3.3 and Corollary 3.4 give local inner and outer boundary-tube
  estimates for spherical convex sets. Thus a dimension-dependent bound
  for arbitrary convex boundaries has direct prior precedent. The 2008
  version had the title *Uniform Smoothed Analysis of a Condition Number
  for Linear Programming* and different theorem numbering.

Searches used combinations of `smoothed analysis`, `exact penalty`,
`mixed integer`, `RHS perturbation`, `condition number`, and `convex
boundary`. They did not identify an identical combined result, but this
absence is not evidence sufficient to establish novelty. The independent
[geometry note](smoothed-penalty-geometry.md) also compares other relevant
sources. A full contribution claim must additionally compare the exact
penalty and multiplier-size literature; this review does not replace the
separate literature audit.

The elementary convex repair argument and finite-grid coupling should
be presented as tools, not independently important discoveries. The
potential contribution is their precisely scoped smoothed consequence
for mixed-integer convex penalties, together with optimized-multiplier
lower tails and the rational encoding statement.

## Targeted verification

Command actually run:

```
python research-20260925/check_smoothed_penalty_review_second.py
```

Result:

```
PASS: 363 exact piecewise-linear penalty cases; 150 exact box/grid tube cases; 1216 exact optimized-penalty sharpness cases.
```

The checker uses rational arithmetic. It minimizes the tested piecewise
linear penalties over all breakpoints, enumerates every point in tested
finite product grids, checks the optimized multiplier formula on sampled
rational RHS values, and checks the exact interval lengths in the lower
bound. These finite cases test the algebra and constants. They do not
prove the general convex theorem, certify novelty, test a solver, or
formalize the proof in Lean. No project-wide verification or CI inspection
was performed.
