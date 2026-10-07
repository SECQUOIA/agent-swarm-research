# Review round 1: `three-var-computation/note.md`

Reviewer: independent research agent (round 1), 2026-10-03. Scope: the whole note,
with the four points the author flagged. "Reviewed" here means checked by a research
agent that did not write the material; it is not journal peer review. The note and the
stream code were not edited. Reviewer code is in [r1-code/](r1-code/), outputs in
[r1-logs/](r1-logs/). All commands ran with `OMP_NUM_THREADS=1`, under `timeout`, with
at most three of my processes at a time; none is left running.

## Verdict

**Minor fixes required**, one of which (issue 1) must be fixed before the note can be
marked verified.

The proofs (Lemmas 1 to 3, the safe-bound derivation) are correct. Every main table
recomputes exactly from the raw logs with my own scripts, and the stream's runs that I
repeated reproduce their logged bounds bit for bit. The conclusions about constructed
instances follow from the data.

The main problem is the headline `spar` number. The 70.01% "gain term / gap" at
`spar090-075-1` is not a weak triple-level result. It is caused entirely by one triangle
inequality, a constraint of `B` itself, that the audit's early-stop rule left violated
by `3.15·10⁻⁶`. The deepest triple's hull depth is exactly the normalized violation of
that triangle. When I enforce the triangle and redo the audit, the minimum depth becomes
`−8.1·10⁻⁹` and the gain term falls to 0.045% of the gap. The Summary's "at most 70.01%"
is technically true of the stored numbers but misleading. It makes the `spar` evidence
look much weaker than it is.

## Issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| 1 | Important | Summary bullet 1; Main result 2; Section 4.1 (paragraphs after the table); Section 7; Section 8 item 2 | The 70.01% ratio is an artifact of an unenforced triangle (details below). In 9 of the 15 audits with saved points, the deepest triple is the triple of the most violated triangle. Its depth is 0.89 to 1.00 times `−4 ×` that violation, and the factor 4 is `1/⟨C_tri, M_c⟩`. My independent six-tetrahedron lift gives depth `= −4 ×` violation to 6 digits for the four triples deeper than `−10⁻⁶`. After strict triangle enforcement on `spar090-075-1` (12,020 triangles, no violation above `10⁻⁸`, primal infeasibility `2.0·10⁻⁹`), the minimum depth over all 117,480 triples is `−8.10·10⁻⁹`. No triple is below `−10⁻⁷`. The gain term is `4.88·10⁻⁵`: 0.045% of the gap, or 0.54% with the primal-to-safe margin. Separately, the three "initially smaller-gap" instances (`spar040-050-2`, `spar050-030-3`, `spar050-050-3`) have `B` primal values at or above the published optimum (by `+5.6·10⁻⁵`, `+2.4·10⁻⁵`, `+3.4·10⁻⁴`). `B` is tight on them to solver accuracy, so their 19%, 54% and 39% ratios divide noise by noise. "A uniformly tiny ratio across all 17 is unsupported" therefore draws the wrong lesson. | Replace the 70.01% headline with the strict re-audit result, or rerun `spar_audit.py` without the early stop for at least `spar090-075-1`. My run took 517 s and is in `r1-logs/spar090_strict.*`. Ideally also rerun the three other audits that have a triple deeper than `−10⁻⁶`. State that the residual depths are the normalized triangle residuals. Drop or relabel the ratios for the three instances whose gap is at solver accuracy. Update Main result 2, Section 7 and Section 8 item 2 ("unresolved numerical residues in `spar`") to match. |
| 2 | Minor | Section 4.1 table, column "triangle violation" | The value `0.0e+00` means "nothing above the separation tolerance `10⁻⁷`", not zero. Recomputed maxima at those points: `8.6·10⁻⁸` (`spar125-075-2`, at its deepest triple), `3.6·10⁻⁸`, `2.0·10⁻⁸`, `4·10⁻⁹`, and so on. | Print the recomputed maximum, or label the column "`< 10⁻⁷`". |
| 3 | Minor | Section 4.4 (Conjecture 1 paragraph); Section 5 | (a) The cross-reference is stale. The completeness note's conjecture is now Conjecture 2.11; "2.9" there is a section and a lemma. (b) The containment argument is incomplete. The 27 localizing matrices (`R_D`, hence `R`) do not imply `Y_ii ≤ x_i`: no generator gives `x_i(1−x_i)`, and that note itself writes `QPB3 = R ∩ {Y_ii ≤ x_i}`. So `R` is not contained in our relaxation; `R ∩ {Y_ii ≤ x_i}` is. The implication still holds, because Conjecture 2.11 is stated as equivalent to `QPB3 = R ∩ {Y_ii ≤ x_i}`. | Cite Conjecture 2.11. Argue with `R ∩ {Y_ii ≤ x_i}` and the equivalence stated in that note (which is itself unreviewed). |
| 4 | Minor | Section 4.2; Section 5 (Anstreicher–Puges bullet); Summary | The AP variant does not reproduce what Anstreicher–Puges observed. Their Table 5 lists 12 gap instances (densities 50 to 85) with absolute gaps 0.03 to 0.8. The stream's 12,000 instances (densities 50 and 75) give one gap of `1.04·10⁻³` (relative `3.6·10⁻⁶`). My probe of 12,000 more AP-variant instances (`n` = 8 and 10; densities 50, 60, 70, 75, 80, 85; 1000 each) found no gap above `10⁻⁵` relative. The density choice therefore does not explain the mismatch, and the generator probably differs from theirs. The AP text also says "`Q_ij`, `i < j`". The stream includes the diagonal, which is defensible because AP's non-integer optima need a nonzero diagonal, but the note does not say so. | State that the replication does not reproduce AP's gap instances and that the negative small-instance result holds for this generator. Mention the diagonal choice. In the Summary, give the size of the single AP gap (relative `3.6·10⁻⁶`). |
| 5 | Minor | Section 2 "Solvers"; Section 4.5 finding 2; Summary bullet 2; Section 7 | The times are wall clock (`time.time()` in `conic.py`) on a machine with load 12 to 200. Even within one `driver.py` run, methods run sequentially under changing load. On a quieter machine (load about 11), I reran `chain_m300_e0.3_s1` with `F`, `X` and `KA`. The bounds were identical, but the times were 3 to 7 times smaller, `X/F` went from 10.9 to 7.5, and `KA/F` from 3.2 to 1.4. The ordering `F < KA < X` held. The chain `XF` runs come from separate first-draft runs, so comparing `XF` with `F` crosses runs, which the note itself says is not meaningful. | Say the times are wall clock. Report ranges as indicative, or replace them with CPU time or iteration counts. Qualify the `XF` comparison (issue 6). |
| 6 | Minor | Section 4.5 findings 1, 2, 4, 5 and the audit paragraph; Summary bullet 2; Section 7 | Numbers that do not match the logs: "0.26 to 3.7 percentage points" should be 0.31 to 3.73. "`XF` at 0.8 to 1.6 times the solve time of `F` on chains" should be 0.23 to 2.05 (cacti 2.1 to 5.7 is correct), so `XF` is up to 4 times faster than `F` on small chains, not "slightly". "0 to 6 triples outside `QPB3`" on `ht` should be 0 to 7 (`ht_plus_n300_k3_s1`). "About 35%" remaining should be about 32% (`cactus_m1000_s2`). "Smallest family value `−1.6·10⁻⁷` to `−9.6·10⁻⁷`" should be `−1.85·10⁻⁷` to `−9.55·10⁻⁷`. Section 7's "`1.34·10⁻⁷`" should be `1.33·10⁻⁷`. | Correct the numbers. Since `XF` (the exact lift on family-selected triples) is sometimes faster than `F`, say in the Summary that most of the cost advantage over `X` comes from `X`'s hull-depth selection lifting more triples (2999 against 1051 at `m = 3000`), not from the block size alone. |
| 7 | Minor | Section 4.4 table; Summary item 7 ("All comparisons use safe dual bounds") | The `n = 3` closures are computed from primal values. Safe-bound closures agree (minimum `F` 0.999983, `KAF` 0.999912). | Label the table as primal values or switch it to safe values. |
| 8 | Minor | Lemma 3 statement; Section 4.5 audit paragraph | "`R ⊇ B`" reads as "the feasible set of `R` contains that of `B`". The proof needs only that `R` is convex and contains `y_c`. In Section 4.5, the bounds "at most 0.0012, …, 0.043" start from the `F` primal value, so they need the same primal-to-safe margin and feasibility qualification as in Section 4.1. | Reword the hypothesis and add the qualification. |
| 9 | Minor | Section 6.3, Gurobi row | "no queued Gurobi solve never ran" is a double negative. | Write "every queued Gurobi solve ran". |

### Detail for issue 1

