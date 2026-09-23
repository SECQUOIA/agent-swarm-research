# Exact sparse hulls for flat series–parallel chains at fixed simplex dimension

Date: 2026-09-07. Status:
[independently reviewed](../notes/review-network-simplex-reopened-series-parallel.md).

Lean verification of the stronger residual-eliminated manuscript and the
unreduced circuit library is complete in
[topic 15](../formal/topics/15-flat-chain-threshold/README.md). See its coverage
map for the mathematical scope and its verification record for targeted checks.

This note retains the earlier unreduced formulation. The
[current manuscript](../paper-network-simplex/sections/07-fixed-state-chains.tex)
eliminates the residual profile coordinate: two observed labels use five profile
tests and three use sixteen circuit tests, alongside the original-domain and
zero-row checks. Unit flow/product coefficients suffice through three observed
labels but can fail at four. The manuscript also gives recovery without an
online linear program. The 41-circuit library and coefficient bound eight below
remain valid for the unreduced formulation with two explicit labels; they are
superseded by these sharper results.

Consider the sparse network–simplex hull from the
[series–parallel coefficient theorem](network-simplex-series-parallel-coefficient-growth.md),
on the following unit-capacity, unit source-to-sink flow network: an arbitrarily
long serial chain of two-arc parallel gadgets, in parallel with one bypass arc.
All arcs point from source toward sink. Observed products may occur on either
arc of any gadget and on the bypass. Capacities and flow value are one; arbitrary
balance/capacity data and arbitrary nested series–parallel networks are outside
this theorem.

At fixed simplex dimension, this graph class has an exact original-space
separator whose arithmetic work is linear in the number of gadgets and
observations, plus a term depending only on simplex dimension. Its hull also has
a uniform bound on flow/product inequality coefficients depending only on that
dimension. For two explicit simplex coordinates, the separator needs only 41
precomputed nonzero-row circuits.

This complements the exponential coefficient family on the same topology:
growing simplex dimension is essential to that family's unbounded ratios.
General hull separation through the known disaggregated extended formulation
was already polynomial; the contribution here is explicit elimination and a
fixed-dimension original-space oracle.

For \(d=m+1\) simplex states, including the residual state, hull membership can
be reduced to a system in one shared branch profile \(w\in\mathbb R^d\).
Every coefficient row of this system is a signed 0/1 subset indicator. Every
right-hand-side coefficient on an original flow or observed product is in
\(\{-1,0,1\}\). Consequently the hull has a finite inequality description
whose flow/product coefficients have magnitudes at most

\[
(d+1)\Delta_d,
\tag{1}
\]

where \(\Delta_d\) is the largest absolute determinant of a square 0/1 matrix
of order at most \(d\) (and is at least one). This bound depends on simplex
dimension, not the number of gadgets. It does not assert that the description
has a small number of inequalities.

**Reduction.** Write \(\lambda\) for the \(d\) simplex-state weights.
The profile satisfies \(0\le w_j\le\lambda_j\) and
\(\mathbf1^Tw=1-x_h\). A bypass observation forces
\(w_j=\lambda_j-z_{h,j}\).
In one gadget, partition states into \(A\) (only arc \(a\) observed),
\(B\) (only arc \(b\) observed), \(T\) (both observed), and \(U\)
(neither observed). Denote the observed values by \(u_j=z_{a,j}\) and
\(v_j=z_{b,j}\). All observed values must be nonnegative. Require

\[
w_j\ge u_j\ (j\in A),\quad w_j\ge v_j\ (j\in B),\quad
w_j=u_j+v_j\ (j\in T).
\]

Set

\[
R=x_a-\sum_{j\in A\cup T}u_j+\sum_{j\in B}v_j.
\]

Conditional on \(w\), the remaining exact aggregate feasibility conditions are

\[
\sum_{j\in B}w_j\le R\le\sum_{j\in B\cup U}w_j.
\tag{2}
\]

Indeed the state arc-\(a\) values are fixed to \(u_j\) on \(A\cup T\),
fixed to \(w_j-v_j\) on \(B\), and range independently over
\([0,w_j]\) on \(U\). Their sum attains every value between the two
endpoints giving (2). Individual arc capacities are automatic from
\(0\le f^j_a,f^j_b\le w_j\le\lambda_j\). Once each gadget is filled,
its state flow joins consistently with every other gadget through the common
profile, and the bypass carries \(\lambda_j-w_j\). This proves exactness.

