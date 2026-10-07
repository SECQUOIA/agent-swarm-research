# Confirmation recheck of the second revision of "Split-robust lower bounds for single-tree spatial branch-and-bound on paths"

Date: 2026-09-30. Note: `research-20260929/theory-robust-lb/robust-lower-bound.md`
(second revision, 1428 lines; changes listed in its Section 10.2). Earlier
reports: `reviews/robust-lb-review.md` (review) and
`reviews/robust-lb-recheck.md` (recheck, items R1–R7). I did not write the
note or either earlier report. My script and log are in
`reviews/recheck-robust-lb-confirm-checks/`. They share no code with the
authors, the review or the recheck.

Following `AGENTS.md`, I ran only targeted checks: no project-wide
verification and no CI. I did not commit anything or edit the note.

- **No usable earlier copy.** The only earlier copy I found
  (`/tmp/robust-lower-bound.v1.md`) is the pre-review first version.
- **What I compared against.** There is no copy of the text as it stood just
  before the second revision. So I judged each revised passage against the
  recheck's quotations of the old wording and against the evidence.

## Verdict in brief

Every requested fix is applied, and applied correctly. I found no
mathematical error. All recomputed numbers agree with the note. The withdrawn
claims are clearly marked. The new material adds nothing the evidence does not
support, with one exception: a new numerical range for `E_d d^2` is wrong for
odd `d`. That item and three smaller wording points remain (Section 3).

| Item | Verdict |
|---|---|
| R1 Falk (1969) citation | **fixed.** Crossref confirms the reference. The text says "content not checked". Revision 1's "was not located" is withdrawn and marked in Section 10.1. |
| R6 provable base versus tree growth; uniform cap | **fixed.** The uniform cap `mu < 4 ln 64` is proved correctly. The `1 + O(1/d^2)` statements are now limited to the base that Theorem 4.2 can prove. |
| R5 scope of the independent reproduction | **fixed**, slightly narrower than asked. It matches the review's and the recheck's logs. |
| R2 ceiling at the reference parameters | **fixed.** I recomputed `mu0` for all 20 parameter sets in `scan_bd.log`. The stated range 1.022–1.073 is right for the class-(a) sets it refers to. |
| R7 consistency checks limited to class (a), `G <= 2` | **fixed.** The word "independently" was added (remaining problem 2). |
| R3 Lemma 1.3 with `r` varying per point | **fixed; proof correct.** |
| R4 lifted relaxations "bounded below" | **fixed.** |
| Optional: `gamma_10 = 0` exact | **confirmed** by a different exact method (Bernstein coefficients). |
| Optional: `y1 = 0.3` cap | **confirmed:** `mu0 = 2.3782`, 1.0211 and 1.0198 per variable. |
| Optional: smaller wording | **applied.** One new sentence is wrong for odd `d` (remaining problem 1). |

## 1. Each fix, checked from scratch

### R1. Falk (1969)

- **Falk (1969).** A Crossref query for `10.1137/0307039` returns James E.
  Falk, "Lagrange Multipliers and Nonconvex Programs", *SIAM Journal on
  Control* 7(4), 534–545, November 1969. This matches Section 1.5.
- **Falk (1974).** A Crossref query for `10.1287/opre.22.2.410` returns
  "Technical Note—Sharper Bounds on Nonconvex Programs", *Oper. Res.* 22(2),
  410–413. Its abstract says the bounds "are the same if the original problem
  has only linear constraints, or if the problem is separable with certain
  properties". Section 1.5 uses it in exactly this way, and Section 10.2
  item 1 quotes it verbatim.
- **Section 1.5** now says that the content of the 1969 paper "was not
  checked, so it is not used as a source here". This is the wording the
  recheck asked for.
- **Section 10.1 item 2** keeps the history and adds: "This revision said it
  'was not located'; that was wrong, and Section 10.2, item 1, corrects it."
  The withdrawn claim is clearly marked.
- `grep` finds "was not located" only inside these two correction notes.

### R6. The `1 + O(1/d^2)` claim and the uniform cap

**The proof (Theorem 4.3(3), first bullet) is correct.** I checked each step.

