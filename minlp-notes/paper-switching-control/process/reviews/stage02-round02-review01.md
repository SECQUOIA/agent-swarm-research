# Independent review 01 — stage02-round02

**Verdict: no major or minor issues identified.** The strengthened exact instance optimum is justified, including all repeated and shorter schedules. I independently verified its lower bound by exact dual identities for all 972 word/switch-cell linear programs, and verified the matching schedule directly with rational arithmetic.

## Scope

Compared the frozen round-2 and round-1 snapshots. Reviewed every mathematical and verification change: the scoped quotient-size statement in `04-four-block-certificates.tex`, the full strengthened proposition and discussion in `05-small-budget-minimax.tex`, the updated `verification/stage02/check_new_results.py`, and the README description. Rechecked the dependencies concerning endpoint monotonicity, distinct-word maximal reach, scaling, and uniform recurrence. The remaining general four-block proof and certificates are unchanged; the previous round's audit remains applicable, and I did not rerun the complete unchanged certificate suite.

No other round-2 review was read. I did not edit the manuscript or snapshot and used no subagent. All new check artifacts are under `verification/reviewer01/stage02-round02/`.

## Detailed audit of the exact three-mode optimum

- **Lines 194–201, capped inverse:** The complement functions are strictly increasing from zero, with slope at least `1/4`. Their inverses are defined for every nonnegative argument because zero is feasible. If two capped inverse values differ, the smaller is strictly below the horizon and its defining inequality is an equality. The larger still satisfies its defining inequality even when capped. This proves the stated 4-Lipschitz bound, including the zero argument and all cap configurations. If both values are capped, the bound is immediate.
- **Lines 203–215, sensitivity lower bound:** Monotonicity and the inverse bound give a first-endpoint increment at most `4 delta` and a second-endpoint increment at most `20 delta`. For each fixed distinct word, using the largest feasible first and second endpoints maximizes the final reach by the established reach-map monotonicity. Thus this calculation applies to every schedule for that word, not merely the chosen greedy schedule. Both orders of each pair have the same base endpoint `M_i`, so all six words are included. On the suffix, the complement slope is exactly `2/3`; the arithmetic `H_i(L)=M_i+1+21 delta_*` is correct. It excludes every threshold in `[1,E_*)`. The equivalent capped reach bound is valid because the base final reach is `t_*` and increasing the threshold cannot move that final reach backward.
- **Lines 217–229, attainment:** Both proposed switching times lie in the claimed affine segments. Their complement slopes are exactly `1/4`. The three block-end equalities follow with the common error `18673/18396`. Each selected mode is unused before its unique block, and its negative discrepancy decreases after the block. The endpoint argument therefore proves feasibility for the entire trajectory, rather than checking only necessary endpoint conditions.
- **Lines 231–270, repeated and shorter words:** At threshold `E_*`, both terminal masses `m_0,m_1` exceed `2E_*`. The summed terminal constraints therefore exclude every active set of size at most two omitting either of these modes. The only remaining set is `{0,1}`. Any schedule on it with at most three maximal blocks is `p,q,p` after allowing zero-length padding, so both alternations and all shorter schedules are included. Its middle mode has not been used previously, which justifies applying the distinct-pair reach bound to the first two endpoints. Monotonicity plus the allocation slope bound gives `A_q(v)<=A_q(M_2)+15 delta_*`, whether `v` lies below or above `M_2`. The resulting two exact service gaps are positive. This excludes all repeated-mode schedules even at `E_*`, and hence below it.
- **Lines 271–285, all thresholds and quantifiers:** Infeasibility at one excludes thresholds below one by monotonicity, so the proof has no missing low-threshold range. Together with attainment, the two exclusions establish the exact instance optimum. The uniform-input comparison uses the general block-end recurrence, which remains valid at `k=n=3`; it does not improperly apply a spare-mode theorem. Scaling gives exactly `37346/262143` per unit horizon. The text explicitly states this as a minimax lower bound, not its exact minimax value.

The updated supplementary checker correctly distinguishes its direct rational checks of the analytic sensitivity argument from its separate exhaustive error-one polygon audit. Its polygon representation covers closed interpolation cells and degenerate switch intervals. The README describes these roles accurately.

## Other changed claim

`04-four-block-certificates.tex:192–195` now scopes the reported quotient-size ranges to `n>=9`, which is the stable-pattern range established in the preceding argument. I reconstructed all ten quotients at `n=9` with the unchanged builder and obtained exactly 57–162 variables, 151–826 inequality rows, and 10–19 equality rows. The clarification is correct and does not change the proof.

## Independent exact all-word check

Created and ran `exact_lp_audit.py` without importing any manuscript implementation. It constructs the input from the rational table and its uniform suffix, then covers all 27 words of length three and all 36 chronological interpolation-cell pairs for their switching times.

For each of these 972 cases, the variables are the first switch, second switch, and error. The LP includes the closed cell bounds, ordered switching times, nonnegative error, and every mode's one-sided constraint at both switches and the horizon. Endpoint monotonicity makes this an exact representation of that word/cell case. Zero-length blocks and adjacent repeated labels are included. Every possible pair of switching times lies in at least one enumerated closed cell pair.

SciPy proposes a sparse dual support. SymPy then solves the dual coordinate equations on that support using exact rational arithmetic. The script independently verifies every dual multiplier's sign, all three coordinate identities, and that the resulting exact lower bound is at least `18673/18396`. Floating-point solver status or objective values are not used as proof of a lower bound. All 972 exact dual checks passed; the smallest certified bound equals `18673/18396`, and only the word `(0,2,1)` reaches that smallest bound among these certificates. The audit also evaluates the matching schedule directly on the union of the input knots and switching times and obtains exactly that error.

The exact dual data are saved in `dual_certificates.json`. This provides a separate lower-bound check from the manuscript's inverse-sensitivity argument and covers arbitrary error thresholds in each LP, not only threshold one.

Also ran the updated standard-library `check_new_results.py`: the exact-optimum arithmetic, matching schedule, all 972 error-one polygon checks, aggregate identities, and adjacent-pair counterexamples passed.

## Presentation and limitations

The changed proof is sufficiently detailed and keeps the instance/minimax distinction clear. Inspected the supplied rendered page 19 and extracted bounding boxes for changed pages 18–21; no layout issue was identified. The previous round's heading-overrun allegation remains withdrawn and is not a finding of this review.

This is not a new global novelty assessment or a full visual inspection of every page. I did not regenerate unchanged general four-block certificates or implement a second general orbit builder. The independent exact LP check uses SciPy for discovery of support and SymPy for rational calculations, whereas the bundled publication checker remains standard-library-only. Those review dependencies are not new manuscript requirements.

## Required corrections

None identified.
