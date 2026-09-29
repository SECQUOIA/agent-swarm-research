# Rational SOS multipliers for quadratic perturbations

Date: 2026-09-28. Status: complete proof passed
[fresh adversarial review](rational-quadratic-perturbation-multipliers-review.md).
Publication priority remains unestablished.

The quadratic multiplier argument extends to several inhomogeneous
quadratic relations at once. It also permits an arbitrary rational
quadratic form in those relations. The baseline need not be convex.
The useful hypotheses are a quadratic with positive definite leading
matrix in the span of the baseline factors, and affine polynomial
membership of the target relations in their ideal.

## Theorem and input

Let \(n,m,s\ge1\), and let
\(q_1,\ldots,q_m\in\mathbb Q[X_1,\ldots,X_n]\) have degree at
most two. Set
\[
                    F_0=\sum_{i=1}^m q_i^2,\qquad
                    h=1+\|X\|^2.
\]
Suppose the rational span of the \(q_i\) contains
\[
 G=X^{\mathsf T}HX+\ell^{\mathsf T}X+c,\qquad H\succ0.
                                                        \tag{1}
\]
Let \(R_1,\ldots,R_s\) be arbitrary rational polynomials of degree
at most two, each in
\[
 W=\operatorname{span}_{\mathbb Q}
       \{q_i,X_jq_i:1\le i\le m,\ 1\le j\le n\}.
                                                        \tag{2}
\]
Thus \(R_a=\sum_i a_{ai}(X)q_i\) for affine rational
polynomials \(a_{ai}\). The targets may have nonzero linear and
constant terms.

**Theorem.** For every sufficiently large rational \(\lambda>0\),
\[
                    h\left(\lambda F_0-\sum_{a=1}^sR_a^2\right)
                       \in\Sigma\mathbb Q[X]^2.
                                                        \tag{3}
\]
A valid integer threshold and a rational SOS certificate can be
constructed in deterministic polynomial time, with polynomial bit
length in the explicit rational input. Every square factor has degree
at most three.
This bound uses the constructed integer threshold as the scale. For
an externally prescribed larger rational scale, its bit length is
also counted as input.

More generally, for any supplied rational symmetric
\(J\in\mathbb Q^{s\times s}\), the same conclusion holds for
\[
                  h(\lambda F_0-R^{\mathsf T}JR),
 \qquad R=(R_1,\ldots,R_s)^{\mathsf T}.
                                                        \tag{4}
\]
No positivity assumption on \(J\) is required.

The rational polynomial \(G\) in (1) is part of the supplied input.
The algorithm does not claim to discover such a positive definite
quadratic in an arbitrary span.
The span coordinates for \(G\) and the \(R_a\) can be supplied
or found by rational coefficient matching through degree three.
Their bit lengths are polynomial by minor bounds for rational linear
systems. Positive definiteness of the supplied \(H\) is checked
by exact rational linear algebra.

## A common positive Gram matrix

Set \(X_0=1\), and use the possibly redundant list
\[
 w=(X_jq_i)_{\substack{0\le j\le n\\1\le i\le m}},
 \qquad d=m(n+1).
                                                        \tag{5}
\]
Then \(hF_0=w^{\mathsf T}w\). Let \(g,a_1,\ldots,a_s\)
be rational coordinate vectors satisfying
\[
 G=g^{\mathsf T}w,\qquad R_a=a_a^{\mathsf T}w,
\]
and let the columns of \(U\in\mathbb Q^{d\times n}\) express
\(X_jG\) in \(w\). Such columns exist because \(G\) is a
constant linear combination of the \(q_i\).

