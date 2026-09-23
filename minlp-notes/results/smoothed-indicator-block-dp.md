# Exact smoothed dynamic programming for indicator quadratics

Date: 2026-09-22. Status: consolidated research result. The scalar-envelope,
deterministic algorithm, finite-grid, and priority arguments have received
separate independent reviews, linked below. A fresh integrated review also
checked the complete argument and additive certificate without finding a
mathematical gap. No publication priority claim is made.

The later [spectral-bound construction](smoothed-spectral-indicator-messages.md)
covers arbitrary fixed treewidth and removes diagonal dominance. This result
retains a simpler scalar-envelope algorithm and an explicit expected operation
bound for bounded biconnected blocks.

Independent perturbations of indicator penalties permit an exact algorithm
with polynomial expected bit complexity for a restricted, meaningful class
of convex mixed-integer quadratic problems. The Hessian must have a uniform
strict diagonal-dominance margin and bounded entries, the continuous linear
coefficients must be bounded, and every biconnected block of its support graph
must have bounded size. The blocks can be arbitrary graphs; they need not be
cliques. Their intersections are single vertices.

The algorithm constructs all scalar dynamic-programming messages exactly.
Its finite perturbations use only polynomially many random bits. The problem
class includes chains of triangles, on which exact unperturbed optimization
is already [NP-hard](indicator-quadratic-treewidth-two-hardness.md).
The result solves the perturbed instance exactly. It also gives an always
correct additive objective interval for the original instance, with polynomial
expected time at any inverse-polynomial requested accuracy.

The underlying isolation estimate and envelope operations are established
ingredients. The candidate contribution is their combination with exact
support elimination, independent child subproblems, and a finite-grid argument
that controls atoms and bit costs. Practical performance remains untested.

## 1. Problem, assumptions, and main theorem

Consider

\[
 v_\xi=\min\left\{x^TQx+c^Tx+(\lambda+\xi)^Tz:
 x_i(1-z_i)=0,
 \quad x\in\mathbb R^n,\ z\in\{0,1\}^n\right\}.                 \tag{1}
\]

The deterministic matrix \(Q\) is symmetric. Assume

\[
 0<d\le Q_{ii}\le D,\qquad
 \sum_{j\ne i}|Q_{ij}|\le\rho Q_{ii},\qquad
 0\le\rho<1,\qquad |c_i|\le C.                              \tag{2}
\]

The support graph has edge \(ij\) exactly when \(Q_{ij}\ne0\), for
\(i\ne j\). Every biconnected block has at most \(b\) vertices, with
bridges counted as two-vertex blocks. Isolated vertices are allowed.
All deterministic data and structural choices are fixed before drawing noise.
There is no sign or magnitude restriction on \(\lambda\), or on the
perturbed penalties. Negative penalties cause no unboundedness because the
indicators are binary and \(Q\) is positive definite.

For \(C>0\), define

\[
 M=\frac{C}{2d(1-\rho)},\qquad I=[-M,M].                    \tag{3}
\]

**Theorem 1 (finite-grid smoothing).** Suppose the data and the parameter
bounds in (2) are rational. Let \(\sigma>0\) be rational. Draw the
coordinates of \(\xi\) independently and uniformly from

\[
 \left\{-\sigma+\frac{2\sigma k}{N-1}:k=0,\ldots,N-1\right\},
 \qquad N\ge4n2^n.                                       \tag{4}
\]

There is an exact algorithm that constructs all messages on \(I\), returns
an optimal support and rational continuous optimizer of (1), and has expected
arithmetic, comparison, and quadratic-root operation count

\[
 O_b\!\left(n^2
 \left(3+8n\phi\rho D M^2\right)^{b-1}\right),
 \qquad \phi=\frac1{2\sigma}.                            \tag{5}
\]

Each operation can be implemented with bit cost polynomial in
\(n,B,\log N\), where \(B\) bounds the rational input bit lengths,
including \(\sigma\) and the bounds in (2). Taking \(N\) to be the
smallest power of two satisfying (4) requires \(O(n+\log n)\) random
bits per coefficient. For fixed \(b,d,D,C,\rho\), the expected bit
runtime is polynomial in the input length and \(1/\sigma\).

