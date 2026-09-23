# Stage 5, round 1: independent review 1

Verdict: accept stage 5. No major or minor issue identified. The new
finite-grid argument proves the stated stronger lower constant, the upper
and rational-mesh bounds include their stated endpoints, and the
one-objective proposition has a complete conic separation proof.

## Major findings

None.

## Minor findings

None.

## Independent proof assessment

### Definition, quantifiers, and angular upper bound

Every P_F contains the nonempty compact D_r, so the extended Hausdorff
formula is correct, including an empty family and unbounded relaxations.
The infimum over families is never treated as attained. The approximation
theorem is restricted to good multipliers, including their interiors and
arbitrary positive scalings.

The identity h_x(theta)=-f_lambda(theta)(x) and the relation tau=cot(theta)
are correct. Testing only nonnegative directions characterizes the hull;
the text correctly avoids asserting PSD of B(x). Coordinate endpoints
bound both vector norms. The row-sum estimate 5/2 and the derivative
estimate 10 follow, and Taylor expansion at an interior global minimizer
has the required direction: the nearby mesh value is at most the minimum
plus 5 times the squared angular distance. This gives defect 5 Delta²/4.
Endpoint minimizers need no Taylor argument.

The radial matrix identity is exact. Choosing s²=1/(1+2a) cancels the
worst negative defect against B(0)>=I/2, so every relaxed point moves into
D_r. The norm bound sqrt(2) and convex tangent inequality yield the
claimed Hausdorff bound. This works without small-mesh assumptions, hence
also for N=2. Equally spaced meshes give the precise upper constant.

For the integer mesh, the two lists have exactly one common ray, their
extreme-ray identity is exact, and reflection of arctan(j/m) supplies both
endpoints with gaps at most 1/m. This applies at N=3 and N=4, where m=1.
The entrywise bit bound follows from the stated integer magnitude bound;
it is appropriately distinguished from full formulation size. Necessary
and sufficient epsilon cut counts use actual constructions and the lower
bound, not an assumed optimal family.

### New finite-grid lower bound and N=1 boundary

With eta=1/(400N²), every proposed Gram matrix is positive definite, has
both vector norms at most one, and realizes the stated residual vector.
This is valid already in r=2 and embeds in every higher replication
dimension.

For a multiplier with a zero diagonal coordinate, goodness forces its
cross coefficient to vanish and the nonzero cut is strictly satisfied.
Otherwise, dividing an exclusion inequality by epsilon*sqrt(lambda1*
lambda2), while using lambda3<=2sqrt(lambda1*lambda2), gives
t/tau+tau/t<2a with a=1+10eta. This derivation does not require an extreme
ray, positive lambda3, or a bounded range for t. Applying it to two
excluded grid points, adding, and using AM–GM gives
(tau-sigma)²<4tau*sigma(a²-1)<=16(a²-1).

Independently recalculated the final constant:

    16(a²-1) = 4/(5N²) + 1/(100N⁴) < 1/N².

The strict final inequality holds for every N>=1, including N=1, where
the coefficient is 81/100. Thus a cut excludes at most one grid point;
N cuts leave one of the N+1 witnesses feasible. Zero residual on a cut
counts as satisfaction of its nonstrict inequality, as required.

At the surviving witness, the omitted ray has residual 2eta. Its leading
operator norm is tau+1/tau<=5/2. The gradient therefore has norm at most
5sqrt(2) on the convex product of the unit balls. That product contains
the witness, D_r, and the connecting segments. The mean-value inequality
gives distance at least 2eta/(5sqrt(2))=sqrt(2)/(2000N²). This proves the
stronger constant as stated. Unbounded P_F only makes the extended
Hausdorff bound immediate. The proof does not claim formal certification
of the stronger manuscript constant.

### Support gaps and one-objective exactness

When P_F is bounded it is closed, convex, and nonempty. The nearest-point
projection proof gives exactly the support-function/Hausdorff identity.
Its interpretation concerns the worst unit objective for one common
relaxation, including a family obtained adaptively; it gives no iteration
lower bound for a prescribed objective.

