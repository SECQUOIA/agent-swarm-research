# Exact convexification of quadratic indicators on trees: exploration

Date: 2026-09-25. Status: the compact-formulation question remains unresolved.
The investigation proves a transfer from scalar moment incompatibility to
strict original-epigraph gaps, gives rational uniformly conditioned families
failing every subsetwise compatibility order, and proves small LP lifts for
all bounded faces of a star hull. Publication priority is unestablished.

## The question and its significance

For a positive definite matrix `Q`, consider

```
E_Q = {(x,z,t): z in {0,1}^N, x_i(1-z_i)=0, t >= x^T Q x},
H_Q = cl conv(E_Q).
```

Does every tree-supported `Q` admit an exact SOCP or SDP extended formulation
whose size is polynomial in `N`, uniformly over the number of leaves? The
first unresolved case examined here is a star with an unrestricted number
of leaves. No answer is established in this investigation.

Such a formulation could supply an exact reusable relaxation for sparse
quadratic indicator terms when other application constraints are present.
Exact optimization of the unconstrained tree primitive is already
polynomial, so a new optimization algorithm alone would not resolve the
formulation question. Practical value would still require a numerically
usable representation and evidence that its strength justifies its cost
inside constrained applications.

## Strongest relevant results examined

- Choi, Fattahi, Han, Gómez, and Lozano,
  [*Convexification of Mixed-Integer Quadratic Optimization via Decision Diagrams*,
  arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1), Section 7.2 and
  Corollary 1: an exact SOCP lift has size `O(N^(k+1))` when the support tree,
  rooted as in the construction, has `k` leaves. This is a fixed-leaf theorem.
  Its subsequent paragraph explicitly observes exponential size for stars
  and distinguishes polynomial optimization on arbitrary trees. The abstract
  does not justify a uniform polynomial bound for all trees.
