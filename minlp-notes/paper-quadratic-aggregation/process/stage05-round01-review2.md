# Stage 5, round 1, independent review 2

Verdict: **pass; no major or minor correction requested**.

I independently reviewed the entire approximation section, its dependencies
in the accepted hull description, the two new scripts and figure, author
report and snapshot, literature record, bibliography additions, and supplement
instructions. I did not read other current reviewers' reports or coordinate
findings with them. The only repository file I authored is this report.

## Stronger lower bound

The finite-grid argument proves the displayed constant
`sqrt(2)/2000`, including arbitrary interior good multipliers.

- For every integer `N>=1`, `eta=1/(400 N^2)` is positive and below `1/10`.
  The two Gram diagonals are at least `4/5` and the off-diagonal magnitude
  is at most `2/5`; the determinant lower bound `12/25` therefore holds.
  The witnesses exist already in dimension two and embed without changing
  any estimate in larger replication dimensions.
- If a nonzero good multiplier has a zero first or second coordinate,
  its third coordinate vanishes and it excludes none of the witnesses.
  In all other cases, an excluded witness satisfies
  `lambda1/tau + lambda2*tau < (1+10 eta) lambda3`.
  Using `lambda3 <= 2 sqrt(lambda1 lambda2)` gives the claimed condition
  on `t=sqrt(lambda1/lambda2)`, without requiring the multiplier to be an
  extreme ray or requiring `t` to lie in `[1,2]`.
- If one cut excluded two grid parameters, adding these inequalities and
  applying AM–GM gives
  `(tau-sigma)^2 < 4 tau sigma ((1+10 eta)^2-1)`.
  Since both parameters are in `[1,2]`, this is at most
  `16((1+10 eta)^2-1) = 4/(5N^2)+1/(100N^4) < 1/N^2`.
  It contradicts their spacing. The strict inequality is justified because
  exclusion from a nonstrict cut means a strictly positive aggregate.
  Thus the pigeonhole conclusion applies to every family of at most `N`
  cuts, including rescaled, interior, coordinate, or redundant multipliers.
- The omitted witness violates its own rank-one good aggregate by `2 eta`.
  That aggregate's matrix norm is `tau+1/tau <= 5/2`. On the convex product
  of the two unit balls its gradient norm is at most `5 sqrt(2)`, uniformly
  in replication dimension. Both the witness and every hull point belong
  to that product. The mean-value bound therefore gives distance at least
  `2 eta/(5 sqrt(2)) = sqrt(2)/(2000 N^2)`.
- Taking the infimum over all families preserves this lower bound. An
  unbounded relaxation has infinite error and causes no exception. No
  existence of a best family is assumed.

## Upper bound and integer mesh

The angle family generates the good cone, with coordinate rays at both
endpoints. The equivalence tests only nonnegative directions; it does not
replace copositivity on that sector by PSD of the slack matrix.

The endpoint cuts bound both vector norms by one. The row-sum bound gives
operator norm at most `5/2`, and differentiating the angle quadratic twice
gives the bound `10`. At an interior minimizer, a mesh point lies within
half the maximal gap and the first derivative vanishes. Taylor's upper
bound at that mesh point gives the global defect `5 Delta^2/4` with the
correct sign. Endpoint minima are already nonnegative.

The radial identity is exact. Since the origin's slack matrix is at least
`I/2`, the prescribed scaling repairs every direction simultaneously.
The convex tangent estimate for `(1+2a)^(-1/2)` then gives distance at
most `sqrt(2) a`. Thus the equal-angle constant and its denominator
`(N-1)^2` follow, also for `N=2`.

The integer lists have exactly `2m+1` distinct rays, including both
coordinate rays and one common middle ray. Their angles have gaps at most
`1/m`, and their rank-one good-cone identity is exact. The coefficient
range and conservative binary digit bound are valid. The explicit
epsilon-to-cut-count consequence uses this actual construction and
does not incorrectly invert an unattained infimum.

## Objective statements

For bounded `P_F`, both relevant sets are compact convex and nested. The
nearest-point proof correctly establishes equality between the Hausdorff
distance and the supremum of unit-objective support gaps.

The one-objective proposition is also complete. Convexity of all good
aggregates gives the required cone-convexity of the vector map and convexity
of its upward epigraph. That epigraph has nonempty interior. Its point
`(0,v)` is included and is on the boundary; supporting its closure is valid
because a full-dimensional convex set and its closure have the same
interior. Recession directions force the multiplier signs and membership
in the closed good cone. Strict negativity of every nonzero good aggregate
at the origin excludes a zero objective multiplier. After normalization,
evaluation at an attained hull minimizer gives complementarity and common
attainment for the single aggregate. A nonzero objective excludes the zero
aggregation. The proof does not mistake the origin for a strict point of
the original three-row system.

The text correctly distinguishes a uniform representation lower bound from
an iteration or computational bound for one objective. The one-objective
claim is explicitly classical conic duality, not a new principle.

## Literature, figure, and checks actually performed

- Opened Rote's [author-hosted abstract](https://page.mi.fu-berlin.de/rote/Papers/abstract/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.html)
  and linked primary report PDF. The abstract confirms the optimal
  quadratic rate, tangent/chord approximants, and planar comparison.
  The manuscript credits this close antecedent without claiming a new
  general exponent or assigning report theorem numbers to the journal.
- Opened [Arya–da Fonseca–Mount v2](https://arxiv.org/html/2306.15648v2)
  and read its introduction and main theorem statements. The manuscript's
  dimension-dependent polytope/function approximation context is accurate
  and is distinguished from prescribed good quadratic cuts. The local
  Bronshteyn–Ivanov source is used for context, not as an unproved premise
  of the new rate proof.
- Opened the coauthor-hosted Boyd–Vandenberghe book and confirmed its
  edition metadata and generalized-inequality section locator. Independently
  checked the manuscript's self-contained separation proof instead of
  treating the book citation as a substitute for that argument.
- Read both new Python scripts. Ran
  `python3 paper-quadratic-aggregation/supplement/check_approximation.py`:
  passed, reporting 64 rational meshes, 606 exact Gram witnesses, and
  radial identities. The script's finite scope is clearly stated.
- Imported the plotting script's definitions using `runpy` without calling
  its output-writing `main`. Checked the exact radial quartic equation,
  containment, and nesting of the `N=3,5,9` approximants at 8,001 directions:
  passed. No figure files were changed. Algebraically, rationalization
  selects the smaller quartic radial root, including coordinate axes;
  the mesh radial formula follows directly from its quadratic cuts.
- Visually inspected the included PNG figure. Curves, labels, legend and
  enlargement are legible; the caption accurately limits it to planar
  sections rather than computed full-dimensional Hausdorff errors.
- Compared snapshot hashes for the approximation section, wrappers/macros,
  bibliography, both scripts, and supplement README: all match. Scanned
  the dedicated stage 5 final LaTeX and BibTeX logs for warnings, undefined
  references, and overfull/underfull boxes: no matches.
- No new build, formal rerun, project-wide verification, CI inspection,
  solver experiment, or subagent was used.

No formal certification of the stronger constant is inferred from this
review. The pending formal integration and later mathematical stages remain
outside this stage 5 acceptance.
