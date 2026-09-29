# Exact MISOCP feasibility with one algebraic threshold

Date: 2026-09-28. Status: proof extension and
[independent adversarial review](algebraic-threshold-misocp-review.md)
completed; no mathematical gap was found. The argument uses the reviewed
rational nonconvex algebraic bounds, their explicit elimination proof, and
the reviewed unbounded rational MISOCP reduction. It makes no priority claim.

A rational affine objective can be compared with an exactly represented real
algebraic threshold without losing polynomial-time feasibility at fixed
integer dimension and squared-Hessian span. In particular, if an exact finite
mixed-integer infimum has already been recovered with polynomial encoding
length, its attainment is decidable by one such threshold query. This does
not establish the required mixed-integer infimum encoding bound.

The proof also gives the following more general result: all affine cone data
may belong to one explicitly represented real number field. The field degree
is part of the input and need not be fixed. No algorithm for mixed-integer
linear programming with algebraic coefficients is assumed; the final MILP
has rational coefficients.

## 1. Input and result

Represent a real number field by

\[
 K=\mathbb Q(\alpha),\qquad p(\alpha)=0,\qquad a<\alpha<b,
                                                               \tag{1}
\]

where \(p\in\mathbb Z[T]\) is primitive and irreducible of degree
\(D\), and rational nonroot endpoints \(a,b\) isolate exactly one
real root. Every coefficient is given explicitly as a rational polynomial
in \(\alpha\), of degree below \(D\). The selected embedding is
used in all inequalities. Let \(N\ge2\) be the total binary input length,
including the dense polynomial \(p\), the isolator, and all coefficient
vectors. Thus \(D\le N\); a succinct degree encoding is excluded.

For \(w=(z,x)\in\mathbb Z^k\times\mathbb R^n\), consider affine
weak inequalities and equations over \(K\), together with

\[
 \|A_iw+b_i\|_2\le t_i(w):=c_i^Tw+d_i,\qquad i=1,\ldots,m.
                                                               \tag{2}
\]

Put

\[
 q_i(w)=\|A_iw+b_i\|_2^2-t_i(w)^2,\qquad
 h=\dim_K\operatorname{span}_K
       \{2(A_{ix}^TA_{ix}-c_{ix}c_{ix}^T):i\le m\}.             \tag{3}
\]

Always retain the affine signs \(t_i\ge0\). The dimension in (3)
equals the real matrix-span dimension at the selected embedding: rank is
determined by nonzero minors over \(K\). It need not equal the dimension
over \(\mathbb Q\) of these algebraic matrices. For example, \(H\)
and \(\sqrt2H\), with \(H\ne0\) rational, span one dimension over
\(\mathbb Q(\sqrt2)\) and two over \(\mathbb Q\).

**Common-field feasibility theorem.** For fixed \(k,h\), feasibility of
(2), with arbitrary affine rows and no supplied boxes, is decidable in
polynomial Turing time in \(N\). A feasible integer assignment can be
returned. No Slater condition, rational continuous witness, or closedness of
the projection onto \(z\) is required. The exponent may depend on
\(k,h\); no fixed-parameter running-time bound is asserted.

**Algebraic-threshold corollary.** If all original data are rational,
\(f(z,x)\) is rational affine, and \(\theta\) is given by a primitive
minimal polynomial and a rational real-root isolator, exact feasibility after
adding \(f(z,x)\le\theta\) has the same conclusion. The parameter
\(h\) is the original rational squared-Hessian span. Extension from
\(\mathbb Q\) to \(\mathbb Q(\theta)\) preserves the rank of a
rational matrix family, and the added affine row contributes no Hessian.

## 2. The algebraic radius and gap inputs extend to this field

We need two extensions of the rational results in the
[nonconvex certificate note](nonconvex-hessian-span-frontier.md):

1. A nonempty weak quadratic system over \(K\), with arbitrary affine
   rows and Hessian span at most \(h\) over \(K\), has a real feasible
   point whose coordinate magnitudes are at most \(2^{M^{C(h+1)}}\).
2. On a nonempty supplied rational box, the attained minimum of an arbitrary
   quadratic objective has a nonzero integer annihilator with degree and
   coefficient bit length at most \(M^{C(h+1)}\).

