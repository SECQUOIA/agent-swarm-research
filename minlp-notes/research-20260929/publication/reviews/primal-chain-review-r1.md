# Review of track primal-chain (r1)

Verdict: verified. Written to disk by the root from the reviewer's structured return value (the harness blocks subagents from writing report files).

## Summary

# Review of track primal-chain (round 1): exactly feasible points for chain50, chain100, chain200, chain400

Date: 2026-10-01. Reviewer: independent verifier. I did not produce these results, and I did not import, run or copy any of the track's scripts. My code and logs are in /workspace/minlp-notes/research-20260929/publication/reviews/primal-chain-r1/.

**Verdict: verified.** Every main claim is reproduced by my own exact code: exact feasibility, the objective enclosures, the gaps, the box files, R and the free indices. I found no blocker and no major issue. There are four minor issues; three concern display and wording, and one concerns process.

**About the report.** report.md does not exist at publication/primal/chain/report.md, because subagents could not write .md files. The track's summary text passed to me was cut off at "Every coor". I took the full text from the workflow transcript and saved it as logs/author_summary_from_transcript.txt. I reviewed all of it.

## 1. What I checked, with my own code

### 1.1 Exact feasibility and objective (rev_chain_exact.py)

**OSIL reader.** I wrote my own reader using xml.etree:
- every constant is kept as an exact Fraction;
- OSiL defaults are applied (variable lb 0, ub +inf; row bounds −inf/+inf);
- unknown sections, attributes and operators raise an error.

The model files are the cached OSIL files. Their sha256 hashes match the track's logs/osil_sha256.txt. The points files match logs/points_sha256.txt.

**Arithmetic.** My arithmetic differs from the track's:
- an element is a pair (p, q) meaning p + q√D, where D = disc is a rational (the track uses the integer R = num·den);
- sign tests compare p² with q²D;
- a row counts as holding with equality only if lhs − rhs has the representation (0, 0), which is sufficient for the real value 0;
- sqrt is not computed inside the field. Each sqrt node is matched to a precomputed candidate s_k = (t_k + 1/t_k)/2, and accepted only if s_k² equals the argument exactly and s_k ≥ 0. The nonnegative root is unique, so this is exact.

**Rebuilding the point.** I followed the generator's definition text: w, the 20-decimal t_i, α, β, the two roots of T² − αT + α/β (checked to be exact roots, both positive), u_i = (t_i − 1/t_i)/2, and x propagated from x_0 = 1.

**Results.** The same for all four N:
- all variables are continuous, and the only finite bounds are x1 = 1 and x_{N+1} = 3 (4 finite bounds), all exact;
- all rows hold exactly: 51/51, 101/101, 201/201 and 401/401;
- D is not a rational square;
- my R = num·den matches the generator's R, with 1,928, 3,755, 7,323 and 14,507 digits;
- the free indices are a = 1 and b = N−1. They are the argmin and argmax of t over the interior indices at the source point;
- t at the source point is 0.0827–0.0883 (a) and 34.55–36.35 (b).

**Objective and gaps.** I enclosed the objective with math.isqrt of num·den·10^140 and rounded outward to 40 decimals. L is the exact binary value of bnb.bound in open-instances-wave2/cops/logs/chainN_bound.json. That field equals the target, and the run has 0 unresolved boxes.

