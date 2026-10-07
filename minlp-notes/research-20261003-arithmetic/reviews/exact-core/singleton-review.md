# Independent audit of irrational quartic singletons

Date: 2026-10-03. Verdict: the explicit bivariate example and the general
realization theorem pass this audit. The bivariate example directly
answers the exact rational-witness question stated in Table 1 of
*Hesse's Redemption*, version 1. Publication priority remains a separate
literature question.

I read the proofs directly in the
[explicit construction](../../../research-20260927/convex-quartic-irrational-zero.md),
its [rational Hessian certificate](../../../research-20260927/convex-quartic-rational-sos.md),
the [general strongly convex quartic construction](../../../research-20260927/general-strongly-convex-quartic-singleton.md),
the [effective quadratic pencil](../../../research-20260927/general-algebraic-singleton-realization.md),
and the [full Hessian Gram extension](../../../research-20260927/sos-convex-quartic-realization.md).
This assessment does not rely on previous review verdicts.

## 1. Explicit example and exact promise

Let
\[
\begin{aligned}
A(x,y)={}&12599x^2-10000xy+7937y^2\\
&-15874x-12599y+20000,\\
F(x,y)={}&A(x,y)^2+10000\bigl((x^2-y)^2+(y^2-2x)^2\bigr).
\end{aligned}
\]
Then \(F\) is an integer quartic, all its expanded coefficients have
absolute value below \(2^{30}\), and
\[
\min_{\mathbb R^2}F=0,\qquad
\operatorname{argmin}_{\mathbb R^2}F
=\{(\sqrt[3]2,\sqrt[3]4)\}.
\]
It is globally strongly convex with \(\nabla^2F\succeq4124I\).
It also has an explicit rational positive definite Hessian Gram on
the full basis \((a,b,xa,xb,ya,yb)\). These are separate assertions:
ordinary strong convexity alone would not establish that Gram promise.

The unique zero can be checked independently of the curvature proof.
Any zero must have \(y=x^2\) and \(y^2=2x\), whence
\(x(x^3-2)=0\). The candidate \((0,0)\) is excluded by
\(A(0,0)=20000\). At \((r,r^2)\), with \(r^3=2\), direct
substitution gives \(A=0\). Thus this is exactly the zero set.
Eisenstein's criterion makes \(r\) irrational. The rational minimum
is crucial: this example says more than the existence of an irrational
optimizer with an irrational optimal value.

For the analytic curvature proof, divide by \(5000^2\) and translate
by \((r,r^2)\). The quadratic homogeneous part of the translated
quartic has Hessian at least \(I/1250\); its cubic part has Hessian
norm at most \((63/1250)\|u\|\); its quartic part has Hessian at
least \(\|u\|^2I\). All three estimates follow from the displayed
rational interval for \(r\), the residual Jacobian determinant
\(6\), and the positive quadratic part of \(A/5000\). Completing
the square gives
\[
\|u\|^2-\frac{63}{1250}\|u\|+\frac1{1250}
\geq\frac{1031}{6250000}.
\]
Multiplication by \(5000^2\) yields \(4124\). The estimate is
global, not a check at sampled Hessians.

The separate exact certificate proves the weaker bound \(4096I\)
without algebraic coefficients. It supplies a rational positive
definite matrix \(M\) such that
\[
250000\,(a,b)(\nabla^2F-4096I)(a,b)^{\mathsf T}
=w^{\mathsf T}Mw,
\]
after \(x=63/50+X/100\), \(y=1587/1000+Y/100\), where
\(w=(a,b,Xa,Xb,Ya,Yb)\). The certificate's diagonally dominant
matrix \(N\) has strictly positive margins, and its invertible
rational congruence to \(M\) proves \(M\succ0\).

To express the full certificate in the original variables, write
\(w=Tz\), with \(z=(a,b,xa,xb,ya,yb)\), using
\(X=100x-126\) and \(Y=100y-1587/10\). The rational matrix
\(T\) is invertible. Therefore
\[
\frac{T^{\mathsf T}MT}{250000}
+4096\operatorname{diag}(1,1,0,0,0,0)
\]
is a positive definite rational full Hessian Gram for \(F\).
If a normalized full-Gram margin of one is required, an explicit
rational scalar multiplication using the determinant/trace bound
achieves it and preserves the zero set. The unscaled example already
satisfies the positive definite supplied-certificate promise.

The three squares defining \(F\) give a short rational ordinary PSD
Gram. An ordinary positive definite polynomial Gram is impossible
because the full monomial vector has constant entry one and \(F\)
vanishes at a real point. This does not conflict with its positive
definite Hessian Gram.

