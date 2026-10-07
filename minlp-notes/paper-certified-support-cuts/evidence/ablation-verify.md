# Part U ablation: independent check (R8)

Written 2026-10-03. Checker: `verification/R8_ablation.py`. It uses only the
standard library and `fractions`, and it does not import any snapshot code,
SymPy or a solver. No SCIP or Gurobi solve was started. Nothing under
`experiments/` was written, and the manuscript was not edited.

## Verdict

- **Claims (1) and (2) reproduce exactly.** Every count in
  `evidence/ablation-final-summary.md` matches: per part, overall, per model,
  distinct counts, and known-witness counts. The counts were re-derived in two
  ways:
  - from the JSON `cuts`, after recomputing the invalid/material flags exactly;
  - independently from the original records, using my own pool of feasible
    points and the exact rows read from each cut's record.
- **Claim (3) holds only for the ablation's scope.** The certified rows of the
  materially invalid cuts are never violated beyond the tolerance at any pooled
  point. The manuscript sentence "No certified row was violated at any recorded
  feasible point" (`sections/08b-validity.tex`, line 34-35) is broader. Over all
  143,267 recorded rows, 58 point evaluations exceed the protocol tolerance:
  - st_e22: 51 evaluations, at most 1.70e-6, where the threshold is 1e-6;
  - path family: 7 evaluations, at most 3.09e-6, all at Gurobi incumbents.

  These violations are consistent with incumbents that are only approximately
  feasible; they do not show that a certificate is wrong (details below).
  **Severity: major for the manuscript wording.**
- **Two minor points.**
  - The summary says the C4 replay was not finished. It has since finished and
    passed.
  - The manuscript says U1 and U2 "are upper bounds on the true support value".
    This holds only up to rounding: U lies below the certified exact value for
    many cuts, by at most 1.05e-12 relative.

## Command

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cd /tmp && /workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python \
  /workspace/minlp-notes/paper-certified-support-cuts/verification/R8_ablation.py \
  > "$(mktemp -d)/final.json"