- Bhathena, Fattahi, Gómez, and Küçükyavuz,
  [*A parametric approach for solving convex quadratic optimization with
  indicators over trees*](https://link.springer.com/article/10.1007/s10107-025-02222-3):
  the unconstrained tree problem has an `O(N^2)` algorithm. Its local
  full text was examined, including its parametric setup and comparison with
  Stieltjes methods. An objective-dependent dynamic program does not itself
  provide one compact conic lift valid for every linear objective.
- Wei, Atamtürk, Gómez, and Küçükyavuz,
  [*On the convex hull of convex quadratic optimization problems with
  indicators*](https://arxiv.org/abs/2201.00387): the standard representation
  uses the convex hull of embedded principal inverses, followed by a PSD
  epigraph constraint. The inverse-mixture identity used below is established
  theory, not a new representation.
- Liu, Atamtürk, Gómez, and Küçükyavuz,
  [*Polyhedral analysis of quadratic optimization problems with Stieltjes
  matrices and indicators*](https://link.springer.com/article/10.1007/s10107-025-02272-7):
  their tractable relaxation and optimization conclusions have sign
  qualifications; their polyhedral work does not supply the missing arbitrary
  signed-variable star hull. The introduction and the distinction between
  the full inverse polytope and its monotone closures were checked.
- Bluhm and Nechita,
  [*Joint measurability of quantum effects and the matrix diamond*,
  arXiv:1807.01508v3](https://arxiv.org/html/1807.01508), Sections 3 and 5:
  simultaneous PSD binary marginals are an established compatibility problem.
  After normalizing the common moment matrix, the scalar second-moment
  gluing problem below is its real `2 x 2` version. The quantum terminology
  and Boolean PSD-refinement formulation are prior concepts.

The first four papers were also available in `literature/papers/`. Searches
included exact star/tree quadratic-indicator hull phrases, Stieltjes hull
sign qualifications, scalar second-moment compatibility, real-qubit joint
measurability, and the matrix diamond. The papers above were inspected
rather than relying on snippets. No search result establishes originality
by its absence; equivalent formulation and face results may exist under
other terminology.

## What the existing inverse-polytope lower bound does not prove

The repository's [earlier star investigation](../notes/research-20260922-frontier-scout.md)
embeds a correlation-polytope face in the entire inverse-principal polytope
for a uniformly conditioned star. The hard coordinates include all
leaf-to-leaf inverse entries. The original epigraph projects those variables
out. A lower bound on that auxiliary polytope therefore does not transfer to
`H_Q` without an additional argument.

The present work strengthens the warning in a different direction:
[the star-face note](../notes/research-20260925-star-epigraph-faces.md)
proves small LP lifts for all bounded faces. First, faces exposed by a linear objective with positive
coefficient on `t` are analyzed. For `n` leaves, these exposed faces are convex hulls of at most
`2n+2` affine cubes, each of dimension at most `n`, and have `O(n^2)` LP
extended formulations. The proof eliminates the leaves with the center
fixed. Each leaf changes activity at at most two scalar thresholds; between
thresholds the reduced function is strictly convex. A global minimizing
center value can therefore occur at most once in each of `2n+1` intervals.
Root inactivity contributes one more cube. Every bounded face is contained
in a positive-`t` exposed face, so it inherits the same asymptotic bound.

This does not give a lift for the whole curved hull: both the thresholds and
the relevant affine cubes depend on the exposing objective. It does rule
out the straightforward idea that one of these faces already contains a
large correlation polytope. The accompanying note records the exact scope,
closure argument, independent review, and targeted checks.

## A natural local conic construction fails after projection

Write a positive definite star as

```
Q = [[a, b^T], [b, diag(d)]],
d_i > 0, gamma = a - sum_i b_i^2/d_i > 0.
```

Fix the center indicator to one. In a convex-combination representation let
`X` be the center value, `Z_i` the leaf indicator, and `Y_i` the leaf value.
At prescribed first moments `x_0 = E X`, `y_i = E Y_i`, and `z_i = E Z_i`,
put `v = E X^2`, `s_i = E X Z_i`, and `r_i = E X^2 Z_i`.
Completing the square and minimizing over `Y_i` gives exactly

```
a v + sum_i [d_i (y_i + (b_i/d_i)s_i)^2/z_i - (b_i^2/d_i) r_i].
```

The usual closed-perspective convention applies when `z_i=0`.
One may hope to combine leafwise hulls by imposing

```
M = [[1,x_0],[x_0,v]],
M_i = [[z_i,s_i],[s_i,r_i]],
0 <= M_i <= M                       (PSD order).
```

These small PSD constraints admit inconsistent center laws. More strongly,
the inconsistency can decrease the objective in the original variables:

| Matrix and target | Local relaxation certificate | Exact original hull value |
| --- | --- | --- |
| `Q=[[3,1,1],[1,1,0],[1,0,1]]`, `x=(0,1,0)`, `z=(1,1/2,1/2)` | Individual consistency has optimum `3/2` | `1+1/sqrt(3)` |
| `Q=[[4,1,1,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]`, `x=(0,-1,1,0)`, `z=(1,1/4,1/4,1/4)` | Even all leaf-pair consistency constraints admit `359/64` | `96/17` |

In the second row, `359/64` is a feasible relaxation value, not a claim about
its optimum. Its exact gap from the hull is `41/1088`. Both Hessians are
positive definite by the displayed Schur-complement criterion. The first
example is also a path, so it cannot be a lower bound on general compact
lifts: known path lifts are exact.

The [moment-gluing note](tree-indicator-moment-gluing.md) gives the moment
matrices, PSD certificates, hull calculations, and precise relaxation
definitions. Separate fresh reviews check the
[individual case](tree-indicator-moment-gap-review.md) and
[pairwise case](tree-indicator-pair-gap-review.md).

These examples establish that one- and two-leaf second-moment consistency
are insufficient, including after the original epigraph projection. They do
not establish a lower bound for arbitrary SOCP/SDP formulations. The next
section gives a precise arbitrary-order extension for one specified class
of subsetwise compatibility relaxations.

## A general transfer and an explicit arbitrary-order family

The [moment-gluing note](tree-indicator-moment-gluing.md) proves a general
transfer theorem. Fix center mean and strictly interior indicator marginals.
If a scalar second-moment tuple lies outside the full joint compatibility
cone but satisfies a chosen subsetwise compatibility relaxation, then some
positive definite star quadratic and some original leaf means expose a
strict relaxation gap at those original variables, after possibly
complementing leaf indicators.

The proof is constructive from a separating affine functional. Variance
recession directions constrain its second-moment coefficients. Complementing
indicators gives these coefficients the signs needed for a star quadratic.
A small nonnegative coercive perturbation makes the Schur complement
strictly positive. Finally, choosing leaf means makes the eliminated
quadratic objective equal the separating functional plus squares that vanish
at the incompatible point. Thus the mismatch survives projection to the
original epigraph. An [independent adversarial review](tree-indicator-projection-transfer-review.md)
checks closedness, separation, sign changes, the perturbation, and passage
to the closed original hull.

The [uniformly conditioned family](star-uniform-condition-subset-gaps.md) then proves the
following: for every `k >= 1`, a positive definite star with `k+1` leaves
has a strict original-epigraph gap even when every group of at most `k`
leaves admits a joint PSD second-moment refinement. The group refinements
share the center matrix `M` and each singleton matrix `M_i`. They are **not**
required to agree on higher-order pattern matrices on their intersections.
This distinction is essential: the theorem is not a lower bound for every
fixed-degree moment/SOS hierarchy.

The proof uses equally spaced planar binary effects. The compatibility of
each proper subfamily follows from a self-contained planar zonotope
argument and reproduces the established Specker construction of
[Andrejic and Kunjwal](https://arxiv.org/abs/2003.00785), Corollary 8.
A homogeneous matrix inequality remains valid when the total center second
moment varies; this is what permits the direct epigraph-gap proof. The
explicit margin is positive, but decreases with dimension, and the Hessians
become poorly conditioned. Uniform conditioning or a fixed relative gap is
not proved.

The potential addition is the restricted positive-definite star objective
realization and its precise relaxation consequence. Generic incompatibility
witnesses and their conversion to operational objective gaps are already
established, including
[Carmeli, Heinosaari, and Toigo](https://arxiv.org/abs/1812.02985).
The [novelty assessment](tree-indicator-novelty-assessment.md) compares these
claims and treats priority as unresolved.

## Why common moments are a substantive issue

A simultaneous center law would give one PSD matrix `G_S` for every leaf
activity pattern, with

```
sum_S G_S = M,
sum_(S containing i) G_S = M_i.
```

Conversely these equations describe the closure of the joint scalar moment
cone. Positive-mass `2 x 2` PSD blocks have finite two-atom realizations;
zero-mass variance blocks require a limiting interpretation. With `M`
positive definite, normalizing by `M^(-1/2)` gives joint measurability of
binary real-qubit effects. Merely requiring every `M_i` to lie between zero
and `M` keeps only the individual conditions; pairwise refinements still
need not share a common refinement.

This identifies a specific loss of information in a tempting formulation.
It also identifies an existing literature that must be checked before
claiming any general hierarchy obstruction. The exact star objective uses
a restricted combination of these moments. An obstruction for the full
moment cone need not survive that projection; the two explicit examples
above prove that survival directly.

## Assessment and remaining research

A compact exact star formulation would be consequential, but the present
investigation has not found one. Nor has it found an unconditional lower
bound for the original hull. The general transfer and arbitrary-order example go beyond the two small
counterexamples, but their significance and originality require comparison
with established incompatibility witnesses and optimization relaxations.
They prevent three incorrect shortcuts: transferring auxiliary inverse
polytope lower bounds through a projection, treating objective-specific
parametric descriptions as one conic lift, and identifying matching first
two moments with a common center law.

The clearest unresolved opportunities are:

1. Find a representation retaining precisely the compatibility information
   relevant to the star objective, without describing the full inverse or
   moment polytope.
2. Prove a genuine conic extension lower bound for the curved epigraph hull,
   using more than its exposed-face geometry.
3. Determine what remains true for stronger hierarchies that identify
   higher-order pattern marginals across overlapping groups. The present
   proof does not establish their nonexactness. Quantitative order-versus-
   accuracy bounds are being developed separately.
4. Understand whether a bounded number of center-value atoms can be encoded
   convexly without a coefficient-dependent ordering or exponential
   disjunction. A small optimal support for each objective is insufficient
   by itself.

## Verification record

Only targeted checks were run. The face work records
`python code/check_star_epigraph_faces.py` (77 cases and 3232 support checks).
The moment notes and reviews record exact SymPy/Fraction calculations and
support-pattern certificates. A temporary CVXPY search using CLARABEL found
candidate pairwise gaps; its numerical values were used only for discovery.
The reported rational pairwise point and hull value have independent exact
certificates. These methods establish the specified algebraic identities,
finite PSD checks, and proved examples; they do not establish originality
or a complexity theorem. No project-wide verification or CI inspection was
performed.
