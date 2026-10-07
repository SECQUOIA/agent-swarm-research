# Expected local grid counts for integral TU constraints

Date: 2026-10-02. Status: local counting theorem; no complete constrained
exact optimization theorem is asserted.

Integral totally unimodular constraints admit a common set of possible
recourse boundaries determined only by bag size. This strengthens
[the fixed polytope count](polyhedral-chamber-count.md): its geometric
constant can be bounded independently of the number of outside
variables or constraints. The objective contribution still depends
on the total variable count and a full Hessian upper bound.

The result supplies a local count for true feasible near-optimal
tuples. It does not bound the work needed to solve recourse problems
or provide an exact constrained closure algorithm.

## Statement

Let

```text
P = {x in [0,1]^n : A x <= c}
```

be nonempty, where `A` is totally unimodular and `c` is integral.
All variables are continuous. Suppose `F_0` is twice continuously
differentiable on a neighborhood of the box and

```text
Hess F_0(x) <= H I             on [0,1]^n,   H>=0.            (1)
```

Fix a bag of size `1<=b<=n`, write `x=(v,z)`, and let

```text
Q = projection_v(P),
V(v) = min_{z : (v,z) in P} [F_0(v,z)+gamma_out'z],
f* = min_{v in Q} [V(v)+gamma_B'v].
```

The bag noises are independent of one another and of the outside
noises. They are either uniform continuous noises on
`[-sigma,sigma]`, with `sigma>0`, or uniform on the `M>=2`
equally spaced points of that interval. The outside noise law is
arbitrary.

For `h=1/r`, with integer `r>=1`, and `eta>=0`, let

```text
N_h = #{v in Q intersect {0,h,...,1}^b :
        V(v)+gamma_B'v <= f*+eta h^2}.
```

There is a finite computable constant `C_b`, depending only on
`b`, such that the finite uniform law satisfies

```text
E N_h <= C_b [1+(n b H+eta)/sigma+1/(M h)]^b.                 (2)
```

For continuous uniform noise, omit `1/(M h)`. In particular,
the bound is independent of grid resolution in the continuous case,
and is uniform when `M h>=1` in the finite case.

The dependence of `C_b` on `b` is not estimated sharply. This
statement is not a bound with an absolute constant raised only to
the bag-size power.

## Fiber bases and TU determinants

Append the coordinate-bound rows to `A x<=c`; this preserves total
unimodularity and an integral right-hand side. Continue to denote the
augmented system by `A x<=c`, and partition its columns as
`A=[A_v A_z]`. Put `q=n-b`.

When `q>0`, each vertex of a nonempty bounded fiber is represented
by a set `I` of `q` rows for which

```text
B_I=(A_z)_I
```

is nonsingular. Total unimodularity gives
`det(B_I) in {-1,1}`. The corresponding affine candidate is

```text
z_I(v) = B_I^(-1)c_I - B_I^(-1)(A_v)_I v.                    (3)
```

Every entry of the derivative matrix
`-B_I^(-1)(A_v)_I` lies in `{0,-1,1}`. Indeed, Cramer's
rule expresses it, up to sign, as a determinant obtained by replacing
one selected outside column by one bag column. That determinant
is a square minor of the full TU matrix.

Substitution of (3) into any row `j` gives a candidate-feasibility
inequality

```text
alpha_(I,j)' v <= beta_(I,j),

alpha_(I,j)' = (A_v)_j - (A_z)_j B_I^(-1)(A_v)_I,
beta_(I,j) = c_j - (A_z)_j B_I^(-1)c_I.                      (4)
```

The offset `beta_(I,j)` is integral. Each coefficient indexed by
a bag column `ell` is the determinant ratio

```text
alpha_(I,j),ell
  = det([[B_I, (A_v)_(I,ell)],
         [(A_z)_j, (A_v)_(j,ell)]]) / det(B_I).              (5)
```

If row `j` is already in `I`, the numerator is zero.
Otherwise it is a `(q+1)` by `(q+1)` minor of the full TU
matrix. Therefore

```text
alpha_(I,j) in {0,-1,1}^b,       beta_(I,j) in Z.             (6)
```

For `q=0`, the original bag inequalities already have the form
(6), and no fiber basis is needed.

## A universal arrangement in the bag cube

A nonconstant hyperplane

```text
alpha'v=beta,       alpha in {0,-1,1}^b,   beta in Z
```

can meet the bag cube only if `-b<=beta<=b`.
Inequalities whose boundaries do not meet the cube have constant
truth values there. The same is true of zero-normal inequalities.

