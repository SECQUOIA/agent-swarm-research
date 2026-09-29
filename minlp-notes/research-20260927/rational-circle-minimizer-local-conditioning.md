# Long rational minimizers can have polynomial Hessian condition at the optimum

Date: 2026-09-28. Status: passed
[independent review](rational-circle-minimizer-local-conditioning-review.md).
Publication priority is unestablished.

The [unit-circle height construction](rational-convex-quartic-minimizer-height.md)
can be modified so that the Hessian at its rational minimizer has a
polynomial condition number. The statement is local: it concerns the
Hessian at the minimizer, not a uniform smoothness bound on a fixed
neighborhood or a condition number for every aspect of the optimization
problem.

**Theorem.** For every \(k\geq0\), there is a rational quartic
\(F\) in \(N=2(k+1)\) variables, with polynomial bit length,
\(N+1\) supplied rational quadratic square factors, and a supplied
positive definite rational full Hessian Gram, whose unique minimizer
\(p\) satisfies
\[
 \begin{gathered}
 F(p)=0,\qquad p\in\mathbb Q^N,\qquad \|p\|^2<4/3,\\
 \nabla^2F(X)\succeq(3/2)I\quad\text{for all real }X,\\
 2I\preceq\nabla^2F(p)\preceq\bigl(8(k+1)^2+1\bigr)I.
 \tag{1}
 \end{gathered}
\]
Both terminal coordinates have reduced denominators divisible by
\(5^{2^k}\). Thus a coordinate still requires exponentially many
ordinary rational bits, while the Hessian condition number at the
minimizer is at most \(4(k+1)^2+1/2\).

## Shrinking circles and a controlled residual Jacobian

Let \(z_j=((3+4\mathrm i)/5)^{2^j}\), as in the original
construction. Put
\[
 R_j=2^{-j},\qquad p_j=(a_j,b_j)=R_j(\Re z_j,\Im z_j),
 \qquad c_j=R_j/R_{j-1}^2=2^{j-2}\quad(j\geq1).
 \tag{2}
\]
Then \(\|p_j\|=R_j\), and
\(\|p\|^2=\sum_{j=0}^k4^{-j}<4/3\). Scaling the original
fractions by powers of two cannot cancel their powers of five, so both
terminal denominators are divisible by \(5^{2^k}\).

Use residuals
\[
 \begin{aligned}
 r_0&=x_0-3/5,&s_0&=y_0-4/5,\\
 r_j&=x_j-c_j(x_{j-1}^2-y_{j-1}^2),&
 s_j&=y_j-2c_jx_{j-1}y_{j-1}\quad(j\geq1),
 \end{aligned}
 \tag{3}
\]
and let \(q_j=x_j^2+y_j^2-R_j^2\). Their unique common zero is
\(p\), and every \(q_j\) vanishes there. The coefficients in
(2)--(3) require only \(O(k)\) bits.

The Jacobian \(J\) of (3) at \(p\) has identity diagonal
blocks. Each strict subdiagonal block is minus the derivative of the
scaled squaring map, whose norm is
\[
                     2c_jR_{j-1}=1.
\]
Those blocks are orthogonal matrices. Writing \(J=I-T\), the
matrix \(T\) is a block shift with \(\|T\|\leq1\) and
\(T^{k+1}=0\). Therefore
\[
 \|J\|\leq2,\qquad
 \|J^{-1}\|=\|I+T+\cdots+T^k\|\leq k+1,
 \qquad J^{\mathsf T}J\succeq(k+1)^{-2}I.
 \tag{4}
\]
Every individual residual gradient has norm at most two. Its quadratic
part has norm at most
\[
 C=\max\{1,2^{k-2}\}.
\]
Divide all residuals uniformly by \(C\). The divided residuals
then satisfy the quantitative quartic-construction bounds with
\[
          V=2/C,\qquad \nu=1/[C(k+1)],\qquad \|T_j\|\leq1.
 \tag{5}
\]
The bounds permit \(V<1\); their proofs do not require otherwise.

## An exposing quadratic with a fixed spectral margin

Set
\[
 \begin{aligned}
 E_0&=(x_0-3/5)^2+(y_0-4/5)^2,\\
 E_j&=q_j-2a_jr_j-2b_js_j-\tfrac12q_{j-1}\quad(j\geq1).
 \end{aligned}
 \tag{6}
\]
Every \(E_j\) has zero value and full gradient at \(p\).
Its current quadratic block is \(I\), and its predecessor block is
\[
 B_j=2c_j\begin{pmatrix}a_j&b_j\\b_j&-a_j\end{pmatrix}
                                      -\tfrac12I.
 \tag{7}
\]
Because \(2c_jR_j=1/2\), the eigenvalues of \(B_j\) are
zero and minus one. This also verifies gradient cancellation directly:
if \(\Phi_j(u)=c_j(u_1^2-u_2^2,2u_1u_2)\), then
\[
 D\Phi_j(p_{j-1})^{\mathsf T}p_j
       =2c_j^2R_{j-1}^2p_{j-1}=\tfrac12p_{j-1}.
\]

