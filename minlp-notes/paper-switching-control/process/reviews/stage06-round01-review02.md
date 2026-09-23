# Stage 6, round 1 — independent review 02

## Verdict

**No major issue found. One minor correction is requested:** make the modulo operand explicit in the deterministic timing-input formula. The mathematical headlines, classical consequence, exact public computations, certificate scopes, and literature distinctions checked in this review are supported. The complete offline runner and a clean 56-page LaTeX build pass.

I reviewed the immutable `process/snapshots/stage06-round01` snapshot, without consulting other current reports, author/root assessments, or other reviewers. I did not edit the manuscript or snapshot and did not delegate. All generated files are under `verification/reviewer02/stage06-round01/`. Its `relocated/` directory was used for all runner and build outputs. All 161 snapshot hashes still match.

## Minor finding

**MINOR 1 — Ambiguous modulo operand in the reproducible input specification.**

Locator: `sections/12-computations.tex:163–165`, printed page 50, paragraph specifying the data for Table 6. The expression is currently

`1+((j+2)(i+3)+i^2\bmod 11)`.

This can be read as adding `(j+2)(i+3)` to the residue of `i^2`, whereas `verification/stage06/experiments.py` reduces the entire sum modulo 11. For example, at `j=2,i=0`, the implementation's weight is 2, while the narrower modulo interpretation gives 13. This is a notation and reproducibility ambiguity; the checked implementation and archived numbers agree.

Suggested fix: write `1+\bigl(((j+2)(i+3)+i^2)\bmod 11\bigr)`, or define `w_{ji}=1+r_{ji}` with `r_{ji}` the least nonnegative residue of `(j+2)(i+3)+i^2` modulo 11. No numerical result needs changing.

## Mathematical and integration findings with no correction required

