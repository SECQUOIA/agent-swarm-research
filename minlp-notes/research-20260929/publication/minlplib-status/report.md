<!-- Written to disk by the root from the structured return value of fixer round 1 of track minlplib-status in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# MINLPLib status refresh and model-identity history (track minlplib-status)

Revised 2026-10-03 after review round 2. Output folder: `/workspace/minlp-notes/research-20260929/publication/minlplib-status/`. Data are in `data/`, logs in `logs/` and code at the top level. The review response sections list each issue and its resolution.

## Main findings

- **Part A (status refresh): nothing has changed** since the copies the September 29 work used. There are no new or changed bounds or points, no changed solved marks and no changed model files.
- **Part B (model identity): no audited bound was computed on a model different from today's, except for the rounding of three constants in ghg_3veh.**
  - In ghg_3veh the three constants differ by at most 1.84e-15 relative.
  - Class (i) still holds on the old ghg_3veh text.
- **The three priority instances:**
  - glider100: unchanged since at least 2004.
  - ghg_3veh: the same model up to the rounding of the three constants; the text was rewritten between 2017-11-23 and 2018-09-22, after both flagged bounds.
  - topopt-cantilever_60x40_50: unchanged. Complete identical copies exist from 2018-09-22 and 2020-01-11. A copy from 2022-05-22 already shows the flagged LINDO bound; the archive cut it at 1 MiB, and its first 23,479 lines are identical to today's file.
- **Side finding (exact):** the MINLPLib OSIL files of catmix100–800, methanol50 and lop97icx differ slightly from the .gms text, by double-precision rounding of some coefficients (relative error at most 2.4e-16 per coefficient). The audit and the certificates use the OSIL numbers.

## Part A: status refresh

All fetches ran on 2026-10-02 between 02:51 and 03:16 UTC (`fetch_current.py`, `compare_current.py`). The site footer still reads "Last updated: 2026-09-14, Git hash 9472b011".

- **Scope:** 69 instances. These are the 43 paper instances, 15 class (i), 4 class (i-r) and 4 emfl audit instances, and rocket100/200/400. That made 207 requests, all HTTP 200, sent one at a time with a 1 s delay.
- **Instance pages** (the part before the GAMS listing) are byte-identical to every stored copy:
  - the audit copies of 2026-09-30 (69);
  - the scout copies of 2026-09-29 (39);
  - the review copies (34).
- **instances.html** (listing, S marks, listing bounds) and **minlplib.solu** are byte-identical to the audit copies.
- **Parsed contents:** points, infeasibilities, dates and per-solver dual bounds are equal to `bound-audit/pages.json` (69/69) and to `open-instances-scout/fetched.json` (39/39).
- **OSIL files:** all 69 current OSIL files are sha256-identical to `~/.cache/minlplib/minlplib/osil`.
- **File dates:**
  - OSIL Last-Modified is 2019-06-25 for 61 of the 69 files. The other 8 are pricing050 (2024-03-25), the six KAN instances (2025-05-07) and ann_cumene_tanh (2021-11-29). In the whole cache, 1,466 of 1,632 OSIL files are dated 2019-06-25; each of the other 166 is dated with its instance's addition day.
  - GMS Last-Modified is 2020-12-11 for 61 of the 69 files. The other 8 carry their addition day: pricing050 2024-03-25, the KAN instances 2025-05-07 and ann_cumene_tanh 2021-11-29.
- **bounddates.html:** the newest entry for these instances is nd_netgen-2000-3-4-b-a-ns_7 p2 (2026-07-03), which the audit already used. The page states "Removals are not documented."

The per-instance table is Table A in `data/tables.md`.

The round 1 review re-fetched everything with its own code and confirmed all of Part A.

## Part B: model identity

### Sources

- **GAMS World archive** (now github.com/GAMS-dev/gamsworld): GLOBALLib and MINLPLib 1 scalar files converted 2001–2010, dated by their GAMS Convert header.
- **MINLPLib.jl** (github.com/lanl-ansi/MINLPLib.jl):
  - Commit 9002dfa (2017-11-23) first added `instances/minlp2`, the MINLPLib 2 copies (1,513 files).
  - The repository's first commit is d2ba96c (2017-11-21). It holds older collections in 15 directories, including GLOBALLib as `global`, MINLPLib 1 as `minlp` and PrincetonLib as `prince`, but no MINLPLib 2 copies.
  - I translated the `minlp2` files back to GAMS with `jl2gms.py`. This accounts for two quirks of the converter, which I inferred myself:
    - integer lower bounds of 0 are omitted, and +inf is written as 1e20;
    - GAMS `sqr(a)**b` is printed as `(a)^2^b`. This affects lukvle10 only.
