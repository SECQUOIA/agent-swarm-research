# Verifier group A: primal/chain and primal/lnts

Date: 2026-10-03. Paths below are relative to `research-20260929/` unless they start with `P/` (= `research-20260929/publication/`).
Independent scripts and logs: `P/reviews/minor-fixes-review-r1/scratch-A/` (chain_gaps.py/.log, lnts_check.py/.log, extra_checks.py/.log, lnts_repro/).
None of my scripts import track code, except the lnts_repro rerun, which runs a copy of the track's own `lnts_primal.py` to test reproducibility.

## Summary of problems

| # | track | severity | problem |
|---|---|---|---|
| A1 | lnts (lead check 2) | major | The main-summary primal display for lnts100, 0.5545954011669, is **below** the exact point's objective (f_lo = 0.5545954011669111610017828) by 1.12e-14. It is not a valid upper bound. The report's Section 6 claims that the displayed primal values "remain valid upper bounds". The other three displays are valid. Location: `P/primal/lnts/report.md:83`; the integration list should also correct `open-instances-summary.md:18` (suggested display 0.5545954011670). |
| A2 | chain (lead check 1) | major | The main-summary chain gap "≤ 1.0e-14" is false for the exact chain100 point: f_hi − L = 1.00276e-14 against the exact binary64 L. For chain400 the gap is 9.77e-15 against the exact L but 1.01e-14 against the displayed 5.068621694604009. summary.md's integration list does not tell the integrator to change "≤ 1.0e-14". It says only "no main-table range correction" and lists the safe-display gaps. Location: `P/reviews/minor-fixes/summary.md:13,25`; `open-instances-summary.md:33`. Suggested fix: add "change the chain gap to ≤ 1.01e-14", or give the per-instance gaps. The chain report's own suggested edit (report.md:154) already gives 1.01e-14 for chain100. |
| A3 | lnts | minor | Two of the four "verifier duals" used in the report (Section 1) and the integration note are nearest-rounded 16-digit displays of the certified value N·h2 (`mpmath.nstr(N*h2, 16)` in `reviews/open-instances-verification/v_lnts.py:210`), and they lie above it. lnts100: 0.5545954011663566 exceeds N·h2 = 0.5545954011663565656 by 3.44e-17. lnts200: 0.5545770161025291 exceeds 0.55457701610252909504 by 4.96e-18. The printing error of h2 is at most 5e-20, so these differences are real. The gaps do not change at 3 significant digits (f_hi − N·h2 = 5.546e-13 for all four, still ≤ 5.55e-13). The report nevertheless calls these "the full value" of a certified bound. Location: `P/primal/lnts/report.md:17,19,114`. Suggested fix: call them nearest-rounded displays, or use N·h2 rounded down (0.5545954011663565, 0.5545770161025290). |
| A4 | lnts issue 2 | minor | Now that the full report text is on disk, its argument against a fully rational point (Section 3, "Not possible") is incomplete. "cos θ is transcendental for rational nonzero θ" does not exclude a rational value of Σ w_j cos θ_j, and it ignores θ_j = 0. The claim is true, and the r1 review gives a correct proof based on linear independence (Lindemann–Weierstrass). Location: `P/primal/lnts/report.md:57`. |
| A5 | lnts issue 4 / integration | minor | Rounding conventions are inconsistent. Section 1 now says that displayed gaps are rounded upward. However, "5.5e-13" (Section 1, the integration cell and the main summary) is the exact 5.546e-13–5.547e-13 rounded to nearest. At two digits, rounding up gives 5.6e-13; at three digits, the report's own 5.55e-13. Similarly, "5.8e-13 to 6.2e-13" begins above the true lower value 5.789e-13. The response row "3.25e-15–3.54e-15" also rounds 3.5437e-15 down; the body's "within 3.6e-15" is valid. |
| A6 | chain issue 1 | minor | The list of occurrences of the overly rounded displays is not complete. Besides the three named documents, `P/reviews/solver-campaign-review-r1.md:43` ("certified lower bound 5.072261493982863") and `P/solver-runs/report.prev.md:39` ("our certified bound 5.072261493982863") present the display as certified. `P/reproduction/README.md:144,146` and `P/reproduction/cops/report.md` also display it, but with an explicit caveat. In addition, `reviews/cops-verification/verification-report.md:35-38` is a bullet list, not a table; the report says "two tables". |
| A7 | lnts collateral | minor | `logs/lnts_primal_50_100_200_400.json` and `logs/run_all.stdout` were produced by the pre-change script and are now stale. Their zero_enclosure_widths and obj_width come from the invalid step. The report does not say so, and Section 7 (Files) lists neither minor_review_check.py nor its log. My rerun of the changed script reproduces the four point files byte for byte (see lnts issue 1), so only the logs are stale. |

