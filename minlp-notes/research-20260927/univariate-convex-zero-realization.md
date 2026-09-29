# Rational convex multipliers preserving an isolated univariate zero

Date: 2026-09-28. Status: independently reviewed proof with a scoped
primary comparison. This is a supplement to the fixed-degree
[multivariate quartic theorem](general-strongly-convex-quartic-singleton.md),
not a replacement for it.

Every real algebraic number with exactly one real conjugate is the
unique zero of some globally strongly convex rational univariate
polynomial. The polynomial degree is not fixed. The argument uses a
rational center that approaches the zero as the multiplier exponent
increases; a fixed rational center does not suffice for the proof.

## A multiplier lemma

**Lemma.** Let $f\in\mathbb R[x]$ be nonnegative, with a unique real zero
$\alpha$, and suppose $f''(\alpha)>0$. There exist an integer $N\geq2$
and a rational number $c$ such that

\[
 g(x)=f(x)\bigl(1+(x-c)^2\bigr)^N
 \tag{1}
\]

is globally strongly convex. Its only real zero remains $\alpha$.
In particular, if $f$ has rational coefficients, so does $g$.

**Proof.** Since $f\geq0$ and $f(\alpha)=0$, we have
$f'(\alpha)=0$. Choose $r>0$ and $m,M>0$ such that

\[
 m\leq f''(x)\leq M\quad\text{whenever }|x-\alpha|\leq r.
 \tag{2}
\]

On this interval, $f'(x)$ has the sign of $x-\alpha$, and
$|f'(x)|\leq M|x-\alpha|$.

The nonconstant nonnegative polynomial $f$ has positive leading
coefficient and even degree. Thus there exists $R>|\alpha|+r+1$ such
that $f''(x)>0$ and $xf'(x)>0$ whenever $|x|\geq R$.
For every $c$ satisfying $|c-\alpha|\leq r/2$, the signs of $x-c$ and
$x$ agree in that outer region.

Consider the compact set

\[
 A=\{x:|x|\leq R,\ |x-\alpha|\geq r\}.
\]

It contains no zero of $f$. Choose positive bounds

\[
 a\leq\min_{x\in A}f(x),\quad
 B_0\geq\max_{|x|\leq R}|f''(x)|,\quad
 B_1\geq\max_{|x|\leq R}|f'(x)|.
\]

Write $Z=R+|\alpha|+r/2$ and

\[
 b=\frac{a r^2}{(1+Z^2)^2}>0.
\]

These bounds are independent of the particular $c$ in the interval
$|c-\alpha|\leq r/2$. Choose an integer $N\geq2$ large enough that

\[
 b(N-1)\geq2B_1+B_0+1.
 \tag{3}
\]

After choosing $N$, choose a rational $c$ so close to $\alpha$ that

\[
 \delta:=|c-\alpha|\leq r/2,
 \qquad \delta^2\leq\frac{m}{8NM}.
 \tag{4}
\]

Such a rational number exists by density. Put $z=x-c$ and
$w=(1+z^2)^N$. Direct differentiation gives the exact identity

\[
 \frac{g''}{w}
 =f''+\frac{4Nz}{1+z^2}f'
 +\left[\frac{2N}{1+z^2}
             +\frac{4N(N-1)z^2}{(1+z^2)^2}\right]f.
 \tag{5}
\]

On $|x-\alpha|\leq r$, the last term is nonnegative. The middle
term is also nonnegative except possibly when $x$ lies between $c$ and
$\alpha$. On that small interval, $|z|\leq\delta$ and
$|f'(x)|\leq M\delta$. Therefore (2), (4), and (5) give

\[
 \frac{g''(x)}{w(x)}\geq m-4NM\delta^2\geq m/2>0.
 \tag{6}
\]

On $A$, we have $r/2\leq|z|\leq Z$. The elementary bound
$|z|/(1+z^2)\leq1/2$ and (5) yield

