# Exact optimization with one unbounded integer variable

Date: 2026-09-28. Status: proof and
[independent adversarial review](one-integer-value-review.md) completed;
a separate review of the elimination and factor-height bounds also found
no gap. The prior-work audit is complete, with the limitations in Section 6.
The proof uses the reviewed compressed projection formula in
[unbounded MISOCP feasibility](unbounded-misocp-frontier.md), but its
one-integer argument does not require convexity. Novelty is not established.

## 1. Statement and significance

Let

\[
 S=\{(z,x)\in\mathbb R\times\mathbb R^n:
       L(z,x)\le0,\ E(z,x)=0,\ q_i(z,x)\le0\ (i\le m)\},
\]

where all data are rational and every \(q_i\) is quadratic. Let \(q_0\)
be a rational quadratic objective, and put

\[
 h=\dim_{\mathbb Q}\operatorname{span}
       \{\nabla^2_{xx}q_i:i\le m\}.
\]

The objective Hessian is excluded from this definition. The input length is
\(N\ge2\); no variable bounds, convexity, or attainment are assumed.

**Theorem 1 (one-integer precision).** There is an effective absolute
constant \(C\) with the following properties.

1. If \(S\cap(\mathbb Z\times\mathbb R^n)\) is nonempty, it contains
   a point with \(\log_2(2+|z|)\le N^{C(h+1)}\).
2. If the mixed-integer infimum \(\theta\) is finite, it is a real
   algebraic number annihilated by a nonzero integer polynomial of degree
   and coefficient bit length at most \(N^{C(h+1)}\).
3. If the mixed-integer infimum is attained, some optimal integer assignment
   satisfies the same bound as in item 1.

For fixed \(h\), exact feasibility is in NP. Exact classification as
infeasible, unbounded below, or finite, and recovery of the finite value,
are in \(\mathrm{FP}^{\mathrm{NP}}\). Combining item 3 with the separate
[attained-optimizer encoding theorem](nonconvex-attainment-and-optimizer.md)
also puts attainment testing and recovery of an attained optimizer in
\(\mathrm{FP}^{\mathrm{NP}}\).

For rational MISOCP constraints and a rational affine objective, classification,
exact finite-value computation, attainment testing, and recovery of an
attained optimizer are in deterministic polynomial time for fixed
squared-continuous-Hessian span \(h\). For the last two tasks, item 3
reduces the problem to the separately reviewed case of boxed integer
variables.

This extends exact conic value computation beyond objectives depending only
on integer variables. A finite value can now be unattained and can arise
from integer assignments escaping to infinity. The theorem controls that
possibility without identifying continuous and mixed-integer unboundedness.
The suggested solver capability is exact status and value certification for
one-integer conic subproblems. No practical speedup or usable numerical
constant is established.

## 2. Compressed projection and coefficient-sensitive elimination

Write

\[
 \mathcal E=\{(z,t)\in\mathbb R^2:
            \exists x\ (z,x)\in S,\ q_0(z,x)\le t\}.
                                                        \tag{1}
\]

Every vertical fiber of \(\mathcal E\) is empty, all of \(\mathbb R\),
or a ray with a possibly excluded lower endpoint. Its lower endpoint is

\[
 \varphi(z)=\inf\{q_0(z,x):(z,x)\in S\},
\]

with the usual conventions \(+\infty\) for an empty fiber and
\(-\infty\) for an unbounded objective in that fiber.

Apply Section 2 of the compressed-projection theorem with free parameters
\((z,t)\), and with the objective threshold appended as one quadratic
row. Its continuous Hessian adds at most one direction. The formula has
quantifier block sizes \(1,1,h+2\), and integer atomic polynomials with
degree and individual coefficient bit length \(N^{O(1)}\). Its Boolean
matrix can be exponentially large. The determinant, rank-chart, finite-grid,
and bounded-limit arguments are unaffected by having two free parameters:
the coefficients remain polynomial in those parameters, of polynomial degree
and coefficient size. In particular, \(z\) remains a parameter; it is
never counted as another continuous variable in a full-Hessian oracle.