| N | objective, 40 dp (mine = track's) | L (exact double) | gap f_hi − L (up) | relative (up) |
|---|---|---|---|---|
| 50 | [5.0722614939828723164454381769845467731843, …44] | 5.07226149398286274561087338952347636222… | 9.58e-15 | 1.89e-15 |
| 100 | [5.0697846107387605574911913664186759056713, …14] | 5.06978461073875052989023970440030097961… | 1.01e-14 | 1.98e-15 |
| 200 | [5.0689173417931710001847965010674364416891, …92] | 5.06891734179316166830631118500605225563… | 9.34e-15 | 1.85e-15 |
| 400 | [5.0686216946040190143614896914450892607014, …15] | 5.06862169460400924236864739214070141315… | 9.78e-15 | 1.93e-15 |

**Track enclosures.** Using exact sign tests, I checked that the track's exact objective_enclosure and its 40-dp decimal enclosure each contain the exact objective. For every N, the decimal enclosure is identical to mine.

**Box files.** For every coordinate and every N, the exact coordinate lies in [centre − 1e-40, centre + 1e-40] (exact sign tests). Box names and indices match the OSIL variables.

**Run time.** Final run of all four N: 67 s, one process.

### 1.2 Negative controls of my own checker (rev_negative_controls.py, chain50)

- **Unaltered data:** passes.
- **Point perturbations (bound or row checks must fail):**
  - x_5 + 1e-30: row 4 fails.
  - u_5 + 1e-30: row 4 fails.
  - x_N + 1e-30: the ub of x51 fails.
- **Generator or box perturbations (the box check must fail):**
  - t_5 + 1e-20 in the generator: the free pair is solved again, so all rows still hold, but the box check fails as it should.
  - A box centre moved by 3e-40: the box check fails.
- **Root swap (t_a ↔ t_b):** because w_a = w_b = 2, this is a second exactly feasible point. Its objective is 6.3263…, so the root choice matters only for the objective. The generator records it ("smaller"), and the box check rejects the swapped point.
- **Objective decimal moved up by 1e-40:** the containment check reports False.

### 1.3 Side checks: evidence and consistency, not proof (rev_side_checks.py)

- **(a) Distance to the wave-2 double point,** measured against the exact doubles:
  - x: 2.04e-16, 1.76e-16, 1.95e-16, 2.25e-16;
  - u: 9.26e-16, 1.18e-15, 3.94e-15, 6.64e-16.
  - These match the track's build logs.
- **(b) SCIP 10.0 (pyscipopt 6.2.1) checkSol** at feastol 1e-12, with my own doubles of the exact point and nlobjvar set to the double of the upper enclosure: accepted for all four N. This is floating point, so it is evidence only.
- **(c) mpmath iv at 60 digits over the box files:**
  - every row enclosure contains its right-hand side;
  - the largest row width is about 4.0e-40, consistent with the track's half-width residual of 2.1e-40;
  - each objective enclosure contains the exact one.
  - This assumes mpmath iv rounds outward.

### 1.4 The dual bound L and the display claims

**Wave-2 code (chain_bound.py).** The test is `lb >= target`, where lb is an mpmath mpf and target is a Python float. mpmath compares against the exact binary value, and the returned bound = float(min(worst, target)) = target. So the certified L is the exact double, as the track says.

**COPS verifier (v_chain_bnb.py).** It also uses a float target, giving the same doubles. Its logged minimum leaf bounds are:
- chain50: 5.0722614939828627647…, below the displayed 5.072261493982863 and above the double;
- chain200: 5.0689173417931616736…, below the displayed 5.068917341793162 and above the double.

This confirms the track's note:
- the displays of chain50 and chain200 lie 2.54e-16 and 3.32e-16 above the certified doubles, and neither branch and bound certifies those decimals;
- the safe truncations 5.0722614939828627 and 5.0689173417931616 are ≤ L;
- the displays of chain100 (5.0697846107387505) and chain400 (5.068621694604009) are ≤ L;
- against the displayed chain400 value, the gap is 1.01e-14.

I did not recheck the wave-2 or COPS branch and bound themselves. Like the track, I take L as certified, re-certified by reviews/cops-verification Section 1f.

### 1.5 The math in the report

I re-derived the main formulas:
- x_N = 1 + η Σ w_i u_i, so x_N = 3 ⇔ Σ w_i u_i = 4N;
- length row ⇔ Σ w_i s_i = 8N;
- with t = u + s: 1/t = s − u, so Σ w t = 12N and Σ w/t = 4N;
- t_a + t_b = α, 1/t_a + 1/t_b = β, and t_a t_b = α/β.

All are correct.

Two side arguments:
- **"Why not a rational point".** The linear independence of square roots of distinct squarefree integers, together with positive weights, does force all s_i to be rational. The genus-1 remark is plausible (a plane cubic) but not proved. It is a side remark and does not affect any result.
- **Model description.** The OSIL files give η as 1e-2, 5e-3, 2.5e-3 and 1.25e-3. The exact row checks confirm η = 1/(2N).

### 1.6 How the report states its claims

The report separates the three kinds of claim plainly:
- **Proved by exact arithmetic:** feasibility and the objective enclosure.
- **Taken from earlier work:** L.
- **Consistency checks and evidence:** the iv box check and the SCIP check.

It correctly called its own check "separate code, not verified". With this review, the exact claims are now verified by independent code.

The report lists the commands it ran, and the logs in publication/primal/chain/logs/ match them.

## 2. Issues (all minor)

1. **Where the bad displays are.** The integration note places the too-precise displays of chain50 and chain200 in "the summary". The summary table shows "5.06862 … 5.07226", which is valid. The too-precise displays are in three places:
   - open-instances-wave2/cops/report.md, lines 19-22 and 173-176;
   - reviews/cops-verification/verification-report.md, lines 35-38 and 193-196;
   - reviews/closing-audit-a.md, line 132.

   The fix is correct (5.0722614939828627 and 5.0689173417931616) and should be applied in those documents and in the paper.
2. **Which L the gaps use.** The suggested gaps are measured against the exact doubles. Against the truncated displayed bounds, the gaps are 9.62e-15 (chain50), 1.01e-14 (chain100), 9.41e-15 (chain200) and 1.01e-14 (chain400), with relative gaps 1.90e-15, 1.99e-15, 1.86e-15 and 1.98e-15. The paper should say which L it uses, or use these values.
3. **Rounding of the u distance.** "within 3.9e-15 (u)" is rounded down: the largest value is 3.943e-15 (chain200), so it should read 4.0e-15. This is information only.
4. **Process and wording.** report.md is missing at its path, and the integration step must save the full text verbatim. "Equals MINLPLib's |p−d|/min(|p|,|d|)" is really an upper bound, since it uses f_hi in place of p. The minlplib.org pages I fetched do not state the formula; it is the project's convention, checked against metadata values in open-instances-scout/targets.md.

## 3. Commands run by the reviewer

All ran from publication/reviews/primal-chain-r1/, as one single-threaded process at a time (at most 1 core).

1. **Read-only inspection:**
   - the track folder, its scripts and logs;
   - the OSIL sections of chain50.osil;
   - open-instances-wave2/cops/chain_bound.py and the chainN_bound.json files;
   - reviews/cops-verification/v_chain_bnb.py and its chain logs;
   - grep for displayed bounds across the notes.
2. **`sha256sum` of the OSIL files and points/*.json:** both match the track's logs.
3. **`python3 rev_chain_exact.py 50`:** the first version wrongly compared two enclosures of different widths (a bug in my check). I replaced it with exact sign tests, and the rerun passed.
4. **`python3 rev_chain_exact.py 50 100 200 400`:**
   - background run, PID 135848, 33 s: all passed;
   - final rerun after adding a test hook that has no effect on normal runs: 67 s, all passed;
   - log: logs/rev_exact_all.log.
5. **`python3 rev_negative_controls.py`** (chain50), two versions; final output in logs/rev_negative_controls.log, with results as in 1.2.
6. **`python3 rev_side_checks.py 50 100 200`** (16.7 s) and **`python3 rev_side_checks.py 400`** (78 s): all passed. Logs: logs/rev_side_checks_*.log.
7. **One-off python:** gaps against the suggested truncated displays (logs/rev_gap_vs_display.log).
8. **Web, read-only:** WebFetch of minlplib.org instances.html, doc.html and index.html, to check the gap convention; no explicit formula found.
9. **Python extraction** of the track's full summary from the workflow transcript, saved to logs/author_summary_from_transcript.txt.

Software: Python 3.13.11, mpmath 1.3.0, pyscipopt 6.2.1 with SCIP 10.0. No project-wide checks were run, and nothing was committed.

## Issues

- **minor**: The integration note says that "the summary and the wave-2 report" display chain50 as 5.072261493982863 and chain200 as 5.068917341793162. The summary table does not show these decimals. It shows "5.06862 … 5.07226", and both of those values are valid bounds. The too-precise displays, each 2.54e-16 and 3.32e-16 above the certified doubles, appear in three places: open-instances-wave2/cops/report.md (lines 19-22 and 173-176), reviews/cops-verification/verification-report.md (lines 35-38 and 193-196, labelled 'certified'), and reviews/closing-audit-a.md (line 132). The fix is still correct: display chain50 as 5.0722614939828627 and chain200 as 5.0689173417931616. Apply it in those documents and in the paper.
- **minor**: The suggested gaps (9.58e-15, 1.01e-14, 9.34e-15, 9.78e-15) are measured against the exact binary doubles. If the paper shows the truncated bounds, a reader who subtracts the displayed numbers gets 9.62e-15 (chain50), 1.01e-14 (chain100), 9.41e-15 (chain200) and 1.01e-14 (chain400). The matching relative gaps are 1.90e-15, 1.99e-15, 1.86e-15 and 1.98e-15. The paper should say which L each gap uses, or report the gaps against the displayed values.
- **minor**: The report says the exact point lies 'within 2.3e-16 (x) and 3.9e-15 (u)' of the wave-2 double point. The largest u distance is 3.943e-15 (chain200), so 3.9e-15 is rounded down; it should read 4.0e-15. This is information only and does not affect any result.
- **minor**: Process: report.md does not exist at publication/primal/chain/report.md. The report text exists only in the track's structured summary. The copy passed to this reviewer was cut off at 'Every coor', so I took the full text from the workflow transcript and saved it as primal-chain-r1/logs/author_summary_from_transcript.txt. The integration step must save the full text verbatim. Separately, 'equals MINLPLib's |p−d|/min(|p|,|d|)' is an upper bound, not an equality, because it uses f_hi in place of p. The minlplib.org pages doc.html, index.html and instances.html do not state the formula; it is the project's convention, which open-instances-scout/targets.md checked against metadata values.

## Commands run

- `ls/cat/sed/grep read-only inspection of publication/primal/chain (scripts, logs, points), chain50.osil sections, open-instances-wave2/cops/chain_bound.py and chainN_bound.json, reviews/cops-verification/v_chain_bnb.py and logs, displayed-bound greps across notes`
- `sha256sum ~/.cache/minlplib/minlplib/osil/chain{50,100,200,400}.osil and points/*.json -> both match the track's logs`
- `python3 rev_chain_exact.py 50 -> first version had a reviewer bug (compared enclosures of different widths); fixed with exact sign tests; rerun passed`
- `setsid nohup python3 rev_chain_exact.py 50 100 200 400 (PID 135848, 33 s) -> all exact checks passed`
- `OMP_NUM_THREADS=1 python3 rev_chain_exact.py 50 100 200 400 (final, 67 s) -> all rows exact (51/101/201/401), 4 finite bounds exact, R matches, box contains point, objective decimals identical to track, gaps 9.58e-15/1.01e-14/9.34e-15/9.78e-15`
- `python3 rev_negative_controls.py (chain50, two versions) -> unaltered passes; x_5, u_5, x_N perturbations fail; generator/box perturbations fail the box check; root swap gives another feasible point with objective 6.326`
- `OMP_NUM_THREADS=1 python3 rev_side_checks.py 50 100 200 (16.7 s) and 400 (78 s) -> distances match track logs; SCIP checkSol (feastol 1e-12) accepts all; mpmath iv box rows contain RHS (width about 4e-40)`
- `python3 one-off: gaps vs suggested truncated displays -> 9.62e-15, 1.01e-14, 9.41e-15, 1.01e-14`
- `WebFetch minlplib.org instances.html, doc.html, index.html -> no explicit gap formula stated`
- `python3 extraction of the track's full StructuredOutput summary from the workflow transcript -> logs/author_summary_from_transcript.txt`
