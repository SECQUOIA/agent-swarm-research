# waterno2_06: separator branching with cell-dependent slopes

Date: 2026-09-30/10-01 (computations 20:07–02:09; revised after review
2026-10-01). Status: computational result, **independently verified**
([`../../reviews/waterno2-cellslopes-review.md`](../../reviews/waterno2-cellslopes-review.md),
verdict "verified"; its wording and bookkeeping items are applied in
Section 10, which
[`../../reviews/waterno2-cellslopes-confirm-r1.md`](../../reviews/waterno2-cellslopes-confirm-r1.md)
confirmed). Self-checks: exact rational recomputation
of the dynamic program from the stored records (own code), consistency at
the four MINLPLib points, and re-bounding of a sample of pair bounds with
the independent vbb2 (Section 4.3). The review re-checked the validity
argument, the cell coverage and the record data with its own code,
recomputed the DP exactly, and re-bounded **all** 49,315 records that certB
uses with `vbb2.py` through its own driver (33,899 certified at exactly
their rbb bound, 15,416 boxes proved empty, none failed). The DP recomputed
from the vbb2 values alone equals 278.230573774, so certB no longer rests on
`rbb.py` alone. The review's minor corrections are applied below and listed
in Section 10.

This note continues [`separator-branching.md`](separator-branching.md)
(certified dual 272.584700834 with one slope per link; independently
re-bounded in [`../../reviews/waterno2-sepbranch-review.md`](../../reviews/waterno2-sepbranch-review.md)).
Here every cell of every link carries its own slope vector. Code and logs:
[`cellslopes/`](cellslopes/). All runs were single-threaded processes
(`OMP_NUM_THREADS=1`) on the shared 36-core machine, with at most 24 worker
processes at a time (plus at most a few single-process checks); wall times
are indicative only.

## 1. Summary

**Result.** The certified dual bound of waterno2_06 rises from
272.584700834 to **278.230573774** (exact value
39157472136693483/140737488355328 in `cellslopes/logs/certB_verify.json`,
rounded down). The gap to the listed primal 282.8880374 falls from 3.78% to
**1.67%** ((primal − dual)/dual, the convention of `report.md`; relative to
the primal: 1.65%). This closes 55% of the remaining absolute gap (5.65 of
10.30). The gap is not closed. waterno2_09 (part (b)) was **not
attempted**; the budget went into waterno2_06.

| certificate | certified dual (exact, rounded down) | gap | cells per link | slopes | new rbb runs |
|---|---|---|---|---|---|
| wave 2 (`report.md`) | 263.735099441 | 7.26% | 1 | one per link | – |
| cert3 (`separator-branching.md`) | 272.584700834 | 3.78% | 113–162 | one per link | 9,631 |
| certA (this note) | 277.093321045 | 2.09% | 148–240 | 91–152 distinct vectors per link | 43,140 |
| **certB (this note, final)** | **278.230573774** | **1.67%** | 148–240 | 101–174 distinct vectors per link | 24,478 more |

certB supersedes certA. It is certA's cells after one more cycle of slope
changes (no new splits), with certA's records reused where they still give
the needed value.

**Checks of certB** (Sections 4.2, 5.3, 5.4): the DP was recomputed
exactly from the records by `verify_cs.py`, including the exact Lemma-2
corrections; the bounds are consistent with MINLPLib's four feasible points;
vbb2 (independent of rbb.py) re-certified 46 leaf pair bounds at the leaf
slopes (all six of the minimizing path and 40 random corrected ones) and
2,293 distinct records (2,307 runs) of the 44,157 new records used,
including all 208 records on paths within 0.05 of the optimum. Nothing
failed. The independent review
([`../../reviews/waterno2-cellslopes-review.md`](../../reviews/waterno2-cellslopes-review.md))
then re-bounded with vbb2, through its own driver, every one of the 49,315
records that certB uses (cert3, certA and certB runs). None failed, and the
exact DP from the vbb2 values alone gives the same value. The review also
re-bounded 556 corrected leaf pairs at the leaf slopes, which tests Lemma 2
end to end; none failed.

How the bound is built:

1. **Validity (Section 2).** With one slope vector per *cell*, the link
   terms of the Lagrangian still cancel along the cell path of every
   feasible point, provided the cell's vector is used both for the exit term
   of the period before the link and for the entry term of the period after
   it. Nothing else is required (no continuity across cells; offsets are
   irrelevant). A pair bound proved at other slopes on a larger box remains
   usable after an exact linear correction (Lemma 2).
2. **Slopes (Section 3).** For fixed slopes elsewhere, the planning value
   of the dynamic program (DP) is the minimum over the cells of one link of
   a function of that cell's slope alone. So the cells of one link can be
   improved independently: a small LP per cell over a pool of SCIP points
   proposes a slope, SCIP evaluates the affected pairs, and the slope is kept
   only where the cell's best path value rose. Cycles over the links
   alternate with the jump-based splits of the previous note.
3. **Bounds (Section 4).** rbb (unchanged, reviewed) bounds every pair that
   needs it at the pair's own two cell slopes; the other pairs reuse
   earlier records with the Lemma-2 correction. The DP is recomputed exactly.

What failed or did not help (Sections 3 and 6):

- One trust-region LP over all ~600 cell slopes at once: 1 of 5 steps
  accepted. The LP predicts the minimizing paths almost exactly, but it
  equalizes very many paths and any small error then lowers the minimum.
- Planning values for pairs whose slopes had changed were first taken as
  re-priced pool points (an upper estimate). This hid low paths: a split
  round dropped the planning value from 276.10 to 273.19. The fix (a
  pessimistic Lemma-2 estimate) cost 9,010 SCIP evaluations to re-establish
  an honest planning value (275.58).
- Changing slopes is expensive to certify: at certA's slopes, the cert3
  records with corrections alone give only 243.10, so 43,140 new rbb runs
  were needed (cert3 needed 9,631); one more slope cycle needed 24,478
  more.
- Whether cell slopes beat further splitting per unit of work is **not
  established**: the per-evaluation gains of slope steps and split rounds
  were of the same order (Section 6.1).

Costs (Section 8): about 101 CPU-hours measured inside the workers
(SCIP 201,400 s, rbb 154,500 s, vbb2 8,800 s), about 140 worker-hours
allocated, 20:16–02:09 wall with up to 24 workers.

## 2. What validity requires