The same example works with the rational polytope \([1,2]^2\),
and its optimizer lies in the interior. It therefore covers both
unconstrained optimization and optimization over a full-dimensional
rational bounded polytope.

## 2. Precise relation to the published question

I directly checked [Slot, Steurer, and Wiedmer, *Hesse's Redemption*,
Table 1 and Appendix C, version 1](https://arxiv.org/html/2511.03440v1#A3).
Their exact decision problem asks whether some point of a rational
polyhedron satisfies \(f\leq0\); a compact witness is an expanded
rational feasible point of polynomial bit length. Table 1 marks that
witness question unknown for globally convex quartics. Appendix C
distinguishes an irrational quartic optimizer from the stronger absence
of any rational witness and proves a univariate obstruction.

The example above makes the answer negative already in two variables:
there is no rational feasible point at all. It does not contradict the
paper's approximate optimization algorithm or settle the decision
problem's NP membership. Its optimizer has a short algebraic
description. The univariate obstruction also makes two variables the
smallest possible dimension for this unconstrained quartic example
with rational minimum and irrational unique optimizer.

## 3. Audit of the general construction

The input is a dense rational irreducible polynomial \(p\) of degree
\(d>1\), promised to have exactly one real root \(\alpha\).
The result is a rational quartic in \(d-1\) variables with unique
zero \((\alpha,\alpha^2,\ldots,\alpha^{d-1})\), global Hessian
at least \(I\), and a polynomial-size rational SOS. The full positive
definite rational Hessian Gram follows from the separate extension
using its stricter choice of the small square weight. A proof of the
base theorem alone must not be described as supplying that certificate.

The effective quadratic pencil preserves exact vanishing because its
rational matrices satisfy linear remainder equations modulo \(p\).
Approximating its coefficients does not approximate the zero condition.
At the algebraic target parameters, the pencil has zero gradient and
a positive quadratic part with a controlled gap. Its construction uses
the real Vandermonde basis, a rational orthogonal projection onto the
remainder equations, and a spectral estimate only on the relevant
invariant subspace. It does not incorrectly require the projected
matrix to remain positive semidefinite on the entire ambient space.

The residual Jacobian at the power vector has determinant
\(p'(\alpha)\ne0\). Discriminant and root magnitude estimates
give a rational positive lower bound on its smallest singular value
with polynomial bit length. A rational approximation within the
zero-preserving pencil yields
\[
G(a+u)=\eta^{\mathsf T}u+u^{\mathsf T}Hu,
\quad H\succeq mI,\quad\|H\|\leq L,
\quad\|\eta\|\leq\varepsilon.
\]
The Hessian decomposition of
\(G^2+\varepsilon\sum r_j^2\) retains the potentially negative
curvature from squared indefinite residual forms. Its lower estimate
is
\[
2\varepsilon\nu^2-12\varepsilon(L+nV)\|u\|
+2m^2\|u\|^2
\geq\tfrac32\varepsilon\nu^2.
\]
The stated small-weight condition gives this inequality. Dividing by
the rational square \(\varepsilon\nu^2\) produces an unweighted
rational SOS with the required curvature. No coefficients in the output
need to belong to the algebraic number field.

The certificate extension constructs a block Hessian Gram and bounds
its Schur complement. Its additional factor \(n\) in the weight
condition controls the cross-block Frobenius norm. Translation and
exact rational coefficient projection retain the full positive margin.
These checks justify the stronger certificate theorem without equating
global convexity with SOS-convexity.

All required root precision is polynomial in the dense input length.
I also checked the cited primary [Mehlhorn, Sagraloff, and Wang,
Theorem 5](https://arxiv.org/pdf/1301.4870v2), which bounds certified
integer-polynomial root isolation and refinement polynomially in
degree, coefficient bits, and requested precision. The algorithm does
not print a common number-field representation of exponential degree.
Dense input encoding and the one-real-root promise are essential to
this exact theorem; arbitrary succinct polynomial input is outside it.

## 4. Targeted verification actually run

Both commands passed:

```text
python research-20260927/check_convex_quartic_irrational_zero.py
python research-20260927/check_convex_quartic_rational_sos.py
```

They verify rational identities, the certified root interval and all
constants in the analytic curvature estimate, the differentiated
Hessian, both coordinate forms of the rational SOS identity, strict
diagonal-dominance margins, and exact positive LDL pivots of the full
Gram. I read the general arguments separately, including the effective
pencil dependency. I did not rerun Lean, project-wide verification, or
CI checks. Earlier Lean results are not being reported as fresh runs.
