# Prior audit: convex polynomial systems with few nonlinear directions

Date: 2026-09-28. This audit concerns the developing exact-feasibility
argument; it does not certify the complete algorithm or establish
publication priority. It extends the comparison in
[the common quadratic range audit](common-range-fpt-prior.md).

The search found strong precedents for every major algorithmic ingredient.
No inspected source directly states the combined parameterization below.
The defensible candidate contribution is an exact bit-complexity result for
an arbitrary linear continuous extension of a small-dimensional polynomial
system. It should be presented as a consequence of established algebraic
bounds and convex optimization machinery, with the reduction itself made
explicit.

## Scope of the candidate

After a rational change of coordinates, consider

\[
 C v+p(u)\leq 0,
 \qquad u\in\mathbb R^r,\quad v\in\mathbb R^\ell,
\]

where every component of `p` is a rational, globally convex polynomial of
degree at most `d`, and `C` is a constant rational matrix. Affine rows are
allowed, and the number of rows and the dimension `ell` are unrestricted.
The desired running time is `f(r,d) N^C0`, with an absolute exponent `C0`
and total rational input length `N`. No supplied radius or Slater point is
assumed.

The mixed-integer extension has `p(z,u)` jointly convex in
`(z,u) in R^(k+r)`, with `z in Z^k`. Convexity separately on each integer
fiber is insufficient for the proposed integer oracle. Its target bound
is `f(k,r,d) N^C0`. An explicitly supplied coordinate change must count
toward `N`; computing a suitable change is a separate preprocessing claim.

The parameter counts directions on which nonlinear terms depend. It is
different from the number of polynomial rows, the number of monomials, or
the span dimension of quadratic Hessian matrices.

## Closest implicit-description precedents

