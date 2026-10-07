# Confirmation review (round 2) of `theory-bangbang/kappa-negative.md`

Date: 2026-09-30. Referee: fresh and independent. I did not write the note,
its scripts or the earlier reviews. Scope: check the round-2 revision
(note Section 14) against the items of `reviews/kappa-negative-confirm-r1.md`
(R1, R2, R3 and two nits); recompute the numbers that changed; check that
nothing was strengthened. Checks and logs:
`reviews/kappa-negative-confirm-r2-checks/` (`c2_cert.py`,
`c2_author_partition.py`, `c2_phase.py`, `c2_eps.py`, `logs/`).

Labels: **exact** means rational arithmetic in my own code; **float** means
floating-point computation in my own code. I did not import the author's
code. Two of my scripts read the author's JSON logs: `c2_author_partition.py`
reads the node intervals, and `c2_phase.py` reads the grid patterns and break
offsets.

## Verdict

**Minor fixes needed (numbers only).** R1, R2 and both nits are resolved.
The R1 rerun is correct: my own exact certificate confirms `f* = J(zbar)` on
the three `kappa = -0.5`, `N = 4000` grids. The R3 wording is now properly
hedged. However, the R3 break times were recomputed from a logged quantity
`theta_1` that is wrong on grids where the first switch is fractional. The
code reverses the fraction of the stage spent before the switch. This changes
4 of the 13 quoted break times and the implied matching times. It does not
change the conclusion (Section 3, P1). Nothing was strengthened beyond the
evidence, and no item was declined.

## 1. Check of each item

| item | what the revision did | my check | result |
|---|---|---|---|
| R1 (`f* = J(zbar)` claimed at `N = 4000` without a certificate) | ran the missing certificates (`rev2_checks.py two4000`); updated the 9.1 rows and bullet, Summary items 2–3, Section 3 and the status table; recorded the earlier overstatement | **Exact, own code** (`c2_cert.py`): exact KKT point from the logged pattern (`sigma_n = 0` solved exactly; all other signs checked; quadratic structure checked by exact finite differences); plain gap; lifted interval `V` from the affine zero-loss conditions, using the residual `h sigma om + h d^2/2 - (h^2/4) om^2`, which I re-derived for `P = -k`; both ends of `V` rebuilt from scratch; outer nodes anchored at `z(V_hi)` and `z(V_lo)` | **Resolved and independently confirmed.** Fractional controls −0.86390, −0.87258, −0.87282; plain gaps 0.868532, 0.876639, 0.876865 `h^2`, equal to `two.json`. My `V`: `[-0.87557, 0.42318]`, `[-1, 0.45028]`, `[-0.89075, 0.32958]`. Outer-node bounds minus `J(zbar)`: +2.276 and +1.87e-4; +2.101; +1.597 and +3.55e-4 `h^2`, all exactly ≥ 0. So `f* = J(zbar)` holds on all three grids (`logs/cert4000.{log,json}`; under 1 s per grid). The author's partitions also pass under my formulas: each lifted range lies inside my `V`, and each fixed-node bound is ≥ `J(zbar)` (`logs/author_partition.log`). The end points shared with my `V` agree to all printed digits. The author's lifted ranges are narrower on one side than `V`, which costs nodes but does not affect validity. At `(0.7, 1.3)` my `V` reaches `u_- = -1`, so two nodes suffice there; the note's "3 nodes" describes the author's certificate, which is fine. Text: "all 36 grids of Section 9.1" and "all ten grids with a failing stage, `N = 500 … 4000`, 3–9 nodes" now match the table. The note states plainly that the round-1 status row overstated the evidence. |
| R2 (`N`-independence of the `kappa = -0.5` counts) | replaced by the `ubar_n` dependence for both toys, with the `N = 8000`, `epsilon/h^2 = 1e-1` exception | **Float, own code** (`c2_eps.py`): toy-plus KKT points, `q`, `rho*`, `w_0`, predicted counts per side | **Resolved.** `ubar_n` = −0.2470, 0.1839, −0.4606 (`n` = 238, 954, 1909). `q` = 1.522, 1.5225, 1.5225; `rho*` = 7.553, 7.555, 7.555 (spread under 0.1%). At `1e-1`: `w_0 = 0.6325 > ubar_n - u_- = 0.539` at `N = 8000`, so the prediction is 1 + 0 + 1 = 2; at `N = 1000` and `4000` it is 3. The central node is `[-1, 0.1719]`, as in `rev2_eps01.json`. At `1e-4` the per-side split is 3 + 2 (`N = 1000`) against 2 + 3 (`N = 4000`), as stated. |
| R3 (7.2 lacked the 9.3 caveats) | 7.2 now says "at larger `N`", gives the `N = 1000` exception, and calls the agreement a consistency observation needing an undetermined matching time of 0.1–0.5; 9.3 lists the grids and separates [E]'s `s_1` from the switching stage `s_1` | read the text; recomputed the layer-law ratios; **float, own code** (`c2_phase.py`): rebuilt the KKT point of each grid with a fractional second switch and recomputed the switch phase | **Wording resolved; numbers partly wrong.** The hedges are in place, and the ratios are right: `exp(-gamma/|eta|)` = 1.890e-3, 5.581e-3, 4.199e-4, and 2.97e-6 for −0.275. The grid lists and the `N = 1000` cases (fractional second switch for `(0.5, 1.5)` and `(0.45, 1.55)`) are right. But the logged `theta_1` reverses the within-stage fraction, which changes 4 of the 13 break times (P1). |
| Nit 1 (`eta_hat_1 <= -0.34`) | now `<= -0.33`, values listed | `sweep.json`; the round-1 referee's independent sweep logs | **Resolved.** −0.513, −0.551, −0.502, −0.545, −0.3375. |
| Nit 2 ("decided by `e_2`") | "coincide with small `e_2`", with the after-the-fact caveat, in the status table, Summary item 6, 7.2 and 9.3; pointer added in Section 13 | read all four places and the data | **Resolved.** Breaking grids have `e_2 <= 0.079`, the others `>= 0.1756`. Every place now says that the separation was read off the same 14 grids and was not tested. |

