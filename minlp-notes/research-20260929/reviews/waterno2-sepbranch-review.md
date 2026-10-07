# Review: waterno2_06 separator branching (`separator-branching.md`)

Date: 2026-09-30. Reviewer: independent verifier. I did not produce the
work under review or its code.

Reviewed: `open-instances-wave2/waterno2/separator-branching.md` and the code
and logs in `open-instances-wave2/waterno2/sepbranch/`. My scripts and logs
are in `reviews/waterno2-sepbranch-review-checks/`. I edited nothing under
`open-instances-wave2/` or in the earlier verifiers' folders. The authors'
pickles were read through a stub class (`load_cert.py`), so no author code
ran in my certificate checks. The authors' code was imported read-only in one
place only, `scip_claim.py`. There it rebuilt their SCIP models (`period.py`,
`bundle.py`, and `terminal.py` for the last period) for the SCIP checks in
Sections 3.3 and 5.3.

## Verdict

**The certified dual bound 272.584700834 for waterno2_06 is confirmed.**

I re-certified every one of the 8,958 records that the cert3 dynamic program
(DP) uses, not a sample. I used the recheck's `vbb2.py` through my own driver,
with the first verifier's model and implied bounds and my own terminal row.
The authors' `rbb.py` was not used.

- 6,827 records were certified at their rbb bound.
- 2,131 pair boxes were proved empty. These are all 1,782 boxes that rbb had
  also proved empty, and 349 to which rbb had given a finite bound.
- No record failed.

The shortest path recomputed in exact arithmetic from the vbb2-certified
values alone is 19181443079783745/70368744177664. This is the authors' exact
value. So the note's statement that 8,934 records "rest on rbb.py alone" is
now out of date: each record has been certified by two codes.

