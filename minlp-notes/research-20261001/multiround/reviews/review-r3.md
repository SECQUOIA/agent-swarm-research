# Review r3 of stream `multiround` (note.md revised after review round 2)

Reviewer: independent research agent (adversarial review, confirmation
round 3), 2026-10-02. I did not write any of this material. "Reviewed" here
means checked by another research agent, not journal peer review.

## Verdict

**Minor fixes.** Both minor issues of round 2 (n1, n2) and all three optional
items are handled. Every new number I checked matches the raw records, and my
own script, which does not use the stream's code, reproduces them. The new
diag runs reproduce bitwise, including every cut record.

One new minor issue remains, in the restated recovery bullet of Section 3.5
(r3-m1 below). The numbers in that bullet are correct. But its conclusion
("SCIP rounds partly repair the early damage on 6×8; on 10×20 I detect no
repair") does not follow from them. The bullet compares each rule with SCIP's
rule. It never compares with the orbit rule run throughout, which is the
control that isolates the effect of the later SCIP rounds. With that control
the picture changes:

- On 6×8 the deficit of `o1s` shrinks exactly as much as that of the orbit
  rule run throughout.
- On 10×20 one switching rule (`o3s`) does gain significantly over continued
  orbit rounds (uncorrected).

## Status of the round-2 issues

| Issue | Status | Evidence |
|---|---|---|
| n1 (no recovery on 10×20; different round spans) | **Fixed as asked.** The bullet is retitled and now has a table over identical spans for every rule. The 10×20 signs are stated correctly: all changes over 3–20 are negative, and over 10–20 `o3s` is +0.003 and `o5s` +0.005. The interpretation added with the fix has a new problem; see r3-m1. | `analyze_rev2.py` reruns identically to `logs/summary_rev2.log`. My independent script reproduces every cell, e.g. 6×8 `o1s` +0.0128 [+0.0017, +0.0239] and `o2s` +0.0185 [+0.0008, +0.0363]; pooled `o5s` 10→20 +0.0045 [+0.0007, +0.0083], p = 0.021. |
| n2 ("shared by all losing rules") | **Fixed.** The wording in the summary, Sections 3.6, 3.7 and 9, and Open question 4 is restricted to the rules measured. The unmeasured rules are named. The measurement was extended to six more losing rules on 6×8. | Every cell of the Section 3.6 table matches `logs/summary_mech2_6x8.log` (shares, log ratios, losses). My recomputation of the shares (on α = 1/a directly), the log ratios, the losses, the within-rule Spearman values (6×8: −0.136 to +0.058; 10×20: +0.041 to +0.150; all p ≥ 0.3) and `alt` +0.349, p = 0.0063, Holm ×9 = 0.057 agree. |
| o1 (swappot "higher or equal") | Fixed. | |
| o2 (`analyze_mech.py` label, `+nan`) | Fixed. | The reruns of all three `analyze_mech.py` invocations are identical to the stored logs. The 10×20 pooled `tie2` is +0.153 over `orbit` and `pertE0.1`. |
| o3 ("about four fifths") | Fixed. | |

## Remaining issues

### Minor

**r3-m1. The recovery bullet attributes the shrinking deficit to the later
SCIP rounds, but the right control shows no such effect for `o1s` on 6×8,
and does show one on 10×20.**

Location: Section 3.5, bullet "Recovery by later SCIP rounds: detected on 6×8
between rounds 3 and 20, not detected on 10×20", especially its last
sentence, "So SCIP rounds partly repair the early damage on 6×8; on 10×20 I
detect no repair". The same reading appears in Section 12 n1 and in the
author's open question "Why does recovery … appear on 6×8 but not on 10×20?".

The deficit `d(r)` = rule − SCIP must shrink as both trajectories approach
`z_bil`. On 6×8 the mean gap that SCIP's rule leaves falls from 0.080 after
round 3 to 0.027 after round 20, so some compression happens whatever rounds
follow. The bullet's own table shows this. The orbit rule run throughout,
with no SCIP rounds at all, shrinks its 6×8 deficit by +0.012 over rounds
3–20, almost exactly as much as `o1s` (+0.013). Only `o1s` reaches
significance, by a small margin.

The control that isolates the effect of the later SCIP rounds is the paired
contrast (rule − orbit)(20) − (rule − orbit)(3). My script
`reviews/r3-scripts/indep_rev2.py` (log `indep_rev2.log`) gives:

| Rule | 6×8 (n 60) | 10×20 (n 50) | pooled (n 110) |
|---|---|---|---|
| `o1s` | +0.0006 [−0.0106, +0.0117], p 0.92 | +0.0052 [−0.0099, +0.0204], p 0.49 | +0.0027 [−0.0064, +0.0117] |
| `o2s` | +0.0063 [+0.0007, +0.0120], p 0.028 | +0.0054 [−0.0095, +0.0202], p 0.47 | +0.0059 [−0.0014, +0.0132] |
| `o3s` | +0.0044 [−0.0009, +0.0098], p 0.10 | +0.0078 [+0.0017, +0.0140], p 0.013 | +0.0060 [+0.0020, +0.0100], p 0.004 |
| `o5s` | +0.0025 [−0.0015, +0.0065], p 0.21 | +0.0037 [−0.0040, +0.0114], p 0.34 | +0.0030 [−0.0010, +0.0071] |

So the asymmetry the bullet draws between the sizes is an artifact of the
baseline it chose. Against continued orbit rounds:

- `o1s` gains nothing on 6×8. Its "significant recovery" there is the common
  compression of the deficit, not repair by SCIP rounds.
- Each size has exactly one nominally significant contrast. Neither survives
  a Holm correction over the 8 tests of its size (6×8: 0.028 × 8 = 0.22;
  10×20: 0.013 × 8 = 0.11).
- Pooled, `o3s` beats continued orbit rounds significantly.

The data therefore do not support "repair on 6×8, none on 10×20".

This does not affect the main conclusions of Section 3.5. The damage is still
created in rounds 0–4, and the pooled `o3s` contrast is consistent with
"orbit rounds after round 3 still cost something". But the stated reading
does not follow from the data. Suggested fix: report the contrast against
`orbit`, or restate the bullet as: "the deficits shrink as the remaining gap
closes; whether later SCIP rounds repair more than continued orbit rounds
would is not established in either size". Drop or rephrase the open question
about the 6×8/10×20 difference.

### Optional

- **r3-o1.** Section 3.6, first paragraph: "`alt` in its orbit rounds; ties
  at 7–24% of the corners". The `alt` figures in `logs/summary_mech2_6x8.log`
  (0.066–0.181) average over all of `alt`'s corners, SCIP rounds included,
  because `analyze_mech.py` splits by set only for `both`. The lower end, 7%,
  is therefore not a figure for its orbit rounds. Write "`alt` (over all its
  rounds)".
