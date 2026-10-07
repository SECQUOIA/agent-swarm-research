"""One-time document response to integration r1; edits only owned files."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
paths = [BASE/'open-instances-summary.md', BASE/'bound-audit/audit-report.md', BASE/'publication/READINESS.md']
before = OUT/'review-r1-before'
before.mkdir(exist_ok=True)
for p in paths:
    dest = before/p.name
    assert not dest.exists(), 'One-time edit: snapshot already exists'
    dest.write_bytes(p.read_bytes())
s, a, r = [p.read_text() for p in paths]
def replace(text, old, new, count=1):
    assert text.count(old) == count, (old, text.count(old), count)
    return text.replace(old,new)

s = replace(s, 'Updated 2026-10-03:', 'Updated 2026-10-04: integration-review corrections;')
s = replace(s, '|---|---|---|\n\n\n| lnts50', '|---|---|---|\n| lnts50')
s = replace(s, 'lnts (the displayed summary duals), chain (the safe individual dual displays),',
            'lnts, dtoc5, lukvle10, pindyck and the three eg_* rows (their displayed\nduals), chain (the safe individual dual displays),')
s = replace(s, 'for the remaining leaves.\n', 'for the remaining leaves.\n\nThe eg_disc_s display 5.760539610694994 is 2.4e-16 above the certifier\'s\nbinary64 bound; it is valid because the independent retry review certified\nevery leaf against this exact decimal, under the same A1/A2 assumptions.\n')
s = replace(s, 'Göß–Burlacu–Martín', 'Göß–Burlacu–Martin')
s = replace(s, 'Göß 2026 PARA displays a zero percentage gap.', 'Göß 2026 PARA prints a 0.00% gap (below 0.005%).', 2)
s = replace(s, 'Göß 2026 PARA displays a small nonzero gap.', 'Göß 2026 PARA prints a 0.01% gap.')
s = replace(s, 'on the DTOC5 source.', 'on the source model (h·y², M = 600–1000).')
s = replace(s, '| camshape100 | Octeract solved', '| camshape100 | Already solved globally in floating point. Octeract solved')
s = replace(s, '| camshape800 | MINOTAUR claimed', '| camshape800 | Prior global claim false (rigorously for the MINLPLib model; for the rounded QPLIB copy, strong evidence, not proof). MINOTAUR claimed')
s = replace(s, '| eg_int_s | SCIP 8.1 solved', '| eg_int_s | Already solved globally in floating point. SCIP 8.1 solved')
s = replace(s, 'Local CUTEst value and nonclosing solver bounds only.', 'Local CUTEst value and nonclosing solver bounds only; the SIF SOLTN value is a tolerance artifact.')
s = replace(s, 'OSIL coefficients differ slightly from GAMS coefficients. | [control](publication/literature/control/report.md) |',
            'OSIL coefficients differ slightly from GAMS coefficients. | [control](publication/literature/control/report.md); [coefficient check](publication/minlplib-status/report.md) |', 4)
s = replace(s, 'the solution value was already listed.', 'the SIF file already records the value −0.21850.')
s = replace(s, 'CAMINO’s Gurobi optimality claims are refuted; recorded termination status and cause are unknown.',
            "CAMINO's Gurobi 13.0.0 optimality claim is refuted by a feasible point; the data do not record Gurobi's termination status, and the cause is unknown.", 2)
s = replace(s, 'polar/rectangular coefficient rounding prevents unproved exact bound transport. Prior rigorous ACOPF work (Oustry et al.) concerns different models.',
            'the polar and rectangular files differ by coefficient rounding, so a rigorous bound cannot be transferred between them without a perturbation argument. Ours is the first rigorous certificate found for this MINLPLib model. Prior certified ACOPF work (Oustry et al.) concerns different models.')
s = replace(s, 'Prior moment/SDP results solve tapped MATPOWER case39;',
            'Ghaddar et al. 2016 solved tapped MATPOWER case39 globally in floating point (moment relaxation); published SDP gaps are near zero;', 2)
s = replace(s, 'exact network evaluation exposes', "60-digit evaluation of the network at SCIP's points exposes", 2)
s = replace(s, '\n## One-hour solver comparison',
            '\nThe paper should cite the [Göß–Burlacu–Martin publisher correction](https://doi.org/10.1007/s10898-026-01614-9),\nwhich the [small literature report](publication/literature/small/report.md)\nidentifies but could not read. Whether it changes the relied-on Table 17\nremains unchecked. The hvycrash SIF value deserves credit; the lukvle10\nSOLTN value is a tolerance artifact whose origin is inferred, not documented.\n\n## One-hour solver comparison')
s = replace(s, 'numbers taken literally; rounding can explain the conflicts and the\n  underlying solver bounds are unknown.',
            'numbers taken literally. Page rounding of the proven optimum explains\n  the five spring conflicts; earlier rounding to six significant digits\n  could explain the other seven (evidence, not proof). The underlying\n  solver bounds are unknown.')
s = replace(s, 'Missing archive windows\n  and GAMS/OSIL',
            'Missing archive windows\n  (no copy covers March–December 2014 for sssd*persp,\n  watercontamination0303 and smallinvDAX*) and GAMS/OSIL')
s = replace(s, 'exact rational witnesses for the period problems and the seed-dependent\n  cell-pair problem. The higher cell-pair claim is now refuted by an exactly\n  feasible witness; the low claim is not refuted.',
            'exactly feasible rational witnesses that refute SCIP\'s wrong "optimal"\n  claims on three single-period subproblems of waterno2_06 (periods 0, 4\n  and 5) and on one cell-pair subproblem. The wrong claims occur only for\n  some random seeds. The higher cell-pair claims (65.12 on 10.0.x/10.1.0,\n  56.49 on master) are refuted; the low claims near 55.6898 are not.')
s = replace(s, "Not a listed value: SCIP 10's camshape100\n  incumbent from our own run (row violation 1e-8) lies 5.3e-5 below the\n  exact optimum (not independently checked).",
            'In an earlier exploratory SCIP 10 run\n  (before the one-hour campaign), the camshape100 incumbent (row violation\n  1e-8) lay 5.3e-5 below the exact optimum (not independently checked);\n  the campaign\'s SCIP 10.0.3 point lies 1.5e-7 below it, with row violation\n  7.7e-10 ([point checks](publication/solver-runs/point_checks.log)).')
s = replace(s, 'per-instance table explains.\n',
            "per-instance table explains; MINLPLib's own listed bounds were already\nwithin 1.2e-6 (camshape100) and 3.8e-5 (lnts50) relative of closure.\n")
s = replace(s, 'verdicts, proof assumptions, remaining decisions and packaging steps.',
            'verdicts, proof assumptions, remaining decisions and packaging steps.\nIts [computing environment and run times](publication/READINESS.md#computing-environment-and-run-times)\nsection records the current host, pinned reproduction versions, recorded\ncertificate/replay timings and the limits of the original-run metadata.')

a = replace(a, 'such entry involved in this audit is dated 17 or 26 Sep 2013.',
            'such entry involved in this audit is dated 17 or 26 Sep 2013\n  (apart from entries whose 6 digits reach the 8-decimal limit, such as\n  methanol50 LINDO 0.00802826, 2022-02-15).')
a = replace(a, 'solver-point pairs', '(instance, solver) pairs')
a = replace(a, 'SCIP 10 evaluated the spring proof point using bisection at its\n  feasibility tolerance. The resulting objective difference is a numerical\n  evaluation effect, not a conflict with the exact proof.',
            "SCIP 10 accepted the spring proof point at feasibility tolerance 1e-9;\n  the audit-ir script's bisection on SCIP's objective variable found\n  accepted values down to 1.0e-9 below the exact objective. This is the\n  feasibility tolerance, not an objective disagreement.")
a = replace(a, 'the old-text contradiction was re-proved.\n',
            'the old-text contradiction was re-proved. For nine instances\n  (four sssd*persp, watercontamination0303 and four smallinvDAX*), no\n  pre-bound copy was found; no copy covers March–December 2014. Their\n  model identity rests on the 2014-12 statistics and 2017 full copies.\n')
a = replace(a, 'The [status/model-history report](../publication/minlplib-status/report.md)\nand [round-2 review](../publication/reviews/minlplib-status-review-r2.md)\nfind the relevant bounds, points, solved marks and OSIL files unchanged at\nthe 2026-10-02 refresh. Archived listings support model identity for the\naudited past bounds.',
            'The [status/model-history report](../publication/minlplib-status/report.md)\nfinds the relevant bounds, points, solved marks and OSIL files unchanged at\nthe 2026-10-02 refresh, confirmed by [review r1](../publication/reviews/minlplib-status-review-r1.md).\n[Review r2](../publication/reviews/minlplib-status-review-r2.md) found four\nminor issues, since addressed in the report. Archived copies agree with\ntoday\'s model on both sides of the bound dates for most audited instances.\nsssd*persp, watercontamination0303 and smallinvDAX* were added days before\ntheir 2014 bounds; no copy covers March–December 2014, and their identity\nrests on the 2014-12 statistics and 2017 full copies.')
a = replace(a, 'exactly feasible witnesses against wrong optimality claims on the waterno2\nperiod and cell-pair models.',
            "exactly feasible witnesses that refute SCIP's seed-dependent wrong\noptimality claims on three waterno2_06 period subproblems (periods 0, 4\nand 5) and the higher cell-pair claims; the low cell-pair claims are not\nrefuted.")
a = replace(a, 'classification, margin or solver result was regenerated.\n',
            'classification, margin or solver result was regenerated. The spring\nsentence of replacement 33 was then rewritten as minor-fixes review r2,\nissue 5, requested. The 2026-10-04 response to integration review r1 adds\nthe spring bisection attribution, precision exception, model-history limits\nand correct review credit, and the scope of the SCIP witnesses.\n')

r = replace(r, 'Updated 2026-10-03.', 'Updated 2026-10-04: response to integration review r1.')
r = replace(r, 'Claude. No new reviewer was commissioned during this integration.',
            'Claude. The subsequent [independent integration review r1](reviews/integration-review-r1.md)\nreturned **issues**: 0 blockers, 3 major and 12 minor. It confirmed every\nrecomputed gap cell and count. The response below distinguishes these\nimplementation fixes from an additional independent review round.')
r = replace(r, 'Prior floating-point results are partly known.',
            'lnts is partly known: Gurobi closed lnts50 to tolerance, and Göß 2026 PARA prints 0.00–0.01% gaps (floating point).')
r = replace(r, 'ex6_2_* may have earlier ε-global floating-point results in unread sources.',
            'ex6_2_* very likely have earlier ε-global floating-point results (McDonald–Floudas; sources not read).')
r = replace(r, 'Coverage has an exact independent proof.',
            "Coverage has an exact independent proof for eg_disc2_s; eg_int_s and eg_disc_s coverage rests on the retry reviewer's exact tree bookkeeping.")
r = replace(r, 'CAMINO Gurobi claims are refuted, with cause and exact termination status unknown.',
            "For eg_disc_s and eg_disc2_s, CAMINO's Gurobi 13.0.0 optimality claim is refuted by a feasible point; the data do not record Gurobi's termination status, and the cause is unknown.")
r = replace(r, 'four minor corrections addressed in the report. | Relevant status',
            'four minor corrections addressed in the report and checked by the parent orchestrator against the reviews. | Relevant status')
r = replace(r, 'Archive gaps and truncated captures limit historical completeness.',
            'Nine instances (four sssd*persp, watercontamination0303 and four smallinvDAX*) have no pre-bound copy; no copy covers March–December 2014. Their identity rests on 2014-12 statistics and 2017 full copies. Archive gaps and truncated captures limit historical completeness.')
r = replace(r, 'Subsequent minor-fixes/report responses address the listed issues.',
            'Subsequent minor-fixes/report responses address the listed issues; the parent checked the final small-literature minor fixes against its reviews.')
r = replace(r, 'Independent final-analysis verdict **issues**; raw values/counts confirmed. The final report and tables incorporate globality disclaimers, first-batch overload and the minor interpretation corrections.',
            'Setup review r1: **issues** (two major), addressed by the final relaunch. The campaign\'s own round-2 driver review was interrupted and never finished; it has no completed findings or verdict. Solver-analysis review r1: **issues** (two major: six BARON values without a globality guarantee and the overloaded first batch; four minor); it independently re-derived run validity from raw logs and confirmed raw values/counts. The author fixed all six issues. The parent orchestrator (Claude) checked the fixes directly against the review: collect.py diff additive only, per-row flags and report wording. No second independent solver-analysis review round was performed.')
r = replace(r, 'only three of the five examined solutions have refuted wrong claims.',
            "only three of the five examined solutions have refuted wrong claims. Independent minor-fixes review r2 found one major overstatement (SCIP report line 173); round 3 applied the reviewer's exact replacement. The parent spot-checked those fixes, and integration review r1 covers them; there was no further independent minor-fixes track round.")
r = replace(r, 'minor packaging issues addressed in the package response. Final manifest',
            'minor packaging issues addressed in the package response; the parent spot-checked those fixes. No second independent package review round was performed. Final manifest')
r = replace(r, 'Minor-fixes rounds 1–2; latest verdict **issues**, while all 40 ordered replacements are explicitly confirmed correct.',
            'Minor-fixes reviews r1 and r2 were independent; latest verdict **issues** (one major and ten minor), while all 40 ordered replacements are explicitly confirmed correct. Round 3 fixed the major and track-level minor issues; the parent spot-checked those fixes, and integration review r1 covers them. There was no further independent minor-fixes track round.')
r = replace(r, '| numerical display and integration corrections |',
            '| computational environment and run times | [environment capture](integration/environment-r1.json), [recorded timing evidence](integration/runtime-evidence-r1.json), [command index](reproduction/commands.json), source terms below | Collected for this response: current host, pinned reproduction environment and selected recorded timings; timing sources and hashes checked. | Original per-run environments and CPU times are not fully recoverable. Shared machine; the release licence remains a user decision. |\n| numerical display and integration corrections |')

environment = '''## Computing environment and run times

The current host was captured on 2026-10-04 from /proc, uname and
/etc/os-release: Intel Xeon w5-2565X, 18 physical cores / 36 logical CPUs,
49,321,416 KiB RAM (47.04 GiB), Ubuntu 24.04.4 LTS, x86-64 WSL2 kernel
6.18.33.2-microsoft-standard-WSL2. The CPU exposes AVX2/FMA and AVX-512.
[environment-r1.json](integration/environment-r1.json) retains the exact
CPU flags, OS/kernel, memory and current NumPy build/runtime output.
The machine was shared with other sessions. These are current-host facts,
not recovered metadata for every original certificate run.

The pinned [reproduction environment](reproduction/environment.json) and
[requirements](reproduction/requirements.txt) specify Python 3.13.11
(Anaconda, GCC 14.3.0), NumPy 2.5.1, SciPy 1.18.0, mpmath 1.3.0,
SymPy 1.14.0, PySCIPOpt 6.2.1, CVXPY 1.9.3, Clarabel 0.11.1 and
highspy 1.15.1; PySCIPOpt's SCIP is 10.0.2. The current NumPy build reports
OpenBLAS 0.3.33.112.0, USE64BITINT/DYNAMIC_ARCH, and AVX512_SPR support;
current glibc/libm is 2.39. Active BLAS dispatch was not resolved because
threadpoolctl is unavailable. Only the reproduction versions are pinned:
the original BLAS/libm builds, SIMD dispatch and per-run package versions
were not consistently recorded. A2's exp sampling cannot certify another
dispatch. topopt p5 replay uses the committed certificate; regeneration
with one BLAS thread selects a different valid point.

Saved [campaign logs](solver-runs/runs/camshape100__BARON/gams.log) and
[settings](solver-runs/report.md) record GAMS 54.3.1 (build 61154be4),
BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3, with one solver thread.
These versions describe the comparison campaign, not every certificate
computation. The SCIP bug track separately tested 10.0.2, 10.0.3, 10.1.0
and master a01de2c.

The [command index](reproduction/commands.json) contains 443 historical
reproduction commands with wall times. The table selects successful
certificate generation or replay commands, with seconds in instance order;
single values for lnts and camshape cover all four instances in one command.
It is not a total of original search, tuning and review costs. ANN timings
are extension replay/verification; eg_disc2_s's indexed run covers part 1
only; the later all-leaf recheck is described below. Full command IDs,
exact recorded times and verified output hashes are in
[runtime-table-r1.md](integration/runtime-table-r1.md) and
[runtime-evidence-r1.json](integration/runtime-evidence-r1.json).

| family / recorded operation | wall seconds, in listed order |
|---|---|
| lnts50/100/200/400 | 1.84 |
| dtoc5 / camshape100–800 / lukvle10 / optcdeg2 calibration | 5.96 / 0.8 / 337.8 / 8.32 |
| hvycrash / ex6_2_7 / ex6_2_5 / etamac / pricing050 / pindyck | 0.17 / 167.34 / 800.71 / 27.09 / 8.28 / 18.67 |
| chain50/100/200/400 | 11.56 / 15.69 / 20.69 / 28.76 |
| catmix100/200/400/800 | 1049.26 / 1728.27 / 3000.91 / 4602.0 |
| powerflow0030p/0039p/0039r | 12.67 / 316.23 / 463.46 |
| waterno2_06/09/12/18/24 period certificates | 221.25 / 772.61 / 994.2 / 2385.66 / 3210.92 |
| waterno2_06 cell-slope replay | 10.72 |
| ann extension replay runs 1/2; region verification runs 1/2; open-box verification run 2 | 1951.92 / 5613.0 / 668.11 / 3044.08 / 532.1 |
| KAN R: r3 n4/n5/n9; r5 n3/n5/n8 | 22.57 / 23.83 / 22.34 / 1083.76 / 101.5 / 87.33 |
| eg_int_s; eg_disc_s parts 0/1; eg_disc2_s part 1 | 211.51 / 279.04 / 234.6 / 635.18 |
| audit linear / nd_netgen / emfl050_3_3, 050_5_5, 100_3_3, 100_5_5 / topopt p4/p5 regeneration | 6.18 / 0.93 / 3.18 / 14.56 / 5.77 / 26.25 / 167.62 / 164.44 |

For the eg_disc2_s all-leaf recheck, the 38 saved chunk timing fields sum
to 41,162 seconds rounded once (summing individually printed whole seconds
instead gives 41,151); the scheduler log records 5,372 elapsed wall seconds.
Although the track report calls the chunk total CPU time, recheck_leaves.py
measures time.time(), so it is a sum of chunk wall times, not measured CPU
time. Concurrent chunk times must not be read as end-to-end duration.
Original per-certificate CPU times are not consistently available. Shared
load and varying concurrency limit timing comparisons; these measurements
support no isolated-core speed ranking. This response reran no certificate
or solver and used at most three single-thread checks concurrently.

Source licences/terms checked on 2026-10-04:

| source | recorded licence or terms |
|---|---|
| MINLPLib models and pages | The [download page](https://www.minlplib.org/download.html) identifies CC BY 4.0. Preserve source attribution and identify changes under its terms. |
| QPLIB instances | [QPLIB documentation](https://qplib.zib.de/doc.html) identifies CC BY 4.0 for QPLIB and separately reserves website copyright to ZIB and GAMS. Do not assume the instance licence also covers every website asset. |
| CUTEst software and SIF problem collection | The separate [CUTEst LICENSE](https://github.com/ralna/CUTEst/blob/master/LICENSE) and [SIF LICENSE](https://github.com/ralna/SIF/blob/master/LICENSE) each give three-clause BSD terms: retain copyright, conditions and disclaimer; no endorsement without permission. Preserve problem-source credits in the SIF files. |
| MATPOWER software and case data | [MATPOWER software](https://matpower.org/license/) uses three-clause BSD from version 5.1. Its [manual, Section 1.2](https://matpower.org/docs/MATPOWER-manual-8.0b1.pdf) explicitly excludes case data from that licence: data were included by permission or converted from public sources. The saved [case30](literature/network/sources/matpower_case30.m) and [case39](literature/network/sources/matpower_case39.m) headers identify their sources; retain those credits. |

These source terms do not choose a licence for our own paper data or code.
The user must choose the release licence(s), and the package owner must
include the applicable third-party attribution and notices for the actual
release contents. Source articles, archived pages and case data do not
inherit a licence selected for our original code.

'''
r = replace(r, '## Open decisions for the user\n', environment+'## Open decisions for the user\n')
r = replace(r, '\n## Final gap check\n', '''
4. **Release licence:** choose the licence(s) for the paper's original data
   and code. The source terms above remain attached to third-party material;
   this task has not invented or applied a blanket release licence. The
   package owner must carry the applicable attributions and notices into
   the final archive.

## Response to integration review r1

The [independent review](reviews/integration-review-r1.md) returned
**issues** (0 blockers, 3 major, 12 minor); its gap cells and counts were
correct. [Exact checks](integration/review-r1-evidence.log), the renewed
[number checks](integration/review-r1-numbers.log), and
[commands](integration/commands.md) record this implementation response.
The fixes below have targeted implementation checks; no second independent
integration review is claimed. Items 2 and 15 belong to the parallel owner.

| item | resolution |
|---|---|
| 1, major: literature table | Removed both blank lines after the delimiter. The Markdown parser now checks all tables in the summary, audit and this record, including header attachment and the 43 literature rows. A negative control rejects the original broken table. |
| 2, major: eg_disc2_s package coverage | Excluded from this implementation as instructed; the parallel package owner handles the all-leaf evidence and package descriptions. No package file was changed here. |
| 3, major: environment, timings and licence | Added current /proc and uname metadata, pinned reproduction versions, solver versions and a sourced timing table. Original environments and CPU times remain explicitly incomplete; source terms are recorded and choosing our release licence is an open user decision. |
| 4: gap-source list | Added dtoc5, lukvle10, pindyck and all three eg rows to the displayed-dual exceptions; numerical gaps are unchanged. |
| 5: eg_disc_s display | Added its binary64 excess and the independent exact-decimal leaf certification that justifies it, under A1/A2. |
| 6: literature labels/wording | Corrected Martin, camshape100/800 and eg_int_s labels; catmix sourcing; powerflow provenance and transport limits; KAN evaluation precision; CAMINO status limits; PARA percentages and DTOC5 source-model scope. Cited the unread publisher correction, credited hvycrash's SIF value and identified lukvle10 SOLTN as a tolerance artifact. |
| 7: SCIP scope | Named waterno2_06 periods 0, 4 and 5, seed dependence, both higher cell-pair claims and the unrefuted low claims in the two main documents. |
| 8: rounding and spring bisection | Limited the page-rounding explanation to the five spring conflicts; earlier rounding for the other seven is evidence only. Corrected pair terminology and credited the audit-ir script's bisection at feasibility tolerance 1e-9. |
| 9: historical model evidence | Named the nine instances with no pre-bound copy and the uncovered archive window in both main documents and this record; credited status review r1 for the refresh and preserved r2's actual verdict. |
| 10: review facts | Recorded the interrupted driver review, independent solver-analysis r1 (2 major + 4 minor), author fixes and Claude's direct checks without another independent round. Recorded independent minor-fixes r1/r2 and parent spot-checks of round 3, covered by integration r1; also recorded parent checks of status, lit-small and reproduction fixes. |
| 11: readiness wording | Made lnts prior results and the likely ex6_2_* history precise; limited the separate exact coverage proof to eg_disc2_s and cited integration r1's actual verdict. |
| 12: earlier closeness | Restored 1.2e-6 for camshape100 and 3.8e-5 for lnts50 after exact checks against saved values. These are approximate historical gaps, not the current closure enclosures. |
| 13: old SCIP incumbent | Identified the earlier unchecked exploratory run and distinguished the campaign's 1.5e-7 deficit and 7.7e-10 row violation. |
| 14: audit details | Added the methanol50 2022 precision exception and recorded the replacement-33 spring rewrite requested by minor-fixes r2, issue 5. |
| 15: stale track/package displays | Excluded as instructed; handled by the parallel track/package owner. The summary's checked displays remain authoritative. |

The only numerical interpretation disagreement found here concerns the eg
runtime label: the saved timing fields measure wall time, despite the track
report's CPU label. The environment section uses the actual measurement.
For item 10, the parent's checks are recorded as the user specified, not
mislabelled as a second independent review. No gap-cell correction was
needed.

## Final gap check
''')
r = replace(r, '**Scientific evidence still missing for the scoped computational paper:\nnone, if the claims retain the assumptions and limits above.**',
            '**Scientific evidence still missing: none for the stated claims, if\nthey retain the assumptions and limits above.** Environment and timing\nmetadata are now collected to the extent the records allow; complete\noriginal per-run environments and CPU times were not recorded. Source\nlicence facts are documented, but the paper\'s data/code release licence\nand final third-party notices remain to be chosen/prepared.')
r = replace(r, 'and committing the complete dependency set when the user chooses.',
            'choosing the data/code release licence and adding applicable source\nnotices; and committing the complete dependency set when the user chooses.')
r = replace(r, 'An independent review of this final integration has not been performed.',
            'The [independent integration review r1](reviews/integration-review-r1.md)\nfound issues (0 blockers, 3 major, 12 minor). This response fixes the owned\nissues; items 2 and 15 remain with the parallel owner. These fixes have not\nreceived a second independent integration review.')
for p, text in zip(paths, (s,a,r)):
    p.write_text(text)
    print('Updated',p.relative_to(BASE))
