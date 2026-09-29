# Convex relaxation complexity from local curvature, and its limits

Date: 2026-09-28. Status: proved and independently audited; see the
[review record](branching-atlas-review.md). The
[bounded primary-source audit](branching-curvature-prior.md) is complete.
No publication-priority claim is made.

## Question and scope

For a quadratic objective with `k` negative eigenvalues, subdividing only
its negative eigenspace gives `O(epsilon^(-k/2))` convex relaxations. The
question here is whether that exponent survives for smooth objectives
whose negative eigenspaces vary with position.

It does survive if there are at least `n-k` strictly positive Hessian
eigenvalues everywhere on a compact domain. It can fail almost maximally
if that positivity condition is replaced by at most `k` negative
eigenvalues: the [disjoint-well construction](branching-degeneracy-barrier.md)
has at most one negative eigenvalue but requires almost
`epsilon^(-n/2)` convex epigraph pieces.

The positive theorem counts convex subproblems. It does not bound the
work to find a valid curvature cover or solve each subproblem. Its
constant can depend badly on the objective, dimension, domain, and
positive spectral gap. This is not a dimension-free computational result.

## Definitions

Let `D` be a compact convex subset of `R^n` with nonempty interior, and
let `f` be `C^2` on an open neighborhood of `D`. Define

```
E_f = {(x,t): x in D, t >= f(x)}.
```

Write `N_f(epsilon)` for the least number of convex sets `C_1,...,C_N`
whose union `R` satisfies

```
E_f subset R subset {(x,t): x in D, t >= f(x)-epsilon}.
```

Arbitrary convex sets and continuous lifts are allowed: projection
preserves convexity, so allowing a lift for each piece does not change
the definition. We impose no representation-size or arithmetic model.

## Curvature cover theorem

**Theorem 1.** Suppose `1 <= k < n` and every `H(x)=nabla^2 f(x)`,
`x in D`, has at least `n-k` strictly positive eigenvalues. Then

```
N_f(epsilon) = O_(f,D)(epsilon^(-k/2)).
```

The same conclusion holds for `k=n` without any spectral assumption.
If in addition an interior point of `D` has `k` strictly negative
Hessian eigenvalues, then

```
N_f(epsilon) = Theta_(f,D)(epsilon^(-k/2)).
```

When `k=0`, the Hessian assumption implies convexity and `N_f=1`.

### Local rank-k regularization

Fix `x_0 in D`. Choose an orthonormal basis `v_1,...,v_k` for the
eigenspace spanned by the `k` smallest eigenvalues of `H(x_0)`, and put
`P=sum_i v_i v_i^T`. Let `mu>0` be the smallest of the remaining
`n-k` eigenvalues, and choose `M>=0` with `H(x_0)>=-M I`. Then, for
`tau=M+mu`,

```
H(x_0)+tau P >= mu I.
```

By continuity, this remains positive definite, with lower bound
`mu I/2`, on a sufficiently small open ball about `x_0`. Choose a
smaller closed ball `B_0` inside that neighborhood. Its intersection
`D_0=D intersect B_0` is convex. On `D_0`,

```
g_0(x)=f(x)+(tau/2) sum_i (v_i^T x)^2
```

is convex. Compactness supplies finitely many such closed balls whose
interiors cover `D`. We obtain convex compact sets `D_j`, each supplied
with a rank-k quadratic regularizer, and `D=union_j D_j`.

This argument does not require the negative eigenspaces to form a
globally trivial vector bundle or to be constant. Each chart chooses
its own fixed affine branching coordinates.

For `k=n`, use a single chart and choose `tau>0` with `H(x)+tau I>=0`
on all of `D`, which exists by compactness and continuity.

### Convex relaxation on projected cells

In chart `j`, subdivide the bounded range of each scalar coordinate
`y_i=v_i^T x` into intervals of length at most `h_j`. Intersect `D_j`
with each resulting projected box. These intersections are convex;
empty intersections can be discarded. For one cell with bounds
`l_i<=y_i<=u_i`, set

```
f_lower(x)=f(x)+(tau_j/2) sum_i (y_i-l_i)(y_i-u_i).
```

