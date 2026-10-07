# Referee check of the second revision of "Split-robust lower bounds on uniform chains"

Date: 2026-09-30. Note checked:
`research-20260929/theory-robust-lb/robust-chains.md`, revised after review
round 2 (1819 lines; changes listed in its Section 10.2). The review that
asked for the changes is `reviews/robust-lb-chains-confirm-r1.md`. I wrote
neither the note, its scripts, nor that review. My scripts and logs are in
`reviews/robust-lb-chains-confirm-r2-checks/`. They share no code with the
note's `chains/` scripts or with the earlier reviews' checks.

Following `AGENTS.md`, I ran only targeted checks: no project-wide
verification, no CI. I did not commit anything or edit the note.

Labels used below:

- **proved**: checked by hand, step by step;
- **exact**: checked in exact arithmetic (Python fractions or sympy on
  rationals; exact rational interval arithmetic);
- **float**: recomputed in floating point (cvxpy with Clarabel, and SCS
  where stated), not certified.

## Verdict in brief

Both review items were applied correctly. Every new or changed number was
recomputed with my own code and agrees with the note. The new proofs are
correct:

- Lemma A.4, with its exact finite facts;
- the restated Proposition C.5, cases (a)–(d);
- the unboundedness proof for univariate multipliers.

No item was refused. Nothing was strengthened beyond its evidence, apart
from the small points below.

Three minor problems remain. All three are fixes to wording or citations.
No proof or number is wrong.

1. **One sentence in Section 4.6 overgeneralizes** (line 1286). It says
   that the placements not covered by Proposition C.5 "have a root gap or
   are unbounded". Three rows of the note's own table show no gap.
2. **The Waki et al. citations need correcting** (lines 1263–1272,
   1458–1461, 1756).
   - The section numbers are off by one against the local copy.
   - The "`|y_alpha| <= 1` is the analogue" remark does not describe what
     Waki et al. do. They first scale the variables to `[0, 1]` and then add
     `0 <= y_alpha <= 1`. Applied to the chiral chain, their bounds give a
     much larger gap: 0.699 at `n = 5` and 1.332 at `n = 8` (float).
3. **Credit nit** (line 1772). Section 10.2 lists case (b) as "New here",
   but the round-2 review had already stated it.

| Review item | Verdict |
|---|---|
| 1. Moment-SOS scope statements dropped the condition of Proposition C.5 | **fixed.** Placements recomputed with independent code; the gaps certified exactly; the unbounded direction checked exactly; the C.5 identities rechecked. Remaining problems 1–3 are minor. |
| 2. WALL statements about all `n` rested on `n <= 16` | **fixed.** Lemma A.4 proved and its finite facts rechecked exactly by a different method; the hypothesis of Proposition A.3 is correctly removed; all three statements now hold for every `n`. |

## 1. Item 2 (WALL), checked from scratch

**Where the changes are.** Lemma A.4 is new in Section 2.5. The other
changes:

- the hypothesis of Proposition A.3 is removed (line 639);
- the Summary (lines 70–81) and "For solvers" (lines 187–190) cite
  Lemma A.4;
- Section 2.3 (lines 415–421) and the Section 2.2 remark (lines 397–399)
  give the `n/2` bound for every even `n >= 4`;
- Section 7 has new or updated rows, and the Section 8 open item is removed.

All of these are consistent with each other.

**Proof of Lemma A.4 (proved).**

- *Item 1.* The coefficients of `u' - 1` are those of `u` (`u' = 1.022 +
  0.378 t + 5.322 t^2 + 4.344 t^3`). The endpoint values are
  `u'(-1) - 2b = -151/500` and `u'(1) - 2b = 4571/500`. A single root of
  `u' - 2b` with these signs makes `c` the unique minimizer of
  `u(t) - 2bt`.
