# Independent review of the convex quartic irrational zero

Date: 2026-09-28. Scope: the explicit integer polynomial and global
Hessian proof in
[the construction note](convex-quartic-irrational-zero.md), together with
its retained exact checker.
This reviewer did not develop the explicit example or its numerical
constants. The proof was reconstructed independently, including its
normalization, translated homogeneous parts, root interval, operator-norm
estimates, and final curvature constant. No mathematical defect was
found in the example below or in the completed author note.

Define

\[
 \begin{aligned}
 q_1(x,y)&=x^2-y,\\
 q_2(x,y)&=y^2-2x,\\
 A(x,y)&=12599x^2-10000xy+7937y^2\\
       &\qquad-15874x-12599y+20000,\\
 F(x,y)&=A(x,y)^2+10000\bigl(q_1(x,y)^2+q_2(x,y)^2\bigr).
 \end{aligned}
\]

The verified conclusion is

\[
 \nabla^2F(x,y)\succeq4124I\quad\text{for every }(x,y)\in\mathbb R^2,
 \qquad
 \{F\leq0\}=\{(\sqrt[3]2,\sqrt[3]4)\}.
\]

Thus a globally strongly convex integer quartic can have rational minimum
zero attained only at an irrational point. In particular its zero
sublevel has no rational feasible-point witness, regardless of encoding
length. This is not a decision-complexity lower bound or a claim about
all possible verification certificates.

The zero set can be checked before considering convexity. A zero of `F`
must satisfy `q_1=q_2=0`, hence `y=x^2` and `x(x^3-2)=0`. At
`(0,0)`, the value of `A` is `20000`, so that point is excluded.
Writing `r=cuberoot(2)`, substitution shows that `A(r,r^2)=0`.
There are no other real possibilities. The first coordinate is
irrational because `T^3-2` is Eisenstein at two. The displayed sum of
squares also proves nonnegativity everywhere, and its nonzero degree-four
part makes it a quartic.

For the convexity proof, put `p=(r,r^2)`, write `u=(u_1,u_2)` for
displacement from `p`, and normalize `f=F/5000^2`. Define

\[
 \begin{aligned}
 \varepsilon&=\frac1{2500},\\
 j_1&=(2r,-1)^T,\qquad j_2=(-2,2r^2)^T,\\
 J&=\begin{pmatrix}j_1^T\\j_2^T\end{pmatrix},\\
 d_1&=2r-\frac{12599}{5000},\qquad
 d_2=r^2-\frac{7937}{5000},\\
 H&=\begin{pmatrix}2r&-1\\-1&r^2\end{pmatrix}
       -\operatorname{diag}(d_1,d_2),\\
 \ell&=-d_1j_1-d_2j_2.
 \end{aligned}
\]

The exact translated identity is

\[
 f(p+u)=\bigl(\ell^Tu+u^THu\bigr)^2
       +\varepsilon\bigl((j_1^Tu+u_1^2)^2
                          +(j_2^Tu+u_2^2)^2\bigr).
\]

There is no discarded remainder. The constant terms vanish exactly
modulo `r^3-2`; the proof does not substitute a rational approximation
for `r` in this identity.

The rational isolating interval

\[
 \frac{1259921}{10^6}<r<\frac{1259922}{10^6}
\]

was checked by exact cubing. It gives
`0<d_1<44/10^6`, `0<d_2<4/10^6`, and
`d_1+d_2<1/20000`. The apparent algebraic terms in `H` cancel:
its diagonal entries are exactly `12599/5000` and `7937/5000`.
Diagonal dominance therefore gives `H >= (2937/5000)I > I/2`.
Its operator norm is at most its trace and is less than five. This
direct rational bound agrees with the independently checked, slightly
weaker perturbation bound from the unperturbed matrix.

Both `||j_i||` are less than four, so
`||ell|| < 4(d_1+d_2) < 1/5000`. The determinant is exactly
`det J=4r^3-2=6`, while the same rational interval gives
`||J||_F^2=5+4r^2+4r^4<23`. Consequently

\[
 \lambda_{\min}(J^TJ)
   \geq\frac{(\det J)^2}{\operatorname{tr}(J^TJ)}
   >\frac{36}{23}>1.
\]

