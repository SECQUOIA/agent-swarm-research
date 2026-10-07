# Review: waterno2_06 separator branching with cell-dependent slopes (`cell-slopes.md`)

Date: 2026-10-01. Reviewer: independent verifier. I did not produce the
work under review or its code.

Reviewed: `open-instances-wave2/waterno2/cell-slopes.md` and the code and
logs in `open-instances-wave2/waterno2/cellslopes/`. Background: the
predecessor note `separator-branching.md` and its review
`reviews/waterno2-sepbranch-review.md`. My scripts and logs are in
`reviews/waterno2-cellslopes-review-checks/`. I edited nothing under
`open-instances-wave2/` or in the earlier reviewers' folders.

**Independence.** I read the certificate pickles through a stub class
(`load_cs.py`), so no author code ran in my certificate checks. The model is
the first verifier's (`vmodel`), and the implied bounds are the first
verifier's (`my_implied_06.json`). I re-certified the pair bounds with the
recheck's `vbb2.py` through a driver I wrote (`vrebound_cs.py`). I did not
use the authors' `crosscheck_cs.py` or the earlier review's `rebound.py`.
I reused two things from the earlier review. The first is its terminal-row
derivation, which I re-ran (`logs/terminal_T6_rerun.log`). The second is
its check that every model row except the horizon row lies inside one
period or is a link row.

## Verdict

**The certified dual bound 278.230573774 for waterno2_06 (certificate certB)
is confirmed.** Its exact value is 39157472136693483/140737488355328.

I re-certified with `vbb2.py` **every one of the 49,315 records that the certB
dynamic program (DP) uses**, not a sample. This includes the 5,158 cert3
records and the 19,679 certA records that certB reuses, many of them through
a Lemma-2 slope correction. Each record was run on its own boxes and its
own slopes, with the rbb bound as target:

- 33,899 records were certified at exactly their rbb bound;
- 15,416 record boxes were proved empty. These are all 12,298 records with
  rbb bound +∞, plus 3,118 records with a finite rbb bound;
- no record failed.

My own code then added the exact Lemma-2 corrections to the leaf slopes and
computed the shortest path in exact arithmetic over the vbb2 values alone.
The result is 39157472136693483/140737488355328, **the authors' value**. So
certB no longer rests on `rbb.py`: every value it uses has now been
certified by two separate codes.

| check | result |
|---|---|
| validity of cell-dependent slopes (Proposition 1) | correct; the only coupling condition is one vector per cell, used for the exit term of period t and the entry term of period t+1 (Section 1) |
| the code uses one vector per leaf on both sides, including split cells and the last period | yes: `verify_cs.py` and my own DP use one array per link for both adjacent periods; records reach the leaves only through Lemma 2; no record has a slope on a missing side (Section 1) |
| Lemma 2 | re-derived; correct. The exact evaluation in `verify_cs.py` matches my separately written code (Section 2) |
| Lemma 2 tested at the DP's leaf slopes with vbb2 | 556 leaf pairs, all with a nonzero correction (−91.7 to +160.6): 436 certified at the exact corrected bound, 120 proved empty, 0 failed (Section 5.3) |
| level box ⊆ root; leaves partition the root | yes, all 5 links, certB and certA (Section 3) |
| leaf pair → record (period, boxes contain the leaves, slopes, correction) | all 117,736 leaf pairs of certB (and of certA); my selection by box containment over all records gives the authors' set of used records exactly (Section 3) |
| exact DP, certB / certA / cert3 state | identical to the authors' values: 278.230573774 / 277.093321045 / 272.584700834 (Section 4) |
| all certB records re-bounded with vbb2 (own driver) | 49,315 of 49,315; 0 failures; exact DP from vbb2 values only = authors' value (Section 5) |
| negative control: certify p4's value + 0.01 on p4's six leaf pairs | none certified (Section 6) |
| points p1–p4 | every leaf pair containing a point has a bound below the point's period value (smallest margin 0.0098); path sums equal the note's (Section 6) |
| reported costs, counts, negative results, "not established" | agree with the logs and pickles, with minor exceptions (Sections 7 and 8) |

certA (277.093321045) is superseded. I confirmed its data and its exact DP
but did not re-bound it as a whole. Its 43,140 rbb runs include the 19,679
records that certB uses, and those were re-bounded. The issues in Section 8
are minor and concern wording and bookkeeping, not validity.

## 1. Validity of cell-dependent slopes (Proposition 1)