1. **Every term is nonnegative on `[-1,-1/2]^3`.** Both factors are
   `y1^2 x^2 + b x y` and `u(z) + b' y z`, plus shares of `c y^2`.
   - `b = 2 y1 > 0` and `b' > 0`, and `x, y, z < 0`, so both couplings are
     positive.
   - `u >= 0`: its inner piece is a nonnegative quadratic, and its outer piece
     increases in `|z|` from the value `eta y1^2 >= 0` at `|z| = z1`. I
     checked continuity at `z1`: `b' z1 + k = 2 y1`.
2. **The shares of `c y^2` can be taken nonnegative.** `y^2` lies in `S_y` for
   (a), (a0) (where `u_y = c y^2`) and `b_d` with `d >= 2`. By Lemma 1.2, base
   splits that differ by elements of `S` give the same bound. So with `r = 0`,
   the factor minima sum to at least `(s_1 + s_2) c/4 = c/4 > 1/4`. Hence
   `V >= c/4`.
3. **Large `mu` gives nothing.** On the box, `vol/8 = 1/64`. So
   `(vol/8) exp(mu V) > exp(mu/4)/64 >= 1` for `mu >= 4 ln 64 = 16.6355`.
   Then `Phi(mu) >= 1`, and Theorem 4.2 gives no growth.
4. **Small `mu` gives little.** The full cube gives
   `Phi(mu) >= exp(-mu gamma_d)`. So the provable base per gadget is at most
   `exp(16.64 gamma_d) <= exp(33.27 E_d(L))`, using `gamma_d <= 2 E_d(L)`.
5. **Uniform in the parameters.** `E_d(L) <= C/d^2` with `C` independent of
   `y1`. This holds because `L'` is 2-Lipschitz for every `y1`, so Jackson's
   theorem applies. The bound is therefore `1 + O(1/d^2)` for every admissible
   `(y1, eta, eps_v)`.

**The wording is right.**

- Summary item 4, Theorem 4.3(3), Section 8 and the status table all say "the
  base that Theorem 4.2 can prove".
- The Summary adds "This limits the proof method, not the trees: class-b6
  trees grow by 2.0 per variable".
- Section 8 now reads "whether their true tree sizes do is not known".
- The old sentence "for the gadget chains it is false" is gone.
- The proof of Theorem 4.3 separates the proved uniform cap from the two
  computer-evaluated caps.

### R5. Scope of the independent reproduction

- **Review's log.** `robust-lb-review-checks/logs/check3_bb.log` has exactly
  these runs, all with `delta = 0`: class (a) (`d = 2`) at
  `eps = 1e-2, 1e-4, 1e-6`, and b4 and b6 at `1e-4`, each for `G = 1, 2, 3`.
  The counts match Section 6.4.
- **Recheck's log.** `robust-lb-recheck-checks/logs/check_bb.log` has a, b4
  and b6 at `eps = 1e-4`, `G = 1, 2, 3`, all with `delta = 0`.
- **The new wording matches.** It reads: "every `delta = 0` count of classes
  (a), b4 and b6 with the theorem's base split". It names the
  `delta = 1e-3` row (600, 12,330) and the `delta = 0.1` row (44, 108) as not
  reproduced.
- **Places changed.** Summary 6, Section 6.1, the Section 7 row for
  Section 6, and Section 8 ("Numerics").
- **Decision margins.** The Section 6.1 margins (`3.3e-5` pruned, `1.4e-5`
  split) match the review's log (`3.307e-5`, `1.368e-5`).
- **Balanced-split rows.** Neither independent code ran the balanced-split
  rows (b6 balanced; envelopes with the balanced split). The phrase "with the
  theorem's base split" excludes them implicitly. Section 10.2 item 3 says so
  explicitly. Optionally, Sections 6.1 and 8 could list them with the
  unreproduced rows.

### R2. The 1.063 ceiling

I recomputed the corner-box threshold with a third method: a
`50^3` grid, then a bounded L-BFGS-B polish. The quantity minimized is
`mu0 = min ln(8/vol)/g(-a,-b,-c)` over boxes `[-1,-a] x [-1,-b] x [-1,-c]`.

- **Reference box.** For the box `-(0.48, 0.873, 0.813)`:
  - `V = g(vertex) = 2.712390`;
  - a 27^3 grid confirms that the vertex nearest 0 is the minimizer on the box;
  - `(vol/8) exp(mu V) = 0.7905, 1.0368, 1.3599` at `mu = 2.3, 2.4, 2.5`.