Its Hessian is `H(x)+tau_j P_j`, so it is convex. The elementary
quadratic chord bound gives, throughout the cell,

```
0 <= f(x)-f_lower(x)
  <= (tau_j/8) sum_i (u_i-l_i)^2
  <= tau_j k h_j^2/8.
```

Choose `h_j=sqrt(8 epsilon/(tau_j k))`. Each projected coordinate
requires `O_(f,D)(epsilon^(-1/2))` intervals, hence each chart requires
`O_(f,D)(epsilon^(-k/2))` cells. The epigraph of `f_lower` over every
cell is one admissible convex piece. There are finitely many charts,
independent of `epsilon`, proving the upper bound.

The cover need not be a disjoint partition. If a literal branching
implementation is desired, choose small axis-aligned closed boxes in
place of balls, refine once to a common finite box partition, and
assign each box to one containing curvature neighborhood. Subsequent
cuts subdivide its `k` local affine coordinates. Boundary overlap does
not affect validity or the count.

### Matching lower bound

At the interior point with `k` negative eigenvalues, choose an
orthonormal matrix `T` spanning a strictly negative subspace. On a
small cube `Q=[-rho,rho]^k`, continuity gives

```
g(s)=f(x_0+Ts),    nabla^2 g(s) <= -m I,    m>0.
```

For graph points `(x_0+Ts,g(s))` and `(x_0+Tt,g(t))` belonging to
one convex relaxation piece, their midpoint belongs to the piece.
Consequently,

```
epsilon >= g((s+t)/2)-(g(s)+g(t))/2 >= m ||s-t||^2/8.
```

Thus the parameters of graph points covered by each piece have
diameter at most `sqrt(8 epsilon/m)`. Their closures preserve the
diameter bound and cover `Q`. Enclosing each closed set in a box
with side at most that diameter and comparing volumes gives

```
N_f(epsilon) >= (2 rho)^k (m/(8 epsilon))^(k/2).
```

No measurability assumption on the original pieces is needed. This
completes the theorem.

## An example requiring changing branching directions

On `D=[0,1] x [0,2 pi]`, let

```
f(x,y)=exp(x) cos(y).
H(x,y)=exp(x) [[cos(y),-sin(y)],[-sin(y),-cos(y)]].
```

The eigenvalues are `+exp(x)` and `-exp(x)`, so Theorem 1 gives
`N_f(epsilon)=Theta(epsilon^(-1/2))`.

There is no single rank-one positive semidefinite quadratic
regularizer that makes `f` convex on the whole box. Indeed, any
rank-one positive semidefinite matrix has a nonzero kernel vector
`w=(cos theta,sin theta)`. Along that vector,

```
w^T H(x,y) w = exp(x) cos(y+2 theta),
```

which is negative somewhere in the box, whereas the regularizer
contributes zero. Adding independent positive quadratic terms
extends this example to higher dimensions, but the example itself
does not demonstrate a hard optimization instance: its global
minimum can be found directly.

## What this enables and what it does not establish

For minimizing `f` over a compact convex feasible set `D`, solve the
convex relaxation on every cell. Every relaxation minimizer is
feasible for the original problem, because only the objective was
relaxed. Evaluating `f` at those minimizers yields an incumbent whose
value differs from the smallest relaxation bound by at most
`epsilon`. Thus the theorem yields a value certificate using
`O(epsilon^(-k/2))` convex minimizations, subject to exact solves or
separately accounted numerical tolerances.

For a feasible set `D intersect (Z^p x R^(n-p))`, the same objective error
bound applies to each mixed-integer convex subproblem, but those
subproblems have their own combinatorial cost. For nonconvex
constraint rows, separate common-curvature hypotheses are needed;
the maximum negative index of the individual rows is insufficient
to justify a shared k-dimensional branching space.

The theorem supplies a reason to investigate branching directions
derived from locally validated Hessian information. Practical value
requires cheap certified curvature bounds, manageable cover size,
efficient convex subproblem representations, and evidence that these
costs are competitive. None is established here.

## Literature and repository comparison

