# A strongly convex integer quartic with an irrational zero

Date: 2026-09-28. Status: explicit construction, exact targeted checks,
and [independent review](convex-quartic-irrational-zero-review.md) complete.
An [additional audit](convex-quartic-root-audit.md) independently checks
the compact example after developing a different construction.
Publication priority is not established.

There is a globally strongly convex polynomial in $\mathbb Z[x,y]$ of
degree four whose minimum is zero and whose unique minimizer is
$(\sqrt[3]{2},\sqrt[3]{4})$. Consequently, a nonempty zero sublevel set of
a rational globally convex quartic need not contain any rational point.

## The polynomial

Define

\[
 q_1=x^2-y,\qquad q_2=y^2-2x,
\]

\[
 A=12599x^2-10000xy+7937y^2-15874x-12599y+20000,
\]

and set

\[
 \boxed{F(x,y)=A(x,y)^2+10000\bigl(q_1(x,y)^2+q_2(x,y)^2\bigr).} \tag{1}
\]

**Proposition.** For every $(x,y)\in\mathbb R^2$,

\[
 \nabla^2F(x,y)\succeq4124I.
 \tag{2}
\]

Moreover, with $r=\sqrt[3]{2}$ and $p=(r,r^2)$,

\[
 \{(x,y):F(x,y)\leq0\}=\{p\},\qquad p\notin\mathbb Q^2.
 \tag{3}
\]

All expanded coefficients in (1) are integers of absolute value below
$2^{30}$. The construction also works on the rational box $[1,2]^2$;
its unique feasible point is in the interior of that box.

## Exact bounds near the zero

The starting point is the [three-quadratic singleton](convex-qcqp-rationality-boundary.md).
Its third quadratic is

\[
 q_3=(x-y)^2-2x-y+4,
\]

and its nonnegative exposing quadratic is

\[
 (2r-1)q_1+(r^2-1)q_2+q_3
  =(x-r,y-r^2)
    \begin{pmatrix}2r&-1\\-1&r^2\end{pmatrix}
    (x-r,y-r^2)^{\mathsf T}.
 \tag{4}
\]

The rational polynomial $A$ approximates $5000$ times (4):

\[
 A=7599q_1+2937q_2+5000q_3.
 \tag{5}
\]

Write

\[
 a=\frac{7599}{5000},\quad b=\frac{2937}{5000},\quad
 G=\frac A{5000},\quad \varepsilon=\frac1{2500},\quad
 f=\frac{F}{5000^2}=G^2+\varepsilon(q_1^2+q_2^2).
\]

For a displacement $u=(u_1,u_2)$ from $p$, let

\[
 j_1=(2r,-1)^{\mathsf T},\qquad j_2=(-2,2r^2)^{\mathsf T},\qquad
 J=\begin{pmatrix}j_1^{\mathsf T}\\j_2^{\mathsf T}\end{pmatrix}.
\]

Then

\[
 q_1(p+u)=j_1^{\mathsf T}u+u_1^2,\qquad
 q_2(p+u)=j_2^{\mathsf T}u+u_2^2,
\]

