# Independent review 01 — stage02-round01

**Corrected verdict: no major or minor issues identified.** I found no mathematical error or missing essential proof in the new stage, including the stronger three-mode counterexample that excludes repeated-mode schedules. The original presentation finding M1 below is withdrawn after checking the actual PDF coordinates.

## Correction to the original review

**M1 withdrawn: the subsection 7.1 title does not overrun the right margin.** My original pixel estimate from the displayed render was incorrect. After the root challenged the finding, I ran `pdftotext -f 18 -l 18 -bbox` directly on the frozen `main.pdf`. The final heading word `worst-case` ends at `xMax=513.074727` points; ordinary body text on the same page reaches `xMax=513.502290` points (and some punctuation protrudes farther). The heading fits inside that extent. The extracted coordinates are saved as `verification/reviewer01/stage02-round01/page18-bbox.html`.

No manuscript correction is required on this basis. The earlier numerical estimate of approximately 949 pixels was unsupported and should not be used. The mathematical audit and executable-check findings below are unchanged.

## Scope and proof audit

Read all of `03-heavy-and-reach.tex`, `04-four-block-certificates.tex`, and `05-small-budget-minimax.tex`, checked their stage-1 dependencies, and inspected the differences from the previously reviewed stage-1 snapshot. Read the entire exact general four-block verifier. Extracted the compiled PDF text and inspected its provided page-15 and page-18 renders. No other reviewer's report was read, no manuscript file was edited, and no subagent was used.

### Heavy-mode and reordering results

The integral network has a feasible fractional flow with the stated prefix capacities, bounded integer supplies and capacities, and an objective whose integral optimum forces at least two selections of the heavy mode. The use of a maximizing objective is necessary when a heavy terminal mass lies strictly between one and two, and the proof includes it correctly.

In the first-repeat lemma, the first repeated prefix has exactly one doubled mode and all other selected modes occur once. The deadline definition uses the latest point at which allocation is at most one, so a violated deadline gives a strict allocation inequality even with flat portions. The proposed integer start `j` places that deadline inside the doubled interval. The counting contradictions for slots before and after that interval are valid; the latter correctly adds the doubled mode's allocation of at least one. The proof controls all signs before, during, and after activation. Counts are preserved at the prefix boundary, preserving every later discrepancy. The extension-and-scaling argument therefore gives the universal heavy-mode result, including `s=0` and `T<(s+2)E`.

The one-sided reduction uses the heavy theorem in exactly its range. In the other case terminal masses control all positive discrepancies independently of the selected schedule. Its omitted-mode lower bound requires, and explicitly imposes, `k<n`.

### Two- and three-block analytic reach bounds

Checked the latest-endpoint identities, their strict capped-failure implication, and the monotonicity of the reach maps. Distinctness makes service before a mode's activation zero, which is the premise needed by the reach formula.

Re-derived the first-reach pair and triple inequalities, the exclusion inequalities, and the aggregation algebra. The coefficients used to substitute lower bounds are positive in the stated ranges (`n>=3` and `n>=4`). Maximizing pairs remain available outside their two selected indices, so the argument correctly leaves at most two exceptional exclusions. The final strict summed inequalities rule out failure even with flat allocation complements. The stated construction's pair matrix and exceptional scans are consistent with the claimed number of evaluations and comparisons.

### Four-block certificate proof

Every physical uncapped input satisfies each displayed LP constraint. Pair inequalities follow from the latest reach boundary and monotonicity of `H`; event-inclusion inequalities follow from monotonicity of `A`; equal-event constraints are justified by retention of a globally maximizing pair. Omitting other chronological constraints enlarges the feasible set and does not invalidate the required lower bound.

The maximizing-pair intersection with the three-element set, followed by the distinguished index's membership in the four resulting classes, gives exactly the ten table types and nine feasible types at `n=5`. The variable orbit rule distinguishes allocation to an excluded interchangeable index from allocation to another one. Symmetry averaging preserves the objective and feasibility without requiring an optimizer. At most six special indices and three additional indices cover every row pattern; only mass and objective multiplicities change thereafter. The affine reconstruction at dimensions 9 and 10 is therefore supported by a combinatorial count argument, not merely empirical interpolation.

