# Independent review of the unbounded rational radial exponent

Date: 2026-09-28. Verdict: the proposed scaling theorem is correct.
For the explicit quartic \(F\), put
\[
 F_t(X)=t^{-2}F(tX),\qquad R(X)=1+\|X\|^2,
 \qquad t\in\mathbb Q,\ t\ge1.
\]
For every integer \(N\ge0\), there is a real threshold \(T_N\)
such that
\[
 R^N F_t\notin\Sigma\mathbb Q[X]^2
 \quad\text{for every rational }t>T_N.
\]
Thus no exponent depending only on dimension, degree, and the lower
Hessian bound can suffice for these rational strongly SOS-convex
quartics. This conclusion does not require a per-instance existence
theorem. With the separate existence result in
[the denominator frontier, Section 3](rational-denominator-certificate-frontier.md),
the least radial multiplier exponent is finite for every \(t\) and
tends to infinity as rational \(t\to\infty\). Publication priority
is not assessed here.

The inputs about \(F\) are its rational coefficients, degree four,
zero \(p=(a^4/2,a,a^2/2)\), where \(a^5=2\) and \(a>0\),
the strict rational full Hessian Gram certificate, and the explicit
obstruction
\[
 I_2=\operatorname{span}_{\mathbb Q}\{r_0,\ldots,r_4\},
 \qquad
 \Lambda\!\left(\left(\sum_{i=0}^4c_ir_i\right)^2\right)=4c_4^2,
 \qquad \Lambda(F)=-4.
\]
Here \(I_2\) is the rational space of polynomials of degree at most
two vanishing at \(p\), and the displayed identity holds for real
\(c_i\). The [fresh certificate review](rational-denominator-certificate-fresh-review.md)
independently checked the underlying rational arithmetic and the
quadratic obstruction. The stronger real-span obstruction is essential:
failure of rational SOS alone would not justify the real-cone step.

Fix \(N\ge0\) and put \(D=N+2\). Define
\[
 I_D=\{q\in\mathbb Q[X]_{\le D}:q(p)=0\},\qquad
 V_D=\operatorname{span}_{\mathbb R}I_D,
 \qquad C_D=\left\{\sum_j q_j^2:q_j\in V_D\right\}.
\]
All spaces are embedded in finite-dimensional polynomial coefficient
spaces. In particular, \(C_D\subseteq\mathbb R[X]_{\le2D}\).
The space \(V_D\) is the real span of the rational vanishing space.
It is not the whole space of real polynomials of degree at most \(D\)
vanishing at the one real point \(p\).

The cone \(C_D\) is closed in the coefficient topology. To prove this,
choose a real basis vector \(b\) of \(V_D\), and integrate over any
closed ball with nonempty interior. The matrix
\[
 B=\int bb^{\mathsf T}
\]
is positive definite: a nonzero linear combination of the independent
basis polynomials cannot vanish on an open ball. Suppose
\(P_k=b^{\mathsf T}G_kb\to P\) coefficientwise, where
\(G_k\succeq0\). Such matrices exist for every element of \(C_D\).
Integration is a continuous linear functional on this fixed-degree
coefficient space, so
\[
 \lambda_{\min}(B)\operatorname{tr}(G_k)
 \le\operatorname{tr}(BG_k)=\int P_k
\]
is bounded. A positive semidefinite matrix with bounded trace has
bounded entries. A subsequence of the \(G_k\) therefore converges
to a positive semidefinite matrix \(G\), and continuity gives
\(P=b^{\mathsf T}Gb\in C_D\). This coercivity argument is necessary;
linear images of the positive semidefinite cone are not automatically
closed.

Next, \(F\notin C_D\). In a real sum of squares equal to a quartic,
every summand has degree at most two. Indeed, if the maximum summand
degree were \(m>2\), its degree-\(2m\) homogeneous part would be a
sum of squares of nonzero degree-\(m\) forms and could not vanish.
Also,
\[
 V_D\cap\mathbb R[X]_{\le2}
       =\operatorname{span}_{\mathbb R}I_2.
\]
For a precise base-change justification, restrict the map selecting
coefficients of degrees greater than two to \(I_D\). This is a
rational linear map with kernel \(I_2\). Row reduction over
\(\mathbb Q\) shows that its real kernel is the real span of its
rational kernel. Thus any representation of \(F\) in \(C_D\)
would use quadratic summands in the real span of the \(r_i\).
Applying \(\Lambda\) gives \(\Lambda(F)\ge0\), contradicting
\(\Lambda(F)=-4\).

