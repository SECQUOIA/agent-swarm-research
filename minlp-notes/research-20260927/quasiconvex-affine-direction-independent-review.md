# Independent review of quasiconvex polynomial affine directions

Date: 2026-09-28. Scope: Section 4 of
[the projection review](quasiconvex-polynomial-projection-review.md).
The coefficient lemma and its Hessian-kernel consequence are correct under
their stated hypotheses. The coefficient lemma also holds for continuous
functions, and the Hessian consequence holds for globally \(C^2\)
functions. This review does not establish novelty or verify the larger
integer algorithm.

## 1. Independent proof of the coefficient lemma

Let the polynomial

\[
q(y,t)=a(y)t+b(y)
\]

be quasiconvex on its entire real vector space: every weak sublevel is
convex. Restriction to any affine line in the \(y\)-space preserves this
property. It therefore suffices to show that a univariate coefficient
\(a(s)\) is constant.

If \(a\equiv0\), there is nothing to prove. Otherwise choose a nonempty
open interval \(I\) on which \(a\) has constant nonzero sign. At every
real level \(\alpha\), the sublevel in \(I\times\mathbb R\) is the
hypograph of

\[
h_\alpha(s)=\frac{\alpha-b(s)}{a(s)}
\]

when \(a>0\), and is its epigraph when \(a<0\). Thus \(h_\alpha\) is
concave in the first case and convex in the second. For fixed
\(s_1,s_2\in I\) and \(\lambda\in[0,1]\), the corresponding Jensen
inequality is an affine inequality in \(\alpha\), valid for every
\(\alpha\in\mathbb R\). Its coefficient on \(\alpha\) must be zero.
Consequently \(1/a\) satisfies Jensen equality on \(I\). It is continuous,
so

\[
\frac1{a(s)}=As+B\qquad(s\in I).
\]

The polynomial \(a(s)(As+B)-1\) vanishes on an open interval and therefore
vanishes identically. A nonconstant polynomial cannot have a polynomial
multiplicative inverse. Hence \(A=0\) and \(a(s)\) is a nonzero constant.

Every affine-line restriction of \(a(y)\) is therefore constant. Any two
points lie on such a line, proving that \(a(y)\) is constant. This argument
also covers restrictions on which \(a\) vanishes identically. It does not
assume that \(a\) is everywhere nonzero before reaching the conclusion.

The derivative proof in the reviewed note is equivalent: the coefficient
of \(\alpha\) in \(h_\alpha''\) must vanish. Neither proof assumes that
the Hessian of a quasiconvex polynomial is positive semidefinite.

### Continuous strengthening

The coefficient lemma remains valid for any continuous function
\(q(y,t)=a(y)t+b(y)\) that is globally quasiconvex on the whole real
vector space. This stronger proof was communicated during review and
independently checked here. Continuity of \(q\) implies continuity of
\(a(y)=q(y,1)-q(y,0)\) and \(b(y)=q(y,0)\).

First recall a property of closed convex sets. If a closed convex set
\(S\) contains a complete line \(p_0+\mathbb R e\), then for every
\(p\in S\) and every \(\lambda\in\mathbb R\),

\[
(1-\varepsilon)p+
\varepsilon\left(p_0+\frac{\lambda}{\varepsilon}e\right)
\in S\qquad(0<\varepsilon<1).
\]

Taking the limit as \(\varepsilon\) tends to zero gives
\(p+\lambda e\in S\). Thus \(S\) is invariant along that line direction.

Suppose \(a(y_0)=0\). The closed convex sublevel
\(S=\{q\le b(y_0)\}\) contains the complete vertical line through
\((y_0,0)\). If \(a(y_1)\ne0\), some \(t_1\) satisfies
\(q(y_1,t_1)\le b(y_0)\). The line property would put every point
\((y_1,t)\) in \(S\), contradicting the nonzero slope. Consequently
one zero coefficient forces \(a\equiv0\).

Otherwise \(a\) is continuous and nowhere zero on a connected space, so
its sign is fixed. The same all-level Jensen argument used above now
applies to every pair of points in the entire \(y\)-space. It makes
\(1/a\) globally affine. A globally affine real function with a fixed
nonzero sign on a full real vector space must be constant. Hence \(a\)
is constant in this case too. Polynomiality is unnecessary for this
coefficient conclusion.

## 2. Hessian-kernel consequence

Let \(g(z,x)\) be globally quasiconvex and polynomial, and let \(d\) be a
fixed continuous direction. Suppose

\[
\nabla^2_{xx}g(z,x)d\equiv0.
\]

For \(d\ne0\), choose an invertible linear change of continuous coordinates
whose last column is \(d\), and denote its last coordinate by \(t\).
For the transformed polynomial \(q(y,t)\), with all remaining variables
including \(z\) collected into \(y\),

\[
q_{tt}=d^T\nabla^2_{xx}g\,d\equiv0.
\]

Thus \(q\) has degree at most one in \(t\). The coefficient lemma gives
constant \(q_t\), so every derivative of \(q_t\) vanishes. Transforming
back yields

\[
\nabla^2 g(z,x)(0,d)\equiv0.
\]

The reverse implication follows by taking the continuous block. The zero
direction is immediate. Applying the argument separately to each row proves
equality of the common polynomial kernels in the reviewed note.

In fact, the proof establishes the stronger pointwise-in-direction
implication

\[
d^T\nabla^2_{xx}g(z,x)d\equiv0
\quad\Longrightarrow\quad
\nabla^2 g(z,x)(0,d)\equiv0.
\]

This observation is not needed for the claimed kernel-computation method.

The same implication holds for any globally \(C^2\) quasiconvex
function. After the same linear change of coordinates, \(q_{tt}\equiv0\)
implies affine dependence on \(t\) by one-variable calculus. The
continuous strengthening makes \(q_t\) constant in all variables, so
its full gradient vanishes. Polynomiality is needed for the particular
coefficient-matrix computation in the larger theorem, not for this
structural implication.

## 3. Hypotheses that cannot be dropped casually

- Global joint quasiconvexity includes the variables later constrained to
  be integers. Quasiconvexity separately at each fixed integer value is
  insufficient: \(g(z,x)=zx\) is affine in \(x\) for every fixed \(z\),
  but \(g_{xx}=0\) and \(g_{zx}=1\).
- Convexity of a single sublevel is insufficient. The polynomial
  \(q(s,t)=(1+s^2)t\) has the convex zero sublevel \(t\le0\), but the
  coefficient of \(t\) is not constant. At level one, \((0,1)\) and
  \((2,1/5)\) belong to the sublevel while their midpoint has value \(6/5\).
- Quasiconvexity only on a supplied domain is insufficient in general.
  On the convex domain \(s>0,t<0\), the polynomial \(st\) is quasiconvex:
  its negative sublevels are \(t\le\alpha/s\), the hypographs of concave
  functions for \(\alpha<0\); its nonnegative sublevels are the whole
  domain. Its coefficient on \(t\) is variable.

## 4. Verification and limits

The proof was checked independently through Jensen equality, rather than
assuming the derivative calculation in the original note. A targeted
command, `python -` using `fractions.Fraction` and `sympy`, checked the
level-one counterexample and the Hessian of \(zx\) exactly. A second
`python -` command checked Markdown math delimiters, the local link,
whitespace, control characters, and the final newline. Those calculations
verify the examples, not the
universal statements, which rely on the arguments above.

No literature search, novelty conclusion, project-wide verification, or CI
inspection formed part of this narrowly scoped review.
