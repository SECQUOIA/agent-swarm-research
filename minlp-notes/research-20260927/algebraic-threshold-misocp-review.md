# Independent review of exact algebraic-threshold MISOCP feasibility

Date: 2026-09-28. Status: adversarial review completed. No unresolved
mathematical gap or counterexample was found in the common-field theorem
or its one-threshold corollary in
[the draft](algebraic-threshold-misocp.md).

The conclusion is polynomial Turing-time feasibility for fixed integer
dimension and fixed continuous squared-Hessian span, when one explicitly
represented real number field contains all coefficients. The field degree
may grow with the input. The construction ends with rational MILP and
returns an integer assignment with an exact continuous witness. It does
not claim that the MILP's displayed continuous point is that witness.

This review read the full draft, the relevant nonconvex perturbation and
boxed-value arguments, the field-height elimination lemma, the unbounded
projection formula, and the rational cone-lift construction. The primary
Khachiyan--Porkolab and Lenstra statements were checked separately. A
further reviewer independently checked the outward rounding estimates.
The proof still depends on the linked algebraic results; this is a review
of their use and the stated extension, not formal verification or a
priority determination.

## 1. The field model is sufficient and materially restrictive

The input specifies an irreducible polynomial of degree \(D\), a rational
interval selecting one real root \(\alpha\), and power-basis coefficient
vectors over \(K=\mathbb Q(\alpha)\). All this data counts toward the
input length \(N\). Thus \(D\le N\), and field arithmetic cannot hide
an exponentially large input degree.

Multiplication by a field element is a rational \(D\)-dimensional linear
map. A nonsingular \(r\)-dimensional system over \(K\) can therefore
be solved as a rational system of dimension \(rD\). The entries of these
rational matrices have polynomial bit length: reduction of powers modulo
the supplied polynomial uses only polynomial degrees and powers of its
leading coefficient. Determinant bounds then control inverses, affine
charts, and Hessian dependencies. No compositum or normal closure is
constructed.

The matrix-span parameter is correctly taken over \(K\). Flattening the
matrices turns the assertion into invariance of rank under the embedding
\(K\subseteq\mathbb R\), which follows from nonzero minors. A family
of rational matrices also has the same rank over \(\mathbb Q\) and
over \(K\). This proves the stated preservation of the original rational
parameter when only one algebraic affine threshold is appended. In
contrast, the \(\mathbb Q\)-linear span of algebraic matrices can have
a different dimension, as the draft's \(H,\sqrt2H\) example shows.

Independent algebraic encodings of many coefficients do not satisfy this
input promise without further work. Their joint field can have exponential
degree. The draft correctly excludes a polynomial-time claim in that
different representation model.

## 2. The nonconvex radius and value bounds extend over this field

The extension does not apply the convex theorem from
[the field-precision note](algebraic-coefficient-span-precision.md) to
indefinite squared cone residuals. It uses that note's purely algebraic
finite-quotient lemma together with the generic perturbation argument in
[the nonconvex note](nonconvex-hessian-span-frontier.md). This distinction
is necessary and is made explicitly.

The Hessian lift still has exactly \(h\) quadratic equations and retains
every affine row. Its active affine charts are over \(K\). On each
chart, unrestricted ambient quadratic perturbations restrict surjectively
to all chart quadratics. The bad-coefficient hypersurfaces and integer-grid
avoidance argument depend on dimensions and degrees, not rationality of
the original coefficients. The grid coefficients can therefore retain
polynomial bit length over the selected embedding.

For the small-point statement, the squared-norm perturbation remains
uniformly coercive for sufficiently small positive perturbation parameter.
Comparison with any exact feasible point gives a bounded minimizing
sequence. For the boxed-value statement, adding rational bounds for the
lifted quadratic coordinates makes the entire polyhedron compact. Uniform
convergence of the perturbed objective, together with an exact optimizer
that remains feasible in the bands, makes every selected minimizing limit
an original optimizer. Neither argument needs convex quadratic rows.

