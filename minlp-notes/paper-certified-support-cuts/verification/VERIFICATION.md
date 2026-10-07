# Targeted verification for the manuscript

All commands run from this directory with
`/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`
(Python 3.13.11, SymPy 1.14.0, python-flint 0.9.0, PySCIPOpt 6.2.1 with
SCIP 10.0.2) and `OMP_NUM_THREADS=1`. They are targeted checks of the
manuscript's claims; no project-wide test suite or CI was run. Finite checks
support the arithmetic and the implementation; the proofs in the manuscript
establish the quantified statements.

## Mathematical checks (2026-10-03, all exit 0)

| Script | Claims checked | Result |
|---|---|---|
| `M1_examples.py` | Example 5.4 and Example D.2, closure examples, joint versus separate envelopes | all checks passed |
| `M1_closure_random.py` | Theorem 5.2 and Proposition D.1 on random instances (exact LP) | all checks passed |
| `M1_rounding.py` | Proposition 6.1 (safe export), one-sided bounds | all checks passed |
| `M1_exactlp.py` | exact rational LP used by M1 | self-test passed |
| `M2_polytope_checks.py` | Theorem 4.1, degenerate cases, encoding bounds (Appendix B) | 964/964 checks on 153 random instances |
| `M2_simplex_rlt_psd.py` | simplex RLT/PSD example of the earlier draft | passed |
| `M2_crosscheck_impl.py` | polytope oracle implementation against independent enumeration | 177/177 agree |
| `M3_star_sweep.py` | Theorem 4.4: independent sweep, inherited oracle and exhaustive KKT enumeration | 400 cases, all values equal; breakpoint bounds hold |
| `M3_bounds_and_examples.py` | attained breakpoint counts, lower-bound family, gain corollary example | passed |
| `M3_irrational_breakpoint.py` | Remark 4.5 and Appendix C depth-two example | breakpoint 1 - sqrt(2)/2, minimum -3/8 |
| `M4_example.py` | Proposition 3.1, cut (path-cut), dense moment completion | all exact checks passed |
| `M4_family.py` | Theorem 3.2, identity (sdp-identity), Appendix A.1 multipliers, 4000 instances | all exact checks passed |
| `M4_alternation.py` | Theorem 3.3 and the separating polynomial of Appendix A.2, 8002 labelled cases | all exact checks passed |
| `M4_star_oracle.py` | Proposition 3.5 examples (gain versus glued gap) | passed |
| `M5_bernstein.py` | Lemma E.1 conversion formula | passed |
| `M5_chord.py` | Lemma E.3 | 150 cases passed |
| `M5_screening.py` | screening certificate of campaign 1 (Appendix G) and the Hölder pairing | 12000 pairs passed |
| `M5_domain_net.py` | Lemma F.3 | passed |
| `M5_separation.py` | Lemma F.1, Theorem F.2 (column generation with an exact master LP), grid covering | all separation checks passed |

| `M6_revision_checks.py` | re-splitting example and identity (Prop. 3.5(ii)), Helly example, kappa = 3 example, Prop. 3.4, D=[0,2] example of Sec. 5.3 (the docstring uses the numbering of the first revision: its Prop. 3.6 is Prop. 3.5) | all checks passed |

`M4_numeric_explore.py` is a floating-point exploration (LP and SDP
bounds), not a proof.

## Computational records

| Script | Purpose |
|---|---|
| `E1_audit_experiments.py` | recomputes the campaign-1, campaign-2 and repair-cohort numbers from the raw records (418 checks) |
| `analyze_v3.py` | campaign-3 and diagnostic counts (runs, solved, cuts, incumbents, time components) |
| `analyze_mechanism.py` | per-instance mechanism-family table (Table 7 and Table B.3) |
| `make_appendix_tables.py` | writes `../sections/B-tables.tex` from the records |

Replay of every recorded campaign-3 cut is in
`../experiments/v3/runs/*/replay.json` and
`../experiments/v3d/runs/*/replay.json`, produced by `replay_v3.py`.

## Campaign 4 (2026-10-03)

| Script | Purpose |
|---|---|
| `../experiments/v4/replay_v4.py` | replay of every recorded campaign-4 cut (C2, C3, C4, B2, D root, D full: 104,771 cuts, all passed) |
| `../experiments/v4/summarize_v4.py`, `summarize_c4.py` | campaign-4 metrics (`../experiments/v4/results*/`) |
| `campaign4_digest.py`, `campaign4_c4_digest.py` | digests `../evidence/campaign4-digest.md`, `campaign4-c4-digest.md` |
| `R8_path.py`, `R8_minlplib.py`, `R8_funnel_time.py`, `R8_c4.py` | independent standard-library recomputation of the digests (no producer code): 766/766, 338/348 (labelling slips only), 533/552 (run-set definition), 751/753 checks |
| `ablation_uncertified.py` | Part U ablation over all parts of campaigns 3 and 4 (`../evidence/ablation-uncertified.*`) |
| `ablation_slsqp_check.py` | why SLSQP leaves wrong constants (nvs02 tolerance, stationary starts) |
| `R8_ablation.py` | independent exact recomputation of the Part U counts and removals |

## Second review round and campaign 5 (2026-10-03/04)

| Script | Purpose |
|---|---|
| `M7_dense_fullgap.py` | dense first-level relaxation (SDP + all McCormick) on the four-variable path of Burer-Natarajan-Willemsen and on Proposition 3.4 with r = 1, 2, 3: rational feasible points checked exactly (PSD by LDL^T in Fractions, every McCormick inequality), values -0.122 (path; minimum 0) and below 1e-6 (r = 2, 3; minimum 1/2) |
| `R9_*` | second-round reviewer scripts (math, numbers, literature, implementation, writing, referee); reports in `../evidence/review2-*.md` |
| `ablation_global_solve.py`, `ablation_global_solve_spotcheck.py` | Part 5U: Gurobi global solve of every Part U support problem; spot check of 50 cuts in a fresh process |
| `../experiments/v5/test_v5.py` | campaign-5 runner tests (14 tests; defaults reproduce campaign 4; star blocks, block direction, star replay and tampering) |
| `../experiments/v5/replay_v5.py` | replay of every campaign-5 cut (5C-b 84,054; 5S 47,168, finished 2026-10-04 after 10,150 s; 5C-a has no cuts; all passed, tampering rejected in every cut mode) |
| `../experiments/v5/summarize_v5.py` | campaign-5 metrics (`../experiments/v5/results-*`) |
| `make_appendix_tables_v5.py` | writes `../sections/B-tables.tex` from the raw records of campaigns 3-5 |