```

- **Run:** exit 0 in 97.8 s (`elapsed_seconds`), with 1.0 GB peak memory.
- **Output:** copied to `evidence/ablation-verify.json` (SHA-256 `bbe4ef14...`).
  Every number below cites a field of that file in brackets.
- **Script SHA-256:** `30b0808d...`.
- **Input:** `evidence/ablation-uncertified.json`, SHA-256 `b6673379...`
  [`ablation_json_sha256`].
- **Record files:** all 13 have the SHA-256 recorded in the ablation's
  `meta.parts` [`records_sha256_match`], and each part's cut count equals
  `cuts_recorded` [`cuts_recorded_match`].
- **Earlier runs:** a MINLPLib-only test run (`--quick`) and two earlier full
  runs gave the same results. Each final rerun only added fields.

## Checks

| ID | Check | Result | Source field |
|---|---|---|---|
| A1 | Invalid/material flags of all 6,267 cuts × 2 variants, recomputed exactly from stored `u1`/`u2` (hex) and `certified` (rational); `*_excess` strings | 0 mismatches | `A_flags` |
| A2 | MINLPLib table (8 parts + total, 18 numbers per row), from JSON flags and from my own removal recomputation | identical to the summary | `A_table_mismatches` (empty), `A_counts` |
| A3 | Path table (5 parts + total, 20 numbers per row, incl. KW), both ways | identical | same |
| A4 | Per-model lists (U1/U2 material, U1/U2 removing), both ways | identical | `A_model_lists_match` |
| A5 | JSON `summary` and `meta.key_counts` versus JSON `cuts` | consistent | `A_summary_mismatches`, `A_key_counts_mismatches` (empty) |
| A6 | Lower-bound cuts: 151 (43 distinct, 3 models); Arb 142, Bernstein 9; U1 and U2 material for 151; 7 U1 removals, all Bernstein on ex4_1_8; 0 U2; control 0 | identical | `A_lower` |
| A7 | U2-material MINLPLib cuts whose SLSQP runs all stopped after at most one iteration: 166 (nvs02 155, kall_ellipsoids_tc05a 8, kall_ellipsoids_tc02b 3) | identical | `A_minlplib_u2_one_iteration` |
| A8 | Reconstruction 6,267/6,267; certified = `exact_support` for 6,116/6,116 (recount of JSON flags) | identical | `A_reconstruction` |
| A9 | Path sample: `random.Random(0).sample(range(138000), 1000)` reproduced; per part 47/235/170/208/340; JSON entry indices equal the sample | identical | `sample_check` |
| A10 | Record-file SHA-256 and cut counts of all 13 parts | 13/13 | `records_sha256_match`, `cuts_recorded_match` |
| B1 | Feasible-point pool rebuilt: incumbents per model equal `meta.incumbents_per_model`; path models have 10 to 18 points (60 models) | identical | `incumbents_per_model_match_json`, `path_points_per_model` |
| B2 | For all 3,096 materially invalid cuts: c = L − Σ μ_j a_j and r = β − Σ μ_j b_j from the binding; L and μ equal the recorded binary64 direction (a, λ); β equals `support_witness.rhs`; columns map to `x<i>` | 0 problems | `B_binding_problems` |
| B3 | Uncertified row c^T v ≥ r + (U − β) evaluated exactly at every pooled point, for every materially invalid cut-variant | removed sets equal the JSON for every cut-variant; 1,077 removing cut-variants and 13,649 removing (cut, point) pairs, each above 1e-6·max(1,‖c‖₁) | `B_removed_set_mismatches` (empty), `B_removal_cut_variants`, `B_removal_pairs` |
| B4 | Cited incumbents: 791 distinct sources, all resolved to a record with `primal_check.passed` true or to a case witness | all | `B_cited_sources`, `B_cited_unresolved`, `B_cited_not_passed`, `B_removal_all_passed` |
| B5 | Control at the same points: certified exact row and exported binary64 row | beyond tolerance: 0 and 0 | `B_removal_cert_row_beyond_threshold`, `B_exported_row_violated_beyond_threshold` |
| B6 | Seed-1 sample of 300 removing cut-variants (reported separately; all 1,077 are checked in B3) | all pass; min ratio 1.135 | `B_seed1_*` |
| B7 | C4 U2 removals: n80_s5 cut 955, n80_s9 cuts 169 and 1089 (all frozen-wide root runs); each removes 9 of 10 points including the witness | identical | `B_c4_u2_removals` |
| B8 | kall_ellipsoids_tc02b cut 7 (U2): 3 rows; each removes 3 of 9 points; max violation 0.2031 | identical | `B_tc02b_u2_removals` |
| B9 | Path case witnesses (60 cases): exact feasibility on the case model | all exactly feasible (bound, row and integrality violation 0) | `witness_checks` |
| B10 | Broader control: certified exact row and exported row of every recorded row (5,267 MINLPLib + 138,000 path) at every pooled point of its model | **58 evaluations beyond tolerance** (see below) | `broad_control`, `broad_examples` |
| B11 | Export census and an independent safety test (exported rhs ≤ r + Σ min(e_i lo_i, e_i hi_i), e = exported − exact, binding bounds) | census identical; 5,267/5,267 and 138,000/138,000 safe under both tests | `census` |
| C1 | Seed-2 sample of 100 materially invalid exact cuts (57 MINLPLib, 43 path; 5 also U2-material). Checks: U > certified exactly and materially; certified = record `lower_bound` = `exact_support`; coefficients agree; minimizer in the box and on the domain rows exactly; exact a^T u + λ^T g(u) at the minimizer equals the certified value, from the feature strings (ast + Fraction) and from the witness's typed feature trees | 100/100 on every item | `C_sample`, `C_sample_indices` |
| C2 | The same for all 2,945 materially invalid exact cuts (303 also U2-material) | 2,945/2,945 | `C_all` |
| C3 | U is attained at its recorded point. The exact objective at `u1_point`/`u2_point` matches U within 1.34e-16 / 4.44e-16 relative, and the points lie in the box and on the domain rows exactly (materially invalid cuts) | yes | `C_all.u*_point_*` |
| D1 | Manuscript: U1 and U2 "are upper bounds on the true support value" | holds only up to rounding (see below) | `A_U_below_certified_exact` |
| D2 | Summary: "C4 replay not finished" | now finished and passed | `experiments/v4/runs/partC4/replay.json` |

Result: 26 checks, 23 match. B10 contradicts the broad manuscript sentence of
claim (3). D1 is a wording issue in the manuscript, and D2 an outdated
statement in the summary.

## Details

### Claim (3): certified rows at recorded points (B5, B10)

- **Within the ablation's scope** (rows of materially invalid cuts), the
  certified row is violated beyond the tolerance at 0 points
  [`B_removal_cert_row_beyond_threshold`]. In exact arithmetic it is violated by
  a positive amount at 355 point evaluations. The largest violation is 6.87e-7
  relative to max(1,‖c‖₁), below the 1e-6 tolerance
  [`B_cert_row_strictly_violated_point_evaluations`,
  `B_max_relative_certified_violation`].
- **st_e22, all recorded rows.** 51 point evaluations exceed the tolerance
  [`broad_examples`]. The row of each of 3 parts (v3/partA-full,
  v3/partA-root, v3d/partA-root-rowdir) is evaluated at the same 17 pooled
  incumbents. The row is t ≥ −85 on the objective epigraph.
  - −85 is the true optimum: the certified minimizer (7, 3) attains it, and the
    MINLPLib reference primal is −85.0.
  - The incumbents are (7.00000007, 3.00000003), with objective −85.0000017.
    They pass the primal check with max scaled violation 1.0e-8 (tolerance
    1e-5), but they lie slightly outside the feasible set. So the row is
    violated by 1.70e-6, while the threshold is 1e-6.
  - These rows are not materially invalid, so the ablation never evaluated them.
- **Path family, all recorded rows.** 7 point evaluations exceed the tolerance,
  by 1.30e-6 to 3.09e-6 [`broad_examples`]. All rows are single-variable bounds
  (norm 1). All points are Gurobi-mode incumbents with max scaled violation
  6.7e-7 to 1.13e-6:
  - interleaved_path_n10_s4 (1 evaluation);
  - interleaved_path_n20_s4 (1);
  - interleaved_path_n20_s6 (5).
- **Scale.** Over all rows, the certified row is strictly violated (by a
  positive amount) at 3,503 of 41,018 MINLPLib evaluations and 14,079 of
  851,300 path evaluations. These counts are over distinct rows within a part
  [`broad_control`].
- **Suggested wording:** "No certified row of these cuts was violated beyond
  the tolerance." Alternatively, state the tolerance effect for the
  approximately feasible incumbents.

### Robustness of the removal counts (B3)

The removal tolerance 1e-6·max(1,‖c‖₁) is close to the feasibility tolerance of
the incumbents. The cited points have max scaled violation up to 1.13e-6
[`B_removal_max_scaled_violation_of_points`]. The smallest removing violation
is 1.135 times the threshold [`B_removal_min_ratio`]. The counts barely change
under stricter tests [`B_removal_robustness`, `B_removal_threshold_x10_*`]:

| Family / variant | Protocol | Discount the point's certified-row violation | Threshold × 10 | Point satisfies certified row exactly |
|---|---:|---:|---:|---:|
| MINLPLib U1 | 405 | 405 | 389 | 403 |
| MINLPLib U2 | 132 | 132 | 128 | 132 |
| Path U1 | 506 | 506 | 503 | 505 |
| Path U2 | 27 | 27 | 27 | 27 |

- **Models.** With the threshold × 10, the model lists are unchanged:
  - MINLPLib U1: 7 models. nvs02 drops from 129 to 125 and
    cvxnonsep_normcon20r from 91 to 83; kall_ellipsoids_tc02b drops from 52
    to 48.
  - MINLPLib U2: 2 models (nvs02 125, kall_ellipsoids_tc02b 3).
- **Known witness.** The path known-witness counts (404 and 13) use exactly
  feasible witnesses (B9), so the tolerance does not inflate them.
- **SCIP incumbents.** Every removing cut-variant removes at least one
  SCIP-mode incumbent, not only Gurobi incumbents or case witnesses
  [`B_removal_point_sources`]. So "a feasible point that SCIP had returned" is
  accurate.
- **nvs02 epigraph rows.** The removing rows of nvs02 use the objective
  epigraph column, with t set to the incumbent's float objective. To undo the
  smallest such violation, t would have to increase by at least 2.39e-4
  [`B_epigraph_min_t_slack_needed`]. That is far larger than any float error in
  the objective.

### Certified minimizers (C1, C2)

- **Seed-2 sample.** The 100 cuts are `C_sample_indices` (positions in the
  JSON `cuts`), drawn as `random.Random(2).sample(population, 100)`. The
  population is the 2,945 exact cuts with u1_material or u2_material (every
  U2-material cut is also U1-material).
- **Results.** For every sampled cut:
  - U1 (and U2 where it is material) exceeds the certified value exactly and
    by more than 1e-6·max(1,|value|);
  - the certified value equals the record's `support_witness.lower_bound` and
    `support_stats.exact_support`;
  - the minimizer equals the JSON copy, lies in the box, and satisfies the
    domain rows exactly;
  - the exact objective at the minimizer equals the certified value under both
    evaluators.

  So every materially invalid constant has an exact feasible counterexample,
  independent of the oracle's proof. The same holds for all 2,945 cuts
  [`C_all`].

### U below the certified value (D1)

Counted in exact arithmetic over the exact-certificate cuts
[`A_U_below_certified_exact`]:

| Family | Variant | Cuts with U < certified value | Largest relative deficit |
|---|---|---:|---:|
| MINLPLib | U1 | 1,011 | 3.3e-16 |
| MINLPLib | U2 | 2,121 | 1.05e-12 |
| Path | U1 | 8 | 5.0e-17 |
| Path | U2 | 170 | 2.2e-16 |

- **Cause.** These deficits are binary64 evaluation rounding and, for U2,
  SLSQP points accepted within the 1e-9 row tolerance.
- **Fix.** The sentence in `08b-validity.tex` should say "upper bounds up to
  rounding" or something equivalent.

### C4 replay (D2)

`experiments/v4/runs/partC4/replay.json` (written 18:18 EDT by the other
session's `replay_v4.py`; I only read it) reports:

- `passed` true and `archived_passed` true;
- 180 records, 160 admitted runs;
- 48,000 of 48,000 cuts replayed, with 0 missing cut logs.

So the C4 cuts in the ablation are now covered by a passing replay.

### Notes

- **C4 witness objectives.** For 15 of the 20 C4 cases, the exact objective of
  `known_witness_exact` exceeds `known_optimum_exact` by 2.1e-17 to 6.9e-16
  (relative at most 3.9e-16). The witness coordinates are binary64 roundings,
  and the witness is still exactly feasible. The path objective is linear and
  path rows have no epigraph column, so this does not affect any count. The
  "known optimal witness" is optimal up to 3.9e-16 relative.
- **Excluded record.** One D-root record (waternd2) has `original_values` but
  did not pass the primal check, so it is excluded from the pool, as the rule
  says [`excluded_records_with_values_not_passed`].
- **Gurobi incumbents.** The pool contains 60 Gurobi-mode incumbents
  [`B_pool_modes`]. They are recorded feasible points from Gurobi runs, not
  points that SCIP returned.

## Not checked

- **U1 and U2 themselves.** I did not recompute the snapshot's `_sample` set
  or the SLSQP runs. C3 shows only that each stored U is attained at its stored
  point, and that the point is feasible.
- **SLSQP diagnostic.** I did not check the claims based on
  `evidence/ablation-slsqp-check.json`, such as the ftol 1e-14 results,
  |gᵀs| ≤ 7.39e-7 and the 465 starts.
- **Run details.** I did not check the timing and run-environment statements
  of the summary.
- **Incumbent feasibility.** I took incumbent feasibility from
  `primal_check.passed`; I did not run my own primal check of the MINLPLib or
  path incumbents. Only the path case witnesses were checked exactly (B9).
