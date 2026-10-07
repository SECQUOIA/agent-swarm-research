# Review round 2: `three-var-computation/note.md`

Reviewer: independent confirming research agent (round 2), 2026-10-03. Scope: the
fixes for the nine round-1 issues, the revised Summary, Main result 2 and Sections 4.1,
4.4, 4.5, 7 and 8, and the diff against `HEAD`. "Reviewed" here means checked by a
research agent that did not write the material; it is not journal peer review. The
note and the stream code were not edited. My code is in [r2-code/](r2-code/) and my
outputs are in [r2-logs/](r2-logs/). None of my scripts imports stream code. They read
raw stream records (BoxQP files, audit JSON, saved points and depth arrays). All runs
used `OMP_NUM_THREADS=1` and `timeout`, one process at a time. No strict audit was
rerun, and no process is left running.

## Verdict

**Minor fixes.** All nine round-1 issues are fixed, and every changed number I checked
matches the raw records. The `spar` claims are now scoped correctly. The Summary, Main
result 2 and Sections 7 and 8 claim one strict audit (`spar090-075-1`). Section 4.1
lists the 16 instances that were not audited strictly, and the original-audit evidence
is labelled as such. I found no implicit generalisation. The 9-of-15 correspondence,
the small-gap noise figures and the account of the failed strict attempts are accurate.
Lemma 3's new hypothesis and the capped containment argument are correct, and the
citation of Conjecture 2.11 matches the completeness note.

Four new minor issues remain. The most relevant one concerns the precision of the
strict headline. The exact minimum depth at the strict point is provably below the
stated `−8.10·10⁻⁹`. The conclusion still holds: the gain term is far below 1% of the
gap.

## Status of round-1 issues

