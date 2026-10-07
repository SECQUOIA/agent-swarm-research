# Review r1 of `split-practice/note.md`

Date: 2026-10-03. Reviewer: independent research agent (review round 1). I did
not write the note or its code. I did not edit `note.md`, the stream code or the
stream logs. My code is in [`r1-code/`](r1-code/) and its outputs are in
[`r1-logs/`](r1-logs/).

## Verdict

**Major problems (one), otherwise minor fixes.**

The proofs in §4 are correct, apart from one false side remark in
Proposition C(c). Almost every number in §§6–10 and the Summary matches my own
recomputation from the raw logs. My separate brute-force checks confirm the
reported splits and the "finished" normalized results. The literature locators
match the sources.

The major problem is how the note frames Theorem 3. The Summary, §11 and §12
present huge, unstable coefficients as what Theorem 3 gives at numerically
low-rank points. They are a property of this implementation. At all 9
fractional rank-1 roots in the selection, exact LLL finds a maximum-violation
split of the rational neighbour with coefficients of absolute value at most 4.
That split is violated at the stored floating-point point by 0.25 (issue 1).
§8 already hedges, but the headline conclusions do not.

Second, 17 of the 20 "unfinished" normalized searches can be certified after
the fact by Lemma A's norm bound. So the statement "the unfinished searches
remain heuristics" is too weak (issue 2).

## Issues

### Major

**1. The Theorem 3 conclusion confuses implementation artefacts with a property
of the method.**
*Location:* Summary ¶2; §8 "Theorem 3 at rational neighbours"; §11 first
bullet of "Comparison with the earlier notes"; §12 "Exactness and rank";
Open question 2.

*Description.*
- For a rank-1 neighbour `ℓ(x̃)` with `x̃` on the `10⁻⁶` grid, `D = 10⁶` is
  even. So the maximum violation is exactly `¼` (Theorem 4), and the
  maximizers are all `v` with `pᵀv = −D/2`.
- These form an affine lattice of dimension `N − 1`. It has short members,
  roughly `D^{1/(N−1)}` in size.
- `r1-code/r1_rank1_short.py` finds them by exact LLL with an embedding
  (sympy). At the 9 fractional rank-1 roots of the selection, the coefficients
  have absolute value at most 4 and the support is 5–13. The value at the
  stored float matrix is in `[−¼−10⁻⁶, 0)` (in fact `−0.250000`) in 9 of 9
  cases.
- The logged `thm3_exact` results at two of these roots have 7 and 21
  digits, with `q_at_Y = 5738` and `1.4·10³³`.
- The blow-up comes from two implementation choices:
  - `col_hnf` (`code/lattice.py`) is an echelon form without off-diagonal
    reduction, so `T` can be huge;
  - `shorten_mod_kernel` uses floating LLL plus three Babai rounds, which
    cannot reduce integers of hundreds of digits.
- The Gurobi box runs show the same picture at every root: `{0,±1}` incumbents
  with raw violation ≈ ¼ (§8).

So short, valid splits with near-maximal raw violation exist at the stored
points. The real practical obstacle is the objective, not low rank as such.
Raw maximum violation is ≈ ¼ at numerically rank-deficient points, and it is
reached by dense near-kernel splits whose normalized violation (≈ 0.02 for
support 13) is far below that of the elementary and pair splits (≈ 0.12).

