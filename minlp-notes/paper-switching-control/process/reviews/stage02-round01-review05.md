# Stage 2, round 1: independent review 05

Verdict: accept this stage. **No major issues found. No remaining valid minor issues identified.**

## Scope and independence

Reviewed the immutable `process/snapshots/stage02-round01` manuscript, including all of `sections/03-heavy-and-reach.tex`, `sections/04-four-block-certificates.tex`, and `sections/05-small-budget-minimax.tex`, and their stage 1 dependencies. I checked the stage 1 source changes against the prior frozen source, reread the foundations and relevant earlier results, and inspected the current main file, macros, bibliography, README, verification instructions, and exact all-dimension checker. I did not read other stage 2 review reports, contact another reviewer, edit the manuscript, or delegate work.

All computations and builds used a relocated copy under `verification/reviewer05/stage02-round01/`. The original snapshot's 35 manifest entries still match their SHA-256 hashes.

## Mathematical assessment

### Heavy-mode rounding and reduction

Locators: Lemmas 3.2–3.3 and Theorems 3.1, 3.4 in `03-heavy-and-reach.tex`.

The flow construction is feasible with the stated fractional input increments. Integer supplies and integer arc bounds yield an integral maximizer of the terminal flow in the heavy mode, so strict heaviness gives at least two occurrences. This does not assume that a repeated occurrence is already adjacent.

The reordering proof supplies the missing adjacency while preserving full error. I checked the case `A_q(r)=1`, when the latest threshold time is the horizon `r`, the bounds on the proposed integer slot location, artificial deadlines, and the allocation-count contradiction both before and after the double block. The prefix multiset is unchanged, so the suffix is valid. The proof neither promises the heavy mode chosen by the flow nor preserves the floor/ceiling invariant after reordering; the manuscript correctly states these distinctions. Extension, scaling, and restriction preserve the claimed budget.

The one-sided reduction is valid with the stated `k<n` hypothesis. The upper proof separates strict heavy masses from masses at most the threshold, and the omitted-mode lower example requires exactly the spare mode supplied by that hypothesis. The full optimum dominates the one-sided optimum before taking the outer supremum.

### Analytic reach bounds

Locators: equation (21), Lemma 4.1, Theorem 4.2 in `03-heavy-and-reach.tex`.

Latest feasible endpoints are well defined for measurable relaxed inputs because cumulative functions are continuous and the complement functions are nondecreasing. The two boundary statements remain valid on flat portions. I checked the two-largest and three-largest first-reach estimates, the excluded-pair estimate, the aggregate substitutions, and the strict final contradiction. In particular, the coefficients whose sign is used are positive in the stated mode ranges. Appending a mode excluded from the prefix gives distinct schedules, while the minimax competitors retain repetitions. The operation count concerns reach evaluations and comparisons, without claiming a finite integration cost for an arbitrary measurable input.

### Four-block certificate proof

Locators: Section 5 in `04-four-block-certificates.tex` and `verification/reference/verify_general_four_block.py`.

Each event constraint follows from the actual pair maximum, allocation monotonicity, or retention of a global maximizing pair after an exclusion. The absence of chronological constraints between unrelated events enlarges the feasible set and is harmless for a certified lower bound; the manuscript does not claim that every feasible point represents an input.

I checked the ten symmetry types, including the absent tenth type at `n=5`, and the averaging argument. The orbit description distinguishes an excluded interchangeable index from a different interchangeable index. Because each pair-constraint row uses at most three interchangeable indices and at most six indices are fixed, the topology stabilizes by `n=9`. The remaining dimension dependence is exactly the affine mass counts and affine objective multiplicities described in the text. This supplies the mathematical justification for reconstructing those counts at 9 and 10 rather than trusting numerical interpolation.

I read the checker implementation against the displayed constraints and dual identities. Its signs, exact coefficient residual checks, coverage counts, polynomial denominator identity, and shifted-coefficient sign tests establish the claimed lower bound. The finite and polynomial cases have no uncovered integer dimension. The final passage from weighted pairs to excluded triple maxima and four distinct blocks is analytic and its coefficient signs and aggregate identity are correct. The computational dependency is clearly identified; the earlier small-dimension certificate collections are explicitly optional checks.

### Minimax consequences and structural limits

Locators: Sections 6–7 in `05-small-budget-minimax.tex`.

The one-sided lower recurrence holds for repeated modes. Combining it with the reach upper bounds gives the claimed exact one-sided values; combining those values with the heavy-mode reduction gives the full minimax. The equal-terminal-mass result is a separate restricted maximum and does not confuse it with the unrestricted value. I checked the plateau transitions, the listed strict improvements for equal masses, and the asymptotic coefficients.

The new `n=k=3` proposition proves failure for the full class of three-block words under the **one-sided** criterion, not merely six distinct permutations. I checked the interpolation slopes, terminal masses, first and pair reach equations, and the two repeated-word middle-service contradictions. Terminal support inequalities exclude every active set except `{0,1}` when fewer than three modes are used; the remaining schedules have one of the two padded forms `p,q,p`. With three modes in three blocks all labels are distinct. Thus the cases are exhaustive. Attainment is correctly used to turn absence of an error-one schedule into a strict instance-optimum inequality. The comparison uniform schedule has optimum exactly one. The two adjacent-pair counterexamples are correctly limited to fixed unit-slot words and do not overstate a conclusion about continuous switching times.

## Independent checks and reproducibility

The fresh relocated LaTeX/BibTeX build removed the supplied `.pdf` and `.bbl` first, then rebuilt successfully. The final log contains no LaTeX warnings, unresolved references, overfull boxes, or underfull boxes. I visually inspected the stage 2 material on PDF pages 8–20, including both tables, the dense event constraints, certificate instructions, and the counterexample proof. The section progression and references are readable and consistent with the foundations.

The complete relocated stage 2 runner passed all eight programs, including the 179 finite and 10 polynomial certificates, the retained special-case checks, the heavy-mode checks, new-results checks, and symbolic quotient checks. The three documented stage 1 commands also passed from the relocated copy.

I additionally wrote `verification/reviewer05/stage02-round01/independent_check.py` without importing the manuscript's implementation. Results are in `independent_check.log`:

- Exhaustive tests of the first-repeat reordering over all three-mode, four-slot half-integral simplex profiles and every eligible original word: **15,180** reorders preserve error at most one and the prefix multiset. These include **4,794** cases where the repeated mode has prefix allocation exactly one and **3,048** nonintegral selected deadlines. Original words were required only to satisfy the lemma's full-error assumption, not the stronger flow invariant.
- Independent **rational Fourier–Motzkin elimination** excludes an error-one schedule in **972 switching-time cells across all 27 three-block words** for the new three-mode example. This uses elimination rather than the author's polygon-vertex enumeration and includes repeated words, zero-length blocks, and shared cell boundaries.

These finite checks reinforce the proof audit but are not substitutes for the general analytic arguments.

## Limitations

This review does not constitute an independent reimplementation of the complete all-dimension certificate generator or checker. I checked the mathematical reduction and checker source and executed its exact verification; the additional independent programs target the reordering and new all-word counterexample. I did not conduct an external novelty search in this stage. The final abstract, expanded literature comparison, arbitrary-budget developments, later algorithms, and whole-manuscript review are intentionally deferred to their assigned stages.
