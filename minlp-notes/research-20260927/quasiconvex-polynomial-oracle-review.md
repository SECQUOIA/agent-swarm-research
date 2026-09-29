# Independent review of the quasiconvex implicit-row oracle

Date: 2026-09-28. Scope: Section 3 of the
[quasiconvex polynomial extension](quasiconvex-polynomial-nonlinear-dimension-frontier.md).
This reviewer did not develop the proposed construction. The review
reconstructed its geometric and arithmetic arguments, read the existing
[convex oracle audit](polynomial-nonlinear-dimension-oracle-audit.md) and
[independent recursion review](polynomial-nonlinear-dimension-oracle-review.md),
and checked the relevant primary Hildebrand--Koppe text.

**Finding.** No substantive gap was found in the quasiconvex shallow-cut
construction or its transfer through the already reviewed integer
recursion. The uniform degree and coefficient bounds, exact strict
membership interface, and global quasiconvexity are essential hypotheses.
The geometric search is established machinery: Hildebrand--Koppe already
give the constant-line fact, the supporting-gradient fact, and the two
cases of the nearby-point search. The rational LDL construction makes that
machinery explicit for the present implicit-row interface; this review
does not support a novelty claim for shallow-cut separation itself.

This review assumes the separate projection, radius, residual-gap, and
mesh arguments. It does not independently certify the full optimization
or common-field recovery conclusions of the main note.

## 1. The interface actually needed

Let

\[
 Y=\{x\in\mathbb R^s:F_j(x)<0\text{ for every }j\},
\]

where the fixed finite family consists of globally quasiconvex integer
polynomials of degree at most \(D\) and individual coefficient bit length
at most \(H\). The number of rows may be exponential. At a rational
point, the oracle must either certify membership in this strict set or
return an explicit member of this same family with value at least zero.
An oracle for a different weak set would not suffice.

The selected row remains fixed for all evaluations and derivatives in
the current shallow-cut call. No derivative of a changing LP multiplier
or a pointwise maximum is taken. Only the initial \(2s\) test points
need calls to the full membership oracle. Subsequent computations use the
one returned polynomial.

Assume \(s\ge1\) and \(D\ge1\); the application takes \(D\ge2\).
Dimension zero is handled by direct strict membership, and a constant
violated row certifies emptiness immediately.

## 2. The constant-line argument is valid

Suppose the globally quasiconvex polynomial \(F\) is constant on
\(a+\mathbb Rb\). Fix an arbitrary \(x\), and let

\[
 \alpha=\max(F(a),F(x)),\qquad C=\{y:F(y)\le\alpha\}.
\]

The set \(C\) is closed and convex, contains \(x\), and contains the
complete line. For every real \(t\) and integer \(n\ge1\), it contains

\[
 (1-1/n)x+(1/n)(a+ntb).
\]

Taking \(n\to\infty\) proves \(x+tb\in C\). Hence the univariate
polynomial \(q(t)=F(x+tb)\) is bounded above on the whole real line.
It remains quasiconvex because affine restrictions preserve sublevels.

A nonconstant univariate polynomial of odd degree is unbounded above
in one direction. One of even degree with positive leading coefficient
is unbounded above in both directions. If its even leading coefficient
is negative, both tails tend to minus infinity. Choosing two sufficiently
distant endpoints around any fixed interior point then violates
quasiconvexity. Thus a globally quasiconvex polynomial bounded above on
the whole line must be constant.

It follows that \(F\) is invariant in direction \(b\) at every base
point. If each restriction \(F(c+tb_i)\) is constant for a basis
\(b_1,\ldots,b_s\), apply these invariances successively to show that
\(F\) is globally constant. This is why inspecting only these basis
lines suffices.

The global quasiconvex assumption cannot be omitted. The polynomial
\(F(x_1,x_2)=x_1x_2\) is constant on both coordinate axes through zero
and is not constant on the plane. Nor is the bounded-above step a fact
about arbitrary univariate quasiconvex functions: a strictly increasing
bounded function gives a counterexample outside the polynomial class.

## 3. Rounding geometry and the two search cases

Write the rational containing ellipsoid as

\[
 E(A,c)=\{x:(x-c)^TA^{-1}(x-c)\le1\},\qquad A\succ0.
\]

For a rational LDL factorization \(A=L\operatorname{diag}(a_i)L^T\),
choose positive dyadic \(t_i\) with
\(\sqrt{a_i}/2\le t_i\le\sqrt{a_i}\), and set \(b_i=t_iLe_i\).
These are a basis, orthogonal in the \(A^{-1}\) inner product, whose
lengths lie in \([1/2,1]\). The test points

\[
                  c\pm b_i/[2(s+1)]
\]

have ellipsoidal radius at most \(1/[2(s+1)]\). If all are strictly
feasible, quasiconvexity of each row puts their complete convex hull in
\(Y\). After transforming the ellipsoid to the unit ball, this hull
has orthogonal half-axes of length at least \(1/[4(s+1)]\). It contains
a ball of radius \(1/[4\sqrt{s}(s+1)]\), so the conservative rational
rounding ratio \(\beta=4s(s+1)\) is valid. The closed inner ellipsoid
is contained in the strict set; this is stronger than containment in its
closure.

Otherwise fix a returned row \(F\) and its violated test point \(y\).

If \(F(c)<0\), the polynomial \(q(t)=F(c+t(y-c))\) is nonconstant,
with \(q(0)<0\) and \(q(1)\ge0\). For every \(t>1\), it has
\(q(t)\ge0\): a negative value there would place the point at parameter
one between two points in the convex strict sublevel. A nonzero derivative
of degree at most \(D-1\) cannot vanish at all \(D\) points

