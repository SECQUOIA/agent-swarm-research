# Adversarial review of the canonical optimizer field bound

Date: 2026-09-27. Scope: independent proof reconstruction and adversarial
checks of [the ordered-perturbation theorem](ordered-perturbation-optimizer.md).
The reviewer read the complete draft and the underlying
[explicit elimination lemma](explicit-span-separation.md). A separately
delegated reviewer checked the ordered-limit lemma and proposed the exact
stress test below. No substantive mathematical gap was found.

The reviewed claim is that the minimum-norm optimizer of a rational convex
quadratic program with a finite attained optimum has joint field degree at
most \((2n+1)^{\min(h,n)}\) and coordinate minimal-polynomial coefficient
bit lengths \(N^{O(h+1)}\). Here `h` counts the span of native constraint
Hessians, excluding the objective Hessian. The draft obtains finite attainment
from the separately audited classical convex-quadratic attainment result.

## Active restriction and the selected norm

The native-active restriction preserves the lexicographic pair
\((q_0,\|x\|^2)\). If a retained-feasible point improved the objective,
a sufficiently short segment from the original optimizer would retain every
deleted row by its strict slack and improve the original problem. If it had
the same objective and smaller norm, that segment would give an original
optimizer of smaller norm. A distinct point of equal objective and equal norm
would do so by strict convexity of the squared norm. Thus the canonical
optimizer remains unique after deletion of inactive rows.

The additional Hessian-basis difference equations are rational, vanish at
the canonical optimizer, and only restrict this retained set. Rational affine
elimination has polynomial coefficient bit length without knowing the
optimizer's coordinates. On its chart \(x=x_0+Vu\), the retained native
polynomials span at most `h` dimensions as whole polynomials. The subsequent
regularization must use \(\|x_0+Vu\|^2\). Regularizing by \(\|u\|^2\)
would generally select a different optimizer.

## The inner and outer compactness arguments are distinct

On the exact retained feasible set, the objective is at least \(\theta\).
Let \(x_\varepsilon\) minimize
\(q_0(x)+\varepsilon\|x\|^2\) there. Comparison with the canonical
optimizer \(x^*\) gives

\[
 \|x_\varepsilon\|\le\|x^*\|,
 \qquad
 0\le q_0(x_\varepsilon)-\theta\le\varepsilon\|x^*\|^2.
\]

This proves boundedness of the outer sequence. Every cluster point is a
retained optimizer of no larger norm and hence equals \(x^*\).

For each fixed positive \(\varepsilon\), the relaxed problem with
\(q_i\le\delta\) has a strictly convex coercive objective. Its minimizers
belong to the sublevel set through \(x_\varepsilon\), which is feasible
for every positive \(\delta\). This compact set may depend arbitrarily
on \(\varepsilon\). Every cluster point as \(\delta\downarrow0\)
is retained-feasible and minimizes the exact-feasible regularized objective,
so uniqueness gives convergence to \(x_\varepsilon\).

No uniform inner convergence rate, simultaneous compact bound, or chosen
diagonal path is required. In particular, the inequality \(q_0\ge\theta\)
cannot be applied to the relaxed points; the draft correctly applies it only
to the exact-feasible outer sequence.

## The same support works for all nested coordinate limits

For each positive parameter pair, Slater's condition supplies KKT
multipliers. A representation of the negative objective gradient with
minimum active-gradient support has independent supported gradients and
positive weights. Its size is at most \(\min(h,d)\), where `d` is the
chart dimension. Independence concerns numerical gradients, not merely
Hessian coefficient vectors.

For every outer parameter value, select an inner subsequence with fixed
support. Then select an outer subsequence whose support is the same. Finitely
many supports justify both choices. This gives one support and one pair of
nested sequences for every coordinate and every rational linear combination.
It does not assert a support valid on an entire parameter neighborhood.

At these roots, the Lagrangian Hessian includes
\(2\varepsilon V^TV\succ0\). With \(u=p/\Delta\), the active
multiplier equations satisfy

\[
 \frac{\partial G_i}{\partial\lambda_j}
 =-\Delta^2\nabla q_i(u)^TM^{-1}\nabla q_j(u).
\]

Their Jacobian is negative definite. Thus the selected roots are
nonsingular even if other complex components of the same equations are
singular or have positive dimension. No lower bound on this Jacobian or
the nonzero determinant \(\Delta\) is needed. Multipliers may diverge.

## Exceptional specializations do not invalidate extraction

Treat \(\varepsilon\) and \(\delta\) as coefficient indeterminates,
and deform the multiplier equations using a separate parameter \(\beta\).
The proof of the explicit elimination lemma then gives a nonzero polynomial
\(R(\varepsilon,\delta,w)\), after its lowest nonzero \(\zeta\) and
\(\beta\) coefficients are taken. It vanishes at the selected ratios
for every selected parameter pair. The implicit-function neighborhood can
depend on that pair; it is used only to take the local \(\beta\)-limit.

Write

\[
 R(\varepsilon,\delta,w)
   =\delta^r S(\varepsilon,w)+O(\delta^{r+1}),\qquad S\ne0.
\]