- **Archived instance pages, new in this revision:**
  - Every minlplib.org instance page embeds the full .gms model between `<PRE>` and `</PRE>`. Internet Archive captures of these pages are therefore dated, complete model copies.
  - For these instances, captures start on 2018-09-22.
- **Internet Archive model files:**
  - For the 69 instances, the first .gms or .osil capture is from 2021-06. Every capture of these files is byte-identical to the current file or a 1 or 5 MiB prefix of it, cut by the archive; none differs.
  - The archive does hold model files of other instances from 2018-05-29 on (faclay75). Its `.lp` and `.pip` captures precede its `.gms` capture that day. The faclay75 instance page was captured on 2018-05-26; it embeds the .gms listing.
- **Archived statistics pages** from 2014-12-09, 2015-06-08, 2016-03-08, 2017-11-14, 2019-06-23, 2019-10-21, 2020-02-19, 2024-03-15 and 2024-11-14, and old change logs.
- **OSIL file dates** (see Part A). They are evidence, not proof.

### Method

1. **Conversion** (`history.py`, `osil_compare.py`): GAMS 54.3 Convert turns each archived file and the current .gms into a scalar GAMS model and an OSiL file.
   - Text check: equal scalar text means GAMS reads both files as the same model.
   - Semantic check against the current MINLPLib OSIL: variables, types and bounds are compared exactly as rationals. Rows written differently are evaluated with mpmath at 50 digits at 6 random points. This part is evidence, not proof; any difference it reports is real.
2. **Archived listings** (`archived_listings.py`, new):
   - For each of the 22 Part B instances (class (i), class (i-r), rocket100/200/400), the script reads the CDX index of `minlplib.org/<name>.html`.
   - It selects three captures: the earliest, the last one on or before the latest flagged bound date, and the first one after that date.
   - It downloads them raw (`id_`), one at a time with at least 1.2 s delay.
   - It extracts the listing (tags removed, HTML-unescaped) and compares it with today's .gms: "identical" for equal text apart from leading or trailing newlines; "prefix" for a capture cut off before `</PRE>` whose complete lines equal the start of today's file. Throughout this report, listing identity uses this newline convention and does not mean byte identity.
   - It also records which dual bounds the page listed at that time.
3. **Exact comparisons without GAMS** (`exact_forms.py`, `ghg_constants.py`, `obj_shift_bound.py`, new):
   - Both the .gms text and the MINLPLib OSIL are read with every decimal taken as the exact rational it denotes.
   - Each row and the objective are expanded into exact rational functions (these instances use only `+ - * /` and `sqr`).
   - Rows are compared as rational functions, and coefficients one by one.
   - Control runs on spring and nuclear14 report all rows and the objective identical, as expected (`logs/exact_forms_controls.log`).

### Table B1: audited instances (supersedes Table B1 in `data/tables.md`)

Abbreviations used in the table:
- "listing" is the archived instance page's embedded .gms;
- "jl 2017" is the MINLPLib.jl copy of 2017-11-23;
- "stats" means the archived statistics pages: all structural counts are equal to today's; only constraint-class counts were reclassified.

Every listing in the table is identical to today's .gms apart from leading or trailing newlines unless it says otherwise (`logs/archived_listings.log`).

