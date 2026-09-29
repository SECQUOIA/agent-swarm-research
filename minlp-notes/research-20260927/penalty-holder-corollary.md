# Polynomial-size fractional penalties from effective error bounds

Date: 2026-09-27.

Status: supporting corollary of classical effective semialgebraic geometry,
not the main contribution of the current research. The elementary
coefficient–exponent tradeoff below is useful for delimiting what penalty-size
lower bounds do and do not rule out. No novelty claim is made for that tradeoff
or for the resulting exact-penalty corollary.

## Motivation and scope

A linear residual penalty can require a coefficient with exponentially many
bits, or can fail to be exact without a constraint qualification. Replacing the
residual by a sufficiently small positive fractional power changes that
conclusion. On a domain with a suitably bounded diameter and objective
Lipschitz constant, a fractional penalty has a coefficient and an exponent
denominator with polynomial encoding length. This is an existence and
representation result. It does not establish that minimizing the penalized
objective is easier.

The hypotheses controlling the objective and domain matter. Compactness alone
does not suffice, and a rational box with a short description does not control
the size of a polynomial objective given by sparse binary exponents.

## Definitions and encoding

Let \(n\ge 1\), and let \(K\subseteq[-R,R]^n\) be a nonempty compact set,
where \(R>0\) is rational. Assume that a quantifier-free Boolean formula over
rational polynomial sign conditions describes \(K\). Let

\[
r(x)=\max\bigl(\{0\}\cup\{g_i(x):1\le i\le m\}
                    \cup\{|h_j(x)|:1\le j\le s\}\bigr),
\qquad
F=\{x\in K:r(x)=0\},
\]

where the \(g_i,h_j\) are rational polynomials. Assume \(F\ne\varnothing\).
The use of \(\{0\}\) also defines \(r\) when there are no additional
constraints. Let \(f\) be a rational polynomial objective.

Use ordinary sparse polynomial encoding: list each nonzero rational
coefficient and its vector of nonnegative integer exponents, with integers in
binary. The input length \(N\) includes the formula for \(K\), all polynomial
data, the explicitly counted number of variables, and the bound \(R\). When
a Lipschitz bound \(L\) is supplied, include its encoding in \(N\). Thus
\(n\le N\); an enormous number of unused variables is not encoded only by
its binary dimension. Polynomial degree can be exponential in \(N\).

An exact penalty here preserves **all global minimizers**:

\[
\operatorname*{argmin}_{x\in K}
     \bigl(f(x)+\lambda r(x)^{1/Q}\bigr)
 =\operatorname*{argmin}_{x\in F}f(x).
\]

The term is defined as zero when \(r(x)=0\). All sets of minimizers exist
because their domains are nonempty and compact and their objectives are
continuous.

## The coefficient–exponent tradeoff

**Lemma.** Suppose that \(d,r\ge0\), \(d\le M\), and \(M\ge1\). Suppose
also that

\[
d(x)^A\le c\,r(x),
\qquad A\in\mathbb Z_{\ge1},\quad c>0.
\]

For every integer
\(Q\ge\max\{A,\log_2\max(1,c)\}\),

\[
d(x)\le 2M\,r(x)^{1/Q}.
\tag{1}
\]

**Proof.** At points with \(d(x)=0\), (1) is immediate. Otherwise,

\[
d(x)^Q=d(x)^A d(x)^{Q-A}
 \le c M^{Q-A}r(x).
\]

Taking \(Q\)-th roots gives a coefficient
\(c^{1/Q}M^{1-A/Q}\le2M\), proving (1). The argument also covers
\(r(x)=0\), since the assumed inequality then implies \(d(x)=0\).
\(\square\)

This lemma absorbs the logarithm of an error-bound coefficient into the
denominator of the residual exponent. A coefficient with exponentially many
bits is compatible with a new denominator having only polynomially many bits.

## A precise supporting corollary

**Proposition.** Under the definitions above, suppose an integer \(L\ge0\)
satisfies

\[
|f(x)-f(y)|\le L\|x-y\|_2
\qquad(x,y\in[-R,R]^n).
\]

There is a universal polynomial \(p\), which can be taken integer-valued and
nonnegative on positive integers, with the following property. Set

\[
Q=2^{p(N)},\qquad
M=\left\lceil\max\{1,2nR\}\right\rceil,\qquad
\lambda=2ML+1.
\tag{2}
\]

