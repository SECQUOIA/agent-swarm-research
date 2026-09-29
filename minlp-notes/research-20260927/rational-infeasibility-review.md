# Independent review of rational quadratic infeasibility certificates

Date: 2026-09-27. This review checks the proposed support-preserving
rationalization argument independently of its author. The complete draft of
[the rational certificate theorem](rational-infeasibility-certificates.md)
was reviewed, including its explicit perturbation constants. Its algebraic
input is the certificate-size theorem in
[the existing certificate note](algebraic-primal-dual-certificates.md),
including that theorem's field-degree and height bounds. This review does
not re-prove the ordered-perturbation theorem on which those bounds depend.

The proposed argument is mathematically sound. Its useful addition is a
rational certificate format and a quantitative rationalization bound. The
existence of a positive real aggregate is classical; rationalization should
not be presented as a new theorem of alternatives. A separate
[primary-source audit](rational-infeasibility-prior-review.md) checks the
literature comparison.

## 1. Exact setting and certificate soundness

Treat affine constraints as quadratics with zero Hessian. Write every row
as

\[
q_i(x)=\tfrac12 x^TQ_ix+a_i^Tx+c_i\le0,
\qquad Q_i\succeq0,
\]

with rational data. A rational certificate supplies nonnegative weights
\(w_i\), a rational vector \(z\), and optionally the rational number
\(\gamma\), satisfying

\[
\sum_iw_i=1,\qquad
H=\sum_iw_iQ_i,\quad b=\sum_iw_ia_i,\quad
c=\sum_iw_ic_i,
\]
\[
Hz=-b,\qquad \gamma=c+\tfrac12b^Tz>0.
\]

Then

\[
\sum_iw_iq_i(x)
=\gamma+\tfrac12(x-z)^TH(x-z)\ge\gamma>0.
\]

A feasible point would make the left side nonpositive. This identity proves
soundness using rational arithmetic. Positive semidefiniteness follows
from the native PSD promise and nonnegative weights; a verifier accepting
arbitrary purported input can also check that promise by rational linear
algebra. A singular \(H\) causes no problem, and \(z\) need not be the
minimum-norm stationary point.

## 2. Why rational approximation preserves the certificate

Fix the positive support \(I\) of a real positive aggregate. Its support
weights are strictly positive and normalized. Set

\[
W=\bigcap_{i\in I}\ker Q_i,
\qquad S=\sum_{i\in I}Q_i.
\]

For every choice of positive weights on exactly this support,

\[
\ker H(w)=W=\ker S.
\]

This uses positive semidefiniteness: a sum of nonnegative quadratic forms
vanishes exactly when every summand vanishes. Because the matrices are
rational, \(W\) has a rational basis of polynomial input bit length.

The aggregate has a finite global minimum if and only if \(b(w)\perp W\).
Necessity follows by moving in either direction of any vector in \(W\).
For sufficiency, the quadratic is positive definite on \(W^\perp\), and
its restriction has a stationary point. Thus finiteness is preserved by
the rational affine equations

\[
\sum_{i\in I}w_i=1,\qquad
u^T\sum_{i\in I}w_ia_i=0
\quad\text{for each vector }u\text{ in a rational basis of }W.
\]

Gaussian elimination gives a rational chart for this affine space with
polynomial input bit length. Its free coordinates can be chosen from the
weight coordinates themselves. Rounding those coordinates and reconstructing
the dependent coordinates preserves every displayed equation exactly.
Sufficiently accurate rounding preserves the positive support.

On this affine space with the support fixed, the minimum is

\[
\phi(w)=c(w)-\tfrac12 b(w)^T
           (H(w)|_{W^\perp})^{-1}b(w).
\]

It is continuous. Since the original value is positive, sufficiently close
rational weights have positive minimum. Solving the consistent rational
system \(H(w')z=-b(w')\) then gives a rational stationary point and hence
a rational positive margin.

This proof also handles a zero-dimensional affine weight space: its unique
point is rational already. If every supported Hessian is zero, then
\(W=\mathbb R^n\), the equations require \(b=0\), and the positive
minimum is simply \(c>0\). No inverse or positive-eigenvalue statement
should be used in that case.

## 3. Quantitative bound

Let \(N\) be the explicit input length and let the algebraic starting
certificate have joint field degree and absolute logarithmic heights
bounded by \(N^{O(h+1)}\). Normalizing all native and affine weights
preserves this order: their sum is a positive element of the same field,
and sums, products, and reciprocals have controlled absolute height.
The elementary bound

\[
e^{-D H(\beta)}\le |\beta|\le e^{D H(\beta)}
\quad(\beta\ne0)
\]

for a degree-at-most-\(D\) algebraic number implies

\[
\omega:=\min_{i\in I}w_i\ge2^{-N^{O(h+1)}},
\qquad \gamma\ge2^{-N^{O(h+1)}}.
\]

If \(S\ne0\), its smallest positive eigenvalue is at least
\(2^{-\operatorname{poly}(N)}\). One direct proof uses the lowest
nonzero coefficient of its rational characteristic polynomial. That
coefficient is the product of its positive eigenvalues and has polynomial
bit length, whereas every eigenvalue is at most
\(2^{\operatorname{poly}(N)}\). Therefore

\[
H(w)|_{W^\perp}\succeq
\omega S|_{W^\perp}\succeq\kappa I,
\qquad \kappa\ge2^{-N^{O(h+1)}}.
\]

