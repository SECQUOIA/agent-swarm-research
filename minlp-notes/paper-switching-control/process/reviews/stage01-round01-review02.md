# Stage 1, round 1: independent review 02

## Verdict

No major issue found. The mathematical results in the frozen stage are supported by complete analytic arguments, and independent exact checks passed. Two minor scope/definition clarifications should be made before acceptance. Neither requires changing a theorem or proof.

## Scope and independence

Reviewed the complete frozen draft in `process/snapshots/stage01-round01`: `main.tex`, `macros.tex`, both section files, `references.bib`, `main.bbl`, all eight pages of `main.pdf`, and the accompanying README, process instructions, manifest, and supplied source-conjecture image. All 13 manifest hashes match. I inspected the local Sager–Zeile primary-source transcription, including Definition 10, and visually checked the actual displayed conjecture on manuscript page 27 against the paper's transcription. I did not consult other reviewers or edit manuscript files.

All mathematical judgments below come from the frozen proofs and independent derivations. Historical approval and the author's successful test reports were not treated as evidence of correctness. The stage's deliberate deferral of later mathematical sections is not a finding.

## Findings

### Minor R02-01: State the integer domains once in the definitions

**Locators:** `sections/01-foundations.tex:35–48`, `:64–76`, and `:80–82`.

The mode count is expressly an integer, but the switch budget, activation-block count, and grid cell count are introduced without their domains. Their intended meanings are inferable; nevertheless, the attainment proposition and the schedule parameterization implicitly require `s` to be a nonnegative integer, `k` a positive integer, and `N` a positive integer. In particular, `k=0` would produce an empty schedule class for positive horizon and invalidate an unqualified attainment statement.

**Correction:** Add the conventions `s in Z_{≥0}`, `k=s+1 in Z_{≥1}` (or allow independent positive integer `k`), and `N≥1` when these indices are introduced. No new theorem is needed.

### Minor R02-02: Qualify the one-switch result in the overview

**Locators:** `main.tex:23–25`; `sections/02-uniform-one-switch.tex:3–6`.

These overview sentences announce the full continuous one-switch minimax without mentioning the mode range, while the ambient problem permits `n=2` and Theorem 2.4 proves the formula only for `n≥3`. The theorem itself is correctly scoped and the proof never illicitly applies it to two modes. The summary should carry the same restriction so readers do not infer coverage of every admitted mode count.

**Correction:** Add “for at least three modes” to the announced one-switch minimax result. This is a summary-precision issue, not a request to develop an unplanned two-mode theorem in this stage.

## Mathematical audit

- **Schedule class and attainment:** The representation permits zero blocks and repeated words; deleting zero intervals and merging adjacent equal modes give precisely an at-most switch constraint. The telescoping occupation representation is valid even at coincident switching times, and its uniform Lipschitz estimate has coefficient one per boundary. The finite union of compact time-simplex images is compact. The cumulative-input converse and Arzelà–Ascoli argument handle measurable controls. Infimum over schedules preserves the stated Lipschitz estimate, supporting the outer maximum.
- **Endpoint and grid arguments:** The endpoint lemma follows from absolute continuity and derivative signs even if a coordinate is flat. Averaging preserves every competing grid schedule's full and one-sided errors. The supremum comparison correctly applies averaging to an arbitrary continuous input before taking the supremum; there is no interchange of incompatible adversarial classes.
- **No-switch boundary:** The identity `D=T-m_p` uses only terminal masses and remains correct for zero masses, pure inputs, `n=2`, and a one-cell grid.
- **Continuous uniform formula:** The lower recurrence uses an inequality valid for repeated modes; its proof does not silently restrict competitors to distinct words. The omitted-mode bound is used only with `k<n`. The geometric distinct-mode construction has endpoint negative error exactly `E_0`, and its positive errors are bounded by `T/n`. For `s=0`, it reduces to the no-switch baseline; at `n=2` the theorem only includes that budget.
- **Uniform-grid recurrence:** Necessity survives fewer positive blocks because the iterates are nondecreasing. Sufficiency correctly excludes the zero fixed point before claiming strict growth. For `N=1`, even if the nominal budget exceeds available boundaries, truncation yields one positive block. The ceiling identity proves the strict additive inequality, including `n=2`; no unjustified strictness is introduced by rounding.
- **Three-term formula:** Endpoint comparisons retain the positive error of the first mode and the preactivation error of the last mode. The omitted-mass convention is legitimate for `n=2`. At `tau=0` or `T`, zero-length activation introduces no extra switch and the formula equals the constant-schedule error.
- **One-switch upper bound:** The heavy-mass case includes equality `m_q=E`, and there cannot be two additional masses strictly above `E`. The remaining-case contradiction uses strictly failing candidate errors and weak cumulative monotonicity, so flat allocations and ties do not create a logical gap. The second-largest-mass lower estimate has the correct direction, and the positive coefficient used afterward holds for all `n≥3`. The construction uses at most two cumulative-vector evaluations.
- **Matching lower bounds and grid transfer:** The three equal pure blocks force an omitted positive-mass mode for every permitted schedule, including constants. Uniform extremizers provide the higher-mode branch. Moving one switch to a nearest boundary changes cumulative occupations by at most the displacement and creates no new switch. Leading-coefficient sharpness uses legitimate inputs and refining grids.
- **Three-cell minimax:** Choosing the largest and second-largest terminal masses makes every omitted mass at most one and the second-largest mass at most `3/2`. Checking the two occupied coordinates at each prefix justifies the stated upper bound. Uniform input forces an occupation of at least two cells even when the budget is unused.
- **Source corrections:** The conjecture image gives the same branches and restrictions as the manuscript. Definition 10 begins counting switches at interval 2, consistent with free initial activation. Both explicit witnesses satisfy the restrictions. The asymptotic fixed-budget obstruction is justified by choosing the mode count first and grid refinement afterward. It makes no claim about all second-branch cases.

## Independent computations and artifacts

`verification/reviewer02/stage01-round01/independent_checks.py` imports no repository verification module and uses exact rational arithmetic. Its log records:

- 17,104 complete grid schedule words, including repeated modes, checking 85 combinations of `n`, `N`, and admissible `s` against the recurrence and strict gap. Ranges: `2≤n≤6`, `1≤N≤6` for `n≤5`, and `1≤N≤5` for `n=6`.
- 733 rational profiles, including all two-cell simplex-half profiles for `2≤n≤5`, deterministic sparse random profiles through `n=8`, uniform profiles, and pure three-block examples.
- 58,672 comparisons of the three-term formula with direct discrepancy evaluation at every cell endpoint and the switch time, including `tau=0,T` and `n=2`.
- 673 one-switch constructions checked against the bound and an independently computed continuous instance optimum. The latter minimizes over all ordered mode pairs by solving the unique piecewise-linear crossing of `t-A_p(t)` and `T-m_q-t`, then evaluates the original full discrepancy.

All passed. Rendered PDF pages are stored in the same reviewer verification directory; no clipping, broken references, or unreadable displayed equations were observed. The source-conjecture image also matches its transcription.

## Limitations

Finite arithmetic checks supplement the analytic proofs and do not establish the all-measurable-input quantifier. I audited the supplied local primary-source manuscript and its displayed conjecture, but did not perform a new web search or a separate comparison with the publisher's final PDF. Later-stage claims, performance claims, and journal-level completeness of the future assembled paper remain outside this stage review. No evidence of an additional mathematical error emerged from the present audit.
