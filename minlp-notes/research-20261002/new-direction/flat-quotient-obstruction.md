# Eliminating one flat direction can destroy every sparse quotient basis

Date: 2026-10-02. Status: a proved representation obstruction, with
independent derivation and exact checks. This is not an optimization
hardness result or a literature-priority claim.

The [proximal approximation theorem](proximal-growth-grid.md) and its
[exact-recovery extension](proximal-exact-recovery.md) handle arbitrary
optimal sets when a valid growth bound is supplied. The remaining
question is whether a recovered stationary face can support a global
certificate independent of that growth bound. A tempting intermediate
step is to quotient out its flat directions, then reuse a bounded-width
box algorithm on the remaining coordinates.

The example below rules out a general width-preservation claim for that
step. It has bag size two, a unit box, one flat direction and conditioning
ratio two. Every auxiliary-free linear quotient has a complete constraint
graph, in every linear basis. A connected nonconvex version has the same
obstruction on its optimal face, with all diagonal curvatures positive.

## 1. A uniformly conditioned star on a unit box

Let `k>=2` be an integer and `m=k^2`. On `[0,1]^(m+1)`, with coordinates
`x,y_1,...,y_m`, define

```
F0(x,y)=sum_(i=1)^m (y_i-x/k)^2.                                  (1)
```

The interaction graph is a star. Bags `{x,y_i}` arranged in any tree
give a valid decomposition of bag size two. Every Hessian diagonal
entry is two, so the upper coordinate curvature bound is `L=2`.
The optimal set is the line segment

```
S0={(t,t/k,...,t/k):0<=t<=1}.                                    (2)
```

For every feasible `(x,y)`, the point `(x,x/k,...,x/k)` belongs to
`S0` and has squared distance exactly `F0(x,y)`. Hence

```
F0(x,y)>=dist((x,y),S0)^2.                                       (3)
```

Thus `g=1` and `kappa=L/g=2` work independently of `m`. All data are
rational with polynomial input length. No aspect-ratio parameter is
hidden in the domains: every original interval is `[0,1]`.

Put `a=(1/k,...,1/k)`, so `||a||=1`. The quadratic matrix of (1) is

```
[ 1   -a^T ]
[ -a    I  ].
```

Its eigenvalues are zero, two, and one on the remaining subspace.
The Hessian therefore has norm four and a one-dimensional kernel
spanned by `(1,a)`. The flat direction is explicitly available.

## 2. The exact quotient polytope has all pairwise facets

Use residual coordinates

```
r_i=y_i-x/k.
```

This map is a linear quotient by precisely the kernel of (1), and the
objective becomes `sum_i r_i^2`. Feasibility means that some scalar
`t=x/k` satisfies

```
0<=t<=1/k,              0<=r_i+t<=1  for every i.
```

Eliminating `t` gives the exact full-dimensional quotient polytope

```
P_k={r: -1/k<=r_i<=1 for every i,
         r_i-r_j<=1 for every ordered pair i!=j}.                 (4)
```

Indeed, the interval of eligible `t` values is nonempty exactly when

```
max(0,max_i(-r_i)) <= min(1/k,min_i(1-r_i)).
```

Comparing each lower endpoint with each upper endpoint gives (4).

Every displayed inequality in (4) is a genuine facet. There are
explicit points at which just that inequality is tight:

- For `r_i=1`, set all other coordinates to `1/2`.
- For `r_i=-1/k`, set all other coordinates to `(k-1)/(2k)`.
- For `r_i-r_j=1`, set `r_i=1-1/(2k)`, `r_j=-1/(2k)`, and every
  other coordinate to `(k-1)/(2k)`.

All remaining inequalities are strict at the respective point. Since
`P_k` is full dimensional, a sufficiently small relative neighborhood
in that supporting hyperplane is contained in the facet. In particular,
its mandatory facet normals include

```
e_i, -e_i, and e_i-e_j for all i!=j.                              (5)
```

In these residual coordinates the objective is separable, but the
constraint graph is the complete graph on `m` coordinates.

## 3. No change of quotient basis removes the clique

For a finite linear inequality description, join two coordinates in
its constraint-interaction graph when they both have nonzero coefficients
in some inequality. The following statement covers every invertible
linear change of quotient coordinates, as well as an added translation.

**Lemma.** In every basis of the quotient space, every exact finite
linear inequality description of `P_k`, without auxiliary variables,
has the complete constraint graph `K_m`.

*Proof.* In a new basis, let `a_i` be the transformed normal corresponding
to `e_i`. The vectors `a_1,...,a_m` are linearly independent, and the
transformed facet normals include `a_i` and `a_i-a_j` for every pair.
Every facet must occur in any exact finite inequality description with
a proportional normal. To see this, choose a relative-interior point
of the facet. At least one defining inequality is active there; its
supporting hyperplane must contain that facet and therefore have its
normal. Redundant inequalities do not remove this requirement.

Suppose two new coordinates, indexed `u,v`, had no edge in the constraint
graph. Each vector `a_i` would have at most one of its `u,v` entries
nonzero. Invertibility supplies an `a_i` with a nonzero `u` entry, and
an `a_j` with a nonzero `v` entry. They must be different vectors,
and their other respective entries are zero. But the mandatory facet
normal `a_i-a_j` then has nonzero entries in both positions, a
contradiction. Every pair has an edge. QED.