**Norton--Plotkin--Tardos already avoid enumerating a projection.**
In the Cornell report of
[*Using separation algorithms in fixed dimension*](https://ecommons.cornell.edu/server/api/core/bitstreams/36e75f7f-421a-43aa-b069-052b4c6850d7/content),
Theorems 2.3--2.4, printed pp. 6--8, give exact feasibility and linear
optimization from a separation algorithm whose comparisons are affine in
the query point. With dimension `r`, comparison count `q`, and execution
time `t`, the bound is `O(q^r t)`. Theorem 3.1, p. 9, uses dual
certificates to separate an LP projection with potentially exponentially
many faces. Thus implicit projection and certificate-based separation
are established ideas. Substituting polynomial `p(u)` does not preserve
the required affine-comparison model. The displayed input-size exponent
also depends on dimension. An independent subauditor inspected these
theorems and the standing comparison-model assumptions in the full report.

**Toledo supplies the nonlinear oracle precedent, with a stronger parallel application.**
[*Maximizing Non-Linear Concave Functions in Fixed Dimension*](https://www.tau.ac.il/~stoledo/Pubs/concave.pdf),
Theorem 4.4, printed p. 16, permits polynomial separating functions and
returns an exact outcome under its algorithmic hypotheses. The sequential
analysis on p. 15 gives `O(T0^(2^r))`; its parallel version is
`O(T0 (Tp log P)^(2^r-1))`. The model is arithmetic/RAM. The definition on
pp. 3--4 permits fixed-degree polynomial evaluations followed by additions,
constant multiplications, and sign comparisons. A general polynomial-time
LP routine is not automatically an admissible comparison algorithm.
The generic sequential bound has a dimension-dependent exponent. However,
Section 5, printed p. 16, applies the parallel theorem to explicit convex
polynomial rows in arithmetic time
`O(m (log m log log m)^(2^r-1))`. Those logarithmic powers can be absorbed
into a parameter factor times a fixed power of `m`. Thus that application
is compatible with FPT arithmetic complexity and must not be described
as an XP obstruction. The remaining comparison concerns exact Turing
precision and the restricted evaluator interface, especially for an
implicit LP projection. The definition, recurrence, theorem, and Section 5
application were inspected; the last was independently reread during the
[optimization prior audit](polynomial-nonlinear-dimension-optimization-prior.md).

## The integer oracle is largely an established tool

**Hildebrand--Köppe is stronger than a generic fixed-dimensional QE bound.**
[*A new Lenstra-type Algorithm for Quasiconvex Polynomial Integer
Minimization with Complexity 2^{O(n log n)}*](https://arxiv.org/pdf/1006.4661),
Theorem 1.1, already gives true FPT in total integer dimension and degree
for explicitly listed quasiconvex polynomials. Sections 4--6 show that the
row list is used for membership tests and selection of a violated
polynomial. Theorem 5.7 then works with that one polynomial; Remarks
5.5--5.6 retain affine coordinate transformations and evaluate gradients
by the chain rule. Lemma 6.1's lower volume bound uses uniform degree and
coefficient bounds, without dependence on the row count. These passages
were independently read by this auditor and a subauditor. Therefore a
suitable implicit-row oracle can replace the scan. This is a deduction
from their proof, not a new Lenstra algorithm; its detailed adaptation is
being recorded separately by the proof reviewer.

For clarity, the proposed LP oracle has a fixed mathematical family.
Writing `y=(z,u)` or its scaled grid coordinates, set

\[
 \Lambda=\{\lambda\geq0:C^T\lambda=0,\quad
                  \mathbf1^T\lambda=1\},
 \qquad F_\lambda(y)=\lambda^Tp(y)-\epsilon.
\]

Use `F_lambda<0` for every vertex of `Lambda`. At a rational query point
`ybar`, solve the rational phase-I LP

\[
 \min_{v,t}\{t:Cv+p(\bar y)\leq t\mathbf1\}.
\]

If its optimum is below `epsilon`, the query belongs to the strict
projected set. Otherwise an optimal dual vertex returns a violated
polynomial. This remains one fixed family when different query points
select different vertices. A selected multiplier must be retained during
any subsequent evaluations of its polynomial. If `Lambda` is empty,
the phase-I LP is unbounded below, which is the corresponding all-space
case. Direct bounding constraints can be handled separately.

This elementary dual construction has several consequences relevant to
the comparison. The exponential number of vertices need not be listed.
Their rational encodings are uniformly bounded by minors of the constant
matrix. Each polynomial can have its denominators cleared separately.
A common denominator for the entire exponential family is unnecessary.
Joint convexity makes every returned polynomial convex. The grid,
relaxation, bounding region, and positive residual gap still require
independent justification before this oracle proves the intended result.

One invalid shortcut deserves explicit exclusion. Converting each weak
integer polynomial row `G<=0` into `G-1<0` preserves integer solutions,
but it changes membership at noninteger query points. An LP oracle for
the original weak system cannot simply be reused for that enlarged strict
system. The normalized, uniformly relaxed family above avoids this
particular mismatch.

**Other integer oracle results are relevant, but do not remove the
precision obligation.** Oertel--Wagner--Weismantel,
[*Integer convex minimization by mixed integer linear optimization*](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf),
Theorem 1, assumes a known integer box and first-order oracles with stated
accuracy. It returns a solution with feasibility and objective error
`2 epsilon`, or certifies integer infeasibility; exact value oracles permit
exact optimization. Its last paragraph extends the framework to mixed
integers conditional on sufficiently accurate continuous minimization.
The statement, precision convention, and Sections 3--4 were inspected.
This is substantial prior for oracle reductions to MILP. The present
audit does not claim a fresh uniform Turing FPT bound from that source's
fixed-dimensional formulation. It also does not substitute that source
for the independently audited Hildebrand--Köppe interface.

## Radius, gap, and exactness are established quantitative ingredients

**Basu--Roy already give the required dependence on the implicit row
count.** In
[*Bounding the radii of balls meeting every connected component of
semi-algebraic sets*](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
Theorem 4 gives a ball meeting every connected component. Theorem 3
instead contains every bounded component. Their displayed formulas imply
`log R <= f(a,d)(tau+log(s+1)+1)` in dimension `a`, for coefficient bits
`tau` and `s` polynomials. Thus exponentially many Farkas rows need not
make the required radius have exponentially many bits. These two
theorems must not be interchanged: a ball meeting a reciprocal-value set
does not bound its largest reciprocal. The primary formulas and Remark 1
were inspected. Remark 1 credits prior asymptotic radius bounds; no new
general radius theorem should be claimed here.

**Jeronimo--Perrucci--Tsigaridas supply an alternative positive-value
bound.**
[*On the minimum of a polynomial function on a basic closed semialgebraic
set and applications*](https://mate.dm.uba.ar/~perrucci/On_the_minimum_pol_funct.pdf),
Theorem 1, treats a compact connected component defined by arbitrary
polynomial equalities and weak inequalities. For a nonzero polynomial
minimum it gives an explicit lower bound whose negative logarithm is
`f(a,d)(log H+log(s+1))`. The row count enters through
`max(H,2a+2s)`. Applying this to a projected, boxed violation epigraph
is an application of their theorem, including its allowance for singular
and nonconvex algebraic descriptions. The theorem and introduction were
read from the saved primary text. It does not provide an algorithm for
an implicitly listed family.

**Khachiyan--Porkolab provide the integer size theorem, not a free
implicit-description algorithm.**
[*Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Theorem 1.1, bounds an optimal integer point's bits using the degree,
coefficient length, and quantifier-block dimensions, independently of the
number of predicates. Theorem 1.2's algorithm depends polynomially on
the explicit formula size with a dimension-dependent exponent. The
[earlier primary-source audit](common-range-fpt-prior.md) inspected both
statements and their conventions. Consequently their size theorem can
bound `z` after Farkas projection and quantification over `u`; their
algorithm cannot be applied to an exponential row list without charging
for that list. The polynomial extension must retain this distinction.

## Recent convex polynomial work and adjacent special cases

Slot--Steurer--Wiedmer,
[*Hesse's Redemption: Efficient Convex Polynomial Programming*](https://arxiv.org/abs/2511.03440),
Theorem 1.1 and Corollary 1.2, give polynomial solution bounds and
polynomial-time approximation for a convex polynomial objective over a
rational polyhedron, even in variable dimension. Theorem 1.3 decomposes
a convex polynomial into a linear part and a polynomial on a rational
subspace with a controlled quadratic lower bound. These statements and
the input encoding were read in the primary v1 manuscript; the arXiv
version history was checked on the audit date. This is stronger than the
candidate for its objective-over-polyhedron setting, but it does not
cover an arbitrary number of convex polynomial inequality constraints
or exact zero-residual feasibility. Identifying and removing affine
directions is therefore not a new general principle attributable to the
candidate.

De Klerk--Laurent,
[*On the Lasserre Hierarchy of Semidefinite Programming Relaxations of
Convex Polynomial Optimization Problems*](https://homepages.cwi.nl/~monique/files/convex_pop_hierarchy4.pdf),
Section 4.2, explicitly discusses ellipsoid approximation given a radius
and polynomial evaluation/gradient access. Its analysis there is in the
real-number model and keeps the radius and requested tolerance visible.
It does not resolve the candidate's exact bit-complexity question.
Their finite-convergence theorems for SDP hierarchies have additional
regularity assumptions; finite convergence alone is not a uniform exact
algorithm. The assumptions and Section 4 were inspected.

Del Pia's one-convex-quadratic-row result remains a stronger comparator
for that special case: arbitrary continuous rank is permitted with FPT
parameter only the integer dimension. The precise scope and primary
Proposition 4 comparison are recorded in
[the quadratic range audit](common-range-fpt-prior.md). The current
polynomial proposal must derive its additional significance from multiple
polynomial constraints and the bound on their common nonlinear directions.

## Assessment and audit limits

The useful potential advance is a parameterized exact decision theorem
that tolerates a large linear continuous model, without requiring a
supplied feasibility margin or radius. It could justify exact termination
criteria and decomposition methods for models with few nonlinear
continuous decisions. Solver speedups do not follow from this bound;
the parameter factor and the required precision may be large.

The proposed contribution does not include a new ellipsoid method, a new
Lenstra method, or new general semialgebraic radius and separation bounds.
Nor does this audit establish exact optimizer output, attainment
classification, or practical running times. The implicit oracle deduction
makes the result closer to a structural consequence of known machinery
than a fundamentally new optimization algorithm. Whether that consequence
has already appeared in an equivalent formulation remains unsettled.

Searches covered fixed nonlinear variables, few nonlinear directions,
partially linear convex programming, implicit convex programming,
polynomial separators, projected convex polynomial systems, exact
feasibility, and parameterized integer convex optimization. Broader
low-rank objective and separable convex results were checked for scope
but are not treated as matching theorems. An unsuccessful search is not
evidence of priority.

Primary local texts reused were `common-range-prior-sources/toledo.txt`,
`common-range-prior-sources/hildebrand-koppe.txt`, the Basu--Roy text in
`../research-20260925/publication-sources/`, and the JPT and SSW texts in
`nonconvex-prior-sources/`. Newly saved primary copies are in
`polynomial-dimension-prior-sources/`. The Oertel--Wagner--Weismantel
manuscript was inspected through the web PDF reader; direct download
returned HTTP 403. An independent subauditor also inspected the relevant
Norton--Plotkin--Tardos, Toledo, and Hildebrand--Köppe passages. These
checks support the comparisons, not the complete candidate theorem.

Only targeted document checks were run: final newline, trailing
whitespace, control characters, and local Markdown link existence. No
project-wide verification, CI inspection, numerical experiment, or Lean
formalization was performed for this literature audit.