The curve
\[
 P_\varepsilon(X)=(1+\varepsilon\|X\|^2)^N F(X)
\]
converges coefficientwise to \(F\) as \(\varepsilon\to0\).
Since \(C_D\) is closed and excludes \(F\), there is
\(\delta_N>0\) such that \(P_\varepsilon\notin C_D\)
whenever \(0\le\varepsilon<\delta_N\). If rational
\(\varepsilon\) in that interval admitted a rational polynomial
SOS for \(P_\varepsilon\), each summand would have degree at most
\(D\), and evaluation at \(p\) would force each to vanish there.
Each summand would therefore lie in \(I_D\), placing
\(P_\varepsilon\) in \(C_D\), a contradiction. For \(N=0\)
the curve is constant and the same conclusion holds directly.

Now suppose \(R(X)^NF_t(X)=\sum_j u_j(X)^2\) with rational
polynomials \(u_j\). Substituting \(X=x/t\) and multiplying
by \(t^2\) gives
\[
 (1+t^{-2}\|x\|^2)^NF(x)=\sum_j\bigl(tu_j(x/t)\bigr)^2.
\]
The transformed summands remain rational because \(t\) is nonzero
and rational. Taking \(t>\delta_N^{-1/2}\) contradicts the previous
paragraph. The conclusion therefore holds for every sufficiently large
rational \(t\), and in particular for every sufficiently large
integer \(t\). No effective formula for the threshold is obtained
from this proof.

All claimed geometric and arithmetic properties survive this scaling.
The exact identities are
\[
 \nabla F_t(X)=t^{-1}\nabla F(tX),\qquad
 \nabla^2F_t(X)=\nabla^2F(tX)\succeq I.
\]
The minimum remains zero, its unique location is \(p/t\), and
\(\mathbb Q(p/t)=\mathbb Q(p)=\mathbb Q(a)\), of degree five.
At that minimum the Hessian matrix is exactly \(\nabla^2F(p)\),
so its eigenvalues and spectral condition number are unchanged. This
does not assert a uniform condition number for the full Hessian Gram
matrix or a bound on coefficient height.

For the full Hessian Gram certificate, use the uncentered vector
\(Z(X,v)=(v,X\otimes v)\). If
\(v^{\mathsf T}\nabla^2F(X)v=Z(X,v)^{\mathsf T}MZ(X,v)\)
with rational \(M\succ0\), then the scaled Gram matrix is
\[
 M_t=D_t^{\mathsf T}MD_t,\qquad
 D_t=\operatorname{diag}(I_3,tI_9).
\]
It is rational and positive definite because \(D_t\) is rational
and invertible. A certificate initially written at a rational center
can first be moved to the uncentered basis by rational invertible
congruence. Thus strict rational SOS-convexity is preserved.

The positive leading quartic form also persists: the leading form of
\(F_t\) is \(t^2F_4\). Positivity of \(F_4\) follows from the
strict full Hessian Gram certificate. Its principal block on
\(X\otimes v\) is positive definite and represents
\(v^{\mathsf T}\nabla^2F_4(X)v\). Substituting \(v=X\ne0\)
and using Euler's identity
\(X^{\mathsf T}\nabla^2F_4(X)X=12F_4(X)\) gives
\(F_4(X)>0\). Consequently each \(F_t\) satisfies the separately
reviewed sphere corollary's hypotheses: a positive definite leading
form, a finite real zero set, and a positive definite Hessian at its
zero. That corollary supplies existence of a finite radial exponent.
This review treats the corollary as a cited input and does not repeat
its general-ring proof or its literature audit.

