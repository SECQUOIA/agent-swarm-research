# Exact mixed-integer quartic optimization with few integer variables and low continuous constraint rank

Date: 2026-09-28. Status: proved and passed
[independent adversarial review](mixed-quartic-integer-constraint-rank-oracle-review.md),
including additional fresh composition and edge-case reviews. Both
dependency proofs are independently reviewed and closed. Publication
priority is unestablished.

An ordinary fixed-parameter candidate list for the integer variables
can be combined with an exact oracle algorithm for its continuous
fibers. The resulting expected oracle running time is fixed-parameter
in the number of integer variables plus the rank of the continuous
constraint matrix. The continuous dimension may grow with the input.
This note supplies the composition and its representation bounds; it
does not introduce either underlying algorithm.

## 1. Statement and exact dependency interfaces

Consider
\[
 \min\{f(z,y):z\in\mathbb Z^k, y\in\mathbb R^n,
                              Az+By\le c\},            \tag{1}
\]
with explicit rational constraint data and a rational polynomial
\(f\) of degree at most four. Supply \(\mu\in\mathbb Q_{>0}\)
with the global promise
\[
                     \nabla^2 f(z,y)\succeq\mu I_{k+n}
                       \quad\text{for all real }(z,y). \tag{2}
\]
Write \(r=\operatorname{rank}B\), and let \(L\ge2\) be
the total explicit input length, including any rational threshold
and supplied final polynomial observable.

The composition uses these precise interfaces:

1. The [mixed-linear candidate-list theorem](mixed-linear-strong-quartic-candidate-list.md)
   either certifies infeasibility of (1), or prints a finite list
   \(\mathcal Z\subseteq\mathbb Z^k\) of feasible integer
   blocks containing every integer block of a global minimizer.
   It takes ordinary deterministic time and output length at most
   \(a(k)L^{C_1}\), where \(a\) is computable and \(C_1\)
   is absolute. It uses no exact nonlinear-comparison oracle.
2. The reviewed [constraint-rank oracle theorem](constraint-rank-strong-monotone-oracle.md)
   solves degree-at-most-four strongly convex minimization over an
   explicit rational polyhedron, and compares any explicit rational
   polynomial observable of degree at most four at its unique
   minimizer. With continuous constraint rank \(s\), its expected
   time with a PosSLP oracle is \((s+1)^{O(s)}N^{C_2}\), where
   \(N\) is its enlarged input length and \(C_2\) is absolute.
   It returns a polynomial-size rational affine chart and a unique-zero
   polynomial representation of the minimizer.

**Theorem.** Under these two reviewed interfaces, there is a Las
Vegas algorithm with a PosSLP oracle that either detects infeasibility
of (1), or returns a globally optimal integer block \(z_*\) and
an exact implicit representation of its unique optimal continuous
point \(y_*\). Its expected running time is at most
\[
                         F(k,r)L^C,                    \tag{3}
\]
where \(F\) is computable and \(C\) is absolute. It also decides
every exact rational-threshold order or equality comparison of the
optimal objective value within the same bound.

The integer block and the implicit representation have total length
at most \(F_0(k)L^{C_0}\), with an absolute exponent. The continuous
coordinates need not have short expanded algebraic representations.
The input promise can instead be supplied by the checked full rational
positive definite Hessian Gram format used in the two dependencies.
Invalid certificates are rejected before subsequent branches.

## 2. Feasible fibers and substituted input size

For every \(z\in\mathcal Z\), define
\[
       f_z(y)=f(z,y),\qquad P_z=\{y:By\le c-Az\},
       \qquad v_z=\min_{y\in P_z} f_z(y).               \tag{4}
\]
The candidate-list guarantee makes every \(P_z\) nonempty.
The principal continuous Hessian block of (2) gives
\(\nabla^2 f_z(y)\succeq\mu I_n\) globally. Strong convexity
therefore makes each fiber coercive and gives a unique attained
minimizer \(p_z\), even if its polyhedron is unbounded or lies
in a proper affine subspace.

Let \(Q=a(k)L^{C_1}+L\) bound the candidate-list output and
original input lengths. Each candidate integer has at most \(Q\)
bits in total. Substitution into a degree-four polynomial and forming
\(c-Az\) require only a fixed number of products per monomial
and polynomially many rational additions. Thus every printed fiber
instance has encoding at most \(Q^{C_3}\), for an absolute
\(C_3\). The powers in (3) remain independent of \(k,r\).
This size argument uses the fixed polynomial degree; it does not
assume candidate coordinates have length polynomial in \(L\)
with a parameter-independent coefficient.

The number of candidates is at most the list's total output length,
up to the harmless case \(k=0\), where there is a single possible
empty block. Duplicate blocks can be removed by sorting their
printed binary encodings. The total list remains bounded by \(Q\).

## 3. Comparing two constrained fiber minima

