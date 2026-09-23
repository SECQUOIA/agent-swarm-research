# Independent review 01 — stage01-round01

**Verdict: no major or minor findings.** The current stage is mathematically sound and sufficiently explained for the intended mathematical readership. This verdict concerns the frozen stage, not any subsequently edited working files.

## Scope and method

Read `main.tex`, `macros.tex`, `references.bib`, both complete section sources, and the extracted text of all eight PDF pages in `process/snapshots/stage01-round01`. Visually inspected the rendered proof page 6 and the cited source's conjecture page. Reconstructed the proofs directly; did not use historical approval records as evidence. The frozen boundary-check script was inspected for context, but the independent checks below import none of its implementation or other repository code.

## Mathematical checks

- **Section 1, lines 21–33 and Proposition 1.2:** The characterization of cumulative allocations is exact for measurable simplex controls. Uniform closure preserves every required condition, and absolute continuity supplies the converse. The schedule parameterization includes shorter schedules and repeated modes; the displayed telescoping occupation formula is correct, including coincident switch times. Its uniform Lipschitz estimate proves compactness. Taking minima of uniformly 1-Lipschitz error functions establishes stability and therefore minimax attainment. Grid inputs are a compact finite product. No differentiability beyond almost everywhere is implicitly required.
- **Lemma 1.1 and Section 1, lines 119–132:** Endpoint monotonicity follows from the signed derivative bounds, including for inputs that vary within grid cells. Averaging preserves every grid schedule's objective. The minimax comparison has the correct direction even though its input classes differ: the proof inserts the averaged input only after restricting the schedule class. This argument also applies to the one-sided criterion.
- **Proposition 1.3:** The terminal-mass calculation proves the no-switch formula for all stated mode counts, independently of the input's temporal order.
- **Theorem 2.1:** The lower recurrence uses only the current block's length, so repeated-mode competitors cannot invalidate it. The geometric schedule attains the recurrence lower bound on the negative discrepancy, while the positive discrepancy and omitted coordinates are bounded by `T/n`. The result covers `s=0`, `n=2`, and both branches of the maximum. The fixed-budget asymptotic expansion is valid on its stated domain.
- **Theorem 2.2:** Errors of grid schedules are integer multiples of `1/n`. The integer reach recurrence is necessary, and truncating its increasing iterates at `N` gives a valid distinct-mode schedule whenever it is sufficient. Small grids with more permitted blocks than cells cause no difficulty. The floor/ceiling identity and the strict additive-gap estimate are correct, including `n=2` and integral `nE`. The proposed search interval is nonempty and contains a feasible value.
- **Lemma 2.3:** Independently derived all active-mode and omitted-mode endpoint discrepancies. The apparently missing positive extrema are indeed dominated by the displayed terms. The formula remains valid for constant schedules at `tau=0,T` and for two modes with an empty omitted set.
- **Theorem 2.4:** In the first mass case, at most one additional coordinate can exceed the threshold, and the chosen switch time belongs to `[0,E]`. In the second case, failure of all candidate schedules gives the strict inequalities claimed. The second-largest-mass inequality and algebra yield exactly `(2n-1)E < (n-1)^2/n`, contradicting the threshold. Ties, zero masses, and equality at the threshold are assigned to valid branches. The two lower-bound inputs and the mode-count transition are correct. The `O(n)` construction requires only the two stated cumulative-vector evaluations apart from integration.
- **Corollary 2.5:** Rounding one switch to a nearest grid point changes both affected cumulative occupations by at most half the largest cell length and cannot add a switch. The extremizer sequences justify sharpness of the leading coefficient, without asserting sharpness of the grid correction.
- **Proposition 2.6 and Examples 2.7–2.8:** The three-cell upper bound uses the two largest terminal masses correctly; every omitted mass is at most one. The uniform lower bound applies to every admissible word, including constant ones. Both counterexample values and the fixed-horizon refinement rescaling check exactly. The final fixed-budget argument chooses the mode count and then the grid size in a valid order and remains in the conjecture's first branch.

## Independent executable checks

Created and ran `verification/reviewer01/stage01-round01/independent_checks.py`, using rational arithmetic and no repository implementation imports. It passed:

- Exhaustive evaluation of 45,010 admissible cell words, including repeated-mode and constant schedules, comparing 90 `(n,N,s)` cases for `2 <= n <= 6`, `1 <= N <= 6`, and all `0 <= s <= n-2` with the integer recurrence and both grid-gap inequalities.
- Direct endpoint evaluation versus the three-term formula for 5,280 cases from 1,760 rational profiles, with `2 <= n <= 12`, varying horizons, endpoint switches, and fractional interior switches.
- Independent implementation and direct verification of the one-switch construction for 1,600 rational profiles with `3 <= n <= 12`.

The continuous proofs, rather than these finite checks, establish the general claims.

## Source and presentation checks

Compared the quoted conjecture with the locally archived Sager–Zeile author manuscript, its full-text record, and its rendered page 27. The two branches, equality status, and restrictions `n>2`, `1<=s<=N-2` agree. Definition 10 starts counting switches on the second interval, agreeing with the manuscript's free initial activation. The citation does not promote the source conjecture to a theorem. The bibliography identity matches the repository's source record.

The extracted PDF contains all stage text with resolved theorem and bibliography references. The visually inspected theorem page is legible, with no displayed-equation clipping or collisions. I did not perform a pixel-level examination of every PDF page or independently rebuild LaTeX. I did not investigate global novelty, material assigned to future stages, or derive unstated higher-budget formulas.

## Required corrections

None identified in this frozen stage.
