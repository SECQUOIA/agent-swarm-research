# Checker paths, commands and run records

This file belongs to the claim register of the supplement (Section S7.3,
`tab:repro-register`), which gives for each result only the file names of its
checkers, the recorded time, the tier, the evidence level, the status and the
trust-base terms. For every register row, the block `R01`–`R27` below gives, in
the same order, the paper labels, the full checker paths with their arguments,
the command that the claim index (`claims.json`) records, the expected output,
the recorded time and the folders of run records. `build_claims.py` reads the
blocks by row number and checks that both files have 27 rows with the same
labels; `check_claims.py` checks this again.

Conventions:

- Paths are relative to the root of the archive: `$R` is its folder
  `research-20260929/`, `$P` its folder `paper-open-minlplib/`. A bare file name
  lies in the folder of the preceding path. Arguments in angle brackets name an
  instance (`<name>`), a size (`<N>`), a horizon and period (`<T> <t>`, with
  `<TT>` the two-digit horizon) or a point.
- `$SCRATCH` is a disposable output folder. Run every command in the disposable
  copy `$WORK` of Section S7.1 (`README.md`, "Environment and input roots").
- Times are recorded wall times on a shared machine, not guarantees; tiers
  follow Section 10 of the paper (Tier 1 under 10 minutes, Tier 2 under one hour,
  Tier 3 longer, per instance and summed over its parts). A row's tier is that of
  the replay of its displayed result by the checkers named first; the 2nd can
  take longer (row R06).
- "2nd" is the other implementation and what it certifies (Section 2.6 defines
  first and second implementations). For `optcdeg2`, `lukvle10`, `catmix`,
  `etamac`, `pindyck` and the `emfl` enclosures the 2nd is the first
  implementation, which certifies a weaker bound or a wider enclosure; for
  `ex6_2_5`, `ex6_2_7` and `pricing050` it is a third code.
- "Round 1", "round 2" and "round 3" (as in "the round-3 sources") name the
  authors' internal review rounds before submission (`README.md`).
- `Records` lists folders and files of run records that the claim index hashes
  in full; a folder under `Checkers` contributes its Python files.

Earlier and superseded certificates and displays, including strings in older
records that must not be read as bounds, are in `HISTORY.md`.

## Register rows

### R01. Exact optima of the four lnts models

- Labels: `thm:lnts-opt`
- Checkers: `$P/development/reviews/code/sol-lnts-review/verify.py`; 2nd:
  `$P/development/dossiers/checks/lnts-lukvle10/lnts_exact_opt.py` with arguments
  `50 100 200 400` (same optima).
- Command: `python3 "$P/development/reviews/code/sol-lnts-review/verify.py"`
- Expected output: the "PASS" line; rational enclosures of N h* of width below
  1.11e-91; L and U as in `tab:closures`.
- Recorded time: seconds per instance.
- Records: `$P/development/reviews/code/sol-lnts-review/`

### R02. Exact dtoc5 primal and rational dual bracket

- Labels: `thm:dtoc5-bracket`
- Checkers: `$P/development/reviews/code/sol-dtoc5-review/review.py` (full
  rational q(λ̂) from the stored exact point); 2nd:
  `$P/development/dossiers/checks/dtoc5-optcdeg2/dtoc5_checks.py` (rational lower
  bound B_256 ≤ q(λ̂)).
- Command: `python3 "$P/development/reviews/code/sol-dtoc5-review/review.py"`
- Expected output: exact f − q(λ̂) equal to the sum of the completed-square
  losses; the absolute gap as in `tab:closures`.
- Recorded time: 17 s; 3 s for the 2nd.
- Records: `$P/development/reviews/code/sol-dtoc5-review/`

### R03. Certified optcdeg2 bracket

- Labels: `thm:optcdeg2-bound`
- Checkers: `$R/reviews/bangbang-verification/v_states.py`, then
  `v_qcal_exact.py` on the stored split data; 2nd (the first implementation, an
  interval code; weaker bound): `$R/theory-bangbang/optcdeg2_qcal_certify.py` with
  arguments `1.0 0.05`. Primal:
  `$P/development/dossiers/checks/dtoc5-optcdeg2/optcdeg2_primal_int.py`
  (integers) and `$R/reviews/bangbang-verification/v_primal.py` (mpmath).
- Command: `cd "$R/reviews/bangbang-verification" && python3 v_states.py && python3 v_qcal_exact.py`
- Expected output: a rigorous rational bound whose truncation is L; U as in
  `tab:closures`.
- Recorded time: 6 s + 19 s (enclosure and stage minima; 16 to 18 s for the
  latter in other runs); 8 s for the 2nd; primal 1.5 s (integers) and 9 s
  (mpmath).

### R04. Certified lukvle10 bracket

- Labels: `thm:lukvle10-bracket`
- Checkers: `$R/reviews/open-instances-verification/v_lukvle10_prep.py`, then
  `v_lukvle10_bnb.py` with argument `1`; 2nd (the first implementation; weaker
  bound): `$R/open-instances/lukvle10_bound.py` with argument `3`. Primal:
  `$R/publication/primal/dtoc5-lukvle10/lukvle10_enclose.py` and
  `lukvle10_crosscheck.py` (integers only).
- Command: `cd "$R/reviews/open-instances-verification" && python3 v_lukvle10_prep.py && python3 v_lukvle10_bnb.py 1`
- Expected output: a sum of stage bounds whose 200-bit lower end gives L; U as in
  `tab:closures`.
- Recorded time: 5 min; 6 min for the 2nd.

### R05. Certified chain brackets

- Labels: `thm:chain-bound`
- Checkers: `$R/open-instances-wave2/cops/chain_bound.py` with arguments
  `1e-14 <N>`; 2nd: `$R/reviews/cops-verification/v_chain_bnb.py` with arguments
  `1e-14 <N>` (same binary64 bound). Primal:
  `$R/publication/primal/chain/build_points.py` with argument `<N>`, then
  `verify_points.py` with argument `<N>`.
- Command: `cd "$R/reviews/cops-verification" && python3 v_chain_bnb.py 1e-14 <N>`
- Expected output: one binary64 bound per N, equal for both codes; L and U as in
  `tab:closures`.
- Recorded time: 12–29 s; 72–195 s for the 2nd.

### R06. Certified catmix brackets

- Labels: `thm:catmix-bound`
- Checkers: `$R/reviews/cops-verification/v_catmix_dp.py` (N = 100, 200) and
  `$R/reviews/catmix-recheck-checks/recheck_dp.py` (N = 400, 800), with the grid
  arguments in `$R/publication/reproduction/README.md`; 2nd (the first
  implementation; weaker bounds end to end):
  `$R/open-instances-wave2/cops/catmix_bound.py`. Primal: exact simulation of the
  stored binary64 controls,
  `$P/development/dossiers/chain-catmix-checks/r2/exact_catmix.py`, and for
  N = 800 `$R/reviews/catmix-recheck-checks/policy_exact.py` with argument `800`.
