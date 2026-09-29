# Degenerate convex quartics: an exact tractable case and failed extensions

Date: 2026-09-28. Status: exploratory frontier note. The elementary
theorem and explicit counterexamples below have been independently
reconstructed by a second agent and checked symbolically where stated.
They do **not** establish a PosSLP upper bound for general convex
quartics. No publication priority is claimed.

The [existing upper bound](../../research-20260927/strong-convex-quartic-posslp-upper.md)
uses a supplied global positive Hessian bound to enter a Newton
neighborhood with polynomially many printed bits. Its fast refinement
then produces the much greater accuracy needed for exact comparison
as a short rational circuit. Removing the curvature assumption remains
a substantial question. Two natural shortcuts fail, while complete
vanishing of the Hessian at a minimizer is an elementary tractable case.

## 1. A fully degenerate minimum is rationally recoverable

**Proposition.** Let \(f\in\mathbb Q[x_1,\ldots,x_n]\) have degree at
most four and be globally convex. Suppose some global minimizer \(p\)
satisfies \(\nabla^2f(p)=0\), meaning the whole Hessian is zero. Then

\[
 \operatorname{argmin}f=\{x:D^3f(x)=0\}.                 \tag{1}
\]

The right side is a nonempty rational affine space. A rational
minimizer, its exact minimum value, and an affine description of all
minimizers can therefore be computed in polynomial bit time by rational
linear algebra. If the minimizer is unique, its coordinates are rational
and have polynomial bit length.

**Proof.** For fixed vectors \(u,v\), the scalar polynomial

\[
 t\longmapsto u^{\mathsf T}\nabla^2f(p+tv)u
\]

is nonnegative on the real line and vanishes at zero. Its linear
coefficient is consequently zero:
\(D^3f(p)[u,u,v]=0\). Polarization in \(u\) gives \(D^3f(p)=0\).
Stationarity and Taylor expansion, which is exact at degree four, give

\[
 f(p+z)=f(p)+Q(z),\qquad
 Q(z)=\frac1{24}D^4f[z,z,z,z].                         \tag{2}
\]

Here \(Q\) is a nonnegative convex homogeneous quartic, possibly zero.
Because \(D^3f\) is affine, its solution set is
\(p+V\), where

\[
 V=\{v:D^4f[v,\cdot,\cdot,\cdot]=0\}.                \tag{3}
\]

Every \(v\in V\) has \(Q(v)=0\), so every point of \(p+V\)
minimizes \(f\). Conversely, suppose \(Q(v)=0\). Homogeneity implies
\(Q(tv)=0\) for every real \(t\). For \(0<a<1\), convexity gives

\[
 Q(z+tv)
 \le (1-a)Q\!\left(\frac z{1-a}\right)
       +aQ\!\left(\frac{tv}a\right)
 =(1-a)^{-3}Q(z).
\]

Letting \(a\downarrow0\) and then applying the same argument in the
opposite direction shows \(Q(z+tv)=Q(z)\). Differentiating this
polynomial identity gives \(D^4f[v,\cdot,\cdot,\cdot]=0\).
This proves (1). The equations in (1) have rational affine coefficients
of polynomial encoding length and at most \(O(n^3)\) rows. Rational
Gaussian elimination proves the computational claims. \(\square\)

The promise can also be recognized within the class of globally convex
inputs: solve \(D^3f(x)=0\); if consistent, choose a rational solution
\(q\), and test \(\nabla f(q)=0\) and \(\nabla^2f(q)=0\). Acceptance
certifies the stated situation. If a fully degenerate minimizer exists,
the proof guarantees that every chosen solution passes both tests.
This procedure does not recognize global convexity itself.

This is a modest structural observation. It separates complete Hessian
vanishing from partial degeneracy; it does not cover, for example,
\(g(x)+y^4\) when the minimizer of \(g\) is irrational. The implication
\(\nabla^2f(p)=0\Rightarrow D^3f(p)=0\) also follows immediately
from existing derivative inequalities; see Section 4.

## 2. Partial degeneracy defeats ordinary Newton and a tempting correction

For \(f(x)=x^4\), ordinary Newton gives \(x_{k+1}=2x_k/3\), hence
only linear convergence. Reaching error \(2^{-2^s}\) by this iteration
from a fixed nonzero start requires \(\Omega(2^s)\) steps. This rules
out directly reusing that iteration count in the existing circuit proof;
it is not an arithmetic-circuit lower bound, since the minimizer is zero.

