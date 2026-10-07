# Review r1 of stream `multiround` (note.md of 2026-10-02)

Reviewer: independent research agent (adversarial review), 2026-10-02. I did
not write any of this material. "Reviewed" here means checked by another
research agent, not journal peer review.

## Verdict

**Major problems.** The theory in Section 5 holds up. Theorem 2, Lemmas 1
and 4, Corollary 3 and Propositions 5–7 are correct as stated. I verified
Proposition 6 (the negative answer to OQ3 (iii)) independently in exact
arithmetic for two values of `ε` and up to 40 rounds. The loop data
reproduce bitwise, and every table number I recomputed from the raw records
matches.

Three conclusions in the summary, however, are not supported by the
stream's own data:

1. The claim that the corner-bound bug caused about 40% (0.017) of the
   original loop gap.
2. The claim that an orbit round at the root only is harmless.
3. The proposed mechanism for the reversal (bound attainment leading to
   dual degeneracy). Rules that neither attain the corner bound nor create
   ties lose almost as much.

The note needs a revision of Sections 1.3, 2, 3.3, 3.5, 3.6, 4 and 6 and of
the summary before it can be called verified.

## Major issues

### M1. The bug does not explain part of the multi-round gap

Locations: Summary item 1; Section 1.3 item 2; Section 2, first bullet;
Section 6 item 2. The same claim also appears in the author summary ("Part
of the original 0.887 vs 0.931 gap was a bug").

The claim is that about 0.017 of the 0.044 gap after 10 rounds on the 10
original 6×8 instances was caused by the bug: `orbit` gives 0.904 while
`orbit_core` gives 0.883. The 0.904 is computed correctly, but the causal
reading is not supported:

- **The difference comes from one instance.** On the 10 instances
  (`logs/fid2_exploop_6x8.jsonl`), the per-instance differences
  `orbit − orbit_core` after round 10 are
  `0, 0, 0, 0, +0.212, 0, 0, +0.016, +0.004, −0.028`. The paired mean is
  +0.020, with 95% t-interval [−0.028, +0.069]. After rounds 1 and 3 the two
  rules are identical within ±0.002.
- **The large sample shows no effect.** On the 220 main-run instances,
  `orbit − orbit_core` is:
  - after round 1: +0.011 [+0.004, +0.019];
  - after round 10: −0.0008 [−0.0033, +0.0017];
  - after round 20: −0.0016 [−0.0042, +0.0010].

  No size shows a significant difference at round 10. The note's own pooled
  table agrees: `orbit_core` is −0.011 and `orbit` is −0.012 after round 10.

So the bug changes the one-cut and round-1 numbers, and the Section 9.2
corrections stand. It does not change the multi-round reversal. The
correction to sfree Section 9.3 should say that the 0.887 → 0.904 change on
the 10 instances is within the loop's instance-level noise, and that the bug
has no measurable effect after round 10 on 220 instances. "Of which about
0.017 was the corner-bound bug" should be removed from Section 2 and from
the summary.

Reproduce with `reviews/r1-scripts/core_vs.py`.

### M2. Switching experiments: an orbit round at the root is not harmless

Locations: Summary item 2 ("orbit rounds at the root only, or after round 5,
cost nothing"); Section 3.5 reading; Section 3.6 item 4; the recommendation
in Section 4 ("using it at the root only is harmless (`o1s`)").

The data in `logs/summary_key_*.log` show otherwise:

- **4×4:** `first_orbit` (= `o1s`) is −0.006 [−0.016, +0.003] after round 10.
  The orbit rule throughout is −0.008. One root round therefore carries
  about 75% of the full loss. The 4×4 `o1s` row is missing from the
  switching table, although the text says "o1s on 6×8 and 4×4" is harmless.
- **6×8:** `o1s` is −0.014 [−0.025, −0.002] after round 3. This is
  significant, and about two thirds of the orbit rule's own −0.021 at
  round 3. W/L after round 10 is 4/10.
- **Pooled over 4×4 and 6×8** (my recomputation, n = 120): `o1s` is −0.011
  [−0.020, −0.003] after round 3 and −0.005 [−0.010, +0.001] after round 10.
  This is about half of the orbit rule's loss on these sizes.
- **`s1o`** ("cost almost the full amount") is −0.006 against −0.011 on 6×8,
  about 55%.
- **Partial recovery on 6×8.** SCIP rounds do partly repair the damage
  there:
  - `o1s`: −0.014 at round 3, −0.001 at round 20;
  - `o5s`: −0.011 at round 10, −0.006 at round 20;
  - `o2s`: −0.007 at round 10, −0.004 at round 20.

  "SCIP rounds do not recover it" holds only on 10×20.

Failing to reject a zero difference is not evidence of no effect. The
statements should read as follows:

- Round 0 contributes too (significantly at round 3 on 6×8).
- The damage is spread over rounds 0–4.
- Late orbit rounds (`s5o`) show no detectable cost.

Withdraw the recommendation that orbit at the root is harmless. `o1s` was
also not run on 10×20, where the reversal is largest.

### M3. The bound-attainment and degeneracy mechanism does not discriminate between rules

Locations: Summary item 2; Section 3.3 "Consequence" and "Supporting
measurements"; Section 3.6 items 2–3. The note's explanation is that the
orbit cuts attain `z_K`, which by Proposition 7 makes the corner LP dual
degenerate, which leads to flat states and stalling. This is labeled
heuristic, but it is presented as "the cause". The stream's own data
contradict it as a specific explanation:

- **Non-degenerate rules lose almost as much.** I recounted near-binding
  rays from the stored cut records (`logs/diag/diag_6x8_*`, same 1e-3
  tolerance as `analyze_ties.py`; `reviews/r1-scripts/ties_all.py`, run on
  decompressed copies):
  - `pertE0.1` and `geo` have ≥ 2 binding rays at only 0–0.3% of their
    corners in every bucket. SCIP's rule: 0–0.5%. Orbit: 17–24%.
  - Their mean `z_C/z_K` is 0.83–0.92 and 0.79–0.83. SCIP's is 0.84–0.92.

  So these two rules neither attain the bound nor create ties. Yet they
  lose:
  - on 6×8 after round 10: −0.010 (`pertE0.1`) and −0.015 (`geo`), against
    −0.011 for orbit;
  - pooled: −0.008 and −0.009 (Holm p = 0.016 and 0.003), against −0.012
    for orbit.

  `pertE0.1` ties SCIP in round 1 (−0.005), so its later loss is not a bad
  first round. The state comparisons show no significant state degradation
  for these rules either, as the note says ("at most one significant cell").
  The note never reconciles this with its mechanism.
- **The degeneracy feature is unrelated to the per-instance loss, and this
  is not reported.** In `logs/summary_percase_*.log`, the feature `degen`
  (share of rounds 1–5 with a near-zero reduced cost) has Spearman +0.079
  (p = 0.55) on 6×8 and +0.184 (p = 0.33) on 10×20. The note quotes only the
  `loggamma` and `cosobj` correlations.
- **Tilt toward the objective is mostly a trajectory effect.**
  - At the same corners (the `both:orbit` and `both:scip` rows of
    `summary_diag_6x8.log`), the mean `|cos|` with the objective differs by
    at most 0.012 (0.626 vs 0.618, 0.707 vs 0.695).
  - At the root it is equal (0.544 vs 0.546).
  - In rounds 11–19 the orbit value is lower (0.818 vs 0.824).
  - On 10×20 the orbit cuts are on average *less* objective-parallel (mean
    feature difference −0.010 in `summary_percase_10x20.log`).

  The quoted 0.624/0.717 vs 0.588/0.687 compares different states.
- **The step-length signature is shared and inconsistent.**
  - Short steps on expensive rays: `geo` and `pertE0.1` have equally short
    or shorter steps relative to SCIP's set (median log ratio −0.09 to
    −0.30, against −0.10 to −0.22 for orbit).
  - Cheap rays: the orbit step is longer only at the root (+0.10) and in
    rounds 3–5 (+0.35). It is shorter in rounds 1–2, 6–10 and 11–19 (−0.04,
    −0.07, −0.02).

  "Deep along cheap rays, shallow along expensive ones" is therefore not a
  consistent property of the orbit rule.

What remains supported is the following:

- Orbit trajectories reach harder states on 6×8.
- One root orbit round already creates them (M2).
- Proposition 7 itself is correct.

The explanation should be restated:

- Bound attainment and degeneracy may contribute, but they cannot be the
  main cause, because every orbit-family rule loses, including
  non-degenerate ones.
- A shared factor should be considered and tested. One candidate is that
  orbit-family sets are smaller than SCIP's set along most rays. The step
  tables show this, and it would also fit efficacy selection, which mostly
  keeps SCIP's set, doing well.
- Summary item 2 and Section 3.6 must be revised accordingly.

## Minor issues

- **m1. Holm count.** Holm adjustment is over 14 rules, not 15 (Sections 2
  and 4). `analyze_pooled.py` lists 14 rules besides `scip`.
- **m2. "From the same LP state an orbit round is never worse on average"
  (summary).** This holds on 6×8 only. On 10×20 (`summary_state_10x20.log`):
  - root states: SCIP round 0.689, orbit round 0.677;
  - orbit-trajectory states in rounds 3–5: 0.250 vs 0.241.

  Qualify the claim, or restrict it to 6×8 and to states after the root.
- **m3. Ties attributed to Proposition 7.** The summary's colon ties the
  13–34% dual-degenerate corners to Proposition 7. Proposition 7 forces
  degeneracy only when the minimizer has support ≥ 2 (5–16% of root terms).
  As Section 3.3 itself says, the extra ties come from the minimum-norm `F`
  chosen by the bisection, that is, from tie-breaking within the
  bound-optimal family. Say this in the summary. Also say that another
  bound-optimal set might avoid the ties (untested).
- **m4. Swappot range.** Section 3.2 says the per-instance differences are
  "−0.025 to −0.061 in rounds 0–5". `logs/summary_swappot_6x8.log` also has
  −0.014 (orbit trajectory, rounds 3–5).
- **m5. The `eff2` recommendation has no significant support.** `eff2`'s
  pooled gain is not significant at any measure after Holm (p = 0.78 after
  round 10, 0.065 for AUC). Its point estimate on 10×20 is negative (−0.002).
  Only `eff` has a Holm-significant AUC gain (p = 0.025), and `eff` was
  selected as the best of 14 rules. The summary should say plainly that
  `eff2` has no demonstrated gain and is recommended only because it is
  never measurably worse. "About 70% of the benefit" is a ratio of
  non-significant means.
- **m6. Setting L versus OQ3.**
  - OQ3 is stated for a loop with *one* intersection cut per round and a
    general `S = {q ≤ 0}`. Setting L adds a cut for *every* violated
    bilinear term, and Theorem 2's proof uses this: round `r_k` must cut the
    term violated at the accumulation point. Say that Theorem 2 and
    Corollary 3 apply to this multi-cut loop, not directly to OQ3's one-cut
    loop.
  - Proposition 6 has a single term, so the counterexample is unaffected.
    It is also a counterexample for `S = {w ≤ xy}` alone, since `z*` is the
    same.
  - Lemma 4 implicitly assumes `i, j, k` distinct (no square terms). State
    this.
- **m7. Summary item 4.** "Holds for SCIP's rule and for two perturbed orbit
  rules" applies to idealized θ-approximate rules. The body correctly says
  that no uniform θ is proved for the implementation. Carry the caveat into
  the summary.

## Optional

- **o1. Clipped fraction.** `closed` is clipped to [0, 1 + 1e-9]. The stored
  LP values exceed SCIP's `z_bil` in 3684 round states. The excess is at
  most 6.9e-7 relative to `|z_bil|` (at most about 2e-4 of the root gap),
  which is within SCIP's feasibility tolerance. So I found no evidence of
  invalid cuts. A sentence in the note would help.
- **o2. Analysis scripts and compressed logs.** `check_consistency.py` and
  the analysis scripts read plain `.jsonl`. After the gzip step,
  `check_consistency.py` silently prints "compared: 0, differing: 0". Make
  the scripts read `.gz` files or fail loudly.
- **o3. Docstring.** The `mrloop.py` docstring says `alt` is "orbit in odd
  rounds", but the code uses even (0-based) rounds. The code matches the
  note.
- **o4. Notation.** `w` denotes both the reduced costs and the third
  variable in Section 5 (Proposition 5: "reduced costs `w = (1, ε, 1)`" next
  to `w ≤ xy`).
- **o5. Prescribed limit.** The author summary's "drives the LP values to
  any chosen value below the optimum" should be "to any value in
  `(z_LP, z*) = (1, 1 + 2√ε)`". The note's own wording is correct.

## What I checked and found correct

- **Proposition 7.** Line by line: the termwise-equality argument is valid,
  and the relative-interior claim follows. The hypotheses (corner minimizer
  exists, `z_K ∈ (0, ∞)`, `C` convex) are stated.
- **Lemma 1, Theorem 2, Corollary 3.** Correct. Compactness of `P`, closed
  `S_e`, monotone values, and a cut for every violated term per round are
  all used and all available.
- **Lemma 4.**
  - (a) Correct.
  - (b) I checked against `scout_sfree.ms_set` Case 4: `κ = 0`, `r = f = 1`,
    `x̂ = ((x−y)/2, (w+1)/2)`, `ŷ = ((x+y)/2, (w−1)/2)`. Both `φ` branches
    satisfy `φ ≤ ‖·‖` by Cauchy–Schwarz. The Lipschitz constant `1/√2` and
    the ball radius `(a−b)/√2` are right.
  - (c) I checked against `core.Mmat`: `‖M_0(Δs)‖_F = ‖Δs‖`, `det F = 1/q`,
    and family (A) in `fastorbit.py` is unrestricted in `F`.
  - (d) Correct.
- **Proposition 5.** `z_K = 2√ε` by AM–GM. The midpoint argument for
  `α_1 α_2 ≤ 4` is valid. If one step is infinite, take a large finite
  point; this is a trivial omission.
- **Proposition 6.**
  - Maximality: the `(u, v)` construction is valid.
  - Automorphism: correct.
  - Round algebra: correct. The steps are `ξ' − ξ`, `4/(ξ+ξ')` and `∞`; the
    cut multiplies out to `x/ξ' + ξ'y/4 ≥ 1`; the reduced costs are
    positive for `ξ < 2/√ε`; the old cuts and box rows are slack.
- **Novelty and citations.** The claims are appropriately modest. The Muu
  (1985) quote is present on p. 429 of the saved PDF, and its sha256 matches
  the manifest. The Zanette–Fischetti–Balas, Eaves–Zangwill and
  Dey–Molinaro bibliographic data are correct, and their limited use is
  disclosed.
- **Task coverage.** All five steps of the stream task were addressed.
  "Several cuts per term" was tested only with two cuts per term.

## Checks actually run by the reviewer

Every command was run in the foreground with a wall-clock limit or
completed in seconds. Nothing is left running.

1. **Rerun of `oq3_example.py`.** Command:
   `timeout 1200 python3 oq3_example.py 12 60` (from `code/`). Exit 0 in
   23 s. Output identical to `logs/oq3_example.log` ("ALL ROUNDS VERIFIED:
   True").
2. **Independent exact check of Proposition 6.** Command:
   `timeout 600 python3 reviews/r1-scripts/oq3_indep.py`. It uses Python
   `Fraction` only, with no sympy: Cramer rays, exact quadratic roots,
   strict dual feasibility, primal feasibility and the cut identity, plus a
   HiGHS float LP cross-check of each next vertex. All runs pass:
   - `ε = 1/4`, `ξ_r = 2(1−2^{−r})`, rounds 0–40;
   - `ε = 1/9`, `ξ_r = (11/2)(1−3^{−r})`, rounds 0–30, box `X = 12, Y = 1, W = 3`;
   - the same at the hypothesis boundary `X = 2/√ε = 6`, `Y = √ε = 1/3`.

   The limits are 1.5 and 1.6111.
3. **Independent recomputation of the statistics.** Command:
   `python3 reviews/r1-scripts/indep.py`. It reads all 5160 records in
   `logs/main` and `logs/new`, all with status ok. The pooled and per-size
   paired differences, t-intervals, W/L counts, SCIP means and ">0.999"
   counts match Section 2, Section 4 and `logs/summary_*.log`.
4. **LP values against SCIP's bounds.** Command:
   `python3 reviews/r1-scripts/valid.py`. The maximum excess of a stored LP
   value over SCIP's primal value is 6.9e-7 relative (o1). SCIP's gap was 0
   on every instance.
5. **`orbit` against `orbit_core`.** Command:
   `python3 reviews/r1-scripts/core_vs.py`. Results in M1.
6. **Bitwise rerun of the loop.** Command:
   `timeout 1500 python3 mrloop.py ../data/inst_10x20.json scip,orbit,eff2,s1o 20 /tmp/rv/rerun.jsonl 0 3`.
   All 12 trajectories are identical to the stored records (maximum
   difference 0).
7. **Consistency check.** I ran `check_consistency.py` on decompressed
   copies of `logs/diag` under `/tmp`: 780 pairs, 0 differing. On the
   compressed directory as shipped, the same script reports 0 pairs (o2).
8. **Tie recount.** Command: `python3 reviews/r1-scripts/ties_all.py`, on
   the decompressed copies. It covers all rules in the 6×8 diagnostic
   records. Results in M3.
9. **Reading of logs against the note's numbers.** Logs read:
   - `summary_state_*`, `summary_ties_*`, `summary_diag_6x8`,
     `summary_swappot_6x8`, `summary_percase_*`;
   - `support_stats`, `fid2_exploop_*`, `recheck_mccormick_1*`,
     `summarize_zk_scip`, `check_zk`.

   Case study instance 53 (−0.163) confirmed. The mismatches found are
   listed above.
10. **Source check.** `sha256sum sources/kybernetika1985_reverse_convex.pdf`
    matches the manifest. The quoted sentence is found in the extracted
    text.
11. **Process check.** `pgrep -fa 'mrloop|support_stats|oq3_example|run_new|run_queue'`
    found no process of this stream. One `run_queue.sh` was running, with
    working directory `research-20261001/three-var-computation/code`; it
    belongs to another stream and was not touched.

I did not run project-wide verification or look at CI.