| check | result |
|---|---|
| validity argument (cells cover the separator boxes; per-pair bounds; DP combination) | sound; conditions checked on the data (Section 1) |
| terminal row 1/2·E1 + 1/5·E2 + 4/9·E3 ≥ 3913/900 | re-derived independently in exact arithmetic, for T = 6 and for all T in {2, 3, 4, 6, 9, 12, 18, 24} |
| cells cover each link's level box | yes, all 5 links of cert3 and cert2; the leaves partition the box (every elementary cell of the breakpoint grid lies in exactly one leaf) |
| each leaf pair's bound comes from a record whose boxes contain the pair's cells, with the link's single slope and μ = 0 | yes, all 62,088 leaf pairs of cert3 and all 28,858 of cert2 |
| exact DP value, cert3 | 19181443079783745/70368744177664 = **272.584700834** (rounded down), equal to the authors' value |
| exact DP value, cert2 | 38164240025509421/140737488355328 = 271.173235159, equal to the authors' value |
| pair bounds re-certified with vbb2 (not rbb.py), cert3 | **all 8,958 used records**: 6,827 certified at the rbb bound, 2,131 boxes proved empty, 0 failures; exact DP over these values = authors' value (Section 3) |
| pair bounds of cert2 | not re-bounded here (cert2 is superseded); data checks and exact DP only |
| negative control: vbb2 must not certify SCIP estimate + 0.05 on the six path pairs | none certified (bounds stop within 10⁻³ of SCIP's values) |
| known feasible points p1–p4 | every pair bound on a point's cells is below the point's period value (smallest margin 0.019) |

Issues found are minor and concern wording, not validity (Section 6).

## 1. The validity argument

The note's claim (Section 2.1) is

    optimum ≥ min over cell sequences (D_0, …, D_4) of Σ_t B_t(D_{t−1}, D_t),

where B_t(D, D') is any rigorous lower bound on the period-t pair problem
φ_t(D, D') with the Lagrangian terms of one fixed slope vector per link.

I checked the argument step by step, and checked the facts it needs against
the model (first verifier's `vmodel`/`vstruct`) and the certificate data.

1. **Objective and rows.** The objective is the sum of 54 cost variables with
   coefficient 1, 9 per period, and every variable belongs to exactly one
   period. Of the 1,234 rows, all but one lie inside a period or are one of
   the 15 link rows −x_end(t,k) + x_start(t+1,k) = 0. The exception is the
   horizon row e56 (`check_rows.py`, `logs/check_rows.log`).
2. **Telescoping.** For an exactly feasible x the link rows give
   Σ_t λ_t·(s_{t+1}(x) − e_t(x)) = 0 for any real λ_t. So f(x) is the sum
   of the six period Lagrangian values. The float slopes are used as exact
   numbers both in rbb's objective and in vbb's exact objective. I also
   checked the identity numerically at p1–p4: the exact difference between
   the sum of period values and f(x) equals Σ λ·(link residual).
3. **Covering.** The cells of link t must cover every level vector that a
   feasible point can have at link t. Such a vector lies in the OSIL bounds
   and the implied bounds of both copies. I recomputed this box exactly with
   the first verifier's own implied bounds (`my_implied_06.json`). For every
   link, the root cell of the plan contains it, and the leaves cover the
   root cell (Section 2).
4. **Per-pair feasibility.** The restriction of x to period t satisfies the
   period rows, the OSIL and implied bounds, and lies in the pair's cells.
   In the last period it also satisfies the terminal row, which is implied
   by the rows (Section 1.1). Dropping the horizon row itself is a
   relaxation. So each period value is ≥ φ_t ≥ B_t.
5. **Inheritance.** A bound proved on an ancestor pair (larger boxes, same
   slopes) is valid for every leaf pair inside it. Section 2 checks this by
   box containment rather than by the split tree.

The argument is the standard Lagrangian-decomposition bound over a chain
with state-space partitioning. Its rigor rests on the per-pair bounds and on
the implied bounds. The first verifier proved the implied bounds. The pair
bounds are checked in Section 3.

One implementation detail matters and holds. `rbb.Window` caches only
structural data (`_ai`, `_st`), not bound-dependent data. So reusing one
Window for all pairs of a period (`core.PeriodBounder`) cannot leak one
pair's box into another pair's bound.

### 1.1 Terminal row

`ind_verify.py` derives the row by structure, without the authors'
least-squares step. For every period it takes the three tank-balance rows
divided by 3600 and joins the flow variables through the in-period copy rows
(union-find). It then asserts that what remains is

    h_t = d_t + Σ_k A_k (e_{t,k} − s_{t,k}) / 3600,   A = (1800, 720, 1600),

with h_t the period's horizon variable and d_t its fixed demand. It also
asserts that every link row joins an end level and the next start level of
equal area. Summing over the periods and using the horizon row gives

    1/2·E1 + 1/5·E2 + 4/9·E3 ≥ c − Σ_t d_t + (1/2·3.5 + 1/5·4.1 + 4/9·4) = 3913/900,

because c = Σ_t d_t = 1.752499999 exactly. This matches the note for
T = 6. It also matches for T ∈ {2, 3, 4, 9, 12, 18, 24}: c − Σ d_t = 0 and
the right-hand side is 3913/900 in every case (`logs/terminal_allT.log`).

The note's rewriting of μ(c − Σ h_t) as a slope shift μ·w plus a
final-volume price (Section 2.2) is also correct. The folded slopes stored in
the plan equal λ_t + μ·A/3600 from `logs/mult_06_w1_impl.json`, bit for bit.

## 2. Certificate data (`ind_verify.py`)

My own script re-checks the pickles `cert3.pkl` and `cert2.pkl`. It does not
use the authors' `verify.py`, `dpcells.py` or `core.py`.

- **Coverage.** For each link I collect all leaf breakpoints per coordinate.
  Every elementary cell of that grid must lie in some leaf. It lies in
  exactly one leaf on every link, so the leaves partition the root box.
  Grid sizes are up to 34 × 28 × 41. This check does not use the split tree.
- **Records.** For every leaf pair (r, c) of period t, the record named by
  `CSRC` must satisfy the following:
  - it belongs to period t;
  - its stored entry and exit boxes contain the leaf boxes (float
    comparison);
  - its `lam_in` and `lam_out` equal the plan's slope vector of links t−1
    and t;
  - its μ is 0;
  - its bound equals the table entry;
  - an infinite bound has status `infeasible`.

  Because both periods adjacent to a link take their slope from the same
  plan entry, each link has one slope vector. All checks pass. cert3 has
  46,757 finite leaf-pair bounds and 15,331 infinite ones; 8,958 of its
  9,631 records are used. cert2 has 21,580 finite and 7,278 infinite; 5,211
  of its 5,540 records are used.
- **Exact DP.** The shortest path is computed in `Fraction` arithmetic over
  the record bounds:

  | | exact value | rounded down (9 dp) | authors' `*_verify.json` |
  |---|---|---|---|
  | cert3 | 19181443079783745/70368744177664 | 272.584700834 | identical |
  | cert2 | 38164240025509421/140737488355328 | 271.173235159 | identical |

  The minimizing path of cert3 uses records 1, 16, 30, 14, 10 and 3. Their
  bounds (−593.6440, 61.0976, 53.9861, 53.1565, 49.7429, 648.2456) and exit
  cells match the note's table in Section 4.1.

The note's reported counts (leaves per link, 62,088 leaf pairs, 46,757 /
15,331, 9,631 runs with 7,849 certified at target and 1,782 infeasible, 0
below target, 5 retries) agree with the pickles and logs.

## 3. Independent re-bounding of the pair bounds (`rebound.py`)

### 3.1 Method

I re-bounded every record that the cert3 DP uses (8,958 of 9,631; the
other 673 were superseded by larger bounds on the same leaf pairs) with the
recheck's `vbb2.py`. It does not share code
with `rbb.py`: it evaluates node bounds exactly in `Fraction` arithmetic and
uses outward-rounded float propagation. My driver differs from the authors'
`crosscheck_pairs.py` in what it takes from the authors:

| input | authors' crosscheck | my driver |
|---|---|---|
| period model, link order, objective | verifier's `vmodel` | verifier's `vmodel` (same) |
| mapping of cell coordinates to variables | authors' `S["link"]` | verifier's link list |
| implied bounds | authors' `implied_06.json` | first verifier's own `my_implied_06.json` (nowhere weaker than the authors' and covering all their bounds tighter than OSIL) |
| terminal row | authors' `terminal.derive` | my own derivation (Section 1.1) |
| records | 24 per certificate | all 8,958 used by cert3 |

The target is the record's rbb bound for finite records. Records with bound
+∞ (rbb's FBBT proved the box empty) got a finite target: the smallest value
that leaves the DP value unchanged, given the other periods ("required"
value). vbb2 then either proves the box empty or certifies that value. Time
limit 900 s per record, 14 single-threaded workers.

### 3.2 Results

Source: `logs/rebound_cert3_all.jsonl` and `logs/rebound_summary.log`. The
run took 51 min wall and 38,844 CPU-s of vbb2 time. The longest run took
48.1 s and 2,451 nodes; the median was 1.2 s.

| period | records | certified at the rbb bound | box proved empty by vbb2 |
|---|---|---|---|
| 0 | 130 | 57 | 73 |
| 1 | 1,553 | 1,094 | 459 |
| 2 | 1,701 | 1,313 | 388 |
| 3 | 1,828 | 1,430 | 398 |
| 4 | 3,584 | 2,771 | 813 |
| 5 (terminal row) | 162 | 162 | 0 |
| **total** | **8,958** | **6,827** | **2,131** |

The rbb bounds of these records split into two kinds:

- **Finite rbb bound (7,176 records).** vbb2 certified 6,827 at exactly the
  rbb bound and proved the other 349 boxes empty. All 349 are records that
  rbb closed at the root by OBBT with the objective cutoff (0 nodes, bound
  equal to the target). 346 of them have targets above 1,000, because SCIP
  had reported those pairs infeasible.
- **rbb bound +∞ (1,782 records).** vbb2 proved every one of these boxes empty
  at its root (FBBT or OBBT). The fallback "required" target was never
  needed.

Some subsets matter most, and for reporting I labelled them (all are
included in the 8,958):

- **Near-minimal paths.** 205 records lie on a path within 0.05 of the DP
  value, including every record of the tied minimizing paths. All were
  certified; the longest took 12.6 s.
- **rc=False retries.** All 5 were certified.

**Exact DP from vbb2 values only.** Each leaf pair takes the value its
record has under vbb2: the rbb bound where certified, and +∞ where vbb2
proved the box empty. The exact shortest path is then
19181443079783745/70368744177664 = 272.584700834 (rounded down). This
equals the authors' value, so the certified bound no longer depends on
`rbb.py`.

### 3.3 Negative control

A driver that over-constrains the pairs, for example by putting a cell box
on the wrong copy, would make vbb2 certify anything. As a control, I asked
vbb2 to certify the SCIP estimate + 0.05 on the six pairs of the minimizing
path, with the same driver and a 120 s limit (`control.py`,
`logs/control_cert3.jsonl`). vbb2 certified none of them. Its final bounds
lie 5·10⁻⁵ to 9·10⁻⁴ above the default-tolerance SCIP values:

| period | rbb bound | SCIP estimate | vbb2 bound after control run |
|---|---|---|---|
| 0 | −593.64403 | −593.62728 | −593.62676 |
| 1 | 61.09761 | 61.11436 | 61.11524 |
| 2 | 53.98609 | 54.00284 | 54.00351 |
| 3 | 53.15652 | 53.17327 | 53.17345 |
| 4 | 49.74290 | 49.75965 | 49.75982 |
| 5 | 648.24561 | 648.26235 | 648.26240 |

SCIP's default points are feasible only to about 10⁻⁶, so values slightly
below the exact minimum are expected. For periods 1 and 2, SCIP with feasibility
tolerance 10⁻⁹ returned points with exact row violations below 10⁻⁹. Their
values are 61.115239 and 54.003514. vbb2's bounds agree with them to the six
printed decimals (`logs/scip_tight_path.log`).

## 4. Consistency at known feasible points (`point_check.py`)

MINLPLib lists four feasible points p1–p4 of waterno2_06, with maximum row
violation up to 7·10⁻¹⁰. For each point and period, I found the leaves that
contain the point's link levels and computed the point's exact period
Lagrangian value. That value must be at least every certified pair bound on
those cells. It is, with a smallest margin of 0.029 (cert3) and 0.019
(cert2). The sums of pair bounds along the points' cells are:

| point | f(x) | cert3 sum along x's cells | cert2 sum |
|---|---|---|---|
| p4 | 282.888037 | 277.648549 | 277.422681 |
| p3 | 285.226595 | 278.925108 | 278.659044 |
| p2 | 287.243774 | 278.728980 | 278.274926 |
| p1 | 307.045516 | 292.020573 | 285.803373 |

This is a necessary condition only, but it would catch a sign error in the
slopes or a mislabelled cell.

## 5. Other claims

### 5.1 Numbers taken from logs (not re-run)

I compared the note's exploration numbers with the logs; all agree:

- Section 5.2: the p4-path table (`explore_p4path.log`) and the KKT-slope grid
  estimate 223.0424 on 54–72 cells per link and 18,432 pairs (`plan1.log`,
  6,079 s wall).
- Section 5.3: tank-width costs (`explore_tankwidth.log`):
  - tank 3 at width 1: 282.53 → 258.10, and 282.58 → 260.16 (KKT);
    279.57 → 270.94 (wave 2);
  - tank 2 unsplit: 24.56 (KKT), 12.08 (wave 2);
  - tank 1 unsplit: 3.73 (KKT), 2.46 (wave 2).
- Section 5.4: reuse losses (`explore_repeat.log`): 0.81–4.31 for a common
  slope and 7.59 more for the demand interval.
- Section 4.1: the growth of the planning estimate (`plan2.log`,
  `plan3.log`), the median leaf widths (`stats_cert3.log`), and p4's link-1
  levels (4.897, 2.595, 3.347).

These are SCIP estimates, and the note labels them as such. I did not re-run
them.

The station-D explanation in Section 5.3 matches the model rows. Tank 3's
balance gives e − s = 2.25·(q_D − d). A running station D has flow at least
0.24, from rows such as −6/25·b49 + x372 ≥ 0. With d between 0.277 and
0.307, the end level is either s − (0.62 to 0.69) or at least about
s − 0.15. This leaves a gap of about 0.47–0.54 relative to the start
level.

### 5.2 rbb strength defect (Section 5.6)

The code confirms the mechanism. `rbb.solve` calls `choose_branch` with the
node's pre-tightening LP point after reduced-cost tightening. If that point
lies outside the tightened box, no variable qualifies and the node's bound
b is kept as final. b is a valid bound for the node, so the defect affects
strength, not validity. The pickles agree with the note:

- cert2 has 3 records below target (1079, 2236, 2368). None of them is used
  by the DP; 2236 and 2368 were superseded by the rc=False retries 5539 and
  5538.
- cert3 has 5 records with a retry, all certified, and none below target.

### 5.3 SCIP's inconsistent "optimal" claims (Section 5.5)

`scip_claim.py` rebuilt the cert2 record-2236 pair with the authors' SCIP
model builder and evaluated each returned point exactly with my own code
(`logs/scip_claim.log`). SCIP reported "optimal" at three different values:

| SCIP run | reported optimum | exact row violation of its point | exact bound, box and integrality violation |
|---|---|---|---|
| no propagation | 55.689858 | 8.4·10⁻⁹ | 2.4·10⁻⁷ |
| default settings | 55.689773 | 1.5·10⁻⁸ | 9.6·10⁻⁷ |
| default settings, seed shift 7 | 65.123993 | 8.9·10⁻⁷ | 6.3·10⁻⁹ |

So SCIP's own points within its tolerances lie 9.4 below the seed-7 "optimal"
value, as the note says. (The installed pyscipopt reports SCIP 10.0.) I
also saw further SCIP unreliability on the cert3 path pairs:

- With feasibility tolerance 10⁻⁹, SCIP declared the path pairs of periods
  0, 3 and 4 infeasible.
- On the period-5 pair it claimed "optimal" at 664.153199, while its
  default run found 648.262 and vbb2 could not certify 648.312.

I did not resolve which of these statements is correct. It does not matter
for validity: a finite lower bound is also valid for an empty pair. It
confirms that SCIP values are fit for planning only, which is how the note
uses them.

## 6. Issues

None affects the certified value.

1. **Gap convention not stated.** 7.26% and 3.78% are |p − d| / min(|p|, |d|) =
   (primal − dual)/dual, the convention of `report.md`. Relative to the
   primal, the gaps are 6.77% and 3.64%. A one-line pointer to the
   definition would prevent misreading. The "46% of the absolute gap
   (8.85 of 19.15)" is correct.
2. **Target-rule guarantee (Section 3.2).** The statement "every path has a
   certified sum of at least G − 6·10⁻⁴" assumes each pair's slack is 10⁻⁴.
   The slack is max(10⁻⁴, 10⁻⁷|E|), which is 10⁻³ for pairs with the
   placeholder E = 10⁴. For paths through such pairs, the stated argument
   guarantees only G − Σ slack. This is harmless, because the final value is
   computed from the certified bounds, not from the rule. The realized value
   is G − 6.0·10⁻⁴ to the printed precision.
3. **Wording, Section 4.2.** rbb's root OBBT runs with the objective
   cutoff c·x ≤ target. When it returns the target with 0 nodes, it has
   proved that no point has value ≤ target, not that the box is empty. vbb2
   then proved these three boxes empty.
4. **Wording, Section 5.1.** The value 265.148592 was reached with
   [4, 6, 7, 5, 4] cells per link. [6, 7, 8, 6, 5] is the state after the
   next split, which was not evaluated. So "4–7 cells" rather than "4–8".
5. **"The other 8,934 records used by cert3 rest on rbb.py alone"** (Section
   4.2 and the summary). This is out of date after this review. All 8,958
   used records have now been re-certified with vbb2 (Section 3). The note
   could cite this review. Its statement that the new wrappers have not been
   reviewed is also partly out of date. Their outputs (cells, record boxes,
   slopes, DP) were checked here by independent code, although I did not
   line-review `plan.py` or `certify_dp.py`. Their correctness is not needed
   for validity, since the checks cover everything the bound uses.
6. **Summary bullet "282.35–282.66 of 282.89 along p4"** (Section 1). These
   are SCIP estimates on p4-centred cells, not bounds. Section 5.2 labels them
   as estimates; the summary bullet should too.

## 7. What the confirmed value rests on

- The OSIL data of waterno2_06, read by the first verifier's `osilx`.
- The implied bounds, proved by the first verifier (`my_implied_06.json`,
  exact FBBT and OBBT). My re-bounding uses these, not the authors' file.
  The certificate itself used the authors' file, which the first verifier
  confirmed.
- The certified pair bounds. Each of the 8,958 used records is certified
  twice: by the authors' `rbb.py` and, in this review, by `vbb2.py` (the
  first verifier's exact node bounds with the recheck's outward-rounded
  propagation).
- My checks in Sections 1–2 (coverage, record containment, slopes, exact
  DP) and the independent terminal-row derivation.

**Independence.** My code shares nothing with the authors' `sepbranch/` or
`rbb.py`. It does share the first verifier's model reader, relaxation and
node-bound code (`vbb.py`) and the recheck's propagation (`vbb2.py`). The
authors' own crosscheck used the same vbb2. An error common to vbb and vbb2
and to rbb, which is a separate code base, would be needed to invalidate the
bound.

**Not checked.**

- I did not re-run the planning (`plan.py`), the rbb certification, the
  explorations, or the one-cell +0.0008 comparison (`test1.log`).
- I did not review `rbb.py` again beyond the parts named above; the wave-2
  verifier reviewed it.
- I did not search the literature beyond reading the note's Section 7. Its
  novelty statement is appropriately modest: novelty is not claimed, and
  each ingredient is called standard. The MINLPLib numbers it cites (primal
  282.8880374; best listed dual 165.1902989, SCIP) match the first
  verifier's saved copy of the MINLPLib page.

## 8. Files and commands

Folder `reviews/waterno2-sepbranch-review-checks/`:

- `load_cert.py`: reads the pickles through a stub class.
- `check_rows.py`: period split, objective and row coverage.
- `ind_verify.py`: terminal-row derivation; coverage, record and slope
  checks; exact DP.
- `terminal_allT.py`: the terminal-row derivation for all T.
- `point_check.py`: checks at the feasible points p1–p4.
- `select_records.py`: criticality and "required" values; sample groups
  (used only as labels).
- `make_full_selection.py`: selection file for the full run (all used
  records, longest rbb runs first).
- `rebound.py`: vbb2 re-bounding driver.
- `control.py`: negative control.
- `summarize_rebound.py`: status counts and the exact DP over vbb2-certified values.
- `scip_claim.py`: SCIP runs with exact evaluation of the returned points.
- `logs/`: all outputs named below.

Commands, run from that folder with `OMP_NUM_THREADS=1
PYTHONDONTWRITEBYTECODE=1`. `SB` is `open-instances-wave2/waterno2/sepbranch/logs`
and `VI` is `reviews/waterno2-verification/logs/my_implied_06.json`:

```
python3 check_rows.py                                                 # logs/check_rows.log
python3 ind_verify.py $SB/cert3.pkl $VI logs/ind_verify_cert3.json   # > logs/ind_verify_cert3.log
python3 ind_verify.py $SB/cert2.pkl $VI logs/ind_verify_cert2.json   # > logs/ind_verify_cert2.log
python3 terminal_allT.py 2 3 4 6 9 12 18 24                           # logs/terminal_allT.log
python3 point_check.py $SB/cert3.pkl data/waterno2_06.p{1,2,3,4}.sol   # logs/point_check_cert3.log (and cert2)
python3 select_records.py $SB/cert3.pkl logs/sel_cert3.json 0.05 60 30 30 930
python3 rebound.py $SB/cert3.pkl logs/sel_cert3_smoke.json logs/rebound_cert3_smoke.jsonl 12 600   # smoke test, 12 records
python3 make_full_selection.py $SB/cert3.pkl logs/sel_cert3.json logs/sel_cert3_all.json
python3 rebound.py $SB/cert3.pkl logs/sel_cert3_all.json logs/rebound_cert3_all.jsonl 14 900
python3 control.py $SB/cert3.pkl logs/control_cert3.jsonl
python3 scip_claim.py $SB/cert2.pkl 2236                              # logs/scip_claim.log
python3 scip_claim.py $SB/cert3.pkl 1,16,30,14,10,3 tight             # logs/scip_tight_path.log
python3 summarize_rebound.py                                          # logs/rebound_summary.log
```

`logs/sel_cert3_smoke.json` holds the six path records plus the first three
`inf` and three `obbt0` records of `logs/sel_cert3.json`; it was written by an
inline command. The `make_full_selection.py` script was written after the run;
it reproduces `logs/sel_cert3_all.json` byte for byte. The `data/*.sol` files
are in `open-instances-wave2/waterno2/data/`. Only
targeted checks were run. No project-wide checks were run and no CI results
were consulted.
