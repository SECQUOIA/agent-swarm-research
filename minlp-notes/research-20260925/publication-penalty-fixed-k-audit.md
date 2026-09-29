# Publication audit of the quadratic-count penalty boundary

Date: 2026-09-25. Reviewer: `publication_penalty/fixed_k_audit`.
Scope: the completed [penalty upper-bound note](penalty-upper-bound.md),
especially its fixed-count refinement. This is an independent audit of the
accepted proof, rather than a new research direction.

**Verdict.** I found no unresolved mathematical gap in the claim that, under
the stated compactness, convexity, rational encoding, and refined Slater
assumptions, at most \(k\) nonlinear native quadratic inequalities per
integer slice permit a sufficient integer norm penalty with

\[
 \operatorname{bit}(\rho)\le N^{O(k+1)}.
\]

The penalty has multiplier zero and gives both optimal-value and
solution-set exactness. The proof establishes an encoding bound, not a
practical numerical penalty, an efficient algorithm for choosing one, or
priority over the literature. Those limits must remain in any publication
statement. The strongest publication role is as a positive boundary paired
with the explicit lower-bound construction.

## Checks of the value lemma

I independently checked the following steps in the displayed proof.

1. **Deleting affine rows.** The affine space of the active rows is rational,
   including when the optimum itself is irrational. Every omitted affine
   row has positive slack at that optimum. A segment to any allegedly
   better feasible point in the enlarged convex set would enter a common
   neighborhood satisfying all omitted rows. Convexity of the objective
   and the nonlinear inequalities gives the contradiction. Neither a
   rational optimum nor knowledge of the active set is needed.
2. **Parametrization and boundedness.** A full-rank rational subsystem admits
   a parametrization whose free variables are original coordinates. Its
   coefficients have polynomial bit length by determinant bounds. The
   supplied coordinate box consequently bounds the free coordinates of
   the old optimum. The added ball is strict there, retains the old value,
   and supplies one more quadratic inequality. The zero-dimensional case
   is a rational point and is correctly treated separately.
3. **Regularization.** Relaxing all reduced inequalities to
   \(q_i\le\varepsilon\) gives a strict feasible point even when the
   original reduced problem has no constraint qualification. The relaxed
   ball gives one common compact bound. Adding
   \(\varepsilon\|u\|^2\) gives a positive-definite Lagrangian Hessian for
   every nonnegative multiplier vector. Ordinary differentiable convex
   KKT conditions therefore apply to every positive perturbation.
4. **Eliminating primal variables.** The determinant and adjugate formulas
   reconstruct the unique stationary point. The constraint numerators
   are exactly \(\Delta^2(q_i(p/\Delta)-\varepsilon)\), and the
   objective numerator is exactly
   \(\Delta^2(q_0(p/\Delta)+\varepsilon\|p/\Delta\|^2-w)\).
   The system is sufficient as well as necessary because convex KKT is
   sufficient. Its degree is at most \(2d+2\); no unlisted quantified
   primal variables remain.
5. **Coefficient height.** After rational affine substitution there are
   polynomially many quadratic coefficients of polynomial bit length.
   Taking a common denominator preserves a polynomial height bound.
   A determinant coefficient sums at most
   \(d!(h+2)^d\) products of \(d\) entry coefficients. Its logarithmic
   height is therefore polynomial in the original input size, including
   when the number of distinct monomials is large. Degree, coefficient
   height, and number of monomials are kept distinct in the proof.
6. **The quantified limit.** Uniform compactness proves the finite limit
   \(\theta(\varepsilon)\to\theta\). Formula (20) says that optimal
   perturbed values approach the free variable \(v\) at arbitrarily small
   positive perturbations. Since the limit exists, the formula defines
   exactly \(\{\theta\}\). It uses two quantifier blocks of sizes \(1\)
   and \(h+2\le k+3\), with one free variable. No multiplier limit or
   uniform multiplier bound is asserted or needed at this stage.
