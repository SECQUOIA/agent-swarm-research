# Exact smoothed indicator quadratic programming at fixed treewidth

Date: 2026-09-22. Status: consolidated theorem and proof; a fresh
[integrated adversarial review](../notes/review-20260922-fixed-treewidth-result.md)
found no substantive gap. The underlying deterministic construction,
near-optimal support argument, and finite-grid argument have separate review
records linked below. Novelty remains provisional.

The later [spectral-bound construction](smoothed-spectral-indicator-messages.md)
removes diagonal dominance and constructs complete message dictionaries
through approximate restricted optimization and a parameter net. The present
result is retained as an independently reviewed direct dynamic-programming
construction and an application of the higher-moment theorem.

For a symmetric strictly diagonally dominant indicator quadratic program on
a graph of fixed treewidth, independently perturbing only its indicator
penalties permits exact construction of every continuous dynamic-programming
message in polynomial expected bit time. The perturbations are rational and
use only logarithmically many random bits per coordinate. The numerical
bounds and treewidth are fixed; the running-time bound is polynomial in the
inverse noise scale, not its logarithm.

The result concerns full quadratic support formulas. It allows arbitrary
branching, unbounded degrees, and biconnected blocks of unbounded size. Its
proof combines a general bound on all fixed moments of active support counts
with exact algebraic computation in fixed-dimensional bags. The algebraic
construction can have a large polynomial degree and is not a practical
speedup claim. A separate adaptation of classical smoothed optimization
methods can already recover the optimizer-only conclusion; constructing all
continuous messages is the stronger capability studied here.

## 1. Model and statement

Consider the rational optimization problem

\[
 \min\left\{x^TQx+c^Tx+\sum_{i=1}^n(\lambda_i+\xi_i)z_i:
       x_i(1-z_i)=0,\quad z\in\{0,1\}^n\right\}.       \tag{1}
\]

There are no other constraints. The matrix \(Q\) is symmetric. Use rational
bounds satisfying

\[
 0<d\le Q_{ii}\le D,\qquad
 \sum_{j\ne i}|Q_{ij}|\le\rho Q_{ii},\qquad
 0\le\rho<1,\qquad |c_i|\le C,\quad C>0.             \tag{2}
\]

The penalties \(\lambda_i\) can have either sign. The sparsity graph has an
edge \(ij\) when \(Q_{ij}\ne0\), for \(i\ne j\). Fix a tree decomposition
of width at most \(w\) before drawing the noise. It can be supplied as part
of the input. The result below includes its size in the input length; a
reduced decomposition has at most \(n\) nonempty bags. The case \(w=0\)
is separable, so take \(w\ge1\) below.

Put

\[
 M=\frac{C}{2d(1-\rho)},\qquad I=[-M,M],\qquad
 L=2\sqrt w\,\rho DM.                                \tag{3}
\]

The algorithm in Section 4 has a deterministic bit bound

\[
 P_w(\ell)\,(1+n+K)^{a(w)},                           \tag{4}
\]

where \(K\) is the sum of its final message dictionary sizes over all bags
and boundary indicator modes, \(\ell\) is the full rational input length,
including the encoding of the rational smoothing scale \(\sigma\),
\(P_w\) is a polynomial, and \(a(w)\) is a finite computable constant.
They are fixed by the chosen fixed-dimensional algebraic algorithm.

**Theorem 1.** Choose an integer \(p\ge\max\{1,a(w)\}\), a positive
rational \(\sigma\), and let \(N\) be the smallest power of two satisfying

\[
 N\ge 2n(n+1)^p.                                      \tag{5}
\]

Independently draw each \(\xi_i\) uniformly from

\[
 \left\{-\sigma+\frac{2\sigma j}{N-1}:
                    j=0,\ldots,N-1\right\}.            \tag{6}
\]