- Command: `cd "$R/reviews/cops-verification" && python3 v_catmix_dp.py <N> <grid-arguments-from-reproduction-README>`
- Expected output: binary64 bounds giving L; exact primal values giving U
  (`tab:closures`).
- Recorded time: 20.2 to 46.1 min per instance (clean-checkout runs), which makes
  the row Tier 2; 1,049, 1,728, 3,001 and 4,602 s for N = 100, 200, 400 and 800
  for the 2nd, which certifies the weaker bounds (Tier 3 for `catmix800`).

### R07. Certified waterno2_06 lower bound

- Labels: `thm:waterno2-bounds`
- Checkers: `$R/open-instances-wave2/waterno2/cellslopes/verify_cs.py` and 2nd
  `$R/reviews/waterno2-cellslopes-review-checks/ind_verify_cs.py` on the stored
  records `$R/open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz`:
  cover, containment, exact shortest path. Pair bounds: the second branch and
  bound through the review's driver
  `$R/reviews/waterno2-cellslopes-review-checks/vrebound_cs.py` (a task
  selection replays a sample).
- Command: `cd "$R/reviews/waterno2-cellslopes-review-checks" && python3 ind_verify_cs.py "$R/open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz" logs/repro_ind_verify_certB.json "$R/open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json"`
- Expected output: the exact bound 39157472136693483/2^47, displayed in
  `tab:unclosed`.
- Recorded time: 13 s; 11 s for the 2nd; the pair bounds about 60 CPU-hours on
  a loaded machine (Tier 3; the path check alone Tier 1).

### R08. Certified lower bounds for waterno2_09 through waterno2_24

- Labels: `thm:waterno2-bounds`
- Checkers: `$R/reviews/waterno2-recheck/run_period.py` with arguments
  `<T> <t> 2400 logs/my_implied_<TT>.json` for each of the 63 periods (stored
  multipliers and targets), then `vsum2.py` with argument `<T>`; the first
  code's regeneration is `$R/open-instances-wave2/waterno2/certify.py` (S7.4).
  Primal (all five instances):
  `$R/publication/primal/water-ann-kan/code/water_exact.py`,
  `check_water_point.py`.
- Command: `cd "$R/reviews/waterno2-recheck" && python3 run_period.py <T> <t> 2400 logs/my_implied_<TT>.json; python3 vsum2.py <T>`
- Expected output: status "certified" at the stored target in every period;
  exact sums equal to the stored bounds (`tab:unclosed`).
- Recorded time: 35, 49, 150 and 212 min for `waterno2_09`, `_12`, `_18` and
  `_24` (7.4 h in all).

### R09. Exact camshape optima

- Labels: `thm:camshape-opt`
- Checkers: `$R/reviews/open-instances-verification/v_camshape.py` with
  arguments `100 200 400 800` (`Fraction`); 2nd:
  `$P/development/dossiers/checks/camshape/check_exact.py` (`Fraction`, every row
  evaluated from the parsed data); third:
  `$P/development/dossiers/camshape-critique-checks/mine.py` (fixed point with
  directed rounding); the last two read the OSIL files from the working folder.
- Command: `cd "$R/reviews/open-instances-verification" && python3 v_camshape.py 100 200 400 800`
- Expected output: exact rational v_n; the envelope point is exactly feasible
  with objective v_n; the three codes agree to all printed digits.
- Recorded time: 8 s for all four sizes; 6 min for the 2nd; under 2 s for the
  third.

### R10. Certified ex6_2_5 and ex6_2_7 brackets

- Labels: `thm:ex62-bounds`
- Checkers: `$R/reviews/wave2-small-verification/gibbs_kkt.py`, `gibbs_bb.py`,
  `gibbs_bound.py`; 2nd (a third code; slightly stronger bounds):
  `$P/development/dossiers/small-checks/r2/gibbs_cert.py`. Primal:
  `$P/development/dossiers/primal-points-checks/ex62_check.py` (`Fraction`
  intervals). The first implementation certifies weaker bounds (S1.5).
- Command: `cd "$R/reviews/wave2-small-verification" && python3 gibbs_kkt.py ex6_2_7 ex6_2_5 && python3 gibbs_bb.py ex6_2_7 0 6e-15 1 && python3 gibbs_bound.py ex6_2_7 0=logs/ex6_2_7_bb_type0_tau6e-15.json && python3 gibbs_bb.py ex6_2_5 0 1e-17 1 && python3 gibbs_bound.py ex6_2_5 0=logs/ex6_2_5_bb_type0_tau1e-17.json`
- Expected output: L and U as in `tab:closures`.
- Recorded time: 258 s (`ex6_2_5`) and 77 s (`ex6_2_7`); 198 s and 63 s for the
  third code.
- Records: `$P/development/reviews/round1/g7-checks/` (rerun of `gibbs_cert.py`
  after its path edit: identical output apart from timings).

### R11. Certified pricing050 upper bound for maximisation

- Labels: `thm:pricing-bound`
- Checkers: `$R/reviews/wave2-small-verification/v_pricing050.py`; 2nd (a third
  code; the same bound):
  `$P/development/dossiers/small-checks/r2/pricing_check.py`. The first
  implementation certifies a weaker bound (S1.5). Primal (the saved 17-digit
  point; row slacks in mpmath intervals, exact objective), two codes from
  separate agent sessions, each with its own OSIL reader: the earlier
  `$P/development/dossiers/small-checks/pricing_check.py` and the later
  `$P/development/dossiers/small-checks/r2/pricing_check.py`, whose session did
  not read the earlier check before writing its own (session records,
  2026-10-04).
- Command: `cd "$R/reviews/wave2-small-verification" && python3 v_pricing050.py`
- Expected output: the upper bound `-1813.8290784519730577` of `tab:closures`
  and the objective value of the script's own point (the minimizers of the
  terms F_j of S1.5 at the 20-digit multipliers, rounded to 25 significant
  digits; rows checked in interval arithmetic; not saved), printed to 20 digits
  as `-1813.8290784519730578`. That point is not the saved 17-digit point, and
  its value lies between the upper bound and the primal value
  `-1813.8290784519730769` of `tab:closures`; that exact primal value comes from
  the two primal checkers named above (logs under Records).
- Recorded time: 28 s; 3 s for the third code.
- Records: `$P/development/dossiers/small-checks/pricing_check.log`,
  `$P/development/dossiers/small-checks/r2/pricing_check.log`

### R12. Certified etamac bracket

