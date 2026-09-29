# Independent review of the rational rank-one SOS compression

Date: 2026-09-28. Status: no blocking defect found.

The root agent proposed the [compression supplement](cyclic-quartic-square-compression.md)
after the baseline
[cyclic quartic construction](cyclic-quartic-exponential-degree.md)
had passed a separate [fresh review](cyclic-quartic-fresh-review.md).
This reviewer developed the baseline construction but did not develop
the compression lemma. This is an independent review of the new lemma
and its application, not a fresh review of the entire baseline.

The compression reduces the displayed representation from $n+2$ to
$n+1$ integer quadratic squares. It preserves the exact zero, exponential
field degree, global Hessian lower bound after integer scaling,
rational positive definite Hessian Gram certificate, polynomial
construction time, and $O(\log(n+1))$ coefficient-bit bound. This note
does not prove that $n+1$ squares are necessary, and makes no priority
claim for the elementary rational factorization.

## Exact identity

Use the baseline notation $m=n+1$, $M=10^6n^5$,
$Q=32mM^2$, $g_i=z_i/Q$, $G=g^{\mathsf T}q$, and
$R=g^{\mathsf T}g>0$. Choose a positive rational $r$ and put

\[
 t=\frac{R-r^2}{2r},\qquad
 s=\frac{R+r^2}{2r}.
\]

Require $M^{-1}\leq t\leq2M^{-1}$, so both $s,t$ are positive.
Then $s^2=t^2+R$ and $s+t=R/r$. The rational symmetric matrix

\[
 L=tI+\frac{gg^{\mathsf T}}{s+t}
   =tI+\frac rRgg^{\mathsf T}
\]

satisfies

\[
 L^2=t^2I+
 \left(\frac{2t}{s+t}+\frac R{(s+t)^2}\right)gg^{\mathsf T}
 =t^2I+gg^{\mathsf T}.
\]

Indeed the coefficient in parentheses is
$2t/(s+t)+(s-t)/(s+t)=1$. Therefore

\[
 G^2+t^2\sum_{i=0}^{m-1}q_i^2
   =\|Lq\|^2
   =\sum_{i=0}^{m-1}(Lq)_i^2.                       \tag{1}
\]

The eigenvalues of $L$ are $t$ on $g^\perp$ and $s$ on the span
of $g$. It is invertible, so the common zero of the new square factors
is exactly the common zero of the original residuals. In particular,
no new zero or loss of uniqueness can occur.

## Rational parameter selection and denominator

The baseline weight approximation implies $1/5<g_i<5$, hence

\[
 \frac m{25}<R<25m.
\]

For $r>0$, the function $t(r)=(R-r^2)/(2r)$ is strictly decreasing.
At $r=1/8$ it is greater than $2/M$; at $r=8m$ it is negative.
On this interval,

\[
 |t'(r)|=\frac12\left(1+\frac R{r^2}\right)<801m.
\]

Bisect rationally to bracket the solution of $t(r)=3/(2M)$.
After the bracket width is at most $1/(4000mM)$, its midpoint
differs in $t$-value from $3/(2M)$ by less than $1/(2M)$.
Thus it gives the required strict inequalities
$M^{-1}<t<2M^{-1}$. Every comparison is rational, and the midpoint
$r=a/b$ is dyadic. Since $m,M$ have polynomial magnitude, the
bisection uses $O(\log(n+1))$ steps. Both $a$ and $b$ have
polynomial magnitude and $O(\log(n+1))$ bits.

The supplement also gives a general rational bisection procedure for
arbitrary positive rational $R$ and target scale $\tau$. Its derivative
bound for $r(t)=\sqrt{R+t^2}-t$, initial bracket, and stopping width
are valid. One wording correction was requested: the exact target root
is at least $4\Delta$ from the endpoint values $r(\tau),r(2\tau)$;
the chosen midpoint is within $\Delta/2$ of that root and therefore
remains strictly inside the interval. The midpoint itself need only
be at least $7\Delta/2$ from the endpoints. This correction does
not change the algorithm or any result. The author made this correction,
and this reviewer re-read the amended paragraph and confirmed the stated
$4\Delta$ and $7\Delta/2$ margins.

For a shared denominator, let $S=\sum_i z_i^2$, so $R=S/Q^2$.
Then

