# Stage 2, round 2: independent review 05

Verdict: **accept; no major issues found and no valid minor issues identified.**

## Scope

I reviewed every manuscript change from the immutable round 1 snapshot to `process/snapshots/stage02-round02`, including the full revised Proposition 7.1 and its proof in `sections/05-small-budget-minimax.tex`, the dimension-count qualification in `sections/04-four-block-certificates.tex`, the updated verification program, and README instructions. I checked the proof against its unchanged cumulative-control, endpoint, reach, and scaling dependencies. No other round 2 report was read, and no manuscript or frozen artifact was edited. The round 2 snapshot's 40 recorded file hashes still match.

## Mathematical audit

The exact instance optimum in equation (53), `18673/18396`, is proved correctly.

- **Capped inverse:** The interpolation slopes lie in `[0,3/4]`, hence every complement function increases at rate at least `1/4`. Its capped inverse is nondecreasing and 4-Lipschitz on nonnegative arguments. The proof explicitly handles an upper inverse value at the horizon: the lower inverse value is then uncapped, and its equality plus the upper feasibility inequality gives the claimed Lipschitz estimate. The endpoint `y=0` causes no exception.
- **Distinct-mode lower bound:** Increasing the threshold by `delta` increases the first reach by at most `4 delta` and each two-mode reach by at most `20 delta`. The last complement increment on the uniform suffix is exactly `21 delta_*`. Thus no distinct word reaches the horizon for `0 <= delta < delta_*`. The equivalent triple-reach estimate is valid because the final threshold-one root is the start of the uniform suffix, and the inverse has slope `3/2` thereafter until capped. Lower thresholds are correctly excluded by monotonicity rather than left untreated.
- **Attainment:** The proposed times in equation (55) lie in the two specified affine segments. Along word `(0,2,1)`, the slopes `1/4`, `1/4`, and `2/3` yield the three displayed active-block endpoint errors exactly `E_*`. The unused portions of each mode's trajectory cannot have a larger one-sided error by endpoint monotonicity. Both the word and its rational times are correct.
- **Repeated words:** At threshold `E_*`, the masses of modes 0 and 1 exceed `2E_*`. The terminal support argument therefore forces the active set `{0,1}` whenever at most two modes are used. The two padded words `p,q,p` exhaust that set's schedules with at most three blocks. Their pair-end upper bound and the allocation slope bound give the middle-service upper bound in equation (57), even when the actual endpoint lies before `M_2`. Both positive contradiction margins are arithmetically correct. This excludes every repeated word at `E_*` and hence below it.
- **Scaled consequence:** Dividing the exact instance value by `57/8` gives `37346/262143`, which exceeds `8/57`. The manuscript correctly presents this as a minimax lower bound, not an exact determination of the three-mode minimax.

The added `n >= 9` qualification for the quotient dimension counts matches the stabilized symbolic construction and does not alter the certificate theorem or its proof.

## Independent exact optimization

I wrote `verification/reviewer05/stage02-round02/independent_optimum.py` without importing any manuscript verification code or using the reach-sensitivity estimates. It derives the one-sided errors directly from occupations at the three block endpoints.

For each of all 27 mode words, it considers all 36 chronological pairs of closed affine switching-time cells. Each cell produces a linear epigraph problem in the two switching times and the error threshold. The program enumerates every possible vertex using exact integer determinants and rational arithmetic, checks all inequalities, and minimizes the error. This covers shared cell boundaries, coincident switching times, repeated labels, and shorter schedules represented with zero-length blocks. The switching variables are bounded and the error is bounded below, so the minimum is attained at a vertex of this epigraph polyhedron.

All **972 cell problems** were solved. The global minimum is exactly `18673/18396`, attained by `(0,2,1)` at exactly `8341/4599` and `17639/4599`. Every word using fewer than three modes has a strictly larger optimum. The program also checks a degenerate cell with fixed switching coordinates. Complete word-specific rational results are saved in `independent-optimum.log`.

This independently verifies the new quantitative conclusion over the full schedule class, beyond checking the proof's arithmetic or testing threshold one.

## Build, presentation, and portability

I copied the snapshot into `verification/reviewer05/stage02-round02/relocated`, removed its supplied `.pdf` and `.bbl`, and performed a fresh LaTeX/BibTeX build. The 21-page build succeeds; its final log has no LaTeX warnings, unresolved references, overfull boxes, or underfull boxes. I rendered and visually inspected changed pages 14 and 18–21. The exact-value statement, table, inverse argument, repeated-word proof, equations, and following subsections are readable and consistently referenced.

The updated `check_new_results.py` passes from the relocated copy and uses only bundled or standard-library dependencies. The README accurately distinguishes its arithmetic/direct-schedule checks from the threshold-one polygon exclusion. Build and verification artifacts are confined to the assigned reviewer directory.

## Limitations

This review concentrates on the round 2 changes and their mathematical dependencies. I did not rerun the unchanged heavy-mode or all-dimension certificate collections, since the changed result neither modifies nor uses those arguments. I did not conduct a new literature search. The independent exact LP audit verifies this explicit instance, not an exact formula for the unrestricted three-mode minimax.