Every linear quotient map with this same kernel is an invertible linear
transformation of the residual map. The lemma therefore covers every
choice of linear quotient coordinates, not only a badly chosen residual
basis. The quotient's constraint treewidth is `m-1`, although the
original objective graph has treewidth one.

This statement concerns explicit finite linear descriptions without
auxiliary variables. It does not assert a limitation for separation
oracles, implicit representations, or extended formulations.

## 4. Direct elimination also creates a dense quadratic

There is a related obstruction if the proposed reduction minimizes over
the central variable while retaining the original leaf coordinates.
On the open region of `y` values where

```
0 < (sum_i y_i)/k < 1,
```

the minimizing central value lies in its original interval and equals
`x=(sum_i y_i)/k`. Substitution gives

```
min_x F0(x,y)=sum_i y_i^2-(sum_i y_i)^2/m.                         (6)
```

This region is nonempty; take all `y_i=1/(2k)`. Every off-diagonal
Hessian entry in (6) is `-2/m`. Thus direct partial minimization creates
a dense quadratic on an open region, and its leaf interaction graph is
complete.

The conclusion does not require differentiable candidate factors.
For any pair of leaf coordinates, the rectangular mixed difference of
(6) is nonzero on a small rectangle inside that region. In an additive
factorization where no factor contains both coordinates, that mixed
difference would vanish. Hence every pair must occur in some factor
scope in any such exact representation using only the leaf coordinates.

## 5. A connected nonconvex extension with the same obstruction

Add one coordinate `z in [0,1]` and define

```
F(x,y,z)=F0(x,y)+z^2+z(1+x/k).                                   (7)
```

The interaction graph is still a star, with one additional bag `{x,z}`.
All original intervals remain `[0,1]`; every diagonal Hessian entry
is two. The objective is nonnegative and vanishes exactly on

```
S=S0 times {0}.
```

The feasible comparison point `(x,x/k,...,x/k,0)` gives

```
F(x,y,z)>=F0(x,y)+z^2>=dist((x,y,z),S)^2.                          (8)
```

Thus again `L=2`, `g=1`, and `kappa=2`, independently of `m`.
Its global Hessian norm is at most five: the core block has norm four,
the new diagonal is two, and the symmetric `x,z` coupling has norm
`1/k`.

Nevertheless the Hessian is indefinite. The core direction
`v=(1,1/k,...,1/k)` lies in its kernel. On the full direction
`(v,-1/(2k))`, the Hessian quadratic form is

```
2(-1/(2k))^2 + 2(1/k)(-1/(2k)) = -1/(2k^2) < 0.                 (9)
```

The stationary optimal face `z=0` has precisely the core kernel.
Quotienting that face's flat direction therefore produces the
basis-independent clique from Section 3. Eliminating the core's central
variable within that face gives Section 4's dense quadratic. This
shows that the obstruction occurs for a connected nonconvex box QP
with positive coordinate curvatures and uniform growth, not merely
for the globally convex core.

The extension deliberately has an elementary global certificate:
the squares and the term `z(1+x/k)` are nonnegative on its box.
It is not a difficult optimization instance. Its role is to disprove
width preservation for the specified quotient operation.

## 6. Consequences and limits for global certification

Eliminating a flat direction can move sparsity from the objective into
dense feasibility constraints, and a change of quotient basis need not
repair it. Directly minimizing out an internal coordinate can instead
make the reduced objective dense. A proof that simply quotients the
stationary kernel and then invokes a bounded-width box theorem misses
both changes.

An extended formulation avoids the clique: retain `t` and impose
`0<=t<=1/k`, `0<=r_i+t<=1`. Its constraint graph is a star.
It does, however, retain the eliminated direction as an auxiliary
variable and replace the product box by coupled linear constraints.
A suitable algorithm for that representation remains a possible route.
No impossibility result for extended formulations or stronger local
models follows here.

There is also a distinct operation that this result does not obstruct.
If a stationary polytope is **already known** to consist of global
optimizers, one can use its original-coordinate faces rather than form
a quotient. Fixing active original-coordinate bounds preserves objective
sparsity and can remove its flat directions. In the stationary polytope
used by the exact-recovery proof, choosing a vertex removes them all:
the original free Hessian is positive semidefinite, so a null direction
of its remaining free principal block would extend to a null direction
of the whole free block. Small perturbations of either sign would stay
in that polytope, contradicting that the chosen point is a vertex.
Knowing that polytope is globally optimal is exactly the missing
certification obligation; the quotient obstruction neither supplies nor
rules out a way to establish it.

The unresolved target remains an unknown-growth, independently certified
FPT algorithm for arbitrary rational-QP optimal sets. The present lemma
identifies a specific failed reduction rather than a hardness barrier
for that target.

## Verification

The star quotient was independently derived by two explorations. A
delegated reviewer supplied and checked the basis-independent facet
argument and the original-coordinate vertex caveat. The nonconvex
extension and its growth bound were checked directly.

The targeted command actually run for this note was
`python3 - <<'PY'` with `fractions.Fraction`, at `k=2,3,4`. It passed:

- 82,484 exact facet-slack checks, verifying each displayed facet has
  a point where every other displayed inequality is strict;
- 300 checks of projected interval feasibility against (4);
- 162 nonzero Schur mixed-difference checks;
- 30 invertible-basis support checks for the complete graph;
- three exact negative-Hessian-direction checks for (7).

The finite checks support the constructions; the proofs establish the
claims for every `k` and every quotient basis. No project-wide checks,
CI inspection, external search, or knowledge-base access was performed.
