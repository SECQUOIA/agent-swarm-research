# waterno2_06: separator branching on the tank-level links

Date: 2026-09-30. Status: computational result, independently verified.
The dynamic program over the certified pair bounds was recomputed exactly
(`verify.py`), and a sample of the pair bounds, including every pair on the
minimizing cell path, was re-certified by the recheck's independent branch
and bound (`vbb2.py`). *Root update (2026-09-30):* the independent review
[`../../reviews/waterno2-sepbranch-review.md`](../../reviews/waterno2-sepbranch-review.md)
re-checked the validity argument, the cell coverage and the record data
with its own driver (no author code), recomputed the DP exactly, and
re-bounded **all** 8,958 pair records that `cert3` uses with `vbb2.py`
(6,827 certified at exactly their rbb bound, 2,131 proved empty, none
failed). The DP recomputed from the vbb2-certified values alone equals
272.584700834, so the bound no longer depends on `rbb.py`. The review's
minor corrections are applied below and listed in Section 9.

Code and logs: [`sepbranch/`](sepbranch/). Runs were single-threaded
processes (`OMP_NUM_THREADS=1`) on the shared 36-core machine, with at most
24 worker processes at a time; wall times are indicative only.

## 1. Summary

**Result.** For waterno2_06 the certified dual bound rises from
263.735099441 (wave-2 period Lagrangian, [`report.md`](report.md)) to
**272.584700834**. The relative gap to the listed primal 282.8880374 falls from
7.26% to **3.78%**, closing 46% of the absolute gap (8.85 of 19.15). (Gaps
are (primal − dual)/dual, the convention of `report.md`; relative to the
primal they are 6.77% and 3.64%.) The
gap is not closed. Only waterno2_06 was attempted; waterno2_09–24 were not,
for lack of budget.

| stage | certified dual | gap to 282.8880374 | cells per link | rbb runs | time |
|---|---|---|---|---|---|
| wave 2 (one cell per link) | 263.735099441 | 7.26% | 1 | 6 | (report.md) |
| first certificate (`cert2`) | 271.173235159 | 4.32% | 77–101 | 5,540 | planning 24 min, certification 13 min |
| second certificate (`cert3`) | 272.584700834 | 3.78% | 113–162 | 9,631 | planning 15 min more, certification 18 min |

Both values are exact rationals rounded down to 9 decimals
(`logs/cert2_verify.json`, `logs/cert3_verify.json`); the second certificate
supersedes the first.

How the bound is built (details in Sections 2 and 3):

1. **Cells on the separators.** Each of the 5 links (the 3 tank levels at a
   period boundary) is partitioned into boxes ("cells"), stored as a binary
   split tree rooted at the link's level box.
2. **Per-pair bounds.** For every period and every (entry cell, exit cell)
   pair, the wave-2 rigorous branch and bound `rbb.py` bounds the period's
   Lagrangian subproblem with the start levels restricted to the entry cell
   and the end levels to the exit cell.
3. **Lagrangian terms within cells.** One slope per link: the wave-2 link
   multipliers with the horizon multiplier folded in (Section 2.2). Any
   floats are valid.
4. **Horizon row → terminal row.** Modulo the balance and link rows, the
   horizon row is exactly the condition "final stored volume ≥ initial
   volume". This row is derived in exact arithmetic and added to the last
   period, so the horizon row needs no multiplier (Section 2.2).
5. **Dynamic programming.** The bound is the shortest path over the cell
   pairs, recomputed exactly in rational arithmetic.
6. **Refinement.** SCIP estimates of the pair values (planning only) drive a
   DP over estimates. Cells on near-optimal estimated paths are split between
   the two copies of the levels that the pair solutions place in the same
   cell. rbb then certifies every pair at a target derived from the
   estimates (Section 3.2).

What failed or did not help (Section 5):

- Slopes equal to the KKT multipliers at the best known point p4 (the
  recipe of Theorem 3.4 in the decomposition note) are excellent on cells
  around p4's trajectory (SCIP estimates 282.35–282.66 of 282.89 along p4) but poor
  elsewhere. On a uniform 54–72-cell grid, the estimated DP value was only
  223.0. This run took 101 min on 16 workers and was abandoned.
