# Evidence review — final recheck

Date: 2026-10-05 America/New_York; snapshot at
2026-10-06T01:47:11 UTC. Read all four complete sources and
`author-algorithms.md`; no manuscript or companion edits.

| Source | SHA-256 |
|---|---|
| `sections/algorithms.tex` | `8980d76a4a5af79fcedb2dfe77e5ca75ee4f67bfd4a62bce18060383918d2cff` |
| `sections/effort.tex` | `ca0ba9755fdf4a77c66da96b57c905c97c16ca3cf28a5f4bae9b50b0198dec69` |
| `sections/experiments.tex` | `abe0b42d717253b046e7b59e24031278038086afd213aa5bdde1c252d3845e39` |
| `appendices/precursor-study.tex` | `625d05a78116cd39127adadefdd8b7a6496d47eb11364ced28e9f3ad305b8610` |

**All material round-1 findings in these files are closed.** No unresolved
scientific issue was found in the revised algorithms, effort, experiments,
or precursor appendix. The discussion's separate final-solve wording is
outside this recheck and remains with the root.

The revised sources correctly preserve the following distinctions:

- The 104 one-entry known-cutoff histories partition into 97 completed
  unchanged first rounds and seven interrupted first rounds. The latter contain
  three unchanged and four productive partial rounds. A further 22 productive
  first rounds have a completed unchanged second round; one additional second
  round is interrupted. These are numerical stopping events, not exact fixed
  points. A fresh direct read of the saved flags reconfirmed 104/97/7 and 22/1.
- September solved counts exclude the two wrong-answer rows: SCIP control/r5
  573/563; the OBBT-ran control subset is correctly 441. All affected timing,
  node, and final-solve summaries are explicitly the archived originals. The
  narrow post hoc 600-second replacements have been removed from manuscript
  tables rather than mixed with original summaries.
- The rho statistic, no-change rule, adaptive cap, delayed first-round cap,
  conditioned contraction histogram, group-mean interpretation, and numerical
  reference-containment tolerance are now stated correctly.
- October's identical solved sets, all-run PAR-2 rule, uncapped process costs,
  39 comparable gaps, corrected 39.52/5.23 fixed-arm totals, and descriptive
  shared-machine interpretation remain consistent with the saved evidence.
  No additional solve or overall speedup is claimed; search associations are
  separated from causal attribution of particular reductions.
- The callback cap, LP cap, aggregate 6.2%/7.4% shares, observed 1.00501-second
  maximum, roughly 40% individual shares, untimed admission term J, and
  trigger visits without a record are distinguished. The reported 17 ms value
  is correctly an allocation including rejected trigger visits. LP time
  explicitly includes dual-bound validation. No hard overrun bound is claimed
  by the effort theorem for this implementation.
- The algorithms now give the 1 ms LP-limit floor, gain before integer rounding,
  conditional tangent monotonicity, and a qualified support-based discovery
  cost. The exact closure/proof, optional objective proposal, failed-round
  preservation, and fixture table remain faithful to the reference source.
- Nonroot node-zero attribution is now justified as a classification based on
  recorded number/depth plus inspected SCIP source, and the text identifies the
  inspected 10.0.3 version rather than silently equating it with the campaign.
  I additionally inspected the retained **10.0.2** source at
  `research-20260929/publication/scip-bug/src/scipoptsuite-10.0.2/scip/`:
  `CMakeLists.txt` declares 10.0.2; `tree.c` initializes node numbers to zero,
  assigns positive numbers in `SCIPnodeCreateChild`, and leaves probing nodes
  at zero in `treeCreateProbingNode`. This independently supports the same
  classification in the actual campaign version. No solver was executed.
- A direct saved-event read confirms the new bilinear-cycle illustration in
  both arms/seeds: root `first_visit` with no cutoff/zero changes, then
  `incumbent_improvement` with six changes, then `domain_reduction` with six.
  The five-probe and 69-public-incumbent comparison claims agree with the
  archived original-model reviewer source/report.

One optional wording refinement: in the final experimental interpretation,
replace “recorded propagator time was capped at about one second per run” with
“recorded propagator time stayed below 1.00501 seconds per run.” The surrounding
text already establishes the soft allowance and observed overshoot correctly;
this avoids suggesting an enforced hard cap and is not a remaining scientific
blocker.

Verification was limited to targeted read-only source/report inspections,
snapshot hashes, direct saved JSON flag/event reads, and inspection of retained
SCIP source. Prior verified numerical summaries were compared with the revised
transcriptions. No experiment, solver, archived analyzer, mathematical fixture,
project-wide verification, CI status, or CI log was run or inspected.
