# W3 report: computation group (Section 11, experiments/, figures/)

Files changed: `sections/computation.tex` (rewritten), `experiments/instances.py`,
`experiments/run_all.py`, `experiments/figures.py`, `experiments/summarize.py`,
`experiments/localized.py`, `experiments/README.md`, new
`experiments/analysis.py`, new `experiments/chain/run_chain_warmstart.py`
(+ `results_warmstart.csv`), new `experiments/qplib/run_qplib.py`
(+ `results.json`, `run_qplib.log`), regenerated `experiments/results/*`,
`experiments/figures/*`, and copies `figures/E1_states_vs_stage.pdf`,
`figures/E2_plateau_vs_kappa.pdf`, `figures/E3_plateau_vs_n.pdf`. The solver in
`research-20261002-decomposition/solver/` was not modified. The previous
results and figures are kept in `process/w3/backup-results-w2/`.

All numbers in Section 11 are computed by `experiments/summarize.py` from the
new results (`experiments/results/summary.json`), except Table 1 and Table 3,
whose data (`chain/results.csv`, `recourse/results.csv`) were not rerun.

## 1. Adjudication

| id | decision | reason | change |
|---|---|---|---|
| F13 | ACCEPTED (my part) | Terminology drift in Section 11 and the figures. | CT / TRIAL / EX / REC / UC with `\ref{alg:...}` at first use; "graded grid", "grading"; "nodes per coordinate"; "table entries" for bag-table sizes (Tables 1–4, Fig. 1 axis label); figure legends say "graded". Other files: their owners. |
| F21 | MODIFIED (merged with F76, F214) | R6's wording is right but incomplete: a proved lower bound applies. | E4 text: "minimizers form two segments, so they have set growth (Remark rem:setgrowth) but no point growth, and for them Theorem thm:exact guarantees only termination; their objective contains a(x0−x1)², a multiple of the instance of Prop. lim:prop:setgrowth with n=2, on which every run of filtering with thresholds U_j ≥ OPT, in particular CT, that certifies accuracy ε ends with at least 1+1/(2√ε) nodes per coordinate." (wording of the last clause as requested by limits). |
| F26 | ACCEPTED (my part) | British spellings. | "behaviour", "favours" removed ("favors"). Other files: their owners. |
| F34 | ACCEPTED (my part) | Overfull box from `\texttt{fractions.Fraction}`. | Rephrased; Table 3 gets `\small` and `\tabcolsep=4pt`. Build: no overfull/underfull box from computation.tex. |
| F39 | ACCEPTED, one item MODIFIED | R9 R5 is right. | (a) Off-grid minimizers: proved criterion (all nodes of a trial lie in D ∪ (c⁰_i + D), D = dyadic rationals; x*_i = k/21, k≠0, is not dyadic) and measured fraction: 347 of 3,177 free coordinates of x* (11%) are nodes of the last grid in E1–E3 with κ_target ≥ 4 (inspected cases: coordinates the initial descent had already set to x*_i, `process/w3/checks/computation-offgrid.py`); in E6, 42 of 213. The chain could not be given an off-grid minimizer: its minimizer is a corner of the box for every translation, hence a node of every grid; reported honestly together with a warm start at the opposite corner (same stages, same largest grid except m=2, −2% to +8% table entries). (b) New non-designed family E6 with κ brackets (Section 11.3, Table 4). (c) New S1 subsection 11.6 reconciled with E4 (30 vs 20 instances; 542 vs 534 stages are different instance sets). (d) SCIP comparison strengthened (exact gaps, dual bounds, equal-limit, tolerance and offset reruns, both limits). |
| F49 | ACCEPTED (part a, my files) | Terminology. | As F13, including figure legends. Parts (b)–(e): other files. |
| F57 | ACCEPTED (my part) | Constants. | Section 11 cites Lemma lem:commonmesh (added by coreB) with 9/16, 4.2√(nκ), 8θ⁻¹⌈log₂(n+2)⌉, and states that the implementation's cap 100·2^μ⌈log₂(n+2)⌉ is 12.5 times the analyzed cap. |
| F65 | ACCEPTED (my part) | "Algorithm 2", "capped schedule". | Replaced by CT (Algorithm alg:ct) and TRIAL (Algorithm alg:trial). |
| F76 | MODIFIED | The exact count 4(⌊√(n/4)⌋+1)+1 is an empirical formula for the separable κ=2 instances; attributing it to Prop. prop:tu-tight (TU instance, being deleted) or to Cor. cor:uniformgrid (a different family, and a lower bound) would be wrong. | E3 now reports the coupled case κ_target=4; Cor. cor:uniformgrid is cited only for "uniform grids need order √(nκ) nodes on some instances"; the separable count is stated as observed. Flat wording: see F21. |
| F77 | ACCEPTED | S1 unreported. | New subsection 11.6 `sec:comp-localized`; pointer text for 6.5 in Section 3 below. |
| F89 | REJECTED (my file) | I follow the notation of Lemma lem:commonmesh as written by coreB (h_j = s2^{-j}); introducing h_j^c only in Section 11 would create a second name. Section 11 uses no η. | none |
| F91 | ACCEPTED (my part) | The planted-instance sentence left Remark rem:nonconvex (coreA). | Section 11.2 now describes the construction and the κ bracket via Lemma lem:growthcert(a),(b) (also covers coreA request C1). |
| F147 | ACCEPTED (my part) | SCIP 10.0 used, SCIP 8.0 cited; safe bounds missing. | `\cite{VigerskeGleixner2018,HojnyEtAl2025}` (existing keys); one sentence citing `NeumaierShcherbina2004` in the SCIP paragraph. BestuzhevaEtAl2023 is no longer cited anywhere (coordinator). |
| F156 | ACCEPTED (my part) | Lemma added by coreB. | Section 11 cites lem:commonmesh and its items (G1)–(G5). |
| F196 | ACCEPTED (numbers recomputed) | Constants were from an older analysis; sentence false. | Ratios recomputed by `summarize.py` over E1 (graded, filtered), E2 and E3 (theorem θ, both κ_target = 2 and 4), 876 stages, using κ_lb (conservative): D(y_j) ≤ 0.155 Lnh_j² (bound 9/16), radius ≤ 0.179 of 4.2√(nκ)h_j, nodes ≤ 4.7% of 8θ⁻¹⌈log₂(n+2)⌉ (0.38% of the implementation cap). Text: "at most 0.16 Lnh_j², at most 0.18, at most 5%". R8's "0.17" was over the old E3 (κ=2) only; the new coupled E3 gives 0.179. figures.py: bound line 4.2√(nκ), gap line 9/16, both reference lines at κ_lb. |
| F197 | ACCEPTED (rerun) | κ=2 instances are separable. | E3 now runs κ_target ∈ {2, 4}; text reports κ_target=4 (uniform 7→26, graded θ=1/8 9→19, θ=1/4 9→17) and states the separability caveat for κ_target = 2 in E2 and E3 (verified: the initial coordinate descent returns x* on all 18 κ=2 E3 instances, `process/w3/checks/computation-claims.py`). |
| F198 | ACCEPTED (both options partly) | The wrapper uses the row-sum constant. | Implementation list (g) says so. `experiments/analysis.py::lemma_heights` computes Ω of (eq:exact-constants) outside the solver; E4 records both: 49–342 bits (code) vs 21–315 bits (paper). The solver was not changed (not allowed). Request to exact for 6.5 below. |
| F199 | ACCEPTED (numbers differ from R8) | Off-by-one and inflated comparison. | S1 subsection: "within five stages" (0-based index ≤ 4). Single-run threshold measured in `run_all.task_localized`: first stage of one CT run with certified gap < 1/(ΩW), W the denominator of OPT, on the five instances with the most EX stages (542, 542, 542, 542, 534): **40 to 72** stages with (eq:exact-constants), 139 to 157 with the code's constant. R8's 51–73 used a different fifth instance (275 EX stages) and stopped at 1/(2ΩW). A first version of my measurement tested the incumbent's own denominator; it missed two instances whose incumbent was near-optimal but not exactly optimal; corrected and S1 rerun. Also added (exact's suggestion): the face candidate of Def. def:facecand accepted the same 29 instances within nine stages, with the same values. |
| F200 | ACCEPTED (rerun) | QPLIB paragraph misleading. | `experiments/qplib/run_qplib.py`: min-fill bag sizes 20 and 94 (verified); stage-0 entries 5,723,918 and 7.96·10²⁸; QPLIB_3852 with cap 10⁷: one stage, bounds −234 = −234 (library value 234 after sign change), 156 s, 4.4 GB. Not replayed (stated, with the reason). Paragraph rewritten as requested, cap stated. |
| F201 | ACCEPTED, one claim MODIFIED | SCIP gap is SCIP's own claim; unequal limits. | Table 2: columns "gap (exact)" and "dual bound", both limits in the caption. Text: exact gap 2.8·10⁻⁶–6.8·10⁻⁶ on n ≤ 16, primal bounds 1.8·10⁻⁶–1.6·10⁻⁵ below OPT, interval never contains OPT, relative target 10⁻⁸–10⁻⁹ (constants 94–1,577). New E5V reruns (60 s; feastol = dualfeastol = 10⁻⁹; constant as offset): all 27 path runs with n ≥ 32 still hit the limit, interval never contains OPT in 39 runs. R8's "did not change any status" is false for the offset variant on n ≤ 16 (some "gaplimit" became "optimal", both successes), so the sentence is restricted to the n ≥ 32 outcome. The caption notes that the two SCIP columns agree to the digits shown because OPT = 0 and SCIP's incumbents are optimal to 1.3·10⁻¹⁴. |
| F202 | ACCEPTED | Incomplete list of differences. | Seven-item list (a)–(g) in 11.1; which experiments run TRIAL vs CT; abort check verified by `summarize.py` (45 CT runs of E2/E5: 12 restarts, all after full-length trials; E6 and chain never restart). "As Theorem 9.3 predicts" replaced by the θ=0 version of (G1)–(G4) of Lemma lem:commonmesh, whose proof (appendix-growth.tex) I checked does not use θ > 0. |
| F203 | ACCEPTED | Recourse checkers reuse solver code. | Sentence added as proposed. |
| F204 | MODIFIED | The solver must stay unchanged, so the checker hot loop is not hoisted. | Section 11.1: "On the replayed runs below with a solve time of at least 0.1 seconds, replay took between 0.8 and 2.5 times as long as the solve" (computed: 0.81–2.54 over E1–E6, chain, recourse plain grids). QPLIB certificate not replayed, with the reason. grids.tex (coreA) now refers to Section 11 for times. |
| F205 | ACCEPTED | | "shares model parsing, decomposition validation and objective evaluation". |
| F206 | ACCEPTED (range corrected) | | Fig. 2 caption: reference √(nκ/8), statistics defined, certified κ in [0.97, 1.12]·κ_target (R8's [1, 1.12] is slightly off: κ_lb/κ_target goes down to 0.978 at κ=256). |
| F207 | ACCEPTED | | "nodes" throughout. |
| F208 | ACCEPTED | | "Experiment E4 attempted exact output on twenty small instances". |
| F209 | ACCEPTED (verified) | | The three n=3 instances have no continuous coordinate with A_ii > 0 (checked); stage counts explained by the doubling of q (67–77, 132–144, 275, 534 for 49–65, 80–120, 208, 342 bits). |
| F210 | ACCEPTED | | "to within 12%"; κ ∈ [4.0, 4.45]. |
| F211 | ACCEPTED | | "grows somewhat more slowly than √κ". |
| F212 | ACCEPTED | | "fails for every instance with κ_target ≥ 4". |
| F213 | ACCEPTED (rerun) | | `chain/run_chain_warmstart.py`; text as in F39(a); θ=1/4 vs κ ≤ 80 sentence added. |
| F214 | MODIFIED | Remark 9.4 says only "open"; Prop. lim:prop:setgrowth is a proved lower bound for the same structure. | See F21; both time limits (30 s, 5 s) stated. |
| F215 | ACCEPTED | | HojnyEtAl2025 cited. |
| F216 | ACCEPTED | | "reproduction scripts (one command per experiment group)"; solver path relative in `instances.py` and `qplib/run_qplib.py` (chain/recourse scripts were already relative). README lists all commands. |
| F217 | ACCEPTED | | See F34. |
| F218 | ACCEPTED | | Plain-grid replay column added to Table 3 (26.4 s, 50.9 s, ...). |
| F219 | ACCEPTED | | "a core coordinate whose own term −x₀² is concave"; "the functions f_M − z² with f_M from Example ex:cv-fm". |
| F220 | ACCEPTED | | Fig. 2 left: ticks 8,16,32,64 with plain labels, legend moved to the empty upper left; Fig. 1: shared y-axis and dotted 10⁵ cap line; caption says a stage is plotted only if all three runs completed it (the code never plotted survivor medians, so R8's "medians over seeds still running" does not apply); one κ (κ_lb) for both lines in Fig. 2. |
| F221 | ACCEPTED (my part) | | QPLIB settings (cap 10⁷) moved into the Limits paragraph; front already changed the conclusion sentence on floating-point incumbents (see request 3). |

## 2. Labels

Deleted or renamed: none.

New labels in `computation.tex`: `sec:comp-impl` (11.1 implementation),
`sec:comp-growth` (11.2 planted family, E1–E3), `sec:comp-random` (11.3 E6),
`sec:comp-chain` (11.4), `sec:comp-exact` (11.5 E4), `sec:comp-localized`
(11.6 S1), `sec:comp-scip` (11.7 E5), `sec:comp-recourse` (11.8),
`sec:comp-limits` (11.9), `tab:random` (Table 4, E6). Kept: `sec:computation`,
`fig:E1`, `fig:E2`, `tab:chain`, `tab:scip`, `tab:recourse`.

Labels of other groups that Section 11 uses (all resolve in the current
build): alg:ct, alg:trial, alg:ex, alg:rec, alg:uc, app:growth, cor:local,
cor:uniformgrid, def:graded, def:facecand, ex:chain, ex:cv-fm, eq:exact-constants,
eq:minorant, lem:commonmesh (items G1–G5), lem:graded, lem:growthcert,
lim:prop:messages, lim:prop:setgrowth, prop:accept, prop:local, rem:cf,
rem:heights, rem:setgrowth, sec:cuts, sec:grids, sec:limits, sec:recourse,
thm:approx, thm:certificate, thm:exact. Please keep them.

## 3. Requests for other files

1. **exact (`exact-localized.tex`, paragraph "In experiment S1 ...", ~lines
   129–137).** The numbers "51 to 73" are R8's; Section 11 measures 40 to 72.
   Suggested replacement of the first two sentences:
   "In experiment S1 (Section~\ref{sec:comp-localized}) the test accepted 29
   of 30 random unplanted mixed-integer instances, within nine stages with
   the face candidate of Definition~\ref{def:facecand} and within five with
   the stationary point of the face of the stage incumbent, a rule that
   Corollary~\ref{cor:local} does not cover. On the five instances on which
   EX used the most stages, one CT run reaches the threshold of
   Proposition~\ref{prop:accept} with the constants
   of~\eqref{eq:exact-constants} only after 40 to 72 stages, and the
   implementation of EX, which restarts for every $q$, used up to 542 stages."
   Also "neighbourhood" → "neighborhood" (F26). The threshold range
   "about 2^{-315} to 2^{-21}" in lines 3–5 matches Section 11.5 (21–315 bits).
   The face candidate is now `experiments/localized.py::face_candidate`
   (your script's rule), so `process/w3/checks/exact-face-candidate-s1.py`
   need not move.
2. **coreA / coordinator (`grids.tex`).** If any sentence still quotes
   "0.9 to 2.5 times the solve time", change it to "between 0.8 and 2.5
   times" (measured over E1–E6, chain and recourse plain grids, runs with
   solve time ≥ 0.1 s). The current grids.tex text ("Section 11 reports
   measured replay times") needs no change.
3. **front (`conclusion.tex` ~lines 27–30).** E6 adds unplanted random
   instances, and QPLIB_3852 is now solved exactly. Suggested:
   "The experiments show the predicted accuracy-independent grid sizes on
   designed families and on unplanted random instances. On two binary QPLIB
   instances the method is plain dynamic programming: the one whose
   decomposition has bag size 20 is solved exactly in one stage, the other
   has bag size 94, so the width of the available decomposition, not the
   accuracy, is the binding limit."
   `intro.tex` lines 154–155 (gap 10⁻³ at m = 64 with at most eleven nodes)
   remain correct. The abstract's "independent checker" is correct for the
   main checker (Section 11.1 qualifies the recourse checkers).
4. **coreB (`growth.tex`, optional).** Section 11.2 uses that (G1)–(G4) of
   Lemma lem:commonmesh and their proofs hold verbatim for θ = 0 (uniform
   grids), with Lemma lem:graded(a) replaced by w_i(v) ≤ h_j. I checked this
   against the proof in `appendix-growth.tex` (it uses only
   w_i(v) ≤ h + θ|v − c_i| and θ²κ ≤ 1/8). A one-sentence remark after the
   lemma would make the claim visible where it is proved.
5. **limits.** Requests 1 and 2 of `reports/limits.md` are done (Ψ_m, ξ_m,
   wording of the set-growth consequence).
6. **coordinator (`references.bib`).** `BestuzhevaEtAl2023` is no longer
   cited by any section (grep); delete it or keep it deliberately.

## 4. New BibTeX entries

None. Existing keys used: `HojnyEtAl2025`, `VigerskeGleixner2018`,
`NeumaierShcherbina2004`, `FuriniEtAl2019`.

## 5. Checks run (targeted, local; CI not consulted)

All with at most 4 concurrent processes on the shared machine (load 11–19).
Total new compute about 19 minutes wall.

| Command | Purpose | Result / time |
|---|---|---|
| `python3 process/w3/checks/computation-e6-proto.py` | prototype of E6: growth certification rate, κ brackets | 11/40 certified by Lemma growthcert(a); ~30 s |
| `python3 process/w3/checks/computation-e6-proto2.py` | does a sign-aware variant of the certificate help? | only marginally; not adopted (would need a new lemma); ~30 s |
| `python3 process/w3/checks/computation-smoke.py` | new task types on single instances | all ran; ~10 s |
| `cd experiments && python3 run_all.py --jobs 3` | E1–E6, E5V, S1 (423 tasks) | 0 failures; 12 min 51 s wall (768 s in-script), 2,289 s summed task time |
| `cd experiments && python3 run_all.py --only S1 --jobs 4` (twice) | S1 after fixing the single-run threshold, then with the face candidate | 15 s each |
| `cd experiments/qplib && python3 run_qplib.py` | QPLIB bag sizes, stage-0 entries, QPLIB_3852 with cap 10⁷ | exact −234, 1 stage, 5,723,918 entries, 156 s, 4.4 GB; 2 min 38 s |
| `cd experiments/chain && python3 run_chain_warmstart.py` | chain from the upper corner | all certified and replayed; 61 s |
| `python3 process/w3/checks/computation-offgrid.py` | which free coordinates of x* are grid nodes | on-grid ones were set to x*_i by the initial descent (3 instances); ~5 s |
| `python3 process/w3/checks/computation-claims.py` | κ=2: descent returns x* (18/18); n=3 E4 instances have P = ∅; outward-rounded E6 brackets | confirmed; ~10 s |
| `cd experiments && python3 run_all.py --figures` and `python3 summarize.py` | CSVs, figures, all quoted numbers | `results/summary.json` |
| `latexmk -pdf -interaction=nonstopmode -outdir=build/computation main.tex` (several times, last after all edits) | LaTeX check | no errors, warnings, overfull or underfull boxes from computation.tex; no undefined cross-references (`\ref`) in the whole build; latexmk exits 12 only because bibtex finds no `\bibdata` in `main.aux` (coordinator's bibliography setup, not my file) |

## 6. Unresolved

- The QPLIB_3852 certificate was not replayed (the checker's per-entry bag
  search makes it slow at 231 bags; fixing it requires changing the solver,
  which this round does not allow).
- E6: Lemma lem:growthcert(a) certifies growth on only 11 of 40 random
  instances; on the others κ is unknown. One E6 candidate (path, n=16, seed
  16005) is proved optimal by neither test; CT's certified gap still holds.
- The exact-output wrapper still uses the row-sum constant (solver
  unchanged); Section 11 reports both constants.
- `chain/run_chain.py` and `recourse/run_recourse.py` were not rerun (data from
  the previous round, load about 11); Tables 1 and 3 use them.
- R8's suggested runs not done: Example ex:family (R8 experiment 5) and a run
  with the analyzed cap to exercise aborts (R8 experiment 7). In all runs the
  node counts stay below 4.7% of the analyzed cap, so it would not bind either.
- The implementation's EX starts each round from the full box; Section 11.6
  therefore reports both EX's stage counts and the single-run threshold.

## Verification (computation-verify)

Scope: `sections/computation.tex`, `experiments/` (README, scripts, results,
figures) and the copies in `figures/`. I checked every adjudication against the
review text, every changed number in Section 11 against
`experiments/results/*.csv`, `summary.json`, `chain/*.csv`,
`recourse/results.csv` and `qplib/results.json`, every implementation claim of
Section 11.1 against the solver code (`certified_grid.py`, `exact_output.py`,
`verify_certificate.py`), and every mathematical claim of Section 11 line by
line.

### Adjudications

All 40 adjudications are justified, and the ACCEPTED fixes are applied in
`computation.tex`. The F89 rejection matches CONVENTIONS (the common mesh is
`h_j`). The MODIFIED decisions F21/F76/F214 (set growth but no point growth,
plus Prop. `lim:prop:setgrowth`), F198 (both height constants reported, solver
unchanged) and F204 (solver unchanged) are correct. In five accepted fixes the
applied text was still inaccurate, and I corrected it:

| id | problem found | fix |
|---|---|---|
| F196 | "In all runs with 8κθ²≤1 (E1, ...)": the ratios are computed only over the *filtered graded* E1 runs (`summarize.py`), and the node cap is undefined for θ=0. "These ratios use κ_lb, which makes them larger than the true ratios": only the radius ratio depends on κ. | Scope now "the graded runs of E1 with filtering and the runs of E2 and E3 with the theorem's grading ... at all 876 stages". The κ_lb sentence now applies to the radius ratio only ("which can only increase it"). |
| F202 | E1–E3 also run without the per-coordinate cap (adaptive schedule, `coordinate_cap = max_table_states`). This was not stated. | Added "no cap on the nodes per coordinate". |
| F204 | "between 0.8 and 2.5": the measured maximum is 2.54. | "between 0.81 and 2.54 times", with the scope given (E1–E6, chain, plain-grid recourse; solve time ≥ 0.1 s). |
| F210 | "κ∈[4.0,4.45]": the smallest certified lower end is 3.9985 (E1/E3/E5), so the interval as written does not contain all certified κ. | "κ∈[3.99,4.45]" (four places). |
| F213 | "(here κ≤80)" does not show that 8κθ²≤1 fails. | Proved instead: Ψ_m=1 at the point with z_1=1 and all other coordinates 0, so every growth constant is ≤1 and κ≥10. |
| F219 | Example `ex:cv-fm` now calls the function φ_M (recourse renamed it), so "f_M" is undefined. | "φ_M − z² with φ_M from Example ex:cv-fm". I checked the corpus: diagonal −1 in `from_squares` adds −z². |

### Further corrections in `computation.tex`

* Planted family: "has a prescribed smallest eigenvalue 4/κ_target" is exact
  only up to rounding the coupling scale c down to a multiple of 2⁻¹².
  "Entries ... have size 2 to 4, so H is indefinite" is not a valid inference:
  an entry of exactly 2 next to a single neighbor gives a singular PSD 2×2
  block. The text now states the measured fact (λ_min(H) ≤ −1.75 in every
  instance).
- Off-grid paragraph: I added the missing step "filtering moves endpoints only
  to nodes", without which the dyadic-node argument is incomplete (clipped
  nodes are box endpoints), and stated that 347/3,177 counts free coordinates
  once per run. I replaced the anecdotal "in the runs we inspected" with a
  measurement. I reran the 78 single-trial runs of E1 (filtered) and of E3 at
  κ_target=4 (`computation-verify-offgrid.py`). Of the 153 free coordinates on
  the last grid, 146 had been set to x*_i by the initial descent, 3 have
  x*_i=0, and 4 have a first center at a nonzero dyadic distance from x*_i.
  None is unexplained, so the argument holds. The per-run counts equal the
  saved `xstar_nodes_free`.
- "Every certificate produced in Sections 11.2–11.8 was replayed by the
  checker" was false: the EX runs and the single-run threshold runs of S1 are
  not replayed (`task_localized`), and the recourse runs use their own
  checkers. The sentence now says "every certificate on which a result rests
  ... by its checker; the runs of S1 that only count stages were not replayed".
- Fig. 2 caption and E2 text: θ=1/4 violates 8κθ²≤1 only for κ_target≥4
  (F212, which the caption still missed). "Contraction fails for κ≥64" is now
  stated for κ_target, because the certified κ for κ_target=64 starts at 63.7.
- E6: "did not grow with the accuracy ... grew by at most 5 nodes" was
  self-contradictory and is now "stayed the same on 27 ... changed by at most 5
  on the others". "The instances without a growth certificate had grids of the
  same sizes" was inaccurate (certified: 9–11 nodes; others: 8–18) and now
  states these ranges. The bracket [8.0,6663] is now [8.0,6662.2], consistent
  with the other outward roundings.
- S1: I rewrote the comparison ("A fairer comparison" is a judgment). I
  explained "on 12 instances already on the full box": the test passes with X
  in place of the narrowed box. I fixed the tense ("also agree"). I dropped the
  vague "The localized test needed at most nine", which repeats the stage
  counts stated earlier.
- SCIP: "a relative target of 10⁻⁸ to 10⁻⁹" is now "between 6·10⁻¹⁰ and
  1.1·10⁻⁸ of the constant" (10⁻⁶/1577.3 = 6.3·10⁻¹⁰).
- 11.1: I switched the Hessian notation from A to H, matching Section 6 and
  Lemma `lem:growthcert` (11.2 onward already used H). "This constant is larger
  than" is now "never smaller than", because D is a multiple of Δ and the row
  sums dominate Ĥ_ii. "WSL2" is now spelled out.

`experiments/README.md`: the stale numbers "Table 1/2/3/4" now name the
labels. The README now matches all of the corrections above (κ interval,
indefiniteness, off-grid classification, replay exceptions, E6 wording, S1
full-box wording, relative target).

### Checks of statements and data (all confirmed unless fixed above)

- Section 11.1 against the code: cap `100·2^trial·(n+1).bit_length()` =
  100·2^μ⌈log₂(n+2)⌉, which is 12.5× the lemma's cap. The stage limit is the
  least J with (7/8)Lns²4⁻ᴶ≤ε, and 7/8 ÷ 9/16 = 14/9 < 4, so at most one extra
  stage. The first center is the incumbent and later centers are y_j. Polishing
  runs from ℓ, u and the midpoint, then within the current box. The lower bound
  is the maximum over stages and trials. Uniform grids use θ=0. The wrapper
  uses the row 1-norm product over continuous rows, a denominator that also
  clears A_ij/2, q=4 with doubling and restarts with a warm start, and the
  three candidates (with radius 1/(4R²) as in Remark `rem:cf`, and τ=1/(4nR)
  as in REC). The checker imports only `BoxQP` and `rational`.
- θ=0 extension of (G1)–(G4): I reread the proof in `appendix-growth.tex`. θ
  enters only through w_i(v)≤h+θ|v−c_i| and Lθ²/2≤g/16, so it is valid. The
  next uniform grid has 1+⌈R₊/h'⌉+⌈R₋/h'⌉ ≤ 3+(R₊+R₋)/h' ≤ 3+16.8√(nκ) nodes.
- Lemma `growthcert`(a) as applied: the planted generator's H+μI_A equals H+2M
  (μ_i=|ζ_i|/s_i, s_i=2). In E6, `analysis.growth_certificate` matches the
  lemma (inward-gradient test, μ_i, exact LDLᵀ). On the 29 uncertified E6
  instances, H+2M is *exactly* not positive definite (pivot test in rational
  arithmetic, not only numpy), and the first-order conditions hold.
- S1 failure `random_path_n8_s7014`: the EX optimum −6575/108 is attained at a
  vertex, and flipping coordinate 4 (continuous, H_44=−7/2) gives the same
  value. So there are two optimal vertices differing in a concave coordinate,
  and point growth fails (outside Corollary `cor:local`).
- Numbers: E1 entries (1,026–1,049; 83,161; 64,879; 1,068–1,122). Lemma
  ratios: 0.155, 0.179, 4.69%, 0.375%. E2 plateaus 9→49; gaps 4.66/15.3/60.5;
  restarts 12 (κ_target 64, 128: one each; 256: two each). κ_lb/target ≥
  0.978, κ_ub/target ≤ 1.112. E3 7→26, 9→19, 9→17, and the separable formula
  at all six n. E6 table, brackets, 28 localized and 1 unproved, 27/40
  unchanged, spread ≤5, stages 7–9 → 27–29, 42/213, oracle 10/10, time column
  attained at q=50. Chain table, warm start (0.981–1.075, m=2: 6 nodes). E4:
  stages/bits groups, 21.3–315.0 vs 49.2–341.9 bits, limits 3,000 stages,
  30 s/5 s. S1: 29/30, indices ≤4 and ≤8, 12 full-box, 12 oracle, 40–72 and
  139–157, 542/534. E5 table, including SCIP times 5.4457 → 5.4 and 1.4485 →
  1.4, exact gaps 2.757–6.795·10⁻⁶, shortfall 1.82·10⁻⁶–1.61·10⁻⁵, incumbent
  excess ≤ 1.30·10⁻¹⁴. E5V: 39 runs, none contains F*; t60 duals −5.1·10⁻⁵ to
  −7.5·10⁻⁴. Recourse table, QPLIB (20/94, 5,723,918, 156 s, 4.4 GB, −234,
  7.96·10²⁸). Replay ratios 0.81–2.54.
- Figures: `figures/*.pdf` differ from `experiments/figures/*.pdf` only in
  `/CreationDate`. Figs. 1–2 show the cap line, the 4.2√(nκ) and √(nκ/8)
  lines, the 9/16 line, graded/uniform legends and readable ticks.
- CONVENTIONS: algorithm names and first-use references, "graded grid",
  "grading", "nodes per coordinate", "table entries", J_0, ℓ. There are no
  British spellings and no filler phrases.

### Commands run (targeted; CI not consulted)

| Command | Result |
|---|---|
| `python3 process/w3/checks/computation-verify-data.py` | κ brackets (min κ_lb 3.9985, max κ_ub 4.4487, ratio ≤ 1.1123), E2 final trials, E3 plateaus, separable formula: as stated |
| `python3 process/w3/checks/computation-verify-claims.py` (new; 20 s) | S1 tie confirmed; 29/29 uncertified E6 instances have H+2M exactly not PD; E6 times at q=50; SCIP raw times; 30/30 S1 replays valid |
| `python3 process/w3/checks/computation-verify-offgrid.py` (new; 2 min) | 153 on-grid = 146 descent + 3 zero + 4 dyadic offset, 0 unexplained; counts match saved results |
| `latexmk -pdf -interaction=nonstopmode -outdir=build/computation-verify main.tex` | exit 0; no error, warning, overfull or underfull box from `computation.tex`; no undefined reference or citation in the whole build; pages 71–78 inspected visually |

### Remaining

- Request 3 (front, `conclusion.tex` ll. 27–30) is still open. The sentence
  omits E6 and that QPLIB_3852 is now solved exactly. Suggested wording, which
  avoids implying that growth was certified on all E6 instances: "The
  experiments show accuracy-independent grid sizes on designed families and on
  unplanted random instances, including those on which growth could not be
  certified. On two binary QPLIB instances the method is plain dynamic
  programming: the one whose decomposition has bag size 20 is solved exactly in
  one stage, the other has bag size 94, so the width of the available
  decomposition, not the accuracy, is the binding limit."
- Request 4 (coreB, optional): no remark on θ=0 was added after Lemma
  `lem:commonmesh`. Section 11.2 states the extension together with its
  one-line justification, which I checked.
- As reported by the computation agent: the QPLIB_3852 certificate was not
  replayed; the chain and recourse tables come from the previous round's runs;
  growth is certified on only 11 of 40 E6 instances; the wrapper keeps the
  row-sum constant.