In particular, this is polynomial expected time in the encoded input length
when \(1/\sigma\) is polynomially bounded in that length. The dependence
is not polynomial in \(\log(1/\sigma)\). For \(C=0\), every continuous
support optimizer is zero, and the problem is solved directly by selecting
the negative perturbed penalties.

**Theorem 2 (continuous smoothing).** If the independent noises instead have
Lebesgue densities bounded by \(\phi\), the same algorithm has expected
operation count

\[
 O_b\!\left(n^2
 \left(2+8n\phi\rho D M^2\right)^{b-1}\right).            \tag{6}
\]

This theorem uses exact real arithmetic and exact quadratic-root comparisons.
It places no bound on noise tails. It is not a Turing-time claim for arbitrary
real noise samples. Theorem 1 supplies a separate finite-input statement.

## 2. A scalar envelope bound from isolation

The probabilistic input applies beyond quadratics.

**Lemma 3.** Let \(Z\subseteq\{0,1\}^m\) be nonempty and finite, let
\(I\) be a compact interval of length \(T>0\), and let the deterministic
functions \(q_z:I\to\mathbb R\) be \(L\)-Lipschitz. If independent
\(\xi_i\) have densities bounded by \(\phi\), then the set
\(\mathcal T\) of interior points with two distinct minimizing supports
in

\[
 V(t)=\min_{z\in Z}\{q_z(t)+\xi^Tz\}
\]

satisfies

\[
 \mathbb E|\mathcal T|\le2m\phi LT.                       \tag{7}
\]

It is finite almost surely. The number of intervals of unique minimizing
support, counting separated appearances of the same support separately, has
expectation at most \(1+2m\phi LT\). No algebraicity or semialgebraicity
assumption is required.

**Proof.** Fix \(t\), and let \(\Delta(t)\) be the gap between the best
and second-best distinct support values, counting ties as a zero gap. A
single support has infinite gap. For a coordinate \(i\), condition on
all noise except \(\xi_i\). The best costs in its two support classes
have the form \(A_i\) and \(B_i+\xi_i\), for fixed \(A_i,B_i\).
Ignore coordinates with an empty class. The probability that these two
values differ by at most \(\delta\) is at most \(2\phi\delta\).
The two best distinct supports differ in some coordinate, and their values
are the minima within those two classes. Therefore

\[
 \Pr\{\Delta(t)\le\delta\}\le2m\phi\delta.               \tag{8}
\]

In particular, every fixed parameter has a unique winner almost surely.
This is the classical coordinate-conditioning isolation argument; arbitrary
deterministic support offsets do not change it.

Partition \(I\) into \(r\) cells of length \(\eta=T/r\). At a cell
midpoint \(s\), choose its unique winner \(z\). If the cell contains
an optimal tie at \(t\), at least one minimizer \(y\) at that tie
differs from \(z\). Since \(F_y(t)\le F_z(t)\), where
\(F_w=q_w+\xi^Tw\),

\[
 0\le F_y(s)-F_z(s)\le2L|s-t|\le L\eta.
\]

Thus a cell containing any tie has \(\Delta(s)\le L\eta\). If
\(C_r\) counts such cells, (8) gives
\(\mathbb E C_r\le2m\phi LT\). This also detects an isolated tie
with the same winner on both sides.

Almost surely no endpoint or midpoint of any of these countably many grids
is a tie. Every finite subset of \(\mathcal T\) then occupies distinct
cells once the grid is sufficiently fine. Hence
\(|\mathcal T|\le\liminf_r C_r\), with the same interpretation if
the tie set is infinite. Fatou's lemma proves (7). On each component of
\(I\setminus\mathcal T\), the unique winner is locally constant by
continuity and finiteness of \(Z\), and hence constant. Endpoint ties have
probability zero. This proves the interval bound. The events used here are
measurable: the gap is continuous in the finite vector of support values,
and its minimum over a compact cell is a continuous function of the noise.
\(\square\)

