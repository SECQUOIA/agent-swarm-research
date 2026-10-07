# Confirmation of the third revision of "Consistency relaxations on tree decompositions"

Date: 2026-09-30. Note:
[`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
("the note"; third revision, 2227 lines; changes listed in its Section 12.3).
The six points checked here were raised by the previous confirmation,
[`recheck-consistency-confirm.md`](recheck-consistency-confirm.md). I did not
write the note or any earlier report.

**My checks.** My scripts and logs are in
[`consistency-confirm-r1-checks/`](consistency-confirm-r1-checks/). They share
no code with the note, apart from one scratch rerun of the note's new script
(`logs/scratch_rerun.log`). That rerun used a copy in `/tmp/confirm_r1/tc`,
outside the repository.

**Earlier text.** No copy of the second-revision note exists (the
continuation folder is untracked, and `/tmp` holds only the first revision,
in `/tmp/recheck/tc/`). So I read the whole current note. I also diffed it
against the first revision to confirm that every changed region belongs to
an edit listed in Section 12.2 or 12.3.

**Scope.** Targeted checks only: no project-wide verification and no CI. I
did not edit the note, its scripts or its logs, and I did not commit
anything.

## Verdict in brief

**All six points are fixed correctly. I found no mathematical error, and no
claim is stronger than what is proved or computed.** There was no "not
applied" list to judge.

- The one claim that became stronger, "the T1 gap is not attained at any
  finite `K`", is now backed by a proof in Section 3, Remarks. I checked the
  proof step by step, and it is correct.
- Every new number reproduces:
  - with my own code: the ratio classification, the middle-bag excesses
    and 1.03477;
  - with the note's script: a scratch rerun of `check_revision3.py`
    reproduces its log exactly.
- Two small points remain. Both are optional one-line fixes (Section 3):
  - in Proposition 5.8, the letter `C` names two different constants in
    (a) and (b);
  - three "at least" values are rounded up in the last digit.

| Point from the confirmation | Verdict |
|---|---|
| 1. "so it grows with `c`" (Section 5.4) | **fixed.** The clause is gone. The new sentence (grows at `n = 1` and `n >= 16`, falls at `n = 2, 3, 4`, not monotone at `n = 8`) is right. I reproduced it with my own LP and proved it for `n = 1, 2, 3` in closed form. |
| 2. Section 10, T1 at finite `K` | **fixed, by adding the proof.** The proof in Section 3, Remarks, is correct. The numbers for the split `-p` reproduce. All five places (header, Summary (B), Section 7.4, status table, Section 10) now say "proved". |
| 3. Alfonsi et al., `W_1` hypothesis | **fixed.** Checked against the text of arXiv 1905.05663v1: Proposition 5.7 and Corollary 5.8, the remark after the corollary, and Proposition 5.9 and Corollary 5.10. |
| 4. "Analytic up to the breakpoint/kink" | **fixed.** The phrase is gone. All four places now say that each piece extends analytically across the breakpoint (the kink, in the Summary). This matches the hypothesis of Proposition 5.8. |
| 5. Notation in Proposition 5.8(b) | **fixed.** The rate is now `beta_1`. The kink-cell definition and the counting are correct, and `C` and `C'` are right for (b). One new small clash: `C` in (a) is a different, unstated constant (remaining point 1). |
| 6. Status labels | **fixed.** No "not checked independently" label remains for Proposition 5.8(b) or the T1 limit. The header, the Section 9 preamble and the status table cite the confirmation. |

## 1. Each point, checked from scratch

### 1.1 Proposition 5.6 ratio against `c` (point 1)

**The text.** Section 5.4 now says: among the computed degrees, the ratio
`30 (3 + c) n gap` grows with `c` at `n = 1` and for `n >= 16`; it falls at
`n = 2, 3, 4` (35.0, 25.0, 18.3 at `n = 2`); and it is not monotone at
`n = 8` (40.0, 36.5, 39.2). "So it grows with `c`" no longer appears.

**Independent LP** (`r1_e6_ratio.py`). It uses a Legendre basis, its own
graded grid and its own re-evaluation on a 10 times finer grid. For
`c = 0.5, 2, 8` it gives:

| `n` | 1 | 2 | 3 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|---|
| ratios | 105.0, 150.0, 330.0 | 35.0, 25.0, 18.3 | 52.5, 37.5, 27.5 | 37.5, 30.1, 27.0 | 40.0, 36.5, 39.2 | 42.9, 43.5, 54.4 | 45.9, 50.6, 71.7 |
| in `c` | grows | falls | falls | falls | not monotone | grows | grows |

- **Robustness.** At every `n`, the brackets [lower estimate, upper
  estimate] for the three values of `c` are disjoint. So the order does not
  depend on the grid.
- **`n = 64, 128`.** I did not recompute these. The brackets from
  `logs/check_pinch_rates.log` are disjoint and increasing:
  - `n = 64`: [48.6, 48.8], [57.2, 58.3], [89.8, 96.6];
  - `n = 128`: [51.0, 52.7], [63.1, 71.3], [107.5, 175.9].

  So "grows" holds there despite the loose upper estimates.

**Closed forms for `n = 1, 2, 3`.** The band `U = -|s|`,
`L = -|s| - c s^2` is even, and the bracket is convex in `p`. So
symmetrizing `p` does not increase the bracket, and it suffices to take `p`
even.

- *`n = 1`.* For `p = alpha + gamma s`, the bracket is at least
  `1 + |gamma|` (take `s = ±1` in the first term and `s = 0` in the
  second), with equality at `gamma = 0`. So `gap(P_1) = 1`, and the ratio
  `30 (3 + c)` grows with `c`.
- *`n = 2, 3`.* For `p = alpha + gamma s^2` and `-(1 + c) <= gamma <= -1/2`,
  the bracket is `1/(4|gamma|)`. For `gamma > -1/2` it is at least
  `gamma + 1 > 1/2`,
  and for `gamma < -(1 + c)` it is `1/(4|gamma|) + |gamma| - 1 - c`, which
  increases with `|gamma|`. So
  `gap(P_2) = gap(P_3) = 1/(4(1 + c))`, and the ratios are
  `15 (3 + c)/(1 + c)` at `n = 2` and `22.5 (3 + c)/(1 + c)` at `n = 3`.
  Both fall with `c` for every `c >= 0`.
- The LP matches these closed forms to 5 digits.

**The note's script.** `check_revision3.py`, part (1), parses
`logs/check_revision2.log` correctly; its classification equals mine. The
ranges quoted just above the new sentence (18 to 72, 105 to 330, and 51.0,
63.1, 107.5) are unchanged and still right.

### 1.2 T1 at finite `K` (point 2)

**Where.** The proof is now in Section 3, Remarks ("Proof that the gap
stays strictly above `2 E_n` at every finite `K`"). It is credited to the
confirmation. I checked each step.

**The proof, step by step.**

- *Setup.*
  - T1 is a path `A - B - C` rooted at `C`. With `phi_e = -p_e` and
    `r_e = |s| - p_e`, the bags are `-r_1(s1)`,
    `r_1(s1) - r_2(s2) + K (s1 - s2)^2` and `r_2(s2)`.
  - So `rho = -max r_1 + m_B + min r_2`, and `f* = 0`.
  - Taking `s1 = s2` gives `m_B <= min (r_1 - r_2)`, hence `-rho >= X`.
- *Step 1.*
  - At a maximizer of `r_2`, `max (r_2 - r_1) >= max r_2 - max r_1`, so
    `X >= osc r_2`.
  - At a minimizer of `r_1`, `max (r_2 - r_1) >= min r_2 - min r_1`, so
    `X >= osc r_1`.
  - `osc(|s| - p_e) >= 2 E_n`. Equality holds iff `p_e + const` is a best
    approximant. The best uniform approximant from `P_n` on an interval is
    unique (Haar condition), so equality forces `p_e = p + const`.
- *Step 2.*
  - With `r_e = r - c_e`:
    `rho = -(max r - c_1) + m_B + (min r - c_2)`.
  - Hence `-rho = osc(r) + (c_2 - c_1) - m_B`, as stated.
- *Step 3.*
  - `r` is not constant, because `|s|` is not a polynomial. It is a
    polynomial on each side of 0 and continuous. So `r'(s0) != 0` at some
    interior point `s0 != 0`.
  - With `s2 = s0` and `s1 = s0 - delta sign(r'(s0))`, the middle bag
    equals `c_2 - c_1 - |r'(s0)| delta + O(delta^2) + K delta^2`. This is
    below `c_2 - c_1` for small `delta`.
  - This also holds at `K = 0`, where the gap is `4 E_n`, so "every
    `K >= 0`" is right.
- *Conclusion.*
  - Every split has `-rho > 2 E_n`.
  - Proposition 1.2 applies (box, finite-dimensional classes, point
    evaluations in `M_t`), so the supremum is attained, and
    `gap > 2 E_n`.
  - The argument works for every `n >= 0`.

**Numbers for the split `-p`** (`r1_t1_step3.py`: my own discrete Remez for
`sqrt(t)` on `[0, 1]`; dense search over `(s2, s1 - s2)`, then a bounded
local polish).

- *Remez values.* `2E_4 = 0.1352417986` and `2E_8 = 0.0693794562`;
  `Lip(r) = 1.401566` and `2.399963`. These equal the confirmation's
  values.
- *Middle-bag excess `-m_B` and ratio at `K = 100, 1000, 10^4`:*

  | `n` | `K = 100` | `K = 1000` | `K = 10^4` |
  |---|---|---|---|
  | 4 | 4.7024e-3 | 4.8892e-4 | 4.9088e-5 |
  | 8 | 1.1421e-2 | 1.4021e-3 | 1.4361e-4 |

  - All six values are below `Lip(r)^2/(4K)` and approach it as `K`
    grows.
  - For `n = 4`, `K = 100`, `gap(-p)/2E_4 = 1.03477`, the confirmation's
    value for that split.
  - These agree with `logs/check_revision3.log` to the digits shown there.
    That log's search is a valid lower bound: it takes `s1 = s2 + delta`
    over a grid, so it only under-estimates `-m_B`. (The "at least"
    wording has a rounding nit; see remaining point 2.)
- *Random splits.* A test of `-rho >= X >= max(osc r_1, osc r_2)` on 200
  random polynomial splits (`K = 100`, 801-point grid) found no violation
  beyond `3e-17`.
- *Scratch rerun.* `check_revision3.py` (10 s) reproduces
  `logs/check_revision3.log` byte for byte.

**Consistency of the labels.** All five places now state strictness at
finite `K` as proved:

- the header;
- Summary (B): "At every finite `K` the T1 gap stays strictly above
  `2 E_n` (also proved in Section 3)";
- Section 7.4;
- the status table;
- Section 10: "approached as `K -> inf` but not attained at any finite `K`
  (proved in Section 3)".

The older "Values" bullet ("between about 1.013 and 1.036") is weaker than
the confirmation's 1.0148 cited just below it, but not wrong.

### 1.3 Alfonsi et al. (point 3)

I reread `/tmp/recheck/acel.txt` (arXiv 1905.05663v1):

- **Proposition 5.7 and Corollary 5.8** (`W_1`) assume:
  - `mu` and `nu` absolutely continuous;
  - `F_mu - F_nu` changes sign at most `Q` times (conditions
    (5.2.11)–(5.2.12));
  - `rho_mu - rho_nu in L^inf([0, 1])`.
- **After Corollary 5.8**, the authors remark: "it even is sufficient to
  assume that `rho_mu - rho_nu` is bounded on a neighborhood of the points
  at which `F_mu - F_nu` changes sign".
- **Proposition 5.9 and Corollary 5.10** (`W_2^2`) assume
  `rho_mu, rho_nu in L^inf([0, 1], R_+)`.

Section 8 now states exactly this. The reading note records the third
reread. The earlier correction stands: the rates do not come from
approximating Kantorovich potentials.

### 1.4 "Each piece extends analytically across the breakpoint" (point 4)

- **Old phrase gone.** `grep` finds no "analytic up to" in the note.
- **New phrase present.** "Extends analytically across" appears in the
  Summary (D) (as "the kink"), Section 8 (hp-FEM entry), the status table
  and Section 10.
- **Match with the hypothesis.** The hypothesis of Proposition 5.8 is
  continuation to a Bernstein ellipse, bounded by `M` there. For one
  closed piece this is equivalent to analyticity in a neighbourhood of the
  closed piece, by compactness. The phrase therefore matches, and it
  excludes `(s - c0)^{4/3}`.

### 1.5 Proposition 5.8(b) (point 5)

- **Letter clash.** The rate is now `beta_1 = sqrt(log 2 · log rho)`
  throughout (proposition, proof, text after it, Summary, status table,
  Section 10). `b` is left only as the endpoint of `X_S = [a, b]`. The
  unproved geometric-mesh rate is written `exp(-b' sqrt(N))`.
- **Kink-cell rule.** The kink cell is the cell that contains `c`; once
  `c` is a common endpoint of two cells, it is the left one. With this
  rule, after `m` bisections:
  - there are `m + 1` cells;
  - the kink cell has width `(b - a) 2^{-m}`;
  - every other cell lies in one closed piece, so the inclusion
    `E_rho(D) ⊂ E_rho(I)` bounds it.

  `r1_prop58b_count.py` confirms this in exact rational arithmetic for
  five positions of `c` and `m <= 24` (120 cases), including `c` at a
  dyadic point (`c = 0`, `c = 1/2`), where `c` becomes a cell boundary.
  The parenthetical in (b), that from then on the inclusion argument
  covers every other cell and the oscillation bound covers the kink cell,
  is correct.
- **Counting.**
  - `p = ceil(beta_0 m)` gives `rho^{-p} <= 2^{-m}` and
    `p + 1 < beta_0 m + 2`.
  - Hence `N <= beta_0 m^2 + 2m + 2`, and the quadratic gives
    `m >= sqrt((N - 2)/beta_0) - 1/beta_0`.
  - Then
    `2^{-m} <= rho exp(-beta_1 sqrt(N - 2)) <= rho e^{beta_1 sqrt 2} exp(-beta_1 sqrt N)`.
  - So `C = max(4M/(rho - 1), G (b - a))` and `C' = C rho e^{beta_1 sqrt 2}`
    are right, and `C'` equals the confirmation's.
  - `r1_prop58b_count.py` checks each inequality for nine values of `rho`
    in `[1.01, 1e6]` and `m = 0..199` (1800 cases, no failure).
- **New small clash.** See remaining point 1.

### 1.6 Status labels (point 6)

- **Header.** It says the confirmation checked both second-revision
  arguments and found them correct.
- **Section 9 preamble.** It says the same, and adds that the finite-`K`
  proof was proposed and checked in the confirmation and checked again by
  the author.
- **Status table.** Proposition 5.8(b): "added in the second revision,
  checked in the confirmation". Theorem 3.1: "limit proved in the second
  revision and checked in the confirmation; strictness proved in the
  confirmation, checked again here and added in the third revision".
- **Section 12.2.** Its introduction and item 1 now point to Section 12.3.
- **No stale label.** `grep` finds no remaining "not checked
  independently" label on either argument. The only occurrence is the
  historical sentence in Section 12.2, which is accurate.

## 2. Was anything strengthened? Are Sections 11 and 12.3 accurate?

- **Strengthened claims.** Only one: T1 strictness at finite `K`, from
  "numerical" to "proved". The proof is correct (Section 1.2). Every other
  change is a correction, a narrowing or a relabelling:
  - the ratio sentence;
  - the Alfonsi hypothesis;
  - the analyticity phrase;
  - the notation;
  - the status labels, which now cite a check that did happen.
- **Scope of the changes.** Diffing the current note against the
  first-revision copy shows changes only in regions covered by Sections
  12.2 and 12.3.
- **Section 12.3.** It describes the changes accurately. Its numbers
  (35.0, 25.0, 18.3; 40.0, 36.5, 39.2; 4.70e-3 ... 1.44e-4; 1.03477)
  match the logs and my recomputation. There is one rounding nit
  (remaining point 2).
- **Section 11.** It lists the new command and log. The run time (9 s) is
  consistent with my 10 s rerun.
- **Logs.** Only `logs/check_revision3.log` is new. Its timestamp (10:57)
  is the only one after the second revision's logs (08:27, 08:34).

## 3. Remaining points (minor, optional)

1. **Proposition 5.8: `C` in (a) is not the `C` of (b).**
   - *Where.* Proposition 5.8(a) writes
     `gap <= C exp(-(log rho / J) N)` without defining `C`. Item (b) then
     defines `C = max(4 M/(rho - 1), G (b - a))`.
   - *The problem.* From `N = J (p + 1)`, the constant in (a) is
     `4 M rho/(rho - 1)`. Reading (b)'s `C` into (a) would give a bound
     too small by up to a factor `rho`. Section 12.3, item 5, says the
     aligned rate was "made explicit"; the rate is, but the constant is
     not.
   - *Fix.* In (a), write
     `gap <= (4 M rho/(rho - 1)) exp(-(log rho / J) N)`, or call the
     constant `C_a`.
2. **Three "at least" values are rounded up in the last digit.**
   - *Where.* Section 3, Remarks ("Numbers"), and Section 12.3, item 2.
   - *The values.* The computed lower bounds are:
     - 4.889e-4 and 4.909e-5 (`n = 4`; quoted as "at least 4.89e-4" and
       "4.91e-5");
     - 1.436e-4 (`n = 8`; quoted as 1.44e-4, in Section 12.3 only).

     My polished values (4.8892e-4, 4.9088e-5, 1.4361e-4) confirm that
     the true values lie just below the quoted numbers. Likewise,
     "`gap/2E_4 >= 1.0148`" quotes the confirmation's 1.01477.
   - *Effect.* None on any conclusion.
   - *Fix.* Truncate the values (4.88e-4, 4.90e-5, 1.43e-4, 1.0147), or
     say "about".

## 4. Commands run (targeted checks only)

In `reviews/consistency-confirm-r1-checks/`, with `OMP_NUM_THREADS=1`:

```
python3 r1_e6_ratio.py        # logs/r1_e6_ratio.log; own LP for E6(c), n = 1..32, closed forms n = 1, 2, 3; 9 s
python3 r1_t1_step3.py        # logs/r1_t1_step3.log; own Remez, -m_B for the split -p at K = 100, 1e3, 1e4; random-split test; 4 s
python3 r1_prop58b_count.py   # logs/r1_prop58b_count.log; counting inequalities and kink-cell bisection (exact rationals); <1 s
```

In a scratch copy `/tmp/confirm_r1/tc` of the needed files, outside the
repository (result in `logs/scratch_rerun.log`):

```
python3 check_revision3.py    # 10 s; log identical to theory-consistency/logs/check_revision3.log
diff /tmp/recheck/tc/consistency-relaxations.md theory-consistency/consistency-relaxations.md   # changed regions only
```

Source reread: arXiv 1905.05663v1, Propositions 5.7 and 5.9, Corollaries 5.8
and 5.10, and the remark after Corollary 5.8 (text in
`/tmp/recheck/acel.txt`).

Environment: Python 3.13.11, numpy 2.5.1, scipy 1.18.0 (HiGHS). These are
targeted checks only. I did not run project-wide verification, inspect CI,
edit the note or its files, or commit anything.