- The first, purely rigorous refinement loop, starting from one cell per
  link, gained only +1.4 in 9 minutes.
- Exploiting that the periods repeat would cost more than it saves at the
  cell widths we can afford (Section 5.4). The periods differ in the demand,
  and the good slopes differ from link to link.
- SCIP gave inconsistent "optimal" values on one pair (55.690 vs 65.124),
  and it is slow on pairs with wide cells (mean about 8 s).
- `rbb.py` has a strength defect (not a validity defect). It keeps the bound
  of a node whose LP point falls outside the box after reduced-cost
  tightening. This affected 3 of 5,538 runs in `cert2`; a retry without
  reduced-cost tightening fixed the two that mattered (Section 5.6).

## 2. The bound

### 2.1 Cells and the chain dynamic program

Notation (waterno2_06, T = 6):

- Period t has start levels s_t (copies of link t−1; fixed in period 0) and
  end levels e_t (copies of link t; free in period 5).
- The link rows are s_{t+1} = e_t, for t = 0..4.
- Slope terms for the fixed start of period 0 and the free end of period 5
  are absent (λ_{−1} = λ_5 = 0).
- cost_t is the sum of period t's 9 pump-cost variables.

For each link t let P_t be the leaves of its cell tree. The leaves are closed
float boxes covering the link's level box B_t. B_t is the intersection of the
OSIL bounds (widened outward by one ulp, as in rbb) and the implied bounds of
both copies (`core.level_box`).

Fix one slope vector λ_t ∈ R³ per link and μ = 0. For a period t, an entry
cell D ∈ P_{t−1} and an exit cell D' ∈ P_t, the **pair value** is

    φ_t(D, D') = min cost_t(x) + λ_{t−1}·s_t(x) − λ_t·e_t(x)
                 over period t's rows, the OSIL bounds and the implied bounds,
                 with s_t(x) ∈ D and e_t(x) ∈ D'
                 (period 5 also has the terminal row of Section 2.2).

**Claim.** For any rigorous lower bounds B_t(D, D') ≤ φ_t(D, D'),

    optimum of waterno2_06 ≥ min over cell sequences (D_0, …, D_4) of Σ_t B_t(D_{t−1}, D_t).

*Proof.* Let x be exactly feasible and let D_t be a leaf of P_t that
contains x's link-t levels. Such a leaf exists because x's levels satisfy
both copies' bounds, so they lie in B_t, and the leaves cover B_t. The link
rows give Σ_t λ_t·(s_{t+1}(x) − e_t(x)) = 0. Hence

    f(x) = Σ_t [cost_t(x) + λ_{t−1}·s_t(x) − λ_t·e_t(x)].

Each bracket is the pair objective at the restriction of x to period t. That
restriction is feasible for the pair (D_{t−1}, D_t): x satisfies the period
rows, the implied bounds (valid for every feasible point) and, in period 5,
the terminal row (implied by the rows). So each bracket is at least
B_t(D_{t−1}, D_t). □

This is the decomposition note's certificate (its Definition 1.2 and
Lemma 1.5) for the path of periods, with one slope per separator. Each
"leaf" of a period is the product of one entry cell and one exit cell with
the whole period box. A full rbb run replaces the convex program of
Lemma 1.3.

**Inheritance.** When a cell is split, both children keep the parent's
slope. A pair of child cells therefore has a subset of the parent pair's
feasible set with the same objective, so any bound proved for an ancestor
pair is valid for it. `verify.py` checks this ancestor relation for every
leaf pair.

### 2.2 The horizon row is a terminal-volume row

For each period and tank, the balance rows read

    area·(e − s) = 3600·(inflow − outflow),

and the copy rows identify the station flows. Adding the three balance rows
of every period, the link rows and the horizon row
Σ_t qA_t ≥ 1.752499999 (= Σ_t d_t exactly) gives an inequality in the final
levels only.

`terminal.py` finds the combination numerically, rounds the multipliers to
rationals and then checks the identity **exactly** in `Fraction`
arithmetic. For every T ∈ {2, 3, 4, 6, 9, 12, 18, 24} the result is

    E1/2 + E2/5 + 4·E3/9 ≥ 3913/900,  i.e.  1800·E1 + 720·E2 + 1600·E3 ≥ 15652,

