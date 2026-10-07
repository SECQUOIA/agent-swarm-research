# Referee check of the third revision of "Split-robust lower bounds on uniform chains"

Date: 2026-09-30. Note checked:
`research-20260929/theory-robust-lb/robust-chains.md`, revised after review
round 3 (1958 lines; changes listed in its Section 10.3). The review that
asked for the changes is `reviews/robust-lb-chains-confirm-r2.md`,
Section 3. I wrote neither the note, its scripts, nor that review. My
scripts and logs are in `reviews/robust-lb-chains-confirm-r3-checks/`. They
share no code with the note's `chains/` scripts or with the earlier
reviews' checks.

Following `AGENTS.md`, I ran only targeted checks: no project-wide
verification, no CI. I did not commit anything or edit the note.

Labels used below:

- **proved**: checked by hand, step by step;
- **float**: recomputed in floating point (cvxpy with Clarabel, and SCS
  where stated), not certified;
- **heuristic**: a computation whose link to the claim is not proved.

## Verdict in brief

All three review items were applied correctly. Nothing was refused.
Nothing was strengthened beyond its evidence. Every new or changed number
was recomputed with my own code, from both sides of the duality (moment
side and SOS side), and agrees with the note. The note's own round-3
script, rerun, reproduces its logs byte for byte.

| Review item | Verdict |
|---|---|
| 1. Closing paragraph of Section 4.6 overgeneralized | **fixed.** The sentence now says "some of the other placements" and names the placements without a gap. New radius rows recomputed. |
| 2. Waki et al.: section numbers and the "analogue" remark | **fixed.** Section numbers now match the headings of the local copy at every place; the paper's own inconsistent cross-reference is described correctly; the "analogue" remark is withdrawn; the scaled bounds are stated correctly; the new gaps are recomputed. |
| 3. Credit for case (b) | **fixed.** Case (b) is moved out of "New here" in Section 10.2 and credited to the round-2 review, with a correct quotation. |

One small accuracy point remains (Section 4.1 below): a parenthetical in
Section 8 says the third review's code reproduces all the moment-bound
gaps, but that review did not compute the new row "opposite orientation +
scaled bounds". It is a one-phrase fix. Two optional wording points are in
Section 4.2.

## 1. Item 1 (closing paragraph of Section 4.6)

**The change.** Lines 1321–1326 now read: "those that localize the box
constraints as in Proposition C.5 are exact at the root, and some of the
other placements above have a root gap or are unbounded ... Not every
placement outside Proposition C.5 has a gap: the ball with `M = 1.1`,
`1.3` or `1.5`, and `1 - x_i^2` in one clique or with univariate
multipliers, showed none (floating point)." This is the requested fix,
and the added sentence is accurate.

**The cited numbers.**

- The three rows from the round-2 log (`chains/logs/revision2_sos.log`) are
  as stated: `M = 1.1` gives `6.8e-8` and `1.14e-7`; `1 - x_i^2` in one
  clique gives at most `5.6e-9`; `1 - x_i^2` with univariate multipliers
  gives at most `1.2e-8`. (Section 10.3 says "at most `1.1e-7`" for the
  first; the value is `1.139e-7`. This is rounding only.)
- I reran `chains/revision3_chains.py waki` and `radius`. The output is
  identical to `logs/revision3_waki.log` and `logs/revision3_radius.log`.
- My own code (`e1_two_sides.py radius`, `e1_radius.log`) gives, for the
  opposite orientation with the ball (float):

  | `M`, `n` | SOS side | moment side | note |
  |---|---|---|---|
  | 1.5, 16 | `4.7e-8` | `2.6e-7` | `2.6e-7` |
  | 1.5, 32 | `6.8e-8` | `5.2e-7` | `5.2e-7` |
  | 2, 16 | `-0.1328177` | `-0.1328175` | `-0.1328175` |
  | 2, 32 | `-0.3783881` | `-0.3783857` | `-0.3783857` |

  The round-3 review's values (`d5_radius_n.log`: `-0.1328178`,
  `-0.3783882`) also agree.
- "About 0.015 per variable from `n = 8` to `32`": `(0.3784 - 0.0158)/24 =
  0.0151`. Correct.

