# Five equal cells and three modes: exact two-switch worst case

Date: 2026-09-07. Status: finite integer proof, independent mathematical and implementation review, and independent source-scope audit passed.

**Theorem.** For three modes on five equal grid cells of length `Delta>0`, the worst-case cumulative CIA error with at most two grid-boundary switches is exactly `Delta`. Initial activation is free. Arbitrary measurable relaxed controls are included because cell averages determine every grid schedule's full error.

This supplies a counterexample to Sager and Zeile's published Corollary 5, which asserts a lower bound `8 Delta/7` for these admissible parameters. The contradiction concerns that lower-bound statement as written, separately from the previously disproved multi-mode conjecture.

## Exact proof

Normalize `Delta=1`. For profiles with every component's cumulative allocation nonintegral at the five endpoints, a grid word has error below one exactly when all its prefix occupation counts are the corresponding floors or ceilings. A cumulative-floor history is realizable precisely when each bounded prefix coordinate attains both adjacent integers among its feasible integer words. Necessity follows from the standard integral-prefix-flow polytope; sufficiency follows by averaging its integer words.

An exhaustive integer-only enumeration finds 396 realizable strict floor histories. Every one admits a word with at most two switches. An independently written flat enumeration checks all 14,400 candidate floor histories and obtains the same result. Counts of histories with minimum switch counts zero, one, and two are respectively 3, 138, and 255. The proof depends on exhaustive coverage and exact feasibility criteria, not merely agreement of these counts.

Boundary profiles follow by perturbation toward constant rates `(1/7,2/7,4/7)` and continuity of the minimum over the finite schedule set. This gives error at most one for every profile. For the lower bound take the pure relaxed word `(0,1,0,1,0)`. Error below one would force identical integer prefix counts and therefore all four original switches. Thus a two-switch schedule must incur error at least one. Scaling proves the theorem.

The [full proof](../notes/cia-reopened-small-grid-boundary.md), [independent review](../notes/review-cia-reopened-small-grid.md), [author enumeration](../code/cia_reopened/small_grid_boundary.py), and [independent enumeration](../code/cia_reopened/check_small_grid_review.py) preserve all details. This is a computer-assisted proof, not a numerical minimax estimate.

## Source comparison

The [final published article](https://link.springer.com/content/pdf/10.1007/s10589-020-00244-5.pdf), printed p.611, states Corollary 5 for `n_omega>2` and `1<=sigma_max<=N-2` without a congruence restriction on `N`. Its expression `(N+sigma_max+1)/(3+2 sigma_max) Delta` evaluates to `8 Delta/7` at `(n_omega,N,sigma_max)=(3,5,2)`. The preceding attainment argument, p.610, only covers particular grid lengths. Fixing horizon `[0,5]`, five cells, and maximum width one forces the equal grid, so allowing a variable grid does not remove this counterexample.

The [independent literature audit](../notes/cia-reopened-literature.md) checked the final source and found no later correction in the targeted open search. This is not an exhaustive priority claim or a replacement lower formula for the source's full parameter range.
