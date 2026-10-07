# Independent check of the Part C4 digest (2026-10-03)

Scope: every number in `evidence/campaign4-c4-digest.md` (Part C4: path family with a binding
coupling row), plus an independent exact recomputation of bound (ii) and of the reference facts.

## Result

**753 checks, 751 match.** 732 of the checks compare a digest number or claim with my own
recomputation. The other 21 are independent checks of bound (ii), the witnesses and the cut rows.
No digest number is wrong.

Two statements are imprecise. Both are minor:

1. **(e) and (f): the wrong REF field is named as the bound-(ii) multiplier.** The digest says
   "The multiplier of the coupling row in bound (ii) is positive: `multiplier_exact` ranges from
   29/288 ... to 99/256". REF `multiplier_exact` is not the bound-(ii) multiplier. It is the
   coupling multiplier of the exact QP for the optimal assignment (`mechanism_c4.py`, lines 648 and
   670, `exact_assignment_optimum`).
   - It satisfies the bound-(ii) optimality condition S_min(mu) <= c <= S_max(mu) only on the 13
     instances where bound (ii) equals the optimum.
   - It fails on the 7 instances where bound (ii) is below the optimum: n10_s7, n10_s9, n20_s6,
     n20_s7, n20_s8, n80_s7 and n80_s9. For example, n10_s9 has `multiplier_exact` = 31/128, but
     the bound-(ii) multiplier is 1/4. For n20_s8 the values are 85/304 and 19/64.
   - The printed range is still right for the bound-(ii) multiplier. My exact multiplier mu*, and
     also REF `bound_ii.mu`, range from 29/288 (n10_s8) to 99/256 (n10_s6). Both extremes are on
     instances where bound (ii) equals the optimum, so the two fields agree there. The slope range
     [-0.387, -0.101] in (f) therefore stands.
   - Fix: cite `bound_ii.mu` (or the exact mu*) instead of `multiplier_exact`.
2. **(c): the explanation of the rtol 1e-6 result covers only 9 of the 10 instances.** The count
   is right: rowdir-wide is "worse" than baseline at rtol 1e-6 on all 10 commonly solved instances.
   The digest explains this by saying that 11 of its runs stop at the 1e-4 gap limit. But among
   those 10 instances, only 9 rowdir-wide runs are gaplimit stops. The tenth, n20_s7, has status
   optimal (3 nodes). Its incumbent and final bound are both 1.05e-5 below the exact optimum,
   whereas baseline's are 7.90e-6 below. So it is "worse" by 2.64e-6 because its incumbent is
   lower. The other 2 of the 11 gaplimit runs (n40_s5, n40_s8) are not among the 10.