\[
 t=\frac{Sb^2-a^2Q^2}{2abQ^2},\qquad
 L=tI+\frac{a}{bS}zz^{\mathsf T}.                 \tag{2}
\]

The positive integer

\[
 D=2abQ^2S
\]

clears every entry of $L$. Each $2q_i$ has integer coefficients, so
$2D(Lq)_i$ is an integer quadratic. The numbers $z_i,Q,S,a,b,D$
all have polynomial magnitude. Therefore the integer quadratic
coefficients obtained this way have $O(\log(n+1))$ bits. Using a
product of all separately reduced entry denominators would obscure
this bound; the shared denominator (2) establishes it directly.

## Curvature and rational Hessian certificate

Set $\varepsilon=t^2$. Relative to the baseline proof, the rounded
quadratic $G$, its matrices $H,T_i$, and its linear part $\ell$ do
not change. We have

\[
 M^{-2}\leq\varepsilon\leq4M^{-2},\qquad
 \|\ell\|\leq\frac1{4M^2}\leq\varepsilon.
\]

The baseline constants
$\mu=1/(16n^2)$, $\nu=1/(8n)$, and $B=9+8m\leq17n$
remain valid. All its curvature and Gram conditions hold over this
entire interval, since

\[
 \frac4{M^2}\leq
 \min\left(1,\frac{\mu^2}{2m},
          \frac{\nu^2\mu^2}{36nB^2}\right).
\]

For the last inequality it suffices that
$4\cdot170459136\,n^9\leq10^{12}n^{10}$, which holds
for $n\geq2$. The other two bounds have larger margins.
Consequently the rational quartic on the left of (1) has

\[
 \nabla^2\!\left(G^2+t^2\sum_iq_i^2\right)
 \succeq\frac32\varepsilon\nu^2I
 \succeq\frac3{128M^2n^2}I.                       \tag{3}
\]

The same positive definite Hessian Gram construction and rational
coefficient projection apply with this new rational $\varepsilon$.
The previous inverse-polynomial Gram-gap bound remains conservative:
the relevant Schur lower bound is at least its value at
$\varepsilon=M^{-2}$, and its cross-to-quartic-block ratio remains
less than one when $\varepsilon$ increases by a factor of four.
Thus the rational certificate still has polynomial size and can be
constructed in polynomial time. Equation (1) changes the displayed
scalar SOS factors; it does not require those factors individually
to be convex.

For a concrete integer output take

\[
 \widehat F_n=\sum_{i=0}^{m-1}
       \bigl[32MnD(Lq)_i\bigr]^2.                \tag{4}
\]

Its factors are integer quadratics, and (3) gives
$\nabla^2\widehat F_n\succeq24D^2I\succeq I$.
Equivalently, after any positive integer denominator clearing,
multiplying all cleared factors by $16Mn$ already gives a lower
bound of at least $6I$. The exact size of this harmless integer
scaling does not affect the degree or bit conclusions.

Every new factor is a linear combination of the original $m$
two-term residuals. The common monomial support of all factors has
at most $2m$ elements. Although there are $m$ factors, the expanded
quartic therefore has only $O(m^2)$ possible monomials. Each
coefficient is a sum of polynomially many products of integers of
polynomial magnitude. This proves the same $O(\log(n+1))$ bit
bound and polynomial-time expansion. The coordinate translation
used for the baseline minimal-polynomial output obstruction also
preserves all these conclusions.

## Targeted checks

The retained [exact checker](check_cyclic_quartic_rank_one_compression.py)
was run with

```text
python research-20260927/check_cyclic_quartic_rank_one_compression.py
```

It passed the fourfold regularization range and scaling bounds for
$n=2,\ldots,80$. For $n=2,\ldots,6$, it used the certified baseline
weight construction, performed the new dyadic bisection, verified
$L^2=t^2I+gg^{\mathsf T}$ exactly, cleared the shared denominator,
expanded the actual integer output, and checked identity (1), degree,
and integrality. The output rows
$(n,d,\text{factors},\text{monomials},\text{maximum coefficient bits})$
were $(2,3,3,15,716)$, $(3,5,4,31,789)$,
$(4,11,5,50,839)$, $(5,21,6,72,882)$, and
$(6,43,7,98,914)$. The conservative denominator creates larger
constants than the baseline construction; the asymptotic bit bound
is unchanged. The finite checks supplement the universal algebra
and estimates above. No project-wide verification or CI inspection
was run.
