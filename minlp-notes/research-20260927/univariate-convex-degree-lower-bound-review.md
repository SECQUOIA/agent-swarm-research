# Independent review of the univariate convex degree obstruction

Date: 2026-09-28. Status: the [assembled main note](univariate-convex-degree-lower-bound.md)
and its proof have been checked independently; no mathematical gap was
found. This includes the two corollaries, the application of the reviewed
quartic realization theorem, and the quartic quasiconvex comparison.
Novelty and a fresh proof audit of the general realization theorem are
outside this review's conclusion.

## Proposition checked

For

\[
 p_n(x)=(x+2)(x-1)^2+2^{-2n},\qquad n\geq1,
\]

let $\alpha$ be its unique real root. If a rational globally convex
polynomial $g$ has $\alpha$ as its unique real zero, then its degree $D$
satisfies

\[
 D^2>\frac34\,2^n.
\]

The argument originally communicated assumed $3\nmid n$. That assumption
is sufficient for its valuation proof, but is unnecessary: the alternative
irreducibility argument below works for every positive integer $n$.
The coefficient encoding length of $p_n$ is $\Theta(n)$, so this is an
exponential degree obstruction in that length. There is no restriction on
the coefficient heights of $g$.

## Arithmetic and root geometry

Put $\epsilon=2^{-2n}$. The derivative of $p_n$ is $3(x^2-1)$;
its two critical values are $4+\epsilon$ and $\epsilon$, both positive.
It therefore has exactly one real root, of the form

\[
 \alpha=-2-t,\qquad t>0,\qquad t(3+t)^2=\epsilon.
\]

In particular, $0<t<\epsilon/9$.

To check irreducibility without a congruence restriction on $n$, suppose
that its real root is rational. Write $t=a/b$ in lowest terms with positive
integers $a,b$. Then

\[
 \epsilon=\frac{a(a+3b)^2}{b^3}.
\]

This fraction is reduced: both $a$ and $a+3b$ are relatively prime to $b$.
Its numerator would have to equal $1$, since $\epsilon$ has reduced
numerator $1$. But $a\geq1$ and $a+3b\geq4$. This is impossible. A cubic
without a rational root is irreducible over $\mathbb Q$.

The proposed $2$-adic proof is also valid when $3\nmid n$. If $r$ is a
rational root, $v_2(2+\epsilon)=-2n$. Nonnegative $v_2(r)$ cannot cancel
that constant term. For negative $v_2(r)$, the valuations of the other
terms are $3v_2(r)$ and $v_2(r)$, so cancellation requires
$3v_2(r)=-2n$, which is impossible under the stated restriction.

The nonreal roots are $\beta\pm i\eta$, with $\eta>0$. Vieta's
identities give

\[
 \beta=1+\frac t2,\qquad
 \eta^2=3t+\frac34t^2,\qquad
 \ell:=\beta-\alpha=3+\frac32t>3.
\]

The strict imaginary-part bound follows from the exact identity

\[
 \epsilon-\eta^2
 =t\left(6+\frac{21}{4}t+t^2\right)>0.
\]

Thus $0<\eta<2^{-n}$. This calculation does not rely on an asymptotic
root approximation.

## Convexity, normalization, and the analytic inequality

The affine case is excluded because the rational irreducible cubic
$p_n$ divides $g$. A nonaffine globally convex polynomial has positive
leading coefficient and even degree, and tends to $+\infty$ at both
ends. Its unique real zero must be a global minimum with value zero:
a negative value would force distinct zeros on its two sides by
continuity. Therefore $g\geq0$ and $g(\beta)>0$.

Set $h=g/g(\beta)$. The positive scaling preserves convexity. For
$x\in[\alpha,\beta]$, convexity bounds $h(x)$ by the chord joining its
endpoint values $0$ and $1$. Consequently

\[
 0\leq h(x)\leq1,\qquad
 \|h\|_{[\alpha,\beta]}=1.
\]

The rationality of $g$, rather than of $h$, implies $p_n\mid g$;
therefore $h(\beta+i\eta)=0$. Markov's classical derivative inequality,
after affine rescaling from $[-1,1]$ and iteration, gives

\[
 \|h^{(j)}\|_{[\alpha,\beta]}
 \leq
 \left(\frac2\ell\right)^j
 \left(\frac{D!}{(D-j)!}\right)^2
 \leq\left(\frac{2D^2}{\ell}\right)^j
 \quad(1\leq j\leq D).
\]

This applies to real coefficients and hence to the normalized $h$, whose
coefficients need not be rational. Taylor's identity is exact for the
polynomial, including at the complex argument. With
$q=2D^2\eta/\ell$, it yields

\[
 1=|h(\beta)-h(\beta+i\eta)|
 \leq\sum_{j=1}^D\frac{q^j}{j!}
 \leq e^q-1.
\]

Thus $q\geq\log2>1/2$, which in particular implies the weaker stated
bound

\[
 D^2\geq\frac\ell{4\eta}>\frac34\,2^n.
\]