- Labels: `thm:etamac-bound`
- Checkers: `$R/reviews/wave2-small-verification/v_etamac.py`; 2nd (the first
  implementation; weaker bound): `$R/open-instances-wave2/small/etamac.py`.
  Primal: `$P/development/dossiers/small-checks/r2/etamac_point.py`.
- Command: `cd "$R/reviews/wave2-small-verification" && python3 v_etamac.py`
- Expected output: L and U as in `tab:closures`.
- Recorded time: 22 s; 27 s for the 2nd.

### R13. Certified pindyck bracket and concavity

- Labels: `thm:pindyck-bound`
- Checkers: in `$R/reviews/pindyck-review-checks/`: `own_ranges.py`,
  `own_concavity.py`, `verify_own_leaves.py`, `final_bound.py`,
  `primal_check.py`; 2nd concavity proof (the first implementation; slightly
  weaker bound): `$R/open-instances-wave2/small/pindyck_global.py`; bound from
  the stored enclosures: `$P/development/dossiers/small-checks/r2/pindyck_sc.py`.
- Command: `cd "$R/reviews/pindyck-review-checks" && python3 verify_own_leaves.py && python3 final_bound.py`
- Expected output: ∇²J ⪯ −10⁻³ I certified on every leaf; L and U as in
  `tab:closures`.
- Recorded time: 322 s; 19 s for the 2nd; under 1 s for the bound.

### R14. Certified powerflow0030p bracket

- Labels: `thm:pf-0030p`
- Checkers: `$R/reviews/wave3-verification/powerflow/run_root.py` with argument
  `powerflow0030p` on the stored multipliers
  `$R/open-instances-wave3/logs/powerflow0030p.sdpcert.json` (exact LDLᵀ).
  Primal: `$R/publication/primal/powerflow/certify.py` and the review's dyadic
  `$R/publication/reviews/primal-powerflow-r1/verify.py`.
- Command: `cd "$R/reviews/wave3-verification/powerflow" && python3 run_root.py powerflow0030p`
- Expected output: an exact bound giving L; U as in `tab:closures`.
- Recorded time: 4 s.

### R15. Certified powerflow0039p and powerflow0039r brackets

- Labels: `thm:pf-0039`
- Checkers: `$R/open-instances-wave3/powerflow/ext/verify_exact.py` with
  arguments `<name> bb3t` and `verify_bb3.py` with arguments `<name> bb3t` on
  the stored leaves `logs/<name>.bb3t.json` of that folder; 2nd: the leaf checks
  in `$R/reviews/powerflow0039-review-checks/`.
- Command: `cd "$R/open-instances-wave3/powerflow/ext" && python3 verify_exact.py <name> bb3t && python3 verify_bb3.py <name> bb3t`
- Expected output: every leaf matrix positive semidefinite; the minimum over the
  leaves gives L (`tab:closures`).
- Recorded time: 78 s (`powerflow0039p`) and 24 s (`powerflow0039r`); 2 s for
  the separate checks. Regenerating the leaves with `pf_bb3.py` in the same
  folder takes 316 s and 463 s.

### R16. The hvycrash objective is constant on its feasible set

- Labels: `prop:hvycrash-identity`
- Checkers: `$R/open-instances-wave2/small/hvycrash.py`; 2nd:
  `$R/reviews/wave2-small-verification/v_hvycrash.py`; row identities:
  `$P/development/dossiers/small-checks/r2/hvy_check.py`.
- Command: `cd "$R/reviews/wave2-small-verification" && python3 v_hvycrash.py`
- Expected output: objective −437/2000 on the feasible set; an enclosure of the
  witness.
- Recorded time: under 1 s each.

### R17. Certified eg brackets with a recorded run under the accuracy auditor

- Labels: `thm:eg-bounds`
- Checkers: leaf re-certifier with exponential and power values checked by the
  accuracy auditor:
  `$P/development/eg-audit/run_audit.py`, then `compare_audit.py`; stored
  all-leaf results of the unaudited run: `$R/publication/eg-recheck/summarize.py`;
  exact coverage: `$R/publication/reviews/eg-recheck-r1/own_cover.py`. Search:
  `$R/open-instances-wave3/eg/retry/egbb.py`; `verify_primal.py` in the same
  folder writes the points and checks them at 50 digits. Primal:
  `$P/development/dossiers/primal-points-checks/eg_dyadic_check.py`
  (library-free dyadic intervals), rerun with the exponential test
  `$P/development/reviews/round1/eg-dyadic/exp_test.py`.
- Command: `python3 "$P/development/eg-audit/run_audit.py" --workers 4; python3 "$P/development/eg-audit/compare_audit.py"`
- Expected output: last line "RESULT: PASS (complete run; 1234542 leaves
  compared or checked; 63017129222 exp/power results audited, 0 violations)";
  L and U as in `tab:closures`.
- Recorded time: 16,703 s summed over 44 jobs: `eg_int_s` 465 s (Tier 1),
  `eg_disc_s` 1,456 s (Tier 2), `eg_disc2_s` 14,782 s (Tier 3). The artifact's
  `--eg-int` run (`eg_int_s` only, one worker) took 323.818 s.
- Records: `$P/development/eg-audit/`,
  `$P/development/reviews/code/sol-eg-audit-review/`,
  `$P/development/reviews/round1/eg-dyadic/`

### R18. Certified ann_cumene_tanh lower bound

- Labels: `thm:ann-bound`
- Checkers: in `$R/reviews/ann-extension-review-checks/`: `replay.py` with
  arguments `run1` and `run2` (replay by saved node counts), `leaves.py` with
  argument `extract`, `verify_boxes.py` at the target L on two processes.
  Primal: `$R/publication/primal/water-ann-kan/code/nn_exact.py` with argument
  `ann_cumene_tanh`.
- Command: `cd "$R/reviews/ann-extension-review-checks" && python3 replay.py run1 "$SCRATCH/replay_run1.npz" && python3 replay.py run2 "$SCRATCH/replay_run2.npz" && python3 leaves.py extract "$SCRATCH/replay_run1.npz" "$SCRATCH/regions_run1.npz" && python3 leaves.py extract "$SCRATCH/replay_run2.npz" "$SCRATCH/regions_run2.npz"`
- Expected output: frontiers identical to the stored ones; every pruned region
  and unsplit leaf box verified at L (`tab:unclosed`).
- Recorded time: replay 33 min (run 1) and 1.6 h (run 2); verification about
  1.2 h wall on two processes (2.0 CPU-hours).

### R19. The six stored KAN OSIL models are infeasible