**The range "`M = 1.1`–`1.5`" in Section 7 is justified (proved).** The
value of the relaxation is nonincreasing in `M`. The localizing matrix of
`2M^2 - x^2 - y^2` in the basis `(1, x, y)` equals `2M^2 M_1` minus a
matrix that does not depend on `M`, where `M_1` is the order-1 moment
matrix of the clique. `M_1` is a principal submatrix of the order-2 moment
matrix, so it is PSD at every feasible point. Hence a point feasible for
`M` is feasible for every `M' > M`. So "no gap at `M = 1.5`" implies "no gap
for every `M <= 1.5`" at the same `n`. My scan at `n = 8` and `16`
(`e1_monotone.log`) is monotone in `M`, as it must be.

**Long chains (float; heuristic link).** Does "no gap at `M = 1.5`" survive
beyond `n = 32`? I solved the per-bond (bulk) problem: maximize `gamma`
with `W(x, y) + h(x) - h(y) - gamma` in the truncated quadratic module of
`1 + x`, `1 - y` and the ball, with `h` univariate of degree at most 4
(`e2_bulk_radius.py bulk`, `e2_bulk.log`).

- Controls: the orientation of case (b) gives `0` in the bulk. The opposite
  orientation without a ball gives `-0.05208` per bond. The finite-`n`
  slope is `(0.2072 - 0.0553)/3 = 0.0506`.
- With the ball, the bulk is exact (`gamma = 0`) up to
  `M = 1.58348` (bisection) and has a gap above it. At `M = 2` the gap is
  `0.01538` per bond, which matches the finite-`n` slope of 0.0151.
- So `M <= 1.5` is exact in the bulk, which supports the note's "no gap"
  for `M = 1.1, 1.3, 1.5` beyond the tested `n`. The finite-`n` runs at
  `n = 64` (`M = 1.1, 1.3, 1.5`) and `n = 128` (`M = 1.5`) show no gap
  (`e2_long.log`, at most `2.0e-6`).
- For contrast, `M = 1.6` and `1.7` show no gap at `n = 8` (and `M = 1.6`
  none at `n = 16`) but do have a bulk gap. At `n = 32`, `M = 1.7` gives
  a gap of `0.107`. So "no gap at the tested `n`" does not extrapolate to
  long chains for every radius. For the radii the note quotes it does,
  according to this float check.

The bulk value is a heuristic link to finite chains: the end terms are not
treated. It is offered only as support. The note does not need it.

## 2. Item 2 (Waki et al.)

### 2.1 The literature statements

I read `literature/papers/waki2006-sums-of-squares-and-semidefinite/fulltext.md`
(lines 300–350 and 565–615). I also read the text of `original.pdf`
through `pdftotext -layout`. The equations are missing from `fulltext.md`
but present in the PDF text.

- Section 5.4, "Supports for Lagrange multiplier polynomials": replace the
  support of the multiplier by that of one clique `C_l` with `l in J_k`,
  or of "some union `C` of sets `C_l`". Correct as the note states it.
- Section 5.5, "Polynomial valid inequalities and their linearization":
  `0 <= y_alpha <= rho^alpha` when `0 <= x_i <= rho_i`. Correct.
- Section 5.6, "Scaling": `z_i = (x_i - eta_i)/(rho_i - eta_i)`, division
  of each `g_k` by its largest coefficient magnitude, the scaled problem
  (37) with `0 <= z_i <= 1`, and then "we can add the constraints
  `0 <= y_alpha <= 1` (`alpha in F~`)". Correct.
- Section 6 (PDF lines 1540–1547): "the union `C` of all cliques `C_l`
  containing `F_k` as mentioned in Section 5.5", and "the valid
  inequalities of the form `0 <= y_alpha <= 1` given in Section 5.6".
  The note says that only the first reference is off by one. That is
  right: `0 <= y_alpha <= 1` is indeed added in Section 5.6.

The note now uses the heading numbers in Section 4.6 (lines 1287–1308),
Section 6 (lines 1497–1504) and Section 10.2 (lines 1802–1806, with a
correction note). No stale "5.5"/"5.6" reference to the wrong content
remains (`grep`). The word "analogue" now appears only in Section 6 for an
unrelated point (`P_d` classes) and in the revision log.

### 2.2 The scaled bounds as implemented

