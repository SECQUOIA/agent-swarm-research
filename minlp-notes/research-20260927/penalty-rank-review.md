# Independent review of the joint-rank penalty bound

Date: 2026-09-27. Reviewer: `rank_adversary`.

I reviewed [the research note](penalty-frontier.md), including the revised
Section 4, and found no unresolved proof gap under its stated boxed rational
encoding, convex native quadratics, feasibility, and refined Slater
assumptions. The global error bound also justifies its extension to indefinite
quadratic objectives. This is a mathematical review, not a formal verification
or a claim that priority has been established.

## Projection and algebraic bounds

Positive semidefiniteness gives
`ker(sum_i Q_i) = intersection_i ker Q_i`. A rational kernel basis and
rational complement give the claimed coordinate split with polynomial
coefficient bit length. An orthonormal spectral basis should not be substituted
without accounting for its potentially irrational coordinates.

For a transformed system `A v + g(u,t) <= 0`, the finite-dimensional Farkas
alternative gives precisely the inequalities `lambda^T g(u,t) <= 0` for
extreme rays of `{lambda >= 0 : A^T lambda = 0}`. This cone is pointed.
An extreme ray's positive support has a one-dimensional kernel and contains
at most `rank(A)+1` indices. Rational minors therefore give polynomial-bit
generators; at most `2^M` supports are possible for `M` input rows. Each
projected coefficient is a sum of polynomially many polynomial-bit products.
Nonnegative aggregation preserves convexity. This proves projection
closedness directly, without invoking closedness of arbitrary convex
projections.

It is sufficient to clear denominators separately in each projected row.
Alternatively, clear the polynomial-size original system first and use
integer ray generators. A common denominator across exponentially many
separately normalized rays need not have polynomial bit length.

The current note retains `(u,t,w)` with `tw=1` and `w>=0`. This uses `r+2`
variables and degree two, and is valid. The residual reciprocal set is bounded,
so the containing-radius theorem applies. The Slater reciprocal set can be
unbounded; only the meeting-radius theorem is required. This distinction is
essential. The exponential projected row count enters the radius exponent
only logarithmically. These facts give both reciprocal bounds of size
`2^{N^{O(1)} 2^{O(r)}}`.

An alternative substitutes `t=1/w` directly, using `w>=1/R` when `t<=R`.
It has `r+1` variables and degree three, with the same asymptotic bound.
The note's extra-variable formulation is simpler and needs no correction.

## Error bound and nonconvex objectives

The revised affine-repair proof is correct, including degenerate affine rows.
At the Euclidean projection `y` of `x in P` onto
`E=P intersect {Ax=d}`, write `h=x-y` in the cone of active affine normals
and signed equality normals. Choose linearly independent generators and a
nonsingular coordinate minor. Cramer's rule bounds their coefficient sum by
`H ||h||_2`, for uniform `H<=2^{N^{O(1)}}`. Every active affine term has
nonpositive inner product with `h`, because `x in P`. Thus

```
||h||_2^2 <= lambda^T(Ax-d)
           <= H ||h||_2 ||Ax-d||_infinity.
```

No constraint qualification is needed for this polyhedral normal-cone formula.
Zero distance is treated separately before cancellation.

For the nonlinear repair, `x`, `y`, and the margin point all lie in the
continuous box. Its gradient bound therefore gives `g_i(y)<=GH e`.
With `eta=GH e`, the stated choice `alpha=eta/(sigma+eta)` cancels the
convex upper bound on every nonlinear inequality exactly. It yields
`||w-x||_2 <= H(1+GD/sigma)e`. Interpolation stays in one fixed integer
fiber; no fractional integer variables are introduced.

On an equality-infeasible fiber, the diameter of the full input box divided
by the positive residual lower bound controls distance to any fixed global
feasible point. This proves the asserted global mixed-integer distance bound.
For a full-box Lipschitz objective, nearest-point comparison then proves
minimizer-set exactness when `rho>LC`. Indefinite quadratic objectives have
the required polynomial-bit full-box Lipschitz bound. Equality `rho=LC`
can permit infeasible ties, so strictness matters.

The child reviewer `projection_check` independently checked the projection
and determinant arguments. A fresh child reviewer `error_bound_adversary`
independently attacked the repair and nonconvex-objective extension and
confirmed the argument after being supplied the rank-dependent margin bound.
That reviewer did not separately verify the Basu--Roy margin theorem.

There is a further local consequence within an equality-feasible continuous
fiber: following the segment from an infeasible point to its repair strictly
decreases the penalized objective when `rho>L_f K`. Thus infeasible local
minima are excluded there. A further fresh reviewer independently checked
this observation. It must not be asserted globally across all integer fibers:
a compact equality-infeasible fiber itself has a penalized minimum and is
isolated from other fibers. The research note currently makes no such claim.