- *Item 2, `phi`.* `∂_y(2 phi) = u'(y) + 2bx > 1 + 2bx >= 0` for
  `x >= -1/(2b)`. The inequality is strict, so `2 phi(x, y) >= 2 phi(x, -1)`
  with equality only at `y = -1`. Then `2 phi(x, -1) = u(x) - 2bx + u(-1)`
  has its minimum only at `x = c`, and `c > -1/(2b)`.
  - The leftover square `[-1, -1/(2b))^2` lies inside `[-1, -1/2]^2`,
    because `-1/(2b) = -0.5198`.
  - The Lipschitz bound is `sum_i i|u_i| + 2b = 11.066 + 1.924 <= 13`.
  - A grid of step `h` puts every point within `h/2` of a grid point in
    each coordinate. So the grid error is at most `13 (h/2 + h/2) = 13 h`,
    as used.
- *Item 2, `H`.* The same argument works, with
  `∂_y H = u'(y) + b(x - 1)`, the threshold `1 - 1/b = -19/481`, and
  `H(x, -1) = u(x) - 2bx + u(-1) + b`. The bound `|∂_x H| <= 13` on
  `[-1, 0]^2` holds because `|y - 1| <= 2`. Finally,
  `H(-1, c) = 2m + b`.
- *Item 3.* This follows from Proposition A.1(1), `min u = u(-1)` and
  item 2. For odd `n` both ends of the alternating configuration are `-1`.
- *Item 4.* I derived the factors by hand from
  `f_e^r = f_e + r_{e+1}(x_{e+1}) - r_e(x_e)`, for even, odd, first and last
  bonds. Each interior variable lies in exactly one even bond and in one odd
  or end bond.
  - The bond counts are `n/2 - 1` even and `n/2 - 2` odd interior.
  - The sum of the minima is
    `2u(-1) - b(n/2 - 2) + (n/2 - 1)(2m + b) = (n-2)m + 2u(-1) + b`. This
    equals the wall value, since `phi(-1, -1) = u(-1) + b`.
  - The end-bond minimum uses `x_1 + 1 >= 0` and `u' > b`.
  - The shifts lie in `span{t, u}`, so the split is of class (a0); they are
    quartic, so it is also in `b_4`.

**Recomputation, by a different method from the note**
(`d1_wall_exact.py`, `d1_wall_exact.log`):

- *Root counts (exact).* My own Sturm sequences over fractions give 0, 0
  and 1 roots in `(-1, 1]` for `u' - 1`, `u' - b` and `u' - 2b`. The note
  used sympy root counting.
  - `min u' = 1.0150796` at `t = -0.03721`. This is a root of `u''`, a
    quadratic, so the value is in closed form.
  - Exact bisection gives `c = 0.33772319890448543...`.
- *Leftover squares (exact).* I used exact rational interval arithmetic
  (the natural interval extension on `48 x 48` boxes, with no rounding),
  not a grid with a Lipschitz bound:
  - `H >= -0.6557` on `[-1, 1 - 1/b]^2`, which is 0.104 above
    `H(-1, c) = -0.7596`;
  - `2 phi >= -1.2547` on `[-1, -1/(2b)]^2`, which is 0.467 above
    `2m = -1.7216`.

  These are cruder than the note's bounds (`-0.6240` from the grid,
  `-0.6231` by interval arithmetic) but independent, and both margins are
  positive. With `16 x 16` boxes the bound for `H` was too weak; that run is
  kept in the log.
- *Split (exact).* I rebuilt the split for even `n = 4..24`, this time as
  shifts relative to the *unsplit* base split. The shifts come out as
  `r_i = b t` (even `i`) and `u(t) - b t` (odd `i`), with `r_1 = r_n = 0`.
  These lie in `span{t, u}`. The sum of the minima equals the wall value
  with `n` symbolic.
- *Wall values (exact to 50 digits).* `f_n(x^(j))` equals the sum of the
  factor minima for every `j` and every even `n = 4..12`, to within
  `2e-50` (mpmath).
- The note's own logs (`revision2_wall.log`,
  `revision2_independent_wall.log`) contain every number quoted in Lemma A.4
  and its "Checks" paragraph.