Here \(M\) is the explicit input length including the field and, in the
second assertion, the box and objective; \(C\) is an effective absolute
constant after enlarging the structural-size convention by a fixed polynomial.
Only these polynomial forms are used below. No sharp dependence on \(D\)
is required.

These assertions require a proof extension: the convex theorem stated in
[algebraic-coefficient-span-precision.md](algebraic-coefficient-span-precision.md)
cannot itself be applied to the indefinite squared cone rows. Its Section 3
finite-quotient lemma, however, is purely algebraic and already applies over
\(K\) without a convexity assumption. The following accounting combines
that lemma with the generic nonconvex argument.

### 2.1 Affine charts, perturbations, and real limits

Compute a Hessian basis over \(K\), introduce the \(h\) quadratic
coordinates, and retain every affine inequality in the lifted polyhedron.
Every active affine chart is over \(K\). Linear algebra has polynomial
encoding cost here: multiplication by a field element is a \(D\)-by-\(D\)
rational matrix in the power basis, so an invertible \(r\)-by-\(r\)
field system can be solved as an \(rD\)-dimensional rational system.
Determinant bounds control the output bits. Field basis extraction can use
ordinary exact rank tests and these same solves. This is elementary field
arithmetic, not algebraic-coefficient MILP.

The nonconvex genericity lemma is unchanged. Restricted arbitrary quadratics
still range over all quadratics on each chart. A nonzero bad-coefficient
polynomial over the selected embedding cannot vanish on every point of a
sufficiently large integer grid. The degree and chart-count bounds depend
on dimensions and degrees, not on coefficient magnitudes or rationality.
Thus there are integer perturbation coefficients with polynomial bit lengths
which work on every relevant chart for sufficiently small positive
perturbation parameter.

The real arguments also remain unchanged: a squared-norm perturbation gives
bounded feasible minimizers for the small-point result. For a supplied
continuous box, first append rational bounds on every lifted quadratic
coordinate using coefficient magnitude bounds of polynomial bit length.
The lifted polyhedron is then compact, giving convergent minimizing
subsequences for the boxed-value result. These facts
use only the selected real embedding. At the selected perturbed minimizers,
there are at most \(h\) active nonlinear bands, with independent gradients,
nonsingular multiplier Hessian, and nonsingular bordered KKT matrix. Degenerate
original systems, dependent affine rows, and zero-dimensional charts are all
covered by the same chart and perturbation argument. Zero-dimensional chart
points now belong to \(K\), instead of necessarily to \(\mathbb Q\).

### 2.2 Quantitative elimination over \(K\)

After stationarity eliminates the chart variables, the selected multiplier
system has \(s\le h\) variables, multiplier degrees \(a_0=M^{O(1)}\),
and coefficients in \(K\). The outputs are rational functions giving
coordinates or the objective value, along one sequence of nonsingular roots
with a finite selected real limit. The coefficients of all parameterized
polynomials are included in the coefficient norm, before any limit is taken.

Every encoded input field element has absolute logarithmic Weil height
\(M^{O(1)}\). Indeed, the root height of \(\alpha\) is controlled
by the coefficient bits of \(p\), and evaluating a degree-below-\(D\)
rational polynomial increases height by at most the sum of coefficient
heights, \(D\) times the root height, and an elementary logarithmic term.
There are only polynomially many initial coefficient positions.

Affine elimination and determinant substitution preserve a polynomial bound
on the joint coefficient height. At each archimedean place, use coefficient
\(\ell_1\)-norms; at finite places, use maximum coefficient norms. A
\(d\)-dimensional determinant has norm at most \(d!U^d\) at an
archimedean place and \(U^d\) at a finite place, where \(U\) bounds its
entry norms. The determinant and adjugate substitutions occur a fixed number
of times. Therefore the averaged logarithmic local norm \(E\) of the
reduced polynomial system is \(M^{O(1)}\), exactly as in Sections 2--5
of the field-precision note. Generic integer perturbations obey the same
bound. This estimate does not sum the heights of exponentially many expanded
monomials.

That note's algebraic lemma constructs a nonzero \(P\in K[v]\) with