## primal/chain (review P/reviews/primal-chain-review-r1.md)

### Issue 1: location of the overly rounded displays. Verdict: OK, with minor note A6
- I ran grep over all .md/.tex files. The three named documents contain the displays: `open-instances-wave2/cops/report.md:19,21,173,175` (two tables); `reviews/cops-verification/verification-report.md:35,37` (list) and `:193,195` (table); `reviews/closing-audit-a.md:132`.
- The main summary (`open-instances-summary.md:33`) shows "5.06862 … 5.07226". Both values lie below the exact binary64 L of chain400 (5.068621694604009242…) and chain50 (5.072261493982862745…), so the range is a valid display of the dual bounds. There is no paper .tex file in the repository yet.
- From the stored binary64 values, both displays lie above L: 5.072261493982863 − L50 = 2.544e-16 and 5.068917341793162 − L200 = 3.317e-16. This matches the report.
- The safe displays 5.0722614939828627 and 5.0689173417931616 are truncations of the exact L to 17 significant digits. Both are ≤ L, by 4.56e-17 and 6.83e-17.
- The L column in the report table matches the exact binary expansions to all printed digits (extra_checks.log).
- The integration cell in summary.md (row 25) is correct apart from A6. It names the paper as well.

### Issue 2: which dual the gaps use. Verdict: OK
I computed the gaps myself (chain_gaps.py) as f_hi minus the display, using exact Fractions and rounding up to 3 significant digits:
- absolute gaps: 9.62e-15, 1.01e-14, 9.41e-15, 1.01e-14;
- relative gaps: 1.90e-15, 1.99e-15, 1.86e-15, 1.98e-15. They are the same whether I divide by the display or by L.

Against the exact L, the gaps are 9.58e-15, 1.01e-14, 9.34e-15, 9.78e-15 (relative 1.89e-15, 1.98e-15, 1.85e-15, 1.93e-15), as in the table. All four displays used (including chain100 5.0697846107387505 and chain400 5.068621694604009) are ≤ L. The body text, the response row and summary.md rows 13 and 26 agree. For the related integration gap, see A2.

### Issue 3: u-distance. Verdict: OK
I compared the box centres (radius 1e-40) with the exact binary64 values in `open-instances-wave2/cops/logs/chainN_primal.txt`:
- max|du| = 9.263e-16, 1.1758e-15, **3.9432e-15** (chain200) and 6.635e-16, so 4.0e-15 is a valid upper display;
- max|dx| = 2.039e-16, 1.762e-16, 1.951e-16 and 2.248e-16, so 2.3e-16 is valid.

### Issue 4: missing report and relative-gap wording. Verdict: OK
- The report is on disk and complete, including its commands.
- The gap wording now reads "upper bound on the project's relative-gap convention … uses f_hi". This is correct: with d = L < p, min(|p|, |d|) = L, and (f_hi − L)/L ≥ (p − L)/L.
- Citing review r1 is accurate: r1's verdict is "verified" for exact feasibility, objective and gaps.

## primal/lnts (review P/reviews/primal-lnts-review-r1.md)

### Issue 1: invalid second Krawczyk step. Verdict: OK
- **The code change** (`P/primal/lnts/lnts_primal.py:301-302`) sets `Y2 = [iv.mpf(v.mid) for v in Z]` and computes `K2 = krawczyk(thfix_iv, Y2, Z)`.
- **The point y2 lies in Z.** In mpmath 1.3.0, `.mid` is `mpf_shift(mpf_add(a, b, prec, round_nearest), -1)`, a thin interval. Because rounding is monotone and 2a, 2b are representable, fl(a + b)/2 ∈ [a, b]. So y2 ∈ Z always, even though `lnts_primal.py` does not assert it. The author's check does assert it.
- **The mean-value argument holds.** `krawczyk(·, y, X)` evaluates F at y and F' over its third argument, now Z. For a zero z* ∈ Z and y ∈ Z, the segment [y, z*] lies in the box Z. So z* = y − C F(y) + (I − C J̄)(z* − y) with J̄ ∈ F'(Z), and z* ∈ K(Z). C is the inverse of mid F'(Z), and any real matrix is valid there. `meet` (lines 222-228) takes the maximum of the lower ends and the minimum of the upper ends, which is the correct intersection.
- **The author's recheck is real.** `minor_review_check.py` and its log rebuild X from the stored boxes and redo step 1. They report that the old centre is not in Z for all four boxes, and they assert y2 ⊂ Z, max width < 2.1e-106 (largest 2.0894e-106, lnts400 θ_N), objective width < 3e-109 (largest 2.164e-109) and N·h(Z2) ⊂ stored objective enclosure. The script reuses the track's `krawczyk`, so it is not independent.
- **My independent check** (lnts_check.py) uses my own closed-form F = (50h Σw cos − 45, 50h Σw sin, 25h² Σ b_j sin θ_j − 5). The coefficients b_j are checked against the exact recursion with random rationals. The Jacobian is hand-written, the Krawczyk step is my own, and step 2 is centred at the exact rational midpoint of Z1. Results:
  - step 1 passes for all four instances, and the stored centre is not in Z1;
  - step-2 widths are at most 2.15e-108, 1.16e-107, 4.58e-107 and 1.80e-106 (all < 2.1e-106);
  - objective widths are 2.7e-110, 4.9e-110, 9.2e-110 and 1.73e-109 (all < 3e-109);
  - Z2 lies inside the stored box, and N·h(Z2) lies inside the stored 25-digit objective enclosure, for all four.