Notation as in `separator-branching.md`, Section 2.1 (T = 6). Period t has
start levels s_t (copies of link t−1; fixed for t = 0) and end levels e_t
(copies of link t; free for t = T−1, where the terminal row of Section 2.2
of that note is added). The link rows are s_{t+1} = e_t. B_t is the level
box of link t. P_t is a finite family of closed boxes (cells) covering B_t;
here the leaves of a split tree rooted at B_t, so they partition it.

**Cell slopes.** Every cell D ∈ P_t carries a vector λ_{t,D} ∈ R³. The pair
value of period t on (D, D') ∈ P_{t−1} × P_t is

    φ_t(D, D') = min cost_t(x) + λ_{t−1,D}·s_t(x) − λ_{t,D'}·e_t(x)
                 over period t's rows, the OSIL and implied bounds,
                 s_t(x) ∈ D, e_t(x) ∈ D'

(no entry term for t = 0, no exit term for t = T−1).

**Proposition 1 (validity).** If B_t(D, D') ≤ φ_t(D, D') for every period t
and every pair, then

    optimum of waterno2_06 ≥ min over (D_0, …, D_{T−2}) ∈ P_0 × … × P_{T−2} of Σ_t B_t(D_{t−1}, D_t).

*Proof.* Let x be exactly feasible and y_t = e_t(x) = s_{t+1}(x) its link-t
levels. y_t ∈ B_t, so some cell D_t ∈ P_t contains it. Each link term
λ_{t,D_t}·(s_{t+1}(x) − e_t(x)) is zero, so adding all of them to
f(x) = Σ_t cost_t(x) and regrouping by period gives

    f(x) = Σ_t [cost_t(x) + λ_{t−1,D_{t−1}}·s_t(x) − λ_{t,D_t}·e_t(x)].

The period-t bracket is the objective of the pair (D_{t−1}, D_t) at the
restriction of x to period t, which is feasible for that pair (the implied
bounds and the terminal row hold at every feasible point). So it is at least
φ_t(D_{t−1}, D_t) ≥ B_t(D_{t−1}, D_t). □

**Exactly what is needed, and what is not.**

1. *Cover.* The cells of link t must contain every level vector that a
   feasible point can have at link t (here: they cover B_t).
2. *One slope per cell, used on both sides.* The exit term of period t for
   exit cell D and the entry term of period t+1 for entry cell D must use the
   same vector λ_{t,D}. This is the only coupling condition. It is what makes
   the link terms cancel along the cell path of x.
3. *Nothing else.* Slopes may differ arbitrarily between cells of one link
   and between links. No continuity across cell faces is needed: a point on a
   common face is assigned to one of the cells, and both periods use that
   cell (closed cells that overlap on faces are harmless).
4. *Not allowed:* a slope for D that depends on the other cell of the pair
   (for example a slope chosen separately for each pair (D_{t−1}, D_t)). Then
   period t and period t+1 would use different vectors for the same link
   copy and the link terms would not cancel. (Enlarging the DP state to pairs
   of cells would allow it; not done.)
5. *Offsets are useless.* An affine cell minorant λ_{t,D}·y + β_{t,D}, as in
   Definition 1.2 of the decomposition note, adds β_{t,D} to one period and
   subtracts it from the next; every path sum is unchanged. Any function
   g_{t,D}(y) used on both sides would also cancel; linear g keeps the pair
   objective linear, which is what rbb and vbb2 handle.

This is the path case of Definition 1.2 and Lemma 1.5 of
[`../../theory-decomposition/decomposition-certificates.md`](../../theory-decomposition/decomposition-certificates.md)
with cell-dependent minorants l_{t,D}(y) = λ_{t,D}·y + β_{t,D}: condition 2
says that the same l_{t,D} must appear in the child condition (CM) and in
the parent condition (LC). Read this way, the minorants of two neighbouring
cells may jump across their common face. (CM) as stated in Definition 1.2
also covers cells that only touch a leaf on a face, and a jump can violate
it there. The certificate then satisfies (CM) only in the weaker form
allowed by the "touching pairs" remark after Lemma 1.3 of that note, which
needs (CM) only for cells whose interior meets the leaf's. The direct proof
of Proposition 1 above does not need that remark.

**Lemma 2 (reusing a bound after a slope change).** Let r be a record: a
number B_r with

    B_r ≤ min { cost_t + a·s_t − a'·e_t : period t's rows and bounds, s_t ∈ A, e_t ∈ A' }.

If D ⊆ A and D' ⊆ A' carry slopes l and l', then

    φ_t(D, D') ≥ B_r + Σ_k min((l_k − a_k) lo_k, (l_k − a_k) hi_k)
                     + Σ_k min(−(l'_k − a'_k) lo'_k, −(l'_k − a'_k) hi'_k),

where [lo, hi] = D and [lo', hi'] = D'. If B_r = +∞ (box proved empty),
φ_t(D, D') = +∞.

*Proof.* A point feasible for (D, D') is feasible for (A, A'). Its pair
objective equals the record objective plus (l − a)·s_t − (l' − a')·e_t, and
the minimum of a linear function over a box is the sum of the coordinate-wise
minima at the endpoints. □

The verifier evaluates these corrections exactly in rational arithmetic
(the slopes and box ends are floats, hence rationals). Along a path whose two
records on link t used the same old slope a, the two corrections on that link
add up to −Σ_k |l_k − a_k| (hi_k − lo_k). So changing a cell's slope
without new pair bounds costs |Δλ|·width per link; it pays only if the cell's
pairs are re-bounded at the new slope where it matters.


## 3. Choosing the slopes (planning; SCIP estimates, not bounds)

Planning never produces bounds. It chooses cells and slopes and targets for
rbb, using SCIP's incumbents of pair problems as estimates (as in
`separator-branching.md`, Section 3.1; SCIP 10.0 without propagation, 20 s
per pair).

### 3.1 State

The planning state (`cs.py`) holds:

- the split trees of cert3 (130, 113, 114, 124, 162 leaves), extended by
  further splits; children inherit their parent's slope;
- one slope vector per cell (initially the folded wave-2 slope of the link);
- a **point pool** per period: every SCIP solution of every pair evaluation
  (up to 10 per run, near-duplicates removed), stored as
  (start levels, end levels, pure period cost). A pool point lies in every
  leaf pair whose cells contain its levels, and for any slopes it gives an
  upper estimate of that pair's value: c0 + λ_in·s − λ_out·e. The cert3
  estimates seed the pool;
- all rigorous records (the 9,631 cert3 rbb records and new ones). With
  Lemma 2 they give, for every leaf pair at the current slopes, a rigorous
  lower value L.

A pair is *fresh* if SCIP evaluated exactly this leaf pair at its current
slopes, and *stale* otherwise. Lemma 2 applied to SCIP values instead of
bounds gives a **pessimistic estimate** P for every pair: the maximum over
all SCIP evaluations of an ancestor-or-equal pair of (SCIP value + the
Lemma-2 corrections to the current slopes over the leaf boxes). The planning
value of a pair is

    max(L, min(U, P)),

which is about U for fresh pairs and the pessimistic estimate for stale
ones; it is +∞ if a record proved the pair empty, or if SCIP reported it
infeasible and the pool has no point in it. Lazy evaluation (as in plan.py)
evaluates the stale pairs on near-optimal paths of the planning DP until
none is left.

The pessimistic estimate was added after a failure. At first the planning
value of a stale pair was simply U, the pool points re-priced at the new
slopes. That is an *upper* estimate, and after many slope changes it hid
low paths: a split round that created new (hence evaluated) pairs dropped
the planning value from 276.10 to 273.19 (`logs/planC.log`). Switching to
max(L, min(U, P)) lowered the planning value of the same state from 275.38
to 256.13; making all stale pairs on near-optimal paths fresh then took
9,010 SCIP evaluations (35 min on 24 workers) and ended at 275.58. Only the
values obtained after that switch are used below.

### 3.2 First attempt: one trust-region LP over all slopes (failed)

For fixed cells the pool model is concave and piecewise linear in all cell
slopes (minimum over points of affine functions; pairs without points get
the pessimistic Lemma-2 model around the current slopes). Maximizing the
planning DP over the slopes inside a box |Δλ_k| ≤ δ_k is then one LP
(`cs.slope_lp`: about 600 cells × 3 slopes, 110k–320k rows, 3–40 s with
HiGHS). Steps were accepted only if the planning value after lazy
evaluation rose.

Result (`logs/planA.log`, `logs/planB.log`): planA made 3 steps over all
slopes, planB 2 steps restricted to the 120 cells nearest the optimum; 1 of
the 5 was accepted. The accepted one gained +0.23; the others lowered the
planning value (for example LP prediction 273.36, value after evaluation
272.88 against 272.98 before). Each step cost about 700–3,000 SCIP
evaluations. (These runs used the optimistic stale values of Section 3.1.)

Diagnosis (`logs/diag_lpstep.log`): on the minimizing path after a rejected
step the LP's pair predictions were nearly exact (errors 0.00–0.46). The
failure is structural: the LP equalizes very many paths at its optimum z,
and an error on any one of them pushes the minimum below the old value. The
planning DP is extremely flat (in cert3, 83–104 of the 113–162 cells of each
of links 1–4 have a best path within 1 of the optimum), so this happens at
almost every step.

### 3.3 Block-coordinate ascent with per-cell acceptance (used)

Fix the slopes of all links except link t. Every path passes through exactly
one cell D of link t, so

    V = min_{D ∈ P_t} H_D(λ_{t,D}),
    H_D(λ) = min_r [f_{t−1}(r) + φ_t(r, D; λ_r, λ)] + min_c [φ_{t+1}(D, c; λ, λ_c) + g_{t+1}(c)],

where f and g are the forward and backward DP values. H_D depends on the
slope of D only. So the slopes of the cells of one link can be improved
**independently**, and keeping a new slope only where H_D rose cannot lower
V if the values of all other pairs stay the same. (This is a statement about
the planning DP, not about bounds; in practice new SCIP points also change
other pairs' planning values a little, in both directions.)

`plan_bc.py` cycles over the links. For link t:

1. Cells with H_D within 1 of V are touched. The pairs attaining
   min_r and min_c (within 0.3) are made fresh at the current slopes.
2. For each touched cell an 11-variable LP maximizes the pool model of H_D
   over a per-cell trust region (initially (2, 2, 5) in the three tanks;
   ×1.5 after an accepted step, ×0.5 after a rejected one; at most
   (10, 10, 25)).
3. The new slopes are set; the pairs attaining In_D and Out_D are evaluated
   at the new slopes until fresh.
4. Per cell: the new slope is kept if H_D rose, else the old one is
   restored.

After each cycle over the five links, cells on near-optimal paths are split
as in plan.py (40 cells per round, at the midpoint of the two copies of the
levels in the tank with the largest |jump|·|slope|).

## 4. Certification and verification

### 4.1 Pair bounds (`certify_cs.py`)

Starting from a final planning state (`logs/planF.pkl` for certA,
`logs/planG_final.pkl` for certB), every leaf pair
gets the target rule of `separator-branching.md`, Section 3.2: with E the
planning values (BIG = 10⁴ for pairs SCIP reported infeasible), V_E the
shortest path over E and G = V_E − 0.05,

    τ(p) = E(p) − max(10⁻⁴, 10⁻⁷|E(p)|) − max(0, (π(p) − G)/6).

A pair gets no new rbb run if its present rigorous bound (cert3 records
corrected by Lemma 2, plus earlier new records) is already ≥ τ(p), or if
every path through it already has a rigorous value ≥ G (bounds only grow).
All other pairs are bounded by rbb (`core.PeriodBounder`, unchanged; the
`rc=False` retry of the previous note) **at the pair's own cell slopes**,
with τ(p) as target, node limit 20,000 and time limit 300 s. Before that,
SCIP re-evaluated, at the current slopes, every task pair with a stale
estimate whose best estimated path lies within 3 of G (certA: 7,369 pairs,
845 s; certB: 7,266 pairs, 924 s; neither changed V_E). Records from all earlier runs stay in the
state, so certB reuses certA's records wherever the slopes did not change
(and, corrected, where they did).

### 4.2 Exact verification (`verify_cs.py`)

Own code. It reads the state as plain data (it imports `cs` only to
unpickle the state class and calls none of its methods) and uses
`sepbranch/core.level_box` and `sepbranch/terminal.derive`, as the previous
note's `verify.py` did. It checks:

1. the terminal row, re-derived exactly (`sepbranch/terminal.derive`);
2. the split trees: root = the link's level box (`core.level_box`), every
   split halves one coordinate strictly inside the cell, the leaves are the
   state's leaves (so they cover the box);
3. one finite slope vector per leaf, used for both adjacent periods;
4. for every leaf pair, a record of the same period whose stored boxes
   contain the leaf boxes (float comparisons, exact) and μ = 0; the pair
   bound is the record bound plus the Lemma-2 corrections, evaluated
   **exactly in rational arithmetic**; +∞ only for records with status
   infeasible/empty;
5. the shortest path in exact rational arithmetic, rounded down to 9
   decimals;
6. at MINLPLib's feasible points p1–p4, the exact period Lagrangian value
   with the leaf slopes is ≥ the bound of every leaf pair that contains the
   point's link levels (a necessary condition that catches sign errors in
   the corrections).

On the cert3 state (no slope changed) it reproduces 272.584700834 and the
review's p4 path sum 277.648549 (`logs/verify_state0.json`).

### 4.3 Independent re-bounding (`crosscheck_cs.py`)

The independent review's driver (`reviews/waterno2-sepbranch-review-checks/rebound.py`,
first verifier's model and implied bounds, the review's own terminal row,
the recheck's vbb2 with exact node bounds; no code shared with rbb.py) was
run on:

- **leaf checks**: the six leaf pairs of the minimizing path and 40 random
  leaf pairs whose bound uses a slope correction, each with the *leaf*
  boxes, the *leaf* slopes and target equal to the exact pair bound used by
  the DP (rounded down to a float). This checks the records and Lemma 2
  together;
- the six records on the minimizing path, every other record used by a leaf
  pair on a path within 0.05 of the optimum, and random samples of the new
  records used by the DP (100 for certA; 99 and 2,000 for certB), at their
  own boxes, slopes and rbb bounds. Records with bound +∞ get target 10⁴,
  and vbb2 must then prove the box empty.

These were samples. The later review of this note re-bounded every record
that certB uses (Section 5.4).

## 5. Results

### 5.1 Certificates certA and certB

| | cert3 (previous note) | certA | certB (final) |
|---|---|---|---|
| planning value V_E (SCIP estimates) | 272.635301 | 277.143921 | 278.281174 |
| certified bound (exact, rounded down) | 272.584700834 | 277.093321045 | **278.230573774** |
| exact value | 19181443079783745/70368744177664 | 2437338627747397/8796093022208 | 39157472136693483/140737488355328 |
| leaves per link (links 0–4) | 130, 113, 114, 124, 162 | 228, 154, 148, 153, 240 | same as certA |
| distinct slope vectors per link | 1, 1, 1, 1, 1 | 91, 125, 132, 133, 152 | 101, 130, 135, 139, 174 |
| leaf pairs (finite / proved empty) | 46,757 / 15,331 | 80,248 / 37,488 | 79,919 / 37,817 |
| records used by the DP / all records | 8,958 / 9,631 | 48,272 / 52,771 | 49,315 / 77,249 |
| used records by origin (cert3 / certA / certB runs) | – | 5,132 / 43,140 / – | 5,158 / 19,679 / 24,478 |
| leaf pairs whose bound uses a Lemma-2 correction | 0 | 47,295 | 52,826 |
| new rbb runs (certified at target / proved empty / below target) | 9,631 (7,849 / 1,782 / 0) | 43,140 (32,951 / 10,187 / 2) | 24,478 (24,147 / 329 / 2) |
| rbb CPU, longest run, nodes | 25,308 s, 35 s, 1.89 M | 99,680 s, 270 s, 6.37 M | 54,859 s, 218 s, 4.39 M |
| SCIP refresh of stale task pairs before rbb | – | 7,369 pairs, 845 s wall | 7,266 pairs, 924 s wall |
| rbb wall (24 workers) | 1,056 s | 4,171 s | 2,390 s |

Sources: `cellslopes/logs/cert{A,B}.log`, `verify_cert{A,B}.log`,
`cert{A,B}_verify.json`, `stats_cert{A,B}.log`.

- The runs below target hit the node limit (20,000) on period-4 pairs
  (certA: targets 35.68 and 45.96, bounds 34.12 and 33.93; certB: targets
  35.75 and 32.35, bounds 34.12 and 20.26). Their bounds are valid and are
  used as they are. Nine runs needed the `rc=False` retry of the previous
  note; all nine then reached their targets.
- Without new runs, the cert3 records with Lemma-2 corrections give only
  243.097 at certA's slopes (float DP).
- certB is the one to cite. Its records include certA's; the slim file
  `cellslopes/logs/certB_cert.pkl.gz` (cells, slopes, records) suffices for
  `verify_cs.py` and `crosscheck_cs.py`.

The minimizing cell path of certB (pair bounds include the Lagrangian terms
of the cell slopes, so single periods are not pump costs):

| period | certified pair bound | exit cell (tank 1 × tank 2 × tank 3) | exit-cell slope | wave-2 slope of the link |
|---|---|---|---|---|
| 0 | −615.3962 | [4.175, 4.183] × [4.099, 4.108] × [3.332, 3.338] | (33.16, 37.58, 103.55) | (32.78, 34.19, 101.91) |
| 1 | 59.5099 | [3.980, 4.240] × [3.333, 4.167] × [2.670, 2.762] | (34.44, 34.50, 109.66) | (33.70, 34.50, 102.54) |
| 2 | 68.8988 | [4.430, 5.000] × [2.500, 3.009] × [2.612, 2.861] | (35.86, 35.67, 104.08) | (34.89, 35.31, 103.03) |
| 3 | 59.8840 | [2.000, 5.000] × [4.167, 5.000] × [2.500, 3.000] | (36.05, 37.35, 101.19) | (36.49, 35.49, 103.73) |
| 4 | 60.3246 | [4.092, 5.000] × [2.500, 3.333] × [2.500, 3.000] | (38.06, 36.13, 102.12) | (38.50, 37.17, 103.73) |
| 5 | 645.0095 | free end (terminal row) | – | – |

The path now runs through two wide cells (links 3 and 4; at link 3 the
whole tank-1 range). Slopes cannot remove the jumps inside such cells;
they need splitting. certB had no split round after certA (Section 6.6).

### 5.2 The slopes

certB's slopes (`cellslopes/logs/stats_certB.log`; median and maximum of
|cell slope − wave-2 slope| per tank, and the range of the cell slopes):

| link | median | maximum | slope ranges (tank 1; tank 2; tank 3) |
|---|---|---|---|
| 0 | (1.00, 1.00, 2.50) | (10.89, 5.00, 50.89) | [28.5, 43.7]; [30.0, 39.2]; [86.5, 152.8] |
| 1 | (1.00, 1.00, 2.50) | (6.08, 9.55, 17.35) | [29.0, 39.8]; [25.7, 44.1]; [85.2, 119.4] |
| 2 | (0.41, 1.61, 2.50) | (4.86, 9.75, 21.62) | [30.0, 39.1]; [26.2, 45.1]; [87.7, 124.6] |
| 3 | (0.87, 1.54, 2.50) | (6.74, 10.43, 20.00) | [29.7, 40.6]; [25.1, 44.4]; [84.9, 123.7] |
| 4 | (1.35, 1.94, 4.03) | (14.25, 22.18, 29.65) | [24.2, 47.0]; [15.0, 49.2]; [74.1, 123.1] |

Most moved cells moved by about one initial trust-region step; a minority
moved far. The slopes spread on both sides of the wave-2 values; tank-2 and
tank-3 slopes reach down to the KKT multipliers at p4 (folded: tank 2 about
26–28, tank 3 about 82–86) on some cells and far above them on others. There
is no single "right" slope per link, which is what the previous note's
Section 5.2 suggested.

### 5.3 Consistency at the known feasible points

`verify_cs.py` evaluates MINLPLib's points p1–p4 exactly. For every period
the exact Lagrangian value with the leaf slopes is above the bound of every
leaf pair containing the point's link levels (certB smallest margins 0.011,
0.010, 0.0098, 0.010; certA similar). Sums of the pair bounds along the
points' cells:

| point | f(x) | cert3 | certA | certB |
|---|---|---|---|---|
| p4 | 282.888037 | 277.648549 | 279.984082 | 280.436037 |
| p3 | 285.226595 | 278.925108 | 279.388771 | 279.408535 |
| p2 | 287.243774 | 278.728980 | 280.369763 | 281.621985 |
| p1 | 307.045516 | 292.020573 | 290.145567 | 291.201057 |

(cert3 column from the review.) Along p4's own cells the bound is still 2.5
below p4's value; the slopes were tuned for the DP's minimizing paths, not
for p4.

### 5.4 Independent re-bounding

`crosscheck_cs.py` with the review's vbb2 driver
(`cellslopes/logs/crosscheck_cert{A,B}_*.jsonl`). "Leaf" checks use the
leaf boxes, the leaf slopes and the exact pair bound of the DP (rounded down
to a float) as target, so they test the records and Lemma 2 together;
"record" checks use the record's own boxes, slopes and rbb bound.

| certificate | group | runs | certified the target | proved the box empty | failed |
|---|---|---|---|---|---|
| certA | leaf: minimizing path | 6 | 6 | 0 | 0 |
| | leaf: random pairs with a Lemma-2 correction | 40 | 27 | 13 | 0 |
| | record: minimizing path | 6 | 6 | 0 | 0 |
| | record: all other records of leaf pairs on paths within 0.05 of the optimum | 192 | 191 | 1 | 0 |
| | record: random new records used | 100 | 65 | 35 | 0 |
| certB | leaf: minimizing path | 6 | 6 | 0 | 0 |
| | leaf: random pairs with a Lemma-2 correction | 40 | 28 | 12 | 0 |
| | record: minimizing path | 6 | 6 | 0 | 0 |
| | record: all other records of leaf pairs on paths within 0.05 of the optimum | 202 | 202 | 0 | 0 |
| | record: random new records used (two samples of 99 and 2,000; 3 records drawn by both) | 2,096 distinct records (2,099 runs) | 1,466 | 630 | 0 |

vbb2 CPU 8,775 s in total, longest run 69 s. Eleven records of certB's
2,000-sample are also in the near-optimal group. So this note's certB record
checks cover 2,293 distinct records (1,663 certified, 630 proved empty), all
of them certA or certB runs, out of the 44,157 new records that certB uses.
The certA checks repeat no record. The 5,158 cert3 records used were all
re-bounded by the earlier review. A box proved empty makes any bound valid.

**Full re-bounding by the review.** The independent review of this note
([`../../reviews/waterno2-cellslopes-review.md`](../../reviews/waterno2-cellslopes-review.md),
Section 5) re-bounded **all** 49,315 records that certB uses (5,158 cert3,
19,679 certA and 24,478 certB runs) with vbb2 through its own driver, at
each record's own boxes and slopes with the rbb bound as target:

- 33,899 records were certified at exactly their rbb bound;
- 15,416 boxes were proved empty: all 12,298 records with rbb bound +∞ and
  3,118 records with a finite rbb bound;
- none failed.

Its exact DP from the vbb2 values alone, with its own Lemma-2 corrections,
equals 39157472136693483/140737488355328, certB's value. Its status agrees
with this note's checks on all 2,293 records above. It also re-bounded 556
corrected leaf pairs at the leaf boxes and leaf slopes, with the exact
corrected bound as target: the 256 on paths within 0.5 of the optimum whose
record task differs, and 300 random ones. 436 were certified, 120 proved
empty, none failed. So certB no longer rests on `rbb.py` alone.

### 5.5 Planning trajectory

Planning values are SCIP estimates of the DP, not bounds. Only values after
the switch to the pessimistic estimate are comparable with the certificates.

| stage | planning value | SCIP evaluations | notes |
|---|---|---|---|
| cert3 state | 272.635 | (12,922 from the previous note) | one slope per link |
| planA: global LP (3 steps) + 1 split round | 272.977 | 9,470 | 1 of 3 LP steps accepted |
| planB: local LP (2 steps) + 2 split rounds | 273.434 | 2,947 | both LP steps rejected |
| planC, optimistic stale values: 2½ cycles | (275.38) | 20,366 | not comparable (Section 3.1) |
| planC, switch to pessimistic values | 256.13 → 275.58 | 9,010 | honest value of the same state |
| planC: one more cycle + split round | 277.144 | 10,439 | certified as certA (277.093) |
| planG: one more cycle, no split | 278.281 | 9,451 | certified as certB (278.231) |

## 6. Negative results, observations and open issues

### 6.1 Slopes versus splits: attribution not established

The planning logs give the gain of each slope cycle and each split round
(planning values, confounded by the order of operations):

| phase | step | gain | SCIP evaluations | gain per 1,000 evaluations |
|---|---|---|---|---|
| planC (optimistic values) | slope cycle 1 | +0.83 | 5,803 | 0.14 |
| | split round | +0.20 | 988 | 0.20 |
| | slope cycle 2 | +0.84 | 3,828 | 0.22 |
| | split round | −0.10 | 1,262 | – |
| | slope cycle 3 | +0.90 | 6,460 | 0.14 |
| | split round | −2.91 (exposed stale values, Section 3.1) | 771 | – |
| planC (pessimistic values) | slope cycle | +1.38 | 10,439 − 2,305 = 8,134 | 0.17 |
| | split round | +0.19 | 2,305 | 0.08 |
| planG (pessimistic values) | slope cycle | +1.14 | 9,451 | 0.12 |

For comparison, the last 15 minutes of the previous note's split-only
refinement (plan3) gained +1.41 (271.2238 → 272.6353,
`sepbranch/logs/plan3.log`) with about 5,900 estimates (0.24 per 1,000),
at a lower level. So the slope steps gave the larger share of this run's
gain, but per evaluation they were not clearly better than splitting. No
controlled comparison (split-only from the same state, same budget) was
run. The claim "cell slopes are the better lever" is therefore **not**
supported by this data.

This comparison counts SCIP evaluations only, not certification.
Certifying certA and certB took 67,618 new rbb runs (154,539 CPU-s),
against 9,631 runs (25,308 CPU-s) for cert3 with one slope per link
(Section 6.4). Splits alone cannot lower the DP value that the existing
records give, because new cells inherit their parent's slope and the
parent's records apply to them unchanged. Slope changes can: at certA's
cells and slopes the cert3 records gave only 243.10 instead of 272.58
(Lemma 2). If certification cost were counted, it would weigh against
slopes rather than for them.

### 6.2 The global slope LP

See Section 3.2. The LP over all slopes is cheap to solve and its
predictions on the minimizing paths were accurate, yet 4 of 5 steps
lowered the planning value. The per-cell decomposition of Section 3.3
removes the problem because cells of one link do not compete.

### 6.3 Planning with stale estimates

See Section 3.1. Re-pricing old SCIP points at new slopes overestimates the
pair values by up to Σ|Δλ|·width per side, several units for wide cells.
An honest planning value needs the pessimistic estimate, and making it
fresh is costly (9,010 evaluations once, then about 1,000–3,000 per link
step).

### 6.4 Certification cost of slope changes

Every slope change voids the tight bounds of the cell's pairs up to
|Δλ|·width per link (Lemma 2). At certA's slopes the cert3 records alone
give 243.10, and 43,140 new rbb runs were needed; certB's slope cycle needed
24,478 more (at certB's slopes, before its runs, the existing records gave
259.33). In cert3, 9,631 runs sufficed for one slope per link. rbb was fast
on these pairs (median about 1 s; 99% under 17 s).

### 6.5 SCIP

Of the 76,318 new SCIP evaluations (201,353 CPU-s, median 1.2 s), 1,341
hit the 20 s limit and 6,846 reported infeasibility. SCIP values were used
for planning and targets only. rbb reached the targets derived from them in
67,614 of 67,618 runs, which suggests the estimates were not too high on the
pairs that mattered (they were not checked otherwise). The planning value
and the certified value differ by 0.0506 for both certificates, about the
goal margin 0.05 plus the per-pair slack.

### 6.6 What remains

- Remaining gap 4.66 (1.67%).
- The last slope cycle (planG) gained +1.14 in planning value for 9,451
  SCIP evaluations and then needed 24,478 rbb runs to certify; the last
  split round before it gained +0.19. Gains per unit of work are falling.
- certB's minimizing path runs through wide cells at links 3 and 4 (the
  whole tank-1 range at link 3). On every link some leaves still span the
  whole tank-1 range [2, 5] and 0.83 of tank 2. Further progress needs
  splits there as well as slopes; certB had no split round.
