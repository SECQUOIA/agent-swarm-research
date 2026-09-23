# Stage 1, round 1: independent review 04

Verdict: **no major issue found; accept this stage after two minor wording corrections.** I found no incorrect theorem, missing proof step that changes a result, or mismatch with the cited published conjecture. Future sections were not treated as missing material.

## Scope and evidence

I read both frozen section files in full, together with `main.tex`, `macros.tex`, `references.bib`, `main.bbl`, `README.md`, `PROCESS.md`, the snapshot manifest, and both verification Python files. I inspected the two frozen images, extracted and checked the eight-page frozen PDF, and verified all 13 manifest hashes. All manuscript locators below refer to `paper-switching-control/process/snapshots/stage01-round01/`.

I read `literature/AGENTS.md` before consulting the local Sager–Zeile package, including its extracted text and original-PDF conjecture image. I also checked the actual published [Springer article](https://link.springer.com/article/10.1007/s10589-020-00244-5), accessed 2026-09-07. Its Conjecture 1 and equation (7.6) have exactly the two branches and restrictions reproduced here. Definition 10 counts changes starting with cell 2. Definitions 5 and 7 supply the unrestricted cell-simplex input and prefix-error CIA problem; Definition 8, equation (4.1), confirms the free initial activation. The bibliography's 2021 issue year, volume 78, pages 575–623, and DOI match the publisher; the online publication date is in 2020. The local 32-page author manuscript's page numbering need not be confused with journal pagination. The paper uses stable theorem/equation locators, so this does not create a citation problem.

## Findings

### R04-01 — Minor: abstract overstates the mode range of the one-switch result

Locator: `main.tex`, abstract, sentence beginning “We establish exact uniform-input formulas and the full continuous one-switch minimax value.” The model introduced immediately afterward allows `n >= 2`, whereas Theorem 2.4 explicitly covers `n >= 3`. “Full” can therefore imply the binary case has also been established in this draft. This is a scope wording issue, not an objection to the theorem or a demand for a later-stage proof.

Suggested correction: say “the continuous one-switch minimax value for at least three modes.” Alternatively explicitly identify “full-error” as the intended meaning and retain the mode qualification. The final abstract can be updated again when later results are incorporated.

### R04-02 — Minor: make the post-proof construction's normalization explicit

Locator: `sections/02-uniform-one-switch.tex:213–219`, the paragraph beginning “The construction requires no search over switching times.” It reuses `E`, `t_q`, and `t_r`, which were introduced only inside the preceding proof after setting `T = 1`. For a reader implementing the construction on the original horizon, the paragraph should say it continues under this normalization or should restore `E = H_n(T)` and `t_i = T - m_i - E` in the small-mass case. The proof already provides the required scaling argument; no new mathematics is necessary.

## Mathematical checks

- **Foundations.** The cumulative characterization follows from absolute continuity and differentiation almost everywhere. The fixed-word time-simplex representation remains valid with zero-duration blocks and repeated labels, and its displayed Lipschitz estimate is correct. Compactness, continuity of the two objective functions, minimizer attainment, and maximizer attainment follow as stated. For grids, averaging preserves every endpoint objective, which genuinely supplies the missing comparison between the two different minimax input classes. The no-switch formula and scaling claims are correct.
- **Uniform continuous input.** The lower bound's block-end estimate uses total previous occupation only through a lower bound, so it remains valid when modes repeat. A mode is omitted because `k < n`. The geometric distinct-mode construction attains both components of the displayed maximum. The fixed-budget large-mode limit is an instance obstruction and is correctly not claimed as an independently proved minimax formula.
- **Uniform grid.** The integer recurrence is both necessary and sufficient. Truncation at the horizon and the proof of positive progress handle short grids and zero-length padding. The floor/ceiling identity used for the strict additive gap holds, including `n = 2`, and `ceil(n E) + n - 2` supplies the claimed strict inequality.
- **Three-term identity.** Endpoint monotonicity gives all potentially active extrema. The two discarded positive errors are bounded by the two retained terms using the simplex mass identity. A nonpositive last term causes no problem. The empty omitted maximum in the binary case and constant schedules at the endpoint times are correctly covered.
- **One-switch minimax.** The large-mass case includes equality and the possibility of one additional heavy mode. In the small-mass case the candidate failure inequalities sum to the displayed strict contradiction; the second-largest-mass inequality has the correct direction and coefficient. Candidate selection needs only the claimed two cumulative evaluations, with integration treated separately. Three equal pure blocks establish the omission obstruction even if a competitor selects an otherwise unused mode; uniform input establishes the other obstruction. The crossover at five modes is correct.
- **Grid corollary.** A single switch moved to a nearest grid point changes the cumulative occupation by at most its displacement, with no new switch. The stated leading coefficient's sharpness concerns refinement, not finite-grid equality; the proof maintains that distinction.
- **Three cells and counterexamples.** Choosing the two largest masses makes every omitted mass at most one. The endpoint estimates prove the three-cell upper bound, and uniform input attains it. I checked the numerical witnesses `16 > 31/2` and `11/7 > 3/2`, the free initial activation, the condition `1 <= s <= N - 2`, and fixed-horizon refinement. The concluding obstruction for each fixed positive switch budget follows by choosing sufficiently many modes and then sufficiently fine grids. Nothing here asserts a result about all cases of the second conjectured branch.

## Independent computational verification

I wrote a fresh exact-arithmetic checker, without importing the repository's certificate implementations:

`paper-switching-control/verification/reviewer04/stage01-round01/independent_checks.py`

Its saved log is `independent-checks.log` in the same directory. All checks passed:

- 13 snapshot file hashes.
- 60 parameter cases with `2 <= n <= 5`, `1 <= N <= 6`, and every allowed `1 <= k < n`: exhaustive enumeration of cell words, including repeated modes, agrees with the integer recurrence and its strict additive gap.
- 96 reproducibly generated rational four-cell inputs with `3 <= n <= 10`: exact optimization over every ordered mode pair, solving its continuous crossing time, satisfies the one-switch upper bound. Errors were also evaluated directly at all input breakpoints and the switch to check the three-term identity.
- 16 uniform or equal-pure-block profiles: independently optimized continuous errors agree with the claimed sharpness values.

The frozen PDF text has resolved theorem and citation references; the inspected first-page rendering is legible.

## Limitations

The finite computations supplement the analytic proof review; they do not establish claims over all measurable controls. I did not perform a global novelty search and do not certify priority; the current text makes no unsupported “first” claim. I did not audit the entirety of the cited paper beyond the definitions, source claims, and context needed here. I did not rerun the draft author's verification scripts against mutable external dependencies because the independent checker supplies separate evidence for this stage. No manuscript or literature files were edited.