Other round-2 edits: the header (two reviews; round 2 not re-reviewed), the
Section 13 preamble, Section 12 items 18–20 and Section 14. All are accurate.
The `rev2_checks.py two4000` call uses the same `certify_multi` settings as
`run_multi.py two` (`max_nodes = 150`). The quoted times (77–82 s) match the
log.

## 2. Declined items and strengthening

No item was declined. I compared each round-2 passage with the evidence. R1
replaced a claim the evidence did not support with one it now supports, and I
confirmed that claim independently. R2, R3 and the nits only narrow or hedge
the text. No new claim goes beyond its evidence. The only remaining issue is
P1, which concerns the accuracy of quoted float numbers, not the strength of
any claim.

## 3. Remaining problem

**P1 (minor; numbers in a float observation; conclusion unchanged).** The
sweep code computes the phase position of the first switch as

```
theta1 = n1 * h + h * (1 - u[n1]) / 2      (run_multi.py, line 263; n1 = s1 fractional)
```

The first switch goes from `u = +1` to `u = -1`. For that direction, the
phase model of [W, Remark 1.4] (a switch at continuous position `theta`, one
interior control at stage `floor(theta/h)`) gives
`u_n = (+1) f + (-1)(1 - f)` with `f` the fraction of the stage before the
switch. Hence `theta_1 = n1 h + h (1 + u[n1]) / 2`. The code's formula is
also inconsistent with its own vertex rule: as `u[n1] -> -1` it gives
`(n1 + 1) h`, while a vertex `u[n1] = -1` gives `n1 h`. The two formulas
differ by `h u[n1]`, so only grids with a fractional first switch are
affected.