## Verification actually performed

I read the current note using
`sed -n '1,360p' research-20260927/penalty-frontier.md`, and inspected the
existing fixed-count, general-upper-bound, and chain-construction proofs.
The following exact targeted command was executed successfully. It checks
displayed algebra, not the general geometric or real-algebraic theorems.

```bash
python - <<'PY'
import sympy as s
sigma,L,H,d,D=s.symbols('sigma L H d D', positive=True)
alpha=L*H*d/(sigma+L*H*d)
assert s.simplify((1-alpha)*L*H*d-alpha*sigma)==0
assert s.simplify(H*d+alpha*D-H*d*(1+L*D/sigma)) == -D*H**2*L**2*d**2/(sigma*(H*L*d+sigma))
u,w,a,b,c,beta=s.symbols('u w a b c beta')
q=a*u**2+b*u+c
rec=s.expand(w*(q+beta/w))
assert s.Poly(rec,u,w).total_degree()==3
print('PASS: Slater interpolation cancellation, distance bound remainder, and cubic reciprocal degree.')
PY
```

No Lean build, project-wide verification, or CI inspection was performed.

## Sources and significance

- I read Theorems 3 and 4 in the local text of the
  [Basu--Roy final author manuscript](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
  `research-20260925/publication-sources/basu-roy-2010-final.txt`, and the
  repository's earlier source review. The final statements show the
  weak-sign scope and logarithmic row-count dependence used here. I did not
  reprove the external radius theorem or re-audit every explicit constant;
  only an asymptotic bound is claimed in the current note.
- [Andersen, *On formulating quadratic functions in optimization models*](https://docs.mosek.com/whitepapers/qmodel.pdf)
  (2013, revised 2023), Sections 2--3, was examined as a primary precedent
  for exploiting low-rank quadratic factors. It does not establish the
  penalty encoding theorem under review.
- I examined only the abstract and bibliographic information for
  [Zhao and Fan, *On subspace properties of the quadratically constrained quadratic program*](https://www.aimsciences.org/article/doi/10.3934/jimo.2017010)
  (2017). Its exact relationship to this result remains to be checked from
  the full proof; the abstract is insufficient to rule out overlap.
- Searches for common-nullspace, low-rank convex quadratic feasibility,
  and nonlinear-dimension formulations did not establish priority. Common
  kernel reduction, Farkas projection, polyhedral error bounds, and exact
  penalties from error bounds are established mechanisms.

The paper's existing chain has joint native rank exactly `n-1`, since
only the coordinates `a_1,...,a_{n-1}` occur quadratically. Its lower bound
of `2^n` penalty bits therefore verifies the claimed exponential order in
joint rank. Individual rank one does not provide the same protection.

The defensible advance is the joint-rank-sensitive encoding and geometric
error bound, including arbitrary quadratic objectives, together with its
matching exponential rank dependence. The current conservative assessment
is appropriate: this is a useful structural refinement, not yet an established
substantial standalone contribution, efficient repair procedure, or solver
speedup. Independent positive reviews provide evidence, not a correctness
guarantee or a novelty certificate.

## Addendum: restriction to supplied native affine equalities

I subsequently checked only the added affine-restriction paragraph using
`rg -n -A 35 -B 8 "Affine-restriction variant|r_E" research-20260927/penalty-frontier.md`.
The variant is valid. Rational elimination of supplied native equalities
`Ex+Dz=e` gives a polynomial-bit nullspace basis and an affine rational
particular solution `x_0(z)` on every consistent integer slice. Choose the
basis `W` with identity rows at the free coordinates, so those coordinates
inherit original box bounds. Substitution preserves total degree at most
two and uniform polynomial coefficient bits. The restricted Hessians are
`W^T Q_i W`; rows with zero restricted Hessian are affine and correctly
require no strict Slater slack.

Two clarifications were sent to the author. First, an arbitrary rational
spanning matrix `W`, possibly with redundant columns, need not itself have
the free-coordinate normalization or a polynomial-bit representation.
Specify the basis produced by rational elimination; the joint rank is
independent of that basis choice. Second, moving the feasible-fiber repair
back to original coordinates multiplies its constant by at most
`||W||_2 <= 2^{N^{O(1)}}`, which does not change the claimed bound. The
infeasible-fiber step can still use the original full-box diameter. The
zero-dimensional restricted space causes no difficulty.

It is essential to restrict only by native equalities: using the relaxed
linking equalities would remove the points whose penalty is being analyzed.
The paragraph states this distinction correctly. No further computation or
external-source claim was needed for this linear-algebraic specialization.

The author incorporated both clarifications. I reread the corrected paragraph
with `sed -n '79,105p' research-20260927/penalty-frontier.md` and accept it
as written; no unresolved issue remains in this variant.
