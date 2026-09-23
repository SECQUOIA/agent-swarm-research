# Stage 6, round 2 — independent review 1

Verdict: accept this stage. I found no valid major or minor issue in the corrected snapshot.

## Scope and findings

I reviewed `process/snapshots/stage06-round02`, including the whole computation section, generated tables, integration and README, and the changed external implementation and verification sources. I read the round-1 root assessment, correction record, correction validation and updated dependency manifest. I did not read another round-2 report or coordinate judgments with other reviewers.

1. **S06R02-R1-F00 — no outstanding finding.** The major baseline criticism is resolved in both the implementation and the scientific interpretation. The four accepted local corrections are also resolved. No further change is requested.

The following explains the substantive checks underlying that verdict; these are verification conclusions, not additional findings.

## Fixed-weight formulation and original-coordinate recovery

The corrected description at `sections/08-computation.tex:93–105` matches `code/network_simplex_benchmarks/strong_baselines.py:40–85`. I reconstructed the substitution independently. For a retained positive state of weight `w`, its variables satisfy `Af=w b` and `0<=f<=w u`. Substituting `x=sum(f)` repeats each original x coefficient across state blocks. Substituting an observed product adds its coefficient to the corresponding state/arc position. A zero-weight observed product is identically zero. The original y contribution is constant in the objective and is moved to the right-hand side of each additional row. The implementation applies all four operations, including dense rows that simultaneously contain x, y and z terms.

Global merging occurs before zero-state removal. Its default weight is one minus the total weight of observed labels, so it includes the residual and every unused explicit label. These states have identical remaining costs and constraints after the original y contributions are substituted. Conversely, any positive merged default flow can be split proportionally among its constituent weights. This proves the merger is exact also for additional original-coordinate linear rows, and explains why zero residual weight or positive weight only on an unused label causes no defect. The slot map preserves the original, possibly sparse label indices. Recovered original products use that map, and the objective constant is restored after optimization.

My executable `verification/reviewer1/stage06-round02/check.py` constructs a separate original-hull vertex LP. Its network polytope has two parallel arcs carrying total flow two, an independent capacity-three loop, and an isolated zero-balance vertex; its four vertices are explicit. Taking their products with simplex vertices gives the comparison hull without calling a state-flow formulation. Tests covered six explicit labels with sparse observations, no observations, and no explicit labels; all-zero explicit weights; weight only on an unused label; zero residual; positive residual; and mixed zero/positive observed states. Objectives have nonzero y costs, and most cases include three dense original-coordinate coupling rows.

Results:

- 100 fixed-weight full/global objective comparisons passed against this independently constructed vertex LP.
- All 100 returned original points passed objective, fixed-y, coupling-row and state-flow reconstruction checks. Each retained flow satisfied its balance and scaled nonunit bounds; each observed product matched the correct retained slot or zero; aggregate x matched the sum of flows. Model variable counts matched the retained positive states.
- 26 deliberately impossible y-only or zero-product rows were rejected, testing the affine substitution in cases where simply dropping a column would give the wrong answer.
- 24 free-weight full/global comparisons with dense coupling rows also passed.

These are numerical LP comparisons with explicit tolerances. Their role is to check implementation against independent formulations, not to supply an exact optimality certificate. The algebraic argument above establishes formulation equivalence. The manuscript preserves this distinction.

## Remaining stage and corrected interpretation

The sparse-label exact flat implementation and its compact decomposition interface are unchanged by this correction. I retained the direct source audit and independent exact tests from my round-1 report: 71 decompositions, 29 globally checked cuts, and 288 numerical membership comparisons, including sparse labels and zero weights. The current and archived manifests were checked anew. No changed baseline interface invalidates those exact-separator results. The separation/recovery wording at lines 39–49 now correctly distinguishes the three-label circuit separator from inverse-basis recovery and includes observation sorting in the implementation cost.

I re-examined the complete section's model assumptions, numerical/exact status distinction, two-state reduction, independent-state optimization identity, aggregate-budget interpretation, and transportation illustration. The budget is correctly an intersection with the component hull, not a claim that convexification commutes with an added row. The numerical baselines remain numerical, including after rational input weights choose the active states. The implementation is not presented as a general exact LP optimizer.

The rerun changes the relevant conclusion: the globally merged fixed-weight LP has the smaller median than initial compression in both the sparse and budgeted comparisons. The text reports this and notes overlapping ranges in the sparse case. The all-labels-observed control still supports a local compression benefit. The distinction between model size and timing, the limitation to synthetic small controls, and the different evidence returned by exact and numerical queries are clear. No unsupported universal speed claim remains.

## Data, reproducibility and build checks

My separate `verification/reviewer1/stage06-round02/data-check.py` performed these checks:

- Verified all **100 current dependency hashes** and all **83 archived hashes**.
- Compared all three optimization cases with the archived inputs: names, weights, objectives, extra rows, graph sizes, state counts and observations are preserved.
- Confirmed flat, membership and cold-library records are unchanged.
- Independently recomputed all **483** stored minimum/median/maximum timing summaries from raw runs.
- Ran the corrected table generator in a private miniature tree and compared all **five** generated tables byte for byte with the frozen snapshot.
- Independently removed a flat case, duplicated an optimization case name, removed a method measurement, and changed a membership status. The private validator rejected all four mutations.

I also inspected the optimization-only rerun source, including reuse of the archived inputs, fresh warmups and rotation, and its retained-data checks. The single shell continuation in the manuscript is now correct. The complete-grid validation does not merely accept whichever cases happen to remain.

A private clean snapshot build completed successfully with **45 pages**, no LaTeX warnings, no unresolved references and no overfull or underfull boxes. Evidence and logs are under `verification/reviewer1/stage06-round02/`.

## Limits

I did not independently repeat the full official timing campaign: I checked the raw records, input preservation, regeneration and the revised interpretation. The finite numerical tests do not guarantee arbitrary floating-point conditioning, and the manuscript does not claim that guarantee. This round rechecks the whole Stage 6 interpretation and its changed code; it does not reopen every accepted proof in Sections 1–7 or purport to give a new exhaustive literature search. I found no newly exposed dependency issue.