A common deterministic function may be subtracted from every branch without
changing its winners. This will remove a boundary vertex's own costs and
give a sharper Lipschitz constant.

## 3. An invariant interval for every support

Strict diagonal dominance in (2) makes \(Q\) and every principal submatrix
positive definite. Fix any support, and fix any boundary coordinates to
values in \(I\). Its conditional continuous minimizer exists and is unique.
If there are free active coordinates, choose one with largest absolute value
\(X\). Its stationarity equation gives

\[
 X\le\frac{C}{2d}+\rho\max(X,M).
\]

If \(X>M\), then \((1-\rho)X\le C/(2d)=(1-\rho)M\), a
contradiction. Thus every free coordinate belongs to \(I\); inactive
coordinates are zero. The argument also applies to a subtree conditional
problem: missing edges only decrease the absolute off-diagonal row sums.

The assertion is for **every fixed support**, including supports that are
never globally optimal. This permits later elimination of a retained support
outside the interval on which that support happens to win its message.

For a fixed-support message with scalar boundary \(x_v=t\), exclude the
boundary vertex's own diagonal, linear, and penalty terms. Its deterministic
conditional value is a full quadratic \(q_z(t)\). Differentiating the
conditional optimum and using stationarity of the eliminated variables gives

\[
 q_z'(t)=2\sum_{j\text{ internal}}Q_{vj}x_j^z(t),\qquad
 |q_z'(t)|\le L:=2\rho D M\quad(t\in I).                 \tag{9}
\]

All support families are fixed before noise is sampled. Penalty noise adds
only the support constant \(\xi^Tz\). Lemma 3 therefore applies to
the full support family of each message with
\(T=2M\), not to a randomly selected family left after pruning.

## 4. Exact construction with full support quadratics

Root each connected component's block-cut tree at a vertex. Assign every
cross term \(2Q_{ij}x_ix_j\) to its unique block and every diagonal,
linear, and indicator term to its vertex. A block message conditions on its
parent vertex and includes precisely the terms below that block. It excludes
the parent vertex's own terms. Vertex and block operations alternate.

The representation stores full quadratic polynomials and a complete support
or reconstruction pointer for each. Keep one representative per polynomial
that attains the lower envelope on a nonempty open interval in \(I\).
Identify identical polynomials and coalesce adjacent intervals with the same
formula. One formula may appear on several separated intervals, but need be
stored only once. Formulas touching the envelope only at isolated points are
unnecessary: a neighboring interval formula attains the same value there by
continuity. The retained full polynomials represent the message throughout
\(I\), including endpoints.

### Vertex operation and the inactive alternative

Write \(p_u=\lambda_u+\xi_u\). With vertex \(u\)'s indicator fixed
to one, its active message is

\[
 F_u(t)=Q_{uu}t^2+c_ut+p_u+
              \sum_{B\text{ child of }u}H_B(t).           \tag{10}
\]

Merge the child breakpoint lists, maintaining the sum of active polynomial
coefficients and updating each child's contribution at its breakpoint. This
avoids summing all children again on every interval at high-degree vertices.
On each resulting open interval, add the own-vertex terms. The resulting full quadratic
is the exact conditional value of a genuine combination of child supports
for every real \(t\). Deduplicate and prune these formulas as above.
Their minimum equals (10) on \(I\): no feasible-support value can be below
the true message, and one attains it on each open interval. Continuity handles
the remaining points. Recomputing a lower envelope, if needed to coalesce
identical formulas, uses the envelope routine described below.

The inactive alternative fixes \(x_u=0,z_u=0\) and has value

\[
 A_u=F_u(0)-p_u.                                         \tag{11}
\]

At zero, changing \(z_u=1\) to \(z_u=0\) removes exactly its penalty
and imposes no additional condition on descendants. Store one descendant
support attaining (11). One suffices because the descendants interact with
the remaining graph only through \(u\). Active alternatives at zero remain
available, including when \(p_u<0\).

### Block operation