Define the resulting finite least exponent by
\[
 \nu(t)=\min\{N\ge0:R^NF_t\in\Sigma\mathbb Q[X]^2\}.
\]
The admissible exponents are upward closed, since \(R\) is a sum
of rational squares and products of sums of squares are sums of
squares. Failure at exponent \(N\) therefore excludes every smaller
exponent as well. The established quantifiers prove
\(\nu(t)\to\infty\) along rational \(t\to\infty\), rather
than only unboundedness along an unspecified subsequence. A common
denominator of the prescribed form \(R^k\) requires a multiplier
identity for \(R^{2k}F_t\), so its required exponent also grows.

In contrast, an adaptive quadratic denominator remains sufficient.
Let \(R_t(X)=1+t^2\|X\|^2\). The already verified identity
\(RF=\sum_jq_j^2\), with rational cubic-or-lower \(q_j\), yields
\[
 R_tF_t=t^{-2}(RF)(tX)
       =\sum_j\bigl(t^{-1}q_j(tX)\bigr)^2.
\]
Since \(R_t=1^2+\sum_{i=1}^3(tX_i)^2\), multiplication once
more by \(R_t\) gives rational-function squares with common
denominator \(R_t\), numerator degree at most four, and no real
poles. The minimum common-denominator degree remains exactly two:
an affine or constant denominator would cancel as in the earlier
review, and rational polynomial SOS for \(F_t\) would rescale to
rational polynomial SOS for \(F\). The adaptive multiplier identity
alone does not prove finite existence for the fixed radial multiplier;
that distinct fact uses the sphere corollary.

The theorem therefore separates adaptive degree-two rational
denominators from arbitrarily high powers of one prescribed radial
polynomial, within this strict convexity class. It gives no quantitative
bound on the radial order in terms of coefficient height, computational
complexity lower bound, or minimum number of squares.
Its cone concerns rational coefficient constraints; replacing it by
the full real SOS cone would invalidate the obstruction.

I also read the assembled
[radial-exponent manuscript](rational-radial-exponent-obstruction.md)
in full. Its extension to a fixed finite menu
\(h_1,\ldots,h_s\in\mathbb Q[X]\) with \(h_j(0)>0\) is valid.
One can take the single degree bound
\[
 d=\left\lceil\frac{4+\max_j\deg h_j}{2}\right\rceil.
\]
A rational SOS for \(h_jf_t\), after the same change of variables,
would put \(h_j(x/t)F(x)\) in \(C_d\). These products converge
to \(h_j(0)F\), which is outside \(C_d\): its positive scalar
factor can either be cancelled in the real cone or retained in the
strictly negative value of \(\Lambda\). Closedness gives a threshold
for each \(j\), and the maximum threshold works for the finite menu.
No positivity of \(h_j\) away from the origin is needed for this
argument. The stated condition \(h_j(0)>0\) avoids the zero limit
that would invalidate this particular proof.

The manuscript's adaptive certificate bit bound is also correct for
positive integer \(t\) with binary rational-coefficient encoding.
A degree-\(m\) coefficient of \(F\) becomes its fixed original
coefficient times \(t^{m-2}\), for \(0\le m\le4\). A degree-\(m\)
coefficient in \(b(tX)/t\) is its fixed original coefficient times
\(t^{m-1}\), for \(0\le m\le3\). Numerator and denominator bit
lengths are therefore \(O(1+\log t)\). The Gram matrix is fixed,
and the number of entries, monomials, and factors is fixed. Choosing
one rational square-factor expansion of that fixed Gram matrix also
gives a total unweighted certificate size \(O(1+\log t)\); the
constants may depend on the fixed expansion. Multiplication by the
four squares of \(R_t\) preserves this bound. Conversely,
\([X_1^4]F_t=104t^2\), so the input encoding itself has length
\(\Omega(1+\log t)\). Thus the claimed adaptive certificate size
bounded by a constant times this family's input length is justified.
This is an upper bound for the explicit family and construction, not
a bit-complexity bound for discovering certificates for arbitrary
input polynomials.

This was a mathematical audit, with an additional independent reader
checking the cone proof and quantifiers. No new computational claims
were needed beyond the exact certificate and obstruction checks
recorded in the linked fresh review. No project-wide verification or
CI inspection was performed.
