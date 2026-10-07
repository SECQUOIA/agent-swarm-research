# Part U, final run: what certification buys (campaigns 3 and 4)

Written 2026-10-03. Protocol: `experiments/campaign-v4-protocol.md`, Amendment 1,
Part U. No SCIP or Gurobi solve was started. No record, case, snapshot or code
under `experiments/` was changed. The manuscript was not edited.

## Main result

- **MINLPLib parts (A, B, B2, D), exact certificates, 5,116 cuts.** The sample
  minimum (U1) is materially invalid for 1,969 cuts, on 12 models. 405 of the
  resulting rows would remove a recorded feasible point, on 7 models. Adding
  SLSQP (U2) leaves 230 materially invalid cuts on 4 models. 132 of their rows
  would remove a recorded feasible point, on 2 models: nvs02 (129) and
  kall_ellipsoids_tc02b (3).
- **Path family, sample of 1,000 cuts from 138,000.** U1 is materially invalid
  for 976 cuts. 506 rows would remove a recorded feasible point, and 404 of
  them remove the known optimal witness. U2 is materially invalid for 73 cuts.
  27 rows would remove a feasible point, and 13 of them remove the known
  witness.
- **Controls.** The certified row is violated at 0 points (it is evaluated at
  the same points as the uncertified rows). There are 0 reconstruction
  failures. Every exported row is safe (5,267 of 5,267 MINLPLib rows and
  138,000 of 138,000 path-family rows).

## Commands run (targeted; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
P=/workspace/minlp-notes/paper-certified-support-cuts
E=$P/experiments
# 1. Smoke test on campaign-4 records (output to a mktemp directory, then deleted)
T=$(mktemp -d)
$PY $P/verification/ablation_uncertified.py --minlplib $E/v4/runs/partD-full --path $E/v4/runs/partC4 \
    --sample-size 30 --workers 4 --out-md $T/smoke.md --out-json $T/smoke.json
# 2. Preserve the campaign-3-only outputs (byte-identical copies; SHA-256 checked)
cp -p $P/evidence/ablation-uncertified.md   $P/evidence/ablation-uncertified-c3only.md
cp -p $P/evidence/ablation-uncertified.json $P/evidence/ablation-uncertified-c3only.json
# 3. Final run (exactly the command of the task)
$PY $P/verification/ablation_uncertified.py \
  --minlplib $E/v3/runs/partA-full $E/v3/runs/partA-root $E/v3/runs/partB \
             $E/v3d/runs/partA-root-rowdir $E/v3d/runs/partB-root-rowdir \
             $E/v4/runs/partB2 $E/v4/runs/partD-root $E/v4/runs/partD-full \
  --path $E/v3/runs/partC $E/v3d/runs/partC-rowdir $E/v4/runs/partC2 $E/v4/runs/partC3 $E/v4/runs/partC4 \
  --workers 12 --out-md $P/evidence/ablation-uncertified.md --out-json $P/evidence/ablation-uncertified.json