- **r3-o2.** Section 9, "Diagnosis": "measured for eleven losing and
  non-losing rules on 6×8". The table of Section 3.6 has twelve rules: eight
  single-set losing rules, `alt`, and three non-losing rules. Write "twelve",
  or "eleven, besides `alt`".

## Checks of the new and changed material

### Proofs

Section 5 is unchanged since round 2, where I checked Remark 3a, the revised
proof of Proposition 5 and Setting L line by line. No proof was added or
changed in this revision. I spot-checked that the summary's statements of
Theorem 2, Remark 3a, Lemma 4 and Propositions 5 and 6 still match their
hypotheses in Section 5; they do.

### Computations

1. **Independent statistics.** `reviews/r3-scripts/indep_rev2.py` reads the
   raw `.jsonl`/`.jsonl.gz` records directly, without `recio.py` or any other
   stream code. It asserts status `ok` and that duplicate trajectories are
   identical. It reproduces:
   - every cell of the Section 3.5 recovery table, and the pooled `o5s`
     value;
   - every cell of the Section 3.6 table. I computed the share of shorter
     steps from the steps α = 1/a, not from the inverses as
     `analyze_mech.py` does; the two definitions agree;
   - the 10×20 within-rule correlations.

   It also checks that the 660 rule/instance trajectories in `logs/diag` and
   `logs/rev2` that also occur in the main runs are identical to them
   (0 differing). `check_consistency.py` counts more pairs (1170), because it
   also pairs main runs with each other; its stored log is consistent.