| quantity at `spar090-075-1` | stream audit | strict re-audit (r1) |
|---|---|---|
| triangles; maximum violation | 12,018; `3.149·10⁻⁶` | 12,020; `0` (none above `10⁻⁸`) |
| `B` primal / safe | `−6267.557736` / `−6267.558327` | `−6267.557735` / `−6267.558273` |
| minimum depth over 117,480 triples | `−1.2594·10⁻⁵` (triple 35, 79, 84) | `−8.10·10⁻⁹` |
| triples with depth `< −10⁻⁷` | 1 | 0 |
| Lemma 3 gain term / gap | 0.7001 | 0.00045 |
| plus primal-to-safe margin | 0.7055 | 0.0054 |

Adding the two triangles did not change the `B` value (the primal value moved by
less than `10⁻⁹` relative). So the 70% came only from the depth term, not from any change in the
relaxation. Excluding the one triangle-violating triple from the original audit would
already give 0.045%. That figure is only a diagnostic, not a valid use of Lemma 3,
which is why I reran the audit instead.

## Answers to the author's four points

**(a) SPAR_RATIO and SPAR_DEPTH_RANGE.** The values are computed correctly:
`0.7000998651113319` (gain `0.07583937923992252`, gap `0.10832651600048848`); the depth
range is `−1.259445456487625·10⁻⁵` to `−9.97334192433231·10⁻¹⁰`; 0.304% at
`spar125-050-3` over the other 13. The note correctly says that this point "is not a
certified application of Lemma 3". It does not say why, and the Summary still leads with
70.01%. The depth is the triangle residual, and enforcing the triangle removes it
(issue 1). The figure is therefore not meaningful as a measure of triple-level gain.

**(b) Lemma 3 and its qualifications.** The proof is correct. Mixing `y*` with `y_c`
keeps every convex constraint of `R`. For `ε ≥ |δ|`, the triple matrix
`(M + εM_c)/(1+ε)` is a convex combination of Lemma 2's point and `M_c`, so it lies in
`QPB3`, and per-triple auxiliaries exist. The sparse version and the formula for
`f(y_c)` are right; I recomputed `f(y_c)` for all 17 instances. The feasibility and
primal-to-safe qualifications in Section 4.1 are correct and needed. One addition: the
computed depths are not one-sided bounds. For the four deepest triples, my independent
lift gives `|δ|` 0.02% to 0.7% larger than `hullsep.depth`, so `ε` is slightly
underestimated. This does not matter at that scale, and the note already says that the
computed depths must bound the exact ones.

**(c) AP exception.** Confirmed. The rerun of `ap_gap_audit.py` (copy writing to
`r1-logs/`) reproduces every number bit for bit. Independently (cvxpy model, my own
enumeration and six-tetrahedron lift), the optimum is `−289`, `B = −289.0010387`, and
the exact lift on all 84 triples closes the gap to `6·10⁻⁷`. So the gap is a genuine
triple-level gap, and the note's wording (closed by `KA`; no evidence of an extra family
gain) is correct. The withdrawal of the blanket "no natural triple-level gaps" claim is
appropriate. See issue 4 for how representative the generator is.

**(d) Gurobi.** All six late references match `.log` and `.res`. Each `.sol` point lies
in the box, and its objective computed from the instance JSON matches Gurobi's
incumbent to `6·10⁻¹³`. This confirms that the `.lp` files encode the same objective as
the JSON files used by the relaxations. The updated `U` values and closures for the
`m = 30` cacti (0.8718, 0.9249) and the `5.513752·10⁻⁵` bound difference for
`ht_plus_n30_k2_s1` are correct. The killed `chain_m300_e0.3_s1` run has no final
"Best objective" line, so `U` does not use it. Its last incumbent (`−744.955` at 245 s)
is worse than the heuristic `U = −745.188950` anyway.

## Other checks of proofs and design

- **Lemma 1** is correct. The smallest-support minimizer always has a nonsingular
  `K_S`, so skipping singular supports loses nothing in exact arithmetic.
- **Lemma 2** is correct (triangulation, Diananda for `n = 4`, bipolar, and normalization by `M_c`).
- **The safe bound** is correct as derived (weak duality with `Ax + s = b`). The code
  matches the derivation: nonnegative clipping, SOC projection, PSD eigenvalue clipping
  with shift, and Clarabel and SCS svec orders. Every variable bound used is valid:
  `Y` from McCormick, auxiliaries explicit, `N ≤ 2` implied by the block, `W ∈ [0, 1]`
  from the `M₀₀` equation. Agreement with SCS to about `10⁻⁷` supports the cone
  conventions.
