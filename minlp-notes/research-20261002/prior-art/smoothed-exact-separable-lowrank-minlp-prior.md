# Prior-art audit: smoothed exact separable MINLP with a low-rank concave term

Date: 2026-10-02. This audit concerns a candidate expected-exact theorem, not
a priority claim. The target is

\[
 F_d(x)=\sum_{i=1}^n G_i(x_i)-\frac{\alpha}{2}\|Tx\|^2+d^TTx,
 \qquad x_i\in [\ell_i,u_i]\cap\mathbb Z,
\]

where the $G_i$ are rational convex univariate quartics, $T$ has rank at most
$r$, and the entries of $d$ are independently sampled from one finite
rational grid. The proposed algorithm uses separable convex integer
recourse in a Fenchel lift, refines a low-dimensional grid, and chooses the
grid size so that its certified objective gap is below the rational objective
value spacing. Its claimed guarantee is exact rational optimization for each
draw, with expected bit work parameterized by $r$ and a curvature-to-noise
range ratio, without quadratic growth. The theorem and its finite-grid
accounting remain under review.

## Exact algorithms for special cases

Several cases are already easier and should not support a solver-advantage
claim.

- On a binary box, each univariate $G_i$ is affine on its two feasible
  points. For rank one, complementing variables to make the factor
  coefficients have one sign makes the expanded pairwise binary objective
  submodular; an $s$-$t$ minimum cut solves it exactly, without smoothing or
  a growth assumption. For fixed rank, fixed-rank zonotope and
  hyperplane-arrangement algorithms solve the resulting binary quadratic
  problem exactly in $n^{O(r)}$ time. The latter is XP in rank, not an FPT
  bound. These baselines and their primary references are detailed in the
  [separable low-rank audit](separable-lowrank-minlp-prior.md).
- If all variables are continuous, rank-one interactions with convex
  quadratic separable costs admit a scalar exact reduction: each coordinate
  response is clipped affine with only a constant number of breakpoints.
  This does not cover arbitrary integer ranges or convex quartics.
- Existing indefinite-QP/MIQP results give global approximation
  algorithms, usually with work polynomial in $1/u$ and with the integer
  dimension fixed. They do not state this candidate’s exact result for
  arbitrarily many integer variables. See the [low-inertia QP audit](convex-recourse-prior.md).

## Closest smoothed discrete-optimization results

**A close structural match after projection: smoothed Pareto sets.** Let $q$
clear all denominators in $T$, define

\[
 Y=\{qTx:x\text{ is feasible}\}\subseteq D^r,
 \qquad
 h(y)=\min_{x:qTx=y}\left\{\sum_iG_i(x_i)-\frac\alpha2\|Tx\|^2\right\},
\]

for a finite integer set $D$ containing the projected coordinate values. Then
the perturbed optimum has value

\[
 \min_{y\in Y}\left\{h(y)+(d/q)^Ty\right\}.
\]

