# Multi-round intersection cuts for bilinear terms: why the best-orbit rule falls behind, and what the root loop can guarantee

Workstream note, research-20261001, stream `multiround/`. Program:
[../PROGRAM.md](../PROGRAM.md). Builds on
[../../research-20260928b/sfree/optimal-intersection-cuts.md](../../research-20260928b/sfree/optimal-intersection-cuts.md)
("the sfree note"), its code and logs, and OQ3 of the scout report
[../../research-20260928b/scouting/s-free-intersection-cuts.md](../../research-20260928b/scouting/s-free-intersection-cuts.md).
Code in [code/](code/), raw outputs in [logs/](logs/), cached instances in
[data/](data/), downloaded sources in [sources/](sources/).
Dates: work began 2026-10-01; an earlier author run stopped at a usage limit on
2026-10-02, and this note was written in a continuation run on 2026-10-02.
It had four independent review rounds (review round 1,
[reviews/review-r1.md](reviews/review-r1.md), and review round 2,
[reviews/review-r2.md](reviews/review-r2.md), and review round 3,
[reviews/review-r3.md](reviews/review-r3.md), and review round 4,
[reviews/review-r4.md](reviews/review-r4.md)). Final status (2026-10-04):
reviewed in four rounds; r4 verified the r3 fixes; its optional remarks are applied;
not refereed.
Sections 11–13 list each review issue and how
it was handled.
Program files were included in repository commits made outside this program
(e.g. `d91d8d98b`, `f785387a8`, `b59ed1b83`); the program itself makes no commits.

## Summary

**Question.** The sfree note found that choosing, in every round, the
maximal quadratic-free set whose cut is best for the current reduced costs
(the "best-orbit rule") wins the first round but falls behind SCIP's fixed
set after several rounds (6×8 instances, 0.887 against 0.931 of the root gap
after 10 rounds, n = 10). Why, and which multi-round rule works? Does the
root loop converge (OQ3 of the scout report)?

**Main answers** (revised after review round 3; Sections 11–13
list the changes).

1. *The reversal is real but smaller than reported* (numerical, 220 paired
   instances in four sizes). Pooled, the best-orbit rule ties SCIP's rule
   after round 1 (−0.001 [−0.016, +0.014]) and is behind by 0.012
   [0.006, 0.017] after rounds 10 and 20; the loss is significant on 6×8 and
   10×20 (−0.011 and −0.025 after round 10). The earlier corner-bound code
   underestimates `z_K` when two projected rays are collinear (13% of the LP
   corners checked against SCIP). This changes the one-cut numbers of the
   sfree note and the round-1 loop numbers (corrected minus bug-affected
   orbit rule after round 1: +0.011 [+0.004, +0.019], 220 instances), but
   **not** the multi-round reversal (−0.001 [−0.003, +0.002] after round 10).
   On the original 10 instances the corrected rule gives 0.904 instead of 0.887
   after 10 rounds; that difference comes from one instance and is within the
   loop's instance-level noise (Sections 1.3, 2, 6).