The algorithm constructs exact full quadratic representations of every
message of the reduced rooted decomposition on its entire conditional box,
for every boundary indicator mode,
and returns an exact optimizer and optimal value of (1). It terminates
correctly for every noise realization. For fixed \(w,d,D,C,\rho\), its
expected bit running time is polynomial in the input length, including
the encoding of \(\sigma\), and
\(1/\sigma\). Each coordinate uses exactly \(\log_2N=O_w(\log(n+1))\)
random bits. The algorithm neither rejects slow samples nor redraws noise.

For clarity, set \(\phi=1/(2\sigma)\) and

\[
 J=\left[1+8ML\sqrt w\,n\phi(n+1)^p\right]^w.
                                                               \tag{7}
\]

Every message dictionary has \(p\)-th moment at most \(eJ^p\). For a
reduced decomposition, there are at most \(2^wn\) such dictionaries, and

\[
 \mathbb E(1+n+K)^p
       \le e\left[(1+n+2^wn)J\right]^p.               \tag{8}
\]

The exponent depends on \(w\) through the algebraic construction and its
required moment order. The theorem is not a fixed-parameter running-time
claim with a polynomial degree independent of \(w\).

## 2. Conditional support quadratics and a uniform domain

Strict diagonal dominance and symmetry make \(Q\) positive definite.
Fix a support of free active coordinates, set inactive coordinates to zero,
and fix any remaining boundary coordinates in \(I\). Its conditional
quadratic has a unique minimizer. Every free coordinate of that minimizer
also belongs to \(I\).

Indeed, let \(X\) be the largest absolute free coordinate. Stationarity in
a coordinate attaining \(X\), followed by (2), gives

\[
 X\le \frac{C}{2d}+\rho\max\{X,M\}.
\]

If \(X>M\), this implies \(X\le C/[2d(1-\rho)]=M\), a contradiction.
The empty free support needs no argument. Penalties do not enter this bound.

Root the decomposition. Contract an adjacent pair of bags whenever one is
contained in the other. The bags then have size at most \(w+1\), and every
parent separator has size at most \(w\). Each nonroot bag contains a vertex
absent from its parent. Running intersection assigns that vertex uniquely
to its highest bag, proving the bound of \(n\) nonempty bags.

Assign every original objective term to its highest containing bag. Bags
containing the endpoints of an edge form a connected subtree, so this owner
exists and is unique. For a bag with parent separator \(S\), its subtree
objective contains every term involving an internal vertex and contains no
term involving only \(S\). All interactions with the outside pass through
\(S\).

For each indicator mode on \(S\), fix its inactive coordinates to zero and
let its \(k\le w\) active coordinates range over \(I^k\). An indicator
equal to one permits a zero continuous value. Each fixed internal support
\(z\) gives a full rational quadratic branch

\[
 F_z(t)=q_z(t)+\xi_U^Tz,\qquad t\in I^k,              \tag{9}
\]

where \(U\) is the set of internal vertices and \(q_z\) includes the
deterministic penalties. It is obtained by unrestricted positive definite
quadratic elimination. Boundary penalties are absent by term ownership.
The message is the lower envelope of these branches.

The derivative of a branch with respect to a boundary coordinate \(s\)
is

\[
 \frac{\partial q_z}{\partial t_s}
       =2\sum_{i\in U}Q_{si}x_i^*(t).
\]

The maximum principle bounds its absolute value by \(2\rho DM\). Thus
every branch is \(L\)-Lipschitz in Euclidean distance on \(I^k\), using
the common bound (3). This bound is independent of subtree size, penalties,
and support. No concavity or degree restriction is needed for the
probability argument that follows.

## 3. All fixed moments under rational penalty noise

We prove the probabilistic ingredient directly, including atoms. Let
\(Z\subseteq\{0,1\}^m\) be nonempty, and let \(g_z\) be arbitrary
deterministic real costs. Suppose independent coordinates obey the interval
bound

\[
 \Pr\{\xi_i\in A\}\le\phi\,\operatorname{length}(A)+\alpha
                                                               \tag{10}
\]

