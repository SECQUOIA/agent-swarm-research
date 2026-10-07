"""Integrate checked local evidence into the two owned documents."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
G=json.loads((OUT/'gap-values.json').read_text())
s=(BASE/'open-instances-summary.md').read_text()
def replace(old,new):
    global s
    assert old in s,old
    s=s.replace(old,new)
replace('Date: 2026-09-30 (round-4 results added 2026-10-01). This page collects the rigorous dual bounds computed in', 'Updated 2026-10-03: publication-track integration, exact primal points,\nupward gap displays, literature context, refreshed MINLPLib status, solver\ncomparisons, and the independently checked SCIP finding. This page collects\nthe rigorous dual bounds computed in')
replace('three-solver metadata value. Gaps use absolute differences unless marked.', 'three-solver metadata value. The [status refresh](publication/minlplib-status/report.md)\nfound the relevant pages, solved marks, points, bounds and OSIL models unchanged\non 2026-10-02; this is the refresh date, not a claim about a later live state.\nGaps are absolute unless marked relative or percent. Every displayed gap is\nrounded upward and is an upper bound on the gap under the stated proof\nassumptions. Relative gaps in the closed table divide by the absolute\ncertified dual. Gap calculations and exact source fractions are recorded in\n[publication/integration/gap-values.json](publication/integration/gap-values.json).')
replace('## Instances closed (31)', '## Instances closed to the stated gaps (31)')
# Every numeric gap cell is checked in check_numbers.py. Some gaps use a
# tighter saved certificate/point enclosure than the compact bound columns.
new=[]
for line in s.splitlines():
    if line.startswith('| '):
        col=line.split('|');name=col[1].strip()
        key='pricing050' if name=='pricing050 (max)' else name
        if key in G:col[5]=' ≤ '+G[key]['text']+(' rel.' if name.startswith('powerflow') or name.startswith('eg_') else '')+' '
        elif name=='chain50–400':col[5]=' ≤ 1.01e-14 '
        elif name=='catmix100–800':col[5]=' ≤ 1.85e-13 / 1.90e-11 / 6.81e-11 / 1.49e-10 (100/200/400/800) '
        elif name=='ann_cumene_tanh':col[5]=' ≤ '+G['ann']['text']+' (wave 3: ≤ '+G['ann wave3 primal']['text']+') '
        if name=='waterno2_06':col[5]=' ≤ '+G[key]['text']+' (≤ '+G[key+' separator']['text']+'; ≤ '+G[key+' wave2']['text']+') '
        if name=='lnts50':col[7]=' [dual verified](reviews/open-instances-verification/verification-report.md); [exact primal verified](publication/primal/lnts/report.md) '
        elif name.startswith('lnts'):col[7]=' dual and exact primal verified (same reports) '
        elif name in ('dtoc5','lukvle10'):col[7]=' dual verified; [exact primal verified](publication/primal/dtoc5-lukvle10/report.md) '
        elif name=='chain50–400':col[7]=' [dual verified](reviews/cops-verification/verification-report.md); [exact primal verified](publication/primal/chain/report.md) '
        elif name.startswith('powerflow'):col[7]=col[7].strip()+'; [exact primal verified](publication/primal/powerflow/report.md) '
        elif name=='eg_int_s':col[7]=' [verified](reviews/eg-retry-review.md) (all leaves, under A1/A2) '
        elif name=='eg_disc_s':col[7]=' verified (all leaves, under A1/A2) '
        line='|'.join(col)
    new.append(line)
s='\n'.join(new)+'\n'
replace('(exact value of the certificate)', '(certificate value rounded down)')
replace('0.0693 for n8','0.0694 for n8')
replace('optimum of the network relaxation R certified to ~1e-10', 'optimum of the network relaxation R enclosed with absolute gap ≤ 2.42e-8')
replace('| ~1e-10 | reduced-space', '| ≤ 2.42e-8 absolute (per-instance gaps below) | reduced-space')
replace('1.4e-6 relative','1.36e-6 relative')
replace('1.67%','1.68%')
replace('16.0%; the new 0.194% is the same under both', '16.1%; the new gap rounds upward to 0.195% under the primal denominator\nand 0.194% under the dual denominator')
replace('now within 0.194%','now within 0.195%')
replace('intended network relaxation is certified to about 1e-10','intended network relaxation has absolute gap at most 2.42e-8')
replace('## Relaxation certified; OSIL models exactly infeasible', '''Gaps use saved objective enclosure endpoints and certificate values, except
lnts (the displayed summary duals), chain (the safe individual dual displays),
and pricing050 (subtraction of its safe displayed upper and lower bounds).
The pricing gap is deliberately conservative: the saved verifier log reports
a smaller gap, but does not retain enough objective digits to reconstruct it
exactly by subtraction. The catmix gaps use the stronger independently
verified duals, the saved exactly feasible author points for 100/200/400,
and the verifier's exact DP-policy point for 800; the compact dual range is
only a display. See the [catmix recheck](reviews/catmix-recheck.md) and
[exact display record](publication/reproduction/cops/logs/exact_display_checks.json).
For optcdeg2 the gap uses the exact rational certificate, rather than its
rounded-down table display. Zero for camshape and hvycrash means an attained
exact optimum proved analytically, rather than subtraction of displays.

For all three eg_* certificates, **A1** assumes that the certifier's
hand-checked floating-point padding analysis bounds every rounding error;
**A2** assumes numpy's exp has relative error at most 1e-14. A2 is supported
by sampling, not a uniform proof. The final rational certificate tests do
not remove these assumptions about their input enclosures. The
[eg recheck](publication/eg-recheck/report.md) certified all 1,114,361 leaves
of run G for eg_disc2_s, with zero failures. The earlier 1,152,830 count is
processed boxes, not leaves. Independent review also supplied an exact
coverage proof and outward-rounded interval certificates for a separate
10,404-leaf sample in parts 0 and 2–7; that sample does not replace A1/A2
for the remaining leaves.

## Relaxation certified; OSIL models exactly infeasible''')
marker='## Instances substantially improved but not closed'
kan='''The [exact primal track](publication/primal/water-ann-kan/report.md) now
provides points satisfying every retained row of R and all variable bounds.
Their enclosure proof assumes outward rounding by mpmath iv. The original
partition-of-unity rows remain exactly inconsistent; no OSIL-feasible KAN
point or OSIL optimum is claimed.

| instance | absolute gap for R (rounded up) |
|---|---|
'''
for name in G:
    if name.startswith('kan_'):kan+='| '+name+' | ≤ '+G[name]['text']+' |\n'
s=s.replace(marker,kan+'\n'+marker)
replace('## Invalid bounds and solver errors found','''The water and ANN primal columns now bound exactly feasible points; see the
[exact primal report](publication/primal/water-ann-kan/report.md). Water
feasibility uses exact algebraic arithmetic. ANN feasibility uses a forward
construction and outward-rounded enclosures, assuming mpmath iv is correct.

## Prior literature and scope of novelty

The tables describe certificates for the stored MINLPLib OSIL models.
"New as far as found" records the search result; it does not establish
priority against unread or undiscovered sources. Floating-point closure and
rigorous certification are distinct claims. Sources, model comparisons,
unread sources and review responses are in the three literature reports.

| instance | prior result and consequence | report |
|---|---|---|
''')
# Add one row for every instance, including expanded grouped families.
lit=[]
def add(names,text,track):
    for name in names:lit.append(f'| {name} | {text} | [{track}](publication/literature/{track}/report.md) |')
add(['lnts50'],'Göß–Burlacu–Martín: Gurobi tolerance-level closure; Göß 2026 PARA result. Partly known; rigorous closure new as far as found.','control')
add(['lnts100','lnts200'],'Göß 2026 PARA displays a zero percentage gap. Partly known in floating point; rigorous closure new as far as found.','control')
add(['lnts400'],'Göß 2026 PARA displays a small nonzero gap. Partly known in floating point; rigorous closure new as far as found.','control')
add(['dtoc5'],'MINOTAUR floating-point closure on identical QPLIB_8585, with assumed default variable bounds. Waki et al. 2006 found a numerically tight sparse SDP on the DTOC5 source. MINLPLib dynamics multiply the CUTEst quadratic coefficient by 4. Partly known; rigorous certificate new as far as found.','control')
add(['camshape100'],'Octeract solved it globally in floating point; Mittelmann lists Octeract and ANTIGONE on the rounded QPLIB copy. Exact optimum is the new result; ANTIGONE’s reported value is a tolerance artifact.','control')
add(['camshape200'],'Octeract was listed as solving the rounded QPLIB copy; value and log unavailable. Partly known; exact optimum new as far as found.','control')
add(['camshape400'],'No prior global closure found. New as far as found.','control')
add(['camshape800'],'MINOTAUR claimed global closure of the rounded QPLIB copy at a conflicting value. Our exact MINLPLib result is new as far as found; transport of the contradiction to the rounded QPLIB model is strong evidence, not proof.','control')
add(['lukvle10'],'Local CUTEst value and nonclosing solver bounds only. New as far as found.','control')
add(['optcdeg2'],'Older MINOTAUR closure listing on identical QPLIB_8803 lacks the value/log; later infeasibility claim is false. The CUTEst damping coefficient differs by a factor of 4. Partly known; rigorous certificate new as far as found.','control')
add(['chain50','chain100','chain200','chain400'],'COPS local values; no prior global closure found. New as far as found.','control')
add(['catmix100','catmix200','catmix400','catmix800'],'COPS 2.0 local values; COPS 3.0 uses a different discretization. New as far as found. OSIL coefficients differ slightly from GAMS coefficients.','control')
add(['hvycrash'],'Same CUTE HVYCRASH at N=50; the solution value was already listed. Partly known; exact constant-objective identity and feasible witness new as far as found.','small')
add(['ex6_2_5','ex6_2_7'],'McDonald–Floudas ε-global result likely, but key source not read; later BARON global labels are not certificates. Partly known; rigorous certificate new as far as found.','small')
add(['etamac','pricing050','pindyck'],'Local values or nonclosing bounds only. New as far as found; source-model and scaling limits are stated in the report.','small')
add(['eg_int_s'],'SCIP 8.1 solved it globally in floating point (Göß–Burlacu–Martin). Our assumption-qualified certificate is new as far as found. CAMINO’s Gurobi optimality claim is refuted by a feasible point.','small')
add(['eg_disc_s','eg_disc2_s'],'No valid prior closure found. New as far as found. CAMINO’s Gurobi optimality claims are refuted; recorded termination status and cause are unknown.','small')
add(['powerflow0030p'],'Partly known: tolerance-level closure via rectangular twin. MATPOWER case30 loses its two shunts in MINLPLib; polar/rectangular coefficient rounding prevents unproved exact bound transport. Prior rigorous ACOPF work (Oustry et al.) concerns different models.','network')
add(['powerflow0039p','powerflow0039r'],'Prior moment/SDP results solve tapped MATPOWER case39; MINLPLib drops transformer taps. New as far as found for these stored models.','network')
add(['waterno2_06','waterno2_09','waterno2_12','waterno2_18','waterno2_24'],'Huang’s related multi-period models remain unclosed; the cited MSc thesis was not obtained. New as far as found.','network')
add(['ann_cumene_tanh'],'Partly known: the exactly identical ann_cumene_exp twin was closed in floating point by SCIP/LINDO. Our rigorous finite bound is new as far as found and weaker than those floating-point claims.','network')
add(['kan_r3_h1_n4','kan_r3_h1_n5'],'Published SCIP zero-gap claims conflict with the certified minimum of R; exact network evaluation exposes feasibility-tolerance artifacts. Prior claim contradicted; rigorous R result new as far as found.','network')
add(['kan_r3_h1_n9','kan_r5_h1_n3','kan_r5_h1_n5','kan_r5_h1_n8'],'Prior solver runs did not close the gap. New as far as found for R; exact OSIL infeasibility remains separate.','network')
assert len(lit)==43
s=s.replace('## Prior literature and scope of novelty', '## Prior literature and scope of novelty',1)
# The insertion above ends immediately before the old audit body.
pos=s.index('\n**Systematic audit**')
s=s[:pos]+'\n'+'\n'.join(lit)+'''

## One-hour solver comparison

The [final campaign](publication/solver-runs/report.md) and
[per-run table](publication/solver-runs/results_table.md) compare BARON
26.5.27, GUROBI 13.0.2 and SCIP 10.0.3 on the paper instances with a
3600-second solver limit, one thread, and absolute/relative gap requests of
1e-9. There are 129 kept outcomes, including three SCIP memory-limit stops;
126 pass the measurement rule. Certificate-consistent closures are zero
for every solver. BARON’s two optimality claims (camshape100/200) contradict
the proved optimum intervals and return infeasible points.

All 109 finite final solver dual values are weaker than our corresponding
certificates. Six BARON values (catmix100/200/400/800, dtoc5, optcdeg2) carry
BARON’s warning that globality is not guaranteed, leaving 103 without that
warning. Six SCIP values concern slightly tightened log/power argument
bounds. KAN comparisons concern R. The first batch of ten runs suffered
overload and memory pressure; it passes the stated measurement rule but is
not an isolated speed benchmark. BARON’s limit is CPU time; GUROBI/SCIP use
wall time. The report discloses actual solver times, interrupts, capability
failures and shared-machine conditions. These runs establish neither
performance rankings nor failure under other settings or larger budgets.

## Invalid bounds and solver errors found
'''+s[pos:]
# Updated SCIP diagnosis and pair witness, with instrumented-scope qualifier.
start=s.index('- **SCIP 10.0.2 wrong optimal values**')
end=s.index('- **Tolerance artifacts in listed primal values:**',start)
s=s[:start]+'''- **SCIP wrong optimal values on waterno2 subproblems.** The
  [SCIP bug track](publication/scip-bug/report.md) and its
  [independent review](publication/reviews/scip-bug-review-r1.md) supply
  exact rational witnesses for the period problems and the seed-dependent
  cell-pair problem. The higher cell-pair claim is now refuted by an exactly
  feasible witness; the low claim is not refuted. The finding reproduces
  on SCIP 10.0.2/10.0.3/10.1.0 and the tested master commit. In the
  instrumented wrong runs, reverse propagation by the default nonlinear
  handler cuts off a feasible point because of a binary64 residual in a
  cubic equality at fixed bounds. That mechanism is established for those
  traced runs; it is not a diagnosis of every SCIP bound. A minimized
  reproducer and an upstream report are prepared. **The upstream report
  is drafted and has NOT been submitted; filing is the user’s decision.**
'''+s[end:]
# Add audit-ir, identity and replay context to systematic-audit narrative.
replace('- "A solver reported a local optimum as a bound" is an inference, not\n  verified.', '''- **Rounding-scale audit results:** all 12 class (i-r) pairs were
  independently re-proved in [audit-ir](publication/audit-ir/report.md),
  including a global optimum proof for spring. They refute the displayed
  numbers taken literally; rounding can explain the conflicts and the
  underlying solver bounds are unknown. Page parsing and screening were
  independently checked.
- The [model-history check](publication/minlplib-status/report.md) found
  unchanged audited models except for rounding of three ghg_3veh constants;
  the contradiction also holds on that older text. Missing archive windows
  and GAMS/OSIL coefficient differences remain stated limits.
- "A solver reported a local optimum as a bound" is an inference, not
  verified.''')
s+='''
## Evidence and reproduction

The [reproduction guide](publication/reproduction/README.md) and
[package report](publication/reproduction/report.md) map the certificates,
primal definitions and audit classifications to saved inputs, scripts and
outputs. Follow their disposable-copy instructions: several scientific
scripts write logs or certificates when imported or run. The topopt p5
numbers in the audit rest on the committed certificate; a one-BLAS-thread
regeneration selects a different point, as explained in the guide. Exact
replay of saved proofs and numerical regeneration are distinct operations.
Older detailed reports can contain unsafe rounded displays; the checked
bounds and gaps on this page are authoritative for the paper.

The [publication-readiness record](publication/READINESS.md) gives review
verdicts, proof assumptions, remaining decisions and packaging steps. This
integration reran no solver or scientific search, made no commit, and
contacted nobody.
'''
(BASE/'open-instances-summary.md').write_text(s)
# Audit: preserve historical revision records but supersede current caveats.
a=(BASE/'bound-audit/audit-report.md').read_text()
def ar(old,new):
    global a
    assert old in a,old
    a=a.replace(old,new)
ar('Date: 2026-09-30. Status: computational audit. Its results were checked','Updated 2026-10-03: publication integration adds independent class (i-r)\nproofs and page parsing, the model-history/status refresh, the SCIP finding,\nand reproduction limits. The original computational audit is dated\n2026-09-30. Its results were checked')
ar('So all 19 class (i) pairs and all four (ii)-proven emfl instances are now\nconfirmed independently. The (i-r), (ii)-repair and (iii) rows, the parsing\nof the 1633 pages and the instance change histories were not checked\nindependently (Section 8).', '''All 19 class (i) pairs, all 12 class (i-r) pairs and all four (ii)-proven
emfl instances are confirmed independently. The publication tracks also
checked page parsing and model histories (Section 8.4). Class (ii)-repair
and (iii) did not acquire independent validity proofs.''')
ar('(ii)-proven bounds of all four emfl instances. The (i-r) results rest on this\naudit\'s code only.', '''(ii)-proven bounds of all four emfl instances. The later publication
[audit-ir track](../publication/audit-ir/report.md) independently re-proved
all 12 class (i-r) pairs (Section 8.4).''')
ar('  (Section 8), but not the (i-r) results.', '  and all class (i-r) results (Section 8).')
# exact existing wording differs slightly; handle the current paragraph
ar('  (Section 8), but not', '  (Section 8), but not') if '  (Section 8), but not' in a else None
ar('  stored solver bounds are unknown. The spring SCIP objective difference\n  of about 1e-9 comes from bisection and feasibility tolerance; it is not\n  an independent objective disagreement.', '''  stored solver bounds are unknown. In the separate audit-ir recheck,
  SCIP 10 evaluated the spring proof point using bisection at its
  feasibility tolerance. The resulting objective difference is a numerical
  evaluation effect, not a conflict with the exact proof.''')
ar('  would show up here as invalid. I did not check instance change histories.', '''  would show up here as invalid. The later
  [model-history check](../publication/minlplib-status/report.md) examined
  those histories. It found no substantive model change explaining the
  audited conflicts. Only three ghg_3veh constants changed by rounding;
  the old-text contradiction was re-proved.''')
ar('### 8.3 Not checked by either review', '### 8.3 Scope left by the first two reviews (historical)')
ar('## 9. Files, commands and run status', '''### 8.4 Publication checks integrated on 2026-10-03

The [audit-ir report](../publication/audit-ir/report.md), checked by an
[independent reviewer, round 1](../publication/reviews/audit-ir-review-r1.md),
re-proves all 12 class (i-r) pairs with exact rational arithmetic. It also
re-parses the stored pages and independently reproduces the screen and ties.
The four instances are eniplac (three solvers), lop97icx (one), spring
(five) and stockcycle (three). Spring's exact global optimum rounds to all
five listed duals, so display rounding explains the listed conflicts; the
underlying solver bounds remain unknown. The other seven entries could
reflect earlier rounding to six significant digits, but that is evidence,
not a proved account of the solver computations. No classification changes.

The [status/model-history report](../publication/minlplib-status/report.md)
and [round-2 review](../publication/reviews/minlplib-status-review-r2.md)
find the relevant bounds, points, solved marks and OSIL files unchanged at
the 2026-10-02 refresh. Archived listings support model identity for the
audited past bounds. The old ghg_3veh model differs in three rounded
constants; the invalidity proof holds there too. glider100 is unchanged;
complete pre-bound copies support topopt identity, while its later archived
copy is truncated. Some earlier archive windows are absent, so model
history is not established by a continuous chain of archived copies.
The certificates use exact OSIL coefficients; small GAMS/OSIL differences
are recorded in the report. Its current Table B1 supersedes the older
Table B1 in its data/tables.md.

The [SCIP finding](../publication/scip-bug/report.md), independently
[verified in round 1](../publication/reviews/scip-bug-review-r1.md), supplies
exactly feasible witnesses against wrong optimality claims on the waterno2
period and cell-pair models. In instrumented wrong runs, fixed-bound cubic
equalities suffer a binary64 residual and the default nonlinear handler's
reverse propagation cuts off the feasible witness. The trace supports that
mechanism on those runs; it does not diagnose unrelated historical bounds.
The upstream report and minimized reproducer are prepared. **The report
is drafted and has NOT been submitted; filing remains the user's decision.**

The [reproduction guide](../publication/reproduction/README.md) and
[package report](../publication/reproduction/report.md) map each audit
classification to scripts and saved evidence. The topopt p5 objective
numbers in this report use the committed certificate. Regeneration with
one BLAS thread selects a different exactly feasible point because the
pivoted QR basis depends on numerical settings; the guide explains the
resulting display-check differences. This is a replay/regeneration limit
and changes no classification or invalidity conclusion.

The latest review verdicts, responses and limits are recorded in
[publication/READINESS.md](../publication/READINESS.md). Older revision
records below describe the verification status at their own dates.

## 9. Files, commands and run status''')
ar('relative 1.4e-6','relative 1.36e-6')
# Explicitly qualify the current historical-inference paragraph.
a=a.replace('  Independent code has confirmed all class (i) results and the emfl bounds\n  and all class (i-r) results (Section 8).', '  Independent code has confirmed all class (i) and (i-r) results and the\n  emfl bounds (Section 8).')
a+='''
### 10.4 Publication integration (2026-10-03)

Applied the owned exact replacements from the minor-fixes integration list:
page precision and entry-count definitions, the conservative slack floor,
and the spring rounding qualifier. Corrected the emfl050_3_3 relative
"at least" display by exact rational arithmetic. Added the independent
(i-r) proofs, parsing and screening checks, status/model-history refresh,
SCIP bug evidence and committed-certificate reproduction limit. No data,
classification, margin or solver result was regenerated.

Targeted integration commands and their results are recorded in
[../publication/integration/commands.md](../publication/integration/commands.md).
The exact checks read saved data without importing scientific scripts.
No project-wide verification or CI inspection was performed; no commit,
push or outside contact was made.
'''
(BASE/'bound-audit/audit-report.md').write_text(a)
print('WROTE',BASE/'open-instances-summary.md');print('WROTE',BASE/'bound-audit/audit-report.md')
