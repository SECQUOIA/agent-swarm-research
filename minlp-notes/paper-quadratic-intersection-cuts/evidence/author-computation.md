# Computational section: coverage and evidence mapping

Owned manuscript files: `sections/08-computation.tex`, `appendices/F-evidence.tex`. Main section labels `exp:section` and `exp:computation` name the same section. This report and `audit-computation.md` are internal evidence documents, not manuscript prose. No existing research note or experiment code was changed. No optimization experiment was rerun.

## Final disposition

| Source development | Disposition in the paper | Evidence class and limit |
|---|---|---|
| sfree support statistics (888), two-variable orbit checks (24), point-rule misses (13/36), global-solver validation | F, `exp:minor-diagnostics` | Numerical diagnostics; four infinite cases excluded from 40-trial point-rule population; no theorem follows from counts. |
| sfree one-cut McCormick cohort 47+73 | 08 `exp:one-cut`, Table `exp:one-cut-table`; F `exp:ten-corrections` | Corrected numerical table; different one-term denominator from multiround. |
| Ten infeasible antiparallel-ray corner values | F `exp:ten-corrections`, Table `exp:correction-table`; 08 explains effect | Retained rational-check reports; conservative outward display; complete saved witness replay is not promised. |
| Original sfree root loops 12+10; objective-parallel stalling | F `exp:ten-corrections` | Historical cohort retained with corrected original-script and fast-runner trajectories distinguished. |
| Old Case-4 nonzero κ transcription | 08 `exp:fidelity`; F `exp:corner-oracles` | Formula correction. Old finite-only conditional 17,584/19,376 rate excluded because cutoff/cohort differ. |
| 610,193 fidelity comparisons / 1,211 exceptions | 08 `exp:fidelity`, Table `exp:diagnostic-table`; F `exp:corner-oracles` | Relative-step numerical matches; 107 bisection diagnoses not exactly reproduced; monoidal coefficients not independently reconstructed. |
| MINLPLib sampled/complete cohorts and numerical zero faces | 08 `exp:fidelity`; F `exp:populations` and Table `exp:thresholds` | Adaptive two-stage sample, 4,785 sampled attempts/4,578 ray records; zero-rate threshold explicit. |
| Positive-corner ratios and per-instance weighting | 08 `exp:fidelity`; F Table `exp:oracle-table` | 1,067 reduced-space numerical records; 602/233/176/46/10 oracle classes; no global certificate for higher-dimensional cohort. |
| Four waterund32 exceptional zero-rate rays | 08 `exp:fidelity`; F `exp:corner-oracles` | Exact dumped-value restrictions; unresolved true-corner drift; exclude established geometric-gap interpretation. |
| Exact waterund25 feasible point | F `exp:corner-oracles` | Feasible upper bound, not a global optimum certificate. |
| Full rejection split and first-piece ray scaling | 08 Table `exp:diagnostic-table`; F `exp:corner-oracles` | Attempt counts, analytic cut invariance, numerical piece passes; no rescued-cut or rounding-noise causal claim. |
| Generated-cut counters/reset and reversed Boolean descriptions | F `exp:corner-oracles` | SCIP 10.0.3 source audit; implementation provenance specified. |
| Recorded cut entry rates | 08 `exp:fidelity`; F `exp:corner-oracles` | Lower bounds on LP observations; missing/intermediate entry cannot be inferred. |
| Root selection three seeds and strengthening | 08 `exp:selection`, Table `exp:root-table`; F `exp:debug` | Within-seed numerical root-gap comparisons; 251/250/248 denominators; strengthening exploratory. |
| Direction-search quality/cost and offline free-λ tests | F `exp:debug`; heuristic design in08 | 24-direction/local or subgradient search; old 102/120 attainment count excluded because uncorrected zK; LP columns remain denominator-independent. |
| Full-scan floored criterion degeneracy | 08 `exp:selection`; F `exp:debug` | 305 summaries/109,389 corners, 89,307 zero-ray minima; distinct from fidelity face test. Raw dumps and per-instance statuses missing. |
| Original full solve 480 rows and stock 120 reruns | F `exp:debug` plus08 withdrawal | Historical solved counts retained; CPU advantage and instrumentation CPU attribution withdrawn; not a stock enabling prescription. |
| Debug-solution 300 grid, helper correction, residual diagnostics | 08 `exp:selection`; F `exp:debug` | 170 optimal/129 limits/one failure; 73 rows resolved with corrected helper; no clean whole-run validity certificate. |
| Earlier symmetry debug grid, tricp rerun, kall references | F `exp:debug` | Incomplete43-log population and unresolved messages; no ordinary seed0 benchmarks or unperformed primal checks claimed. |
| Larger 220-instance paired multiround experiment | 08 `exp:multiround`, Table `exp:multiround-table`; F `exp:policy-details` | Corrected main/new trajectories, cached denominator checks, paired intervals, flooring and clipping explicit. |
| Bug effect and withdrawn40% attribution | 08 `exp:multiround`; F `exp:ten-corrections` | Early-round effect retained; later effect nearzero; withdrawn causal attribution omitted. |
| State interventions, ties, steps, maj2/random control | 08 `exp:multiround`; F `exp:policy-details` | Exploratory causal evidence; exposure differs; numerical tie proxy; same-state LP dominance wording excluded. |
| o1s external single-orbit-root switching | 08 `exp:multiround`; F `exp:policy-details` | External loop only. Actual orbit-LMI SCIP candidate explicitly was not implemented. |
| Post hoc efficacy policies and recovery | 08 `exp:multiround`; F `exp:policy-details` | Holm14 and12/36/33 families, test sensitivity, fresh-data requirement; no equivalence inference. |
| Uniform-depth convergence and counterexamples | Mathematical sections07/E owned by minors/convergence;08/F empirical applicability caveat | Proof distinct from finite small pointedness proxies; no natural-rule failure theorem inferred from adversarial sequence. |
| Minor fixed(2,2) random600+300 diagnostics | F `exp:minor-diagnostics` | Finite numerical attainment/support/tangency; incomplete apex/ray retention noted. |
| Minor258 cut matches /157 LP corners | 08 `exp:one-cut`; F `exp:minor-diagnostics` | Coefficient and RHS errors separated; Ipopt guard/build stated; mean nearest-SCIP advantage not established. |
| MinorA/B/S1 exact examples; PR/rotation brackets | Mathematical06/D owned by minors author; F archived bracket table | Coarse portable exact matrices inD; fine A/S1 endpoints lack saved witnesses; complete B fine witnesses retained. |
| Minor24 rounded certificates and rational searches | F `exp:minor-diagnostics`; audit numeric corrections | One-sided exact-check reports plus numerical lower values; rounded upper displays corrected; no24 two-sided comparisons. |
| Ratio depth proofs and five sharpness box data sets | Mathematical04/B owned by depth; F `exp:companion` | All required completed leaf lists and current verifiers in companion; line count distinct from leaf count. |
| Near-boundary0.028 correction to[.03052,.03056] | F `exp:companion`; internal audit | Binary-float exact-check report, missing retained upper dual matrices; no solver-free saved-data replay promise. |
| Ratio-family ε progression, normalized coefficient calibration,15,731fixed-rule sample,150support-one checks | F `exp:minor-diagnostics`; mathematical calibration inB | NumericalA/heuristicB columns, fixed-condition12.0136 calibration; sample minima0.0140/.2397/.1823 are not worst-case guarantees; borderline SDP cases retained. |
| False-bound MAXDEPTH searches and heuristicB lower values | F `exp:companion`; internal audit | Failed searches, not certificates; exact feasible sets explain failures; generic heuristic outputs remain numerical. |
| Closure theorem/certificates/60saved cuts | Mathematical05/C owned by closure; F `exp:companion` | Full saved exact data and present verifier safeguards; safe lower displays handled by closure author. |
| Closure surveys, unfinishedB/BP attempts, rebasing | F `exp:companion`; internal audit | Numerical11/7survey populations; incomplete certificates excluded; analytic W proof supersedes stopped diagnostic; objective-bound/feasible-vertex counts separated. |