**The argument.** Let x be exactly feasible. Let y_t be its link-t levels,
so s_{t+1}(x) = e_t(x) = y_t. Let D_t be any one leaf of link t that
contains y_t. For each link, add the term λ_{t,D_t}·(s_{t+1}(x) − e_t(x)),
which is zero, to f(x) = Σ_t cost_t(x). Grouping by period gives

    f(x) = Σ_t [cost_t(x) + λ_{t−1,D_{t−1}}·s_t(x) − λ_{t,D_t}·e_t(x)],

with no entry term for t = 0 and no exit term for t = 5. The period-t bracket
is the objective of the pair (D_{t−1}, D_t) at x's restriction to period t.
That restriction is feasible for the pair: it satisfies the period rows, the
OSIL and implied bounds, the cell boxes and, in period 5, the terminal row.
So the bracket is at least φ_t(D_{t−1}, D_t), and at least any rigorous
bound B_t(D_{t−1}, D_t). Summing over t, f(x) is at least the shortest path.
I find the argument correct. It needs exactly the following:

1. *Cover.* The leaves of link t contain every level vector that a feasible
   point can have. Checked in Section 3.
2. *One vector per cell, used on both sides.* In the bracket of period t the
   exit vector is λ_{t,D_t}. In the bracket of period t+1 the entry vector is
   the same λ_{t,D_t}, so the link terms cancel. It does not matter which
   cell is chosen for a point on a shared face, because both periods use the
   chosen cell. No continuity across faces is needed.
3. *Pair-dependent slopes are not allowed*, as the note says (item 4). Two
   adjacent periods would then use different vectors for the same link and
   the terms would not cancel. Offsets β_{t,D} cancel along every path (item
   5). Both statements are correct.
4. *Rigorous pair bounds*, with +∞ only for pair boxes that are really
   empty. Checked in Section 5.

The facts the argument uses about the model hold. The objective is a sum of
cost variables, each in exactly one period. Every row other than the
horizon row is a period row or a link row. These two facts come from the
earlier review's `check_rows.py`. The terminal row
1/2·x253 + 1/5·x265 + 4/9·x277 ≥ 3913/900 is implied by the rows; I re-ran
the earlier review's independent derivation for T = 6.

**Relation to Definition 1.2 (note Sections 2 and 6.7).** Read as an
instance of that definition, the certificate has cell minorants that jump
across cell faces. Condition (CM) of the definition then holds on a shared
face only through the "touching pairs" remark after Lemma 1.3 of the
decomposition note. The note's direct proof of Proposition 1 does not need
that remark, so this affects only the cross-reference.

**Does the code use one vector per cell on both sides?** Yes:

- `verify_cs.py`, the authors' exact check, builds one array per link,
  `lam[l]`, from `st.lam[l][leaf]`. It uses `lam[t−1][rows]` for the entry
  correction of period t and `lam[t][cols]` for the exit correction of
  period t. So link l's array serves period l (exit) and period l+1 (entry).
- My own DP (`ind_verify_cs.py`) is written the same way, with one array
  `LAM[l]` per link. Every leaf has one finite float vector.
- *Cells split after their slopes were set.* `cs.State.split` copies the
  parent's vector to both children. Later slope steps change the children
  only. The DP never uses an interior (non-leaf) node's slope. Records made
  on the parent box keep their own stored slopes (`lam_in`, `lam_out`).
  They reach the leaves only through the Lemma-2 correction, from the
  record's slopes to the leaf's slopes over the leaf box. So the bound does
  not depend on the order in which cells were split and slopes changed. My
  check selects records by box containment over all records and never
  consults the split tree or the order of events.
- *Last period.* Period 5 has an entry term only. All 77,249 records store
  lam_out = 0 for t = 5 and lam_in = 0 for t = 0, so no record carries a
  slope on a side that does not exist. rbb's period-5 model includes the
  terminal row (`certify_cs.py` starts its workers with
  `cs.init_worker(T, implied, True)`, which calls
  `terminal.add_terminal_row`). My vbb2 driver adds the terminal row with
  outward-rounded float coefficients for propagation and exact coefficients
  for the LP rows.
- *Exact link-term cancellation.* At p1–p4, along each point's cell path,
  I checked exactly that the sum of the six period values at the leaf slopes
  equals f(x) + Σ_t λ_{t,D_t}·(link-t residual). The residuals are exactly
  0 in the .sol files (Section 6).

## 2. Lemma 2 (reusing a bound proved at other slopes on a containing box)

