# Classical low-dimensional bounds: independent review

Date: 2026-09-28. Status: independent source and proof review completed.
No gap was found in the application below, including Section 6 of the
[author note](common-range-optimizer-witness.md). The low-dimensional
degree and height bound is a consequence of classical quantifier
elimination, not an independent new theorem of this research package.

The initial generic-perturbation proof was also checked, including a
separate genericity review, and is preserved in the
[alternative review](common-range-lowdim-perturbation-review.md).
The classical deduction is simpler and should be the main justification.

## 1. Source statement and its scope

Theorem 2.27 in
[Basu's author survey, printed page 16](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf)
gives quantifier elimination for a Boolean formula using \(s\)
polynomials of degree at most \(d\), with quantified block sizes
\(k_1,\ldots,k_\omega\) and \(\ell\) free variables. Each output
polynomial has degree at most \(d^{O(k_\omega)\cdots O(k_1)}\).
For integer inputs of coefficient bits at most \(\tau\), its
coefficient bits are at most
\(\tau d^{O(k_\omega)\cdots O(k_1)O(\ell)}\). These bounds do not
depend on \(s\). The output count and runtime do depend on \(s\),
with exponents depending on the block sizes. The theorem is attributed
there to Basu--Pollack--Roy.

The reviewer read the statement directly in the preserved
[source text](../research-20260925/publication-sources/basu-2014-author-survey.txt),
lines 784--805. This application uses the bounds for an existing output
polynomial. It does not construct the potentially large eliminated
formula or infer a fixed parameter runtime for quantifier elimination.

## 2. Finite infimum

Let
\[
 D=\{u\in\mathbb R^r:p_i(u)\le0\ (1\le i\le m)\}\ne\varnothing,
\]
where every \(p_i\), and an objective \(g\), are rational polynomials
of degree at most four. Let each rational coefficient have numerator and
denominator bits at most \(\tau\ge1\). Clear denominators separately
for each polynomial, using a positive multiplier. There are at most
\(\binom{r+4}{4}\) coefficient positions per polynomial, so the
resulting integer coefficient bits are at most \(F(r)\tau\). No
denominators are multiplied across all \(m\) rows.

Consider the formula with one free scalar \(t\),
\[
 \Phi(t)\equiv\exists u\,[u\in D\ \wedge\ g(u)\le t].
\]
Its degree is at most four and its quantified block has size \(r\).
If \(\theta=\inf_D g\) is finite, the truth set is either
\([\theta,\infty)\) or \((\theta,\infty)\), according to
attainment.

Some nonzero polynomial in a quantifier-free output must vanish at
\(\theta\). Otherwise every nonzero output polynomial would have
constant sign in a common neighborhood of \(\theta\); identically
zero polynomials have constant sign as well. The whole Boolean formula
would then have constant truth value there, contradicting the endpoint
property. The source theorem therefore supplies an integer annihilator
of degree \(F(r)\) and coefficient bits \(F(r)\tau\).

No boundedness, attainment, constraint qualification, or radius estimate
is needed. The case \(r=0\) is the constant-objective case and is
immediate.

## 3. All coordinates of one selected optimizer

Suppose the minimum is attained. Its optimizer set is nonempty and
closed. A norm-minimizing sequence can be restricted to a closed ball
by comparison with one optimizer, so the least norm is attained. The
set of minimum-norm optimizers is compact, being a closed subset of a
fixed sphere. It has a unique lexicographically least point \(u^*\),
obtained by minimizing its coordinates successively.

For a candidate \(u\), use the formula
\[
\begin{split}
 \mathcal A(u)\equiv{}&u\in D\\
 &\wedge\ \forall v\,[v\in D\Rightarrow g(u)\le g(v)]\\
 &\wedge\ \forall w\,[(w\in D\wedge g(w)=g(u))
                     \Rightarrow\|u\|^2\le\|w\|^2]\\
 &\wedge\ \forall y\,[(y\in D\wedge g(y)=g(u)
                     \wedge\|y\|^2=\|u\|^2)
                     \Rightarrow u\le_{\rm lex}y].
\end{split}
\]
The clauses impose global optimality, minimum norm, and then the unique
lexicographic choice. The last relation is a Boolean formula in linear
equalities and strict inequalities. The universal blocks merge into
one block \((v,w,y)\) of size \(3r\). No unknown optimal value is
inserted as a coefficient.

For coordinate \(j\), apply quantifier elimination to
\[
 \exists u\,[\mathcal A(u)\wedge t=u_j].
\]
It has quantified block sizes \(r\) and \(3r\), one free scalar,
and atom degrees at most four. Separate denominator clearing still
gives coefficient bits \(F(r)\tau\). Its truth set is the singleton
\(\{u_j^*\}\), so the local-sign argument supplies a nonzero integer
annihilator with degree \(F(r)\) and coefficient bits \(F(r)\tau\).
All coordinate formulas describe the same point; selecting unrelated
optimizers separately for different coordinates would not suffice.

Multiplying the \(r\) coordinate degree bounds gives a common field
degree at most \(F(r)^r\), still depending only on \(r\). The same
height bound gives a rational univariate representation of total bits
\(F(r)\tau\), after increasing \(F\). An explicit conversion appears
in Section 4 of the
[alternative review](common-range-lowdim-perturbation-review.md): scale
the coordinates by their annihilator leading coefficients, select a
small primitive integer linear combination, and use the nonsingular
trace pairing and Cramer's rule. Conjugate root bounds and the nonzero
integer discriminant bound the resulting coefficients and real isolating
interval. All field degrees involved depend only on \(r\), so the
height dependence stays linear in \(\tau\).

Thus the proposed weaker encoding bound
\(F(r)(\tau+\log(m+1)+1)\) follows. The source theorem removes the
row-count term from this per-polynomial bound under the stated
individual-coefficient convention. It does not remove the row-count
dependence from constructing the whole eliminated formula.

## 4. Canonical projected coordinates in the convex case

This section checks the additional argument in Section 6 of the author
note, taking its quadratic programming chart lemma as established.
Write \(D_I\) for each closed chart domain, \(g_I\) for its quartic
objective, and \(\theta\) for the attained finite optimum. The
projection \(U^*\) of the original optimal set onto the nonlinear
coordinates satisfies
\[
 U^*=\bigcup_I\{u\in D_I:g_I(u)=\theta\}.
\]
For the forward inclusion, replace the fiber optimizer by its
minimum-norm fiber optimizer, which the chart lemma represents. For the
reverse inclusion, every retained chart point is original feasible and
has value \(\theta\). Thus the identity is exact.

This is a finite union of closed sets, so \(U^*\) is closed. If the
original feasible set and objective are convex, the original optimal
set is convex and its linear projection is convex. Hence \(U^*\) has
a unique minimum-norm point \(\bar u\). The closedness argument is
essential: general linear projections of closed convex sets need not
be closed.

Let
\[
 H(u,t)=\bigvee_I[u\in D_I\wedge g_I(u)=t].
\]
The formula
\[
\begin{split}
 H(u,t)&\wedge\forall v\bigwedge_I
       [v\in D_I\Rightarrow t\le g_I(v)]\\
 &\wedge\forall w\bigwedge_I
       [(w\in D_I\wedge g_I(w)=t)
                          \Rightarrow\|u\|^2\le\|w\|^2]
\end{split}
\]
selects exactly \((\bar u,\theta)\). Membership supplies an actual
chart point; the first universal clause makes its value globally
optimal; the second minimizes the norm over the exact set \(U^*\).
For each scalar coordinate output, quantify \((u,t)\) existentially
and merge \((v,w)\) universally. The block sizes are \(r+1\) and
\(2r\), and degrees are at most four. Exponentially many chart
predicates do not change the source theorem's per-polynomial bounds.
Each chart coefficient has polynomial bits in the original input
length \(N\), giving common-field degree \(F(r)\) and total bits
\(F(r)N^C\), with an absolute constant \(C\).

Finally, for a convex quadratic
\(f(x)=\tfrac12x^TQx+a^Tx+c\), the gradient is constant over its
convex optimal set. If \(x,y\) are optimizers, their whole segment is
optimal, so \((x-y)^TQ(x-y)=0\). Positive semidefiniteness implies
\(Q(x-y)=0\). One algebraic chart optimizer therefore encodes all
coordinates of the common gradient \(g^*\) in a single field of degree
\(F(r)\) and total bits \(F(r)N^C\). Taking its compositum with the
field of \((\bar u,\theta)\) preserves these forms of bound. There
are two bounded-degree fields, not a separate field for each ambient
gradient coordinate.

## 5. Verification limits

This review independently checked the exact source statement, separate
denominator clearing, the endpoint argument, the canonical optimizer
formula and its quantified blocks, the common-field conversion, and
the projected-coordinate and gradient addendum. It does not establish
the full common-range optimization algorithm or its oracle runtime.

Only targeted source reads and document checks were used for this
classical deduction. The separate perturbation review records its
exact symbolic example checks. No project-wide verification, CI
inspection, or Lean verification was performed.
