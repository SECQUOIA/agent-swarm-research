# R8: computational section and implementation claims

Reviewer role: verify every number in `sections/computation.tex` against the
experiment outputs, the implementation claims against the solver code, the
QPLIB statements, the SCIP comparison and the two figures, and say whether the
section supports the computational claims in the abstract, introduction and
conclusion.

Version reviewed: `sections/computation.tex` as of 2026-10-03 01:19, which
includes the new "Recourse" subsection and Table 3. The compiled PDF has this
section on pages 77–80.

## Verdict

Almost every number in Tables 1–3 and in the text of Sections 11.2–11.6
matches the CSV/JSON outputs. The exceptions are listed below (M1, M4, m6,
m7). The section supports the abstract's one computational claim, that the
predicted accuracy-independent grid sizes appear, on the families tested.
Seven problems need fixing before submission:

1. Several constants in the text and in Figure 2 come from an older version of
   the analysis. They do not match `growth.tex`. One claim, "in all
   theorem-compliant runs", is false for runs the paper itself reports (M1).
2. The dimension experiment (κ≈2) uses instances whose free coordinates are
   uncoupled. The polishing step finds x* before the first grid, and the
   "exact √n law" is the separable law (M2).
3. The exact-output wrapper does not use the Ω of Proposition 6.6; it uses a
   larger admissible constant. The "bits required" are therefore not the
   paper's. The comparison quoted in `exact-localized.tex` (≤4 stages versus
   up to 542) refers to an experiment that Section 11 does not describe, has
   an off-by-one error, and inflates the height rule's cost by a factor of
   4–10 (M3, M4).
4. The QPLIB paragraph is misleading. The code was the current release, not
   "a first release", and the refusal comes from an unstated 3·10⁴-state cap.
   With a 10⁷ cap, the unchanged code solves QPLIB_3852 exactly in 152 s (M5).
5. The SCIP comparison is described honestly, but there are two problems. The
   "gap reached" entries are SCIP's own claim: evaluated exactly, the gap was
   never below 10⁻⁶. The two solvers also had unequal time limits. My reruns
   show that the time-limit outcome is robust, so the authors can state this
   (M7).
6. The implementation differs from the analysis in more than the three ways
   listed, and some of the differences affect how the reported numbers should
   be read (M6).
7. The checker claims need qualifying. Decomposition validation is shared
   with the solver. The recourse "checkers" re-run solver code. Replay cost
   grows with the number of bags (M8, M9).

None of these makes a main theorem false, so there is no critical finding.

## Targeted commands actually run

All checks are in `process/w2/checks/`, with at most 4 processes. I did not
modify any experiment or paper file.

| Script | Purpose | Result |
|---|---|---|
| (inline Python) | recompute E1–E5 aggregates and table entries from `experiments/results/*.csv`, `summary.json`, `chain/results.csv`, `recourse/results.csv` | see the "Numbers verified" section |
| `r8_incumbent_start.py` | quality of the incumbent before the first grid stage on planted instances | κ_target=2: x0 = x* exactly; κ_target ≥ 4: no |
| `r8_chain_warmstart.py` | chain G_m with a warm start at the upper corner instead of ℓ = x* | same stages and node counts; 1–8% more states |
| `r8_scip_variants.py` | SCIP: paper formulation with 60 s on paths n ≥ 32; constant moved to an objective offset, 20 s, all 21 instances | still time limit on all 9 paths; primal bounds still below F* |
| `r8_scip_tight.py` | SCIP: feastol = dualfeastol = 10⁻⁹; absgap 10⁻⁵ | still time limit on all 9 paths n ≥ 32 |
| `r8_qplib_tables.py` | min-fill width and stage-0 table size for QPLIB_3852/5881 | width 19, 5.72·10⁶ states; width 93, 8·10²⁸ states |
| `r8_qplib3852_bigcap.py` | QPLIB_3852 with the unchanged solver and a 10⁷ cap | exact, value −234 (= −library value 234), 1 stage, 152 s; replay had not finished after 590 s (about 4 times the solve time) and was stopped |
| `r8_height_constants.py` | Ω used by `exact_output.py` versus Ω of eq:exact-constants on the E4 instances | code needs 49–342 bits; paper's Ω needs 21–315 bits |
| `r8_height_single_run.py` | stages one grid run needs to reach the height-rule threshold (S1 instances with the most stages) | 51–73 (paper Ω), 75–158 (code Ω), versus 275–542 reported |
| `r8_e3_coupled.py` | E3 design at κ_target = 4 (coupled free block), n = 8…128 | geometric 9→19, uniform 9→25/26; formula not exact |
| `r8_example_family.py` | Example ex:family (coupled indefinite blocks), Γ a path of m blocks | m = 32 (n = 96): certified 10⁻⁶ in 0.73 s, replay 1.0 s, optimum −3m/2 found |