Compared the displayed constraints, objective, variable enumeration, orbit reduction, and signs with the verifier implementation. The finite and polynomial dual identities have the correct sign for a minimization lower bound. Positivity of the shifted denominator and nonpositivity of shifted inequality multipliers establish the entire symbolic tail; the finite cases fill its complement. The code's checks cover all declared case identifiers. The analytic passage from weighted pairs to the aggregate triple reach and then four blocks is valid, with positive substitution coefficient for `n>=5`.

### Minimax and structural conclusions

The one-sided uniform recurrence lower bound allows repeated modes, and the upper reach schedules meet the full horizon at the reciprocal threshold. The heavy-mode reduction gives the full minimax formulas in the stated spare-mode range. Equal terminal masses independently control the positive discrepancy, giving the sharper restricted result. Checked the transition polynomials, their shifts, and the asymptotic coefficients.

For Proposition `prop:three-mode-failure`, the interpolated input is admissible, and the knot slopes make every allocation complement strictly increasing. The six distinct-mode reaches therefore stop at the stated last knot. The terminal necessary condition rules out every active set of size at most two that omits mode 0 or mode 1. Every remaining schedule with at most three blocks is represented by `p,q,p`, including shorter words by zero-length padding. The first two block constraints yield the claimed common maximum second endpoint, and allocation monotonicity yields the middle-service upper bound. Both exact lower/upper gaps are positive. Compactness then upgrades absence of an error-one schedule to a strict optimum above one. The uniform comparison is independently justified by the recurrence, so it does not improperly invoke the spare-mode theorem at `k=n`.

Both adjacent-pair counterexamples correctly concern fixed unit slots. Their prefix contradictions, terminal allocations, and displayed feasible alternative words support the claims. The discussion does not mistake either example for a refutation of the separate largest-heavy-mode conjecture.

## Independent checks performed

Created and ran these files only under `verification/reviewer01/stage02-round01/`:

- `check_analytic.py`: fresh rational implementation of the first-repeat reordering. Exhausted all 1,296 three-mode, four-cell half-simplex profiles and verified the construction for all 35,145 words whose original error was at most one. The reordered words retain their full multiset, contain an adjacent equal pair, and remain within error one. Every tested profile has a heavy mode and admits such a word.
- The same script built an independent continuous endpoint LP for each of the 27 three-block mode words and all 36 ordered pairs of interpolation cells for its switch times: 972 LPs for the new three-mode input. Every computed minimum exceeded one; the smallest was approximately `1.0150576212220048`. This uses floating-point optimization as corroboration only, not as a proof or an asserted exact optimum. The script independently checks the exact rational knot slopes and terminal masses.
- The same script checks both shifted transition polynomials and both displayed second-order asymptotic expansions using symbolic rational algebra.
- `check_reach.py`: fresh exact rational reach implementation tested 210 piecewise-constant inputs for `n=3,...,8`, including pure-mode profiles with flat allocation complements. Checked the two-, three-, and four-block reach conclusions on their appropriate ranges. Checked 30,205 instances of the stronger weighted-pair inequality, covering every three-element subset and every distinguished mode for each applicable uncapped profile. All passed.
- Ran the frozen `verify_general_four_block.py` after reading it: all 179 finite certificates and all ten polynomial certificates passed using integer arithmetic.

## Limitations

Finite input tests corroborate but do not prove the general results; the proof audit and exact certificate identities supply their mathematical justification. The independent LP check of the new three-mode example is numerical and is not relied on for its strict result. I did not reproduce certificate discovery, implement a wholly separate orbit-matrix generator, assess global novelty, inspect every PDF page visually, or judge the intentionally deferred general-bound, abstract, and literature-integration stages.