| instance | flagged dual bounds (date) | copies dated before the bound | copies dated after the bound | verdict |
|---|---|---|---|---|
| glider100 | LINDO, COUENNE −1255.058601 (2014-08-16, 2015-06-25) | GLOBALLib 2004-04-20 (identical GAMS text) | jl 2017 (same); listing 2018-09-22 | unchanged |
| topopt-cantilever_60x40_50 | LINDO 35.35267044 (2022-02-15) | listings 2018-09-22 and 2020-01-11 (complete, 100,760 lines) | listing 2022-05-22, which already shows the LINDO bound; cut at 1 MiB; its 23,479 complete lines equal the start of today's file | unchanged |
| methanol50 | LINDO 0.00802826 (2022-02-15) | GLOBALLib 2001-07-24 (identical GAMS text); listings 2018-09-23 and 2020-01-09 | listing 2022-05-23, which shows the bound | unchanged |
| nuclear14 | LINDO −1.12965944 (2022-02-15) | MINLPLib 1 2001-04-27 (identical GAMS text); listings 2018-09-23 and 2020-01-10 | listing 2022-05-23, which shows the bound | unchanged |
| nd_netgen-2000-3-4-b-a-ns_7 | CPLEX 10729659.03, GUROBI 10729661.15 (2022-02-16) | listings 2018-09-23 and 2020-01-09 (complete, 21,626 lines) | listing 2022-05-22, which shows both bounds; .gms capture 2022-12-10 (byte-identical) | unchanged |
| ghg_3veh | ANTIGONE, BARON 7.7543245 (2013-09-26, 2014-08-16) | MINLPLib 1 2010-08-05 | jl 2017, which has the same text as 2010; listing 2018-09-22 | same up to the rounding of 3 constants (≤ 1.84e-15 relative); class (i) holds on the old text |
| sssd20-04persp, sssd22-08persp, sssd25-04persp, sssd25-08persp | LINDO 347716.8909, 508748.972, 300186.8048, 472098.947 (2014-03-02) | none (added 2014-02-24) | stats 2014-12-09; jl 2017 (same); listings 2018-09-22/23 | unchanged from 2014-12 (stats) and 2017-11 (full model); 2014-03 to 2014-12 not covered |
| watercontamination0303 | BONMIN 207.9850352, LINDO 207.9850353 (2014-02-28) | none (added 2014-02-21) | stats 2014-12-09; jl 2017 (same, checked exactly by the review); listing 2018-09-22 (242,580 lines) | as sssd |
| smallinvDAXr1b150-165, r2b150-165, r1b200-220, r2b200-220 | LINDO 88.1049355, 88.1049355, 156.604269, 156.604269 (2014-02-28) | none (added 2014-02-26) | stats 2014-12-09; jl 2017 (same); listings 2018-09-22/23 | as sssd |
| eniplac | COUENNE, LINDO, SCIP −132117 (2013-09-17) | MINLPLib 1 2001-08-08 (identical GAMS text) | jl 2017; listing 2018-09-23 | unchanged |
| lop97icx | ANTIGONE 4099.06 (2013-09-17) | MINLPLib 1 2001-06-25: same model as today's .gms; it also set branching priorities, now removed | jl 2017; listing 2018-09-22 | unchanged |
| spring | ANTIGONE, BARON, COUENNE, LINDO, SCIP 0.84624567 (2013-09-17) | MINLPLib 1 2001-04-27 (same; term order differs) | jl 2017; listing 2018-09-22 | unchanged |
| stockcycle | ANTIGONE, BARON, COUENNE 119949 (2013-09-17) | MINLPLib 1 2001-04-18 (identical GAMS text) | jl 2017; listing 2018-09-22 | unchanged |
| rocket100 | LINDO −1.0128319 (2018-05-23) | GLOBALLib 2001-07-31 (same); jl 2017 (same) | listing 2018-09-23 | unchanged |
| rocket200 | LINDO −1.01283563 (2015-03-08) | GLOBALLib 2001-07-31 (same) | jl 2017; listing 2018-09-23 | unchanged |
| rocket400 | LINDO −1.01283634 (2017-09-13) | GLOBALLib 2001-07-31 (same) | jl 2017; listing 2018-09-22 | unchanged |

More on the table:

- **Statistics.** Every archived snapshot has the same structural counts as today: from 2014-12-09 on, and from 2019-06-23 on for topopt and nd_netgen, which were added on 2018-08-18.
- **Captures checked.** I checked 30 captures in all, and every complete listing is identical to today's .gms apart from leading or trailing newlines.
- **Bounds on the archived pages.**
  - The 2018 pages already list the flagged 2013–2018 bounds, with the same values and dates as today.
  - The pages captured in 2020-01 do not yet list the four 2022 bounds; the pages captured in 2022-05 do.

### Details for selected instances