## Commands run (targeted, local; no project-wide tests, no CI)

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
cd /workspace/minlp-notes/paper-certified-support-cuts
CACHE=$(mktemp); OUT=$(mktemp)
$PY verification/R8_c4.py --values --cache $CACHE > $OUT   # about 27 s; prints every check and value
```

I also ran some short read-only inspections with the same Python:
- the record, case, REF and replay schemas;
- `grep` of `mechanism_c4.py` for `multiplier_exact`;
- the snapshot's `integration.py` (`RowSeparator._expired`);
- `results-c4v/results.md` and `results-c4/c4-results.md`;
- `evidence/campaign4-replay.md` and `evidence/campaign4-digest.md`;
- the `replay.json` mtime and `sha256sum replay_v4.py`.

I started no solver. I changed no file under `experiments/`, and I did not edit the manuscript.
The temporary cache and output files came from `mktemp` and were deleted. I wrote two files:
`verification/R8_c4.py` and this file.

## Method

`verification/R8_c4.py` uses only the standard library and imports no producer code. It reads:
- `experiments/v4/runs/partC4/records.jsonl` (streamed line by line);
- `jobs.json`, `cases/*.json` and `replay.json` in the same directory;
- `experiments/v4/c4-references.json`.

For the cross-references in the digest it also streams the C2 and C3 records (Gurobi, baseline and
rowdir-wide) and reads the C3 cases. It hard-codes every digest number as printed. The tolerance is
half a unit in the last printed digit. Counts, lists and instance names must match exactly. I
implemented the definitions from the protocol and the runner README:
- solved: status optimal or gaplimit; returncode 0; no `worker_status`; `primal_check.checked`
  and `primal_check.passed`; finite primal;
- time: `total_seconds + preparation_seconds`;
- SGM: shift 1 s, over the runs solved (full) or completed with a root bound (root) by every
  compared mode;
- root bound: `root_dual`, or the final dual for a SCIP run with node limit 1 or one node;
- gap closed: relative to the case fields `known_optimum` and `reference_bound_ii`;
- bound comparison: rtol * max(1, |a|, |b|); 'flagged' on a failed primal check or a
  reference conflict.

Cut directions are classified as follows. The support direction is taken from
`support_witness.model.coefficients` (exact binary64 hex values). The affine part comes from
`signed_sides[0].affine_terms`. A direction is "row" if a = lambda * aff exactly on (x_i, y_i, z_i),
"remainder" if a = 0, and "LP" otherwise. For every cut, the script also checks:
- the exact row coefficients of x_i, y_i and z_i equal a - lambda * aff, and the coefficient of
  t_i equals lambda > 0;
- whether the y_i coefficient is zero agrees across four places: a_y - lambda aff_y, the exact row,
  the exported row and the SCIP-stored `actual_row`;
- no coefficient lies outside the block;
- the root and full runs carry the same list of (block, exact row, `compensated_rhs`,
  `eliminated_rhs`), compared by SHA-256.

## Independent check of bound (ii) and the references

I did this for all 20 instances, not only three:
- **phi_i from the case rows.** Each copy row is t_i >= D_i(x, y, z). The script checks that the
  row has no x z term and that the x^2 and z^2 coefficients are <= 0. So for fixed y the minimum is
  at a vertex (x, z) in {0, 1}^2. This gives phi_i = min of four parabolas, each with y^2
  coefficient exactly 2. On all 20 instances the four parabolas equal
  {(y - s)^2 + (y - t)^2 : s in A_i, t in C_i} from the case `triples`.
- **Exact Lagrangian bisection.** h(mu) = sum_i min_{y in [0,1]} (phi_i(y) + mu y) - mu c is
  computed in rationals over 110 steps on [0, 4].
  - Lower bound: max h(lo), h(hi). Upper bound: a primal point, the convex combination of the
    minimizers at lo and hi with sum y = c.
  - The exact optimal multiplier mu* is then found from the structure inside the final bracket and
    checked exactly against S_min(mu*) <= c <= S_max(mu*). This makes h(mu*) the exact bound (ii).
  - Results:
    - mu* was found on 20/20 instances.
    - |mu* - REF `bound_ii.mu`| <= 1e-15 on 20/20.
    - h(mu*) lies in the script's own [L, U] on 20/20.
    - |h(mu*) - REF `bound_ii.value`| <= 7.4e-17 on 20/20, far inside the requested 1e-9.
- **Convex hull of phi_i on a grid plus exact pieces** (n10_s9, n20_s8, n80_s7; I chose all three
  from the instances where bound (ii) is below the optimum).
  - Grid j/2^16, plus the parabola vertices and the bitangent points.
  - The bound is then minimized by a greedy slope fill under the coupling row.
  - The hull bound minus the exact bound is 0.0, 2.2e-16 and 2.2e-16. The a-priori error bound
    n h^2 / 2 is 1.2e-9, 2.3e-9 and 9.3e-9.
- **Optimum >= bound (ii)** on 20/20, compared in exact rationals. The difference is exactly 0 on
  the 13 instances the digest lists. It is not merely "zero up to the bisection error": the exact
  bound equals REF `optimum_exact`. On the other 7 it is exactly:
  - 1/65536 = 1.53e-5 (n10_s7);
  - 1/16384 = 6.10e-5 (n10_s9);
  - 1/36864 = 2.71e-5 (n20_s6);
  - 5/32768 = 1.53e-4 (n20_s7);
  - 403/622592 = 6.47e-4 (n20_s8);
  - 625/2326528 = 2.69e-4 (n80_s7);
  - 9/149504 = 6.02e-5 (n80_s9).

  All seven match the digest.
- **Fractional copies.** One copy must be fractional exactly where S_min(mu*) < c < S_max(mu*).
  This happens on the same 7 instances, matching REF `fractional_copies` (1 there, 0 elsewhere).
  On n20_s7 and n80_s9, 2 and 3 copies have tied minimizers, but one fractional copy is enough.
- **Coupling row and c.**
  - The last case row is `sum_i y_i <= c`, with c equal to REF `coupling.c`, on 20/20.
  - y_i* is recomputed as the smallest minimizer of phi_i. sum y* and c = floor(64 * sum y* / 2) / 64
    equal REF on 20/20.
- **Witness and optimum.**
  - The binary64 witness (`witness_exact`) is feasible in exact arithmetic on 20/20: x and z are in
    {0, 1}, y is in [0, 1] and t_i >= D_i. Its objective equals `witness_objective_exact`.
  - The coupling row binds at the witness: 0 <= c - sum y_i <= 1.75e-15, i.e. below n * 2^-52.
  - `y_exact` sums to exactly c and attains `optimum_exact` exactly on 20/20.
  - Caveat: I did not repeat the exact branch and bound that certifies that no other assignment does
    better on the 7 instances with a positive gap. On those, my check gives
    bound (ii) < `optimum_exact`, and `optimum_exact` is attained.
- **Row-direction cuts.** All 1,500 row-direction cuts (750 root + 750 full) are exactly
  t_i >= min phi_i: the t coefficient is 1, the x, y and z coefficients are 0, and
  `compensated_rhs` / t coefficient = min phi_i in exact arithmetic. sum_i min phi_i equals the C3
  `known_optimum` on 20/20.

## What was checked (all match unless noted)

Sources are the raw records unless stated. Values in brackets are recomputed.

- **Integrity.**
  - 180/180 scheduled runs are recorded (`jobs.json` vs `records.jsonl`). None is missing,
    unscheduled or duplicated.
  - Return code 0 and no `worker_status` everywhere.
  - All 180 incumbents passed the primal check, with max scaled violation [9.975e-7].
  - 0 flagged runs; 180/180 reference-witness checks passed; 0 classifier errors.
  - The case fields equal REF on 20/20.
  - Workers: `driver_workers` 6, at most 6 active.
- **(a) Replay** (`replay.json`). All fields of the table match, including:
  - 48,000/48,000 cuts, 12,000 per mode and phase;
  - 0 config failures of 160 and 0 Gurobi failures of 20;
  - 20 omitted Gurobi runs (timelimit 14, optimal 6);
  - 106 source files verified;
  - 1658.4 / 1684.3 s;
  - both SHA prefixes; `wrapper_source_sha256` equals `sha256sum replay_v4.py` (05e01381...).

  Tampering 14/14 per mode and part-level. The run log has one line. The `replay.json` mtime is
  22:18:36Z, and mtime minus `wrapper_seconds` gives a start of 21:50:32Z. Root and full cut lists
  are identical on 20/20 per mode. The totals 104,771, 112,269 and 143,267 follow from the numbers
  in `campaign4-replay.md`.
- **(b) Root runs.** All of the following match:
  - status counts;
  - n10_s6 gaplimit at 1 node in both cut modes;
  - all four time triples;
  - the n10_s6 detail;
  - all 60 cells of the root-bound and optimum table;
  - better than baseline on 20/20 at both rtols;
  - all 90 gap-closed values, with argmin and argmax names;
  - the gap tables differ on exactly 7 instances;
  - all 32 cells of root bound minus bound (ii), with names;
  - no root bound above bound (ii) or the optimum;
  - rowdir-wide at n=80 between [-0.02876, -0.01582];
  - `root_dual` differs between full and root runs on 1, 2, 4 and 12 instances; where both are
    finite, the full run is higher;
  - the n40_s8 example;
  - every differing full run has FIXED variables, and no root run does;
  - exactly the six listed full runs have a root-node bound above bound (ii). All six are root_dual
    values, gaplimit at 1 node, below the optimum and with FIXED variables. No other full run has a
    root bound above bound (ii);
  - no SCIP final dual above the exact optimum, in root or full runs.
- **(c) Full runs.** All of the following match:
  - solved counts, statuses and solved lists;
  - time triples and median nodes;
  - 1-node solves, all gaplimit;
  - the six-instance table (SGMs, SCIP, excl. callback, callback, nodes);
  - ratios with pair and faster counts;
  - the 10-instance SGMs and nodes;
  - the 20-run SGMs 12.96 and 12.20 s;
  - the n80 time ranges;
  - the final-dual comparisons at 1e-4 (better 10 on all n40 and n80; Gurobi 10, 6 and 4, worse
    on n20_s5-s8);
  - rowdir-wide worse at 1e-6 on 10/10 (see issue 2);
  - final dual minus optimum (all 12 values);
  - the fw n80_s5 example;
  - the SCIP and Gurobi incumbent minima with their locations;
  - Gurobi parameters (Threads 1, NonConvex 2, MIPGap 1e-4, Seed 0, TimeLimit equal to
    `remaining_solve_budget`, version 13.0.3);
  - every cell of the Gurobi table, with time = `total_seconds + preparation_seconds`;
  - the C2/C3 Gurobi excess [1.157e-6] (from the C2/C3 records).
- **(d) Funnel, caps, time.** All of the following match:
  - both funnel rows, in both phases, identical across phases;
  - causes, repeat skips 6 and 12, binding shares 2.0% and 1.8%;
  - caps: cut cap 20/20 in every mode and phase; support, round and 60 s caps 0;
  - support ratios 0.4475-0.505 and 0.475-0.525; callbacks 6-8 and 7-8;
  - callback-second ranges;
  - config (16n, 40n, 4n, 10, n, 60, 0.5, `row_directions`);
  - `budget_exhausted` 20/20 per mode and phase; the `_expired` code in the snapshot
    `integration.py` (lines 391-396) also sets this flag at the cut cap;
  - all 42 time-decomposition cells;
  - all 40 sums;
  - host load 8.13-8.19 and 7.86-9.10;
  - run window 20:59:57Z to 21:32:14Z.
- **(e) References.** All match except the field attribution in issue 1:
  - min, median and max of `optimum_minus_bound_ii`, which equals float(`optimum_exact` -
    `lower_exact`) on 20/20;
  - the list of 13 and the 7 values;
  - the c values and ratios [0.4957, 0.5];
  - binds 20/20; `y_exact` sums 20/20;
  - certificates, witness checks and switches 20/20.
- **(f) Cut directions.** All class counts, y-nonzero counts, nonzero patterns, slope medians,
  q1/q3, min/max and sign counts match, in both phases. q1/q3 use the "exclusive" quartile
  method; for the remainder rows the "inclusive" method gives -1.781 and -1.352 instead. Also:
  - 46,376 nonzero and 1,624 zero y coefficients, consistent in all four places;
  - no cut-level inconsistency;
  - LP cuts on every block of every run;
  - exactly one row cut per block in rowdir-wide;
  - n80 LP counts 1278-1279 and 1198-1199;
  - the shares 99.7%, 93.5%, 79%, 83% and 99.7%;
  - the gap closed by the row-cut bound, 0.0243 [-5.70, 0.693]; below baseline on 10/20;
  - every fw and rw root bound above it;
  - C3 rowdir-wide: root gap closed min [0.9999994], 20/20 solved, max [33.17] s (C3 records).
- **(g)** All match:
  - max root time 34.48 s; max outer wall 302.3 s;
  - the four multi-node full runs without `root_dual`;
  - 31 time-limit runs (baseline 10, baseline-extra 7, gurobi 14), all above 300.01 s, by at most
    0.198 s;
  - intersection cuts: 20 runs, 27,288 enforcement calls and 12,692 cuts at the root; 20 runs,
    83,316,305 calls and 12,940 cuts in full runs;
  - eccuts, interminor and minor 0 calls;
  - baseline n20_s5-s8 times 3.95-14.1 s;
  - VR has the pair-hull line, and its per-n gap medians equal C's.

## Missing or understated facts

1. **(b): FIXED variables also occur in full runs whose root bound did not change.** 37 full SCIP
   runs end with FIXED original variables. 19 of them are the runs whose `root_dual` differs from
   the root run's. The other 18 have an unchanged `root_dual`: baseline n10_s7; frozen-wide n10_s8,
   n20_s6-s9 and n40_s5-s9; rowdir-wide n40_s7, n40_s9 and n80_s5-s9. FIXED therefore does not
   single out the runs with a changed root bound. This weakens the inferred mechanism, which the
   digest already calls unverified.
2. **(e): the exact differences are known.** Bound (ii) equals the optimum exactly on the 13
   instances, and the 7 positive differences are the simple rationals listed above. The digest
   describes the 13 as "zero up to the bisection error".
3. **(f): the rhs of the row-direction cuts is verified.** All 1,500 row-direction cuts are exactly
   t_i >= min phi_i. The digest states this form but does not say it was checked.
4. **(c): rowdir-wide n20_s7.** It is status optimal with primal = dual 1.05e-5 below the exact
   optimum. It is the one non-gaplimit run behind the rtol 1e-6 "worse" count (issue 2).

## Not verifiable from the records

- The statement in the digest's Commands section that "the only change in both summaries was the
  replay line" (summary history).
- The replay start time to the second, which is consistent with the `replay.json` mtime.