For a block \(B\) with parent vertex \(v\), choose at each
\(u\in B\setminus\{v\}\) either a retained active quadratic or the
inactive alternative (11). Add the cross terms assigned to \(B\). Set
inactive block variables to zero and minimize over the active block variables
without interval restrictions. A Schur complement produces a full quadratic
in \(x_v\).

This operation is exact for three reasons.

1. Every chosen combination specifies a genuine complete internal support.
   A retained polynomial is that support's exact conditional value everywhere,
   rather than a formula whose validity ends at its winning interval.
2. The eliminated active matrix is a Schur complement of a positive definite
   principal matrix of \(Q\). The minimizer exists uniquely. For a parent
   value in \(I\), the preceding maximum principle applied to the complete
   support puts all its internal minimizing variables in \(I\).
3. Conversely, take a true optimum conditional on any \(x_v\in I\).
   Its child boundary values belong to \(I\). Replace each child's
   descendants by a retained support attaining its message at that boundary,
   or by its inactive alternative. These replacements preserve feasibility
   and value. The enumerated combination therefore attains the true optimum
   after block elimination.

Thus pruning cannot lose the optimum, and extending retained polynomials
beyond their winning intervals cannot create an infeasible underestimate.
No step assumes that the block is a clique.

At each root, compare its inactive alternative with the minima on \(I\)
of its active quadratics. The maximum principle contains an optimizer of
every global support problem, so this gives the unrestricted optimum.
Stored local minimizers and choices reconstruct the point by back substitution.
The deterministic algorithm is exact for every penalty vector, including
finite-grid outcomes with persistent duplicate formulas.

## 5. Expected construction work

Let \(K_u\) be the number of distinct retained active formulas at vertex
\(u\). A block generates at most

\[
 N_B=\prod_{u\in B\setminus\{v\}}(K_u+1)                 \tag{12}
\]

quadratic candidates. The extra alternative is the inactive atom. For one
block, its child-vertex subtrees are disjoint. Each \(K_u\), including
all tie decisions, depends only on the noises in its own subtree. Use a fixed
deterministic rule for duplicate representatives and other ties. The child
counts in (12) are consequently independent. No independence between ancestors
and descendants is asserted or needed.

Under continuous noise, Lemma 3 and (9) imply

\[
 \mathbb E(K_u+1)\le 2+2n\phi LT
                   =2+8n\phi\rho D M^2=:A_{\rm cont}.
\]

The boundary's own penalty is common to all active branches and does not
affect the count. Therefore \(\mathbb E N_B\le A_{\rm cont}^{b-1}\).
There are at most \(n-1\) nontrivial blocks in a connected component.

For completeness, the lower envelope of \(r\) distinct full univariate
quadratics has at most \(2r-1\) open pieces. A winner sequence containing
\(a,b,a,b\) would force at least three distinct roots of their nonzero
quadratic difference. Removing adjacent repeated labels gives an order-two
Davenport--Schinzel sequence, whose length is at most \(2r-1\).
Merge two ordered envelopes by traversing overlapping intervals and comparing
their two active quadratics, with at most two crossings on an overlap.
This takes time linear in the two envelope lengths. Divide and conquer gives
\(O(r\log r)\) arithmetic, comparison, and quadratic-root operations.
These are standard envelope facts, not new algorithmic primitives.

Every retained formula has a support representative. Hence each list has
at most \(2^n\) entries, and the logarithmic factors in all envelope
constructions and breakpoint sorts are \(O_b(n)\) deterministically.
Each candidate requires a Schur complement of dimension at most \(b-1\).
All vertex merges together process at most \(2\sum_BN_B\) child-envelope
pieces. Support bookkeeping and local back substitution fit the coarse bound

\[
 O_b\!\left(n\left(n+\sum_BN_B\right)\right).             \tag{13}
\]

Explicit support labels cost at most a further linear-in-\(n\) amount per
generated formula, already covered in (13); alternatively use backpointers.
Taking expectations in (13) proves Theorem 2. Only first moments are used.
In particular, the proof does not replace \(\mathbb E K_u^2\) by
\((\mathbb E K_u)^2\).