Choose weights \(w_j=k+1-j\). The sum
\(E^*=\sum_{j=0}^kw_jE_j\) has positive quadratic part \(H_*\).
Each block except the last is
\(w_jI+w_{j+1}B_{j+1}\), and the last is \(I\). Hence
\[
                  I\preceq H_*\preceq(k+1)I.
 \tag{8}
\]

Replace only the coefficients \(a_j,b_j\) in (6) by rational
approximations with coordinate error at most \(\eta\), and call
the weighted sum \(G\). This preserves \(G(p)=0\) exactly.
Each block error has norm at most \(4C(k+1)\eta\), while the
full gradient error has norm at most \(4k(k+1)\eta\), since
each unscaled residual gradient has norm at most two. Thus, for
\[
 \eta\leq\min\left\{1,\frac1{8C(k+1)},
                        \frac{\varepsilon}{8(k+1)^2}\right\},
 \tag{9}
\]
we have the exact centered form
\[
 G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,
 \qquad mI\preceq H\preceq LI,
 \quad\|\ell\|\leq\varepsilon,
 \quad m=1/2,\quad L=k+2.
 \tag{10}
\]
Approximate the unit-circle chain \(z_j\) by the dyadic iteration
from the original construction, and multiply by \(R_j\). Since
\(R_j\leq1\), this gives the required approximations in time
polynomial in \(k+\log(1/\eta)\).

## Quartic construction and the Hessian at its minimizer

Choose a positive square dyadic \(\varepsilon=t^2\) with
\[
 \varepsilon\leq\min\left\{1,\frac{m^2}{2N},
          \frac{\nu^2m^2}{36N(L+NV)^2}\right\},
 \tag{11}
\]
and use it in (9). The same reviewed abstract realization as in the
original note gives
\[
 F=\left(\frac{G}{t\nu}\right)^2+
       \sum_{j=0}^k\left[
          \left(\frac{r_j}{C\nu}\right)^2+
          \left(\frac{s_j}{C\nu}\right)^2\right].
 \tag{12}
\]
It proves the global Hessian lower bound in (1), a rational full
positive definite Hessian Gram, and all asserted polynomial bit bounds.
The small rational Gram is obtained by polynomial-precision center
approximation and exact coefficient projection, exactly as in the
original reviewed proof. The norm bound for the center here is the
constant two. No exact expansion of \(p\) is used.

At \(p\), the Hessian has the particularly simple expression
\[
 \nabla^2F(p)=\frac{2}{\varepsilon\nu^2}\ell\ell^{\mathsf T}
                          +2(k+1)^2J^{\mathsf T}J,
 \tag{13}
\]
because \(C\nu=1/(k+1)\). The first summand is PSD, and its norm
is at most
\[
 \frac{2\varepsilon}{\nu^2}
       \leq\frac{m^2}{18N(L+NV)^2}<1.
\]
Apply (4) to the second summand. This proves both local Hessian bounds
in (1).

The theorem supplies a positive definite full Gram, but does not
normalize that Gram to be at least identity: an additional positive
scaling would change the absolute bounds in (1). Such a scaling would
preserve the ratio of Hessian eigenvalues and the optimizer height.

## Interpretation and limits

The Hessian condition number at the exact optimizer can remain
polynomial despite the rational-output obstruction. This is a narrower statement than
saying that the optimization instance is well-conditioned in every
sense. Coefficients, higher derivatives, and curvature away from the
optimizer can grow with \(k\), and no dimension-independent
neighborhood with a polynomial uniform smoothness bound is asserted.

The representation distinction remains: the rational minimizer has a
short arithmetic circuit and polynomial-precision approximations, but
its expanded exact fractions are long. The certificate-height
consequences in the
[optimal Gram note](rational-circle-optimal-gram-height.md) apply to
this family too, using divisibility by \(5^{2^k}\) in place of
an exact full-denominator identity.

## Verification

The fresh reviewer independently reconstructed the scaling, the local
exposing identity, every quantitative bound, and the abstract realization
interface, including the permitted case \(V<1\). No mathematical
correction was needed. The interpretation above incorporates the review's
wording refinement: the condition number can grow polynomially.

The reviewer wrote and ran the separate exact checker, which the author
also ran independently:

```text
python research-20260927/check_circle_local_conditioning_review.py
```

It checks the symbolic scaled exposing identity and orthogonal gate
derivative; rounded exact zeros, spectral margins, Jacobians, and local
Hessian bounds for \(k=0,\ldots,8\); and the Hessian formula by
direct differentiation for \(k=0,1,2\). All passed. These finite
checks support the identities, while the proof establishes the uniform
bounds. No project-wide or CI checks were run.