Then the penalty in (2) is exact. Both \(Q\) and \(\lambda\) have
polynomial encoding length. No convexity or constraint qualification is
required.

**Proof.** Write \(d(x)=\operatorname{dist}(x,F)\). The set \(F\) is
nonempty and compact. A formula for the graph of \(d\) on \(K\), with free
variables \((x,t)\), is

\[
\begin{aligned}
x\in K\ \wedge\ t\ge0\ \wedge\ \exists y\ \forall z:\quad
&y\in F\ \wedge\ \|x-y\|_2^2=t^2\\
&\wedge\bigl(z\in F\Longrightarrow
                        \|x-z\|_2^2\ge t^2\bigr).
\end{aligned}
\tag{3}
\]

Compactness supplies a nearest point, so (3) describes the distance exactly.
The formula has two quantified blocks of \(n\) variables and \(n+1\) free
variables. Clear rational denominators using positive integer multipliers.
This increases coefficient bitlength by a polynomial in \(N\).

Let \(d_0\ge2\) bound the degrees and let \(\tau\) bound the resulting
integer coefficient bitlength. Effective quantifier elimination gives a
quantifier-free graph description whose degrees and coefficient bitlengths
are bounded, respectively, by

\[
\Delta=d_0^{O(n^2)},\qquad
T=\tau d_0^{O(n^3)}.
\tag{4}
\]

The residual graph has a direct quantifier-free description: its value
dominates \(0,g_i,h_j,-h_j\) and equals one of those finitely many
quantities. Thus it has the required bounded degrees and coefficient sizes
without quantifier elimination. Increase \(\Delta,T\) if necessary to cover
that graph and the description of \(K\).

Both \(r\) and \(d\) are continuous semialgebraic functions on \(K\), and
\(r^{-1}(0)=d^{-1}(0)\). The effective Łojasiewicz inequality therefore
gives

\[
d(x)^A\le c\,r(x),\qquad
A\le 2^{\operatorname{poly}(N)},\qquad
\log_2\max(1,c)\le 2^{\operatorname{poly}(N)}.
\tag{5}
\]

To see the last size assertions, the sparse encoding implies
\(\log d_0=O(N)\) and \(\tau=\operatorname{poly}(N)\). Consequently (4)
makes \(\log\Delta\) and \(\log T\) polynomial in \(N\). The effective
Łojasiewicz exponent is \(\Delta^{O(n)}\), and its coefficient has logarithm
at most \(T\Delta^{O(n^2)}\). These are each singly exponential in a
polynomial in \(N\).

Choose a universal \(p\) large enough that \(Q\) dominates both bounds in
(5). Since \(d(x)\le2\sqrt n R\le M\), the lemma gives
\(d(x)\le2M r(x)^{1/Q}\). For a nearest \(y\in F\), let
\(f_* =\min_F f\). Then

\[
f(x)\ge f(y)-L d(x)
      \ge f_*-2ML r(x)^{1/Q}.
\]

For each infeasible \(x\), equation (2) consequently gives

\[
f(x)+\lambda r(x)^{1/Q}
 \ge f_*+r(x)^{1/Q}>f_*.
\]

On \(F\), the penalty is zero. This proves the asserted equality of global
minimizer sets. The bitlengths of \(M,L,\lambda\) are polynomial in the
input length, as is \(\log_2 Q=p(N)\). \(\square\)

The polynomial \(p\) is universal but has not been expanded into numerical
constants here. The proposition is therefore a size theorem, not a supplied
numerical rule for setting solver parameters.

### Two concrete input classes

1. **Quadratic objective on a rational box.** Write
   \(f(x)=\sum_\alpha c_\alpha x^\alpha\) with
   \(|\alpha|_1\le2\), and put \(\overline R=\max(1,R)\). One may use
   \[
   L=\left\lceil\overline R
           \sum_\alpha |c_\alpha|\,|\alpha|_1\right\rceil.
   \]
   This integer has polynomial bitlength. Thus the proposition covers
   rational quadratic systems, including convex quadratic systems, on a
   rational box of polynomial encoding length. It also allows higher-degree
   constraint polynomials; quadraticity is only needed here to bound the
   objective's Lipschitz constant from its short input.