- **Rerun of the changed script.** I ran a copy of the changed `lnts_primal.py` in scratch-A/lnts_repro (5.6 s). It reproduces all four point files byte for byte. Its widths equal the author's minor_review_check.log values exactly. The 25-digit displays are therefore unchanged, as claimed.
- **Report text.** Section 3 now describes the valid step correctly. The summary.md cell ("None; gaps and displayed enclosures are unchanged") is correct.

### Issue 2: missing report. Verdict: OK, with minor note A4
- The report is on disk and lists commands, including the lnts_primal, crosscheck, jacobian_check and mutation_test runs and the old-vector comparison.
- The interval assumption (mpmath iv outward rounding) is stated.
- The integration cell (remove lnts50–400 from the sentence at open-instances-summary.md:43-46) is correct.

### Issue 3: missing old-vector comparison script. Verdict: OK, with a rounding nit (A5)
- The comparison is saved in `minor_review_check.py`.
- My own computation uses the exact binary64 old values and the stored 60-digit enclosures. The upper distances are 3.2546e-15, 3.4513e-15, 3.5434e-15 and 3.5437e-15.
- In each instance exactly one coordinate rounds differently: the middle control x26/x51/x101/x201, whose old value is 0.

### Issue 4: relative-gap rounding. Verdict: OK, with minor note A5
- Section 1 now states upward rounding to 3 significant digits.
- All table entries match my exact recomputation:
  - against the summary duals: 5.79e-13 (1.05e-12), 6.12e-13 (1.11e-12), 5.84e-13 (1.06e-12), 5.88e-13 (1.06e-12);
  - against the 16-digit verifier duals: 5.55e-13 (1.01e-12, 1.00e-12, 1.00e-12, 1.01e-12).
- The exact absolute gaps against the summary duals are 5.789e-13–6.112e-13, against the verifier duals 5.5456e-13–5.5470e-13, and against the certified N·h2 5.546e-13 for all four.
- The integration cell's "about 5.8e-13–6.2e-13" and "5.5e-13 against full verifier duals" are right as approximations; see A3 and A5.

### Issue 5: tiny middle control. Verdict: OK
- The stored middle controls are −3.839e-112, 8.212e-112, −3.009e-112 and 6.197e-112. All are below 1e-110 in absolute value, and they are the only controls below 1e-50.
- Keeping them is correct, because changing them would define a different point.
- The explanation (rounding a numerical tangent-law solve to 40 digits) matches the code (TH_DIGITS = 40) and review r1.

### Lead check 2 (lnts displays in the main summary)
- **Primal displays** (open-instances-summary.md:17-20) compared with f_hi:
  - lnts50 0.5546687649387: +2.11e-14, valid.
  - **lnts100 0.5545954011669: −1.116e-14, invalid (A1).** Suggested display: 0.5545954011670.
  - lnts200 0.5545770161031: +1.63e-14, valid.
  - lnts400 0.5545724137007: +1.29e-14, valid.
  - Fix: correct `P/primal/lnts/report.md` Section 6, first bullet (it says "(e.g. 0.5546687649387) remain valid upper bounds"), and add the lnts100 display correction to the summary.md integration list. In the old double vector, the lnts100 objective (0.5545954011669111) was already above the display, so the display was never a valid upper bound.
- **Dual displays** 0.5546687649381, 0.5545954011663, 0.5545770161025 and 0.5545724137001 lie below the certified N·h2 by 2.42e-14, 5.66e-14, 2.91e-14 and 3.25e-14. All are valid. The certified duals are mpmath values N·h2, not binary64. The 16-digit "bound" strings happen to equal Python repr of a double, but the certificate is N·h2 (see A3).