I rebuilt each affected KKT point with my own code. The round-1 referee's
independent sweep logs (`kappa-negative-confirm-r1-checks/logs/sweep_m690.log`,
`sweep_m490.log`) give the same `u[s1]`. Break offsets are from `sweep.json`;
the round-1 referee reproduced them on every grid. Corrected
`break time − theta_1` (`logs/phase.log`):

| configuration | `N` | `u[s1]` | logged (note) | corrected |
|---|---|---|---|---|
| `(0.55, 1.45)` | 4000 | −0.8821 | 5.29e-4 | 9.71e-4 |
| `(0.55, 1.45)` | 6000 | +0.5000 | 9.17e-4 | 7.50e-4 |
| `(0.45, 1.55)` | 1000 | +0.6275 | −3.73e-4 | −1.63e-3 (−0.81 stage) |
| `(0.45, 1.55)` | 6000 | +0.2647 | 2.11e-4 | 1.23e-4 |

The other 9 grids have a vertex first switch, and their values are
unchanged. Consequences for the text:

- Section 7.2 (line 1095): "`2e-4` to `9e-4`" should be about `1.2e-4` to
  `9.7e-4`. Line 1098: "`0` and `-3.7e-4`" should be `0` and `-1.6e-3`.
  Line 1103: the matching times should be about 0.30–0.35, 0.10–0.17 and
  0.29–0.48, not 0.30–0.35, 0.09–0.16 and 0.48–0.50.
- Section 9.3 (lines 1424–1429): `(0.55, 1.45)`: `5.7e-4 … 9.7e-4`;
  `(0.45, 1.55)`: `1.2e-4 … 2.0e-4`, not `2e-4`; the `N = 1000` value
  `-1.6e-3`.
- Section 14, R3 (lines 1956–1965): the same corrections. The round-1
  review's `-3.7e-4` came from the same log value.

What survives: the overall matching-time range is about 0.10–0.48. This still
lies inside "about 0.1 to 0.5", a factor of about 5, so the hedged conclusion
in 7.2 and 9.3 stands. The `N = 1000` exception becomes more pronounced. The
larger-`N` times stay roughly constant per configuration (factors 1.2, 1.7
and 1.6).

*Fix:* correct the formula in `run_multi.py` to `(1 + u[n1]) / 2` (or
recompute in `rev2_checks.py tallies` from the logged offsets and `u[s1]`).
Then update the numbers in 7.2, 9.3 and 14, and give the convention for
`theta_1` once.

## 4. Literature examined by this referee

- [W] `theory-bangbang/window-exactness.md`, Remark 1.4 (phase model), read
  for the definition of the phase position.
- The round-1 confirmation review and its check logs (`sweep_m*.log`), used
  as an independent source of `u[s1]` and break offsets.
- No web searches and no new literature. The note's novelty statements were
  not changed in round 2, and I did not re-examine them.

## 5. Commands run (targeted only)

All commands were run from `reviews/kappa-negative-confirm-r2-checks/` with
`OMP_NUM_THREADS=1` and an explicit `timeout`. No project-wide verification
was run, CI was not inspected, nothing was committed, and no process was
killed.

1. `python3 c2_cert.py logs/cert4000.json` → `logs/cert4000.{log,json}`
   (exact; about 2 s in total).
2. `python3 c2_author_partition.py` → `logs/author_partition.log` (exact;
   reads `theory-bangbang/kneg/logs/rev2_two4000.json` for node intervals
   only).
3. `python3 c2_phase.py` → `logs/phase.log` (float; reads
   `theory-bangbang/kneg/logs/sweep.json` for `s1`, `s2`, fractional stages
   and break offsets).
4. `python3 c2_eps.py` → `logs/eps.log` (float).
5. Read-only inspections: `rev2_checks.py`, `run_multi.py` (the `theta1`
   line, the `certify_multi` settings), `ktoy.py` (data conventions),
   `logs/rev2_*.json`, `logs/two.json`, `logs/qneg.json`, and the round-1
   referee's sweep logs.
