# Earlier and superseded certificates and displays

This file is the one home of the project's display and certificate history. The
paper and the supplement print only the current certificates and their
displays; the display rules are in Section 2.4 of the paper and the display
record of the supplement (`app:displays`). Paths are relative to the root of
the archive (`$R` = `research-20260929/`, `$P` = `paper-open-minlplib/`); labels
in backticks name objects of the paper. Checker paths and run records of the
current certificates are in `RUNS.md`. "Round 1", "round 2" and "round 3" name
the authors' internal review rounds before submission (`README.md`).

## 1. Strings in older records that must not be read as bounds

Logs and older reports in the archive contain strings that must not be read as
bounds: a shortest round-trip string of a binary64 number (Python's `repr`) can
lie on either side of the number, and fixed-digit prints are rounded to nearest.
The table lists the strings that we know to be unsafe or superseded, including
those corrected in the version of the paper that this archive accompanies, with
the reason and the display used in the paper. Each entry was rechecked against
the exact value or certificate end in exact rational arithmetic (2026-10-04,
against `$P/data/numbers.json`,
`$R/publication/reproduction/cops/logs/exact_display_checks.json` for the
`catmix` primal ends of the first implementation's points, and
`$R/reviews/open-instances-verification/logs/lnts_verify.json` for N·h₂ of the
second `lnts` implementation; the round-1 rows in `$P/development/reviews/round1/g7-checks/`
(`audit-displays.log`, `powerflow-widths.log`) and
`$P/development/reviews/round1/sol-numbers.md` (SCIP witness residual
32122061/10995116277760000000000); margin and percent rows from the exact
values in the decision register and `numbers.json`; the QPLIB margins from
`numbers.json`, `claims_table`). "Above" and "below" compare the string with the
exact value or certificate end that it was meant to represent; differences are
approximate.

| instance, quantity | string in older records | problem | display in the paper |
|---|---|---|---|
| `lukvle10`, L | 352.2380254050785 | 4.4·10⁻¹⁴ above the certified end | 352.2380254050784 |
| `lukvle10`, L | 352.238025369202 | valid but superseded (the first implementation's weaker certificate) | 352.2380254050784 |
| `lnts100`, `lnts200`, `lnts400`, L | 0.5545954011663566, 0.554595401111452; 0.5545770161025291, 0.554577016047626; 0.5545724136452299, 0.554572413645230 | roundings to nearest of the lower ends that earlier computations certified (Section 2, item 1), above them by about 5·10⁻¹⁸ to 4·10⁻¹⁶; superseded by the exact optima | floor and ceiling of v* (`tab:closures`) |
| `dtoc5`, absolute gap | 7.2·10⁻⁴³ | below the exact certificate gap 7.2051…·10⁻⁴³ | 7.21·10⁻⁴³ |
| `optcdeg2`, L | 293.87607509587509238 | rounded up; 6·10⁻¹⁹ above the rigorous evaluation | 293.87607509587509237 |
| `optcdeg2`, objective at the point | 293.876075095875093277……559491 ± 5·10⁻⁶⁴ | the 45-decimal string lies 4.7·10⁻⁴⁷ below the objective, so the interval does not contain it | U = 293.87607509587509328 |
| `chain50`, L | 5.072261493982863 | shortest binary64 string; 2.5·10⁻¹⁶ above the bound | 5.0722614939828627 |
| `chain200`, L | 5.068917341793162 | shortest binary64 string; 3.3·10⁻¹⁶ above the bound | 5.0689173417931616 |
| `catmix100`, L | −0.04806943203114456 | shortest binary64 string; 1.4·10⁻¹⁸ above the bound | −0.048069432031144562 |
| `catmix200`, L | −0.04805914560067171 | shortest binary64 string of the first implementation's weaker bound; 1.3·10⁻¹⁸ above it | −0.048059145599072769 |
| `catmix800`, L | −0.04805590147967565 | shortest binary64 string; 1.5·10⁻¹⁸ above the bound | −0.048055901479675652 |
| `catmix100`, U | −0.0480694320309595635 | binary64 value printed with 20 digits as the exact objective; 5.8·10⁻¹⁹ below the upper end of the enclosure | −0.0480694320309595629 |
| `catmix200`, U | −0.0480591455801144; −0.0480591455801143916 | binary64 values printed as the objective; the first lies 6.4·10⁻¹⁸ below the upper end, the second 2.0·10⁻¹⁸ above it with wrong digits after …11439 | −0.0480591455801143935 |
| `catmix400`, U | −0.048056547756611555 | 1.4·10⁻¹⁹ below the upper end | −0.0480565477566115548 |
| `catmix800`, U | −0.048055901330847467 | 1.1·10⁻¹⁹ below the upper end; superseded by a better point | −0.0480559013312308003 |
| `ex6_2_5`, L | −70.75207783344770758 | 3.5·10⁻¹⁹ above the certified end | −70.75207783344770759 |
| `ex6_2_5`, U | −70.752077833447706 | 4.2·10⁻¹⁶ below the upper end of the objective enclosure | −70.75207783344770558 |
| `ex6_2_7`, L | −0.16084761546364904 | 3.4·10⁻¹⁸ above the certified end | −0.16084761546364905 |
| `etamac`, L | −15.294675643368092, −15.294675643368092168 | 1.7·10⁻¹⁶ and 5·10⁻¹⁹ above the certified end | −15.29467564336809217 |
| `eg_disc_s`, L | 5.760539610694994 | target of the leaf re-certification, 2.4·10⁻¹⁶ above the binary64 bound of the first implementation's search, which therefore does not confirm it | 5.760539610694993 |
| `powerflow0039r`, L | 41869.05148327244 | 6.0·10⁻¹² above the exact bound | 41869.05148327243 |
| `powerflow0039p`, `powerflow0039r`, L | 41868.26524, 41867.77921 | superseded earlier bounds; the first could not be reproduced | `tab:closures` |
| `powerflow0030r`, L | 576.8934126255 | bound for the rectangular twin, never verified | none (no claim) |
| `powerflow0039p`, `powerflow0039r`, `ann_cumene_tanh`, U | 41869.0515113202, 41869.0515113208; −3379.9824 | objective values of earlier points rounded to nearest; 3.8·10⁻¹², 1.8·10⁻¹⁰ and 5.9·10⁻⁶ below the upper ends of the enclosures at the exactly feasible points | 41869.0515113203, 41869.0515113210 (`tab:closures`); −3379.9823940 (`tab:unclosed`) |
| `topopt-cantilever_60x40_50`, objective | 10.335474275747004, 13.077481991525133 | binary64 roundings to nearest of rational upper bounds of the second implementation; may lie below them | `tab:audit-pairs` (archived points) |
| `glider100`, `methanol50`, `nuclear14`, second φ | −983842.2577881224, 0.0079302187992, −1.12968744117116 | printed as upper ends, but below the exact upper ends by 1.5·10⁻¹¹, 4.1·10⁻¹⁴ and 3.4·10⁻¹⁵ | −983842.2577881223, 0.0079302187993, −1.12968744117115 (`tab:audit-second`) |
| `powerflow0039p`, `powerflow0039r`, enclosure width | ≤ 2.8·10⁻⁴² | below the exact widths 2.8208…·10⁻⁴² | ≤ 2.83·10⁻⁴² (`tab:points`) |
| `methanol50`, coefficient change | at most 2.38·10⁻¹⁶ | below the exact maximum 1/4196280000000000 = 2.383…·10⁻¹⁶ | 2.39·10⁻¹⁶ (`app:audit-history`) |
| SCIP witnesses, binary64 residual | at most 2.9·10⁻¹⁵ | below the exact maximum 2.9215…·10⁻¹⁵ | 2.93·10⁻¹⁵ (`prop:scip-witnesses`) |
| `waterno2_06`, relative gap | 1.67% | below the exact 1.674…% | 1.68% |
| `waterno2_12`, `waterno2_18`, factor | 4.36, 6.22 | rounded to nearest, above the exact 4.358… and 6.2159… | 4.35, 6.21 |
| `kan_r5_h1_n5`, relative gap | 3.73·10⁻¹⁰ | below the exact 3.7337·10⁻¹⁰ | absolute gap only (`tab:kan`) |
| `ann_cumene_tanh`, earlier gap | 16.01% | below the exact 16.0147% (dual denominator) | not used |
| `lnts50`, listed relative gap | "within 3.8·10⁻⁵" | below the exact 3.8248·10⁻⁵ | 3.9·10⁻⁵ |
| `lnts50` p1, margin below v* | 4.24·10⁻¹¹ | valid but measured against an older, weaker dual | 4.30·10⁻¹¹ |
| `camshape100`, BARON margin | 5.26·10⁻⁷ | above the exact 5.2581…·10⁻⁷ | 5.25·10⁻⁷ |
| `optcdeg2`, Gurobi p2 margin | 1.459 | above the exact 1.4589… | 1.45 |
| QPLIB copies, margins | ≥ 3.162849·10⁻³, ≥ 1.552322·10⁻⁴; later 3.162·10⁻³, 1.552·10⁻⁴ | the first above the exact values; all valid only for displays rounded to nearest | 3.11·10⁻³, 1.54·10⁻⁴, for any value within one unit of the last displayed digit (`prop:qplib-copies`) |
| `eg`, CAMINO margins | 4.3%, 7.5%, 81% as "at least" | the last two exceed the exact 7.487…% and 80.598…% | 4.33%, 7.48%, 80.5% (`sec:intro`, `prop:camino-eg`) |
| `camshape`, amplification | "about 600-fold" | not supported by a proof | the deficit bound D_n(ε) (`prop:camshape-deficit`) |

The rows above the waterno2 gap concern bounds, primal values and widths; the
rows from there on concern gaps, factors and margins.

## 2. Superseded certificates (valid, weaker or replaced)

These certificates are valid; later certificates of the paper supersede them,
and the paper no longer prints them. The round-1 version of the supplement
printed them in Section S1; the first internal review round removed them. The dossiers
named below are the sources in the archive.

1. **Earlier `lnts` dual.** The `lnts` dual bound that was verified first
   applied `prop:lnts-support` at the shifted step h₂ = h*(1 − ε) in mpmath
   interval arithmetic: the first implementation `$R/open-instances/lnts_bound.py`
   at ε = 10⁻¹⁰ (60 digits) and the second implementation
   `$R/reviews/open-instances-verification/v_lnts.py` at ε = 10⁻¹⁰ and 10⁻¹²
   (50 digits, own reader), two implementations with two readers. The certified
   bound N·h₂ left gaps of at most 6.2·10⁻¹³. `thm:lnts-opt` supersedes it with
   the exact optima and removes mpmath from the dual side. Source:
   `$P/development/dossiers/lnts-lukvle10.md` (Sections 2 and 6 and the
   verification table); the round-1 supplement printed it in its verification
   record (former table `tab:lnts-verification`).
2. **Two earlier `dtoc5` bounds.** Both have the form of `thm:dtoc5-bracket`,
   with multipliers from a Newton solve, evaluated in mpmath intervals. The first
   implementation (`$R/open-instances/dtoc5_bound.py`, output
   `logs/dtoc5_bound.json`) used λ = −2u from a double-precision Newton solve and
   30 digits: 5.3896721191811325. An earlier second implementation
   (`$R/reviews/open-instances-verification/v_dtoc5.py`, output
   `logs/dtoc5_verify.json`) used its own Newton solve plus three 40-digit Newton
   steps, with λ rounded to doubles: [5.3896721191811404674239647238640027,
   …8610945]; it agrees with the exact evaluation to about 1.8·10⁻²⁴, but its
   multipliers were not stored, so reproducing it means regenerating them. An
   earlier summary display, 5.38967211918114, lay above the first
   implementation's certificate and rested on these unstored multipliers. The
   exact certificate of `thm:dtoc5-bracket` supersedes both. Source:
   `$P/development/dossiers/dtoc5-optcdeg2.md` ("Earlier certificates of the
   same form", item 1 of the summary, DO-5).
3. **The `optcdeg2` progression.** Successive lower bounds, all valid; each gap
   is computed from the certified value of the bound (whose display is shown)
   and the upper end of the objective enclosure of `prop:optcdeg2-point`, and
   rounded up.

   | certificate | lower bound | gap |
   |---|---|---|
   | affine split, earlier multipliers (mpmath intervals) | 293.2500703 | 0.627 |
   | same, plus an exact window over stages 0–3079 (mpmath intervals) | 293.8699938 | 6.09·10⁻³ |
   | quadratic calibration, interval cells (own outward-rounded binary64) | 293.8760750958728 | 2.29·10⁻¹² |
   | quadratic calibration, exact (`thm:optcdeg2-bound`) | 293.87607509587509237 | 8.98·10⁻¹⁶ |

   In the second row, a monotonicity certificate (positive interval enclosures
   of the costate p^v over the reachable states) shows that the all-lower
   control minimizes the window formed by the first 3,080 stages
   (`prop:split-window`). The first wave's head-block certificates were
   293.8699938542 at m = 3080 and 293.8700386118 at m = 3090. The third row is
   the weaker bound of the first implementation, which the paper still prints
   as such (`tab:trust-full`, Section 4 and S1.2). Source:
   `$P/development/dossiers/dtoc5-optcdeg2.md` (the affine failure, DO-5 and the
   table plan); the round-1 supplement printed the table (former
   `tab:optcdeg2-progression`).
4. **Earlier `camshape` code.** The first implementation's original
   computation (`$R/open-instances/camshape_bound.py`, `camshape_model.py`)
   asserted the structure of the OSIL files and evaluated U, S, R and E in
   mpmath intervals at 0.4n + 60 digits from the decimal constants (read as
   `repr(float(s))`, which is exact because every constant has at most 15
   significant digits), using upper ends only in the envelope; it evaluated the
   envelope as a primal point in 50-digit arithmetic (violations at most
   4.8·10⁻¹⁶, from float storage). Its bound is valid and its values agree with
   `thm:camshape-opt`, whose three exact or directed-rounding codes supersede
   it. Source: `$P/development/dossiers/camshape.md` (Section 6); the round-1
   supplement mentioned it in its verification record.

## 3. Historical checkers

- **Unguarded second KAN code (path (I)).**
  `$P/development/dossiers/ann-kan-checks/kan_bnb_rigexp.py` with arguments
  `<name> 4e-11 1800 1024`, run beside the second implementation's modules in
  `$R/reviews/wave3-verification/` (logs in
  `$P/development/dossiers/ann-kan-checks/logs/`), was the second checker of
  `thm:kan-enclosure` until round 1: 55 CPU-minutes for all six models on a
  loaded machine (25.7, 23.1 and 54.9 s for the `r3` models; 1,221, 761 and
  1,188 s for the `r5` models, from the `time` fields of its `*.bnb.json`). A
  review (`$P/development/reviews/round1/sol-math-supp2.md`, item 1) found that
  its quadratic routine `minquad` assumes that halving a binary64 curvature is
  exact and can return a value above the true minimum for a subnormal
  curvature. The guarded copy in `$P/development/reviews/round1/kan-guard/`
  replaced it as the second checker; its replay reproduced all six bounds of
  the unguarded code bit for bit, with no guard trigger (`RUNS.md`, R20).
- **Library-exponential second KAN code.** An earlier branch and bound of the
  second session, `$R/reviews/wave3-verification/kan_bnb.py`, used the library
  exponential (an assumption, not a proof); five of its bounds equal the
  rigorous-exponential ones bit for bit, and its `kan_r5_h1_n3` bound is about
  3.2·10⁻¹² higher. It supports no claim of the paper.

## 4. History moved from the supplement

The second internal review round moved the following passages out of the
supplement. Each heading names the source in the round-3 sources (file and
label); the text is quoted with the notation simplified for Markdown, and
"first code" and "second code" are the first and second implementations of
Section 2.6 of the paper.

### `J-displays.tex`, `app:displays` (the former Section S8): provenance of the table in Section 1

The table of Section 1 was the table `tab:displays-unsafe` of the former
Section S8, now Section S7.5 of the supplement, which keeps the display rules.
Its plan is in `$P/development/outline.md` (Section 6, item J; the unsafe
strings in Section 8, item 11) and in the decision register
(`$P/development/decision-register.md`, items CC-09, SM-06, PP-04, LL-09 and
AU-05). Every offset was rechecked on 2026-10-04 in exact rational arithmetic,
with a script and inline `Fraction` checks that were not archived
(`/tmp/appj/check.py`), against the sources listed in Section 1. The margin
and percent rows use the exact values in the decision register (Section 5), the
solvers, ann-kan, audit and lnts-lukvle10 critiques, and `numbers.json`. The
CAMINO percentages are the exact (bound − U)/U from the values of
`prop:camino-eg` and the U of `numbers.json` (4.3352%, 7.4870% and 80.5977%),
as in `$P/development/numbers-check.md`, item 16.

### `B7-eg.tex`, `app:eg-model`: an earlier interval branch and bound

An earlier interval branch and bound of the project, which intersected
term-wise enclosures of the objective rows with a mean-value form, reached only
the bound 2.43 for `eg_int_s` after 603 s; a bound that adds up the ranges of
individual terms loses the cancellation of the weights. Its enclosure remains in
the supplement as "the earlier enclosure" (S1.7, evidence paragraph, and
`fig:eg-enclosures`a).

### `B8-waterno2.tex`, `app:waterno2-proof` (after `tab:waterno2-values`): the multiplier searches

For the other four instances (`waterno2_09` to `waterno2_24`; `waterno2_06`
uses cellwise slopes) only the period Lagrangian was used; the multiplier
searches for `waterno2_18` and `waterno2_24` were stopped with a predicted
further gain of about 1–2, and the one for `waterno2_24` started from zero
multipliers.

### `B9-ann-kan.tex`, `app:annkan-kan-enclosure`: the first run of path (I)

In its first run, path (I) of the KAN enclosure (the second code) used the
library exponential widened by a relative 2⁻⁵⁰, an assumption supported only
by sampling (the library-exponential code of Section 3). It was rerun with that
one function replaced by the enclosure of path (II) (a 64-entry table, a
degree-8 Taylor polynomial with remainder at most 10⁻²⁵, one `nextafter` step
per operation, exact scaling by powers of two, and constants checked in exact
rational arithmetic); the rest of the code has an identical syntax tree, and all
runs ended with no open box (`tab:kan-rerun`). This rerun is the unguarded
second code of Section 3, which the guarded copy replaced; the review of the
change and the run times are in `RUNS.md` (row R20).
