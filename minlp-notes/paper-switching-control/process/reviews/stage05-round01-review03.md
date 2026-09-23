# Independent review 03: stage 5, round 1

**Verdict: no major issues and no valid minor issues identified.** The new results are supported by the printed proofs within their stated assumptions. I recommend accepting this stage. This is an independent review, not reliance on historical approvals or on other current reviews.

## Scope and integrity

I reviewed the frozen `stage05-round01` snapshot, especially all of `sections/10-instance-algorithms.tex` and `sections/11-transfer-and-coarsening.tex` (printed Sections 13–14, pp.40–48), their endpoint/compactness/one-switch dependencies, the complete new continuous enumerator and coarsener, their checks and documentation, the bundled reference optimizer and relevant historical checkers, and the source record and bibliography. I did not inspect other current review reports or author/root assessments. I made no manuscript or snapshot edits.

All 122 snapshot-manifest hashes matched before the independent checks and again after the review. The relocated standard-library runner independently verified all 30 bundled original-artifact hashes. Log-producing checks and the LaTeX build ran only in my own relocated copy.

## Mathematical and algorithmic assessment

### Exact grid algorithms: Section 13.1–13.3

- **Theorem 13.1:** The ordered-pair dominance argument is correct. Replacing the final label by a largest-total label outside the initial mode weakens both the terminal-active and omitted-mode terms. This leaves the two leader starts and the best initial cumulative mass outside the leaders. Constants, a prescribed initial label, and restricted internal boundaries are handled correctly. I independently checked the strict increase of `2t-A_p(t)-T+m_q`; the neighboring-boundary search follows without a smoothness assumption. Its quoted query complexity explicitly excludes reading/preprocessing the full input and sorting eligible boundaries.
- **Lemma 13.2:** The completion formula remains correct with negative residuals. At the start of the final block all already-incurred endpoint errors are bounded by `E0`; during that block only the final negative excursion of the selected mode and final positive excursions of the other modes can add error. The largest eligible residual exchange therefore applies even if some residuals are negative. The text correctly limits this result to completion of a fixed prefix.
- **Proposition 13.3 and Theorem 13.4:** The component cost includes all nominal block endpoints and the nonzero cost of an unused mode. A mode may receive disconnected subsets. The min/max subset recurrence represents exactly all assignments and has the stated `3^k` transition count. Padding a shorter grid schedule by subdividing runs proves completeness of enumeration with exactly `min(s+1,N)` nominal blocks. It does not spend extra actual switches. The arithmetic/storage bounds and the fixed-budget bit-complexity qualification are consistent with this construction.
- **Dwell constraints:** Checking maximal consecutive strings of a mode's assigned block subset implements physical runs, including initial and terminal runs. It preserves subdivision invariance. Separate visits cannot pool their dwell durations. The manuscript correctly excludes arbitrary transition graphs from this separability argument.
- **Lemma 13.5:** The exchange proof accounts for both the newly omitted mass and the cost of the replacement role. An unused candidate exists among the `d` cheapest labels because only `d-1` other roles are occupied. Ties and `n=d` cause no exception. No broader constrained-assignment claim is made.

### Exact continuous enumeration: Section 13.4

The LP objective and signs agree with the original integrated-discrepancy objective. Between schedule switches the active component discrepancy is nonincreasing and the others are nondecreasing, including across input breakpoints; consequently schedule endpoints suffice. For the one-sided objective the retained inequality is correctly `W-A <= E`.

The `n^k binom(N+k-2,k-1)` enumeration includes all words and nondecreasing time-cell assignments, with `k=s+1` even when `k>N`. Closed cells, repeated labels and zero blocks cover input-boundary switches and schedules with fewer switches. Boundedness of switch times and `0<=E<=T` makes the active-set enumeration complete. A vertex of a lower-dimensional bounded polytope still has `k` independent active inequality normals in the ambient `k` variables; the proof does not incorrectly assume full dimensionality. Rational elimination/determinant bounds justify the stated fixed-`k` bit complexity.

I independently reconstructed the instance LPs using **block durations** with a separate sum-of-durations equality, rather than copying the author's switch-time rows. The independent numerical minima agreed with exact outputs on all tested continuous instances. I also evaluated the exact returned rational schedules directly on the common set of original-input and schedule breakpoints. These tests separately exercise full and one-sided objectives, repeated modes, input-boundary switches, zero-error degenerate instances, and a one-cell input with a budget exceeding the input cell count.

### Transfer and sharpness: Section 14.1

- **Theorem 14.1:** The fractional occupations provide a feasible flow with integer prefix lower/upper bounds; integral feasible flow yields one positively supported label per cell. Floor/ceiling bounds imply strict discrepancy below one cell width, including exact integer prefixes. Cell monotonicity extends the endpoint estimate to all times. Positive support gives strictly increasing representative times in the original schedule; their original block indices are nondecreasing, so removing repeated selections and merging labels gives a subsequence and cannot increase the switch count. The explicit-grid polynomial bit bound is appropriate.
- **Corollary 14.2:** The strict instance bound uses attainment of the continuous optimum. The strict minimax bound separately uses an attained grid maximizer and exact cell averaging for the input-class comparison. It does not make the invalid general inference that a supremum preserves a pointwise strict inequality.
- **Proposition 14.3:** The binary greedy invariant works for unequal cell lengths. When both labels have positive occupation, the two possible new discrepancies are separated by at most the maximum width and bracket the permitted interval in the required sense. Positive-support chronology gives the switch count. The one-cell equal-occupation example establishes sharpness for a supplied schedule, as stated.
- **Proposition 14.4 and its following paragraph:** The first-cell lower bound and the all-final-mode matching grid schedule give the exact grid optimum. Direct rational integration confirms the stated continuous competitors and the instance-gap lower bounds. Exactness of the continuous competitor is neither needed nor claimed. The four-mode/five-cell/three-switch example satisfies `1<=s<=N-2` and gives a gap at least `9/16`, exceeding one half. The limit argument establishes the universal coefficient across varying mode counts and budgets; it is not presented as a fixed-mode sharpness theorem.

