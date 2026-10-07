# Review r2 of stream `orbit-closure`

Reviewer: an independent research agent that wrote neither the note nor the
round 1 review. Date: 2026-10-03. Object of review: the revised `../note.md`
(1015 lines, modified 2026-10-03 22:05), the changed code
(`verify_box_cert.py`, `test_verify_box_cert.py`, `verify_closure_cert.py`,
`certify_closure_point.py`, `closure_lower.py`, new `check_review_r1.py`,
`test_verify_closure_cert.py`) and the new logs in `../logs/revision-r1/`. I
read the full diff against `HEAD` (`git diff -- research-20261001/orbit-closure/`).
My scripts are in `r2-code/`, their outputs in `r2-logs/`. I did not edit the
note, the code or the logs. I did not rerun the stopped Proposition 16 (B) box
certificate or the BP triangle search.

## Verdict

**Minor fixes.** All twelve round 1 issues are fixed correctly. The main
answer and every certified number hold. I found two new low-severity issues
that need a short fix, and two optional points:

- N1. Both verifiers accept a point `λ̂` with a negative entry on a ray that
  no bound lists. Such a point is never in a closure. No saved certificate is
  affected. This is not a double-counting route; the double-counting hole of
  round 1 is closed.
- N2. A displayed identity in the proof of Theorem 11(c), case (v), is false
  as written. The sign conclusion drawn from it is correct. This text predates
  the revision.

No result changes.

## Status of the round 1 issues