\[
 \frac{g''(x)}{w(x)}
 \geq-B_0-2NB_1+bN(N-1)
 \geq N(B_0+1)-B_0>0.
 \tag{7}
\]

Finally, when $|x|\geq R$, the first two terms in (5) are positive
and the last is nonnegative. Hence $g''$ is positive on all of the real
line. It is a polynomial of positive even degree with positive leading
coefficient, so it tends to infinity at both ends. Its global minimum
is attained and is strictly positive. This proves global strong
convexity. The multiplier in (1) is everywhere positive, so it does not
change the real zero set. $\square$

## The algebraic characterization

Let $p\in\mathbb Q[T]$ be the minimal polynomial of a real algebraic
number $\alpha$ and assume it has exactly one real root. Then
$f=p^2$ is nonnegative and has only that zero. Characteristic zero makes
$p$ separable, so

\[
 f''(\alpha)=2p'(\alpha)^2>0.
\]

The lemma therefore gives a rational globally strongly convex
univariate polynomial with unique zero $\alpha$.

Conversely, if a rational univariate polynomial has $\alpha$ as its
only real zero, every real conjugate of $\alpha$ is also a zero because
the minimal polynomial divides it. Thus $\alpha$ has exactly one real
conjugate. Convexity is not needed for this direction.

The resulting equivalence is therefore

\[
 \begin{gathered}
 \alpha\text{ is real algebraic with exactly one real conjugate}\\
 \Longleftrightarrow\\
 \alpha\text{ is the unique zero of a rational globally strongly
 convex univariate polynomial}.
 \end{gathered}
\]

This statement does not claim a degree bound polynomial in the dense
input length, a polynomial-time expanded output, or a quartic
univariate realization. Those would require further estimates or can
fail in fixed degree. The multivariate theorem retains degree four by
using auxiliary coordinates instead.

## Why the center must be chosen carefully

The assertion that $f(x)(1+x^2)^N$ eventually becomes convex is false
when $f$ has a zero away from the fixed center. For example, put
$f(x)=(x-1)^2$ and evaluate (5) with $c=0$ at $x_N=1-2/N$.
As $N\to\infty$,

\[
 \frac{[f(x)(1+x^2)^N]''\big|_{x=x_N}}
      {(1+x_N^2)^N}\longrightarrow-2.
\]

Thus the products fail to be convex for all sufficiently large $N$.
The choice (4), made after (3), is what controls this region of negative
curvature. Merely invoking a convexification theorem for strictly
positive polynomials would not address it.

## Closest inspected prior

[Kurdyka and Spodzieja, *Convexifying positive polynomials and sums of
squares approximation*](https://arxiv.org/pdf/1507.06191), Remark 3.2,
already treats a univariate polynomial that is positive on a bounded
interval except possibly at the multiplier center zero. It states
eventual strict convexity there. Lemma 3.3 treats unbounded intervals
under strict positivity, and Remark 3.4 allows a shifted multiplier center
under that hypothesis. Theorem 5.5 assumes a positive lower bound;
Corollary 5.7 obtains convexity after a perturbation that changes zeros.

The distinction in this note is modest: a nondegenerate zero permits a
nearby rational center, preserving rational coefficients and the exact
irrational zero. The local estimate (6) supplies that arithmetic step.
Convexification by polynomial multipliers itself is established prior.
The cited passages were read directly; no exhaustive novelty claim is
made. The [independent adversarial review](univariate-convex-zero-realization-review.md)
found no gap in the proof and confirmed the modest prior positioning.
This remains a useful supplement rather than a separate main contribution.

A targeted inline `python - <<'PY'` command using SymPy verified the
exact differentiation identity (5) and the fixed-center limit $-2$.
The same command checked this note's local links, display delimiters,
whitespace, and final newline. All checks passed. They do not replace
independent review of the global argument. No project-wide or CI check
was run.
