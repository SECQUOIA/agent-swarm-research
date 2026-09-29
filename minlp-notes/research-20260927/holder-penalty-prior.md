# Prior-art and encoding audit for fractional exact penalties

Date: 2026-09-27. This note records the source investigation for a candidate
polynomial-size fractional-penalty representation. It is not a proof or a
priority certificate for that candidate.

The qualitative conclusion is established prior art: a continuous
semialgebraic optimization problem on a compact semialgebraic domain admits
an exact fractional-power residual penalty. The potentially additional
statement concerns simultaneous bounds on the ordinary binary encoding of
the coefficient and exponent, with an explicit input convention. The
effective tools needed for that statement also predate this investigation.

## Closest sources inspected

### Effective exponent and coefficient bounds

Saugata Basu and Ali Mohammad-Nezhad, *Improved effective Łojasiewicz
inequality and applications*, Forum of Mathematics, Sigma **12** (2024),
e115, [DOI 10.1017/fms.2024.66](https://doi.org/10.1017/fms.2024.66),
[open publisher text](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improved-effective-lojasiewicz-inequality-and-applications/022BF859F5714FDA8050F6DC1992E48B),
[arXiv:2211.10034](https://arxiv.org/abs/2211.10034).

Theorem 2.2 treats compact semialgebraic `A ⊂ R^n` and continuous
semialgebraic `f,g` with `f^{-1}(0) ⊂ g^{-1}(0)`. If the quantifier-free
descriptions have degree at most `d ≥ 2`, it supplies

\[
 |g(x)|^q\le c|f(x)|,\qquad q=(8d)^{2(n+7)}.
\]

For integer coefficients of bit size at most `τ`, the same theorem gives

\[
 c\le\min\{2^{\tau d^{O(n^2)}},2^{\tau d^{O(n\log d)}}\}.
\]

Theorem 2.11 supplies a degree-sensitive distance error bound for polynomial
systems. Section 3.1 identifies Solernó's earlier coefficient bound.
**Comparison:** the candidate must be presented as an application of
effective real algebraic geometry. It does not provide a new effective
Łojasiewicz inequality. The explicit coefficient bound is particularly
useful because an exponent bound alone does not bound penalty encoding.

Pablo Solernó, *Effective Łojasiewicz inequalities in semi-algebraic
geometry*, Applicable Algebra in Engineering, Communication and Computing
**2** (1991), 1–14. Theorem 3(ii), as compared explicitly by the source
above, bounds the coefficient by `2^{τ D^{c n²}}`, where `D` bounds the sum
of input polynomial degrees and `c` is universal. The original full text
was not obtained in this investigation. Any direct dependence on its exact
hypotheses still needs inspection of that original statement.

### Exact fractional penalties on compact domains

Liguo Jiao, Tiến-Sơn Phạm, and Nguyen Van Tuyen, *Exact penalty functions
in optimization with unbounded constraint sets*,
[arXiv:2507.03424v2](https://arxiv.org/html/2507.03424v2).
Theorem 5.2 and Remark 5.3(ii) were read in the open full text.
For compact semialgebraic `X` and compact nonempty semialgebraic `S ⊂ X`, continuous semialgebraic
objective `f₀` and continuous semialgebraic residual `ψ`, that remark gives
some `c_* > 0` and `α ∈ (0,1]` such that, for every `c > c_*`,

\[
 \min_S f_0=\min_X(f_0+c\psi^\alpha),\qquad
 \operatorname{argmin}_S f_0
 =\operatorname{argmin}_X(f_0+c\psi^\alpha).
\]

The authors identify this compact-domain statement as already covered in
the subanalytic setting by Warga and Dedieu. The inspected result does not
state bounds on ordinary binary encodings of `c_*` and `α`.
**Comparison:** absence of a constraint qualification, fractional powers,
global exactness, and equality of minimizer sets are not new ingredients.

The older references identified there are:

- Jack Warga, *A necessary and sufficient condition for a constrained
  minimum*, SIAM Journal on Optimization **2**(4) (1992), 665–667,
  [DOI 10.1137/0802033](https://doi.org/10.1137/0802033), Theorem 1.
- Jean-Pierre Dedieu, *Penalty functions in subanalytic optimization*,
  Optimization **26** (1992), 27–32,
  [DOI 10.1080/02331939208843840](https://doi.org/10.1080/02331939208843840),
  Theorem 3.1.
- Zhi-Quan Luo, Jong-Shi Pang, and Daniel Ralph, *Mathematical Programs
  with Equilibrium Constraints*, Cambridge University Press (1996),
  Theorem 2.1.2.

These older full statements were not recovered here. The comparison is
therefore based on the explicit attribution and mathematical restatement
in Jiao–Phạm–Tuyen, not on an independent audit of the originals.

### Convex quadratic error bounds

Tao Wang and Jong-Shi Pang, *Global error bounds for convex quadratic
inequality systems*, Optimization **31**(1) (1994), 1–12,
[primary publisher abstract](https://www.tandfonline.com/doi/abs/10.1080/02331939408844003).
The abstract states a global error bound of the form

\[
 \operatorname{dist}(x,S)
 \le C\bigl(v(x)+v(x)^{2^{-d}}\bigr),
\]

without a constraint qualification. Here `d` is a degree of singularity,
bounded by the number of constraints. It also states sharpness examples.
This already makes qualitative fractional-penalty existence for convex
quadratic systems routine. The full proof was not recovered, so a sharp
joint-Hessian-rank specialization was not attributed to that paper.

Two different Luo–Sturm chapters must not be conflated:

- *Error bounds for quadratic systems*, in *High Performance Optimization*
  (2000), 383–404,
  [institutional publication record](https://research.tilburguniversity.edu/en/publications/error-bounds-for-quadratic-systems).
- *Error bounds for mixed semi-definite and second-order cone programming*,
  in *Handbook on Semidefinite Programming* (2000), 163–190,
  [institutional publication record](https://research.tilburguniversity.edu/en/publications/error-bounds-for-mixed-semi-definite-and-second-order-cone-progra).

Only bibliographic records were inspected for these chapters. They do not
support a claim about their precise rank bounds.

## Candidate encoding mechanism and its actual additional content

The following elementary inequality is independent of the source search.
For `M,C,r > 0`, `β > 0`, and `0 < α ≤ β`,

\[
 \min\{M,Cr^\beta\}
 \le M^{1-\alpha/\beta}C^{\alpha/\beta}r^\alpha.
 \tag{1}
\]

Indeed, `min(a,b) ≤ a^{1-θ}b^θ` for `θ ∈ [0,1]`; substitute
`a=M`, `b=Cr^β`, and `θ=α/β`. If an objective deficit is bounded both by
`M` and by `Cr^β`, decreasing the exponent can therefore absorb a very
large `C` into a bounded factor. For instance, `C ≥ 1` and
`α/β ≤ 1/max{1,log₂ C}` give `C^{α/β} ≤ 2`.

This inequality is not a substantial standalone advance. Its potential
use here is that effective semialgebraic estimates can have
`log C ≤ 2^{poly(N)}` and `β ≥ 2^{-poly(N)}`. A dyadic
`α=2^{-p(N)}` then has polynomial binary length, while a sufficient penalty
coefficient has polynomial binary length if `M` does. The two properties
must be proved together for the actual input representation.

The repository already distinguishes ordinary binary coefficients from
short expressions in
[the previous penalty priority audit](../research-20260925/publication-penalty-priority-audit.md).
It explicitly excludes instance-dependent fractional penalties from the
scope of the ordinary norm-penalty lower bound. The proposed result would
study that excluded representation, rather than contradict that lower
bound or the polynomial-encoding result for MIQP of Gu–Ahmed–Dey.

## Encoding counterexample: unrestricted sparse polynomial objectives

The phrase “every bounded rational polynomial MINLP” is too broad if
degrees are supplied in binary and no objective-range assumption is made.
Consider

\[
 \min x^{2^k}\quad\text{subject to}\quad 1\le x\le2,\quad x\ge2.
\]

Its sparse encoding has size `O(k)`. Penalize the sole additional
constraint by `ρ [2−x]_+^α`, keeping `[1,2]` as the native domain.
At `x=1`, the penalized objective equals `1+ρ` for every `α>0`; at the
unique feasible point `x=2`, it equals `2^{2^k}`. Value exactness therefore
requires

\[
 \rho\ge2^{2^k}-1.
\]

Thus decreasing the exponent cannot always replace a huge coefficient.
A valid general theorem needs bounded degree, dense/unary degree encoding,
or a supplied objective-range bound of polynomial binary length. Bounded
rational quadratic MINLP satisfies the needed range control under ordinary
explicit encoding. A general arithmetic circuit can also create enormous
objective values by repeated squaring, so merely replacing sparse input
by circuit input does not repair this obstruction.

## Proof obligations for the candidate

1. A compact native domain must include all bounded integer assignments,
   including assignments with an infeasible continuous slice. A distance
   error bound only inside feasible slices does not address the others.
2. The unknown optimum may be irrational. Applying the integer-coefficient
   version of the effective theorem directly to `[f*−f(x)]_+` would require
   a separate algebraic encoding argument. One clean route introduces a
   scalar `t` and restricts the compact domain by “`t ≤ f(y)` for every
   feasible `y`”, then eliminates that quantified block.
3. Bounded integers can be represented using polynomially many binary
   variables, equations `b(1−b)=0`, and an affine binary expansion. This
   avoids enumerating integer slices. Every degree, coefficient-size, and
   variable-count increase must still be tracked through elimination.
4. A depth-`p` square-root expression has a length-`p` quadratic lift, but
   the corresponding equalities are nonconvex. This is a representation
   statement, not an efficient solution algorithm or preservation of
   convexity.
5. Tiny exponents can cause severe evaluation and conditioning problems.
   Polynomial description length does not establish a useful numerical
   penalty or a computational speedup.

## Search and review record

The initial search covered Wang–Pang, Luo–Sturm, convex quadratic
singularity degree, Hessian rank, and facial reduction. After the scope
changed, searches covered exact semialgebraic/subanalytic penalties,
effective Łojasiewicz coefficients, polynomial encoding, bit complexity,
fractional powers, and exponent–coefficient tradeoffs. Primary open full
texts were inspected for Basu–Mohammad-Nezhad and Jiao–Phạm–Tuyen. Relevant
local penalty source and priority audits were also read.

An independent source-search subagent confirmed the older compact-domain
penalty references, checked (1), and flagged both infeasible integer slices
and the irrational-optimum encoding issue. No equivalent explicit
polynomial-size coefficient/exponent theorem was identified in this search.
That does not establish novelty. The next priority audit should inspect
the older originals and search citations of both the effective
Łojasiewicz and compact exact-penalty papers.

Only targeted file reads and literature queries were performed for this
note. No numerical experiment or Lean proof was needed for its elementary
counterexample and interpolation calculation. No project-wide checks or
CI status/log inspection were performed.