| r1 # | Status | How I checked |
|---|---|---|
| 1 Duplicate rays in the box verifier | **Fixed** | I read the new code. `json.load` uses an `object_pairs_hook` that rejects duplicate keys at any level. `ray_index` accepts only `str` keys equal to `str(int(key))` in `[0, n)`. The ray IDs from `v` and `kb` together must be distinct. So each ray contributes at most once per leaf. Leaves are checked one by one, and nothing is summed across leaves. 14 of my own double-counting probes on the false point `(1/10, 0, 1/12)` are all rejected (`r2-logs/probe_r2_verifiers.log`). They cover the aliases `"0_0"` (Python's `int` accepts underscores), `" 0"`, `"+0"`, `"-0"`, Arabic-Indic and full-width digits, integer and string `kb`, `kb` as an object, `v`/`kb` overlap, every leaf listed twice, and duplicate literal `"v"` and `"lam"` keys. The verifier still checks the right thing: the original certificates pass and the false point without tricks fails (21 failures). The r1 probe is now rejected (`rerun_r1_probe.log`). The wording "separate verifier by the same author" is used in the Summary, §4 and §9.1. The one remaining gap concerns the sign of `λ̂` (N1), not double counting. |
| 2 Rounded-up certified bounds | **Fixed** | I grepped the note. Every certified lower endpoint is now `0.97538` (Summary item 1; Theorem 9(c), twice; §4 table, twice), and Proposition 10 uses `0.9953611`. The remaining `0.97539` and `0.9953612` values are labelled approximate or are numerical table values (§4 `α ≈ 0.97539`, §7, §8, §12 rows 12 and 26). My exact checks: `0.97538 ≤ 0.9753853514`; `0.9953611 ≤ z_LP < 0.9953612`; the upper endpoints `0.25905` and `0.2591` lie above `136/525`; `0.2324859` lies above `w^T λ̂ = 464971761/2000000000`; `0.2596/0.2324859 ≥ 1.1166`. The case (v) bound `(√(65/14) − 1)/4 = 0.2886823` is `> 0.2886` (checked by squaring rationals). The exact W-corner cut `((√2 − 1)/4)(λ_1 + λ_2) + ((√2 + 1)/4) λ_4 ≥ 1` was rederived by my own code (check D below). |
| 3 "15 of 16" | **Fixed** | "17 of 18 (11 P and 7 BP values)" matches the §7 table: P has 11 entries, BP has 7, and only adv8_1 BP differs. |
| 4 Lemma 7 interior | **Fixed** | Line-by-line check below. My symbolic check: the linear part has determinant `−(F^T)_21 det F^T / 2`, and `(F^{-T}J)_22 = −(F^T)_21/det F^T`. So the linear part is singular exactly when `(F^{-T}J)_22 = 0`, and then the `(2,2)` entry of the image is the nonzero constant `(F^T)_22`. |
| 5 Lemma 8 general proof | **Fixed** | Line-by-line check below. My own sympy check (A1–A6) confirms all identities for symbolic `S`, `m`, `N`, and the Theorem 14 forms `−8b/3, 8b/3, 10b/9`, `m^T S m = 4a/9` computed from the corner's vertices. |
| 6 Closure verifier pruning | **Fixed** | `verify_closure_cert.py` reads `instance.xpoints`. It checks that every point lies in `X` and fails at once otherwise. It requires `x_j = 0` for every `j` with `λ̂_j = 0` before using the vertex inequality. This is sound: the inactive coordinates of a piece range over `R_+`, but they do not change `a^T x` when `x_j = 0` there. Then `a^T x < 1` at the vertices gives `a^T x < 1` on the whole piece plus the cone. So no cut vector valid for `X` lies there. When `x_j > 0` the piece is not pruned (it needs an SDP certificate), which is conservative. My probe prunes the W-corner piece with `x = (0, 0, 0, 2) ∈ X`, although the piece plus `R_+ e_4` contains the valid cut vector `(0, 0, 0, 1/2)`. The revised verifier rejects this; the `HEAD` verifier accepted it (exit 0). So the round 1 gap was real, and it is now closed. The producer applies the same guard (`outside_V(..., act)`). The three current certificates and the repacked legacy certificate pass, with 0 pruned pieces. |
| 7 Lemma 16 on unbounded coordinates | **Fixed** | Line-by-line check below. Theorem 11(b) now falls under the lemma with `I_0 = {4}`. I rechecked the integer certificate: `R = [[14, 18], [18, 85]]`, determinants `120, 799, 91`, and `Q` PSD with positive trace at the four vertices (E1–E3). |
| 8 BP preimage wording | **Fixed** | `{M : sym(AMB^T) ⪰ 0} = {M : sym(B^{-1}A M) ⪰ 0}`, so the preimage is `C_F` with `F^T = B^{-1}A`. The rest of the paragraph (`F^T M(s̄) = B^{-1} Y B^{-T}`) is consistent with this. |
| 9 Renumbering | **Fixed** | The note's result headers are in order 1–16 (Lemma 12 is the inline item before Proposition 13). No internal reference uses an old number: the only hits for "Lemma 14", "Proposition 12" and "Corollary 13" are in the §11.1 changelog. "Theorem 14", "Proposition 9" and "Proposition 16" always refer to the sfree note. For stale references in other files, see "Stale external references". |
| 10 B2(1) citation | **Fixed** | Ratio-bound note Theorem B2(1) (line 423): "For every `ε ∈ (0, 1)`: `z_A/z_K ≤ z_B/z_K ≤ 137 √ε / z_0`". The setting is the corners of Theorem B (unit costs, `z_K = z_0 = (1 + √(1 + 4ε))/2`). Its (B) family `B_X = cl(C_X + R_+ e_w)`, `det X > 0`, is this note's (B). Proposition 5 with `N = 3` gives `411√ε/z_0`. `Cl_B ⊆ Cl_A` gives the same rate for (A). The status label "computer-assisted" is correct. The ratio-bound round 2 review verdict is "Verified". See optional point O1. |
| 11 Saved Proposition 10 cuts | **Fixed** | My own exact replay (`r2-code/indep_prop10_replay.py`, no stream imports, see check 8) gives the same rational `z_LP = 396503562307491652037015395705021177207626376155404352/398351441316353660966368086274075897893464946699521021 ≈ 0.995361184077`. |
| 12 Gzipped checkpoint | **Fixed** | §5, §12 and §15 say to decompress first. `box_cert.py INSTANCE FAMILY OUT.json --resume` reads `OUT.json`, which matches the instructions. |

The corrected header ("Repository commits made outside this program have
included this stream's files") is true: `git log` shows `note.md` in commit
`d91d8d98b` (2026-10-02).

## Proofs checked line by line

**Lemma 7.**

1. `int B_F ≠ ∅ ⇒ C_F ≠ ∅` holds, since `B_F = cl(C_F + R_+ e_w)`.
2. The linear part of `s ↦ sym(F^T M(s))` has rank 3 or 2. If `(F^T)_21 = 0`,
   it maps `(w, x, y)` to `(f_11 w + f_12 y, (f_11 x + f_22 y)/2, 0)`. This
   has rank 2, because `f_11 ≠ 0`.
3. In the rank-2 case, a kernel element satisfies `sym(F^T M_0(d)) = 0`. So
   `F^T M_0(d) = tJ` with `t ≠ 0`, which gives `(F^{-T}J)_22 = 0`.
4. If the image contained `0`, then `M(s) = t'F^{-T}J`, so `M(s)_22 = 0`.
   This contradicts `M(s)_22 = 1`.
5. A plane through the PSD cone that misses the apex meets the open PD cone.
   Every supporting hyperplane of a closed convex cone passes through the
   apex: if `⟨c, x_0⟩ = β < 0` at a touching point, then `⟨c, 2x_0⟩ < β`.
   A hyperplane that meets `K` but not `int K` would be such a supporting
   hyperplane.
6. The preimage of the open PD part of the plane, under an affine map onto
   the plane, is open and nonempty.
7. The rest of the proof is unchanged and was accepted in round 1.

Correct.

**Lemma 8.**

1. `S J^T S = −det(S) J` holds for symmetric `S`, since `A^T J A = det(A) J`
   for every `2 × 2` matrix `A`.
2. With `v^T = m^T S J^T`:
   `−v^T S N v = −m^T (S J^T S) N J S m = det(S) m^T J N J S m`. This form is
   linear in `S`.
3. `J^T S J = adj(S)` and `S adj(S) S = det(S) S`.
4. `v^T Z v = (v^T S m) v_1 = 0`, so `v` is kept.
5. The final step uses `det S > 0`.

Correct, and general.

**Lemma 16.**

1. `Q` is affine, so PSD with positive trace extends from the vertices to `Π`.
2. `Q` is constant along `e_j` for `j ∈ I_0`, because `Y_j = 0` there.
3. `a_j A_0 + A_j ⪰ 0` follows from `A_0 + α_j A_j ⪰ 0`, divided by `α_j`.
   For `α_j = ∞` it is the recession condition.
4. The identity
   `Σ⟨A_j, Y_j⟩ = tr(F^T Σ M_0(p_j) Y_j) = −tr(F^T M(s̄) R) = −⟨S, R⟩`
   uses that `R` is symmetric.

Correct. The statement implicitly assumes `λ̂ ≥ 0` when it is applied with
`I_0 = {j : λ̂_j = 0}`. This is true for every point in the note; see N1 for
the verifier.

**Theorem 11(c), case (v).** I checked every step symbolically (C1–C9). The
chain from `h > 0` and admissibility of ray 1 to `c < c_1`, then
`(1 − 2β + c)/(c − β²) > (3 − β)/(β(1 + β)) ≥ 65/14`, then `> 0.2886`, is
correct. The ratio decreases in `c`, with derivative
`−(1 − β)²/(c − β²)²`, and `(3 − β)/(β(1 + β))` decreases in `β`. One
displayed identity is wrong as written (N2).

## New issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| N1 | Low | `code/verify_box_cert.py` (cut leaves, lines 245–291); `code/verify_closure_cert.py` (`act`, lines 49–50); note §9.1 ("unlisted rays contribute zero") and §9.2 | Neither verifier checks that `λ̂ ≥ 0` or that `λ̂` has one entry per ray. Letting unlisted rays (box) or inactive coordinates (closure) contribute zero is valid only when those entries of `λ̂` are `≥ 0`. My probes are accepted with exit 0 and "ALL PASS": `λ̂ = (1/5, −1, 1/6)` with `boxcert_thm14_BP.json` (ray 1 is listed in no leaf); `λ̂ = (1/5, 0, 1/6, −5)` (extra entry, ignored); and `λ̂ = (20, 20, 20, −5)` with `closure_cert_wcorner_A_A.json`. None of these points lies in a closure, since `Cl ⊆ R^N_+`. Every saved certificate has `λ̂ ≥ 0` of the right length (printed in the verifier logs), so no result is affected. This is not a double-counting route. | In both verifiers, reject `λ̂` with a negative entry or a length different from the number of rays, and add these mutations to the tests. In §9.1 say "unlisted rays contribute zero (`λ̂ ≥ 0` is checked)". |
| N2 | Low | Proof of Theorem 11(c), case "Ray 1 admissible, ray 2 not" (note line 510) | "`f_2'(t_K)(β − c)² = (c − β²) h(β, c)`" is false as written. It holds for the numerator `N'D − ND'` of `f_2' = (N'D − ND')/(2D²)`, which is what `verify_wcorner.py` checks. The exact relation is `f_2'(t_K) = (c − β)² h / (2(c − β²)(1 − 2β + c)²)`. The conclusion "inadmissibility means `h > 0`" is still correct, because `c − β² = det S > 0` (with `a = 1`) and `1 − 2β + c = 𝟙^T S 𝟙 > 0`. Check C1a–C1c in `r2-logs/indep_math_r2.log`. This text predates the revision; round 1 did not flag it. | Write "the numerator of `f_2'` at `t_K`, times `(β − c)²`, equals `(c − β²) h`", or state the exact relation above. |
| O1 | Optional | Corollary 14; §13 | The qualitative conclusion (`ρ_f = ∞` for (B) and (A) with the vertex fixed) needs only the proved Theorem B(5). As written, the corollary rests on the computer-assisted B2(1) for everything. | Say that `ρ_f = ∞` follows from the proved B(5) and Proposition 5, and that B2(1) adds the explicit rate. Limit the §13 dependence to the rate. |
| O2 | Optional | `code/loop_rank2.py` docstring | "Section 7 of the note" should be Section 8. This predates the revision. | Update the pointer. |

The revision introduced no other error that I could find. The new text in
§3, §5, §6, §9, §11.1, §12 and §13 agrees with the code and the logs. The
§12 rows 21–31 agree with my reruns.

## Stale external references (not edited)

- `../ratio-bound/reviews/review-r2.md` (section "Consistency with
  `orbit-closure/note.md`", lines 99–123):
  - It cites this note's line numbers (249, 425, 454, 537, 846, 542). These
    have shifted.
  - It says the note uses "three results", "Theorem B(5) (lines 537, 846)" and
    "Theorem B(4) (line 542): `3 · 160 = 480`". The revised note no longer
    states the `480√ε/z_0` rate for (A) or the B(4) range.
  - It suggests strengthening "Corollary 13", which is now Corollary 14.
  - `../ratio-bound/reviews/r2-code/r2_misc.py` (docstring line 6) checks the
    same removed `480` arithmetic.
  - These are dated review records, so they are historical rather than
    wrong, but a reader following them will not find the cited text.
- `../PROGRAM.md` line 48: "Nothing in this continuation is committed."
  This contradicts the corrected header of the note: `orbit-closure` files
  are in commit `d91d8d98b`. This is not a numbering reference, but it is
  stale.
- No other file in `research-20261001/`, `research-20261002/`,
  `research-20260928b/` or the top-level `README.md` cites this note's
  result numbers:
  - `ratio-bound/note.md` line 1372 names only the directory.
  - `research-20261002/CLOSEOUT.md` links only `CLOSEOUT.md`.
  - The `0.97539` values in `minor-sets/` are sfree values, not citations of
    this note.

## Checks run

All runs used `OMP_NUM_THREADS=1`, `PYTHONDONTWRITEBYTECODE=1` and `timeout`,
with at most four processes at a time. Commands ran from `orbit-closure/code/`
(stream scripts) or `orbit-closure/reviews/` (my scripts). These are targeted
local checks. I ran no project-wide checks and did not consult CI.

| # | Command | Outcome |
|---|---|---|
| 1 | `timeout 300 python3 verify_box_cert.py ../logs/boxcert_$c.json` for `thm14_B thm14t_B thm14_BP thm14t_BP thm14w_B` | ALL PASS, exit 0 each (5.3, 17.3, 0.8, 0.7, 11.0 s). `λ̂` as in the note. `r2-logs/rerun_verify_box_*.log` |
| 2 | `timeout 300 python3 verify_closure_cert.py ../logs/closure_cert_$c.json` for `thm14_A prop16_A wcorner_A_A`, and for `../logs/revision-r1/closure_cert_thm14_legacy_repacked.json` | ALL PASS, exit 0 (25, 92, 1, 25 pieces; 0 pruned). `rerun_verify_closure_*.log` |
| 3 | `timeout 1200 python3 test_verify_box_cert.py ../logs/boxcert_thm14_B.json ../logs/boxcert_thm14_BP.json` | Originals accepted; 33 of 33 mutations rejected (one by crash, exit 2: "cut leaf relabelled skip" in family B); exit 0; 60 s. `rerun_test_verify_box.log` |
| 4 | `timeout 300 python3 test_verify_closure_cert.py ../logs/closure_cert_prop16_A.json ../logs/closure_cert_wcorner_A_A.json` | All regressions pass, exit 0. `rerun_test_verify_closure.log` |
| 5 | `timeout 900 python3 closure_lower.py --verify ../logs/revision-r1/closure_lower_prop16_cuts.json` | 60 cuts certified; same exact value; PASS, exit 0; 4.5 s. `rerun_closure_lower_verify.log` |
| 6 | `timeout 120 python3 check_review_r1.py`; `timeout 900 python3 verify_wcorner.py`; `timeout 300 python3 ../reviews/r1-code/probe_verifier_duplicates.py` | ALL PASS, exit 0; ALL PASS, exit 0 (8.4 s); the r1 probe's doubled-ray false certificate is now rejected (exit 1, 33 failures). `rerun_check_review_r1.log`, `rerun_verify_wcorner.log`, `rerun_r1_probe.log` |
| 7 | `timeout 600 python3 r2-code/probe_r2_verifiers.py` | 20 probes. All 14 double-counting routes are rejected, as are the duplicate-key and leaf-duplication probes. The revised closure verifier rejects pruning on a free coordinate. Unsound but accepted: the `HEAD` closure verifier on that pruning (r1 issue 6, now fixed), and 3 negative or extra `λ̂` entries (N1). `r2-logs/probe_r2_verifiers.log` |
| 8 | `timeout 900 python3 r2-code/indep_prop10_replay.py ../logs/revision-r1/closure_lower_prop16_cuts.json` | My own exact code. The instance equals the note's corner. All 60 cuts have `sym(X) ≻ 0` and `sym(X(I + μ_ij N_j)) ⪰ 0`. I enumerated all 39,711 basic solutions (646 feasible). Minimum `≈ 0.995361184077`, equal to the saved rational and minimizer. The exact dual `y ≈ (0.28555, 0.56140, 0.14842)` on tight rows 15, 16, 59 satisfies `y ≥ 0`, `G^T y ≤ 1` and `1^T y = z_LP`. `0.9953611 ≤ z_LP < 0.9953612`, `z_LP > 0.9839` and `z_LP ≤ 0.999`. ALL PASS, exit 0. A floating HiGHS solve was tried first: it returned a point infeasible by `3·10^-8` and was not used. `r2-logs/indep_prop10_replay.log` |
| 9 | `timeout 600 python3 r2-code/indep_math_r2.py` | My own sympy/rational checks. Lemma 8 identities in general and the Theorem 14 forms (A1–A6). Lemma 7 plane criterion (B1–B4). Case (v) chain, including N2 (C1a–C9). W-corner exact cut at `S = I`, with the kernel vectors kept, so the steps of `B_F` equal those of `C_F` on rays 1, 2, 4 (D0–D6). Theorem 11(b) certificate (E1–E3). Rounded endpoints and `411 = 3·137` (F). ALL PASS, exit 0. `r2-logs/indep_math_r2.log` |
| 10 | `grep` over `note.md`, `research-20261001/`, `research-20261002/`, `research-20260928b/`, `README.md`; `git diff` and `git log` on `orbit-closure/` | Renumbering, stale references and history as reported above |
| 11 | `find code logs note.md -newer reviews/review-r1.md`; `ps -eo pid,args` | No stream file was modified by my runs (all newer files predate them); no `__pycache__` in `code/`; no process of mine left running |

Not run (as instructed or not needed): the Proposition 16 (B) box certificate
and the BP triangle search; `box_cert.py`, `closure_lower.py --save`, and the
numerical scans.