## Collateral (diff of before/ against current report)

**chain**, 9 hunks:
- Status line, gap wording, integration note, u-distance, independence paragraph and suggested summary edit: all explained by issues 1–4.
- "Open issues" was replaced by "Remaining limitations": the obsolete items (missing report.md, not verified, summary display) were removed correctly, and the L-not-rechecked and Q(√R) limitations were kept.
- No numbers changed except 3.9e-15 → 4.0e-15. No links broke: `../../reviews/primal-chain-review-r1.md` exists.
- The statement "Wave-2 gaps … measured against the displayed decimal bounds" is unchanged and harmless.
- Nits: A6 ("two tables").

**lnts**, 5 hunks:
- Section 1 rounding sentence, middle-control paragraph, Section 3 second step, commands bullet, open-issues independence bullet and response table: all explained.
- The new claim "independent review r1 … including an integer-only enclosure of sin and cos" is true: r1's verify_no_mpmath.py uses Taylor remainder bounds.
- Stale or unsupported statements: Section 6's "remain valid upper bounds" (A1, pre-existing and unchanged, but it contradicts the data), the stale logs (A7) and the Section 3 "Not possible" argument (A4).
- Section 4's "widest is 7.7e-107" still holds with the new code: the new maximum row width is 7.64e-107.

## Commands run (exact)

All from `/workspace/minlp-notes/research-20260929` (R) or `P/reviews/minor-fixes-review-r1` (W); one process at a time.

1. `cat BRIEF.md; ls -la` (W); `cat PROGRESS.json; ls reviews/minor-fixes; grep -n -i -E "chain|lnts" reviews/minor-fixes/summary.md; ls primal/chain primal/lnts …` (P)
2. `cat reviews/primal-chain-review-r1.md`, `cat primal/chain/report.md; diff -u reviews/minor-fixes/before/primal__chain.txt primal/chain/report.md` (P)
3. `cat primal/chain/minor_review_check.py logs/minor_review_check.log; grep dist logs/build_*.log`
4. Inspection of the box/primal/bound JSON formats with `head -c` and `python3 -c` one-liners.
5. `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B scratch-A/chain_gaps.py 2>&1 | tee scratch-A/chain_gaps.log` (W)
6. `grep -rn -E "5\.07226149398286(3|27)|5\.06891734179316(2|16)" --include=*.md . ; grep -n chain open-instances-summary.md` (R); `sed -n` of closing-audit-a.md 128-138, reproduction/README.md 136-150, reproduction/cops/report.md 88-98
7. `python3 -B -c '<exact f_hi − L for chain50..400 vs 1e-14>'; sed -n 28,48p open-instances-summary.md` (R)
8. `python3 -c '<print issues.json rows for chain/lnts>'; grep -n -i -E "chain|lnts" commands.md` (reviews/minor-fixes)
9. `cat reviews/primal-lnts-review-r1.md; cat primal/lnts/report.md; diff -u reviews/minor-fixes/before/primal__lnts.txt primal/lnts/report.md` (P)
10. `git diff -- lnts_primal.py; grep -n "def krawczyk" -A 40 lnts_primal.py; cat minor_review_check.py logs/minor_review_check.log; sed -n 195-340p lnts_primal.py` (primal/lnts)
11. `grep -n "def mid" … mpmath/ctx_iv.py; grep -n "def mpi_mid" -A8 mpmath/libmp/libmpi.py`
12. `grep -o '<var [^>]*>' ~/.cache/minlplib/minlplib/osil/lnts50.osil | …` (OSIL names skip x256)
13. `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B scratch-A/lnts_check.py 2>&1 | tee scratch-A/lnts_check.log` (W; the first run stopped at my own wrong assertion of the h variable name, which I fixed with sed; the second run passed, 0.7 s)
14. `grep -n "h2\|bound" reviews/open-instances-verification/v_lnts.py; python3 -c '<print lnts_verify.json>'` (R)
15. `cp lnts_primal.py osil_iv.py scratch-A/lnts_repro/; cd scratch-A/lnts_repro && OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B lnts_primal.py 50 100 200 400 > logs/run_all.stdout; cmp points/lnts{N}_point.json <track>/points/…` (identical for all four; 5.6 s); python one-liner comparing new and old log widths
16. `OMP_NUM_THREADS=1 python3 -B scratch-A/extra_checks.py | tee scratch-A/extra_checks.log` (W)
17. `grep -rln "5.072261493982863\|5.068917341793162" --include=*.tex --include=*.md .` (R)

No track files were edited, and nothing was committed. The only process with a construction-like role was the 5.6 s rerun of the lnts point construction on a scratch copy. No solver runs.