- **Reference threshold.** `mu0 = 2.3866`, at box `-(0.476, 0.872, 0.813)`.
  The ceiling is 1.0624 per variable. This matches Section 4.4 and both
  earlier codes.
- **Other sets.** My `mu0` agrees to 4 digits with the authors' Nelder–Mead
  search for all eight parameter sets in `logs/revision2_checks.log`. It also
  agrees with the recheck's grid on its six sets.
- **Class-(a) range.** Over the seven non-reference sets of Section 6.5 and
  the recheck, the class-(a) ceilings are **1.0219–1.0733** per variable, as
  the note states. The lowest is the new set `(0.38, 0.05, 0.2)`, with
  `mu0 = 2.2706`.
- **Section 6.5 table.** Every `mu0` and ceiling entry is right. For the
  `b_d` rows, `exp(mu0 gamma_d/3)` gives 1.0062, 1.0198, 1.0019 and 1.0062.
  In every row the computed base is below its ceiling.
- **"Every minimizing `mu` in `logs/scan_bd.log` lies below the corresponding
  `mu0`" (Section 10.2 item 4).** The authors computed `mu0` for only 8 of the
  20 distinct parameter sets in that log. I computed it for all 26 rows. The
  claim holds in every row. The smallest margin `mu0 - mu` is 0.110, for b6
  at `(0.30, 0.02, 0.002)`, where `mu = 2.252` and `mu0 = 2.362`.
- **"At the reference parameters" wording.** It now appears in the Summary,
  the Open paragraph, Section 4.4, the Section 6.5 text, Section 7 and
  Section 8. Section 10.1 item 4 keeps its historical "on this gadget" with a
  pointer to Section 10.2. That is acceptable for a history section.
- **A precision point.** The range "1.022–1.073 at the other parameter sets
  tried" is right for class (a) on the seven sets where `mu0` was computed.
  Suppose "parameter sets tried" is read as every set in `scan_bd.log`. Then
  the class-(a) ceiling at `(0.38, 0.005, 0.002)` is 1.0752, just above the
  range. No class-(a) base was computed at that set, so nothing is wrong.
  Adding "class (a)" and naming the sets would remove the ambiguity (remaining
  problem 4).

### R7. Consistency checks

- `logs/verify_leaves.log` covers class (a), `eps = 1e-4`, `G = 1, 2`:
  - 20 + 600 = 620 leaves, with maximum excess `2.75e-16` and maximum split
    error `8.9e-16`;
  - 19 + 599 = 618 split boxes, with maximum residual `1.2e-15` and the
    closest value `2.187e-6` below the target.
- Section 6.1 reports these numbers correctly. Summary 6 now states the
  restriction to class (a) with `G <= 2`.
- The revision also added the word "independently" (remaining problem 2).

### R3. Lemma 1.3 with a different `r` for each removed point

The revised statement and proof are correct.

- **Definition.** `F = sup_{r in S} F^r_{B_k}` is convex, as a supremum of
  convex functions.
- **Finiteness.** `F` is finite on `B_k`:
  - `F >= F^0_{B_k}`, which is finite because `0 in S`;
  - `F <= f`, because each `vex f^r_e <= f^r_e` and `sum_e f^r_e = f`.
- **Upper semicontinuity.** Extend `F` by `+inf` outside the box. The result
  is a convex function whose domain is a polytope. Rockafellar's Theorem 10.2
  then gives upper semicontinuity on the box.
- **Every removed point.** Each removed point has
  `F(y) >= F^{r_y}(y) > UBD - eps`.
- **Closure.** The removed points are dense in each frame piece. By upper
  semicontinuity, `F >= UBD - eps` on the closed piece.
- **Jensen step.** Take an S-consistent family on the piece, with common mean
  `z`. For every `r`, its value is at least `F^r_{B_k}(z)`, by consistency
  (telescoping) and Jensen on `(B_k)_e`. Taking the supremum over `r` gives at
  least `F(z) >= UBD - eps`.

The one-`r`-per-round case is correctly described as a special case. The
status table notes the extension.

### R4. Lifted relaxations

The paragraph now requires the lifted relaxation to be "feasible at every
point of `B_k` and bounded below". It gives bounded lifted edge sets
(McCormick, RLT, moment relaxations on a box) as an example. That is
sufficient: with a linear objective and a bounded feasible set,
`phi_{B_k} > -inf`. With the containment assumption, a point mass at `y` gives
a feasible lifted point. So `phi_{B_k}` is finite and convex, and Theorem 10.2
applies.

