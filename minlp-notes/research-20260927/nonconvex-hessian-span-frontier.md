# Algebraic certificates for nonconvex systems with few Hessian directions

Date: 2026-09-27. Status: proof and two adversarial reviews completed; no
mathematical gap was found. A subsequent prior-work audit found a shorter
proof of the feasibility result from classical quadratic-map sampling.
The value argument remains separate. Novelty has not been established.

The main developed argument controls exact quadratic optimum encodings
without convexity. The feasibility-certificate bound is a simpler corollary
of Grigoriev--Pasechnik's established sampling theorem and an elementary
polyhedral-face argument, given in Section 3.1. It should not be presented
as a new general algebraic-certificate technique. Both statements separate
the size of exact descriptions from the difficulty of finding them: one
nonconvex quadratic inequality with affine rows can encode an NP-hard
problem. No polynomial-time solution algorithm is proposed.

## 1. Theorems

Let

\[
 S=\{x\in\mathbb R^n:Ax\le b,\ Ex=e,\ q_i(x)\le0
                \ (i=1,\ldots,m)\},\qquad
 q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
\]

with rational data of total explicit binary length \(N\ge2\). The
symmetric Hessians \(Q_i\) need not be positive semidefinite. Put

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

**Feasibility corollary of Grigoriev--Pasechnik.** If \(S\ne\varnothing\), there is
an exactly feasible real algebraic point whose coordinates lie in one number
field of degree \(N^{O(h+1)}\), and which has a rational univariate
representation of total binary length \(N^{O(h+1)}\). No input bounds or
constraint qualification are required. Consequently exact feasibility is
in NP for every fixed \(h\), and a feasible point exists with magnitude
at most \(2^{N^{O(h+1)}}\).

Here a rational univariate representation consists of a nonzero squarefree
integer polynomial \(f\), a rational interval isolating one real root
\(\alpha\), and rational polynomials expressing every coordinate as a
polynomial in \(\alpha\). The proposed conclusion is an existence and
certificate-size bound, not a deterministic method for finding the point.

**Bounded-value theorem.** If an explicit finite rational box is
also supplied, the global minimum of an arbitrary rational quadratic
objective over nonempty \(S\) has an integer annihilator of degree and
coefficient bit lengths \(N^{O(h+1)}\). The objective Hessian is excluded
from \(h\). An optimal point can be chosen with a common algebraic
description of this same size. This second statement relies on compactness;
it is not an unbounded finite-infimum theorem.

## 2. Why the convex proof cannot simply be copied

At a minimum-norm feasible point, deleting inactive constraints preserves a
local minimum but need not preserve a global minimum. For example, consider

\[
 4(x-2)^2+y^2=4,\qquad x\ge5/2.
\]

The equality is represented by two opposite quadratic inequalities, whose
Hessians span dimension one. The minimum norm on the retained ellipse cap
is attained at \((3,0)\), with squared norm nine; its affine inequality is
inactive there. After deleting that inequality, \((1,0)\) is feasible
with squared norm one. The ellipse is connected. Therefore choosing an
arbitrary sample point on the active variety, or on its connected component,
does not preserve feasibility for the deleted rows.

The construction below keeps every original affine inequality throughout.
It introduces a small number of quadratic equations globally, rather than
deleting inactive nonlinear rows at the outset.
The counterexample does not refute the minimum-dimensional face argument
in Section 3.1; that argument selects a different face for a different reason.

## 3. Lift the matrix span into a few quadratic equations

Choose a rational Hessian basis \(B_1,\ldots,B_h\) and rational
coefficients \(c_{ij}\) such that \(Q_i=\sum_jc_{ij}B_j\). Define

\[
 y_j=\tfrac12x^TB_jx\quad(j=1,\ldots,h),\qquad w=(x,y).
\]

The original system is equivalent to

\[
 w\in P,\qquad F_j(w):=\tfrac12x^TB_jx-y_j=0
                                      \quad(j=1,\ldots,h),       \tag{1}
\]

