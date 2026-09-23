# Reviewer 4 — independent whole-manuscript review, full-round01

**Verdict: PASS WITH ONE MINOR CORRECTION. No major issue found.**

I reviewed the complete frozen 28-page manuscript, including the proofs,
appendices, source comparison, bibliography, coverage map, and reproducibility
instructions. All 22 manifest hashes match. I did not read another reviewer's
full-round report or edit the manuscript. This is a whole-paper assessment,
not reliance on the earlier stage verdicts.

## Required minor correction

**Make the connected principal-window transfer explicit for the empty
arithmetic source.** In `sections/04-structural.tex:196–199`, the empty source
produces one isolated fixed-voltage bus. Corollary 5.5 then says to apply the
corresponding AC transfer and states that it changes no graph
(`sections/04-structural.tex:257–259`). However, the referenced principal-window
corollary requires `n >= 2` (`sections/03-ac.tex:321`), and its stated padding
rule adds isolated buses (`:337–339`). Applying that rule to the one-bus output
would break the connectedness asserted by Corollary 5.5.

This is a boundary-case composition omission, not a counterexample to the
hardness statement. For every nonempty arithmetic source, the connector adds
at least one bus, so the final connected network already has at least two
buses. Fix the proof by saying this explicitly and handling the empty source
with a connected two-bus network having unit conductance, both voltages fixed
to 1, and zero active/reactive injections. It is a singleton feasible set and
meets all graph restrictions, with cosine `c_2 = 3/4`. Alternatively, add a
uniquely fixed dummy arithmetic variable before this transfer when necessary.
Either correction removes the need for isolated padding in the structural
corollary. The real-angle and reference-fixed box transfers need no change.

## Substantive assessment

The proof sequence is coherent and sufficient for the stated scope. In
particular:

- The source and RPF models make the independent singleton bounds explicit.
  Copy allocation retains unused variables, separates repeated occurrences,
  and gives the stated sizes and degree. The inversion identities, positive
  division, voltage range, and redundant free-injection bound establish both
  directions and a unique rational extension.
- The AC formulation has consistent complex-power signs. The determinant
  crossing rule handles both orientations, axes, unequal magnitudes, and
  obtuse short arcs; the fundamental-cycle equations supply exactly the real
  lift. The equal-angle energy proof requires that lift. The rational
  counterexamples and shrinking-window transfer respect that distinction.
  One-sided reactive intervals force zero by total reactive cancellation.
  Reference-fixed boxes give unique rectangular voltages componentwise.
- The bounded crossover preserves complete solution sets. The occurrence-aware
  planar realization handles repeated names and the inversion's two adjacent
  strands. The connector remains redundant throughout the box; harmonic even
  subdivision gives unique affine extension and the simultaneous unit,
  bipartite, degree, girth, and planarity restrictions. The minor case above
  is the sole composition issue I found.
- The revised universality proof uses conjunctions throughout. Compactness
  justifies scaling and denominator guards; all appendix identities give
  converse recovery as well as forward extension. The basic-closedness
  invariant and three-quadrant obstruction prove the sharp rational scope.
  Finite simplex nonface equations support the separate topological claim.
  Empty sets, the point of R^0, and rational singleton fields cause no
  difficulty in these arguments. The designated coordinate, rather than only
  the collective coordinate field, generates the requested algebraic field.
- The residual constants follow from the actual gadget equations. The explicit
  infeasible family includes `k=0`, has a valid rational profile with just one
  injection violation, and proves a residual scale rather than an algorithmic
  time lower bound. The JPT epigraph satisfies compactness, connectedness,
  integer-coefficient, and degree hypotheses; its specialization and
  fixed-data comparison are correct. The promise verifier remains sound with
  singleton voltage bounds, zero weighted degree, and empty networks. Reactive
  stability has the stated signs and constants; componentwise and isolated-bus
  handling make the final combined estimate valid.

All eight historical examples have the claimed exact outcome and uniqueness
when feasible. The manuscript correctly separates those analytic conclusions
from old solver tolerances and time-limited runs. The introduction and
conclusion match the theorem scopes, including the rational coefficient
qualification, the absence of a fixed positive principal-window hardness
claim, and the distinction between exact and promised approximate decision.
The source/version corrections from stage 4 are present. I found no omitted
in-scope repository or worktree development and no missing scientific
development needed to support the final claims.

## Verification and publication judgment

A fresh forced build succeeds with **28 pages and no LaTeX warnings or layout
diagnostics**. I inspected the complete extracted manuscript and rendered
pages 6, 13, 23, 25, and 27. The diagrams, long arithmetic displays, table, and
appendix transition are clear and unclipped.

All four exact suites pass with the counts printed in the verification
appendix. As a distinct check, I wrote an independent rational interval
implementation of the nested arithmetic gates. It certifies valid ranges and
strictly positive reciprocal denominators over full input intervals using
`delta = 1/1024`, rather than sampling points. This supports the appendix's
uniform continuity choice without imposing an additional quantitative claim
on arbitrary input descriptions. Fresh original-source extracts confirm the
ETR-INV definition and completeness, the JPT bound, and the BM version; the
primary triangulation source supports precisely the homeomorphism used here.
Eight relevant files remain identical across the two actual worktrees.

Evidence is retained under
`paper-power-flow/verification/reviewer4/full-round01/`, notably
`manifest-check.log`, `build.log`, `build/main.log`, `pdfinfo.log`,
`check_*_exact.log`, `check_gate_intervals.py`, `gate-intervals.log`,
`worktree-check.json`, primary-source extracts, and `audit-receipt.md`.

After the small transfer clarification above, I regard the manuscript as a
complete, readable research paper with supported mathematical claims and an
appropriate reproducibility supplement. I found no valid major criticism or
additional required research task. This assessment is an independent review,
not a prediction of a journal's editorial decision or formal proof
certification.
