# Stage 7, round 1: independent whole-manuscript review 02

## Verdict

**No major issue remains in this review. I found no valid minor issue requiring a correction.** I recommend accepting this manuscript at the final review stage, subject to the independent findings of the other reviewers. This recommendation follows a fresh review of the whole manuscript and its proof dependencies, not the acceptance of earlier stages.

The manuscript distinguishes proved results from remaining research questions. In particular, the higher-block reach question, the unrestricted three-mode three-switch minimax value, and broader dwell-constrained transfer are clearly identified as open developments. They are not gaps in a theorem the paper claims to prove. The counterexample and chronological-chamber certificate in the appendix have appropriately limited conclusions.

## Scope and independence

I read every section and proof in the frozen `process/snapshots/stage07-round01` manuscript: the abstract, introduction, Sections 2–16, Appendix A, and the references. I checked definitions and quantifiers across section boundaries, rather than checking only the new or changed text. The review covered the verification code and certificate foundations relevant to the main results, the computational presentation, and the source passages underlying the published-bound corrections and classical comparison. I did not read other current reviewer reports, author or root assessments, or root research outputs; I did not confer with other reviewers or delegate work.

All execution and generated artifacts are confined to `verification/reviewer02/stage07-round01/`, principally its `relocated/` copy. The source snapshot was not modified. A final SHA-256 check found **all 162 manifested files unchanged**; the result is recorded in `integrity-final.json`.

## Mathematical review

The following gives the precise locations and the substantive checks behind the no-issue verdict.

### Definitions, uniform inputs, and one switch

In `sections/01-foundations.tex`, Sections 2.1–2.3, I checked the distinction between cumulative controls, schedules, nominal blocks, physical switches, and full versus one-sided error. The ordered-time-simplex parametrization admits zero-length blocks and repeated labels without changing the feasible class. The compactness and continuity arguments support both minima and maxima used later. Cell averaging is asserted to preserve the evaluation of grid schedules, not the continuous optimum of the averaged input; the subsequent comparison of input classes uses the correct direction of the quantifiers.

In `sections/02-uniform-one-switch.tex`, Theorems 3.1–3.2 and Lemma 3.3–Theorem 3.4, I checked the uniform recurrence against arbitrary repeated labels. Earlier occupation of a repeated mode only strengthens the block-end inequality. The omitted-mode lower bound is used only where the number of available blocks is smaller than the number of modes. The integer recurrence, its floor/ceiling operations, the strict continuous-to-grid gap for uniform input, and the cases `n=2`, `s=0`, and `N=1` are consistent. The continuous three-term one-switch formula includes the terminal errors and the constant-schedule endpoints. The heavy and all-light cases in the upper-bound proof cover ties and zero allocations. The three-cell formula and the published-conjecture examples have the stated admissible budgets.

### Heavy modes and exact reach results

In `sections/03-heavy-and-reach.tex`, Theorem 4.1 and Lemmas 4.2–4.3, I checked the integral-flow repetition argument and the reordering of the first repeated prefix. The artificial deadlines, flat cumulative allocations, and the two positions left for the repeated mode are compatible with the strict deadline-counting contradiction. Reordering preserves the multiset of prefix occupations and therefore the unchanged suffix errors. Extension, rescaling, and restriction give the claimed theorem on the original horizon. Theorem 4.4 uses the heavy theorem only under its strict horizon condition and obtains the complementary upper bound from one-sided error and terminal masses.

For Section 5, the latest inverse convention is sufficient even when `H_i` is flat. The strict inequalities used to contradict failure of reach require an uncapped endpoint and are applied only in that situation. I checked the two- and three-block summations, the excluded-mode indexing, and the positivity of the coefficients at the minimum allowed dimensions.

