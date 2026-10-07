# Corrections to the archived research reports

The archive preserves original files and experimental source bytes. The
manuscript supplies revised statements and proofs. The following corrections
apply when reading the older mathematical reports; they do not change the
archived experimental outcomes or the frozen numerical policy.

1. **Boundary contraction.** September Proposition 11's refined active-width
   estimate needs a separate treatment when the initial enclosing scale is
   already below the cutoff floor. Its geometric free-coordinate enclosure is
   a rate bound in a prescribed enclosing scale, rather than a proved
   contraction of each successive actual free-coordinate width. The manuscript
   uses a repaired statement and proof and gives an explicit analytic
   counterexample to the unrestricted estimate.
2. **Two-variable rate.** The exact multiplicative rate holds on the symmetric
   eigenvector boxes. For arbitrary boxes containing an interior neighborhood
   of the optimizer, the proved statement is a two-sided geometric bound and
   its kth-root rate; convergence of successive width ratios is not established.
3. **Residual after an exact round.** Suppose the first exact displacement is
   `d`, an upper bound is `r >= d`, and the checked nonnegative matrix inequality
   is `r + M e <= e`. After the completed exact first round, remaining movement
   is bounded by `M e <= e - r`. The older prohibition on subtracting an upper
   residual is incorrect under this stronger premise. This bound does not
   transfer to a partially updated or unrelated numerical state.
4. **Lifted attainment.** Compact projected sublevel sets do not by themselves
   ensure that a lifted objective infimum is attained. Identifying a projected
   objective sublevel with the projection of a lifted cutoff set needs that
   premise. The bounded rational reference relaxation has it. Projected
   monotonicity suffices for objective-value ceilings; literal retention of the
   same auxiliary coordinates additionally needs lifted nesting.
5. **Cutoff thresholds.** Keeping every witness at a cutoff is stronger than
   retaining sufficient witnesses to cover every face. The manuscript gives
   the exact retained-pool face threshold and the full-relaxation threshold
   for a prescribed candidate box. These refine the older sufficient rule.
6. **Complete basis coverage.** A basis region proves a support formula where
   its rows remain feasible. A collection must separately cover the entire
   invariant parameter region. The manuscript gives finite strict-violation
   tests for this obligation. The archived checker does not automatically
   discover or certify arbitrary complete covers.
7. **Nonlinear graph example.** The older repair constant and `15/16` rate
   remain valid. The manuscript uses the sharper one-sided repair constant
   `L=1/2048` and proves the rate bound `1/3` at width at most `1/8`.
8. **Cost accounting.** The work-ledger admission proof assumes serial
   completed operations, or reservations that cover outstanding work. A bound
   on enhancement cost along the modified run does not bound its native search
   work relative to an independent baseline.
9. **Monotonicity of moving tangent rows.** A deterministic relaxation
   construction that depends only on the box need not be monotone under box
   restriction. The five box-relative square tangents used by the numerical
   studies give a counterexample even when no cached tangent pool is retained.
   Their individual rows remain valid underestimators. The manuscript's
   iteration rates and future-round certificates require a separately checked
   monotone family; the numerical policies implement current-round bounds and
   screening instead.
10. **Fixedness of a limit.** Nested nonempty compact iterates alone do not
   prove that their limit is a fixed box. The manuscript states a closedness
   condition along decreasing box sequences and proves the identification
   with the greatest fixed box under that additional premise.

September's reported solve-count and trajectory corrections also apply:
SCIP control/r5 solve counts are 573/563 and first-round tightening occurs on
239 of 339 known-cutoff trajectories. The old tables retain the earlier
success rule; their time and node summaries were not recomputed for this paper.
Among the 104 known-cutoff histories with one recorded round, 97 have a
completed unchanged round, 3 a capped unchanged round, and 4 a capped productive
round. Thus the 100 unchanged rounds and 7 capped rounds overlap. A further 22
histories have a productive first round followed by a completed unchanged
second round; one additional unchanged second round was capped. These are
numerical stopping observations, not exact fixed-point certificates.
The companion README and manuscript evidence audits give the exact scope.

These errata are analytic and archival corrections. Preparing the manuscript
and companion did not rerun the experiments.