- The minimizing paths still do not follow p4's trajectory, and along p4's
  cells the bound is 2.5 below p4's value.
- Closing the gap would need cheaper pair bounds or a way to reuse them
  across slope changes with smaller loss than Lemma 2; not attempted.
- waterno2_09–24 were not attempted.

### 6.7 Relation to the theory notes

- *Decomposition note, Definition 1.2 / Lemma 1.5.* The certificate here is
  that model on a path with cell-dependent affine minorants; Section 2 makes
  explicit that the only coupling condition is one minorant per cell used on
  both sides of the separator. Because these minorants may jump across cell
  faces, (CM) holds on shared faces only through the "touching pairs"
  remark after Lemma 1.3 (Section 2). Proposition 1's own proof does not
  need that remark.
- *Proposition 2.6 (wrong slopes cost a first-order copy error).* Lemma 2's
  loss |Δλ|·width per link is the same first-order term, seen from the other
  side: a bound proved at one slope is worth that much less at another.
- *Theorem 3.4 (slopes = gradients at the minimizer).* Its recipe assumes
  one minimizer and growth around it. Here the tuned slopes vary widely from
  cell to cell (Section 5.2) and the minimizing paths are not p4's; the
  per-cell tuning is an empirical substitute, not an instance of the
  theorem.