**Re-derivation.** Let record r satisfy

    B_r ≤ min { cost_t + a·s − a'·e : x in period t's set, s ∈ A, e ∈ A' }.

Let D ⊆ A and D' ⊆ A' be leaves with slopes l and l'. A point feasible for
(D, D') is feasible for (A, A'). Its pair objective is the record objective
plus (l − a)·s − (l' − a')·e. For s ∈ D and e ∈ D', that added term is at
least

    Σ_k min((l_k − a_k) lo_k, (l_k − a_k) hi_k) + Σ_k min(−(l'_k − a'_k) lo'_k, −(l'_k − a'_k) hi'_k),

because a linear function on a box is minimized coordinate by coordinate at
an endpoint. The feasible levels form a subset of the box, and restricting
to a subset can only raise the minimum, so the bound stays valid. If B_r = +∞, the record's box is empty, so
every sub-box is empty and φ_t(D, D') = +∞. The lemma is correct as stated.

The note's remark is also correct. If both records on link t used the same
old slope a, the exit correction of period t and the entry correction of
period t+1 at the same cell add up to

    Σ_k [min(d_k lo_k, d_k hi_k) − max(d_k lo_k, d_k hi_k)] = −Σ_k |d_k| (hi_k − lo_k).

**The code's exact evaluation.** `verify_cs.py` evaluates

- the entry correction as
  `d = F(float(lam[t−1][r,k])) − F(rec["lam_in"][k])`, followed by
  `min(d·F(lo), d·F(hi))`;
- the exit correction as `d = F(float(lam[t][c,k])) − F(rec["lam_out"][k])`,
  followed by `min(−d·F(lo), −d·F(hi))`.

The leaf boxes and slopes are taken from the leaves on the correct side:
link t−1 for the entry and link t for the exit. Every slope and box end is
a float, so the evaluation is exact. My own implementation
(`ind_verify_cs.corr_exact`) is written separately. It gives the identical
exact DP value (Section 4). It also finds the same number of corrected leaf
pairs, 52,826, defined as finite pair bounds that differ from their record's
bound.

Lemma 2 was also tested end to end with vbb2 (Section 5.3). Leaf pairs were
re-bounded on the leaf boxes at the leaf slopes, with the target set to the
exact corrected bound rounded down. This was done for every corrected leaf
pair on a path within 0.5 of the optimum and for 300 random corrected leaf
pairs. None failed.

## 3. Cell coverage and the link from leaf pairs to records

`ind_verify_cs.py` checks, for certB and for certA:

- **Level box ⊆ root.** For each link I computed the exact level box from
  the OSIL bounds of both copies and the first verifier's implied bounds.
  It lies inside the root cell of the link's tree on all 5 links. Example:
  link 0's root has tank-3 range [3.3324999992334576, 5.936197237759838];
  my exact box is [3.3324999992499995, 5.936197237652734].
- **Leaves partition the root.** I took all leaf breakpoints per coordinate.
  Every elementary cell of the resulting grid lies in exactly one leaf
  (multiplicity 1 everywhere), on all five links. Grid sizes go up to
  52 × 65 × 49 (link 4). Every leaf has positive width in every coordinate.
  This check does not use the split tree. The note's leaf counts are
  confirmed: 228, 154, 148, 153, 240.
- **Record fields.** All 77,249 records were checked:
  - the period lies in 0..5 and μ = 0;
  - the entry box is present exactly for t > 0 and the exit box exactly for
    t < 5, with lo ≤ hi;
  - every bound is a float that is neither NaN nor −∞;
  - +∞ occurs only with status `infeasible` (12,298 records). In `rbb.solve`,
    +∞ comes only from root FBBT, which runs without an objective cutoff.
    Section 5 re-proves all 12,298 boxes empty with vbb2.
- **Leaf pair → record.** For each of the 117,736 leaf pairs of certB, I
  considered every record of the same period whose stored entry box contains
  the entry leaf and whose stored exit box contains the exit leaf. Containment
  was checked by exact float comparison over all records, not through the
  tree. Of these records I chose the one with the largest float value of
  bound plus correction (ties go to the smallest record number) and then
  evaluated its value exactly. Every leaf pair has at least one containing
  record.
- **Agreement with the authors.** The set of records used is identical to the
  authors' `used_records`: 49,315 for certB and 48,272 for certA. This is
  expected. Every record's stored boxes equal the boxes of its tree nodes
  (all 77,249 records checked). The leaves partition the root and none is
  degenerate. So a record box contains a leaf only if the leaf lies under
  the record's node.
- **Other counts.**
  - certB: 79,919 finite and 37,817 infinite pair bounds; 52,826 corrected.
  - certA: 80,248 finite and 37,488 infinite; 47,295 corrected.
  - Distinct slope vectors per link: certB 101, 130, 135, 139, 174;
    certA 91, 125, 132, 133, 152.
  - Every leaf's slope differs from the wave-2 slope of its link in at least
    one coordinate.

## 4. Exact DP

Shortest path in `Fraction` arithmetic, own code:

| certificate | exact value (own code) | rounded down | authors' value | minimizing leaf path |
|---|---|---|---|---|
| certB | 39157472136693483/140737488355328 | **278.230573774** | identical | [124, 139, 131, 5, 220] |
| certA | 2437338627747397/8796093022208 | 277.093321045 | identical | [207, 142, 29, 88, 52] |
| cert3 state (`state0.pkl.gz`) | 19181443079783745/70368744177664 | 272.584700834 | identical (and equal to the earlier review) | [52, 27, 105, 30, 148] |

certB's minimizing path uses records 52772, 52771, 52856, 53013, 52936 and
53069. All six are certB rbb runs at exactly the leaf boxes and leaf slopes,
so they need no correction. Their bounds (−615.3962, 59.5099, 68.8988,
59.8840, 60.3246, 645.0095) agree with the note's table in Section 5.1. So
do the exit cells and exit slopes. The wave-2 slopes in the same table match
the folded slopes stored as `base` in the pickle.

## 5. Independent re-bounding with vbb2

### 5.1 Method

`vrebound_cs.py` is my own driver. It uses the first verifier's model
(`vmodel`, `vbb.Period`) with the recheck's outward-rounded float
propagation (`vbb2.PeriodF`). Node bounds are evaluated exactly in
`Fraction` arithmetic, and root OBBT runs without an objective cutoff.

- **Objective.** cost_t + lam_in·x_start(t) − lam_out·x_end(t), built by
  `vmodel.period_objective`. The coordinates follow the verifier's link
  list.
- **Bounds.** OSIL bounds and the first verifier's implied bounds,
  intersected with the task's entry box (on the start copies, link t−1) and
  exit box (on the end copies, link t).
- **Last period.** The terminal row is added to the exact LP rows and to the
  float propagation rows (lower side rounded down).
- **Tasks.**
  - Record tasks use the record's stored boxes and slopes. The target is the
    rbb bound, or 10⁴ for records with bound +∞.
  - Leaf tasks use the leaf boxes and the leaf slopes. The target is the
    exact DP pair bound, rounded down to a float.
- **Settings.** Node limit 10⁶ and time limit 900 s per task.

`vbb.solve` reports "infeasible" only when propagation or OBBT, both without
an objective cutoff, prove the box empty. It reports "certified" only when
its bound equals the target.

The tasks were ordered as follows: the minimizing path; records and leaf
pairs on paths within 0.05 of the optimum; the same within 0.5; 300 random
corrected leaf pairs; then all other used records in random order. In the
end every task ran, so the order only mattered as insurance.

A leaf task was dropped when it was identical to its record's task (same
boxes, same slopes, hence the same target). This was the case for 3,912 of
the 4,168 leaf pairs within 0.5 of the optimum, including all 208 within
0.05. Those leaf pairs use fresh certB or certA runs at exactly their own
cells and slopes.

The run used 24 single-threaded workers, 12:07–14:36 (8,971 s wall), plus a
first launch of about 6 minutes. I stopped that first launch to remove the
duplicate leaf tasks, then resumed: the output is keyed, so finished tasks
were not repeated. The 996 results of the first launch are kept; 497 of them
are the duplicate leaf tasks, all certified. The stop left broken-pipe
tracebacks in the `.out` file before the resume line; there are none after
it.

The machine was not idle. Another job ran 10–18 processes until about 13:50,
so the per-task times are inflated by up to about 2×.

### 5.2 Records used by the DP

Sources: `logs/rebound_summary.log`, `logs/rebound_breakdown.log`, and
`logs/rebound_certB_all.jsonl.gz`.

| period | records | certified at the rbb bound | box proved empty by vbb2 | failed |
|---|---|---|---|---|
| 0 | 228 | 87 | 141 | 0 |
| 1 | 9,127 | 5,153 | 3,974 | 0 |
| 2 | 11,944 | 8,346 | 3,598 | 0 |
| 3 | 11,504 | 8,771 | 2,733 | 0 |
| 4 | 16,272 | 11,302 | 4,970 | 0 |
| 5 (terminal row) | 240 | 240 | 0 | 0 |
| **total** | **49,315** | **33,899** | **15,416** | **0** |

By origin, 5,158 cert3, 19,679 certA and 24,478 certB records were
re-bounded, which is all of them.

- **rbb bound +∞ (12,298 records).** vbb2 proved every one of these boxes
  empty.
- **Finite rbb bound (37,017 records).** vbb2 certified 33,899 at exactly
  the rbb bound and proved the other 3,118 boxes empty. All 3,118 are
  records that rbb closed at the root with 0 nodes and bound equal to the
  target, through OBBT with the objective cutoff. 2,256 of them have
  targets ≥ 1,000 (pairs that SCIP had reported infeasible). This matches
  what the earlier review found for cert3.
- **Records near the optimum.** All 6 path records and the 202 other
  records within 0.05 were certified. Within 0.5: 3,954 certified and 3
  proved empty.
- **Runs below target** (rbb node limit). The two certB runs below target
  (records 76211 and 77248) are used by the DP with their lower rbb bounds,
  and vbb2 certified those bounds. The two certA runs below target are not
  used by certB.
- **Run statistics.** vbb2 CPU was 214,979 s for the record tasks. Median
  1.55 s, 99th percentile 33.5 s, longest run 123.2 s, at most 3,257 nodes.
- **Agreement with other vbb2 runs.**
  - The authors' cross-checks re-bounded 2,293 distinct certB records. My
    status agrees on all of them (1,663 certified, 630 empty).
  - The earlier review re-bounded all 5,158 cert3 records that certB uses.
    My status agrees on all of them (3,029 certified, 2,129 empty).
  - `logs/compare_other_runs.log`.

**Exact DP from vbb2 values only.** Each leaf pair takes its record's vbb2
value:

- the certified value (= the rbb bound);
- +∞ where vbb2 proved the record box empty.

My exact Lemma-2 correction from the record's slopes to the leaf slopes is
then added. The shortest path in `Fraction` arithmetic is
39157472136693483/140737488355328 = 278.230573774 (rounded down), identical
to the authors' value.

### 5.3 Leaf pairs at the DP's slopes (Lemma 2 end to end)

There were 556 leaf tasks that differ from their record's task. Every one
has a nonzero correction, from −91.7360 to +160.6369
(`logs/leaf_corrections.log`).

| group | runs | certified at the exact corrected bound | leaf box proved empty | failed |
|---|---|---|---|---|
| leaf pairs on paths within 0.5 of the optimum whose record differs (25 cert3 records, 231 certA records) | 256 | 255 | 1 | 0 |
| random corrected finite leaf pairs anywhere in the DP (259 cert3, 41 certA records) | 300 | 181 | 119 | 0 |

These runs use the leaf boxes and the leaf slopes directly. So they test the
records, the correction formula, its sign and the bookkeeping of which slope
belongs to which side all at once. CPU: 3,395 s, longest run 83.6 s.

## 6. Feasible points p1–p4 and a negative control

`point_check_cs.py` (own code) works on the exact `.sol` values. For each
point and period, it evaluates the exact period Lagrangian value at the leaf
slopes for every leaf pair that contains the point's levels and compares it
with the exact pair bound (record plus correction). Every point lies in
exactly one leaf per link.

| point | f(x) | certB: sum of pair bounds along x's cells | certB smallest margin | certA sum | certA smallest margin |
|---|---|---|---|---|---|
| p4 | 282.888037 | 280.436037 | 0.0104 | 279.984082 | 0.0104 |
| p3 | 285.226595 | 279.408535 | 0.0098 | 279.388771 | 0.0098 |
| p2 | 287.243774 | 281.621985 | 0.0101 | 280.369763 | 0.0101 |
| p1 | 307.045516 | 291.201057 | 0.0113 | 290.145567 | 0.0212 |

All margins are positive, and the sums and margins equal the note's
Section 5.3. As said in Section 1, the telescoping identity holds exactly
along each point's cells.

**Negative control** (`control_cs.py`, `logs/control_p4_certB.jsonl`).
Suppose the driver over-constrained the pair problem, for example by
putting a box on the wrong copy or using the wrong slope sign. Then vbb2
could certify values above the true pair minimum. For each of the six leaf
pairs on p4's cell path, I asked vbb2 to certify p4's exact period value
(at the leaf slopes) plus 0.01, with a 120 s limit. It certified none of
them. Its final bounds lie below p4's values: by 4·10⁻⁵ in period 0,
0.035 in period 1, 0.16 in period 2, 1.58 in period 3, 0.033 in period 4
and 5·10⁻⁴ in period 5.

## 7. Reported numbers, negative results and "not established"

I compared the note's numbers with the logs and pickles (`record_stats.py`,
`logs/record_stats_cert{A,B}.log`). Unless an item below says otherwise,
they agree.