- **"`B` lies inside `QPB3` up to solver accuracy"** holds once the triangle residuals
  are accounted for. At triangle-feasible triples, the depths go down to `−2.1·10⁻⁷`,
  which is comparable to the recorded primal infeasibility (up to `1.3·10⁻⁷`). The
  strict `spar090-075-1` point gives `−8·10⁻⁹`.
- **Generators:** `spar` re-implementation, chain, cactus and `ht` match their
  descriptions. The `.lp` and JSON files encode the same objective.
- **Skip rule** for coordinates at a bound (`K`/`A`/`X` selection) is valid: `x_i = 0`
  or `1` reduces `M_T` to a pair, where Shor + RLT is exact.

## Checks run

| check | command (from `three-var-computation/` unless stated) | outcome |
|---|---|---|
| `spar` numbers from raw logs | `python reviews/r1-code/spar_recompute.py` | 99 base runs: 82 below `10⁻⁶`, 85 below `10⁻⁵`, 14 larger, all with `n ≥ 50`. All 17 audit rows, the ratio 0.7000998651113319, 0.304%, the three small-gap ratios, the depth range and the maximum primal infeasibility `1.3309·10⁻⁷` reproduced. The deepest triple equals the most violated triangle in 9 of 15 audits. |
| independent depth of deepest triples | `python reviews/r1-code/check_argmin_triples.py` | Six-tetrahedron primal lift: depth `= −4 ×` triangle violation to 6 digits for all four triples deeper than `−10⁻⁶`. |
| strict re-audit of `spar090-075-1` | `timeout 1800 python reviews/r1-code/spar090_strict.py` | Minimum depth `−8.10·10⁻⁹`; gain term / gap `4.5·10⁻⁴` (issue 1). |
| Section 4.3 and 4.5 tables, SCS table, late Gurobi table, `.sol` files | `python reviews/r1-code/tables_recompute.py` | All 32 compact rows (16 chain, 8 cactus, 8 `ht`) identical to the note. Sparse `U`, gaps and ratios 5.97%, 2.82%, 19.88% reproduced. SCS safe bounds and times reproduced. 7,598 / 7,459 = 1.02 reproduced. Derived-claim discrepancies in issue 6. |
| derived claims | `python reviews/r1-code/derived_checks.py` | `KA` shortfall 0.31 to 3.73 pp; `XF/F` time 0.23 to 2.05 on chains, 2.1 to 5.7 on cacti. |
| small dense and the AP gap | `python reviews/r1-code/small_dense_check.py` | 18,000 + 12,000 records, seeds 1 to 1000 in every file; one gap (AP `n = 9`, `d = 75`, seed 586). Largest relative gaps `1.29·10⁻⁹` (primal) and `2.26·10⁻⁷` (safe). The independent model confirms the AP gap and its closure by the exact lift. |
| AP density probe | `python reviews/r1-code/ap_density_probe.py {8,10} 1000 50,60,70,75,80,85` | 12,000 instances; 0 gaps above `10⁻⁵` relative (issue 4). |
| `n = 3` pool table | `python reviews/r1-code/n3_pool_recompute.py` | Mean, median and minimum closures reproduced (primal); safe closures agree (issue 7). |
| stream unit checks | from `code/`: `python test_basic.py`; `python test_counterexample.py`; `python check_validity.py 2000 1` | All pass; outputs as quoted in Section 6.1. |
| stream closeout check | from `code/`: `timeout 120 python verify_closeout.py` | 5 PASS lines. |
| AP gap audit rerun | from `code/`: `PYTHONPATH=. python ../reviews/r1-code/ap_gap_audit_rerun.py` (copy with outputs redirected) | Audit JSON and all seven method bounds identical to the stream's logs. |
| end-to-end small instance | from `code/`: `python driver.py --json ../data/chain_m30_e0.3_s2.json --methods K,A,KA,KAF,KAFc,F,X,KAX,Xc --log ../reviews/r1-logs/chain_m30_e0.3_s2.jsonl --max_rounds 25` | All 10 final safe bounds and model sizes identical to the logged run. |
| timing reproducibility | from `code/`: `python driver.py --json ../data/chain_m300_e0.3_s1.json --methods F,X,KA --log ../reviews/r1-logs/chain_m300_e0.3_s1.FXKA.jsonl --max_rounds 25` | Bounds identical; times 3 to 7 times smaller; `X/F` 7.5 (logged 10.9), `KA/F` 1.4 (logged 3.2) (issue 5). |

All checks are targeted to this stream. No project-wide verification was run, no CI was
inspected, and no git state was changed. Running the stream's scripts from `code/` may
have refreshed `code/__pycache__/`; no stream source, log or data file was written.