## 7. Literature examined and novelty

Examined for this note (local folder `literature/` and one web search):

- Yang and Yang, "Globally converging algorithm for multistage stochastic
  mixed-integer programs via enhanced Lagrangian cuts", Optimization Online
  (2025); local summary `literature/papers/yang2025-…` read. Their SDDP-L
  partitions the state intervals, adds interval indicators and generates
  Lagrangian cuts in the lifted space; after projection the cuts give
  convex envelopes per partition element. This is the closest relative found:
  cut coefficients that depend on the active partition element, as our slopes
  depend on the cell. Their setting is MILP stages with SDDP sampling; ours is
  a deterministic chain of nonconvex MINLP periods with rigorous spatial B&B
  per pair and an exact DP.
- Füllner and Rebennack, "Non-convex nested Benders decomposition",
  Math. Program. (2022). The original search found it by web search and used
  the abstract only, but the local folder has its full text and a read
  summary (`literature/papers/fullner2022-non-convex-nested-benders-decomposition/`,
  added 2026-09-04); the summary was read for the revision after review.
  It combines dynamically refined binary approximations of the state with
  Lagrangian cuts for multistage nonconvex MINLPs; projecting the cuts back
  to the original state gives nonconvex, piecewise-linear value-function
  approximations. Also their SDDP review (SIAM Review
  2025; local summary read), which lists Lagrangian cuts, binary lifting and
  NC-NBD as the routes for nonconvex value functions.