2. **Sparse polynomial objective on the unit cube.** If \(R=1\), arbitrary
   binary-encoded degrees are allowed, with
   \[
   L=\left\lceil
          \sum_\alpha |c_\alpha|\,|\alpha|_1\right\rceil.
   \]
   This bound again has polynomial bitlength. Indeed, on \([-1,1]^n\),
   the gradient's Euclidean norm is bounded by its one-norm, which is at
   most the displayed sum. Integrating along a segment in the cube gives
   the required Lipschitz inequality.

For a fixed or polynomially bounded degree on a general rational box, the
same reasoning gives a polynomial-bit Lipschitz bound. With unrestricted
sparse binary degrees, this conclusion can fail outside the unit cube.

## Exact lower examples and essential limitations

### A sharp coefficient–exponent tradeoff on the unit cube

For an integer \(m\ge0\), use variables \(u_0,\ldots,u_m,x\) and the
compact domain

\[
K_m=\{(u,x)\in[0,1]^{m+2}:
 u_0=1/2,\ u_{i+1}=u_i^2\ (0\le i<m)\}.
\]

Penalize the equation \(u_mx=0\), and minimize \(f(u,x)=-x\).
All data have degree at most two and small rational coefficients. On this
domain,

\[
u_m=\varepsilon_m=2^{-2^m},\qquad
r(u,x)=\varepsilon_m x,\qquad
F_m=\{(u,x)\in K_m:x=0\}.
\]

For every integer \(Q\ge1\), exactness holds **if and only if**

\[
\lambda>\varepsilon_m^{-1/Q}=2^{2^m/Q}.
\tag{6}
\]

For necessity, the infeasible endpoint \(x=1\) has penalized value
\(-1+\lambda\varepsilon_m^{1/Q}\). A value below zero beats the feasible
optimum, and a value equal to zero prevents equality of minimizer sets.
For sufficiency, \(x^{1/Q}\ge x\) on \([0,1]\), so the penalized value is
strictly positive at every \(x>0\) when (6) holds. At equality, both endpoints
minimize; if \(Q=1\), every point minimizes.

Thus \(\log_2\lambda>2^m/Q\) is necessary. Keeping coefficient bitlength
polynomial requires a denominator exponential in the chain length \(m\).
Because the declared encoding lists exponent vectors, its input length is
polynomial in \(m\); the conclusion is a superpolynomial denominator in
input length, not a claim of a \(2^{\Omega(N)}\) lower bound.
The example supports the scale of the tradeoff, but does not prove the
universal upper denominator optimal. Its squaring equalities make the
description nonconvex; it is not a convex quadratic lower example.

### A short rational box does not bound a sparse objective

Let

\[
K=[0,2],\quad F=[0,1],\quad r(x)=(x-1)_+,\quad
f_k(x)=-x^{2^k}.
\]

The objective has a sparse binary encoding of length \(O(k)\). Its feasible
optimum is \(-1\), whereas \(r(2)=1\). For every positive residual
exponent, exactness therefore requires

\[
\lambda>2^{2^k}-1.
\]

Reducing the exponent cannot help at a point with residual one. This refutes
the version of the proposition that omits the polynomial-bit Lipschitz or
objective-scale assumption while retaining arbitrary sparse degrees on a
general rational box.

### Compactness alone does not bound the required coefficient

Use the compact domain

\[
K_m=\{(v,t):v_0=2,\ v_{i+1}=v_i^2\ (0\le i<m),\ 0\le t\le1\}.
\]

Penalize \(t=0\) with residual \(r=t\), and minimize the quadratic
objective \(f(v,t)=-v_m t\). Here \(v_m=2^{2^m}\). At \(t=1\), every
positive fractional power of the residual equals one. Exactness therefore
requires \(\lambda>2^{2^m}\). The description is compact, quadratic, and
short, but a containing rational box cannot have polynomial bitlength.

## Literature inspected and what is added

The following are primary sources; statements were inspected on 2026-09-27.