- **topopt-cantilever_60x40_50.**
  - Identical complete copies exist from 2018-09-22 and 2020-01-11.
  - The 2022-05-22 copy already lists LINDO 35.35267044 (2022-02-15). The archive stored only its first 1,048,576 bytes; the complete lines of its listing (23,479 of 100,760 lines; 1,039,259 characters) equal the start of today's file.
  - There is no capture between 2020-01-11 and 2022-05-22.
  - Today's .gms was last modified on 2020-12-11 and the OSIL on 2019-06-25, both before the bound.
  - The model is unchanged. This rests on the copies on both sides of the bound date and on the file dates.
- **nd_netgen-2000-3-4-b-a-ns_7.** Identical complete copies exist from 2018-09-23 and 2020-01-09 (before the bounds) and from 2022-05-22 (after; this page lists the CPLEX and GUROBI bounds of 2022-02-16). A .gms capture of 2022-12-10 is byte-identical. The model is unchanged.
- **ghg_3veh.**
  - The 2010 MINLPLib 1 file and the 2017 MINLPLib.jl copy write factored products. Today's file writes the expanded products as rounded decimals. This gives 3 distinct constants in 6 places across 4 rows (`ghg_constants.py`, exact Fractions):

    | old factored form | exact product | written today | rows (occurrences) | relative difference |
    |---|---|---|---|---|
    | `150000*(0.0181052631578947/x + …)` | 2715.789473684205 | 2715.7894736842 | e32, e39, e46 (1 each) | 1.84e-15 |
    | `11.34*(33.1610917987189 - x95)` | 376.046780997472326 | 376.046780997472 | e113 (2) | 8.67e-16 |
    | `0.854659090909091*(33.1610917987189 - x95)` | 28.34142857024600834… | 28.341428570246 | e113 (1) | 2.94e-16 |

  - The other factored products (for example 150000·0.03458 = 5187) expand without rounding.
  - The 2018-09-22 listing already equals today's file. So the text changed after the MINLPLib.jl copy (committed 2017-11-23) and before 2018-09-22, which is after both flagged bounds (2013-09-26, 2014-08-16). The bounds were therefore computed on the factored text.
  - The audit's proof re-run on both old versions with the audit's `verify.py` (`verify_archived.py`) gives an objective in [7.754006050048, 7.754006050065]. Both bounds are invalid by 3.18e-4, so class (i) holds.
  - The round 1 review checked this independently with an outward-rounded interval proof on a nearby perturbed point. It got 7.754006050100459 on the 2010 text and 7.754006050100454 on today's OSIL, both below 7.7543245.
- **methanol50.**
  - The 2001 GLOBALLib file gives the same GAMS text as today's .gms.
  - Today's MINLPLib OSIL is not the same as the .gms text (see the side finding). All 1,497 constraint rows are identical rational functions. The objective differs in 360 of its 635 expanded coefficients (the constant, 104 linear and 255 quadratic ones), by at most 1e-15 absolute and 2.38e-16 relative per coefficient.
  - GAMS 54.3's own OSiL rendering of the .gms has exactly the .gms objective (`logs/methanol50_gams_osil.log`). So the earlier re-proof on that rendering is a proof on the .gms model. It used the audit's `verify.py`, gave the enclosure [0.007930218791205, 0.007930218793331] and a margin of 9.80e-5: class (i).
  - In addition, an exact argument without GAMS:
    - At p4, the .gms objective exceeds the OSIL objective by 4.83e-16 (exact).
    - On the box p4 ± 1, the difference is at most 3.2e-15 (`obj_shift_bound.py`, exact).
    - The audit's proved point lies in that box: its Newton polish moved variables by at most 7.4e-13, and its Krawczyk radius is 1e-12·max(1, |x|) (`bound-audit/logs/verify/methanol50.p4.json`).
- **lop97icx.**
  - The 2001 file and today's .gms define the same model; the old file also set branching priorities, which do not affect feasibility or the objective.
  - All 87 constraint rows of the .gms text and the MINLPLib OSIL are identical polynomials (exact). The objective differs in 30 of 967 coefficients (18 linear, 12 quadratic), by at most 2e-14 absolute and 1.36e-16 relative.
  - At p2, which the audit's exact route A shows is exactly feasible, the objective is exactly 4099.0599536 on the .gms form and 4099.059953600000099 on the OSIL form. Both are below the listed 4099.06, so the audit's (i-r) verdict holds on both forms.
