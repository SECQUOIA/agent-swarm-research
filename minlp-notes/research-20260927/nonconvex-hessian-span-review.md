# Nonconvex Hessian span: witness question and proof boundaries

Date: 2026-09-27. Status: the complete proof in
[nonconvex-hessian-span-frontier.md](nonconvex-hessian-span-frontier.md) was
read and adversarially reviewed. After two precision clarifications described
below, this review finds no mathematical gap in its feasibility-certificate
and bounded-optimum encoding conclusions. Publication priority remains
unestablished. The earlier failed sampling route is retained as an explicit
boundary of the argument.

The reviewer contributed the outward-perturbation suggestion and two
clarifications during development. The final proof was then independently
reread, but this is not a wholly independent discovery of the proof. A second
reviewer was staffed separately by the root agent.

## Question and elementary reduction

Consider rational quadratic inequalities and affine rows in arbitrarily many
real variables. The Hessians may be indefinite. Let `N` be the explicit
binary input length and let `h` be the dimension of the rational linear span
of the native Hessian matrices.

The reviewed claim is that every nonempty such set has a feasible point with a
**common rational univariate representation** whose degree and total binary
length are `N^{O(h+1)}`. A common representation expresses all coordinates as
rational functions of one specified real algebraic root. This would provide
an NP certificate for fixed `h`: exact signs of the original rational
quadratics at that represented point can be checked in polynomial time. It
would not provide a polynomial-time feasibility algorithm. Nonconvex quadratic
programming with arbitrary affine inequalities is already NP-hard.

The matrix-span condition has a direct exact lift. Choose rational matrices
`B_1,...,B_h` spanning all native Hessians and introduce continuous variables

```
y_j = (1/2) x^T B_j x  (j=1,...,h).
```

Each original quadratic inequality becomes affine in `(x,y)`. Rational linear
algebra bounds all lift coefficients by a polynomial in `N`. The result has
exactly `h` quadratic equations and arbitrarily many affine inequalities.
Replacing the equations by pairs of inequalities gives at most `2h` quadratic
inequalities. This elementary reduction is valid without convexity.

The lift alone does not settle the question: available few-quadratic sampling
theorems do not treat arbitrarily many affine inequalities as free.

## A concrete failure of the convex deletion argument

Take

```
F = {(x,y): 4(x-2)^2+y^2=4, x>=5/2}.
```

Write the equality as two opposite quadratic inequalities. Their Hessians
are `diag(8,2)` and its negative, so their matrix span has dimension one.
On the ellipse,

```
x^2+y^2 = -3x^2+16x-12.
```

The cut restricts `x` to `[5/2,3]`. The displayed polynomial is strictly
concave, so its minimum on that interval is the smaller of the two endpoint
values, `37/4` and `9`. Consequently `(3,0)` is the unique minimum-norm
point of `F`, and its squared norm is `9`. The affine inequality is inactive
there.

Deleting that inactive inequality leaves the full connected ellipse. Its
minimum squared norm is `1`, attained at `(1,0)`. Thus deleting inactive rows
does not preserve the global minimum norm in the nonconvex case. Restriction
to the active quadratic variety only preserves local optimality.

This example also explains the sampling problem. A theorem that returns one
sample from each connected component may return `(1,0)` from the ellipse's
single component; that sample violates the deleted row. Its norm does not
bound the original minimum norm from above. This defeats that proof route,
not the proposed algebraic-witness theorem: the original set itself has the
short rational witness `(3,0)`.

## Strongest prior results checked