### Coarsening and dwell: Section 14.2

- **Theorem 14.5:** Exact coarse cumulative values suffice to compute the error of the coarse schedule against the original input because of endpoint monotonicity. This is distinct from claiming reconstruction of arbitrary within-cell input behavior. The code explicitly assumes constant rates within its supplied input cells, and its documentation makes this restriction clear. Common-refinement integration and the fixed-budget complexity bound agree. Choosing `M=ceil(1/epsilon)` gives strictly smaller than `epsilon*T` suboptimality.
- The one-switch and binary half-width refinements are correctly nonstrict, while zero-switch optimization is exact. The general strict certificate remains correct. Lower-bound clipping correctly distinguishes a negative raw lower endpoint from a raw endpoint equal to zero.
- The fine-grid bracket requires nesting (or actual allowed switch boundaries); the text correctly limits the nonnested guarantee to continuous feasibility. It does not claim that dwell-constrained coarse optima enjoy this unrestricted transfer certificate.
- **Example 14.6:** On an odd uniform grid, two runs each of length at least one half cannot occur because their only possible switching time is one half. Constants therefore have exact optimum one half at every odd resolution, whereas the continuous schedule has zero error. This is a valid persistent obstruction, not merely a coarse-grid accident.
- **Corollary 14.7:** Applying the cumulative-input Lipschitz estimate to both the optimum and the returned schedule gives the stated lower/upper bounds and width `h+2 delta`. It correctly certifies the original input separately from exact optimization of its rational approximation.

## Independent tests actually performed

Own reproducible scripts and JSON summaries are under `verification/reviewer03/stage05-round01/`.

1. `grid_transfer.py` uses a direct integrated-error oracle and explicit grid-word enumeration, independently of the tested recurrence/evaluator. It passed:
   - 440 fixed-budget/dwell comparisons on rational nonuniform inputs;
   - 210 one-switch comparisons with restricted boundaries and prescribed initial labels;
   - 380 arbitrary-prefix completion comparisons, including 69 prefixes with negative residuals;
   - 36 exhaustive abstract role-assignment comparisons for the candidate-set lemma;
   - 60 uniform transfer inputs, enumerating 229 supported prefix-rounded words and checking their original-input discrepancy and switch count;
   - 45 binary nonuniform transfer cases with direct support-constrained enumeration.
2. `continuous_coarse.py` reconstructed 894 continuous LPs in block-length variables in total. It compared eight exact continuous benchmark results, tested 24 additional nonaligned coarse instances against every budget-feasible coarse word and the original input, and corroborated applicable certificate intervals with the independent continuous LPs. Among the coarse cases, 22 lower endpoints were clipped and two were strict. It also directly checked the sharpness family for `n=2,...,8` and six odd-grid dwell obstructions. The separate numerical LP comparison is corroboration, not an exact lower-bound certificate; direct schedule evaluation used rational arithmetic.
3. The relocated `verification/stage05/run_checks.py` completed successfully, including all four historical checkers and `check_new_results.py`. Its summary records, among other tests, 3,836 switch-budget comparisons, 3,139 prescribed partitions, 608 dwell comparisons, 8,819 exhaustive original transfer controls, 22,065 supported witnesses, and nine rational continuous benchmark cases. These are bundled-suite counts, distinct from my independent counts above.
4. A relocated `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` build completed with a 48-page PDF. The final `main.log` contains no undefined-reference/citation, overfull, underfull or other warning. I visually inspected the stage-5 contact sheets covering pp.40–48; equations and text are legible and not clipped.

## Primary-source check

I independently read the relevant portions of the available primary PDFs/text and checked all three recorded PDF hashes for Bestehorn–Kirches, Zeile's thesis, and Sager–Zeile. They match the source record. Bestehorn–Kirches Corollary 2.7 supplies the credited supported uniform-grid ingredient. The thesis Section 6.4.3/Remark 6.3 supplies the credited switching-time enumeration context. I also retrieved and read Section 1.1 and Remark 15 of the primary shortest-path paper, confirming the scoped attribution to existing exact DAG methods and constraint adaptations.

The paragraph immediately preceding Sager–Zeile Conjecture 1 and the corresponding paragraph before thesis Conjecture 7.1 do argue for a half-maximum-width instance correction by individual switch movement. The new text accurately characterizes this as the conjecture's motivating argument, rather than falsely labeling it a proved transfer theorem. Its counterexample genuinely addresses that instance claim. The bibliography's 2020 volume/2021 publication distinction for the PAMM article matches the source.

## Limitations

The finite tests do not prove the universal statements; the proof audit above is the basis for accepting those statements. The independent LP oracle uses numerical optimization, while the author benchmark and direct witness checks use exact rational arithmetic. I did not undertake a broad publication-priority search, repeat unchanged earlier-stage certificate suites, run optional application/performance benchmarks, or assess the intentionally pending final abstract/introduction/literature/experimental synthesis. No missing later-stage material is treated as a defect of this stage. I identified no required correction in the reviewed scope.