At selected minimizers, there is at most one active orientation per band,
hence at most \(h\) active nonlinear constraints. The genericity result
supplies independent active gradients and nonsingular multiplier and
bordered KKT matrices. After a fixed chart and support are selected along
a subsequence, the adjugate substitution has at most \(h\) multiplier
variables. A zero-dimensional chart gives a point over \(K\) directly.
These are precisely the hypotheses needed by the elimination lemma in
[the explicit separation note](explicit-span-separation.md); bounded
multipliers and nonsingularity of unrelated components are not needed.

The field-height estimate survives this substitution. Explicit input
coefficients have polynomial Weil height. At each place, determinant and
adjugate expressions have polynomial logarithmic coefficient norm: use
the coefficient \(\ell_1\)-norm at archimedean places and the maximum
coefficient norm at finite places. There are only a fixed number of
linear-algebra and determinant-substitution stages. The estimate therefore
does not sum the heights of exponentially many expanded monomials.

For multiplier degree \(a_0\) and \(s\le h\), the finite quotient
has dimension \(L=(a_0+1)^s\). The determinant norm gives a polynomial
\(P\in K[v]\) of degree at most \(L\) and joint coefficient height
at most

\[
 W=L(a_0(s+1)+1)E+\log(L!)+L\log3.
\]

The first nonzero coefficient extractions preserve these bounds. They
preserve the selected finite limit because the selected root is
nonsingular and its output denominator is nonzero. All real arguments use
the selected embedding. Other embeddings enter only through coefficient
norms; they need not preserve feasibility or optimality.

Finally,

\[
 [\mathbb Q(\beta):\mathbb Q]\le DL,\qquad
 h_{\rm W}(\beta)\le W+\log2,
\]

and the primitive integer minimal polynomial has logarithmic coefficient
norm at most \(DL(W+2\log2)\). These are polynomial bounds for fixed
\(h\), because \(D\) belongs to the explicit input. Cauchy's bound and
its reciprocal version give the required coordinate radius and positive
gap. No conversion to a normal closure or multiplication of separate
coordinate field degrees is used.

As a finite exact check of this field-to-rational step, over
\(K=\mathbb Q(\sqrt2)\) the equation \(v^2-\sqrt2=0\) gives
the rational annihilator \(v^4-2\). Its degree is \(DL=4\); the
normal closure is unnecessary. This example checks the mechanism, not
the universal height estimate.

## 3. The additional generator quantifier is valid

The compressed formula in
[the unbounded MISOCP proof](unbounded-misocp-frontier.md) has prefix

\[
 \exists R\;\forall\delta\;\exists(\varepsilon,\lambda),
 \qquad \dim\lambda=h.
\]

Its construction uses every relevant rank chart, a finite perturbation
grid, and a radius chosen before the universal perturbation bound. These
features remain valid over \(K\). In particular, the fixed radius
prevents sequences of fiber points escaping to infinity from making an
empty fiber look feasible. The formula defines the projection itself,
including when the projection is not closed.

First reducing all field arithmetic modulo the minimal polynomial and
then replacing coefficients by their polynomials in a variable \(t\)
produces rational polynomial atoms. Positive rational common denominators
can be cleared without changing signs. The original rational-function
chart denominators are separately cleared by even powers under their
nonvanishing guards, as in the linked proof. These are different
denominator operations, and neither presumes an algebraic denominator is
positive.

Conjoining the minimal polynomial equation and the isolator for \(t\)
forces exactly the intended value \(t=\alpha\). Putting this variable
in the first existential block gives block dimensions \(2,1,h+1\).
It does not give a block of size \(D\); the growing degree contributes
to atomic polynomial degree instead. Both atomic degree and individual
coefficient bit length remain polynomial in \(N\).