**Consequences.** Proposition A.3 now holds for every even `n >= 4`. Its
proof used the global optimality of the walls only through `f*`, and that is
now proved. Classes (a) and (a0) are exact at the root for every `n`. The
authors also found and closed a gap in the first version: the odd-`n`
statement relied on `min phi = phi(-1, c)`, which had been checked only on a
grid. The earlier review missed this.

## 2. Item 1 (moment-SOS scope), checked from scratch

### 2.1 Proposition C.5 (proved; identities exact)

`d3_exact.py ids` (`d3_exact_ids_dir.log`; sympy, with symbolic `b, g, ev,
M`) gives residual 0 for each of the following:

- the bracket decomposition used in (a) and (b), and both end terms;
- `1 ± y = [(1 ± y)^2 + (1 - y^2)]/2` for (c), and the end terms with
  `1 - t^2` (multiplier `t^2`);
- the ball identity of (d) with general `M`.

The first bracket of (d) is a quadratic form with eigenvalues `ev/2` and
`b - g(M^2 + 1) + ev/2`. So the condition is right, and at
`(0.6, 0.3, 0.05)` it gives `M <= sqrt(39)/6 = 1.04083`.

All degrees are at most 4. The multipliers in (a) and (b) are localized
where the proof says. In particular, case (b) matches the orientation
"`1 - x_i` in `(i, i+1)`, `1 + x_i` in `(i-1, i)`". Case (d) also works with
univariate multipliers at the ends: my run "univariate multipliers + ball
`M = 1`" gives about `1e-9` (float) at `n = 5` and `n = 8`.

### 2.2 The placement table (float, independent code)

`d2_sdp.py` is my own moment-side code (`d2_sdp.log`). It keeps one global
moment dictionary, so the univariate moments are shared by construction, not
through equality constraints. It reproduces every row of the table in
Section 4.6:

| placement | note `n = 5` / `n = 8` | mine `n = 5` / `n = 8` |
|---|---|---|
| (a) every clique | `1.9e-8` / `1.8e-8` | `3.1e-9` / `1.5e-9` |
| (b) one clique, certificate orientation | `7.6e-9` / `1.0e-7` | `1.1e-9` / `1.6e-9` |
| one clique, opposite orientation | `-0.0553` / `-0.2072` | `-0.0553055` / `-0.2071799` (SCS: `-0.05524`, `-0.20702`, "optimal_inaccurate") |
| opposite + ball `M = 1`, `1.01`, `1.1` | about `1e-7` | about `1e-8` or less |
| opposite + ball `M = 2` | `1.9e-7` / `-0.0158` | `8.6e-10` / `-0.0158185` (SCS agrees) |
| opposite + ball `M = 10` | `-0.0427` / `-0.1782` | `-0.0426889` / `-0.1782067` |
| univariate multipliers, linear | unbounded | Clarabel `-1.2e7` / `-2.1e7`, SCS `-3.9e3` / `-9.4e3` |
| same + `\|y_alpha\| <= 1` | `-0.0628` / `-0.1263` | `-0.0627682` / `-0.1262654` (SCS agrees) |
| `1 - x_i^2`: every clique, one clique (either side), univariate (with or without bounds) | no gap | `<= 5e-9` everywhere |

### 2.3 The gaps can be certified (exact)

`d3_exact.py gap` (`d3_exact_gap.log`) certifies the gaps as follows:

1. Take the Clarabel moment vector.
2. Mix in the moments of the uniform product measure on `[-1, 1]^n`, with
   weight `1e-4`.
3. Round to rationals with denominators at most `1e12`.
4. Check every moment, localizing and ball matrix by exact `LDL^T`
   (fractions), and the bounds `|y_alpha| <= 1` exactly.

Each point is exactly feasible. Its exact objective is therefore an upper
bound on the relaxation value, which proves the following root gaps:

- opposite orientation: at least 0.05519 (`n = 5`) and 0.20698 (`n = 8`);
- ball `M = 2`: at least 0.01564 (`n = 8`);
- ball `M = 10`: at least 0.04257 (`n = 5`);
- univariate multipliers with `|y_alpha| <= 1`: at least 0.06265 (`n = 5`).

The note labels these gaps "floating point", which is correct. With this
check they could be labelled proved lower bounds (optional).

### 2.4 Unboundedness with univariate multipliers (proved; exact)

`d3_exact.py dir` (`d3_exact_ids_dir.log`) checks the direction in three
ways:

- *Symbolic `LDL^T`.* I factored the `6 x 6` clique moment matrix in the
  natural basis `(1, x, y, x^2, xy, y^2)`. This is a different route from
  the note's leading minors of two blocks. The pivots are `1, 1/2, 1/2,
  (32 s^2 + 15)/4, 2(s^2 + 1), 2(64 s^4 + 77 s^2 + 22)/(32 s^2 + 15)`, all
  positive for every real `s`. The determinant is
  `(s^2 + 1)(64 s^4 + 77 s^2 + 22)/4`.
- *Block structure (proved).* The blocks the note names are `{1, x, x^2,
  y^2}` and `{y, xy}`. Every entry between them is a moment the direction
  sets to 0. The note's minors, `(32 s^2 + 15)/8`, `(64 s^4 + 77 s^2 +
  22)/4` and `s^2 + 1`, are consistent with this.
- *Global check (exact).* For `n = 5` and `s = 1, 10, 1000`, all
  clique moment matrices and all univariate localizing matrices are PSD in
  exact arithmetic. The univariate moments agree across cliques, and the
  objective is `a n/2 - (g/2)(n - 1) s`, which gives `-4787/8` at
  `s = 1000`.

The dual remark is also correct. The degree-4 parts of the clique SOS terms
are nonnegative forms that sum to 0, so each vanishes. Then no term can
produce `x_i x_{i+1}^2`.

### 2.5 The literature statements (local full texts)

I read the local copies:
`literature/papers/lasserre2006-convergent-sdprelaxations-in-polynomial-optimization/fulltext.md`
and `literature/papers/waki2006-sums-of-squares-and-semidefinite/fulltext.md`,
cross-checked against `original.pdf` with `pdftotext`.

- **Lasserre.** These statements are correct:
  - Assumption 3.1 (`|x|_inf < M` on `K`);
  - the ball constraints (3.1), `n_k M^2 - |X(I_k)|^2 >= 0`;
  - Assumption 3.2 ("The index set `J` ... is partitioned into `p`
    disjoint sets `J_k`").

  So in Lasserre's form `M > 1` is required for `[-1, 1]`. The note's "exact
  for `M <= 1.0408` (proved)" therefore means `1 < M <= 1.0408` there, which
  is fine. The claim "exact for every `M`" in orientation (b) follows from
  case (b): adding constraints cannot lower the bound. My run with
  orientation (b) and ball `M = 10` gives `3.7e-9` and `1.6e-9`.
- **Waki et al.**
  - Section 4.2 restricts the multiplier of `f_k` to the variables in
    `F_k`, and (20) is the sparse SOS relaxation of Section 4.3. Correct.
  - The union-of-cliques variant contains the certificate of case (a). This
    is correct, as the note says (proved, not computed).
  - The experiments of Section 6 use the union support. Correct.
  - The section numbers and the "analogue" remark need fixing; see
    remaining problem 2.

## 3. Remaining problems

### 3.1 Section 4.6 closing paragraph overgeneralizes (minor)

Line 1286 reads: "those that localize the box constraints as in Proposition
C.5 are exact at the root, and those with the other placements above have a
root gap or are unbounded". Three rows of the table above it are not
covered by Proposition C.5 and show no gap (float):

- opposite orientation with ball `M = 1.1`;
- `1 - x_i^2` in one clique;
- `1 - x_i^2` with univariate multipliers.

My runs add opposite orientation with `M = 1.3` and `1.5`: no gap up to
`n = 32` (`d5_radius_n.log`).

The other scope statements are worded correctly ("can fail", "can have a
root gap or be unbounded").

**Fix:** "some of the other placements above have a root gap or are
unbounded".

### 3.2 Waki et al.: section numbers and the "analogue" of their bounds (minor)

**Section numbers.**

- In the local copy (both `fulltext.md` and `original.pdf`):
  - Section 5.4 is "Supports for Lagrange multiplier polynomials" (one
    clique, or a union of cliques);
  - Section 5.5 is "Polynomial valid inequalities and their linearization"
    (`0 <= y_alpha <= rho^alpha`);
  - Section 5.6 is "Scaling".
- The note cites these as 5.5 and 5.6 at three places: lines 1263–1266,
  lines 1458–1461 and line 1756. The paper's own Section 6 cross-references
  them that way ("as mentioned in Section 5.5", "given in Section 5.6"), so
  the source itself is inconsistent. The round-2 review used the same
  numbers.
- The note says it read these sections in the local copy, so it should use
  the headings, or say that the paper's cross-references differ.

**The "analogue".** Lines 1264–1266 say that `|y_alpha| <= 1` is the
analogue for `[-1, 1]` of Waki et al.'s `0 <= y_alpha <= rho^alpha`. That
is not how Waki et al. handle a general box.

- Their Section 5.6 (Scaling) maps `x_i in [eta_i, rho_i]` to
  `z_i = (x_i - eta_i)/(rho_i - eta_i) in [0, 1]`.
- Their Section 6 says they added bounds "so that the scaling technique and
  the valid inequalities of the form `0 <= y_alpha <= 1` ... can work
  effectively".
- For the chiral chain this means `0 <= L(((1 + x)/2)^alpha) <= 1` on every
  clique monomial of degree at most 4. These are different linear
  constraints from `|y_alpha| <= 1`.

With univariate multipliers and these bounds, my moment relaxation gives
`-0.6988746` at `n = 5` and `-1.331693` at `n = 8` (float; Clarabel and SCS
agree; `d2_sdp.log`, rows with `"zbound": true`). This is a much larger gap
than `0.0628` and `0.1263`. So the note's conclusion holds and is stronger
for Waki et al.'s own bounds, but "the analogue" describes a different
relaxation.

**Fix:** correct the section numbers. Then either drop "is the analogue" or
add a short statement such as: "Waki et al. first scale the variables to
`[0, 1]`; with their bounds `0 <= y_alpha <= 1` on the scaled moments the
gap is 0.699 (`n = 5`) and 1.332 (`n = 8`), floating point (referee
check)."

### 3.3 Credit for case (b) (nit)

Section 10.2, item 1, lists under "New here": "(iv) one clique per
constraint in the orientation of the certificate is exact (case (b),
proved)" (line 1772). The round-2 review (`robust-lb-chains-confirm-r1.md`,
Section 2.1) had already stated: "*Proved* ... for the one-clique assignment
in the right orientation (the same certificate)". The novelty paragraph of
the Summary does not claim it, so only Section 10.2 needs the change.

**Fix:** credit the review for (iv), or drop it from "New here".

## 4. Optional additions (not problems)

These go beyond the review's requests. They are offered only because they
strengthen statements already in the note.

- **A more common placement also has a gap** (`d4_more_placements.log`,
  float). Put both linear bounds of `x_i` in the same clique, all in
  `(i, i+1)` or all in `(i-1, i)`. This is the simplest way to assign each
  constraint to one clique.
  - Without a ball, the gaps are 0.0878 (`n = 5`) and 0.2653 (`n = 8`),
    larger than for the opposite orientation.
  - With the ball `M = 1.5` the relaxation is exact; with `M = 2` the gap is
    0.0042 at `n = 8`.

  This supports the "For solvers" warning better than the opposite
  orientation, which looks contrived.
- **Growth with `n` for the ball** (`d5_radius_n.log`, float). With
  `M = 2` the gap is 0.072, 0.133, 0.255 and 0.378 at `n = 12, 16, 24, 32`,
  about 0.015 per variable. So the gap grows linearly; Section 8 says this
  growth was not studied. With `M = 1.1, 1.3, 1.5` there is no gap up to
  `n = 32`, which supports "sufficient, not necessary" (line 1244) beyond
  `n = 8`.
- **Univariate multipliers with the ball** (float). With `M = 1` the
  relaxation is exact, consistent with C.5(d), which allows univariate
  multipliers at the ends. With `M = 2` the gaps are 0.0080 (`n = 5`) and
  0.1617 (`n = 8`).
- The exact gap certificates of Section 2.3 above.

## 5. Refusals, and was anything strengthened?

- Nothing was refused.
- I compared every revised passage with its evidence:
  - The Summary scope bullet (lines 148–165), "For solvers" (lines
    195–205), Section 6 (lines 1447–1475), Section 7 (rows C.5 and 4.6) and
    Section 8 (lines 1558–1564, 1571–1577) now state the localization
    condition or the ball alternative, and label the gaps as floating point.
  - The Summary bullet says that `M = 2` "leaves a gap" without saying that
    at `n = 5` it does not. The table and the Lasserre paragraph give the
    precise statement, and my larger-`n` runs confirm the gap. This is
    acceptable.
  - "Proved" is used only for the C.5 cases, the unboundedness and
    Lemma A.4. Each was checked above.
  - The header's account of what is exact, interval-checked or floating
    point (lines 5–19) is accurate.
  - The authors recorded the failed first unbounded direction and the
    floating-point basis of the first version's odd-`n` claim. Both are
    useful negative results.
- The only overstatement is the sentence in Section 3.1 above. The credit
  item in Section 3.3 is a small over-attribution in the revision log.

## 6. Commands run

All were run from `reviews/robust-lb-chains-confirm-r2-checks/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, on a shared machine with a load
average of about 18–24. Each run took seconds to a few minutes, about
15 minutes of wall time in total.