2. **Bitwise rerun of the new runs.**
   - Commands: `mrloop.py ../data/inst_6x8.json pert0.1,pertE1,lex0.1 20 … 20 23 diag`
     and the same with `orbit_core,orbitB,alt`.
   - Result: all 18 records are identical to `logs/rev2/diag2_6x8_20.jsonl.gz`
     in `closed`, `ncuts`, `rounds` and every cut record. The timing field
     was not compared.
   - My first attempt at the second job ran inside a backgrounded subshell
     and exited with code 1 without writing a log. This was a mistake in my
     shell command, not in the stream. I reran it in the foreground: exit 0.
3. **Reruns of the analysis scripts, diffed against the stored logs.** All
   are identical:
   - `analyze_rev2.py` against `logs/summary_rev2.log`;
   - `analyze_mech.py '../logs/[dr]*/diag*_6x8_*.jsonl' 10` against
     `summary_mech2_6x8.log`;
   - `analyze_mech.py '../logs/diag/diag_10x20*.jsonl' 10` against
     `summary_mech_10x20.log`;
   - `analyze_mech.py '../logs/diag/[cd]*_6x8*.jsonl' 10` against
     `summary_mech_6x8.log`.
4. **Bookkeeping.**
   - `logs/rev2/done.txt` lists all 6 jobs with exit code 0.
   - The chunk logs show 10 instances × 6 rules each, 360 records in total.
   - `run_rev2.sh` puts each job under `timeout 5400`.
   - `mrloop.py` is unchanged by this revision; its rule definitions are as
     reviewed in round 2.
5. **Code reading.**
   - `analyze_rev2.py` computes the paired changes over identical spans and
     asserts that every rule covers every SCIP instance.
   - The new `analyze_mech.py` block leaves out undefined correlations and
     labels the pooled lines correctly.
   - The `alt` share mixes SCIP-round cuts (share 0) with orbit-round cuts,
     as the note says.

### Statistics and conclusions

The Section 3.6 claims are now correctly scoped:

- the eight single-set losing rules are measured on 6×8 and three of them on
  10×20;
- the three non-losing rules are measured;
- the within-rule test is reported as weak;
- the opposite-direction `alt` correlation is reported with its confound and
  a Holm value.

The factor stays labeled heuristic, which is right. The one conclusion that
goes beyond its evidence is r3-m1.

### Novelty, solver relevance, task coverage

These are unchanged from round 2 and remain appropriately modest. The
recommendation ("keep SCIP's set") follows from the data.

### Processes

`pgrep -fa 'mrloop|run_rev|analyze_|indep_'` found no running process after
my checks. My reruns were under `timeout` and used at most 2 loop processes at
a time. The note's statement that the stream left no process running agrees
with what I saw.

## Checks actually run by the reviewer

All commands were run from `multiround/code/` unless stated, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`.

1. `timeout 900 python3 indep_rev2.py`, run from `reviews/r3-scripts/`, with
   output in `indep_rev2.log`. Exit 0. All values match the note and the
   logs; the contrasts are in the r3-m1 table.
2. `timeout 1500 python3 mrloop.py ../data/inst_6x8.json pert0.1,pertE1,lex0.1 20 /tmp/rv3/a.jsonl 20 23 diag`
   gave exit 0.
   `timeout 1500 python3 mrloop.py ../data/inst_6x8.json orbit_core,orbitB,alt 20 /tmp/rv3/b.jsonl 20 23 diag`
   gave exit 0 on the foreground rerun; the first, backgrounded attempt gave
   exit 1, a fault in my shell command. An inline Python comparison with
   `logs/rev2/diag2_6x8_20.jsonl.gz` found 18 records and 0 differences.
3. `timeout 600 python3 analyze_rev2.py` plus `diff`: identical.
4. `timeout 900 python3 analyze_mech.py …`, three invocations as listed
   above, plus `diff`: all identical.
5. I read `logs/check_consistency_rev2.log` (1170 pairs, 0 differing),
   `logs/rev2/done.txt`, the chunk logs, and the 10×20 correlation block of
   `logs/summary_mech_10x20.log`.
6. `pgrep -fa 'mrloop|run_rev|analyze_|indep_'`: no process.

I did not run project-wide verification and did not look at CI.
