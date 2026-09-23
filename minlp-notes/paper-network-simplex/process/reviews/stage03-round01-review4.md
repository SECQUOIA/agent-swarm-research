# Stage 3, round 1 — independent reviewer 4

Snapshot: `process/snapshots/stage03-round01`.

## Verdict and enumerated findings

**Accept this stage. No major or minor defects identified.**

1. **R4-S03-01 — No actionable finding.** The explicit descriptions,
   globally valid branch cuts, arithmetic bounds, and compact recovery claims
   are supported by the arguments in the frozen section. The transportation
   proof checks target nonnegativity rather than assuming it.

## Proof and scope audit

I read all of `sections/03-structured-oracles.tex` and checked its notation
against the preceding foundations and compression sections.

- **Theta geometry.** The third path's extra sign gives `(s,t,-s-t)` in
  consistently traversed path deviations and `(s,t,h)` in signed observations.
  The five feasibility inequalities follow from intersection of the rectangle's
  attainable sum interval with the stated sum bounds. Projecting onto `s` and
  `t` gives exactly the tight-support formulas. The Minkowski argument handles
  points and permitted segments separately; it does not incorrectly extend a
  planar edge argument to higher-dimensional facets.
- **Affine expansion and unit coefficients.** Lower endpoints are maxima of
  affine expressions; upper endpoints are minima. Subtracting an upper endpoint
  from a lower endpoint is still a maximum of affine branches. The local
  comparisons use either different coordinate types or a same-type pair of
  observations, in which an identical product cancels. Support branches use
  products from distinct coordinate types. Summing states does not repeat a
  product column because its label is part of its index. Aggregate `h(x)` uses
  two distinct representative arcs. Thus every claimed `x,z` coefficient is
  indeed in `{0,1,-1}` in the stated rational scaling.
- **Global separation.** A violated convex piecewise-affine left side is the
  maximum of a finite family of globally required affine inequalities. An
  active branch has the same violation and is globally valid. In the
  parallel-path formulation, an active affine branch majorizes the concave
  right side, so replacing it by that branch is a valid relaxation with exactly
  the candidate's violation. The inequality directions are correct in both
  arguments. Negative-row and local violations also have the required finite
  branch form.
- **Theta recovery.** Reflection and translation of the suffix Minkowski sum
  produce exactly the displayed interval intersection. The chosen `s` lies in
  the projected feasible interval. The chosen `t` satisfies both its upper
  bound and the sum upper bound, while enforcing the lower bounds. Sequential
  subtraction preserves suffix membership. The final empty suffix forces zero
  remainder. Merged default coordinates are normalized only at positive
  merged weights; zero defaults are unused. Globally zero-weight states need
  no dense flow output.
- **Complexity.** There are at most `|O|` observed block/label pairs. Endpoint
  scanning, a constant number of support calculations per theta state, suffix
  sums, and the recovery steps have the stated linear arithmetic count after
  grouping. The grouping comparison cost is disclosed. Storing one constant-size
  default coordinate vector per cycle/theta block and its observed-label
  exceptions gives compact storage, while the separate dense output bound
  accounts for all state/arc entries. The rational-bit qualifications are
  consistent with these operation counts.
- **Transportation sufficiency.** The lower-endpoint shift gives nonnegative
  capacities and column targets from the local conditions. Complementary subset
  inequalities then give nonnegative row targets; total row and column targets
  agree because aggregate deviations sum to zero. For fixed source-side rows,
  independent column-side choices yield precisely the stated minimum cut.
  Substituting the shift cancels the lower endpoints and gives exactly the
  subset inequality. The `R=0` case is valid: every target is nonnegative and
  all targets sum to zero, hence the zero shifted matrix is feasible.
- **Flow oracle and output.** A deficient cut's row set remains deficient
  after minimizing over column sides. The graph has `k+a+3` nodes and
  `k(a+1)+k+a+1` arcs. Endpoint construction and cut extraction respect the
  displayed size bound; the maximum-flow cost is additional. Choosing a
  polynomial augmenting-path rule and clearing rational denominators gives
  polynomial bit complexity. Arbitrary path augmentation is not used to claim
  polynomial complexity. Storage for the returned state matrices and normalized
  defaults fits the graph-construction bound.
- **Examples and boundaries.** I checked the two separate one-label
  decompositions in the joint-state example and its exact `1/3` violation.
  At `k=3`, singleton and complementary subsets give the six theta supports
  after the third-path sign change. Empty and full subsets are redundant under
  local column feasibility. The section correctly excludes general nested
  series–parallel blocks and makes no new general polynomial-separation claim.

## Source coverage and actual checks

I compared the current stage with
`results/network-simplex-cycle-theta-hull.md` and
`results/network-simplex-parallel-path-hull.md`. Their material scoped
developments are represented: arbitrary orientations, repeated observations,
zero weights, block-local state mergers, unit coefficients, exact projected
cuts, compact decomposition, and the larger-series–parallel boundary. The
proofs are readable without consulting those notes. Historical computational
counts are properly left to the later computational stage.

I wrote the independent exact-integer script
`verification/reviewer4/stage03-round01/check_formulas.py`, importing no
repository implementation. It passed:

- 3,375 theta interval systems, of which 2,487 were nonempty; independently
  enumerated boundary intersections agree with feasibility and all six supports;
- 1,453 exact greedy decompositions of vertices of summed-support polygons,
  including degenerate domains;
- 4,000 bounded transportation candidates compared with explicit enumeration
  of attainable integer column sums, including 1,376 locally feasible systems
  with a negative shifted row target.

Results are saved in `check_formulas.json`. These are finite checks with
integer data, not a substitute for the rational/general proofs.

A private snapshot copy built successfully with `latexmk` in
`verification/reviewer4/stage03-round01/build`. The final build log has no
warning, undefined reference, overfull, or underfull matches.

## Limitations

I did not independently re-audit the bibliography or benchmark the repository
separator implementation in this stage. The exact test instances do not cover
every graph preprocessing configuration; those assertions were checked from
the block/path argument. I read no other current-round reports, edited no
manuscript sources, and spawned no agents.