These are targeted checks only. No project-wide verification was run.

## Numbers verified (no finding)

- **Table 1 (chain)**: all 48 entries match `chain/results.csv`, including
  stages, nodes, states, times and 2^{m−1}. The text's "5 to 11 nodes",
  "linear in m" (stages ≈ m + 10) and "first trial" are correct.
- **Table 2 (SCIP)**: every maximum solve, replay and SCIP time matches
  `E5_grid_runs.csv` and `E5_scip.csv`. The statuses match. "gap below 10⁻⁶
  on all 21" holds (gaps 2.3·10⁻⁷ to 1.0·10⁻⁶). The SCIP incumbents are
  within 1.0·10⁻¹⁵ to 1.3·10⁻¹⁴ of F* when evaluated exactly. Every dual bound
  is ≤ 0. The primal bounds lie 1.82·10⁻⁶ to 1.61·10⁻⁵ below F*.
- **Table 3 (recourse)**: every entry matches `recourse/results.csv`.
  "certified" for dense cut 33 corresponds to status `epsilon_optimal`.
- **E1 text**: 83,161 at stage 11; 64,879 at stage 6; about 1,000 states from
  stage 5; uniform plateau about 1,090; D ≤ 0.155 Lnh² (rounded to 0.16). All
  correct for E1. See M1 for the "all theorem-compliant runs" part.
- **E2 text**: 9→49 nodes (geometric, theorem θ). Last-stage ratios 4.66,
  15.3 and 60.5 are rounded to 4.7, 15 and 61. Final trials are 2/2/…/3/3/4,
  that is, first trial for κ ≤ 32, then one or two restarts. All correct.
- **E3 text**: the uniform plateau 9, 9, 13, 13, 21, 25 equals
  4(⌊√(n/4)⌋+1)+1 for all seeds; geometric runs give 9→19. Correct, but see
  M2.
- **E4 text**: 20 instances, 18 exact, all values and points correct; stage
  and bit ranges 67–144 for 49–120 bits, 275/534 for 208/342 bits; flat cases
  reach gaps 2^{−11.8} and 2^{−10.8} against required 2^{−52.5} and
  2^{−54.9}. Correct, but see M3 and m3–m5.
- **Recourse instance descriptions** match `completion/benchmarks/corpus.py`,
  except m15.
- **Implementation claims that are correct**: rational input only
  (`rational()` rejects floats); min-fill default (`decompose_qp`); empty
  separators (roots chained); corrections `max(A_ii,0)·w²/8`; endpoint grids
  for `A_ii ≤ 0`; two-pass DP with all min-marginals and messages
  (`finite_dp.solve_tree`); filtering `min(m_k, m_{k+1}) ≤ U` with hull; trial
  grading 2^{−μ}, μ = 2,3,…; cap 100·2^μ·⌈log₂(n+2)⌉; restart at the
  incumbent over the full box; two coordinate-descent sweeps; optional convex
  presolve (n ≤ 64). The checker recomputes tables and messages, checks
  Bellman equalities, min-marginals, exclusions, incumbents and the final
  status, and imports only `BoxQP` and `rational` from the solver.
- **Load and environment**: 248 s wall, 4 workers, load 10.9→15.5, Python
  3.13.11, SCIP 10.0, PySCIPOpt 6.2.1. The chain and recourse runs had load
  about 11. "11–16" is fine.

