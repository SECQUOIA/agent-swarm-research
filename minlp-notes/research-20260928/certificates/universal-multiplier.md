# Adaptive multipliers: a scale obstruction and unresolved degree question

Date: 2026-09-28. Status: supporting deduction passed
[independent adversarial review](universal-multiplier-review.md). No universal adaptive degree theorem or growing-dimension degree
lower bound is proved here. Publication priority is unestablished.

The earlier scaling family requires arbitrarily large powers of the
fixed radial multiplier, while a quadratic multiplier chosen for each
instance suffices. The degree question therefore has to distinguish a
fixed multiplier from a multiplier that can depend on the input. This
note records a consequence for the coefficients of every bounded-degree
adaptive certificate and preserves several unsuccessful degree routes.

## 1. Setup inherited from the reviewed example

Use the integer quartic

\[
\begin{aligned}
r&=(2-2xy,\ 2x^2-2yz,\ 2y^2-4z,\ 2z^2-x,\ 2xz-y),\\
A&=4r_0+5r_1+3r_2+9r_3,\\
F&=A^2+\sum_{i=0}^3r_i^2-r_4^2,
\end{aligned}
\]

and set \(f_t(X)=t^{-2}F(tX)\) for integers \(t\geq1\).
The [reviewed radial-order note](../../research-20260927/rational-radial-exponent-obstruction.md)
establishes all of the following facts used here:

- Every \(f_t\) is strongly SOS-convex over the rationals, has Hessian
  at least the identity, and has a unique zero \(p/t\), where
  \(p=(a^{-1},a,a^{-3})\) and \(a=2^{1/5}>0\).
- If \(I_s(p)\) is the rational space of degree-at-most-\(s\)
  polynomials vanishing at \(p\), and
  \(V_s=\operatorname{span}_{\mathbb R}I_s(p)\), then
  \[
  C_s=\{\textstyle\sum_j u_j^2:u_j\in V_s\}
  \]
  is closed in coefficient space and does not contain \(F\), for
  every integer \(s\geq2\).
- \(R_t=1+t^2\|X\|^2\) gives a rational SOS multiplier and a
  pole-free common denominator for \(f_t\).

Closedness refers to this cone with rational vanishing constraints
extended to real coefficients. The ordinary real SOS cone contains
\(F\); replacing \(C_s\) with that larger cone would invalidate the
argument below.

## 2. Bounded-degree adaptive certificates require coefficient growth

Fix an integer \(d\geq2\). Coefficients use the ordinary monomial
basis. Constants in the statements can depend on \(d\) and the fixed
polynomial \(F\), but not on \(t\) or the chosen certificate.

**Proposition.** There is \(c_d>0\) such that both statements below
hold for every integer \(t\geq1\).

1. Suppose \(h\in\mathbb Q[X]\) has degree at most \(d\), is
   nonnegative on \(\mathbb R^3\), satisfies \(h(0)>0\), and
   \(h f_t\) is rational polynomial SOS. Then
   \[
   \max_{2\leq|\alpha|\leq d}
   \frac{|h_\alpha|}{h(0)}\ \geq\ c_d t^2.                 \tag{1}
   \]
2. Suppose \(q\in\mathbb Q[X]\) has degree at most \(d\), has
   no real zeros, and \(q^2 f_t\) is rational polynomial SOS.
   Then
   \[
   \max_{2\leq|\alpha|\leq d}
   \left|\frac{q_\alpha}{q(0)}\right|\ \geq\ c_d t^2.    \tag{2}
   \]

The common choice of \(c_d\) can be obtained by decreasing the two
constants from the separate proofs.

**Proof of (1).** Divide \(h\) by its positive constant value and
write the result as
\[
H(X)=1+\sum_{i=1}^3 b_iX_i+
               \sum_{2\leq|\alpha|\leq d}c_\alpha X^\alpha.
\]
Multiplication of a rational SOS by a positive rational scalar
preserves rational SOS. After the substitution \(X=x/t\), the
certificate assumption therefore implies
\[
                         H(x/t)F(x)\in C_s,
\qquad s=\left\lceil\frac{d+4}{2}\right\rceil.           \tag{3}
\]
Every rational square factor vanishes at \(p\), since the product
vanishes there. Its degree is at most \(s\), by the absence of
cancellation between leading real squares. These facts justify (3).

Since \(C_s\) is closed and does not contain \(F\), continuity of
coefficient multiplication supplies an \(\eta>0\) such that
\[
\max_{\alpha\ne0}|U_\alpha|\leq\eta,
\quad U(0)=1,\quad \deg U\leq d
\quad\Longrightarrow\quad UF\notin C_s.                 \tag{4}
\]
Choose a real \(R\geq\max\{1,2/\eta\}\), and set
\[
S_d(R)=\sum_{k=2}^d R^{k-1},\qquad
c=\min\left\{\eta,\frac{\eta}{2S_d(R)}\right\}>0.
\]
Suppose, towards a contradiction, that
\[
B:=\max_{2\leq|\alpha|\leq d}|c_\alpha|/t^2\leq c.
\]
All degree-at-least-two coefficients of \(H(x/t)\) then have
absolute value at most \(B\), because \(t\geq1\). Nonnegativity
at the two points \(x=Re_i\) and \(x=-Re_i\) gives
\[
\frac{|b_i|}{t}\leq\frac1R+B\sum_{k=2}^dR^{k-1}
                         \leq\eta\qquad(1\leq i\leq3).
\]
Indeed, only pure powers of \(x_i\) survive at these two points;
bounding their contributions by absolute values gives the displayed
inequality regardless of the signs of the coefficients. Thus every
nonconstant coefficient of \(H(x/t)\) has magnitude at most
\(\eta\), contradicting (3)--(4). Hence \(B>c\), proving (1).