- **Section 5.1 table.**
  - Runs: 43,140 = 32,951 at target + 10,187 proved empty + 2 below target;
    24,478 = 24,147 + 329 + 2.
  - rbb CPU: 99,680 s and 54,859 s. Longest runs: 270.1 s and 217.5 s.
    Nodes: 6.37 M and 4.39 M. cert3: 25,308 s, 35 s, 1.89 M.
  - The four below-target runs have the stated targets and bounds (all in
    period 4, 20,000 nodes). Their bounds are valid lower bounds. The two
    certB runs are used by certB, and vbb2 certified them (Section 5.2).
  - rc=False retries: 5 in certA and 4 in certB; all reached their targets.
  - Used records by origin: certB 5,158 / 19,679 / 24,478; certA 5,132 /
    43,140. Every certB run is used.
  - Rigorous DP before the runs: 243.097042 (certA) and 259.330233 (certB).
    SCIP refreshes: 7,369 and 7,266 pairs, without a change of V_E.
  - Medians: 0.85 s and 1.08 s. 99th percentiles: 16.6 s and 13.0 s
    ("median about 1 s; 99% under 17 s").
- **Sections 5.2 and 6.6.** The slope statistics agree with my
  recomputation from the pickle: medians, maxima and ranges per link
  (`logs/scip_slope_stats.log`). On every link, 12–21 leaves still span the
  whole tank-1 range [2, 5] with a tank-2 width of at least 0.83.