where \(P\) is the rational polyhedron defined by all original affine
rows and the affine inequalities

\[
 \sum_jc_{ij}y_j+a_i^Tx+c_i\le0.
\]

The lift has polynomial encoding length in \(N\), by rational linear
algebra and determinant bounds. Its dimension is \(n+h\); it uses
exactly \(h\) quadratic equations. If \(h=0\), the original system
is affine and the conclusion is classical. Assume \(h\ge1\).

### 3.1 The shorter established route to a feasible certificate

Let \(V=\{w:F_j(w)=0\ (1\le j\le h)\}\). Among the nonempty
faces of \(P\) meeting \(V\), choose a face \(F\) of minimum
dimension; \(P\) itself is allowed. Every point of
\(\operatorname{relbd}F\) lies in a proper face of \(F\), which is
also a face of \(P\). Thus

\[
 V\cap\operatorname{relbd}F=\varnothing.
\]

Choose a connected component \(C\) of \(V\cap\operatorname{aff}F\)
meeting \(F\). Its intersection with \(F\) is nonempty and closed
in \(C\), and it equals \(C\cap\operatorname{relint}F\), which is
open in \(C\). Hence \(C\subseteq F\). This argument also applies
to unbounded polyhedra and polyhedra with lineality.

A rational chart for \(\operatorname{aff}F\) has polynomial-bit
coefficients. Apply
[Grigoriev--Pasechnik, Theorem 1.2](https://arxiv.org/pdf/cs/0403008v3),
to the \(h\) restricted quadratic equations and the outer polynomial
\(p(Y)=\sum_jY_j^2\). Its real univariate samples meet every connected
component; one therefore belongs to \(C\) and is feasible for \(P\).
The theorem's degree and coefficient bounds give total representation
length \(N^{O(h+1)}\). Univariate denominator inversion and real-root
isolation give the representation used here. No minimum face needs to be
found or certified by an NP verifier: the final algebraic point is checked
against all original rows.

This proves the feasibility corollary and its small-radius consequence.
The [prior-work audit](nonconvex-hessian-span-prior-audit.md) records the
source statement, representation conversion, and independent checks. It
found mathematical subsumption by established sampling plus this short
face lemma, without finding a publication stating the exact corollary.
Those facts do not justify a substantial originality claim for feasibility.

The remaining perturbation proof is retained as an alternative feasible-point
proof and as the foundation for the bounded-value result and its
[finite-infimum extension](nonconvex-finite-infimum.md). The minimum-face
argument alone does not preserve a prescribed optimum: its boundary may
contain feasible points with larger objective values.

## 4. A quantitative genericity lemma

The needed lemma concerns quadratic optimization on a fixed affine space,
over the complex numbers for its algebraic assertions.

Fix \(d\ge1\) and \(s\le d\), and let \(r,f_1,\ldots,f_s\)
be quadratic polynomials in \(u\in\mathbb C^d\), with all coefficients
allowed to vary independently. Let \(p\) be the number of these
coefficients. For generic coefficient tuples:

1. every point with \(f_i(u)=0\) has linearly independent gradients
   \(\nabla f_i(u)\);
2. every KKT solution
   \(f_i(u)=0\),
   \(\nabla r(u)+\sum_i\lambda_i\nabla f_i(u)=0\)
   has both an invertible multiplier Hessian
   \(M=\nabla^2r+\sum_i\lambda_i\nabla^2f_i\) and an invertible
   bordered KKT matrix
   \(\begin{pmatrix}M&G^T\\G&0\end{pmatrix}\),
   where \(G\) has rows \(\nabla f_i(u)^T\).

For \(s>d\), generic quadratics have no common zero. The bad coefficient
tuples in each statement lie in a proper algebraic hypersurface which can
be chosen with degree \(2^{\operatorname{poly}(d+s)}\). The polynomial
in this last expression is absolute. No coefficient-height bound for that
hypersurface is needed below.

### 4.1 Properness of the bad sets

For gradient dependence, fixing \(u\) leaves the values \(f_i(u)\)
and gradients \(\nabla f_i(u)\) as independent affine-linear functions
of the polynomial coefficients. Vanishing of all values has codimension
\(s\). Rank deficiency of an \(s\)-by-\(d\) matrix has codimension
\(d-s+1\). Thus the incidence of a common zero with dependent gradients
has dimension at most \(p+d-s-(d-s+1)=p-1\). Its projection onto
coefficient space is contained in a proper algebraic subset. If \(s>d\),
the common-zero incidence alone has dimension at most \(p+d-s<p\).

For the KKT assertions, consider the incidence in variables
\((u,\lambda,\text{coefficients})\). Solve its \(s\) value equations
for the constant terms of the \(f_i\), and its \(d\) stationarity
equations for the linear coefficients of \(r\). This parameterizes the
incidence as an affine space, of dimension exactly \(p\). In particular,
it is irreducible. Neither determinant vanishes identically on it: use

\[
 f_i(u)=u_i^2-1\quad(i\le s),\qquad
 r(u)=\sum_{j=1}^du_j^2+\sum_{i=1}^su_i.
\]

At \(u_i=\pm1\) for \(i\le s\), \(u_j=0\) otherwise, take
\(\lambda_i=-1-1/(2u_i)\). Then \(M\) is diagonal, with entries
\(-1/u_i\) in the first \(s\) positions and 2 elsewhere. The gradient
rows are \(2u_ie_i^T\), so \(GM^{-1}G^T\) is diagonal and
invertible. Both determinants are nonzero. Each determinant-zero incidence
therefore has dimension at most \(p-1\), as does the closure of its
coefficient projection.

### 4.2 Effective degree and small integer choices

All these incidences admit descriptions in polynomially many variables by
polynomially many equations of degree \(O(d+s+1)\). To avoid using the
possibly exponential list of gradient minors, cover the dependent-gradient
incidence by \(s\) charts: introduce a nonzero dependence vector
\(\mu\), normalize one of its entries to one, and impose
\(\sum_i\mu_i\nabla f_i=0\) together with \(f_i=0\). Each chart
has \(s+d+1\) equations of degree at most three. The KKT bad incidences
use the value and stationarity equations together with one determinant.

Use cumulative geometric degree: the sum of the degrees of **all**
irreducible components, including components of lower dimension. Repeated
affine Bezout gives a bound \(2^{\operatorname{poly}(d+s)}\) for these
incidences, and linear projection does not increase the cumulative degree
of the image closure. Each proper irreducible image component is contained
in a hypersurface of degree at most its own degree. Multiplying the defining
polynomials for these hypersurfaces covers every image component with total
degree at most the cumulative degree. These facts give the stated
single-exponential bound; no sharp discriminant formula is needed.

The degree convention, projection inequality, and affine Bezout inequality
are stated in Krick--Pardo--Sombra,
[*Sharp estimates for the arithmetic Nullstellensatz*](https://mate.dm.uba.ar/~krick/KrPaSo01.pdf),
Section 1.2.1. The containing-hypersurface fact and projection bound are also
used explicitly in the proof of Proposition 5 of Ovchinnikov--Pogudin--Vo,
[*Bounds for elimination of unknowns in systems of differential-algebraic equations*](https://par.nsf.gov/servlets/purl/10251735),
citing Heintz (1983), Lemma 2 and Proposition 3. These primary texts were
inspected for the degree facts, independently of the present genericity
argument.

Apply the lemma to every nonempty affine space obtained by making a subset
of the rows of \(P\) equalities, and to every oriented subset of the
\(h\) equations in (1). There are at most \(2^{\operatorname{poly}(N)}\)
choices. Each such affine space has a rational chart with polynomial
coefficient bit lengths. Restricting an arbitrary quadratic polynomial in
\(w\) to one chart is surjective onto all quadratics in its free variables.

Choose quadratic polynomials \(P_0,P_1,\ldots,P_h\) in \(w\), and
consider the parameter path

\[
 r_\varepsilon(w)=\|w\|_2^2+\varepsilon P_0(w),\qquad
 f_{j,\sigma,\varepsilon}(w)
   =\sigma\bigl(F_j(w)+\varepsilon^2P_j(w)\bigr)-\varepsilon,
 \quad\sigma\in\{-1,1\}.                              \tag{2}
\]

For every fixed nonzero \(\varepsilon\), the coefficient map from
the selected \(P_j\) and \(P_0\) onto the restricted objective and
selected constraint quadratics is surjective. Thus substituting (2) into
each bad polynomial gives a nonzero polynomial in
\((\varepsilon,\text{coefficients of the }P_j)\).
Select one nonzero coefficient in its expansion in \(\varepsilon\).
Avoiding the resulting polynomial ensures that the bad condition does not
hold identically along the path.

The product of these finitely many selected coefficient polynomials is
nonzero and has degree at most \(2^{\operatorname{poly}(N)}\). A nonzero
polynomial of total degree at most \(D\) cannot vanish on the entire
integer grid \(\{0,\ldots,D\}^p\); this follows by induction on the
number of variables. Hence the \(P_j\) can be chosen with integer
coefficients of polynomial bit length in \(N\), simultaneously for all
charts and all oriented subsets. This is an existence argument; the product
and grid need not be constructed by a verifier.

For such a choice, only finitely many nonzero real \(\varepsilon\)
are bad for any one chart and subset, and there are finitely many choices.
All the generic conclusions therefore hold for every sufficiently small
positive \(\varepsilon\).

The case of a zero-dimensional chart is direct: its point is rational with
polynomial bit length. In charts with positive dimension, at most \(d\)
nonlinear rows can be active, by the \(s>d\) clause of the lemma.

## 5. Feasible perturbations and a bounded sequence

Minimize \(r_\varepsilon\) subject to

\[
 w\in P,\qquad
 |F_j(w)+\varepsilon^2P_j(w)|\le\varepsilon
                                       \quad(j=1,\ldots,h).     \tag{3}
\]

Fix any original feasible point \(\bar w\). It remains feasible in
(3) for every sufficiently small positive \(\varepsilon\), since
\(F_j(\bar w)=0\) and \(\varepsilon^2|P_j(\bar w)|\le\varepsilon\)
eventually. The same chosen perturbation polynomials work for all instances
of \(\varepsilon\) along this tail.

For sufficiently small \(\varepsilon\), the Hessian of
\(r_\varepsilon\) is uniformly positive definite. Its quadratic part
dominates a positive multiple of \(\|w\|_2^2\), and its linear and
constant coefficients are uniformly bounded. It is therefore uniformly
coercive. The nonempty closed feasible set in (3) has a global minimizer
\(w_\varepsilon\). Comparing its objective with
\(r_\varepsilon(\bar w)\) bounds all such minimizers in one compact
set. The bound can depend on the unknown \(\bar w\); its existence is
enough, and it is not inserted into any coefficient.

Choose \(\varepsilon\downarrow0\) so that \(w_\varepsilon\to w^*\)
along a subsequence. Every affine row remains satisfied. Boundedness and
continuity in (3) give \(F_j(w^*)=0\), hence \(w^*\) is feasible
for (1). This argument does not claim that the sequence or its cluster
point is unique.

## 6. Few multiplier variables control one common limit

At each \(w_\varepsilon\), make every active polyhedral row an equality
and take a rational chart of that affine space. The point is in the relative
interior with respect to all the other affine inequalities. The minimizer
is therefore a local minimizer of the nonlinear problem in that chart;
inactive affine rows can be omitted for this local KKT assertion only.
If a zero-dimensional chart occurs along an infinite subsequence, its one
rational point is constant there and is the required feasible limit.
Otherwise retain a subsequence whose charts have positive dimension.

Only one orientation of any band in (3) can be active, since its two
boundaries differ by \(2\varepsilon>0\). Thus there are at most
\(h\) active nonlinear rows. Genericity gives independence of their
gradients in the chart, so KKT holds with ordinary objective multiplier one.
The multiplier Hessian and bordered KKT matrix are nonsingular. Pass to a
further subsequence with one fixed chart and one fixed oriented active subset
\(J\), of size \(s\le h\), while preserving the same primal limit.

Write all restricted quadratics with their polynomial dependence on
\(\varepsilon\). Stationarity is

\[
 M(\varepsilon,\lambda)u=-a_0(\varepsilon)
                    -\sum_{i\in J}\lambda_i a_i(\varepsilon).
\]

With \(\Delta=\det M\ne0\) and the adjugate numerator \(p\), one
has \(u=p/\Delta\). Substituting into each selected active equality and
multiplying by \(\Delta^2\) gives \(s\) polynomials

\[
 H_i(\varepsilon,\lambda)=0\quad(i\in J).             \tag{4}
\]

Their degree in \(\lambda\) is \(O(d+1)\), their degree in
\(\varepsilon\) is \(O(d+1)\), and their coefficient bit lengths
are polynomial in \(N\). Rational affine substitution, adjugate expansions,
and one common denominator give these bounds exactly as in the convex
Hessian-span proof. The generic perturbation coefficients also have
polynomial bit length by Section 4.

At the selected roots, differentiating the reconstructed active equalities
with respect to \(\lambda\) gives

\[
 \frac{\partial H}{\partial\lambda}
       =-\Delta^2 GM^{-1}G^T,                          \tag{5}
\]

where \(G\) is the active-gradient matrix. This matrix is nonsingular by the
Schur complement of the bordered KKT matrix. Positive definiteness is not
used in (5).

Apply the [finite-quotient elimination lemma](explicit-span-separation.md),
Section 2, to (4). That lemma requires a sequence of nonsingular roots and
finite limits of rational outputs; it does not require convexity or bounded
multipliers. Every coordinate of \(w_\varepsilon\) is a rational output
with numerator and denominator degree \(O(d+1)\) in the multipliers.
It follows that each coordinate of the one common limit \(w^*\) has an
integer annihilator of degree and coefficient bit length \(N^{O(h+1)}\).

The lemma's common-field argument is essential: every rational linear
combination of these coordinates is a rational output along the same roots,
with the same degree bound. The primitive element theorem then gives

\[
 [\mathbb Q(w^*):\mathbb Q]\le N^{O(h+1)}.             \tag{6}
\]

The conclusion would not follow from multiplying separate coordinate-degree
bounds. The affine charts, selected multipliers, and perturbation coefficients
need not be part of the final feasibility certificate.

## 7. A short common algebraic certificate

For completeness, the coordinate and common-field bounds imply a short
rational univariate representation. Let \(D\) bound the common field
degree and \(H\) the coefficient bit lengths of all coordinate minimal
polynomials. Both are \(N^{O(h+1)}\), using the elementary factor bound
to pass from annihilators to minimal polynomials.

Among integer combinations \(\alpha=\sum_jt_jw_j^*\), coefficients
\(t_j\in\{0,\ldots,D(D-1)/2\}\) suffice to find a primitive element.
Indeed, distinct embeddings coincide on a combination only on one proper
linear hyperplane; the product over all pairs has degree at most
\(D(D-1)/2\), and the grid argument applies. Its minimal polynomial has
coefficient bit length \(N^{O(h+1)}\), by applying the same output
elimination lemma to this bounded-coefficient combination.

Here is an elementary size bound for expressing \(w_j^*\) in the power
basis of \(\alpha\). Multiply \(\alpha\) and \(w_j^*\) by the
leading coefficients of their primitive minimal polynomials, obtaining
algebraic integers \(A\) and \(B\). The leading coefficients have
\(\operatorname{poly}(D,H)\) bit length, and their scaled algebraic
integers' conjugate magnitudes are at most
\(2^{\operatorname{poly}(D,H)}\), by Cauchy's bound. Write
\(B=\sum_{r=0}^{D_0-1}c_r A^r\), where
\(D_0=[\mathbb Q(\alpha):\mathbb Q]\le D\).

Taking traces after multiplication by \(A^s\), \(0\le s<D_0\),
gives an integer linear system. Its coefficient matrix has entries
\(\operatorname{Tr}(A^{r+s})\), and its right-hand side has entries
\(\operatorname{Tr}(BA^s)\). The trace matrix is nonsingular because
the field extension is separable and \(1,A,\ldots,A^{D_0-1}\) is a
basis. Cramer's rule bounds numerator and denominator bit lengths of the
\(c_r\) by \(\operatorname{poly}(D,H)\). Scaling back gives each
coordinate as a rational polynomial in \(\alpha\) of that size.

A rational isolating interval for the intended real root of the primitive
polynomial has \(\operatorname{poly}(D,H)\) bit length, by the usual
discriminant root-separation bound. Thus the full description has total
length \(N^{O(h+1)}\). Exact polynomial sign determination at an isolated
algebraic real root verifies every original row in polynomial time in this
description and the input, using univariate remainder and Sturm or
subresultant computations. A false certificate cannot pass because its
represented real point must satisfy the original inequalities exactly.

Algebraic coordinates are necessary even at \(h=1\): the opposite
inequalities \(x^2\le2\) and \(2-x^2\le0\) have Hessian span one
and feasible points \(\pm\sqrt2\), with no rational feasible point.

This also proves the NP consequence already obtained in Section 3.1.
Bounded integer coordinates can also be
included: guess their
polynomial-length values and use the continuous algebraic certificate for
that slice. No unbounded-integer claim follows.

## 8. Bounded objective values and exact optimizers

If an explicit rational box is supplied for \(x\), append rational bounds
for the lifted \(y_j\), obtained by summing absolute coefficients of their
quadratic forms over that box. This makes \(P\) compact. Replace the
objective in (2) by

\[
 r_\varepsilon(w)=q_0(x)+\varepsilon P_0(w),
\]

where \(q_0\) is the given arbitrary quadratic objective. The same
genericity argument applies. The original optimal point is feasible in the
bands for sufficiently small \(\varepsilon\). Compactness and uniform
convergence of the objective imply that each convergent minimizing
subsequence tends to an original global optimizer and its values tend to
the original optimum. Equations (4)--(5) and the finite-quotient lemma apply
to the objective value as well as the coordinates. This gives the stated
bounded-value and optimal-point encoding bounds.

An arbitrary quadratic objective over a polyhedron is NP-hard even though
this statement has \(h=0\). Small exact encodings therefore do not imply
easy discovery. No polynomial-time verification of global optimality is
claimed by the feasible-point certificate.

Feasibility itself is already NP-hard with \(h=1\): encode a Boolean
formula by variables \(0\le x_i\le1\), its usual linear clause
inequalities, and the single concave inequality
\(\sum_i x_i(1-x_i)\le0\). Each summand is nonnegative on the box, so
this last row forces every coordinate to be binary. This is the classical
Boolean-encoding argument, included to delimit the algorithmic claim.

## 9. Literature boundaries and unresolved checks

[Vavasis's quadratic-programming result](https://doi.org/10.1016/0020-0190(90)90100-C)
gives polynomial-size rational witnesses for one quadratic inequality plus
affine rows. Its mixed-integer extension is
[Del Pia, Dey and Molinaro, *Mixed-integer quadratic programming is in NP*](https://arxiv.org/abs/1407.4798).
The present proposed statement uses algebraic witnesses and arbitrarily many
quadratic rows of fixed Hessian span. It should not be advertised as the
first NP certificate for quadratically constrained systems.

[Grigoriev and Pasechnik](https://arxiv.org/abs/cs/0403008), Theorem 1.2,
already give degree and coefficient-size bounds for sampling over a
fixed-component quadratic map. Arbitrarily many affine inequalities are
not free components in that theorem. [Bienstock, Del Pia and Hildebrand](https://arxiv.org/abs/2011.08347),
Introduction, explicitly distinguish the few-quadratic results from the
case of two quadratics with arbitrarily many affine inequalities. Their
discussion also distinguishes rational witnesses from exact decision and
near-feasible certificates. The local full text was inspected for these
boundaries; no direct fixed-Hessian-span NP theorem was identified there.

[Nie and Ranestad](https://arxiv.org/abs/0802.1233) give precise generic
algebraic degrees for polynomial optimization. Their QCQP degree formula
is closely related to the generic KKT step here. The proposed addition needs
degenerate original inputs, a common-field height bound, arbitrarily many
affine rows, and an explicit perturbation that preserves some feasible
limit. Generic algebraic degree alone does not establish those assertions.

The effective degree facts, perturbation argument, and common-field limits
were subsequently checked in both written reviews. The later
[prior-work audit](nonconvex-hessian-span-prior-audit.md) provides the
stronger assessment for feasibility recorded in Section 3.1, and adds
comparisons with multihomogeneous degree-and-height bounds and attained
polynomial minima. The boxed-value and finite-infimum results require their
separate proofs; their priority remains unresolved. An unsuccessful search
is not evidence of novelty.

## 10. Meaning, limitations, and verification

The feasible-point corollary is useful despite its modest originality:
a solver handling many rows built from a fixed collection of quadratic
forms could in principle return an algebraic feasible point that a separate
program verifies exactly. The separate value results control algebraic
degrees and heights through degeneracy and, in the linked extension, at
infinity. Producing manageable descriptions from numerical candidates,
identifying useful application families with small \(h\), and sharpening
the worst-case bounds remain necessary for practical value. No computational
speedup has been established.

The following limits are material:

- Feasibility is already NP-hard at \(h=1\); the proof gives short
  certificates and does not avoid searching among many affine faces.
- A short encoding of an optimal point does not give a short certificate
  that this point is globally optimal.
- The feasibility corollary allows unbounded continuous domains. The value
  theorem proved in this file requires an explicit box. The separate
  [finite-infimum note](nonconvex-finite-infimum.md) studies finite,
  possibly unattained infima on unbounded nonconvex domains.
- Weak inequalities and rational quadratic data are assumed. No statement
  about unbounded integer variables, strict-inequality limits, or arbitrary
  polynomial degree is proved here.
- The common algebraic representation is essential; separate coordinate
  polynomials do not alone supply a polynomial-time multivariate verifier.

The completed reviews are
[nonconvex-hessian-span-review.md](nonconvex-hessian-span-review.md) and
[nonconvex-hessian-span-adversarial.md](nonconvex-hessian-span-adversarial.md).
The first reviewer contributed an early perturbation suggestion and later
clarifications; the second was assigned independently by the root agent.
The root also reread the complete proof and checked the substantive repairs.
These reviews are evidence of correctness, not a guarantee.

The second review records its own exact checks of the generic KKT example,
an indefinite Schur-complement counterexample, and the ellipse obstruction.
They check those finite calculations, not the universal certificate theorem.
The author ran a targeted inline Python check of this file's control
characters, trailing whitespace, final newline, and local links, and
`git diff --check -- research-20260927/nonconvex-hessian-span-frontier.md`.
Both returned successfully; the Python check covers the current file
independently of Git tracking status. No Lean formalization, project-wide
verification, or CI inspection was run for this work.
