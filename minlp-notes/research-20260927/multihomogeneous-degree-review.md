# Independent review of the multihomogeneous degree refinement

Date: 2026-09-27. Reviewer: a fresh adversarial review agent, not an author
of the degree note. Review target:
[the multihomogeneous degree proof](multihomogeneous-span-degree.md).

**Verdict:** I found no substantive gap in the parameter lemma, ordered
specialization, KKT root count, or joint-field conclusion. The proof supports
the stated bound

\[
 [\mathbb Q(x_1^*,\ldots,x_n^*):\mathbb Q]
 \le \max_{0\le s\le\min(h,n)}2^s\binom ns
\]

for the unique minimum-norm optimizer under the stated rational convex
quadratic assumptions. I also read Sections 2--4 of the
[ordered perturbation note](ordered-perturbation-optimizer.md), rather than
treating its existence as sufficient evidence. Its affine restriction,
ordered convergence, and common support supply the hypotheses used here.
This review does not independently establish the separate coefficient-height
estimate or the full mixed-integer optimization algorithm.

## 1. The generic algebra and exceptional parameters

The potentially dangerous step is replacing the full polynomial zero set
by the algebra

\[
 E=\mathbb Q(t)[y,1/(DA)]/(F),\qquad D=\det F_y.
\]

At any geometric point remaining after localization, the square Jacobian
is invertible. The local ring of the zero set there is a reduced
zero-dimensional ring. Therefore such a point cannot belong to a
positive-dimensional component, including at an intersection with another
component. A finite-type zero-dimensional algebra over a field is finite
over that field. After extending to an algebraic closure, the localized
algebra is consequently a finite product of fields, with dimension equal
to the number of surviving regular roots. This justifies both finiteness
and the use of the isolated-root bound for its dimension.

A component confined to a special parameter locus cannot contribute a
regular specialized root that this generic algebra misses. At a real
regular root, the implicit function theorem gives a root for every
parameter in a real open neighborhood. In particular the component
containing that local branch projects onto an open set. If the generic
localized algebra were zero, clearing denominators in the identity
`1 = 0` would prohibit such roots outside the zero set of one nonzero
parameter polynomial. That contradicts the open neighborhood.

The characteristic-polynomial identity does not require a globally chosen
basis that specializes well. Its coefficients lie in `Q(t)`; after
clearing their denominators, its vanishing in the localized algebra is a
finite algebraic identity. Clearing denominators in that identity gives
an additional nonzero parameter polynomial `e(t)`, and powers of `D A`.
At a regular root with `A` nonzero and `e(t)` nonzero these factors can be
cancelled. This yields the stated polynomial identity for the output.

At an exceptional parameter with `e(t) = 0`, the same local implicit
branch has `D A` nonzero in a neighborhood. The complement of the zero
set of `e` is dense in that neighborhood. Continuity of the polynomial
identity and of `C/A` therefore extends the identity to the original
root. This argument is the reason an exceptional parameter may be retained;
simply discarding exceptional parameters would be insufficient.

These observations also show why an increase in the number of regular
roots at a special parameter is not an obstruction. Each of finitely many
distinct regular roots persists on a common nearby parameter neighborhood.
A generic nearby fiber must contain all of those branches. New singular
roots or positive-dimensional special fibers are not counted, and are not
used in the construction.

## 2. Ordered limits and the joint field

The global lowest nonzero coefficient in `delta` must be selected before
specializing `epsilon`. The note does this. At a particular outer parameter
that coefficient can specialize to the zero polynomial, but the required
equality then still holds. Dividing the full identity by the selected
power of `delta` and taking a finite inner limit is valid without any bound
on the other root coordinates or the multipliers. All higher coefficients
are polynomials in the finite output variable and the fixed outer
parameter.

After the inner limits, the lowest nonzero `epsilon` coefficient is treated
in the same way. The result is a nonzero rational polynomial of no larger
output degree. A nonzero constant polynomial cannot be the final outcome
when the stated finite limits exist, because the limiting identity would
make that constant zero. No diagonal relation between the perturbation
parameters is implicit in this argument.

Finitely many supports suffice for the nested subsequence choice: choose
one support recurring along an inner sequence for each outer index, then
one recurring along an outer subsequence. This support is selected before
the output linear form. Thus every rational linear combination of the
same limiting coordinates receives the same degree bound. Separate
coordinate degree bounds would not suffice to bound their compositum;
the rational linear form argument avoids that problem. In characteristic
zero the finite field generated by the coordinates has a primitive element
which is a rational linear combination of them. Applying the proved bound
to that element establishes the joint-field assertion.

The objective value belongs to this field because it is a rational
polynomial evaluated at the optimizer. No additional multiplication of
coordinate degrees is needed.