- **Section 6.5 (SCIP).** In `certB.pkl.gz`, 76,318 SCIP evaluations are not
  in `state0.pkl.gz`, and none of the 12,922 cert3 evaluations was
  overwritten. These new evaluations took 201,353 CPU-s in total, with a
  median of 1.15 s. 1,341 of them hit the time limit and 6,846 reported
  infeasibility. rbb reached its target in 67,614 of 67,618 runs. Planning
  and certified values differ by 0.0506 for both certificates.
- **Section 8 (costs).** SCIP CPU by stage is consistent with the stored
  evaluation counts and CPU totals of `stats_planF/certA/planG/certB.log`:
  - 18,259 + 124,857 = 143,116 s up to planF;
  - 20,155 s for the certA refresh;
  - 16,166 s for planG;
  - 21,917 s for the certB refresh.

  The totals check out: SCIP 201,353 s, rbb 154,539 s, vbb2 8,775 s (710.8 s
  for certA plus 8,064.5 s for certB), together 364,667 s ≈ 101 CPU-hours.
- **Planning logs (Sections 3, 5.5, 6.1).**
  - Global LP: 1 of 5 steps was accepted, with +0.23 (planA iteration 2,
    272.6352 → 272.8669). The other four lowered the planning value. LP
    sizes were 110,463–315,633 rows and 3–39 s.
  - `diag_lpstep.log`: per-period prediction errors of 0.000–0.456.
  - The stale-value failure: 276.0956 → 273.1891 after a split round. At
    the 22:02 restart the value went from 275.3814 to 256.1303, and to
    275.5760 after 9,010 evaluations (about 34 min of lazy rounds).
  - Every gain and evaluation count in the 6.1 table matches `planC.log` and
    `planG.log`. For example, slope cycle 1 gave +0.825 for 5,803
    evaluations and the pessimistic cycle +1.383 for 8,134. Totals: planA
    9,470, planB 2,947, planC 39,815, planG 9,451.