In `sections/04-four-block-certificates.tex`, Section 6, I checked the path from a measurable control to a feasible point of the necessary-condition LP, then from its dual certificates back to the weighted pair inequality and the four-block theorem. No converse from LP feasibility to an actual control is required. The ten orbit types account for the marked triple, maximizing pair, and excluded mode. Symmetrization preserves the objective and feasibility. The symbolic construction beyond the finite range is supported by a stable orbit pattern, not just interpolation of observed optimal values. The manuscript clearly states where the proof is computer-assisted, what exact identities are checked, and why floating-point search is outside the proof boundary.

Theorem 7.1, Theorem 7.2, and Corollary 7.3 in `sections/05-small-budget-minimax.tex` correctly separate one-sided minima, unrestricted full minimax, and the equal-terminal-mass subclass. The restrictions on `n` are essential and are present. The plateaus at dimensions 8 and 12 and the displayed expansions agree with exact algebra.

### The all-word three-mode obstruction

I gave Proposition 8.1 and its proof in `sections/05-small-budget-minimax.tex` a separate analytic and computational audit. The rational knot table defines a legitimate cumulative control; all increments are nonnegative and sum to the time increment. The first-reach and pair-reach identities at threshold 1 are correct. The lower slope bound for `H_i` gives the stated displacement bound for capped latest inverses, including their boundary cases. The final uniform segment then gives the necessary lower threshold for every distinct triple.

The repeated-mode argument is essential, and I checked it independently. The terminal masses force both modes 0 and 1 to be used at any threshold under consideration. Thus a schedule with at most three blocks and at most two distinct labels can be covered by the form `p,q,p`, including zero blocks and its reductions. The middle-service estimate uses the absolute cumulative allocation at the second switch together with the initial-service bound; it does not incorrectly substitute an allocation increment for this quantity. The two final positive gaps exclude the repeated-label cases even at the claimed optimum. The displayed `0,2,1` schedule attains the threshold on the specified inverse segments. The comparison with uniform input concerns the same one-sided, at-most-three-block instance problem at `n=k=3`.

As an independent numerical proof check, I reconstructed all 972 continuous LPs directly from the rational input using three block lengths and an error variable. Exact primal and dual checks give the optimum

`18673/18396`,

attained by word `0,2,1`, with switch times `8341/4599` and `17639/4599`. The smallest optimum among repeated-label words is `61618/51465`, strictly larger. These additional numbers validate the manuscript claim; the stronger repeated-word number is only a review artifact and is not needed by the paper.

### General budgets, seeds, and boundary claims

In `sections/06-general-budgets.tex`, Lemma 9.1, I checked both the largest-mass and smallest-mass choices. The branch condition on the old coefficient, positivity of the new horizon and error threshold, the constant-schedule branch, and the redistributed simplex-valued control all hold. The coefficient transform remains valid when the auxiliary transformed variable is negative; positivity of the actual error coefficient is not lost. The argument bounds the one-sided error for the constructed schedule and does not silently assume a bound on positive discrepancy.

For Theorems 9.2 and 9.6, Corollaries 9.3–9.4 and 9.7, and Propositions 9.5 and 9.8, I checked the closed forms, telescoping seed transfer, monotonicity needed for strict improvement, the elementary plateau factorization, the integer form of the seeded plateau test, and the `n=16,k=5` example. I independently expanded all four established seed families and checked the exact second-order coefficients. The general asymptotic discussion claims matching leading order and an explicit gap between bounds; it does not claim a second-order expansion of the unknown minimax value.

In `sections/07-predecessors-and-frontier.tex`, Lemma 10.1 and Corollary 10.2, the all-light construction is valid when its intermediate coefficient becomes negative: the displayed comparison follows from the conservation identity and does not require that coefficient to be positive. Early completion of the horizon is allowed. The equal-mass consequence under `(n-k)^2 <= k` is indeed an **instance identity for every equal-mass profile**, using the omitted-mode lower bound, not merely a worst-case equality. The full plateau statement for `k<n<=2k` and the heavy case for `n<=k` are appropriately distinguished. The classical dimension-free comparison in Proposition 10.3 uses a universal upper bound; the cited source's grid-size restriction for sharpness is not imported as a restriction on that upper bound. The retained analytic predecessors are described as useful bounds, with their relation to the stronger theorem made explicit.