- Labels: `prop:kan-infeasible`
- Checkers: `$R/reviews/wave3-verification/kan_infeas_cert.py` with argument
  `<name>` (Sturm counts and pairwise resultants), confirmed by `kan_struct.py`
  (greatest common divisors and root isolation) and `kan_infeas_detail.py` with
  arguments `<name> <edge>` in the same folder; 2nd, a separately written
  propagation over the rationals that shares only the OSIL reader:
  `$P/development/dossiers/ann-kan-checks/kan_infeas_edge.py` and
  `kan_infeas_edge_class.py` with arguments `<name> <edge>`, edges `x1076`,
  `x1344`, `x2416` (`kan_r3_h1_n4`, `_n5`, `_n9`) and `x776`, `x1292`, `x2066`
  (`kan_r5_h1_n3`, `_n5`, `_n8`).
- Command: `cd "$R/reviews/wave3-verification" && python3 kan_infeas_cert.py <name>`
- Expected output: for one edge and every admissible knot interval, no common
  real solution of the partition-of-unity rows; the 2nd certifies every
  admissible piece infeasible (`kan_infeas_edge_class.py` for the `r3` models
  and `kan_r5_h1_n3`, `kan_infeas_edge.py` for `kan_r5_h1_n5` and
  `kan_r5_h1_n8`).
- Recorded time: 0.6–1.7 s per model; about a second per model for the 2nd.
- Records: `$P/development/reviews/code/sol-kan-review/`,
  `$P/development/dossiers/ann-kan-checks/logs/`

### R20. Certified objective brackets for the KAN relaxation

- Labels: `thm:kan-enclosure`
- Checkers: `$R/open-instances-wave3/kan/run_kan.py` with arguments
  `<name> 1e-10 7200`; 2nd: the guarded copy
  `$P/development/reviews/round1/kan-guard/kan_bnb_rigexp.py` with arguments
  `<name> 4e-11 7200 1024`, run for the record by the driver `run_replays.py` in
  that folder (it expects its tree under `/tmp/kan-guard` and six cores; logs in
  its `logs/`; the section "Guarded KAN replay of row R20" below reruns the
  searches inside `$WORK`, one process at a time), with the reader
  `$R/reviews/wave3-verification/kan_decode.py` and the shared interval modules
  `$R/open-instances-wave3/kan/kan_iv.py` and
  `$R/open-instances-wave2/small/ia.py`; exact checks of the shared exponential
  constants: `$P/development/dossiers/ann-kan-checks/check_constants.py`.
  Points of R_P: `$R/publication/primal/water-ann-kan/code/nn_exact.py` with
  argument `<name>` and `$R/reviews/wave3-verification/kan_primal.py`. The
  unguarded original of the 2nd is historical (`HISTORY.md`).
- Command: `python3 "$P/development/reviews/code/sol-kan-review/run_review.py" <r3-name>`
- Note: the command is the Tier 1 short check of the artifact; it regenerates an
  `r3` search of the unguarded original, which the guarded replay reproduces bit
  for bit. The guarded replay is the command block of the section "Guarded KAN
  replay of row R20" below.
- Expected output: both lower bounds; the reported L is the weaker one
  (`tab:kan`); the guarded replay gives the second bound bit for bit, with no
  guard trigger.
- Recorded time: first implementation 22–24 s per `r3` model and 87 s to 18 min
  per `r5` model; guarded 2nd 22.71–58.86 s per `r3` model and 12.4 to 19.6 min
  per `r5` model (six concurrent processes). Tier 1 for the three `r3` models,
  Tier 2 for the three `r5` models.
- Records: `$P/development/reviews/code/sol-kan-review/`,
  `$P/development/reviews/round1/kan-guard/`; historical: the unguarded original
  `$P/development/dossiers/ann-kan-checks/kan_bnb_rigexp.py` and the
  library-exponential second code `$R/reviews/wave3-verification/kan_bnb.py` with
  its session's files `$R/reviews/wave3-verification/kan_bnb_v1.py`,
  `$R/reviews/wave3-verification/kan_soundness.py` (soundness sampling, evidence
  only), `$R/reviews/wave3-verification/kan_local.py` and
  `$R/reviews/wave3-verification/dump.py`

### R21. Certified feasible points and objective enclosures

- Labels: `sec:points`, `tab:points`
- Checkers: per family in `$R/publication/primal/` (folders `lnts`,
  `dtoc5-lukvle10`, `chain`, `powerflow`, `water-ann-kan`); separate checks in
  `$R/publication/reviews/primal-*-r1/`; the other families as in the rows above.
- Command: `cd /tmp && python3 "$P/data/make_tables.py"`
- Expected output: every row, bound and integrality requirement holds exactly
  or by an existence proof; objective enclosures giving U.
- Recorded time: seconds to minutes.
- Records: `$P/development/reviews/round1/g7-checks/`,
  `$P/development/reviews/round1/eg-dyadic/`

### R22. Nineteen invalid listed dual/point pairs on fifteen instances

- Labels: `prop:audit-refute`, `tab:audit-pairs`
- Checkers: in `$R/bound-audit/`: `audit.py` with arguments `screen`,
  `evaluate`, `verify`, `classify`; `verify_one.py` with argument
  `<instance>.<point>`; `cert_linear.py`, `cert_ndnetgen.py`, `cert_topopt.py`.
  2nd: `$R/reviews/bound-audit-verification/` and
  `$R/reviews/bound-audit-recheck/`; index:
  `$R/publication/reproduction/audit-map.json`.
- Command: `cd "$R/bound-audit" && python3 audit.py verify && python3 audit.py classify`
- Expected output: the counts of `sec:audit-screen`; 19 class (i) pairs on 15
  instances, each margin above one display unit.
- Recorded time: seconds per point; about 3 min per
  `topopt-cantilever_60x40_50` point.
- Records: `$P/development/reviews/round1/g7-checks/`,
  `$P/development/reviews/round1/sol-numbers.md`

### R23. Spring optimum, emfl enclosures and rocket margins

- Labels: `prop:spring-opt`, `prop:emfl-enclosure`
- Checkers: `$R/publication/audit-ir/spring_global.py`; `emfl`: checker V2
  `$R/reviews/bound-audit-recheck/emfl_bounds.py` (the displayed enclosures)
  and 2nd, the audit implementation `$R/bound-audit/cert_socp.py` with arguments
  `<emfl-instance> <points>` (wider enclosures, which also establish every
  verdict on listed values; status of the displayed enclosures: weaker second);
  `rocket`:
  `$R/reviews/wave2-small-verification/v_lindo.py` with argument `rocket<N>` and
  2nd `$P/development/dossiers/checks/audit-r2/rocket_kraw.py`.
- Command: `python3 "$R/publication/audit-ir/spring_global.py"; cd "$R/reviews/bound-audit-recheck" && python3 emfl_bounds.py <emfl-instance> <label=value-arguments-from-recorded_commands>`
- Expected output: the optimum of `spring`; two-sided `emfl` enclosures, those
  of V2 inside those of the audit implementation; the `rocket` margins
  (`app:audit`).