# 4. SLSQP diagnostic (new, read-only; writes evidence/ablation-slsqp-check.json)
$PY $P/verification/ablation_slsqp_check.py
```

- **Smoke test.** Exit 0 in 27.7 s wall time. It analyzed 58 cuts (all 28
  cuts of D-full and a 30-cut sample of C4). Worker errors: 0. Binding
  mismatches: 0. Control violations: 0.
- **No adaptation needed.** `ablation_uncertified.py` reads campaign-4
  directories unchanged, because each v4 run directory has the same layout
  (`snapshot/research-20261003-convexification/solver/integration.py`, SHA-256
  `35b5a4fd928e...`). `Config(**record['config'])` accepts the added
  `row_directions` field. So no `ablation_uncertified_v4.py` was made.
- **Final run.** Exit 0. It ran from 2026-10-03 21:52:43 to 21:54:56 UTC:
  2 min 12.9 s wall time and 4 min 21 s user time. `meta.elapsed_seconds` is
  132.0. The script caps parallelism at `MAX_WORKERS = 4`, so `--workers 12`
  ran 4 worker processes, each single-threaded.
- **SLSQP diagnostic.** Exit 0 in 18.3 s.
- **Other analysis.** The per-part "distinct" and per-model counts below were
  computed read-only from `cuts` in the JSON, with the key of
  `family_counts`: (model, block variables, binary64 direction). The snippet
  is at the end of this file.

The archived replay of Part C4 (`replay_v4.py runs/partC4`, started by another
session at 17:50 EDT) was still running when this summary was written, and
`runs/partC4/replay.json` did not exist yet. This ablation used the certified
values stored in the C4 records. For all 340 sampled C4 cuts, the reconstruction
reproduces the stored binding, and the certified value equals the recorded exact
minimum. Check the C4 replay result before citing C4 numbers.

## Files

- `evidence/ablation-uncertified.md` and `.json`: final run (new).
- `evidence/ablation-uncertified-c3only.md` and `.json`: the earlier
  campaign-3-only run. They are byte-identical copies, and the copy of the .md
  still names `ablation-uncertified.json` as its data file; its data are now
  in `ablation-uncertified-c3only.json`.
- `verification/ablation_slsqp_check.py` and
  `evidence/ablation-slsqp-check.json`: the SLSQP diagnostic (new).

## Inputs

There are 13 parts. The MINLPLib parts analyze all 5,267 recorded cuts.
The path-family sample is `random.Random(0).sample(range(138000), 1000)` over
the concatenated cut lists of v3/partC (6,000 cuts), v3d/partC-rowdir
(30,000), v4/partC2 (24,000), v4/partC3 (30,000) and v4/partC4 (48,000). The
sample sizes per part are 47, 235, 170, 208 and 340. Source: `meta.parts` and
`meta.sample` in `ablation-uncertified.json`, and the Inputs table in
`ablation-uncertified.md`.

Every campaign-4 cut uses the `quadratic_polytope` oracle (an exact
certificate). The only lower-bound certificates (Arb, Bernstein) are in the
campaign-3 Part A records.

## U1 and U2 counts, exact certificates

The tables use these terms:

- **inv**: the uncertified constant exceeds the certified exact minimum.
- **mat**: materially invalid, meaning the excess is larger than
  1e-6·max(1,|value|).
- **rem**: materially invalid cuts whose uncertified row is violated by more
  than 1e-6·max(1,‖c‖₁) at one or more recorded feasible points of the same
  model.
- **(d, m)**: number of distinct cuts and number of models, both counted
  within the row.
- **ctl**: cuts whose certified row is violated at one of the same points.
- **KW**: rem cuts that remove the case file's known optimal witness.

Sources:

- inv, mat, rem and model counts: `summary[part].quadratic_polytope.{u1,u2}`
  (`exceeds`, `material`, `removing_cuts`, `material_models`,
  `removing_models`, `removing_known_witness`,
  `certified_row_violated_cuts`).
- "All" rows: `meta.key_counts["minlplib/exact"]` and
  `meta.key_counts["path/exact"]`.
- Distinct counts per part: computed from `cuts` (snippet below).

### MINLPLib parts

| Part | Cuts (d, m) | U1 inv | U1 mat (d, m) | U1 rem (d, m) | U2 inv | U2 mat (d, m) | U2 rem (d, m) | ctl |
|---|---|---:|---|---|---:|---|---|---:|
| v3/partA-full | 149 (38, 9) | 81 | 72 (24, 4) | 21 (7, 2) | 18 | 0 | 0 | 0 |
| v3/partA-root | 409 (360, 9) | 313 | 280 (256, 4) | 55 (48, 4) | 88 | 0 | 0 | 0 |
| v3/partB | 845 (366, 25) | 366 | 191 (71, 4) | 96 (33, 2) | 239 | 65 (26, 1) | 51 (24, 1) | 0 |
| v3d/partA-root-rowdir | 413 (360, 9) | 313 | 280 (256, 4) | 55 (48, 4) | 88 | 0 | 0 | 0 |
| v3d/partB-root-rowdir | 529 (366, 25) | 207 | 108 (70, 4) | 51 (32, 2) | 140 | 36 (25, 1) | 30 (23, 1) | 0 |
| v4/partB2 | 1007 (455, 25) | 427 | 238 (109, 4) | 75 (33, 2) | 302 | 76 (37, 2) | 48 (24, 1) | 0 |
| v4/partD-root | 1736 (897, 13) | 1229 | 772 (385, 4) | 48 (24, 1) | 734 | 51 (26, 2) | 1 (1, 1) | 0 |
| v4/partD-full | 28 (14, 2) | 28 | 28 (14, 2) | 4 (2, 1) | 12 | 2 (1, 1) | 2 (1, 1) | 0 |
| **All MINLPLib** | 5116 (1773, 47) | 2964 | 1969 (765, 12) | 405 (105, 7) | 1621 | 230 (63, 4) | 132 (25, 2) | 0 |

Models in the "All MINLPLib" row (cut counts from `cuts`):

- **U1 materially invalid (12 models):** cvxnonsep_normcon20r 460,
  kall_ellipsoids_tc02b 399, kall_ellipsoids_tc05a 364, nvs02 194,
  kall_circlespolygons_c1p12 148, ex8_1_7 102, prob06 93,
  p_ball_10b_5p_2d_m 87, ex8_3_4 46, ex4_1_8 39,
  kall_circlesrectangles_c6r1 22, kriging_peaks-full100 15.
- **U1 removing (7 models):** nvs02 129, prob06 93, cvxnonsep_normcon20r 91,
  kall_ellipsoids_tc02b 52, ex8_3_4 32, ex4_1_8 6, p_ball_10b_5p_2d_m 2.
- **U2 materially invalid (4 models):** nvs02 155, kall_ellipsoids_tc05a 32,
  kall_circlespolygons_c1p12 22, kall_ellipsoids_tc02b 21.
- **U2 removing (2 models):** nvs02 129, kall_ellipsoids_tc02b 3.

There are no known witnesses for MINLPLib models (KW = 0).

Every materially invalid cut is also *witnessed*: the recorded certified
minimizer is exactly feasible, and its exact objective value lies below the
uncertified constant by more than the material tolerance (`Witnessed` column of
the removal table in `ablation-uncertified.md`).

### Path family (sample)

| Part | Cuts (d, m) | U1 inv | U1 mat (d, m) | U1 rem (d, m) | U1 KW | U2 inv | U2 mat (d, m) | U2 rem (d, m) | U2 KW | ctl |
|---|---|---:|---|---|---:|---:|---|---|---:|---:|
| v3/partC | 47 (47, 15) | 47 | 47 (47, 15) | 25 (25, 13) | 16 | 37 | 6 (6, 5) | 2 (2, 2) | 1 | 0 |
| v3d/partC-rowdir | 235 (234, 20) | 234 | 234 (233, 20) | 118 (117, 18) | 94 | 195 | 17 (17, 10) | 9 (9, 7) | 5 | 0 |
| v4/partC2 | 170 (169, 19) | 167 | 166 (165, 19) | 89 (89, 15) | 67 | 134 | 15 (15, 8) | 6 (6, 6) | 2 | 0 |
| v4/partC3 | 208 (208, 20) | 202 | 199 (199, 20) | 111 (111, 19) | 82 | 161 | 15 (15, 10) | 7 (7, 6) | 2 | 0 |
| v4/partC4 | 340 (337, 20) | 333 | 330 (329, 20) | 163 (163, 20) | 145 | 266 | 20 (20, 14) | 3 (3, 2) | 3 | 0 |
| **All path** | 1000 (995, 60) | 983 | 976 (973, 60) | 506 (505, 58) | 404 | 793 | 73 (73, 37) | 27 (27, 19) | 13 | 0 |

Feasible points per path model: 10 to 18 (median 10), counting incumbents
pooled by `model_sha256` across parts plus the case witness. The 60 case
witnesses come from v3/partC (20 models, also used for the identical C2
models), v4/partC3 (20) and v4/partC4 (20). Source: `meta.case_witnesses` and
"Incumbents available per model" in `ablation-uncertified.md`.

For C4, the known witness is the case file's `known_witness_exact`. Per
`mechanism_c4.py`, it is the exact optimum with y rounded down and t rounded
up to binary64, and it passes the archived primal check. The 3 C4 U2 removals
are on interleaved_path_coupled_n80_s5 (run 020 root frozen-wide, cut 955) and
interleaved_path_coupled_n80_s9 (run 024 root frozen-wide, cuts 169 and 1089).
Each removes 9 of the 10 feasible points of its model, including the known
witness.

## Lower-bound certificates (Arb, Bernstein)

There are 151 cuts: 43 distinct, on 3 models (cvxnonsep_psig20r, ex4_1_8,
syn05m). Arb has 142 cuts (36 + 53 + 53) and Bernstein 9 (3 + 3 + 3), in
v3/partA-full, v3/partA-root and v3d/partA-root-rowdir. The campaign-4 parts
have none.

- U1 and U2 both exceed the certified bound materially for all 151 cuts. These
  cuts are not counted as invalid, because a certified lower bound is not the
  minimum.
- Removal: 7 U1 rows remove a recorded feasible point, all Bernstein cuts on
  ex4_1_8 (3 + 2 + 2). No U2 row does.
- Control: 0.

Source: `meta.key_counts["minlplib/lower"]` and `summary[part].{arb,bernstein}`.
These counts are identical to the campaign-3-only run.

## Reconstruction

- 6,267 of 6,267 analyzed cuts were reconstructed exactly: the snapshot's
  `_prepare` gives the stored binding, the feature strings round-trip, and the
  box is binary64-exact. Worker errors: 0. Binding mismatches: 0.
- For 6,116 of 6,116 exact-certificate cuts, `support_witness.lower_bound`
  equals `support_stats.exact_support`.
- Row-check errors: 0, and no feasible point lacked a column.

Source: "Reconstruction" paragraph of `ablation-uncertified.md`;
`summary[*][*].{u1,u2}.row_check_errors`.

## Export census (every recorded cut, not only the sample)

Source: `export_census` in the JSON; "Exported rows" table of the .md.

| Family | Rows | Rounded coefficients | Nonzero E | Safe | max abs(E) | max rel. rhs rounding |
|---|---:|---:|---:|---:|---:|---:|
| MINLPLib (8 parts) | 5,267 | 710 (13.5%) | 432 | 5,267 | 8.48e-16 (v4/partD-root) | 2.17e-16 |
| Path family (5 parts) | 138,000 | 127,678 (92.5%) | 99,862 | 138,000 | 2.12e-16 (v4/partC2) | 2.09e-16 |

Share of rows with rounded coefficients, by part:

- **MINLPLib:** v3/partA-full 15/188 (8.0%), v3/partA-root 56/465 (12.0%),
  v3/partB 162/845 (19.2%), v3d/partA-root-rowdir 56/469 (11.9%),
  v3d/partB-root-rowdir 85/529 (16.1%), v4/partB2 121/1007 (12.0%),
  v4/partD-root 209/1736 (12.0%), v4/partD-full 6/28 (21.4%).
- **Path family:** v3/partC 97.0%, v3d/partC-rowdir 89.0%, v4/partC2 95.9%,
  v4/partC3 91.0%, v4/partC4 93.4%.

The largest relative abs(E), abs(E)/max(1,|r|), is 8.48e-16 for MINLPLib and
1.52e-16 for the path family. In the campaign-3 parts the largest abs(E) was
2.22e-16; the campaign-4 maximum of 8.48e-16 is on v4/partD-root.

## Why SLSQP leaves materially invalid U2 constants

Source: `summary` in `evidence/ablation-slsqp-check.json`.

The diagnostic reran SLSQP from the 3 recorded starts of every U2-materially
invalid cut:

- once with the ablation settings (ftol 1e-6, maxiter 200);
- once with ftol 1e-14 and maxiter 1000.

The default reruns reproduce every recorded SLSQP value and iteration count
(918 of 918 starts). None of these cuts has domain rows, so the feasible set
is the block box. A start is called *stationary* if the infinity norm of its
projected gradient is at most 1e-12.

Of the 230 U2-materially invalid MINLPLib cuts, 166 had every SLSQP run stop
after at most one iteration: nvs02 155, kall_ellipsoids_tc05a 8 and
kall_ellipsoids_tc02b 3 (`meta.key_counts["minlplib/exact"].u2.slsqp_one_iteration`,
split by model from `cuts`).

### nvs02 (recurs in B2)

nvs02 has 155 U2-materially invalid cuts (26 distinct): v3/partB 65,
v3d/partB-root-rowdir 36 and v4/partB2 54. 129 of them remove recorded
feasible points: 51, 30 and 48. All 155 come from 4D or 3D blocks whose
widest box side is 200.

- **SLSQP never moves.** At all 465 starts, SLSQP returns "Optimization
  terminated successfully" after 1 iteration, at the start point itself.
- **Cause: the default tolerance.** SLSQP's first quadratic subproblem uses
  the identity as Hessian, so its first search direction is the box-projected
  negative gradient s. The directional derivative |gᵀs| along s is at most
  7.39e-7 at every start. That is below ftol = 1e-6, so SLSQP's convergence
  test passes before any line search. Of the 465 starts, 56 are exactly
  stationary. At the others, the largest projected-gradient entry is at most
  8.6e-4.
- **Effect of a tighter tolerance.** With ftol 1e-14, 139 of the 155 cuts
  reach the certified value within the material tolerance (up to 35
  iterations). The other 16 stay above it, by at most 2.1e-4.

This agrees with the explanation in `sections/08b-validity.tex`: SLSQP stops
after one iteration because its default absolute tolerance is too large for
this block. More precisely, the tolerance is larger than the directional
derivative along the first step.

### Models that are new in the campaign-4 parts

- **kall_circlespolygons_c1p12 (B2; campaign-3 model).** It has 22
  U2-materially invalid cuts (11 distinct). All come from 4D blocks found only
  in the presolve-off modes all-diag-noaggr and all-diag-rowdir-noaggr: B2 has
  211 cuts on this model, while v3/partB has 25 cuts, all in mode all-diag.
  SLSQP converges in 2 to 3 iterations to non-global local minima. Tightening
  ftol gives the same values (22 of 22 still materially invalid; excess 0.033
  to 0.094). None of these rows removes a recorded feasible point (19 points).
- **kall_ellipsoids_tc02b (Part D; new model).** It has 21 U2-materially
  invalid cuts (10 distinct).
  - In 16 of them, SLSQP stopped early under the default tolerance after 1 to
    3 iterations, with relative excess at most 5.1e-4. With ftol 1e-14 they
    reach the certified value.
  - 3 of them are the direction of cut 7 in three runs (all-diag root, all
    and auto full). All three starts are exact stationary points with value 0
    (first-order stationary points on the face x43 = −1 that are not local
    minima), and the certified minimum is −1/4 at
    (1/2, 1, −1). Only these 3 rows remove recorded feasible points: 3 of 9
    points, maximum violation 0.203. This is the only U2 removal outside
    nvs02.
  - 2 of them (cut 137) converge to a local minimum: −0.03889 against the
    certified −0.04167.
- **kall_ellipsoids_tc05a (Part D; new model).** It has 32 U2-materially
  invalid cuts (16 distinct). 48 of the 96 starts stop at the start point after
  one iteration: 44 are exactly stationary and 4 have |gᵀs| ≤ 1.1e-11. The
  other 48 starts converge in 2 to 7 iterations to non-global local minima.
  Tightening ftol does not help (32 of 32 remain; excess up to 0.25). No run
  of this model found a feasible point (all 9 D runs have no
  `original_values`), so the removal test has no points. All 32 cuts are
  witnessed by the certified minimizer.
- **Part D models with U1 errors only:** kall_circlesrectangles_c6r1 (22 cuts)
  and kriging_peaks-full100 (15). SLSQP corrects both, and none of their rows
  removes a recorded feasible point.
- **Path family, new instances (C3 s5–s9 and C4 coupled).** Every one of the
  40 new models has U1-materially invalid cuts. The 73 U2-materially invalid
  path cuts are all non-global local minima: SLSQP takes 1 to 3 iterations,
  and 31 of 219 starts are exactly stationary. With ftol 1e-14 the best value
  drops for 23 of the 73 cuts, but none of the 73 becomes immaterial (largest
  excess 0.030). This is the same behavior as in campaign 3.

## Comparison with the campaign-3-only run

- **Campaign-3 MINLPLib numbers are unchanged.** For the 5 campaign-3
  MINLPLib parts, `summary` and `export_census` are identical to
  `ablation-uncertified-c3only.json`, and the 2,507 cuts present in both runs
  have identical U1 and U2. More incumbents are now pooled per model (nvs02:
  19 points instead of 14), but the removal counts did not change.
- **The path-family sample is new.** The population grew from 36,000 to
  138,000 cuts with the same seed 0, so the v3 and v3d path rows are a
  different sample (47 + 235 cuts instead of 180 + 820).

Manuscript statements in `sections/08b-validity.tex` that depend on these
numbers. They are not edited here.

- "8 to 19%" of MINLPLib rows rounded: 8.0 to 21.4% with campaign 4.
- Bound correction "at most 2.2e-16": 8.48e-16 with campaign 4.
- "40% of the cuts": 1,969/5,116 = 38.5%. The campaign-3 figure was
  931/2,345 = 39.7%.
- "278 ... rows ... on six models": 405 rows on 7 models.
- "the remaining ones are on nvs02": now nvs02, kall_circlespolygons_c1p12,
  kall_ellipsoids_tc02b and kall_ellipsoids_tc05a, with removals only on nvs02
  and kall_ellipsoids_tc02b.
- "more than a third" of path-family rows remove the known optimum:
  404/1,000.
- `\input{sections/08b-ablation-table}` points to a file that does not exist.

## Snippet used for the per-part distinct and model counts

```python
import json
d = json.load(open("evidence/ablation-uncertified.json"))
key = lambda r: (r["name"], tuple(r["variables"]), tuple(r["coefficients"]))
for part in [p["label"] for p in d["meta"]["parts"]]:
    g = [r for r in d["cuts"] if r["part"] == part and r["exact_certificate"] and "error" not in r]
    for v in ("u1", "u2"):
        mat = [r for r in g if r[v + "_material"]]
        rem = [r for r in mat if r[v + "_rows"]["removed"]]
        print(part, v, len({key(r) for r in mat}), len({r["name"] for r in mat}),
              len({key(r) for r in rem}), len({r["name"] for r in rem}))
```
