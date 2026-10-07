# Review r2 of stream `multiround` (revised note.md of 2026-10-02)

Reviewer: independent research agent (adversarial review, confirmation
round 2), 2026-10-02. I did not write any of this material. "Reviewed" here
means checked by another research agent, not journal peer review.

## Verdict

**Minor fixes.** All three major issues of round 1 are fixed correctly, and
so are all seven minor issues and the five optional items. Every number in
the revised sections that I checked matches the raw records. My own
independent script reproduces all of these numbers to the printed digits:

- the bug analysis (M1);
- the switching table and the `o1s` rows for the other sizes and pooled (M2);
- `maj2`, `rnd0.33` and `maj2 − rnd0.33` (M3, Section 3.6);
- the Holm values for the three new rules.

The new runs reproduce bitwise. The new proofs are correct: Remark 3a and the
revised proof of Proposition 5. I checked Proposition 6 again in exact
arithmetic, for a new value of `ε`.

Two small inaccuracies remain in the new text. Both are wording problems,
not wrong data:

- **n1.** The note claims that on 10×20 the `oKs` losses do not shrink
  between rounds 10 and 20. The table shows otherwise for `o3s` and `o5s`.
- **n2.** The note says the "shorter sets" factor is shared by *all*
  losing rules. It was measured for only three of them.

## Status of the round-1 issues

| Issue | Status | Evidence |
|---|---|---|
| M1 (the bug and the multi-round gap) | **Fixed.** The 0.017 attribution is withdrawn in the summary, Sections 1.3, 2 and 6, and in the corrections list. | `orbit − orbit_core` on 220 instances: +0.0114 [+0.0040, +0.0189] after round 1, −0.0008 [−0.0033, +0.0017] after round 10, −0.0016 after round 20. On the 10 original instances the per-instance differences are exactly as stated (one instance gives +0.212). The figures match my recomputation. |
| M2 (an orbit round at the root is not harmless) | **Fixed.** `o1s` was run on 8×12 and 10×20. The table now has round-3 columns. The root-only recommendation is withdrawn. "Damage spread over rounds 0–4" is stated, and so is "failing to detect a cost does not show it is zero". | All 48 cells of the switching table and the `o1s` figures for the other sizes and pooled match my recomputation. Examples: pooled −0.0062 [−0.0108, −0.0015] after round 10; `o1s − orbit` +0.0056 [+0.0011, +0.0101]; `s1o` 57% and 68%; `s3o` pooled −0.0062 [−0.0116, −0.0008]; `s5o` pooled −0.0011 [−0.0034, +0.0013]. One sentence remains inaccurate; see n1. |
| M3 (the degeneracy mechanism does not discriminate) | **Fixed.** The mechanism is withdrawn as the main cause. The tie and `z_C/z_K` recounts for `pertE0.1` and `geo`, the degeneracy correlations, the same-corner tilt comparison and the step signature for all rules are now reported. A shared factor was considered and tested (new Section 3.6) and is labeled heuristic. | `logs/summary_mech_6x8.log` and `logs/summary_mech_10x20.log` regenerate identically. Table 3.6 matches the log (shares, mean log ratios, within-rule Spearman between −0.14 and +0.15, all p ≥ 0.3). The intervention numbers match my recomputation. One overgeneralization remains; see n2. |
| m1 (Holm over 14 rules) | Fixed. | |
| m2 ("never worse from the same state") | Fixed. | The 10×20 figures are correct: 0.677 vs 0.689; 0.241 vs 0.250; 0.505 vs 0.503. The orbit round is ahead by 0.036, 0.034, 0.030 and 0.001 on SCIP's states. All are from `logs/summary_state_10x20.log`. |
| m3 (the ties and Proposition 7) | Fixed. | I confirmed in `fastorbit.orbit_feasible` that the bisection returns the minimum-Frobenius-norm `F`. "Another bound-optimal set might avoid the ties" is correctly marked as untested. |
| m4 (the swappot range) | Fixed. | The per-instance means in rounds 0–5 are −0.028, −0.025, −0.034, −0.028, −0.061 and −0.014. |
| m5 (`eff2` shows no gain) | Fixed. | The summary, Section 4 and the recommendation all say "no demonstrated gain". The 70% figure is withdrawn. The note flags that `eff` was selected post hoc. |
| m6 (Setting L vs OQ3; distinct indices) | Fixed. | See Remark 3a below. The statement about `S = {w ≤ xy}` alone is correct: `εx + y + w ≥ 2√(εxy) + w ≥ 2√(εw) + w ≥ 1 + 2√ε`. |
| m7 (idealized θ in the summary) | Fixed. | |
| o1–o5 | Fixed. | `check_clip.py` reruns identically (3728 of 52347 states above `z_bil`; at most 6.9e-7 relative). The new `logs/rev1` records also stay below 6.9e-7 (335 of 5335 states). `recio.py` stops with an error when nothing matches. `check_consistency.py` now reports 810 pairs. The docstring, the `c̄` notation and the interval `(z_LP, z*)` are fixed. |