For nearby weights remaining at least \(\omega/2\), the perturbed
restriction has eigenvalues at least \(\kappa/2\). Normalization and
nonnegativity bound \(\|H\|\), \(\|b\|\), and \(|c|\) by
\(2^{\operatorname{poly}(N)}\). Their changes are at most that size
times \(\|w'-w\|_\infty\). The inverse identity

\[
H'^{-1}-H^{-1}=H'^{-1}(H-H')H^{-1}
\quad\text{on }W^\perp
\]

therefore gives

\[
|\phi(w')-\phi(w)|
\le2^{N^{O(h+1)}}\|w'-w\|_\infty.
\]

Choosing the weight error below both \(\omega/2\) and a suitable
multiple of \(\gamma\) preserves positivity. The rational chart's
coefficient norms add only a polynomial input term to the required
precision. Thus \(N^{O(h+1)}\) bits per free coordinate suffice.

The resulting rational matrix and right-hand side have this same bit-length
order. Rational elimination in \(H'z=-b'\), followed by the rational
calculation of \(\gamma'\), keeps the total certificate length in
\(N^{O(h+1)}\). Keeping the original support also keeps any previously
proved support bound. The argument proves certificate existence; an
algorithm that recovers the starting field certificate and chooses the
rounding precision must be specified separately if construction time is
claimed.

The manuscript's explicit constants also check. With the notation used
there, the two linear-term cross products contribute at most
\(2M^2\varepsilon/\eta\), and the inverse difference contributes
\(M^3\varepsilon/\eta^2\). Including the constant term gives
\(L=M+2M^2/\eta+M^3/\eta^2\le4M^3/\eta^2\). Hence its chosen
\(\varepsilon\le\alpha\eta^2/(16M^3)\) leaves a minimum at least
\(3\alpha/4\). A minor wording correction was requested: the product
of positive eigenvalues is a characteristic-polynomial coefficient up to
sign, or a positive coefficient of \(\det(tI+Q)\). This sign convention
does not change the spectral estimate.

## 4. Stress cases and necessary dependence on the parameter

Preserving positivity and normalization alone is insufficient. For

\[
q_1(x,y)=x^2+y+1,\qquad q_2(x,y)=x^2-y+1,
\]

equal weights give the positive aggregate \(x^2+1\). Replacing them by
\((1/2+\epsilon,1/2-\epsilon)\), with \(0<|\epsilon|<1/2\),
gives \(x^2+2\epsilon y+1\), which is unbounded below. The exact
kernel equations are essential.

There is also an elementary exponential lower bound for the normalized
rational certificate format. For \(h\ge1\), consider the infeasible
system in \(h\) variables

\[
\tfrac12-x_1\le0,\qquad
x_i^2-x_{i+1}\le0\quad(1\le i<h),\qquad
x_h^2\le0.
\]

Its native Hessian span is \(h\), and its explicit input length is
polynomial in \(h\). Infeasibility follows backwards from
\(x_h=0\). At the rational point

\[
x_i=2^{-2^{i-1}},
\]

every row except the last equals zero, and the last equals
\(2^{-2^h}\). Therefore every normalized positive aggregate has
minimum

\[
0<\gamma\le2^{-2^h}.
\]

If \(\gamma\) is recorded as a reduced positive rational, its
denominator has at least \(2^h+1\) binary digits. Consequently a
polynomial bit bound independent of \(h\) is impossible for this
certificate format. This is a lower bound for explicit rational margins,
not for all conceivable infeasibility proof systems. The familiar squaring
chain should not be described as a novel construction.

A stronger variant, identified by the independent prior-audit branch and
rechecked here, forces large rational weights even when the margin is not
recorded. In \(n\) variables use

\[
\tfrac12-x_1\le0,\qquad
x_i^2-x_{i+1}\le0\quad(1\le i<n),\qquad x_n\le0.
\]

Now the Hessian span is \(h=n-1\). Write the corresponding nonnegative
aggregate weights as \(\lambda_0,\ldots,\lambda_n\), with no
normalization required. A globally positive aggregate must have
\(\lambda_0>0\), since otherwise its value at zero is zero. Set
\(d=2^{n-1}\) and evaluate the aggregate along
\(x_i=t^{2^{i-1}}\). All intermediate rows vanish, so positivity at
\(t=(1+1/d)/2\) requires

\[
\frac{\lambda_n}{\lambda_0}
>\frac{1/(2d)}{2^{-d}(1+1/d)^d}
>\frac{2^{d-1}}{3d}.
\]

The last inequality uses \((1+1/d)^d<3\). For rational weights,
the numerator of \(\lambda_n\) and denominator of
\(\lambda_0\) must together contain at least
\(d-O(\log d)=2^h-O(h)\) bits. Thus the rational weights alone
need exponential total length in \(h\), independently of normalization,
the center, or an explicitly recorded margin. This strengthens the first
chain's format-specific margin bound, but still concerns positive-aggregate
certificates rather than arbitrary proof systems.

## 5. Verification record and remaining limits

Independent symbolic derivation checked the normalization, common kernel,
affine chart, inverse perturbation estimate, rational stationary point,
and exact certificate identity. A targeted `python -` command using only
`fractions.Fraction` checked the squaring-chain row values and denominator
bit counts for \(h=1,\ldots,9\), and checked that the displayed
normalized perturbation breaks the kernel equation. Both checks passed.
A second targeted `python -` command, again using exact fractions, checked
the stronger chain's row values and weight-ratio inequalities for
\(n=2,\ldots,10\); it passed.
These finite calculations confirm the examples, not the general proof.
A targeted Markdown check for this review's trailing whitespace, paired
math delimiters, and local links also passed.

No project-wide checks, CI inspection, numerical conditioning experiments,
or Lean verification were performed. The certificate-size bound depends
on the existing algebraic height theorem. Novelty is not established by
this review, and practical certificate sizes or extraction performance
remain unmeasured.
