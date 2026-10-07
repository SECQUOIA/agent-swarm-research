# Independent review of the support-one contact criterion

## Finding

The new main-text proof is correct under its stated unique-contact and
positive-height hypotheses. Closed interval feasibility is equivalent to
`z_A = z_K` as a supremum. An admissible orbit set attains this value exactly
when a common interval point lies in the interior of the interval for the LP
vertex. Failure of closed feasibility for every positive parameter gives a
strict gap.

The constructive treatment of singular matrix limits removes the
full-dimensionality requirement used by the original source proof and the
first version of `audit-depth.md`. Neither the contact theorem nor its
approximation lemma needs a rank assumption. This improvement requires the
stated positive heights and strict positivity of `q` at the noncontact
vertices; these hypotheses must be retained.

No counterexample or mathematical defect was found in the main-text proof
or its expanded appendix proof. The contact review is resolved.

## Scope and material inspected

This review covers `dp:contact-approx` and `dp:contact-intervals` in
`sections/04-depth.tex`, their surrounding definitions, the expanded
`dp:contact-proof` in `appendices/B-depth.tex`, the contact derivation in
Section 5 of `research-20261001/ratio-bound/note.md`, and the replacement
proof in `evidence/audit-depth.md`. It does not review the completed family B
criterion, computational certificates, the sharp cylinder example, or other
sections of the manuscript.

The project instructions, manuscript brief, and author contract were read.
No literature research, solver experiment, numerical search, or certificate
generator was run. A separate child reviewer independently checked the
perturbation lemma and its appendix expansion and found no issue. The algebra
and compactness argument below were derived independently from the PSD
definitions.

## Hypotheses used

The section assumes finitely many projected rays, strictly positive costs,
`q(sbar) > 0`, and a nonempty feasible corner with finite optimum. These give
`q > 0` on each contracted simplex `T_r`, for `r < 1`, and `q >= 0` on
`T*`. The contact theorem additionally assumes:

- the only feasible geometric contact of `T*` is `t*`, with `q(t*) = 0`;
- `t*` is a scaled-ray vertex, so the contact has support one;
- every other generating vertex has positive tangent height.

After translation to the contact frame these other vertices have `h_v > 0`
and `q(v) = h_v - x_v y_v > 0`. In particular, the LP vertex satisfies both
inequalities. Positivity of `q(v)` is needed in both singular-limit
constructions. Positivity of `h_v` is needed for the interval division and
for the positive first diagonal entry. Finiteness is needed to choose one
parameter that works for every vertex and one perturbation size for every
contracted vertex. The proof never assumes three independent rays.

The manuscript states these requirements in the paragraph preceding the
theorem; its reference to those assumptions is adequate. Interpreting
"unique contact" explicitly as `T* intersect S = {t*}` would make the
geometric condition particularly easy to check.

## Contact normalization and intervals

Write `X = [[a,b],[c,d]]`. At the centered contact,
`M(0) = [[0,0],[0,1]]`, so

`sym(X M(0)) = [[0,b/2],[b/2,d]]`.

PSD membership forces `b = 0` and `d >= 0`. If `det X > 0`, then
`ad > 0`, so `d > 0` and `a > 0`. Positive scaling by `1/d` gives exactly
`X = [[alpha,0],[beta,1]]`, with `alpha > 0`.

For `v = (x,y,h)`, its PSD matrix is

`[[alpha h, (alpha x + beta h + y)/2],
  [(alpha x + beta h + y)/2, beta x + 1]]`.

Its determinant satisfies

`4 det(sym(X M(v))) = 4 alpha q(v) - (alpha x - y - beta h)^2`.

Because `alpha h > 0`, the determinant inequality implies PSD membership
and the trace condition. Its strict form is equivalent to positive
definiteness. Solving the square inequality for `beta` gives precisely the
closed interval printed in the manuscript, and its strict form gives that
interval's interior. No sign change is lost when dividing by `h > 0`.

For completeness, a singular PSD matrix at the LP vertex cannot represent
an interior point of this contact set. If the lower diagonal entry vanishes,
then `beta != 0`, and changing `x` makes that entry negative. Otherwise both
diagonal entries are positive; a null vector has both coordinates nonzero,
and varying `y` changes its quadratic form with a nonzero linear coefficient.
Thus interior membership is exactly positive definiteness here.

An attaining set contains all scaled-ray endpoints and therefore `T*`; it
contains the contact and has the stated normalization. Conversely, an
interval solution strict at the LP vertex gives an admissible convex orbit
set containing `T*`. Its cut has ratio at least one, and validity bounds that
ratio above by one. This proves both directions of the attainment criterion.

## Closed-set perturbation

Let `A(s) = sym(X M(s))` for an invertible positive-determinant matrix whose
set contains `T*`. Fix `0 < r < 1` and a generating vertex `v`, and set
`v_r = (1-r)sbar + r v`. Affinity gives

`A(v_r) = (1-r)A(sbar) + r A(v)`.

Both summands are PSD, and both coefficients are positive. Therefore

`ker A(v_r) = ker A(sbar) intersect ker A(v)`.

