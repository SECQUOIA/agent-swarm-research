# Independent review of the signed odd-root circuit quartic

Date: 2026-09-28. Status: mathematical proof and amended text passed;
no unresolved defect remains.

This review covers the full
[signed odd-root circuit construction](signed-odd-root-circuit-quartic.md),
including its input model, normalization, local and coupled exposing
identities, constants, exact-zero preservation, and polynomial bit
complexity. The reviewed initial source had SHA256
`3fd0a1e94f05691af8066f0700343b00cfa22ff1bcf28906d47deb0a794df70c`.
No blocking mathematical defect was found. This reviewer did not develop
the circuit extension, although the reviewer developed the separate
cyclic quartic construction using the same general regularization tools.
The proof audit does not establish publication priority or provide a
Lean formalization.

## Input model and coordinate scope

The algorithm receives the rational gate data, odd degrees in unary,
and rational interval certificates avoiding zero. It checks interval
containment using all retained predecessor powers, including signs.
These checks imply that the recursively defined unique odd roots lie
in the supplied intervals. The theorem does not claim that the
intervals can be found in polynomial time from an arbitrary signed
arithmetic circuit.

The certificate's distance from zero is part of its binary encoding.
If that distance requires exponentially many bits relative to some
smaller circuit description, the theorem does not promise polynomial
cost in the smaller description. This distinction is essential for
the derivative and approximation bounds and is stated correctly.
Unary degree encoding also matters: the algorithm explicitly introduces
$(d_i+1)/2$ coordinates for gate $i$ and computes rational powers
with exponents of that order.

For a negative box, multiplication by $\sigma_i\kappa$ reverses
its endpoints and makes it positive. The equation transforms as

\[
 (\sigma_i\kappa\xi_i)^{d_i}
 =\sigma_i\kappa^{d_i}c_i+
 \sum_{j<i,e}\sigma_i\sigma_j^e\kappa^{d_i-e}
             a_{ije}\alpha_j^e.
\]

Oddness of $d_i$ and $\sigma_j^{-e}=\sigma_j^e$ give exactly
the coefficients in the note. This holds for negative as well as
positive gate values. Taking exact interval powers before or after
the sign and scale change gives the same transformed ranges, with
endpoint reversal where needed. Thus the normalized radicand intervals
are at least one; this is not an assumption inferred merely from the
value at the true point.

The original retained values are recovered through the rational map

\[
 \xi_i^e=(\sigma_i/\kappa)^eX_{i,e}.
\]

The stated Hessian lower bound is for the normalized variables $X$.
It does not automatically have the same constant after an arbitrary
diagonal coordinate change. The theorem correctly provides the recovery
map separately. I requested that the certificate paragraph say
"uncentered normalized $X$ variables" instead of "original variables",
and that the optional original boxes be imposed through
$\xi_i=\sigma_iX_{i,1}/\kappa$. These clarify the existing result
rather than alter it.

## Residual rank and local exposing identity

The $N$ chain and terminal residuals have a unique common real zero.
The chain enforces all powers, and each terminal equation enforces
one unique odd root after its predecessors are fixed. In the block
Jacobian the determinant is
$\prod_i d_i\alpha_i^{d_i-1}\geq1$. Each entry has magnitude at
most $2A^N$, including signed predecessor coefficients. Thus
$\|J\|_F\leq2NA^N\leq V=4NA^N$. The product-of-singular-values
bound then gives $\sigma_{\min}(J)\geq V^{-(N-1)}=\nu$.
This checks the full matrix norm, rather than using an individual
gradient bound as though it were an operator bound. Every residual's
homogeneous quadratic matrix has norm at most one.

For one gate, the congruence
$T_\alpha=D T_0D$ is exact, with $D$ as in the note. The Toeplitz
matrix $T_0$ has minimum eigenvalue
$1-\cos(\pi/(n+1))\geq1/(n+1)^2$.
Because $\alpha\geq1$, its congruence preserves this lower bound.
On the power curve, the diagonal terms of
$\ell^{\mathsf T}T_\alpha\ell$ produce the even powers in the
geometric sum, and its doubled off-diagonal terms produce the odd
powers. Therefore

\[
 P_\alpha(t,\ldots,t^n)=(t-\alpha)(t^{2n-1}-\alpha^{2n-1}).
\]

The centered difference map is lower bidiagonal with diagonal one
and subdiagonal $-\alpha$. Its inverse entries have magnitude at
most $A^{n-1}$, giving the bound $nA^{n-1}$ on its norm. Consequently
the common local lower bound $h_0$ in the note is conservative.
The upper bound $L_0$ is also conservative: use
$\|T_\alpha\|\leq2A^{d-1}$ and difference-map norm at most $1+A$.

The affine predecessor dependence is fully retained. Expanding

\[
 P_{\alpha_i}(X_i)+(\alpha_i-X_{i,1})
                      (b_i(X)-\alpha_i^{d_i})
\]

at the complete circuit point gives the local centered form and
exactly the cross term
$-u_{i,1}\sum_{j<i,e}a_{ije}u_{j,e}$. Both the constant term
and every gradient component vanish, including predecessor directions.
No radicand is improperly treated as constant during differentiation.

The representative map $M\mapsto m_{w(M)}$ is linear on the
monomial expansion. Applying it to the displayed power-curve identity
gives the four representatives for weights $2n,2n-1,1,0$.
Rearranging gives the exact rational-residual formula
$E_i^*=S_i-\alpha_iT_i+\sum_M\beta_M(\alpha_i)R_M$.
Every residual in this formula vanishes at the true circuit point.
Therefore approximating its coefficients leaves the zero exact,
even though the approximation no longer has exactly zero gradient.

## Constants and the coupled quadratic

