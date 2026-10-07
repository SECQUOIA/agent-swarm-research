# Exact box QP with a small feedback vertex set

Date: 2026-10-02. Status: a mathematical derivation with fresh independent
review and targeted rational checks recorded below. The disjoint-path
case is self-contained. The forest extension uses a separately audited
exact polynomial-bit forest-QP theorem. No external search was performed
for this derivation, and no novelty claim is made. The result removes
occurrence dependence for a supplied small feedback vertex set. It does
not settle the corresponding question for every bounded-treewidth graph.

## Result

Let

\[
 F(x)=\tfrac12x^TAx+b^Tx+c
\]

be a rational quadratic on a nonempty rational box. Suppose a supplied
coordinate set \(C\), of size \(r\), leaves a forest in the interaction
graph when deleted. Thus \(C\) is a supplied feedback vertex set.
Assume a unique minimizer \(x^*\) and global quadratic growth

\[
 F(x)-F(x^*)\ge g\|x-x^*\|_2^2 \qquad (x\in X), \quad g>0.
 \tag{1}
\]

Put \(L=\max(0,\max_{i\in C}A_{ii})\). If \(L>0\), put
\(\kappa=\max(1,L/g)\). There is an algorithm returning a feasible
rational point and a certified objective gap at most \(2^{-q}\) in

\[
 f(r,\kappa)(I+q+1)^K
 \tag{2}
\]

bit operations, where \(K\) is an absolute constant. There is also an
exact algorithm for a global optimizer and the optimum value in
\(f_1(r,\kappa)(I+1)^{K_1}\) bit operations. Neither algorithm needs
\(g\) or \(\kappa\) as input. Here \(I\) is the binary input length,
including the core. A global Hessian bound \(\|A\|_2\le H\) gives
\(L\le H\), so these are also FPT bounds in \((r,H/g)\).

For \(L=0\), evaluating the \(2^r\) core-box corners and solving each
residual forest problem gives an exact optimum without a growth promise.
For \(r=0\), the residual forest algorithm alone solves the whole problem.
Fixed coordinates are substituted out first.

In fact the full-vector uniqueness and growth assumption (1) can be
weakened: it is enough that the core value function
\(v(h)=\min_zF(h,z)\) has a unique minimizer \(h^*\) and satisfies
\(v(h)-\min v\ge g\|h-h^*\|^2\). The residual optimum at \(h^*\)
may be nonunique or contain a continuum. The same algorithm and parameter
bound return one exact global optimizer. The proof below identifies where
this weaker assumption suffices.

For box quadratics, uniqueness of the optimal core automatically implies
that some positive projected growth constant exists, as proved below.
Thus the exact algorithm terminates on every instance with a unique
optimal core. Its FPT bound depends on the numerical ratio \(L/g\),
which need not be small merely because the core optimum is unique.

The checked [mixed-core extension](mixed-core-extension.md) permits any
core coordinates to range over large binary-encoded integer intervals,
while the residual forest remains continuous. It gives the same FPT
input and accuracy exponents using nested integer ranges and continuous
intervals; integer interval cardinalities are not enumerated.

Deleting the universal hub of a fan leaves a path, so \(r=1\), while
the usual path decomposition contains the hub in arbitrarily many bags.
Deleting a clique of \(r\) universal hubs joined to a path leaves the
path; its treewidth is \(r+1\) when there are at least two path vertices.
Consequently (2) has parameter dependence on width and conditioning for
these families, with no variable-occurrence parameter. The core need not
be a clique for the theorem.

More generally, the proof applies whenever fixing the core permits an
exact rational residual optimization algorithm of uniform polynomial bit
complexity. An algorithm trace can supply lower-bound evidence if the
oracle has no separate certificate format. The disjoint-path case below
provides such an algorithm directly.

