# Verified numbers for the paper

This directory holds the single source of the numbers that the paper displays,
and the script that checks them and writes the LaTeX tables.

| file | content |
|---|---|
| `make_tables.py` | reads the sources below, checks the certified bound, primal, gap and margin displays that it generates with exact rational arithmetic, writes `numbers.json`, `check.log` and `../tables/tab-*.tex` (except the two tables below) |
| `make_campaign_table.py` | `../tables/tab-campaign-runs.tex` from `numbers.json` and the campaign results; checks every finite one-hour dual against the certified bound |
| `make_points_table.py` | `../tables/tab-points-all.tex` from `numbers.json`; checks the direction of every primal display |
| `numbers.json` | all displayed numbers, each with its exact value or enclosure end and its source |
| `check.log` | output of the last run: every check, then the SHA-256 of every file read |
| `../figures/make_fig_headline.py` | Figure 1 from `numbers.json` (`headline_figure`) to `../figures/fig-headline.pdf` |

Run from anything outside the source trees, for example:

```bash
cd /tmp && python3 <repo>/paper-open-minlplib/data/make_tables.py
cd /tmp && python3 <repo>/paper-open-minlplib/figures/make_fig_headline.py
```

`make_tables.py` uses only the Python standard library, imports no project
module, and runs no certificate or search. It exits with status 1 if any check
fails. It takes about 5 seconds on one core. The figure script needs
matplotlib.

## Conventions

- Model: the stored OSIL file, decimals read as exact rationals; exact
  feasibility (outline section 4.1).
- Dual bounds are rounded down (up for the maximization instance pricing050).
  Primal values are rounded up (down for pricing050). Gaps are rounded up.
  "At least" margins and improvement factors are rounded down. Nothing is
  rounded to nearest.
- Absolute gap: Delta = s(U - L) from the exact certificate ends (not from the
  displays), three significant digits, rounded up.
- Relative gap: delta = Delta / min(|L|, |U|), three significant digits, rounded
  up. Percent cells have two decimals (three significant digits below 1%),
  rounded up.
- Exact optima (lnts, camshape, hvycrash): Table 2 prints "exact optimum" in
  the gap cells; L and U are the floor and ceiling displays of v*.
- Where the printed displays of L and U differ by more than the gap cell, the
  record has `table_footnote_cert_ends: true` and Table 2 marks the cell.
- Listed data: best single-solver dual bound on the instance page; best listed
  point with listed violation <= 1e-8 (`best_point`). Pages fetched 2026-09-29/30
  (`research-20260929/bound-audit/pages.json`), unchanged at the 2026-10-02
  refresh. Sizes and sense come from the refreshed OSIL files in
  `research-20260929/publication/minlplib-status/pages/models/osil/`.

## Sources of the certified values

Every record in `numbers.json` names its source file and field. Below, `R/` is
`research-20260929/` and `development/` is `paper-open-minlplib/development/`. Summary:

| family | dual L | primal U |
|---|---|---|
| lnts50-400 | exact rational enclosure of the optimum, `development/reviews/code/sol-lnts-review/certificate.json` (`opt_exact`) | same (attained optimum) |
| dtoc5 | `development/reviews/code/sol-dtoc5-review/result.json` (dual `down_100`); `dossier_lower_exact.txt` also certifies the display | `primal_exact.txt` (= primal-track exact objective) |
| optcdeg2 | `R/reviews/bangbang-verification/logs/qcal_exact.json` (`bound_str`) | `.../primal_check.json` (`J_upper`) |
| lukvle10 | `R/reviews/closing-confirm-r2-checks/logs/lukvle10_lower_end.log` | `R/publication/primal/dtoc5-lukvle10/logs/lukvle10_enclose.json` |
| chain | `R/open-instances-wave2/cops/logs/chainN_bound.json` (binary64, exact) | `R/publication/primal/chain/points/chainN_box.json` |
| catmix | `R/publication/reproduction/cops/logs/exact_display_checks.json` (verifier/recheck doubles) | same file, `primal_hi` |
| camshape | `development/dossiers/checks/camshape/check_exact.json` (`opt_30` +- 1e-30), cross-checked with the verifier log | same |
| ex6_2_5/7 | `R/reviews/closing-confirm-r2-checks/logs/ex6_2_5_lower_end.log` | `development/dossiers/primal-points-checks/logs/ex62_check.log` (mpmath-free) |
| etamac | certified end -15.2946756433680921685 (small dossier 3.3, register N-09) | `development/dossiers/small-checks/r2/etamac_point.log` |
| pricing050 | `development/dossiers/small-checks/r2/pricing_check.log` (upper bound) | same log, exact objective of the saved point |
| pindyck | recomputed here: -(J_hi + |g|^2/(2 mu)) from `R/reviews/pindyck-review-checks/logs/primal_enclosure.txt` | -J_lo, same file |
| powerflow | `sdpcert.json` / `bb3t.json` exact bounds | `R/publication/primal/powerflow/logs/certify.*.log` |
| eg | min(route R target in the review verify logs, S-route binary64 in `development/dossiers/checks/eg/r2/logs/displays.log`) | `*.retry.sol` objvar |
| waterno2 | `certB_verify.json` (06), `cert_TT_w1_impl.json` (09-24) | `R/publication/primal/water-ann-kan/points/*.exact.json` |
| ann, KAN | point files in `R/publication/primal/water-ann-kan/points/` (`dual_bound`, `objective_hi`) | same |