\[
 G(p+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,\qquad
 H=\begin{pmatrix}12599/5000&-1\\-1&7937/5000\end{pmatrix}.
 \tag{6}
\]

Here all three $q_i$ vanish at $p$, and

\[
 \ell=-d_1j_1-d_2j_2,\qquad
 d_1=2r-1-a,\qquad d_2=r^2-1-b.
\]

The following bounds use the Euclidean norm and its induced operator norm:

\[
 H\succeq\tfrac12I,\quad \|H\|<5,\quad
 \|j_1\|<4,\quad\|j_2\|<4,\quad J^{\mathsf T}J\succeq I,
 \quad \|\ell\|<\frac1{5000}.
 \tag{7}
\]

To check them, diagonal dominance gives
$H\succeq(2937/5000)I\succ I/2$, and its trace is less than five.
Since $r<13/10$, both $\|j_i\|<4$. Also

\[
 \det J=4r^3-2=6,\qquad
 \operatorname{tr}(J^{\mathsf T}J)=5+4r^2+8r<23.
\]

Thus the smaller eigenvalue of $J^{\mathsf T}J$ is greater than
$36/23>1$. Finally, exact cubing gives

\[
 \frac{1259921}{10^6}<r<\frac{1259922}{10^6}.
\]

Substitution into the increasing expressions for $d_1,d_2$ gives

\[
 d_1,d_2>0,\qquad
 d_1+d_2<\frac{11861521}{250000000000}<\frac1{20000}.
\]

Therefore $\|\ell\|\leq4(d_1+d_2)<1/5000$, completing (7).

## Global convexity

Put $h(u)=u^{\mathsf T}Hu$ and decompose $f(p+u)=f_2+f_3+f_4$ into
homogeneous parts:

\[
 \begin{aligned}
 f_2&=(\ell^{\mathsf T}u)^2+
       \varepsilon\bigl((j_1^{\mathsf T}u)^2+(j_2^{\mathsf T}u)^2\bigr),\\
 f_3&=2(\ell^{\mathsf T}u)h(u)+
       2\varepsilon\bigl((j_1^{\mathsf T}u)u_1^2+
                          (j_2^{\mathsf T}u)u_2^2\bigr),\\
 f_4&=h(u)^2+\varepsilon(u_1^4+u_2^4).
 \end{aligned}
 \tag{8}
\]

By (7),

\[
 \nabla^2f_2\succeq2\varepsilon I.
 \tag{9}
\]

Furthermore,

\[
 \nabla^2(h^2)=8(Hu)(Hu)^{\mathsf T}+4hH
       \succeq\|u\|^2I.
\]

The two remaining quartic terms have positive semidefinite Hessians, so

\[
 \nabla^2f_4\succeq\|u\|^2I.
 \tag{10}
\]

For any real vector $v$ and real symmetric matrix $T$, direct
differentiation gives

\[
 \nabla^2\bigl(2(v^{\mathsf T}u)(u^{\mathsf T}Tu)\bigr)
 =4\bigl((v^{\mathsf T}u)T+v(Tu)^{\mathsf T}+(Tu)v^{\mathsf T}\bigr).
\]

Its operator norm is at most $12\|v\|\|T\|\|u\|$. Apply this to
each of the three terms in $f_3$, using (7) and the coordinate matrices
of norm one. The result is

\[
 \|\nabla^2f_3\|
 \leq\left(\frac{60}{5000}+96\varepsilon\right)\|u\|
 =\frac{63}{1250}\|u\|.
 \tag{11}
\]

Combining (9)--(11) and completing the square in $t=\|u\|$ gives

\[
 \begin{aligned}
 \nabla^2 f(p+u)
 &\succeq\left(t^2-\frac{63}{1250}t+\frac1{1250}\right)I\\
 &=\left(\left(t-\frac{63}{2500}\right)^2+
          \frac{1031}{6250000}\right)I.
 \end{aligned}
\]

Multiplying by $5000^2$ proves (2) on all of $\mathbb R^2$.
Equation (1) is nonnegative and vanishes at $p$. Strong convexity therefore
makes $p$ its unique zero and minimizer. Eisenstein's criterion for
$t^3-2$ shows that $r$ is irrational, proving (3).

## Scope and the published question

[Slot, Steurer, and Wiedmer, *Hesse's Redemption: Efficient Convex
Polynomial Programming*, arXiv:2511.03440v1, Table 1 and Appendix C](https://arxiv.org/html/2511.03440v1#A3)
leave open whether exact feasibility for globally convex rational quartics
always has a rational witness of polynomial bit length. Their Appendix C
gives a convex sextic with an irrational unique zero and proves that a
univariate convex rational quartic cannot have a rational minimum attained
at an irrational point. The example above gives a negative answer to the
quartic witness question in two variables. It does not contradict the
univariate statement or the paper's approximate optimization results.

This is an obstruction to rational feasible-point witnesses. It gives no
hardness result for exact decision and does not exclude short certificates
in other formats. The displayed point already has a short algebraic
description. The arXiv landing page showed only version 1 when checked on
2026-09-28; that fact alone does not settle publication priority.

A limited follow-up search inspected [Ahmadi and Hall, *On Approximate
Computation of Critical Points*, the 2026 manuscript hosted by
Optimization Online](https://optimization-online.org/wp-content/uploads/2026/01/Approx_Crit_Point_Ahmadi_Hall.pdf).
The inspection covered its occurrences of “rational” and “convex” and
its Section 4 discussion of the Slot--Steurer--Wiedmer result. That
discussion concerns approximate critical points; the inspected passages
did not give a convex quartic with an irrational zero or address the
exact rational-witness question. This was a targeted relevance check,
not a full audit of that paper or of all subsequent literature.

## Targeted verification

[The exact verification script](check_convex_quartic_irrational_zero.py)
checks the polynomial identities modulo $r^3-2$, the rational root
interval, all numerical inequalities used in (7), the homogeneous
decomposition, the cubic Hessian identity, and the final square-completion
constant. It uses rational arithmetic throughout. The global matrix
inequalities are proved above, without sampling Hessians.

Command actually run:

```sh
python research-20260927/check_convex_quartic_irrational_zero.py
```

Result: passed. No project-wide or CI checks were run.

The standalone
[Lean file](../formal/ConvexQuarticIrrationalZero.lean) also verifies the
exact zero characterization, existence and uniqueness of the real zero,
strict positivity at every rational pair, and a uniform lower bound of
\(4096\) on the second derivative in every unit direction. The last
statement uses formal differentiation and the exact
[rational sum-of-squares certificate](convex-quartic-rational-sos.md).
The file also proves global convexity as `ConvexOn ℝ Set.univ` on
`ℝ × ℝ`, by applying the second-derivative criterion on affine lines. Its
[verification record](convex-quartic-lean-verification.md) and independent
[correspondence review](convex-quartic-lean-correspondence-review.md)
state the precise scope. The stronger constant \(4124\) retains the
proof above and the separate exact checks and review. The Lean file states
the curvature bound through actual second derivatives along affine lines;
it does not separately package the standard strong-convexity consequence.

The independent reviewer reconstructed the translated polynomial and all
curvature bounds, checked the constants with separate exact calculations,
and confirmed the primary-source comparison. The review found no
mathematical defect. The additional audit independently checked the same
global Hessian bound and the zero set.