## Source and version mapping

Primary computational notes are the six `research-20261001/{scip-rule-fidelity,scip-set-selection,multiround,minor-sets,ratio-bound,orbit-closure}/note.md` files, the starting `research-20260928b/sfree/optimal-intersection-cuts.md`, their reviews, compact records, and final `research-20261001/CLOSEOUT.md`. `companion-inventory.json` records hashes and original sizes; the selected companion manifest gives per-file package identities. The source commit at audit start was `5c13cc58f7f4cebbe54e496c7b04cc6c30901261`; current hashes identify the actual files, without implying frozen run-specific versions where none were recorded.

| Population | Source identity | Principal retained record paths |
|---|---|---|
| Fidelity | Saved SCIP10.0.3 GitHash `d409edf9f6`, SoPlex8.0.3 GitHash `13e2ab24`; Release/GMP/LAPACK on, Ipopt/PaPILO off | `scip-rule-fidelity/logs/an_mc11.jsonl`, `an_mc12.jsonl`, `an_minlplib/`, `an_minlplib2/`, `index/`, `check_revision_r2.log`; dump patch retained. |
| Corner correction | Seed11/12 generator; saved rational checks and separate corrected floating re-solves | `scip-rule-fidelity/logs/certify_two_ray_{11,12}.log`, `recheck_note_affected_{11,12}.log`; `multiround/logs/recheck_mccormick_{11,12}.log`. |
| Selection root/full/debug | SCIP10.0.3 patched point/corner/eff settings and stock rerun; distinct seeds/build/batches | `scip-set-selection/logs/{root,rootseeds,full_analysis,debugsol_analysis,stock_analysis_r1}.json`, `degeneracy_root.jsonl`, cohort text lists. |
| Multiround | Generated caches seeds1001–1004; live sibling sfree imports; floored weights | `multiround/data/inst_{4x4,6x8,8x12,10x20}.json`; `logs/main/*.jsonl`, `logs/new/*.jsonl`, `summary_pooled.log`, controls/summary logs. |
| Minor | PySCIPOpt6.2.1 /SCIP10.0.3 /Ipopt3.14.19; standalone no-Ipopt behavior distinct | `minor-sets/logs/exp_random_N*.jsonl`, `exp_lp_{3x3,4x4}.jsonl`, `scip_fidelity_*.log`, `certify_*.log`, `reviews/r4-logs/r4_minor.log`. |
| Depth | Exact rational box leaf data; old header and current-header rerun mapped | `ratio-bound/logs/zB_cert/leaves*.jsonl.gz`, `logs/rev1/leaves_rho137_rerun.jsonl.gz`, `compare_leaves_rho137.log`, `certify_lower_found.log`. |
| Closure | Current standalone verifiers and complete certificate JSON | `orbit-closure/logs/boxcert_thm14*.json`, `closure_cert*_A*.json`, `revision-r1/closure_lower_prop16_cuts.json`; stopped datasets indexed as excluded. |