It follows that every candidate-feasibility region in (4) is a union
of cells of the one universal arrangement

```text
alpha'v=beta,
alpha in {0,-1,1}^b excluding zero,
beta in {-b,...,b},
v in [0,1]^b.                                               (7)
```

There are fewer than `(2b+1)3^b` listed hyperplanes before
discarding duplicates. Cube boundary hyperplanes are included.
The arrangement, its faces, and any fixed rational triangulation of
them depend only on `b`.

On the relative interior of an arrangement cell that lies in `Q`,
the list of feasible affine candidates is fixed and nonempty. The
fiber is their convex hull. On the closed cell, the same
representation follows by the boundary interpolation argument in
[the chamber proof](polyhedral-chamber-count.md#affine-fiber-vertices-on-closed-polyhedral-regions).
This includes fibers of lower dimension and degenerate vertices.

Thus every recourse chamber needed for the counting proof is one of
finitely many universal cells from (7). Its geometry does not depend
on the number of constraints, the outside dimension, or the values
of the integral right-hand side.

## Curvature after substitution

The linear part of the full affine map `v -> (v,z_I(v))`
has `n` rows and `b` columns, all with absolute value at most
one. Its squared operator norm is bounded by its squared Frobenius
norm, hence by `n b`. The same operator-norm bound holds for
every convex combination of these affine maps.

Representing the fiber by convex combinations, (1) therefore makes
each substituted objective semiconcave with constant

```text
K=n b H.                                                    (8)
```

The substituted outside noise is affine and contributes no Hessian.
Taking an infimum over the fixed simplex of convex-combination
weights preserves this semiconcavity on each closed arrangement
cell. Neither `K` nor the chamber geometry depends on the outside
noise realization.

## Applying the face count

Apply the directional face argument from
[the general chamber theorem](polyhedral-chamber-count.md#face-counting-within-one-simplex)
to the fixed triangulation of (7). For completeness, its dependence
on the parameters is as follows.

Within each simplex, classify a grid point by the face spanned by
its barycentric coordinates that are at least `h`. For sufficiently
small `h`, that face is nonempty. If its dimension is `k`, the
point lies within a constant times `h` of it. Hence the number
of such grid points is at most `D_b h^(-k)`, where `D_b`
depends only on the universal simplex geometry.

There are `k` fixed independent directions in that face for
which both steps `v+h d_j` and `v-h d_j` remain feasible.
True near-optimality and (8) confine the directional bag noises
to intervals of lengths at most

```text
(K ||d_j||^2+2 eta) h.
```

A nonsingular coordinate minor of the direction matrix exists.
After conditioning on the other bag noises, its inverse bounds
each of the remaining `k` noise coordinates by an interval
of length at most

```text
D'_b (K+eta) h.
```

The constants needed here depend only on the finite universal
triangulation. The conditional probability is at most

```text
[D'_b (K+eta)h/(2 sigma)+1/M]^k
```

for the finite law, with the last term omitted for continuous noise.
Multiplication by the node count cancels `h^k`. Summing over the
fixed finite collection of simplices and faces proves (2), after
absorbing constants into `C_b`.

The finitely coarse range of meshes excluded by the barycentric
threshold argument has a number of grid nodes bounded only by
`b`; enlarging `C_b` covers it. Rational hyperplane data and
finite triangulation also make all these geometric constants
computable from `b` alone.

## Scope and verification

The integral right-hand side is essential to this universal-arrangement
argument. Arbitrary rational offsets can produce arbitrarily many
distinct hyperplanes of the same normal direction. Clearing
denominators in the inequalities does not generally preserve total
unimodularity. This proof therefore does not silently extend (2) to
arbitrary rational right-hand sides.

The aligned setting here also admits
[mean-preserving feasible TU rounding](tu-feasible-rounding.md).
That lemma uses the same full Hessian assumption. The combination
does not yet prove the exact constrained closure, the complete
algorithm's expected bit work, or the original box theorem under
only a coordinatewise diagonal curvature bound.

This note concerns continuous variables. Fixing a particular integer
slice preserves TU structure, but counting across all possible
integer slices requires a separate argument.

The determinant identities, universal arrangement, and dependence
of the chamber bound were checked analytically. A separate reader
reviewed the complete proof and found no mathematical blocker.
The targeted
formatting command was `git diff --no-index --check /dev/null
research-20261002/new-direction/tu-polyhedral-cell-count.md`.
No numerical tests, project-wide verification, CI inspection, or
literature search were performed.
