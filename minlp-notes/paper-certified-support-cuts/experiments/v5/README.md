# Campaign 5 runner

Implements Parts 5S, 5C-a and 5C-b of `../campaign-v5-protocol.md`, including its
Amendment 1 (5C-b modes use max_rounds 40). Part 5U3 is
not part of this runner. Nothing here modifies `../v4/`, `../v3/`, `../v3d/` or
`research-2026100*-convexification/`. Files from those directories are read
only, with hash checks.

Status: built, tested and smoke-tested. The job directories under `runs/` and
the main runs are built and launched by the campaign coordinator, not by this
build. All three parts were built against the current snapshot (manifest
`b9c4ba84...`).

## Files

| File | Role |
|---|---|
| `snapshot.py` | Builds `snapshot/` from the manifest-verified campaign-4 snapshot (`../v4/snapshot`, manifest `098bda40...`, integration.py `35b5a4fd...`). It applies the two protocol additions to `research-20261003-convexification/solver/integration.py` by exact text replacement (`PATCHES`) and adds the runner files of `common.RUNNER_FILES` and the protocol. It copies the campaign-4 `scip-parameters.json` unchanged (campaign 5 adds no SCIP parameter; the worker's sets must equal it) and writes `snapshot-info.json` (including the patch hashes) and `source-manifest.json`. It refuses to overwrite an existing snapshot. |
| `stars.py` | Part 5S generator: exact case data, the exact optimum by piece enumeration in rationals, a cross-check against `verification/M3_star_sweep.py` (loaded read-only), and the witness (docstring). |
| `mechanism.py` | Byte-identical copy of `../v4/mechanism.py` (C3 generator), used to verify the C3 cases. |
| `make_jobs.py` | Creates one output directory per part (`partS5`, `partC5a`, `partC5b`) in the campaign-2/3/4 layout: `cases/`; a snapshot copy with `frozen-cases/`; `source-manifest.json`, `jobs.json` and `build.json`; and `c5-inputs/`, which holds copies and SHA-256 of the files the cases were checked against. `--smoke` uses the smallest instance(s) at 10 s soft / 30 s hard. |
| `v5_worker.py` | Copy of `v4_worker.py`. Every campaign-4 mode is unchanged; the campaign-5 modes and the certification log are added. |
| `driver.py` | The campaign-4 driver. Only the worker path and the slot directory (`v5/.slots`, six slots shared by all campaign-5 drivers) differ. It is resumable; stop it with SIGTERM. |
| `replay_v5.py` | The campaign-4 replay wrapper, plus tampering controls on the first star cut of every mode that has star cuts, and a check of the per-record `cut_methods`. |
| `summarize_v5.py` | `summarize_v4.py` plus the star and bound-(ii) metrics, the certification-by-method table, grouping by family (`star`, `mechanism` = C3, `mechanism-coupled` = C4), and several campaign-4 reference directories (`DIR=REF1,REF2`; modes `c4:<mode>`). |
| `test_v5.py` | Targeted tests (below). |
| `smoke/` | Smoke runs, replays and `smoke/results.md` (not for the paper). `smoke/partS5`, `smoke/partC5a` and `smoke/partC5b` were built and run with `snapshot-smoke/`. `smoke/partC5b-amended` was built and run with `snapshot/`, after Amendment 1. |
| `snapshot-smoke/` | The snapshot before Amendment 1 (manifest `e8f0152e...`), kept unchanged because the first three smoke directories refer to it. It differs from `snapshot/` only in `v5_worker.py` (5C-b max_rounds 10 instead of 40), `test_v5.py` and the protocol file (without the amendment). Do not use it for new runs. |

## Code: the two additions

Snapshot `integration.py` SHA-256
`9eab51a09ed1bdcdef60e6bfdff7c5238c12e601401b7086ece1c3f122af8971`. Snapshot
manifest SHA-256 `b9c4ba84332e53a91d486a50572c8acd0741f88526763e5a8d098a841953db3a`
(97 files; it was rebuilt after Amendment 1; the earlier snapshot is
`snapshot-smoke/`, manifest `e8f0152e...`, with the same `integration.py`).
Patch-list hash (`snapshot.patch_digests()["all"]`, SHA-256 of the
JSON of `PATCHES`):
`9a5a635bb98127665a37274b9e2ea73f3a16de2c7335e4a0f0eb1ca2ed9136fe`. Per patch:

| # | Anchor | SHA-256 |
|---|---|---|
| 1 | `Config` fields `aggregate_directions: bool = False`, `star_leaves: int = 0` | `9abceafc...` |
| 2 | Validation: `aggregate_directions` must be a bool; `star_leaves` must be an int >= 0. The check `max_dimensions > 4` is unchanged. | `be6861b1...` |
| 3 | New `star_variable_sets(admissible, config)` before `discover` | `de18296e...` |
| 4 | `discover`: star entries first, with their own caps on sides and domain rows | `0738dd08...` |
| 5 | Domain-row cap `max_rows` per entry | `a0032050...` |
| 6 | `block_cap_reached` counts all entries | `213af173...` |
| 7 | `discovery['star_blocks']` (only when `star_leaves > 0`) | `6347e9ff...` |
| 8 | `RowSeparator._directions`: block direction first; blocks of more than four variables | `0c818736...` |

The behaviour:

1. **`aggregate_directions`.** When True, `_directions` first yields the
   *block direction* for each block: lambda = 1 for every chosen side, and
   `a_v` = the exact rational sum of the sides' affine coefficients of block
   variable v, rounded once to binary64. This is the support of the sum of the
   block's rows. The directions of the mode then follow unchanged: whole-row
   directions if `row_directions`, then remainder directions, then LP
   directions. A direction already tried for the block is skipped as before.
2. **`star_leaves`.** When positive, `discover` forms star blocks.
   - **Centers.** A center is any variable c that occurs in admissible
     two-variable sides together with at least two other variables.
   - **Leaves.** The block is c plus the first `star_leaves` of these other
     variables in variable order. Equal variable sets are kept once.
   - **Sides and domain rows.** The block gets the first `star_leaves`
     admissible sides that lie in it, and the first `2 * star_leaves + 4`
     affine domain rows.
   - **Order and caps.** Star blocks come first, ordered by center, and they
     count against `max_blocks`. `discovery.star_blocks` records how many were
     kept. All other blocks keep the dimension cap of four and their caps.
   - **Directions.** For a block of more than four variables, `_directions`
     yields only the block direction (if `aggregate_directions`) and, if
     `row_directions`, the whole-row direction of every side. There are no
     remainder directions, no sampling and no LP.

Certification is unchanged. `support.certify_support` enumerates the polytope
only up to dimension 4 (`max_polytope_dimension`). A star block (dimension k + 1
>= 5) therefore falls back to the inherited kernels. Their `_star_center` finds
the center, and the constrained-star oracle (`theory/quadratic_star.py` of
research-20261002) certifies the cut with witness method `quadratic_star`
(format `support-cut-v1`). The archived replay (`experiments/replay.py`)
replays it through `replay_support`, which uses the inherited `replay_star`.

## Modes as implemented (`v5_worker.mode_config`)

All campaign-4 modes are unchanged (`../v4/README.md`; a test compares them
with `v4_worker.mode_config`). Gurobi mode is as in campaign 4. New modes, all
`run_instance` mode `all` with no SCIP parameters:

| Mode | Part | Config overrides |
|---|---|---|
| rowdir-star4 | 5S | star-family limits + `row_directions` |
| agg-star4 | 5S | star-family limits + `aggregate_directions`, `row_directions` |
| agg-star | 5S | agg-star4 + `star_leaves` 16 |
| frozen-cap32 | 5C-b | max_blocks n, max_cuts 32n, max_cuts_per_round 8n, max_support_calls 80n, max_rounds 40 (Amendment 1; 10 in the original protocol text), max_separation_seconds 150, separation_budget_fraction 0.5 |
| rowdir-cap32 | 5C-b | frozen-cap32 + `row_directions` |
| frozen-cap64 | 5C-b | as frozen-cap32 with 64n, 16n, 160n |
| rowdir-cap64 | 5C-b | frozen-cap64 + `row_directions` |

Star-family limits (n stars, k leaves): max_blocks n k, max_cuts 4 n k,
max_cuts_per_round n k, max_support_calls 10 n k, max_rounds 10,
max_separation_seconds 60, separation_budget_fraction 0.5. Part 5S also runs
baseline, baseline-novarlocks, baseline-extra and gurobi, as in campaign 4.

## Measurements added in the worker (frozen solver code unchanged)

- **`certification_log`.** One entry per call of
  `solver.support.certify_support`: block dimension, method, status, whether a
  support was certified, and seconds. The worker wraps the module attribute,
  which the separator imports at each callback. The time covers the whole
  call, including the symbolic preparation, not only the oracle.
  `certification_summary` aggregates the log by method. The run fails if the
  log does not have exactly one entry per separator `certification_calls`.
- **`cut_methods`.** The certificate method (`support_witness.method`) of each
  recorded cut, counted. The replay checks it against the witnesses.
- The campaign-4 measurements (`row_binding_rejection_causes`,
  `native_statistics`) are unchanged.

## Instances and rules as implemented

- **5S instance draw** (`stars.py`). The protocol fixes the draw:
  `random.Random(100000 k + 1000 n + s)`; per star, then per leaf,
  `rng.sample(range(49), 2)` / 64 gives (a1, a2), then `rng.choice` gives d from
  (1/8, 1/4, 1/2, 1).
- **5S variables and rows.**
  - Variables, star by star: y_i, then x_ij and t_ij.
  - Rows 1..nk: Phi_ij - t_ij <= -a1^2, expanded exactly.
  - Rows nk+1..2nk: x_ij - y_i <= d.
  - Row 2nk+1: sum y_i <= 0.8 n.
  - Every coefficient is exact in binary64.
  - Names `constrained_star_k{k}_n{n}_s{s}`. Every case file of campaigns 1-4
    and every MINLPLib name was checked, and none matches.
- **5S exact optimum.**
  - Breakpoints: 1 - d and the zero of the affine factor g in each regime of
    U(y) = min(1, y + d). All are rational, since
    Phi(U, y) - Phi(0, y) = U g(y).
  - On each piece the endpoint choices are fixed and the sum is one quadratic.
    Candidates are the piece ends and interior stationary points, and F is
    evaluated exactly at each.
  - The value equals the M3 sweep on every star of every instance (also checked
    against a dense numerical grid during development).
  - The sum of the smallest minimizers is about 0.4 n against 0.8 n, so the
    coupling row does not bind.
- **5S witness.**
  - y* (the smallest minimizer) is rounded down. A leaf at U(y*) is recomputed
    as min(1, y_b + d) and rounded down (the protocol does not say how to round
    x), and t = Phi(x, y) is rounded up.
  - It is feasible exactly in rationals. Its objective is at most 1e-9 (in fact
    at most about 2e-16) above the optimum.
  - It passes the archived primal check. That check works in binary64 and
    reports a scaled violation of up to about 3e-17.
- **5C-a / 5C-b cases.** These are the 20 C3 and 20 C4 cases of campaign 4.
  Each is regenerated (`mechanism.case`; `../v4/mechanism_c4.case` with
  `../v4/c4-references.json`, generator hash checked), compared byte for byte
  with `../v4/runs/partC3/cases` and `../v4/runs/partC4/cases`, and written
  identically. Each C4 witness gets the primal check, and the certificate and
  bound (ii) <= optimum are checked.
- **Jobs.** Seed 0; full before root; larger instances first; modes of a job
  rotated by (model index + seed) mod (number of modes); at most six workers.
  - 5S: larger = more variables, n(2k+1). Full: 7 modes at 300 s / 360 s; root:
    the 6 SCIP modes, node limit 1, 120 s / 180 s. 60 jobs, 390 runs.
  - 5C-a: n descending, C3 before C4. baseline-novarlocks, full 300 s / 360 s
    and root 120 s / 180 s. 80 jobs, 80 runs.
  - 5C-b: root, node limit 1, 300 s / 360 s, four modes. 20 jobs, 80 runs.
- **Summaries.**
  - 5S root gap closed: (root(m) - root(baseline)) / (opt - root(baseline)).
  - Root bound: `root_dual`, or the final dual bound of a run that ended at the
    root without one (agg-star often prunes the root).
  - 5C-b: distance (ii) - root and gap closed relative to (ii), compared with
    the 16n-cap runs of 4C4 (`c4:frozen-wide`, `c4:rowdir-wide`; their root
    runs had 120 s).

## Commands

```bash
V5=/workspace/minlp-notes/paper-certified-support-cuts/experiments/v5
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cd $V5
```

(i) Snapshot: it exists (manifest `b9c4ba84...`, rebuilt after Amendment 1),
and the final tests and `smoke/partC5b-amended` used it. Do not recreate it.

(ii) Build the job lists (each copies the verified snapshot):

```bash
$PY make_jobs.py partS5  --output runs/partS5
$PY make_jobs.py partC5a --output runs/partC5a
$PY make_jobs.py partC5b --output runs/partC5b
```

(iii) Launch one chain with at most six workers. Do not run campaign-4 drivers
at the same time, because they use a separate slot directory.

```bash
nohup bash -c "$PY driver.py runs/partS5 --workers 6 && \
               $PY driver.py runs/partC5b --workers 6 && \
               $PY driver.py runs/partC5a --workers 6" > runs/launch-v5.log 2>&1 &
# Resume after a stop or crash: rerun the same command (finished runs are skipped).
# Stop: kill -TERM <driver pid> (never SIGKILL). Progress: tail -f runs/launch-v5.log; wc -l runs/*/records.jsonl
```

The three drivers may also be started at the same time on separate `nohup`
lines. The six slots in `v5/.slots` keep the total at six workers.

(iv) Replay (exit 0 only if passed; writes `runs/<part>/replay.json`). Run the
replays one at a time, because the archived replay holds a whole ledger in
memory.

```bash
for p in partS5 partC5a partC5b; do $PY replay_v5.py runs/$p > runs/replay-$p.log; done
```

(v) Summaries (after the replay):

```bash
$PY summarize_v5.py runs/partS5 runs/partC5a=../v4/runs/partC3,../v4/runs/partC4 \
    runs/partC5b=../v4/runs/partC4 --dest results
```

Targeted tests: `$PY -m unittest test_v5` (14 tests, about 60 s).

## Wall-time and storage estimate (6 workers)

The estimates use the smoke runs, campaign-4 Parts C2/C3/C4 and four probe runs
on the largest instances. The probes were run in a temporary directory and are
not part of any part:

- `constrained_star_k16_n20_s0`:
  - baseline full: time limit at 300 s, bound 7.06;
  - gurobi full: time limit at 300 s, bound 10.478;
  - rowdir-star4 root: 64.5 s, bound 6.587, 303 cuts;
  - agg-star root: 64.6 s, bound 10.578023652744267, equal to the known
    optimum in binary64; 408 cuts, of which 237 are star cuts; 20 star blocks;
    star-oracle calls (dimension 17) median 10.5 ms, maximum 98 ms; polytope
    calls (dimension 4) median 66 ms.
- `interleaved_path_coupled_n80_s5`, rowdir-cap64 root: 37 s, 1851 cuts after
  10 callbacks, bound 1.781888 (bound (ii) 1.783474; 4C4 rowdir-wide 1.756996).

The upper bounds assume that every run reaches its hard limit.

| Launch | Expected | Upper bound |
|---|---|---|
| 5S | 2-2.5 h. Root: the three cut modes use the 60 s separation allowance, about 65 s per run (about 35 s on k4 n10). Full: on the 15 larger instances (k16 n20, k8 n20, k16 n10) most modes probably reach 300 s, about 2,000 s per job. The longest job is about 2,100 s. | (210 x 360 + 180 x 180) s / 6 = 5.0 h |
| 5C-b | 15-25 min. With 40 callbacks the separation runs longer than in the 10-callback probe (37 s at n80): perhaps 60 s (cap32) to 150 s (cap64, the separation allowance) per n80 run. | 80 x 360 s / 6 = 1.3 h |
| 5C-a | 20-25 min. In campaign 4 the baselines of n >= 40 (and some n = 20) reached 300 s; root runs take 1-3 s. | (40 x 360 + 40 x 180) s / 6 = 1.0 h |
| Replay | About 1.5 h in total. In the smoke runs 5S took about 0.12 s per cut, because the replay re-enumerates each 4-variable polytope cut (star cuts are cheaper). With roughly 40,000-50,000 cuts that is 1-1.5 h. 5C-b took about 12 ms per cut; with roughly 70,000 cuts that is about 15 min. 5C-a has no cuts. | |

The expected total is 3-3.5 h of runs plus about 1.5 h of replay; the upper
bound for the runs is 7.3 h. The archived replay holds a whole ledger in
memory: roughly 2 GB of compact JSON for 5S and for 5C-b, so expect 10-20 GB of
RAM per replay. The host has 47 GB; campaign 4 replayed a 0.9 GB ledger.

Storage: records are large. One indented `runs/<id>.json` plus its compact
ledger line take about 45-70 MB for a cut-mode run on k16 n20 and about 130 MB
plus 40 MB for a 5C-b run with n = 80. Expected disk use is roughly 10-15 GB
for 5S, 10-25 GB for 5C-b (more cuts with 40 callbacks; up to 64n = 5120 cuts at n = 80) and under 0.1 GB for 5C-a (414 GB free). Campaign 4
Part C4 used 3.4 GB.

## Verification done (targeted; no project-wide tests, no CI)

`python -m unittest test_v5`: 14 tests passed (59 s on `snapshot-smoke/`;
69 s on the rebuilt `snapshot/`, after Amendment 1). They check:

- **Mode table.** Every campaign-4 mode equals `v4_worker.mode_config`; the
  campaign-5 limits are as specified; the SCIP parameter record is unchanged.
- **Config.** `aggregate_directions` accepts only a bool; `star_leaves` accepts
  only an int >= 0; `max_dimensions = 5` is still refused; every other default
  equals the campaign-4 value.
- **Patched file.** The snapshot `integration.py` equals the campaign-4 file
  with exactly the `PATCHES` applied.
- **Star discovery** on k4 n10:
  - 10 star blocks come first, with variables (y_i, x_i1..x_i4), the four Phi
    rows of star i as sides, and the four center-leaf rows as domain rows;
    every other block has at most four variables.
  - With `star_leaves = 2`, the first block is (y_1, x_11, x_12) with its 2
    sides and 2 rows.
  - With the defaults, or both additions explicitly off, discovery is identical
    and has no `star_blocks` key.
- **Block direction.** On k4 n10 and k16 n10, for the first and last star:
  - the block direction has lambda = 1 and the exact summed affine
    coefficients;
  - a star block gets exactly 1 + k directions;
  - its support, certified by `quadratic_star`, equals the generator's exact
    star optimum minus sum a1^2, and the exported rhs does not exceed it.
  - On a four-variable block the block direction comes first, then the first
    whole-row direction.
- **Star cut replay.** A recorded agg-star run on a test-only star instance
  (k4 n5):
  - discovery kept 5 star blocks; all cuts replay with the archived
    `check_run`;
  - a star cut of dimension 5 alone also passes;
  - all archived tampering mutations and the four star-certificate mutations
    are rejected.
- **Defaults reproduce campaign 4.** The campaign-4 and campaign-5 snapshots,
  each in its own process, give identical cut records, root and final bounds,
  and support-call counts:
  - interleaved_path_coupled_n10_s5, mode rowdir-wide, root;
  - ex8_1_7 (MINLPLib), mode all-diag-rowdir-noaggr, root;
  - each with the defaults and with both additions explicitly off.
  Both equal the archived campaign-4 records (root bound and cut normals).
- **Instances.** The 30 star instances are deterministic, exact and new, and
  their witnesses pass. The C3/C4 cases equal campaign 4 and their generators.
- **Jobs.** Counts (390/80/80), order, rotation, limits and the smoke
  selection.

### Smoke runs (`smoke/`, 10 s soft / 30 s hard; separation allowance 5 s)

The three parts were built with `make_jobs.py PART --smoke` against
`snapshot-smoke/` (manifest `e8f0152e...`, before Amendment 1) and run together
(6 slots, about 27 s wall). All 21 runs completed,
with no failures. The replay passed in every part, with no config, Gurobi or
cut-method mismatches. Every tampering mutation was rejected in every cut
mode, including the star-cut controls in agg-star. Summary:
`smoke/results.md`.

| Part | Case(s) | Runs | Statuses | Cuts replayed (polytope / star) | Tamper modes |
|---|---|---:|---|---:|---|
| 5S | constrained_star_k4_n10_s0 | 13 | optimal 7, nodelimit 5, gaplimit 1 (gurobi) | 221/221 (147 / 74) | rowdir-star4, agg-star4, agg-star (+ star controls) |
| 5C-a | interleaved_path_n10_s5, interleaved_path_coupled_n10_s5 | 4 | optimal 2, nodelimit 2 | 0 | - |
| 5C-b | interleaved_path_coupled_n10_s5 | 4 | nodelimit 4 | 924/924 (924 / 0) | all four cap modes |

5S root bounds. The optimum is 0.74261474609375. The root gap closed versus
the baseline is in parentheses.

| baseline | baseline-novarlocks | baseline-extra | rowdir-star4 | agg-star4 | agg-star |
|---:|---:|---:|---:|---:|---:|
| 0.713415 | 0.439344 (-9.39) | 0.696093 (-0.59) | 0.724081 (0.365), 28 cuts | 0.721159 (0.265), 31 cuts | 0.742614 (0.99998), 50 cuts |

- **agg-star.** The 50 cuts are 37 `quadratic_star` (10 star blocks,
  dimension 5) and 13 polytope cuts. The root node was pruned at the 1e-4 gap,
  so the bound shown is the final dual.
- **Certification times.** Star-oracle calls had a median of 3.4 ms and a
  maximum of 11 ms; polytope calls had a median of 60-68 ms.
- **Full runs.** All SCIP modes solved the instance in 0.4-6.4 s. Cuts:
  rowdir-star4 31, agg-star4 29, agg-star 52 (37 star). Gurobi stopped at the
  gap limit after 0.48 s.
- **5C-a.** Root bounds: C3 n10_s5 -0.001399 (optimum 0.019165); C4 n10_s5
  0.124351 (optimum = bound (ii) = 0.130127). Both full runs were solved.
- **5C-b.** Distance to bound (ii) at the root:
  - frozen-cap32/64: 1.4e-4 (238 cuts);
  - rowdir-cap32/64: 3.1e-5 (224 cuts);
  - 4C4 frozen-wide: 1.8e-3 (160 cuts); 4C4 rowdir-wide: 4.7e-4 (160 cuts).
  - cap32 and cap64 gave identical runs. All 10 callbacks ran with about 24
    cuts per callback, so neither cap was reached. The n = 80 probe (1851 cuts,
    below 32n = 2560) points the same way. This led to Amendment 1.

### Amended 5C-b smoke run (`smoke/partC5b-amended`, `snapshot/`, max_rounds 40)

Built with `make_jobs.py partC5b --smoke` against `snapshot/` (manifest
`b9c4ba84...`). Case: interleaved_path_coupled_n10_s5, root, 10 s soft / 30 s
hard. All 4 runs completed (nodelimit). The replay passed: 1022/1022 cuts, no
config or cut-method mismatches, and every tampering mutation rejected in all
four modes.

| Mode | Cuts / cap | Callbacks / max_rounds | Support calls | Root bound | Distance to (ii) |
|---|---:|---:|---:|---:|---:|
| frozen-cap32 | 270 / 320 | 16 / 40 | 336 | 0.1300701 | 5.7e-5 |
| frozen-cap64 | 264 / 640 | 13 / 40 | 328 | 0.1300777 | 4.9e-5 |
| rowdir-cap32 | 243 / 320 | 13 / 40 | 328 | 0.1301024 | 2.5e-5 |
| rowdir-cap64 | 245 / 640 | 18 / 40 | 333 | 0.1301035 | 2.3e-5 |

More than 10 callbacks now ran, so max_rounds 40 is in effect. At smoke limits,
however, the 5 s separation allowance (half of the 10 s budget) ended every run
(`budget_exhausted`) before either cap was reached. The small cap32/cap64
differences come from timing, not from the caps, so the smoke run cannot show
whether the caps bind. Whether they bind at the protocol limits (150 s
allowance) will be visible in the main 5C-b runs. A check at the protocol
limits was not done: my first attempt wrote to a wrong path and produced no
records (it ran before the main runs started). A rerun would have exceeded six
solver processes, because the main 5C-b driver was already using all six
slots.
