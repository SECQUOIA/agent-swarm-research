# Prior work for constrained exact arithmetic extensions

Date: 2026-10-03. Scope: the new low-nonlinear-dimension, structured-box
Newton and separable-flow results. This source comparison does not replace
their mathematical reviews or establish publication priority.

Two different extensions are involved. The
[nonlinear-dimension theorem](../constrained-exact/theorem.md) proposes
ordinary fixed-parameter tractability of exact optimizer predicates for
arbitrary rational polyhedra, parameterized by the essential-variable
dimension of the cubic and quartic part. The
[Newton transfer theorem](../constrained-exact/structural-newton.md)
instead permits unrestricted nonlinear dimension and gives
\(\mathrm P^{\mathrm{PosSLP}}\) when every exact Taylor QP has a suitably
bounded arithmetic algorithm. Its current specializations cover forest
Hessian interactions or nonpositive off-diagonal Hessian entries over
boxes, and [separable polynomial network flows](../constrained-exact/network-flow.md).

## Essential variables and algebraic degree

Enrico Carlini,
[*Reducing the Number of Variables of a Polynomial*](https://arxiv.org/pdf/math/0507531),
Proposition 1, identifies the essential-variable dimension of a
homogeneous polynomial with the rank of its first catalecticant. It also
identifies the essential-variable space using derivatives of order one
less than the degree. The coefficient-matrix extraction in the present
quartic theorem is the degreewise adaptation to the cubic and quartic
homogeneous pieces. The rank construction should be credited as existing
algebraic structure. Carlini's proposition does not concern constrained
optimization, active sets or exact sign complexity.

Jiawang Nie and Kristian Ranestad,
[*Algebraic Degree of Polynomial Optimization*](https://arxiv.org/pdf/0802.1233),
Theorem 2.2, gives a generic algebraic-degree formula for polynomial
optimization with specified equality degrees. Its nongeneric upper-bound
statement assumes a zero-dimensional critical system. Corollary 2.5
treats inequality constraints after the active inequalities have been
identified. Section 3.1 specializes to the familiar unconstrained degree
bound \((d-1)^n\).

Those results explain why reducing the number of algebraically nonlinear
variables matters. They do not, by themselves, give the present
coefficient-height bound or an algorithm that avoids guessing the active
face. Strong convexity ensures one real stationary point, but does not
ensure that the full complex critical locus is zero-dimensional. The
real-projection quantifier-elimination argument retained in the new proof
handles that distinction. It should not be replaced by an unqualified
application of a generic algebraic-degree formula.

The proposed additional statement is therefore the complete ordinary
\(F(k)L^C\) exact-sign algorithm, including arbitrary linear constraints,
zero observables and recovery of the full active set. Essential-variable
extraction, quadratic elimination and the real-algebraic separation tool
are ingredients with established antecedents.

## Low-rank optimization is not one uniform problem class

Shashi Mittal and Andreas S. Schulz,
[*An FPTAS for Optimizing a Class of Low-Rank Functions over a Polytope*](https://web.mit.edu/schulz/www/epapers/ms-mp-2013.pdf),
Definition 1, uses a whole objective of the form
\(f(x)=g(a_1^Tx,\ldots,a_k^Tx)\). Theorem 2 gives an approximation
scheme under its Conditions 1--3. The Section 3.2 runtime contains
\((\log(M/m)/\varepsilon)^k\) times a linear-programming cost.

This is a different guarantee and parameter. In the present theorem the
quadratic part may have full rank; only terms of degree at least three
must use few directions. Exact zeros of observables are part of the
required output. Polynomial time for each fixed rank with an exponent
depending on rank is also distinct from the claimed \(F(k)L^C\) bound
with an absolute input-length exponent.

Ravi Kannan and Luis Rademacher,
[*Optimization of a Convex Program with a Polynomial Perturbation*](https://www.math.ucdavis.edu/~lrademac/fplusp.pdf),
Theorem 4, is a closer structural predecessor: a convex objective plus a
polynomial depending on \(k\) variables over a convex body. Its
approximation guarantee uses a number of optimization calls proportional
to \((O(kd^2/\sqrt\varepsilon))^k\), with error scaled by the polynomial's
range. This already exploits a small nonlinear part with convex
recourse. Its reciprocal-accuracy dependence does not yield the present
exact-zero test by simply requesting the algebraic-separation precision.
The new theorem uses strong convexity and elimination on the unknown
optimal face to obtain a different precision bound and computation model.

## Quadratic convergence of constrained Newton steps is prior

Jason D. Lee, Yuekai Sun and Michael A. Saunders,
[*Proximal Newton-Type Methods for Minimizing Composite Functions*](https://stanford.edu/group/SOL/multiscale/papers/14siopt-proxNewton.pdf),
Theorem 3.4, printed page 1431, proves

\[
 \|x_{j+1}-x_*\|\leq\frac{L_2}{2m}\|x_j-x_*\|^2
\]

for exact proximal Newton refinement under strong convexity and
Lipschitz Hessian assumptions. Section 3.2 explains the local nature of
the required bounds. Taking the nonsmooth term to be the indicator of
the feasible polyhedron gives the exact constrained Taylor-QP step used
here. The theorem does not need strict complementarity. Its numerical
convergence guarantee does not itself bound the cost of executing every
exact QP on short arithmetic-circuit coefficients.

The new transfer statement combines this prior recurrence with an
arithmetic-operation bound for the quadratic subproblems and a separation
bound for the original polynomial instance. Its sign-test branches are
adaptive, so the justified complexity is a polynomial-time Turing
reduction to PosSLP. A single final many-one instance is not established.
Removing active-set identification from the convergence analysis is not
itself a new Newton result.

## Exact box and flow quadratic subroutines are prior

Jong-Shi Pang and Shaoning Han,
[*Some Strongly Polynomially Solvable Convex Quadratic Programs with
Bounded Variables*](https://optimization-online.org/wp-content/uploads/2021/12/arxiv.pdf),
Algorithm I and Proposition 2.1, give at most \(2n\) pivots when a
positive admissible vector satisfies the specified principal-inverse
inequalities. The text explicitly permits degeneracy. The displayed
algorithm uses arithmetic, linear systems and comparisons. Proposition
4.2(a) treats tridiagonal matrices through their comparison matrices, and
Section 6.1 gives the specialized quadratic operation bound. Their
comparison-matrix framework also explains the admissible-vector
construction used for the forest case in the new note. The new proof
must verify its admissible vector for each Hessian; positive
definiteness alone is not enough to invoke Proposition 2.1.

László A. Végh,
[*A Strongly Polynomial Algorithm for a Class of Minimum-Cost Flow
Problems with Separable Convex Objectives*](https://doi.org/10.1137/140978296),
Theorem 20, printed page 1753, supplies exact quadratic-cost flow
optimization with \(O(m^4\log m)\) operations for capacitated instances.
The model on page 1729 explicitly permits arithmetic and comparisons.
Section 6.1 implements the quadratic case by rational linear systems and
parametric search, then verifies the rational bit-size property. The
downloaded [author PDF](https://personal.lse.ac.uk/veghl/papers/vegh-quadratic.pdf)
was read locally for these details.

The new use is to retain the quadratic subroutine's arithmetic values as
shared circuits and answer comparisons through PosSLP, then iterate
constrained Newton. The ordinary polynomial bound on printed rational
QP output must not be applied to circuit input as if its expanded
coefficients were small. Conversely, the source's discussion of barriers
to strongly polynomial nonquadratic flow optimization does not contradict
an oracle algorithm whose complexity depends on the original input bit
length.

The structured quartic results should be presented as consequences of
this arithmetic composition with classical subroutines. They neither
introduce strongly polynomial box/flow QP nor classify arbitrary
constrained quartics. A strongly polynomial QP algorithm is a sufficient
input interface here; this audit asserts no equivalence between the
remaining general quartic problem and strongly polynomial QP.

## Audit record

The essential-variable, algebraic-degree and low-rank approximation
theorem passages were independently inspected by a delegated source
reviewer. The proximal Newton, Pang--Han and Végh passages were read
directly for this note, including their computational models. Bibliographic
metadata is recorded in the continuation's shared bibliography.

The targeted searches considered essential variables, catalecticant rank,
low-rank polynomial objectives, algebraic degree, proximal Newton, exact
box QP and separable quadratic flows. These comparisons identify direct
antecedents and input/output differences. They do not establish that no
equivalent theorem exists elsewhere.

A scoped Python document check verified final newline, trailing
whitespace and local links. `git diff --check --
research-20261003-arithmetic/literature/constrained-prior.md` passed.
No project-wide verification or CI inspection was run.