Coefficient-sensitive block quantifier elimination gives a quantifier-free
formula for \(\mathcal E\), all of whose nonzero atomic polynomials
\(P(z,t)\in\mathbb Z[z,t]\) have

\[
              \deg P\le D=N^{O(h+1)},\qquad
              \operatorname{bitsize}(P)\le H=N^{O(h+1)}.     \tag{2}
\]

The individual degree and coefficient bounds do not depend on the number
of atoms. This distinction is essential: constructing this formula is not
part of the final polynomial-time or oracle algorithm.

The source is Basu--Pollack--Roy, *Algorithms in Real Algebraic Geometry*,
Theorem 14.16, stated with the integer coefficient bound in
[Basu's author survey, Theorem 2.27](https://arxiv.org/abs/1409.1534).
The primary statement was inspected in the local full-text copy
`research-20260925/publication-sources/basu-2014-author-survey.txt`,
lines 784--805. Its coefficient bound is linear in input coefficient size
and singly exponential in the product of the quantified block dimensions;
here the number of blocks and the number of free variables are fixed.

The same argument without the objective row gives a univariate description
of \(Y=\{z:\exists x\ (z,x)\in S\}\), with the bounds (2).
Every finite endpoint of \(Y\) is a root of one of those polynomials.
Cauchy's root bound places all such endpoints inside
\([-2^{H+2},2^{H+2}]\). Beyond that interval membership in \(Y\) is
constant. If \(Y\) contains an integer, it therefore contains one with
polynomially bounded bit length as in Theorem 1.1. This argument works for
nonconvex \(Y\), because the integer dimension is one.

## 3. An effective tail lemma independent of the number of atoms

We prove an elementary quantitative version of planar semialgebraic
monotonicity. Let an upward-closed set \(\mathcal E\subseteq\mathbb R^2\)
be described by a Boolean formula in integer polynomials of total degree at
most \(D\) and coefficient bit length at most \(H\). There is an integer

\[
       B\ge2,\qquad \log_2 B\le (H+1)(D+1)^{O(1)},          \tag{3}
\]

such that, on each of \((B,\infty)\) and \((-\infty,-B)\), its lower
fiber endpoint is identically \(+\infty\), identically \(-\infty\), or
one real analytic algebraic function. In the last case this function is
constant or strictly monotone, and membership of its graph in \(\mathcal E\)
is constant along the entire tail.

### 3.1 Factor and project individual polynomials

Factor each nonzero atom over \(\mathbb Q[z,t]\), and use distinct
primitive integer irreducible factors. Each factor has degree at most
\(D\) and coefficient bit length polynomial in \(D,H\). One elementary
way to verify the height assertion is the substitution
\(z=X,t=X^{D+1}\): it is injective on the monomials of every factor,
its degree is at most \(D(D+1)\), and it preserves the factorization.
For completeness, Cauchy's bound bounds every root of the substituted input
by \(1+2^H\). The leading integer coefficient of an integer factor divides
the input's leading coefficient. Expressing its other coefficients as
elementary symmetric functions of a subset of the roots bounds their bit
lengths by \(O(D(D+1)(H+2))\). Injectivity gives the same bound for the
bivariate factor. This is a height argument, not a proposed factoring algorithm.

Include every factor that depends only on \(z\) in a projection family.
For every factor \(G(z,t)\) of positive \(t\)-degree, also include its
leading coefficient as a polynomial in \(t\), and the nonzero polynomials

\[
 \operatorname{Res}_t(G,G_t),\qquad
 \operatorname{Res}_t(G,G_z),                              \tag{4}
\]

where the second is omitted if \(G_z=0\). Finally include
\(\operatorname{Res}_t(G,K)\) for every distinct pair of positive
\(t\)-degree factors. Zero constants or redundant nonzero constants may
be discarded.

All displayed resultants that are asserted nonzero are indeed nonzero.
An irreducible \(G\) of positive \(t\)-degree is primitive in
\(\mathbb Q[z][t]\), so remains irreducible over \(\mathbb Q(z)\).
Characteristic zero gives \(\gcd(G,G_t)=1\). If \(G_z\ne0\), the
strict decrease of its \(z\)-degree rules out divisibility by \(G\).
Distinct primitive irreducible factors are coprime over \(\mathbb Q(z)\).

Every member of the projection family has degree and coefficient bit length
bounded by a fixed polynomial in \(D,H\). A Sylvester determinant has
size at most \(2D\), so this follows directly by expanding that determinant.
Cauchy's bound now gives an integer \(B\) satisfying (3) and exceeding
the absolute values of all real roots of every projection polynomial.
There can be arbitrarily many such polynomials: the same individual root
bound applies to every one, without multiplying them together.

### 3.2 Sections, signs, and monotonicity

On either tail, the leading coefficients are nonzero and every specialized
\(G\) has simple roots. The real roots form analytic sections over the
whole tail; they cannot appear, disappear, escape at a finite parameter,
or collide. Roots belonging to different factors cannot cross. Ordered
sections therefore partition the tail cylinder into graphs and open strips.
Every original atom has a constant sign on each graph or strip, so the
Boolean formula has constant truth value there. Upward closure implies that
its lower boundary is everywhere empty, everywhere all real values, or
exactly one fixed section.

For a section \(t=g(z)\) belonging to \(G\),

\[
                  g'(z)=-G_z(z,g(z))/G_t(z,g(z)).            \tag{5}
\]

The denominator never vanishes. If \(G_z=0\), the section is constant;
otherwise the second resultant in (4) makes the numerator nonzero everywhere
on the tail. Its sign is constant, so \(g\) is strictly monotone. The
constant truth value on the boundary graph also proves the final membership
assertion. This establishes the tail lemma.

## 4. Integer infima and limits at infinity

Choose the integer \(B\) above and partition the integer line into
\([-B,B]\), \(\{B+1,B+2,\ldots\}\), and
\(\{-B-1,-B-2,\ldots\}\). Suppose the mixed-integer infimum is finite.
Neither tail can have lower endpoint \(-\infty\).

On a nonempty tail with finite lower endpoint \(g\), monotonicity shows
that the infimum over integers is either its value at the first integer in
that tail or its limit at the infinite end. The latter limit exists in the
extended reals. If that tail contributes to a finite global infimum, its
limit is finite whenever it is the relevant candidate.

Every finite value \(\varphi(j)\) at an integer \(|j|\le B+1\) is
annihilated by a nonzero specialization \(P(j,t)\) of some atom from (2).
Indeed, after zero specializations are removed, if none of the remaining
polynomials vanished there then every sign would be locally constant in
\(t\), contradicting the finite endpoint of the vertical fiber.
The specialized degree is at most \(D\), and coefficient bit length is
at most

\[
                       H+D\log_2(B+2)+O(\log(D+1)).          \tag{6}
\]

For a finite tail limit \(\ell\), take the factor \(G\) defining its
section and write

\[
                    G(z,t)=\sum_{a=0}^{d} z^aG_a(t),
                    \qquad G_d\ne0.
\]

Dividing \(G(z,g(z))=0\) by \(z^d\) and letting \(z\) tend to the
corresponding infinity gives

\[
                              G_d(\ell)=0.                  \tag{7}
\]

Boundedness of \(g\) along this limit justifies discarding every lower
power. The polynomial \(G_d\) is nonzero and inherits the factor degree
and height bounds.

The global infimum is the minimum of finitely many central fiber infima
and the two tail infima. Therefore it equals one of the algebraic numbers
just bounded. Taking a minimum does not require multiplying their minimal
polynomials: one candidate polynomial already annihilates the selected
value. Combining (2), (3), (6), and (7) proves Theorem 1.2 with a bound
\(N^{O(h+1)}\).

For attainment, suppose an optimal integer lies farther along a tail than
its first integer. If the boundary function were strictly monotone, either
the first integer or a farther integer would have a strictly smaller fiber
infimum, contradicting global optimality. Thus the boundary function must
be constant. Since the optimum is attained at one point of its graph,
Section 3.2 says the whole boundary graph belongs to \(\mathcal E\).
The first integer of that tail also has an attained optimum. This proves
Theorem 1.3. It does not assert that every optimal integer is small.

## 5. Exact algorithms without constructing the projection

### 5.1 Nonconvex feasibility and rational thresholds

The integer-witness bound from Section 2 lets an NP verifier guess a
polynomial-bit integer \(z\) for fixed \(h\). Substitute it in the
original system. The reviewed
[nonconvex few-Hessian witness result](nonconvex-hessian-span-frontier.md)
provides a common real algebraic representation of a feasible continuous
point with polynomial encoding length. Exact polynomial evaluation and
sign determination verify this representation. Conversely, an accepted
certificate supplies an actual feasible point. Thus feasibility is in NP.
The same argument applies to every rational objective threshold, which adds
at most one continuous Hessian direction.

An integer factor-height bound turns the annihilating-polynomial bounds
into bounds of the same form on the primitive minimal polynomial. Let
\(D_*,H_*\le N^{C(h+1)}\) denote these enlarged bounds for a finite
value. Cauchy's bound gives \(|\theta|<M\), where
\(M=2^{H_*+2}\). First test feasibility. On a nonempty instance, a single
threshold query \(q_0\le -M-1\) distinguishes \(-\infty\) from a finite
infimum. In the finite case, rational threshold bisection keeps an interval
containing \(\theta\): a yes answer gives \(\theta\le t\), and a no
answer gives \(\theta\ge t\). At an unattained threshold equal to the
infimum, the latter weak inequality is the correct invariant.

A polynomial number of bits of approximation, together with \(D_*,H_*\),
permits exact algebraic recognition by the classical integer-relation
method used in the [continuous finite-infimum note](nonconvex-finite-infimum.md).
This proves \(\mathrm{FP}^{\mathrm{NP}}\) classification and value recovery.
The constants in the theoretical radius and height bounds can be fixed
from the effective inequalities; their useful practical size is not claimed.

If the value is attained, Theorem 1.3 bounds one optimal integer assignment.
The attained-optimizer theorem then bounds an algebraic continuous optimizer.
An NP certificate for attainment guesses this pair. To verify objective
value \(\theta\), evaluate its supplied minimal polynomial at
\(q_0(z,x)\) and verify that the value lies in the supplied rational
isolating interval for \(\theta\). There is no need to construct a
compositum with an unrelated representation of \(\theta\). Standard
bit-by-bit search in this bounded NP certificate relation recovers an
optimizer when one exists.

### 5.2 Rational MISOCP

For rational cone constraints, retain both the squared residual inequality
and its affine sign condition. For every rational affine objective threshold,
[unbounded MISOCP feasibility](unbounded-misocp-frontier.md) supplies a
deterministic polynomial-time oracle at fixed \(h\). Thus the same cutoff,
bisection, and recognition procedure yields exact status and value in
polynomial time, including finite unattained infima.

To decide attainment after computing \(\theta\), apply
[boxed-integer SOCP optimization](boxed-misocp-optimization.md) with the
rational integer bounds \(-B-1\le z\le B+1\) from Section 3. Let its
finite infimum be \(\beta\), when its feasible set is nonempty.
The original infimum is attained if and only if \(\beta=\theta\) and
the boxed problem's infimum is attained. The forward implication is
Theorem 1.3; the reverse follows because the boxed feasible set is a
subset of the original set. The boxed algorithm decides these conditions
and returns an exact optimizer when they hold. Equality of the two exact
algebraic values is decidable in polynomial time. The binary length of the
new integer bounds is polynomial for fixed \(h\), so the composition
remains polynomial time. This step does not assume that equality of finite
infima alone implies attainment.

The separate [algebraic-threshold oracle](algebraic-threshold-misocp.md)
and its completed independent review offer another route: test the original system
with \(q_0\le\theta\), return an integer assignment, and solve its
rational continuous fiber by
[continuous SOCP optimization](continuous-socp-optimization.md). The main
attainment proof does not depend on that more general oracle.

## 6. Boundaries, example, and prior work

The system

\[
 z\ge1,\quad x\ge0,\quad \|(2,z-x)\|_2\le z+x,
 \qquad z\in\mathbb Z,
\]

with objective \(\min x\), has fiber optimum \(1/z\). Its global
infimum is zero and is not attained. The squared residual is
\(4-4zx\), so its continuous Hessian span is \(h=0\).
This example shows that unattainment caused by the integer tail already
occurs at the smallest continuous span. The tail proof detects zero from
the leading-\(z\) coefficient of \(zt-1\).

The proof is specific to one integer variable. With two or more integer
variables, a semialgebraic tail does not reduce to finitely many ordered
monotone branches. Lattice approximation to irrational directions can
matter. The reviewed [two-integer Pell boundary](two-integer-pell-output-boundary.md)
gives a concrete obstruction to extending the nonconvex output bound:
the family \(x^2-5^{2m+1}y^2=1\), with \(x\ge2\), \(y\ge1\)
integer and objective \(\min x\), has input length \(\Theta(m)\)
but optimum and every feasible witness require \(\Theta(5^m)\) or
more binary digits. There are no continuous variables, so \(h=0\).
This is a classical Pell output-size phenomenon, not a new lower bound;
its indefinite equality does not obstruct the separate
[convex multiple-integer theorem](unbounded-misocp-multiple-integer-frontier.md).
This note also does not claim a polynomial-time algorithm for nonconvex systems at fixed span:
the purely continuous case can already be NP-hard.

The underlying semialgebraic monotonicity, cylindrical sign decomposition,
resultant bounds, and algebraic recognition are established tools. The
candidate addition is their combination with the compressed projection
whose quantified dimension is controlled by the continuous Hessian span,
including arbitrary affine rows, cross terms, degeneracy, and nonattainment.
The projection formula and the height bound, rather than monotonicity by
itself, carry the parameter-sensitive claim.

The completed [prior-work audit](one-integer-value-prior.md) records two
especially close precedents. Grigoriev--Pasechnik's Theorem 1.5 announces
exact infimum computation for few quadratic maps, including nonattainment,
but defers its proof. [Kamminga--Rudolph, ITCS 2026, Theorem 5.2 and
Remark 5.3](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.83/LIPIcs.ITCS.2026.83.pdf)
explicitly treats few-variable critical formulas with symbolic parameters;
the paper also says that a proof of that earlier unbounded optimization
claim is unavailable to the authors' knowledge. Consequently, neither
few-variable compression nor symbolic parameter treatment is claimed as
new in itself. Arbitrarily many affine rows and an unbounded integer
coordinate are additional features of the present theorem.

Existing one-integer convex optimization through slice-value oracles is
also prior work: Baes--Oertel--Wagner--Weismantel, Section 4.1, assumes a
bounded integer interval, a finite objective spread, and approximate slice
oracles. It does not supply the unbounded exact value bound used here.
The audit gives the sources and detailed assumption comparisons. A remaining
novelty pressure point is whether parameterized quadratic-map sampling plus
the minimum-face argument already yields the projection bounds as a short
corollary; that uniform specialization argument has not been completed in
the audit. The available evidence does not establish priority.

## 7. Verification status

The coefficient-size clause of the primary quantifier-elimination theorem
was inspected directly. The proof above gives explicit algebraic reasons
for the required projection resultants to be nonzero and for the finite
limit to satisfy (7). The independent review read the full proof and its
revised boxed-integer attainment argument, attacked open endpoints and
switching branches, and found no gap. A separate reviewer directly checked
the primary elimination height clause and the factor-height argument.
These reviews do not replace the existing reviews of the compressed
projection and continuous algebraic-encoding dependencies.

The targeted command
`python research-20260927/check_one_integer_value.py` passed five exact
projection/limit cases and 64 exact cone fibers. Its first run exposed a
mistaken expected sign for one nonzero resultant in the test; the expected
identity was corrected. No proof step depends on that sign. The script
checks examples and algebraic identities, not the general elimination,
analytic-section, or complexity arguments. No project-wide verification
or CI inspection was performed.

A targeted `python -` document check passed for twelve local links, matching
math delimiters, whitespace, control characters, and the final newline.
These formatting checks do not verify the mathematical argument.