2. *Cause: a state effect created in rounds 0–4; the mechanism is only
   partly identified* (numerical evidence and heuristics, Section 3).
   - On 6×8, from the same LP state after the root, one orbit round closes on
     average at least as much of the remaining gap as one SCIP round. This
     does not hold everywhere: on 10×20 the orbit round is slightly worse at
     the root (0.677 vs 0.689) and on orbit-trajectory states in rounds 3–5
     (0.241 vs 0.250). The loss comes mainly from the states that orbit rounds
     create, from which every rule progresses more slowly (6×8).
   - Switching experiments: the damage is spread over rounds 0–4. One orbit
     round at the root followed by SCIP rounds already carries about half of
     the orbit rule's loss (pooled over 220 instances: −0.006 [−0.011, −0.002]
     after round 10, against −0.012). Orbit rounds from round 5 on show no
     detectable cost. Shrinking deficits against SCIP do not by themselves
     show repair by later SCIP rounds. Against continued orbit rounds over
     rounds 3–20, `o1s` on 6×8 gains `+0.0006 [−0.0106, +0.0117]`, while
     `o3s` on 10×20 gains `+0.0078 [+0.0017, +0.0140]` (p = 0.013,
     uncorrected). With paired t-tests, neither size has a significant contrast after Holm over
     the 12 rule/size/pooled comparisons. Pooled `o3s` gains
     `+0.0060 [+0.0020, +0.0100]` (p = 0.00369, Holm p = 0.044 for those
     12 tests, but 0.133 over all 36 tests for three round spans, or 0.122 over
     the 33 distinct tests). The 12-test finding depends on the test choice (Section 3.5). This is
     exploratory evidence, not an established difference in repair between
     sizes (Section 3.5).
   - The mechanism of the first version is **withdrawn as the main cause**.
     It said that bound-attaining cuts make the corner LP dual degenerate
     (Proposition 7, proved; the orbit cuts have ≥ 2 binding rays at 13–34% of
     the corners, SCIP's at 0–0.5%) and that this produces flat states.
     Proposition 7 forces such ties only when the corner minimizer has
     support ≥ 2 (5–16% of root terms); the other ties come from the
     minimum-norm set that the bisection picks among bound-optimal sets. The
     mechanism does not separate the rules: `pertE0.1` and `geo` have ties at
     0–0.3% of their corners and `z_C/z_K` like SCIP's set, yet lose about as
     much (pooled −0.008 and −0.009 after round 10), and the per-instance
     degeneracy feature does not correlate with the loss.
   - A factor common to the losing rules that were measured (restricted
     after review round 2): on 6×8, the sets of the eight losing rules that
     use one non-SCIP set in every round (`orbit`, `orbit_core`, `orbitB`,
     `pert0.1`, `pertE0.1`, `pertE1`, `lex0.1`, `geo`) are shorter than SCIP's
     set on 57–71% of the rays at the same corner (on 10×20, measured only
     for `orbit`, `pertE0.1` and `geo`: 53–73%), while the three selection
     rules measured that do not lose (`eff`, `sumstep`, `oracle_seq`) pick sets that are
     shorter on only 8–25% of the rays. Not measured: `pert0.01`, `pert1`,
     `hyb0.9`, `alt2` and the switching schedules; `alt` mixes both sets. A
     direct test is inconclusive. Rule
     `maj2` uses the orbit set only where it is at least as long on most rays
     (a fifth to a third of the cuts); it has no detectable cost (pooled 0.000
     [−0.003, +0.003] after round 10). A random third (`rnd0.33`) costs
     −0.0025 [−0.0055, +0.0004]. The difference between the two, +0.003
     [−0.002, +0.007], is not significant. Within each of the eight single-set
     losing rules (on 6×8; three of them also on 10×20), none of the per-instance features tested (share of
     shorter steps, ties, degeneracy) correlates significantly with the loss;
     for `alt` the share of shorter steps correlates in the opposite direction
     (Section 3.6). So the common factor is a hypothesis consistent with the
     between-rule data, not an established cause.
   - Cut parallelism, the choice of terms and single-cut strength do not
     explain the reversal.
3. *Rules* (numerical, Section 4).
   - No rule that picks the set by a corner bound for one direction beats
     SCIP's rule after 10–20 rounds. This covers perturbed reduced costs,
     Euclidean geometry, lexicographic choice, alternation and completion (B).
   - The LP-gain oracle and two cuts per term win early (+0.03 to +0.04 after
     round 1) and lose the advantage by round 10.
   - Choosing per term among a few candidate sets by efficacy (`eff`, `eff2`),
     by the sum of normalized steps (`sumstep`), or by `maj2` is never
     significantly worse than SCIP's rule in any size. Only `eff` has a
     Holm-significant gain: +0.004 in the mean over rounds 1–10 (Holm
     p = 0.025 over 14 rules). `eff` was the best of those 14 rules, chosen
     after seeing the data. `eff2` has **no demonstrated gain** (+0.002 after
     round 10, Holm p = 0.78; mean over rounds 1–10 p = 0.065; −0.002 on
     10×20).

   **Recommendation:** keep SCIP's set. Do not replace it by the
   bound-optimal set, neither in every round nor at the root only. The
   controlled recovery comparison gives limited evidence for switching
   over continued orbit rounds, and no switching rule establishes a gain
   over SCIP throughout. If a
   second candidate set is computed, choosing per term by efficacy was never
   measurably worse on this generator, but it has no demonstrated benefit.
   All of this was measured on one random generator, outside SCIP.
4. *Convergence (OQ3).*
   - Proved (Theorem 2): if every cut for a term violated by at least `ε` has
     depth at least `η(ε)`, the values of the loop that cuts every violated
     term converge to the bilinear optimum. This also holds for a one-cut loop
     that cuts a most violated term (Remark 3a).
   - With pointed cones the depth condition holds for SCIP's rule and for
     *idealized* θ-approximate versions of two perturbed orbit rules
     (Lemma 4). I did not prove a uniform θ for the implemented bisection.
     The bound-optimal rule is not uniformly deep: its step can be `2√ε` at a
     fixed violation 1 (Proposition 5).
   - **OQ3 (iii) is answered negatively** (Proposition 6, proved; rounds
     0–12 checked in exact arithmetic). On a 3-variable instance, a sequence
     of maximal quadratic-free sets drives the LP values to any prescribed
     limit `1 + εξ_∞` in `(1, 1 + 2√ε) = (z_LP, z*)`. For `ε = 1/4` the limit
     can be 3/2 instead of `z* = 2`. The sets are images of SCIP's own set
     under automorphisms of `w ≤ xy`, and every vertex violates the
     constraint by 1.
   - OQ3 (i) and (ii) stay open. The observed loops have cones that become
     flat (pointedness 0.001 by rounds 11–19), so the sufficient condition does
     not apply to them.

**Novelty.** The convergence argument is standard. The counterexample is new
to these notes; the diagnosis is partial (a state effect created in early
rounds, with an unconfirmed candidate factor). That greedy one-round cut
quality is a poor guide over several rounds is well known for Gomory cuts. My
literature search was short, so no novelty claim is made.

**Solver relevance.** Limited. Everything is measured with the Python model
of SCIP's set in a simplified root loop on random McCormick instances. The
results argue against replacing SCIP's set by the bound-optimal set, even at
the root only. They show no measurable harm, and no demonstrated benefit, from
adding it as a second candidate filtered by efficacy, which SCIP's cut
selector would do naturally.

## 1. Setting, code and validation

### 1.1 The loop

As in the sfree note (Section 9.3, `exp_loop.py`): random bilinear programs
with McCormick envelopes and a few random rows (generator
`exp_mccormick.make_instance`, unchanged). Each round solves the LP (HiGHS),
takes the optimal basis cone, and adds, for every bilinear term violated by
more than `1e-6`, the cut(s) chosen by a rule. The measure is the fraction of
the root gap `z_bil − z_LP` closed after each round (`z_bil` from SCIP 10 via
PySCIPOpt). The stored fraction is clipped to `[0, 1 + 10^{-9}]`: in 3728 of the
52347 stored round states of the main runs the LP value exceeds SCIP's `z_bil`,
by at most `6.9·10^{-7}` relative to `max(1, |z_bil|)` (at most `2.1·10^{-4}` of
the root gap). This is within SCIP's feasibility tolerance, so there is no
evidence of invalid cuts (`code/check_clip.py`, `logs/check_clip.log`; the
reviewer's count against SCIP's primal value, with a `10^{-9}` threshold, is 3684). Sizes `p×m` mean `p` original variables and `m` products
(4×4: 3 extra rows; 6×8: 4; 8×12: 5; 10×20: 6).

Instances are cached once (`code/gen_instances.py`, logs `logs/gen_*.log`):
60 instances each of 4×4 and 6×8, and the first 50 of the 60 cached 8×12 and
10×20 instances. Filters as in `exp_loop.py`: LP optimal with a simplicial
basis cone, SCIP status optimal, `z_bil − z_LP > 1e-6`.

The loop runner is `code/mrloop.py` (helpers `code/mrcore.py`,
`code/fastorbit.py`). Rules:

| Rule | Set chosen for each violated term |
|---|---|
| `scip` | Python model of SCIP's Case-4 set (default `λ`), as `exp_loop.py` |
| `orbit` | best sliced-orbit set `C_F` for the corner bound with the current reduced costs `w` (bisection, family (A) of the sfree note) |
| `orbit_core` | the same, but the bisection is capped by `core.corner_bound`, as in `exp_loop.py` (see 1.3) |
| `orbitB` | completion (B) of the `orbit` set |
| `corner` | the objective-parallel corner cut `w^T λ ≥ z_K` |
| `pertD` | best orbit set for the weights `u = w/max w + D` (`D` = 0.01, 0.1, 1) |
| `geo` | best orbit set for `u_j = ‖r_j‖`, i.e. maximize the smallest Euclidean step `min_j α_j‖r_j‖` |
| `pertED` | best orbit set for `u_j = ‖r_j‖(ŵ_j + D)`, `ŵ_j = (w_j/‖r_j‖)/max_i(w_i/‖r_i‖)` (`D` = 0.1, 1): a corner bound with perturbed reduced costs, in Euclidean units |
| `lex0.1` | among orbit sets within 10% of the best corner bound, the one with the largest smallest Euclidean step |
| `alt`, `alt2` | orbit in even rounds and SCIP in odd rounds (`alt`), or the reverse (`alt2`) |
| `first_orbit` (= `o1s`), `oKs` | orbit in rounds `0..K−1`, SCIP afterwards |
| `sKo` | SCIP in rounds `0..K−1`, orbit afterwards |
| `both`, `bothpert` | two cuts per term: SCIP and orbit, or SCIP and `pert0.1` |
| `oracle` | per term, the candidate of the pool {scip, orbit, pert0.1, pert1, geo} with the largest LP value when added alone to the current LP |
| `oracle_seq` | as `oracle`, but each candidate is evaluated together with the cuts already chosen in this round |
| `eff` | same pool, largest efficacy (Euclidean distance from the vertex to the cut hyperplane) |
| `depth` | same pool, largest distance from the vertex to `K ∩ {cut}` |
| `sumstep` | same pool, largest sum of normalized step lengths `Σ_j min(1, α_j/t_j)` (`t_j` = first hit of ray `j`) |
| `eff2` | per term, the larger-efficacy cut of the two sets `scip` and `orbit` |
| `hybT` | per term, SCIP's set if its corner bound is at least `T·z_K`, else the orbit set (`T` = 0.9, 0.5) |

`oracle` and `oracle_seq` re-solve the LP for every candidate. They are
oracles for "the LP gain after re-solving", not practical rules.

### 1.2 Reproduction of `exp_loop.py`

Rerunning the original script of the sfree note
(`exp_loop.py 21 30 8` and `exp_loop.py 22 30 10 … 6 8 4`) reproduced every
recorded number exactly: maximum absolute difference 0 over all instances,
rules and rounds (`code/compare_repro.py`, `logs/compare_repro.log`). In
particular the 6×8 values after 10 rounds are again 0.931 (SCIP) and 0.887
(orbit), n = 10. **Computed exactly** (bitwise rerun).

The new runner on the same 10 instances (regenerated with the same seed and
filters, `data/inst_exploop_6x8.json`) gives SCIP 0.686 / 0.820 / 0.861 /
0.931 after rounds 1/2/3/10 with 32.6 cuts, identical to `exp_loop.py`, and
`orbit_core` 0.701 / 0.795 / 0.829 / 0.883 against 0.701 / 0.796 / 0.832 /
0.887 (`logs/fid2_exploop_6x8_summary.log`, final code; the earlier run
`logs/fid_exploop_6x8_summary.log`, made before the SDP fallback fix of item 3
below, gave 0.884, and differs from the rerun in 7 of 50 runs by at most
0.0095). The small `orbit_core`
difference comes from the SDP solver path (Clarabel called directly here,
through cvxpy in `exp_loop.py`); the bisection returns the same `F` up to
solver tolerance (`code/check_fastorbit.py`: maximum relative coefficient
difference `5.3e-6` on 8 corners), and the loop amplifies such differences
over 10 rounds.

### 1.3 A bug in the earlier corner-bound code, and its effect

`core.corner_bound` (sfree note) can return an infeasible two-ray point when
the two projected rays are collinear: the closed form for the pair is then
`0/0`-unstable. It then *underestimates* `z_K`.

- Against SCIP global solves of `min{w^T λ : λ ≥ 0, q(s̄ + Pλ) ≤ 0}` on 420
  LP corners (root and after 1–2 SCIP rounds, all four sizes;
  `code/check_zk_scip.py 101 25`, `logs/check_zk_scip.log`): `core` differs by
  more than `1e-4` (relative) in 82 corners; in 58 it is below SCIP's value and
  its minimizer is infeasible in 55 (33 of 167 root corners, 17 of 141 after
  one round, 5 of 112 after two). At those 55 corners the median ratio of the
  `core` value to the corrected one is 0.06 (`code/summarize_zk_scip.py`,
  `logs/summarize_zk_scip.log`).
- The vectorized replacement `mrcore.zk_vec` (supports of size 1 and 2,
  which suffice for bilinear terms by Theorem 4 of the sfree note; pairs of
  collinear projected rays skipped; every returned point checked feasible)
  agrees with SCIP within `1e-4` in 393 of 420 corners. In the other 27 the
  values are tiny (`1e-7`–`1e-5`) and `zk_vec` is up to 7.6% *larger*, with a
  checked feasible point; this is consistent with SCIP's absolute feasibility
  tolerance `1e-6` letting it accept slightly infeasible points. On 347
  random and LP corners `zk_vec` and `core` agree except in 10 corners, in all
  of which the `core` point is infeasible (`code/check_zk.py 1 300`,
  `logs/check_zk.log`).

Effects on earlier results (corrections to the sfree note, Section 9):

1. **One-cut table (Section 9.2).** Recomputed with the corrected `z_K` and
   the corrected cap of the orbit bisection (`code/recheck_mccormick.py`,
   `logs/recheck_mccormick_11.log`, `logs/recheck_mccormick_12.log`): `core`
   was wrong in 3 of 47 corners (4×4) and 7 of 73 (6×8). Corrected means: SCIP
   corner increment 0.724 (was 0.700) and 0.616 (was 0.591); orbit and corner
   increment 0.783 (was 0.755) and 0.675 (was 0.648); LP re-solve with the
   orbit set 0.931 (was 0.929) and 0.910 (was 0.907). The orbit set attains
   the *corrected* `z_K` in all 120 corners (minimum ratio 1.000000 at the
   bisection resolution). SCIP's set is below `0.9 z_K` in 27 of 120 corners
   (was 26) and below `0.5 z_K` in 3. Orbit beats SCIP's set after the LP
   re-solve by more than 0.01 in 62 corners (was 60) and loses by more than
   0.01 in 22 (was 26). The qualitative conclusions of Section 9.2 stand.
2. **Loop table (Section 9.3).** `exp_loop.py` capped the orbit bisection by
   the wrong `z_K`, so its "best orbit set" was sometimes not the best. With
   the corrected cap (`orbit`) the same 10 instances give 0.904 after 10
   rounds instead of 0.887 (`logs/fid2_exploop_6x8_summary.log`); SCIP's 0.931
   is unchanged. *Revised after review round 1:* the first version attributed
   about 40% (0.017) of the reported gap of 0.044 to the bug. That is not
   supported. The per-instance differences `orbit − orbit_core` after round 10
   on the 10 instances are `0, 0, 0, 0, +0.212, 0, 0, +0.016, +0.004, −0.028`
   (mean +0.020 [−0.028, +0.069]): one instance carries the whole change, and
   after rounds 1 and 3 the two rules agree within ±0.002 on average. On the
   220 main-run instances the bug matters in round 1 (`orbit − orbit_core`
   +0.011 [+0.004, +0.019]) but not later: +0.004 [−0.001, +0.008] after round
   3, −0.001 [−0.003, +0.002] after round 10 and −0.002 [−0.004, +0.001] after
   round 20, and no size differs significantly after round 10
   (`code/analyze_rev1.py`, `logs/summary_rev1.log`). So the bug changes the
   one-cut and round-1 numbers but not the multi-round reversal; the change
   from 0.887 to 0.904 on the 10 instances is within the loop's
   instance-level noise.
3. An SDP solver failure (`NumericalError` of Clarabel inside the bisection)
   was treated as infeasibility in the first version of `fastorbit.py`; it now
   falls back to the cvxpy formulation of the sfree note (`FALLBACK` counter).
   All reported loop runs use the corrected version, except the first
   fidelity run `logs/fid_exploop_*` (superseded by `logs/fid2_exploop_*`);
   stored trajectories were re-checked against later reruns (Section 8,
   item 12).

## 2. Larger sample: the reversal is real but small

Main runs: 20 rounds, all instances of Section 1.1, paired by instance
(`code/run_main.sh`, `code/jobs_main.txt`, `code/run_queue.sh`; records
`logs/main/*.jsonl`; summaries `logs/summary_main_*.log`
(`code/analyze_main.py`, t- and bootstrap intervals agree) and
`logs/summary_key_*.log` (`code/analyze_key.py`)). With SCIP's rule the loop
closes more than 0.999 of the gap after 20 rounds in 48/60, 42/60, 40/50 and
29/50 instances (4×4, 6×8, 8×12, 10×20), so later-round differences come from
the remaining instances.

Mean fraction of the root gap closed, and the paired difference to SCIP's rule
(mean [95% t-interval], wins/losses by more than 0.01 after round 10):

| Size (n) | SCIP r1 / r3 / r10 / r20 | orbit r1 / r3 / r10 / r20 | orbit − SCIP, r3 | r10 | r20 | W/L r10 |
|---|---|---|---|---|---|---|
| 4×4 (60) | 0.757 / 0.929 / 0.974 / 0.980 | 0.761 / 0.925 / 0.966 / 0.971 | −0.004 [−0.017, +0.010] | −0.008 [−0.016, +0.001] | −0.009 [−0.019, +0.000] | 4/8 |
| 6×8 (60) | 0.754 / 0.920 / 0.968 / 0.973 | 0.755 / 0.899 / 0.957 / 0.964 | −0.021 [−0.038, −0.004] | −0.011 [−0.019, −0.002] | −0.009 [−0.016, −0.001] | 5/14 |
| 8×12 (50) | 0.804 / 0.948 / 0.974 / 0.976 | 0.799 / 0.945 / 0.969 / 0.971 | −0.003 [−0.010, +0.004] | −0.005 [−0.010, +0.000] | −0.005 [−0.010, +0.001] | 1/7 |
| 10×20 (50) | 0.705 / 0.881 / 0.937 / 0.945 | 0.699 / 0.866 / 0.912 / 0.920 | −0.015 [−0.037, +0.006] | −0.025 [−0.045, −0.005] | −0.024 [−0.044, −0.005] | 6/14 |

Pooled over all 220 instances (`code/analyze_pooled.py`,
`logs/summary_pooled.log`): orbit − SCIP is −0.001 [−0.016, +0.014] after
round 1, −0.011 [−0.019, −0.003] after round 3, −0.012 [−0.017, −0.006] after
round 10 (Holm-adjusted p = 0.0008 over the 14 rules compared) and −0.012
[−0.017, −0.006] after round 20.

Conclusions (**numerical evidence**):

- The reversal reported in the sfree note is real: the best-orbit rule ties
  SCIP's rule in round 1 and falls behind from round 2–3 on, in every size,
  significantly in 6×8, 10×20 and pooled. It is smaller than the n = 10 sample
  suggested (0.044 there); the typical loss is 0.005–0.025 of the root gap.
  The corner-bound bug of Section 1.3 does not change the multi-round loss
  (`orbit` and `orbit_core` differ by −0.001 [−0.003, +0.002] after round 10).
- The loss is concentrated: on 6×8, 14 instances lose more than 0.01 after
  round 10 and 5 gain; most instances are closed by both rules.
- The bug-affected variant `orbit_core` and the completion (B) `orbitB`
  behave like `orbit` after round 10 (pooled −0.011 for `orbit_core`; on 6×8,
  −0.014 for `orbitB`); `orbit_core` is worse in round 1 (pooled −0.013).
  Completion (B) never helps.
- The objective-parallel corner cut stalls after one round in every size
  (pooled −0.42 after round 10), as in the sfree note.

## 3. Diagnosis of the reversal

Data: diagnostic runs `logs/diag/diag_6x8_*.jsonl` (60 instances) and
`logs/diag/diag_10x20_*.jsonl` (30 instances), rules `scip`, `orbit`,
`pertE0.1`, `geo`, `both`, 20 rounds, with per-cut records and two
counterfactual rounds from every visited LP state: one SCIP round and one
orbit round ("swap"). Their trajectories are identical to the main runs
(Section 8, item 12). Summaries: `logs/summary_diag_6x8.log` (`code/analyze_diag.py`),
`logs/summary_state_6x8.log`, `logs/summary_state_10x20.log`
(`code/analyze_state.py`). "Rate" means the fraction of the *remaining* gap
`z_bil − z_r` closed by one round. Buckets of rounds: 0, 1–2, 3–5, 6–10,
11–19; only states with remaining gap above `10^{-3}` of the root gap count.

### 3.1 On 6×8 the orbit round is not worse from the same state

On 6×8, from the same LP state, one orbit round closes on average at least as
much of the remaining gap as one SCIP round, on both trajectories (numerical;
at the root the two rates are 0.754 and 0.755 of the root gap):

| States visited by | rounds | SCIP round | orbit round |
|---|---|---|---|
| SCIP's rule | 1–2 (n = 88) | 0.604 | 0.627 |
| | 3–5 (n = 94) | 0.336 | 0.365 |
| | 6–10 (n = 116) | 0.164 | 0.200 |
| | 11–19 (n = 175) | 0.051 | 0.078 |
| the orbit rule | 1–2 (n = 70) | 0.451 | 0.464 |
| | 3–5 (n = 90) | 0.275 | 0.294 |
| | 6–10 (n = 124) | 0.136 | 0.141 |
| | 11–19 (n = 172) | 0.034 | 0.037 |

On 10×20 (`logs/summary_state_10x20.log`) the statement holds on SCIP's
states after the root (the orbit round is ahead by 0.036, 0.034, 0.030 and
0.001 in the four buckets), but not everywhere: at the root the orbit round
closes 0.677 against 0.689 for a SCIP round, and on orbit-trajectory states in
rounds 3–5 it closes 0.241 against 0.250 (rounds 1–2: 0.505 vs 0.503). So, at
least on 6×8 and on SCIP's 10×20 states, the reversal is **not** a per-round
effect: replacing one SCIP round after the root by an orbit round would, on
average, gain more in that round. The cause must lie mainly in the states the
orbit rule leads to.

### 3.2 The orbit rule leads to harder states

The table above already shows it: from the states the orbit rule visits, even
a SCIP round closes much less of the remaining gap (0.451 against 0.604 in
rounds 1–2). Because the two trajectories keep different instances alive, the
comparison is repeated paired by instance: for each instance and bucket,
average a state measure over the states of each trajectory, then compare
orbit − SCIP across instances with states on both (6×8, mean, 95% t-interval,
Wilcoxon p):

| Measure at the visited states | rounds 1–2 | 3–5 | 6–10 | 11–19 |
|---|---|---|---|---|
| rate of a SCIP round | −0.082 [−0.138, −0.026], p 0.006 (n 36) | −0.075 [−0.163, +0.013], p 0.07 (31) | −0.070 [−0.146, +0.005], p 0.007 (24) | −0.065 [−0.161, +0.031], p 0.33 (17) |
| potential `max_e z_K/(z_bil − z_r)` | −0.060 [−0.124, +0.005], p 0.12 | −0.062 [−0.154, +0.030], p 0.09 | −0.066 [−0.142, +0.011], p 0.004 | −0.056, p 0.26 |
| fraction of reduced costs `≤ 10^{-3} max` | +0.003, p 0.41 | +0.007, p 0.19 | +0.024 [+0.007, +0.040], p 0.007 | +0.029 [+0.001, +0.057], p 0.04 |
| `log10 γ` (pointedness) | −0.099 [−0.173, −0.026], p 0.006 | +0.011, p 0.56 | −0.068, p 0.47 | −0.211, p 0.52 |

The *potential* is the best single-cut gain of the most promising term at the
state (the corner bound with the current reduced costs), as a fraction of the
remaining gap; it bounds what any one intersection cut can achieve in the
corner relaxation. On 10×20 (30 instances) the signs agree but fewer cells
are significant: rate of an orbit round in rounds 3–5 −0.146 [−0.270, −0.022]
(p 0.005), tiny reduced costs in rounds 3–5 +0.014 [+0.004, +0.023]
(p 0.010), rate of a SCIP round in rounds 3–5 −0.102 (p 0.08). For the
perturbed rules `pertE0.1` and `geo` the same comparisons show at most one
significant cell per size (`logs/summary_state_*.log`).

So, **numerically**: orbit trajectories reach states with less corner
potential, more (near-)zero reduced costs and, early on, flatter cones; from
those states every rule progresses more slowly. Exact zero reduced costs
(`≤ 10^{-9}` of the maximum) occur at 4.0%, 2.1%, 1.4% and 1.3% of the orbit
vertices in the four buckets and never on SCIP's trajectory
(`logs/summary_diag_6x8.log`); the `corner` rule, whose cut is fully
objective-parallel, has them at every vertex after round 0.

*Direct one-step test.* The comparison above is between trajectories. To
isolate one round, `swappot` runs (6×8, 60 instances, `scip` and `orbit`
trajectories; `logs/diag/swappot_6x8.jsonl`, `logs/summary_swappot_6x8.log`)
apply one SCIP round and one orbit round to the *same* state and measure the
vertex each produces. Median potential of the new vertex, after a SCIP round
vs after an orbit round, at states of SCIP's trajectory: 0.270 vs 0.206
(round 0, 37 states), 0.216 vs 0.189 (rounds 1–2), 0.133 vs 0.073 (3–5),
0.049 vs 0.038 (6–10), 0.010 vs 0.006 (11–19). The state-level paired
differences are significant only in rounds 6–10 (Wilcoxon p = 0.008) and
11–19 (p = 0.03) on SCIP's trajectory and in rounds 1–2 on the orbit
trajectory (p = 0.03); averaged per instance, the differences are negative
(−0.014 to −0.061 in rounds 0–5) but their intervals include 0. Vertices with
a normalized reduced cost `≤ 10^{-6}` follow 2–9% of the orbit rounds and
0–1% of the SCIP rounds, and the mean number of reduced costs `≤ 10^{-3}` is
higher or equal after orbit rounds in every bucket (for example 0.41 vs 0.23
in rounds 6–10; equal, 0.27 vs 0.27, on the orbit trajectory in rounds 3–5). States where either round closes the whole gap are excluded (the
potential is undefined there), which removes 23 of the 60 root states. So
one orbit round leaves, from the same state, a vertex with somewhat less
corner potential and more near-degenerate reduced costs: the direction is
consistent with Section 3.2, the statistical strength is modest.

### 3.3 Bound-attaining cuts and dual degeneracy: true for `orbit`, but not the main cause

**Proposition 7.** Let `w ∈ R^N_{>0}`, `S'` closed, `x̄ ∉ S'`, and let
`λ*` be a corner minimizer: `λ* ≥ 0`, `x̄ + Rλ* ∈ S'`,
`w^T λ* = z_K ∈ (0, ∞)`, with support `J`. Let `C` be S'-free with
`x̄ ∈ int C` and steps `α_j`. If the cut attains the corner bound,
`z_C(w) = min_j w_j α_j = z_K`, then `w_j α_j = z_K` for every `j ∈ J`, and
the corner LP after the cut, `min{w^T λ : λ ≥ 0, Σ_j λ_j/α_j ≥ 1}`, has the
whole simplex `conv{α_j e_j : j ∈ J}` in its optimal face; `λ*` lies in the
relative interior of that simplex. In particular, if `|J| ≥ 2`, the corner LP
after a bound-attaining cut is dual degenerate, and its optimal face contains
a point of `S'`.

*Proof.* `λ*` corresponds to a point of `S'` in the cone, so it satisfies the
valid cut: `Σ_{j∈J} λ*_j/α_j ≥ 1`. For every `j`, `w_j α_j ≥ z_C = z_K`, i.e.
`1/α_j ≤ w_j/z_K` (also when `α_j = ∞`). Hence
`1 ≤ Σ_{j∈J} λ*_j/α_j ≤ Σ_{j∈J} λ*_j w_j / z_K = 1`, so equality holds termwise
for `j ∈ J` (where `λ*_j > 0`): `α_j = z_K/w_j < ∞`. Then
`λ* = Σ_{j∈J} (λ*_j/α_j)(α_j e_j)` with weights summing to 1, and each
`α_j e_j` has objective `w_j α_j = z_K`, the optimal value of the corner LP. ∎

Status: **proved** (elementary). For a bilinear term the corner minimizer has
support at most 2 (sfree note, Theorem 4). In both cases the optimal set of
the corner LP after a bound-attaining cut contains a point that satisfies the
term: for `|J| = 1` it is the first hit `x̄ + t_j r_j` of the cheapest ray
(then `α_j = t_j`), for `|J| = 2` an edge through the corner point.

How often each case occurs (numerical): at the root vertices, the corner
minimizer has support 2 for 8.5%, 5.1%, 8.1% and 16.3% of the violated terms
(4×4, 6×8, 8×12, 10×20; 117–398 terms per size), and the orbit set attains
`z_K` (relative `10^{-6}`) for 117/117, 211/215, 221/222 and 392/398 of them
(`code/support_stats.py`, `logs/support_stats.log`). The orbit cut has two or
more binding rays (`w_j α_j` within `10^{-3}` of `z_C`), i.e. a dual degenerate
corner LP, at 17–24% of the corners in every bucket on 6×8 and 13–34% on 10×20;
SCIP's cut at the same corners has two binding rays at 0–0.5% of them
(`code/analyze_ties.py`, `logs/summary_ties_*.log`). So the orbit sets create
more ties than Proposition 7 forces: Proposition 7 forces ties only when the
corner minimizer has support ≥ 2 (5–16% of root terms). The other ties come
from the choice among bound-optimal sets: the bisection returns the
minimum-norm `F`, which tends to make several rays binding. Another
bound-optimal set might avoid them (untested).

*Proposed consequence (first version; withdrawn as the main cause after
review round 1).* The first version argued as follows (**heuristic**). The
best orbit set attains `z_K` at essentially every LP corner (mean `z_C/z_K`
between 0.995 and 1.000 per bucket), so after an orbit cut the corner LP's
optimum already contains a point that satisfies the term, and with two binding
rays a whole edge on which the objective is constant. In the full LP that
point is usually cut off by other rows and other terms' cuts, the next vertex
lies on a nearly flat part of the new face, its corner bound is near zero, and
the loop stalls, as in the classical stalling of objective-parallel Gomory
cuts under dual degeneracy (Zanette, Fischetti and Balas, Math. Program. 130,
2011, known to me through its abstract only). SCIP's set does not attain
`z_K` (mean `z_C/z_K` 0.84–0.92), and the corner LP after its cut has a unique
optimal vertex.

This mechanism is real for `orbit`, but it does not separate the rules, so it
cannot be the main cause of the reversal (`code/analyze_mech.py`,
`logs/summary_mech_6x8.log`, `logs/summary_mech_10x20.log`; numerical):

- *Rules without ties lose about as much.* `pertE0.1` and `geo` have ≥ 2
  binding rays at 0–0.3% of their corners in every bucket (6×8 and 10×20),
  like SCIP's set (0–0.5%) and unlike `orbit` (17–24% on 6×8, 13–34% on
  10×20). Their mean `z_C/z_K` is 0.83–0.92 (`pertE0.1`) and 0.79–0.83
  (`geo`) on 6×8, like SCIP's 0.84–0.92. Yet they lose: on 6×8 after round 10
  −0.010 (`pertE0.1`) and −0.015 (`geo`) against −0.011 for `orbit`; pooled
  −0.008 and −0.009 (Holm p = 0.016 and 0.003) against −0.012. `pertE0.1`
  ties SCIP's rule in round 1 (−0.005, pooled), so its later loss is not a bad
  first round.
