# Stage 2, round 1: independent review 04

**Major-issue verdict: no major issue found.** I also found no minor issue requiring a correction in the stage reviewed. The analytic arguments establish their stated claims, including the strengthened counterexample over all three-block schedules. The computer-assisted result has an explicit and sound verification boundary. I recommend accepting this stage, subject to the primary agent's assessment of the other independent reviews.

## Scope

All manuscript locators below refer to the immutable snapshot `paper-switching-control/process/snapshots/stage02-round01/`.

I read every line of the new files `sections/03-heavy-and-reach.tex`, `sections/04-four-block-certificates.tex`, and `sections/05-small-budget-minimax.tex`, and rechecked the stage 1 definitions and results they use. I inspected `main.tex`, `macros.tex`, `README.md`, the reference-artifact README, the provenance and snapshot manifests, the general four-block verifier, the three new stage 2 checkers, and the heavy-mode construction checker. I extracted the 20-page PDF and inspected the supplied page-18 rendering. All 35 snapshot hashes match.

I did not consult other reviewers or their reports. The postponed introduction, broad literature attribution, and arbitrary-budget results were not treated as stage 2 omissions. No manuscript, source literature, or frozen-snapshot files were changed.

## Findings

There are no requested corrections. The following detailed checks identify the principal risks I considered and why I regard them as resolved in the current text.

### Universal heavy-mode theorem and one-sided reduction

Locators: `sections/03-heavy-and-reach.tex:9–139`.

- The prefix-flow network represents cumulative counts correctly. Slot supplies enter a chain at their own time; the outgoing chain flow is therefore the relevant prefix count. Integer lower and upper capacities and supplies permit an integral optimum. Maximizing the heavy mode's final count forces at least two occurrences because a feasible fractional value exceeds one. No unjustified inference from a repeated occurrence to a saved switch is made.
- The first-repeat prefix has exactly the claimed multiplicities. Its endpoint errors imply the bounds on each terminal prefix allocation. The latest unit-mass crossing used as a deadline is well defined, including flat allocation segments and equality at the end of the prefix.
- The deadline ordering argument covers both sides of the prescribed double block. For a mode following that block, the first `ell` modes would each have allocation greater than one at time `ell+1`, while the repeated mode has allocation at least one there; this yields the required contradiction. The artificial deadline cannot fail.
- The reordered prefix has error at most one for each sign, and it preserves all counts at the attachment time. The unchanged suffix consequently preserves all later discrepancies. Arbitrary measurable inputs cause no gap because blockwise endpoint monotonicity applies to them.
- Extending the horizon, scaling by `E`, and restricting the result preserve feasibility and the switch limit. The theorem includes `s=0`. The first repeated mode may differ from the heavy mode used in the flow objective, which the text explicitly distinguishes.
- The exact one-sided reduction uses attainment appropriately and separates the strict-heavy and no-heavy cases. Its omitted-mode lower bound uses exactly `k+1` available modes; the hypothesis `k<n` is needed and present. Repetitions remain allowed in the minimizing class.

### Analytic two- and three-block reach arguments

Locators: `sections/03-heavy-and-reach.tex:145–288`.

The reach maps use latest feasible endpoints. Their boundary equalities and strict terminal failure inequalities remain valid with flat parts of `H_i`. A composition with distinct modes controls the entire one-sided trajectory: a mode's negative discrepancy cannot increase after its block ends, and unused modes have nonpositive one-sided discrepancy.

I checked the two-first-reach identity, the three-first-reach identity, and the exclusion inequalities directly. The ordering bounds on allocations at the second- and third-largest first reaches have the correct directions. A pair attaining the global maximum survives every exclusion outside its two labels. The estimate `x_p+x_q >= x+y` holds even if neither deleted label achieves the two largest first reaches, and ties cause no change. The coefficients multiplying the global pair maximum are positive in the stated mode ranges. Substituting the bounds gives exactly `sum M_i >= n B_2`, and terminal failure then contradicts the target horizon.

The stated operation count is an evaluation count for reach maps and comparisons, not a claim of finite arithmetic integration for arbitrary measurable controls. Computing the first reaches, pair matrix, and two exceptional excluded maxima supplies the advertised construction.

### Four-block computational proof and all-dimension coverage

Locators: `sections/04-four-block-certificates.tex:17–256`; `verification/reference/verify_general_four_block.py`.

I compared each inequality family in the text with the checker. They agree. In particular, the pair constraints follow from uncapped reach and monotonicity, and reverse event-allocation inequalities are imposed only when the chosen maximizing pair survives the relevant exclusion. The stronger inequality permits an arbitrary distinguished mode; choosing a smallest first reach only occurs in its subsequent application.

The symmetry argument establishes a relaxation, not a representation of all controls. Averaging is valid without a finite optimizer. The orbit labels correctly distinguish allocation to an interchangeable excluded index from allocation to a different interchangeable index. Each `Q` event contains at most one interchangeable index because its excluded pair meets `S`, so unordered-pair orientation causes no missing orbit. The ten type representatives cover all positions of the global maximizing pair and distinguished mode, with exactly one type absent at `n=5`.

The all-dimension argument is more than numerical interpolation. At most six indices are individually labeled. A constraint can involve at most three other indices, so all its equality patterns occur once `n>=9`. The mass-equation and objective multiplicities are established affine counts; the remaining matrix coefficients stabilize. For the ten chosen representatives, the individually labeled set is an initial interval of labels, which also supports the asserted stable first-occurrence ordering. The reconstruction from dimensions 9 and 10 consequently has a mathematical justification. I reran the supplied direct comparisons at 11, 23, and 37 as an additional check, without interpreting those finite comparisons as the proof of stabilization.