where 15652 = 1800·3.5 + 720·4.1 + 1600·4: the final stored volume is at
least the initial one. The row is valid for every exactly feasible point.
It is added, scaled to integers, to the last period (`add_terminal_row`).

With this row the horizon row can be dropped. For feasible x the same
identity gives

    μ(c − Σ qA) = μ w·s_0 − μ w·e_5 + Σ_t μ w·(s_{t+1} − e_t),  w = (1800, 720, 1600)/3600.

So the horizon multiplier is equivalent to adding μ·w to every link slope
plus a price on the final volume, and that price is dominated by the hard
terminal row.

We therefore use μ = 0 and the folded slopes λ'_t = λ_t + μ·w, with the
wave-2 multipliers (`logs/mult_06_w1_impl.json`):

| link | tank 1 | tank 2 | tank 3 |
|---|---|---|---|
| 0 | 32.782 | 34.191 | 101.906 |
| 1 | 33.696 | 34.503 | 102.538 |
| 2 | 34.894 | 35.309 | 103.034 |
| 3 | 36.486 | 35.491 | 103.728 |
| 4 | 38.498 | 37.173 | 103.728 |

Rounded here for display; the certificate uses the exact float values
stored in every record.

With one cell per link, the terminal row adds +0.0008 to the wave-2 bound
(263.735935 against 263.735099, float sum of the six rbb bounds,
`logs/test1.log`). This confirms quantitatively the coupling note's
statement that the horizon row is not the bottleneck. Once the links are
exact it carries no coupling at all, because its partial sums are linear in
the level state.

### 2.3 Pair bounds

