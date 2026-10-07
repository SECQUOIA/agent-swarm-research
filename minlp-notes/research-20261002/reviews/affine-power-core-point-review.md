# Independent review of affine-power core point completion

Date: 2026-10-02. Result: **PASS** on the complete actual
[affine-power draft](../new-direction/affine-power-core-point-oracle.md),
including the two final precision clarifications. No mathematical or
bit-complexity gap remains in this scoped corollary. This review covers
the supplied positive even-affine-power representation, the known
rational polytope, and the previously reviewed selected-core interface.
It makes no claim about recognizing such representations or about the
separate proposed theorem for general convex polynomials.

## 1. Scalar bound and optimal-fiber equations

Equation (3) has the stated constant. Put `u=t-s`. Applying the scalar
monotonicity inequality at `s+theta u` and `s`, then multiplying by
`p/theta`, gives the integrand bound
`p 2^(2-p) theta^(p-1)|u|^p`. Integration from zero to one cancels
the factor `p`. The endpoint follows by continuity, and `p=2` gives
equality. No optimality claim for the constant at higher degree is
needed.

The completion objective is convex because
`T_a=G_alpha+||v||^2/2-(beta a+c)'v+constant`. Its minimizer set is
exactly the global optimal fiber `S_a`: the original objective is at
least its global minimum, and the added nonnegative penalty vanishes
exactly at the selected core. Constrained first-order optimality for
`T_a` proves the first inequality in (4); the independent comparison
with the original global minimum proves the second.

Both directions of (5) hold. At zero gap, PSD of `Q` implies `Qu=0`,
every positive-weight power term forces `a_j'u=0`, and the core penalty
forces `Eu=0`. Equality of objective values then forces `ell'u=0`.
Conversely these rows preserve the quadratic, every affine-power
argument, the affine term and the core. The linear row and the core
rows must be retained, as they are in the draft. The matrix contains
only known rational data; an irrational optimizer appears only in its
right-hand side.

## 2. The error constant has polynomial binary length

The row-sum bound `M` bounds the operator norm of the symmetric PSD
matrix `Q`, so `||Qu||^2<=M u'Qu<=2M Delta`. The rational bound
`2M Delta^(1/d)` follows for `Delta<=1` and `d>=2`. For each power,
the root of `2^(p_j-2)/w_j` is at most `C_j`, and
`Delta^(1/p_j)<=Delta^(1/d)`. The core estimate uses `beta>=1`.
These observations prove all of (6), including zero gap.

Writing the quadratic part of `T_a` with matrix `Q+E'E` gives the
claimed difference bound `R(||Qu||+||Eu||)`. The power derivative
bound is `K_j`, and
`||beta a+c||<=sqrt(k)(beta+sigma)<=N`. Solving the objective-value
difference for `ell'u` therefore proves the displayed `C_lin`.
Adding the block residual bounds gives `C_res` without a missing
row-count factor.

The general-polytope Hoffman argument linked in the draft is valid
uniformly in the equality right-hand side. At the nearest point in
the slice, choose independent equality rows and active inequality
normals from the original integer matrices. There are at most `n`
rows. Their Gram determinant is a positive integer, hence at least
one, and their largest singular value is at most `nC`. Their least
singular value is therefore at least `(nC)^(-(n-1))`. The active
inequality terms have nonpositive inner product with a displacement
from a feasible point, leaving only the equality residual. Clearing
denominators multiplies that residual by `D`.

This proves (7) with the displayed constant, including redundant rows
and lower-dimensional polytopes. If the selected row set is empty,
the distance is already zero. The proof does not introduce a height
bound for the unknown right-hand side. The supplied coordinate box
gives rational `R` and `B_j` with polynomial binary length. Products
used to clear denominators and the power `(nC)^(n-1)` also have
polynomial binary length. Consequently `Gamma` is computable with
polynomial bit work for fixed `d`, uniformly over all selected cores
and noise atoms.

## 3. Minimum-norm rate and precision budgets

Comparison with the minimum-norm point `p` proves
`||x_tau||<=||p||<=R` and an unregularized gap at most `tau R^2<=1`.
Comparison with the nearest optimizer `s` also gives
`Delta(x_tau)<=tau(||s||^2-||x_tau||^2)<=2R tau e`.
Projection optimality of `p` onto the convex set `S_a` gives
`||x_tau-p||^2<=2R e`. Thus the two displayed rate inequalities
require neither an interior optimizer nor strict complementarity.

For positive `e`, substitution of (8) gives exactly

```
(2R tau Gamma^d)^(1/(d-1))
 = epsilon^2 / (2^((3d-1)/(d-1)) R)
 <= epsilon^2/(8R).
```

The case `e=0` has `x_tau=p` by minimum-norm uniqueness. The
regularization displacement is therefore at most `epsilon/2`.

The final draft explicitly assigns core-oracle error `delta/2` and
dyadic-rounding error at most `delta/2`. Clipping this auxiliary core
vector to `[0,1]^k` cannot increase its distance to `a`. The rounded
vector need not itself be a feasible projected core; completion is
still solved over the original polytope. No coordinate clipping of
the completed feasible point is used.

The perturbed completion gap is bounded by

```
eta+2 beta sqrt(k) delta
 = tau epsilon^2 (1/8+1/(16 sqrt(k)))
 <= 3 tau epsilon^2/16
 <= tau epsilon^2/4.
```

The regularized objective has strong-convexity modulus `2 tau` in
the original ambient Euclidean metric. A feasible objective gap
therefore gives distance at most `epsilon/2` to `x_tau`, including
on a lower-dimensional domain. Adding the regularization displacement
proves the full requested point accuracy. The separately reviewed
convex value interface provides the required rational feasible
objective-gap solve.

All extra precision lengths are `poly_d(I)+O_d(q)`. Short dyadic
rounding before completion prevents an exact core fallback record
from becoming the completion solver's coefficient representation.
The same selected-core oracle, finite law and random work factor are
used for every query. This justifies the expected-work composition
without resampling or assuming a bound on expanded algebraic output.

The final zero-core paragraph correctly omits `delta` and the core
oracle. It retains only `tau` and `eta`, the known rational slice,
and deterministic convex optimization. The regularizer remains the
original ambient norm. Singleton and zero-dimensional domains are
handled directly.

## Verification scope

This was an independent actual-file proof and bit-complexity review.
The oracle-error split and zero-core clarification were reread after
the author applied them. The inherited Hoffman and selected-core
interfaces were checked in their actual files. No numerical diagnostic
or generic optimization test was repeated; the author's distinct scalar
and rate diagnostic is recorded in the draft.

A targeted inline Python check of this review passed local file links,
balanced code fences and display delimiters, and trailing whitespace.
`git diff --check -- research-20261002/reviews/affine-power-core-point-review.md`
also passed. No external search, index edit, project-wide verification
or CI inspection was performed. This finishes the assigned scoped
review; no further research direction is part of this work.