For fixed \(\varepsilon_l\), divide the selected identities by the
nonzero \(\delta_{lj}^r\) and take the finite inner ratio limit. This
gives \(S(\varepsilon_l,w_l)=0\). If specialization makes
\(S(\varepsilon_l,w)\) identically zero, the resulting identity is
vacuous but remains valid. Writing

\[
 S(\varepsilon,w)=\varepsilon^tP(w)+O(\varepsilon^{t+1}),
 \qquad P\ne0,
\]

and taking the outer limit after division by \(\varepsilon_l^t\)
gives \(P(w^*)=0\). Positivity in the application ensures that the
parameter divisions are valid. Each remainder is a polynomial evaluated at
a bounded ratio sequence in the limit being taken. This argument does not
interchange the two limits or exclude special parameter values.

## Degree, height, and the common field

The common denominator \(A=\Delta^2\) and original-coordinate
numerators

\[
 B_j=\bigl(x_{0j}\Delta+(Vp)_j\bigr)\Delta
\]

have multiplier degree at most \(a=2d\), as do the active equations.
The deformed quotient therefore has dimension
\(L=(a+1)^s\le(2n+1)^{\min(h,n)}\).

The coefficient norm estimate does not acquire an extra exponent from the
second coefficient parameter. Each normal-form replacement multiplies the
full polynomial coefficient \(\ell_1\)-norm by at most \(2^\tau\),
and the reduction depth is at most \(T=a(s+1)\). Consequently the existing
determinant estimate still gives

\[
 K=L\bigl[\tau(T+1)+2+\lceil\log_2L\rceil\bigr].
\]

The integer annihilator has norm at most \(2^K\). Rational affine
elimination and determinant expansion give \(\tau=N^{O(1)}\),
including common rational-denominator clearing. Hence
\(K=N^{O(h+1)}\). Passing to the primitive minimal polynomial requires
an integer factor bound; it preserves the asymptotic estimate, though the
identical numerical `K` need not be preserved. The draft makes that
distinction correctly.

Every rational linear combination of the coordinate numerators uses the
same support and nested limits and has the same multiplier degree. Its
coefficients can increase the height bound but cannot change `L`. Each
coordinate is algebraic, and the primitive element theorem supplies a rational
linear combination generating their field. Thus the joint degree is at most
`L`, rather than a product of separate coordinate degrees. The optimal value
belongs to this field because the objective has rational coefficients.

For `d=0`, the affine chart is a rational point. For `s=0`, the quotient has
dimension one; equivalently, one can extract the ordered coefficients of
\(Aw-B\) directly. Both cases give the stated degree-one bound.

## Exact stress test with diverging multipliers

The separately delegated reviewer proposed

\[
 G=\delta\lambda-1,\qquad
 A=1+\varepsilon\lambda,\qquad B=\varepsilon\lambda.
\]

The selected root \(\lambda=1/\delta\) is nonsingular for positive
parameters and diverges in the inner limit. Its ratio is
\(w=\varepsilon/(\varepsilon+\delta)\). Taking the positive
\(\delta\)-limit first and then the positive \(\varepsilon\)-limit
gives one; reversing the limits gives zero.

Here \(a=s=1\). Deform by \(\beta\lambda^2\), use quotient basis
\((1,\lambda)\), and clear multiplication matrices by \(\beta^2\).
The exact determinant is

\[
 H=\beta^3\left[\beta(w-\zeta)^2
 -\delta\varepsilon(w-1)(w-\zeta)
 -\varepsilon^2(w-1)^2\right].
\]

The lowest \(\zeta\) and then \(\beta\) coefficients give

\[
 R=-\varepsilon(w-1)[\delta w+\varepsilon(w-1)].
\]

Its lowest \(\delta\) coefficient is
\(-\varepsilon^2(w-1)^2\). Extracting the lowest \(\varepsilon\)
coefficient gives \(-(w-1)^2\), which retains the required limit.
This is a stress test of the algebraic lemma, not itself an optimizer
construction. It illustrates why the order of extraction matters.

Both reviewers independently checked this determinant and its limits with
exact SymPy arithmetic. The saved
[targeted script](check_ordered_perturbation_optimizer.py) also checks the
quotient multiplication identity and substitution of the selected ratio into
`R`.

## Scope and verification record

This review establishes no publication-priority claim. Strictly convex norm
regularization, ordered perturbations, and finite-algebra elimination are
established techniques. The separate literature review is responsible for
comparison with their strongest known forms.

The theorem bounds the encoding of one selected point. It does not itself
find the active restriction, construct coordinate expressions in a common
number field, give a practical numerical speedup, or establish the same
exponent for the complete recovery algorithm. Applying it to a mixed-integer
optimum requires an attained optimal integer assignment. Its bit length
enters the height estimate after substitution, though not the field-degree
formula.

The general proof was checked symbolically. Ran
`python research-20260927/check_ordered_perturbation_optimizer.py`; every
assertion passed. These calculations verify the stated example, not the
general theorem. No floating-point experiment or Lean proof is asserted.
Targeted document checks cover local links, final newline, trailing
whitespace, control characters, and balanced display-math delimiters. No
project-wide checks or CI inspection were run.