\[
 \deg P\le L=(a_0+1)^s=M^{O(h+1)},\qquad
 H_{\rm aff}(\operatorname{coeff}P)
 \le L(a_0(s+1)+1)E+\log(L!)+L\log3=M^{O(h+1)}.               \tag{4}
\]

Coefficient extraction and the selected real limit give \(P(\beta)=0\)
for the chosen coordinate or value \(\beta\). This step needs no
optimization property at the other embeddings. If \(W\) denotes the
height bound in (4), the elementary field-height argument gives

\[
 [\mathbb Q(\beta):\mathbb Q]\le DL,\qquad
 h_{\rm W}(\beta)\le W+\log2,
\]
\[
 \log\|p_\beta\|_\infty\le DL(W+2\log2)=M^{O(h+1)},         \tag{5}
\]

for its primitive integer minimal polynomial. Equivalently, taking the
field norm of a nonzero polynomial over \(K\) gives a nonzero rational
annihilator; no conjugate factor is the zero polynomial. The local-height
bound (5) supplies the necessary coefficient control without constructing
a normal closure.

Cauchy's upper root bound proves assertion 1. For a positive value, remove
initial zero coefficients from its integer annihilator and apply Cauchy's
bound to the reciprocal polynomial. This gives

\[
                    \beta=0\quad\hbox{or}\quad
                    |\beta|\ge2^{-M^{C'(h+1)}}.               \tag{6}
\]

This proves the boxed positive-gap assertion as well. The proof is an
encoding and magnitude argument; it does not enumerate the affine charts,
construct the perturbation grid, or solve a nonconvex optimization problem.

## 3. A small integer witness with one field-generator variable

Let \(Y\subseteq\mathbb R^k\) be the real projection of the original
conic feasible set. It is convex, and it can be nonclosed. The construction
in Sections 2.1--2.5 of the
[unbounded MISOCP note](unbounded-misocp-frontier.md) works with coefficients
in \(K\): lift the Hessian span, include every rank chart, use a finite
integer perturbation grid, eliminate chart variables by stationarity, and
require one uniform radius while the perturbation tends to zero. It gives
an exact formula over the selected field with block sizes

\[
                 \exists R\quad\forall\delta\quad
                 \exists(\varepsilon,\lambda_1,\ldots,\lambda_h).
                                                               \tag{7}
\]

Each atom has polynomial degree and polynomial coefficient bit length in
the explicit power-basis representation. This follows from polynomial-size
determinants over \(K\) and a fixed number of substitutions. The Boolean
matrix may be exponentially large. That size is immaterial to the witness
bound, and the formula is not constructed by the feasibility algorithm.

Replace every field coefficient by its polynomial in a new variable \(t\)
and conjoin \(p(t)=0\), \(a<t<b\). Positive rational common
denominators clear the atoms without changing inequality directions. Field
arithmetic is reduced modulo \(p\) before this replacement. The chart
and stationarity denominators have already been guarded and cleared by even
powers, as in the rational projection proof; only rational coefficient
denominators remain in this step. Thus each
resulting atom is an integer polynomial, of degree and coefficient bit length
\(N^{O(1)}\), including when \(D\) grows. Place \(t\) in the
first existential block, obtaining block sizes

\[
                              2,\quad1,\quad h+1.             \tag{8}
\]

The isolator forces the one intended embedding, so the resulting formula
defines exactly \(Y\). The fixed radius remains outside the universal
quantifier. It therefore excludes continuous witnesses escaping to infinity
as the perturbation shrinks; the construction does not replace \(Y\)
by its closure.

[Khachiyan--Porkolab, Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
bounds the integer witness length for a convex first-order set by the atomic
coefficient length times the atomic degree raised to an exponent depending
on the free integer dimension and the quantified block dimensions. The
number of atomic predicates does not enter that bound. Applying it to (8),
with one extra integer coordinate fixed to zero as in their feasibility
reduction, gives an effective bound

\[
 Y\cap\mathbb Z^k\ne\varnothing\ \Longrightarrow\quad
 \exists z^*\in Y\cap\mathbb Z^k:\quad
 \log_2(2+\|z^*\|_\infty)\le N^{C(h+1)(k+1)^4}.             \tag{9}
\]

Only this witness theorem is used, not its formula-size-dependent algorithm.
Choose the resulting rational integer box. It preserves existence, rather
than every feasible integer assignment outside the box. When \(k=0\),
this step is unnecessary.

For every integer assignment in that box, substitution gives a quadratic
system over the same field with uniformly polynomial input length for fixed
\(k,h\). Assertion 1 in Section 2 supplies a rational continuous box
meeting every nonempty fiber in the integer box. The boxes can be enlarged
to symmetric bounds \([-Z,Z]^k\) and \([-R,R]^n\), with \(Z,R\ge1\),
whose endpoint bit lengths are polynomial for fixed \(k,h\). No integer
assignment or continuous fiber is enumerated to choose them.

## 4. Uniform gap on the boxes

For each boxed integer \(z\), define

\[
 \gamma_z=\min_{x\in[-R,R]^n}
 \max\{0,\ q_i(z,x),\ -t_i(z,x),\ \ell_j(z,x),
                                    e_j(z,x),\ -e_j(z,x)\},   \tag{10}
\]

where \(\ell_j\le0\) are the original affine inequalities and
\(e_j=0\) the affine equations. The maximum includes every scalar row.
Compactness gives an attained minimum, and \(\gamma_z=0\) exactly
when the original boxed fiber is feasible.

An epigraph variable for (10) adds no Hessian direction. A rational upper
bound on its value, obtained from absolute coefficient and box bounds, makes
the epigraph domain compact and nonempty. Section 2 then gives one effective
rational number

\[
 \Delta=2^{-B}\le1,\qquad B=N^{C_{k,h}},\qquad
                     \gamma_z=0\ \hbox{or}\ \gamma_z\ge\Delta,
                                                               \tag{11}
\]

uniformly over the boxed integer assignments. Composing radius and gap bounds
can increase \(C_{k,h}\). The proof needs only polynomial time for fixed
\(k,h\), and makes no sharper exponent claim.

## 5. The short reduction for one algebraic threshold

Suppose all cone maps and affine rows are rational except the added row
\(f(w)-\theta\le0\). Refine the isolating interval for \(\theta\)
to obtain a rational upper endpoint \(\widehat\theta\) with

\[
                   0\le\widehat\theta-\theta\le\Delta/4.    \tag{12}
\]

Its construction and bit length are polynomial in the field representation
and \(B\), by univariate real-root isolation and bisection. Retain every
other affine row exactly, and replace the threshold by
\(f(w)\le\widehat\theta\).

Let \(T\ge1\) be a rational bound for every \(|t_i(w)|\) on the
boxes. Use the rational Lorentz-cone lift from the
[SOCP feasibility proof](socp-hessian-span-frontier.md#4-rational-polyhedral-cone-approximation)
with tolerance \(\varepsilon=\Delta/(12T^2)\), retaining the signs
\(t_i\ge0\). Every original feasible point lifts. Every lifted point
satisfies

\[
 q_i(w)\le3\varepsilon T^2=\Delta/4,\qquad
                       f(w)-\theta\le\Delta/4.               \tag{13}
\]

Consequently an integral lifted assignment has \(\gamma_z\le\Delta/4\),
which by (11) forces \(\gamma_z=0\). The resulting rational MILP has
exactly the original feasible integer assignments within the chosen boxes,
and has only the original \(k\) integer variables. Its displayed
continuous point need not be feasible for the original system.

This proves the threshold corollary using the ordinary rational cone lift.
In particular, the algebraic threshold is never replaced by a merely numerical
equality test, and the proof remains valid at an irrational singleton or an
unattained finite objective threshold.

## 6. Rationalizing all affine cone data

For the full common-field theorem, rational approximation must also relax
the affine rows and cone maps outward. Here are explicit error estimates.
Choose a rational \(T\ge1\) bounding \(\|A_iw+b_i\|_2\) and
\(|t_i(w)|\) throughout the boxes. Absolute coefficient bounds and the
vector \(\ell_1\)-norm suffice; no square roots are needed. Set

\[
                 \eta=\frac{\Delta}{256T},\qquad
                 \varepsilon=\frac{\Delta}{256T^2}.           \tag{14}
\]

Approximate coefficients rationally so that, uniformly on the boxes,

\[
 \|u_i(w)-\widehat u_i(w)\|_2\le\eta,\quad
 |t_i(w)-\widehat t_i(w)|\le\eta,\quad
 |\ell_j(w)-\widehat\ell_j(w)|\le\eta,\quad
 |e_j(w)-\widehat e_j(w)|\le\eta.                              \tag{15}
\]

For example, if \(r=k+n\), \(V=\max(Z,R,1)\), and \(d_*\)
bounds all cone-vector dimensions and one, scalar coefficient error at most
\(\eta/((r+1)V(d_*+1))\) suffices. Approximating the isolated root
\(\alpha\), then evaluating its coefficient polynomials with interval
bounds, gives (15) in polynomial time in the input and requested precision.
An explicit derivative-magnitude bound with polynomial bit length on the
original isolating interval controls the needed root precision. For a
coefficient polynomial \(P(t)=\sum_j a_jt^j\), one can use
\(\sum_{j\ge1}j|a_j|H^{j-1}\), where
\(H=\max(1,|a|,|b|)\). Its magnitude can be exponential, but its
bit length and the required number of root-precision bits are polynomial
for fixed \(k,h\).

Use rational affine rows

\[
              \widehat\ell_j\le\eta,\qquad
              -\eta\le\widehat e_j\le\eta,                   \tag{16}
\]

and the rational cone lift applied to

\[
                     (\widehat u_i,s_i),\qquad
                     s_i=\widehat t_i+2\eta.                 \tag{17}
\]

Retain the rational boxes exactly. The lift implies \(s_i\ge0\) and
\(\|\widehat u_i\|_2\le(1+\varepsilon)s_i\). For a true feasible
point, (15) gives
\(\|\widehat u_i\|_2\le\|u_i\|_2+\eta\le\widehat t_i+2\eta=s_i\),
so that point has a lift, including at the cone apex.

Conversely, a lifted point has original affine residuals at most \(2\eta\),
and \(-t_i\le3\eta\). Since \(\eta\le1\), \(T\ge1\), and
\(|s_i-t_i|\le3\eta\), its squared residual obeys

\[
 \begin{split}
 q_i
 &\le \bigl(\|\widehat u_i\|_2^2-s_i^2\bigr)
       +\eta(2T+\eta)+3\eta(2T+3\eta)\\
 &\le3\varepsilon(T+3\eta)^2+18T\eta\\
 &\le48\varepsilon T^2+18T\eta
   =\frac{66}{256}\Delta<\Delta/2.                            \tag{18}
 \end{split}
\]

The first line uses absolute errors of squared norms and squared right sides;
it assumes no sign for the true \(t_i\). The explicit sign residual bound
is therefore necessary. All residuals in (10) are below \(\Delta/2\).
For integral \(z\), (11) forces an exact original feasible fiber.

The construction is a rational MILP of polynomial length for fixed \(k,h\)
and introduces no integer variables. Classical rational mixed-integer linear
feasibility with fixed integer dimension therefore decides it and returns
\(z\); the allowance of arbitrarily many continuous variables is explicit
in [Lenstra (1983), Section 5](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf).
This proves the common-field theorem.

The rationalized squared Hessians need not retain span \(h\). This causes
no problem: the algebraic radius and gap are proved for the original exact
system, and the rationalized data are used only in the final polyhedral lift.
No span-dependent theorem is applied to the approximated system.

## 7. Consequences and boundaries

If \(\theta=\inf\{f(z,x):(z,x)\text{ originally feasible}\}\) is
finite and known exactly, then

\[
 \theta\text{ is attained}\quad\Longleftrightarrow\quad
       \exists(z,x)\text{ feasible with }f(z,x)\le\theta.      \tag{19}
\]

For rational affine \(f\), the threshold theorem decides (19) in time
polynomial in the original input plus the exact encoding of \(\theta\),
for fixed \(k,h\). If that encoding has polynomial length, this is a
polynomial-time attainment decision relative to the original input. It does
not require a separate minimum-norm optimizer encoding theorem.

For rational original data, a feasible integer vector returned by this
threshold query has an attained continuous fiber optimum equal to
\(\theta\): it contains a point with \(f\le\theta\), and no
original feasible point has \(f<\theta\). The
[rational continuous optimization algorithm](continuous-socp-optimization.md)
can therefore recover a full algebraic optimizer on that fiber. This
additional recovery conclusion uses that algorithm's separately reviewed
optimizer-encoding input. It needs no optimizer algorithm with algebraic
cone coefficients, and its running time is polynomial in the original input
plus the encoding of \(\theta\), for fixed \(k,h\).

The [continuous optimization note](continuous-socp-optimization.md) avoids
algebraic cone-oracle inputs by compact objective comparisons and an optimizer
radius. The present route instead extends feasibility itself. These are two
sufficient approaches to attainment; the threshold route does not establish
mixed-integer value recovery or a uniform optimizer bound in original input
length before the value has been encoded.

The common-field representation is material. Separate algebraic coefficient
encodings can generate a compositum of exponential degree; this proof gives
no polynomial bound in that different input model. It also does not cover
transcendental constants, succinct high-degree field encodings, strict cone
constraints, arbitrary nonconvex quadratic decision, or a fixed \(h\) with
unrestricted integer dimension. Algebraic coefficient affine systems at
\(h=0\), zero-dimensional fibers, and empty or lower-dimensional conic
sets are included.

No exact algebraic MILP algorithm, rational feasible-point promise, or
continuity of integer projections is used. The output integer assignment
has an exact continuous witness, but the MILP's continuous assignment may
violate the original conic rows. The result is a complexity proof, not an
implemented solver or a practical precision estimate.

## 8. Prior results and what this extension adds

Khachiyan--Porkolab already treat algebraic input coefficients explicitly:
their discussion of algebraic polyhedra on printed pages 208--209 permits
separately isolated algebraic coefficients in fixed total dimension. Thus
handling algebraic coefficients, selecting their real embeddings, and
extending integer feasibility beyond rational polyhedra are established
ideas. Their general theorem also applies directly to the present conic
input when the total dimension is fixed. Here the continuous dimension can
grow; the small Hessian span supplies the compressed projection formula,
and the uniform positive gap permits a polynomial-size rational MILP.
The common-field input assumption is an assumption of this proof, not a
necessity theorem about all algebraic input models.

The rational outer approximation itself is inherited from
[Kocuk's construction and its source audit](socp-rational-lift-source.md).
The number-field height estimates use established local-height arithmetic,
as compared with Krick--Pardo--Sombra and Silverman in the
[field-precision note](algebraic-coefficient-span-precision.md#7-sources-and-verification-limits).
The additional work here is checking that the nonconvex radius and gap
proofs extend to one explicitly represented field, and that rounding all
affine cone maps outward preserves exact integer feasibility after applying
that gap. This is a technical extension of the rational theorem. No claim
of a new general algebraic optimization method or historical priority is
made. Searches for exact conic feasibility with algebraic coefficients did
not identify an equivalent theorem with this Hessian-span parameter; that
search outcome does not establish novelty.

## 9. Verification record

The primary text of Khachiyan--Porkolab was checked at printed pages 207--208
for its arbitrary Boolean formula model, size-independent witness bound, and
feasibility reduction. The Lenstra primary text was opened for the rational
mixed-integer algorithm. The substantive algebraic and conic ingredients
are linked where used; this note adds the field-coefficient extension,
field-generator quantifier, and outward rationalization estimates.

A targeted inline `python` command using `fractions.Fraction` checked the
displayed residual identities and constants at 36 pairs of rational
\((T,\Delta)\), and checked 4,212 scalar boundary cases of the rounded
cone inclusion, including negative true right sides near the apex. All
passed. These are exact illustrative checks; the norm inequalities in
Section 6, not the finite sample, establish the bound in every dimension.
A second targeted inline `python` command checked this note's final newline,
trailing whitespace, control characters, paired math delimiters, and all
nine local Markdown links. Those checks passed. Neither command checks
the universal algebraic elimination theorem. No Lean formalization,
project-wide verification, or CI inspection was performed.