- *The degeneracy feature does not predict the loss.* The share of rounds
  1–5 whose vertex has a near-zero reduced cost (orbit minus SCIP trajectory)
  has Spearman correlation +0.08 (p = 0.55) with the per-instance loss on 6×8
  and +0.18 (p = 0.33) on 10×20 (`logs/summary_percase_*.log`; the first
  version reported only the other features). The share of corners with ties
  on the orbit trajectory does not correlate either (−0.11, p = 0.42, on 6×8;
  +0.07, p = 0.70, on 10×20; `logs/summary_mech_*.log`).

Other measurements of the first version, re-examined (6×8,
`logs/summary_diag_6x8.log`, numerical):

- *Tilt toward the objective is mostly a trajectory effect.* On the own
  trajectories, mean `|cos|` between cut normal and objective is 0.624 and
  0.717 for orbit in rounds 1–2 and 3–5, against 0.588 and 0.687 for SCIP;
  but these are different states. At the same corners (rule `both`, which
  computes both cuts at every corner) the orbit cut is more objective-parallel
  by at most 0.012 (0.626 vs 0.618 in rounds 1–2, 0.707 vs 0.695 in rounds
  3–5, 0.008 and 0.005 later), and the values are equal at the root (0.544 vs
  0.546). On the own trajectories in rounds 11–19 the orbit value is lower
  (0.818 vs 0.824). On 10×20 the orbit cuts are
  on average slightly *less* objective-parallel in rounds 1–5 (mean feature
  difference −0.010, `logs/summary_percase_10x20.log`).
- *Step lengths.* On rays with normalized reduced cost `> 0.1`, the orbit step
  is shorter than SCIP's by a median factor `10^{-0.10}`–`10^{-0.22}`, but
  `geo` and `pertE0.1` have equally short or shorter steps there
  (`10^{-0.09}`–`10^{-0.30}`). On cheap rays (`≤ 10^{-3}`) the orbit step is
  longer than SCIP's only at the root (`10^{+0.10}`) and in rounds 3–5
  (`10^{+0.35}`), and shorter in rounds 1–2, 6–10 and 11–19 (`10^{-0.04}`,
  `10^{-0.07}`, `10^{-0.02}`). So "deep along cheap rays, shallow along
  expensive ones" is not a consistent property of the orbit rule; "shorter
  than SCIP's along most rays" is a property of every orbit-family rule
  (Section 3.6).
- *Violation left behind.* Median violation of the terms that receive cuts:
  orbit 0.068 and 0.031 in rounds 1–2 and 3–5, SCIP 0.036 and 0.014; orbit
  cuts are shallower relative to the violation (median depth/violation 0.32
  against 0.44 in rounds 1–2). This is again a comparison of different states.
- *Per-instance association.* Across the 60 instances, the loss of the orbit
  rule after round 10 correlates with flatter cones (Spearman +0.36,
  p = 0.005) and with more objective-parallel cuts (−0.36, p = 0.005) on its
  trajectory in rounds 1–5, relative to SCIP's (`code/analyze_percase.py`,
  `logs/summary_percase_6x8.log`); on 10×20 the same correlations are +0.35
  (p = 0.055) and −0.35 (p = 0.061). These features are partly consequences of
  stalling, so this is association, not evidence of cause.
- *Case study* (6×8 instance 53, the largest loss: −0.163 after 10 rounds).
  Both rules start from the same root state (round 1 closes 0.518 with the
  orbit set, 0.483 with SCIP's). The vertex after the orbit round has two zero
  reduced costs; the orbit rule then adds one cut, the cone pointedness drops
  from 0.12 to 0.035, 0.008 and 0.005 in rounds 1–3, and the loop crawls
  (0.661, 0.690, 0.702, …, 0.837 after 10 rounds). SCIP's trajectory has `γ` =
  0.087, 0.035, 0.030 in rounds 1–3 and reaches 0.959 after 3 rounds. One
  instance illustrates the degeneracy route; the counts above show that it is
  not the typical route.

### 3.4 What does not explain the reversal

- *Cut parallelism and diversity.* Within a round, the largest `|cos|`
  between a new cut and earlier cuts of the same round is similar
  (rounds 1–2: orbit 0.60, SCIP 0.53; rounds 6–10: 0.74 and 0.70); against
  cuts of earlier rounds it is 0.86–0.998 for every rule. Near-parallel cuts
  are universal in later rounds and do not separate the rules.
- *Which terms get cuts.* The fraction of cuts on a term that was also cut in
  the previous round is 0.85–0.97 for both rules. The orbit rule cuts *more*
  terms per round later (5.3 against 4.5 in rounds 6–10), because more terms
  stay violated.
- *Single-cut strength.* The single-cut LP gain of an orbit cut is at least
  that of SCIP's (Section 3.1 and table "Mean single-cut LP gain").
- *Dual degeneracy as a frequent exact event.* Exact zero reduced costs occur
  at only 1–4% of the orbit vertices, too rarely to explain the gap alone; the
  continuous measures (potential, tiny reduced costs) carry the effect.

### 3.5 State versus policy: switching rules mid-loop

If the damage is done by the states the orbit rounds create, a few orbit
rounds followed by SCIP rounds should keep the loss, and orbit rounds started
late should be harmless. Rules `oKs` (orbit in rounds `0..K−1`, then SCIP;
`o1s` = `first_orbit`) and `sKo` (SCIP in rounds `0..K−1`, then orbit),
difference to SCIP's rule (mean [95% t-interval]; 6×8: 60 instances, 10×20:
50; `code/analyze_rev1.py`, `logs/summary_rev1.log`, which also gives rounds 1
and 5; revised after review round 1, which found that the first version
omitted the round-3 column and the 4×4 row of `o1s`; `o1s` on 8×12 and 10×20
was run for this revision):

| Rule | 6×8, r3 | 6×8, r10 | 6×8, r20 | 10×20, r3 | 10×20, r10 | 10×20, r20 |
|---|---|---|---|---|---|---|
| `o1s` | −0.014 [−0.025, −0.002] | −0.003 [−0.010, +0.004] | −0.001 [−0.007, +0.005] | −0.012 [−0.030, +0.007] | −0.013 [−0.027, +0.002] | −0.015 [−0.031, +0.001] |
| `o2s` | −0.023 [−0.040, −0.005] | −0.007 [−0.014, −0.000] | −0.004 [−0.010, +0.002] | −0.015 [−0.036, +0.006] | −0.017 [−0.032, −0.002] | −0.018 [−0.033, −0.004] |
| `o3s` | −0.021 [−0.038, −0.004] | −0.007 [−0.015, +0.001] | −0.004 [−0.011, +0.003] | −0.015 [−0.037, +0.006] | −0.019 [−0.039, +0.001] | −0.017 [−0.033, −0.000] |
| `o5s` | −0.021 [−0.038, −0.004] | −0.011 [−0.019, −0.002] | −0.006 [−0.014, +0.001] | −0.015 [−0.037, +0.006] | −0.026 [−0.044, −0.007] | −0.021 [−0.036, −0.006] |
| orbit throughout | −0.021 [−0.038, −0.004] | −0.011 [−0.019, −0.002] | −0.009 [−0.017, −0.001] | −0.015 [−0.037, +0.006] | −0.025 [−0.045, −0.005] | −0.024 [−0.044, −0.005] |
| `s1o` | −0.004 [−0.012, +0.003] | −0.006 [−0.011, −0.001] | −0.006 [−0.011, −0.001] | −0.006 [−0.017, +0.006] | −0.017 [−0.030, −0.004] | −0.019 [−0.033, −0.006] |
| `s3o` | 0 | −0.006 [−0.013, +0.001] | −0.004 [−0.010, +0.001] | 0 | −0.006 [−0.015, +0.002] | −0.006 [−0.013, +0.000] |
| `s5o` | 0 | −0.002 [−0.006, +0.002] | −0.002 [−0.006, +0.002] | 0 | +0.000 [−0.002, +0.002] | −0.004 [−0.010, +0.002] |

`o1s` in the other sizes and pooled (same log): 4×4 −0.009 [−0.021, +0.004]
after round 3 and −0.006 [−0.016, +0.003] after round 10 (orbit throughout:
−0.004 and −0.008); 8×12 +0.002 [−0.007, +0.010] and −0.003 [−0.009, +0.003]
(orbit: −0.003 and −0.005); pooled over 4×4 and 6×8 −0.011 [−0.020, −0.003]
after round 3 and −0.005 [−0.010, +0.001] after round 10; pooled over all 220
instances −0.008 [−0.015, −0.002] after round 3, −0.006 [−0.011, −0.002] after
round 10 and −0.006 [−0.011, −0.001] after round 20, about half of the orbit
rule's −0.012 (`o1s − orbit` after round 10: +0.006 [+0.001, +0.010]).

Reading (**numerical evidence**):

- *The root round contributes.* One orbit round at the root followed by 19
  SCIP rounds is significantly worse than SCIP's rule pooled (−0.006 after
  round 10) and on 6×8 after round 3 (−0.014); on 10×20 it carries about half
  of the full loss after rounds 10 and 20 (−0.013 and −0.015, intervals just
  include 0); on 4×4 about four fifths (−0.006 of −0.008, ratio 0.82 in the log; not
  significant).
  The first version's statement that an orbit round at the root is harmless
  was wrong: it rested on a non-significant round-10 difference on 6×8.
- *Later early rounds contribute too.* Each further orbit round in rounds 1–4
  adds loss on 10×20 (`o2s` −0.017, `o5s` −0.026 after round 10), and orbit
  rounds from round 1 on (`s1o`) cost 57% of the full loss on 6×8 and 68% on
  10×20 after round 10. `s3o` still costs −0.006 on both sizes (pooled over
  6×8 and 10×20: −0.006 [−0.012, −0.001]). Orbit rounds from round 5 on (`s5o`)
  show no detectable cost (pooled −0.001 [−0.003, +0.001] after round 10).
  So the damage is spread over rounds 0–4. Failing to detect a cost for `s5o`
  does not show that the cost is zero.
- *Shrinking deficits and the control for later SCIP rounds* (revised after
  review round 3). Change of the deficit `d(r)` = rule − SCIP after `r` rounds,
  paired per instance over the same spans for every rule (`code/analyze_rev2.py`,
  `logs/summary_rev2.log`; positive = the deficit shrinks):

  | Rule | 6×8, `d(20) − d(3)` | 6×8, `d(20) − d(10)` | 10×20, `d(20) − d(3)` | 10×20, `d(20) − d(10)` |
  |---|---|---|---|---|
  | `o1s` | +0.013 [+0.002, +0.024] | +0.002 [−0.001, +0.005] | −0.004 [−0.018, +0.011] | −0.002 [−0.007, +0.002] |
  | `o2s` | +0.019 [+0.001, +0.036] | +0.003 [−0.001, +0.007] | −0.004 [−0.017, +0.010] | −0.002 [−0.005, +0.002] |
  | `o3s` | +0.017 [−0.002, +0.035] | +0.003 [−0.002, +0.007] | −0.001 [−0.017, +0.015] | +0.003 [−0.002, +0.008] |
  | `o5s` | +0.015 [−0.003, +0.032] | +0.004 [−0.001, +0.009] | −0.005 [−0.019, +0.009] | +0.005 [−0.001, +0.011] |
  | orbit throughout | +0.012 [−0.003, +0.028] | +0.002 [−0.002, +0.006] | −0.009 [−0.026, +0.008] | +0.001 [−0.003, +0.005] |

  The span 3–20 contains only SCIP rounds for `o1s`, `o2s` and `o3s`; for
  `o5s` it also contains the orbit rounds 3 and 4. On 6×8 the deficits of
  `o1s` and `o2s` shrink significantly between rounds 3 and 20, and all five
  changes point the same way. On 10×20 no change over rounds 3–20 is
  positive and none is significant. Between rounds 10 and 20 the changes are
  small and none is significant in either size; on 10×20 their signs are
  mixed: the deficits of `o1s` and `o2s` grow slightly, those of `o3s` and
  `o5s` shrink by about as much as on 6×8 (`o5s` +0.005 on 10×20, +0.004 on
  6×8). Pooled over both sizes, the only nominally significant change is `o5s`
  between rounds 10 and 20 (+0.0045 [+0.0007, +0.0083], p = 0.021, one of 15
  pooled tests, not corrected for multiplicity).

  These are changes against SCIP throughout, not evidence that later SCIP
  rounds repair more than continued orbit rounds would. On 6×8 the mean
  remaining root gap under SCIP falls from `0.0802154` at round 3 to
  `0.0272196` at round 20, and even orbit throughout shrinks its deficit by
  `+0.0121881`, nearly the `+0.0127674` of `o1s`. Comparing whether each
  unadjusted interval separately excludes zero does not test their difference.

  The paired control contrast is `e(20) − e(3)`, where `e(r)` = switching
  rule − orbit throughout on the same instance. Positive means a gain over
  continued orbit rounds, measured as a fraction of the root gap. New
  analysis of the existing records (`code/analyze_rev3.py`,
  [logs/summary_rev3.log](logs/summary_rev3.log)); 95% paired t-intervals and
  uncorrected two-sided p-values:

  | Rule | 6×8 (n 60) | 10×20 (n 50) | Pooled (n 110) |
  |---|---|---|---|
  | `o1s` | +0.0006 [−0.0106, +0.0117], p 0.918 | +0.0052 [−0.0099, +0.0204], p 0.492 | +0.0027 [−0.0064, +0.0117], p 0.557 |
  | `o2s` | +0.0063 [+0.0007, +0.0120], p 0.0278 | +0.0054 [−0.0095, +0.0202], p 0.473 | +0.0059 [−0.0014, +0.0132], p 0.112 |
  | `o3s` | +0.0044 [−0.0009, +0.0098], p 0.104 | +0.0078 [+0.0017, +0.0140], p 0.0134 | +0.0060 [+0.0020, +0.0100], p 0.00369 |
  | `o5s` | +0.0025 [−0.0015, +0.0065], p 0.214 | +0.0037 [−0.0040, +0.0114], p 0.340 | +0.0030 [−0.0010, +0.0071], p 0.139 |

  `o1s` on 6×8 shows no detectable gain over continued orbit rounds. Each
  size has one nominally significant gain (`o2s` on 6×8, `o3s` on 10×20);
  with paired t-tests, neither survives Holm adjustment over all 12 cells of this table
  (p = `0.278`, `0.148`). Pooled `o3s` does survive that adjustment
  (p = `0.0443`). For `o3s` both trajectories use orbit through round 2,
  so this contrast starts from the same state and directly compares SCIP
  with orbit in subsequent rounds. For `o1s` and `o2s` the states at round 3
  already differ; their contrasts measure subsequent changes of those
  schedule differences. The `o5s` contrast also contains orbit rounds 3 and
  4; its contrast starting at round 5 is identical, since `o5s` and orbit
  coincide through that round.

  The log also reports spans 5–20 and 10–20. No contrast survives Holm over
  all 36 tests (four rules, two sizes and pooled, three spans); pooled `o3s`
  over 3–20 then has p = `0.133`. Three tests duplicate `o5s` 3–20 and 5–20
  in each group; over the 33 distinct tests the value is `0.122`. With
  Wilcoxon signed-rank tests, the 3–20 raw p-values are `0.0029` (10×20
  `o3s`), `0.0049` (pooled `o2s`) and `0.0056` (pooled `o3s`). Holm over
  the 12 cells keeps 10×20 `o3s` (`0.035`) but not pooled `o3s` (`0.056`).
  The size-specific t-test statement therefore depends on test choice; the
  exploratory reading and lack of an established size difference remain.
  These spans and rules were examined after
  seeing earlier results, and the adjustment does not cover the program's
  other comparisons. This is limited numerical evidence for later SCIP
  rounds helping some schedules relative to continued orbit rounds, not an
  established repair difference between 6×8 and 10×20. It also does not
  establish a gain over SCIP throughout (the baseline in the first table).