for every interval, including closed intervals and singletons. The grid
(6) satisfies (10) with \(\alpha=1/N\): its spacing is
\(2\sigma/(N-1)\), and an interval contains at most its length divided
by that spacing plus one grid point.

For \(\delta\ge0\), let \(A_\delta\) be the supports whose costs
\(g_z+\xi^Tz\) are within \(\delta\) of the minimum, and let
\(V_\delta\) be the VC dimension of this binary family. A coordinate set
is shattered if all its binary patterns occur as projections of family
members.

**Lemma 2.** For \(1\le r\le m\),

\[
 \Pr\{V_\delta\ge r\}
       \le {m\choose r}(2\phi\delta+\alpha)^r.        \tag{11}
\]

**Proof.** Fix an \(r\)-coordinate set \(R\) and condition on all other
noise coordinates. For each pattern \(a\in\{0,1\}^R\), define

\[
 C_a=\min_{z_R=a}\left(g_z+\sum_{i\notin R}\xi_i z_i\right).
\]

An empty class prevents shattering. Otherwise, if \(R\) is shattered by
\(A_\delta\), every class minimum \(C_a+\xi_R^Ta\) is within
\(\delta\) of the global minimum. Comparing the zero pattern and the
unit pattern at each \(i\in R\) yields

\[
 |C_{e_i}+\xi_i-C_0|\le\delta.
\]

The conditional class costs do not depend on \(\xi_R\). Independence
and (10) therefore bound this event by \((2\phi\delta+\alpha)^r\).
Take the union over \(R\). Every shattered larger set contains a
shattered \(r\)-set. \(\square\)

The classical Sauer--Shelah lemma gives

\[
 |A_\delta|\le\sum_{j=0}^{V_\delta}{m\choose j}
                    \le(m+1)^{V_\delta}.
\]

The second inequality follows by encoding a subset of size at most
\(V_\delta\) as its ordered elements followed by zeros. Hence, for any
real \(p\ge1\), the tail bound (11) implies

\[
 \begin{aligned}
 \mathbb E|A_\delta|^p
 &\le 1+\sum_{r=1}^m(m+1)^{pr}\Pr\{V_\delta\ge r\}\\
 &\le\exp\left[m(m+1)^p(2\phi\delta+\alpha)\right].  \tag{12}
 \end{aligned}
\]

This argument permits arbitrary deterministic costs and any feasible
subset of the binary cube. It does not multiply dependent coordinate-wise
near-tie probabilities: the simultaneous class conditioning in Lemma 2 is
what makes the product bound valid.

Now let \(q_z\) be deterministic \(L\)-Lipschitz functions on \(I^k\),
and let \(H\) count all supports minimizing
\(q_z(t)+\xi^Tz\) at some point of the box. This includes isolated ties
and repeated identical formulas. Choose the global value

\[
 \delta=\frac1{4n\phi(n+1)^p}.                        \tag{13}
\]

For \(m\le n\), (5), (12), and (13) give
\(\mathbb E|A_\delta(t)|^p\le e\) at every fixed parameter point.
For \(L>0\), partition the box into cubes with Euclidean covering radius
\(\eta=\delta/(2L)\), and use their centers. There is a net with at most

\[
 J_k\le\left[1+\frac{2ML\sqrt k}{\delta}\right]^k\le J
\]

points. If \(z\) minimizes at \(t\), a net point \(s\) within
\(\eta\), together with a minimizer \(u\) at \(s\), satisfies

\[
 F_z(s)\le F_z(t)+L\eta
          \le F_u(t)+L\eta
          \le F_u(s)+2L\eta.
\]

Thus every active support belongs to a near-optimal set at a net point.
Convexity yields

\[
 H^p\le J_k^{p-1}\sum_s|A_\delta(s)|^p,
 \qquad \mathbb EH^p\le eJ_k^p\le eJ^p.              \tag{14}
\]

If \(L=0\) or \(k=0\), one parameter point suffices and the same bound
holds. For \(m=0\), only one support is present. Independence across net
points or across messages is unnecessary.