No polynomial coefficient bound is used in this analytic step.

## Two extensions checked separately

The Markov and Taylor argument only needs a real polynomial $h$ with
$h(\beta)=1$, $h(\beta+i\eta)=0$, and
$\|h\|_{[\alpha,\beta]}\leq1$. The following consequences therefore
hold beyond the original unique-zero statement.

**Finite systems without auxiliary variables.** Suppose finitely many
rational globally convex univariate polynomial inequalities
$g_i(x)\leq0$ have feasible set exactly $\{\alpha\}$. Discard identically
zero rows. Some active row satisfies $g_i'(\alpha)\geq0$. Otherwise every
active row has strictly negative derivative; together with continuity of
the inactive rows and finiteness of the family, this would make a small
right neighborhood of $\alpha$ feasible.

For this row, the supporting-line inequality gives $g_i(x)\geq0$ for
$x\geq\alpha$. Also $g_i(\beta)>0$: if it were zero, convexity and that
lower bound would make the polynomial vanish throughout
$[\alpha,\beta]$, contradicting its being nonzero. Chord convexity now
gives the same normalization on this interval. Since $p_n\mid g_i$,
the row degree $D_i$ satisfies $D_i^2>3\cdot2^n/4$. Thus increasing the
number of convex rows cannot remove the degree obstruction when no
auxiliary variables are allowed.

**Unconstrained convex objectives.** Let a nonconstant rational globally
convex polynomial $f$ attain its minimum at $\alpha$. Its derivative
$q=f'$ is a nonzero rational polynomial, is nondecreasing on $\mathbb R$,
and satisfies $q(\alpha)=0$. Hence $p_n\mid q$ and $q(\beta)>0$; otherwise
monotonicity would make $q$ identically zero on an interval. Monotonicity
gives $0\leq q(x)/q(\beta)\leq1$ on $[\alpha,\beta]$. Applying the same
argument to this normalized derivative gives

\[
 (\deg f-1)^2>\frac34\,2^n.
\]

This conclusion does not assume that the minimum value of $f$ is rational
or zero. Neither extension rules out representations with auxiliary
variables or algebraic coefficients.

## Lifting and the quasiconvex comparison

The [quartic realization theorem](general-strongly-convex-quartic-singleton.md)
requires an irreducible rational polynomial of degree $d>1$ with exactly
one real root. The family $p_n$ satisfies these assumptions with $d=3$.
Its conclusion therefore supplies a polynomial-size rational strongly
convex quartic $H_n$ in $d-1=2$ variables with unique zero
$(\alpha_n,\alpha_n^2)$. Its rational sum-of-squares expression gives
$H_n\geq0$, so $H_n\leq0$ has precisely that singleton as its feasible
set. Projecting to the first coordinate gives exactly $\{\alpha_n\}$.
The assembled manuscript imports the theorem and its separate review
accurately. This review checks that application rather than claiming a
new independent audit of the quartic construction.

For the additional comparison, put

\[
 J_n(x)=x^4/4-3x^2/2+(2+2^{-2n})x.
\]

Its derivative is exactly $p_n$. Since this cubic has just one real root
$\alpha_n$ and positive leading coefficient, it is strictly negative
to the left of $\alpha_n$ and strictly positive to its right. Hence
$J_n$ is strictly decreasing and then strictly increasing, with unique
minimizer $\alpha_n$. Every sublevel is an interval or the empty set,
so $J_n$ is globally quasiconvex. The identity $J_n''(0)=-3$ excludes
global convexity. Its fixed degree and rational coefficient bit length
$O(n)$ establish the claimed exact representation comparison with the
convex-objective degree lower bound. No statement about practical solver
performance follows from this comparison.

## Primary source and targeted checks

The open primary research article by Rafał Pierzchała,
[*Markov's inequality and polynomial mappings*](https://link.springer.com/article/10.1007/s00208-015-1294-9),
Mathematische Annalen 366 (2016), 57–82, states the needed classical
inequality in Theorem 1.1. Its statement was read directly. The affine
rescaling, iteration, and application to a complex Taylor argument above
were checked independently. A Cambridge-hosted alternative proof PDF
could not be fetched and was not used as evidence.

Two targeted inline `python - <<'PY'` commands using SymPy checked:

- the exact factorization
  $p_n(x)=(x-\alpha)((x-\beta)^2+\eta^2)$ after substituting
  $\epsilon=t(3+t)^2$;
- the exact separation and positive-difference identities above;
- rational irreducibility at every integer $1\leq n\leq21$.

All checks passed. A further targeted inline SymPy command verified
$J_n'=p_n$ and $J_n''(0)=-3$ exactly. A targeted document command checked
display delimiters, whitespace, control characters, and final newline
for this review. The symbolic identities corroborate the algebra;
the finite irreducibility checks do not prove the general theorem. The
general proof is the reduced-fraction argument above. No project-wide
verification or CI inspection was performed. A requested additional
subreview could not be started because the agent thread limit had been
reached; this review does not represent an additional nested review.