- Ahmed, Tawarmalani and Sahinidis, "A finite branch-and-bound algorithm for
  two-stage stochastic integer programs", Math. Program. (2004); local
  summary read: branching on the tender (coupling) variables.
- The sources of `separator-branching.md`, Section 7 (Carøe and Schultz 1999;
  Ghaddar et al. 2015; Gleixner et al. 2012; Zou, Ahmed and Sun 2019), not
  re-read.
- Definition 1.2 and Lemma 1.5 of the decomposition note, which allow one
  affine minorant per separator cell.

Novelty is not claimed. Cell-dependent multipliers are the obvious
generalization of the previous note and of Definition 1.2, and related
partition-dependent Lagrangian cuts exist (Yang and Yang). Lemma 2 (re-using
a bound after a slope change) and the per-link decoupling behind the
per-cell acceptance are elementary. The search was brief; an unsuccessful
search does not establish novelty. No other publication with a dual bound for
waterno2_06 was searched for.


## 8. Costs

CPU times are sums of the per-task times measured inside the workers;
"allocated" is wall time × worker processes.

| item | wall | workers | tasks | CPU |
|---|---|---|---|---|
| planning planA, planB (global LP) | 20:16–20:39 | 24 | 12,417 SCIP evaluations | 18,259 s |
| planning planC (block coordinate) | 20:39–23:15 | 24 | 39,815 SCIP evaluations | 124,857 s |
| certA: SCIP refresh | 23:15–23:29 | 24 | 7,369 SCIP evaluations | 20,154 s |
| certA: rbb | 23:29–00:39 | 24 | 43,140 rbb runs | 99,680 s |
| certA: exact verification; vbb2 cross-checks | 00:39–00:51 | 1; 4 | 344 vbb2 runs | 710 s (vbb2) |
| planning planG | 00:40–01:05 | 20 | 9,451 SCIP evaluations | 16,166 s |
| certB: SCIP refresh | 01:05–01:21 | 24 | 7,266 SCIP evaluations | 21,917 s |
| certB: rbb | 01:21–02:01 | 24 | 24,478 rbb runs | 54,859 s |
| certB: exact verification; vbb2 cross-checks | 02:02–02:09 | 1; 24 | 2,359 vbb2 runs | 8,065 s (vbb2) |