7. **Algebraic value and separation from zero.** I read the degree and
   integer coefficient-height clauses of Theorem 2.27, printed page 16 of
   [Basu's survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
   Substitution of those block sizes gives both bounds
   \(L^{O(k+1)}\). A quantifier-free singleton description contains a
   nonzero polynomial vanishing at that singleton. Removing a power of
   its variable and applying Cauchy's root bound to the reciprocal
   polynomial gives the claimed lower bound on a nonzero value.

The quantifier-elimination coefficient-height clause is essential. Merely
citing an arithmetic operation count or generic QCQP algebraic degree would
not justify the argument. The note uses the stronger clause correctly.

## Checks of the penalty consequence

The residual-distance program adds only affine inequalities and a bounded
scalar variable. A nonempty native slice without a zero residual has a
positive optimum by compactness; the value lemma applies without Slater
on that slice.

For a feasible original slice, the capped maximum common nonlinear slack
is positive under the stated refined Slater assumption. Minimizing its
negative is again a compact convex QCQP with at most \(k\) nonlinear
inequalities. The value lemma therefore bounds this positive slack away
from zero uniformly in the integer assignment.

Evaluating an optimal Lagrangian at this margin point gives

\[
 \sigma_z\sum_i\mu_i\le f(\bar x,z)-v_z\le2F.
\]

The sign is correct: the native affine multiplier terms are nonpositive
there, and the linking terms vanish. Only the nonlinear multipliers occur
in this sum. With them fixed, the remaining stationarity vector belongs to
the cone of active native affine normals and both signs of linking normals.
A conic representation with independent generators uses at most \(n\)
columns. Restricting to an invertible row minor and applying rational
determinant bounds controls its coefficients even when the stationarity
vector and nonlinear multipliers are irrational. It preserves stationarity
and complementarity and bounds one suitable linking multiplier. Redundant
affine rows do not require every possible multiplier certificate to be
bounded. The case with no nonlinear rows omits the slack argument.

All integer coordinates are explicitly bounded. Substituting them into
degree-two rational polynomials gives uniformly polynomial encoding length
for these auxiliary problems. The uniform bound depends on coefficient
height, dimension, and \(k\), rather than on the number of integer
assignments. Choosing the penalty strictly above the multiplier bound and
the objective range divided by the infeasible-slice residual bound gives
solution exactness. The infinity-norm conclusion transfers to the 1-norm
because the latter is larger and has the same zero set.

## Degeneracy stress check

The limit step must allow unbounded perturbed multipliers. A useful test is

\[
 \min\{1+u:u^2\le0,\ u^2\le1\}.
\]

Its value is \(1\), and the first constraint has no strict feasible point.
For \(\varepsilon=t^2\), \(0<t\le1/2\), the proof's perturbed problem has

\[
 u_t=-t,\qquad
 \lambda_t=\frac{1-2t^3}{2t},\qquad
 \theta(t^2)=1-t+t^4.
\]

The ball multiplier is zero. The stationary Hessian is \(1/t>0\), while

\[
 \lambda_t\longrightarrow+\infty,
 \qquad\theta(t^2)\longrightarrow1.
\]

A targeted exact SymPy command verified stationarity, primal slack,
objective value, the determinant numerators, and both limits. Every
identity passed. This example checks a meaningful singular boundary of
the proof: the value-limit formula remains valid without a bounded family
of perturbed multipliers. It is not a proof of the general lemma or a
verification of the quantifier-elimination theorem.

## Literature and publication scope

The note correctly distinguishes the sampling theorem from the older
deferred optimization proof in Grigoriev and Pasechnik. It also
correctly treats the full Kamminga–Rudolph version as a closer comparator
than its bounded approximation statement alone. A separate primary-source
audit checked the precise comparator statements; its findings are recorded in
[the companion prior-art audit](publication-penalty-fixed-k-prior-audit.md).

That audit identified a closer explicit application: Section 8.5,
Corollary 8.14 and equation (115), concern QCQP with a fixed total number
of constraints and no convexity assumption. I independently reread that
section and the algebraic-representation proof in Sections 7.1–7.2.
Following our affine-face reduction, equations
\(q_i(u)+s_i^2=0\) encode the remaining inequalities, with the added
ball bounding both the primal variables and their squared slacks. This
fits the source's bounded quadratic-map setting. Its Theorem 7.2 proof
provides explicit integer coefficient-height bounds for algebraic
representations; the connection is not an inference from the numerical
approximation guarantee alone. The direct KKT proof's explicit exponent
linear in \(k\) should be kept distinct from the source's more general
parameter bounds. I recommended adding this closer predecessor to the
main note rather than leaving its relevance phrased as a possibility.
The parent incorporated that comparison, and I reread the revised
paragraph. Its mathematical and priority scope is correct; I also
recommended naming the added bounding ball explicitly, since affine-face
deletion alone need not leave a bounded set.

These are derived consequences of established convex duality and real
algebraic geometry. Their publication value depends on the explicit
penalty-encoding boundary and its relationship to the lower construction.
This review supports correctness under the stated assumptions; it does
not establish priority or that the value lemma is an independent new
contribution.

I also read the earlier general upper-bound proof, KKT sparsification,
reciprocal graph, and source-correction records. Their slice arguments are
consistent with this refinement. I did not rederive every explicit
Basu–Roy radius constant or reprove the external quantifier-elimination
theorem. No Lean build, project-wide test, or CI inspection was performed
for this audit.