- **sssd\*persp, watercontamination0303, smallinvDAX\*.** These were added a few days before their bounds, so no earlier copy exists. The earliest full model copies are from 2017-11-23 (MINLPLib.jl) and 2018-09-22/23 (listings), and both match today's. The earliest statistics (2014-12-09) are equal. March to December 2014 is not covered.
  - For smallinvDAX, the integer variables have no explicit upper bound: the old GAMS default was 100, today's is +inf. The 2017 copies already use +inf. The proving points have integer values of at most 47 and 63, so the verdict holds either way.
- **rocket100/200/400.** The 2001 GLOBALLib files and the 2017 copies define the same model as today, and the 2018-09 listings are identical. rocket100's bound (2018-05-23) is bracketed by the 2017-11-23 copy and the 2018-09-23 listing.

### Other 47 instances (paper and emfl)

- Every archived predecessor defines the same model as today (Table B2 of `data/tables.md`).
- The GAMS World PrincetonLib files named dtoc5 and optcdeg2 have smaller dimensions than today's instances. Its hvycrash file uses a different formulation; equivalence was not checked:

  | instance | PrincetonLib (2006) | current |
  |---|---|---|
  | dtoc5 | 9,999 variables (10,000 with the objective variable) | 99,999 (100,000) |
  | optcdeg2 | 1,202 (1,203) | 150,002 (150,003) |
  | hvycrash | 203 variables; 51 in [0.005, 6.2881854]; one extra variable fixed at 0.005 | 202 variables; 51 in [0, 6.2831854] |

  Comparing hvycrash bounds as multisets, both endpoints of 51 variable bounds are shifted by exactly 0.005 in PrincetonLib, and it has one extra variable fixed at 0.005. All other bound multiplicities agree. Matching variables by name gives a misleading count because the numbering differs. This comparison does not establish whether the formulations are equivalent. hvycrash's 2017 copy matches today's.
- The KAN instances, pricing050 and ann_cumene_tanh are newer than any archive; their file dates equal their addition days.
- I did not check archived listings for these 47 instances; Part B's scope is the audited instances.

### MINLPLib practice

- `dates.html` records only additions and removals. The flowchan models are the clearest case of a buggy model being removed and replaced under a new name: they were removed on 2015-02-09 with the note "Bug in original GAMS model had been found, fixed version available as flowchan*fix".
- Vigerske's MAGO 2014 slides (slide 23 of 35, PDF page 41) say the dual bounds came from ANTIGONE, BARON, Couenne, Lindo and SCIP, with "No way to verify correctness of bound!".

## Side finding: the OSIL form and the .gms form differ by rounding (exact)

MINLPLib's OSIL files expand products of constants in double precision. `exact_forms.py` compares the .gms text and the MINLPLib OSIL with exact rational arithmetic. Five instance families differ:

| instance | coefficients that differ | exact value (.gms) → OSIL value | relative error per coefficient | rows |
|---|---|---|---|---|
| catmix100 | 200 (2 in each of 100 rows) | 0.045 (9/200) → 0.045000000000000005 | 1.11e-16 | 100 of 200 differ; objective identical |
| catmix200 | 400 | 0.0225 (9/400) → 0.022500000000000003 | 1.33e-16 | 200 of 400 differ |
| catmix400 | 800 | 0.01125 (9/800) → 0.011250000000000001 | 0.89e-16 | 400 of 800 differ |
| catmix800 | 1,600 | 0.005625 (9/1600) → 0.005625000000000001 | 1.78e-16 | 800 of 1,600 differ |
| methanol50 | 360 objective coefficients (constant, 104 linear, 255 quadratic) | e.g. 5.01625659 → 5.016256589999999 | ≤ 2.38e-16 (≤ 1e-15 absolute) | all 1,497 rows identical |
| lop97icx | 30 objective coefficients (18 linear, 12 quadratic) | e.g. 11.2897376 → 11.289737599999999 | ≤ 1.36e-16 (≤ 2e-14 absolute) | all 87 rows identical |

The other 64 instances have the same model in both forms: GAMS 54.3 conversion plus 60-digit evaluation in history.py, confirmed by the review's batch. The audit and the certificates use the OSIL numbers. The paper should say so. The catmix certificates were not re-run on the .gms form.

## What is proved and what is not