### Arbitrary grids and floor histories

In `sections/08-finite-grid-one-switch.tex`, Theorem 11.1 and its proof, I checked both LP families, their necessity, their sufficiency after reconstruction, and the elimination leading to the admissibility conditions. The symmetry reduction does not accidentally add the small-second-mass assumption to the other family. Endpoint cases, including equality in the cutoff condition and the `T/3` boundary, are covered. The finite-family/subsequence argument justifies taking the supremum threshold. The claimed rational-operation and polynomial-bit complexity applies to the compressed extremizer representation. Corollary 11.2 includes the correct three residue classes and the separate one-cell endpoint.

In `sections/09-three-mode-floor-chambers.tex`, Proposition 12.1 proves an all-length realizability statement: averaging the finite set of full compatible paths gives strict fractional coordinates at every interior time because the necessary floor and ceiling values are both represented. This is more than verification for five to seven cells. The perturbation argument passes from strict chambers to arbitrary inputs without changing the relevant finite set of schedules. I checked the exact-count argument, the exceptional six-history orbit, and the three repair words for the seven-cell upper bound. The repair proof bounds the three exceptional discrepancies by quantities whose sum is at most 4. The lower witnesses establish the same-grid values, and the continuous consequences have the claimed full-error scope: `F_{3,2}(T)=T/5` and `T/7 <= F_{3,3}(T) <= T/6`.

Section 12.4 carefully distinguishes the published lower bound in Sager–Zeile Corollary 5 from the separately restricted construction in Proposition 4. The counterexample violates the former as printed, while the latter is used only with its stated restriction. I checked these distinctions against the primary source text.

### Algorithms and transfer

In `sections/10-instance-algorithms.tex`, Section 13, I checked the dominance argument for the three one-switch candidates, its tied-mass cases, and the continuous crossing formula. In Lemma 13.2, a potentially negative terminal residual causes no problem because the prefix error is retained in the maximum. The subset recurrence correctly charges each mode for its entire assigned subset, including disconnected uses and the empty subset. Enumeration of exactly the padded number of nominal blocks still includes schedules with fewer physical switches. Dwell conditions are evaluated on merged physical runs, as required. The bounded candidate-label argument uses the equivalence of block roles only in its stated unrestricted setting.

The continuous LP enumeration covers every word and every nondecreasing cell assignment of the switching times, including repeated labels, coincident boundaries, and more nominal blocks than input cells. The endpoint inequalities suffice by monotonicity of each component within a block. The vertex-enumeration argument remains valid in lower-dimensional feasible polytopes. The polynomial-bit claim is expressly for fixed block budget.

In `sections/11-transfer-and-coarsening.tex`, Theorem 14.1, support preservation gives a chronological subsequence of the original switching word and hence does not increase the switch count. Integral prefix bounds yield the strict discrepancy bound even when some fractional prefixes are integral. The proof of the strict minimax comparison uses attainment, rather than assuming that a pointwise strict inequality remains strict under a supremum. I checked the binary nonuniform-grid construction, the sharpness family, and the separation between sharp instance transfer and an unproved sharp minimax gap. The coarsening certificate accommodates nonaligned input breakpoints and separately accounts for input perturbation. The odd-grid dwell example correctly marks a limitation of the theorem's feasible class, not a contradiction.

### Appendix, sources, and overall presentation

In `sections/14-higher-reach.tex`, Appendix A, I checked the general exclusion algebra and its additional premises. The weighted premise needed for extension is not asserted to follow from the currently proved reach theorem. The nonphysical feasible assignment disproves the stated relaxation implication, not a reach theorem. The interpolation lemma supplies a cumulative trajectory but does not imply the inverse and maximizer identities needed for the reach model. The final exact certificate covers the one prescribed chronological chamber; the manuscript does not generalize it to all chambers.

