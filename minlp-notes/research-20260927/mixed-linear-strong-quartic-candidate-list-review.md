# Independent review of mixed-linear quartic candidate lists

Date: 2026-09-28. Reviewer: `mixed_linear_final_review`, assigned after
the proof was written. A separate fresh reader,
`mixed_linear_source_check`, checked the two approximation and
initialization imports. Neither reviewer developed the submitted proof.

Reviewed note: [mixed-linear-strong-quartic-candidate-list.md](mixed-linear-strong-quartic-candidate-list.md),
initial SHA256
`40f4a7ccdb8b2ebd12ba26cad6cc964ed07051275b9b996434960900bdc34c0a`.

**Finding.** The constrained-fiber residual construction is correct,
including deficient-dimensional polyhedra, redundant constraints, and
unbounded sets of optimal multipliers. The resulting ordinary FPT list
contains every optimal integer block. No substantive correctness or
uniform FPT accounting gap was found. One routine edge clarification
was requested and incorporated: after initial feasibility, return the singleton empty
integer vector directly when the integer dimension is zero. The imported
positive-dimensional integer-query algorithm is then unnecessary.

## 1. The primal-dual inequality

I derived the inequality independently. Put
\(d_z=w-z\), \(d_y=v-\widehat y\), and use the notation
\(s,r_y,q,E\) from equation (7) of the note. Feasibility gives

\[
 \lambda^{\mathsf T}(A d_z+B d_y)\le\lambda^{\mathsf T}s.
\]

Consequently the linear term in the joint strong-convexity inequality
is bounded below by

\[
 q^{\mathsf T}d_z+r_y^{\mathsf T}d_y-\lambda^{\mathsf T}s.
\]

Completing the square in \(d_y\) gives precisely

\[
 f(w,v)\ge f(z,\widehat y)+q^{\mathsf T}d_z
       +\frac\mu2\|d_z\|^2-E.
\]

The substitution \(f(z,\widehat y)\ge g(z)\) has the correct
direction. Taking the other fiber minimum therefore proves the claimed
bound on \(g(w)-g(z)\). If \(w,z\) are distinct integer points,
\(\|d_z\|^2\ge1\), so \(E\le\mu/4\) leaves the stated
quadratic margin. This retains every other no-worse integer block,
including exact ties. It does not require an extension or differentiability
of the projected value function. A zero normal gives a unique optimal
integer block, rather than merely a stationary point of a continuous
extension.

## 2. Small residuals without bounded multipliers

The coercive radius, polynomial derivative bounds, and choice of
\(\delta\) are valid. In particular, coefficient-sum bounds give
each Hessian entry at most \(12CS^2\) in magnitude; its operator
norm is at most \(12mCS^2<K\). The analogous gradient bound is
smaller than \(G\). Strong convexity and the constrained first-order
inequality convert the feasible objective approximation to distance
at most \(\delta\), even when the minimizer is on the boundary.

The normal cone of a polyhedron at a feasible point is the cone generated
by its active inequality normals. This is valid on a deficient-dimensional
polyhedron and needs no Slater point. Hence the multiplier
\(\lambda_*\) in (16) exists, although it need not be rational or
unique. Stationarity and complementary slackness give

\[
 \lambda_*^{\mathsf T}(c-Az-B\widehat y)
 =\nabla h(p)^{\mathsf T}(\widehat y-p).
\]

The right side is nonnegative by constrained optimality and is at most
\(G\delta\). This identity is the reason that large multiplier norms
do not enter the precision budget. The gradient residual is at most
\(K\delta\). Thus the two terms of \(\mathcal E(\lambda_*)\)
are bounded by \(\mu/16\) and \(\mu/32\), respectively. An
additive \(\mu/8\) approximation to its minimum has residual at
most \(7\mu/32<\mu/4\). All arithmetic is rational at this stage.

There is no hidden attainment assumption in this residual quadratic
program. An elementary independent argument is useful. With
\(a=\nabla h(\widehat y)\), its image cone is

\[
 C_B=\{(B^{\mathsf T}\lambda,s^{\mathsf T}\lambda):
                                  \lambda\ge0\}.
\]

It is a closed polyhedral cone with second coordinate \(t\ge0\).
The objective becomes \(t+\|a+u\|^2/(2\mu)\). Its sublevel at
the value of \(\lambda=0\) is nonempty and compact in \((u,t)\),
so a minimizer exists and lifts to some nonnegative multiplier. Neither
rank of \(B\) nor a bound on the lifting multiplier is needed.

The case with no continuous variables needs only the exact rational
integer-block gradient, as stated in the note. Zero rows of \(B\),
opposite inequalities representing equalities, and an empty constraint
system cause no change to the argument.

## 3. Primary-source contracts and uniform size bounds