## Remaining issues

### Minor

**n1. "No recovery on 10×20" is not true for every `oKs` rule.**

Location: Section 3.5, reading, bullet "Partial recovery on 6×8, none on
10×20". The author summary makes the same claim.

The note says: "On 10×20 the loss of the `oKs` rules does not shrink between
rounds 10 and 20." By the note's own table and `logs/summary_rev1.log`, this
holds only for `o1s` and `o2s`:

| Rule | 10×20, round 10 → 20 | 6×8, round 10 → 20 |
|---|---|---|
| `o1s` | −0.0128 → −0.0152 | |
| `o2s` | −0.0170 → −0.0184 | |
| `o3s` | −0.0191 → −0.0165 | |
| `o5s` | −0.0255 → −0.0206 | −0.0105 → −0.0063 |

So `o3s` and `o5s` do shrink on 10×20. The recovery of `o5s` on 10×20 is
0.005, about the same size as the 0.004 on 6×8 that the note cites as
partial recovery. The bullet also compares different spans: rounds 3→20 for
`o1s` and `o2s`, but rounds 10→20 for `o5s`.

Suggested wording: "On 10×20 the losses of `o1s` and `o2s` grow slightly
between rounds 10 and 20, and those of `o3s` and `o5s` shrink by 0.003–0.005.
SCIP rounds recover less of the damage there than on 6×8." Change the bullet
title accordingly.

**n2. "Shared by all losing rules" goes beyond what was measured.**

Locations:

- Summary item 2: "A factor shared by all losing rules: their sets are
  shorter …".
- Section 3.6: "Every rule that loses picks sets that are shorter than
  SCIP's on most rays".
- Section 3.7, item 4: "All losing rules share sets …".

The step-shortness measurement exists only for `orbit`, `pertE0.1` and `geo`
(and for the orbit cut of `both`). The diagnostic records (`logs/diag`)
contain no other losing rule. The following rules were never measured,
although Section 3.6 lists several of them as losing:

- `pert0.1`, `pertE1`, `lex0.1`, `orbit_core`, `orbitB`, `hyb0.9`;
- `alt` and `alt2` (`alt2` loses −0.014 on 10×20);
- the `oKs` and `sKo` schedules.

On the non-losing side, the measurement covers only `eff`, `sumstep` and
`oracle_seq`. It does not cover `hyb0.5`, `depth`, `eff2`, `oracle` or
`bothpert`.

For `orbit_core`, `orbitB` and the switching rules the property is plausible
by construction. For the other rules it is untested. Because this factor is
the note's best candidate explanation, the wording should match the
evidence. For example: "the three losing rules for which it was measured
(`orbit`, `pertE0.1`, `geo`) pick sets shorter than SCIP's on 61–71% of the
rays; the three non-losing selection rules measured pick sets shorter on
8–25%."

### Optional

- **o1.** Section 3.2, swappot paragraph: "the mean number of reduced costs
  `≤ 10^{-3}` is higher after orbit rounds in every bucket". On the orbit
  trajectory in rounds 3–5 the two values are equal (0.27 vs 0.27,
  `logs/summary_swappot_6x8.log`). Write "higher or equal".
- **o2.** `code/analyze_mech.py` builds the header line "pooled orbit,
  pertE0.1, geo (rank correlation within rule, then averaged by Fisher z)"
  but never prints it. So the last three lines of `logs/summary_mech_*.log`
  ("shorter mean within-rule Spearman …") have no label. On 10×20 the `tie2`
  line prints `+nan`, because `geo` has no ties.
- **o3.** Section 3.5: "on 4×4 about three quarters (−0.006 of −0.008)". The
  log ratio is 0.82. Harmless, but "about four fifths" matches the log.