For general forests, the required exact Turing-model oracle is supplied
by Del Pia and Khajavirad's forest box-QP theorem. The separate
[local prior-art audit](../prior-art/geometric-grid-prior.md) checked the
standard Turing-model definition, the polynomial encoding-length
requirement in the definition of strong polynomiality, rational optimizer
output in Lemma 19, and the final encoding-length argument in Section 2.4
of the [primary source](https://arxiv.org/html/2609.35595v1). The present
argument uses this exact rational oracle, not a unit-cost real-arithmetic
interpretation of it. The self-contained path proof below is sufficient
for fans and clique-hubset-plus-path graphs regardless of that citation.

## Exact rational optimization on a path

Consider the rational path objective

\[
 P(z)=\sum_{i=1}^n u_i(z_i)+\sum_{i=1}^{n-1}e_i z_i z_{i+1},
 \tag{3}
\]

where each \(u_i\) is quadratic and each \(z_i\) lies in a rational
interval. Fixing rational core coordinates changes only the unary linear
and constant coefficients, and their bit lengths remain polynomial in the
input and in the core point's bit length.

Choose an optimizer of (3) with as many coordinates at their bounds as
possible. Every maximal interval of its strictly interior coordinates
has a positive-definite principal Hessian. Indeed, the Hessian on all free
coordinates is positive semidefinite by second-order necessity. If one
of its interval blocks were singular, a nonzero null direction supported
on that interval would have zero linear and quadratic objective change.
Moving along that direction until another coordinate reaches a bound
would preserve the objective and increase the number of bound
coordinates, a contradiction.

Construct a directed acyclic graph with vertices \((i,s)\), where
\(i\in\{1,\ldots,n\}\) and \(s\) is either bound of coordinate
\(i\), together with sentinels \(0,n+1\). An arc from \((i,s)\) to
\((j,t)\), \(i<j\), asserts that \(i+1,\ldots,j-1\) are free.
Sentinels omit the corresponding endpoint. For every such arc:

1. Require the Hessian on \(i+1,\ldots,j-1\) to be positive definite.
   An empty block passes this test.
2. Solve its stationary equations with the two indicated endpoint values.
3. Retain the arc if the resulting free coordinates lie in their closed
   box intervals. Allowing a solution to reach a bound is harmless.
4. Give the arc the objective contribution of its interior unaries, all
   path edges between the indicated endpoints, and the right endpoint's
   unary when the right endpoint is not a sentinel.

Every source-to-sink path describes a feasible original point, and its
arc weights sum to the objective exactly. Each unary and each edge is
counted once. Conversely, the maximal-boundary optimizer just selected
defines such a path. A shortest path therefore returns an exact global
optimizer. There are \(O(n)\) vertices and \(O(n^2)\) arcs; every
positive-definiteness test, linear solve, and rational comparison has
uniform polynomial bit cost. Fraction-free elimination or determinant
height bounds justify this statement without assuming unit-cost rational
arithmetic. All solved matrices have size at most \(n\) and coefficient
bit length polynomial in the supplied slice.

Independent path components can be solved separately. This proves the
residual oracle used in (2), including exact rational output. A checker
can regenerate every arc, verify its rational solve, and verify the
shortest-path values. The oracle does not require a growth condition,
uniqueness, or a positive-definite full Hessian.

## Curvature survives minimization of the other coordinates

Write \(x=(h,z)\), with \(h=x_C\), and define

\[
 v(h)=\min_z F(h,z),\qquad v^*=F(x^*).
\]

Compactness makes this minimum attainable. The core minimizer \(h^*\)
is unique and

\[
 v(h)-v^*\ge g\|h-h^*\|_2^2.
\tag{4}
\]

The remainder of the proof uses only (4) and uniqueness of \(h^*\).
The stronger assumption (1) supplies them directly but is not otherwise
needed.

For each fixed \(z\), the function
\(F(h,z)-\tfrac12h^TA_{CC}h\) is affine in \(h\). Therefore

\[
 \phi(h)=v(h)-\tfrac12h^TA_{CC}h
 \tag{5}
\]

is concave: it is the pointwise infimum of affine functions. This does
not assert that \(v\) is differentiable or that residual optimizers vary
continuously with \(h\).

For a core box \(B=\prod_i[a_i,b_i]\), let
\(w_i=b_i-a_i\) and

\[
 \delta_B=\tfrac18\sum_{i\in C}\max(A_{ii},0)w_i^2,
 \qquad
 m_B=\min_{a\in\operatorname{vert}(B)}v(a).
 \tag{6}
\]

Then

\[
 v(h)\ge m_B-\delta_B\qquad(h\in B).
 \tag{7}
\]

To prove this, express \(h\) as the expectation of a random corner
\(Y\), independently rounding each coordinate to its two endpoints.
Concavity in (5) gives

\[
 \begin{aligned}
 v(h)&\ge \mathbb E v(Y)
       -\tfrac12\sum_i A_{ii}(h_i-a_i)(b_i-h_i)\\
     &\ge m_B-\delta_B.
 \end{aligned}
 \tag{8}
\]

The off-diagonal terms cancel because the corner coordinates are
independent. Thus only positive diagonal core curvature enters the
bound. In particular, if all core diagonals are nonpositive, (7) with
\(\delta_B=0\) proves the exact corner algorithm claimed above.

## Unique optimal cores have positive projected quadratic growth

**Lemma.** Suppose that all global optimizers of a quadratic on a compact
box have the same core coordinates \(h^*\). Then there is a constant
\(g>0\) such that

\[
 v(h)-v^*\ge g\|h-h^*\|^2
\]

on the core box. No rationality assumption is needed for this qualitative
statement.

*Proof.* For each fixed core value \(h\), choose a residual optimizer
with the maximum possible number of bound coordinates. The Hessian on
its free residual coordinates is positive definite. It is positive
semidefinite by second-order necessity, and a nonzero null direction
would preserve the objective until an additional coordinate reaches a
bound, contradicting the selection rule.

There are finitely many residual face patterns. For each pattern whose
free principal Hessian is positive definite, the stationary equations
give an affine residual point \(z_j(h)\). The requirement that this
point lie in its box, together with the core bounds, defines a closed
polytope \(D_j\). The empty free set is allowed. Omit empty domains.
The function

\[
 q_j(h)=F(h,z_j(h))
\]

is quadratic, is at least \(v^*\) on \(D_j\), and can equal
\(v^*\) only at \(h^*\). Every residual optimum selected above is
one of these candidates. Hence

\[
 v(h)=\min_{j:\ h\in D_j}q_j(h).
\]

If \(\min_{D_j}q_j>v^*\), compactness supplies a positive objective
gap. Dividing that gap by the maximum squared distance from \(h^*\)
on \(D_j\) gives a positive quadratic-growth bound for this piece.
A domain consisting only of \(h^*\) imposes no restriction on the
growth constant.

Otherwise \(h^*\) is the unique minimizer of \(q_j\) on \(D_j\).
A quadratic with a unique minimizer on a compact polytope has positive
quadratic growth there. To see this directly, suppose there were points
\(h_k\ne h^*\) with

\[
 \frac{q_j(h_k)-q_j(h^*)}{\|h_k-h^*\|^2}\longrightarrow0.
\]

Compactness and uniqueness imply \(h_k\to h^*\). Set
\(t_k=\|h_k-h^*\|\) and, along a subsequence,
\(u_k=(h_k-h^*)/t_k\to u\), with \(\|u\|=1\). Write
\(a=\nabla q_j(h^*)\) and let \(B_j\) be its Hessian. The segment
from \(h^*\) to \(h_k\) is feasible, so \(a^Tu_k\ge0\).
The exact expansion

\[
 \frac{q_j(h_k)-q_j(h^*)}{t_k^2}
 =\frac{a^Tu_k}{t_k}+\tfrac12u_k^TB_ju_k
\]

therefore implies \(a^Tu=0\) and \(u^TB_ju\le0\). The
polyhedral tangent cone is closed, so its direction \(u\) gives a
feasible short ray \(h^*+tu\). Optimality on this ray gives
\(u^TB_ju\ge0\). Equality follows, and the quadratic expansion
makes the whole short ray optimal, contradicting uniqueness.

Each of the finitely many pieces consequently has a positive growth
constant relative to \(v^*\). Their minimum and the finite
representation of \(v\) prove the lemma.
QED.

The face patterns are used only in this existence proof. The algorithm
does not enumerate them or compute this growth constant. The lemma
provides eventual termination, while the quantitative parameter
\(\kappa\) controls the useful runtime guarantee.

## Levelwise box refinement and its count

Assume \(L>0\), and let \(s\) be the largest core-box side length.
At level \(j\), put \(h_j=s2^{-j}\). Use the lattice of intervals
of length \(h_j\), anchored at each original lower bound, and clip the
last interval to the original upper bound. These partitions are nested.
Every box has side lengths at most \(h_j\), and every parent has at
most \(2^r\) children. This isotropic construction avoids dependence on
the aspect ratio of the original box.

At level zero there is one box. At each level evaluate every corner of
every generated box with the exact residual oracle, and let \(U_j\)
be the best feasible objective found so far. For each generated box use
the valid lower bound

\[
 \operatorname{LB}(B)=m_B-\delta_B.
\]

Discard boxes with \(\operatorname{LB}(B)\ge U_j\); refine all
remaining boxes at the next level. If no boxes remain, the incumbent is
exact. A discarded box always has a lower bound at least the current
incumbent, including after later improvements, so discarding is safe.

Put

\[
 \delta_j=\tfrac18 Lr h_j^2.
 \tag{9}
\]

Unless the exact optimum is already found, a generated box containing
\(h^*\) survives. Applying (8) at \(h^*\) in that box gives

\[
 0\le U_j-v^*\le\delta_j.
 \tag{10}
\]

For any retained box, choose a corner \(a\) attaining \(m_B\).
Its retention and (10) imply

\[
 v(a)<U_j+\delta_B\le v^*+2\delta_j.
\]

Consequently, (4) gives

\[
 \|a-h^*\|_2
 <h_j\sqrt{Lr/(4g)}.
 \tag{11}
\]

Each retained box therefore has a corner in this ball. In each
coordinate there are at most \(2R/h_j+3\) lattice endpoints inside an
interval of radius \(R\); the extra endpoint accounts for clipping.
Each corner belongs to at most \(2^r\) boxes. Hence the number of
retained boxes is at most

\[
 B(r,\kappa)=2^r\bigl(\sqrt{r\kappa}+3\bigr)^r.
 \tag{12}
\]

This bound holds at every level. Generating children and evaluating
their corners requires at most \(4^rB(r,\kappa)\) oracle calls per
level, apart from level zero. Reusing corner evaluations can improve
this count but is unnecessary for (2).

The global lower bound is the minimum of \(U_j\) and the lower bounds
of retained boxes. Since \(m_B\ge U_j\) for every generated box,
the resulting certified gap is at most \(\delta_j\). Thus

\[
 J=\max\left(0,\left\lceil\tfrac12
       \log_2\bigl(Lrs^2/(8\varepsilon)\bigr)\right\rceil\right)
 \tag{13}
\]

levels suffice for gap \(\varepsilon\). Powers of two can be compared
rationally instead of computing this logarithm. For
\(\varepsilon=2^{-q}\), \(J=O(I+q+1)\). At level \(j\), corner
coordinates have bit length \(O(I+j)\). Exact residual solves, values,
and lower bounds consequently have bit length polynomial in \(I+j\),
with a degree independent of \(r\). Equations (12)--(13) prove (2).

The algorithm never uses \(g\). Growth is used only in counting the
retained boxes. All lower bounds and the stopping test remain valid
without it. The certificate can contain the generated subdivision tree,
all corner oracle evidence, and the lower bounds used in discarding
boxes. Its size obeys the same FPT bound.

## Exact rational output without knowing the growth constant

Use the rational height bounds in
[`exact-box-qp.md`](../geometric-dp/exact-box-qp.md). They give explicit
integers \(R,V\) of polynomial bit length such that some global
optimizer has coordinate denominators at most \(R\), and the optimum
value has denominator at most \(V\). All global optimizers have the
same core \(h^*\) under the weaker assumption (4). Consequently its
core coordinates have denominator at most \(R\), even if residual
optimizers are nonunique.

Continue the same refinement run. Once the certified objective interval
has width less than \(1/(2V^2)\), reconstruct its unique rational of
denominator at most \(V\); it is \(v^*\). At this and each later
level, put \(\rho=1/(4R^2)\) and attempt to reconstruct, for every
incumbent core coordinate \(a_i\), a rational of denominator at most
\(R\) in \([a_i-\rho,a_i+\rho]\). There is at most one such rational.
If all exist and the reconstructed core lies in its box, solve its
residual problem exactly. Accept only if the resulting feasible
objective equals the already isolated value \(v^*\).

This acceptance test is sound independently of growth. It eventually
succeeds under (4): by (10),
\(\|a-h^*\|^2\le\delta_j/g\), so all reconstructions equal their
true coordinates once \(\delta_j/g<\rho^2\). This takes
\(\operatorname{poly}(I)+O(\log\kappa)\) levels. Every residual
optimizer returned at \(h^*\) gives a full global optimizer.
The rational reconstruction, final slice solve, and equality check have
uniform polynomial bit cost. This proves the exact FPT claim.

## A uniformly conditioned nonconvex fan

For integers \(m\ge2\) and \(n=m^2\), let \(h\in[-1,1]\), \(z_1\in[0,1]\), and
\(z_i\in[-1,1]\) for \(i\ge2\). Define

\[
 F(h,z)=h^2+z_1-\tfrac12z_1^2+\sum_{i=2}^n z_i^2
       +\tfrac14\sum_{i=1}^{n-1}z_i z_{i+1}
       +\frac{h}{4m}\sum_{i=1}^n z_i.
 \tag{14}
\]

Its interaction graph is a fan. The Hessian is indefinite because its
\(z_1z_1\) entry is \(-1\). All triangle edges have positive
coefficients, so a triangle cannot be transformed to all negative edges
by coordinate sign changes. Thus the complete graph is outside the
sign-switchable submodular class.

On the box, the unary terms in \(z\) dominate
\(\tfrac12\|z\|^2\); the path term is at least
\(-\tfrac14\|z\|^2\); and the hub term is at least
\(-\tfrac18(h^2+\|z\|^2)\). Therefore

\[
 F(h,z)\ge\tfrac78h^2+\tfrac18\|z\|^2.
\]

The unique minimizer is zero, with \(g=1/8\). All coordinates except
\(z_1\) are interior there. The path Hessian has norm at most \(5/2\),
and the hub coupling block has norm \(1/4\); hence
\(\|A\|_2\le11/4\), uniformly in \(n\). This gives
\(H/g\le22\), while the hub occurs in \(n-1\) usual path bags.
The new algorithm therefore has a uniform polynomial bit bound on this
family. This example illustrates the assumptions; its explicit optimum
does not itself constitute a difficult computational benchmark.

## Targeted validation

Only the path oracle, the core-box bound, and the displayed fan family
were in scope for local checks. No project-wide checks or CI inspection
were performed.

Commands actually run were `python - <<'PY'` for a SymPy version check
(version 1.14.0), followed by a second `python - <<'PY'` invocation
containing targeted inline exact-rational checks with seed 261002:

- 54 path instances: the interval-DAG oracle agreed with independent
  exhaustive active-face enumeration. The cases included an interior
  rational minimizer, a singular free Hessian with nonunique optima, an
  indefinite Hessian with a boundary optimum, and a three-vertex path
  with two bound endpoints and one free middle coordinate.
- 144 exact core-box lower-bound checks passed on random rational
  quadratics with one or two core coordinates and two residual
  coordinates. Residual values were obtained by independent active-face
  enumeration. The checks used interior points at one-quarter, one-half,
  and three-quarters of each side.
- 300 rational samples satisfied the displayed fan growth inequality
  for \(m=1,2,3\). The \(m=1\) samples test the inequality only; the
  non-sign-switchable fan illustration requires \(m\ge2\).

The inline check exited with status zero. These finite checks support
the formulas and implementation of the path oracle; the mathematical
proofs above supply the general statements. A fresh independent review
checked the lower bound, packing count, equality pruning, exact recovery,
uniform bit exponent, and path-cost bookkeeping. It found no substantive
gap and requested the now-applied restriction \(m\ge2\) for the
triangle-based example claim.

A final targeted `python - <<'PY'` invocation checked trailing whitespace,
paired inline and displayed math delimiters, and the two local source
links in this file; all passed. The scoped command
`git diff --check -- research-20261002/new-direction/fan-exploration.md`
also exited with status zero.

The parent agent separately checked the implemented refinement algorithm
in [`check_core_box_bb.py`](check_core_box_bb.py): 14 instances, 930 boxes,
and 855 oracle calls passed the per-level interval and mesh-gap checks.
Those cases include aspect ratio 1024, flat residual optima, and zero
positive core curvature. See the parent
[occurrence-free overview](occurrence-free-qp.md) for that run's record;
these are separate from the commands run for this note.

A further fresh review checked the qualitative unique-core growth lemma.
It confirmed the finite residual-face representation and the polyhedral
tangent-ray proof, including the empty-domain and singleton-domain cases.
No substantive gap was found.