Other sections: the audit (`R/bound-audit/results.json`, `pages.json`,
`screen.json`), the one-hour runs (`R/publication/solver-runs/results_table.csv`,
`point_checks.json`, and `inconsistencies.json` for the returned objective values
of the trace files and their count in the caption of `tab:claims`), the
contradicted-claims table (sources per row; the field `evaluation` says whether a
value is as reported, `none`, an exact evaluation of the objective at the point,
`exact`, or an ordinary high-precision evaluation without an enclosure,
`numerical`), and
the eg exp/pow audit status (`development/eg-audit/out/compare.log`; the trust
table switches from "pending" to "passed" when its last line reports a complete
PASS).

Displays follow section 5 of the decision register (rows marked checked)
rather than `R/open-instances-summary.md`: lnts exact optima (N-01 to N-04), the
dtoc5 rational certificate (N-05), lukvle10 (N-06), ex6_2_5 and etamac (N-08 to
N-10), the pricing050 gap 1.92e-14 (N-11), the pindyck strong-concavity bound
(N-12), the individual chain and catmix displays (N-13 to N-20) and eg_disc_s
(N-23). The eg verification wording (N-24) follows the audit status above. For
dtoc5 the script uses the review's 100-digit outward enclosure of the full
rational dual instead of parsing the 9-million-bit fraction.

## What the checks cover

- each L and U display lies on the safe side of its exact value or enclosure
  end, and L <= U (L >= U for pricing050);
- each gap cell bounds the exact gap and is not above the summary's cell;
- cross-checks between independent sources (both chain codes give the same
  double; dtoc5 review rational equals the primal track; lnts review hash equals
  the refreshed OSIL; KAN point-file bound equals the search log; etc.);
- OSIL sizes and sense agree with the instance pages; no instance has a solved mark;
- waterno2 percent cells equal the summary cells; factors are rounded down;
- the 19 audit pairs: margins exceed one display unit, labels, counts
  (1,633 pages, 2,816 points, 11,086 bounds, 158 screened pairs, 3,851 ties);
- the campaign counts per solver, and that every finite one-hour dual is weaker
  than the certificates in this file;
- every margin in the claims table is positive and rounded down; the lnts50 p1
  value equals 50 times its step variable exactly; every returned objective
  value of the trace files that lies beyond a certified bound by more than its
  printing precision does so in exact arithmetic, and for the 15 evaluated
  points it agrees with the 50-digit evaluation to its printed digits;
- headline facts: largest closure gap 3.1e-9 (catmix800), 9 exact optima,
  factor range 1.68 to 6.21; 22 invalid listed bounds on 18 instances with the
  three rocket bounds (16 LINDO); every class (i) margin at least 1.115 display
  units;
- the campaign partition of the 109 finite final duals: 79 bounds on the
  unmodified GAMS models with a globality guarantee and no tightened bounds, 6 disclaimed by BARON, 6
  SCIP bounds on tightened models, 18 KAN comparisons; only two runs end within
  a relative gap of 1e-6;
- prior status (7 floating-point closures or near-closures, 9 other earlier
  results, 15 none) and evidence levels (14 rerun, 7 stored, 9 hand+stored, 1
  hand) of the 31 closures;
- the fixed width cells of the points table against exact widths
  (`development/reviews/round1/g7-checks/powerflow-widths.log`) and the lnts
  Krawczyk-point log; the QPLIB margins against the floors of the copies' exact
  optima, for any reported value within one unit of its last displayed digit.

Tables typed in the LaTeX sources (for example `tab:audit-second` in
`sections/E-audit.tex`) are not read by these scripts and are checked
separately; `sections/J-displays.tex` records those checks.

`numbers.json` records, for each display, the documents (register, outline,
summary, dossiers, reviews) that print the same string (`*_printed_in`).
Displays marked "new" were generated here from the exact value.