- Recorded time: 2–13 s per `emfl` instance (V2) and 3–26 s (2nd); about one
  second per `rocket` instance.
- Records: `$P/development/reviews/round1/g7-checks/`,
  `$P/development/reviews/round1/sol-numbers.md`,
  `$R/publication/audit-ir/logs/spring_global.json`

### R24. Exact feasible SCIP witnesses and minimal reproducers

- Labels: `prop:scip-witnesses`, `prop:scip-reproducers`, `lem:scip-cube`
- Checkers: in `$R/publication/scip-bug/`: `exact_check.py`, `spec_check.py`,
  `indep_check.py`, `gams_check.py` (exact witnesses); `checksol_witness.py`
  (SCIP's own check); `binary64_analysis.py`; the reproducers
  `$R/publication/scip-bug/min/fm336_v1010.cip` and
  `$R/publication/scip-bug/minimal/tiny2.cip` with their witness files.
- Command: `cd "$R/publication/scip-bug" && python3 exact_check.py <model.cip> <witness.json> [claim]; python3 spec_check.py <spec.json> <witness.json>; python3 indep_check.py; python3 gams_check.py`
- Expected output: every witness exactly feasible below SCIP's claim and
  accepted by SCIP; the claims per version and seed as in `app:solvers`. The
  largest binary64 row violation of the large witnesses, 32122061/10995116277760000000000
  (displayed as 2.93·10⁻¹⁵ in `prop:scip-witnesses`), was computed exactly in
  `$P/development/reviews/round1/sol-numbers.md`, lines 34–40.
- Recorded time: seconds for the exact checks; SCIP runs need the listed builds.
- Records: `$P/development/reviews/round1/sol-numbers.md`

### R25. Reported values lie beyond certified bounds

- Labels: `prop:baron-camshape`, `prop:qplib-copies`, `prop:kan-scip`,
  `prop:camino-eg`, `prop:minotaur-optcdeg2`, `tab:claims`
- Checkers: exact comparison of the reported values with the certified values
  in `$P/data/make_tables.py`; campaign points:
  `$R/publication/solver-runs/point_checks.json`; QPLIB copy bounds:
  `$P/development/dossiers/checks/camshape/`.
- Command: `cd /tmp && python3 "$P/data/make_tables.py"`
- Expected output: the margins of `tab:claims`, rounded down.
- Recorded time: seconds for the comparisons. The exact optima of the QPLIB
  copies (`prop:camshape-copies`, which `prop:qplib-copies` uses): under 2 s for
  the second parser, which also evaluates the reference points; about 10 min for
  the first parser on the four copies and the four MINLPLib files together, and
  about 5 min for its evaluation of the reference points (certificate box in
  S1.3).

### R26. Recorded one-hour solver campaign outcomes

- Labels: `tab:solvers`, `tab:claims-campaign`
- Checkers: in `$R/publication/solver-runs/`: the run logs, `results_table.csv`
  and the analysis scripts; a rerun needs GAMS 54.3.1 and solver licences, and
  the driver `driver.py` names the GAMS installation of the original machine.
- Command: `Read "$R/publication/solver-runs/results_table.csv" and the run logs; a rerun requires GAMS and licences.`
- Expected output: the counts of `tab:solvers`.
- Recorded time: 129 one-hour runs.

### R27. Directed rounding of generated certified displays

- Labels: `app:displays`
- Checkers: `$P/data/make_tables.py`
- Command: `cd /tmp && python3 "$P/data/make_tables.py"`
- Expected output: exit status 0; `check.log` lists every check. The check
  covers the bound, primal, gap and margin displays that the script generates;
  certified numbers typed in the LaTeX sources were checked separately, and
  solver output, run times and numerical evidence carry no directed-rounding
  guarantee (S7.5).
- Recorded time: about 5 s.
- Records: `$P/development/reviews/round1/g7-checks/`, `$P/artifact/HISTORY.md`

## Guarded KAN replay of row R20

The archived driver `run_replays.py` ran the six guarded searches at once in
`/tmp/kan-guard` on six cores. The commands below rerun them inside `$WORK`
(`README.md`, "Environment and input roots"), one process at a time, and
compare each result exactly with the archived guarded run and with the reported
bound. `README.md` ("Guarded KAN replay") records a test of these commands.

```bash
A="$P/development/reviews/round1/kan-guard"   # archived guarded code and logs
G="$WORK/kan-guard"; mkdir -p "$G/logs"
cp "$A/kan_bnb_rigexp.py" "$G/"
export PYTHONPATH="$R/reviews/wave3-verification:$R/open-instances-wave3/kan"
for n in kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9; do  # r5: kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8
  python -u "$G/kan_bnb_rigexp.py" "$n" 4e-11 7200 1024 > "$G/logs/$n.guard.log" 2>&1
  python - "$n" "$A/logs/$n.bnb.json" "$G/logs/$n.bnb.json" "$P/data/numbers.json" <<'PY'
import json, sys
from fractions import Fraction
n, old, new, numbers = sys.argv[1], *(json.load(open(f)) for f in sys.argv[2:])
diff = sorted(k for k in old.keys() | new.keys() if k != 'time' and old.get(k) != new.get(k))
ok = (not diff and new['done'] and new['open'] == 0 and new['minquad_stats']['guard_entries'] == 0
      and Fraction(new['lower_bound']) >= Fraction(numbers['kan'][n]['L']['exact']))
print(n, 'PASS: as archived except time; no guard trigger; bound >= reported L' if ok else 'FAIL', diff)
PY
done
```

## Reruns and checks of the first internal review round (2026-10-04)

Separate agent sessions reran the following from `/tmp` copies; the folders are
part of the index (rows R10, R17, R20–R24 and R27).

- **KAN, guarded path (I)** (`$P/development/reviews/round1/kan-guard/`): a copy
  of `kan_bnb_rigexp.py` whose quadratic lower-bound routine `minquad` checks
  exact halving and outward rounding entry by entry and falls back to exact
  rational minimization (proof in `minquad-proof.md`; 72,240 exact test
  comparisons in `test-minquad.log`). `run_replays.py` replayed all six KAN
  searches, 23 s to 20 min wall per model with six concurrent processes; every
  archived bound was reproduced bit for bit, with no guard trigger
  (`comparison.log`, `logs/`). Search times: `kan_r3_h1_n4` 24.74 s,
  `kan_r3_h1_n5` 22.71 s, `kan_r3_h1_n9` 58.86 s, `kan_r5_h1_n3` 1,175.59 s,
  `kan_r5_h1_n5` 744.42 s, `kan_r5_h1_n8` 1,005.18 s (`report.md`).
- **eg, dyadic primal check** (`$P/development/reviews/round1/eg-dyadic/`): the
  library-free check `eg_dyadic_check.py` was rerun and read in full and
  confirms the three points (`primal-rerun.log`); because its built-in
  self-test skips reciprocity above 100, `exp_test.py` checks enclosures and
  reciprocity at 452 arguments, among them 1234/7 (`exp-test.log`).
- **Audit**: the second `rocket` proofs and the exact GAMS/OSIL comparison were
  rerun from clean copies with the published results; the record is
  `$P/development/reviews/round1/sol-numbers.md`.
- **Displays** (`$P/development/reviews/round1/g7-checks/`): exact checks of the
  three corrected second-proof upper ends of `tab:audit-second` and of the
  `methanol50` coefficient change (`audit-displays.log`), the exact objective
  widths of the `powerflow` points (`powerflow-widths.log`, read by
  `make_tables.py`), and a rerun of `gibbs_cert.py` after its path edit
  (identical output apart from timings).

## Run records moved from the supplement

The second internal review round moved these run records, timings, negative
controls and repeated runs out of the supplement. Each heading names the
register row and the source of the passage in the round-3 sources (file and
label); the text is quoted with the notation simplified for Markdown, and
"first code" and "second code" are the first and second implementations of
Section 2.6 of the paper.
Passages that only repeated MINLPLib's listed data were not copied; the archived
instance pages and `numbers.json` keep those data.

### Row R01: `B1-lnts-lukvle10.tex`, `app:lnts-proof` (computation of the enclosure)

The first code asserts the model structure from the OSIL file and finds a
bracket of width 2·10⁻⁶². The second code's final brackets have width below
10⁻⁹⁰, and its rational enclosures of v*, which give the displays, are narrower
than 1.11·10⁻⁹¹. Negative controls: shifting the final bracket by ±10⁻⁵⁵ fails
the sign test (`$P/development/dossiers/checks/lnts-lukvle10/lnts_negative_test.log`);
changing one acceleration coefficient by 10⁻⁴⁰ fails the model-structure
assertion.

### Row R03: `B2-dtoc5-optcdeg2.tex`, `app:optcdeg2-point` (after `prop:optcdeg2-point`)

As a negative control of the primal enclosure, a bracket placed entirely above
the root shows no sign change.

### Row R05: `B4-chain-catmix.tex`, caption of `tab:chain-bnb`

The clean-copy reproduction runs of the claim register took 12 to 29 s
(`chain_bound.py`) and 72 to 195 s (`v_chain_bnb.py`) per instance.

### Row R06: `B4-chain-catmix.tex`, `app:catmix-computation` ("Where the gap comes from", after `lem:catmix-losses`)

The stage minimizations of the first code stop within 10⁻¹⁴ of a
floating-point incumbent, and its logged per-stage loss is at most 9.99·10⁻¹⁵
(logged for N of the N+1 minimizations; floating-point estimates). By
`lem:catmix-losses`, they account for at most about 10⁻¹² of that code's
`catmix100` gap of 7.9·10⁻¹²; the rest is interpolation error in its window
rays, whose spacing on the singular arc grows from about 1.3·10⁻⁷ at stage 70
to about 6.5·10⁻⁷ at stage 20.

For N = 100, uniform base spacings 2⁻⁹, 2⁻¹¹, 2⁻¹³ and 2⁻¹⁵ give gaps of about
3.2·10⁻⁴, 2.1·10⁻⁵, 1.28·10⁻⁶ and 8.0·10⁻⁸; almost all of the loss accumulates
on the singular arc, which is why the record grids refine a band there and a
window around the trajectory of a good feasible point.

### Row R06: `B4-chain-catmix.tex`, `app:catmix-computation`, table `tab:catmix-grids`

Ray grids of the record `catmix` runs (second code). The base grid has the
stated dyadic spacing on [0, 13/128) and spacing 2⁻⁷ on [13/128, 1]. Bands
refine the base grid on the stated θ-interval (and stages); at each stage a
window replaces the rays in its span by 2K+1 rays at the stated spacing around
the θ-trajectory of a good feasible point. Rays per stage are averages over the
stages; pairs are (interval, cone) pairs bounded in the backward pass. Times
are wall-clock times of single-threaded runs on a shared machine and are
indicative only; they are the original times of the record runs (the register
gives the clean-copy times). Any grid gives a valid bound.

| N | grid | rays per stage | pairs | time |
| ---: | --- | ---: | ---: | ---: |
| 100 | base 2⁻¹⁶; band [0.0697, 0.0715] at 2⁻²⁰; window of 601 rays at 2⁻²⁵ | 9,131 | 2.0·10⁹ | 2,358 s |
| 200 | base 2⁻¹⁵; band [0.0695, 0.0717] at 2⁻¹⁹; window of 401 rays at 2⁻²⁴ | 4,917 | 8.6·10⁸ | 1,170 s |
| 400 | base 2⁻¹³; on stages 40–310 a core band [0.0703, 0.0710] at 2⁻²¹ and a shell [0.0695, 0.0717] at 2⁻¹⁹; window of 401 rays at 2⁻²⁴ except on stages 56–288 | 2,629 | 1.74·10⁹ | 2,578 s |
| 800 | base 2⁻¹³; on stages 95–600 the same core and shell bands, and on stages 570–650 a band [0.060, 0.0695] at 2⁻¹⁷; window of 401 rays at 2⁻²⁴ except on stages 112–576 | 2,647 | 1.88·10⁹ | 2,595 s |

### Rows R07 and R08: `B8-waterno2.tex`, `app:waterno2-model`

Separate exact parsers find the GAMS and OSIL forms identical for all five
instances (every row as a polynomial with rational coefficients, every bound
and type, and the objective); the comparison detects a change of 10⁻⁸ in one
coefficient (negative control).

### Rows R07 and R08: `B8-waterno2.tex`, `app:waterno2-verification`

For fixed targets and a fixed software stack (Python 3.13.11, NumPy 2.5.1,
SciPy 1.18.0 with HiGHS) the searches are deterministic: 21 saved V_fl runs
and, in a separate replay, 1,564 V_fl tasks (1,008 records and the 556 leaf
checks) gave identical status, bound and node count. In the recorded runs, V_fl
re-established the 63 period statements of `waterno2_09`–`waterno2_24` in 7.4 h
in total and the 49,315 record statements of `waterno2_06` in about 60
CPU-hours on a loaded machine; the 1,564-task replay suggests 20 to 30
CPU-hours on an unloaded one. The exact combination steps take seconds.

Regeneration derives each period target anew from time-limited SCIP runs (the
smallest incumbent minus max{10⁻⁴, 10⁻⁷·|value|}) and proves it with code P. A
complete rerun reproduced the bounds of `waterno2_06`, `waterno2_09` and
`waterno2_12` exactly, including node counts, and gave the slightly lower, also
valid values 4790.820086219 and 6576.150434342 for `waterno2_18` and
`waterno2_24`, because SCIP returned different incumbents in three periods
(S7.4, `app:repro-regen`, which prints them rounded down as 4790.820086 and
6576.150434).

### Rows R10–R13 and R16: `B5-small.tex`, `app:small` (opening paragraph)

The MINLPLib `.gms` files of the six small instances agree with the OSIL files
at five random points per instance (all rows to within 3.5·10⁻⁵¹ relative and
the objectives exactly, in 50-digit arithmetic); this is numerical evidence,
and no claim depends on it.

### Row R10: `B5-small.tex`, `app:small-ex62` ("Other implementations")

A separate agent session read the code of the third implementation, reran the
`ex6_2_7` case and ran a negative control (without the windows the exclusion
step fails at the minimizer with value −4.19·10⁻¹⁵).

### Row R11: `B5-small.tex`, `app:small-pricing` (computation and proof of `thm:pricing-bound`)

A cutting-plane method and, separately, a direct search, each followed by a
50-digit refinement, found the same digits of the multipliers μ_e5 and μ_e6.

### Rows R14 and R15: `B6-powerflow.tex`, certificate box of `thm:pf-0030p` and `thm:pf-0039` (field "Implementations")

The primal check of the three points rejected five negative controls. (The two
exact checks of `rem:pf-anglefree` remain in that remark.)

### Row R15: `B6-powerflow.tex`, `app:powerflow-0039` ("Computation")

The six leaves of `powerflow0039p` arise from cuts of B₀ at P_g ≈ 6.70938 and
7.07845; the middle slab is cut at Q_g = 1.66, its lower part at
W₃₀,₃₀ = 1.0996, and the upper part of that at P_g ≈ 6.74629, which leaves the
box [6.70938, 6.74629] × [1.4, 1.66] × [1.0996, 1.1236] (end points rounded).
The nine leaves of `powerflow0039r` are the same, except that this box is cut
further at Q_g = 1.426, W₃₀,₃₀ = 1.1212 and P_g ≈ 6.71444 into four leaves.
The searches took 11 nodes (6 leaves, 309 s) and 17 nodes (9 leaves, 423 s); a
regeneration on the archived software stack gave identical final bounds.

### Row R17: `B7-eg.tex`, `app:eg-computation` (the first code's search)

With the relative cutoff 10⁻⁹, the fast mode processed 56,189, 62,779 + 55,973
(two parts) and 1,152,830 (eight parts) boxes of `eg_int_s`, `eg_disc_s` and
`eg_disc2_s` in 274, 726 + 650 and 12,378 s, and the interval mode 56,189 and
62,779 + 55,971 boxes in 2,113 and 2,660 + 2,373 s and, for part 1 of
`eg_disc2_s`, 134,607 boxes in 5,755 s (CPU times on a shared machine, which
support no speed claims). The logged statistics of the two modes agree, except
that part 1 of `eg_disc_s` closed one box earlier in the interval mode.

### Row R17: `B7-eg.tex`, `app:eg-computation` ("Evidence about the method")

With relative cutoff 10⁻⁶ and a 900 s limit on `eg_int_s`, the full search
closed after 55,903 boxes (591 s), the searches without propagation or with
second-order remainders only after 57,499 and 66,141 boxes, and the search
without the LP stopped at the limit after 125,375 boxes with bound 6.4526561
and 30,720 open boxes; near the best point the LP bound combines row e12 with
the side row e26 (multiplier 22.27), and no single row gives the bound there.

### Row R17: `B7-eg.tex`, `app:eg-primal`, and `C-points.tex`, `app:points-instances` (the `eg` points)

The dyadic primal check was rerun and read in full by a separate agent session,
which confirmed the three points (folder
`$P/development/reviews/round1/eg-dyadic/`). Its built-in self-test skips the
reciprocity assertion for arguments above 100; a separate test, `exp_test.py`
in the same folder, checks enclosures and reciprocity at 452 arguments,
including both signs of 1234/7. The tests support, and do not replace, the
alternating-series proof. Decimal arithmetic at 60 digits with directed
rounding (same reader) and mpmath interval arithmetic at 120 digits and at 200
bits (two further, separately written readers) confirm the slacks of the
points.

### Row R17: `F-eg-rounding.tex`, `app:egrounding-run` (tests of the auditor)

Two separately written test programs compared the enclosure of
`lem:eg-auditexp` with mpmath at 300 and 400 bits on 32,010 and 141,706
arguments (among them reduction half-points (m + ½)L and their float
neighbours, multiples of L, the ends −708 and 709, and subnormal and tiny
arguments; relative width of [lo, hi] at most 4.4·10⁻¹⁵). For the exponential
and the three powers, the first checked that injected relative errors of
±1.0001ε and more and NaN, infinite and negative results are rejected and
errors of ±0.3ε accepted, and the second, for 6,000 arguments, that the first
floats outside the band of relative width ε are rejected and errors of ±½ε
accepted; the second also checked the constants at 400 bits. End-to-end tests
on 512 leaves of `eg_disc2_s`, part 1, replaced one exponential or power result
by a value with relative error between 1.1·10⁻¹⁴ and 10⁻¹²; each injection
flagged exactly the leaf that owns the affected piece (all 64 leaves of the
batch for ŝ²), and injected errors of 3·10⁻¹⁵ were accepted.

### Row R17: `F-eg-rounding.tex`, caption of `tab:eg-audit`

With eight jobs in parallel the audited run took 37 minutes (the certificate
box of `thm:eg-bounds` keeps this time).

### Row R18: `B9-ann-kan.tex`, `app:annkan-ann-verif`

The search tree is not stored, but both runs replay deterministically by saved
node counts (about 2 h on one core), and the replay regenerates the region lists
of the re-certification, which were not archived; re-certifying all regions
took 2.0 CPU-hours (1.2 h on two processes) in the recorded reproduction run,
of which the 208,223 open boxes, which can also be re-certified directly from
the stored frontier, took about 15 CPU-minutes.

### Row R20: `B9-ann-kan.tex`, `app:annkan-kan-enclosure` (rerun with a rigorous exponential)

A separate agent session read the change from the library exponential to the
rigorous exponential (`HISTORY.md`, Section 4) and the exponential code,
checked its constants, tested the enclosure at 19,916 arguments against
100-digit values, and reran the three `r3` searches, which reproduced every
recorded field except the time; the guarded replay reran all six.

### Row R20: `B9-ann-kan.tex`, certificate box of `prop:kan-infeasible` and `thm:kan-enclosure` (field "Replay")

The unguarded path (I) with the rigorous exponential took 55 CPU-minutes for
all six models on a loaded machine (per-model times from
`$P/development/dossiers/ann-kan-checks/logs/kan_*.bnb.json`: 25.7, 23.1 and
54.9 s for the `r3` models and 1,221, 761 and 1,188 s for `kan_r5_h1_n3`,
`_n5` and `_n8`). The box now gives the tiers per model: `r3` Tier 1, `r5`
Tier 2.

### Row R22: `E-audit.tex`, `app:audit-existence` ("The proof methods in detail")

The Krawczyk proof:

1. integer variables are rounded and fixed;
2. continuous variables within 10⁻⁷ (relative) of a bound are put on it;
3. the active rows are all equality rows and the inequality rows that are
   violated or within 10⁻⁷ of a side, held at that side; rows with vanishing
   gradient in the free variables move to the box check;
4. a basis of |E| continuous variables is chosen by QR factorization with
   column pivoting, with weights that favour variables away from their bounds;
   the other variables keep their exact decimals;
5. Newton's method runs on the square system with residuals at 40 digits;
6. the Krawczyk test runs on a box of relative radius 10⁻¹², 10⁻¹⁰ or 10⁻⁸
   around the Newton point;
7. the box check of `cor:audit-box` encloses every other row, using exact
   polynomial arithmetic in the basic variables where possible and interval
   arithmetic otherwise, and encloses the objective.

If a basic variable ends on a bound, it is fixed there and the attempt is
repeated (up to three rounds), followed by a variant that puts all near-bound
variables on their bounds first. The shifted Krawczyk proof first fixes,
repeatedly, every continuous variable that a linear row determines alone; then
one linear program (HiGHS) finds a direction that keeps the linearized
equalities and strictly improves as many active inequalities and bounds as
possible, and a second one minimizes the objective change on that set. The
point moves a distance t along this direction, with t growing by factors of ten
from three times the violation, and a Krawczyk proof follows; the linear
programs only propose the point, and the Krawczyk proof proves it.

### Row R22: `E-audit.tex`, `app:audit-existence` ("Trust and replay")

The 12 refutations with exact proofs need only rational arithmetic and the
correctness of the checking code. The seven Krawczyk-based ones also need IEEE
binary64 arithmetic for the matrix products, in any summation order. Most
certificates replay in seconds from stored centre points.

### Row R23: `E-audit.tex`, `app:audit-rocket`

On 2026-10-04 a separate agent session reran the second proof on copies of the
models, points and code: every inclusion test passed, the brackets were
[−1.0128320069151, −1.0128320069130], [−1.0128356770698, −1.0128356770677] and
[−1.0128365294843, −1.0128365294821], and the thrust and mass were pinned at
76 and 64, 151 and 127, and 315 and 254 nodes, as in the original runs
(record: `$P/development/reviews/round1/sol-numbers.md`).

### Row R24: `H-solvers.tex`, `app:solvers-scip` ("Instrumented runs and settings")

The 15 instrumented wrong runs are `tiny2`, `pumps_default`, `fm336`,
`pair2236` (seed shift 8), p4, p5 (two seeds) and p0 in the 10.0.2 debug build,
and `fm336`, `fm318`, `pumps_default`, `tiny2`, `pair2236` (seed shift 14), p4
and p5 in the debug build of the development snapshot.

With the setting `b` of `varboundrelax`, which relaxes all bounds by ε,
including fixed ones, the wrong runs fell from 27/60 to 0/60 (PySCIPOpt: p0, p4
and p5 with seeds 0–9, `pair2236` with seeds 0–29), from 19/20 to 0/20
(development snapshot: its wrong runs of p4, p5, `pair2236` and
`pumps_default`, and one more), from 30/40 to 0/40 (`fm336` and `fm318`, seeds
0–9, development snapshot and 10.1.0) and from 2/2 to 0/2 (the two small-excess
runs): 78/122 against 0/122 in total.

### Row R26: `H-solvers.tex`, `app:solvers-protocol` (machine, admission and measurement rule; overloaded first batch)

The runs shared an Intel Xeon w5-2565X (18 cores, 36 hardware threads, about
47 GiB of memory) with other work. At most ten runs ran at once, and a run was
admitted only when the one-minute load average was at most 30 and at least
8 GiB of memory was available. A monitor sampled every five seconds and
stopped a run whose resident plus swapped memory exceeded 8192 MiB; the hard
wall-clock timeout of 4200 s was never reached. An attempt passes the
measurement rule if it ends on its own and the CPU time of its process group is
at least 0.9 times its wall time; attempts that end within 60 s are exempt from
the ratio test. A failing attempt was rerun, up to three attempts in all, and
the driver kept the attempt ranked first by proper ending, presence of a trace
and CPU share, not by bound or incumbent.

The first ten runs were admitted within one second, before the load average
reflected their work; during that hour the load rose to 47–51 on 36 hardware
threads and the available memory fell to 1.06 GiB. Their CPU shares, 0.9561 to
0.9811, are the ten lowest among the 117 kept runs longer than 60 s (all others
have at least 0.9991), and all four BARON wall-time overruns (3706 to 3728 s,
with at most 3601.65 s of BARON CPU time) occurred in this batch. The ten runs
pass the measurement rule, and removing them changes no bound comparison.

### Rows R03, R08, R14, R15, R18, R20 and R23: `I-reproduction.tex`, `app:repro-regen` (script names of the regenerations)

- `waterno2`: the first code's script
  `$R/open-instances-wave2/waterno2/certify.py` regenerates the period
  certificates (it derives each period's target from time-limited SCIP runs and
  certifies it with the first code's branch and bound); at the stored targets,
  `$R/reviews/waterno2-recheck/run_period.py` certified all 63 periods of
  `waterno2_09`–`waterno2_24` again in a clean copy.
- `optcdeg2`: the split is regenerated by
  `$R/theory-bangbang/optcdeg2_refine_primal.py`, then
  `optcdeg2_qcal_certify.py` in the same folder; this may give a different
  valid bound, and the replay uses the stored split data.
- `powerflow`: a new SDP solve for `powerflow0030p`
  (`$R/open-instances-wave3/powerflow/pf_cert.py`) overwrites the stored
  certificate; the `powerflow0039p` and `powerflow0039r` leaf certificates are
  regenerated by `$R/open-instances-wave3/powerflow/ext/pf_bb3.py` (316 s and
  463 s, identical final bounds).
- `ann_cumene_tanh`: `replay.py` replays the runs by saved node counts, and
  `replay.py` and `leaves.py` regenerate the region lists of the second code's
  verification (`$R/reviews/ann-extension-review-checks/`).
- KAN: the separate agent session reran the second code on the three `r3`
  models through the driver
  `$P/development/reviews/code/sol-kan-review/run_review.py`; the guarded
  replay is in `$P/development/reviews/round1/kan-guard/`.
- Audit: on 2026-10-04 a separate agent session reran the second `rocket`
  proofs and the exact GAMS/OSIL comparison from clean copies (record:
  `$P/development/reviews/round1/sol-numbers.md`).