### Optional items

- **`gamma_10 = 0` is exact.**
  - **Method.** I checked the recheck's rational polynomial with a different
    exact method from the recheck's and the authors' sympy root counting. I
    computed Bernstein coefficients in exact `Fraction` arithmetic, with
    bisection when needed. All four defining polynomials are proved positive
    on their closed intervals, using 1, 2, 4 and 3 subintervals.
  - **Slack.** The floating-point minimum slacks are `2.8e-3`, `2.8e-3`,
    `4.6e-4` and `9.0e-4`. The last three rows correspond to
    `1 + eps_v - q`, `rho - L` and `U - rho`.
  - **Transcription.** The coefficients in Section 3.3 match the recheck's
    rationals, and so do those in `revision2_checks.py`. The latter writes two
    of them with denominator `5e8`; I checked that they are equal.
  - **Why the certificate works.** On `[0, y1]` the band is
    `[y^2, (1 + eps_v) y^2]`, and on `[y1, 1]` it is
    `[2 y1 y - y1^2, (1 + eps_v) y^2 - (1-eta)(y-y1)^2]`. So the four tests
    are exactly `L <= rho <= U`, and `gamma_10 = 0` follows, as Section 3.3
    says.
- **`y1 = 0.3` cap.**
  - `mu0 = 2.3782` at `(0.30, 0.005, 0.002)`.
  - `E_4(L) = 0.013056` at `y1 = 0.3`, from a full (not only even) Chebyshev
    basis.
  - With these, `exp(2.4 · 2 E_4/3) = 1.0211` and
    `exp(mu0 · 0.0247/3) = 1.0198`. The band LP gives
    `gamma_4 = 0.024740` there.
  - All of this matches Theorem 4.3(3). Removing the "not checked" hedge is
    justified. The proof of Theorem 4.3 labels this cap as computer-evaluated.
- **`gamma_d` table.** The band LP gives the following, and all agree with
  Sections 3.3 and 6.5:
  - reference parameters: `gamma_2 = 0.076119`, `gamma_4 = 0.007770`,
    `gamma_6 = 0.002373`, `gamma_8 = 0.000776`, `gamma_10 = 0` (to `1e-6`);
  - `(0.50, 0.005, 0.002)`: `gamma_6 = 0.007338`.
- **Quantifiers in Summary 3 and the Section 3.4 sufficient condition.** Both
  are now correct: "for each `d`, the gap is positive when
  `eps_v + eta (1-y1)^2 < 2 E_d(L)`", and "width below `2 E_d(L)`".
- **"Computer-evaluated base".** Summary 5 and the Section 5 status row now use
  this term.

## 2. Silent strengthening and withdrawn claims

**Mathematics: nothing is strengthened silently.** The second revision makes
four stronger statements. Each is listed in Section 10.2 and is either proved
or labelled.

- Lemma 1.3 allows `r` to vary per point. It is proved (item 6).
- Theorem 4.3(3) has a uniform cap. It is proved (item 2).
- `gamma_10 = 0` is stated as exact. It rests on an exact certificate
  (item 8).
- The `y1 = 0.3` cap is now stated without a hedge. It rests on a
  computer-evaluated `mu0`, labelled as such in the proof (item 9).

**Withdrawn claims are clearly marked.**

- Section 10.1 item 2 marks "was not located" as wrong.
- The old Section 8 sentence "for the gadget chains it is false" is gone, and
  Section 10.2 item 2 records its replacement.
- Section 10.1 items 4 and 9 point to the corrections in Section 10.2.

**Wording: two small new overstatements** (remaining problems 1 and 2).

## 3. Remaining problems

