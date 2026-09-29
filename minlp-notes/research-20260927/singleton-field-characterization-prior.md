# Prior audit of the field characterization for convex singletons

Date: 2026-09-28. Scope: the final characterization and the planar
corank-one pencil in
[the three-quadratic construction](few-quadratic-unbounded-degree.md).
This supplements [the earlier construction audit](three-ellipsoid-degree-prior-audit.md).
An independent adversarial check of the signature necessity is included
below; this note does not repeat the full construction proof review.
The [fresh review](singleton-field-characterization-prior-review.md) checks
the proof and source comparisons. Complementary searches are recorded in
[the native-polynomial audit](singleton-field-characterization-prior-independent.md)
and [the spectrahedral audit](planar-corank-one-singletons-prior.md).

No inspected primary source states the full equivalence proved in the
construction note. This does not establish priority. Irrational singleton
feasibility, moment representations of finite varieties, interpolation
over real and complex roots, and rational rounding of Gram matrices all
have direct predecessors. The most specific remaining comparison is the
realization of every permitted coordinate by **three rational
positive-definite quadratic inequalities**, together with the prescribed
two-parameter, corank-one pencil and short binomial construction.

## 1. Exact statement and an independent necessity check

The statement concerns finite systems

\[
 S=\{x\in\mathbb R^n:f_i(x)\le0,\quad i=1,\ldots,m\}=\{x_*\},
 \qquad f_i\in\mathbb Q[x_1,\ldots,x_n],
\]

where each defining polynomial is globally convex. A real algebraic
number \(\alpha\) occurs as a coordinate of such a singleton if and
only if its minimal polynomial has exactly one real root. Sufficiency
comes from the separately reviewed three-quadratic construction, with a
simple rational construction for degree one.

The following necessity argument was checked independently by the audit
author and a separate arithmetic reviewer. A rational semialgebraic
singleton has algebraic coordinates: each coordinate projection is a
semialgebraic singleton defined over \(\mathbb Q\), and real quantifier
elimination makes its coordinate a root of a nonzero rational polynomial.
Put \(K=\mathbb Q(x_{*,1},\ldots,x_{*,n})\).

Let \(I\) be the indices active at \(x_*\). Their inequalities alone
have feasible set \(\{x_*\}\). Indeed, if another point \(y\)
satisfied them, convexity would make the whole segment from \(x_*\)
to \(y\) satisfy them. Every inactive polynomial is strictly negative
at \(x_*\), so continuity keeps a sufficiently short initial segment
feasible for that row. There are finitely many rows, hence a common
positive segment length works for all of them, contradicting uniqueness.

Every real embedding \(\sigma:K\hookrightarrow\mathbb R\) preserves
the active polynomial **equalities**. Thus \(\sigma(x_*)\) satisfies
all active inequalities, and the preceding argument forces
\(\sigma(x_*)=x_*\). Since the coordinates generate \(K\), there is
exactly one real embedding of \(K\). Consequently
\([K:\mathbb Q]=1+2r_2\) is odd.

For a coordinate \(\alpha\), let \(L=\mathbb Q(\alpha)\).
The degree \([K:L]\) is odd. Given any real embedding
\(\tau:L\hookrightarrow\mathbb R\), choose a primitive element of
\(K/L\), apply \(\tau\) to its irreducible minimal polynomial,
and take a real root of the resulting odd-degree polynomial. This gives
a real embedding of \(K\) extending \(\tau\). Since \(K\) has
only one real embedding, so does \(L\). That is precisely the claimed
one-real-conjugate property of \(\alpha\).

This proof does not assume that real embeddings preserve inequality
signs. It uses preserved equalities, uniqueness of the **whole tuple**,
and finiteness of the constraint family. No gap was found in these steps.

In fact, necessity only needs each individual active zero sublevel
\(\{f_i\le0\}\) to be convex; global convexity of its defining
polynomial is stronger. That weaker representation class should not be
advertised as a difficult sufficiency result: if an irreducible
\(p\in\mathbb Q[t]\) has exactly one real root, the single row
\(p(t)^2\le0\) already defines that singleton and has a convex zero
sublevel. The three positive-definite quadratic realization is the
substantive stronger representation.

## 2. Essential scope distinction

The result is not a characterization of all convex semialgebraic
singletons. For example,