**Proof of (2).** The real polynomial \(Q=q/q(0)\) is positive
everywhere: it is continuous, never zero, and equals one at the
origin. The certificate gives
\[
                              Q(x/t)^2F(x)\in C_{d+2}.
\]
Continuity now supplies \(\eta>0\) such that every degree-at-most-
\(d\) polynomial \(U\) with constant term one and nonconstant
coefficients bounded by \(\eta\) satisfies
\(U^2F\notin C_{d+2}\). Repeat the positivity argument above for
\(Q\). This proves (2). \(\square\)

The proof is existential in \(c_d\). It gives neither a useful
numerical constant nor a uniform bound when \(d\) is allowed to
increase with \(t\).

For fixed degree, the coefficient norm and the supremum norm on the
unit cube are equivalent. Thus (1) also implies
\[
\frac{\max_{[-1,1]^3}h}{h(0)}\geq c'_d t^2,
\]
and (2) gives the same estimate for \(|q|/|q(0)|\). If a multiplier
is strictly positive on the cube, the ratio between its maximum and
minimum is at least this large. Scaling the whole multiplier by a
constant does not remove the ratio. For pole-free common denominators,
the exhibited quadratic \(R_t\) has coefficient ratio and cube
maximum of order \(t^2\), so the exponent two is sharp for this
coefficient-growth statement.

After normalization at the origin, representing a coefficient of
magnitude at least \(c_d t^2\) requires \(\Omega(\log t)\) bits
for fixed \(d\). This is only linear in the input bit length of the
family. It is not an exponential encoding lower bound or a numerical
algorithm lower bound.

## 3. What this does not resolve

The proposition rules out uniformly bounded normalized coefficients
for all bounded-degree pole-free adaptive certificates of the scaling
family. It does not rule out bounded adaptive degree; the family has
degree-two examples. Multipliers that vanish at the origin are outside
(1), and denominators with real zeros are outside (2). These are
material restrictions, not removable conveniences in this argument.

For an algebraic zero \(p\), a proposed degree-\(2r\) multiplier
for a quartic must satisfy the necessary
condition
\[
hf\in\operatorname{span}_{\mathbb Q}
               \{uv:u,v\in I_{r+2}(p)\}.
\]
Positivity of a Gram matrix on that span is an additional condition.
This finite-degree condition is the useful obstruction; the global
symbolic-square terminology alone does not establish it. In an affine
polynomial ring over \(\mathbb Q\), the vanishing ideal of an
algebraic point is maximal, and its ordinary square is primary.
Consequently its symbolic square equals its ordinary square. The
issue is the degree of polynomial representatives and products.

Algebraic field degree alone is insufficient for a multiplier degree
lower bound. The earlier quintic tower has exponential field degree
but admits a common quadratic denominator. Moreover, the gradient
cubics of any stationary quartic already belong to \(I_3(p)\), so
one cannot force all low-degree vanishing spaces to remain zero as
the number of variables grows.

Sums of independent copies over disjoint fields could in principle
test whether adaptive degrees add. A product of their individual
quadratic multipliers provides an upper bound. No lower bound for
such a sum has been obtained here. The existing domination results
for quadratically generated ideals warn that sufficient baseline
strength can allow one common low-degree multiplier.

## 4. Primary literature examined and scope

[Scheiderer, *Sums of squares of polynomials with rational coefficients*](https://ems.press/content/serial-article-files/32129),
Sections 2--3, constructs real-SOS forms with no rational polynomial
SOS representation. His Theorem 3.3 proves that the special norm-form
family of degree \(e\) needs and admits a multiplier of degree
\(e-2\). Proposition 3.4 describes the multipliers of that degree.
This gives adaptive-degree lower bounds as the polynomial degree
grows, including a degree-two multiplier for the quartic norm-form
case. Those forms do not have the strict convexity and isolated
nondegenerate affine minimum assumed here. The theorem does not
settle bounded adaptive degree for all strongly SOS-convex quartics
as dimension grows.

The earlier [denominator frontier](../../research-20260927/rational-denominator-certificate-frontier.md)
already explains how results of Burgdorf, Scheiderer, and Schweighofer
give some pole-free rational denominator for the present class, and
why Reznick's fixed-denominator obstruction is a different statement.
The coefficient proposition above is a deduction from the earlier
reviewed scaling obstruction. It is a supporting limitation for
certificate conditioning, not a proposed major theoretical advance.

Searches on 2026-09-28 included the phrases “convex quartic rational
SOS multiplier denominator,” “SOS-convex multiplier rational,” and
“sums of squares over the rationals denominator.” They did not locate
a theorem resolving the universal adaptive-degree question. That
unsuccessful search is not evidence of novelty or openness.

## 5. Verification status

The displayed proof was checked algebraically by its author. No
numerical optimization, new computational identity check, Lean
formalization, project-wide verification, or CI inspection was used.
The closedness and separation facts are inherited from the linked
independently reviewed note. The [independent review](universal-multiplier-review.md) checked the
coefficient argument, cone substitution, scope restrictions, and
primary-source comparison. No substantive correction was needed.
