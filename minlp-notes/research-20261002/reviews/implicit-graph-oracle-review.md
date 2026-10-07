# Review of the implicit polynomial graph oracle interface

Date: 2026-10-02. Status: fresh completed-text review passed after the
zero-anchor and singleton-dependent preprocessing cases were clarified.
No mathematical or bit-complexity blocker remains under the stated global
graph and curvature premises.

This review covers the actual
[interface note](../new-direction/implicit-graph-oracle-interface.md),
including all 24 numbered equations. It also checked the linked local
[convex-patch evaluation proof](../new-direction/convex-patch-evaluation.md)
and [exact fallback proof](../new-direction/polynomial-exact-fallback.md).
The previously verified GLS and fixed-block quantifier-elimination source
interfaces are used as stated there; this review did not conduct a new
source or literature search.

## 1. Scalar oracles and global premises

The monotonicity and endpoint brackets on the entire real anchor hull
give one root in each prescribed dependent interval. The nonzero derivative
also gives smooth local extensions at boundary points. Defining the chart
on the real hull is necessary for rounding integer coordinates and for
evaluating derivatives at hull midpoints that are not integral.

At a rational anchor, exact rational sign tests support ordinary scalar
bisection. Rational brackets certify the actual implicit root; numerical
root approximants need not themselves satisfy the graph equation. Factor
intervals converge at a rate controlled by rational absolute sensitivity
bounds. Negative costs and cancellation do not affect this argument.

The derivative bounds in equation (5) are valid through order three.
The third-order implicit derivative has terms bounded by
`A(1+P1)^3` and `3A(1+P1)P2`, followed by division by `mu`.
These are entry bounds; the note correctly sums entries to obtain matrix
and gradient variation bounds. Intersecting denominator intervals with
the supplied positive range avoids spurious division through zero.
All derivative orders and reciprocal powers are fixed, so precision work
is polynomial in the encoded bounds, query length and accuracy bits.

Global positivity, bracketing and curvature remain valid premises or
separately verified assertions. The note does not claim that individual
row brackets certify those global facts or that arbitrary polynomial
positivity can be checked in polynomial time.

Two preprocessing clarifications were checked in the final text. With no
remaining anchor, the algorithm bypasses DP and returns the fixed implicit
graph point. This avoids demanding zero-width rational factor intervals
from a zero DP error budget. A singleton dependent interval can be
substituted because the global bracket premise then forces its defining
polynomial to vanish at that value throughout the anchor hull; no residual
anchor constraint is discarded.

## 2. Approximate DP and retained-cell witnesses

Let `D=sum_B delta_B<=E` and let `H^-` be the sum of lower costs.
Then `G-D<=H^-<=G`. Rounding a covered global optimizer gives
`m^-<=f*+E`; the lower-cost minimizing assignment has actual objective
at most `m^-+D`. Thus the updated incumbent is a certified upper bound
on an exact implicit feasible witness, even when its value is irrational.

Fixed-cell rounding gives `q_C^- - E<=G(t)` throughout the corresponding
current physical cell domain. Initial whole-box coverage and nested
partitions therefore preserve every global optimizer inductively. The
weak retention inequality preserves ties. For a retained cell, an attained
DP min-marginal supplies a consistent witness with

\[
 G(v)\le q_C^-+D\le U+E+D
       \le f^*+2E+2D\le f^*+4E.
\]

The error budget applies to costs assigned once per bag. Refining reused
rows when the level changes is necessary and is explicitly required.
Exact rational DP does not require exact comparison of algebraic objective
values. Each message value sums costs from disjoint assigned bags; its
encoding length does not grow with the total number of table rows.

The corresponding semiconcavity interval has length
`La+8E/a=La+nLh^2/a`, so the counting factor changes from `1+n/2`
to `1+n`. Approximate costs may depend on sampled coefficients: the
counting argument still applies to the resulting actual near-optimal
witnesses. No conditioning on the pruning history is needed.

## 3. Certified derivative tests and stopping constants

The gradient enclosure in equation (13) includes both the midpoint
evaluation error and variation across the hull. It is applied only to
continuous anchor coordinates, where the original-box first-order
condition justifies fixing an original bound.

Symmetric entry approximations with error `epsilon_H/dim(C)` give the
claimed operator error. The rational positive-definiteness test in
equation (14) accounts for this error and the third-derivative variation,
so it certifies a positive Hessian modulus throughout the patch.

Under the growth and active-margin assumptions used only for stopping,
the witness radius is `h sqrt(nL/(2g0))`. The coarse
`A=2+nL/g0` still bounds the cell and hull distances. At equation (15),
the gradient enclosure error relative to the optimum is at most
`3tau/4`, and the tested Hessian matrix is at least `(g0/4)I`.
These strict margins suffice for all claimed stopping decisions.
The proof does not replace algebraic midpoint Hessians by purported exact
rational evaluations.

## 4. Weak separation and GLS evaluation

