# W5 report: computation group

Files changed: `sections/computation.tex`, `sections/appendix-computation.tex`
(new content; already input last by `appendix.tex`), `experiments/README.md`,
`experiments/chain/run_chain.py`, `experiments/recourse/run_recourse.py`
(output paths only). Files added: `experiments/scip_shortfall.py`,
`experiments/replay_s1_ex.py`, `experiments/results/E5_scip_shortfall.csv`,
`experiments/results/S1_ex_replay.csv`,
`experiments/results/dependencies_sha256.json`,
`process/w5/checks/computation-eigs.py`. `figures/` and `run_all.py` are
unchanged. Nothing outside the paper directory was touched.

## Pages (measured from builds)

| Build | Section 11 | Length |
| --- | --- | --- |
| Snapshot `sections-before-w5` (`/tmp/w5-computation-base`) | p. 71 (line 25 of 50) to p. 78 (line 40 of 49) | about 7.35 pages |
| After W5 (`/tmp/w5-computation`, with the other groups' current files) | p. 64 (line 42 of 52) to p. 69 (line 38 of 47) | about 5.0 pages |

Saving in the main text: about 2.35 pages. New Appendix H
(`app:computation`, "Additional computational results"): pp. 123-126, about
3.3 pages. The target of about 4.5 pages is not fully reached; moving
Table `tab:chain` (the only table left in Section 11) to Appendix H would
save about 0.25 page more. I kept it because the CUTPLAN does not list it and
the introduction advertises the chain result.

## Cut-plan items

| Item | Done | Change |
| --- | --- | --- |
| Fix SCIP paragraph and table caption (C-computation-1) | yes | see C-computation-1 below |
| Merge E3 into E2 | yes | one paragraph "E2 and E3: conditioning and dimension"; the separable-case formula moved to App. H |
| Merge 11.5 and 11.6 | yes | 11.4 "Exact output and localized acceptance"; S1 is a `\paragraph` carrying `\label{sec:comp-localized}` (resolves to 11.4) |
| Shorten 11.9 (now 11.8 Limits) | yes | 13 lines instead of 17; checker detail dropped |
| Create `appendix-computation.tex`, move E6 table, SCIP table, recourse table and detail, leaving one summary paragraph each | yes | 11.5, 11.6, 11.7 are each one summary paragraph with the key numbers |
| Further moves to approach 4.5 pages (within my files) | yes | the list (a)-(g) of implementation differences, the "further modules" sentence, the Lemma `lem:commonmesh` ratios, the growth-bracket method, the off-grid argument, the E4 stage groups, the E6 interval list and distributions, the E5V details now live in App. H; Section 11 keeps a summary of each |

Section order is now 11.1 implementation, 11.2 E1-E3, 11.3 chain, 11.4 E4 and
S1, 11.5 E5 (SCIP), 11.6 E6 (random), 11.7 recourse, 11.8 limits, so the
experiment names appear in order (see C-computation-7).

## Labels

No label deleted or renamed. Moved to `sections/appendix-computation.tex`:
`tab:scip`, `tab:random`, `tab:recourse`. New: `app:computation` (section H).
Renumbered by the reordering (references elsewhere resolve automatically):
`sec:comp-chain` 11.3, `sec:comp-exact` 11.4, `sec:comp-localized` 11.4,
`sec:comp-scip` 11.5, `sec:comp-random` 11.6, `sec:comp-recourse` 11.7,
`sec:comp-limits` 11.8. External references checked: `exact-localized.tex`
(lines 4 and 131: `sec:comp-exact`, "experiment S1 (Section
sec:comp-localized)"), `conclusion.tex` 28, `intro.tex` 158 and 383,
`growth.tex` 288 and 375, `grids.tex` 309; all still correct, and the
numbers they quote are unchanged in Section 11.

## Adjudication of assigned findings

| Id | Verdict | Reason | Change |
| --- | --- | --- | --- |
| C-computation-1 (major) | MODIFIED (paper text ACCEPTED as the verifier's corrected fix) | Correct: `task_scip` clips SCIP's point before exact evaluation; the shortfall is mostly bound violation. Verified directly on all 21 runs (below). | 11.5 now says: incumbents lay outside the box by about 1e-8 at every coordinate at a bound in x* (SCIP's tolerance permits it); bound violations give 51%-94% of the shortfall, the epigraph violation 9e-7 the rest; projected incumbents optimal within 1.3e-14; exact gap 2.8e-6 to 6.8e-6 for n<=16; coefficients rounded to double precision. Table `tab:scip` caption: "exact value of SCIP's incumbent, projected onto the box, minus its dual bound" and "SCIP's projected incumbents". App. H gives the split. README E5 paragraph rewritten. Code part modified: instead of editing `run_all.py` (which would break the SHA-256 recorded in `environment*.json` for the scripts that produced the results), the new `experiments/scip_shortfall.py` reruns the 21 SCIP runs and records the largest bound violation, F at the unprojected point and the exact split in `results/E5_scip_shortfall.csv`; the README documents that `epigraph_shortfall` = F(projected x) - t includes the bound part. |
| C-computation-2 | ACCEPTED | Confirmed: planted('tree', 6, 4, 4100) of E4 has lambda_min(H) = -1.1613; E1-E3, E5 at most -1.75. | "at most $-1.16$" (11.2); README likewise. |
| C-computation-3 | ACCEPTED (first option) | Correct: `task_localized` never replays its EX certificates. | `replay_s1_ex.py` reruns the 30 S1 EX runs (status, value and completed stages reproduced on 30/30) and replays every certificate (30/30 valid; `results/S1_ex_replay.csv`). The paper's replay sentence now excepts only "the CT runs of S1 that only measure when the gap falls below a threshold"; README explains both. |
| C-computation-4 | ACCEPTED | Correct (`certified_grid.solve` tests `upper - lower` with the cumulative bound; `exact_output.solve_exact` passes `warm_start=point`, which replaces l as `initial_point`). | Item (e): "The lower bound used in the success test and reported at the end is the largest bound of all stages and trials ..."; item (g): "with the incumbent as its first center and, in place of l, as a start of the descent". The list is now in App. H. README updated, with the check that in all 45 CT runs of E2 and E5 the last stage's own gap is at most epsilon (re-verified from the stage CSVs: 24/24 and 21/21). |
| C-computation-5 | ACCEPTED | Correct (`run_all.design`). | E2: "in single trials of 12 stages", "CT with epsilon = 2^-20"; E3: "in single trials of 11 stages. The plateau of Figure fig:E2 (left)", whose caption defines the statistic. |
| C-computation-6 | ACCEPTED (artifact pinning MODIFIED) | Correct: both scripts wrote to the cwd. | `run_chain.py` and `run_recourse.py` now write next to themselves (`HERE = dirname(abspath(__file__))`), so the documented commands work from `experiments/`. README: all imported files outside the paper directory (solver, recourse corpus with `frozen/baseline/`, piecewise-recourse modules, QPLIB corpus and data; 36 files) are pinned to commit b59ed1b836e4 of `minlp-notes` (tracked, clean working tree, last modification 2026-10-02 23:18, before all runs) with SHA-256 in `results/dependencies_sha256.json`; the six hashes in `environment.json` match. Bundling the tree for a public artifact is left to the authors (unresolved). The paper sentence "Code, inputs, raw results and reproduction scripts ... accompany the paper" is kept as a statement about the supplementary material. |
| C-computation-7 | MODIFIED | Correct that E6 appeared before E4 and E5. | Used the reviewer's alternative: reordered the subsections (random instances moved after SCIP) instead of renaming. Experiments now appear as E1-E3, chain, E4 with S1, E5, E6, recourse. Renaming would have changed CSV/raw/summary names and the hashes recorded for `run_all.py`/`summarize.py`, and `exact-localized.tex` (not mine) cites "experiment S1". The order also helps: E6 uses the localized test and the enumeration, which 11.4 now introduces first. README has a paper-to-experiment map. |
| C-writing-18 | MODIFIED | Order: as C-computation-7. Captions: correct. | S1 is introduced as "the supplementary experiment S1" inside the E4 subsection, which explains its name. `tab:random` caption: "``Bag'' is the maximum bag size." `tab:recourse` caption replaced by the proposed one, with the table limit confirmed in `certified_grid.grid_dp`: a stage stops when the sum over bags of its table entries would exceed `max_table_states` = 2e5 (README states this and that the pipeline status `epsilon_optimal` is shown as "certified"). `tab:scip` caption also starts with the bag definition. |
| R-referee-5 | MODIFIED | Option (b) as proposed claims "We did not find library instances ..."; there is no record of a systematic library search, so that claim cannot be verified. Option (a) needs a library scan and new runs (out of this round's scope). | The opening paragraph of Section 11 now says that all instance families with continuous coordinates are synthetic, that the only library instances run are binary (11.8), "so we do not test whether modelled instances with continuous nonconvex terms have small width and a moderate condition number". |

## Verification of numbers newly stated

* `python3 experiments/scip_shortfall.py` (4 workers, 63 s, load about 4):
  21 runs; primal bound equal to `E5_scip.csv` in 21/21; in every run the
  violated coordinates are exactly the planted active ones, outward;
  largest violation 0.998e-8 to 1.0002e-8; SCIP's `checkSol` accepts 21/21;
  shortfall 1.82e-6 to 1.61e-5; bound share 0.5055 to 0.9441; epigraph
  part 9.00e-7 to 9.03e-7; bound part equals mu * sum(violations) to
  relative 4e-9.
* `python3 experiments/replay_s1_ex.py` (4 workers, 16 s): 30/30 exact,
  30/30 as in `S1_localized.csv`, 30/30 replays valid.
* `python3 process/w5/checks/computation-eigs.py`: largest lambda_min(H) over
  E1 -2.993, E2 -2.992, E3 -1.750, E5 -2.993, E4 planted -1.161.
* Inline Python on the result files: lemma ratios (D/(Lnh^2) max 0.1552,
  i.e. 0.276 of 9/16; radius 0.179; nodes 0.047); E4 stage groups (5 + 7 + 1
  + 2 = 15 instances beyond the three with n = 3); E5V offset variant exact
  gaps 1.88e-6 to 5.78e-6 on the 12 small instances, 0/39 intervals contain
  F*; t60 dual bounds -5.1e-5 to -7.5e-4; inward derivatives 23 to 192.5;
  last-stage gaps of the 45 CT runs of E2 and E5 all at most epsilon.
* Solver code read (not modified): `certified_grid.py` (`grid_dp` table
  limit, cumulative lower bound, `warm_start`), `exact_output.py`
  (warm start per round), `verify_certificate.py`, `verify_recourse.py`
  (both raise on invalid certificates, so `bool(result)` in
  `run_recourse.py` is a valid replay flag).
* `git status` and `git log` for `research-20261002-decomposition`: clean,
  last commit b59ed1b83; file mtimes before all runs.
* `python3 -m py_compile` on the two edited scripts; import test of
  `run_chain` from another directory.

## Build

`rm -rf /tmp/w5-computation && mkdir -p /tmp/w5-computation && rsync -a main.tex macros.tex references.bib sections figures /tmp/w5-computation/ && cd /tmp/w5-computation && latexmk -pdf -interaction=nonstopmode main.tex`
(last run with all groups' current files): no errors, no undefined
references, no overfull or underfull boxes. The only warning is the
undefined citation `AbelloEtAl2001` on p. 60 (Section 10, not my files).
126 pages. Baseline: the snapshot built the same way in
`/tmp/w5-computation-base`. These are targeted local checks; CI was not
consulted.

## Requests for other files

None required. All external references to Section 11 still resolve and
quote unchanged numbers.

## Unresolved

* Section 11 is about 5.0 pages, not 4.5. Moving Table `tab:chain` to
  App. H would save about 0.25 page; the authors or coordinator can decide.
* R-referee-5 option (a): no application-derived continuous instance with
  small width is tested; finding one needs a library scan (QPLIB/MINLPLib
  box-constrained or reformulable instances with bag size at most 4).
* C-computation-6: the public artifact must bundle the pinned solver tree
  (or the 36 files listed in `dependencies_sha256.json`); the repository is
  private.

## Verification

Verifier for group computation. I diffed `sections/computation.tex` against
`process/w5/sections-before-w5/computation.tex`, read the new
`sections/appendix-computation.tex`, the README, the two edited scripts and
the two new scripts, and checked every newly stated number against the
result files. The revision is sound. I found no mathematical error. I fixed
the eight problems listed below. Section 11 still ends at the same place on
p. 69 (line 35) as in the agent's version, so the fixes cost no space.

### Assigned findings: verdicts confirmed

| Id | Agent's verdict | Verification |
| --- | --- | --- |
| C-computation-1 | MODIFIED | Confirmed. The text follows the verifier's corrected fix and does not use the undefined $\mu$. `E5_scip_shortfall.csv` gives 21/21 primal bounds equal to `E5_scip.csv`; violated coordinates = active ones, outward, in 21/21 runs; largest violation 0.998e-8 to 1.0002e-8; SCIP's `checkSol` accepts 21/21; shortfall 1.82e-6 to 1.61e-5; bound share 0.5055 to 0.9441; epigraph part 8.9999e-7 to 9.030e-7; $F$ at the projected point at most 1.30e-14. `E5_scip.csv`: exact gaps 2.757e-6 to 6.795e-6 on the 12 instances with $n\le16$. `task_scip` builds the model from `float(...)` coefficients, which supports "coefficients rounded to double precision". Keeping `run_all.py` unchanged and adding a separate script is justified: the current hashes of `run_all.py` and `summarize.py` match `environment_S1.json`. The caption of `tab:scip` and the README are correct. I reworded one sentence (item 6 below). |
| C-computation-2 | ACCEPTED | Confirmed by rerunning `process/w5/checks/computation-eigs.py`: the largest $\lambda_{\min}(H)$ is -2.993 (E1), -2.992 (E2), -1.750 (E3), -2.993 (E5) and -1.1613 (E4, tree); the script uses the instance lists of `run_all.design()`. |
| C-computation-3 | ACCEPTED | Confirmed. `S1_ex_replay.csv` has 30 rows with status exact, `as_in_S1` True and `replay_valid` True. `replay_s1_ex.py` uses the seeds and `solve_exact` arguments of `run_all.design()` and `task_localized`. `task_localized` shows that the threshold runs are separate `solve` calls that are not replayed, which matches the new sentence in 11.1. |
| C-computation-4 | ACCEPTED | Confirmed. Items (e) and (g) in App. H read as the finding asks. |
| C-computation-5 | ACCEPTED | Confirmed: `design()` sets `max_stages=12` for E2 and 11 for E3, and epsilon 1/1048576 for the E2 default schedule. I clarified the E3 wording (item 3 below). |
| C-computation-6 | ACCEPTED / MODIFIED | Confirmed. Both scripts write to `HERE`, and all four scripts compile. The 36 hashes in `dependencies_sha256.json` match both the working tree and `git show b59ed1b8:...` (0 mismatches). The public-artifact bundling remains an author decision. |
| C-computation-7 | MODIFIED | Accepted: the experiments now appear in order (11.2 E1-E3, 11.4 E4 and S1, 11.5 E5, 11.6 E6), and the README maps them to sections. Renaming would invalidate the recorded script hashes and the name "S1" used in `exact-localized.tex`. |
| C-writing-18 | MODIFIED | Confirmed. The table limit in `certified_grid.grid_dp` is `sum(prod(len(grids[i]) for i in bag) for bag in bags) > max_table_states` with 2e5 from `run_recourse.py`, which matches the caption. I corrected one table cell (item 8 below). |
| R-referee-5 | MODIFIED | Accepted. The added sentence makes no claim of a library search and states the limitation. |

### CUTPLAN items: verified

All done. E3 is merged into E2 and 11.5/11.6 are merged; S1 keeps `\label{sec:comp-localized}`, which resolves to 11.4, so `exact-localized.tex` line 128 still reads correctly. The Limits subsection is shorter. App. H holds `tab:scip`, `tab:random` and `tab:recourse` with their details. I compared the snapshot with the main text plus App. H block by block. No sentence with content was lost except: the cap of $10^7$ entries for QPLIB_3852, the checker's slowness mechanism (both still in the README), and the $\theta=1/4$ sentence of the Fig. `fig:E2` caption (the figure legend labels the curve and the E2 paragraph gives the numbers). All 17 labels exist exactly once, with no duplicate labels anywhere in `sections/`. External references to Section 11 (`exact-localized.tex` 4 and 128, `conclusion.tex`, `intro.tex`, `growth.tex`, `grids.tex`) still match the text. The conclusion's sentence on tolerances ("projected onto the box", "bounds and constraints") agrees with the corrected SCIP account.

### Problems found and fixed

1. 11.2 (E1): "In all 876 stages of the runs of E1--E3 that satisfy $8\kappa\theta^2\le1$" was wrong as a set description. That set includes the uniform runs ($\theta=0$ satisfies the inequality trivially, and (G5) gives no finite bound) and the unfiltered E1 runs, which are not among the 876 stages. I restored the precise set ("the filtered graded runs of E1 and the runs of E2 and E3 with the theorem's grading") and named the bounds (G3)--(G5), which match `lem:commonmesh` in the current `growth.tex`.
2. 11.1: "the current incumbent, which exact coordinate descent improves before stage 0" is now "provides before stage 0 and may improve after every stage", as in item (d).
3. 11.2 (E3): "The plateau of Figure~\ref{fig:E2} (left) grew from 7 to 26" read as if Figure 2 showed E3 data. It now says "The plateau, measured as in Figure~\ref{fig:E2} (left), grew ...".
4. 11.4 (E4): the agent wrote $\log_2(\Omega W)$ for the implementation's constant and then "the constant $\Omega$ of~\eqref{eq:exact-constants}". That gives $\Omega$, reserved by CONVENTIONS, two meanings. The text now uses $\Omega'\ge\Omega$, the denominator bound of Proposition `prop:accept`, for the implementation's constant, and writes "$\Omega'=\Omega$" for the lemma constant. This is valid because the row-sum constant is never smaller than $\Omega$, so it is also a denominator bound for OPT.
5. 11.4 (S1): the agent's sentence "... from which on an optimal candidate passes the acceptance test of that proposition, after 40 to 72 stages ..." was hard to parse. I rewrote it as two clauses. The mathematics is unchanged: for an optimal $x$, $F(x)-\beta\le U-\beta<1/(\Omega'W)$.
6. 11.5: "Outside the box, $F$ decreases at the rate of the inward derivative, so these violations account for 51% to 94%" presented a measured share as if it followed from the rate. It now reads "Moving such a coordinate outward decreases $F$ at the rate of its inward derivative, and these violations account for ...". I also removed the duplicate "with default settings"; the last sentence of the subsection keeps it.
7. 11.7: "All certificates were replayed by the respective checkers, which reuse the solver's ... code" wrongly covered the plain-grid runs, which `run_recourse.py` replays with the independent `verify_certificate`. The sentence now says that only the recourse pipeline's checkers reuse solver code. App. H: the definition of the split was clarified with $\bar x$; $F(\bar x)-t$ equals the shortfall up to $1.3\cdot10^{-14}$.
8. Table `tab:recourse`: the plain run on "dense cut, $n=7$" showed gap $1\cdot10^{-3}$ with status "certified", which the new caption defines as gap at most $2^{-10}\approx9.77\cdot10^{-4}$. `recourse/results.csv` gives exactly 0.0009765625 = $2^{-10}$. The cell now shows $2^{-10}$.

I also restored and then removed again the chain sentence "so that the first incumbent is not optimal". It is true (`results_warmstart.csv`: initial upper bounds > 0 = OPT), but "the solver's first descent start" already implies it.

### Checks run (local, targeted; CI not consulted)

* `python3 process/w5/checks/computation-eigs.py` (output above).
* Inline Python on `E4_exact.csv` (rounds 5/6/7/8, i.e. q = 64/128/256/512, for 5/7/1/2 instances; bits 49.2-65.0, 80.0-120.2, 207.95, 341.65-341.88; lemma bits 21.3-315.0), `E5_scip.csv`, `E5_scip_shortfall.csv`, `E5V_scip_variants.csv` (39 runs: offset 21, t60 9, feastol 9; exact gaps with offset 1.88e-6 to 5.78e-6; t60 dual bounds -7.45e-4 to -5.11e-5; interval contains $F^*$ in 0/39), `S1_ex_replay.csv`, `recourse/results.csv`, `chain/results_warmstart.csv`. Run counts: E1 filtered 24 + E3 at $\kappa_{\mathrm{target}}=4$ 54 = 78; E5V path runs with $n\ge32$: 27; inward derivatives 23 to 192.5; objective constants 93.7 to 1577.
* SHA-256 of the 36 dependencies against the working tree and commit b59ed1b8 (0 mismatches); current hashes of the seven experiment scripts against `environment_S1.json` (all equal).
* `python3 -m py_compile` on `chain/run_chain.py`, `recourse/run_recourse.py`, `scip_shortfall.py`, `replay_s1_ex.py`.
* I did not rerun `scip_shortfall.py` or `replay_s1_ex.py`: the W4 verifier's independent script reproduced the same split on five instances, and the CSVs are internally consistent.
* Build: `rm -rf /tmp/w5-computation-verify && ... && latexmk -pdf -interaction=nonstopmode main.tex` with all groups' current files: 127 pages; no errors, no undefined references, no overfull or underfull boxes. The only warning is the undefined citation `AbelloEtAl2001` on p. 60 (Section 10, not this group). For comparison, I built the agent's version (my edits reverted) in `/tmp/w5-cv-agent`.

### Pages (from `/tmp/w5-computation-verify/main.aux` and the PDF)

Section 11: p. 64 (from line 38 of 45) to p. 69 (line 35 of 41), about 5.0
pages. This is the same end point as the agent's version in the same build.
Appendix H: p. 124 (from line 21 of 50) to p. 127 (Tables 5 and 6), about 3.2
pages.

### Unresolved

* Section 11 is about 5.0 pages; the target was about 4.5. Moving `tab:chain` to App. H would save about 0.25 page (coordinator decision).
* R-referee-5 option (a): no modelled continuous instance of small width is tested.
* C-computation-6: the public artifact must bundle the 36 pinned files, because the repository is private (author decision).
* Outside this group: `AbelloEtAl2001` is undefined (p. 60).