Write each target, with a symmetric rational \(T_a\), as
\[
 R_a=X^{\mathsf T}T_aX+r_a^{\mathsf T}X+s_a.
                                                        \tag{6}
\]
Put
\[
\begin{aligned}
 b_a&=XR_a,\\
 A&=c\sum_a a_aa_a^{\mathsf T}
       -\frac12\sum_a s_a(ga_a^{\mathsf T}+a_ag^{\mathsf T}),\\
 C_a&=\frac{a_a\ell^{\mathsf T}-UT_a-gr_a^{\mathsf T}}2,\qquad
 C=(C_1\ \cdots\ C_s),\\
 \mathcal H&=I_s\otimes H,\qquad
 v=(w,b_1,\ldots,b_s)^{\mathsf T}.
\end{aligned}
                                                        \tag{7}
\]
The vector \(v\) has \(d+sn\) entries of degree at most three.
The exact zero identity is
\[
             v^{\mathsf T}
             \begin{pmatrix}A&C\\C^{\mathsf T}&\mathcal H\end{pmatrix}
             v=0.
                                                        \tag{8}
\]
To verify all inhomogeneous terms, consider one target. Its contribution
to the left side is
\[
\begin{aligned}
 &b_a^{\mathsf T}Hb_a+R_a\ell^{\mathsf T}b_a+cR_a^2\\
 &\quad -(XG)^{\mathsf T}T_ab_a-G r_a^{\mathsf T}b_a
                  -s_aGR_a\\
 &=GR_a^2-GR_a(X^{\mathsf T}T_aX+r_a^{\mathsf T}X+s_a)=0.
\end{aligned}
\]
Summation proves (8). The additional constant term in \(A\)
and the additional \(gr_a^{\mathsf T}\) term in \(C_a\)
are necessary.

Define
\[
 \eta=\frac{\det H}{(\operatorname{tr}H)^{n-1}}>0,\qquad
 B_A=\sum_{i,j}|A_{ij}|,
\]
and choose
\[
 \varepsilon=\min\left\{
 1,\ \frac1{2(1+B_A)},\
 \frac{\eta}{4(1+\|C\|_F^2)}
 \right\}>0.
                                                        \tag{9}
\]
The rational Gram matrix
\[
 Q_\varepsilon=
 \begin{pmatrix}
 I_d+\varepsilon A&\varepsilon C\\
 \varepsilon C^{\mathsf T}&\varepsilon\mathcal H
 \end{pmatrix}
                                                        \tag{10}
\]
represents \(hF_0\) on \(v\), by (8).

The estimate \(\|A\|_{\rm op}\le B_A\) gives
\(I_d+\varepsilon A\succeq I_d/2\). Its inverse has norm at
most two. Since \(\mathcal H\succeq\eta I\), the Schur
complement in (10) is at least
\[
       (\varepsilon\eta-2\varepsilon^2\|C\|_F^2)I
                    \succeq \frac{\varepsilon\eta}{2}I.
                                                        \tag{11}
\]
Thus \(Q_\varepsilon\succ0\), regardless of redundancies or
linear dependencies among the targets or the entries of \(v\).
The argument also covers constant, linear, and zero targets when
they satisfy (2).

## Subtraction and arbitrary symmetric perturbations

Let \(A_R=(a_1\ \cdots\ a_s)\), and put
\[
 D_J=\operatorname{diag}(A_RJA_R^{\mathsf T},J\otimes I_n).
                                                        \tag{12}
\]
With the target-major order of \(b_1,\ldots,b_s\),
\[
                 v^{\mathsf T}D_Jv=hR^{\mathsf T}JR.
                                                        \tag{13}
\]
Let \(t=d+sn\), and define
\[
 \delta=\frac{\det Q_\varepsilon}
                   {(\operatorname{tr}Q_\varepsilon)^{t-1}}>0,
 \qquad
 B_J=\max_i\sum_j|(D_J)_{ij}|.
                                                        \tag{14}
\]
The usual determinant estimate gives \(Q_\varepsilon\succeq\delta I\),
and symmetry gives \(\|D_J\|_{\rm op}\le B_J\). Therefore any
rational
\[
                       \lambda\ge\frac{B_J+1}{\delta}
                                                        \tag{15}
\]
satisfies
\[
 \lambda Q_\varepsilon-D_J\succeq I,\qquad
 h(\lambda F_0-R^{\mathsf T}JR)
      =v^{\mathsf T}(\lambda Q_\varepsilon-D_J)v.
                                                        \tag{16}
\]
Taking the ceiling of (15) supplies the promised integer threshold.
The sum-of-squares subtraction (3) is the case \(J=I_s\).

## Size, rational functions, and convexity

The matrices have polynomial dimension in \(n,m,s\), and their
entries have polynomial bit length. Exact determinants, rational
inverses, powers with polynomial exponents, and coefficient matching
therefore give the claimed polynomial-time construction.