**One quadratic inequality plus arbitrary affine inequalities.**
[Vavasis, *Quadratic programming is in NP*, Information Processing Letters
36 (1990), 73--77](https://doi.org/10.1016/0020-0190(90)90100-C), gives a
polynomial-size rational feasible witness for this class. The statement is
also recorded in the introduction of the primary Bienstock--Del Pia--Hildebrand
paper cited below. It concerns one quadratic inequality, not arbitrary
many inequalities with one-dimensional Hessian span. For example, the pair
`x^2<=2` and `-x^2<=-2` has Hessian span one and only irrational points.

**Few quadrics, without an arbitrary collection of affine inequalities.**
[Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
Sampling in real algebraic sets*, Computational Complexity 14 (2005),
20--52](https://logic.pdmi.ras.ru/~grigorev/pub/quadric_cc.pdf), Theorem 1.2,
constructs a real univariate sample representation in each component of
`Z(p(Q(x)))`, where `Q` has `k` quadratic components and `p` has degree `d`.
The degree and coefficient-bit bounds have the form `(dn)^{O(k)}` times the
input coefficient-bit bound. Degenerate and unbounded sets are allowed.
For a fixed number of quadratic constraints this already gives polynomial-size
exact algebraic witnesses; arbitrary affine equalities can be eliminated.
Encoding many affine inequalities by separate squared slacks increases the
quadratic-map dimension, so it does not give the present claim.

The paper's Theorem 1.5 announces an optimization result but explicitly
defers its proof to a continuation. This review does not rely on that
announcement. The fully proved sampling theorem is the relevant verified
ingredient. A separately staffed source reviewer inspected Theorem 1.2 and
the deferred-proof language directly.

**The affine-inequality boundary is explicitly recognized in prior work.**
[Bienstock, Del Pia, and Hildebrand, *Complexity, Exactness, and Rationality in
Polynomial Optimization*](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf),
introduction, p. 3 of the inspected 2020/2021 text, distinguishes the
Barvinok/Bienstock few-quadratic analyses from a system with arbitrarily many
linear inequalities and only two quadratic inequalities. Its fixed-dimension
near-feasible rational certificates use a different parameter. This
observation does not establish that NP membership for the present class is
open; it establishes that the cited algorithms cannot simply be applied with
affine inequalities omitted from their count.

**Generic critical degree is polynomial for few active quadrics.**
[Nie and Ranestad, *Algebraic Degree of Polynomial Optimization*](https://arxiv.org/pdf/0802.1233),
Theorem 2.2, Corollary 2.5, and its QCQP specialization, give the generic
critical-point degree `2^k binomial(n',k)` after active affine equations leave
dimension `n'` and there are `k` active quadratic rows. The nongeneric
conclusions in that argument require zero-dimensional critical equations.
This is strong precedent for the desired degree scale, but does not by itself
give a uniform coefficient-height bound through singular feasible sets and
abnormal first-order multipliers.

Searches did not locate a directly applicable exact NP theorem with arbitrary
affine inequalities and fixed native Hessian span. This is a limited search
result, not a claim of novelty or of an established open problem.

## Audit of the completed perturbation proof

The full proof resolves the earlier genericity and common-limit obstacles.
It keeps the polyhedron `P` exact, replaces each lifted equation `F_j=0` by

```
|F_j(w)+epsilon^2 P_j(w)| <= epsilon,
```

and minimizes `||w||^2+epsilon P_0(w)`. The perturbation polynomials are
chosen once with polynomial-bit integer coefficients. The following steps
were checked independently against the saved proof.

**Proper generic exceptional sets.** On a fixed affine chart, the incidence
of KKT equations in primal variables, multipliers, and all quadratic
coefficients is an affine space: solve constraint values for their constant
coefficients and stationarity for the objective's linear coefficients. Its
dimension equals the coefficient-space dimension. Neither the multiplier
Hessian determinant nor the bordered KKT determinant vanishes identically,
as the explicit diagonal example in the primary proof verifies. Each
determinant-zero incidence therefore projects into a proper algebraic subset.
The independent-gradient assertion follows from the independent value and
gradient coefficients and the codimension of deficient-rank matrices. The
case of too many active quadratics is also excluded generically.

**Effective degree, including smaller components.** The initial wording
needed to distinguish cumulative degree from degree of only the components
of largest dimension. The revised proof explicitly sums degrees of all
irreducible components. It also replaces an unrestricted list of gradient
minors by normalized dependence-vector charts: set one nonzero dependence
coordinate to one, impose the gradient dependence, and impose the constraint
values. Each chart has polynomially many equations of degree at most three.
The determinant incidences also have polynomially many defining equations
of polynomial degree. Repeated cumulative affine Bezout and projection then
give the coarse bound `2^{poly(N)}` that is needed.

These degree facts were independently checked in Krick--Pardo--Sombra,
[*Sharp estimates for the arithmetic Nullstellensatz*](https://mate.dm.uba.ar/~krick/KrPaSo01.pdf),
Section 1.2.1, printed pp. 12--13. It uses the cumulative convention and
states the linear-image-closure and unrestricted intersection bounds. For
each proper irreducible image component of dimension `r`, a generic linear
projection into `r+1` coordinates has a hypersurface image closure of no
larger degree. Pulling its equation back gives a containing hypersurface.
Multiplying across the components covers the entire exceptional set and
retains the cumulative-degree bound. Thus components of smaller dimension
are not silently discarded.

**Polynomial-bit perturbations on all faces.** Every relevant affine chart
has polynomial-bit rational coefficients. Restriction of arbitrary ambient
quadratics onto a fixed chart is surjective. For each fixed nonzero
`epsilon`, the proposed perturbation coefficients therefore range over the
entire quadratic coefficient space used by the genericity lemma. Substituting
the path into a nonzero bad-set polynomial cannot give the zero polynomial
in both `epsilon` and the perturbation coefficients. Choosing a nonzero
`epsilon` coefficient and multiplying these choices over all charts and
oriented subsets gives a nonzero polynomial of degree `2^{poly(N)}`.
An integer grid of that side length contains a point where it does not
vanish. The grid coordinates require only polynomially many bits. No height
bound on the bad-set equations is needed for this existence argument.

For this one chosen perturbation, every relevant univariate bad polynomial
has only finitely many nonzero roots. Finitely many charts and subsets
therefore leave a common sufficiently small positive interval where all
generic conclusions hold. The verifier never needs to construct the grid
or enumerate the faces.

**Feasibility and compactness without an encoded bound.** Any fixed original
feasible point satisfies the perturbed bands for sufficiently small
`epsilon`, because their width has order `epsilon` and their perturbation at
that point has order `epsilon^2`. The norm objective remains uniformly
coercive. Comparison with that fixed point bounds every minimizing sequence
under consideration. Its limit satisfies all original affine rows and
quadratic equations. This addresses the inactive-row failure exhibited by
the ellipse example.

**Nonsingular elimination on a fixed face.** Only one orientation of each
band can be active, so the number of active nonlinear rows is at most `h`.
The exact active affine face admits a rational chart. Inactive affine rows
may be omitted only for the local KKT assertion. Genericity gives independent
nonlinear gradients and both nonsingular matrices. Finitely many choices
allow selection of one chart and active subset along a convergent
subsequence. The revised text separately handles a zero-dimensional chart,
whose fixed rational point is itself the feasible limit.

After eliminating primal variables by the invertible multiplier Hessian,
the Jacobian of the cleared active equations is the negative Schur complement
`-Delta^2 G M^{-1} G^T`. It is nonsingular because the bordered KKT matrix
is nonsingular. Positive definiteness is not being assumed at this step.
The remaining equations have `s<=h` multiplier variables, degree `O(n+h)`,
and polynomial coefficient bits. The
[finite-quotient elimination lemma](explicit-span-separation.md) applies to
these nonsingular roots and their finite rational-output limits; divergent
multipliers are permitted. This avoids requiring a new Puiseux-sampling
theorem.

**One common field and a short representation.** Applying the elimination
lemma to every rational linear combination of the coordinates preserves one
degree bound. The primitive element theorem therefore bounds the degree of
their common number field, rather than multiplying separate coordinate
degrees. A bounded integer combination separates all pairs of field
embeddings by the same grid argument. Applying the output lemma to that
combination gives a bounded-height primitive polynomial.

The power-basis coefficient bound was also checked: multiplying each
coordinate and the primitive element by its minimal polynomial's leading
coefficient gives algebraic integers. The trace-pairing linear system has
integer entries, controlled conjugate magnitudes, and nonzero determinant.
Cramer's rule supplies polynomial-bit rational coordinate coefficients.
Ordinary univariate root separation supplies a short isolating interval.
Thus exact sign verification of the original constraints gives the stated
NP certificate. There is no claim that this certificate verifies global
optimality.

**Bounded objective theorem.** With explicit input bounds on the original
variables, the lifted variables also have polynomial-bit bounds. Keeping
these in `P` makes the perturbed domains compact. Minimizing an arbitrary
quadratic objective plus its small generic perturbation then has subsequences
converging to original global optimizers. The same elimination argument
bounds the value and an optimal point. For `h=0`, this specializes to the
classical rational-encoding property of quadratic programming over a
polyhedron. No unbounded finite-infimum statement or unbounded-integer
certificate follows from this proof.

The number of possible affine faces may be exponential. This is consistent
with both the short-certificate conclusion and NP-hardness, and it remains
the principal distinction between describing a solution and finding one.

## Verification record

The ellipse counterexample was checked symbolically and with an inline SymPy
script. The script checked the eliminated norm polynomial, its endpoint
values, its second derivative, and the rank-one span of the two vectorized
Hessians; all checks passed. This computation verifies that counterexample,
not the proposed witness theorem.

The source investigation used openly accessible primary manuscripts and the
repository's existing few-quadratic and algebraic-degree audits. A fresh
subagent independently examined the closest NP and exact-sampling literature.
For the final review, the complete saved primary proof and the full
finite-quotient elimination lemma were reread. The incidence dimensions,
determinant witness, integer-grid choice, bounded minimizing sequence,
Schur complement, common-field degree argument, and trace coefficient bound
were checked symbolically. The repaired cumulative-degree argument and the
explicit zero-dimensional-face case were rechecked after revision.
Targeted document checks were `git diff --check --
research-20260927/nonconvex-hessian-span-review.md` and an inline Python check
of this file's whitespace, final newline, and control characters; both passed.
No Lean formalization, project-wide verification, or CI inspection was run.