For a fixed draw, any minimizing $y$ is Pareto-optimal for maximizing the
random linear criterion $p(y)=-(d/q)^Ty$ and minimizing the arbitrary fixed
criterion $h(y)$. This brings the proposal close to Beier, Röglin, Rösner,
and Vöcking, [“The smoothed number of Pareto-optimal solutions in bicriteria
integer optimization”](https://doi.org/10.1007/s10107-022-01885-6),
*Mathematical Programming* 200 (2023), 319–355. Their Theorem 1 allows an
arbitrary finite set $Y\subseteq D^r$, an arbitrary deterministic weight
function $h$, and independent continuously distributed coefficients in the
random linear criterion. It bounds the expected number of Pareto-optimal
solutions by

\[
4\Delta |D|\Bigl(\sum_{j=1}^r\phi_j\Bigr)
              \Bigl(\sum_{j=1}^r\mu_j\Bigr)+|D|r+1,
\]

where $\Delta=\max_{a,b\in D}|a-b|$, $\phi_j$ bounds the density of the
$j$th random coefficient, and $\mu_j$ is its expected absolute value.
Thus, in factor coordinates the independent-noise model and arbitrary base
value function are already present in the smoothed Pareto literature. This
is a meaningful anti-concentration/output-size precedent, not an exact
MINLP solver theorem: its bound is pseudo-polynomial in the numeric range
and domain size, it does not give an algorithm for the implicit projected
set and value function produced by $T$ and the $G_i$, and it does not recover
an optimizer in the original coordinates. The paper assumes continuous
coefficient densities; the proposed finite grid has atoms, so its bound
does not directly control the finite-grid sample.

**Winner isolation and pseudopolynomial equivalences.** Beier and Vöcking’s
STOC 2004 paper, [“Typical Properties of Winners and Losers in Discrete
Optimization”](https://doi.org/10.1145/1007352.1007409), proves winner-gap
bounds for finite binary optimization under independent random coefficients
of a linear objective. Adaptive rounding then recovers the exact discrete
winner when coupled with a suitable pseudopolynomial algorithm. Röglin and
Vöcking extend the framework to integer programs in [“Smoothed Analysis of
Integer Programming”](https://doi.org/10.1007/s10107-006-0055-7), with
independent additive perturbations to selected input numbers. Their Theorem
1 characterizes polynomial smoothed complexity by a unary/pseudopolynomial
algorithm for classes whose variable domains have polynomial cardinality.
The formal smoothed-complexity guarantee is a high-probability tail bound;
their paper notes that expected polynomial time needs a stronger
pseudolinear algorithm and a suitable machine model. The objective-noise
case perturbs independent coefficients in the decision vector. Their
extension to arbitrary nonlinear adversarial objectives applies when
constraints, rather than objective coefficients, are randomized. These
results provide the closest general precedent for isolation followed by
rounding and exact discrete recovery, but do not directly cover a single
rank-$r$ correlated noise vector in the original $x$ coordinates or the
candidate’s direct expected rational bit-work.

There is a useful qualification to the correlation distinction. After
projection to $y=qTx$, the candidate’s noise coordinates are independent,
and the Pareto theorem above applies to the abstract finite set $Y$ under
continuous noise. The generic integer-programming equivalence is not
automatically a solver reduction: the projected set and its nonlinear
recourse value are implicit, the range $D$ can be exponentially large in
the binary input length, and the candidate’s finite rational distribution
is not the continuous perturbation model used by the winner-gap theorems.

**Low-rank expected global optimization.** Kelner and Nikolova’s FOCS 2007
paper, [“On the Hardness and Smoothed Complexity of Quasi-Concave
Minimization”](https://doi.org/10.1109/focs.2007.4389517), already gives
expected-time polynomial optimization for constant-rank quasi-concave
objectives over integral polytopes under a random rotation of the objective
subspace. Its projected-shadow algorithm rules out a broad claim that
expected polynomial-time global optimization under low-dimensional
randomness is new. The perturbation is a rotated subspace, and the objective
is low-rank quasi-concave; it is not the independent additive factor-space
tilt of a separable-convex-minus-concave-quadratic MINLP. Its theorem does
not state the finite-grid exact rational Turing guarantee considered here.
The existing [smoothed exact QP audit](smoothed-exact-qp-prior.md) compares
this source with the spatial branch-and-bound and low-inertia approximation
literature.

## What remains a distinct algorithmic question

The Pareto-set result gives the strongest overlap found for the projected
random objective: it bounds, in expectation, a superset of the possible
projected winners for arbitrary deterministic base costs. It does not
construct those winners. The target’s algorithm uses the product-box
structure to evaluate its Fenchel value function through independent
univariate integer minimizations, then searches a low-dimensional
semiconcave function. Its direct expected-cell bound depends on the
curvature, projected box widths, and noise density rather than on the
integer values’ encoding range. The proposed finite-grid choice further
uses an objective-value lattice: a terminal cell certificate smaller than
the lattice spacing proves exactness for that draw, while a discrete-noise
atom term keeps the expected number of visited cells controlled.

The closest prior pattern is therefore not an absence of smoothing theory.
It is a combination of known pieces—random scalarization/Pareto
anti-concentration, low-dimensional global optimization, and exact
discrete winner isolation—with a specialized separable recourse oracle and
a tie-safe finite rational perturbation. Any novelty statement should be
restricted to the proved algorithmic combination and its dependence on
rank, width-to-noise ratio, input bits, and grid precision. It should not
claim new low-rank binary tractability, a new general smoothed winner-gap
principle, or a generic exact consequence of low-rank perturbations.

## Source status

The primary publisher text for the Beier–Röglin–Rösner–Vöcking Pareto paper
was read at the DOI-linked page. The readable B&V conference source and the
Röglin–Vöcking author-hosted IPCO paper were also checked against their
primary texts; the latter’s published journal version is Math. Programming
110(1):21–56 (2007), DOI 10.1007/s10107-006-0055-7. The Pareto paper and
Röglin–Vöcking source were routed to the sole literature ingestion agent
because they were not present as readable local packages at audit time. No
literature index or package was modified here.
