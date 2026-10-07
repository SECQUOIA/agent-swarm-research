# Review r2 of stream `ratio-bound` (confirmation round)

Reviewer: an independent research agent that wrote neither the note nor the
round-1 review. Date: 2026-10-03. Object of review: `../note.md` (1450 lines,
the revision after review round 1; Section 6.3 lists the changes, Section 8.3
the checks). My scripts are in `r2-code/` and their outputs in `r2-logs/`. I
did not edit the note, the stream's code or its logs.

## Verdict

**Verified, with optional wording fixes.** All three minor issues and all
seven optional points of round 1 are handled correctly. The new and changed
material is correct:

- Theorem B2(2) at `ρ = 1367/10`;
- the new Theorem B3(5);
- the exact upper end of the near-boundary bracket (Section 6.1);
- the SCIP scope statement;
- the revised proof of Theorem C(3);
- the corrected statements about the failed box searches.

I re-derived each of these and checked every changed number independently.
Each changed claim carries the right status label (proved, computer-assisted,
or numerical). The Summary agrees with the body.

I found no major issue and no minor issue. Six optional points (N1–N6) are
listed below. None of them affects a claim's truth. The citations in
`orbit-closure/note.md` are correct.

## Status of the round-1 issues

| r1 issue | handled? | how I checked |
|---|---|---|
| Minor 1: wrong reason for three failed box searches | **Yes.** Sections 8.2, 9 and 6.3 now say that the bounds tried at `ρ = 6/5` (`tan:1/100:4`) and `ρ = 1, 19/20` (`tan:1/1000:9/4`) are false. The note no longer says that the closed relaxation blocked them. | The new exact sets of Theorem B3(5) have `ρ = 1.2234` (for `L ≥ 2.986`) and `ρ = 1.0414` (for `L ≥ 3.090`). A set that contains `T_r` contains every `T_r'` with `r' ≤ r`, so these sets refute the bound at all three `ρ`. The seven box conditions do not depend on `L`, so one `L` suffices. I re-verified the sets exactly (`r2_lower_sets.py`). The remaining general caveat (the conditions are only necessary) is correct and is labelled as such. |
| Minor 2(a): `[0.0305, 0.0306]` labelled exact | **Yes.** The upper end is now certified by a rational dual certificate, which gives `[763/25000, 191/6250]`. | Independent certificate (`r2_adv3_bracket.py`) with a different symmetry repair. I also removed the float-`z_K` caveat: the exact corner bound of the float data is `Z = 1 + 2.7·10^-16`, and I certified both ends for `T_{RZ}(p)`. So the bracket holds for the float instance with its exact `z_K`. |
| Minor 2(b): `136.707` presented as certified | **Yes.** The same `X` is now certified at `ρ = 1367/10` (Theorem B2(2)). The bracket `[136.7, 137]` and the gap `0.2195% < 0.22%` are exact. | `r2_lower_sets.py`: exact PSD checks; `ε_1` equals the note's fraction; a float step computation gives `136.7054` at `ε = ε_1, 10^-6, 10^-8`. |
| Minor 2(c): "(B) value = (A) value at the best height" | **Yes.** Section 3.1 now proves only "`≥`". It states that `sup_H ρ_max(H)` and the (B) constant both lie in `[136.7, 137]`, and labels equality as numerical. | I re-derived both inclusions. The lower one uses the shrinking argument and `ρ_max(31966.2) ≥ 136.7`. The upper one holds because an orbit set feasible for `ρ_max(H)` with `ρ ≥ 137` yields, after shrinking, a `B_X` that meets the seven conditions at `ρ = 137`. |
| Minor 3: scope of the SCIP part | **Yes.** The scope is now stated in Summary item 3, at the start of Section 4 and in Section 9: Case 4, `κ_S = 0`, unit coefficient on `w`, no linear terms, given coordinates. The Case-2 remark now gives the relative discriminant. | I read SCIP 10.0.3 `nlhdlr_quadratic.c`: `intercutsComputeCommonQuantities` starts at line 1111; `kappa` is computed at lines 1151–1204; `norm` and `xextra` are at lines 1665–1666. A sympy transcription of the Case-4 formulas (`r2_scip_scope.py`) confirms four claims: (1) for `w − xy ≤ 0`, `x̂ = ((x − y)/2, (w + 1)/2)`; (2) `2w − 2xy ≤ 0` is the same rule in the coordinates `(√2x, √2y, 2w)`; (3) `w − xy − c ≤ 0` gives `κ_S = −c`; (4) the relative discriminant of `(x_0 − s)² + 1` is `−4/(8x_0² + 4)`. The apex claim (`w = 1` in SCIP's coordinates, `w = 1/2` in the original ones) follows from Lemma S. |
| O1 (both logs for the (B) column) | Yes | Section 3.3 caption |
| O2 (`√(1 + H)`) | Yes | `rhomax.log`: `31.6386 = √1001`, `54.7814 = √3001` (`r2_compare_leaves.log`) |
| O3 (15,731 corners; 0.2397) | Yes. The note also adds `0.1823` for the uncompleted set. | `r2_scip_minima.py` parses the four `.log.gz` files directly. It finds 15,731 corners and the minima `0.0140` (`D ≤ 2`, `κ = 433.7`), `0.2397` (Case-4 set) and `0.1823` (uncompleted set) with `D ≤ 2`, `κ ≤ 10`. The meaning of `scipA`/`scipB` was confirmed in `rb.scip_ratio`. |
| O4 (`κ` used for two things) | Yes | SCIP's constant is now `κ_S` everywhere (grep) |
| O5 (decides attainment, open boundary case) | Yes | Summary item 4, end of Section 5, Theorem C(3), open question 4 |
| O6 (`D ≥ 1` in Corollary A') | Yes | I re-checked the proof: rays that meet `S` give `A ≤ 2 ≤ 2Dγ_D` because `γ_D ≥ 1/D`, and rays with `a_j ≥ 0` give `α ≥ 1/D`, which is at least the stated bound |
| O7 (old box-file headers) | Yes | My own comparison (`r2_compare_leaves.py`) finds 28,699 vs 28,699 leaves, identical in order and content; only the header differs. The r1 reviewer's independent verifier passes on the rerun file (`rerun_stream/r1indep_rho137_rerun.out`). |
| r1 remark: Prop. 12 not needed in Theorem C(3) | Yes | See "Theorem C(3)" below |

## Review of new and changed material

- **Theorem B2(2)** (`ρ = 1367/10`, `h_0 = 5417132036/169459`). The logic is
  sound:
  - `sym(X) ≻ 0` puts `s̄` in `int C_X ⊂ int B_X` and gives `det X > 0`;
  - `P_1, P_2 ∈ C_X`;
  - `(ρ, ρ, h_0) ∈ C_X`, so by upward closure `P_3 ∈ B_X` once
    `1 + ρ/√ε ≥ h_0`;
  - convexity then gives `T_r`, so `z_B ≥ r z_K`.

  The vertices `P_1 = (ρ, −ρ, 1)`, `P_2 = (ρ, −2ρ, 1)` and
  `P_3 = (ρ, ρ, 1 + ρ/√ε)` are correct for `r = ρ√ε/z_0` in the normalized
  frame of Theorem B. The constant `√2 · 136.7 = 193.323` is correct. The set
  of heights where `X` is PSD on the line is `[31710.24, 32226.36]`, so the
  quoted `h_0` has slack.
- **Theorem B3(5).** The same argument applies with `P_3 = (ρ, ρ, 1 + ρL)`
  and `r = ρ/z_K`, and `z_K` cancels: `D z_B/z_K = √k z_B ≥ √k ρ`. All four
  constants, `L_0` values and percentage gaps match my exact computation:
  - constants `2461/1250`, `6117/2500`, `15621/10000`, `18851/12500`;
  - `L_0 = 2.386, 2.986, 3.090, 3.340`;
  - gaps `0.061%`, `2.174%`, `0.826%`, `2.117%`.

  A float step computation with my own (B) membership test, at
  `L = 3.4, 10, 1000`, gives `D · min step = 1.96885, 2.44682, 1.56216,
  1.50820`, just above the certified values. The `X` matrices are the exact
  decimals printed in the cited logs (parsed from the logs, not copied from
  the code).
- **Section 6.1 bracket.** The duality argument is correct: for `Y_0 ≻ 0`,
  `Y_j ⪰ 0` and `Σ M(v_j) Y_j = 0`, the trace identity forces some
  `sym(X M(v_j))` to fail PSD, so `z_A/z_K ≤ R`. Interior points of `C_F` are
  positive definite points, by the same face argument as in Theorem B(5). My
  independent certificates hold at both ends, with margins `3.4·10^-9` (dual)
  and `1.0·10^-4` (primal) in the normalized frame.
- **Theorem C(3), new compactness step.** It is correct. A limit of `F_n`
  with `det F_n > 0` has `det F ≥ 0`. If `det F > 0`, then `C_F ⊇ T*` by
  closedness, and `F` is a positive multiple of some `(α, β)` by part (1). If
  `det F = 0`, then `F^T = u v^T` and `C_F` lies in the plane
  `{M(s)^T v ∈ R u}`. This equation is nontrivial for `v ≠ 0`, so `C_F`
  cannot contain the full-dimensional `T*`.
- **Section 3.1, "Why the (B) value is about 137".** Correct as revised (see
  Minor 2(c) above).
- **Summary.** It agrees with the body: the B3(5) brackets, "within a factor
  3.72" (`1.54(1 + √2) = 3.718`), and the SCIP scope. The only differences
  are N1 and N2 below.
- **Status labels.** Each changed claim carries the right label:
  - computer-assisted / exact: B2(2), B3(5), the bracket;
  - numerical: the equality of the (B) constant and `sup_H ρ_max`; the (A)
    constants; `56.7`;
  - derived from reading the source, not tested in SCIP: the scope
    consequences.

## Consistency with `orbit-closure/note.md`

The sibling note says that it uses three results of this note. All of its
citations are correct, and they use the current numbering:

- **Lemma S** (line 249): `F^T = R_θ`, `(sin θ, cos θ) = x̂/‖x̂‖`,
  `x̂ = ((x − y)/2, (w + 1)/2)`. This matches Section 4.
- **Theorem A** (lines 425, 454): at the W-corner, `q(s̄) = 2`,
  `X~ = Y~ = 2/ε`, so `D = √2/ε`. Then `z_K f(D) = 2/((1 + √2)D) =
  (2 − √2)ε` (sympy, `r2_misc.log`). Theorem A explicitly allows `N` rays and
  non-simplicial cones, so it covers the four projected rays. The bound needs
  `D ≥ 1`, i.e. `ε ≤ √2`, which holds in the regime used.
- **Theorem B(5)** (lines 537, 846): "`z_B/z_K → 0` as `ε → 0`" is exactly
  Theorem B(5).
- **Theorem B(4)** (line 542): `3 · 160 = 480`, with the range
  `ε ≤ 1.024·10^-7`. This is correct. Theorem B(4) is still stated in this
  note, marked as superseded by B2(1).

One suggestion for the sibling note, not an error. Its Limits say that
Theorem B(5) is "proved there, without a rate". Theorem B2(1)
(computer-assisted) now gives a rate for every `ε ∈ (0, 1)`:
`z_B/z_K ≤ 137√ε/z_0`, hence `z_cl,B/z_K ≤ 411√ε/z_0`. The same bound covers
(A) for all `ε`, not only for `ε ≤ 1.024·10^-7`. Citing B2(1) would
strengthen Corollary 13, at the price of depending on a computer-assisted
result.

## New issues

### Major

None.

### Minor

None.

### Optional

- **N1. The rounded range `ε ≤ 1.83·10^-5` is wider than the certified
  `ε_1`** (Summary item 2, Section 3.1 line 533, Section 6.1 line 1075,
  Section 9 line 1398). The certificate gives `ε_1 = 1.8288·10^-5`, which is
  below `1.83·10^-5`. The statement as written is still true: with the same
  `X`, the height `h' = 31800` is PSD and gives `(ρ/(h' − 1))² = 1.848·10^-5`
  (`r2_misc.log`, exact). Change: write `ε ≤ 1.828·10^-5` (or `ε_1`), or
  quote the larger range together with a check that covers it.
- **N2. "`= 193.8/D`" in Summary item 2.** `137√2 = 193.747`. The body
  correctly writes `< 193.8/D`. Change: write "`< 193.8/D`" in the Summary as
  well.
- **N3. "No theorem changed"** (Summary "Corrections" and Section 6.3).
  Theorem B2(2) was strengthened (`273/2 → 1367/10`), Theorem B3 gained part
  (5), and Corollary A' gained a hypothesis. Nothing was weakened or
  withdrawn, which is presumably what the sentence means. Change: say "no
  claim was weakened or withdrawn; B2(2) was strengthened and B3(5) added."
- **N4. "The results list"** (Section 6.3, under minor issue 1 and point O5)
  points to a structured list that is not part of `note.md`. It was
  presumably the author's report to the coordinator, and there is no
  `ratio-bound` file in `../.coordination/`. Change: remove the references or
  say where the list is.
- **N5. Section 8.3, `certify_adv3_upper.py` row.** The row quotes one float
  dual margin, `1.9·10^-8`. That is the margin for `R = 153/5000`; for
  `R = 191/6250` it is `3.4·10^-9`
  (`logs/rev1/certify_adv3_upper_191_6250.log`). This does not affect
  exactness. Optionally, the note can also drop the "float `z_K`" caveat of
  Section 6.1: my check shows that the bracket holds with the exact corner
  bound of the float data.
- **N6. "Nothing here has been committed"** (line 15; also `PROGRAM.md`).
  `git log` shows that `note.md` is in commit `d91d8d98b`, and the working
  copy equals `HEAD`. The commit was not made by this stream's agents as far
  as I can tell, but the sentence is now false. Change: update it, or say
  that commits are made outside the stream.

## Checks actually run (reviewer r2)

All checks are targeted and local. No project-wide verification was run and
CI was not consulted. All Python runs used `OMP_NUM_THREADS=1` and a
`timeout`. At most three processes of mine ran at once. My scripts do not
import the stream's code or the sfree code.

| command (from `reviews/r2-code/` unless noted) | purpose | outcome |
|---|---|---|
| `timeout 900 python3 r2_lower_sets.py` | Theorem B2(2), Theorem B3(5): exact checks of the 5 sets parsed from the logs; PSD height interval; `ε_1`, `L_0`, constants; float step lengths with my own (B) membership test | ALL PASS (`r2-logs/r2_lower_sets.log`) |
| `timeout 900 python3 r2_adv3_bracket.py` | Section 6.1: instance rebuilt from `theta`; exact `z_K` of the float data by face enumeration in 60 digits; my own dual certificate at `R_u ≤ (191/6250)Z` and my own primal orbit set at `R_l ≥ (763/25000)Z` | `Z = 1 + 2.7·10^-16`; both ends certified exactly; ALL PASS (`r2-logs/r2_adv3_bracket.log`) |
| `timeout 300 python3 r2_scip_minima.py` | O3: minima recomputed from the `.log.gz` files | 15,731 corners; `0.0140`, `0.2397`, `0.1823` as in the note (`r2-logs/r2_scip_minima.log`) |
| `timeout 300 python3 r2_scip_scope.py` | Minor 3: SCIP Case-4 `x̂`, `ŷ`, `κ_S` from the source formulas (sympy); relative discriminant `−4/(8x_0² + 4)` | ALL PASS (`r2-logs/r2_scip_scope.log`) |
| `timeout 300 python3 r2_compare_leaves.py` | O7: stored vs rerun `ρ = 137` box file; O2: `√(1 + H)` | identical leaves (28,699, same order); values match `√1001`, `√3001` (`r2-logs/r2_compare_leaves.log`) |
| `timeout 300 python3 r2_misc.py` | N1 (range `1.83·10^-5`), orbit-closure arithmetic (`D = √2/ε`, `(2 − √2)ε`, `480`), percentage gaps, factor 3.72 | all as stated (`r2-logs/r2_misc.log`) |
| `timeout 3600 ./run_reruns.sh` (each job `timeout 1500`, three at a time) | reruns of the stream's key certificates, from `code/`: `certify_lower_found.py`, `certify_adv3_upper.py 191/6250`, `certify_adv3_upper.py`, `verify_zB.py` on `logs/rev1/leaves_rho137_rerun.jsonl.gz` and on the `k = 49/25` file, `certify_zB_lower.py`, `certify_sharpA.py`, `certify_support_one.py`, `scip_kD_family.py`; plus the r1 reviewer's `indep_verify_boxes.py` on the rerun `ρ = 137` file | all exit 0 and ALL PASS / ALL LEAVES VERIFIED / INDEPENDENT CHECK PASS. Outputs are byte-identical (`diff`) to `logs/rev1/certify_lower_found.log`, both `logs/rev1/certify_adv3_upper*.log`, `logs/certify_zB_lower.log`, `logs/certify_sharpA.log`, `logs/certify_support_one.log`, `logs/scip_kD_family.log`, and to `logs/rev1/verify_rho137_rerun.log` apart from that log's trailing `exit 0` line (`r2-logs/rerun_stream/`) |
| read-only `sed`/`grep` of SCIP 10.0.3 `scip/src/scip/nlhdlr_quadratic.c` (lines 1100–1210, 1560–1720) | line numbers and formulas cited in Section 4 | as stated (see Minor 3) |
| read-only `git log` / `git diff --stat` on `note.md` | N6 | committed in `d91d8d98b`; working copy equals `HEAD` |

Process hygiene: I started one `find /` by mistake. It was slow, and I
stopped it after about two minutes. All my runs have finished, and no
process of mine is left running. A temporary debug file in `/tmp` was
deleted. I did not change git state.
