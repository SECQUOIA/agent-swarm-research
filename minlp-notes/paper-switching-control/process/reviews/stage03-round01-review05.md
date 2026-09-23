# Stage 3, round 1: independent review 05

Verdict: **accept this stage; no major issues found and no valid minor issues identified.**

## Scope and independence

I reviewed all of `sections/06-general-budgets.tex` and `sections/07-predecessors-and-frontier.tex` in the immutable `process/snapshots/stage03-round01` snapshot, together with the necessary earlier reach, heavy-mode, uniform-input, endpoint, and scaling results. I also read the new verification scripts, the chronological-chamber checker and its original relaxation builder, the independent event-witness checker, and the manuscript and stage 3 READMEs. I did not consult other stage 3 review reports or delegate work.

All builds, executions, and independent programs are under `verification/reviewer05/stage03-round01/`. The frozen snapshot was not modified; its 71 manifest entries still match their hashes.

## Mathematical findings

No corrections are requested. The following were the main points of the audit.

### Mode removal, elementary and seeded bounds

Locators: Lemma 8.1 through Proposition 8.8 in `06-general-budgets.tex`.

Both branches of the mass-removal lemma are valid. For the maximum-mass branch, `E >= T/n` and failure of the constant-mode branch give a strictly positive residual error. For the minimum-mass branch, `a <= T/n` and `E > T/[n(n-1)]` give positivity; the prefix length is positive as well. The slope of the affine function of terminal mass changes sign at precisely `C=1/(n-1)`, so the respective extremal-mass choices prove the required contraction inequality. I checked the equality case separately. Completing the remaining rates preserves the simplex constraint and measurability, and appending the previously unused mode preserves distinctness and the one-sided error bound.

The transformed recurrence is correct. Its telescoping product gives the elementary coefficient, including the zero transformed seed when the initial dimension is two. The full, one-sided, and equal-mass bounds use the correct input classes and lower witnesses. The plateau factorization includes its endpoints and is described as a guaranteed interval, not a maximal one.

The general seed formula retains the sign of the seed transform and has positive denominators. The negative four-block seeds are valid one-sided bounds and can be propagated by the minimum-mass branch; clipping them would weaken that conclusion. I checked the derivative used for strict comparison with the elementary coefficient, the `n=16,k=5` plateau arithmetic, and the integer plateau criterion. The text correctly distinguishes strict improvement of the one-sided coefficient from full bounds that may coincide on a plateau.

The elementary, uniform, and seeded series coefficients agree with expansion of the displayed rational functions. The seed-series proof expands the transform far enough before cancellation of the leading denominator factor. The manuscript limits its general minimax conclusion to the common first-order correction and does not misstate a seeded upper expansion as an exact second-order minimax expansion.

### Light-input and boundary results

Locators: Lemma 9.1 and Corollary 9.2 in `07-predecessors-and-frontier.tex`.

The predetermined greedy endpoints increase, and the unused-mode allocation average gives the required active-mode bound at the next endpoint, including a final endpoint capped at the horizon. The mass assumption controls the opposite discrepancy sign throughout. The relation `k(n-k+1)/(n-k) >= n` is exactly `(n-k)^2 <= k`.

The new equal-mass conclusion is correctly an **instance-wise equality** throughout its stated band: the construction gives error at most `T/n`, and every schedule with fewer blocks than modes omits a mode of that terminal mass, for every input in this class. No characterization outside the band is claimed. I also checked the `n <= k` heavy-only upper bound and the exact `k<n<=2k` plateau.

The strict finite-mode dimension-free bound and its supremum follow from the displayed coefficient difference and the uniform lower limit. The certificate-free four-block bound is the analytic three-block seed propagated once; its smallest dimension uses the minimum-mass branch. Its plateau, positive gap, and series agree with the formulas. The third-largest-mass sufficient condition correctly reserves an unused large-mass final mode, and the eight-mode example has the stated stronger instance guarantee.

