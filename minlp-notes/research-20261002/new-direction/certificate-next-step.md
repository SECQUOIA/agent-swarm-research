# Next step after the arbitrary-optimal-set promise theorem

Date: 2026-10-02. This is a research assessment, not a new global algorithm.
It distinguishes proved local structure, open certificate questions, and
classes that already have convex-relaxation certificates.

The remaining target is an exact rational box-QP algorithm with
`f(p,kappa) poly(I)` work whose global correctness does not trust a supplied
growth constant, even when the optimal set is a continuum. The
[proximal algorithm](proximal-growth-grid.md) and
[exact recovery lemma](proximal-exact-recovery.md) establish the same bound
under a supplied valid growth promise. Their final value and stationarity
checks do not remove that promise.

## What the certificate audit settled

Three distinctions now matter.

- The current corrected coordinate-grid lower bound can need
  `Omega(eps^-1/2)` nodes along a flat optimal projection, even at fixed
  width and conditioning. Listing stationary polytopes also fails: a
  connected fixed-width family has exponentially many flat components.
  These are [representation limits](unknown-growth-certificate-audit.md),
  not hardness of the QP itself.
- Pointwise smooth-function information is insufficient for the desired
  unknown-growth extension. A deterministic algorithm needs
  `Omega(eps^-1/2)` queries on a flat instance of conditioning one because
  an unqueried small negative bump remains admissible. The
  [oracle result](unknown-growth-oracle-barrier.md) does not apply to
  explicitly encoded quadratic coefficients. A successful QP algorithm
  must use their algebraic structure.
- Exact convex quadratic terms and box-bound products can represent all
  components of the obstruction family in linear size. This is a
  [diagonal Lagrangian certificate](flat-direction-certificates.md), not
  a new general exactness theorem. Solving only that certificate class
  would not settle the open target.

The [sparse SDP and SOS prior comparison](../prior-art/regridded-qp-prior.md)
also records existing exact sparse relaxations under restricted diagonal
sign and interface conditions, and finite-convergence results under
additional optimality assumptions. A bounded-growth/treewidth claim must
be separated from those established classes.

The bounded-diagonal-convexification obstruction also has a positive
escape: cell-dependent shifts give logarithmically many slabs while
their magnitudes grow as inverse accuracy. Their encoding lengths stay
logarithmic. Thus a future proof must not quietly impose a bound on those
numerical magnitudes.

## A proved local bridge, and its missing global step

The new lemma in [the certificate note](flat-direction-certificates.md)
provides useful structure beyond an assumed relaxation certificate. Fix an
optimal integer slice, if present. Choose a continuous box face maximal
by inclusion among faces whose relative interiors contain a global
optimizer. Let `J` be its free coordinates and `H_JJ` its free Hessian.
Then

```
2g P_range(H_JJ) <= H_JJ <= p diag(H_JJ) <= p L I.
```

The lower bound follows because nearby optima cannot leave that maximal
face; within it they are exactly the feasible part of an affine kernel.
The upper bound follows by coloring the Hessian graph with at most `p`
colors and applying Cauchy--Schwarz to its PSD square root. Consequently
the nonzero spectrum of each such optimal-face patch has condition number
at most `p*kappa/2`. Its flat kernel can remain represented exactly.

This is a local statement. It supplies neither the face nor a global
certificate that no other face has a lower value. In particular, a face
returned by the snapping recovery lemma need not be maximal. A bag's
lower/free/upper statuses also do not determine its subtree Schur
complement, linear term, or separator value function. Counting only
`3^p` statuses would hide the main cost.

## The scalar-message test is now closed negatively

The proposed test was **scalar-separator Bellman certificates on chains
of triangle blocks**. Consecutive blocks share one articulation variable;
the graph has treewidth two and may have an arbitrarily large feedback
vertex number. This is narrow enough to analyze exact quadratic messages,
while genuinely going beyond the forest recourse used earlier.

