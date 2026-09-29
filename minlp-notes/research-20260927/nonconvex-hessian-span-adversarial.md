# Adversarial review of nonconvex Hessian-span certificates

Date: 2026-09-27. Reviewer: a separate research agent who had not worked on
the Hessian-span proofs before this assignment.

The proof in [the candidate note](nonconvex-hessian-span-frontier.md)
withstands this review. I found no substantive gap in the stated feasibility
certificate theorem or the bounded-objective extension. The genericity step
needs the full bordered KKT determinant, as the note now includes. The
quantitative projection facts used there are established algebraic geometry;
an inspected primary source explicitly uses both needed facts.

This conclusion is a mathematical proof audit, not a formal verification or
a novelty finding. It does not establish a polynomial-time algorithm for
finding a feasible point. The final certificate has a polynomial-time
verifier for fixed Hessian span.

## 1. Exact statements reviewed

The system consists of rational weak quadratic inequalities and rational
affine rows. Its continuous dimension, number of rows and Hessian ranks can
vary. The parameter is the dimension \(h\) of the rational linear span of
the native constraint Hessians.

The claims reviewed are:

- Every nonempty such system has a feasible tuple in one real number field
  of degree \(N^{O(h+1)}\), with a common univariate description of total
  binary length \(N^{O(h+1)}\).
- Feasibility therefore belongs to NP for every fixed \(h\).
- With an explicitly bounded original domain, arbitrary quadratic
  optimization has an optimal tuple and value with these encoding bounds;
  the objective Hessian need not be included in \(h\).

The last statement is an encoding theorem. The supplied feasible-point
certificate does not verify global optimality. No assertion about attainment
of an arbitrary unbounded nonconvex problem was reviewed or follows.

## 2. Incidence dimensions and the two determinant conditions

Here is an independent reconstruction of the key genericity argument.
Let \(d\) be the dimension of one affine chart, \(s\) its selected active
quadratics, and \(p\) the number of coefficients of those quadratics and
the objective.

For \(s\le d\), at fixed \(u\), the values and first derivatives of the
constraint quadratics are independent linear functions of their coefficients.
For example, after choosing each quadratic homogeneous part, its linear
and constant coefficients can prescribe these data independently. Therefore
the common-zero incidence has codimension \(s\), and gradient rank below
\(s\) has a further codimension \(d-s+1\). Including \(u\) leaves dimension
at most \(p-1\). For \(s>d\), the common-zero incidence alone has dimension
\(p+d-s<p\). Projection closure does not increase dimension.

For the KKT incidence, eliminate the \(s\) constraint constants using
the equations \(f_i(u)=0\). Next eliminate the \(d\) objective linear
coefficients using stationarity. These are polynomial substitutions with
unit coefficients on the eliminated entries. The resulting incidence is
isomorphic to affine space of dimension \(p\), hence irreducible.

The sample

\[
f_i=u_i^2-1,\qquad
r=\sum_{j=1}^d u_j^2+\sum_{i=1}^s u_i
\]

has KKT points with \(u_i=\pm1\) for \(i\le s\), other coordinates zero,
and \(\lambda_i=-1-1/(2u_i)\). At each such point,

\[
M=\operatorname{diag}(-1/u_1,\ldots,-1/u_s,2,\ldots,2)
\]

is invertible, and \(GM^{-1}G^T\) is diagonal and invertible. Thus neither
\(\det M\) nor the bordered KKT determinant is identically zero on the
incidence. Their zero loci have dimension at most \(p-1\). Their projected
closures are proper, even if some fibers elsewhere are unbounded or have
positive dimension.

The proof must not replace bordered nonsingularity by LICQ and invertibility
of \(M\). For example,

\[
M=\operatorname{diag}(1,-1),\qquad G=(1,1)
\]

has full row-rank \(G\) and invertible \(M\), but \(GM^{-1}G^T=0\).
The note avoids this error by excluding both determinant-zero loci.

The empty active set is also covered: the objective Hessian alone is the
KKT matrix. Zero-dimensional affine charts can be treated directly as
rational points of polynomial bit length.

## 3. Effective degree and one small perturbation tuple

The number of coefficient, primal and multiplier variables in the incidence
description is polynomial in \(d+s\). Its equations have degrees bounded
by a polynomial in \(d+s\). A cumulative affine degree bound from Bézout
is therefore \(2^{\operatorname{poly}(d+s)}\).