| # | r1 issue | Status | Evidence |
|---|---|---|---|
| 1 | 70.01% `spar` headline was a triangle artefact | **Fixed** (see new issues 1 and 3) | The strict depth array (117,480 entries) and the base point in `logs/strict_r1/` are bit-identical to `r1-logs/spar090_strict.*`. The gain term `4.877596495809501·10⁻⁵`, ratio 0.04505% and 0.5423% with margin, primal change `2.8·10⁻¹⁰` relative, 12,020 triangles and triangle maximum `3.5411876556090682·10⁻⁹` all recompute from the raw files. The coverage text is accurate: one strict audit; `spar100-050-1/2` stopped with enforced-triangle maxima `1.036850683089341·10⁻⁸` (9 triangles above `10⁻⁸`) and `1.580930453215501·10⁻⁸` (469 above `10⁻⁸`); round 2 at `tol=10⁻¹⁰` returned bit-identical `B` values. The tolerance is passed to Clarabel (`conic.py` lines 172–177), so a stalled `AlmostSolved` iterate repeating is plausible. The `spar125-050-1` log is empty, which is consistent with "no solved point". The 9-of-15 correspondence and the 0.89–1.00 factor are reproduced (0.8905–0.9998). Small-gap `B − opt` values (`5.59315064947441·10⁻⁵`, `2.4258285520772915·10⁻⁵`, `3.360297760082176·10⁻⁴`) and ratios 19.17%, 53.77%, 39.22% are reproduced. The maximum over the other 13 larger-gap instances is 0.3035% (`spar125-050-3`). The minimum depth at triangle-feasible triples is `−2.115·10⁻⁷`, and the maximum primal infeasibility is `1.330910265919611·10⁻⁷`. Summary, Main result 2, §4.1, §5, §7 and §8 claim only the single strict instance, plus the original-audit evidence labelled as such. |
| 2 | Thresholded triangle zeros | **Fixed** | All 15 recomputed triangle maxima in the §4.1 table match my recomputation to the displayed digits (for example `8.642851345719293·10⁻⁸` at `spar125-075-2`). |
| 3 | Stale conjecture number; containment needs caps | **Fixed** (see new issue 4) | `three-var-completeness/note.md` §2.10 states Conjecture 2.11: `P3+ = cl(D3^quad) + Σ_g cl cone(gF)`, "equivalently `H3+ = R`, and … `QPB_3 = K3 = R ∩ {Y_ii ≤ x_i}`". Its `R` is `R_D` (27 localizing matrices) plus the family LMI `[[1, bᵀ],[b, B − N_g]] ⪰ 0` of all 24 copies, the same blocks as `F` here. The containment `QPB3 ⊆ R ∩ {Y_ii ≤ x_i} ⊆ B + 24 orientations` is correct (projection to `(x, Y)`). The `A = B = ∅` localizing matrix is the Shor block. Generators `x_i`, `1 − x_i` (with `L = 1`) give the box. Two-element `w_{A,B}` give McCormick. Three-element `w_{A,B}` give level-3 RLT, and sums of two of them give each triangle (for example `x_i(1−x_j)(1−x_k) + (1−x_i)x_jx_k`). The cap is added explicitly. Under Conjecture 1 both containments become equalities, and the stated equivalence then gives Conjecture 2.11. That equivalence (Prop. 2.2, Cor. 2.4 (iv)) was checked as correct by the completeness stream's round-1 reviewer. |
| 4 | AP generator mismatch | **Fixed** | §4.2, §5, §7 and the Summary state the non-reproduction, the diagonal choice, the generator limitation, the density probe (labelled a primal screen) and the relative gap `3.597760740527601·10⁻⁶` (`= 0.001039752854/289`). |
| 5 | Wall-clock timings | **Fixed** | §2, §4.5 finding 2, §4.6, §7 and the Summary say the times are wall clock and indicative, and cite the r1 rerun. Chain `XF` times are identified as coming from separate runs. |
| 6 | Number corrections | **Fixed** (see new issue 2) | 0.31–3.73 pp, `XF/F` 0.23–2.05 (chains) and 2.1–5.7 (cacti), `ht` 0–7 with the separate six-triple audit, about 32%, `−1.85·10⁻⁷` to `−9.55·10⁻⁷`, and `1.33·10⁻⁷` all match. The added sentence on the source of the cost advantage overgeneralises (new issue 2). |
| 7 | `n = 3` table used primal values | **Fixed** | Safe closures from `data/pool_hard3.jsonl`: `K` 0.9084/0.9177/0.7668, `A` 0.5766/0.5811/0.2619, `KA` = `K`, `F` minimum `0.9999826604704566`, `KAF` minimum `0.999912428316144`. `X_safe − F_primal ≤ 5.46·10⁻⁹`. |
| 8 | Lemma 3 hypothesis; §4.5 margins | **Fixed** | The new hypothesis (convex `R` containing `y_c`, `y* ∈ R`) is exactly what the proof uses. Convexity gives `y_ε ∈ R`. For `ε ≥ |δ|`, `(M + εM_c)/(1+ε)` is the convex combination with weight `(1+|δ|)/(1+ε)` of Lemma 2's point and `M_c`, so it lies in `QPB3`. The sparse version holds because `y_c` restricted to the pattern satisfies Shor, McCormick, the caps and the triangles. The §4.5 gain terms and margins (0.00120, 0.01124, 0.03027, 0.00071, 0.01334, 0.04326), primal infeasibility `2.97·10⁻⁹` to `5.30·10⁻⁸`, 921 blocks at `m = 3000`, and the cactus triangle residual `5.35·10⁻⁷` all recompute from `logs/audit/`. |
| 9 | Double negative | **Fixed** | §6.3 reads "every queued Gurobi solve ran". |

## New issues