\[
 \{x:x^2-2=0,\ x\ge0\}=\{\sqrt2\}
\]

is rational semialgebraic and convex, but \(\sqrt2\) has two real
conjugates. Expressing equality as two inequalities includes a defining
row whose zero sublevel is not convex.

Nor does the argument apply to arbitrary rational SOCP or SDP
descriptions. The earlier audit records explicit quadratic-irrational
singleton examples, including SPECTRA's rational univariate pencil with
singleton \(\{\sqrt2\}\) and feasible-matrix corank two. A convex
cone constraint is not automatically a globally convex polynomial
inequality after squaring or expanding principal minors.

Bodirsky--Jonsson--von Oertzen, *Essential Convexity and Complexity of
Semi-Algebraic Constraints* (2012), Section 6, explicitly considers
systems of polynomial inequalities whose individual solution sets are
convex. That is a relevant established representation class. The
inspected Sections 3, 4 and 6 concern logical descriptions and
complexity, not the present number-field classification.
[Primary PDF](https://lmcs.episciences.org/1218/pdf)

## 3. Direct native-polynomial predecessor

Slot--Steurer--Wiedmer, *Hesse's Redemption: Efficient Convex Polynomial
Programming*, arXiv:2511.03440v1, Appendix C, Example C.2, gives

\[
 f(x)=(x^3+x+1)^2,
 \qquad f''(x)=30x^4+6x^2+2(3x+1)^2\ge0.
\]

Its zero sublevel is the unique real root of \(x^3+x+1\), an
irrational algebraic number of degree three. This is already a rational
globally convex polynomial with an irrational singleton feasible set.
Lemma C.3 contrasts it with univariate convex quartics whose minimum
value is rational: those have rational minimizers. These statements do
not give the arbitrary-degree quadratic-system construction or the full
signature characterization.
[Primary Appendix C](https://arxiv.org/html/2511.03440v1#A3)

## 4. A close antecedent to the construction's positive semidefinite form

Krick--Mourrain--Szanto, *Univariate Rational Sums of Squares*, Section
2.1, equations (4) and (6), uses Lagrange polynomials \(u_\beta\) for
the roots of a squarefree real polynomial \(p\) of degree \(d\). Distinct root
polynomials have product zero modulo \(p\). Their displayed
construction, formally specialized to zero target polynomial, gives

\[
 h=2\sum_{\{\beta,\bar\beta\}}
       \lambda_\beta u_\beta u_{\bar\beta}
   =2\sum_{\{\beta,\bar\beta\}}\lambda_\beta
       \big((\operatorname{Re}u_\beta)^2+
            (\operatorname{Im}u_\beta)^2\big)
       \equiv0\pmod p,
 \qquad \lambda_\beta>0.
\]

The corresponding Gram matrix has kernel spanned by the real root
evaluation vectors. For one real root this supplies the same structural
positive semidefinite form \(B_*\) used in the local construction.
This specialization is an inference from the displayed identities, not
their Proposition 2.2, which assumes strict positivity at real roots.
Lemma 2.7 and Proposition 2.8 also provide rational rounding and
projection arguments.
[Primary PDF](https://arxiv.org/pdf/2112.00490)

There is a material difference at the zero target. Let \(p\in\mathbb Q[t]\)
be irreducible of degree \(d\), with a real root \(\alpha\), and put
\(v(t)=(1,t,\ldots,t^{d-1})^T\). For rational \(B\) with
\(v(t)^TBv(t)\equiv0\pmod p\), positive semidefiniteness would imply
\(Bv(\alpha)=0\). Independence of
\(1,\alpha,\ldots,\alpha^{d-1}\) would then force \(B=0\).
Thus a nonzero rational positive semidefinite approximation satisfying
the exact congruence is impossible in this boundary situation. The new construction instead
preserves positivity on the subspace associated with nonreal roots,
allows \(B\) to be indefinite, and uses the companion-matrix sandwich
\((C-\alpha I)^TB(C-\alpha I)\) to obtain the required positive
semidefinite matrix. The conversion of these ingredients into three
rational ellipsoids remains the specific step requiring priority review.

## 5. Spectrahedral and arithmetic predecessors

Laurent's finite-variety moment representation already supplies the
power-basis singleton of arbitrary degree when \(p\) has one real
root. The representation has \(d-1\) scalar variables and its unique
matrix has rank one, hence corank \(d-1\). The construction under
review has two scalar variables and corank one. These are different
properties. The precise Laurent comparison, and Laplagne's published
irrational singleton Gram example, are recorded in the
[earlier audit](three-ellipsoid-degree-prior-audit.md).
[Laurent primary PDF](https://ir.cwi.nl/pub/11663/11663D.pdf),
[Laplagne primary PDF](https://arxiv.org/pdf/1810.04215)

Hillar's 2010 BIRS slides, slide 18, explicitly raise a fixed-variable
question about representing real algebraic numbers by finite rational
spectrahedra, and credit Laurent for representations when the sizes may
vary. This is historical motivation, not evidence that the question
remains open. The slide's final display is imprecise, so it should not
be used as a precise theorem or problem specification.
[Primary slides](https://staff.math.su.se/shapiro/ProblemSolving/hillarbirstalk20100302.pdf)

There is also an established spectral restriction on one-parameter
pencils. Liang--Li--Bai (2013), Lemma 3.8(2), printed p. 3095, states
that the finite eigenvalues of a positive semidefinite Hermitian pencil
are real, including the singular-pencil setting. This is a direct
predecessor for the total-reality obstruction in a rational
one-parameter singleton pencil. It is not itself an arithmetic
realization theorem, nor the two-parameter corank-one construction.
[Primary PDF](https://web.cs.ucdavis.edu/~bai/publications/lianglibai13.pdf)

The separate [one-parameter classification](one-parameter-spectrahedral-fields.md)
derives the total-reality criterion and sharp minimum size \(2d\), with
an [independent proof review](one-parameter-spectrahedral-fields-review.md).
Those statements use classical spectral and trace-form ingredients;
their publication priority is not asserted.

Hillar's Theorems 1.4--1.5 and Scheiderer's later Theorem 1.2 and
Proposition 1.6 establish sums-of-squares and quadratic-module descent
over totally real extensions. They concern fields of **SOS
coefficients**, not fields of entries in an arbitrary PSD feasible
matrix. The trace-form signature and real embeddings are established
arithmetic ingredients.
[Hillar primary PDF](https://arxiv.org/pdf/0704.2824),
[Scheiderer primary PDF](https://ems.press/content/serial-article-files/32129?nt=1)

Chua--Plaumann--Sinn--Vinzant, *Gram Spectrahedra*, Remark 1.7, makes
the distinction explicit: \(x^2+\sqrt2\) has a PSD Gram matrix with
entries in \(\mathbb Q(\sqrt2)\) under its chosen embedding but is
not a sum of squares over that field. Positivity at one embedding is
weaker than positivity at every ordering. Consequently SOS descent
cannot be invoked merely because a PSD matrix has totally real
entries.
[Primary PDF](https://arxiv.org/pdf/1608.00234)

## 6. Assessment and verification record

The searched sources do not establish the exact globally convex
polynomial singleton equivalence or the three-ellipsoid realization.
The necessary field argument is short and uses classical convexity,
quantifier elimination and elementary field theory. Its correctness
should not be confused with evidence of originality. The sharper
representation and coefficient bounds deserve the main significance
assessment; arbitrary-degree spectrahedral singletons alone are already
covered by prior moment constructions.

Searches covered rational convex polynomial singletons, conjugates and
real embeddings, uniquely ordered fields, totally real SOS descent,
Gram spectrahedra, corank-one singleton pencils, rational spectrahedral
points, and fixed-variable representations of algebraic numbers.
Independent agents checked the arithmetic literature, the spectrahedral
literature, and convex constraint-satisfaction terminology. The active
constraint and field-extension argument above received an independent
adversarial proof check. The key primary pages cited above were inspected;
the detailed older Laurent/Laplagne/SPECTRA checks remain recorded in the
linked earlier audit.

This note reports a literature comparison and a proof audit. It does not
claim a solver speedup, a decision lower bound, or an obstruction to all
exact witness representations. An inline `python - <<'PY'` check using
`pathlib` and `re` verified this file's final newline, trailing whitespace,
control characters, balanced inline/display math delimiters, and relative
Markdown links. It passed. No project-wide checks or CI inspection were
used.