**Coefficient bound.** Express equalities by two inequalities to obtain
\(Lw\le r(x,y,z)\), where each row of \(L\) is a signed subset indicator.
The nonnegative Farkas cone \(\{\mu\ge0:L^T\mu=0\}\) is pointed. Every
extreme ray has a minimally dependent support of at most \(d+1\) rows. Its
primitive integer entries are, up to a common divisor, signed minors of order at
most \(d\). Changing signs of rows turns those minors into 0/1 determinants,
so every ray entry is at most \(\Delta_d\). A zero row contributes a singleton
ray with coefficient one. Farkas' lemma says that the corresponding inequalities
\(\mu^T r(x,y,z)\ge0\) describe the projection exactly. At most \(d+1\)
right-hand sides contribute, each with unit flow/product coefficients, proving
(1). Original flow/simplex inequalities and product nonnegativity also satisfy
the bound.

For example, \(m=2\) gives \(d=3\), \(\Delta_3=2\), and the conservative
uniform bound eight. This is not a sharp facet classification, but it rules out
unbounded coefficient growth in this flat topology at fixed simplex dimension.
The proof does not extend automatically to nested series–parallel graphs, where
several interacting profile vectors remain after local elimination. Determining
whether fixed simplex dimension controls coefficients for those larger graphs
remains a separate question.

**Original-space separation.** First check the original flow constraints,
capacities, simplex conditions, and observed-product nonnegativity. Then there
are at most \(2(2^d-1)+1\) distinct
signed subset rows, including the zero row. Group all copies of the same row by
their minimum right-hand side. For fixed \(d\), precompute all positive circuits
of the signed-subset row universe. Each circuit uses at most \(d+1\) rows, so
there are at most \(2^{O(d^2)}\) candidates; exact rational nullspace computations
identify the positive ones. At a tested point, evaluate each present row's tightest
right-hand side and every circuit supported on present rows. A negative circuit
sum is a separating inequality. Freeze the minimizing original row in each
participating group to recover an explicit original-space affine cut. Zero-row
violations are tested separately. If none fail, Farkas' lemma certifies membership.

Given \(L\) serial gadgets, constructing their rows takes
\(O(dL+|O|+m)\) arithmetic operations, followed by \(2^{O(d^2)}\)
parameter-only work. The construction needs no profile variables in the target
formulation. At fixed \(d\), a feasible profile can instead be recovered by
solving the grouped linear program with at most \(2^{d+1}\) constraints and
\(d\) unknowns, after which a greedy interval fill constructs every gadget's
state arc flows in \(O(dL)\) additional work. Rational encoding lengths remain
polynomial. This is a structural original-space specialization, not a new
general separation complexity claim.


## Verification and literature scope

The [exact circuit script](../code/network_simplex_exploration/flat_chain_circuits.py)
enumerates 1, 5, and 41 positive circuits for one, two, and three total states,
respectively. Their largest primitive ray entries are 1, 1, and 2. All 600 exact
rational circuit-membership decisions agreed with a separately assembled LP:
428 feasible and 172 infeasible systems. Zero-row conditions are direct scalar
inequalities and are not included in those circuit counts.

The [independent graph/profile audit](../code/network_simplex_review/flat_chain_profile_audit.py)
does not import the author code. All 320 comparisons of the profile formulation
with the convex hull of directed-path/simplex-vertex pairs passed: 171 feasible
and 149 infeasible cases. These use one to four explicit simplex coordinates,
varied observations on both gadget arcs and the bypass, zero residual weights,
and zero explicit-state weights. The reviewer also reproduced the circuit counts
using independent exact enumeration.

The profile reduction and determinant argument use classical interval
feasibility and Farkas circuits. A direct priority claim for this exact
specialization requires the literature comparison recorded with the
[companion theorem](network-simplex-series-parallel-coefficient-growth.md).
This result should be presented as the positive fixed-dimension complement to
that theorem, rather than as a new general polynomial separation result.