| # | Severity | Location | Description | Required change |
|---|---|---|---|---|
| 1 | Minor | Summary bullet 1; Main result 2; §4.1 "Strict re-audit" paragraph | The stated minimum depth `−8.10·10⁻⁹` is not the exact minimum at the strict point. The normalized triangle quadratic is a feasible `C` in Lemma 2 (`⟨C_tri, M_c⟩ = 1/4`), so the exact depth satisfies `δ ≤ −4·tv`. At triple (0, 11, 47) the triangle residual is `3.541·10⁻⁹`, so `δ ≤ −1.416·10⁻⁸`. On 73,615 of the 117,480 triples, the stored depths lie above the exact triangle and diagonal-cap bounds, by up to `9.7·10⁻⁸`. My independent five-tetrahedron lift has errors of the same size at this point, so neither computation is accurate to better than about `10⁻⁷` here. With the exact bound alone, the gain term is at least 0.079% of the gap (0.576% with the margin). If the depth errors are below `10⁻⁷`, the gain term is at most 0.56% (1.05% with the margin). The conclusion stands, but "0.045%" is more precise than the computation supports. The same applies to the r1 figure that this reproduces. | Report the strict figure as the value at the computed depths (about 0.05%). State that the computed depths have errors of up to about `10⁻⁷` on the unsafe side, that the exact minimum depth is at most `−1.42·10⁻⁸` (ratio at least 0.079%), and that the ratio stays below about 0.6% (1.1% with the margin) if the depth errors are below `10⁻⁷`. |
| 2 | Minor | Summary bullet 2 ("Most of this advantage comes from `X`'s hull-depth selection"); §4.5 finding 2; §7 timing bullet | This holds for the chains, but not for the cacti. On the chains, `log(X/XF)` is 0.65 to 1.26 of `log(X/F)` for every chain with `m ≥ 300`. That supports the claim, although chain `XF` times come from separate runs. On the cacti, `XF` ran in the same `driver.py` run as `F` and `X`. There, `XF/F` is 2.1 to 5.7 and `X/XF` is 0.80 to 2.8, so selection explains −0.15 to 0.48 of `log(X/F)`. Lifting the same triples costs several times more than family blocks, so on the cacti the block type, not selection, accounts for most of the advantage. This wording came from my predecessor's suggestion in r1 issue 6. | Limit the sentence to the chains (for example, "at `m = 3000`: 2999 against 1051 lifted triples"). Add that on the cacti, where the comparison is within one run, the exact lift on the same family-selected triples took 2.1 to 5.7 times the solve time of `F`. |
| 3 | Minor | §4.1, the two consecutive paragraphs that begin "The other 13 original instances" and "On the other 13 instances" | "The other 13" names two different sets. The first is the 17 audits minus the four deep instances. The second is the 14 instances with relative gap above `10⁻⁵` minus `spar090-075-1`. The second set includes the three unaudited deep instances and excludes the three small-gap ones. A reader can attach the 0.304% bound to the listed 13. | Name the second set explicitly. For example: "On the 13 instances other than `spar090-075-1` with relative gap above `10⁻⁵` (including `spar100-050-1`, `spar100-050-2` and `spar125-050-1`) …". |
| 4 | Minor | §4.4 ("parallel (unreviewed)"); §5 third bullet; §6.5 row 3 | The completeness note is no longer unreviewed. It has a round-1 review ("minor fixes"; no error found in a proved statement; Prop. 2.2 and Cor. 2.4, which give the cited equivalence, checked as correct). It has been revised and is not yet re-reviewed. | Say "reviewed in round 1 and revised; not re-reviewed" instead of "unreviewed". |

**Optional (no change required).** Two of the note's residue explanations can be made
sharper.

- At the original audit points, the bulk of the depths at triangle-feasible triples are
  normalized diagonal-cap residuals: the cap quadratic `x_i − x_i²` has uniform mean
  `1/6`, so a cap residual `c` forces a depth of at most `−6c`. At `spar125-050-1`, all
  125 caps are exceeded, by up to `3.18·10⁻⁸`. The cap bound is `−1.91·10⁻⁷`, against
  the triangle-feasible minimum `−2.12·10⁻⁷`; the median depth is `−1.82·10⁻⁷`, and
  317,740 of the 317,750 triples are below `−10⁻⁷`.
- At the final `F` point of cactus `m = 300`, the minimum depth `−2.138·10⁻⁶` equals
  `−4 ×` the triangle residual `5.35·10⁻⁷` of the same triple.