## Checks of the new and changed material

### Proofs

- **Remark 3a (new).** I checked it line by line.
  - Case (a): a term maximizing `dist(x^r, S_e)` has distance at least
    `dist(x^{r_k}, S_e) ≥ ε`, so the depth hypothesis applies to the cut
    actually added. The chain
    `x^{r_m} ∈ P_{r_m} ⊆ P_{r_k+1} ⊆ K_{r_k} ∩ H_k` holds for the one-cut
    loop as well.
  - Case (b): `q_{e_{r_k}} ≥ q_e ≥ dist(x^{r_k}, S_e) ≥ ε` by Lemma 4(a),
    which needs distinct indices; Setting L now assumes them. Lemma 1 then
    gives depth `≥ γ_0 κ ε`.
  - The appeal to Lemma 4 for SCIP's rule, and for idealized `geo` and
    `pertED`, is valid under `P ⊆ [−B, B]^n`.
  - The note correctly says that an arbitrary term order is not covered.

  Correct.
- **Proposition 5 (revised proof).**
  - For finite `t_i ≤ α_i`, the points `(0, t_1, 1)` and `(t_2, 0, 1)` lie in
    `C`, because `C` is closed and convex.
  - The points of the segment from the interior point `s̄` to the midpoint
    lie in `int C`.
  - If `t_1 t_2 > 4`, a point near the midpoint lies in `S'`.
  - So `t_1 t_2 ≤ 4`, which forces both steps to be finite (since
    `α_2 > 0`) and gives `α_1 α_2 ≤ 4`.
  - The θ-bound-optimal consequence `α_1 ≤ 2√ε/θ` follows.

  Correct. The infinite-step case is now covered.
- **Setting L.** Distinct indices are now stated. The remark that Theorem 2
  and Corollary 3 do not need distinctness is correct, because they use only
  that `S_e` is closed. I rechecked the step "at least one `α_j` finite":
  if all steps were infinite, then `K_r ⊆ int C`, which contradicts
  `∅ ≠ F ⊆ K_r ∩ S'_e`.
- **Unchanged results.** Theorem 2, Lemma 1, Lemma 4, Corollary 3 and
  Propositions 6 and 7 were checked in round 1. I reread them and found
  nothing new.

### Computations

- **Independent statistics** (`reviews/r2-scripts/indep_rev1.py`). The
  script reads all records in `logs/main`, `logs/new` and `logs/rev1`
  (smoke file excluded). It asserts status `ok` and that duplicate
  trajectories are identical, and computes paired t-intervals. All of the
  following match the note and `logs/summary_rev1.log` to the printed
  digits:
  - the M1 statistics;
  - every `o1s`, `oKs` and `sKo` cell;
  - `maj2` and `rnd0.33` by size and pooled;
  - `maj2 − rnd0.33` by size and pooled;
  - `o1s − orbit`.

  The Holm values over the three new rules (0.029, 0.19, 0.99) follow from
  the raw p-values.
- **Exact check of Proposition 6 for a new case**
  (`reviews/r2-scripts/oq3_r2.py`). This is new code that uses only Python
  `Fraction`. The case is `ε = 1/16`, `ξ_r = 7(1 − 2^{−r})`, box
  `X = 9, Y = 1, W = 2`. For rounds 0–29 the script checks:
  - the three tight rows and strictly positive exact duals, so the vertex is
    the unique optimum;
  - primal feasibility of all rows;
  - exact boundary steps of `C_a` along the basis rays (rational roots);
  - that the cut equals `x/ξ' + ξ'y/4 ≥ 1`;
  - violation exactly 1.

  Result: True. The LP value tends to 1.4375, while `z* = 1.5`.
- **Bitwise rerun of the new rules.** I ran `mrloop.py` with `maj2` and
  `rnd0.33` on 6×8 instances 0–2, and with `first_orbit`, `maj2` and
  `rnd0.33` on 10×20 instances 40–41. All 12 trajectories are identical to
  the stored `logs/rev1` records (maximum difference 0).
- **Reruns of the analysis scripts, diffed against the stored logs.** All
  outputs are identical:
  - `analyze_rev1.py`;
  - `analyze_mech.py` (6×8 and 10×20);
  - `analyze_pooled.py`;
  - `analyze_key.py 10x20`;
  - `analyze_percase.py` (6×8).

  `check_clip.py` and `check_consistency.py` also give the same output as
  the stored logs: 3728 of 52347 states; 810 pairs, 0 differing.