`core.PeriodBounder` builds one `rbb.Window` per period, restricts the
start and end level variables to the cell boxes (intersected with the OSIL
and implied bounds), sets the objective with `rbb.Window.objective` (exact
float coefficients) and calls `rbb.solve`. It returns a number B ≤ φ_t(D, D'),
or +∞ when the pair box is empty (after intersection or by FBBT).

`rbb.py` itself is unchanged; its rigour (outward-rounded FBBT, relaxation
constants and Neumaier–Shcherbina node bounds) was reviewed by the wave-2
verifier. What differs from wave 2 is only the box of each call and, for
retries, the existing `rc=False` switch (Section 5.6). SCIP and HiGHS supply
hints only.

### 2.4 What the certificate rests on

1. `rbb.py` (reviewed) and the new wrappers `core.py`, `tasks.py`,
   `dpcells.py`, `certify_dp.py` (not independently reviewed as code; the
   independent review re-derived their output instead: coverage, record
   data and all used pair bounds, the latter with `vbb2.py`).
2. `terminal.py`'s exact identity check, and the wave-2 implied bounds
   `logs/implied_06.json` (proved valid by the first verifier).
3. `verify.py`'s checks:
   - the cell trees partition the link boxes;
   - every leaf pair takes its bound from a record of the same period whose
     cells are ancestors of the pair's cells, whose stored boxes equal those
     cells, and whose slopes equal the plan's;
   - the shortest path is recomputed in exact rational arithmetic.
4. IEEE double arithmetic, as for wave 2.

## 3. Algorithm

### 3.1 Planning with SCIP estimates (`plan.py`)

- **Initial grid** (`logs/plan2.json`):
  - tank 1 unsplit;
  - tank 2 split at 3⅓ and 4⅙;
  - tank 3 split every 0.5 (these widths come from Section 5.3).
  - This gives 18, 21, 24, 24, 24 cells on links 0–4 and 2,076 pairs.
- **Estimates.** Every pair gets a SCIP estimate: the value of SCIP's
  incumbent (no propagation, 20 s limit) for the pair subproblem, or +∞ when
  SCIP reports it infeasible. The shortest path over the estimates is the
  predicted bound V_est.
- **Refinement.** Repeat:
  1. Take the cells on estimated paths within 0.5 of V_est.
  2. At each such cell, compare the end levels of the best entering pair's
     SCIP solution with the start levels of the best leaving pair's
     solution: the "jump".
  3. Split along the tank with the largest jump × |slope|, midway between
     the two copies (clamped to the middle 60% of the cell).
  4. Child pairs inherit the parent's estimate. They are re-estimated when
     they lie on an estimated path within 0.5 of V_est.

### 3.2 Certification (`certify_dp.py`)

Let E(p) be the estimate of pair p (+∞ replaced by 10⁴), V_E the shortest
path over E, and G = V_E − 0.05 the goal. Pair p of period t gets the target

    τ(p) = E(p) − max(10⁻⁴, 10⁻⁷|E|) − max(0, (π(p) − G)/6),

where π(p) is the best E-path value through p.

For any path, Σ (π(p) − G)⁺/6 ≤ max_p (π(p) − G)⁺ ≤ (Σ E − G)⁺. So if every
pair is certified at its target, every path has a certified sum of at least
G − Σ_p max(10⁻⁴, 10⁻⁷|E(p)|), which is G − 6·10⁻⁴ when no pair on the
path has |E| > 10³. (Corrected after review: pairs with the placeholder
E = 10⁴ get slack 10⁻³, not 10⁻⁴. This is harmless: the final value comes
from the certified bounds, and it is G − 6.0·10⁻⁴ to the printed
precision.)

- Pairs far from the optimal paths get low targets, which rbb reaches in few
  nodes.
- Pairs whose estimate was inherited are certified once, on the ancestor
  pair's box, at the maximum target of its leaf pairs. That maximum is at
  most the ancestor's estimate.
- Whatever rbb returns is a valid bound. The targets only steer the work.

### 3.3 Exact recomputation and independent re-bounding

- `verify.py` recomputes the certificate as described in Section 2.4.
- `crosscheck_pairs.py` re-bounds selected records with the recheck's
  `vbb2.py`. vbb2 has exact-rational node bounds and shares no code with
  `rbb.py`.
  - It runs on the verifier's own period model and Lagrangian objective, for
    the record's slopes.
  - The bounds are the authors' implied bounds intersected with the record's
    cells; the terminal row is added in the last period.
  - The target is the record's rbb bound.

## 4. Results

### 4.1 Certificates

| | cert2 | cert3 |
|---|---|---|
| planning estimate V_est (SCIP) | 271.223835 | 272.635301 |
| certified bound (exact, rounded down) | **271.173235159** | **272.584700834** |
| leaves per link (links 0–4) | 77, 79, 81, 89, 101 | 130, 113, 114, 124, 162 |
| leaf pairs (all periods) | 28,858 | 62,088 (46,757 bounded, 15,331 proved empty) |
| SCIP estimates / CPU time | 7,012 / 22,756 s | 12,922 / 30,311 s (plan2 and plan3 together) |
| rbb runs (certified at target / infeasible by FBBT, bound +∞ / below target) | 5,540 (4,473 / 1,064 / 3) | 9,631 (7,849 / 1,782 / 0) |
| rbb CPU time, longest run, nodes | 18,140 s, 27 s, 1.49 M | 25,308 s, 35 s, 1.89 M |
| certification wall time (24 workers) | 758 s | 1,056 s |

Planning wall times, with the grid estimates included in the first row:

- plan2: grid 534 s, then refinement 905 s (24 workers);
- plan3: a further 904 s (20 workers).

The estimate grew as follows: 265.39 on the grid, 267.49 after 83 s of
refinement, 269.74 after 359 s, 271.22 after 905 s, and 272.64 after
another 904 s. The growth slows: about +0.08 per minute at the end.

The minimizing cell path of `cert3` (pair values include the Lagrangian
terms of the folded slopes, so single periods are not pump costs):

| period | certified pair bound | SCIP estimate | exit cell (tank 1 × tank 2 × tank 3) |
|---|---|---|---|
| 0 | −593.6440 | −593.6273 | [4.250, 4.438] × [2.500, 2.976] × [3.937, 4.000] |
| 1 | 61.0976 | 61.1144 | [2.800, 3.100] × [4.167, 5.000] × [3.734, 4.000] |
| 2 | 53.9861 | 54.0028 | [2.750, 3.500] × [3.333, 4.167] × [3.750, 4.000] |
| 3 | 53.1565 | 53.1733 | [3.126, 3.825] × [4.167, 4.583] × [3.324, 3.500] |
| 4 | 49.7429 | 49.7597 | [4.264, 4.332] × [4.481, 4.673] × [2.713, 2.765] |
| 5 | 648.2456 | 648.2624 | free end (terminal row) |

- Each certified pair bound lies about 0.0168 below its estimate. This is
  the target reduction of Section 3.2 for a path whose estimates sum to
  272.685 (the E-minimal path sums to 272.635).
- The path does not follow p4's trajectory. At link 1, p4's levels are
  (4.90, 2.59, 3.35). So the remaining gap comes from other level regions,
  where the wave-2 slopes and the present cells still allow profitable jumps.
- Median leaf widths per tank are:
  - link 0: 0.19 × 0.36 × 0.04;
  - link 2: 0.95 × 0.83 × 0.23;
  - link 4: 0.07 × 0.05 × 0.04.
- On every link some leaves still span the whole tank-1 range [2, 5]
  (`logs/stats_cert3.log`).

### 4.2 Independent re-bounding

`crosscheck_pairs.py` re-bounded 24 records of each certificate with
`vbb2.py`. The sample was the 6 records on the minimizing path plus 18
random records used by the DP (seeds 1 and 2).

- **cert2:** 24/24 re-certified (23 certified at the rbb bound, 1 proved
  infeasible). The longest run took 28 s and 1,367 nodes
  (`logs/crosscheck_cert2.{out,json}`).
- **cert3:** 24/24 re-certified (21 certified, 3 proved infeasible). The
  longest run took 12 s and 679 nodes (`logs/crosscheck_cert3.{out,json}`).
- The three infeasible cert3 records are pairs SCIP had reported infeasible.
  rbb had returned its target (about 8,300) with 0 nodes, because its root
  OBBT, which runs with the objective cutoff c·x ≤ target, proved that no
  point of the box has value ≤ target (not that the box is empty; corrected
  after review); vbb2 proves them empty directly.
- The minimizing-path records of both certificates, including the
  last-period pair with the terminal row, are among the re-certified ones.

The other 8,934 records used by cert3 rested on `rbb.py` alone when this
note was written. *Root update:* the independent review re-bounded all
8,958 records used by cert3 with `vbb2.py` (see the header), so this is no
longer the case.

## 5. Negative results and failures

### 5.1 Rigorous refinement from one cell (first attempt)

`sepbranch.py` (`logs/test1.log`) refined lazily from one cell per link,
with rbb bounds only and SCIP targets per pair. It used 12 workers and
synchronous batches.

- It took 88 s for the six root pairs (263.735935).
- After 540 s, with 4–7 cells per link ([4, 6, 7, 5, 4]) and 112 rbb runs, it reached
  265.148592.
- Pairs with wide cells take 20–60 s each, and the batches were often only 1–8
  pairs. We stopped it and moved to the two-phase scheme.

### 5.2 Slopes from the KKT multipliers at p4

`explore_p4path.py` (`logs/explore_p4path.log`) sums SCIP pair values over
cells of width w centred at p4's link levels. It measures how tight the
bound is along the best known trajectory:

| w | 3 (≈ one cell) | 1 | 0.5 | 0.25 | 0.1 | 0.02 | 0 |
|---|---|---|---|---|---|---|---|
| wave-2 slopes | 263.74 | 266.61 | 278.66 | 279.57 | 280.53 | 282.12 | 282.89 |
| KKT slopes at p4 | 212.36 | 252.15 | 282.53 | 282.58 | 282.65 | 282.86 | 282.89 |

- Along p4, the gradient slopes (Theorem 3.4's recipe) leave only about 0.35
  at w = 0.5. The wave-2 slopes leave 4.2.
- On a uniform grid (3 cells in each of tanks 1 and 2, 0.5-wide cells in
  tank 3; 54–72 cells per link, 18,432 pairs), however, the estimated DP value with KKT slopes was **223.04**
  (`logs/plan1.log`). This is far below even the one-cell wave-2 bound.
- Away from p4 the KKT slopes misprice the levels, and cells of this size
  let the periods exploit it.
- The run cost 101 min on 16 workers (mean SCIP time about 5 s per pair)
  and was abandoned.

Per-cell slopes (KKT slopes near p4, wave-2 slopes elsewhere) are valid in
the same argument, provided each cell uses one slope on both sides. They
were not tried. Changing a cell's slope voids the inherited bounds of its
pairs; a corrected inherited bound loses |Δλ|·(cell width) per link.

### 5.3 Which tanks must be refined

`explore_tankwidth.py` (`logs/explore_tankwidth.log`) varies the width per
tank of p4-centred cells:

- **Tank 3 needs width ≤ 0.5.**
  - With KKT slopes, width 1 in tank 3 drops the sum from 282.5 to about
    258–260.
  - With wave-2 slopes, from 279.6 to 270.9.
  - This matches the station-D minimum flow. With station D off, tank 3
    falls by 2.25·d ≈ 0.62–0.69 per period; with it on (flow ≥ 0.24) it
    changes by at least about −0.15. So a band of end levels about 0.5 wide
    is unreachable, and wider cells mix both sides.
- **Tank 2 unsplit costs 12–25** (the other tanks at width 0.5; wave-2 and
  KKT slopes respectively).
- **Tank 1 unsplit costs 2.5–3.7** (same comparison).

### 5.4 Exploiting that the periods repeat

In waterno2_06 the periods differ only in the demand of one row. Two
consequences follow:

- One pair evaluation can serve periods 1–4 only if all links use the same
  slopes.
- The demand must also be relaxed to the interval [0.277222222, 0.294444444]
  of the middle-period demands.

`explore_repeat.py` (`logs/explore_repeat.log`) measured the cost along p4:

| cells (w1, w2, w3) | per-link KKT slopes | one common slope | common slope + demand interval |
|---|---|---|---|
| (1, 1, 0.5) | 282.35 | 278.04 | 270.45 |
| (0.5, 0.5, 0.5) | 282.53 | 279.53 | 271.94 |
| (0.25, 0.25, 0.25) | 282.58 | 280.66 | 273.07 |
| (0.1, 0.1, 0.1) | 282.65 | 281.84 | 274.25 |

- The link slopes vary by about ±2 across links (tank 1 from 33.8 to 37.5).
  A common slope loses roughly |Δλ|·w per link.
- The demand interval lets each period pick the favourable demand: 7–8
  more.
- Sharing would divide the middle-period pairs by at most 4. It is not
  worth this loss, so it was not used.
- The demand itself also blocks exact reuse (reasoning, not tested). A
  different demand is equivalent to shifting the exit cell in tank 3 by
  2.25·Δd, plus a constant from the exit slope. The entry cell is not
  shifted, because the pump heads depend on the actual start level. One
  link's cells are the exit cells of one period and the entry cells of the
  next, so a single grid cannot be shifted for both roles.

### 5.5 SCIP

- On one period-3 pair of `cert2`, SCIP claimed "optimal" at:
  - 55.689858 with no propagation;
  - 55.689773 with default settings;
  - 65.123993 with default settings and random seed shift 7.

  The third claim is wrong by more than 9 (`check_fail.py`,
  `logs/timing_notes.log`). This is consistent with the SCIP 10.0.2
  findings in `report.md`.
- 155 of the 7,012 cert2 estimates hit the 20 s time limit.
- SCIP values are used only as planning estimates and targets.
- The independent review saw further unreliable SCIP output: with
  feasibility tolerance 1e-9, SCIP declared three of the six minimizing-path
  pairs infeasible, and on the last-period pair it claimed "optimal" at
  664.15 while its default run found 648.26. The review did not resolve
  which of these claims are correct. No validity impact, since SCIP values
  only steer the work.

### 5.6 rbb: a node that cannot be branched after reduced-cost tightening

In 3 of the 5,538 `cert2` runs, rbb stopped far below its target (for
example 48.34 against 55.09) after few nodes.

- `debug_leaf.py` shows the cause. Reduced-cost tightening shrank a node box
  (a speed to [0.6, 0.6 + 10⁻¹²], some binaries to 0). The node's LP point
  then lay outside the new box, so `choose_branch` found nothing to branch
  on.
- rbb then keeps the node's pre-tightening bound as final. That bound is
  valid but weak.
- `tasks.rbb_task` now retries such runs with `rc=False` and keeps the
  larger of the two valid bounds. The two re-queued `cert2` tasks were then
  certified at their targets; the third failed run was superseded by other
  records. In `cert3` the retry fired 5 times, and all 5 retries were
  certified at their targets.
- This is a strength issue in `rbb.py`, not a validity issue. A fix would
  re-solve the node LP after tightening.

### 5.7 Budget

Total machine use for this note was about 3.6 h of wall time (14:30–18:05)
with up to 24 worker processes, roughly 60 CPU-hours of allocated worker
time. The largest single item is the abandoned KKT-slope grid (about 27
CPU-hours); the cert3 pipeline (plan2, plan3 and cert3) took about 22.
The gap was not closed within this budget, and we stopped.

Continuing the same refinement would raise the bound further, slowly
(Section 4.1). Closing the gap would need something more:

- better slopes on the near-optimal cells;
- cheaper pair bounds;
- or both.

## 6. Relation to the theory notes

- **Coupling note, Section 7.1.** It said the horizon row is not the
  bottleneck and that the gap sits in the level separators. Both are
  confirmed. The horizon row becomes a local terminal row (+0.0008), and the
  certified bound rises only by refining the 3-dimensional level cells.
- **Decomposition note, Theorem 3.4.** Its slope recipe, gradients at a
  local minimizer x̂, works as predicted near x̂: nearly the whole gap
  disappears with 0.5-wide cells around p4's trajectory. The theorem's
  assumptions (quadratic growth, one minimizer, shells growing away from x̂)
  do not hold here. A uniform grid with these slopes fails badly away from
  x̂ (Section 5.2).
- **Decomposition note, Proposition 2.6.** The proposition says that wrong
  slopes (there, zero slopes) leave a first-order copy error that only cell
  refinement removes. The wave-2 slopes are approximately optimal for one
  cell per link, but near p4 they are wrong slopes in this sense: along p4
  they give 280.5 at w = 0.1, against 282.65 with gradient slopes.

## 7. Literature examined and novelty

Examined for this note:

- Carøe and Schultz, "Dual decomposition in stochastic integer programming",
  Oper. Res. Lett. 24 (1999; journal details from memory). Only the ZIB
  preprint page and search summaries were seen. It dualizes
  copy (nonanticipativity) constraints and branches on the copied
  first-stage variables, with Lagrangian bounds per node. Our scheme is the
  chain analogue: cells on the copies of the state, one Lagrangian slope per
  link, and DP across stages.
- Ghaddar, Naoum-Sawaya, Kishimoto, Taheri and Eck, "A Lagrangian
  decomposition approach for the pump scheduling problem in water
  networks", EJOR 241(2) (2015). Abstract only. It decomposes a pump
  scheduling problem with Lagrangian relaxation and pairs it with a primal
  heuristic.
- Gleixner, Held, Huang and Vigerske, "Towards globally optimal operation of
  water supply networks", NACO 2(4) (2012), and Huang's 2011 master's thesis:
  the origin of waterno2 (MINLPLib page). Abstract only.
- From the decomposition note: Berenguel, Casado, García, Hendrix and
  Messine (2013), the star-shaped precursor of cell-wise copy bounds.
- From memory, not re-read: Zou, Ahmed and Sun, SDDiP (Math. Program.
  2019), which uses local copies of the state and Lagrangian cuts in nested
  decomposition.

Novelty is not claimed. Each ingredient is standard:

- Lagrangian relaxation of state copies, branching on the copied
  variables and DP over stages;
- per-pair spatial B&B bounds;
- aggregating a horizon constraint into a terminal state constraint.

We did not find this combination, with rigorous per-pair bounds and
estimate-driven targets, in the few sources examined, but the search was
brief. The certified value for waterno2_06 is higher than every dual bound
listed on MINLPLib (the best is 165.19, SCIP) and than the wave-2 bound;
other publications were not searched for bounds on this instance.

## 8. Files, commands and checks

Code in `sepbranch/`:

- Certificate path:
  - `core.py`: pair bounds via `rbb.py`; level boxes.
  - `terminal.py`: exact terminal row.
  - `dpcells.py`: split trees, tables and DP.
  - `tasks.py`: SCIP and rbb worker tasks.
  - `plan.py`: planning and refinement.
  - `certify_dp.py`: targets and rbb runs.
  - `verify.py`: exact recomputation.
  - `crosscheck_pairs.py`: vbb2 re-bounding.
  - `stats.py`: tables.
- First attempt: `sepbranch.py` (with `inspect_state.py`).
- Exploration (SCIP estimates, not bounds):
  - `explore_p4.py`, `explore_lagr.py`, `explore_p4path.py`,
    `explore_tankwidth.py`, `explore_repeat.py`;
  - `t_pair_timing.py`, `t_levels.py`, `t_scip_sample.py`;
  - `check_fail.py`, `debug_leaf.py`, `inspect_plan.py`.
- Smoke test: `test_crosscheck.py` (`logs/test_crosscheck.log`). rbb and
  vbb2 both certify two p4-centred pairs. vbb2 does not certify SCIP + 0.05
  on either pair, and its bounds there (83.9291, 542.9717) lie above SCIP's
  feastol-10⁻⁶ values (83.9281, 542.9714). SCIP's loose-tolerance points lie
  slightly below the exact minima, as the recheck also found.

Logs in `sepbranch/logs/`:

- configs `*.json`;
- `plan{1,2,3}.{log,pkl}`, `cert{2,3}.{log,pkl}`, `cert{2,3}_verify.json`,
  `verify_cert{2,3}.log`;
- `crosscheck_cert{2,3}.{out,json}`;
- `stats_cert{2,3}.log`;
- `test1.{log,pkl}`, `explore_*.log`, `timing_notes.log` (terminal outputs
  copied for the record).

Commands actually run (from `sepbranch/`, `OMP_NUM_THREADS=1`):

```
python3 terminal.py 2 3 4 6 9 12 18 24
python3 sepbranch.py logs/test1.json                  # first attempt, stopped at 540 s
python3 plan.py logs/plan1.json                       # KKT slopes, abandoned
python3 plan.py logs/plan2.json                       # grid + 900 s refinement
python3 certify_dp.py logs/cert2.json                 # twice (the second run re-queued 2 tasks)
python3 verify.py logs/cert2.json
python3 crosscheck_pairs.py logs/cert2.json "path+random:18:1" logs/crosscheck_cert2.json 1200 8
cp logs/plan2.pkl logs/plan3.pkl; python3 plan.py logs/plan3.json   # 900 s more refinement
python3 certify_dp.py logs/cert3.json
python3 verify.py logs/cert3.json
python3 crosscheck_pairs.py logs/cert3.json "path+random:18:2" logs/crosscheck_cert3.json 1200 8
python3 explore_p4path.py; python3 explore_tankwidth.py; python3 explore_repeat.py
python3 test_crosscheck.py; python3 check_fail.py logs/cert2.pkl 2236; python3 debug_leaf.py logs/cert2.pkl 2236
```

Only targeted checks were run. No project-wide checks were run and no CI
results were consulted.

## 9. Root revision after review (2026-09-30)

From [`../../reviews/waterno2-sepbranch-review.md`](../../reviews/waterno2-sepbranch-review.md)
(verdict: verified; all issues minor). Changes: the header records the full
independent re-bounding of the 8,958 records; the gap convention is stated
in Section 1; the Section 1 bullet on p4's trajectory now says the values
are SCIP estimates; Section 3.2 states the slack correctly
(`max(10⁻⁴, 10⁻⁷|E|)` per pair); Section 4.2 describes rbb's cutoff OBBT
correctly and no longer says the other records rest on rbb alone;
Section 5.1 says 4–7 cells; Section 2.4 notes what the review re-derived;
Section 5.5 adds the review's further SCIP
observations. The certified value 272.584700834 is unchanged.
