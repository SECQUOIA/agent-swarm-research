# Independent review of cubic full-point completion

Date: 2026-10-02. Verdict: **PASS** on the actual saved
[cubic completion theorem](cubic-core-full-point-oracle.md).
I read its complete statement, rational error bound, canonical schedule,
and inherited oracle contracts. A separate mathematical reviewer also
checked the irrational-slope bridge before the main draft was written.
This is a correctness assessment, not a publication-priority claim.

## The selected fiber and rational rows are correct

The auxiliary coefficient `beta=alpha+1` is used only for convex
completion. It preserves convexity and is positive even on the
`alpha=0` branch. The original search parameter remains `alpha`, so
this change introduces no additional numerical inverse-noise factor
in the search bound.

For an exact optimal core `a`, the identity
`T_a=F_c+(beta/2)||v-a||^2` proves that its minimum is the original
global value and its minimizer set is exactly the optimal fiber at
`a`. This set is compact and convex. Its minimum-norm point is therefore
one well-defined selector, including draws with several optimal cores.

All Hessians are correctly formed after rational affine-hull reduction.
No ambient positive-semidefiniteness claim is made off `aff(P)`.
Reflection through the known relative interior point gives
`H(w)<=B_0 H_0` with `B_0=1+R_0/r`; hence the center kernel is common
to every feasible Hessian. Along that kernel the convex cubic is affine
with its rational center-gradient slope.

The target fiber is precisely the intersection of the feasible polytope
with the three equality blocks `H_0 d=0`, `g_0'd=0`, and `Ed=0`.
The core equality removes the unknown coefficient `a` from the slope
equation. This is not an application of a rational-height bound to an
irrational matrix: every matrix row used in the Hoffman bound is
rational and computed from base data. Only the equality right-hand side
depends on the selected exact optimizer.

## Error-bound constants and degenerate cases

Cubic symmetry and first-order optimality give the endpoint-curvature
bound `s<=6 Delta`. With `||d||<=2R_0` and
`H(w)<=B_0 M I`, one also has `s<=8 B_0 M R_0^2`.
These imply the saved estimate

```
d'H_0d <= 3R_0 sqrt(2B_0 M s).
```

The resulting fourth-power transverse constant is
`108 R_0^2 B_0 M/lambda_0^2`. It is at least one, so taking that
number itself instead of its fourth root is a valid rational upper
bound. The determinant lower bound for the positive eigenvalues has
polynomial encoding length. If the center Hessian has rank zero,
reflection makes every feasible Hessian zero and the transverse term
is correctly set to zero.

The common-kernel gradient remainder has norm at most `B_0 M R_0`.
The unknown slope contributes only
`||beta a+c|| ||Ed||<=k(beta+sigma)||Ed||`.
The exact completion identity gives `||Ed||<=2 sqrt(Delta)`.
Summing the three block residual norms yields the stated `C_res`.
Its conversion from square-root and linear gap terms to a fourth-root
term uses the explicitly restricted range `0<=Delta<=1`.

The general-polytope Hoffman step follows from the same projection
argument as the reviewed box version. After denominator clearing,
independent equality rows and active inequality normals form an integer
matrix with at most the relative dimension many rows. Its nonzero
singular values have the stated minor lower bound. Active inequality
contributions have the required nonpositive sign because the point being
corrected is already feasible. Redundant rows and irrational equality
right-hand sides cause no problem. Multiplication by the norm bound for
the affine lift converts the estimate back to original coordinates.

Thus `Gamma` is computable with polynomial binary length uniformly over
all selected cores and all sampled coefficients in the prescribed
support. In particular, it does not require a numerical residual
strong-convexity, slack, or active-multiplier lower bound.

## Canonical regularization and rational approximation

The target norm is consistently the original Euclidean norm. Comparing
the regularized minimizer with the minimum-norm point gives norm bound
`R_x`, unregularized gap at most `tau R_x^2<=1`, and

```
e^4/Gamma^4 <= 2R_x tau e,
||x_tau-p_a||^2 <= 2R_x e.
```

The chosen `tau=epsilon^6/(1024 R_x^4 Gamma^4)` implies the saved
`epsilon/2` bias bound. The rational surrogate uses a short approximate
core `b`, not expanded algebraic coefficients. Dropping irrelevant
constant terms, its difference from the exact-core regularized objective
is bounded by `beta sqrt(k)||b-a||` uniformly on `P`. The actual saved
tolerance `delta=tau epsilon^2/(32 beta k)` is more conservative than
needed. Together with `eta=tau epsilon^2/8`, it makes the exact-core
regularized gap at most `tau epsilon^2/4`. Strong convexity then gives
the other `epsilon/2` point error.

The short dyadic output requirement is explicit, including on rare
algebraic fallback draws. This prevents an exponentially long fallback
record from being silently treated as a short convex-solver input.
The extra requested core bits are `poly(I)+O(q)` with a uniform bound,
so the existing all-query random work factor composes correctly.
There is no resampling or optimization of a differently regularized
nonconvex global instance at each query.

For simultaneous objective accuracy, a polynomial-bit gradient bound
converts a tighter point request to the required original objective gap.
Combining that feasible upper value with an independent global value
enclosure gives the stated interval. Both calls concern the same sampled
objective and the same fixed core selector.

## Scope and verification

Both the total-degree-three and joint-convexifier assumptions are used.
This is not a theorem for arbitrary cubic residual slices at a fixed
core. Full-point Cauchy output remains distinct from exact active labels
or small expanded algebraic coordinates. The reviewed cubic radical
activity example already explains why those stronger outputs cannot be
inferred merely from accurate points.

The author reports a distinct exact diagnostic covering irrational-core
rows, lifted error bounds, rational surrogate solves, tied-core selection,
and rank-zero cases. I did not rerun it or duplicate the earlier cubic
Hessian fixtures. This review independently checked the algebra, constants,
input lengths, output selector, and scope against the actual draft.
No index edits, external searches, project-wide tests, or CI inspection
were performed.