## 6. A finite-grid envelope bound

The density argument cannot be applied directly to grid noise, which has
atoms. The following separate estimate is sufficient.

**Lemma 4.** In Lemma 3 suppose each \(q_z\) is a quadratic polynomial
and each coordinate of \(\xi\) is uniform on the \(N\)-point grid
in (4), for any \(N\ge2\). Count maximal positive-length intervals of
envelope formulas, identifying identical polynomials and ignoring isolated
ties. Let their number be \(K\). With \(\phi=1/(2\sigma)\),

\[
 \mathbb E K\le1+2m\phi LT+\frac{4m2^m}{N}.              \tag{14}
\]

A formula appearing on separated intervals is counted separately. When
\(m=0\), the bound is one.

**Proof.** Grid spacing implies that every real interval \(J\) satisfies

\[
 \Pr(\xi_i\in J)\le\phi\,\operatorname{length}(J)+1/N.    \tag{15}
\]

Introduce independent uniforms \(U_i\in[-1,1]\), independent also of
\(\xi\), and set \(\eta_i=\xi_i+\delta U_i\) for \(\delta>0\).
The \(\eta_i\) have continuous densities. Conditioning on \(U_i\)
and translating \(J\) shows that (15) also holds for \(\eta_i\), with
the same bound, independent of \(\delta\).

Condition on all \(\eta_j\) except coordinate \(i\). For nonempty
bit classes define

\[
 h_i(t)=\min_{z_i=0}\left(q_z(t)+\sum_{j\ne i}\eta_jz_j\right)
       -\min_{z_i=1}\left(q_z(t)+\sum_{j\ne i}\eta_jz_j\right).
\]

This function is \(2L\)-Lipschitz, with total variation at most \(2LT\).
Each class has at most \(2^{m-1}\) branches. The quadratic-envelope bound
in Section 5 shows that the common refinement of their envelopes has fewer
than \(2^{m+1}\) pieces. On each piece \(h_i\) is quadratic. Splitting
at stationary points gives at most \(J_m=2^{m+2}\) monotone arcs.

Constant arcs and all arc endpoint levels have conditional probability zero
of being hit by the continuously distributed \(\eta_i\). Every remaining
open monotone arc contributes at most one solution of \(h_i(t)=\eta_i\).
Sum (15) over their image intervals. The image lengths add to at most the
total variation. The conditional expected number of level hits is at most

\[
 2\phi LT+J_m/N.
\]

Every optimal tie between distinct supports differs in some coordinate and
therefore satisfies that coordinate's class equality. Summing over coordinates
bounds the expected number of tie points, and hence the jittered envelope's
expected number of intervals, by

\[
 1+2m\phi LT+mJ_m/N.                                    \tag{16}
\]

To remove the jitter, fix a grid outcome. Pick an interior point from each
of its finitely many envelope pieces, avoiding intersections with every
nonidentical polynomial. At these points the winning polynomial class has
a positive gap from all other classes. A class can contain several support
labels with identical full polynomials. For all sufficiently small
\(\delta\), every jittered winner at each chosen point belongs to its
original class. Consecutive chosen points have different classes and thus
require at least as many jittered envelope intervals. For any sequence
\(\delta\downarrow0\),

\[
 K(\xi)\le\liminf_{\delta\downarrow0}K(\xi+\delta U)
\]

along that sequence, almost surely. Countably many positive jitter sizes have
no persistent support ties simultaneously. Fatou's lemma and (16) establish
(14). Counting polynomial formulas rather than requiring a unique support
at zero jitter is essential. \(\square\)

For a message with \(m\le n\) internal indicators, (4) gives
\(4m2^m/N\le1\). Consequently

\[
 \mathbb E(K_u+1)\le 3+8n\phi\rho D M^2=:A_{\rm grid}.
\]

Identical polynomial formulas are interchangeable for future elimination:
they have the same value at every boundary value, and their subtree connects
to the rest only through that boundary. A deterministic representative
therefore suffices even at an inactive atom. Sibling independence continues
to hold under grid noise. Applying (12)--(13) with \(A_{\rm grid}\)
proves the operation bound (5).