For two anchor points in the patch, their one-norm distance is at most
`D1`. Hence the approximate-gradient affine function in equation (18)
is a valid lower support. A query below its value is strictly separated
by the rational normal `(g_hat,-1)`. Otherwise its epigraph violation
is at most `epsilon`, giving the required nearby-body answer. The normal
has infinity norm at least one, so normalization is well defined and
has polynomial bit cost. No exact algebraic equality decision is hidden
in either branch.

The capped epigraph has the stated rational inner and outer radii.
The linked GLS argument handles comparison against the eroded body and
the returned point's approximate feasibility. Rational projection repairs
the anchor box constraint. The extra `eta/2` upper-value allowance is
necessary because the feasible witness value is generally irrational.
Equations (19)--(21) correctly give
`a<=G*<=G(v)<=U` and `U-a<=eta`.

The exact feasible witness is `(v,psi(v))`; only its anchor coordinates
are rational. Strong convexity bounds anchor distance even at boundary
minimizers. The chart Lipschitz bound and the two half-error allocations
in equation (23) then give the stated rational approximation to the
physical optimizer. The note correctly avoids claiming that this rational
ambient approximation satisfies the graph equations.

## 5. Exact output and fallback

Graph equations, branch intervals and anchor-box KKT conditions describe
the same reduced constrained minimizer. Positivity of each `q_y` makes
the displayed graph-multiplier elimination valid. The certified reduced
strong convexity gives one primal optimizer; no positive ambient Hessian
or exact active-set identification is needed for subsequent evaluation.

The fallback is applied to the original polynomial objective and compact
graph domain. Adding the dependent coordinates to the two quantified
blocks preserves fixed degree and a base-only exponential format bound.
Integer-label expansion has logarithmic size polynomial in the base
input. The cited elimination and univariate-refinement interface therefore
retains polynomial dependence on sampled coefficient bits and requested
precision. It covers ties and continua of optimizers.

For fallback approximations, clipping anchors and reattaching their exact
scalar roots preserves feasibility. Independently clipping all physical
coordinates would not; the note explicitly excludes that operation.

## 6. Scope and targeted checks

This is an interface proof. It does not establish a complete smoothed
theorem, its finite-noise tails or its common sampling law, and it does not
implement a general optimizer. The distinction between a compact final
patch description and a potentially large global pruning trace is stated
correctly.

Targeted commands run for this review were `cat` and `sed` on the three
linked notes and `python3 - <<'PY'` for document checks. The initial Python
check passed interface whitespace, balanced display delimiters, equation
tags 1 through 24 and local links. A final scoped Python check of the
interface and this review also passed whitespace, display delimiters and
local links, and reconfirmed the interface tags. No executable optimizer
test, project-wide verification, CI inspection or external search was
performed.

## 7. Inspection of the cubic-chart diagnostic

A separate inspection of
[`check_smoothed_implicit_graph.py`](../new-direction/check_smoothed_implicit_graph.py)
and its imported sparse-DP and exhaustive-grid routines found no false
assertion or model mismatch. The
[saved report](../new-direction/smoothed-implicit-graph-check-results.json)
records the author's successful run: five stages, 296 lower-cost
min-marginal comparisons, 82 retained-cell witness checks, 120 discarded
cells, 326 nonpoint root brackets and 18 noisy value-refinement cases.
These are counts of checks, not claims about distinct points or asymptotic
behavior. This inspection did not rerun the already-passing diagnostic.

The scalar equation `u+u^3=rhs` has derivative `1+3u^2>=1` on its
entire interval, and exact rational bisection maintains valid sign
brackets. The factor interval computation correctly encloses both the
control square and the optional linear dependent-coordinate noise.
Its width bound uses the sum of their absolute derivative bounds, so
separate interval terms and negative noise coefficients cause no error.
The rational-root test also establishes that a queried chart value is
irrational; the test is not confined to rational graph roots.

For control centers `c=+/-1/2`, the reduced scalar curvature is

\[
 \frac{2-6u^2+12cu}{(1+3u^2)^3}\le\frac72.
\]

Thus the fixture's largest anchor diagonal is at most
`2+(7/2)(1+1/16)=183/32<6`, validating its supplied `L=6`.
The retained-coordinate squares prove anchor point growth at the known
optimum. The script compares every sparse rational lower min-marginal
with an independently enumerated complete-grid minimum. Each retained
cell obtains a globally consistent witness whose certified true upper
value obeys the `4E` bound. The known optimum remains covered throughout.

After integer labels are fixed, the final closure uses rational interval
bounds proving nonnegative curvature for both scalar control terms.
The true reduced Hessian is then `2I` plus two positive-semidefinite
rank-one terms. This certifies the nonpolynomial objective on the whole
reported patch, rather than just the sampled lower-cost rows.

The DP and closure fixture uses zero perturbations. The separate nonzero
dependent-noise cases test cost enclosure and refinement consistency.
The diagnostic does not exercise noisy DP trajectories, active continuous
bound fixing, the generic approximate midpoint-Hessian test, the GLS weak
separator, the algebraic fallback or a smoothed expected-work bound.
Its useful finite coverage is accurately narrower than the mathematical
interface proved above. Only read-only code and report inspection was
performed for this addendum; no executable diagnostic was rerun.
