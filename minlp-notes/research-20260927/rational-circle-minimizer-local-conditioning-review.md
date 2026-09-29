# Independent review of the shrinking-circle conditioning bound

Date: 2026-09-28. Verdict: the mathematical strengthening passes this
review. Publication priority remains unestablished.

This is a fresh review of the new scaling and weights in
[the local-conditioning note](rational-circle-minimizer-local-conditioning.md).
The reviewed manuscript has SHA-256
`66c574b8b55fb2af9819826fbbb44e0e4a6ed15a8fb926be8d5f911d1320d30b`.
I previously reviewed the unscaled circle construction, but did not
develop the shrinking radii, linear weights, or new Jacobian estimates.
No substantive mathematical correction was needed.

## The scaling controls the Jacobian and the exposing quadratic

Let the predecessor radius be \(R\), so the successor radius is
\(R/2\) and the squaring coefficient is \(c=1/(2R)\).
Write the predecessor as \(R(a,b)\), with \(a^2+b^2=1\).
The gate derivative is

\[
 D\Phi(Ra,Rb)=\begin{pmatrix}a&-b\\b&a\end{pmatrix},
\]

an orthogonal matrix. Thus the complete residual Jacobian is indeed
\(J=I-T\), where \(T\) is a nilpotent block shift of norm at
most one. The finite geometric inverse gives
\(\|J^{-1}\|\leq k+1\); no commutativity of the different
orthogonal blocks is required. The upper bound \(\|J\|\leq2\)
and lower singular-value bound \(1/(k+1)\) are both valid,
including \(k=0\).

There is also a useful direct identity. If \(u\) and \(w\) are
centered predecessor and successor displacements, the proposed local
exposer is exactly

\[
 E_j(p+(u,w))=\|w\|^2-(-b u_1+a u_2)^2.
 \tag{1}
\]

This verifies its vanishing value and full gradient, the absence of
cross blocks, and the predecessor eigenvalues zero and minus one.
The coefficient \(-1/2\) on the predecessor circle equation is
essential and correct. Equivalently,
\(D\Phi(p_{j-1})^{\mathsf T}p_j=p_{j-1}/2\), so that the
predecessor gradients cancel.

For weights \(w_j=k+1-j\), each nonterminal quadratic block
has eigenvalues \(w_j\) and \(w_j-w_{j+1}=1\). The last
block is the identity. Hence \(I\preceq H_*\preceq(k+1)I\).
This bound has a fixed lower margin despite the shrinking radii.

## Approximation and small residual-gradient bounds

Approximating only the coefficients multiplying exact vanishing
residuals preserves the value zero at the true point. A predecessor
block error has norm at most \(4c_jw_j\eta\), bounded by
\(4C(k+1)\eta\). Each block receives only one such error.

The full gradient estimate also has the stated constant. Each gate
contributes at most \(8w_j\eta\), using the individual residual
gradient bound two. Summing
\(\sum_{j=1}^kw_j=k(k+1)/2\) yields
\(4k(k+1)\eta\). The chosen tolerance therefore guarantees
the claimed leading-matrix margins and \(\|\ell\|\leq
\varepsilon\). At \(k=0\), this perturbation is absent.

The quadratic parts of the original residuals have norms at most
\(C=\max(1,2^{k-2})\). Dividing every residual by the same
\(C\) gives the required norm-one bound, a Jacobian lower bound
\(\nu=1/[C(k+1)]\), and gradient upper bound \(V=2/C\).
There is no hidden hypothesis \(V\geq1\) in the imported
construction. In particular, the mixed Hessian Gram block estimate is

\[
 \|D\|\leq6\sqrt N\bigl(\|\ell\|L+
             \varepsilon\sum_i\|\nabla(r_i/C)(p)\|
                                      \|T_i/C\|\bigr)
 \leq6\sqrt N\,\varepsilon(L+NV).
\]

It uses \(V\) only as a nonnegative upper bound. The remaining
Hessian and Schur-complement inequalities likewise require no lower
bound on \(V\). Thus values \(V<1\) cause no loss in the
global strong convexity or full Gram certificate.

All required precisions still have polynomial bit length. The largest
new coefficient is a power of two with exponent \(O(k)\).
The chosen tolerance can be obtained by polynomial-precision dyadic
simulation of the unit-circle chain, followed by the rational radius
scaling. The original rational Gram approximation and exact projection
argument applies unchanged, with center norm bounded by two.

## The local Hessian bound follows from the actual square factors

Every factor vanishes at \(p\). Differentiating the displayed SOS
therefore gives exactly

\[
 \nabla^2F(p)=
 \frac{2\ell\ell^{\mathsf T}}{\varepsilon\nu^2}
                  +2(k+1)^2J^{\mathsf T}J.
 \tag{2}
\]

The second term lies between \(2I\) and \(8(k+1)^2I\).
The first is positive semidefinite and has norm at most

\[
 \frac{2\varepsilon}{\nu^2}
 \leq\frac{m^2}{18N(L+NV)^2}<1.
\]

This proves both bounds in the theorem and the Hessian condition-number
bound. The division by \(C\) was included consistently: its
cancellation uses \(C\nu=1/(k+1)\).

Multiplying coordinates by powers of two cannot cancel the denominator
power \(5^{2^k}\). The geometric sum of squared radii is strictly
less than \(4/3\), including at \(k=0\). Thus the arithmetic
and norm conclusions survive the scaling.

The interpretation must stay local. The result proves polynomial
Hessian condition at the optimizer; it does not bound curvature
uniformly on a fixed neighborhood, higher derivatives, the conditioning
of the Gram representation, or the sensitivity of exact rational
reconstruction. I recommended replacing an unqualified reference to
absence of ill-conditioning by the precise statement that the local
Hessian condition number can remain polynomial.

## Independent exact checks

The separate [checker](check_circle_local_conditioning_review.py) was run as

```text
python research-20260927/check_circle_local_conditioning_review.py
```

It passed the symbolic identity (1) modulo \(a^2+b^2-1\) and
the orthogonality identity for the gate derivative. For
\(k=0,\ldots,8\), exact rational checks passed the denominator
divisibility, norm bound, rounded exact zero, exposing-matrix margins,
gradient bound, Jacobian bounds, and scalar bound on the first term
of (2). These include instances with \(V<1\).

For an independent check of the Jacobian inequalities, the script
forms an exact block orthogonal transformation taking \(J\) to
the scalar unit lower-bidiagonal matrix tensored with \(I_2\),
and checks the proposed scalar spectral margins by rational LDL.
For \(k=0,1,2\), it directly differentiates the constructed
quartic and verifies (2).

The script reuses only fraction and rounding helpers from the earlier
independent checker. It does not reuse the author's construction code.
The finite tests check formulas and sample margins; the arguments
above establish the general bounds and polynomial complexity. No
project-wide checks, CI inspection, or Lean proof were used.

An inline `python - <<'PY'` check passed local-link, math-delimiter,
whitespace, control-character, and final-newline checks on this review
and its checker: two files and two local links. `git diff --check --`
restricted to those two paths also passed.