## 7. Exact rational and algebraic computation

Choose \(N\) to be the smallest power of two satisfying (4). A uniform
integer \(k\in\{0,\ldots,N-1\}\) then uses exactly \(\log_2N\)
independent random bits, and its grid value has polynomial bit length.
For other \(N\), rejection sampling also gives an exact uniform draw with
expected \(O(\log N)\) random bits; the bit bound then includes \(\log N\).

Every retained full quadratic is the exact conditional value of a support
of the original rational problem. Its coefficients are Schur-complement
expressions from a principal matrix of \(Q\), its linear terms, and a
sum of support penalties. Clearing input denominators, determinant bounds,
and Cramer's rule give coefficient bit lengths polynomial in
\(n,B,\log N\). This bound holds for every support, whether retained
or discarded. Principal matrices are nonsingular by (2).

Use reduced rational arithmetic. A constant-size block elimination and a
vertex sum of at most \(n\) contributions have polynomial-size intermediate
fractions. A completed message coefficient cannot accumulate an unbounded
tower of bit lengths: it is a coefficient of a fixed-support conditional
value covered by the preceding determinant bound.

Every breakpoint is an endpoint of \(I\) or a real root of a difference
of two rational quadratics. It therefore has algebraic degree at most two
and polynomial-size defining coefficients. Store it by its defining polynomial
and root choice or rational isolating interval. Root comparison, equality,
sorting, and quadratic sign testing on overlapping intervals take polynomial
bit time by fixed-degree algebraic computation. Subsequent Schur complements
act on rational coefficients, not on expressions involving old breakpoints;
algebraic degrees therefore do not grow through the recursion.

The selected support has a rational continuous optimizer, obtained by local
back substitution or by solving its positive definite principal linear system.
Its coordinates and objective value have polynomial bit length. Thus every
operation in (5) has a polynomial bit implementation, uniformly over all
grid outcomes. This proves the bit assertion in Theorem 1.

## 8. An always correct additive objective interval

**Corollary 5.** Under Theorem 1's assumptions, for any rational
\(\varepsilon>0\) there is an algorithm that returns a feasible point
and a valid interval of width at most \(\varepsilon\) containing the
unperturbed optimum. The guarantee holds for every noise outcome. For fixed
\(b,d,D,C,\rho\), expected bit time is polynomial in the input length
and \(1/\varepsilon\).

**Proof.** Let \((\widehat x,\widehat z)\) be the exact perturbed
optimizer, with value \(v_\xi\). Its original objective and a valid
original lower bound are

\[
 U=v_\xi-\xi^T\widehat z,\qquad
 L_{\rm original}=v_\xi-\sum_i\max(\xi_i,0).             \tag{17}
\]

Indeed, every feasible original cost is its perturbed cost minus
\(\xi^Tz\), hence is at least \(L_{\rm original}\). Feasibility
gives an upper bound \(U\). Their width is

\[
 \begin{aligned}
 U-L_{\rm original}
 &=\sum_{\widehat z_i=0}\max(\xi_i,0)
   +\sum_{\widehat z_i=1}\max(-\xi_i,0)\\
 &\le\sum_i|\xi_i|\le n\sigma.
 \end{aligned}                                           \tag{18}
\]

Choose \(\sigma=\varepsilon/n\) in Theorem 1. The interval (17) has
the claimed width, including all ties and negative perturbed penalties.
Only running time is averaged. \(\square\)