*Required change.*
- Reword Summary ¶2, §11 (the proposed qualification of the split note's §8)
  and §12. State that this implementation, without exact reduction of the
  representative, gives huge coefficients; that short exact maximizers exist
  at the rank-1 roots (cite this check); and that the useful conclusion
  concerns the raw-violation criterion. Do not state that low numerical rank
  makes Theorem 3 impractical.
- Either add exact lattice reduction of the returned representative (for
  example exact LLL on the kernel lattice, or an embedding as in the reviewer
  script) and rerun the `r ≤ 12` points, or restrict every Theorem 3 claim
  explicitly to this implementation.
- The phrase "huge-coefficient Euclidean certificate" in §12 should go:
  Euclid plus reduction gives short certificates.

### Minor

**2. Most capped normalized searches are certifiable by Lemma A.**
*Location:* Summary ¶2 ("the unfinished searches remain heuristics"); §8 root
paragraph; §12 "at larger sizes its capped results should be used as a cut
heuristic"; Proposition E remark ("not practical").

*Description.* If the reported ratio is `ρ`, Lemma A implies that every split
with a larger ratio has `‖w‖² ≤ ⌊1/(4(ρ − |λ_min(S)|⁻))⌋`.
`r1-code/r1_bruteforce.py` enumerates all such `w` at the stored float point
when feasible. It confirms the reported maximum to within `7.6·10⁻⁷` on 110
of 123 records, with no better split found. This includes all 16 capped roots
and the capped `bt_n50_p0_s0__BT__cut` (`ρ ≥ 0.066`, so `‖w‖² ≤ 3`). Under
the same floating-point rules, 120 of 123 results are therefore finished or
certified. The only uncertified results are the two dense DM60 points and
`dm_QUTO_t1_n60_p75_s0__DM__cut` (`‖w‖² ≤ 7`). Proposition E is impractical
with a fixed small `ρ`, but used adaptively with the found `ρ` it is a cheap
post-check.

*Required change.* Report this certificate and adjust the counts and wording.
Add "apply the norm bound of Lemma A to certify or cap the search" to the
solver policy in §12.

**3. The §6 table does not follow the stated best-known-value rule.**
*Location:* §3 ("best of the Gurobi incumbent and any integral SDP point");
§6 table, DM60 row; §6 finding 2.

*Description.* `code/summ_points2.py` uses `max(o, c['obj'])`, which is the
wrong direction for minimization. An integral SDP point therefore never
replaces the incumbent. At `dm_LIN_t3_n60_p50_s0` the final point is integral
(max `|x − round x| = 2.2·10⁻⁶`, `1ᵀx = 0`, `f(x) = −279.7802`) and better
than the incumbent `−279.3811`. The text counts it as closed (so 12 open
instances), but the table counts it as open. With the stated rule, the DM60
row reads: closed 12 (not 11), mean closure 98.4 (not 98.3), mean SDP gap 9.91
(not 9.92).

*Required change.* Fix the rule in the summary script and the table, or state
the rule the table actually uses.

**4. The §7 table column does not match its caption or the text.**
*Location:* §7 table, column "rounds where only general splits were violated",
and the text "2057 of 2688".

*Description.* `summ_loop_bt.py` counts rounds with `fam_viol['3'] ≤ 10⁻⁶`
and normalized `ratio > 10⁻⁶`. It ignores supports 1 and 2, and the column
sums to 2123 rounds. The text's 2057 uses all supports 1–3 (I reproduce 2057).
Under the text's definition the per-`p` means are 0, 0.3, 14.9, 22.4, 22.5,
28.3, 20.1, 27.0, 22.4, 25.8 and 22.0.

*Required change.* Recompute the column with the text's definition, or
relabel it.

**5. Proposition C(c): "this `w = a·e₁` is non-primitive" is false for
`D ∈ {2, 3}`.**
*Location:* §4, Proposition C(c).

*Description.* For these `D`, `a = ⌊D/2⌋ = 1`, so `v = (−1, e₁)` is the
elementary split itself, and its normalized violation equals the elementary
one. I checked this exactly for `D = 2…8` (`r1-logs/r1_props.txt`).

*Required change.* Restrict to `D ≥ 4`, or say "for `D ≥ 4`, non-primitive
and strictly smaller".

**6. The remark after Proposition D goes beyond its proof, and its cross-reference is wrong.**
*Location:* §4, sentence after Proposition D.

*Description.* Proposition D proves NP-completeness for `{0,1}^{n+2}`. The
remark applies it to the box `|vᵢ| ≤ 1`, that is `{−1,0,1}`, and cites §6; the
box MIQP is in §8. The same construction does work for the signed box: a
violated split exists if and only if `Σεᵢaᵢ = ±T` for some
`ε ∈ {−1,0,1}ⁿ`, which is signed subset sum and NP-complete. I confirmed the
equivalence exhaustively for `n ≤ 3` (`r1-logs/r1_props.txt`). The note,
however, does not prove it.

*Required change.* Add the two-line signed case to the proof, or restrict the
remark to 0/1 boxes. Fix the cross-reference.

**7. The letter `q` has two meanings in §4.**
*Location:* paragraph after Proposition E ("every violating split has
`‖w‖² = q + 1`", "normalized violation below `1/(4(q+1)(n+1))`").

*Description.* Here `q` is the X3C parameter, while `q_Y` and `min q`
elsewhere denote the split value. §10 has the same clash: the table's `q`
column next to "min q (C)".

*Required change.* Rename the X3C parameter, or say explicitly that it is the
X3C `q`.

**8. The claim "only practical points" is too broad.**
*Location:* §9 finding 3 ("These two points are the only practical points in
this study where the tested `{0,±1}` families … find nothing and the returned
general splits are dense"); §10 finding 4.

*Description.* In the BT10 split-closure loops there are 2057 rounds in
which the tested families find nothing and the general separator returns a
split. Those splits have support 2–10 out of `n = 10` and violation up to
0.22 (§7).

*Required change.* Restrict the claim to the stored separation points and the
`dmfam`/`dmplus` loops, or to `n ≥ 20` with violation above `10⁻³`.

**9. Theorem 3 completeness flag; non-reduced echelon form.**
*Location:* §5, first bullet; `code/lattice.py`, `thm3_exact`.

*Description.* The second enumeration, which collects all candidates within
`10⁻⁹` of the floating minimum, has a cap of `2·10⁵` nodes. Its completeness
flag `c2` is discarded, so "finished" reflects only the first enumeration.
Also, `col_hnf` is described as a "column Hermite normal form", but it does not
reduce entries off the diagonal (see issue 1).

*Required change.* Record `c2`, or state the limitation in §5 and §8. Call
`col_hnf` a column echelon form, or reduce it.

**10. The "12 open instances" include one whose gap is only an upper bound.**
*Location:* Summary ¶1 ("the 12 instances with gaps above 0.01%"); §6
finding 2.

*Description.* For `dm_LIN_t3_n60_p75_s0`, Gurobi timed out even at 3600 s
(gap 6.01%). §9.1 states correctly that the true gap is unresolved, but the
Summary and §6 list the instance as having a gap above 0.01% without that
qualifier.

There is weak evidence that the gap after the families is positive. The
`dmplus` bound (`−336.6375`) is a valid lower bound and lies `0.0075` above
the families-only bound (`−336.6450`). That margin is comparable to the
accuracy of Clarabel's `optimal_inaccurate` solves, so it is not proof.

*Required change.* In the Summary and §6, write "11 established, 1 with an
upper bound only" or similar. Optionally mention the `dmplus` evidence with
its accuracy caveat.

### Optional

**11. Median definition.** §8: "three-index … violation above `10⁻³` on 15
of 17 points (median 0.152 …)". 0.152 is the median over all 17 values,
including two negative ones. The median over the 15 is 0.1545. State which one
is meant.

**12. Count of `sep_ratio` calls.** §7: "All 4768 calls of `sep_ratio` in
these loops" counts the `bt` mode only. The `btfam` loops make 400 more
calls, so 5168 in total, and none of them is capped either.

**13. Dense-point ratios are lower bounds.** With the stream's `sep_ratio` and
a 10× larger node cap (`2·10⁸`), the two dense DM60 cut points give
normalized ratios 0.001629 (QUTO) and 0.001723 (LIN). The logged values are
0.001260 and 0.001388. Both runs are still capped
(`r1-logs/r1_dense_cap.out`). This supports §8's caveat. The note could say
that the reported dense ratios are lower bounds that moved by about 25–30%
with the cap.

**14. Letchford (IPCO 2010).** Its concluding remarks state: "Another
important question is whether the separation problem for the split
inequalities can be solved in polynomial time." §2 says only that the paper
contains no separation result. Adding that it poses the question would help
the split note's attribution, which says Letchford's paper was not checked.

**15. Relation to the binary-separation stream.** `binary-separation`
Corollary 6 shows strong NP-hardness of split separation at positive definite
binary points whose violators all lie in `{0,±1}`. This is relevant to §10
finding 4, §12 "What the hardness result predicts" and Open question 6. I
found no contradiction between the two notes. Proposition D (0/1 splits at
rank 1, ordinary NP-completeness) is consistent with the binary note's FPT
claim for full families at fixed rank.

**16. Undocumented and slightly different numbers.**
- The first-run load figure "about 190–220" (§§7, 11) has no saved log. Say
  that it comes from the first agent's transcript.
- §11 says that resetting `Y₀₀` made the smallest eigenvalue `−3.3·10⁻⁸`.
  From the stored root I get `−2.0·10⁻⁷`; `Y₀₀ = 1 + 4.44·10⁻⁷` after clipping
  matches the note. The qualitative claim holds, and the congruence fix works
  (see Checks).

**17. Grammar.** §12: "the support-at-most-3 extension close 6 of the 12"
should read "closes".

## Answers to the author's specific questions

- **Corrected §4 proofs.**
  - Lemma A is correct, including the minimizer `u = {t} − 1`.
  - Lemma B is correct. It holds as an exact identity for every symmetric `Y`;
    `a, b, c ≥ 0` follows from the choice of `t`.
  - Proposition C (a), (b) and (d) are correct, including the attainment
    criterion and the `(√2, ½)` example. In (c) only the non-primitivity remark
    fails (issue 5).
  - Proposition D is correct. All cases check out, including
    `T − a(S) ≤ −1` giving `τ ≤ −9/5`.
  - Proposition E is correct.
  - The Dinkelbach argument in §5 is correct for exact arithmetic.
    `Y + η·diag(0, 1, …, 1)` is positive definite because `Y₀₀ = 1`, and only
    finitely many `w` have a ratio above a positive `η`.
  - Relation to the split note: the note uses Theorem 4, Lemma 1 and Lemma 4
    correctly. Its statements do not contradict Theorem 3, which assumes
    rational input.
- **Numerical completeness.** "Complete" means that the floating Schnorr–Euchner
  enumeration finished on the clipped, congruence-normalized matrix; that the
  start threshold is `max(best elementary ratio, 10⁻⁶)`; and that the
  residual tolerance is `10⁻¹⁰`. §5, §8 and Limits state this adequately.
  Two additions are needed: the discarded `c2` flag (issue 9) and the
  Lemma A post-certificate (issue 2).
  - At my certified points the stored-point maximum differs from the
    clipped-matrix result by at most `7.6·10⁻⁷`.
  - The three "no vector" records are `bt_n10_p10_s0` root (integral to
    `5·10⁻⁹`) and `bt_n20_p16_s2` cut and trace. Their claim covers only
    ratios above `10⁻⁶`, as the note says. At the trace point,
    `max |x − round x| = 0.028`, so that point is not integral.
- **Support-1/2 changes within the triples extension.** At the 12 open
  families-only final points, support-1/2 splits with the best right-hand
  side have violations of at most `1.9·10⁻³`. They exceed `10⁻³` only at
  `bt_n50_p0_s0` (`1.87·10⁻³`) and `dm_LIN_t2_n60_p75_s0` (`1.08·10⁻³`), in
  both cases with `t ≈ ±2`, that is, the right-hand sides missing from
  (4.11)–(4.12). The support-3 violations there are 0.086–0.199. So triples
  dominate at these points, which supports the note's attribution. Isolating
  the effect would need a `dmfam` variant that keeps the original 1/2-index
  rules.
- **Unresolved linear DM60 optimum.** §9.1 handles it correctly. The Summary
  and §6 need the qualifier (issue 10).

## Checks run (by the reviewer)

All checks ran from `research-20261001/split-practice/` with
`OMP_NUM_THREADS=1` (and `OPENBLAS_NUM_THREADS=1` for the numeric scripts),
under `timeout`, with at most 4 of my processes at a time (including Gurobi child processes). These are targeted
checks of this stream only. No project-wide checks were run and CI was not
inspected. No process of mine is left running.

| Check | Command | Outcome |
| --- | --- | --- |
| Recompute §§6–10 and Summary from raw logs (own script, no stream imports) | `timeout 900 python3 reviews/r1-code/r1_tables.py` → `r1-logs/r1_tables.txt` | Exit 0. Matches the note except issues 3, 4, 10, 11 and 12. Confirmed: 748 stage records; 10 failed face solves (none at open instances); 27/180 inaccurate; 171 rank-1 integral; 16 non-rank-1; 12 open with gap 0.0117–1.0378%, ranks 9–39 (5–38 at `10⁻³`), second eigenvalue 0.374–7.44; root gap ratio median `1.07·10⁻⁹`, max `4.75·10⁻⁵`; all 187 de Meijer loops end with 0 violated cuts (max 19 rounds). BT10 closure 65.01% (`bt`) and 56.54% (`btfam`); per-`p` values as in the table; 2057/2688; supports 2–10, max coefficient 6, 91 of support ≤ 3; BT20 54.5/44.2%, 13 capped; rerun max difference 0.0. §8: 123 records, all three shards 41; classes 99/17/7; finished 83/13/7; times, medians, supports and Gurobi statuses as stated; 120 vectors re-evaluated exactly at the stored `Y`, max `|Δq| = 2.29·10⁻⁶`, no violation above `10⁻³` lost, all integer and inside the box; Theorem 3: 113 attempts, 2 errors, 111 values, 98/5/4 within `10⁻⁹` of `−¼`, 35 equal to `−0.25`, 7 of 109 sane, digits 59/307 and 772.5/1848. First-run comparison: 115 common points, family values identical, 2 ratio differences (0.000748, 0.000413), flags agree, 103 Theorem 3 values identical. §9 table, rounds, supports 24–49, coefficients ≤ 13, violation 0.031–0.172, 21/21 and 24/24 capped calls, 0.003784 and 0.002216 points, §9.1 percentages: all as stated. §10: 88 records, 80 finished, max deviation `1.15·10⁻¹⁶`, 13/16 and 7/8 unfinished, SCIP/Gurobi ratio 2.04–430.6, condition 24–4370, violations `5.7·10⁻⁵`–0.025. Load: 360 samples, 10.15–172.39, median 16.42, 90th percentile 103.06. |
| Independent certification of the normalized maxima at the stored points (Lemma A norm bound plus exhaustive enumeration; own code) | `timeout 1700 python3 reviews/r1-code/r1_bruteforce.py 2e8` → `r1-logs/r1_bruteforce.txt` | Exit 0. 110 records certified (no better split; max excess `7.6·10⁻⁷`), including 17 capped ones; 3 records with ratio 0 skipped; 10 skipped as too large. (A first attempt hung while estimating the work for very large `B`; I fixed my script and reran it. That partial run's output is overwritten.) |
| Independent rebuild of the X3C hard matrices (generator re-implemented, Theorem 1 formula) and exact rational enumeration of all violators (own code) | `timeout 500 python3 reviews/r1-code/r1_hard.py 5` → `r1-logs/r1_hard.txt` | Stopped by the timeout after 19 instances, as intended (exact enumeration is slow beyond `N = 14`). All 19, `q = 2..4` with both matrix kinds, match exactly: violator set equals Theorem 1(b), `min q` equals the prediction and the logged value, logged cover flags are correct, and no violator exists without a cover. The `q = 3, n = 9` planted instance has 2 covers, which confirms that the planted cover need not be unique. |
| Independent exact checks of Lemma A, Lemma B, Proposition C(c) and Proposition D (own code) | `timeout 900 python3 reviews/r1-code/r1_props.py` → `r1-logs/r1_props.txt` | Exit 0. Lemma A: 384 cases, 0 failures. Lemma B: 500 cases, 0 failures. Proposition D: 3470 instances, 0 mismatches. Signed box (`n ≤ 3`): 0 mismatches. Proposition C(c): `a = 1` at `D = 2, 3` (issue 5). |
| Short representatives at rank-1 roots (exact LLL via sympy; own code) | `timeout 600 python3 reviews/r1-code/r1_rank1_short.py 12` → `r1-logs/r1_rank1_short.txt` | Exit 0. 9/9 fractional rank-1 roots: coefficients ≤ 4, value at stored `Y` equal to `−0.250000` (issue 1). |
| Rerun of the stream's `exp_separate.analyse` on 3 points (stream code on purpose) | `timeout 900 python3 reviews/r1-code/r1_rerun_sep.py reviews/r1-logs/r1_rerun_sep.jsonl <bt_n10_p8_s0 root> <dm_LIN_t2_n30_p50_s0 cut> <dm_QUTO_t2_n30_p25_s0 root>` | Exit 0. Family values, normalized vector and ratio, completeness and Theorem 3 values identical to the logs. Gurobi statuses identical; time-limited incumbents differ slightly. The old crash point runs without error. |
| `sep_ratio` with a 10× node cap on the two dense DM60 points (stream code) | `timeout 1500 python3 reviews/r1-code/r1_dense_cap.py 2e8 <QUTO cut> <LIN cut>` → `r1-logs/r1_dense_cap.out` | Exit 0. Ratios 0.001629 and 0.001723 (logged: 0.001260 and 0.001388), still capped (issue 13). |
| Check of the `Y₀₀` congruence fix (inline Python) | not saved | At `dm_QUTO_t2_n30_p25_s0` root: after clipping, `Y₀₀ − 1 = 4.44·10⁻⁷`. Resetting the entry gives `λ_min = −2.0·10⁻⁷`, and Cholesky of `Y + 10⁻⁶·diag(0, 1, …)` fails. The congruence gives `Y₀₀ = 1`, `λ_min = −4.6·10⁻¹⁶`, and Cholesky succeeds. |
| Literature: de Meijer et al. v1 text; B–T preprint (`pdftotext` to `/tmp`); Letchford IPCO text; Herrmann text | `grep` and `sed` on `sources/` | §4 quotation, (4.10)–(4.12), the §6.4 rules (`10⁻³`, 5000 cuts, fewer than `n`), §7 sizes 60–120 and the Appendix A generators all match. B–T Table 2 GAP and STD ALL columns match the note exactly, as do problem (7), Algorithm 1, §6.1 and the §6.2 quotation. Letchford Prop. 3 (CVP, strongly NP-hard) matches, and the paper poses the separation question (issue 14). Herrmann's paper concerns linearly constrained IQP with general `Q`; no conflict. |
| Consistency with `binary-separation/note.md` | read Summary, Corollary 6 and the split-note corrections | No contradiction (issue 15). |

The note's own "Checks actually run" section lists its closeout commands and
the earlier producers adequately. I did not rerun `check_props.py` or
`test_lattice.py`; their saved outputs report 0 failures, and my own checks of
the same statements pass.
