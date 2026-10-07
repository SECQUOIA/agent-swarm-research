<!-- Written to disk by the root from the structured return value of verifier round 1 of track minlplib-status in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Review of track minlplib-status (round 1)

Reviewer: independent verifier, second agent in this role. The first agent was cut off by a usage limit; I checked and continued its work. All check code, logs and data are in `/workspace/minlp-notes/research-20260929/publication/reviews/minlplib-status-r1/` (`code/`, `logs/`, `dl/`, `conv/`, `PROGRESS.json`). No processes of mine are still running.

## Verdict

**Issues: one major issue and several minor ones.** Part A is confirmed independently. Most of Part B is confirmed independently, and three re-proofs on old model versions now have independent checks.

The major issue is that the author missed full model copies that sit in its own folder. The archived instance pages embed the complete GAMS listing. For topopt-cantilever_60x40_50 and nd_netgen-2000-3-4-b-a-ns_7, these copies remove the report's main caveats. The conclusions get stronger, but the report's statements about the evidence are wrong and must be corrected before the paper uses them.

## Major issue

### M1. The archived instance pages hold full model copies, which the report ignores

The 2018–2022 minlplib.org instance pages captured by the Internet Archive contain the full GAMS model between `<PRE>` and `</PRE>`. The author downloaded full pages (`pages/wayback/instpages/*.full.html`), but `wayback_pages.py` parsed only the part before `<PRE>`.

My checks (`code/pre_vs_gms.py`, which extracts and HTML-unescapes the listing and compares it with the current `.gms`):

- All 21 of the author's archived full pages from 2018-09-22/23 are **raw-identical** to today's `.gms` files (`logs/pre_vs_gms_all.log`). This covers glider100, ghg_3veh, topopt, methanol50, the four sssd instances, nuclear14, nd_netgen, watercontamination0303, the four smallinvDAX instances, eniplac, lop97icx, spring, stockcycle, rocket200 and rocket400.
- **topopt-cantilever_60x40_50**, from my own Wayback downloads:
  - 2018-09-22: full listing, 100,760 lines, identical to today's `.gms`.
  - 2020-01-11: full listing, identical.
  - 2022-05-22: this page already lists LINDO 35.35267044 dated 2022-02-15. The capture is cut at 1,048,576 bytes; its partial listing (1,039,258 characters, 23,478 lines) is an exact prefix of today's `.gms`.
  - Today's `.gms` has Last-Modified 2020-12-11 (HEAD request), and the OSIL 2019-06-25. Both dates are before the bound.