The elementary objective-perturbation inequality is classical. The point here
is that an exact perturbed solver makes the interval computable without a
support-margin assumption. This is an additive approximation scheme, not a
relative-error FPTAS, and it does not recover the unperturbed exact optimizer.
It is not a new approximation frontier. Under these same numerical bounds,
deterministic grid dynamic programming already gives an additive certificate,
even on arbitrary bounded-treewidth graphs. To see this, round an optimal
fixed-support solution to the grid \(\{jM/K:-K\le j\le K\}\), retaining
its indicators. Fixed-support stationarity cancels the linear error, so the
cost increase is at most \(nD(1+\rho)M^2/(4K^2)\). Exact finite-state
dynamic programming on a tree decomposition gives the grid optimum \(U_K\);
subtracting this error gives a valid original lower bound. Choosing \(K\)
polynomial in \(n\) and \(1/\varepsilon\) proves the comparison. The
[integrated review](../notes/review-20260922-integrated-smoothed-dp.md)
gives the details and discusses related approximation literature. The
substantive contribution under investigation remains exact smoothed message
construction.

## 9. Literature comparison and limits on novelty

The [independent priority audit](../notes/review-20260922-smoothed-dp-priority.md)
records the inspected theorem statements and source searches. The strongest
relevant comparisons are as follows.