| Command | Log | What | Kind |
|---|---|---|---|
| `python3 d1_wall_exact.py` | `d1_wall_exact.log` | Lemma A.4: Sturm counts, `min u'`, `c`, symbolic monotonicity steps, exact rational interval bounds on the leftover squares, split relative to the unsplit base (`n = 4..24`), sum of minima, 50-digit wall values | exact (wall values: mpmath) |
| `python3 d2_sdp.py 5 8` | `d2_sdp.log` | own moment relaxation, 21 placements per `n`, including Waki-style scaled bounds | float (Clarabel; SCS on some rows) |
| `python3 d3_exact.py ids` and `dir` | `d3_exact_ids_dir.log` | C.5 identities; the unbounded direction (symbolic `LDL^T`, exact feasibility for `n = 5`) | exact |
| `python3 d3_exact.py gap` | `d3_exact_gap.log` | exact rational feasible moment points proving the gaps | exact (solver output used only as a starting point) |
| `python3 d4_more_placements.py 5 8` | `d4_more_placements.log` | both bounds of a variable in one clique; extra radii | float |
| `python3 d5_radius_n.py` | `d5_radius_n.log` | opposite orientation with ball `M = 1.1, 1.3, 1.5, 2` at `n = 12, 16, 24, 32` | float |

I also read the note's logs `chains/logs/revision2_wall.log`,
`revision2_sos.log`, `revision2_independent_wall.log` and
`revision2_independent_sos.log`, and the scripts `revision2_chains.py` and
`revision2_independent.py`. The note's text matches these logs.

**Literature examined:** the local full texts of Lasserre (2006) and Waki,
Kim, Kojima and Muramatsu (2006), listed in Section 2.5; for Waki et al.
also `original.pdf` (the optimization-online preprint) through `pdftotext`.
I did not check the published SIAM version, whose section numbering may
differ from the preprint's. No web search was made. Whether software such
as TSSOS or SparsePOP localizes bound constraints in every clique was not
checked.