Before combining like monomials, each diagonal term of
$\ell^{\mathsf T}T_\alpha\ell$ contributes at most four to
the coefficient absolute sum, and each neighboring term contributes
at most four. Thus the total is below $8n$; cancellations only reduce
it. The coefficient degrees are at most $2n$. On root approximations
within one of the true value, the derivative coefficient sum is
therefore bounded by $16N^2(A+1)^{2N}$. Multiplying by the coefficient
norm bound two for $R_M$, and adding the terminal residual's norm
$A+1$, proves the stated $B_0$ bound.

After scaling each gate block by $\sqrt{\omega_i}$, a cross
coefficient joining gates $j<i$ is multiplied by
$\rho^{(i-j)/2}$, not its reciprocal. There are at most $N$ such
entries in a row. Their row-sum bound $NA\sqrt\rho/2=h_0/4$
is valid even with signed coefficients and access to every retained
predecessor power. The scaled exposing matrix is at least
$3h_0I/4$; scaling back gives the weaker stated gap
$\gamma=h_0\rho^{k-1}/2$. The upper bound $W$ follows by summing
local norms and absolute cross coefficients.

For a quadratic coefficient error of absolute sum $E$, its quadratic
matrix has norm at most $E$, and its gradient error at the point has
norm at most $2A^NE$. The latter follows term by term, including
linear and mixed quadratic monomials. No omitted factor of $\sqrt N$
is needed. The chosen $\theta$ gives quadratic-part error at most
$\gamma/4$ and gradient error at most $\varepsilon/2$, so the
weaker inequalities stated in the note follow.

The regularization condition uses $N$ both as ambient dimension and
as the number of residuals, consistently with the imported quartic
and block-Gram lemmas. It supplies the curvature bound
$\nabla^2F\succeq(3/2)I$, and the explicit rational factors in
the note number $N+1$. Their exact common zero proves uniqueness.
The positive definite quadratic part of $G$ ensures degree exactly four.

## Approximation and certificate cost

For every maintained normalized box, $1\leq x\leq A$.
The retained power derivatives are bounded by $eA^{e-1}$, and the
total radicand coefficient absolute sum is at most $A$. Consequently
the radicand-width multiplier $C=NA^N$ is valid for signed coefficients.
Interval evaluation is inclusion-preserving: replacing the supplied
predecessor boxes by subintervals retains the initial certificate's
lower bound one. The odd-root derivative is therefore at most one
throughout each evaluated interval.

Exact bisection of the increasing rational-power comparison on a
supplied normalized box gives each endpoint enclosure to outward
error $\eta$. Intersection with the given box keeps the true root.
The recurrence in the note follows, and
$\eta=2^{-P}/[4k(C+1)^k]$ yields narrower intervals than required.
The comparison exponents are unary-sized. Bisection endpoint precision,
coefficient denominators, and exact affine interval evaluations all
have polynomially many bits. No dense minimal polynomial is used.

The logarithms of all conditioning bounds are polynomial in the
specified input size: in particular $N\log A$,
$k\log(1/\rho)$, and $(N-1)\log V$ are polynomial. Evaluating
the local coefficient polynomials at rational approximate roots and
forming the weighted sum therefore has polynomial cost and output size.

Once these rational quadratics are fixed, the centered Hessian Gram
has constant block quadratic in the center, cross block affine in
the center, and quartic block independent of it. Translating to the
uncentered $X$ basis preserves degree at most two in the formal center
coordinates. The imported positive Schur margin and the shift norm
bound $\|p\|\leq NA^N$ give an inverse-exponential gap with
polynomial bit length. Derivative coefficient bounds then require only
polynomially many additional center bits. The same certified root
algorithm supplies them; controlling retained powers uses
$N(A+1)^N$. Exact rational coefficient projection and positivity
are justified by the reviewed Gram construction. This is a rational
linear-algebra calculation of polynomial dimension, with no hidden
common-field expansion or exact semidefinite optimization oracle.

## Distinct targeted check and limits

The retained [independent checker](check_signed_odd_root_review.py)
was run with

```text
python research-20260927/check_signed_odd_root_review.py
```

It uses the exact original roots $\xi_1=-1/2$, $\xi_2=3/4$ with
degrees three and five, the signed second radicand
$2035/1024+2\xi_1-3\xi_1^2$, and the boxes
$[-51/100,-49/100]$ and $[7/10,4/5]$.
It checks the original interval certificate, transformed coefficients
and intervals, and recovery of every retained original power.
It verifies complete gradient cancellation, the exact global exposing
margin by rational LDL decomposition, the coupled Jacobian determinant
and Frobenius bound, and exact-zero preservation after rational
coefficient perturbation. The coefficient and gradient error bounds
and the retained positive quadratic margin also passed.

This computation specifically tests negative gate normalization and
signed dependence on multiple predecessor powers, which the author's
local positive-root tests do not cover. It does not verify all circuit
sizes, the general complexity bound, or the final rational Hessian
Gram construction. Those are covered by the algebraic audit above and
the cited certificate lemma. No project-wide verification, CI
inspection, or Lean checking was run.

The result expands the circuit representation covered by the quartic
lift. It gives neither a method to find the required interval certificates
for arbitrary signed circuits nor a decision-complexity lower bound.
A separate literature comparison is still required for novelty claims.

The author incorporated the two coordinate clarifications. I re-read
the amended passages and checked the resulting main-source SHA256:
`116f6ec976b9ece0e2e63630dfa57e4c49dbff5313b1b5e01a9435809d038012`.
The Hessian certificate is now explicitly described in uncentered
normalized $X$ coordinates, and the original boxes are imposed through
the rational recovery map. These edits change no formula, estimate,
or computational conclusion.
