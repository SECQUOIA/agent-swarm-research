# Independent review 03: stage 6, round 1

**Verdict: no major issues and no valid minor issues identified in this stage's authoring and integration scope.** The new claims, numerical results, source comparisons, and manuscript presentation withstand the checks below. No correction is requested.

## Scope and preservation

I reviewed the complete new abstract and introduction, computation section, discussion, new classical small-mode comparison, appendix placement, bibliography, figures/tables, stage 6 programs and records, complete runner, README, and the permitted coverage map/inventory. I read relevant earlier theorem statements and proof dependencies as needed. This is not a replacement for the separate forthcoming whole-manuscript proof review.

A direct comparison against `stage05-accepted` shows that the former higher-reach section is moved **byte for byte** to `sections/14-higher-reach.tex`. Apart from its removal and the explicitly added classical comparison in section source 07, all pre-existing mathematical section files are unchanged. The appendix's unresolved five-block scope and its one-chamber certificate remain clearly separated from established universal results. All 161 frozen-manifest hashes matched before verification and after this review. No snapshot or manuscript file was edited. I did not consult other current reviewer reports or root/author assessments.

## Mathematical findings: no required corrections

### Headline statements and narrative

Locators: `main.tex` abstract; `sections/00-introduction.tex`, especially `eq:intro-main`, the following asymptotic formula, `tab:results-synopsis`, and the discussion of finite-grid and transfer scope.

The main formula is restricted to `0<=s<=3` and `n>=s+2`, consistently with the earlier theorem. I independently checked the geometric-term transition counts 5, 8, and 12. The introduction distinguishes the one-sided uniform term, the full minimax value, and input-wise discretization gaps. It does not present the uniform one-sided term as the full error of that input in every parameter regime. The general asymptotic formula has the correct fixed-block-count first correction. The three-mode boundary claims are the proved `F(3,2)=T/5` and the band `T/7<=F(3,3)<=T/6`; no exact three-switch continuous value is implied.

The explanation of heavy-mode reduction, the necessary event LP and all-mode certificate coverage, repeated competing modes, and the spare-mode restriction agrees with the earlier development. The synopsis, discussion, and figures use the same scopes. The text does not promote the single chronological chamber, the failed relaxation, or a numerical sample into a general reach theorem. The larger open questions are stated as research directions, rather than missing premises in established results.

### New classical consequence

Locator: `sections/07-predecessors-and-frontier.tex:108–119`, `eq:classical-small-mode` (printed equation 84).

The estimate `F(n,k-1)(T) <= ((2n-3)/(2n-2))*T/k` is a correct application of the cited unrestricted CIA bound on `k` equal cells. Its rounding schedule automatically has at most `k-1` switches. Endpoint monotonicity makes cell averaging preserve the error against the original measurable control. This argument works for all stated `n>=2,k>=1`, including `k>=n`. The source's separate tightness condition does not restrict its upper bound; the manuscript correctly avoids importing that tightness into the continuous hard-budget problem. Algebraically, this comparison is strictly better than `T/(k+1)` exactly when `k>2n-3`, so the prose about sufficiently large `k` is accurate.