**Diagnostic of the remaining 16.** At the saved near-strict base points of
`spar100-050-1` and `spar100-050-2`, my independent lift gives depths of `−7.5·10⁻⁸` and
`−9.4·10⁻⁸` for the originally deepest triples. These triples had original depths of
`−1.48·10⁻⁶` and `−1.36·10⁻⁶`. Over the 100 originally deepest triples, the minimum
depths are `−8.6·10⁻⁸` and `−1.26·10⁻⁷`, each matching `−6×` a cap residual. This
supports the note's explanation for these two instances. It covers 100 triples per
instance at points that are not strict, so it is not a strict audit. The note is right
not to claim one.

## Checks run

All commands ran from `three-var-computation/` with
`OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1` and the `timeout` shown.

| Check | Command | Outcome |
|---|---|---|
| §4.1 recomputation: 17 audits, 9 of 15, small-gap noise, strict reproduction, failed attempts | `timeout 600 python reviews/r2-code/r2_spar_check.py` → `r2-logs/r2_spar_check.out` | Reproduced all quoted §4.1 numbers (round-1 issue 1 row). The strict depth array and base point are bit-identical to the r1 records. Failed-attempt maxima and the 17 and 24 added triangles match the logs. |
| One-sidedness of stored depths at original points | `timeout 600 python reviews/r2-code/r2_depth_side.py` → `r2_depth_side.out` | Stored depths exceed the exact bound `−4·tv` by up to `1.8·10⁻⁷` (`spar040-050-2`) and by at most `5.3·10⁻⁸` elsewhere. This is consistent with the note's one-sided-accuracy caveat. |
| Cap-residual explanation of bulk depths | `timeout 600 python reviews/r2-code/r2_cap_residual.py` → `r2_cap_residual.out` | Bulk depths match `−6 ×` cap residuals (optional remark). |
| Exact bounds at the strict point | `timeout 300 python reviews/r2-code/r2_strict_bounds.py` → `r2_strict_bounds.out` | Exact minimum depth `≤ −1.416·10⁻⁸`. Stored depths lie above exact bounds on 73,615 triples, by up to `9.7·10⁻⁸`. Ratio sensitivity is given in new issue 1. |
| Independent lift at the strict point (120 triples) | `timeout 900 python -W ignore reviews/r2-code/r2_strict_probe.py` (core: `r2_lift_probe_core.py`) → `r2_strict_probe.out` | The lift also exceeds the exact bounds by up to `4.9·10⁻⁸` (some `optimal_inaccurate`). Depths at this scale are solver-limited. |
| Independent lift at the failed strict attempts' points (100 triples each) | `OPENBLAS_NUM_THREADS=1 timeout 900 python reviews/r2-code/r2_lift_probe.py` → `r2_lift_probe.out` | Sanity checks: `depth(M_c) = 1.0000000000003`, rank-one depth `4·10⁻¹²`. The originally deepest triples are no longer deep (diagnostic paragraph above). |
| Cost split, §4.5 audits, `n = 3` safe table | `timeout 300 python reviews/r2-code/r2_cost_split.py` → `r2_cost_split.out` | §4.5 and `n = 3` numbers match. Cost-mechanism finding in new issue 2. Timing ratios come from the regenerated `logs/table_*.md`, which r1 had checked against the raw logs. |
| Conjecture 2.11 and the definition of `R` | read `three-var-completeness/note.md` §1, §2.10 and its `reviews/review-r1.md` | Matches the citation. Containment verified by hand (round-1 issue 3 row). |
| Lemma 3 | proof re-derived by hand, including the sparse case and `y_c` against the triangles and caps | Correct as stated. |
| Diff and links | `git diff -- research-20261001/three-var-computation/note.md`; every local link in the note tested with `test -e` | No broken links. No new errors beyond the four issues above. |
| Process and write check | `pgrep -af 'strict_spar_audit\|three-var-computation'`; `find . -newer …` outside `reviews/r2-*` | No stream process running (only my own shell matched). No files written outside `reviews/review-r2.md`, `reviews/r2-code/` and `reviews/r2-logs/`. |

All checks are targeted to this stream. No project-wide verification was run, no CI
was inspected, and no git state was changed.