This graph class alone is not an unclaimed tractability boundary:
Del Pia--Khajavirad's Corollary 8 already treats block-cactus graphs under
additional positive-diagonal forest, interface-size, and cross-rank
conditions. The target here would allow arbitrary diagonal signs and
unbounded interface rank, with the new quantitative restriction instead
being growth. It must not be described as the first exact treatment of
triangle-block graphs.

Allow a message to be a shared collection of interval-restricted
quadratics, keeping singular affine relations implicit. A proposed
certificate consists of local Bellman inequalities and a root lower
bound matching the recovered candidate. Each inequality, once its input
pieces and validity intervals are specified, is a constant-dimensional
quadratic nonnegativity test. Exact active-face stationary calculations
can verify it without trusting a growth estimate. The certificate remains
valid even if the proposed growth estimate was wrong.

The decisive lemma would be a bound

```
total retained message pieces <= f(kappa) poly(I)
```

for a candidate-guided construction, with an absolute input exponent.
Quadratic growth may help discard irrelevant conditional regions, while
the spectral lemma permits exact treatment of a surviving flat patch.
Neither fact currently proves the displayed bound. Off-optimum
conditional messages need not inherit the full problem's growth constant;
this is the first issue to challenge. A shared expression DAG alone does
not solve it either: its exact evaluation or Bellman checks must not expand
all combinations of pieces.

A subsequent [stable-recurrence counterexample](scalar-message-growth-obstruction.md)
settles the full-message version negatively. On a chain of `m` triangles,
with all diagonal curvatures positive and `kappa<=60`, the terminal message
has `2^m` isolated zeros. Any exact representation by interval-restricted
quadratic pieces needs at least `2^(m-1)` pieces. The
[independent review](scalar-message-growth-review.md) confirms the result.
Its objective is already a sum of nonnegative squares and box products,
so this is not optimization hardness and does not exclude selective or
factorized certificates. It does rule out the proposed full-message
closure lemma, even with fixed conditioning. Work should move to the
next target rather than seek that false bound.

## Current target: sparse algorithms controlled by negative curvature

For continuous box QP, a distinct target is to replace `L/g` by
`max(1,nu/g)`, where `nu=max(0,-lambda_min(H))`, while retaining treewidth
as the structural parameter and allowing arbitrary negative inertia.
This would remove large positive curvature from the sparse algorithm's
conditioning parameter. It connects two tractable limits: convex QP when
`nu=0`, and ordinary finite-state tree DP when all coordinates can be
restricted to endpoints by concavity.

The natural decomposition keeps `H+nu I` exactly convex and discretizes
only the diagonal concavity. Its immediate gap is algorithmic: finite
labels coupled to continuous convex recourse are not ordinary finite
tables. Eliminating the convex variables can destroy sparsity. A proof
must address that interface rather than assuming a convex subproblem
oracle composes through the tree decomposition.

This target is for continuous boxes. The mixed-integer version would
include convex integer QP at `nu=0` and needs a separate tractability
assumption. The current negative-inertia theorem is complementary: it
controls the number of negative directions, while this proposed sparse
target would allow that number to grow with the instance.

The [working negative-curvature note](negative-curvature-sparse.md) now
records two useful ingredients: growth in the exact convex-part metric,
and a Moreau envelope with curvature/growth ratio `O(1+nu/g)`. It also
separates the easy proximal-convergence regime `nu<2g` from the general
target. Neither metric change currently preserves the bounded-width
finite-state representation needed for the claimed sparse complexity.

## Review and targeted checks

The [spectral review](flat-face-spectral-review.md) independently checks
the local lemma and the role of maximality. The individual linked notes
record their formula checks and scope limitations.

The command
`python3 -B research-20261002/new-direction/check_nonconvex_certificate_barrier.py`
passed 6,561 exact growth identities and 400 arbitrary-grid witnesses.
The scoped `git diff --check` on the four certificate/quotient notes also
passed. These checks do not establish a compact selective certificate or a
new global algorithm. No project-wide verification or CI inspection was
performed.