- [Bhathena, Fattahi, Gómez, and Küçükyavuz, tree-structured indicator
  quadratics, Theorem 3.2](https://arxiv.org/html/2404.08178v1), already gives
  an exact quadratic arithmetic-time algorithm on trees without penalty
  noise or diagonal dominance. The present theorem is weaker on trees.
- Their [March 2026 structured-graph paper, Definition 5, Lemma 9, and
  Theorem 1](https://arxiv.org/html/2603.02103v1) is the closest exact
  algorithmic antecedent. Its bounds use graph growth, conditioning, solution
  bounds, and a uniform support-margin condition. The present theorem supplies
  a specified penalty-noise analysis for a narrower separator class and permits
  unbounded degree and nonpolynomial graph growth. A pointwise isolation bound
  is not a proof of their uniform margin hypothesis.
- [Gómez, Han, and Lozano, Theorem 1 and Section 4.2](https://arxiv.org/html/2405.03051)
  provides additive approximation for banded matrices under spectral bounds.
  [Choi, Fattahi, Gómez, Han, and Lozano, Theorem 4 and Section 8](https://arxiv.org/html/2608.22815v1)
  treats approximate decision diagrams through volume growth, boundary size,
  and spectral decay. These are substantial antecedents for approximation.
  The theorem here constructs exact messages for the perturbed instance;
  bounded block size does not imply bounded bandwidth or polynomial growth.
- Classical isolation comes from the smoothed discrete-optimization literature,
  including [Beier and Vöcking, STOC 2004 version](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/BeierV.pdf).
  More strongly, [Röglin and Teng, FOCS 2009, Theorem 6.2 and Section 6.2](https://www.roeglin.org/publications/FOCS09.pdf)
  establishes an **expected-time** equivalence for perturbed linear binary
  optimization with randomized pseudopolynomial algorithms and discusses
  finite precision. [Dughmi and Roughgarden, Proposition II.3](https://www.math.uwaterloo.ca/~cswamy/courses/co759/agt-material/blackbox.pdf)
  states the corresponding FPTAS-to-exact-smoothed conversion. Neither that
  conversion nor finite-precision smoothing is new in general.
- Eliminating continuous variables here yields
  \(g(z)+(\lambda+\xi)^Tz\), with
  \(g(z)=-\tfrac14c_S^TQ_{SS}^{-1}c_S\). The deterministic \(g\)
  is generally nonlinear, nonadditive, and nonintegral. A pseudopolynomial
  oracle in the noisy linear coefficients is not supplied merely by an
  additive approximation to this objective; distinct support values need
  not have unit spacing. The existing unit-penalty hardness construction
  makes this mismatch concrete. This prevents an immediate invocation of
  the cited linear-objective theorem, but does not rule out an extension of
  its methods or an alternative general smoothed argument.
- [Beier, Röglin, Rösner, and Vöcking, Theorem 1](https://link.springer.com/article/10.1007/s10107-022-01885-6)
  bounds smoothed Pareto sets with an arbitrary deterministic objective and
  one random linear objective. [Moitra and O'Donnell, Section 2](https://www.cs.cmu.edu/~odonnell/papers/pareto-optima.pdf)
  treats several random objective directions. The present branch costs have
  support-dependent deterministic curvature, slope, and intercept; those
  directions have not independently been perturbed. These results do not
  immediately count repeated intervals of the full nonlinear envelope.
- [Applegate et al., Section 6](https://arxiv.org/html/1805.06420) is a direct
  antecedent for smoothed parametric complexity, using angular perturbations
  and affine shortest-path costs. Standard quadratic lower-envelope routines
  are covered, for example, by [Sharir's notes, Theorem 3.2.6](https://www.math.tau.ac.il/~michas/notes.pdf).

The candidate addition is an explicit exact algorithm and finite-bit bound
for the nonlinear support problem, including all continuous messages and
the expected Cartesian-product work at bounded-size blocks. An unsuccessful
search does not establish priority. Equivalent results under other formulations,
and extensions of general smoothed-complexity methods, remain possible.

## 10. Scope, verification, and further questions

The graph hypothesis is bounded **biconnected-block size**, not arbitrary
bounded treewidth. Two-vertex separators require a new envelope argument.
The proof uses a uniform coordinate maximum principle; spectral conditioning
alone has not been shown to replace strict diagonal dominance. All competing
support bits must receive the specified independent noise. Marginal density
bounds without the needed conditional independence are insufficient. The
penalty noise does not perturb the Hessian, continuous linear coefficients,
or graph.

The algorithm's worst-case size remains exponential. The expectation can
deteriorate with small noise, a weak diagonal-dominance margin, large coefficient
bounds, or growing block size. The result proves neither a practical speedup
nor support stability at a useful perturbation scale. Implementing the efficient
envelope routine and assessing these issues are necessary for solver claims.
The finite-grid result and the additive interval are theoretical capabilities.

The work was developed in the
[frontier investigation](../notes/research-20260922-next-frontier.md) and
[finite-grid note](../notes/research-20260922-finite-grid-smoothing.md).
Independent reviews cover the
[scalar envelope](../notes/review-20260922-smoothed-envelope.md),
[deterministic block algorithm and arithmetic bound](../notes/review-20260922-smoothed-block-dp.md),
[grid atoms, formula deduplication, and bit costs](../notes/review-20260922-finite-grid-smoothing.md),
and [priority and significance](../notes/review-20260922-smoothed-dp-priority.md).
A [fresh integrated review](../notes/review-20260922-integrated-smoothed-dp.md)
rechecks these proofs together and the additive certificate; it also records
the deterministic approximation comparison above.
These reviews support the arguments but do not certify correctness or novelty.

The [exact-check record](../notes/research-20260922-smoothed-dp-checks.md)
reports the targeted command actually run during verification:

```text
python code/research_20260922/check_smoothed_block_dp.py
PASS {'instances': 9, 'messages': 66, 'support_qps': 892,
      'endpoint_bounds': 3580, 'derivative_bounds': 864, 'atoms': 48,
      'candidates': 100, 'outside_active_region': 32}
```

The checker uses exact rational elimination and exact quadratic-inequality
sets. It compares complete envelopes, including irrational crossings and ties,
against support enumeration on nine small instances: triangle chains, several
triangles sharing a vertex, and a four-cycle. It checks inactive atoms,
negative penalties, conditional bounds, and retained full quadratics used
outside their winning regions. The four-cycle is within this theorem's graph
class; the narrower historical wording in the check record predates the
reviewed biconnected-block formulation.

The checker deliberately uses expensive enumeration and does not implement
the efficient envelope algorithm. It therefore tests deterministic identities,
not the general expected running-time theorem. The finite-grid reviewer also
reports 52,266 exact interval-mass checks and 5,150 atomic-budget checks. Those
test endpoint and rounding details; the probabilistic limits and general bit
bounds rest on their written proofs. No Lean proof, project-wide verification,
or CI inspection was performed for this result.

The most consequential open directions are higher-dimensional separators,
weaker numerical assumptions supporting a uniform conditional domain, and
whether a general approximation-oracle conversion can recover the optimizer
conclusion without also constructing all messages. A separate priority search
for the exact finite-grid nonlinear-envelope statement is still appropriate.