Indeed, a zero quadratic form of the sum forces both nonnegative endpoint
forms to vanish, and a PSD matrix annihilates any vector on which its form
vanishes. This common kernel is annihilated by `A(s)` on the whole segment
from `sbar` to `v_r`.

Every real two-by-two skew-symmetric matrix is a scalar multiple of
`J = [[0,1],[-1,0]]`. Thus for a nonzero common null vector `z`,

`X M(s) z = k(s) J z`.

All segment points lie in `T_r`, where `q > 0`. Hence `M(s)` and `X` are
invertible. If `k(s)` vanished, the displayed equation would contradict
that invertibility. Its continuous nonzero scalar therefore has a constant
sign on the connected segment. The endpoint equations give

`M(sbar)^(-1) M(v_r) z = (k(v_r)/k(sbar)) z`,

with a strictly positive ratio. The order of the two matrices is correct:
first cancel `X`, then premultiply by `M(sbar)^(-1)`.

Consequently `H_v = sym(M(sbar)^(-1) M(v_r))` is positive definite when
restricted to `ker A(v_r)`. Set
`X_epsilon = X + epsilon M(sbar)^(-1)`. At the contracted vertex its PSD
matrix is `A(v_r) + epsilon H_v`. On the positive eigenspace of `A(v_r)`,
positivity persists. In a kernel/eigenspace block decomposition its Schur
complement on the kernel is

`epsilon H_KK - epsilon^2 H_KP
 (A_PP + epsilon H_PP)^(-1) H_PK`,

which is positive definite for sufficiently small positive `epsilon`.
If the kernel is zero, continuity suffices; if it is the entire space,
the positive kernel restriction gives direct positive definiteness. Thus
the argument covers every possible nullity.

At `sbar` the new symmetric matrix is `A(sbar) + epsilon I`, hence positive
definite. Finitely many generating vertices allow one common positive
`epsilon`, and `det X_epsilon > 0` persists by continuity. The new set is
admissible and contains `T_r`. Its cut ratio is at least `r`; letting `r`
increase to one proves the exact supremum. No claim that the perturbation
contains the original contact point is needed or made.

## Necessity, including singular limits

Assume `z_A = z_K` and choose admissible matrices whose cut ratios increase
to one. Multiplication by a positive scalar preserves each set; normalize
the matrices to Frobenius norm one. A subsequence converges to a nonzero
matrix `X` with `det X >= 0`. For each fixed generating vertex, the
contracted vertices converge to the corresponding vertex of `T*`. The PSD
cone is closed and `M` is continuous, so the limiting PSD inequalities
contain every generating vertex and hence `T*`.

If `det X > 0`, the preceding contact normalization immediately yields the
closed interval solution. If `det X = 0`, contact membership yields
`X = [[a,0],[c,d]]`, `d >= 0`, and `ad = 0`. There are exactly two cases.

When `d > 0`, `a = 0`. At every noncontact vertex the first diagonal entry
is zero, so PSD membership forces `c h_v + d y_v = 0`. Set `beta = c/d`.
For a new positive `alpha`, the contact-set determinant slack becomes

`4 alpha q(v) - alpha^2 x_v^2`.

Choose `0 < alpha < min_{x_v != 0} 4 q(v)/x_v^2`; if the indexed set is
empty, any positive `alpha` works. This makes every slack strictly positive.
The first diagonal entry is also positive, so every noncontact matrix is
positive definite, including the LP vertex matrix. The new orbit set is
admissible, contains `T*`, and attains the exact value.

When `d = 0`, PSD membership at the LP vertex gives `a h_sbar >= 0`.
If `a = 0`, its off-diagonal entry `c h_sbar/2` forces `c = 0`, which would
contradict the nonzero normalization. Thus `a > 0`. At any noncontact
vertex,

`det(sym(X M(v))) = -(a x_v - c h_v)^2/4`,

so `x_v = (c/a) h_v`. Set `beta = alpha c/a`. The new determinant slack is

`4 alpha q(v) - y_v^2`.

Choose `alpha > max_v y_v^2/(4 q(v))`. Finiteness and strict positivity of
`q(v)` make this a finite choice. Again all noncontact matrices are positive
definite, and the new orbit set attains the exact value.

Both singular cases therefore produce finite interval parameters and even
strict feasibility at the LP vertex. A limiting matrix lying in a plane is
not an obstruction; its linear relation supplies the required construction.
This is why full dimensionality is unnecessary for the revised theorem.

Taking the contrapositive of necessity, and using `z_A <= z_K`, gives the
stated strict-gap conclusion.

## Verification record

Only targeted source inspections were run: `rg --files`, `rg -n`, `cat`, and
`sed` on the instructions, contact source note, author audit, main-text
section, and contact appendix. Exact symbolic identities above were checked
by direct algebra. A targeted inline `python3` script using SymPy also
verified the contact determinant identity, the `d=0` determinant identity,
and both singular-limit slack identities exactly; all four assertions passed.
No computational experiment or certificate generator was rerun. No
project-wide verification or CI inspection was performed. The expanded
appendix matches the independently derived argument, including the two
extreme nullities and the explicit finite parameter bounds.