The order-convexity calculation for F uses the correct dual-cone sign,
and it makes the upper epigraph E convex. Fixed x with positive orthant
slack and t>0 supplies a full-dimensional interior. The minimizer gives
(0,v) in E; no point (0,v-delta) can belong to E. The use of a supporting
hyperplane at this included boundary point is justified despite possible
nonclosedness, since a full-dimensional convex set and its closure have
the same interior.

The slack recession directions force lambda in K_r and mu>=0. Strict
negativity of every nonzero good aggregate at the origin rules out
mu=0. After normalizing mu=1, the global Lagrangian lower bound, together
with feasibility of x_*, gives complementarity f_lambda(x_*)=0. A zero
lambda would bound a nonzero linear objective below on all of Euclidean
space and is impossible. Every point satisfying the single aggregated
inequality has objective at least v, while x_* attains it. This proves
both minima and common attainment, with precisely the claimed scope.

## Figure, software, and literature

Read both scripts and independently derived the plotted planar formulas.
Rationalizing the smaller root of a*rho⁴-rho²+3/4=0 gives the exact
squared radius; the angular-cut denominator and numerator are correct.
The plotted N=3,5,9 meshes are nested. Viewed the PNG preview: labels,
legend, zoom rectangle, and outer-boundary ordering are legible and agree
with the mathematics. The caption correctly identifies a planar
illustration rather than a full-dimensional Hausdorff computation.

The exact checker uses rational arithmetic and accurately limits its
claimed coverage. Its witness checks supplement the universal argument;
they are not presented as proof of the pigeonhole or Hausdorff theorem.
The plotting dependencies are separate from the supplied PDF's LaTeX
build dependency.

Read the primary local Bronshteyn–Ivanov extraction and independently
opened Rote's author-hosted report, checking its abstract, Theorem 1 and
the rate corollaries. The manuscript accurately distinguishes the older
one-dimensional tangent/chord rate from this prescribed family of
quadratic cuts. The report/journal version distinction is preserved:
https://page.mi.fu-berlin.de/rote/Papers/pdf/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.pdf .

Independently checked the Arya–da Fonseca–Mount primary v2 introduction
and Theorem 1's facet-approximation setting, and Boyd–Vandenberghe's
Section 5.9.1 dual-cone signs and generalized Slater discussion. These
support the limited contextual/duality attributions:
https://arxiv.org/html/2306.15648v2 and
https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf .

The new contribution is scoped to a two-sided, dimension-uniform
good-cut bound for the specific example. No unsupported first-exponent,
general-duality, solver-performance, arbitrary-quadratic-rate, or optimal-
constant claim is made. This reviewer did not repeat an exhaustive
priority search and does not infer novelty from search absence.

## Actual targeted checks

- Read section 07 completely, prior accepted cone/hull dependencies,
  relevant main/macros/bibliography changes, both new scripts, supplement
  README, author/literature records, snapshot and coverage integration.
- Ran `python3 paper-quadratic-aggregation/supplement/check_approximation.py`:
  **PASS** (64 meshes, 606 rational witnesses, radial identities).
- Independently checked the grid constants and Gram bounds with exact
  fractions for N=1 and N=2: **PASS**.
- Loaded the plotting functions with `runpy.run_path` without invoking
  their output-writing main function. Checked exact-boundary residuals
  numerically and nested outer containment at 8,001 angles: **PASS**.
  No supplied figure was rewritten.
- Compared all 20 author-snapshot SHA-256 entries: all match.
- Searched final `build/stage05/main.log` and `.blg` for warnings,
  undefined references and overfull/underfull boxes: no matches. No
  redundant LaTeX build was needed.
- Primary-source reads described above; no CI, project-wide checks,
  Lean reruns, other current reviewer-report reads, or reviewer coordination.

This report is the only authored repository file in this review turn.