- So the loss is a **state effect** created in rounds 0–4, while the LP is
  still far from `z_bil`; late rounds have little gap left to lose.

### 3.6 Rules that neither attain the bound nor create ties also lose: a common factor?

Section 3.3 shows that bound attainment and ties occur for `orbit` (and, as
the runs of the revision after review round 2 show, for the other members of
the orbit family that use the bound-optimal set: `orbit_core`, `orbitB`, and
`alt` (over all its rounds); ties at 7–24% of the corners), while `pertE0.1`,
`geo`, `pert0.1`, `pertE1` and `lex0.1` have ties at no more than 3.4% of the corners and
lose too (Sections 2 and 4). A candidate factor common to these rules is that
their sets are *smaller than SCIP's set along most rays*. Measured at the
corners of each rule's own trajectory against SCIP's set at the same corner
(`code/analyze_mech.py`; `logs/summary_mech2_6x8.log` for all 6×8 rows,
`logs/summary_mech_10x20.log`; numerical). The first version of this section
and of the summary called the factor "shared by all losing rules", although it
had been measured only for `orbit`, `pertE0.1` and `geo` (review round 2,
issue n2). For this revision the measurement was extended on 6×8 to six more
losing rules (`code/run_rev2.sh`, records `logs/rev2/`, 60 instances, 20
rounds; their trajectories are identical to those of the main runs,
Section 8 item 33):

| Rule (6×8) | share of rays where the step is shorter than SCIP's | mean `log10(α/α_SCIP)` | loss after round 10 on 6×8 (n) |
|---|---|---|---|
| `orbit` | 0.61–0.62 | −0.11 to −0.22 | −0.0108 (60) |
| `orbit_core` | 0.61–0.63 | −0.11 to −0.22 | −0.0121 (60) |
| `orbitB` | 0.58–0.61 | −0.11 to −0.19 | −0.0145 (60) |
| `pert0.1` | 0.60–0.64 | −0.11 to −0.23 | −0.0135 (60) |
| `pertE0.1` | 0.63–0.65 | −0.11 to −0.32 | −0.0101 (60) |
| `pertE1` | 0.61–0.71 | −0.12 to −0.28 | −0.0102 (60) |
| `lex0.1` | 0.57–0.70 | −0.18 to −0.23 | −0.0093 (60) |
| `geo` | 0.65–0.71 | −0.14 to −0.29 | −0.0154 (60) |
| `alt` (orbit and SCIP rounds alternate) | 0.61 at the root, 0.19–0.37 later | −0.06 to −0.16 | −0.0087 (60) |
| `oracle_seq` | 0.14–0.25 | −0.04 to −0.02 | −0.0003 (30) |
| `eff` | 0.12–0.15 | −0.01 to +0.01 | +0.0038 (30) |
| `sumstep` | 0.08–0.13 | 0.00 to +0.02 | +0.0029 (30) |

(Ranges over the round buckets 0, 1–2, 3–5, 6–10, 11–19; shares over the
rays on which at least one of the two steps is finite; `eff`, `oracle_seq`
and `sumstep` from the 30-instance choice runs. The loss column is the mean
of rule − SCIP over the instances of these diagnostic records, as printed by
`analyze_mech.py`; the first version gave pooled losses from Section 4 here.
For `alt` the shares average the cuts of its orbit rounds with those of its
SCIP rounds, whose share is 0.) On 10×20 only `orbit`, `pertE0.1` and `geo`
were measured; their shares are 0.53–0.73.

So every losing rule measured that uses one non-SCIP set in every round (eight
rules on 6×8, three on 10×20) picks sets that are shorter than SCIP's on most
rays, and every selection rule measured that does not lose picks sets that are
rarely shorter, mostly because it often picks SCIP's set itself (60–70% of the
terms for `eff`, `logs/summary_choice_6x8.log`). Not measured: `pert0.01`,
`pert1`, `hyb0.9`, `alt2`, the switching schedules `oKs` and `sKo`, and every
rule other than `orbit`, `pertE0.1` and `geo` on 10×20. The orbit rounds of
`hyb0.9`, `alt2` and the switching schedules use the orbit set, so their cuts
in those rounds are presumably as short as `orbit`'s, but their corners differ
and this was not measured.

Two tests of this factor:

- *Within rules.* Across instances, the mean share of shorter steps in rounds
  0–4 does not correlate significantly with the loss after round 10 for any
  of the eight single-set rules of the table (Spearman between −0.14 and
  +0.15, all p ≥ 0.3, on 6×8 for all eight and on 10×20 for `orbit`,
  `pertE0.1`, `geo`; `logs/summary_mech2_6x8.log`,
  `logs/summary_mech_10x20.log`). The share varies little between instances,
  so this test is weak. For `alt` the correlation is +0.35 (p = 0.006,
  uncorrected; Holm over the nine 6×8 rules p ≈ 0.06): instances with *more*
  shorter steps lose *less*, the opposite of the hypothesis. For `alt` the
  share also measures how many of the cuts of rounds 0–4 come from its orbit
  rounds, so this does not cleanly test the factor either.
- *Intervention* (runs of this revision, all 220 instances, 20 rounds;
  `code/run_rev1.sh`, `code/run_rev1b.sh`, records `logs/rev1/`). Rule `maj2`
  takes, per term, the orbit set if its step is at least SCIP's on more than
  half of the rays where either step is finite, else SCIP's set; it takes the
  orbit set for 22%, 27%, 29% and 32% of the cuts (4×4 to 10×20). The control
  `rnd0.33` takes the orbit set for a pseudo-random third of the terms
  (33% of the cuts). If shorter sets cause the loss, `maj2` should not lose
  and `rnd0.33` should lose about a third of the orbit rule's loss. Pooled
  after round 10: `maj2` 0.000 [−0.003, +0.003], `rnd0.33` −0.0025
  [−0.0055, +0.0004] (21% of the orbit rule's loss), and `maj2 − rnd0.33`
  +0.003 [−0.002, +0.007] (after round 20: +0.003 [−0.001, +0.007]). By size
  `maj2 − rnd0.33` after round 10 is +0.007 [+0.001, +0.013] on 4×4, 0.000 on
  6×8, +0.006 [−0.001, +0.012] on 8×12 and −0.002 [−0.016, +0.011] on 10×20,
  the size with the largest reversal. Neither rule differs significantly
  from SCIP's rule in any size. The direction agrees with the hypothesis in
  three sizes, but the test does not have the power to confirm it.

Status: **heuristic** hypothesis consistent with the between-rule data, not
confirmed by the within-rule or the intervention test.

### 3.7 Explanation of the reversal (summary, revised after review round 3)

1. On 6×8, and on SCIP's 10×20 states after the root, an orbit round from the
   same state is on average at least as good as a SCIP round (3.1); on 10×20
   it is slightly worse at the root and on some orbit-trajectory states.
2. The loss is a state effect created in rounds 0–4, including the root round
   (3.5). Orbit trajectories reach states with lower corner potential and more
   near-zero reduced costs, from which every rule progresses more slowly
   (3.2, significant in some cells on 6×8, weaker on 10×20). The controlled
   recovery contrasts give limited evidence for gains from later SCIP
   rounds over continued orbit rounds, with no established repair difference
   between sizes (3.5).
3. Bound attainment and the resulting dual degeneracy (Proposition 7, proved,
   and the tie counts) are real for `orbit`, but rules without them lose
   about as much, and the degeneracy feature does not predict the per-instance
   loss; they are at most a contributing factor (3.3).
4. Every losing rule measured that uses one non-SCIP set in every round
   (eight rules on 6×8, three of them also on 10×20) picks sets that are
   shorter than SCIP's set on most rays, and the three non-losing selection
   rules measured do not; several losing rules (`pert0.01`, `pert1`,
   `hyb0.9`, `alt2`, the switching schedules) were not measured. This is the
   best candidate factor, but the direct tests do not confirm it (3.6).

So the reversal is explained as a state effect of early non-SCIP rounds; why
the orbit-family states are worse is only partly identified.

## 4. Alternative multi-round rules

Pooled over 220 instances, difference to SCIP's rule (mean [95% t-interval];
"AUC" is the mean of the fraction closed over rounds 1–10, which rewards
early progress; Holm-adjusted p-values over the 14 rules other than `scip` run on every size in the main runs;
`logs/summary_pooled.log`):

| Rule | r1 | r3 | r10 | r20 | AUC r1–10 | Holm p (r10 / AUC) |
|---|---|---|---|---|---|---|
| `orbit` | −0.001 [−0.016, +0.014] | −0.011 [−0.019, −0.003] | −0.012 [−0.017, −0.006] | −0.012 [−0.017, −0.006] | −0.011 [−0.016, −0.005] | 0.0008 / 0.003 |
| `pert0.1` | −0.009 | −0.010 [−0.017, −0.003] | −0.014 [−0.020, −0.007] | −0.013 | −0.011 | 0.0003 / 0.001 |
| `pertE0.1` | −0.005 | −0.010 [−0.017, −0.003] | −0.008 [−0.013, −0.003] | −0.008 | −0.008 | 0.016 / 0.006 |
| `geo` | −0.068 [−0.085, −0.050] | −0.017 | −0.009 [−0.014, −0.004] | −0.009 | −0.018 | 0.003 / 4e-10 |
| `alt2` | 0 | −0.003 | −0.004 [−0.008, −0.000] | −0.004 | −0.002 | 0.33 / 0.35 |
| `hyb0.9` | +0.018 [+0.009, +0.027] | +0.002 | −0.004 [−0.008, −0.000] | −0.004 | −0.000 | 0.25 / 0.95 |
| `hyb0.5` | +0.002 | +0.002 | +0.000 [−0.003, +0.003] | −0.001 | +0.001 | 1 / 0.35 |
| `both` | +0.030 [+0.021, +0.039] | +0.005 [+0.001, +0.010] | −0.003 [−0.006, +0.001] | −0.003 | +0.005 [+0.001, +0.008] | 0.78 / 0.053 |
| `oracle_seq` | +0.036 [+0.026, +0.046] | +0.008 [+0.003, +0.014] | +0.001 [−0.003, +0.004] | −0.001 | +0.008 [+0.004, +0.012] | 1 / 0.001 |
| `eff` | +0.000 | +0.004 [+0.000, +0.008] | +0.003 [−0.000, +0.006] | +0.003 [−0.001, +0.006] | +0.004 [+0.001, +0.006] | 0.33 / 0.025 |
| `sumstep` | +0.003 | +0.006 [+0.001, +0.010] | +0.002 [−0.002, +0.005] | +0.001 | +0.003 [+0.001, +0.006] | 0.79 / 0.053 |
| `eff2` | +0.002 [−0.000, +0.005] | +0.003 [+0.000, +0.005] | +0.002 [−0.001, +0.005] | +0.002 [−0.001, +0.005] | +0.003 [+0.001, +0.005] | 0.78 / 0.065 |
| `corner` | −0.219 | −0.379 | −0.422 | −0.427 | −0.383 | ≈ 0 |

Rules run for the revision after review round 1 (`logs/summary_rev1.log`;
not in the Holm family above; Holm over these three rules after round 10:
p = 0.029, 0.19 and 0.99):

| Rule | r1 | r3 | r10 | r20 | raw p r10 |
|---|---|---|---|---|---|
| `o1s` (= `first_orbit`) | −0.001 | −0.008 [−0.015, −0.002] | −0.006 [−0.011, −0.002] | −0.006 [−0.011, −0.001] | 0.010 |
| `maj2` | −0.006 [−0.015, +0.003] | +0.000 | +0.000 [−0.003, +0.003] | +0.0005 [−0.003, +0.004] | 0.99 |
| `rnd0.33` | +0.005 [−0.004, +0.015] | −0.001 | −0.0025 [−0.0055, +0.0004] | −0.002 [−0.006, +0.001] | 0.095 |

By size (difference to SCIP after round 10, `logs/summary_key_*.log`):

| Rule | 4×4 | 6×8 | 8×12 | 10×20 |
|---|---|---|---|---|
| `eff` | +0.005 [−0.002, +0.013] | +0.003 [−0.003, +0.008] | +0.003 [−0.002, +0.007] | +0.001 [−0.006, +0.008] |
| `eff2` | +0.004 [−0.001, +0.010] | +0.001 [−0.003, +0.005] | +0.005 [+0.001, +0.009] | −0.002 [−0.011, +0.006] |
| `sumstep` | +0.005 | +0.002 | +0.003 | −0.002 |
| `depth` | +0.004 | +0.004 | – | – |
| `oracle_seq` | −0.001 | +0.004 | +0.002 | −0.002 |
| `oracle` | −0.003 | +0.004 | – | – |
| `both` | +0.002 | −0.002 | −0.004 | −0.007 |
| `bothpert` | +0.001 | +0.001 | – | – |
| `pertE0.1` | −0.007 | −0.010 | −0.003 | −0.012 |
| `geo` | −0.000 | −0.015 | −0.004 | −0.017 |
| `lex0.1` | −0.001 | −0.009 | – | – |
| `alt` / `alt2` | −0.004 / −0.001 | −0.009 / −0.001 | – / +0.001 | – / −0.014 |
| `hyb0.5` | +0.002 | −0.001 | +0.001 | −0.002 |

Findings (**numerical evidence** on this generator):

1. **No rule that chooses the set by a bound for one objective direction
   beats SCIP's rule over 10–20 rounds.** Perturbing the reduced costs
   (`pertD`, `pertED`), using geometry instead (`geo`, `lex0.1`), or
   alternating (`alt`, `alt2`) reduces the loss of the orbit rule in some
   sizes but never turns it into a gain. `geo` (largest smallest Euclidean
   step) is also clearly worse in round 1 (−0.068).
2. **The LP-gain oracle wins early, not late.** `oracle_seq` (the candidate
   with the best LP value after re-solving, given the cuts already chosen) is
   ahead by 0.036 after round 1 and 0.008 after round 3, but even after round
   10, even this oracle is no better than SCIP's rule. Greedy one-round
   optimality, even measured exactly, does not give a better multi-round loop;
   this is the same lesson as the reversal itself.