- **Preservation of accepted mathematics.** I compared every pre-existing section against `stage05-accepted`. All files except `07-predecessors-and-frontier.tex` are byte-identical. In that file, the only mathematical addition is the disclosed classical bound; its higher-reach section is moved verbatim to `14-higher-reach.tex`. Thus the move does not change hypotheses, proof text, certificate claims, or unresolved questions.
- **Headlines and scopes.** `main.tex` and `00-introduction.tex:26–137` correctly limit the exact continuous formula to `0<=s<=3`, `n>=s+2`. The geometric term is identified as the one-sided uniform term, rather than automatically as the full uniform error in every range. Exact rational comparison confirms the transition mode counts 5, 8, and 12 for one, two, and three switches. The uniform input on `s+2` modes supplies the plateau witness. The asymptotic formula is for fixed block count, and the stated first correction matches the accepted general-budget result. The introduction correctly distinguishes `F_{3,2}=T/5`, the unresolved interval for `F_{3,3}`, instance errors, grid optima, and minimax values.
- **New classical consequence.** `07-predecessors-and-frontier.tex:108–120` follows directly by applying the cited unrestricted-grid bound to `k` equal cells and then using endpoint preservation under cell averaging. Every schedule on those cells uses at most `k-1` switches. I independently checked [Zeile–Robuschi–Sager, Corollary 1](https://link.springer.com/article/10.1007/s10107-020-01533-x): the inequality applies without the extra grid-length condition; that condition belongs to sharpness. The manuscript preserves this distinction. Algebraically, its coefficient improves `T/(k+1)` exactly when `k>2n-3`, consistent with the stated eventual improvement for fixed small `n`.
- **Exact continuous comparison.** `12-computations.tex:102–122` gives a complete direct proof of the uniform three-mode/two-switch instance value `1/6`. A schedule omitting a mode has error at least `1/3`; otherwise its three positive blocks use distinct modes. The last mode's start and terminal errors imply `E>=max(v/3,2/3-v)>=1/6`; the stated times `1/4,1/2` attain it. This does not improperly invoke the earlier theorem requiring a spare mode.
- **Public input and quantization.** `12-computations.tex:13–49` accurately separates raw decimal columns, normalized simplex rates, and the quantized input actually optimized. Largest-remainder rounding, tie breaking, and the denominator are specified. The claimed normalization, rate-quantization, and cumulative-quantization bounds hold on independently reconstructed data. The perturbation statement compares against the normalized source, not invalid raw simplex data.
- **Continuous public optimum.** The all-pair crossing argument is valid because one term is nondecreasing and the other strictly decreasing; the omitted mass is constant. All pair domains include both endpoint schedules, so constants cannot improve the global minimum. Independent piecewise-linear minimization confirms `4721469/2500000`, the mode-two-to-mode-three order, and the same exact switch time. The fine-grid gap `1031/2500000` is correct and smaller than half the original cell width.
- **Same-grid and nested-grid claims.** Every public-table row holds the switching grid fixed while comparing budgets. The 12-, 24-, and 48-cell grids are nested inside the original 12,000-cell grid. Consequently the displayed coarse upper bounds are feasible for both continuous and original-grid optimization. The interval endpoints, clipping, and strictness in Table 5 match the general certificate. The normalized-source enlargement by one cumulative tolerance on each side is correct. The nonnested uniform-grid example correctly illustrates that coarse optima need not decrease when the cell count increases.
- **Timings and figures.** Timings use matched inputs, grids, objectives, and budgets. The code excludes input construction and subsequent verification from the timer and includes solver validation. Every archived median is the middle of its three corresponding samples. The text does not infer asymptotic complexity from those observations or claim superiority over untested CIA solvers. I inspected both plotting routines and their mathematical/data sources; the figures use only the stated mode and grid cases, and their captions correctly treat connecting lines as visual aids.
- **Discussion and coverage.** The new discussion and appendix distinguish complete results from the general five-block reach problem, the unresolved three-mode/three-switch value, and constrained-transfer extensions. They do not promote a nonphysical event witness or a single chronological chamber into a general theorem. I checked the allowed coverage map against the repository inventory and the cited manuscript labels; it distinguishes subsumed historical results, retained input-specific predecessors, completed extensions, and remaining research directions.

## Independent computations

The new `verification/reviewer02/stage06-round01/independent.py` does not import the author's optimization or data-transformation functions. `independent.log` records its results, and `independent-results.json` preserves all six exact continuous pair minima and the exhaustive public-grid results.

1. Downloaded the pinned CSV into `public.csv` and independently verified its required SHA-256 digest. Parsed every decimal as a rational, checked the 12,001 timestamps and 12,000 widths, normalized rates, and reconstructed largest-remainder quantization with independent selection logic.
2. Recomputed all three exact perturbation maxima and matched the archived values. Verified every derived integrated mass on all three coarse public grids.
3. Enumerated every fine-grid ordered pair, including constants and endpoint choices, and evaluated component service directly at the switch and terminal endpoints. The optimum is exactly `1889/1000`, with zero-based modes `(1,2)` and switch index 1889.
4. Independently minimized each continuous ordered pair by inspecting **all input-cell endpoints and all pairwise intersections of the three affine objective pieces**, rather than using the author's crossing locator. All six exact pair minima match; the global minimum is `4721469/2500000`.
5. Exhaustively enumerated labeled words and boundaries for **all 12 public coarse-grid/budget cases**, including the 48-cell cases that the author's archived experiments certify through the subset solver. The 48-cell/three-switch check alone covers **1,313,415** labeled-word/boundary cases and returns exactly `10526709/20000000`. All other values and certificate endpoints match.
6. Independently enumerated the uniform three-mode/two-switch comparison on all nine reported grids, using scaled integer occupations and direct endpoint service. Every plotted coarse value matches.
7. Checked the exact geometric/plateau transition counts, the classical-bound crossover condition, and all archived timing medians.

The independent enumeration allows repeated adjacent labels and shorter physical schedules, so it checks at-most budgets rather than only schedules with the maximum number of actual switches.

## Portable verification and source audit

In the relocated copy, I ran the complete offline `verification/run_all.py` suite. Every proof, integrity, exact algorithm, derived-experiment, and generated-table check passed. I then cleaned the LaTeX outputs with `latexmk -C` and rebuilt with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`; the result is 56 pages, with no LaTeX/natbib warnings or overfull/underfull box diagnostics. Logs are retained as `relocated/reviewer-offline.log`, `reviewer-clean.log`, and `reviewer-build.log`.

I read the new experiment, rendering, and offline-check code, both relevant READMEs, the bibliography, and the stage source record. I inspected the supplied introduction/computation page renders and fresh page-50/51 renders from my clean build. No clipping or materially misleading graphical presentation was found.

For new attribution claims, I checked the local primary texts for Sager–Jung–Kirches's switch-constrained decomposition and branch-and-bound formulation; Knuth's integral-flow treatment of two-order rounding; the cited SUR, compactness, and adaptive-refinement papers; and the state-error discussion in Zeile–Weber–Sager. The primary [Abbasi-Esfeden et al. publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0959152425001507) confirms the introduction's precise statement about lost optimal substructure and the absence of a general global-optimality guarantee. The manuscript's claims stay within those inspected scopes.

## Limitations

This stage review assesses final authoring and integration, with the accepted mathematics checked for preservation rather than re-proving all earlier universal theorems. The separate whole-manuscript proof review remains necessary under the requested workflow. The source audit is targeted, not an exhaustive priority search. I did not attempt to reproduce elapsed-time constants on a shared host, and I did not audit the inaccessible full Abbasi-Esfeden et al. article beyond the primary preview needed for the actual citation claim. The pinned fine-source values were independently reproduced; this is stronger numerical evidence than merely validating the archived summaries, but it does not establish any nonlinear trajectory or economic-objective guarantee.

**Major-issue verdict: none found. Required minor correction: explicit modulo grouping in the deterministic input formula.**
