# P-split Theorem 6: counterexample and a geometric repair

Status: the counterexample and local repair passed an [independent source and mathematical audit](review-p-split-theorem-six.md),
2026-09-04, with the finite-link/common-radius qualifications below.
This note concerns the published theorem's universal nonexactness claim,
not the validity of the P-split formulation itself.

## 1. Source and exact counterexample

Kronqvist, Misener, and Tsay, *P-split formulations: a class of intermediate
formulations between big-M and convex hull for disjunctive constraints*,
Mathematical Programming 218, 57–94 (2026),
[published article](https://doi.org/10.1007/s10107-025-02232-1),
[open published PDF](https://d-nb.info/1373875933/34).
Definition 4 and Theorem 6 appear on local PDF pages 15–16. The definition means
pairwise disjoint feasible disjuncts. The theorem asserts nonexactness of every
P-split formulation for fully disjoint disjunctions with additive bounds and
strictly convex constraint functions.

Take

\[
X=[0,3]\times[-1,1],\qquad
D_0=\{(t,w)\in X:t^2+w^2\le1\},\qquad
D_3=\{(t,w)\in X:(t-3)^2+w^2\le1\}.
\tag{1}
\]

Both constraints are strictly convex and additively separable. The disjuncts are
nonempty and disjoint: their first-coordinate ranges lie in \([0,1]\) and
\([2,3]\). Exact bounds on sums of the component functions are additive over the
box \(X\). Each disjunct uses one constraint. Source Assumption 4, asking for few
constraints relative to dimension, is explicitly described as technically
unnecessary; an arbitrary-dimensional version is also given below.

Every vertex of \(X\) belongs to \(D_0\cup D_3\). Therefore

\[
\operatorname{conv}(D_0\cup D_3)=X.
\tag{2}
\]

Every continuous P-split relaxation is convex, contains both disjuncts, and
retains the constraint \(x\in X\). Its projection is consequently exactly \(X\).
Thus **every P-split partition is exact** in this example, contradicting the
stated universal nonexactness claim.

The full two-split formulation can also be checked directly, respecting the
source's minimal auxiliary-variable convention. Use a shared auxiliary for
\(w^2\). For any \((t,w)\in X\), choose

\[
(\alpha_0,\alpha_3,\alpha_w)=(3t,9-3t,1).
\]

This is the convex combination, with weights \(1-t/3,t/3\), of the valid lifted
points \((0,9,1)\) and \((9,0,1)\). The original epigraph links hold because
\(t^2\le3t\), \((t-3)^2\le9-3t\), and \(w^2\le1\). This gives an explicit
extended witness for (2), rather than relying only on the formulation's validity.

For any \(n\ge2\), the same counterexample uses

\[
X=[0,3]\times[-1,1]^{n-1},\qquad
g_0(x)=x_1^2+\frac1{n-1}\sum_{i=2}^n x_i^2,\qquad
g_3(x)=(x_1-3)^2+\frac1{n-1}\sum_{i=2}^n x_i^2,
\]

with disjuncts \(g_0\le1\) and \(g_3\le1\). They are disjoint, strictly convex,
and contain all box vertices between them. The coefficients are rational, and
there is only one constraint per disjunct even in arbitrarily large dimension.

## 2. Where the proof fails

There are two distinct issues in the published argument.

First, strict convexity of a univariate component only gives strict Jensen slack
when its two arguments differ. A mixed hull-boundary segment can vary in some
coordinates and remain fixed in others. In (1), the top boundary joins
\((0,1)\) and \((3,1)\); the shared \(w^2\) component has no Jensen slack.

Second, even if epigraph inequalities admit a neighborhood, the retained domain
constraint \(x\in X\) may not. A segment on a facet of \(X\) cannot have an
outward feasible neighborhood within \(X\). The proof's neighborhood argument
does not establish a relaxation point outside the hull in this situation.

The counterexample does not imply that nonlinear P-split relaxations are usually
exact. It shows that strict convexity, disjointness, and additive bounds alone
cannot justify their universal nonexactness.

## 3. A sufficient local repair

Consider any lifted convex relaxation of the form

\[
R=\{x\in X:\exists\alpha\in Q,\ F_a(x)\le\alpha_a\ (a\in A)\},
\tag{3}
\]

where \(A\) is finite, \(Q\) is convex, and \(F_a\) are continuous convex functions. P-split
relaxations have this form, with \(Q\) the convexified auxiliary disjunction.
Let two original feasible points \(x^0,x^1\) have valid lifted vectors
\(\alpha^i_a=F_a(x^i)\in Q\), and let
\(x^\theta=(1-\theta)x^0+\theta x^1\), \(0<\theta<1\).
Define their Jensen slacks

\[
\Delta_a=(1-\theta)F_a(x^0)+\theta F_a(x^1)-F_a(x^\theta).
\]

Suppose a supporting inequality \(c^Tx\le\beta\) of the true hull is tight at
\(x^\theta\), and there is a direction \(d\) with \(c^Td>0\) such that:

1. \(x^\theta+\varepsilon d\in X\) for all sufficiently small
   \(\varepsilon\ge0\);
2. for every \(a\) with \(\Delta_a=0\),
   \(F_a(x^\theta+\varepsilon d)\le F_a(x^\theta)\) for all sufficiently small
   \(\varepsilon\ge0\).

Then (3) is strictly larger than the true hull. Indeed, keep
\(\alpha=(1-\theta)\alpha^0+\theta\alpha^1\in Q\). Every positive slack
survives a sufficiently small step by continuity; condition 2 preserves all
zero-slack links. The stepped point is therefore in \(R\), but violates the
supporting inequality. Unlike the source's argument, this criterion explicitly
checks both the domain and the zero-slack components.

If each varying link is locally \(L_a\)-Lipschitz along the ray, any positive
\(\varepsilon\) within a common radius where domain feasibility, zero-slack
nonincrease, and all the stated Lipschitz bounds hold, and satisfying
\(\varepsilon L_a\le\Delta_a\) for every positive-slack link is certified.
Its support violation is exactly \(\varepsilon c^Td\). Strong convexity, when
available for that particular component and pair of points, supplies a lower
bound on \(\Delta_a\); it does not remove the two directional conditions.

This local criterion is a direct continuity argument and is retained as a proof
repair, without a separate novelty claim.

## 4. Follow-up to investigate

For two separated Euclidean balls with the bounding box extending beyond their
centers, the strongest split relaxation may admit a simple explicit description.
That would distinguish genuine nonlinear loss from the domain-truncation
counterexample above. No unreviewed formula is asserted here yet.