In particular, the number of distinct necessary quadratic formulas is at
most \(H\). This avoids any genericity assumption for grid noise. The
bound counts supports and formulas, not their connected winning regions.
Even a small number of general Lipschitz branches can alternate infinitely
often, which is irrelevant to (14).

## 4. Exact message construction in polynomial dictionary work

A message dictionary stores full quadratic polynomials, with an internal
support representative for each. Merge identical polynomials. Retain only
polynomials that uniquely minimize among the distinct formulas somewhere
in the relative interior of the parameter box. For a zero-dimensional mode,
retain one minimum constant.

This pruning preserves the envelope on the entire closed box. A finite
family of distinct polynomials has a dense set of unique-minimizer points:
each nonzero polynomial difference has a zero set with empty interior.
Every point is a limit of such points; along a subsequence one retained
formula wins, and continuity gives equality at the limit. Supports that win
only on boundaries or other lower-dimensional sets need not be retained.

Suppose the child dictionaries of a bag \(B\) are available. Fix an
indicator mode on all of \(B\), and lift the selected child-mode
polynomials to its active bag coordinates. There are at most \(w+1\)
such coordinates. Take all pairwise differences within each child
dictionary, discard identically zero differences after restriction, and
include the box-boundary polynomials. If the selected child dictionary
sizes are \(K_j\), this gives at most

\[
 O_w\left(1+\sum_jK_j^2\right)
\]

polynomials of degree at most two.

Construct a sign-invariant cylindrical algebraic decomposition (CAD). In
fixed dimension this requires polynomial work in the number and rational
bit length of the input polynomials. For every full-dimensional cell inside
the relative open box, use its sample point to select one minimum formula
from each child. Identical restricted formulas may use a fixed tie rule.
All selected formulas remain minimal on the cell. Their sum, with the
objective terms owned by \(B\), is a full quadratic for a consistent
support in the child interiors. Those interiors are disjoint and have no
edges between them.

For each selected tuple, set inactive bag coordinates to zero and
unrestrictedly minimize over its active coordinates outside the parent
separator. The Hessian of these forgotten coordinates is positive definite,
as a Schur complement of a principal submatrix of \(Q\). The resulting
full quadratic is exactly the value of a complete internal support. Store
it as a candidate for the resulting parent boundary mode. Repeat for all
at most \(2^{w+1}\) bag modes. With no active bag coordinates, select a
tuple at the single point directly.

The CAD cells discover support tuples; they are not constraints on the
subsequent quadratic elimination. This distinction is essential for exact
coverage and rational coefficients.

**Validity.** Every candidate is the conditional value of a feasible complete
support at every separator point. It cannot lie below the true message,
including outside the cell that generated it.

**Coverage.** Fix any separator point and choose a conditional optimizer.
Its bag coordinates lie in the box by Section 2. Approach these bag
coordinates by points in relative full-dimensional arrangement cells.
Only finitely many tuples occur, so one occurs along a subsequence. By
continuity all its child formulas attain the child envelope values at the
target coordinates. Its summed bag polynomial therefore attains the true
conditional value there. Unrestricted minimization over forgotten bag
coordinates can only decrease that value; validity gives the reverse
inequality. This candidate attains the true message value at the specified
separator point. The approximating sequence is allowed to change boundary
coordinates because it only discovers a full polynomial, later evaluated
at the required boundary point.

Prune the candidates using another fixed-dimensional sign-invariant
decomposition, now in at most \(w\) variables. Retain the unique minimum
formula on every relative full-dimensional cell after duplicate merging.
The initial continuity argument proves coverage on the closed box. This
completes the induction from the leaves. At the root, the separator is empty
and the minimum constant gives the exact optimum and a support. Solve its
positive definite principal system to recover the continuous optimizer.

The number of comparison polynomials, cells, selected tuples, candidates,
and pruning operations at a bag is polynomial in the sum of its child
dictionary sizes. The exponent depends only on \(w\). Summing over bags
gives polynomial work in \(n+K\). No Cartesian product over all children
is enumerated, so arbitrary branching causes no exponential factor of its
own. The decomposition and the list of boundary modes are fixed before the
noise is sampled.