- **Run bookkeeping.** `logs/rev1/done.txt` and `done_b.txt` list all 13 and
  6 jobs with exit code 0. The record counts match the chunking in
  `run_rev1.sh` and `run_rev1b.sh`: 20 records per 10-instance chunk with
  two rules, and so on. Every record has status `ok`. No log contains a
  traceback.
- **Code reading.**
  - `maj2` in `mrloop.py` does what the note says. On the rays where either
    step is finite, it picks the orbit set if `a_o ≤ a_s` (orbit step ≥ SCIP
    step) holds on strictly more than half of them.
  - `rndP` draws deterministically from a CRC of `s̄` and the round.
  - The `shorter` measure in `analyze_mech.py` uses the same set of rays and
    a 1e-9 relative tolerance.
  - The rule `eff` and the others take their losses against the identical
    `scip` trajectory in `logs/diag`.
- **Fairness.** The rules are compared paired on the same instances. Seeds
  are fixed (instance generator, `rnd` draws). Timing is not used for any
  conclusion.

### Novelty, solver relevance, task coverage

The novelty and solver-relevance statements are appropriately modest, and
the recommendation now follows from the data ("keep SCIP's set"). The
explanation of the reversal is honestly labeled partial. That is a
legitimate outcome of the task's diagnostic step, not an omission.

### Processes

`pgrep -fa 'mrloop|run_rev1|analyze_|run_queue|oq3'` found one
`run_queue.sh`. Its working directory is
`research-20261001/three-var-computation/code`, so it belongs to another
stream, and I did not touch it. No process of this stream was running. Every
reviewer job ran in the foreground with a `timeout` and finished. I used at
most 4 processes at a time.

## Checks actually run by the reviewer

All commands were run from `multiround/code/` unless stated, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`.

1. `timeout 600 python3 reviews/r2-scripts/indep_rev1.py` (from
   `reviews/r2-scripts/`). Exit 0. All values match; see above.
2. `timeout 300 python3 oq3_r2.py` (from `reviews/r2-scripts/`). Output:
   "rounds 0-29 verified: True".
3. `timeout 900 python3 analyze_mech.py '../logs/diag/[cd]*_6x8*.jsonl' 10`,
   the same for `'../logs/diag/diag_10x20*.jsonl'`, and
   `timeout 600 python3 analyze_rev1.py`. All exit 0. Outputs are identical
   to `logs/summary_mech_6x8.log`, `logs/summary_mech_10x20.log` and
   `logs/summary_rev1.log`.
4. `timeout 600 python3 check_clip.py` and
   `timeout 900 python3 check_consistency.py`. Outputs are identical to the
   stored logs.
5. `timeout 600 python3 analyze_pooled.py`,
   `timeout 600 python3 analyze_key.py 10x20` and
   `timeout 600 python3 analyze_percase.py '../logs/diag/diag_6x8*.jsonl' 10`.
   All are identical to the stored logs.
6. `timeout 900 python3 mrloop.py ../data/inst_6x8.json maj2,rnd0.33 20 /tmp/rv2/rr.jsonl 0 3`
   and
   `timeout 900 python3 mrloop.py ../data/inst_10x20.json first_orbit,maj2,rnd0.33 20 /tmp/rv2/rr10.jsonl 40 42`.
   Both exit 0. All 12 trajectories are bitwise identical to `logs/rev1`.
7. An inline Python count of LP values above `z_bil` in `logs/rev1`: 335 of
   5335 states, at most 6.9e-7 relative.
8. An inline Python check of `logs/fid2_exploop_4x4.jsonl`. Round 1:
   `orbit` 0.891, `orbit_core` 0.863. This matches Section 6, item 2.
9. Reading of `logs/summary_state_10x20.log`,
   `logs/summary_swappot_6x8.log`, `logs/summary_ties_10x20.log`,
   `logs/summary_key_6x8.log`, `logs/summary_key_4x4.log`,
   `logs/rev1/done*.txt` and the record counts and statuses in `logs/rev1`.
10. `pgrep -fa 'mrloop|run_rev1|analyze_|run_queue|oq3'`, plus `/proc/PID/cwd`
    for the one match. It belongs to another stream; see Processes above.

I did not run project-wide verification and did not look at CI.