A stronger obstruction is the rational bivariate quartic

\[
 f(x,y)=(x^2+y^2)^2+xy^2+y^2.                         \tag{4}
\]

It has unique minimizer \((0,0)\), since

\[
 f(x,y)=x^4+y^4+(2x^2+x+1)y^2
\]

and \(2x^2+x+1>0\). Its Hessian has
\(H_{11}=12x^2+4y^2\), and

\[
 \det H=
 24x^2(2x^2+x+1)+4y^2(24x^2-6x+1)+48y^4.             \tag{5}
\]

Both quadratic factors are strictly positive. Thus \(H\succ0\)
off the origin, while \(H(0,0)=\operatorname{diag}(0,2)\).
In particular, (4) is globally convex and the ordinary Newton map
\(N(z)=z-H(z)^{-1}\nabla f(z)\) is defined everywhere except at
the minimizer. Direct calculation gives

\[
 N(0,t)=
 \left(\frac{1-2t^2}{2(1+12t^2)},
       \frac{t(16t^2-1)}{2(1+12t^2)}\right).           \tag{6}
\]

Therefore \(N(0,t)\to(1/2,0)\) as \(t\to0\). An arbitrarily
accurate starting point can leave every sufficiently small Newton
neighborhood in one step. A positive-definite Hessian at all nearby
nonoptimal points is insufficient to prevent this.

One tempting correction is \(T=3N\circ N-2N\). For a homogeneous
quartic with invertible Hessian, Euler's identity gives
\(N(x)=2x/3\); this correction eliminates that linear error. It
would also cancel a differentiable Newton map whose derivative at
the solution had only eigenvalues zero and \(2/3\). But in (4),

\[
 T(0,t)=\left(\frac{13}{24}t^2+O(t^4),
                   \frac58t-\frac{51}{4}t^3+O(t^4)\right). \tag{7}
\]

It consequently fails quadratic local convergence. The assumed
differentiability of the original Newton map was false. These examples
leave other regularized, deflated, or higher-order methods open.

A second shortcut would assume the Hessian kernel at a degenerate
minimizer has a rational basis. This is false even in three variables:

\[
 F(t,u,v)=t^4+2t^2-4t+(u-tv)^2+(u^2+v^2)^2.            \tag{8}
\]

Let \(a\) be the unique real root of \(a^3+a-1=0\). The first
three terms in (8) have derivative \(4(t^3+t-1)\), and the remaining
terms are nonnegative, with \((u^2+v^2)^2=0\) only at \(u=v=0\).
Consequently \(p=(a,0,0)\) is the unique minimizer. Global convexity
requires a separate check; the squared residual is not itself asserted
convex. Put \(y=(u,v)\), \(r=\|y\|\), and \(b=(1,-t)\). The
Hessian blocks are

\[
 H_{tt}=12t^2+4+2v^2,\quad H_{ty}=(-2v,-2u+4tv),\quad
 H_{yy}=2bb^{\mathsf T}+4r^2I+8yy^{\mathsf T}.
\]

For \(r>0\), the cross block has norm at most \((2+4|t|)r\),
and the Schur-complement correction is at most

\[
 H_{ty}H_{yy}^{-1}H_{yt}
 \le(2+4|t|)^2/4\le2+8t^2.
\]

The Schur complement is therefore at least \(4t^2+2+2v^2>0\).
At \(r=0\), the off-diagonal blocks vanish and both diagonal blocks
are positive semidefinite. This proves global convexity. Moreover,

\[
 \ker\nabla^2F(p)=\operatorname{span}\{(0,a,1)\}.        \tag{9}
\]

The cubic has no rational root, so this line contains no nonzero
rational vector. Thus partial degeneracy cannot always be removed by
an exact rational change of coordinates adapted to the kernel. This
does not rule out approximate or algebraic coordinates.

## 3. Why infinitesimal quadratic regularization is not yet a reduction

Suppose \(m=\min f\) is attained at \(p\) with \(\|p\|\le R\).
For \(\varepsilon>0\), define

\[
 f_\varepsilon(x)=f(x)+\varepsilon\|x\|^2,
 \qquad m_\varepsilon=\min f_\varepsilon.
\]

The elementary and useful bound is

\[
                 0\le m_\varepsilon-m\le\varepsilon R^2. \tag{10}
\]