- S. Basu and A. Mohammad-Nezhad, *Improved effective Łojasiewicz inequality
  and applications*, Forum of Mathematics, Sigma 12 (2024), e115,
  [article and DOI](https://doi.org/10.1017/fms.2024.66),
  [open PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/022BF859F5714FDA8050F6DC1992E48B/S2050509424000665a.pdf/improved_effective_lojasiewicz_inequality_and_applications.pdf).
  Theorem 2.2, page 3, applies to continuous semialgebraic functions on a
  closed bounded semialgebraic set. With defining degree \(d\), it gives
  exponent \((8d)^{2(n+7)}\); for integer coefficient bits \(\tau\), the
  coefficient can satisfy
  \(\log_2 c\le\min\{\tau d^{O(n^2)},\tau d^{O(n\log d)}\}\).
  Theorem 2.11, page 5, already supplies error exponents for nonempty
  polynomial feasible sets on bounded test sets without a constraint
  qualification. Theorem 4.1, page 12, states the effective quantifier
  elimination bounds used above. Consequently, neither existence of
  fractional error bounds nor their singly exponential exponent bounds is
  an addition of this note.

- S. Basu, *Algorithms in Real Algebraic Geometry: A Survey*,
  [open author PDF](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf),
  Theorem 2.16, page 12. An independent reviewer inspected the fixed-block
  quantifier-elimination degree and integer coefficient-size bounds in
  this source and applied them to (3). With quantified block sizes
  \(n,n\) and \(n+1\) free variables, they give (4).

- P. Solernó, *Effective Łojasiewicz Inequalities in Semialgebraic Geometry*,
  Applicable Algebra in Engineering, Communication and Computing 2
  (1991), 1–14,
  [open author PDF](https://mate.dm.uba.ar/~psolerno/Solerno,%20Effective%20Lojasiewicz%20Inequalities%20in%20semialgebraic.pdf).
  The abstract and opening statement were inspected. They already give a
  singly exponential exponent and an effective integer-data coefficient
  bound, with dependence on the number and degrees of defining
  polynomials. The complete proof was not audited here; the proposition
  above uses the newer source directly.

The contribution of this supporting note is the explicit encoding conclusion
obtained by increasing the residual-power denominator until the coefficient
becomes small, together with the stated boundary examples. These are natural
consequences of known theory. The literature search was sufficient to locate
strong prior results and prevent a claim that this is a new general error
bound theorem. It was not an exhaustive search for every equivalent
coefficient–exponent formulation or exact-penalty corollary. An unsuccessful
search would not establish novelty.

## Review and verification record

The derivation was independently checked by the research subagent
`constant_tradeoff`, separate from the authoring subagent
`holder_frontier`. The reviewer independently obtained the coefficient
absorption inequality, checked the two-block formula and the size bounds in
(4), and supplied the sparse-objective counterexample and the sharp tradeoff
family. The author independently checked the nearest-point argument, the
strict inequality needed to preserve all minimizers, and the distinction
between the unit cube and a general rational box. A final independent review
of the precise rational-box/Lipschitz hypotheses found no substantive gap;
it also checked constant objectives, empty constraint lists, \(F=K\),
\(R<1\), and compact sets described using strict atoms. The reviewer then
read the complete file and checked all three lower examples. Its only
requested clarification was to distinguish exponential dependence on chain
length from exponential dependence on encoded input length; that distinction
is now explicit above. Positive review is evidence, not a guarantee of
correctness.

The checks are mathematical arguments and source comparisons. There is no
Lean formalization, no claim of machine verification of the effective
geometry theorems, and no computational evidence of improved solver
performance. The lower examples use exact symbolic identities; floating
point calculations are not needed.

Targeted local check actually run:

```sh
git diff --check --no-index /dev/null research-20260927/penalty-holder-corollary.md
```

Result: no whitespace diagnostics. The command returned exit status 1 because
the new file differs from `/dev/null`; it was not a mathematical check. No
project-wide verification or CI inspection was performed for this note.

## What remains before practical use

- Make the universal bound numerical if a parameter-selection rule is
  desired; the hidden constants in effective geometry are not expanded
  here.
- Study whether less conservative exponents are available for relevant
  structured problem classes. The general denominator can be enormous
  even though its binary encoding is short.
- Analyze algorithms for the penalized objective. Its fractional term is
  generally nonconvex and is non-Lipschitz at residual zero. Exactness of
  global minima provides no local-minimum, stationarity, numerical
  conditioning, or complexity guarantee.
- Treat integer variables and their encoding explicitly in any claimed
  MINLP reformulation. This note establishes a continuous semialgebraic
  statement; bounded integrality can be represented semialgebraically,
  but a short integer bound alone does not make every such representation
  short.

The established capability is a concise exact-penalty representation under
explicit size assumptions. Solver acceleration and useful robust treatment
of degeneracy remain possible applications, not proved consequences.
