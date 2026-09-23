# Independent audit of the quadratic rank integer-complexity theorem

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Source: `results/quadratic-rank-integer-complexity.md`.

## Verdict

The rank law, explicit constant, arbitrary convex integer-lift lower bound,
and compact binary linear upper bound pass independent mathematical review.
No required proof correction was found. The proof handles indefinite and
rank-deficient Hessians correctly. This review does not establish literature
priority or publishability.

The intended positive tolerance in the logarithmic upper formula can be
made explicit. At zero tolerance and positive rank, the stated finite lower
bound already rules out every finite integer dimension. At rank zero, the
affine graph is exactly polyhedral and uses zero integer coordinates.

## Geometric lemma

Compactness gives a maximizing tuple of `d+1` points. If the affine hull is
full-dimensional, the maximum absolute determinant is positive. Replacing
a single column of the maximizing matrix keeps all simplex vertices in
`S`; Cramer's rule gives the replacement determinant `c_i det A`. Thus
`|c_i|<=1`, proving the full enclosure in the affine image of `[-1,1]^d`.
The argument does not require convexity of `S` or any assumption about its
boundary.

For `q(v)=v^T Mv/2`, polarization gives exactly

```
v_i^T Mv_j = q(v_i)+q(v_j)-q(v_i-v_j).
```

The diagonal bound is `2 delta` and the off-diagonal bound is `3 delta`.
Every row norm is at most `3 sqrt(d) delta`, so Hadamard gives
`|det(A^T M A)| <= (3 sqrt(d) delta)^d`. Taking square roots after using
`det(A^T M A)=(det A)^2 det M` proves the displayed volume bound. Absolute
determinants correctly accommodate every inertia of the nonsingular
symmetric matrix. For `delta=0`, a nonsingular Gram matrix would have every
entry zero, which is impossible; hence only the zero-volume case remains.

## Parity, constants, and rank deficiency

Same-parity integer lifts have an integral midpoint. Its graph-output
error is `(s-t)^T H(s-t)/8`, so the lemma's parameter is exactly
`delta=4 epsilon`. Closures of the support sets in the compact box preserve
the pairwise inequality and coverage, supplying measurable sets without
closedness or measurability assumptions on the original lift.

For a nonsingular Hessian in dimension `r`, the volume cover yields

```
V sqrt(|det H|) <= 2^p 2^r (12 sqrt(r) epsilon)^(r/2).
```

Raising this inequality to `2/r` introduces a factor 4 from `2^r`; hence
the denominator is exactly `48 sqrt(r)`. All powers of volume and
determinant in the stated constant are correct.

A real symmetric rank-`r` matrix has exactly `r` nonzero eigenvalues. The
sum of its principal minors of order `r` is their nonzero product, so at
least one principal minor is nonzero. This argument does not assume
positive semidefiniteness. Fixing the complementary coordinates within
their box intervals intersects the original convex lift with affine
equations. Every point on the restricted exact graph still has a lift;
every admitted restricted point retains the original error guarantee.
The restricted Hessian is precisely that nonsingular principal submatrix,
and no new integer coordinate is introduced.

## Upper formulation

The spectral decomposition supplies exactly `r` nonzero square terms.
Each associated linear form has positive width on a box with interior.
Normalization is therefore valid, and shifting its interval contributes
only an affine term. The coefficient sum `A=sum_j |c_j|` is positive when
`r>0`.

I checked the invoked square sawtooth formulation against its explicit
statement in `results/mip-relaxation-binary-lower-bounds.md`: it contains
the exact square graph and has two-sided error at most `2^(-2L-2)` with
`L` binaries and a linear number of auxiliary variables and rows. Applying
it to dependent linear forms still contains every exact graph point:
each square block can be lifted independently at the common chosen `x`.
Signs of the quadratic coefficients are handled by the triangle
inequality with their absolute values.

For positive epsilon below `A/4`, the stated ceiling ensures
`A 2^(-2L-2)<=epsilon`; for epsilon at least `A/4`, depth zero suffices.
The binary count is `rL`, with leading term
`(r/2)log2(1/epsilon)`. All decomposition and box constants depend on
`H,B`, while the affine coefficients of `f` do not affect the count.
The finite lower bound gives the matching leading term after taking
logarithms. Both minima exist as nonnegative integer minima for each
positive tolerance because this construction supplies an admissible
finite formulation.

## Scope checks

The whole graph on a box with nonzero side lengths is essential. The
proof does not assert this lower bound on a lower-dimensional feasible
set merely because an ambient quadratic formula has rank `r`. A
rank-`r` restriction on an actual full-dimensional transverse box would
be sufficient. The two-sided vertical error condition on every admitted
point is also essential; an epigraph can have different complexity.

The lower theorem permits arbitrary continuous convex constraints,
continuous lift dimensions, integer ranges, and real coefficients. The
compact upper is an existence statement with real coefficients. No claim
of a rational bit-complexity algorithm is needed for this theorem; an
irrational spectral decomposition would need separate handling if such a
claim were added.

## Optional independent corroboration by covariance

The following alternate proof gives the same geometric exponent and an
optional improved dimension-dependent constant. It is not needed to
repair the reviewed proof. The covariance and moment inequalities are
classical tools; no novelty claim is attached to this argument.

Assume `S` has positive volume, translate its centroid to zero, and let
`X,Y` be independent uniform points on `S`. Write `Sigma=E[XX^T]`, which
is positive definite because a positive-volume set cannot lie almost
everywhere in a hyperplane. Compactness ensures finite fourth moments.
Set `A=X^T M X`, `B=Y^T M Y`, and `C=X^T M Y`. The pairwise hypothesis and
independence give

```
delta^2 >= E[q(X-Y)^2]
        = (1/2) E[A^2] + (1/2)(E[A])^2 + E[C^2]
        >= tr(M Sigma M Sigma).
```

The cross expectations involving `AC` and `BC` vanish because both random
vectors have zero mean. The trace is the sum of squared eigenvalues of
`Sigma^(1/2) M Sigma^(1/2)`. Applying the arithmetic-geometric mean
inequality to these squared eigenvalues yields

```
|det M| det Sigma <= (delta^2/d)^(d/2).
```

For completeness, a direct volume-covariance bound is

```
volume(S) <= omega_d (d+2)^(d/2) sqrt(det Sigma),
```

where `omega_d` is the volume of the unit Euclidean ball. To prove it,
apply `Sigma^(-1/2)` to the centered set. The resulting set has covariance
identity, volume `W`, and second moment integral `dW`. Among sets of volume
`W`, the centered ball of radius `R=(W/omega_d)^(1/d)` minimizes the
integral of squared norm: outside this ball squared norm is at least
`R^2`, and inside it is at most `R^2`, so exchanging equal amounts of
volume cannot decrease the ball's integral. That ball's integral is
`d W R^2/(d+2)`. Hence `R^2<=d+2` and the claimed inequality follows by
undoing the linear transformation.

Combining the two bounds proves the alternative estimate

```
volume(S) <= omega_d ((d+2) delta/sqrt(d))^(d/2)
             / sqrt(|det M|).
```

The same parity cover then proves the optional lower constant

```
epsilon >= c_cov 2^(-2p/r),
c_cov = sqrt(r) |det H_I|^(1/r) V_I^(2/r)
        / [4(r+2) omega_r^(2/r)].
```

For dimension one this reproduces the reviewed denominator 48; for
dimension two it yields `sqrt(2)/(16 pi)` times the determinant-volume
factor. The existing simpler maximal-simplex proof is already sufficient
for the full theorem. This alternate calculation was derived independently
as an additional consistency check and would need another review before
being promoted into the main result.