## Findings

### Major

**M1. Constants from an older analysis; the "all theorem-compliant runs"
claim is false** (`computation.tex:72–75`, Figure 2 caption `:80–84`,
`experiments/figures.py:113–118`, `summarize.py:36–41`).

`growth.tex:155–158` states that the common-mesh variant used by the code has
radius bound 4.2√(nκ) h_j and cap 8θ⁻¹⌈log₂(n+2)⌉. Lemma 5.3(iv) gives the
gap bound D(y_j) ≤ (9/16) L n h_j². The experiments and the figure use
5√(nκ) h_j, the gap bound 7/8, and the implementation cap 100θ⁻¹⌈log₂(n+2)⌉.

The sentence "In all theorem-compliant runs … the retained radius at most 0.12
of its bound, and the number of labels per coordinate at most 0.4% of the cap"
has four problems:

- `summarize.py` computes the maxima over the E1 geometric-filtered runs only.
- The E3 runs with the theorem's θ (θ = 1/8, κ ≤ 2.224, so 8κθ² = 0.28) reach
  a radius ratio of 0.1425 at n = 4, even against 5√(nκ_ub).
- Against the paper's 4.2√(nκ) bound the maximum is 0.17 (E1 alone: 0.135).
- "0.4% of the cap" compares with the implementation's cap, which is 12.5
  times the analysis cap. Against 8θ⁻¹⌈log₂(n+2)⌉ the maximum is 4.7% (E3),
  4.3% (E1) or 4.1% (E2).

The ratios also use κ_ub, the upper end of the certified interval, which makes
them smaller.

