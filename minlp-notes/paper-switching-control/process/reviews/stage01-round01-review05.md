# Stage 1, round 1: independent review 05

Verdict: accept after two minor clarifications. No major issue found.

## Scope and independence

I read the complete frozen manuscript in `process/snapshots/stage01-round01`: `main.tex`, `macros.tex`, both section files, `references.bib`, and the eight-page PDF. I also read the snapshot README, process description, and boundary-check program to understand the intended stage. I did not consult other reviewers or previous approval reports. Later-stage results, the final introduction, and the final expanded abstract are outside this review.

The mathematics in this stage is sufficiently developed for an optimization/control reader. In particular, the distinction between an instance optimum and a minimax value is explicit, the measurable-control arguments do not assume piecewise-constant inputs, and the uniform-input lower bound applies to competing schedules with repeated modes.

## Findings

### R05-1 — Minor: explicitly specify the budget domains

Locator: `sections/01-foundations.tex`, lines 35–46, before the definition of `\Wcal_{n,k}(T)`; also the unrestricted attainment statement in Proposition 1.2.

The horizon and mode count receive explicit domains, but the activation-block budget `k` and switch budget `s` do not. The intended domains can be inferred from counting language, yet the subsequent parameterization and attainment proposition require an integer `k >= 1`; `k=0` would give an empty schedule class for `T>0`. State once that switch budgets are nonnegative integers and block budgets are positive integers, with `k=s+1` when comparing them. This closes a quantifier omission without changing any mathematical result.

### R05-2 — Minor: keep the construction's normalization explicit outside its proof

Locator: `sections/02-uniform-one-switch.tex`, lines 213–219, the implementation paragraph immediately after Theorem 2.4.

The theorem is stated for arbitrary `T`, whereas `E`, `t_q`, and `t_r` in this paragraph were introduced locally in the proof after setting `T=1`. The paragraph gives operational instructions using those symbols without saying that the reader must first normalize the horizon. This is recoverable from the scaling section, but it is an avoidable ambiguity for someone implementing the promised construction on a physical horizon. Either begin the paragraph with “On the normalized horizon `T=1`” and explain rescaling the returned time, or give `E=H_n(T)`, `t_q=T-m_q-E`, and `t_r=T-m_r-E` for the general-horizon implementation. No change to the proof is needed.

## Mathematical checks

I independently checked the cumulative-allocation converse, compactness and attainment, endpoint monotonicity, cell-average preservation of grid errors, minimax domination, scaling, and the no-switch value. The compact parameterization correctly permits zero-length intervals and consecutive equal labels.

For Theorem 2.1 I rederived the recurrence from the active mode's cumulative occupation, including prior occurrences of that mode. The distinct-mode construction has negative extrema exactly `-E_0` and positive discrepancies at most `T/n`. For Theorem 2.2 I checked necessity, truncation at the horizon, strict increase of accepted integer iterates, the ceiling/floor identity in the gap proof, and the edge cases `s=0`, `n=2`, and budgets exceeding the number of grid boundaries within the theorem's stated mode range.

I checked all endpoint extrema in Lemma 2.3, including the empty omitted-mode maximum and switches at 0 or `T`. I rederived the contradiction inequality in Theorem 2.4 and its terminal-mass estimate. The large-mass case, equality at `E=1/3`, strict inequalities in the contradiction, ties, and omitted zero-mass modes are handled correctly. The extremizers and the threshold between four and five modes match the formula. Moving a single switch to a nearest grid point proves Corollary 2.5 without creating an additional switch. The three-cell upper proof and both conjecture counterexamples are correct.

I wrote a separate exact-rational verification program without importing the author's implementation. Its results are saved in `verification/reviewer05/stage01-round01/independent_check.log`:

- Exhaustive enumeration of every unit-grid word, including repeated labels, for `2 <= n <= 6`, `1 <= N <= 6`, and every `0 <= s <= n-2`: the recurrence and strict grid-gap inequality agree in all 90 parameter triples.
- Direct evaluation on the union of input knots and switch times for 800 rational piecewise-constant profiles with `2 <= n <= 9`: all tested three-term identities hold, including endpoint switches. The independent implementation of the constructive bound succeeds on all tested profiles with `n >= 3`.

These checks supplement the analytic verification; finite checks alone would not establish the measurable-input theorems.

## Sources and presentation

I checked the local Sager–Zeile primary PDF, using a fresh text extraction, at Conjecture 1 / equation (7.6) and Definition 10. The conjecture's two branches, parameter restrictions, and free-initial-activation interpretation match the manuscript. The examples lie in the admissible source range and disprove an upper bound, so they do not depend on a stronger interpretation of the source's equality. I did not independently fetch the final published PDF or conduct a novelty search in this review.

I built the frozen source both with its supplied bibliography output and from a clean copied source tree without a `.bbl`. The fresh BibTeX build succeeds. The final LaTeX log has no warnings, unresolved references, overfull boxes, or underfull boxes. I rendered and visually inspected all eight PDF pages: equations, theorem labels, bibliography, margins, and page breaks are readable; there is no severe layout issue. All generated artifacts are confined to `verification/reviewer05/stage01-round01/`.

## Limitations

This is a review of stage 1 only. It does not verify later certificates, later algorithms, a complete literature-positioning claim, or the eventual whole-paper consistency. The two findings above concern explicit domains and implementable notation, not a gap in any central proof. A new five-reviewer round is not mathematically required by this review once those minor clarifications are made.