For two feasible candidates \(z,w\), introduce disjoint variables
\(y,y'\) and define
\[
 \begin{aligned}
  g_{z,w}(y,y')&=f_z(y)+f_w(y'),\\
  P_{z,w}&=P_z\times P_w,\\
  H_{z,w}(y,y')&=f_z(y)-f_w(y').
 \end{aligned}                                                   \tag{5}
\]
The Hessian of \(g_{z,w}\) is block diagonal with lower bound
\(\mu I_{2n}\). Its unique constrained minimizer is
\((p_z,p_w)\), and
\[
                   H_{z,w}(p_z,p_w)=v_z-v_w.            \tag{6}
\]
The product polyhedron has constraint matrix
\[
                    \begin{pmatrix}B&0\\0&B\end{pmatrix},
\]
whose rank is \(2r\), including \(r=0\). All printed input
lengths in (5) are polynomial in \(Q\). The constraint-rank
theorem therefore decides any comparison of \(v_z-v_w\) with
zero in expected time
\[
                       (2r+1)^{O(r)}Q^{C_4}.           \tag{7}
\]
The observable \(H_{z,w}\) may be nonconvex. This is permitted
by the reviewed fixed-degree observable theorem used by that
algorithm. No exact comparison of two independently printed
algebraic numbers is assumed.

A newly supplied full Hessian Gram for (5) is unnecessary in the
internal call: the checked original certificate, if that input
format is used, already proves the global bound for both fibers and
their sum. The promise-version oracle theorem accepts the derived
bound \(\mu\). If \(n=0\), all fibers have constant rational
objectives and every comparison is ordinary rational arithmetic.

## 4. Selection, output, and expected time

Sort the candidate blocks lexicographically and scan them in that
fixed order. Maintain the first candidate attaining the smallest
fiber value seen so far. For each subsequent candidate, use (6) to
replace the incumbent exactly when its value is strictly smaller.
There are at most \(|\mathcal Z|-1\) comparisons. Equality
keeps the earlier candidate, so the selected integer block is the
lexicographically smallest global optimal block in the list.
Because the list contains every global optimal block, this is also
the lexicographically smallest block among all optimizers of (1).

Run the single-fiber rank algorithm once more for \(z_*\). It
returns rational data \(\bar y,Z\) and an explicit globally
strongly monotone cubic map \(U\) such that
\[
                y_* =\bar y+Zt_*,\qquad U(t_*)=0,
\]
with exactly one real zero \(t_*\). This is the promised exact
representation; a zero-dimensional chart returns a rational point
directly. Its chart can depend on the random sampling, but
every returned chart represents the same fiber minimizer. The chosen
integer block and objective comparison answers are independent of
the sampling outcomes.

To compare the global minimum with a rational \(\tau\), apply
the single-fiber theorem to the explicit observable \(f_{z_*}-\tau\).
Alternatively evaluate this observable through the returned chart
with the reviewed unique-zero comparison theorem. Both respect
the same parameter and encoding bounds. The algorithm can likewise
compare a supplied polynomial observable of degree at most four at
the selected optimizer, after fixing \(z_*\). This latter question
concerns that specified optimizer; it is not an assertion about all
optimizers when several integer blocks tie.

For each comparison, its conditional expected runtime given all
earlier algorithm history is bounded by (7), because all possible
candidate fiber encodings have the common bound above. Summing these
expectations over the at most \(Q\) calls, and adding construction
and final recovery, gives
\[
              a(k)L^{C_1}+(2r+1)^{O(r)}Q^{C_4+1},
\]
which has the form (3). Independent random bits may be used for
successive calls. Every call returns a correct answer and terminates
almost surely with finite expected time, so the composition remains
Las Vegas. The exponent of \(L\) remains absolute after substituting
\(Q=a(k)L^{C_1}+L\).

If the candidate-list procedure reports infeasibility, no fiber call
is needed. Coercivity and closedness ensure attainment in every
feasible instance, so the algorithm has no unattained-infimum or
unbounded-below branch. With the convention that the empty minimum
is \(+\infty\), any requested threshold predicate in the empty
case can be assigned its direct truth value.

## 5. Scope and attribution

The combined parameter is \(k+\operatorname{rank}B\).
The rank of the integer constraint matrix \(A\) is not added:
its effect is handled in the ordinary candidate-list construction.
The number of continuous variables and constraints remains
unrestricted. The rank is that of all continuous constraint normals,
not merely the active rows at a selected optimum.

This composition turns a finite integer-block candidate list into
exact optimization for fibers of bounded constraint rank. It does
not yield deterministic exact optimization, an ordinary algorithm
without PosSLP, or expected polynomial time when the parameters grow
without bound. Coordinate output is an implicit unique-zero
representation, not a polynomial-size expanded algebraic witness.

The sources and strongest comparisons are recorded in the two
dependency notes. The first uses established fixed-integer convex
feasibility and lattice recursion together with rational approximate
primal-dual cuts. The second uses the classical violator-space
algorithm and the reviewed exact strongly monotone zero primitive.
The disjoint-product comparison in (5) is elementary. No separate
publication-priority claim is made for this composition, and no
practical solver speedup is established.

## 6. Verification status

The main independent reviewer and an additional fresh composition
reviewer reconstructed the dependency interfaces, printed candidate
sizes, global fiber curvature, rank doubling, nonconvex observable
permission, ties, conditional expected-time bounds, and exact implicit
output. A further fresh review checked degenerate inputs. No
mathematical or parameter-accounting defect was found. The final
revision closes the dependency statuses and states the inherited
zero-dimensional rational-output convention explicitly.

The review records the closed dependency hashes and the scope of the
audit. No additional computational test was needed for this elementary
composition. The substantive exact checks are recorded with the two
dependency proofs. Author scoped document checks passed for math
delimiters, spacing commands, local links, whitespace, and control
characters; targeted `git diff --check` also passed. No additional
algorithm implementation, project-wide checks, or CI inspection is
claimed.