This is the required full-rank estimate. A bound on the lengths of the
gradient vectors alone would not have supplied it.

Separating the translated polynomial by degree gives a direct global
Hessian certificate. Its quadratic part has Hessian
`2 ell ell^T+2 epsilon J^T J >= 2 epsilon I = I/1250`.
For `h(u)=u^THu`,

\[
 \nabla^2(h^2)=8(Hu)(Hu)^T+4(u^THu)H
                    \succeq\|u\|^2I,
\]

using `H >= I/2`. The remaining quartic terms are
`epsilon(u_1^4+u_2^4)` and have PSD Hessian. Thus the full quartic
part contributes at least `||u||^2 I` everywhere.

For the cubic terms, the exact general identity is

\[
 \nabla^2\bigl(2(a^Tu)(u^TKu)\bigr)
 =4(a^Tu)K+4\bigl(a(Ku)^T+(Ku)a^T\bigr),
\]

for symmetric `K`. Its operator norm is at most
`12 ||a|| ||K|| ||u||`. Applied first to `a=ell, K=H`, then to
the two coordinate rank-one matrices and `a=epsilon j_i`, this gives
the total cubic Hessian bound

\[
 \|\nabla^2 f_3(u)\|
 \leq\left(12\frac1{5000}\,5
            +12\varepsilon(4+4)\right)\|u\|
 =\frac{63}{1250}\|u\|.
\]

In particular, the factor of two from the square expansion and every
Hessian factor are included. Writing `t=||u||`, the three contributions
combine to give

\[
 \begin{aligned}
 \nabla^2 f(p+u)
 &\succeq\left(t^2-\frac{63}{1250}t+\frac1{1250}\right)I\\
 &\succeq\left(\frac1{1250}
                    -\frac14\left(\frac{63}{1250}\right)^2\right)I
 =\frac{1031}{6250000}I.
 \end{aligned}
\]

Multiplying by `5000^2=25000000` gives `4124I`. This estimate is
uniform over all real displacements. It is stronger than a Hessian
check at the zero, a grid test, or a local convexity certificate.

The initial triangle-based motivation also survives adversarial review.
In the two-dimensional cubic-field construction, the two parameter
gradients have rank two. In the simple quadratic relation basis used
here, that is already the exact identity `det J=6`. A triangle whose
offsets sum to zero and whose rational centroid approximates the
irrational center to second order cancels the first-order cubic term.
The quadratic Hessian is then of order `delta^2`, the quartic Hessian
dominates `||u||^2`, and the cubic Hessian is only of order
`delta^2 ||u||`. Completing the square makes global convexity possible.
This reasoning would fail without the rank condition or the stronger
centroid accuracy. The explicit polynomial avoids relying on
asymptotic notation: the bounds above give the complete certificate.

The primary-source comparison was checked directly. Section 1.3 defines
compact witnesses as rational feasible points of polynomial bit length;
Table 1 leaves their existence for exact convex quartic programming
unknown. Appendix C gives a sextic with only an irrational zero and
proves the corresponding impossibility for univariate quartics in
Lemma C.3. The bivariate example above therefore gives a negative answer
to that rational-witness possibility; it does not contradict the
univariate lemma or settle exact decision complexity.
[Slot--Steurer--Wiedmer, version 1, Table 1 and Appendix C](https://arxiv.org/html/2511.03440v1).
The [current arXiv record](https://arxiv.org/abs/2511.03440) showed only
version 1 when checked. Targeted searches did not locate a later primary
resolution. This limited search is not a proof of publication novelty.

Targeted verification used an independent inline Python/SymPy command.
It checked the root interval by exact rational cubing, all interval
bounds used above, the expanded integer coefficients of `A`, vanishing
of `F` and its gradient modulo `r^3-2`, `det J=6`, the complete
translated identity, the cubic homogeneous component, and the final
scalar curvature bound. Every check passed. The global matrix estimate
was audited symbolically as above, rather than inferred from numerical
sampling. The retained checker was inspected without rerunning its
overlapping checks. A second targeted inline command verified that the
expanded integer coefficients are all below `2^30` in absolute value
and checked this review's local link, display delimiters, newline,
whitespace, and control characters. It passed. The rational root
interval also places the zero strictly inside the stated box `[1,2]^2`.
No project-wide verification or CI inspection was performed.