1. **New numerical range, wrong for odd `d` (small, factual).**
   - **Where.** Summary item 3 (line 102, "about `0.09/d^2` to `0.18/d^2` for
     `d = 2..12`"), Section 3.3 (line 678, "`E_d(L) d^2` lies between 0.095
     and 0.18 for `d = 2..12`") and Section 10.2 item 10 (line 1412).
   - **Why it fails.** `L` is even, so `E_{2k+1}(L) = E_{2k}(L)`. My full-basis
     LP confirms this, and so does the recheck's `check_gamma.log`. The range
     holds only for even `d`. At `y1 = 0.38`:

     | `d` | 3 | 5 | 7 | 9 | 11 |
     |---|---|---|---|---|---|
     | `d^2 E_d` | 0.406 | 0.252 | 0.129 | 0.205 | 0.208 |

     For even `d = 2..12`, `d^2 E_d` lies between 0.0949 and 0.1803, as
     stated.
   - **Fix.** Say "for even `d = 2, 4, ..., 12` (odd degrees add nothing:
     `E_{2k+1} = E_{2k}`)".
   - **Scope.** The conclusion "of order `1/d^2`" is unaffected.
2. **"Checked independently" in Summary 6 (line 134; wording).**
   - **The problem.** These checks are the authors' own scripts
     (`verify_leaves.py`, `verify_split.py`). They compare with an independent
     *estimate* (grid plus local search). Section 6.1 correctly calls this "a
     consistency check, not a certificate". Next to the reproduction by the
     review, "independently" can be read as checked by another party.
   - **Suggested text.** "both consistency-checked (not certified) for class
     (a) with `G <= 2`".
3. **Section 10.2 opening, "No theorem, count or computed base changed"
   (line 1337; wording).**
   - **The problem.** The statement of Lemma 1.3 was broadened, and
     Theorem 4.3(3) gained a proved uniform cap. Both are listed in items 2
     and 6, so neither change is hidden, but the sentence is inaccurate.
   - **Suggested text.** "No count or computed base changed; Lemma 1.3 was
     broadened and Theorem 4.3(3) gained a proved cap."
4. **Optional precision.**
   - **Scope of the 1.022–1.073 range.** Lines 48, 945 and 1175 say
     "1.022–1.073 (or 1.02–1.07) at the other parameter sets tried". This is
     the class-(a) ceiling on the seven parameter sets of Section 6.5 and the
     recheck. The status table already says "class (a)". Saying the same in
     the Summary, Section 4.4 and Section 8 avoids the reading discussed
     under R2. The class-(a) ceiling at the b4/b6 scan set
     `(0.38, 0.005, 0.002)` is 1.075.
   - **"Its share of `c y^2 >= c/4`" (Theorem 4.3(3), lines 874–876).** This
     reads as if each share were at least `c/4`. Say "each factor is at least
     its share of `c y^2`, and the shares add up to `c y^2 >= c/4`".
   - **"The recheck's brackets agree to 8 digits" (line 677).** For
     `E_4` and `E_8` the recheck's brackets differ at about `5e-8` to `7e-8`.
     "Agree to about `1e-7`" is accurate.
   - **"Every minimizing `mu`" (Section 10.2 item 4).** The claim is true; I
     verified all 26 rows. But the authors' log computes `mu0` for only 8 of
     the 20 parameter sets. The sentence could cite the sets actually checked,
     or this report.

None of these items changes a theorem, a proof or a count.

## 4. Checks run

All commands were run from
`research-20260929/reviews/recheck-robust-lb-confirm-checks/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`,
single-threaded and time-limited. They are targeted checks only: no
project-wide checks and no CI. The note and the authors' files were not
modified.

| Command | Purpose | Result |
|---|---|---|
| `python3 check_confirm.py > logs/check_confirm.log` (2.3 s) | (1) exact Bernstein positivity for the `gamma_10` certificate; (2) `mu0` by grid plus L-BFGS-B for all 20 parameter sets of `scan_bd.log`, ceilings, and `mu < mu0` for all 26 rows; (3) `E_d(L)`, `d = 2..12`, full Chebyshev basis; (4) band-LP `gamma_d`; (5) arithmetic of the caps | everything in Section 1 above; odd-`d` values of problem 1 (`logs/check_confirm.log`) |
| `curl https://api.crossref.org/works/10.1137/0307039` and `.../10.1287/opre.22.2.410` | R1 bibliographic data and the Falk (1974) abstract | Section 1, R1 |
| Reading `theory-robust-lb/logs/{revision2_checks,scan_bd,verify_leaves}.log`, `robust-lb-review-checks/logs/check3_bb.log`, `robust-lb-recheck-checks/logs/{check_bb,check_ceiling_params,check_ceiling_crossover,check_gamma}.log` | R5, R7 and R2 evidence | Section 1 |