Rational LDL factorization of (16), followed by the
[binary rational-square expansion](rational-tower-quadratic-denominator.md#4-polynomial-construction-and-certificate-size),
produces polynomially many rational polynomial square factors in
deterministic polynomial time. This avoids an assumption about the
complexity of finding four integer squares.

Writing \(P=\lambda F_0-R^{\mathsf T}JR\) and
\(hP=\sum_\ell f_\ell^2\), one obtains
\[
 P=\sum_\ell(f_\ell/h)^2+
                   \sum_{j,\ell}(X_jf_\ell/h)^2.
                                                        \tag{17}
\]
The numerators have degree at most four, and the common denominator
has degree two and no real zeros. This theorem alone does not say
that degree two is necessary: the polynomial \(P\) may already
be rational SOS.

If a rational positive definite full Hessian Gram \(M\) for \(F_0\)
is also supplied as part of the input, the choice of \(\lambda\)
can preserve strict SOS-convexity. The quartic \(R^{\mathsf T}JR\) has a
rational, possibly indefinite, Hessian Gram \(B\) on
\((u,X\otimes u)\), obtained by coefficient matching. Such a Gram
always exists for a rational quartic, because every monomial of its
Hessian biform is a product of two entries of that vector. A rational
bound on \(\|B\|_{\rm op}\), together with
\(\mu=\det M/(\operatorname{tr}M)^{\dim M-1}\), gives the extra
threshold
\[
                         \lambda\ge(1+\|B\|_{\rm bound})/\mu.
                                                        \tag{18}
\]
All data and this threshold retain polynomial bit length.

At any common zero of the \(q_i\), condition (2) makes every
\(R_a\) vanish, so \(P\) and its gradient vanish there.
If (18) is imposed, that point is consequently the unique global
minimizer with value zero. This additional conclusion needs a common
zero; the multiplier theorem itself does not assume one.

## Scope and questions

The proof extends the
[homogeneous single-relation lemma](rational-tower-quadratic-denominator.md)
by retaining the missing linear and constant terms, and by adding
several positive lower Gram blocks at once. It applies to every
quartic in the span of products of a supplied family of quadratic
relations satisfying (2). It does not cover an arbitrary quartic
that merely has value and gradient zero at a given point.

The hypothesis concerns affine polynomial membership of a quadratic
target in the baseline ideal. Membership with higher-degree
coefficients is treated in the separately reviewed
[higher-membership extension](rational-quadratic-multipliers-higher-membership.md).
Also, replacing the quadratic
targets by genuine higher-degree polynomials cannot give the same
statement: their squared negative leading term can make
\(\lambda F_0-\sum R_a^2\) negative at infinity for every \(\lambda\).

The lemma provides an exact certificate operation that avoids
recovering a common algebraic field of zeros. The explicit membership
and positive quadratic part must be available or computed first.
Its usefulness in a solver, and its novelty relative to established
denominator and ideal methods, need further assessment. No numerical
speedup or general complexity lower bound is asserted.
The [primary-source comparison](rational-quadratic-multiplier-prior.md)
records the closest examined frameworks and examples showing why
the hypotheses matter.

Fresh review checked the inhomogeneous identity, simultaneous blocks,
arbitrary symmetric perturbation, rational size bounds, and optional
convexity statement. It required one input clarification: the optional
positive definite Hessian Gram must be supplied, not merely assumed
to exist. The author independently rechecked that correction and the
complete review.
The higher-membership reviewer subsequently requested an explicit
complexity convention for a prescribed larger scale. Its bit length
must be counted as input; the displayed construction itself chooses a
scale of polynomial bit length.

The reviewer's retained targeted command was:

~~~text
python research-20260927/check_quadratic_perturbation_multiplier_review.py
~~~

All three exact stress cases passed, including an indefinite target
matrix and zero, constant, and linear targets. The author inspected
the checker without rerunning the same computation. These finite
checks support the formulas; they do not prove the universal theorem.
No project-wide verification, CI inspection, or Lean formalization was
performed.
A targeted inline Python check also passed for this note and its
review: five local links, math delimiters, whitespace, control
characters, and final newlines were valid.