General convex polynomial solution bounds give an \(R\) with polynomial
logarithm; this part of the argument does not require strong convexity.
Likewise, algebraic separation of a nonzero minimum-threshold gap
survives nonuniqueness: all stationary points of a convex polynomial
have the same value, so their value projection is still a singleton.

However, a uniform available separation bound has the form
\(g=2^{-2^{a(L)}}\). Taking
\(\varepsilon\le g/(8\max\{1,R^2\})\) makes (10) small enough
for shifted exact comparisons. Its explicit binary encoding can have
exponential length. Its short repeated-squaring circuit does not solve
this problem: the existing theorem takes explicitly encoded rational
coefficients and curvature \(\mu=2\varepsilon\). Its preliminary
optimization and Newton-neighborhood bounds depend on
\(\log(1/\mu)\), which is now exponential in the original input
length. Substituting the short circuit for the printed coefficient
without a new argument changes the input model of that theorem.

Formal infinitesimals also do not automatically repair the iteration.
For \((x-1)^4+\varepsilon x^2\), Newton from \(x_0=0\), viewed
as rational functions of \(\varepsilon\), has constant term
\(x_k(0)=1-(2/3)^k\) after every finite number of steps. The
minimizer tends to 1 as \(\varepsilon\downarrow0\), so no such
finite iterate has even positive-order infinitesimal error. This
illustrates a missing initialization argument; the example itself is
easy by Section 1. Equality must also be handled by a gap shift:
regularization can turn a zero minimum into a strictly positive one.

Thus (10) is a valid approximation statement, but neither the explicit
nor symbolic regularization route presently yields the desired
polynomial-size exact reduction. No impossibility result for such a
reduction is claimed.

## 4. Sources examined, significance, and verification

The following primary sources were read directly on 2026-09-28.

- Slot, Steurer, and Wiedmer,
  [*Hesse's Redemption: Efficient Convex Polynomial Programming*, v1](https://arxiv.org/html/2511.03440v1),
  Theorem 1.1, Corollary 1.2, Theorem 1.3, and the stated complexity
  comparison. These give bounded-norm minimizers and approximation in
  time polynomial in input size and \(\log(1/\varepsilon)\).
  The structural quadratic lower bound is not a pointwise positive
  Hessian bound on the original objective. The source explicitly
  distinguishes exact comparison from approximation.
- Nesterov,
  [*Quartic Regularity*](https://link.springer.com/article/10.1007/s10013-024-00720-z),
  Vietnam Journal of Mathematics 53 (2025), 553–575, especially Lemma 4
  and the method descriptions. Lemma 4 bounds the third derivative by
  the second and fourth derivatives. Setting the Hessian to zero and
  letting its positive parameter tend to zero yields the derivative
  vanishing used in Section 1. The stated global linear convergence
  does not give the polynomial number of rational refinement steps
  required for doubly exponential accuracy here.

Searches also used the terms “convex quartic singular minimizer
Newton,” “convex polynomial rational minimizer Hessian,” and
“PosSLP convex polynomial.” A 2013 regularized-Newton result surfaced,
but its full text was not retrieved and no theorem from it is used.
The search does not establish novelty of the proposition or examples,
nor settle the general exact-comparison question.

The potential consequence for MINLP is a broader exact arithmetic
interface for convex polynomial node bounds without a strict curvature
certificate. This note establishes no such interface. Its present
contribution is to rule out unsupported proof shortcuts and to
identify a small exact preprocessing case. A successful extension needs
a uniform succinct refinement argument in the partially degenerate
regime, or a different exact reduction. Practical solver value would
additionally require controlled circuit growth and useful benchmarks.

Targeted verification: one inline `python - <<'PY'` command with SymPy
verified the determinant identity (5), the exact Newton formula (6),
and the series (7). It also checked third-derivative linear
reconstruction for a translated fourth power with nonunique minimizers
and a sum of two independent translated fourth powers with a unique
minimizer. A further inline SymPy command checked every Hessian block
and the kernel vector in the three-variable example (8). A second agent
independently proved the fully degenerate proposition and reconstructed
(4)–(7); the author then reran the exact
symbolic checks independently. The general proposition and global
convexity follow from the displayed proofs, not numerical samples.
A targeted inline Python check passed for this note's local links,
paired math delimiters, final newline, and absence of trailing whitespace.
No Lean formalization, project-wide verification, or CI inspection was
performed.