- Vavasis, *Approximation algorithms for indefinite quadratic
  programming*, Mathematical Programming 57 (1992), 279–311,
  [DOI](https://doi.org/10.1007/BF01581085), is the classical fixed
  negative-eigenspace antecedent. The present pass examined the open
  [1991 precursor chapter](https://api.pageplace.de/preview/DT0400.9781400862528_A23705221/preview-9781400862528_A23705221.pdf)
  and the detailed modern reproduction below; the 1992 full text was
  not yet independently obtained.
- Zhang and Xia, *On the relaxation complexity of nonconvex quadratic
  global optimization*, Communications in Optimization Theory 2024,
  paper 19, [open paper](https://cot.mathres.org/issues/COT202419.pdf).
  Sections 2–3 reproduce negative-coordinate subdivision and bound
  the number of convex relaxations for an indefinite quadratic
  objective over bounded convex quadratic constraints, using a
  relative value-range error. Theorem 1 here instead concerns an
  additive-error epigraph cover for nonquadratic C² functions, with
  a finite family of local coordinate systems.
- Nohra, Raghunathan, and Sahinidis, *Spectral relaxations and branching
  strategies for global optimization of mixed-integer quadratic
  programs*, [arXiv:2010.04822](https://arxiv.org/abs/2010.04822).
  The introduction and Section 4 of the
  [full text](https://arxiv.org/pdf/2010.04822) were examined. They use
  eigenvalue-based convex quadratic perturbations and choose binary
  variables by estimating how fixing them improves the smallest
  eigenvalue. This is distinct from locally changing affine spatial
  coordinates for a nonquadratic objective.
- Anstreicher's eigenvector branching is also used in
  *A novel algorithm for a broad class of nonconvex optimization
  problems*, [open manuscript](https://optimization-online.org/wp-content/uploads/2023/06/RPT-BB.pdf),
  Sections 1 and 4. It branches using a lifted matrix discrepancy;
  the present construction uses local Hessian convexification.
  This distinction does not by itself establish priority.
- The repository's
  [quadratic epigraph precision theorem](../../results/quadratic-inertia-one-sided-integer-complexity.md)
  proves a matching half-negative-inertia coefficient for minimum
  integer dimension under arbitrary convex lifts. The local
  negative-slice lower bound here is the same curvature mechanism.
  The new question is the smooth, spatially varying upper bound and
  the failure without a strict positive complement. The repository's
  [constant Hessian-rank graph theorem](../../results/constant-hessian-rank-smooth-precision.md)
  concerns two-sided graph approximation, a different object.
- Pawlaschyk, *On some classes of q-plurisubharmonic functions and
  q-pseudoconcave sets*, 2015 dissertation,
  [primary text](https://d-nb.info/1081429941/34), Theorem 2.4.3,
  identifies the smooth pointwise inertia condition with real
  q-convexity, and the strict positive-complement condition here with
  strict real k-convexity. Theorem 2.6.7 gives approximation by
  q-convex functions with corners, defined through local finite
  maxima of smooth q-convex functions. These are not convex epigraph
  covers, and the examined statement provides no accuracy-dependent
  cover count. This alternate terminology was checked during the
  independent review and is relevant to further priority searches.

The completed [primary-source comparison](branching-curvature-prior.md)
also checks generalized nondiagonal αBB underestimation, Pawlaschyk's
2025 formulation of real q-convexity, Bungart's earlier corners
approximation, and convex-cover terminology. Quadratic convexification
and negative-coordinate subdivision are established methods. The
retained result is their local spectral application and finite-cover
argument for a fixed smooth function. The short proof and uncontrolled
cover constant limit the significance claim; publication priority
remains unestablished.

## Verification record

The arguments above were derived by hand. A targeted `python` heredoc
using SymPy checked the rotating example's Hessian trace and
determinant, its directional quadratic form, and both radial-well
eigenvalue identities in the companion construction. Every symbolic
assertion passed. These checks establish algebraic identities, not the
covering or asymptotic claims. No project-wide check was run.
The [independent adversarial review](branching-atlas-review.md) found the
theorem sound. Its requests to clarify the mixed-integer feasible set
and require `tau>0` in the full-dimensional edge case were incorporated.
The bounded literature audit is complete and its access limitations are
recorded separately. It does not establish publication priority.