- **"Not established" (Section 6.1).** The claim is supported, and stated
  with appropriate caution. Per 1,000 SCIP evaluations, slope cycles gained
  0.12–0.22. The two split rounds that gained gave 0.20 and 0.08. Two other
  split rounds lost value (−0.10, and −2.91 when the stale values were
  exposed). The rates are of the same order, and the phases are confounded
  by their order and, before the 22:02 restart, by stale estimates. No controlled comparison was run. The
  6.1 table counts SCIP work only. Slope changes also cost far more rbb
  certification: 67,618 runs and 154,539 CPU-s, against 9,631 runs and
  25,308 s for cert3, which gained less. If certification cost were
  included, it would weigh against slopes rather than for them. Section 6.4
  of the note says this.
- **Other summary claims.**
  - The gap is 4.657 = 1.674% of the dual (1.646% of the primal).
  - The bound closes 5.646 of 10.303 = 54.8% ("55%").
  - certA's gap is 2.09%.
  - "Along p4's cells the bound is still 2.5 below p4's value": 2.452.
  - "waterno2_09 not attempted": no waterno2_09 code or log exists in
    `cellslopes/`.

## 8. Issues

None affects the certified value.

1. **Out-of-date statements after this review.**
   - Status line: "not independently reviewed".
   - Summary and Section 5.4: "The other new records rest on the reviewed
     `rbb.py` alone; a full independent re-bounding … was not done".

   All 49,315 records used by certB have now been re-certified with vbb2
   (Section 5). The note could cite this review.
