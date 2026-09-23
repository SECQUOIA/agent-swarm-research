# Stage 5, round 1: independent review 5

Verdict: mathematically pass, with one minor caption clarification. No major
issue found. The stronger lower constant, upper bound, integer variant, and
one-objective proposition are justified by the supplied proofs.

## Finding requiring a minor correction

- `sections/07-approximation.tex:160`: replace “inside the unit square bounds”
  by “inside $[-1,1]^2$” or “with $|x|,|y|\leq1$.” The conventional unit
  square is $[0,1]^2$ (and has side length one), whereas the figure and the
  planar section use $[-1,1]^2$. The displayed curves and mathematics are
  correct; this is a precision issue in the caption only.

## Mathematical assessment

Read the full approximation section and checked its dependencies on the
accepted good cone, closed hull, and exact ray descriptions.

The Hausdorff objective properly allows arbitrary nonzero good multipliers,
rescaling, interior multipliers, and unbounded relaxations. Its use of an
infimum does not assume an optimizer. The explicit epsilon-to-cut count
statements instead use the actual mesh construction, and their ceiling and
strict numerical upper-count inequality are correct.

For the upper bound, endpoint cuts give the product of unit balls. The slack
matrix operator bound 5/2, derivative bound 10, and nearest-grid-point Taylor
argument give defect 5 Delta^2/4. The correction B(sx) = s^2 B(x) +
(1-s^2) B(0) has the right sign; B(0) >= I/2 and s = (1+2a)^(-1/2)
make every nonnegative-direction test nonnegative. It is not necessary for
B(x) itself to be PSD. The Euclidean displacement bound supplies the stated
5 sqrt(2)/4 constant, including the coarse N=2 case.

The integer mesh has precisely 2m+1 distinct multipliers; only the central
one is shared. It preserves the rank-one identity exactly and includes both
coordinate endpoints. The angle gaps and the loose but valid binary-digit
bound follow as claimed. No full-dimensional encoding or solver-precision
claim is inferred from the three multiplier entries.

The lower proof works for all good cuts, not just extreme rays. For positive
diagonal weights, dividing by their geometric mean and bounding lambda3 on
both sides yields the stated exclusion inequality. Zero diagonal weights
cannot exclude any witness. Two exclusions yield the AM–GM estimate
(tau-sigma)^2 < 16((1+10 eta)^2-1). With eta = 1/(400N^2), the right-hand
side is exactly 4/(5N^2)+1/(100N^4), strictly below 1/N^2 even for N=1.
Thus the finite pigeonhole argument has the required cardinality and strictness.
The Gram matrices remain positive definite and realizable already in r=2.
The violated rank-one aggregate has operator norm at most 5/2 and gradient
norm at most 5 sqrt(2) on the entire relevant convex product of balls.
The resulting distance lower bound is exactly sqrt(2)/(2000N^2), independent
of r. Neither extremality nor a parameter-range restriction on the competing
cut was inserted. The comparison to arbitrary quadratic descriptions remains
qualitative, as it should.

The Hausdorff/support identity is proved with the correct orientation for an
outer approximation. Bounded P_F is compact and convex, since its inequalities
are closed convex sublevels. The nearest-point projection supplies the reverse
support-gap bound, and equality of the sets is separately harmless.

The one-objective epigraph argument is sound despite possible nonclosedness.
Its order-convexity follows from convexity of every aggregate in the closed
cone. Adding the positive orthant and the upward objective ray gives nonempty
interior. The attained point (0,v) is a boundary point, and a convex set with
nonempty interior has the same interior as its closure, justifying support
there. Recession directions force the correct dual signs. Strict negativity
of all nonzero good aggregates at the origin rules out a zero objective
multiplier; the nonzero linear objective rules out a zero aggregation after
normalization. Complementarity at the compact-hull minimizer gives both
global lower-bounding and common attainment. The text correctly says that
the origin is strict for the convex-hull description, not the original rows.

## Literature, figure, and coverage

Read the dedicated author/literature reports, snapshot, associated bibliography
entries, stage-5 coverage, both scripts, and supplement README. The stronger
finite-grid bound supersedes the older logarithmic proof without promoting
the stronger constant to an unverified formal claim. All stage-5 source
developments have manuscript destinations; later formal integration is bounded.

Read the local primary Bronshteyn–Ivanov theorem and its approximation setting.
Independently opened Rote's
[author abstract and bibliography](https://page.mi.fu-berlin.de/rote/Papers/abstract/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.html):
these support the stated tangent/chord, planar-figure, and optimal N^-2 context.
The manuscript distinguishes that classical exponent and conic duality from
the specific prescribed-good-cut bound. I did not conduct a new exhaustive
priority search or independently recheck every primary source in the author's
literature report; no broader novelty conclusion is inferred here.

Inspected the PNG figure visually and derived its exact and finite-mesh polar
radius formulas. The curves, nesting, coordinate signs, legend, and enlarged
panel agree with those formulas. The caption correctly distinguishes a planar
illustration from the full-dimensional Hausdorff bound, apart from the minor
square terminology above. Plot generation is optional for the LaTeX build.

## Targeted checks actually run

- `python3 paper-quadratic-aggregation/supplement/check_approximation.py`:
  PASS for 64 rational meshes, 606 exact Gram witnesses, and radial identities.
- Independent standard-library Fraction heredoc: checked the grid-separation
  constant for every N from 1 through 100 and representative boundary,
  interior, and coordinate good cuts against the complete corresponding grid.
  Each cut excludes at most one witness; all checks passed. These finite
  checks supplement the universal proof read above.
- Loaded plotting functions with `runpy.run_path` without invoking `main` or
  rewriting figures. On 12,001 independent polar directions, checked the exact
  quartic residual and outer containment for N=2,3,5,9: all passed.
- SHA-256 compared all 20 author-snapshot entries: no mismatches.
- Inspected saved dedicated LaTeX and BibTeX logs: 30 pages; no Warning,
  Overfull, Underfull, or undefined matches. Did not rerun LaTeX.

No manuscript source or figure was edited, no other stage-5 review was read,
and no review coordination, subagent, global check, CI inspection, or Lean
rerun was used.