- *Definition (proved).* The note writes `0 <= L(z_i^p z_{i+1}^q) <= 1`, for
  every clique monomial of degree 1 to 4, as
  `2^{-(p+q)} sum C(p, r) C(q, s) y_{x_i^r x_{i+1}^s}`. This is the
  binomial expansion of `((1 + x)/2)^p ((1 + y)/2)^q`. `revision3_chains.py`
  implements exactly this. With univariate multipliers, the support `F~`
  of the primal SDP consists of the clique monomials of degree at most 4,
  so "every clique monomial of degree 1 to 4" is the right index set.
- *Equivalence (proved).* The note says the computed relaxation is Waki et
  al.'s form (20) with the Section 5.6 bounds, up to a positive constant.
  - `z_i` and `1 - z_i` are `(1 + x_i)/2` and `(1 - x_i)/2`.
  - The bases `(1, z_i)` and `(1, x_i)` are related by an invertible
    linear map, so the localizing cones agree.
  - The clique moment cones are invariant under the affine change of
    variables.
  - Dividing the constraints by positive constants changes no cone.
    Dividing the objective scales the value.

  So the claim holds. In (37) the bounds `0 <= z_i <= 1` are present twice
  (once from the original box constraints, once from (36)), which changes
  nothing.

### 2.3 Recomputation (float, both sides)

`e1_two_sides.py waki` (`e1_waki.log`) is my own code. The moment side
uses one global moment vector indexed by `n`-variate exponents. The SOS side
maximizes `gamma` with Gram matrices for the clique SOS terms and for the
multipliers. Each linear moment bound `L(p) >= 0` becomes a term
`lambda p` with `lambda >= 0`, and coefficients are matched in the global
polynomial ring.

| placement | note `n = 5` / `n = 8` | mine, SOS side | mine, moment side |
|---|---|---|---|
| univariate multipliers + scaled bounds | `-0.6989` / `-1.3317` | `-0.6988745` / `-1.331693` (SCS agrees) | `-0.6988746` / `-1.331693` (SCS agrees) |
| opposite orientation + scaled bounds (new in round 3) | `-0.0538` / `-0.1994` | `-0.05375047` / `-0.1994184` (SCS agrees) | `-0.05375047` / `-0.1994185` (SCS agrees) |
| univariate multipliers + `\|y_alpha\| <= 1` | `-0.0628` / `-0.1263` | `-0.06276814` / `-0.1262653` | `-0.06276815` / `-0.1262654` |
| orientation (b) + scaled bounds (control) | — | `6e-9` / `1.4e-8` | `3e-10` / `1.5e-9` |
| opposite orientation, no bounds (control) | `-0.0553` / `-0.2072` | `-0.05530552` / `-0.20718` | `-0.05530545` / `-0.2071798` |

All of the note's values are reproduced from both sides. Two derived
statements also check out:

- "about ten times larger": `0.699/0.0628 = 11.1` and
  `1.332/0.1263 = 10.5`;
- "the scaled bounds do not close the gap" in the opposite orientation:
  `0.0538` against `0.0553`, and `0.1994` against `0.2072`.

## 3. Item 3 (credit for case (b))

`reviews/robust-lb-chains-confirm-r1.md`, Section 2.1 (line 336–337)
reads: "*Proved* for the 'every clique' setting and for the one-clique
assignment in the right orientation (the same certificate)." The note
quotes this correctly in Section 10.3, and Section 10.2 (lines 1824–1829)
now lists case (b) under "Written out here, but not new", with the
reference. The renumbered "New here" item (iv) is now "quadratic box
constraints `1 - x_i^2` showed no gap in any placement tried". I checked
that the round-2 review did not report quadratic box constraints
(`robust-lb-chains-confirm-r1.md`, Section 2.1 table;
`c4_sdp_variants.log`), so this item is correctly listed as new.

## 4. Remaining problems

### 4.1 Section 8: "the third review's own code gives the same values" is too broad (nit)

Lines 1604–1607 say that the gaps with `|y_alpha| <= 1` and with Waki et
al.'s scaled bounds were computed on the moment side only, and that "the
third review's own code gives the same values". The third review computed
the scaled bounds only with univariate multipliers (`d2_sdp.log`: two rows
with `"zbound": true`, both `"place": "uni"`). The new row "opposite
orientation + scaled bounds" (`0.0538`, `0.1994`) was computed only by the
note's own code. Its Section 10.3 correctly calls this row "New here".