3. **Two cuts per term** (`both`, `bothpert`) help early (+0.030 after round
   1) at twice the cuts, and the advantage disappears by round 10.
4. **Selection by efficacy is never significantly worse than SCIP's rule**
   at rounds 3, 10 or 20 in any size, and it has the largest pooled gain after
   round 10 among the 14 rules run on every size (`eff`: +0.003 after round 10, +0.004 AUC, Holm p = 0.025 for
   AUC; after round 10 alone the gain is not significant, Holm p = 0.33).
   `eff` was the best of the 14 rules, identified after seeing the data, so
   even its AUC gain should be confirmed on fresh instances. (`oracle_seq`, `sumstep` and `hyb0.5` are also never significantly
   worse in any size, but `oracle_seq` and `hyb0.5` have no late gain.) Its choices are mostly SCIP's set (60–70% of terms in
   every round bucket on 6×8, `logs/summary_choice_6x8.log`); it switches to an
   orbit-type set when that cut is farther from the vertex in Euclidean terms,
   so its sets are rarely shorter than SCIP's along most rays (Section 3.6).
   `depth` and `sumstep` behave alike. The cheap version `eff2` (choose
   between SCIP's set and the best orbit set by efficacy) has **no
   demonstrated gain**: +0.002 [−0.001, +0.005] after round 10 (Holm
   p = 0.78), +0.003 in AUC (Holm p = 0.065), and −0.002 [−0.011, +0.006] on
   10×20. It is only never measurably worse than SCIP's rule. (The first
   version said that `eff2` keeps "about 70% of the benefit" of `eff`; that is
   a ratio of non-significant means and is withdrawn.) It costs a fifth to a
   half of the run time of `eff` in this Python implementation. `maj2`
   (Section 3.6) is likewise never significantly different from SCIP's rule.
5. `hyb0.9` (use the orbit set only where SCIP's set is more than 10% below
   the corner bound) is good in round 1 (+0.018) and then falls behind, like
   the orbit rule; `hyb0.5` is indistinguishable from SCIP's rule.