\[
                      1+j/(D+1),\qquad 1\le j\le D.
\]

At one of them, \(w=c+t(y-c)\) satisfies \(F(w)\ge0\) and
\(\nabla F(w)\ne0\). The factor \(t<2\) keeps its ellipsoidal
radius strictly below \(1/(s+1)\).

If \(F(c)\ge0\), first test the restriction coefficients to determine
whether all \(q_i(t)=F(c+tb_i)\) are constant. If so, Section 2 proves
that \(F\) is a nonnegative constant and the family is empty. Otherwise
fix one nonconstant restriction and evaluate at

\[
                t_j^\pm=\pm j/[(D+1)(s+1)],\qquad 1\le j\le D.
\]

One entire finite sample side has nonnegative values. Indeed, a negative
sample on each side would put the center in the convex strict sublevel.
On the nonnegative side, at least one of the \(D\) derivative evaluations
is nonzero. That sample again supplies a violated point with nonzero
gradient and ellipsoidal radius strictly below \(1/(s+1)\).

No claim that a nonconstant quasiconvex polynomial has a nonzero gradient
at every violation is used. The basic counterexample is \(F(x)=x^3\)
at zero. The procedure explicitly handles this case.

## 4. The returned normal gives the required cut

For any \(x\in Y\), quasiconvexity gives

\[
 F(w+\lambda(x-w))\le F(w),\qquad 0\le\lambda\le1.
\]

Differentiation at \(\lambda=0\) gives
\(g^T(x-w)\le0\), where \(g=\nabla F(w)\ne0\). The
ellipsoidal Cauchy--Schwarz inequality yields

\[
 Y\subseteq\{x:g^Tx\le g^Tw\}
 \subseteq\left\{x:g^Tx\le g^Tc+
                  \frac{\sqrt{g^TAg}}{s+1}\right\}.
\]

These weak cuts also contain the closure of \(Y\). The computed normal
and the stronger offset \(g^Tw\) are rational. The square-root expression
describes the shallow-cut guarantee and need not be encoded exactly.
The argument proves a weak supporting inequality; a strict one should
not be substituted without an additional justification.

## 5. Bit bounds and recursion

If the rational ellipsoid entries have at most \(H_E\) bits, rational
minor bounds give LDL data with at most \(f(s)(H_E+1)\) bits. A dyadic
square root within a factor of two can be found by comparing powers of
four with the positive rational diagonal entry. Its exponent magnitude,
and therefore its binary encoding length, obey the same bound.

The sample parameters add only \(O(\log(D+1)+\log(s+1))\) bits.
A degree-\(D\) polynomial has at most \(\binom{s+D}{D}\) monomials.
Substitution into a rational line, exact coefficient tests, evaluation,
and differentiation therefore have coefficient and output bit bounds

\[
                         f(s,D)(H+H_E+1).
\]

The dependence on both varying bit bounds is linear. The number of
arithmetic operations is parameter-bounded apart from the supplied
membership cost, and the bit-operation exponent is absolute. These bounds
do not depend on the number of implicit rows.

The remaining integer-recursion requirements transfer unchanged:
affine restrictions preserve quasiconvexity; positive denominator clearing
preserves signs; strict integer values supply the uniform negative margin;
and gradient size bounds, rather than convexity of the polynomials,
provide the conditional volume threshold. The independently reviewed
rational quadratic lattice subroutines, short unimodular section maps,
fresh bounding balls, and controlled ellipsoid rounding can therefore use
this oracle with the same linear height recurrence. This statement relies
on those reviewed recursion results; it is not a new independent proof of
their lattice or precision theorems.

## 6. Prior comparison and verification record

The primary source inspected was
[Hildebrand--Koppe, *A new Lenstra-type Algorithm for Quasiconvex Polynomial
Integer Minimization*](https://arxiv.org/pdf/1006.4661), Sections 5.2--5.3,
also available locally as `common-range-prior-sources/hildebrand-koppe.txt`.
Lemma 5.2 already states global invariance from one constant line, and
Corollary 5.3 uses basis-line derivative samples to detect a constant
polynomial. Lemma 5.4 supplies the supporting-gradient inequality.
Theorem 5.7, Cases 2.1--2.2, gives the same two-case nearby-gradient
search. The present construction changes the rational coordinate and
sampling details and supplies an implicit-row interface; no new
quasiconvex geometry is being claimed.

A targeted inline `python -` command using exact SymPy rational arithmetic
checked six instances: the stationary boundary of \((x-1)^3\), the
decreasing row \(-x^3\), a stationary boundary of
\((9x^2+9y^2-4)^3\), a noncentral stationary boundary of
\((x^2+y^2-1)^3\), a constant violated row, and an inner-rounding
certificate. Both search branches returned violations with nonzero
gradients and squared ellipsoidal radius below \(1/(s+1)^2\).
Their cuts were also checked on finite exact feasible sample sets. All
six final checks passed. An initial test incorrectly expected a violated
test point where all test points were strictly feasible; correcting that
test setup required no change to the argument.

These examples challenge specific algebraic and boundary cases. They do
not establish the general theorem, certify input quasiconvexity, or verify
the asymptotic bit bound. Those conclusions rest on the proofs above and
the stated imports. A separate targeted inline `python -` document check
passed for all three local links, balanced math delimiters, whitespace,
control characters, and the final newline. No project-wide verification,
CI inspection, or Lean formalization was performed.
