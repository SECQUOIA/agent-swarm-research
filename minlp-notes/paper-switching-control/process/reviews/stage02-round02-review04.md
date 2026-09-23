# Stage 2, round 2: independent review 04

**Major-issue verdict: no major issue found.** I found no minor correction that should block acceptance. The exact instance optimum, its matching schedule, and the resulting minimax lower bound are supported by the revised analytic proof. A fresh independent exact optimization over all words confirms the value.

## Scope and files

I reviewed every textual difference between the frozen `stage02-round01` and `stage02-round02` snapshots, concentrating on the revised `sections/05-small-budget-minimax.tex`, its unchanged knot data and reach dependencies, the scope correction in `sections/04-four-block-certificates.tex`, `README.md`, `PROCESS.md`, and `verification/stage02/check_new_results.py`. I also checked the revised PDF text and the supplied page-20 rendering. All 40 manifest hashes match.

All manuscript locators below are relative to `paper-switching-control/process/snapshots/stage02-round02/`. I did not consult other round-2 reviews, modify the manuscript or snapshot, or spawn agents. Unchanged computational certificates did not raise a new concern and were not rerun.

## Findings and analytic verification

No corrections requested.

1. **Capped inverse and sensitivity — `sections/05-small-budget-minimax.tex:187–215`.** The piecewise-linear allocation slopes remain in `[0,3/4]`, including the uniform extension. Thus `H_i(t)-H_i(u)>=(t-u)/4` globally. The inverse is defined for every nonnegative argument because `H_i(0)=0`, and the proof of its 4-Lipschitz bound correctly handles a capped upper endpoint. If two inverse values differ, the smaller one is uncapped, so its exact root equation is available. The first-reach increase is at most `4 delta`; applying the same bound to the next inverse gives `4(4 delta + delta)=20 delta` for either order of each complementary pair. All comparisons use nonnegative `delta`.

2. **Distinct-mode lower bound — lines 203–215.** The identity `H_i(L)=M_i+1+21 delta_*` follows from the uniform tail and `L-t_*=(63/2)delta_*`. A final mode requires an argument at least this large, whereas the preceding pair and current threshold supply at most `M_i+1+21 delta`. This excludes every distinct word for `0<=delta<delta_*`. The stated reach bound using the suffix inverse slope `3/2` is also valid: increasing the threshold does not move the final inverse below its threshold-one starting point `t_*`. Capping only reduces its increase.

3. **Matching schedule — lines 217–229.** I checked that `u_*=8341/4599` lies in the stated first-mode segment and `v_*=17639/4599` lies in the stated second-mode segment. On both segments the relevant complement slope is exactly `1/4`. Consequently `H_0(u_*)=E_*`, `H_2(v_*)=u_*+E_*`, and `H_1(L)=v_*+E_*`. The word `(0,2,1)` is feasible and attains error `E_*=18673/18396`. Endpoint monotonicity controls all times, and direct error evaluation independently confirms it.

4. **Repeated-mode exclusion — lines 231–273.** The support inequality is now correctly scaled to `|J|E_*`. The two masses exceed `2E_*`, leaving only the active set `{0,1}` among schedules using at most two modes. Such schedules with at most three blocks are covered by the two `p,q,p` forms and zero-duration padding. The pair bound applies at `E_*`, and `M_2+20delta_*<L`. Allocation monotonicity and the global `3/4` slope bound yield the displayed middle-service upper bound even when `v<M_2`. The required terminal lower bounds exceed those upper bounds by `2923/4599` and `4372/4599`, respectively. The repeated-mode argument excludes all lower thresholds by feasibility monotonicity. Combined with the distinct-mode argument on `[1,E_*)` and infeasibility at one, this proves the exact minimum, with no remaining reliance on merely distinct-word failure.

5. **Uniform comparison and scope — lines 275–296.** The uniform schedule and lower recurrence still establish a uniform-input optimum of one on horizon `57/8`, allowing repeated competitors. Dividing the new exact instance value by that horizon gives `37346/262143`, strictly greater than `8/57`. The manuscript explicitly identifies this as a minimax lower bound, not an exact determination of `G^-_{3,3}`. It also preserves the distinction from the spare-mode and equal-mass settings. The theorem statement and proof use consistent one-sided-error notation.

6. **Certificate counts — `sections/04-four-block-certificates.tex:192–199`.** Adding `n>=9` correctly scopes the quoted stable quotient dimensions. The change does not alter the LP, symmetry argument, finite certificates, or polynomial identities. The previously checked all-dimension proof remains applicable.

7. **Verification claims — `verification/stage02/check_new_results.py` and `README.md`.** The added checks directly evaluate the matching schedule and exact sensitivity arithmetic. The script explicitly treats its three sampled sensitivity shifts as checks accompanying the analytic slope proof, not as proof of a continuum. The polygon audit is correctly described as being at threshold one, while the exact optimum is established analytically. The README's instance/minimax distinction is accurate.

## Fresh independent checks

I wrote `paper-switching-control/verification/reviewer04/stage02-round02/exact_projection.py`, which imports no manuscript verifier. Its log is `exact-projection.log` in the same directory.

The program builds the full one-sided scheduling inequalities directly from the knot table for every three-symbol word and every chronological pair of affine cells containing the two switch times. It includes zero-duration blocks. It uses rational Fourier–Motzkin elimination to remove both switch-time variables and project each feasible cell onto the error coordinate. This determines each cell's minimum exactly, rather than testing only error one or assuming the sensitivity formula.

All checks passed:

- 40 frozen artifact hashes;
- 27 words and 972 switching-time cells;
- global minimum exactly `18673/18396`, attained by word `(0,2,1)`;
- minimum over repeated-mode words `61618/51465`, strictly above the claimed optimum;
- direct evaluation of the stated schedule at every allocation knot and switch;
- the scaled coefficient, exact terminal masses, sensitivity arithmetic, and both repeated-mode margins.

I also reran the revised bundled `check_new_results.py`; it passed. Output is saved as `bundled-new-results.log`. The PDF extraction is saved as `main-extracted.txt`; the inspected revised page is readable.

## Limitations

This review targets the round-2 changes and their dependencies. The independent exact optimization establishes the stated finite piecewise-linear instance; it is not a proof of an unknown general three-mode minimax formula. The analytic inverse argument was checked separately from the computation. I did not repeat unchanged certificate verification, a global literature search, or a full final-manuscript review. No new priority claim or dependency on an unresolved result was introduced by these changes.