Total measured: 364,667 CPU-s (101 CPU-hours): SCIP 201,353 s, rbb
154,539 s, vbb2 8,775 s, plus a few minutes of single-process exact
verification and development tests. Allocated: about 140 worker-hours
(20:16–02:09). The work of killed runs (one planA and one planB iteration,
two planC link steps) is not in the CPU column but is in the allocated time.
The largest items are SCIP (201,353 s, 55.2%; the planning runs alone
159,282 s, 43.7%; the two refreshes before certification 42,071 s, 11.5%)
and the rbb runs of the two certificates (154,539 s, 42.4%).

## 9. Files, commands and checks

Code in `cellslopes/` (imports `../period.py`, `../rbb.py`,
`../bundle.py` and `../sepbranch/{core,terminal,dpcells}.py` unchanged):

- `cs.py`: planning state (cells, cell slopes, point pool, records), tables
  U, L, P and the planning value, DP, the global slope LP (Section 3.2), and
  the SCIP and rbb worker tasks (`rbb_task` is `sepbranch/tasks.rbb_task`
  with per-pair slopes);
- `plan_cs.py`: planning with the global LP (planA, planB);
- `plan_bc.py`: block-coordinate planning with per-cell acceptance (planC,
  planG);
- `certify_cs.py`: targets, SCIP refresh of stale task pairs, rbb runs;
- `verify_cs.py`: exact recomputation (Section 4.2);
- `crosscheck_cs.py`: vbb2 re-bounding via the review's `rebound.run`;
- `stats_cs.py`: statistics; `diag_lpstep.py`: diagnosis of Section 3.2;
  `export_cert.py`: slim certificate file (cells, slopes, records).