Recorded experiment stack: Python3.13, NumPy2.5.1, SciPy1.18.0, CVXPY1.9.3, Clarabel0.11.1, SCS3.3.1, SymPy1.14.0, highspy, PySCIPOpt6.2.1. Some substreams omit individual version pins. Gurobi records require separate solver/license provenance. Literature versions are documented by the sole literature author; no literature search occurred in this work. Source manifests distinguish the SCIP source snapshot and preprint/report versions from journal references.

The original raw fidelity traces remain separately preserved:48 gzip members, total2,199,648,289bytes; archive2,193,209,777bytes, SHA256 `81a2a2a07c08b0137364f40ebbd5d438f4de2e62026af4d044e6f49cb9a816a9`. All48 local hashes and sizes match the existing member index. Neutral wrapper metadata points to the repository's original evidence index for restoration information, without inventing a public DOI or exposing author URLs in new metadata.

## Companion and verification

The selected archive preserves repository-owned code/records/certificates with their original bytes. Its neutral wrapper does not sanitize author paths/URLs already inside originals and does not claim full anonymity. No third-party literature, MINLPLib input/solution, solver installation, or new redistribution license is included. Generated multiround inputs are repository-created random models and are included with their reference denominators. Source notes/CLOSEOUT are inventoried as context rather than included in the default payload.

Targeted checks: read-only standard-library JSON/JSONL/gzip parsing and metadata/hash checks; delegated exact rational certificate arithmetic; isolated LaTeX compile of 08/F with shared macros. The first isolated compile succeeded but identified three overfull lines, which were rewritten. Final targeted compilation passes with no overfull boxes (10-page temporary document); four undefined-reference warnings concern sibling files omitted from that document. Companion verification validates hashes, record counts, completed certificate metadata and paired denominators only, with no experiment or solver execution. No project-wide local verification or CI inspection was performed.

Commands actually run for the authored outputs:

- `pdflatex -interaction=nonstopmode -halt-on-error -output-directory /tmp/quadratic-computation-tex-v46yvn0a /tmp/quadratic-computation-tex-v46yvn0a/check.tex`: the temporary driver inputs shared macros and only 08/F; exit 0, no overfull boxes in the final check.
- `python3 paper-quadratic-intersection-cuts/companion/check_manifest.py`: exit 0; eight wrapper identities and payload-manifest hash pass; 1,397 payload files, 1,393 original files, 74 primary trajectory files, 5,160 trajectories, 220 baseline instances and cached denominators pass.
- `python3 paper-quadratic-intersection-cuts/companion/inspect_archive.py`: delegated archive-only check passes; hashes, members, neutral archive owner/timestamps, and exclusions pass, without solver or proof replay.
- Inline `python3` readers: inventory JSON parses and all 1,405 referenced source/package identities match sizes and SHA-256; cohort/transcription and leaf/piece checks are described in the computational audit.
- `git diff --check --` the owned 08/F and three evidence files: exit 0; targeted whitespace check.

Final companion payload is 1,393 original files / 80,680,117 bytes, plus neutral metadata. The completed compressed archive is 12,387,186 bytes, SHA-256 `f027b4f952f8ba25d3a291d59bb12c2bccf52702498145e87975c0bba0e9e0e6`; the lead selected a byte-for-byte delivery copy named `delivery/quadratic-intersection-cuts-companion.tar.gz`. This report does not claim a new experiment, mathematical replay, redistribution license, or full anonymization of original internal strings.

Final integration repair: the neutral `companion/archive/survey-labels.json` and companion README map R1–R8 to source names and 12 retained coordinate/result rows. Metadata was rebuilt, preserving all 1,393 original-file hashes and their 80,680,117 bytes. The archive now has 1,398 members; the payload manifest inventories 1,397 files / 80,710,667 bytes. Top-level hash/cohort/mapping checks and archive inspection pass. The earlier comma-spacing cleanup split thousands separators in F; all affected integers were repaired, and the targeted module compile still passes without overfull boxes.