The finite dual multiplier sign is correct for `Ax <= b`: nonpositive multipliers reverse the inequalities and yield the desired lower bound. All coefficient residuals are checked, so no omitted nonnegative-variable residual multipliers are needed. Polynomial identities, positivity of the denominator, and shifted nonnegativity of the negated inequality multipliers establish the certificate for every integer `n>=23`. Together with dimensions 5 through 22, there is no uncovered dimension. The computational dependency is labeled clearly in the theorem and final minimax statements.

Locators: `sections/04-four-block-certificates.tex:260–307`.

The passage from weighted pairs to four distinct blocks has the correct exclusion sets and counts. A maximizing triple survives outside its three-mode set. The coefficient of its global reach is positive already at `n=5`; the aggregate substitution gives exactly `sum N_i >= n B_3`. The final contradiction uses uncapped latest endpoints, preserving the necessary strict inequality. The retained special-case verifiers are explicitly supplementary and are not used to hide a missing step in the all-dimension result.

### Minimax consequences, equal masses, and transitions

Locators: `sections/05-small-budget-minimax.tex:7–118`.

The one-sided uniform lower recurrence holds for arbitrary repeated-mode schedules. Combining it with the reach upper bounds gives the claimed one-sided minimax in each stated range. The full minimax formula follows from the universal heavy reduction; the uniform input's additional omitted-mode term is dominated by the pure-block obstruction when `n>=s+2`.

Equal terminal masses bound every positive discrepancy irrespective of the chosen schedule, so the restricted full-error formula follows. I checked the plateau thresholds, the stated intervals of strict improvement, and both asymptotic expansions. The expansions describe the full minimax because uniform input dominates beyond the proved crossover dimensions.

### Strengthened three-mode counterexample

Locators: `sections/05-small-budget-minimax.tex:131–229`, especially lines 183–221.

This is a valid strengthening beyond failure of six distinct-mode reach words.

- The knot increments define an admissible input; the largest individual slope is at most `3/4`, so each `H_i` is strictly increasing. The six distinct-word reaches equal `971/146`, and the uniform-tail extension does not create a later feasible root.
- The terminal masses are exactly `(5281,3985,3217)/1752` and sum to `57/8`. Both the first and second masses exceed two.
- Summing terminal inequalities over the active-mode set gives `sum_{i not in J} m_i <= |J|`. If at most two modes are used, omitting mode 0 or mode 1 therefore fails. The only possible active set is `{0,1}`; shorter schedules are covered by zero-length blocks in one of its two `p,q,p` words.
- The first two endpoint inequalities imply `u<=R_p` and `v<=M_2`. The middle-service estimate does not wrongly subtract first-block service from a repeated mode: it is applied to the mode `q`, which is unused until its middle block. Thus `v-u <= A_q(v)+1 <= A_q(M_2)+1 = M_2-R_p` is valid.
- The two terminal lower bounds for middle service are respectively `2725/876` and `3373/876`. They exceed the upper bounds by `781/876` and `1057/876`, as printed. Every repeated-mode schedule is ruled out, and every three-mode schedule with three positive blocks is one of the six distinct words already ruled out.
- Compact attainment converts infeasibility at error one into a strictly larger optimum. The explicit uniform schedule and repeated-mode-valid lower recurrence prove the uniform comparator's optimum is exactly one.

The proposition establishes failure of uniform extremality for the one-sided problem at `k=n=3`. The surrounding statements preserve that scope and do not conflate it with the spare-mode range or an equal-mass result.

### Prescribed-pair counterexamples

Locators: `sections/05-small-budget-minimax.tex:231–end`.

I checked the tabulated rates, masses, and prefix contradictions. The four-cell example eliminates each possible adjacent pair of the specified heavy mode; its two feasible witness words have error at most one. The five-cell example eliminates the specified pair position for the uniquely largest-mass mode, while its stated alternative works. Their conclusions concern fixed unit slots, which the text states explicitly. They do not purport to disprove existence of some adjacent pair for a largest heavy mode.

## Verification performed

All logs and the fresh checker are under `paper-switching-control/verification/reviewer04/stage02-round01/`.

My independent `independent_checks.py` imports no manuscript verifier. It passed:

- all 35 snapshot hashes;
- 1,296 half-simplex four-cell profiles, checking integral prefix feasibility for each of 2,025 specified-heavy instances;
- 15,180 first-repeat rearrangements, covering every feasible nonadjacent word for those profiles;
- exact Fourier–Motzkin elimination for every one of 27 three-block words and every chronological switching-time cell of the new three-mode input: all 972 cells are infeasible at error one;
- direct checks of the six distinct reaches, terminal masses, and knot slopes;
- 48 independently evaluated distinct-reach examples in the two-, three-, and four-block ranges, including pure-cell inputs with flat `H_i`;
- 3,295 direct evaluations of the stronger weighted-pair inequality on those examples where all pairs are uncapped.

I separately reran the bundled `verify_general_four_block.py`, `check_new_results.py`, and `check_symbolic_quotient.py` from the frozen snapshot. All passed. Their logs report all 179 finite and ten polynomial certificates; the two structural examples; the new three-mode counterexample; the aggregate, plateau, equal-mass, and expansion checks; and all ten quotient comparisons at dimensions 11, 23, and 37. The extracted PDF contains no unresolved-reference markers, and the inspected page-18 rendering is readable.

## Limitations

Finite examples do not prove a universal theorem; the conclusions above rest on the separately inspected analytic reductions and, for four blocks, exact dual identities and the all-dimension orbit argument. I inspected and reran the supplied general certificate checker but did not write a second complete polynomial certificate verifier. The independent heavy-mode enumeration has finite bounds and supplements the general flow/reordering proof. I did not rerun the optional historical special-case certificate sets or perform a new global literature search. The current draft does not make a priority claim requiring such a search at this stage.