Logs in `cellslopes/logs/`:

- configs `*.json` (`planC.json` was edited at the 22:02 restart:
  `delta_eval_global` 0.3 → 1.0, as noted in `planC.log`);
- planning logs `plan{A,B,C,G}.{log,out}`;
- certification logs `cert{A,B}.{log,out}`, exact verification
  `verify_cert{A,B}.log`, `cert{A,B}_verify.json` (and
  `certA_verify_slim.json`, the same check on the slim file);
- cross-checks `crosscheck_certA_{leaf,near}.*`,
  `crosscheck_certB_{leaf,near,rand2000}.*`;
- statistics `stats_{planF,planG,certA,certB}.log`; `diag_lpstep.log`;
  `verify_state0.json` (the cert3 state run through `verify_cs.py`);
- pipeline tests `verify_test.json`, `crosscheck_test*.jsonl` (their state
  file was deleted);
- **certificate files** `certA_cert.pkl.gz` (3.9 MB) and
  `certB_cert.pkl.gz` (6.1 MB): cells, cell slopes and all records; these
  are what `verify_cs.py` and `crosscheck_cs.py` need;
- gzip-compressed working states (gunzip before re-running a config that
  names them): `state0.pkl.gz` (cert3 converted), `planA.pkl.gz`,
  `planB.pkl.gz` (used by `diag_lpstep.py`), `planF.pkl.gz` (input of
  certA), `certA.pkl.gz` (input of planG), `planG_final.pkl.gz` (input of
  certB), `certB.pkl.gz` (latest full state). Together about 64 MB; the
  root may prefer not to commit them.

Commands actually run (from `cellslopes/`, `OMP_NUM_THREADS=1`;
`PYTHONPATH=../sepbranch:..` for verify and crosscheck):