*Fix.* Recompute over E1, E2-geom_theorem and E3-geom_theorem with the
paper's constants and replace the sentence with: "In all runs with
8κθ² ≤ 1 (E1, and the runs of E2 and E3 with the theorem's θ), the gap D(y_j)
was at most 0.16 Lnh_j² (bound 9/16), the retained radius at most 0.17 of the
bound 4.2√(nκ)h_j, and the number of nodes per coordinate at most 5% of the
cap 8θ⁻¹⌈log₂(n+2)⌉." In Figure 2 (`figures.py`), change the bound line to
4.2√(nκ), the gap line to 9/16, and the legend to match the caption (see m1).

**M2. The dimension experiment uses uncoupled instances**
(`computation.tex:95–98`; `instances.py:95–100`).

For κ_target ≤ 2 the generator sets the coupling scale c = 0, so H_SS = 2I and
the free coordinates are not coupled to each other. The "path" with n = 16 has
7 of 15 off-diagonal entries nonzero, and n = 128 has 57 of 127. Every one of
them touches an active coordinate. In addition, the solver's initial
coordinate-descent polish returns x* exactly before the first grid stage
(`r8_incumbent_start.py`), so E3 measures only the lower-bound side. This is
why the uniform count follows the separable law of Proposition 8.19 exactly.
The κ=2 point of E2 has the same structure, which explains its uniform value
(13 nodes, larger than the 11 at κ=4) in Figure 2, left panel. My rerun at
κ_target = 4 (coupled) gives the same trends, geometric 9→19 and uniform
9→25/26 for n = 8…128, but not the exact formula.

*Fix.* Add: "For κ_target = 2 the generator sets the free–free couplings to
zero (H_SS = 2I); the free coordinates are then separable, the initial
coordinate descent already returns x*, and the uniform count equals the
separable count of Proposition 8.19 exactly. With κ≈4.4 (coupled free block)
the counts are 9→19 (graded) and 9→26 (uniform) for n = 8,…,128." The
cleaner option is to rerun E3 at κ_target = 4, which takes about 2 minutes.

**M3. The exact-output wrapper does not implement the Ω of Proposition 6.6**
(`computation.tex:25–27, 134–137`; `exact_output.py:15–37`;
`exact-localized.tex:3–4`).

`rational_heights` uses a different determinant bound: the product over
continuous non-fixed i of max(1, Σ_j |Δ′H_ij|). This is the row-Hadamard
alternative of Remark 6.5. The code's Δ′ also clears H_ij/2. The paper's
eq:exact-constants uses R = Δ ∏_{i∈I_C⁺} P_ii instead. The code's rule is
admissible, so validity holds, but it is not "the acceptance rule of
Proposition 6.6". On the E4 instances it needs 49–342 bits; the paper's Ω
needs 21–315. For example, random_band2_n6 needs 100 bits with the code's
constant and 38 with the paper's (`r8_height_constants.py`). The "49–120 bits"
and "208 and 342 bits" in the text, and the "2^{−50} to 2^{−350}" in
`exact-localized.tex:3–4`, are therefore values of the code's constant.

*Fix.* Either change `rational_heights` to the diagonal constant and rerun E4
and S1 (seconds), or write: "An exact-output wrapper implements the
acceptance rule of Proposition 6.6 with the row-sum height constant of
Remark 6.5, which is larger than (eq:exact-constants); with the constant of
(eq:exact-constants) the required gaps would be 2^{−21} to 2^{−315} instead
of 2^{−49} to 2^{−342}."

**M4. The localized-acceptance comparison is unsupported, off by one, and
inflated** (`exact-localized.tex:95–98`, citing Section 11; S1 data).

1. Section 11 does not describe S1 at all, so the cross-reference points to
   nothing.
2. `local_first_stage` is a 0-based stage index with maximum 4, so the test
   accepted within five stages, not four. README.md has the same error.
3. "the height rule needed up to 542 stages" counts all stages of
   `solve_exact`. That function restarts the grid solver from the original box
   for each precision q = 4, 8, …, 512 and checks acceptance only between
   rounds. On the five S1 instances with the most stages (275–542), one grid
   run reaches the height-rule threshold in 75–158 stages with the code's
   constant and 51–73 with the paper's Ω (`r8_height_single_run.py`). The
   localized test still wins (at most 5 stages), but by about 10–15 times,
   not about 100 times.

*Fix.* Add a short S1 paragraph to Section 11 (design: 30 random unplanted
MIQPs, n = 4…16, paths, trees and bands, 1–2 integer coordinates; result 29/30
accepted; failure: a tie; agreement with solve_exact and the oracle). Replace
the sentence in `exact-localized.tex` with: "In the experiments of
Section 11 the test accepted 29 of 30 random unplanted mixed-integer
instances within five stages; on the same instances one grid run reaches the
threshold of Proposition 6.6 only after 51 to 73 stages, and the restarting
procedure EX used up to 542." Alternatively, make the wrapper check
acceptance after every stage.

**M5. The QPLIB paragraph is misleading** (`computation.tex:220–226`).

The extra-benchmarks and completion/benchmarks records show the following.

- **"A first release of the code" is wrong for the widths quoted.** Widths 19
  and 93 come from the phase-two run (`completion/benchmarks`,
  `completed_grid`). That run used the same `certified_grid.py` (sha256
  b3fe4f…) and `decomposition.py` (40d3e5…) as the paper's experiments. The
  first release used minimum degree, with widths 25 and 95.
- **Undisclosed limits.** The runs used a 3·10⁴ per-stage table cap and a
  2-second limit; neither is stated.
- **The refusal comes from the cap.** For a binary QP, stage 0 has grids
  {0,1} with no correction, so the first stage is an exact DP. With min-fill,
  QPLIB_3852 needs 5.72·10⁶ table states. With a 10⁷ cap the unchanged solver
  certifies the optimum exactly, value −234 (library value 234 in max form),
  in one stage and 152 s (`r8_qplib3852_bigcap.py`). QPLIB_5881 (width 93,
  about 8·10²⁸ states) is out of reach. "Both runs stopped at the table limit
  before the first stage" is true only under the small cap.
- **Wording.** "The best decompositions found by the minimum-fill heuristic"
  should be "the decompositions found": there is one deterministic
  heuristic. The paper elsewhere uses bag size p, which is width + 1.

*Fix.* Replace the paragraph with: "The same code was also run on two binary
instances from QPLIB, QPLIB_3852 (231 variables) and QPLIB_5881 (120
variables). For binary variables the first grid is exact, so the method is
plain dynamic programming over the decomposition. The minimum-fill heuristic
gives bag sizes 20 and 94. With a cap of 10⁷ table states QPLIB_3852 is solved
exactly in one stage (5.7·10⁶ states, 152 s); QPLIB_5881 would need about
10²⁹ states. Large width, not the accuracy, is the binding limit; Section 10
shows that this is unavoidable in the worst case." Update the conclusion
(`conclusion.tex:24–25`) if needed.

**M6. The implementation differs from the analysis in more than three ways**
(`computation.tex:18–25`). Undisclosed differences that affect how the numbers
should be read:

- **Stage limit.** The per-trial stage limit J is computed from
  (7/8) L n s² 4^{−J} ≤ ε (`certified_grid.py:412–416`), not from Algorithm
  2's (9/16) n_P η_0² 4^{−J} ≤ ε. Trials can therefore last one stage longer.
- **E1–E3 do not run Algorithm 2.** They run one fixed-θ trial with
  `schedule="adaptive"`, `slope_decay_period=0`, no per-coordinate cap, a
  fixed number of stages (16, 12, 11) and ε = 2⁻⁸⁰ (`run_all.py:101–102, 127`).
  The "θ from theorem" is computed from the certified κ_ub, which the
  algorithm itself does not know. Only the E2 "capped schedule" rows, E5,
  the chain and the recourse runs use Algorithm 2.
- **Uniform mode is not UC.** "Uniform" grids are the θ = 0 single-center
  hull grids, not algorithm UC of Theorem 9.3, which uses unions of
  lattice-aligned cells without hulls. "as Theorem 9.3 predicts" (`:72`)
  therefore cites a different algorithm. The plateau of the single-center
  uniform grid follows from the localization argument of Lemmas 5.3–5.4 with
  θ = 0.
- **Polishing starts.** Polishing starts from three points: ℓ, u and the
  midpoint. This matters for the chain (x* = ℓ) and for κ=2 (M2).
- **Lower bound.** The reported lower bound is the maximum over all stages
  and trials, not β of the last stage.
- **Exact wrapper.** It starts at q = 4, restarts each round from the full
  box with the incumbent as warm start, adds a `limit_denominator`
  reconstruction candidate, and uses the constant of M3.
- **The cap never binds.** With the 12.5-times larger cap, no trial in any
  experiment was aborted by the cap. All restarts (E2, κ ≥ 64) were triggered
  by the stage limit J. The experiments therefore do not exercise the abort
  mechanism on which Theorem 5.5(b) relies.

*Fix.* Replace "It differs from the analysis in three ways" with a short
list, and add: "Experiments E1–E3 run single trials (Algorithm 1) with the
fixed θ shown and a fixed number of stages, with θ computed from the
certified upper bound on κ; E2's capped schedule, the comparison with SCIP,
the chain and the recourse runs use Algorithm 2. No trial was aborted by the
cap; all restarts were caused by the stage limit." Replace "as
Theorem 9.3 predicts" with "as the localization argument of Lemmas 5.3 and
5.4 with θ = 0 predicts".

**M7. The SCIP comparison: what "gap reached" means, unequal limits, and
robustness** (`computation.tex:143–179`).

The description is fair in tone and correctly disclaims a ranking. Four
things are missing or misleading:

- **"SCIP reached its gap"** is SCIP's own floating-point claim. With SCIP's
  incumbent evaluated exactly, the gap to its own dual bound was
  2.76·10⁻⁶ to 6.79·10⁻⁶ on all 12 "gap reached" runs, so the requested
  10⁻⁶ was never met. In all 21 runs SCIP's reported interval
  [dual, primal] lies strictly below F* = 0 and so does not contain the
  optimum. This is a sharper statement than the current "primal bound lay
  below the true optimum".
- **Unequal limits.** The certified solver had a 60-second limit
  (`run_all.py:372`), which is not stated; SCIP had 20 s. My reruns show the
  outcome does not depend on this:
  - with 60 s, SCIP still hits the limit on all 9 paths with n ≥ 32, with dual
    bounds −5.1·10⁻⁵ to −7.5·10⁻⁴;
  - with the constant moved to an objective offset, the shortfall is
    1.0·10⁻⁶ to 1.5·10⁻⁵;
  - with feastol = dualfeastol = 10⁻⁹, the shortfall is 2.2·10⁻⁷ to
    1.4·10⁻⁶, still below F*, and the status is still time limit;
  - with absgap 10⁻⁵, the status is still time limit.
- **Scaling.** The planted instances have inward gradients μ = 15.5 to 785 and
  objective constants 94 to 1,577 with F* = 0. The 10⁻⁶ absolute target is
  therefore about 10⁻⁹ relative to the data, which is near SCIP's
  tolerances. The reader should know this.
- **Dual bounds at the limit.** The table shows only "time limit" for
  n ≥ 32. SCIP's dual bound at the limit (−6·10⁻⁵ to −7.6·10⁻⁴) is
  informative.

*Fix.* Add columns "SCIP gap (exact)" and "SCIP dual bound", and add to the
text: "SCIP's reported gap is computed from floating-point bounds; with its
incumbent evaluated exactly, the gap to its dual bound was 2.8·10⁻⁶ to
6.8·10⁻⁶ on the instances with n ≤ 16, so the requested 10⁻⁶ was not reached,
and its reported interval did not contain the optimum in any run. The
certified solver had a 60-second limit; giving SCIP 60 seconds, tightening its
feasibility tolerances to 10⁻⁹, or moving the objective constant into an
offset did not change any status. The planted objectives have constants up to
1.6·10³ and F* = 0, so the absolute target 10⁻⁶ is a relative target of about
10⁻⁹." Change the Table 2 caption to state both limits.

**M8. The recourse "checkers" are not independent; replay cost needs
qualifying** (`computation.tex:38–39, 192–193`; `grids.tex:223–225`).

- **Recourse checkers.** `verify_convex_recourse` calls the solver's own
  `_grids`, `_tables`, `solve_tree` and `_filter` (`convex_recourse.py`, lines
  391–508). `verify_recourse.verify_pipeline` imports `transform` and `lift`
  from `recourse.py`, and `verify_mincut` lives in the solver module. The
  piecewise rows of Table 3 are therefore replays by solver code. They are
  not checks of the kind the paper stresses for the main checker.
- **Replay cost.** The main checker finds the home bag of every coordinate
  and pair inside the loop over table entries (`verify_certificate.py`,
  lines 133–145). Its cost is therefore about (#bags × p²) times the number of
  table entries. On the small experiments replay took 0.94 to 1.94 times the
  solve time (2.5 times for the 17-variable affine star). On QPLIB_3852
  (5.7·10⁶ states, 231 bags) the replay had not finished after 590 s, about
  4 times the 152 s solve, when I stopped it. "checking costs about as much as the
  successful run" (`grids.tex:224`) is not supported in general.

*Fix.* Write "each with its own checker; the convex value-factor and
recourse checkers reuse the solver's grid, table and lifting code, so only
the main checker is independent in the sense above." In Section 11 state:
"replay took 0.9 to 2.5 times the solve time in all runs reported here". Hoist
the home-bag lookup in `verify_certificate.py` out of the state loop
(a one-line change).

### Minor

**m1.** Figure 2 caption, middle panel: "the reference √(nκ)", but the figure
plots √(nκ/8). *Fix:* "the reference √(nκ/8)". The caption should also say
what "at the plateau" means: "maximum over free coordinates, median of the
last four stages and of three seeds", and that the x-axis is the target κ,
with the certified κ in [κ_target, 1.12 κ_target].

**m2.** Terminology: the section says "labels per coordinate" in four places
(`:16, 75, 88, 96`), while Table 1, the figures and Lemma 5.4 say "nodes".
*Fix:* use "nodes" throughout.

**m3.** `:129` "Twenty small instances were solved exactly", but two were
not. *Fix:* "Exact output was attempted on twenty small instances".

**m4.** `:135` "at most one stage for three instances with n=3": the reason
is missing. These three instances have no continuous coordinate with
A_ii > 0 (P = ∅), so the endpoint grid is exact; one is closed by the initial
interval bound with zero stages. *Fix:* add "these have no continuous
coordinate with positive curvature, so the first grid is exact".

**m5.** `:134–137` "The number of stages tracked the number of bits": the
stage counts are a step function set by the doubling of q. They are 67–77 for
49–65 bits (5 rounds, up to q = 64), 132–144 for 80–120 bits (q = 128), 275
for 208 bits (q = 256) and 534 for 342 bits (q = 512). *Fix:* "Because
the wrapper doubles q and restarts each round, the number of stages is about
the first power of two above the required number of bits: …".

**m6.** `:54` "Rational certificates give κ to within 11%": the maximum of
κ_ub/κ_lb is 1.112. *Fix:* "to within 12%". In Figure 1 and Table 2,
"κ≈4.4" is the upper end; the certified κ lies in [4.0, 4.45].

**m7.** `:89` "the retained radius grows like √κ": the measured log–log slope
is 0.36–0.41 (geometric runs 2.1h→15.2h for κ 2→256). *Fix:* "grows somewhat
more slowly than √κ".

**m8.** `:90` "the condition 8κθ² ≤ 1 fails for every instance": for
κ_target = 2, κ_lb = 2 exactly, so 8κθ² = κ/2 ≥ 1 may hold with equality.
*Fix:* "fails for every instance with κ_target ≥ 4".

**m9.** Chain (`:100–106`): the minimizer 0 is the lower corner ℓ, where the
implementation starts, so the incumbent is optimal from the start. With a
warm start at the upper corner the stages and node counts are unchanged
(m = 4…32) and the states grow by 1–8% (`r8_chain_warmstart.py`). Also,
θ = 1/4 succeeded although 8κθ² ≤ 1 holds only for κ ≤ 2 (here κ ≤ 80).
*Fix:* add one sentence on each.

**m10.** `:139–141` "this is the behaviour expected without growth": the
flat instances do have quadratic growth towards the optimal set (g_S ≥ 1/4);
what they lack is a unique minimizer. *Fix:* "this is expected when the
minimizers form a continuum: the instances have set growth, but no
accuracy-independent grid bound is known in that case (Remark 9.4), and only
termination is guaranteed (Theorem 6.11)". The flat runs also had a 5 s
limit, while the other E4 runs had 30 s; state both limits.

**m11.** SCIP citation (`:145`): the paper used SCIP 10.0 but cites the SCIP
8.0 suite paper. *Fix:* cite the SCIP 10.0 report (Hojny et al. 2025,
arXiv:2511.18580; in the literature base as
`hojny2025-the-scip-optimization-suite-10`).

**m12.** `:39–40` "a one-command reproduction script": `run_all.py` covers
E1–E5 and S1. The chain, recourse and QPLIB runs need three other scripts in
two directories. `instances.py:27` hard-codes `/workspace/local-home/...` as the
solver path. *Fix:* "reproduction scripts (one command per experiment
group)", and make the solver path relative.

**m13.** Overfull boxes: `computation.tex` paragraph lines 10–28 (17.8 pt,
`\texttt{fractions.Fraction}`) and Table 3 (10.6 pt). *Fix:* allow a break
or use `\small`/`\tabcolsep` in Table 3.

**m14.** Table 3 caption "times in seconds, solve and replay": the plain-grid
side shows only solve times. Their replays took 26.4 s and 50.9 s for the
affine stars, longer than the 20 s solve. *Fix:* add the plain replay column,
or say it is omitted.

**m15.** Recourse descriptions (`:184–189`):

- The affine-star core coordinate has diagonal +126 in the full objective.
  Only its own term −x₀² is concave, and the reduced function after
  elimination is concave.
- The piecewise instances are f_M − z², not f_M of Example 7.23 (the corpus
  adds `diagonal={0:-1}`).

*Fix:* "a core coordinate whose own term −x₀² is concave" and "the
function f_M − z² with f_M from Example 7.23".

**m16.** Figures:

- **Figure 1.** The panels have different y-ranges. *Fix:* add a horizontal
  line at the 10⁵ cap, and say in the caption that medians at later stages
  are over the seeds still running.
- **Figure 2, left panel.** The legend overlaps the top curve, and the log₂
  y-axis has only two ticks (2⁴, 2⁵), so the values 9–55 cannot be read.
  *Fix:* use a linear axis or ticks at 8, 16, 32, 64.
- **Figure 2, middle panel.** The bound line uses max κ_ub, while the
  reference line uses κ_target.

Both figures are otherwise legible at text width.

**m17.** `:42–46` "All runs below used …": the QPLIB runs came from another
benchmark (2 s limit, 3·10⁴ cap, different date). *Fix:* move the QPLIB
settings into the Limits paragraph (see M5).

**m18.** `conclusion.tex:21–23`: "a replayable certificate allows the result
of a floating-point solver to be checked". The experiments evaluate SCIP's
incumbent exactly; they do not check SCIP's bounds with a certificate. *Fix:*
"… allows a floating-point incumbent to be certified: its exact value
together with a grid certificate gives a rigorous gap".

## Experiments a referee would ask for (each feasible in minutes)

1. **SCIP with equal limits and exact gaps (M7).** 9 runs × 60 s ≈ 3 min with
   4 processes. Done in `r8_scip_variants.py` and `r8_scip_tight.py`; the
   result supports the paper's statement.
2. **E3 at κ_target = 4 (M2).** About 2 min. Done in `r8_e3_coupled.py`.
3. **Exact output with the paper's Ω and acceptance checked after every
   stage (M3, M4).** Seconds per instance; makes the localized comparison
   fair.
4. **QPLIB_3852 with a 10⁷ cap (M5).** 152 s; exact. Fix the replay hot loop
   first (M8).
5. **The paper's showcase family, Example 5.10 (coupled indefinite blocks
   with 2^m strict local minima).** It is not run. For Γ a path, m = 32
   (n = 96), the default solver certifies 10⁻⁶ in 0.73 s (replay 1.0 s) and
   finds the optimum −3m/2 (`r8_example_family.py`). Running Γ = k × m' grid
   graphs with k = 2, 3 would test bag sizes 3–4 on an instance family the
   paper did not design for the experiments.