[Khachiyan--Porkolab, printed pages 207--208, Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
allows arbitrary Boolean first-order formulas and gives an integer-witness
bound independent of the number of atoms. The feasibility reduction by an
additional integer coordinate fixed to zero is stated immediately before
the theorem. Thus the large Boolean matrix and finite grid do not spoil
the use made here. Only the witness bound is used; applying their
formula-size-dependent algorithm would not establish the claimed running
time.

The set to which the theorem is applied is convex because it is the real
projection of the original conic system. No convexity of the set in the
additional quantified variables is required. The resulting integer box
preserves existence. Substitution of its polynomial-bit integer points,
followed by the field small-point bound, supplies one continuous box
meeting every nonempty integer fiber in that integer box.

## 4. The gap belongs to the exact system

The maximum residual includes the squared cone rows, both signs of every
affine equality, the original affine inequalities, and the cone sign
residuals \(-t_i\). On the continuous box it is continuous and attains
its minimum. Its zero set is exactly the original boxed fiber.

The epigraph variable has zero Hessian block. A rational upper bound on
the residual maximum gives a compact nonempty epigraph system, so the
nonconvex boxed-value theorem applies with the original span \(h\).
Integer substitution has uniformly bounded input length, which gives
one gap \(\Delta\) for every boxed integer assignment without
enumerating them.

For the threshold corollary, this gap and the radius must be obtained
after the algebraic threshold row has been included. That is how the
draft uses them. A gap for the earlier system alone would not justify
rounding the new threshold.

An upper rational endpoint for the threshold enlarges its feasible set,
and produces residual at most \(\Delta/4\). The rational cone lift
with \(\varepsilon=\Delta/(12T^2)\) produces the same upper bound
for each squared cone residual. Thus any lifted integer fiber has minimum
residual strictly below \(\Delta\) and must have minimum zero. This
argument works at an irrational singleton and rejects an unattained
infimum threshold. It does not compare floating-point values for equality.

## 5. The outward rationalization estimates are correct

For the general field case, the scalar coefficient accuracy stated in the
draft bounds each affine-coordinate error by \(\eta/(d_*+1)\).
Summing absolute errors over at most \(d_*\) cone coordinates gives
the required vector error in \(\ell_1\), hence in \(\ell_2\).
The prescription also remains defined when there are no continuous
variables or a cone vector has dimension zero.

Using the shifted right side \(s=\widehat t+2\eta\) preserves every
original feasible point:

\[
 \|\widehat u\|\le\|u\|+\eta\le t+\eta
 \le\widehat t+2\eta=s.
\]

At the original apex, \(\|\widehat u\|\le\eta\) and
\(s\ge\eta\), so the inclusion also holds there. Relaxing affine
equalities to \(|\widehat e|\le\eta\) similarly preserves
irrational singleton witnesses.

Conversely, the lift gives \(s\ge0\) and
\(\|\widehat u\|\le(1+\varepsilon)s\). Since
\(|s-t|\le3\eta\), the original sign residual satisfies
\(-t\le3\eta\). No sign of the true \(t\) is needed for the
squared-error estimates:

\[
 \bigl|\|u\|^2-\|\widehat u\|^2\bigr|
       \le\eta(2T+\eta),\qquad
 |s^2-t^2|\le3\eta(2T+3\eta).
\]

Their sum is \(8T\eta+10\eta^2\le18T\eta\), because
\(\eta\le1\le T\). Also \(s\le T+3\eta\le4T\) and
\(\varepsilon\le1\), so

\[
 q\le48\varepsilon T^2+18T\eta
   =\frac{66}{256}\Delta<\frac12\Delta.
\]

The affine residuals are at most \(2\eta\), and the sign residuals
at most \(3\eta\); both are also strictly below \(\Delta/2\).
All displayed inequality directions and constants are valid. The
separate sign residual is essential: a shifted cone can admit a point
with negative true right side, even though a true cone cannot.

Rational coefficient approximation is polynomial in the requested
precision. For a coefficient polynomial \(g(X)=\sum a_jX^j\) and
\(H=\max(1,|a|,|b|)\), one can use

\[
 \sup_{X\in[a,b]}|g'(X)|
 \le\sum_{j\ge1}j|a_j|H^{j-1}.
\]

This bound has polynomial bit length; its magnitude need not be
polynomial. Review prompted replacement of the initial wording
“polynomial derivative bound” by this explicit bit-length statement.
The corrected passage and displayed derivative bound were reread and
are valid. No precision obstruction remains.

The rounded squared Hessians need not keep span \(h\). For example,
over \(\mathbb Q(\sqrt2)\), take
\(A_1=\operatorname{diag}(2,\sqrt2)\),
\(A_2=\operatorname{diag}(\sqrt2,1)\), and constant cone right
sides. The squared Hessians satisfy \(H_1=2H_2\). Replacing both
occurrences of \(\sqrt2\) by the same rational \(r\) gives a
flattened two-column minor \(16-4r^4\ne0\), so the rounded span is
two. The draft correctly avoids applying any span-dependent theorem to
that rounded system. The gap has already been proved for the exact data.

## 6. Final algorithm and limitations

The cone lift is rational, has polynomial size in cone dimension and
logarithmic inverse tolerance, and introduces only continuous variables.
The construction therefore ends with exactly the original \(k\) integer
variables. [Lenstra, Section 5, printed page 547](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf)
explicitly allows a growing number of continuous variables when the
integer dimension is fixed. No algorithm for MILP with algebraic
coefficients is assumed.

The feasibility theorem gives existence equivalence and a valid integer
assignment. It does not by itself recover an exact algebraic continuous
optimizer, preserve a continuous objective value in one MILP, prove a
uniform mixed-integer infimum encoding bound, or cover arbitrary separately
encoded algebraic coefficients. The attainment consequence is valid once
the exact finite value has already been supplied: adding the affine
threshold decides whether that value is attained.

The final draft adds a valid optimizer-recovery composition for rational
original data. If the threshold is the global finite infimum \(\theta\),
the returned integer assignment has a rational original continuous fiber
containing a point with objective at most \(\theta\). Every original
feasible point has objective at least \(\theta\), so this fiber has
attained optimum exactly \(\theta\). Substituting the polynomial-bit
integer assignment preserves rationality and Hessian span and leaves a
polynomial-length input. Applying
[the rational continuous optimization algorithm](continuous-socp-optimization.md)
to that original fiber recovers a full optimizer in the claimed time.
It need not send the algebraic threshold to that algorithm. This
additional conclusion depends on the separate optimizer-encoding and
recovery results stated in the continuous note, whose complete statement
and reduction were reread for this composition. It does not establish
analogous recovery for arbitrary common-field cone coefficients or recover
the unknown mixed-integer infimum.

The final prior-work paragraph was also checked against
[Khachiyan--Porkolab, printed pages 208--209](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf).
Their algebraic-polyhedron application already admits separately isolated
algebraic coefficients in fixed dimension. The draft accurately presents
the present contribution as the common-field extension with growing
continuous dimension and fixed Hessian span. It does not claim that a
common-field input representation is necessary for every possible
polynomial-time theorem about algebraic coefficients.

## 7. Targeted verification

An inline `python` command using `sympy` and `fractions.Fraction` checked
the field-norm annihilator \(v^4-2\), the exact and rounded Hessian
minors above, and 12 exact rational cases of the residual constants for
\(T\in\{1,3/2,17,2^{30}\}\) and
\(\Delta\in\{1,1/2,2^{-40}\}\). All passed. The rounding
reviewer separately ran exact rational checks of the constants. These
finite calculations support the displayed calculations; the inequalities
above supply their general proof.

A targeted inline Python check of this review's final newline, whitespace,
control characters, paired math delimiters, and local links was run,
together with `git diff --check --
research-20260927/algebraic-threshold-misocp-review.md`. Neither reported
errors. The review was untracked, so the Python check supplies the actual
saved-file integrity check independently of Git tracking. No project-wide
verification or CI inspection was performed.