I independently reconstructed the complete 454-variable appendix matrix from the displayed definitions, without importing the author's matrix builder. The original feasible witness has objective `40328/387` and violates chronological monotonicity. With the 378 indicated chronological inequalities, the supplied dual and matching primal certify the exact value `13104/125`. Thus both the negative example and its limited repair have direct exact support.

The abstract, introduction, results table, figures, Section 15 computations, and Section 16 discussion describe the same mathematical scopes as the theorems. The public-profile results distinguish the pinned source, quantized input, grid-constrained optima, and the continuous one-switch optimum. Tables comparing budgets use the same grid on each row. Coarsening intervals retain the strict lower endpoint where justified. Timings are presented as implementation measurements, not asymptotic or priority evidence. References and surrounding prose acknowledge earlier CIA, prefix-rounding, shortest-path, and dwell-constrained work. I found no unsupported priority claim.

I inspected contact renders of all 56 pages after a clean build. The figures, tables, proof transitions, appendix, and bibliography fit their pages; I found no visible clipping or missing mathematical content. The final LaTeX log contains no warning, undefined reference, overfull box, or underfull box diagnostic. The length is substantial but consistent with the paper's combination of exact minimax proofs, certificate explanations, algorithms, and reproducible calculations.

## Checks and artifacts

The following work was performed in this final review, beyond reading the proofs.

- `relocated/reviewer-offline.log`: the complete portable `verification/run_all.py` suite passes, including exact finite and symbolic certificate checking, archived algorithm checks, integrity checks, and numerical-table/figure checks.
- `relocated/reviewer-clean.log` and `relocated/reviewer-build.log`: a clean `latexmk` build produces the 56-page manuscript. `relocated/contact-1.jpg` through `contact-7.jpg` support the whole-document layout inspection.
- `deep_checks.py` and `deep-checks.log`: independently reconstructed appendix matrix and exact dual verification; symbolic identities for the removal transform, plateau and dimension gap; 34 seed expansions; 1,035 integer seeded-plateau comparisons; all 972 three-mode continuous LPs; and 40 additional symbolic-quotient topology checks at dimensions 11, 17, 23, and 31. The last topology checks use the supplied quotient generator but test dimensions beyond its interpolation points; the appendix and three-mode LP assemblers are independently written.
- `n3-all-word-certificates.json`: exact primal and dual data for all 972 independently assembled cases. Floating-point optimization only proposed candidates; the checker verified exact primal feasibility, dual feasibility, and equality of objectives. Where direct rationalization failed, exact active-basis reconstruction supplied the certificate.
- `profile_checks.py` and `profile-checks.log`: 48 exact recursive construction cases, exercising 52 largest-mass choices, 24 smallest-mass choices, five constant branches, and flat/degenerate profiles. Direct discrepancy evaluation at all input and schedule breakpoints verifies the resulting schedules. A separate 48 shuffled equal-mass pure-phase profiles verify the instance identity in four boundary-band parameter pairs, including `(n,k)=(20,16)`.
- `floor_words.py` and `floor-words.log`: an independent full-word bitset construction, without the supplied count-node recurrence, recovers the distributions `{0:3,1:138,2:255}`, `{0:3,1:255,2:1377,3:237}`, and `{0:3,1:414,2:4542,3:3891,4:6}` for five, six, and seven cells. It identifies precisely the six permutations of the exceptional history and checks the three repair words and their single exceptional coordinates.
- `integrity-final.json`: all 162 snapshot hashes match the frozen manifest.

## Limitations

This is a mathematical and computational peer review, not a formal proof-assistant verification. The fresh exact tests supplement the written arguments; they do not replace the analytic universal proofs. I did not repeat machine-dependent timing measurements or refetch the public data in this final round: the complete archived computational suite was rerun, and the public-source reproduction had already been independently checked during the preceding computational review. I checked the source claims material to the mathematical comparisons and corrections, but did not attempt an exhaustive global novelty search.

No proposed manuscript correction follows from this review. I have finished the review and will make no further writes to its artifacts.