I checked the source equation and its hypotheses directly in [Zeile–Robuschi–Sager, Corollary 1](https://link.springer.com/article/10.1007/s10107-020-01533-x). The formula and the separate condition `N>=n-1` for tightness match the manuscript's interpretation.

### Public continuous optimum and input transformation

Locator: `sections/12-computations.tex:13–49`, `eq:public-continuous`; `verification/stage06/experiments.py`, `public_input` and `continuous_one`.

The pinned CSV contains 12,001 time nodes and 12,000 equal cells on `[0,12]`. Its rates are interpreted as constant on each following cell. The manuscript explicitly distinguishes the normalized decimal profile, its quantized simplex profile, and the original unnormalized columns. Largest-remainder quantization preserves nonnegativity and the row sum, and its strict per-component rate bound gives the stated cumulative bound `delta=12/10^6`. Independent parsing and normalization reproduced all recorded exact perturbation maxima and all derived grid masses.

For each ordered pair, `2t-A_p(t)-T+m_q` is strictly increasing, is nonpositive at zero, and nonnegative at the horizon. Its unique crossing minimizes the maximum of the increasing and decreasing terms; the omitted mass is constant. Constants are covered as endpoint schedules of a pair, so no omitted zero-switch competitor invalidates the minimization. The code's signs and affine interpolation match the discrepancy objective.

I independently minimized the entire maximum of the signed switch and terminal endpoint affine forms in every input cell, taking all pairwise affine intersections and cell edges. This method does not call or copy the specialized two-term crossing routine. All six resulting pair optima agree exactly with the archive. The global continuous optimum is `4721469/2500000`, the fine-grid optimum is `1889/1000`, and their exact difference is `1031/2500000 < 1/2000`. The stated mode order and schedule are independently feasible and have the asserted error.

### Coarse grids, certificates and comparisons

Locators: `sections/12-computations.tex:51–101`, `tab:public-profile`, `tab:public-certificates`; stage 6 data and renderer.

Every table row compares the same original quantized input on one fixed grid for all budgets. The 12-, 24-, and 48-cell boundaries are nested and are all contained in the 12,000-cell grid. Thus the coarse optimum is an upper bound for both the continuous and fine-grid instance optima, while the transfer lower bound applies to both. The displayed intervals have correct endpoints and strictness; in particular, the negative raw lower endpoint for the 12-cell/three-switch case is clipped to a closed zero endpoint. The source-perturbation enlargement uses the correct two-sided `delta` adjustment. The one-switch half-mesh and zero-switch exactness refinements are correctly distinguished from the general certificate.

My independent integer cell-count-state optimizer confirms all twelve public coarse optima, including every 48-cell case. It stores occupied-cell counts, last label and actual changes, and minimizes the maximum prefix error over histories with that state. This is a different exact recurrence from the author's fixed-block subset assignment. At a fixed state, future service possibilities are identical, which justifies keeping the history of least maximum error.

### Uniform benchmark, timing and plots

Locators: `sections/12-computations.tex:103–194`, Figures 1–2, Tables 6–7.

The new direct proof of the uniform three-mode/two-switch **instance** optimum `1/6` is sound. With at most three blocks, either a mode is omitted, costing `1/3`, or each mode occurs once. The last mode gives `E>=max(v/3,2/3-v)>=1/6`. The displayed switches `1/4,1/2` attain the bound. This avoids applying the earlier `k<n` uniform theorem outside its range. Independent exact cell-state optimization reproduces all nine plotted grid values, including the nonnested increase from `M=4` to `M=5`.

The deterministic controlled instances match the specified modular formula. Independent enumeration of actual cell words, without padded block enumeration or subset-cost calls, confirms all three controlled optima. The table's larger word counts are correctly labeled as labeled-word/boundary cases including repeated labels, not distinct physical schedules.

I checked all 26 archived timing records: each median is the median of its three nonnegative recorded samples. The timer excludes construction and subsequent verification, includes solver validation, and uses equal instance/grid/budget objectives for the matched methods. Both CPU and wall samples and the shared-host limitation are explicit. No asymptotic complexity, superiority to an established CIA solver, nonlinear trajectory quality, or closed-loop guarantee is inferred from these measurements. The figures show the stated formulas or exact data; connecting discrete points is explicitly described, and nonnested monotonicity is not implied.

## Independent verification performed

Artifacts are confined to `verification/reviewer03/stage06-round01/`.

- `independent_checks.py` imports **no manuscript optimization routine**. It verifies the pinned CSV hash, parses exact source numbers, reproduces quantization and all 84 derived coarse cells, scans all fine-grid one-switch endpoint schedules, solves six continuous piecewise-affine envelopes, and checks all public coarse optima by the independent state recurrence. The public DP visits 142,503 states in total: 2,349 at 12 cells, 16,773 at 24 cells, and 123,381 at 48 cells.
- It independently checks 297, 844, and 1,137 distinct budget-feasible controlled cell words, confirming optima `175/1056`, `622257/3069248`, and `1816751/16336320`. It also checks all nine uniform convergence points, the three exact regime transitions, the classical comparison threshold for a finite range as an algebraic sanity check, and timing-summary arithmetic. All checks pass; detailed values are in `independent-results.json`.
- The public CSV was retrieved into my own directory from the pinned URL, with the expected SHA-256 `1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883`.
- I ran the complete author `experiments.py --data ... --output ...` from the relocated bundle. Every exact result, schedule record and derived mass agrees with the archive after excluding timing/environment fields. This reproduces the fine source checks that the offline suite explicitly cannot perform.
- I ran **all** of `verification/run_all.py` in the relocated copy. All proof/certificate, integrity, exact algorithm, archived experiment, and generated-text checks passed. The runner's claim of offline operation is consistent with its code; fetching fine source data is separate and explicit.
- A clean relocated `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` build generated a 56-page PDF. The final log has no warnings, undefined citations/references, or overfull/underfull boxes. I visually inspected the new introduction, figures, synopsis, computations, discussion, and appendix transition using pages 1–5 and 47–52 rendered from that build. Text, equations, table precision, legends, and cross-references are readable and unclipped.

## Literature, coverage and limitations

The introduction's attribution is appropriately scoped. I checked the local primary text for Sager–Jung–Kirches (switch-constrained CIA formulation and branch and bound), Knuth (integral flow for partial-sum rounding), the SUR paper, compactness/convergence paper, adaptive SCARP preprint, and the state-error theorem/corollary. Their cited roles agree with their settings. Earlier precise transfer-source records are retained without expanding their claims.

The current [primary publisher introduction of Abbasi-Esfeden et al.](https://www.sciencedirect.com/science/article/pii/S0959152425001507) explicitly states the loss of optimal substructure and absence of a general global-optimality guarantee. The manuscript's methodological distinction is supported; I did not audit that paper's complete algorithm or experiments. The bibliography preserves the stated issue-year/preprint distinctions and does not assert broad priority.

The allowed source-to-result map gives a disposition for each substantive result in the permitted repository inventory: retained, subsumed by a stronger theorem, developed further, or explicitly open. Its mapping agrees with the integrated manuscript. I did not re-read every historical investigation or review, and I make no exhaustive literature-priority claim. The Python run used 3.13.11, so older advertised interpreter versions were not independently executed. The new exact programs and all archived checks passed in the supplied environment; timing magnitudes themselves are not expected to reproduce exactly on a shared host.

No valid major or minor issue was identified. The pending whole-manuscript proof review remains necessary under the requested process; this favorable stage verdict does not substitute for it.