Use the sum of the degrees of irreducible components if a variety has
components of different dimensions. This avoids ambiguity in the word
"degree" when projecting a reducible set. Applying the projection bound
component by component gives the same coarse estimate needed here.

The two specific projection facts were checked in
Ovchinnikov, Pogudin and Vo,
[*Bounds for elimination of unknowns in systems of differential-algebraic
equations*, Proposition 5, proof, PDF page 20](https://par.nsf.gov/servlets/purl/10251735).
That proof explicitly uses that the closure of a linear projection has
degree no larger than the original variety, and that a proper image lies
in a nonzero hypersurface of degree at most that bound. It attributes
these facts to Heintz, *Definability and fast quantifier elimination in
algebraically closed fields* (1983), Lemma 2 and Proposition 3.
The inspected [PDF](nonconvex-review-sources/ovchinnikov-pogudin-vo.pdf)
and [extracted text](nonconvex-review-sources/ovchinnikov-pogudin-vo.txt)
are retained locally.

The number of affine restrictions and oriented active subsets can be
exponential in the input size. This does not invalidate the proof. Each
proper bad set supplies one nonzero polynomial of singly exponential
degree; multiplying over singly exponentially many choices still gives
degree \(2^{\operatorname{poly}(N)}\).

For every fixed nonzero \(\varepsilon\), restriction of each independently
chosen perturbing quadratic onto any full-rank affine chart is surjective
onto the chart's quadratic polynomials. Multiplication by
\(\varepsilon\) or \(\varepsilon^2\) and the fixed shifts preserve
surjectivity. The two opposite orientations of the same band must not be
selected simultaneously; the note expressly excludes that situation.

Thus each bad polynomial remains nonzero after substituting the parameter
path. Choosing a nonzero coefficient in its expansion in \(\varepsilon\)
and avoiding the product of these coefficients guarantees that the path is
not identically bad for any chart and support. The integer-grid argument
then supplies a perturbation tuple with polynomial coefficient bit lengths.
No bound on the coefficient height of the bad hypersurfaces is needed:
the size of the avoiding grid depends on their degrees only.

For this one tuple, each exceptional set of nonzero \(\varepsilon\)
is finite. Their finite union is avoided throughout a sufficiently small
positive interval. Genericity is therefore available along the sequence
used in the optimization argument; it is not merely generic in a
parameter space unrelated to that sequence.

This is an existence argument. It neither enumerates the affine restrictions
nor promises to find the generic perturbation in polynomial time.

## 4. Coercivity and the feasible limit

The quadratic-map lift correctly leaves exactly \(h\) equations and
places every original row in one rational polyhedron. No native inequality
is deleted. The lift and all affine charts have polynomial coefficient
bit lengths by rational linear algebra.

For an original feasible anchor \(\bar w\), the perturbed bands contain
it once \(\varepsilon |P_j(\bar w)|\le1\) for all \(j\). This threshold
can depend on the unknown anchor; the threshold is not a coefficient of
the later elimination system.

For sufficiently small positive \(\varepsilon\), the Hessian of
\(\|w\|^2+\varepsilon P_0(w)\) is bounded below by a fixed positive
multiple of the identity. Its linear and constant parts stay uniformly
bounded. Consequently comparison with the anchor's objective value
bounds every selected global minimizer in one common compact set.
Closedness gives attainment on each perturbed feasible set, even if the
polyhedron is unbounded.

A convergent subsequence stays in the polyhedron. Its band residuals tend
to zero, because the points are bounded and the perturbing polynomials
are fixed. Its limit is therefore feasible for the original lifted
equations. No uniqueness, explicit radius, bounded multiplier or
preselected algebraic anchor is required.

At a selected minimizer, restricting all active affine rows gives a
rational affine chart. All other affine rows are strictly slack locally.
Hence the original minimizer is a local minimizer of the remaining
nonlinear inequalities in that chart. LICQ is enough for KKT necessity
there. This only deletes inactive affine rows for the local stationarity
assertion; it does not repeat the invalid nonconvex global reduction.

The ellipse example in Section 2 correctly demonstrates the danger:
on \(4(x-2)^2+y^2=4\), squared norm is
\(-3x^2+16x-12\). Its minimum for \(5/2\le x\le3\) is nine at
\((3,0)\), whereas the full ellipse has minimum one at \((1,0)\).

## 5. Elimination, the common field and certificate length

After fixing one chart and active oriented subset on a subsequence, the
adjugate reconstruction uses at most \(h\) multiplier variables.
The full bordered determinant and \(\det M\ne0\) imply nonsingularity
of the reduced multiplier equations by their Schur complement.
Positive definiteness of \(M\) is not used.

The reduced equations and coordinate output numerators have multiplier
degree \(O(d+1)\), parameter degree \(O(d+1)\), and logarithmic
coefficient norm polynomial in \(N\). There are only
exponentially many expanded monomials at worst, with polynomial logarithm.
Thus the coefficient-sensitive finite-quotient lemma has the required
input bounds and yields degree and coefficient-bit bounds
\(N^{O(h+1)}\) for each coordinate limit.

Every rational linear combination uses the same selected roots and the
same convergent tuple. Its annihilator degree has the same bound,
independent of the combination's coefficient heights. The primitive-element
argument therefore bounds the joint field degree, rather than a product
of individual degrees.

The bounded primitive-element grid and the trace-matrix argument in
Section 7 are sound. Scaling by leading minimal-polynomial coefficients
makes the relevant numbers integral. Their traces are integers of
polynomial bit length in the degree and height bounds. Separability makes
the power-basis trace matrix nonsingular. Cramer's rule therefore gives
rational coordinate coefficients of polynomial bit length in those bounds.
An isolated real generator root makes the final sign verifier sound.

One minor wording clarification was sent to the author: conjugate
magnitudes have exponential bounds, but the bit lengths of leading
coefficients themselves have polynomial bounds. The stronger polynomial
bit bound already follows immediately from the preceding hypotheses.

## 6. The bounded optimization extension

The explicit box gives polynomial-bit rational bounds on every lifted
quadratic coordinate, making the lifted polyhedron compact. Generic
perturbations of an arbitrary quadratic objective remain valid in the
incidence argument; coercivity is no longer needed.

For any original optimizer, the perturbed bands eventually retain it.
Uniform convergence on the compact polyhedron and the usual subsequence
comparison therefore force every selected limiting minimizer to be an
original global optimizer. Its coordinates and objective are rational
outputs of the same fixed multiplier system. The common-field conclusion
still applies.

The argument includes \(h=0\): a quadratic objective over a rational
polytope can be NP-hard even though it has a small exact optimum encoding.
This is an explicit distinction between short descriptions and easy
optimization, not a contradiction.

## 7. Prior work and significance limits

The [inspected Bienstock--Del Pia--Hildebrand paper](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf),
Introduction, PDF pages 2--3, distinguishes classical few-quadratic
algorithms from systems with arbitrarily many affine rows and two quadratic
inequalities. The later
[local full text](../literature/papers/bienstock2023-complexity-exactness-and-rationality-in/fulltext.md)
retains that distinction. This supports treating arbitrary affine rows
as a material part of the present theorem's scope. It does not prove
that the NP conclusion has no other antecedent.

The candidate correctly compares against Vavasis's one-quadratic
rational-witness theorem, the mixed-integer extension by Del Pia,
Dey and Molinaro, few-quadratic sampling by Grigoriev and Pasechnik,
and generic algebraic-degree calculations by Nie and Ranestad.
The proposed addition combines a Hessian-span lift, arbitrary affine
restrictions, controlled perturbations of degenerate inputs, common-field
degree and height bounds, and an exact sign verifier.

Targeted searches used combinations of "fixed number quadratic constraints",
"linear inequalities", "NP", "algebraic certificate", and "few quadratic
equations". They did not identify an equivalent theorem during this audit.
That search outcome does not establish novelty. A specialist literature
review remains warranted before describing this as a new complexity result.

NP-hardness already holds for \(h=1\): the bounds \(0\le x_i\le1\)
and one concave inequality \(\sum_i x_i(1-x_i)\le0\) force all variables
to be binary. Affine clause inequalities then encode satisfiability.
This elementary known reduction prevents a polynomial-time discovery claim.
The contribution, if new, is short exact witnesses for a broader class,
not a general speedup for nonconvex optimization.

## 8. Targeted verification

The command actually run was

~~~sh
python research-20260927/check_nonconvex_hessian_span_adversarial.py
~~~

It passed. Its exact SymPy calculations check 56 sample KKT points in
dimensions one through four, including empty active sets; verify both
determinants and their Schur relation; confirm the indefinite isotropic
counterexample to omitting bordered nonsingularity; and verify the ellipse
endpoint calculations.

These checks support the algebraic examples and delicate distinctions.
They do not prove the general incidence dimension, effective elimination,
or NP statements. The proof audit and inspected degree source address
those steps. No numerical experiments, Lean formalization, project-wide
verification, or CI inspection were performed for this review.