```
python3 -c "import cs, pickle; pickle.dump(cs.from_cert3('../sepbranch/logs/cert3.pkl'), open('logs/state0.pkl','wb'))"   # inline, equivalent
python3 verify_cs.py logs/state0.pkl ../logs/implied_06.json logs/verify_state0.json ../data/waterno2_06.p4.sol ../data/waterno2_06.p1.sol
python3 plan_cs.py logs/planA.json          # stopped by hand during iteration 4
python3 plan_cs.py logs/planB.json          # stopped by hand after its second split round
python3 plan_bc.py logs/planC.json          # three runs (resumed); see the comments in logs/planC.log
python3 diag_lpstep.py > logs/diag_lpstep.log
python3 certify_cs.py logs/certA.json       # state logs/planF.pkl = planC.pkl at 23:14
python3 verify_cs.py logs/certA.pkl ../logs/implied_06.json logs/certA_verify.json ../data/waterno2_06.p{1,2,3,4}.sol
python3 crosscheck_cs.py logs/certA.pkl logs/certA_verify.json logs/crosscheck_certA_leaf.jsonl 0 1 4 900 leaf
python3 crosscheck_cs.py logs/certA.pkl logs/certA_verify.json logs/crosscheck_certA_near.jsonl 100 3 4 900 near
python3 plan_bc.py logs/planG.json          # stopped by hand after link 4
python3 certify_cs.py logs/certB.json       # state logs/planG_final.pkl
python3 export_cert.py logs/certA.pkl logs/certA_cert.pkl; gzip -9 logs/certA_cert.pkl   # same for certB
python3 verify_cs.py logs/certA_cert.pkl.gz ../logs/implied_06.json logs/certA_verify_slim.json ../data/waterno2_06.p4.sol
python3 verify_cs.py logs/certB_cert.pkl.gz ../logs/implied_06.json logs/certB_verify.json ../data/waterno2_06.p{1,2,3,4}.sol
python3 crosscheck_cs.py logs/certB_cert.pkl.gz logs/certB_verify.json logs/crosscheck_certB_leaf.jsonl 0 1 24 900 leaf
python3 crosscheck_cs.py logs/certB_cert.pkl.gz logs/certB_verify.json logs/crosscheck_certB_near.jsonl 100 5 24 900 near
python3 crosscheck_cs.py logs/certB_cert.pkl.gz logs/certB_verify.json logs/crosscheck_certB_rand2000.jsonl 2000 11 24 900
python3 stats_cs.py <state> <earlier state>   # logs/stats_*.log
```

Pipeline tests before the certificates: rbb on 10 task pairs of a planning
state and exact verification of that state (bound 253.034285335 with the
corrected cert3 records, p4 check passed); vbb2 on the 10 new records and on
46 leaf checks (all certified or proved empty).

Only targeted checks were run. No project-wide checks were run and no CI
results were consulted.

## 10. Revision after review (2026-10-01)

From [`../../reviews/waterno2-cellslopes-review.md`](../../reviews/waterno2-cellslopes-review.md)
(verdict: verified; seven minor issues, none affecting the certified value).
Each issue was checked against the logs before the text was changed. The
certified value 278.230573774 (exact 39157472136693483/140737488355328) is
unchanged.

1. **Review status (header, Section 1, Sections 4.3 and 5.4).** The note
   said it was not independently reviewed and that the new records outside
   the samples rested on `rbb.py` alone. The review re-bounded all 49,315
   records that certB uses with vbb2: 33,899 certified, 15,416 proved empty
   (12,298 with rbb bound +∞, 3,118 finite), none failed. Its exact DP from
   these values alone equals certB's value. Checked in
   `reviews/waterno2-cellslopes-review-checks/logs/rebound_summary.log` and
   `rebound_breakdown.log`, which also give the 556 leaf checks (436
   certified, 120 proved empty). The header, the Summary and Section 5.4 now
   report this and cite the review; Section 4.3 points to it.
2. **Distinct records (Section 1, Section 5.4).** "2,307 of the 44,157 new
   records" and the row "99 + 2,000 | 1,467 | 632" counted runs. Recounted
   from `cellslopes/logs/crosscheck_certB_{near,rand2000}.jsonl`: the 2,307
   record runs counted in the table (the files also re-run the six path
   records once more) cover 2,293 distinct records (1,663 certified, 630
   proved empty), all certA or certB runs. 3 records were drawn by both random
   samples, and 11 records of the 2,000-sample are also in the near-optimal
   group. The random samples cover 2,096 distinct records, 1,466 certified
   and 630 proved empty. The certA checks repeat no record. Both places now
   give distinct records.
3. **SCIP share (Section 8).** "The planning SCIP runs (56%)" used 201,353 s,
   which is all SCIP work, including the two refreshes before certification.
   From `stats_planF.log`, `stats_planG.log`, `stats_certA.log` and
   `stats_certB.log`: planning SCIP is 143,116 + 16,166 = 159,282 s, 43.7% of
   364,667 s; all SCIP is 55.2%; the refreshes are 42,071 s (11.5%); rbb is
   42.4%. Section 8 now gives these numbers.
4. **plan3 gain (Section 6.1).** `sepbranch/logs/plan3.log` goes from
   271.2238 (round 0, 7,012 estimates) to 272.6353 (round 89, 12,922
   estimates, 904 s): +1.41 for 5,910 estimates, 0.24 per 1,000. Corrected
   from +1.42.
5. **Füllner and Rebennack (Section 7).** The full text and a read summary
   are in `literature/papers/fullner2022-non-convex-nested-benders-decomposition/`
   (added 2026-09-04); the original search used only the abstract. The
   bullet now says so. The summary was read for this revision and agrees
   with the note's description. The novelty statement is unchanged.
6. **Definition 1.2 (Sections 2 and 6.7).** With minorants that jump across
   cell faces, (CM) as stated in Definition 1.2 can fail on a face that a
   leaf shares with a neighbouring cell. It holds in the form allowed by the
   "touching pairs" remark after Lemma 1.3 of the decomposition note, which
   needs (CM) only for cells whose interior meets the leaf's (checked against
   that remark). Both sections now say this, and that Proposition 1's direct
   proof does not need the remark.
7. **Certification cost (Section 6.1).** Section 6.1 now says that its
   comparison counts SCIP work only. It gives the rbb cost of certifying
   certA and certB (67,618 runs, 154,539 CPU-s, from `stats_certB.log`)
   against cert3's (9,631 runs, 25,308 CPU-s). It says that counting this
   cost would weigh against slopes, and gives the reason: splits keep the
   existing records' value, while slope changes lowered it to 243.10 at
   certA's slopes (Section 6.4). The conclusion "not established" is
   unchanged.

Checks for this revision: inline Python recounts of the cross-check JSONL
files above, and reading the cited logs, the decomposition note's
Definition 1.2 and Lemma 1.3, and the local Füllner–Rebennack summary. No
computation was re-run. No project-wide checks were run and no CI results
were consulted.