**Recommended rule (revised after review round 3).** Keep SCIP's set. Do not
replace it by the bound-optimal set, neither in every round nor at the root
only: one orbit round at the root already costs about half of the orbit
rule's loss (`o1s`, pooled −0.006 [−0.011, −0.002] after round 10; Section
3.5). Later SCIP rounds have limited numerical evidence of a gain over
continued orbit rounds for some schedules, but that comparison does not
establish a gain over SCIP throughout or a repair difference between sizes;
its pooled `o3s` result is sensitive to the multiplicity family (Section 3.5).
If a second candidate set is computed anyway, keeping per term the cut
with the larger efficacy (`eff2`, or `eff` with a pool of five sets) was never
measurably worse than SCIP's rule in any size, but has no demonstrated gain
(only `eff`'s AUC gain of +0.004 is Holm-significant, and it was selected
post hoc). This is a robustness statement ("does not suffer the reversal on
this generator"), not a claim of an improvement. The first version's
recommendation of `eff2` as a cheap source of gain, and its statement that an
orbit round at the root is harmless, are withdrawn.

In SCIP 10 the default (hybrid) cut selector scores
cuts by efficacy with weight 1.0, objective parallelism 0.1 and integral
support 0.1, with a minimum orthogonality of 0.9
(`scip/src/scip/cutsel_hybrid.c`, `DEFAULT_*WEIGHT`), so the natural implementation is to generate both cuts and let the
cut selector choose, which is close to `eff2` (but with `both`-style
duplicates when both are kept; `both` loses slightly after round 10).

Cost (median seconds per instance run of 20 rounds, shared machine, rough):
SCIP 0.1–0.9 s, `eff2` 0.4–4.8 s, `eff` 1.0–9.5 s, `oracle_seq` 0.7–10.7 s.
The orbit bisection (25 small SDPs per term and round) dominates.

## 5. Convergence of the root loop (OQ3)

OQ3 of the scout report asks whether the loop "optimal LP vertex → one
intersection cut from a maximal quadratic-free set (simplicial cone) →
re-solve" converges to `min{c^T x : x ∈ conv(P ∩ S)}`, (i) for SCIP's rule,
(ii) for the bound-optimal rule, (iii) for every rule. This section gives a
sufficient condition (Theorem 2), shows that SCIP's rule and two perturbed
rules satisfy its depth part while the bound-optimal rule does not
(Lemma 4, Proposition 5), and answers (iii) negatively (Proposition 6). (i)
and (ii) remain open in general.

### 5.1 Setting

*Setting L.* `P = {x ∈ R^n : Ax ≤ b}` is a polytope contained in the box
`[−B, B]^n`. For each term `e` (from a finite set `E`) with pairwise distinct
indices `(i, j, k)` (bilinear terms, no squares `x_k = x_i^2`; the generator
of Section 1.1 draws distinct pairs), `S_e = {x : x_k = x_i x_j}`. Theorem 2 and
Corollary 3 do not use distinctness; Lemma 4 does. Let `F = P ∩ ⋂_e S_e`, assumed
nonempty, and `z* = min{c^T x : x ∈ F}` (attained; it equals the minimum over
`conv F` because the objective is linear). Put `P_0 = P`. In round `r`, let
`x^r` be an optimal basic solution of `min{c^T x : x ∈ P_r}` with an optimal
basis; the basis defines the cone `K_r = x^r + cone{r^r_1, …, r^r_n}` (the
`n` tight rows of the basis), so `P_r ⊆ K_r`. If `x^r ∈ F` the loop stops.
Otherwise, for **every** term `e` with `x^r ∉ S_e`, let `S'_e` be the side that
`x^r` violates (`S'_e = {x_k ≤ x_i x_j}` if `x^r_k > x^r_i x^r_j`, else
`{x_k ≥ x_i x_j}`), choose a closed convex `C` with `x^r ∈ int C` and
`int C ∩ S'_e = ∅`, and add its intersection cut
`Σ_j λ_j/α_j ≥ 1` with respect to `K_r` (notation of the sfree note,
Section 1). `P_{r+1}` is `P_r` intersected with all cuts of round `r`.

Each cut is valid for `K_r ∩ S'_e ⊇ P_r ∩ S_e ⊇ P_r ∩ F` (sfree note,
Section 1), so `F ⊆ P_r` for all `r` by induction, and `c^T x^r` is
nondecreasing and at most `z*`. Because `F ⊆ K_r ∩ S'_e`, at least one step
`α_j` is finite.

*Relation to OQ3.* OQ3 is stated for a loop that adds **one** intersection cut
per round, for a general `S = {q ≤ 0}`. Setting L instead adds a cut for
**every** violated bilinear term, and the proof of Theorem 2 uses this (round
`r_k` must cut the term that is violated at the accumulation point). So Theorem
2 and Corollary 3 are statements about this multi-cut loop; Remark 3a below
transfers them to a one-cut loop that cuts a most violated term. Proposition 6
has a single term, so there the two loops coincide; it is also a counterexample
for `S = {w ≤ xy}` alone, because the optimal value is the same for
`w = xy` and for `w ≤ xy` (the minimum of `εx + y + w` over `w ≤ xy`, `w ≥ 1`
is attained with `w = 1` and `xy ≥ 1`).

For a cut `H = {Σ_j λ_j/α_j ≥ 1}` at round `r` define

- its **depth** `d = dist(x^r, K_r ∩ H)` (Euclidean);
- its **smallest Euclidean step** `δ = min{α_j ‖r_j‖ : α_j < ∞}`;
- the **pointedness** of the cone `γ_r = dist(0, conv{r_j/‖r_j‖ : j})`
  (`γ_r > 0` because `K_r` is pointed; `γ_r` is small when the cone is flat).

### 5.2 A sufficient condition

**Lemma 1.** `d ≥ γ_r δ`.

*Proof.* Let `y = x^r + Σ_j λ_j r_j ∈ K_r ∩ H`, `λ ≥ 0`. Put
`μ_j = λ_j ‖r_j‖` and `u_j = r_j/‖r_j‖`. Then
`‖y − x^r‖ = ‖Σ_j μ_j u_j‖ = (Σ_j μ_j) ‖Σ_j (μ_j/Σ_i μ_i) u_j‖ ≥ γ_r Σ_j μ_j`,
and `1 ≤ Σ_{j : α_j < ∞} λ_j/α_j = Σ_{j : α_j < ∞} μ_j/(α_j‖r_j‖) ≤ Σ_j μ_j / δ`.
So `‖y − x^r‖ ≥ γ_r δ`. ∎

**Theorem 2 (convergence under uniform depth).** In Setting L, suppose there
is a function `η : (0, ∞) → (0, ∞)` such that every cut added at a round `r`
for a term `e` with `dist(x^r, S_e) ≥ ε` has depth at least `η(ε)`. Then
either the loop stops with an optimal `x^r ∈ F`, or `c^T x^r → z*` and every
accumulation point of `(x^r)` lies in `F` and is optimal.

*Proof.* If the loop stops, `x^r ∈ F` and `c^T x^r ≤ z*`, so `x^r` is
optimal. Otherwise `(x^r)` lies in the compact set `P`. Let `x̂` be an
accumulation point, `x^{r_k} → x̂`, and suppose `x̂ ∉ S_e` for some `e`. Put
`ε = dist(x̂, S_e)/2 > 0` (`S_e` is closed). For large `k`,
`dist(x^{r_k}, S_e) ≥ ε`, so round `r_k` adds a cut `H_k` for `e` of depth at
least `η(ε)`. For `m > k`,
`x^{r_m} ∈ P_{r_m} ⊆ P_{r_k + 1} ⊆ P_{r_k} ∩ H_k ⊆ K_{r_k} ∩ H_k`, hence
`‖x^{r_m} − x^{r_k}‖ ≥ η(ε)`. This contradicts the convergence of
`(x^{r_k})`. So `x̂ ∈ ⋂_e S_e`, and `x̂ ∈ P` because `P` is closed: `x̂ ∈ F`.
The values `c^T x^r` are nondecreasing and bounded by `z*`, so they converge
to some `v ≤ z*`, and `c^T x̂ = v`. Since `x̂ ∈ F`, `v ≥ z*`. ∎

**Corollary 3.** If `γ_r ≥ γ_0 > 0` for all `r` and the rule satisfies
`δ ≥ η_0(ε)` whenever `dist(x^r, S_e) ≥ ε`, the conclusion of Theorem 2
holds (take `η = γ_0 η_0`, Lemma 1).

**Remark 3a (one cut per round).** Change Setting L so that round `r` adds the
cut of only one violated term `e_r`. The conclusion of Theorem 2 still holds if
(a) `e_r` maximizes `dist(x^r, S_e)` and the depth hypothesis of Theorem 2
holds; or (b) `e_r` maximizes the violation `q_e = |x^r_k − x^r_i x^r_j|`,
`γ_r ≥ γ_0 > 0`, and the rule satisfies `δ ≥ κ q_e` for the cut term with a
constant `κ > 0` (by Lemma 4 this holds for SCIP's rule and for idealized
θ-approximate `geo` and `pertED`).

*Proof.* In the proof of Theorem 2 replace "round `r_k` adds a cut for `e`" by
"round `r_k` adds a cut `H_k` for `e_{r_k}` of depth at least `η'`", where
`dist(x^{r_k}, S_e) ≥ ε`. In case (a), `dist(x^{r_k}, S_{e_{r_k}}) ≥ ε`, so
`η' = η(ε)`. In case (b), `q_{e_{r_k}} ≥ q_e ≥ dist(x^{r_k}, S_e) ≥ ε` by
Lemma 4(a), so `δ ≥ κε` and, by Lemma 1, `η' = γ_0 κ ε`. The rest of the proof
is unchanged: `x^{r_m} ∈ K_{r_k} ∩ H_k` for `m > k` gives
`‖x^{r_m} − x^{r_k}‖ ≥ η'`. ∎

If the term is chosen arbitrarily (for example, always the first violated term
in a fixed order), the argument does not apply, and I have no result.

All four statements are **proved**. They are elementary; I did not find
this exact statement for quadratic intersection cuts, but convergence
arguments of this type (a cut that removes a ball of fixed radius around a
point that stays infeasible) are standard in the cutting-plane literature
(for example the general theory of Eaves and Zangwill, SIAM J. Control 9,
1971, which I know only by its bibliographic record, see
[sources/MANIFEST.md](sources/MANIFEST.md)). No novelty is claimed.

### 5.3 Which rules are uniformly deep

For one term write `s = (x_i, x_j, x_k) = (x, y, w)`, `s̄` the projection of
`x^r`, and `q = |w̄ − x̄ȳ| > 0`. Projected rays `p_j` are coordinate
projections of `r_j`, so `‖p_j‖ ≤ ‖r_j‖`. Hence if `C ⊇ B(s̄, ρ)` in `s`-space,
then `α_j ≥ ρ/‖p_j‖ ≥ ρ/‖r_j‖` for every `j` with `p_j ≠ 0` (and `α_j = ∞` if
`p_j = 0`), so `δ ≥ ρ`.

**Lemma 4.** Assume `P ⊆ [−B, B]^n`.

(a) `q ≥ dist(x^r, S_e)`.

(b) *SCIP's set.* For side `+` (`S' = {w ≤ xy}`) put
`x̂(s) = ((x − y)/2, (w + 1)/2)` and `ŷ(s) = ((x + y)/2, (w − 1)/2)`, so
`‖x̂‖^2 − ‖ŷ‖^2 = w − xy`; for side `−` put `x̂ = ((x + y)/2, (1 − w)/2)`,
`ŷ = ((x − y)/2, (−1 − w)/2)`. SCIP's Case-4 set with the default
`λ = x̂(s̄)/‖x̂(s̄)‖` (as modeled by `scout_sfree.ms_set`, used by rule
`scip`) contains `B(s̄, ρ_S)` with
`ρ_S = q / (√2 (‖x̂(s̄)‖ + ‖ŷ(s̄)‖)) ≥ q / (2√2 L_B)`,
`L_B = (B^2 + (B + 1)^2/4)^{1/2}`.

(c) *Orbit set with `F^T = M(s̄)^{-1}`.* The sliced orbit set `C_F` of the
sfree note (Lemma 10) with `F^T = M(s̄)^{-1}` contains
`B(s̄, σ_min(M(s̄)))`, and `σ_min(M(s̄)) ≥ q/‖M(s̄)‖_F ≥ q/(3B^2 + 1)^{1/2}`.

(d) *Rules `geo` and `pertED`.* Suppose the rule returns an orbit set whose
value `min_j u_j α_j` is at least `θ` times the supremum over all orbit sets
(`0 < θ ≤ 1`). For `geo` (`u_j = ‖r_j‖`), `δ ≥ θ q/(3B^2 + 1)^{1/2}`. For
`pertED` with `D > 0` (`u_j = ‖r_j‖(ŵ_j + D)`, `0 ≤ ŵ_j ≤ 1`),
`δ ≥ θ D q / ((1 + D)(3B^2 + 1)^{1/2})`.

So by (a), SCIP's rule, `geo` and `pertED` satisfy `δ ≥ κ_B ε` whenever
`dist(x^r, S_e) ≥ ε`, with a constant `κ_B > 0` that depends only on `B`
(and on `θ`, `D`).

*Proof.* (a) The point obtained from `x^r` by replacing `x_k` with
`x_i x_j` lies in `S_e` and is at distance `q`.

(b) Side `+`. With `ψ = (u, v, w)`, the eigen-coordinates of
`q(s) = w − xy` are `v = (x − y)/2` (eigenvalue `+1/2` of `Q` after scaling),
`u = (x + y)/2` (eigenvalue `−1/2`) and the null direction `w` carrying the
linear term; the constant `κ` of Chmiela–Muñoz–Serrano is 0 here, so Case 4
with `r = f = 1` gives exactly the `x̂, ŷ` above (this is the computation in
`scout_sfree.ms_set`; the identity `‖x̂‖^2 − ‖ŷ‖^2 = w − xy` is checked
symbolically in `code/example_depth.py`). The set is
`C = {s : φ(ŷ(s)) ≤ λ^T x̂(s)}`, where `φ(y) = ‖y‖` or
`φ(y) = ((1 − ℓ^2)(‖y‖^2 − y_2^2))^{1/2} + ℓ y_2` with `ℓ = λ_2`; in the second
case Cauchy–Schwarz for the vectors `((1 − ℓ^2)^{1/2}, ℓ)` and
`((‖y‖^2 − y_2^2)^{1/2}, y_2)` gives `φ(y) ≤ ‖y‖`. Hence
`C ⊇ C_0 = {s : ‖ŷ(s)‖ ≤ λ^T x̂(s)}`. The maps `x̂, ŷ` are affine with linear
parts of norm at most `1/√2` (for example
`‖Δx̂‖^2 = ((Δx − Δy)^2 + Δw^2)/4 ≤ (2Δx^2 + 2Δy^2 + Δw^2)/4 ≤ ‖Δs‖^2/2`). Let
`a = ‖x̂(s̄)‖ = λ^T x̂(s̄)` and `b = ‖ŷ(s̄)‖`; `a^2 − b^2 = q > 0`. For
`‖s − s̄‖ ≤ t`: `λ^T x̂(s) ≥ a − t/√2` and `‖ŷ(s)‖ ≤ b + t/√2`, so `s ∈ C_0`
whenever `√2 t ≤ a − b = q/(a + b)`. On the box,
`‖x̂‖^2 ≤ (2B)^2/4 + (B + 1)^2/4 = L_B^2` and likewise `‖ŷ‖ ≤ L_B`. Side `−`
is the same computation with the stated `x̂, ŷ`.

(c) `M(s) = M(s̄) + M_0(s − s̄)`, where `M_0` is the linear part
(`M_0(Δs) = [[Δw, Δx], [Δy, 0]]` for side `+`, `[[Δx, Δw], [0, Δy]]` for
side `−`), so `‖M_0(Δs)‖_2 ≤ ‖M_0(Δs)‖_F = ‖Δs‖`. With `F^T = M(s̄)^{-1}`,
`F^T M(s) = I + M(s̄)^{-1} M_0(Δs)`, and
`‖M(s̄)^{-1} M_0(Δs)‖_2 ≤ ‖Δs‖/σ_min(M(s̄))`. If `‖Δs‖ ≤ σ_min(M(s̄))`,
the symmetric part of `F^T M(s)` is `⪰ 0`, so `s ∈ C_F`. The set is S'-free
by Lemma 10(3) of the sfree note because `det F = 1/det M(s̄) = 1/q > 0`.
Finally `σ_min σ_max = |det M(s̄)| = q` and `σ_max ≤ ‖M(s̄)‖_F =
(x̄^2 + ȳ^2 + w̄^2 + 1)^{1/2}`.

(d) By (c), the set `F_0 = M(s̄)^{-T}` has `α_j(F_0) ≥ ρ_A/‖r_j‖` with
`ρ_A = q/(3B^2 + 1)^{1/2}`. For `geo`, the supremum of `min_j ‖r_j‖ α_j` is
at least `ρ_A`, so the returned set has `δ = min_j ‖r_j‖α_j ≥ θ ρ_A`. For
`pertED`, the supremum of `min_j u_j α_j` is at least
`min_j (ŵ_j + D) ρ_A ≥ D ρ_A`; the returned set satisfies
`‖r_j‖ α_j = u_j α_j/(ŵ_j + D) ≥ θ D ρ_A/(1 + D)`. ∎

Status: **proved**. Numerical sanity check (not needed for the proof):
`code/check_inradius.py 3 400 50` tested 20000 random directions at random
points in `[−3, 3]^3`; the smallest ratio of SCIP's step to `ρ_S` was 1.415
(so (b) holds with room, probably by a factor `√2`), and the smallest ratio of
the `F_0` step to `σ_min` was 1.0005 (`logs/check_inradius.log`).

The implemented bisection (25 halvings of `[0, z_K(u)]`) returns a set whose
value is within `2^{-25} z_K(u)` of the supremum over family (A). This is a
`θ`-approximation with `θ` close to 1 whenever the supremum is not tiny
compared with `z_K(u)`; I did not prove a uniform `θ` for the implementation.

**Proposition 5 (bound-optimal sets are not uniformly deep).** Let
`S' = {(x, y, w) : w ≤ xy}`, `s̄ = (0, 0, 1)` (`q = 1`), rays
`r_1 = e_y`, `r_2 = e_x`, `r_3 = e_w` and reduced costs `c̄ = (1, ε, 1)`
(written `c̄` here because `w` is a coordinate),
`0 < ε ≤ 1`. Then `z_K = 2√ε`. Every closed convex S'-free `C` with
`s̄ ∈ int C` satisfies `α_1 α_2 ≤ 4`. If `C` is `θ`-bound-optimal
(`min_j c̄_j α_j ≥ θ z_K`), then `α_1 ≤ 2√ε/θ`, so `δ ≤ 2√ε/θ` and the depth
is at most `2√ε/θ`, while the violation stays `q = 1`. SCIP's set at `s̄` is
`{w ≥ (x + y)^2/4}` with steps `(2, 2, ∞)` for every `ε`.

*Proof.* The point `s̄ + λ_1 e_y + λ_2 e_x + λ_3 e_w = (λ_2, λ_1, 1 + λ_3)`
lies in `S'` iff `1 + λ_3 ≤ λ_1 λ_2`, so
`z_K = min{λ_1 + ελ_2 : λ_1 λ_2 ≥ 1} = 2√ε` (AM–GM, attained at
`(√ε, 1/√ε)`). Let `0 < t_1 ≤ α_1` and `0 < t_2 ≤ α_2` be finite. Because
`C` is closed and convex and contains `s̄`, the points `(0, t_1, 1)` and
`(t_2, 0, 1)` lie in `C`, hence so does their midpoint `m = (t_2/2, t_1/2, 1)`,
and for `0 < τ < 1` the point `(1 − τ)m + τ s̄ = ((1 − τ)t_2/2, (1 − τ)t_1/2, 1)`
lies in `int C` (`s̄ ∈ int C`). It lies in `S'` iff `(1 − τ)^2 t_1 t_2/4 ≥ 1`;
if `t_1 t_2 > 4`, some small `τ` gives a point of `int C ∩ S'`, a
contradiction. So `t_1 t_2 ≤ 4` for all such `t_1, t_2`; hence both steps are
finite and `α_1 α_2 ≤ 4`. If `α_1 ≥ θ z_K = 2θ√ε` and
`εα_2 ≥ 2θ√ε`, then `α_2 ≥ 2θ/√ε` and `α_1 ≤ 4/α_2 ≤ 2√ε/θ`. The depth is at
most `‖(s̄ + α_1 e_y) − s̄‖ = α_1` because that point lies in `K ∩ H`. SCIP's
set is computed in `code/example_depth.py` (symbolic). ∎

Status: **proved** (the numbers in `logs/example_depth.log` agree: the
implemented orbit rule gives `α_1 α_2 = 4.0000` and `α_1 = 2√ε` for
`ε = 1, …, 10^{-6}`, while `geo` keeps `α_1 = 2` and `pertE0.1` keeps
`α_1 ≥ 0.603`). This corner is the LP corner of
`min{y + εx + w : x, y ≥ 0, w ≥ 1}` at `(0, 0, 1)`.

So Corollary 3 covers SCIP's rule, `geo` and `pertED` when the cones stay
pointed, but not the bound-optimal rule. Proposition 5 does not show that the
bound-optimal loop fails; on that very corner it closes the gap in one round
(Section 5.4).

**The pointedness hypothesis is not met in practice.** In the 6×8 loops the
median `γ_r` falls from 0.117 at the root to 0.020 in rounds 3–5 and 0.001 in
rounds 11–19, for every rule (`logs/summary_diag_6x8.log`, table "Median
pointedness"); 10×20 is similar. So Corollary 3 explains nothing about the
observed loops. It is a sufficient condition, and Proposition 6 shows that its
depth part cannot be dropped even when the cones stay pointed.

### 5.4 The answer to OQ3 (iii) is no

**Proposition 6.** Let `0 < ε < 1`, `X ≥ 2/√ε`, `Y ≥ √ε`, `W > 1`, and
consider `min{εx + y + w : 0 ≤ x ≤ X, 0 ≤ y ≤ Y, 1 ≤ w ≤ W, w = xy}`, whose
optimal value is `z* = 1 + 2√ε` (at `(1/√ε, √ε, 1)`). For `a > 0` let
`C_a = {(x, y, w) : w ≥ (ax + y/a)^2/4}`. Then:

1. each `C_a` is a maximal `S'`-free set for `S' = {w ≤ xy}`, and it is the
   image of SCIP's set at `(0, 0, 1)` (Proposition 5) under the automorphism
   `(x, y, w) ↦ (x/a, ay, w)` of `S'`;
2. for every increasing sequence `0 = ξ_0 < ξ_1 < ξ_2 < …` with limit
   `ξ_∞ < 2/√ε`, the loop of Setting L that uses `C_{a_r}`,
   `a_r = 2/ξ_{r+1}`, in round `r` has the unique LP optimum
   `x^r = (ξ_r, 0, 1)` in every round. The LP values `1 + εξ_r` converge to
   `1 + εξ_∞ < z*`, and every `x^r` violates `w = xy` by exactly 1.

For example `ε = 1/4`, `ξ_r = 2(1 − 2^{-r})`: the values converge to
`3/2`, while `z* = 2`.

*Proof.* (1) `int C_a ∩ S' = ∅` because
`(ax + y/a)^2/4 − xy = (ax − y/a)^2/4 ≥ 0`. Maximality: by the automorphism
it suffices to take `a = 1`. In the coordinates `u = (x + y)/2`,
`v = (x − y)/2`, `C_1 = {w ≥ u^2}` and `S' = {w ≤ u^2 − v^2}`. Let `p ∉ C_1`,
so `w_p < u_p^2`. For `0 < τ < 1` take `c ∈ C_1` with `u_c = u_p`,
`v_c = −τ v_p/(1 − τ)`, `w_c = u_p^2 + η` (`η > 0` small, so `c ∈ int C_1`). The
point `z = (1 − τ)c + τp` has `u_z = u_p`, `v_z = 0` and
`w_z = (1 − τ)(u_p^2 + η) + τ w_p`, so
`u_z^2 − v_z^2 − w_z = τ(u_p^2 − w_p) − (1 − τ)η > 0` for small `η`. Thus `z`
lies in the interior of `S'`, and it lies in the interior of
`conv(C_1 ∪ {p})` (a convex combination with positive weight on an interior
point of the full-dimensional set `C_1`). So no convex set strictly containing
`C_1` is `S'`-free. The map `(x, y, w) ↦ (x/a, ay, w)` preserves `xy` and maps
`C_1` onto `C_a`.

(2) Induction on `r`; write `ξ = ξ_r`, `ξ' = ξ_{r+1}`, `a = 2/ξ'`.

*Round 0.* At `(0, 0, 1)` the tight rows are `x ≥ 0`, `y ≥ 0`, `w ≥ 1`; the
rays are `e_x, e_y, e_w` with reduced costs `ε, 1, 1 > 0`, so this is the
unique LP optimum. `C_a` contains `(0, 0, 1)` in its interior. Its steps are
`α_x = 2/a = ξ'`, `α_y = 2a = 4/ξ'`, `α_w = ∞`, so the cut is
`x/ξ' + ξ' y/4 ≥ 1`.

*Invariant for `r ≥ 1`.* `P_r` consists of the box, `w ≥ 1` and the cuts
`x/ξ_k + ξ_k y/4 ≥ 1` (`1 ≤ k ≤ r`), and `x^r = (ξ, 0, 1)` with tight rows
`y ≥ 0`, `w ≥ 1`, `x/ξ + ξy/4 ≥ 1`. The older cuts are slack at `x^r` because
`ξ/ξ_k > 1`, and the box rows are slack because `0 < ξ < X` and `W > 1`. The rays of the basis cone are
`e_x`, `r_1 = (−ξ^2/4, 1, 0)` and `e_w`, with reduced costs `ε`,
`1 − εξ^2/4` and `1`, all positive because `ξ < 2/√ε`. So `x^r` is the unique
LP optimum.

*Cut of round `r`.* `x^r ∈ int C_a` because `(aξ)^2/4 = (ξ/ξ')^2 < 1`. Along
`e_x`, `(a(ξ + t))^2/4 ≤ 1` iff `t ≤ ξ' − ξ`, so `α_x = ξ' − ξ`. Along `e_w`
the defining inequality only gets slacker, so `α_w = ∞`. Along `r_1`,
`C_a(x^r + t r_1) := 1 − (aξ(1 − ξt/4) + t/a)^2/4` factors as
`−(ξ − ξ')(ξ + ξ')(tξ − tξ' − 4)(tξ + tξ' − 4)/(16ξ'^2)`; it is a concave
quadratic in `t`, positive at `t = 0`, whose positive root is
`α_1 = 4/(ξ + ξ')`. In cone coordinates `λ_1 = y`,
`λ_x = x − ξ + ξ^2 y/4`, `λ_w = w − 1`, the cut
`λ_x/(ξ' − ξ) + λ_1(ξ + ξ')/4 ≥ 1` multiplies out to
`x/ξ' + ξ' y/4 ≥ 1`.

*Next vertex.* `x^{r+1} = (ξ', 0, 1)` satisfies all rows of `P_{r+1}`, its
tight rows are `y ≥ 0`, `w ≥ 1` and the new cut, and the invariant holds with
`ξ'` (reduced costs `ε`, `1 − εξ'^2/4`, `1`, positive because
`ξ' < ξ_∞ < 2/√ε`). Since `ξ_r < ξ_∞`, `εξ_∞ < 2√ε` gives the strict gap. ∎

Status: **proved**; the one-round algebra (steps, factorization, cut, reduced
costs) is also checked symbolically, and rounds 0–12 of the example
`ε = 1/4`, `ξ_r = 2(1 − 2^{-r})`, box `[0, 10]^2 × [1, 10]`, are checked in
exact rational arithmetic: LP optimality by strict dual feasibility of the
stated basis, primal feasibility of all rows, the three steps, and the new
cut (`code/oq3_example.py 12 60`, `logs/oq3_example.log`: "ALL ROUNDS
VERIFIED: True").

Remarks.

- The sets are maximal and come from SCIP's own construction under an
  automorphism of `S'`, so the answer to OQ3 (iii) ("does the loop converge for
  every rule choosing maximal quadratic-free sets?") is **no**. The adversary
  shrinks the step along the cheapest ray, `α_x = ξ_{r+1} − ξ_r → 0`, while the
  violation stays 1; the cones stay pointed (the rays `e_x`, `r_1`, `e_w` keep
  angles bounded away from `π`). So the failure is entirely a failure of the
  depth hypothesis of Theorem 2.
- On the same instance the natural rules converge (numerical, same log): the
  orbit rule reaches `z*` in one round (its cut is objective-parallel on the
  face spanned by `e_x, e_y` and the optimal face contains the feasible point);
  SCIP's rule and `geo` are within `10^{-6}` (relative) of `z*` by round 10,
  and `pertE0.1` within `3·10^{-6}` by round 5.
- The scout report expected that a negative answer would need a Zwart-type
  construction with flat cones. Proposition 6 needs no flat cones, because the
  rule is free to choose shallow maximal sets; I have not compared it with
  Zwart's examples in detail. For Tuy-type cuts (the unique
  maximal set of a reverse-convex constraint) the analogous question is
  different, because there the rule has no freedom.
- (i) and (ii) remain open. Theorem 2 reduces them to a depth bound along the
  loop; the obstruction is the pointedness of the basis cones, which the rule
  does not control.

## 6. Corrections to earlier notes

These are recorded here; the earlier notes are not edited.

1. *sfree note, Sections 9.1–9.2 and 11 (`core.corner_bound`).* The function
   returns an infeasible two-ray point, and hence an underestimate of `z_K`,
   when two projected rays are collinear (Section 1.3). Section 9.1's
   validation (77 random corners, no mismatch) did not contain such corners;
   on LP corners the error occurs in 13% of the corners checked against SCIP
   (55 of 420). Corrected numbers for the one-cut table are in Section 1.3. The
   statement "the best orbit set attained `z_K` in all 120 LP corners" stays
   true for the corrected `z_K`, but in 10 of those corners the old code
   compared with a wrong `z_K` and capped the orbit bisection there.
2. *sfree note, Section 9.3* (revised after review round 1). With the
   corrected cap of item 1, the orbit rule closes 0.904 instead of 0.887 after
   10 rounds on the 10 6×8 instances, but that change comes from one instance
   and is within the loop's instance-level noise (Section 1.3, item 2); on 220
   instances the bug has no measurable effect after round 10 (−0.001
   [−0.003, +0.002]). It does affect round 1: on the 12 4×4 instances the
   corrected orbit rule closes 0.891 after round 1 instead of 0.863
   (`logs/fid2_exploop_4x4.jsonl`), and on 220 instances the corrected rule is
   ahead of the bug-affected one by +0.011 [+0.004, +0.019] after round 1. The
   first version of this note attributed about 0.017 of the 0.044 gap to the
   bug; that attribution is withdrawn. The reversal is real (Section 2), and
   its cause is investigated in Section 3. In the larger
   sample the orbit rule does not win the first round on average; it ties
   (pooled −0.001 [−0.016, +0.014]) and loses later.
3. *sfree note, Section 9.4,* "for one cut, the orbit bisection is a strict
   improvement over SCIP's fixed set": true per cut and per round from the
   same state (Section 3.1 here), but not over several rounds (Section 2).

## 7. Comparison with the earlier notes and with prior work

- *Sfree note.* That note proved that the best single cut equals the corner
  bound and showed that the orbit family attains it on LP corners. This note
  does not change those results (apart from the correction in Section 6). It
  shows that "best single cut" is the wrong objective for a multi-round loop
  on these instances, shows that the loss is a state effect of early rounds
  (Section 3; the mechanism is only partly identified), and finds that the
  orbit sets should not replace SCIP's set; as an alternative candidate chosen
  by efficacy they do no measurable harm and bring no demonstrated gain.
- *Scout report, OQ3.* Theorem 2 and Lemma 4 give a conditional positive
  answer for SCIP's rule and for perturbed rules; Proposition 5 shows why the
  same argument fails for the bound-optimal rule; Proposition 6 answers (iii)
  negatively. The scout report's observation that 11 small instances all
  converged is consistent with Proposition 6, which needs an adversarial set
  choice.
- *Cut selection in MIP.* That greedy single-round cut quality is a poor
  predictor of multi-round performance, and that objective-parallel cuts
  create dual degeneracy and stalling, is well known for Gomory cuts (Zanette,
  Fischetti and Balas 2011, known to me only from its abstract; the survey of
  Dey and Molinaro, arXiv:1805.02782, discusses cut selection in general). The
  specific facts here, for intersection cuts from maximal quadratic-free sets
  for bilinear terms, are: the bound-attaining set produces dual degenerate
  corner LPs (Proposition 7, plus the tie counts), which however is not the
  main cause of the loss (Section 3.3); the damage is created in rounds 0–4,
  including the root round (Section 3.5); and efficacy selection among a few
  maximal sets does not suffer it. I did not find these statements in the sources I
  checked; the search was short, so this is not a novelty claim.
- *Convergence of concavity/Tuy cuts.* Muu (Kybernetika 1985, saved in
  `sources/`) states that the convergence of pure Tuy-cut methods for
  reverse convex constraints was open and combines the cuts with branch and
  bound; the scout report found no later resolution. Proposition 6 is about a
  different situation (a bilinear equation and a free choice among many
  maximal sets), so it does not settle that question. Theorem 2 is a standard
  type of argument (Section 5.2).

## 8. Checks actually run

All are targeted local checks of this stream; no project-wide verification
was run and CI was not consulted. Commands run from `code/` unless stated,
with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`.
Python 3 (miniconda), numpy, scipy, sympy, highspy, Clarabel 0.11.1, cvxpy
1.9.3, PySCIPOpt 6.2.1 (SCIP 10). The large diagnostic records are stored
gzip-compressed (`logs/diag/*.jsonl.gz` except `swappot_6x8.jsonl`, and
`logs/fid_exploop_*.jsonl.gz`). Since the revision after review round 1 the
analysis scripts read `.jsonl` and `.jsonl.gz` files directly (`code/recio.py`)
and stop with an error if a pattern matches no file. Items 1–11 were run by the interrupted
earlier author run on 2026-10-01/02; I checked that their outputs are complete
and consistent with the final code (items 12, 22) instead of rerunning them.

1. `python3 exp_loop.py 21 30 8 …/logs/repro_exp_loop_small.json` and
   `python3 exp_loop.py 22 30 10 …/logs/repro_exp_loop_big.json 6 8 4` (in
   `research-20260928b/sfree/code`), then `python3 compare_repro.py`: maximum
   difference 0 to the sfree note's records (`logs/compare_repro.log`).
2. `python3 check_fastorbit.py 5 6`: Clarabel bisection vs the cvxpy original
   on 8 corners, maximum relative certificate difference `1.7e-8`, coefficient
   difference `5.3e-6`.
3. `python3 check_zk.py 1 300`: 347 corners, 10 disagreements, the `core`
   point infeasible in all 10 (`logs/check_zk.log`).
4. `python3 check_zk_scip.py 101 25`: 420 corners against SCIP global solves
   (Section 1.3; `logs/check_zk_scip.log`).
5. `python3 gen_instances.py 4 4 3 1001 60 400 120 ../data/inst_4x4.json`
   and likewise `6 8 4 1002`, `8 12 5 1003`, `10 20 6 1004` (60 kept each, no
   SCIP failures; `logs/gen_*.log`); `gen_instances.py 6 8 4 22 100 30 60` and
   `4 4 3 21 100 30 60` for the `exp_loop` instances (10 and 12 kept).
6. `python3 recheck_mccormick.py 11 150 4 4 3 …exp_mccormick_11_final.json`
   and `12 200 6 8 4 …exp_mccormick_12_big_final.json` (final code with the SDP
   fallback): Section 1.3 numbers (`logs/recheck_mccormick_1*.log`).
7. `python3 example_depth.py`: Proposition 5 numbers (`logs/example_depth.log`).
8. `python3 check_inradius.py 3 400 50`: minimum ratios 1.415 and 1.0005
   (claims ≥ 1; `logs/check_inradius.log`).
9. Main runs: `sh run_main.sh 3` (first chunks), then
   `sh run_queue.sh jobs_main.txt MAXP` for the rest: 3840 records
   (4×4 and 6×8: 60 instances × 22 rules; 8×12 and 10×20: 50 × 12), no LP
   failures, no tracebacks (`logs/main/`).
10. `sh run_diag.sh 1`: diagnostic runs, 6×8 (60 instances) and 10×20 (30),
    5 rules (`logs/diag/diag_*.jsonl`).
11. `sh run_extra.sh`: `swapgamma_6x8.jsonl` (60 × 2 rules) and
    `choice_6x8.jsonl` (30 × 3 rules).
12. Validity of the stored runs: `python3 check_consistency.py` compares every
    trajectory stored more than once across `logs/main`, `logs/diag`,
    `logs/new` (made with different code versions): 0 differences
    (final count in item 22). In addition, a rerun of 8×12 instances 0–1 with
    the final code reproduced the main records of `scip`, `orbit`, `eff`
    exactly (smoke test of the new rules).
13. `timeout 10800 sh run_new.sh 4` (new rules `o2s, o3s, o5s, s1o, s3o, s5o,
    eff2, hyb0.9, hyb0.5` on 6×8 and 10×20; `eff2, hyb0.9, hyb0.5` on 4×4 and
    8×12; each job limited to 2 h): 30 jobs, all exit code 0, 1320 records
    (`logs/new/`, `logs/new/done.txt`).
14. `python3 analyze_key.py SIZE` for the four sizes
    (`logs/summary_key_*.log`), `python3 analyze_main.py …` for the four sizes
    (`logs/summary_main_*.log`), `python3 analyze_pooled.py`
    (`logs/summary_pooled.log`).
15. `python3 analyze_diag.py '../logs/diag/diag_6x8_*.jsonl'`
    (`logs/summary_diag_6x8.log`), `python3 analyze_state.py` for 6×8 and
    10×20 (`logs/summary_state_*.log`), `python3 analyze_ties.py` for both
    (`logs/summary_ties_*.log`), `python3 analyze_percase.py … 10` for both
    (`logs/summary_percase_*.log`),
    `python3 analyze_swapgamma.py` (`logs/summary_swapgamma_6x8.log`),
    `python3 analyze_choice.py` (`logs/summary_choice_6x8.log`).
16. `python3 summarize_zk_scip.py` (`logs/summarize_zk_scip.log`) and
    `timeout 3600 python3 support_stats.py 4x4 6x8 8x12 10x20`
    (`logs/support_stats.log`).
17. `timeout 1200 python3 oq3_example.py 12 60`: symbolic one-round algebra,
    exact rounds 0–12 "ALL ROUNDS VERIFIED: True", and the natural rules on the
    same instance (`logs/oq3_example.log`).
18. `timeout 3000 python3 mrloop.py ../data/inst_exploop_6x8.json
    scip,orbit_core,orbit,orbitB,corner 10 ../logs/fid2_exploop_6x8.jsonl 0 10`
    and the 4×4 analogue (8 rounds, 12 instances): final-code fidelity runs
    (`logs/fid2_exploop_*`).
19. `timeout 5400 python3 mrloop.py ../data/inst_6x8.json scip,orbit 20
    ../logs/diag/swappot_6x8.jsonl 0 60 swappot` and
    `python3 analyze_swappot.py '../logs/diag/swappot_6x8.jsonl'`
    (`logs/summary_swappot_6x8.log`; Section 3.2).
20. `sha256sum sources/kybernetika1985_reverse_convex.pdf`: matches the
    manifest.
21. `grep DEFAULT_ scip/src/scip/cutsel_hybrid.c` in the read-only SCIP
    10.0.3 source: cut selector weights quoted in Section 4.
22. (final) `python3 check_consistency.py` after all runs: "pairs of
    duplicate trajectories compared: 780, differing: 0".

Checks of the revision after review round 1 (2026-10-02; code changes:
`code/recio.py` and its use in the analysis scripts; rules `maj2` and `rndP`
and a per-set cut counter in `code/mrloop.py`, which leave the existing rules
unchanged, see item 25; new scripts `code/analyze_rev1.py`,
`code/analyze_mech.py`, `code/check_clip.py`, `code/run_rev1.sh`,
`code/run_rev1b.sh`):

23. `timeout 7000 sh run_rev1.sh 3`: `first_orbit,maj2` on 8×12 and 10×20 and
    `maj2` on 4×4 and 6×8, 20 rounds, 13 jobs, all exit code 0
    (`logs/rev1/done.txt`), no tracebacks. A first launch with 4 processes was
    stopped after about a minute to keep one slot free for analyses; its partial
    files were deleted and its processes killed before the relaunch.
24. `sh run_rev1b.sh 3` (started by a waiting wrapper under `timeout 7000`):
    `rnd0.33` on all four sizes, 6 jobs, all exit code 0
    (`logs/rev1/done_b.txt`).
25. `timeout 1800 python3 mrloop.py ../data/inst_6x8.json
    scip,orbit,first_orbit,eff2,s1o 20 ../logs/rev1/smoke_6x8.jsonl 0 6` with
    the final code, then `timeout 900 python3 check_consistency.py` (now also
    reading `logs/rev1`): "pairs of duplicate trajectories compared: 810,
    differing: 0" (`logs/check_consistency_rev1.log`). So the code changes of
    the revision did not change the existing rules.
26. `timeout 600 python3 analyze_rev1.py` (`logs/summary_rev1.log`): the M1
    statistics (Section 1.3), the switching table (Section 3.5), `maj2` and
    `rnd0.33` (Sections 3.6, 4).
27. `timeout 900 python3 analyze_mech.py '../logs/diag/[cd]*_6x8*.jsonl' 10`
    and `… '../logs/diag/diag_10x20*.jsonl' 10` (`logs/summary_mech_*.log`):
    ties, `z_C/z_K`, step shortness and tilt for every diagnosed rule, and
    per-instance correlations (Sections 3.3, 3.6).
28. `timeout 600 python3 check_clip.py` (`logs/check_clip.log`): 52347 round
    states, LP value above `z_bil` in 3728, maximum excess `6.9e-7` relative
    and `2.1e-4` of the root gap (Section 1.1).
29. Reruns of the analysis scripts on the compressed records, outputs compared
    with the stored logs by `diff`: `analyze_diag.py` (6×8), `analyze_state.py`,
    `analyze_ties.py`, `analyze_percase.py … 10` (6×8 and 10×20),
    `analyze_swappot.py`, `analyze_swapgamma.py`, `analyze_choice.py`,
    `analyze_pooled.py`, `analyze_key.py` (four sizes): all 15 outputs
    identical to the stored logs.
30. `timeout 1200 python3 oq3_example.py 12 60`: output identical to
    `logs/oq3_example.log` ("ALL ROUNDS VERIFIED: True");
    `timeout 600 python3 example_depth.py`: output identical to
    `logs/example_depth.log`.

Checks of the revision after review round 2 (2026-10-02; code changes: new
`code/analyze_rev2.py` and `code/run_rev2.sh`; `code/analyze_mech.py` now
prints the label of its last block and leaves out rules whose feature is
constant; `code/check_consistency.py` also reads `logs/rev2`; `mrloop.py` is
unchanged):

31. `timeout 600 python3 analyze_rev2.py` (`logs/summary_rev2.log`): changes
    of the deficits of `o1s`, `o2s`, `o3s`, `o5s` and `orbit` over rounds
    3–20, 5–20 and 10–20 on 6×8 and 10×20 and pooled (Section 3.5, recovery
    table).
32. `timeout 6000 sh run_rev2.sh 3` (each of the 6 jobs under `timeout
    5400`): diag records for `pert0.1, pertE1, lex0.1, orbit_core, orbitB,
    alt` on the 60 6×8 instances, 20 rounds; all 6 jobs exit code 0
    (`logs/rev2/done.txt`), 360 records, about 17 minutes; then
    `gzip -9 logs/rev2/diag2_6x8_*.jsonl`.
33. `timeout 900 python3 check_consistency.py` (now also reading
    `logs/rev2`): "pairs of duplicate trajectories compared: 1170, differing:
    0" (`logs/check_consistency_rev2.log`). The 360 new pairs are the new
    diag trajectories against the main runs, so the diag records describe the
    same trajectories as the loss statistics.
34. `timeout 900 python3 analyze_mech.py '../logs/[dr]*/diag*_6x8_*.jsonl' 10`
    (`logs/summary_mech2_6x8.log`; reads the old diag records and the new
    ones): the extended table of Section 3.6 and the within-rule correlations
    of the six new rules. Rerun after compressing the new records: identical
    output.
35. `timeout 900 python3 analyze_mech.py '../logs/diag/[cd]*_6x8*.jsonl' 10`
    and `… '../logs/diag/diag_10x20*.jsonl' 10` with the patched script,
    compared with the stored logs by `diff`: only the last block differs (the
    new label line and rule lists; on 10×20 the pooled `tie2` value is now
    +0.153 over `orbit` and `pertE0.1` instead of `+nan`, because `geo` has no
    ties on 10×20). The stored `logs/summary_mech_*.log` were replaced by
    these outputs.

Checks of the revision after review round 3 (2026-10-03; new analysis
`code/analyze_rev3.py`, existing records only). Both commands used
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`:

36. From `code/`: `timeout 300 python3 analyze_rev3.py >
    ../logs/summary_rev3.log`. Exit 0, ALL PASS: 54 files, 3180 records;
    matched sets of 60 6×8 and 50 10×20 instances for all six rules; finite
    21-state trajectories. Computes the paired control contrasts against
    orbit throughout over spans 3–20, 5–20 and 10–20, and Holm adjustments
    over each span's 12 tests and all 36 tests (Section 3.5). It checks any
    duplicate selected trajectory for exact equality; none occurs in these
    inputs.
37. From `reviews/r3-scripts/`: `timeout 120 python3 indep_rev2.py >
    ../../logs/indep_rev3_confirmation.log`. Exit 0; the unchanged independent
    reviewer script reproduces all 12 control contrasts over 3–20 and the
    original deficit table. Its diagnostic comparison finds 660 trajectory
    pairs and 0 differences. This is a rerun of existing reviewer code,
    not a new independent review of the revision.
38. From the repository root: inline `timeout 60 python3` comparison of
    the two logs. All 12 control contrasts over 3–20 match the reviewer
    output at its printed precision (`logs/check_rev3_comparison.log`).
    A separate inline `timeout 60 python3` syntax check using `compile()`
    passes for `code/analyze_rev3.py`, without writing bytecode.
    `GIT_OPTIONAL_LOCKS=0 git diff --check -- research-20261001/minor-sets
    research-20261001/multiround` exits 0 with no whitespace errors.
39. From the repository root: inline `timeout 60 python3` scan of Python
    command lines and `/proc/*/cwd`. No revision analysis or certificate
    process remains in either stream (`logs/process_check_rev3.log`).

Background processes: every job started in this continuation run and in the
revisions had a wall-clock limit (`timeout`); the earlier run's jobs (items
9–11) predate the process-hygiene rule and had none, but all of them had
completed before this run started. The revision used at most 3 loop processes
plus one analysis process. All processes had finished before the revised note
was completed (checked with `pgrep -fa "mrloop|run_rev1"`: no processes of
this stream). The revision after review round 2 used 3 loop processes plus at
most one analysis process; after the last check, `pgrep -fa
"mrloop|run_rev2|analyze_"` found no process of this stream.
The round-3 revision launched no background job; all foreground analyses
ran under `timeout` with one BLAS/OpenMP thread and finished.

## 9. Limits

- **One generator.** All loop results use the random McCormick generator of
  the scout report and the sfree note (dense random rows, box bounds, uniform
  random products). Nothing here is measured on MINLPLib or QPLIB, or inside
  SCIP. The effects are small (0.005–0.025 of the root gap after 10–20 rounds)
  and could change sign on structured instances.
- **Python model of SCIP's set.** Rule `scip` is the Python model of SCIP's
  Case-4 construction used by the sfree note, not SCIP's separator (no
  strengthening, no cut selection, no numerics safeguards, one cut per term
  and round, all cuts kept). The fidelity of that model is the subject of
  stream `scip-rule-fidelity/`.
- **Loop model.** Cuts are never removed, every violated term gets a cut in
  every round, and no cut-selection filter (efficacy, parallelism) is applied.
  A solver would behave differently; in particular a parallelism filter would
  remove most later cuts (Section 3.4).
- **Statistics.** Confidence intervals are per comparison (95% t-intervals,
  checked against bootstrap intervals in `logs/summary_main_*.log`); with
  about 25 rules and 6 rounds per size, a few nominally significant cells are
  expected by chance. I base conclusions on effects that are consistent
  across rounds and sizes. Failing to reject a zero difference is not
  evidence of no effect: several statements of the form "no detectable cost"
  (`s5o`, `maj2`, `eff2`) have intervals of about ±0.003 pooled and wider per
  size. The intervention test of Section 3.6 was not powered to detect the
  expected difference (about 0.004).
  The recovery contrasts of Section 3.5 are exploratory: pooled `o3s` over
  3–20 survives Holm with paired t-tests over that table's 12 cells (p = 0.0443),
  but not over the 36 contrasts across three spans (p = 0.133), or the 33 distinct
  tests (p = 0.122). With Wilcoxon, the 12-test survivors differ (Section 3.5). Neither adjustment covers
  all comparisons in this program; no repair difference between sizes is
  established.
- **Timing.** Seconds per instance were measured on a shared machine whose
  load varied from about 20 to over 200; they are only rough relative costs.
- **Theory.** Theorem 2 needs uniform cut depth, not pointed cones.
  Corollary 3 obtains that depth from uniform pointedness and step bounds;
  the observed cones become flat, so Corollary 3 does not apply. No uniform
  depth bound is established for the experiments, so Theorem 2 does not
  explain their behavior either.
  Proposition 6 uses an adversarial (if maximal and SCIP-derived) choice of
  sets; it says nothing about SCIP's or the bound-optimal rule. Theorem 2 and
  Corollary 3 are about the loop that cuts every violated term; Remark 3a
  covers a one-cut loop only with a most-violated-term selection. The
  positive results for `geo` and `pertED` are for idealized θ-approximate
  rules; no uniform θ is proved for the implemented bisection.
- **Diagnosis.** The cause of the reversal is identified only as a state
  effect of early non-SCIP rounds. The candidate common factor (shorter sets
  along most rays, Section 3.6) is supported by between-rule comparisons
  only, and was measured for twelve losing and non-losing rules on 6×8
  (60 or 30 instances) but only for `orbit`, `pertE0.1` and `geo` on 10×20
  (30 instances); several losing rules were never measured.
- **Literature.** The searches for prior work were short (Section 7); an
  unsuccessful search does not establish novelty.

## 10. Open questions

1. OQ3 (i) and (ii): does the loop converge for SCIP's rule or for the
   bound-optimal rule without a pointedness assumption? Proposition 6 shows
   that any proof must use the specific rule; Theorem 2 shows that a uniform
   depth bound would suffice. A counterexample would need cones that become
   flat, which happens in practice.
2. Is there a natural rule (not an adversary) whose loop provably fails?
   The bound-optimal rule is the candidate: Proposition 5 shows its steps can
   vanish at a fixed violation, but on the instance of Proposition 6 it
   converges in one round.
3. Does the orbit-then-SCIP or SCIP-then-orbit schedule behave the same way
   inside SCIP with its cut selection, on MINLPLib/QPLIB instances?
4. Is the common factor of Section 3.6 causal, and does it also hold for the
   losing rules not yet measured (`pert0.01`, `pert1`, `hyb0.9`, `alt2`, the
   switching schedules) and on 10×20 for more than three rules? A better-powered test would
   compare `maj2` with `rnd0.33` on several hundred instances, or construct
   orbit-family sets that are at least as long as SCIP's set on most rays
   while keeping a larger corner bound. Would another bound-optimal set (not
   the minimum-norm one) avoid the ties of Section 3.3, and would that matter?
5. Can the state measure "corner potential" (Section 3.2) be used directly as
   a look-ahead criterion, for example by preferring sets whose cut leaves the
   largest potential at the next vertex? This needs a cheap estimate of the
   next vertex.

## 11. Revision after review round 1 (2026-10-02)

Review: [reviews/review-r1.md](reviews/review-r1.md) (verdict "major
problems"; the theory of Section 5 was found correct). Each issue and how it
was handled:

- **M1 (the bug does not explain part of the multi-round gap).** Accepted.
  Recomputed with `code/analyze_rev1.py` (`logs/summary_rev1.log`): on the 10
  original instances the `orbit − orbit_core` difference after round 10 comes
  from one instance (+0.212; mean +0.020 [−0.028, +0.069]); on 220 instances it
  is +0.011 [+0.004, +0.019] after round 1 but −0.001 [−0.003, +0.002] after
  round 10 and −0.002 [−0.004, +0.001] after round 20. The attribution of 0.017
  of the gap to the bug is withdrawn in the summary (item 1), Section 1.3
  item 2, Section 2 and Section 6 item 2; the corrections of the one-cut table
  stand.
- **M2 (an orbit round at the root is not harmless).** Accepted, and
  extended with new runs: `o1s` was run on 8×12 and 10×20 (`code/run_rev1.sh`).
  The switching table of Section 3.5 now has round-3 columns and `o1s` rows
  for all sizes. Pooled over 220 instances `o1s` loses −0.006 [−0.011, −0.002]
  after round 10, about half of the orbit rule's loss; on 10×20 −0.013
  [−0.027, +0.002]; on 6×8 −0.014 [−0.025, −0.002] after round 3. `s1o` carries
  57% (6×8) and 68% (10×20) of the loss, not "almost the full amount".
  The round-1 attribution of shrinking deficits to repair by later SCIP
  rounds was revised in round 2 and withdrawn in round 3: the continued-orbit
  control does not establish a repair difference between sizes (Section 13,
  r3-m1). The damage is
  described as spread over rounds 0–4, and the root-only recommendation is
  withdrawn (summary item 3, Section 4).
- **M3 (the bound-attainment and degeneracy mechanism does not discriminate).**
  Accepted. Recounted ties and `z_C/z_K` for every diagnosed rule
  (`code/analyze_mech.py`): `pertE0.1` and `geo` have ties at 0–0.3% of
  corners and SCIP-like `z_C/z_K`, yet lose about as much. The degeneracy
  correlations (+0.08, p = 0.55; +0.18, p = 0.33) are now reported. The tilt
  comparison is now made at the same corners (differences ≤ 0.012), and the
  step-length signature is reported for all rules. The mechanism is withdrawn
  as the main cause (Section 3.3, summary item 2). As the review suggested, a
  shared factor was considered and tested (new Section 3.6): all losing rules
  pick sets shorter than SCIP's on most rays, the non-losing selection rules
  do not (measured then for only three losing rules; restricted and extended
  after review round 2, Section 12, n2); a within-rule test and a new intervention (rules `maj2` and
  `rnd0.33`, `code/run_rev1.sh`, `code/run_rev1b.sh`) are consistent with this
  factor but do not confirm it (`maj2 − rnd0.33` +0.003 [−0.002, +0.007]).
  The explanation (Section 3.7) is restated as a state effect of early
  non-SCIP rounds whose mechanism is only partly identified.
- **m1 (Holm count).** Corrected to 14 rules in Sections 2 and 4.
- **m2 ("never worse from the same state").** Restricted to 6×8 and to SCIP's
  10×20 states after the root; the 10×20 exceptions (root 0.677 vs 0.689;
  orbit-trajectory rounds 3–5 0.241 vs 0.250) are stated in the summary and
  Section 3.1.
- **m3 (ties attributed to Proposition 7).** The summary and Section 3.3 now
  say that Proposition 7 forces ties only for support ≥ 2 (5–16% of root
  terms), that the other ties come from the minimum-norm choice among
  bound-optimal sets, and that another bound-optimal set might avoid them
  (untested; Open question 4).
- **m4 (swappot range).** Corrected to −0.014 to −0.061 (Section 3.2).
- **m5 (`eff2` has no significant support).** The summary and Section 4 now
  say plainly that `eff2` has no demonstrated gain (Holm p = 0.78 after round
  10, 0.065 for AUC, negative on 10×20); the "70% of the benefit" figure is
  withdrawn; `eff`'s AUC gain is flagged as selected post hoc.
- **m6 (Setting L versus OQ3; distinct indices).** Section 5.1 now states that
  Theorem 2 and Corollary 3 concern the loop that cuts every violated term,
  and that Proposition 6 is unaffected and is also a counterexample for
  `S = {w ≤ xy}` alone. New Remark 3a (proved) transfers the convergence
  result to a one-cut loop that cuts a most violated term (by distance, or by
  violation for rules with `δ ≥ κ q`). Setting L now requires pairwise
  distinct indices, which Lemma 4 uses.
- **m7 (summary item 4).** The summary now says that the positive result for
  the perturbed orbit rules is for idealized θ-approximate rules and that no
  uniform θ is proved for the implementation.
- **o1 (clipping).** A sentence in Section 1.1 reports the clipping and the
  size of the excess (`code/check_clip.py`: 3728 of 52347 states, at most
  `6.9e-7` relative).
- **o2 (compressed logs).** New `code/recio.py`; all analysis scripts and
  `check_consistency.py` read `.jsonl.gz` directly and stop with an error if
  nothing matches; `check_consistency.py` also fails if it finds no
  duplicates. Rerun outputs are identical to the stored logs (Section 8,
  item 29).
- **o3 (docstring).** The `mrloop.py` docstring now says that `alt` uses the
  orbit set in even rounds counted from 0 and that `first_orbit` uses it in
  round 0.
- **o4 (notation).** Proposition 5 writes the reduced costs as `c̄`, since `w`
  is a coordinate there. The proof now also covers infinite steps explicitly
  (the review called this omission trivial).
- **o5 (prescribed limit).** The summary states the limit as any value in
  `(z_LP, z*) = (1, 1 + 2√ε)`.

Not changed: Propositions 5–7, Lemmas 1 and 4, Theorem 2, Corollary 3 and the
statistics of Sections 2 and 4 that the review recomputed and confirmed.

## 12. Revision after review round 2 (2026-10-02)

Review: [reviews/review-r2.md](reviews/review-r2.md) (verdict "minor fixes";
all round-1 issues found fixed, the numbers checked reproduced). Each issue and
how it was handled:

- **n1 (no recovery on 10×20 is wrong for `o3s` and `o5s`; different round
  spans compared).** Accepted. New script `code/analyze_rev2.py`
  (`logs/summary_rev2.log`) computes, per instance, the change of the deficit
  rule − SCIP over the same spans for every rule (rounds 3–20, 5–20, 10–20),
  with paired intervals. The round-2 revision added the deficit-change table
  to Section 3.5. Its interpretation as repair on 6×8 but not on 10×20 is
  withdrawn after round 3: the continued-orbit control does not establish
  that asymmetry (Section 13, r3-m1). Findings about deficits against SCIP:
  on 6×8 the deficits of `o1s` and
  `o2s` shrink significantly over rounds 3–20 (+0.013 [+0.002, +0.024],
  +0.019 [+0.001, +0.036]); on 10×20 all five changes over rounds 3–20 are
  negative and none is significant; over rounds 10–20 no change is
  significant in either size, and on 10×20 the signs are mixed (`o3s`
  +0.003, `o5s` +0.005, as the review noted, against −0.002 for `o1s` and
  `o2s`). Section 11 (M2) now points to this correction.
- **n2 ("shared by all losing rules" was measured for three rules only).**
  Accepted, and handled in two ways. (a) The measurement was extended: new
  diag runs (`code/run_rev2.sh`, 60 6×8 instances, `logs/rev2/`) for
  `pert0.1`, `pertE1`, `lex0.1`, `orbit_core`, `orbitB` and `alt`; their
  trajectories are identical to the main runs (Section 8, item 33). The five
  single-set rules among them pick sets shorter than SCIP's on 57–71% of the
  rays, like `orbit`, `pertE0.1` and `geo`; `alt` is shorter on 61% at the
  root and 19–37% later, because half of its cuts are SCIP's. Within each
  of the five, the share does not correlate with the loss (|Spearman| ≤ 0.08,
  p ≥ 0.55); for `alt` it correlates in the opposite direction to the
  hypothesis (+0.35, p = 0.006 uncorrected), which is reported in
  Section 3.6. (b) The wording is restricted to the rules measured, and the
  unmeasured losing rules are named (`pert0.01`, `pert1`, `hyb0.9`, `alt2`,
  the switching schedules, and all but three rules on 10×20): summary item 2,
  Section 3.6 (title "a common factor?", text and table, whose loss column now
  gives the 6×8 losses of the diagnostic instances instead of pooled
  losses), Section 3.7 item 4, Section 9 ("Diagnosis") and Open question 4.
  The status of the factor is unchanged: a heuristic hypothesis, not
  confirmed.
- **o1 (swappot "higher in every bucket").** Changed to "higher or equal",
  with the equal case (0.27 vs 0.27, orbit trajectory, rounds 3–5) stated
  (Section 3.2).
- **o2 (`analyze_mech.py` unlabeled last block, `+nan`).** The script now
  prints the label line, lists the rules used, and leaves out rules whose
  feature is constant (so the correlation is undefined). Rerun on both sizes:
  only the last block changed; the 10×20 `tie2` value is +0.153 over `orbit`
  and `pertE0.1` (Section 8, item 35). No number quoted in the note changed.
- **o3 ("about three quarters" on 4×4).** Changed to "about four fifths
  (ratio 0.82 in the log)" (Section 3.5).

Not changed: the theory of Section 5, the statistics of Sections 2 and 4, the
switching table of Section 3.5, the intervention test of Section 3.6 and the
recommendation, which the review confirmed.

## 13. Revision after review round 3 (2026-10-03)

Review: [reviews/review-r3.md](reviews/review-r3.md), verdict "minor fixes",
one minor issue and two optional items. Round 4 verified this revision;
its optional multiplicity, test-choice and indentation remarks are applied.

- **r3-m1 (recovery needs the continued-orbit control).** New analysis
  `code/analyze_rev3.py` (`logs/summary_rev3.log`) computes the paired
  changes of switching rule − orbit throughout on the 110 existing matched
  instances. Section 3.5 reports all four rules, both sizes and pooled,
  keeps the deficit table as a descriptive comparison against SCIP, and
  withdraws the repair asymmetry. On 6×8 `o1s` gains
  `+0.0006 [−0.0106, +0.0117]` over continued orbit rounds. On 10×20 `o3s` gains
  `+0.0078 [+0.0017, +0.0140]` (p = 0.0134, uncorrected). Neither size has
  a Holm-significant contrast over the table's 12 tests; pooled `o3s`
  does (p = 0.0443), but not over all 36 contrasts across three spans
  (p = 0.133). Summary, explanation, recommendation, Limits and the
  round-1/round-2 revision entries now follow this controlled comparison.
  The recommendation remains to keep SCIP's set: gains relative to orbit
  throughout do not establish gains relative to SCIP throughout.
- **r3-o1 (`alt` tie counts mix both types of rounds).** Section 3.6 now
  says "`alt` (over all its rounds)"; the numerical counts are unchanged.
- **r3-o2 (diagnostic rule count).** Limits now says twelve measured rules
  on 6×8, counting `alt` as well as the eleven other rules.

No new experiment ran. The theory, main-run statistics and raw records are
unchanged. Section 8 records the targeted analyses and their results.