- **Exact under the stated reading of the files:**
  - GAMS-text identities (as GAMS 54.3 reads the files).
  - Listing identities (exact text equality of the HTML-unescaped archived listing with today's .gms apart from leading or trailing newlines).
  - The `exact_forms.py`, `ghg_constants.py` and `obj_shift_bound.py` results, which use decimals as exact rationals, no GAMS and no floating point.
- **Documentary evidence:** a listing shows what minlplib.org published on the capture date. That a solver ran on exactly that file at the bound date is inferred from copies on both sides of the date. For topopt it is also supported by the file dates; the 2022-05-22 copy covers only the first 23,479 of 100,760 lines.
- **Numerical evidence:** row equality at sample points (history.py, used for the 64 other instances and the older copies).
- **Proofs on old versions:**
  - ghg_3veh (both old texts) and methanol50 (the .gms form) were re-proved with the audit's own `verify.py`. That is the audit's code, not an independent check.
  - Independent checks exist from the round 1 review: an interval proof for ghg_3veh on the 2010 text and on today's OSIL; an exact rational feasibility check of lop97icx p2 on the 2001 text; exact constraint identity and the exact objective shift for methanol50.
  - My `exact_forms.py` comparisons are independent of GAMS and of the audit code.
- **Not covered:** for sssd\*persp, watercontamination0303 and smallinvDAX\*, March to December 2014.

## Revision after review round 1 (2026-10-02)

1. **M1 (major): the archived instance pages hold full model copies.** I agree.
   - What I did:
     - Wrote and ran `archived_listings.py` for all 22 Part B instances: 30 captures, including 9 newly downloaded bracketing captures and rocket100's earliest capture after a fresh CDX query.
     - Every complete listing is identical to today's .gms apart from leading or trailing newlines. topopt's 2022-05-22 capture is a matching 1 MiB prefix.
   - Report changes:
     - Replaced "no copy at or before the bound exists … rests on file dates" (topopt) with the bracketing copies.
     - Replaced "Unchanged since 2022-12-10; before that the evidence is file dates" (nd_netgen) with "bracketed by identical complete copies of 2020-01-09 and 2022-05-22".
     - Removed the open issue "No full model copy from 2018-2022 was found".
     - Added the listing copies to Table B1 for all 22 instances. They also bracket the 2022 bounds of methanol50 and nuclear14.
   - My counts match the review's, except that I count 23,479 complete lines and 1,039,259 characters in the cut topopt capture where the review gives 23,478 lines and 1,039,258 characters. The difference is in how the last complete line is counted.
2. **ghg_3veh constants.** I agree.
   - `ghg_constants.py` confirms 3 constants in 6 places across 4 rows, with exact relative differences 1.84e-15, 8.67e-16 and 2.94e-16. The table above gives the details.
   - Added that the text changed between 2017-11-23 and 2018-09-22, after both bounds.
   - Qualified the headline: "except for the rounding of three constants in ghg_3veh".
3. **methanol50.** I agree that "differs only in the objective constant" was wrong; corrected.
   - The exact comparison finds 360 differing objective coefficients and all 1,497 rows identical.
   - The review says these are "the constant and 359 linear coefficients". My exact count by degree is 1 constant, 104 linear and 255 quadratic (`logs/exact_forms_degrees.log`). For example, the coefficient of x260² is 1.38384e-05 in the .gms and 1.3838400000000001e-05 in the OSIL. The totals agree.
   - Added the exact shift at p4 (+4.83e-16), the bound of 3.2e-15 on p4 ± 1, and the fact that GAMS 54.3's rendering keeps the exact .gms objective.
4. **catmix.** I agree. The constants now read 0.045, 0.0225, 0.01125 and 0.005625, with per-coefficient errors from 0.89e-16 to 1.78e-16. These are measured exactly, replacing the sample-point row measure.
5. **lop97icx.** I agree: 30 objective coefficients, at most 2e-14 absolute and 1.36e-16 relative, all 87 rows identical.
   - One correction to the review: at p2 the OSIL value is 4099.059953600000099, not 4099.0599536000000099. The review's figure has one zero too many; the difference from the .gms value 4099.0599536 is 9.9e-14. The audit's route A enclosure (`results.csv`) shows the same digits. Both values are below 4099.06.
6. **MINLPLib.jl first commit.** I agree. 9002dfa (2017-11-23) is the commit that first added `instances/minlp2`; the first commit is d2ba96c (2017-11-21), checked with `git log` and `git ls-tree`.
7. **Internet Archive statement.** I agree. It is now limited to the 69 instances' .gms and .osil files. Model files of other instances exist from 2018-05-29 (faclay75, from the stored CDX lists), and archived pages for the 69 instances embed model listings from 2018-09-22 on. The faclay75 instance page was captured earlier, on 2018-05-26.
8. **Independence and preamble.** The integration preamble ("report.md was not written …", "Status: partial") is gone. The report now cites the review's independent checks and states which checks use the audit's `verify.py`. It adds my own exact comparisons that use neither GAMS nor floating point.

`data/tables.md` (from round 0) was not regenerated. Its Table B1 "archived versions" column lacks the listing copies and says "none found" for topopt and nd_netgen. Table B1 in this report supersedes its Table B1; a notice at the stale table directs readers here.

## Files

- **New code:** `archived_listings.py`, `ghg_constants.py`, `exact_forms.py`, `obj_shift_bound.py`.
- **New data:** `data/archived_listings.json`, `data/exact_forms.json`.
- **New logs:**
  - `logs/archived_listings.log`, `logs/ghg_constants.log`;
  - `logs/exact_forms.log`, `logs/exact_forms_2.log`, `logs/exact_forms_3.log`, `logs/exact_forms_controls.log`, `logs/exact_forms_degrees.log`;
  - `logs/obj_shift_bound.log`, `logs/methanol50_gams_osil.log`.
- **New downloads** (git-ignored `pages/`): `pages/wayback/instpages/*.full.html`.
- **Round 0 files**, unchanged: `fetch_current.py`, `compare_current.py`, `history.py`, `osil_compare.py`, `jl2gms.py`, `stats_history.py`, `verify_archived.py`, `wayback_*.py`, `bounddates.py`, `make_tables.py`, `data/*.json`. Table B1 in `data/tables.md` now carries a supersession notice.
- **Progress file:** `PROGRESS.json`.
- **Round 2 evidence check:** `minor_review_check.py`, `logs/minor_review_check.log`.

## Commands run

### Revision after review round 2 (2026-10-03)

- `python3 minor_review_check.py > logs/minor_review_check.log`: passed. The script limits itself and its children to two CPU cores and runs checks sequentially using stored evidence, without network requests. It runs the reviewer's `code/spotchecks.py` and `code/listing_check.py` (all 30 stored captures), loads `code/hvy_bounds.py` with `runpy.run_path`, checks the 0.005 shifts with exact fractions against this track's current .gms, and reads the stored faclay75 CDX entries.
- The script also runs `git log --reverse --format='%h %ad %s' --date=short` and `git ls-tree --name-only d2ba96c instances/` in `pages/sources/MINLPLib.jl`.
- `git diff --check -- research-20260929/publication/minlplib-status/`: passed after the edits.

These were targeted local checks. No project-wide verification was run, and CI was not consulted.

### Revision (2026-10-02)

All commands ran in the foreground, one process at a time. There were no background jobs and none are left running.

1. `timeout 580 python3 archived_listings.py | tee logs/archived_listings.log`
   - Sent 10 requests to web.archive.org, one at a time with at least 1.2 s delay: 1 CDX query (rocket100) and 9 page captures.
   - Checked 30 captures: all complete listings identical, topopt 2022-05-22 a prefix.
2. `python3 ghg_constants.py | tee logs/ghg_constants.log`: 3 constants, 6 places, 4 rows.
3. `python3 exact_forms.py catmix100`: test run.
4. `python3 exact_forms.py > logs/exact_forms.log`: the catmix results are complete. The run stopped at methanol50's point evaluation (KeyError 'x2'), because variables missing from the `.sol` file were not set to 0 as MINLPLib specifies. I fixed this.
5. `python3 exact_forms.py methanol50 lop97icx > logs/exact_forms_2.log` and `python3 exact_forms.py catmix100 catmix200 catmix400 catmix800 > logs/exact_forms_3.log`: results as above; `data/exact_forms.json` holds all six.
6. Control runs of `exact_forms.compare`:
   - spring and nuclear14: all rows and the objective identical (`logs/exact_forms_controls.log`).
   - stockcycle and ex6_2_5 were not usable: an assertion in the objective extraction for stockcycle, and an unsupported `log` for ex6_2_5.
7. Degree count of the differing objective coefficients (`logs/exact_forms_degrees.log`); comparison of methanol50's GAMS 54.3 OSIL with the exact .gms objective (`logs/methanol50_gams_osil.log`: no difference).
8. `python3 obj_shift_bound.py | tee logs/obj_shift_bound.log`: |Δ| ≤ 3.2e-15 (methanol50) and ≤ 4.8e-13 (lop97icx) on p ± 1.
9. Read `bound-audit/logs/verify/methanol50.p4.json`: max_move 7.4e-13, Krawczyk rho 1e-12.
10. `git log --reverse` and `git ls-tree` (d2ba96c, de0a263, 9002dfa) in `pages/sources/MINLPLib.jl`.
11. `awk` on the stored CDX prefix lists: the first model-file capture of any instance is 2018-05-29.

### Round 0

- `curl` (1 s delay) of minlplib.org index.html, dates.html, bounddates.html, doc.html, download.html, statistics.html, instances.html, minlplib.solu and instancedata.csv, plus HEAD requests: all 200.
- `python3 fetch_current.py --budget 540`: 207 requests, all 200.
- `python3 compare_current.py`: all identical.
- Internet Archive CDX queries with curl (1 s delay). The first attempts returned empty answers or "Temporarily Offline"; later attempts succeeded.
- `python3 wayback_files.py` (17 captures), `python3 wayback_meta.py`.
- `git clone --filter=blob:none` of GAMS-dev/gamsworld (sparse) and lanl-ansi/MINLPLib.jl.
- `python3 stats_history.py`.
- GAMS 54.3 convert test runs.
- `history.py`: development runs, then the authoritative final run `setsid nohup … history.py` (PID 213959, EXIT=0).
- `python3 verify_archived.py`: 4 re-proofs, all proved.
- `python3 wayback_pages.py` (three runs), `python3 bounddates.py`, `python3 make_tables.py`.
- WebSearch and WebFetch of the MAGO 2014 slides.
- Edit of `/workspace/minlp-notes/.gitignore`: added the `pages/` line, as permitted.

**Round 0 incident:** I mistook a wrapper PID for a job PID and started a duplicate history.py run. For about 2 minutes two processes ran, above the 1-process budget. I killed the duplicate (PID 201304). All results come from the later single-process run.

Nothing was committed and nobody was contacted.

## Open issues

- **catmix100–800:** the certificates and the audit use the OSIL numbers, which differ from the .gms text by at most 1.78e-16 relative in half of the rows. The catmix certificates were not re-run on the .gms form, and the paper should state which form is certified.
- **sssd\*persp, watercontamination0303, smallinvDAX\*:** no model copy or statistics exist for 2014-02-28 to 2014-12-09.
- **topopt-cantilever_60x40_50:** there is no capture between 2020-01-11 and 2022-05-22, and the 2022-05-22 copy covers only the first 23,479 lines. The file dates (.gms 2020-12-11, OSIL 2019-06-25) cover the rest.
- **`data/tables.md`:** not regenerated; its Table B1 is marked as superseded by Table B1 in this report.

## Response to review round 2

All four minor findings were confirmed before editing. `minor_review_check.py` records the checks in `logs/minor_review_check.log`. There is no disagreement with the review, and no audit or certificate verdict changes.

1. **OSIL file dates:** corrected to 61 of 69 files dated 2019-06-25, with 8 exceptions, confirmed from `data/part_a.json`.
2. **MINLPLib.jl first commit:** corrected to 15 older collections, including `global`, `minlp` and `prince`, with no `minlp2`, confirmed from the tree of d2ba96c (2017-11-21).
3. **hvycrash:** replaced the name-based count of 167 with the bound-multiset comparison: PrincetonLib has 203 variables against 202 today, 51 variable bounds have both endpoints shifted by exactly 0.005, and one extra variable is fixed at 0.005. Equivalence was not checked; the report describes a different formulation without claiming a different model.
4. **Listing equality and archive dates:** qualified listing equality to allow leading or trailing newlines. The 29 complete captures each have one extra trailing newline; the cut topopt capture remains a matching prefix. Corrected the faclay75 statement: its `.lp` and `.pip` captures precede its `.gms` capture on 2018-05-29, and its instance page was captured on 2018-05-26. Also marked the stale Table B1 in `data/tables.md` as superseded by this report's Table B1.