2. **Counts of the authors' re-bounding (Summary, Section 5.4).**
   - "2,307 of the 44,157 new records" counts runs. The distinct records
     number 2,293: 3 records were drawn by both random samples, and 11
     records of the 2,000-sample were also in the near-optimal group.
   - The table row "99 + 2,000 | 1,467 | 632" also counts runs. The 2,096
     distinct random records split into 1,466 certified and 630 empty.
3. **Section 8, "the planning SCIP runs (56%)".** 201,353 s is all SCIP work,
   including the two pre-certification refreshes, and is 55.2% of the total.
   Planning SCIP alone is 159,282 s, or 43.7%.
4. **Section 6.1, plan3 comparison.** `plan3.log` gives 271.2238 → 272.6353,
   a gain of +1.41, not +1.42. The rate of 0.24 per 1,000 estimates is
   right.
5. **Section 7, Füllner and Rebennack (2022).** The note says this paper was
   "found by web search; abstract only". The repository has its full text and
   a read summary in
   `literature/papers/fullner2022-non-convex-nested-benders-decomposition/`
   (added 2026-09-04). The novelty statement claims nothing, so this changes
   only the description of what was examined.
6. **Sections 2 and 6.7, relation to Definition 1.2.** With minorants that
   jump across cell faces, condition (CM) at shared faces needs the "touching
   pairs" remark after Lemma 1.3 of the decomposition note. Proposition 1's
   own proof is complete without it.
7. **Section 6.1, scope of the comparison.** The per-evaluation comparison
   counts SCIP work only. The slope route also needed 67,618 rbb runs
   (154,539 CPU-s) to certify. The note's conclusion ("not established") is
   right. A sentence saying that certification cost, if counted, would weigh
   against slopes would make the comparison complete.

## 9. What the confirmed value rests on, and what was not checked

- The OSIL data of waterno2_06, read by the first verifier's `osilx`/`vmodel`.
- The implied bounds proved by the first verifier (`my_implied_06.json`).
  vbb2 used these. rbb used the authors' file, which the first verifier
  confirmed.
- The terminal row. The authors and the earlier review derived it
  independently, and I re-ran the earlier review's derivation.