The value is correct. My two-sided check (Section 2.3) reproduces it. Only
the attribution of the cross-check is too broad.

**Fix (one phrase):** "the third review's own code gives the same values
for univariate multipliers". The authors may also cite this check for the
opposite-orientation row. The same applies to "moment side only for the
moment bounds" in the Section 7 row: that is accurate for the note's own
computations and needs no change.

### 4.2 Optional wording

- The Lasserre paragraph (line 1283) says "(computed, `n <= 32`)". The runs
  were at `n = 5, 8, 16, 32` (the third review added `12` and `24`).
  "`n = 5, 8, 16, 32`" would be exact. The bulk computation of Section 1
  above supports the extrapolation, so this is not a substantive problem.
- Section 8 (line 1602) says "the ball rows also at `n = 16, 32`". Only the
  rows `M = 1.1, 1.3, 1.5, 2` were run there, not `M = 1, 1.01, 10`.
- The monotonicity of the value in `M` (Section 1 above, proved in three
  lines) would make the "`M = 1.1`–`1.5`" range of Section 7 self-evident.
  It would also show that the `M = 1.1` and `1.3` runs are implied by the
  `M = 1.5` run.

## 5. Refusals, and was anything strengthened?

- Nothing was refused.
- I compared every passage changed in round 3 with its evidence:
  - the header status line;
  - the Summary scope and novelty paragraphs (lines 160–165, 220–223);
  - Section 4.6 (table rows marked †, the bullet on scaled bounds, the
    radius bullet, the Lasserre and Waki paragraphs, the closing paragraph);
  - Section 6 (what was read);
  - the Section 7 row for Section 4.6;
  - Section 8 (numerics);
  - Section 9 (the new script and its run times);
  - Sections 10.2 and 10.3.
- Every new number is labelled floating point. "Proved" is not used for any
  round-3 addition.
- The Summary novelty paragraph credits the third review for the
  scaled-bound gaps and the radius runs. It under-claims the
  opposite-orientation scaled-bound row, which is new in the note. That is
  harmless.
- Section 10.3 states that no proved statement and no existing value
  changed. That is accurate.
- The note's run times in Section 9 (13 s and 25 s) differ from my rerun
  (34 s and 19 s). The difference comes from machine load and is
  immaterial.

## 6. Commands run

All were run from `reviews/robust-lb-chains-confirm-r3-checks/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, on a shared machine with a load
average of about 24. Total wall time was about 2.5 minutes.

| Command | Log | What | Kind |
|---|---|---|---|
| `python3 e1_two_sides.py waki` | `e1_waki.log` | scaled bounds and `\|y_alpha\| <= 1` with univariate multipliers; scaled bounds with opposite orientation and orientation (b); opposite orientation without bounds; `n = 5, 8`; SOS and moment side | float (Clarabel; SCS on the scaled-bound rows) |
| `python3 e1_two_sides.py radius` | `e1_radius.log` | opposite orientation + ball, `M = 1.5, 2` at `n = 16, 32`, `M = 1.7` at `n = 8, 32`; both sides | float |
| `python3 e1_two_sides.py monotone` | `e1_monotone.log` | value against `M = 1.5..2.0` at `n = 8, 16` (moment side) | float |
| `python3 e2_bulk_radius.py bulk` | `e2_bulk.log` | per-bond (bulk) problem against `M`, bisection for the threshold `1.58348` | float; heuristic link to finite `n` |
| `python3 e2_bulk_radius.py long` | `e2_long.log` | `n = 64` (`M = 1.1, 1.3, 1.5`) and `n = 128` (`M = 1.5`) | float |
| `python3 revision3_chains.py waki` and `radius` (the note's script, from `chains/`, output to `/tmp`) | compared with `diff` | reproducibility of `logs/revision3_*.log` | identical output |

I also read `chains/logs/revision2_sos.log` and the round-3 review's logs
`d2_sdp.log` and `d5_radius_n.log`.

**Literature examined:** the local copy of Waki, Kim, Kojima and Muramatsu
(2006), `fulltext.md` and `original.pdf` (via `pdftotext -layout`),
Sections 4.2–4.3, 5.4–5.6 and the description of the experiments in
Section 6. I did not check the published SIAM version, whose section
numbering may differ from this preprint. No web search was made. This
round makes no novelty claim that needs a literature search.