6. **The chain with a warm start away from x* (m9).** Seconds; done.
7. **Abort by the cap.** A run of E2's capped schedule with the analysis cap
   8θ⁻¹⌈log₂(n+2)⌉ would show whether any trial is aborted by the cap (M6).

## Does the section support the claims elsewhere?

- **Abstract**, "An exact-arithmetic implementation with an independent
  certificate checker exhibits the predicted accuracy-independent grid
  sizes": supported by E1 (plateaus over 16 stages), E2 and the chain. Two
  qualifications: the families are benign (M2, m9; planted x* with steep
  inward gradients), and "independent" holds for the main checker only (M8;
  it also shares decomposition validation, see below).
- **Introduction `:83–85`** (gap 10⁻³ at m = 64 with at most eleven nodes):
  supported.
- **Introduction `:165–167`** ("experiments confirming the predicted grid
  sizes"): supported as above.
- **Conclusion `:24–25`** ("the width of the available decomposition, not the
  accuracy, is the binding limit"): plausible, but the QPLIB evidence as
  stated is an artefact of the cap (M5). Restate it as in M5.
- **Conclusion `:21–23`**: see m18.
- **`exact-localized.tex:3–4, 95–98`**: not supported as written (M3, M4).
- **`grids.tex:224`** ("checking costs about as much as the successful
  run"): holds only for the small instances (M8).

A further, smaller point on the main checker. `computation.tex:31–34` says
the checker "validates the decomposition … it shares only model parsing and
objective evaluation". Decomposition validation is the solver's own
`BoxQP._validate_decomposition`, run when the checker parses the model, and
the checker's docstring says so. *Fix:* "it shares model parsing,
decomposition validation and objective evaluation with the solver".