Both reviewers directly read
[Del Pia v2, Theorem 3 and its definition of accurate solution](https://arxiv.org/html/2311.00099v2#S4).
The theorem permits the zero quadratic objective and arbitrary rational
mixed linear constraints, with the integer dimension as its FPT
parameter. A feasible instance then has an attained finite optimum, and
the algorithm returns a feasible point. Proposition 4 also explicitly
provides a witness and handles unboundedness and deficient dimension.
The constructions use rational arithmetic and deterministic routines.
This is sufficient for the stated initialization; no exact nonlinear
optimization is hidden there.

Both reviewers directly read
[Slot--Steurer--Wiedmer v1, Corollary 1.2 and Appendix D](https://arxiv.org/html/2511.03440v1).
The approximation theorem permits nonempty unbounded and deficient-
dimensional rational polyhedra. Appendix D works in the bit model,
returns an exactly feasible rational point, and uses a rational affine-
hull reduction. Only objective accuracy is relaxed. The fiber objective
is coercive, and the residual quadratic objective is nonnegative on its
orthant, so neither call is unbounded below. The printed omission of
convexity from Proposition 3.2 does not affect this application: the
well-stated Corollary 1.2 is used and both objectives are convex. An
implementation can replace any requested error by its minimum with one
without weakening the proof.

Fixed degree four makes substitution of the queried integer vector and
evaluation of the rational approximate point polynomial in their binary
encodings. The residual quadratic objective has polynomially many
coefficients in the number of input rows; its coefficients have polynomial
bit length. Its algorithmic size depends on these rational data, not on
the unknown exact multiplier used only in the existence proof.

The first witness has length \(a_0(k)L^{C_0}\), which gives the
same form of bound for the integer radius. Every subsequent oracle
answer costs a fixed polynomial in the original data, radius encoding,
and original-coordinate query length. Substitution into the inherited
integer-query bound preserves \(a(k)L^C\) with absolute \(C\).
There is no polynomial exponent recursively composed through integer
dimension reductions.

I directly checked
[Ari--Hildebrand v2, Definition 3.4 and Theorem 3.5](https://arxiv.org/html/2609.18266v2#S3.SS3):
it permits arbitrary closed convex targets in the box, strict rational
integer-query separators, empty targets, and original-coordinate queries.
Its polynomial degree is absolute. The earlier
[independent FPT review](fixed-integer-strong-quartic-fpt-independent-review.md)
and [source audit](integer-query-convex-oracle-prior.md) remain dependencies
for the complete underlying lattice and ellipsoid algorithm. This review
does not reprove that algorithm.

## 4. The list and its exact-selection limitation

All returned inequalities are strict separators for their query and
are valid for the fixed empty set. Completing the oracle arbitrarily at
a zero-normal early stop makes the actual run a prefix of a valid
empty-set execution. Termination is therefore established before an
optimal candidate is assumed to exist in the list.

For any omitted optimal block \(w\), hardcode membership acceptance
only at \(w\). Every domain separator retains it, and every other
feasible query yields a cut retaining it by the no-worse integer margin.
A zero normal at a different query is impossible. This total singleton
oracle has the same uniform answer bound and would produce the identical
transcript, contradicting an emptiness verdict. The argument handles
ties and infeasible queried fibers. The parity proof that there are at
most \(2^k\) optimal blocks is also correct.

The theorem outputs feasible integer blocks, not their ordering by
constrained fiber value. General constrained quartic comparison is not
silently identified with the unconstrained PosSLP theorem. The discussion
of nonadaptive exact-selection queries keeps that dependency explicit.
The main significance is an ordinary FPT discrete candidate search
despite an arbitrary-dimensional continuous block and mixed linear
constraints. Actual exact selection and practical performance require
additional results or algorithms.

The novelty qualifications are appropriate. Integer-query geometry,
optimization without bisection, Lagrangian lower bounds, and convex
quadratic optimization are established ingredients. The quantitative
constrained-fiber combination is the proposed application. These source
checks are not an exhaustive review of inexact Benders methods or value-
function oracles and do not establish priority.

## 5. Exact computational challenges

The independent script
[check_mixed_linear_candidate_review.py](check_mixed_linear_candidate_review.py)
uses exact fractions for explicit strongly convex quartics in one integer
and one continuous variable. The multiplier quadratic programs are
solved by rational candidate enumeration and accepted only after full
orthant KKT verification. Examples include unbounded fibers, equality
fibers, redundant constraints, narrow feasible intervals, infeasible
fibers, and scaled active normals that force very large multipliers.

Command actually run:

```text
python research-20260927/check_mixed_linear_candidate_review.py
```

It passed 4,240 residual certificates and complementary-slackness
identities, 26,480 full primal-dual inequalities, 22,240 integer margin
checks, and 1,360 Farkas certificates. These include 1,160 no-worse
cuts at exact ties, 224 zero normals, and 185 certificates with an
optimal multiplier exceeding \(2^{200}\). A separate one-dimensional
integer separation simulation passed 540 nonempty instances with 1,410
queries, including 138 tied-optimum instances and 168 early stops;
another 60 instances were empty. Every optimal block was retained.

The finite tests challenge signs, degeneracies, ties, and the absence
of a multiplier-norm factor. They do not prove the general theorem,
implement the cited high-dimensional FPT routine, or measure practical
performance. No Lean formalization, project-wide checks, or CI inspection
was performed.

A targeted Python check passed for this review and its checker: final
newlines, trailing whitespace, balanced Markdown math delimiters, and
all four local links. The following targeted command also passed:

```text
git diff --check -- research-20260927/mixed-linear-strong-quartic-candidate-list-review.md research-20260927/check_mixed_linear_candidate_review.py
```

## 6. Final amendment check

The final main note was independently read in full at SHA256
`9c4a69a9527d498c8ca79ad8bb781fd26aedc311735a01c3e02174187ec7f448`.
It includes the explicit zero-integer-variable dispatch, the independent
residual-QP attainment argument, and accurate review and testing limits.
The author separately rechecked both mathematical additions. The
changes correctly preserve the theorem and its exact-selection scope;
the review is closed with no remaining correctness objection.