- The pair bounds. Each of the 49,315 used records is certified by `rbb.py`
  and, in this review, by `vbb2.py` (the first verifier's exact node bounds
  with the recheck's outward-rounded propagation).
- Lemma 2, re-derived here, and my exact implementation of it. It agrees with
  the authors' implementation and passed the 556 leaf-level vbb2 checks.
- My checks of coverage, record containment and slopes, and my exact DP.

**Independence.** My code shares nothing with the authors' `cellslopes/`,
`sepbranch/` or `rbb.py`. It does share the first verifier's model reader,
relaxation and node-bound code (`vbb.py`), and the recheck's propagation
(`vbb2.py`). The authors' own cross-checks and the earlier review used the
same vbb2. To invalidate the bound, an error would have to be common to
vbb/vbb2 and to rbb, which is a separate code base.

**Not checked.**

- I did not re-run the planning (`plan_cs.py`, `plan_bc.py`), the SCIP
  evaluations or the rbb certification. I did not line-review `cs.py`,
  `plan_bc.py` or `certify_cs.py`. Their correctness is not needed for
  validity, because the checks above cover everything the bound uses.
- I did not re-run `diag_lpstep.py` or the authors' cross-checks. I compared
  their logs.
- I did not review `rbb.py` or `vbb2.py` again.
- I searched the literature only to check the sources the note cites.

## 10. Files and commands

Folder `reviews/waterno2-cellslopes-review-checks/`:

- `load_cs.py`: reads the pickles through a stub class.
- `ind_verify_cs.py`: record fields; level box and partition; slopes; leaf
  pair → record by box containment; exact Lemma-2 corrections; exact DP;
  near-optimal sets.
- `record_stats.py`: record counts, statuses, CPU, retries, use by the DP.
- `point_check_cs.py`: checks at p1–p4, including the exact telescoping
  identity.
- `control_cs.py`: negative control at p4's cells.
- `make_selection.py`: task list for the re-bounding.
- `vrebound_cs.py`: vbb2 re-bounding driver.
- `summarize_cs.py`: status counts and the exact DP from vbb2 values only.
- `breakdown_cs.py`: breakdown by period and group.
- `leafcorr_cs.py`: correction sizes of the leaf checks.
- `scip_slope_stats.py`: SCIP-evaluation counts and slope statistics.
- The check that every record's stored boxes equal its tree-node boxes was
  an inline command; its result was 0 differences in 77,249 records.
- `logs/`: outputs. The four large files are gzip-compressed; gunzip them
  before re-running the scripts that read them.

Commands, run from that folder with `OMP_NUM_THREADS=1
PYTHONDONTWRITEBYTECODE=1`. The variables are:

- `CS` = `open-instances-wave2/waterno2/cellslopes/logs`;
- `D` = `open-instances-wave2/waterno2/data`;
- `PR` = `reviews/waterno2-sepbranch-review-checks/logs/rebound_cert3_all.jsonl`;
- `C3` = `open-instances-wave2/waterno2/sepbranch/logs/cert3.pkl`.

```
python3 ind_verify_cs.py $CS/certB_cert.pkl.gz logs/ind_verify_certB.json $CS/certB_verify.json   # logs/ind_verify_certB.log
python3 ind_verify_cs.py $CS/certA_cert.pkl.gz logs/ind_verify_certA.json $CS/certA_verify.json   # logs/ind_verify_certA.log
python3 ind_verify_cs.py $CS/state0.pkl.gz /tmp/ind_verify_state0.json $CS/verify_state0.json     # logs/ind_verify_state0.log (json not kept)
python3 record_stats.py $CS/certB_cert.pkl.gz logs/ind_verify_certB.json                          # logs/record_stats_certB.log (same for certA)
python3 point_check_cs.py $CS/certB_cert.pkl.gz logs/ind_verify_certB.json $D/waterno2_06.p{4,3,2,1}.sol   # logs/point_check_certB.log (same for certA)
python3 control_cs.py $CS/certB_cert.pkl.gz $D/waterno2_06.p4.sol logs/control_p4_certB.jsonl 120
python3 vrebound_cs.py $CS/certB_cert.pkl.gz logs/sel_smoke.json logs/rebound_smoke.jsonl 12 300   # smoke test, 6 path records + 6 path leaf pairs
python3 make_selection.py $CS/certB_cert.pkl.gz logs/ind_verify_certB.json logs/sel_certB.json 300   # logs/make_selection.log
python3 vrebound_cs.py $CS/certB_cert.pkl.gz logs/sel_certB.json logs/rebound_certB_all.jsonl 24 900   # logs/rebound_certB_all.out
python3 summarize_cs.py $CS/certB_cert.pkl.gz logs/ind_verify_certB.json logs/rebound_certB_all.jsonl $PR $C3   # logs/rebound_summary.log
python3 breakdown_cs.py $CS/certB_cert.pkl.gz logs/sel_certB.json logs/rebound_certB_all.jsonl   # logs/rebound_breakdown.log
python3 leafcorr_cs.py $CS/certB_cert.pkl.gz logs/sel_certB.json logs/rebound_certB_all.jsonl    # logs/leaf_corrections.log
python3 scip_slope_stats.py $CS/certB.pkl.gz $CS/state0.pkl.gz $CS/certB_cert.pkl.gz             # logs/scip_slope_stats.log
(cd ../waterno2-sepbranch-review-checks && python3 terminal_allT.py 6)                            # logs/terminal_T6_rerun.log
```

A few files were written by inline commands:

- `logs/sel_smoke.json`: the 6 path records and the 6 path leaf pairs;
- `logs/compare_other_runs.log`: comparison with the authors' and the earlier
  review's vbb2 statuses.

The first launch of `vrebound_cs.py` used an earlier version of
`make_selection.py` that still contained the duplicate leaf tasks (Section
5.1). My CPU use: about 215,000 s of vbb2 for the records, 3,400 s for the
leaf checks, 660 s for the control, and a few minutes for the exact checks.

Only targeted checks were run. No project-wide checks were run and no CI
results were consulted.