- **nd_netgen-2000-3-4-b-a-ns_7**: the full listings of 2018-09-23 (author's file), 2020-01-09 and 2022-05-22 (my downloads) are identical to today's `.gms`. They bracket the CPLEX and GUROBI bounds of 2022-02-16.

So these report statements are wrong or understated:

- topopt: "no copy at or before the bound exists ... Probably unchanged since 2019-06-25; this rests on file dates and is not proved".
- nd_netgen: "Unchanged since 2022-12-10; before that the evidence is file dates".
- Open issue: "No full model copy from 2018-2022 was found."

Suggested replacements:

- topopt: "identical full copies from 2018-09-22 and 2020-01-11; the 2022-05-22 copy, which already shows the LINDO bound, matches in its first 1 MiB; .gms and OSIL files were last modified before the bound date."
- nd_netgen: "bracketed by identical full copies of 2020-01-09 and 2022-05-22."

## Minor issues

1. **ghg_3veh constants.** The 2010 MINLPLib 1 file and the 2017 MINLPLib.jl file both write the factored form `-150000*(0.0181052631578947/x44 + 0.03458*x47 - 0.03458*x48)*x49/(...)`. GAMS 54.3 turns this into **3 distinct constants, 6 occurrences, 4 rows**:

   | Constant (old form) | Rows | Current value |
   |---|---|---|
   | 2715.789473684205 | e32, e39, e46 | 2715.7894736842 |
   | 376.0467809974723 | e113 (twice) | 376.046780997472 |
   | 28.34142857024601 | e113 | 28.341428570246 |

   - The report omits the third constant.
   - The per-constant relative difference is at most 1.84e-15. The report's "3.2e-15" is a row-value difference at random points.
   - The 2018-09-22 listing already equals today's file. So the text changed between 2017-11-23 and 2018-09-22, after both bounds (2013-09-26 and 2014-08-16) were computed.
   - The headline "no audited bound was computed on a model different from today's" should say "up to rounding of three constants in ghg_3veh".

2. **methanol50.** "The current OSIL differs from the .gms only in the objective constant" is wrong. An exact polynomial comparison (`code/poly_cmp.py`, `code/obj_delta.py`) finds 360 differing objective coefficients: the constant and 359 linear coefficients, each at most 2.4e-16 relative. All 1,497 constraint rows are identical rational functions (`code/rat_cmp.py`, exact). At p4 the .gms-form objective is higher by about 4.83e-16 (computed exactly). The margin is 9.8e-5, so the verdict is unaffected.

3. **catmix.** "0.045 is written 4.5000000000000005e-2" is true only for catmix100. The other three round different constants:

   | Instance | Exact constant | OSIL value |
   |---|---|---|
   | catmix200 | 9/400 | 0.022500000000000003 |
   | catmix400 | 9/800 | 0.011250000000000001 |
   | catmix800 | 9/1600 | 0.005625000000000001 |

   Each coefficient is off by 0.9e-16 to 1.8e-16 relative. The report's "1.6e-17 relative per row" is a row value at random points.

4. **lop97icx.** The objective coefficients differ by up to 2e-14 absolute and 1.36e-16 relative per coefficient, not "1.0e-17". At p2 the 2001 (.gms) form gives exactly 4099.0599536 and the cached OSIL gives 4099.0599536000000099. Both lie below the listed 4099.06. All 87 constraint rows are identical polynomials.

5. **MINLPLib.jl.** 9002dfa (2017-11-23) is the commit that first added `instances/minlp2`. It is not the repository's first commit: that is d2ba96c (2017-11-21), which already contains copies such as `instances/global/glider100.jl` and `instances/minlp/ghg_3veh.jl`. This does not change any verdict.

6. **"There are no captures before 2021-06."** This holds for the gms/osil files of the 69 instances only. The archive has model files of other instances from 2018-05. The archived instance pages are model copies from 2018 on (M1).

7. **Independence of the re-proofs.** The report says the re-proofs on old versions use the audit's verify.py. This review now provides independent checks (below); the integration step can cite them.

8. **Report preamble.** report.md starts with "report.md was not written ..." and "Status: partial". These are integration artifacts and should be removed.

## What I confirmed with independent code

### Part A (status refresh)

All of this agrees with the report.

- **Own re-fetch** (`code/vfetch.py`, `logs/vfetch.log`, 142 requests, all HTTP 200, 1 s delay; `code/vcompare.py`, `logs/vcompare.log`):
  - The 69 OSIL files are sha256-identical to `~/.cache/minlplib/minlplib/osil`.
  - The 69 page heads are byte-identical to the audit copies, and 39/39 to the scout copies.
  - `instances.html` and `minlplib.solu` are byte-identical to the audit copies.
  - The site footer still reads "Last updated: 2026-09-14, Git hash 9472b011".
- **GMS dates:** all 69 current `.gms` files fetched (`code/vfetch_gms.py`, `logs/gms_head.log`). Last-Modified is 2020-12-11 for 61 files. The other 8 carry their addition day: pricing050 2024-03-25, the six KAN instances 2025-05-07, ann_cumene_tanh 2021-11-29.
- **OSIL file dates:** in the cache, 1,466 of 1,632 OSIL files are dated 2019-06-25, and each of the other 166 carries its instance's addition day from dates.html.
- **bounddates.html:** the newest entry for these instances is nd_netgen p2 (2026-07-03). The page states "Removals are not documented."
- **dates.html:** flowchan50/100/200/400 were removed on 2015-02-09 with "Bug in original GAMS model had been found, fixed version available as flowchan*fix".
- **MAGO 2014 slides:** "No way to verify correctness of bound!" is on slide 23/35 (PDF page 41).

### Part B (model identity)

- **Scope:** the audit's `results.csv` has 15 class (i), 4 class (i-r) and 4 emfl (ii)-proven instances. With the 43 paper instances and rocket100/200/400 that makes 69, as the report says.
- **Wayback model files** (`dl/wayback_digest_check.json`): 149 distinct HTTP-200 captures of 57 instances.
  - 135 have a CDX SHA-1 digest equal to the current file.
  - The other 14 are exactly the author's "prefix" set. I downloaded three (eg_disc2_s osil 2021-08-02, nd_netgen osil 2024-12-10, topopt gms 2022-06-25); each is an exact 1 MiB prefix of the current file.
  - None of the 69 instances has a gms/osil capture before 2021-06.
  - The gamsworld.org MINLPLib 2 captures from 2014-04 cover only clay0304h. The earliest listing and statistics pages are from 2014-12-09, as the report says.
- **Old files against current, through GAMS 54.3 Convert** (`code/conv.sh`, `code/osil_eval_cmp.py`, 60-digit evaluation at random points; numerical evidence):
  - Identical OSIL: glider100 (2004), methanol50, nuclear14, eniplac, stockcycle and catmix100 (2001).
  - lop97icx: identical OSIL. Its scalar differences are only 899 `.prior` lines and `prioropt`.
  - spring, rocket100, rocket200 and rocket400 (2001): rows equal at 60 digits.
  - ghg_3veh: differs only in rows e32, e39, e46 and e113, at ≤1.9e-15 relative.
- **2017 MINLPLib.jl copies against the cached OSIL**, with my own JuMP evaluator that does not use GAMS (`code/jl_cmp.py`, `logs/jl_cmp_small.log`, `logs/jl_cmp_batch.log`):
  - All 57 copies agree with the author's verdicts.
  - The sssd, smallinvDAX, spring, rocket, nuclear14, glider100, emfl, waterno2 and other instances are identical at 50 digits (bounds and types too).
  - ghg_3veh differs in 4 rows at ≤2.9e-15. The catmix family differs at ~1e-17 (OSIL rounding).
  - lukvle10 matches only when `(a)^2^b` is read as `sqr(a)**b`. Read literally in Julia it would mean a^(2^b). The author disclosed this writer quirk.
  - watercontamination0303 was checked exactly (`code/jl_lin_cmp.py`): all 108,217 linear rows and the 4,657-term objective are identical, as are the variable bounds and types.
- **Statistics:** I fetched the 2014-12-09 `allinstancedata.html` myself (`dl/stats2014.json`). For the 55 of the 69 instances present then, every structural count equals today's: nvars, ncons, nbin, nint, nz, nlnz, Jacobian and Hessian counts, and objective sense. Only constraint-class counts were reclassified (pindyck, glider100, ghg_3veh, eniplac, rocket100/200/400), with constant sums.
- **OSIL against GMS for all 69 instances** (`logs/osil_gms_batch.log`): only catmix100–800, methanol50 (objective only) and lop97icx (objective only) differ. All other instances are equal at 60 digits.
- **PrincetonLib files are different models:**

  | Instance | PrincetonLib (2006) | Current |
  |---|---|---|
  | dtoc5 | 10,000 variables | 100,000 |
  | optcdeg2 | 1,203 | 150,003 |
  | hvycrash | 203 (1 fixed) | 202 |

- **Archived pages, audited bounds:** the 2018 pages list the 2013–2015 audited bounds with the same values and dates as today. The 2022 bounds (methanol50, nuclear14, topopt, nd_netgen) were added later.
- **No missed public history:** GitHub has no public MINLPLib repository. msakai/minlplib2-pb (2015, pure binary) and MINLPLib.jq (2019) add no pre-2018 copies of these instances.

### Independent checks of the re-proofs on old versions

1. **ghg_3veh**, interval proof (`code/tri_proof.py`, `code/perturb.py`; `logs/ghg_proof_old.log`, `logs/ghg_proof_cur.log`).
   - **Method:** the 58 equalities are triangular. Each one defines a continuous variable linearly, so forward substitution in outward-rounded mpmath interval arithmetic proves that a real, exactly feasible point exists. All inequalities and bounds are then checked over the enclosures, and integrality exactly.
   - **The listed p2 is not usable as is:** it violates e9, e18, e25 and e27 by up to 7e-15.
   - **Perturbed point:** moving 11 free variables by at most 1.6e-10 gives a proved feasible point on both the 2010 form and the current OSIL.
   - **Result:** the objective is 7.754006050100459 (2010 form) and 7.754006050100454 (current), with enclosure width below 1e-56. Both lie below the ANTIGONE/BARON bound 7.7543245 by 3.18e-4. Class (i) holds on the old form.
2. **lop97icx**, exact check (`code/exact_feas.py`).
   - p2 is exactly feasible in rational arithmetic on both the cached OSIL and the 2001 form: bounds, integrality and all 87 rows hold.
   - The objective is 4099.0599536000000099 on the cached OSIL and 4099.0599536 on the 2001 form. Both are below 4099.06.
3. **methanol50**, exact argument. All 1,497 constraint rows of the 2001 form equal the cached OSIL exactly as rational functions. At p4 the objective differs by +4.83e-16. The audit's OSIL-form verdict (margin 9.8e-5) therefore carries over.
4. **smallinvDAX upper bounds:** the 2017 copies set the integer upper bound to 1e20 (+inf), the same as today. The proving points have integer values of at most 47 and 63.

## Not checked

- The page copies the report calls "review copies (34)".
- The "constraint-class reclassified" labels in snapshots other than 2014-12-09.
- Archived statistics other than 2014-12-09.

## Commands run (this review; results above)

1. **Predecessor's transcript:** parsed with python. Its downloads (`dl/`), conversions (`conv/`) and code were reused after checking. I reran `python3 code/vcompare.py`: identical, as above.
2. **CDX analysis** of the stored CDX JSON and text files, with python:
   - gms/osil captures of the 69 instances: none before 2021-06;
   - gamsworld minlplib2 captures: listing and statistics pages from 2014-12-09;
   - digest comparison: 135 identical, 14 prefix.
3. **Capture downloads**, `curl https://web.archive.org/web/<ts>id_/...` with 1 s delay: three model-file prefixes (all exact 1 MiB prefixes); topopt pages 2018-09-22, 2020-01-11 and 2022-05-22; nd_netgen page 2022-05-22; 2014-12-09 allinstancedata.html.
4. **Listing comparisons:** `python3 code/pre_vs_gms.py` on 21 author pages and on my downloads; all identical, and the 2022 topopt listing is a prefix.
5. **ghg_3veh proof:** `python3 code/perturb.py` and `python3 code/tri_proof.py` on `conv/ghg_3veh.old/out.osil` and the cached OSIL: PROVED for both.
6. **Old against current conversions:** `python3 code/osil_eval_cmp.py` for rocket100, spring, methanol50, lop97icx, ghg_3veh and nuclear14; rocket200 and rocket400 after fetching the 2001 GLOBALLib files from GitHub raw and converting them with `code/conv.sh`.
7. **Current .gms files:** `setsid nohup python3 code/vfetch_gms.py` (PID 915935, `logs/vfetch_gms.log`), 69 files with sha256 and SHA-1; then HEAD requests for 21 files (`logs/gms_head.log`).
8. **jl comparisons:** `python3 code/jl_cmp.py` on 10 instances, then `code/run_jl_batch.sh` (PID 918729, `logs/jl_cmp_batch.log`, 47 instances; watercontamination0303 timed out at 1,500 s). Re-done with `python3 code/jl_lin_cmp.py` (exact, 9.5 s). The lukvle10 recheck used a `sqr(a)**b` rewrite.
9. **OSIL against GMS:** `code/run_osil_gms_batch.sh` (PID 922319, `logs/osil_gms_batch.log`, 64 instances; the other 5 were done by the predecessor).
10. **Exact comparisons:** `python3 code/poly_cmp.py`, `code/rat_cmp.py`, `code/obj_delta.py` and `code/exact_feas.py` on methanol50, lop97icx and the catmix family.
11. **dates.html and bounddates.html** text checks (python).
12. **GitHub API** repository search (curl).
13. **PrincetonLib headers** (sed).
14. **MINLPLib.jl history:** `git log` and `git ls-tree` in the author's clone.

At most 2 cores were used at any time. Nothing was committed and nobody was contacted.