### General exclusion and the research boundary

Locators: Lemma 10.1 and Sections 10.1–10.3 in `07-predecessors-and-frontier.tex`.

The exclusion inequalities follow from actual uncapped maximum-composition reaches and allocation monotonicity. The coefficient of the global `(k-1)`-block reach is positive over the stated domain. Under the two additional premises, the recurrence for `B_j` gives the aggregate lower bound and the strict final contradiction. The weighted higher-block premise is explicitly left as a premise, not silently imported from the four-block case.

The negative event assignment is a counterexample to sufficiency of the specified relaxation, not to a measurable-control reach theorem. The numerical event order and coordinate decrease contradict a common cumulative trajectory. The text also correctly notes that the chosen four-element set is not required to support a globally maximizing four-word.

The interpolation lemma is correct, including tied event times and events at zero. Conservation and coordinate monotonicity provide simplex-valued interpolation slopes, but do not enforce the inverse-reach identities; the manuscript explicitly preserves this distinction.

The chronological proposition concerns exactly one closed event-order chamber. Its inequalities enforce that order by conservation, without fixing numerical event times. The dual residual has the correct nonnegative sign because variables are nonnegative; the inequality multipliers have the correct nonpositive sign. The uniform primal supplies attainment. Neither the proof nor the conclusions extend the certificate to other orderings, other maximizing sets, other dimensions, or the general five-block question.

## Independent checks beyond the supplied logs

I wrote two programs without importing project implementation code.

1. `independent_chamber.py` reconstructs all **3,660 original inequalities, 378 chamber inequalities, and 64 equalities** from the stated row families and event enumeration. It independently checks the old witness and its objective, reconstructs the chronological permutation, confirms the 239 coordinate-order violations and maximum decrease, and verifies the saved rational dual against the independently built rows. It then constructs the uniform primal directly from the formulas rather than trusting the saved primal. The exact lower and upper values both equal **13104/125**, and the dual has 254 nonzero rows. Results are in `independent-chamber.log`.

2. `independent_light_band.py` constructs irregular pure-mode profiles with exactly equal terminal masses by splitting each mass into unequal pieces and shuffling them. It implements the greedy endpoints independently and directly evaluates full discrepancy on the union of input and schedule breakpoints. All **42 profiles** pass. They test the inclusive band boundary and adjacent values for deficits `d=1,...,5`, on horizon `7/3`; 30 lie within the full-horizon band and have exact error `T/n`, while 12 just outside it satisfy the promised prefix bound. Results are in `independent-light-band.log`.

These are supplementary checks. The universal measurable-input claims rest on the analytic proofs, and the chamber assertion rests on the exact dual/primal certificate with the verified row construction.

## Build, presentation, and standalone execution

I made a relocated copy, removed its supplied PDF and bibliography output, and rebuilt with LaTeX/BibTeX. The fresh 32-page build succeeds. The final log contains no LaTeX warnings, unresolved references, overfull boxes, or underfull boxes.

All eight documented stage 3 verification programs pass from the relocated copy, including integrity checks and the chronological certificate. The optional numerical discovery program is not used by verification; its separate requirements and certificate scope are documented.

I rendered and visually inspected PDF pages 21–32, covering all new material. Equations, proof divisions, parameter ranges, cross-references, and the dense event specification remain readable. The progression from proved bounds to the explicitly conditional research question is clear. Later grid/algorithm chapters, the completed abstract, and final literature integration are intentionally outside this stage.

## Limitations

I did not rerun unchanged earlier certificate families or undertake a new external literature search. The independent chamber reconstruction covers the one advertised chamber, not all chronological permutations. The independent greedy checks sample piecewise-constant measurable inputs; they do not prove the all-input theorem by enumeration. No finding in this review resolves the explicitly open higher-block reach conjecture or the unused largest-heavy-mode adjacency strengthening.