## 5. Bit complexity and expectation

Every stored candidate is a fixed-support Schur-complement expression from
the original rational input. Clearing denominators and using determinant
bounds gives polynomial bit length in the original input length and
\(\log N\), uniformly over all supports and grid outcomes. Intermediate
bag sums involve at most \(n\) such expressions, and elimination has
dimension at most \(w+1\). Reduced rational arithmetic has polynomial
intermediate bit length as well.

CAD sample coordinates are used only to choose support formulas. They are
never substituted into stored message coefficients. The coefficients
therefore remain rational; recursive CAD calls do not generate towers of
algebraic extensions. Standard fixed-dimensional CAD has polynomial bit
complexity in the number and encoding length of its rational input
polynomials. Exact support recovery is rational linear algebra of
polynomial bit complexity. These facts give (4).

Each final dictionary contains at most the number of supports active
somewhere in its complete conditional box. Section 3 bounds its \(p\)-th
moment by \(eJ^p\). Add \(n+1\) constant summands to the at most
\(2^wn\) dictionary sizes and apply convexity:

\[
 (1+n+K)^p\le(1+n+2^wn)^{p-1}
       \left(1+n+\sum_{\text{dictionaries}}K_j^p\right).
\]

Taking expectations proves (8). Shared subtree noise creates dependence,
but this inequality does not require independence between dictionaries.
Since \(p\ge a(w)\), equations (4) and (8) prove Theorem 1. The finite
grid has polynomial cardinality for fixed \(w\); its random coordinates
have polynomial rational encoding length. Only the runtime is averaged.

The same proof with \(\alpha=0\) proves all fixed dictionary moments
under continuous independent densities bounded by \(\phi\), with a
slightly smaller net. That is a mathematical size bound and an algebraic
computation statement. The rational grid is what supplies the stated
Turing algorithm.

## 6. Consequences, prior results, and significance

For the sampled instance the messages are exact functions, not values at
a parameter mesh. The net in Section 3 is only a proof device. These
functions can answer conditional value queries anywhere in their boxes and
support exact reconstruction through the fixed decomposition. This is a
potential foundation for decomposition-based MINLP methods with discrete
activation and convex quadratic continuous subproblems. It does not yet
show an efficient practical representation at useful noise scales.

An elementary objective comparison gives an additive certificate for the
unperturbed problem. If the sampled optimizer is \((\widehat x,\widehat
z)\), with value \(v_\xi\), set

\[
 U=v_\xi-\xi^T\widehat z,\qquad
 B=v_\xi-\sum_i\max\{\xi_i,0\}.
\]

Then \(B\le v_0\le U\) and

\[
 U-B=\sum_{\widehat z_i=0}\max\{\xi_i,0\}
       +\sum_{\widehat z_i=1}\max\{-\xi_i,0\}
       \le n\sigma.
\]

Taking \(\sigma=\varepsilon/n\) gives an always valid additive interval
in expected time polynomial in \(1/\varepsilon\), under the fixed
assumptions. This comparison is classical. It is not a relative FPTAS or
an original approximation frontier: deterministic grid dynamic programming
already supplies additive certificates under these same bounds.

The strongest relevant comparisons are:

- [Röglin and Teng, FOCS 2009, Section 6](https://www.roeglin.org/publications/FOCS09.pdf)
  already establishes higher-gap estimates, fixed moment bounds, expected
  smoothed algorithms, and finite-precision arguments for binary linear
  optimization. The conditioning argument here is closely related. The
  local [approximation-to-exact investigation](../notes/research-20260922-approximation-exact-smoothing.md)
  adapts that method to the nonlinear deterministic support costs of (1),
  using certified additive optimization and a partition procedure. Its
  candidate optimizer-only result therefore limits novelty of that part of
  Theorem 1. The theorem here additionally constructs all continuous messages.
- The classical [Sauer--Shelah lemma](https://www.sciencedirect.com/science/article/pii/0097316572900192)
  supplies the combinatorial counting step.
  The [higher-moment investigation](../notes/research-20260922-envelope-higher-moments.md)
  records the general Lipschitz statement and further Pareto-count antecedents.
  The candidate addition is the explicit parametric application with one
  shared random penalty direction, not the introduction of moment bounds
  in smoothed optimization.
- [Bhathena, Fattahi, Gómez, and Küçükyavuz, Theorem 3.2](https://arxiv.org/html/2404.08178v1)
  gives an exact arithmetic algorithm on trees without this noise or diagonal
  dominance. Their [structured-graph paper, Definition 5, Lemma 9, and Theorem 1](https://arxiv.org/html/2603.02103v1)
  is a closer exact algorithmic antecedent beyond trees, using graph growth,
  numerical bounds, and a uniform support-margin condition. The present
  theorem allows any fixed treewidth and removes the deterministic margin
  through a specified penalty-noise model. It is weaker on trees.
- [Arnon, Collins, and McCallum, CAD I](https://www.lacl.fr/pvanier/cours/2015-2016/lm/articles/Cylindrical%20Algebraic%20Decomposition%20I-%20The%20Basic%20Algorithm.pdf)
  supplies the classical fixed-dimensional sign decomposition machinery.
  The algorithmic contribution under investigation is its combination with
  full support elimination and moment bounds, not a new CAD algorithm.
- The [bounded-block result](smoothed-indicator-block-dp.md) gives a sharper
  explicit operation bound and uses only univariate quadratic envelopes.
  Fixed treewidth strictly extends its graph class, but the more elementary
  algorithm can be preferable when its graph assumption holds.

An unsuccessful literature search does not establish novelty. Equivalent
parametric smoothed-complexity results, or older formulations combining
generalized gap estimates with fixed-dimensional arrangements, remain
possible. A dedicated priority review of the consolidated theorem is still
required before a publication claim.

## 7. Verification and limitations

The constituent investigations are the
[deterministic arrangement construction](../notes/research-20260922-planar-message-algorithm.md),
[its independent review](../notes/review-20260922-planar-message-algorithm.md),
and the [general moment proof](../notes/research-20260922-envelope-higher-moments.md).
The planar deterministic argument uses dimension three; its proof extends
here to fixed bag dimension \(w+1\) without a planar topology claim. The
separate [monotone finite-grid transfer](../notes/research-20260922-finite-grid-planar.md)
is useful in other settings but is unnecessary for the direct atomic proof
in Section 3.

The deterministic reviewer checked 256 exact Schur-complement identities
for a branching width-two bag. The bounded-block work checked complete
scalar envelopes against support enumeration. Those computations support
specific algebraic identities and conventions. They do not verify CAD
construction, higher moments, or the arbitrary-treewidth theorem. No Lean
formalization or computational test proves the probability argument.
Fresh integrated adversarial review remains pending. A targeted Python scan
of this file's local Markdown links and trailing whitespace passed. No
project-wide checks or CI inspection were used for this result.

The numerical assumptions supply a uniform conditional box and branch
Lipschitz bound. Mere spectral conditioning has not been proved sufficient
to replace them. All internal indicator bits receive independent noise;
marginal anti-concentration without the corresponding conditional product
structure is insufficient for Lemma 2. Additional global constraints would
require new support formulas, domain bounds, and separator bookkeeping.

Worst-case dictionaries and runtime remain exponential. The expectation
can deteriorate with small noise, a small diagonal-dominance margin, large
coefficient bounds, or growing width. The noise changes the objective and
need not preserve the original optimizer. The theorem shows neither that
CAD is competitive with existing solvers nor that penalties can be perturbed
at a useful application scale without changing desired decisions.

The next consequential questions are whether a simpler message-construction
algorithm gives a useful exponent, whether weaker numerical assumptions
still bound conditional supports uniformly, and how the full-message result
compares precisely with earlier generalized-gap and parametric optimization
theory.