## 3. KKT regularity and the classical count

The support is minimal among nonnegative representations of the negative
objective gradient. Its positive-weight gradient columns are independent:
any linear dependence permits a displacement of the coefficient vector
that preserves its represented gradient and nonnegativity, until one
coefficient becomes zero. The affine restriction bounds the dimension of
the whole constraint-polynomial span by `h`, hence also that of their
gradients evaluated at any point. It follows that `s <= min(h,d)`.

The regularized Lagrangian Hessian is positive definite, and the selected
gradient matrix has full column rank. The Schur complement of the KKT
Jacobian is negative definite. Consequently its selected real roots are
regular roots of the full square polynomial system, even when other
complex KKT components have positive dimension.

The bidegrees `(1,1)` for each stationarity equation and `(2,0)` for each
active equation give exactly

\[
 [U^d L^s](U+L)^d(2U)^s=2^s\binom ds.
\]

I checked the primary statement in Dedieu, Malajovich, and Shub, Section 5,
Theorem 5.1. It bounds isolated zeros in the product of projective spaces;
it does not require every component to have dimension zero. Homogenization
with the stated upper bidegrees agrees with the original system on the
affine chart. A regular affine root remains isolated there and therefore
in the projective zero set. Additional components at infinity do not
invalidate the bound. [Primary source](https://arxiv.org/pdf/math/0312083).

I also checked that Nie and Ranestad's Theorem 2.2 and Corollary 2.5 state
a zero-dimensionality assumption for their nongeneric extension, and that
Section 3.2 gives the same QCQP count. The present count is classical; the
additional argument concerns the Hessian-span reduction and the selected
nongeneric limit. This source comparison does not establish that the full
structural theorem is new. [Primary source](https://arxiv.org/pdf/0802.1233).

The maximum over supports cannot be replaced by the term with `s = h` in
general. For `n = h = 3`, the terms are `1, 6, 12, 8`. The ratio of
successive terms is `2(n-s)/(s+1)`, which verifies the maximizing index
given in the note, including its possible tie. Monotonicity in the ambient
dimension then justifies replacing `d` by `n`.

The boundary cases are valid. With `s = 0`, the regular KKT system is
linear in the primal variables and the count is one. With `d = 0`, the
rational affine chart is a single rational point and no KKT count is
needed. The conventions in the note also cover `n = 0` and `h = 0`.

## 4. Attempts to break the argument

The following small systems isolate the principal failure modes.

- **A positive-dimensional component beside a regular root:** the system
  `u(u-1) = 0`, `u(v-t) = 0` has the entire line `u = 0` and the isolated
  regular root `(1,t)`. Localizing by the Jacobian determinant removes the
  line. The output `u+v` satisfies `w-(1+t) = 0`.
- **A regular root at a degree-dropping parameter:** the equation
  `t u^2 + u - 1 = 0` has a regular root `u = 1` at `t = 0`. For the
  rational output `w = 1/u`, the identity `w^2-w-t = 0` remains valid there.
  Loss of a root at infinity does not remove the finite regular root.
- **Why regularity is necessary:** the equation `t(u^2-2) = 0` has a whole
  line of roots at `t = 0`, including transcendental outputs. Its Jacobian
  in `u` vanishes there. No identity controlling only the two generic
  roots can be extended to every such special root. The note excludes
  precisely this behavior.
- **Why a common polynomial family is necessary:** rational numbers can
  converge to a transcendental number. Their individual degree-one
  certificates need not arise from one fixed polynomial parameter family.
  The characteristic-polynomial construction supplies the missing common
  relation in the present proof.

None of these tests contradicts the stated lemma.

## 5. Verification record and remaining limits

A targeted `python - <<'PY'` command using SymPy and exact integer arithmetic
passed the following checks: localization of the line-plus-point example
by a Groebner basis over `Q(t)`; the rational-output identity at the
degree-dropping exceptional fiber; ordered lowest-coefficient extraction
for `delta^2 epsilon^3 (w^2-2-epsilon-delta)`; and the stated maximizing
support formula for all 1,681 pairs `0 <= n,h <= 40`.

These exact checks exercise the indicated algebraic examples and the
combinatorial formula. They do not prove the general parameter lemma or
its application to every convex quadratic program. Those conclusions
rest on the argument reviewed above. No numerical experiment, project-wide
verification, or CI inspection was used.

The argument itself does not bound coefficient heights. It does not give
a degree bound for every point of a positive-dimensional optimal face,
which can contain transcendental points. The mixed-integer fiber
corollary is a degree statement conditional on an attained optimal integer
assignment; a uniform height or search bound still requires control of
that assignment's size. These limitations are stated in the author note.
