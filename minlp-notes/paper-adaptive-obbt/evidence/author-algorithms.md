# Author report: algorithms, effort, and computational evidence

Lane: algorithms-and-evidence writer. Date: 2026-10-05.

## Files written

| File | Content | Labels other sections may use |
|---|---|---|
| `sections/algorithms.tex` | Exact certified-closure procedure and its outcome theorem; numerical SCIP policy, validated bounds, scheduling | `sec:algorithms`, `sec:algorithms-family`, `sec:algorithms-lp`, `sec:algorithms-closure`, `sec:algorithms-policy`, `thm:closure`, `lem:lp-certificate`, `prop:row-correction`, `prop:dual-residual`, `lem:enclosure`, `prop:sidecar-validity`, `tab:contracts`, `tab:closure-runs`, `tab:policy-parameters` |
| `sections/effort.tex` | What must be charged, serial ledger, no comparison from a ledger, interleaving and serial rescue, history-only selection, evaluation consequences | `sec:effort`, `sec:effort-*`, `prop:ledger`, `prop:no-comparison`, `thm:interleaving`, `cor:equal-shares`, `prop:rescue`, `ex:history` |
| `sections/experiments.tex` | Precursor summary; frozen protocol; outcomes; work decomposition; interpretation and limits | `sec:experiments`, `sec:experiments-precursor`, `sec:experiments-design`, `sec:experiments-outcomes`, `sec:experiments-work`, `sec:experiments-interpretation`, `tab:cohort`, `tab:campaign`, `tab:work` |
| `appendices/precursor-study.tex` | Details of the September external-presolve study | `sec:precursor-details`, `tab:precursor-solver`, `tab:precursor-control`, `tab:precursor-rounds` |

The appendix file is an addition beyond the three assigned sections, created
because the task asked for precursor details in an appendix if valuable. No
other author's file was edited. `main.tex` (root) now inputs the appendix.

No new macros. The files use `\R`, `\Q`, `\hull` from the shared preamble,
the `example` environment, `booktabs` rules (`\toprule`, `\midrule`,
`\cmidrule`, `\addlinespace`), `\tabularnewline`, and `\operatorname`. Equation
labels referenced from other sections: `eq:projected`, `eq:mccormick-gap`.
Theorem labels referenced: `lem:order`, `lem:fixed-persist`,
`lem:reference-family`, `prop:current-round`, `thm:protected`,
`prop:round-check`, `ex:round-check`, `cor:objective-ceiling`,
`ex:three-variable`, `ex:halving`, `ex:heron`, `prop:corrected-dual-con`.

## Developments beyond transcription

### Exact closure procedure (`thm:closure`)

The archived report described the driver informally. The manuscript states
the procedure step by step and proves five outcome properties: committed
rounds equal exact Jacobi rounds via the rational weak-duality certificate;
`fixed` returns a witness pool, a fixed box that contains every fixed box in
`B_0`, persistence under all relaxation-sound sequences with cutoffs at least
`U`, and a relaxation-value ceiling; a round whose input box is fixed always
returns `fixed`, so every committed round without `fixed` strictly shrinks
the box and detection is at most one round late; `unfinished` and
`inconclusive` return the last committed iterate and certify nothing about
the failed round, in particular no infeasibility; validity of all returned
boxes under the caller's validity premise. After the certificates section
appeared, the proof was shortened to cite `thm:protected`,
`lem:fixed-persist`, `prop:round-check`, and `cor:objective-ceiling` instead
of repeating them, and the reference family is cited from
`lem:reference-family` (notation `y_k`, `Gz<=g`) instead of a second
monotonicity proof. All six table rows were checked against the saved driver
outputs; the square fixtures are tied to `ex:halving` and `ex:heron`. The
fourth Heron iterate `21523361/21523360` was computed by hand.

### Numerical bound validation

- `prop:dual-residual` states the residual bound and proves that its right-hand
  side is the LP dual function with bound multipliers eliminated, so its
  maximum over `y<=0` equals the LP value. It cross-references the stored-dual
  version `prop:corrected-dual-con`.
- `lem:enclosure` and the three-pass description prove the directed-rounding
  evaluation in the frozen solver source (`dual_box_bound`), including the
  behavior under overflow (rejection, or `pred(+inf)` = largest finite number,
  still a lower bound) and the gradual-underflow premise.
- `prop:row-correction` states the outward correction precisely. Checking the
  source showed that original, McCormick, and tangent coefficients are already
  binary64 numbers; only derived coefficients such as the secant slope need
  correction, while right-hand sides stay exact until one upward rounding.
- `prop:sidecar-validity` is a new formal statement of what an applied bound
  guarantees: every stored-feasible point with objective at most the cutoff
  satisfies it. The following paragraph states exactly why the cutoff makes the
  guarantee conditional.

### Policy description corrected against the frozen source

- The pilot is a single test after the second LP (the accumulated gain never
  decreases). Without screening it examines both bounds of the top-ranked
  variable. Its gain is the proposed movement of each SCIP-accepted bound,
  before integer rounding, divided by the callback-start width.
- Each LP time limit is `max(1 ms, min(0.25 s, remaining time))`; the floor
  can exceed the remaining allowance.
- Trigger evaluation is timed even when no callback is admitted.
- Trigger state is keyed by SCIP node number. Probing nodes share number 0, so
  the policy admits at most three callbacks for all probing nodes of a run.
  The SCIP 10.0.3 source (`src/scip/tree.c`) shows that `nodeCreate` sets
  `number=0`, that only `SCIPnodeCreateChild` assigns a positive number, and
  that `treeCreateProbingNode` never assigns one. The campaign used 10.0.2;
  the manuscript states which version was inspected.
- The history-dependent tangent pool can break lifted monotonicity; the
  manuscript does not claim it always does.

### Effort section

Follows `audit-constraints.md`: serial-operation premise with the concurrent
counterexample, the separate untimed admission term `J`, reservation form, and
the overrun form of serial rescue. Additions: the explicit
`c_1 Delta L > c_0 Delta C` trade-off, an equal-shares corollary with a complete
proof (`a_A(t)>=t/2`, `a_H(t)>=t/2-q/2`), and the formal statement that no
function `g(N_0,b)` bounds `N+E` under the reservation ledger.

### Derived statistics from archived records

All are labeled in the text as computed afterwards; none was part of the frozen
analysis. The script below rechecks each one.

- Work by node class (`tab:work`): root 100/98 callbacks, tree 166/505,
  probing 90/90, unsupported 48/48; LPs 1150/336, 662/1203, 360/180; accepted
  62/62, 50/244, 0/2; times 8.224/3.554, 5.485/13.287, 3.684/2.593,
  0.068/0.066 s. Trigger visits without a callback cost 2.069/3.623 s.
  LP solve plus validation: 12.818/10.393 s.
- About 17 ms of non-LP sidecar time per admitted callback (including
  rejected trigger visits) and about 6 ms per LP in both arms.
- 27 fixed runs used all 64 LPs; 20 adaptive runs outside `qp3` hit the
  24-callback cap. Much of the 20.9% LP reduction follows from this cap.
- Solved-run process totals 34.21/39.52/39.88 s; increases 5.32/5.67 s;
  sidecar on those runs 5.23/5.72 s. PAR-2 differences come only from these runs.
- Public mean gap without `bayes2_50`: 0.274/0.282/0.289. In 11 of 12 gap
  losses of each arm the final dual bound was weaker.
- Largest sidecar total 1.00501 s; 7/11 runs above 1 s; summed share 6.2%/7.4%;
  largest per-run share about 40%.
- Process time outside the solver call 0.41--0.59 s; Python 3.13.11
  `subprocess` waits with a polling interval growing to 50 ms, matching the
  observed 0.05 s clusters.

## Corrections to archived statements

- October RESULTS/evidence: "these counts show that the experiment exercised
  in-tree tightening" needs qualification: 90 nonroot callbacks per arm were at
  probing nodes (fixed: 360 LPs, no accepted change).
- The adaptive LP reduction is not evidence of better direction choice; the
  call cap binds first.
- Four public models, not two, have unbounded original variables
  (`bayes2_50`, `pointpack08`, `powerflow0009r`, `qp3`).
- September: corrected SCIP solved counts 573 (control) and 563 (`r5`); 441
  for the control on OBBT-ran instances. Time, node, and final-solve summaries
  are labeled as archived originals. Hard-instance SCIP node ratios are
  1.06--1.27 (archived report: 1.06--1.26; `ad0.5` is 1.2654). `ad0.8`
  stops after round one on 46--54%. One-round trajectories: 97 completed
  without change, 7 capped (3 unchanged, 4 productive); 22 productive first
  rounds followed by a completed unchanged second round, 1 more capped. The
  archived "23 converge" and "104 fixed after one round" claims are not used.
  The rule `fp` is named a no-change-or-limit rule, not a fixed-point
  certificate. The 149-trajectory contraction histogram is stated as a
  conditioned sample.
- A post hoc adjustment of the two wrong-answer runs (control 1.157 to 1.162,
  `r5` 1.231 to 1.235) was computed but removed from the manuscript, following
  `review-evidence-r1.md`; the check script still verifies it.

## Review findings addressed

All ten corrections and the smaller clarifications of `review-evidence-r1.md`
were applied: unbounded count; definition of `rho` and the adaptive stops;
aggregate scope of the 6.2%/7.4% shares and exclusion of `J`; "changed search"
replaced by "no additional solve or demonstrated speedup" with an explicit
association-not-causation sentence; probing provenance supported by the SCIP
source; rounded values 39.52, 5.23, 1.00501; LP time floor; pilot gain
definition; discovery-cost wording, conditional lifted monotonicity, and no
claim that SCIP cuts enter the sidecar; the detection example now cites
`ex:round-check`; "LP solve and dual-bound validation"; bilinear-cycle timing
stated per arm; polling stated as an observation rather than an error bound;
group-mean wording and final-solve wording in the appendix.

## Citation requests for the literature lead

The manuscript text currently cites only `hendel2018adaptive` and
`chmiela2023scheduling` from my files. The following claims are stated without
citation and would benefit from vetted sources:

1. Safe LP bounds from inexact duals with interval arithmetic
   (`prop:dual-residual`): Neumaier and Shcherbina (2004), Safe bounds in linear
   and mixed-integer linear programming, Math. Programming 99; Jansson (2004),
   Rigorous lower and upper bounds in linear programming, SIAM J. Optim. 14.
2. Exact rational LP solving as an alternative proposal source: Applegate,
   Cook, Dash, Espinoza (2007), Exact solutions to linear programming problems,
   Oper. Res. Lett. 35; Gleixner, Steffy, Wolter (2016), Iterative refinement for
   linear programming, INFORMS J. Comput. 28.
3. IEEE 754-2019 for round-to-nearest, `nextafter`, and gradual underflow.
4. Algorithm portfolios and interleaving (`thm:interleaving`, `prop:rescue`):
   Huberman, Lukose, Hogg (1997), Science 275; Gomes and Selman (2001), Artificial
   Intelligence 126; Luby, Sinclair, Zuckerman (1993), Inf. Process. Lett. 47.
5. Software and data used in the experiments: the SCIP 10 report
   (`literature/papers/hojny2025-the-scip-optimization-suite-10` exists
   locally), PySCIPOpt (Maher et al. 2016), HiGHS (Huangfu and Hall 2018),
   MINLPLib (Bussieck, Drud, Meeraus 2003, or the library website), OSiL
   (Fourer, Ma, Martin 2010), Gurobi 13 documentation.
6. Benchmark metrics: PAR-2 (SAT competition scoring) and the shifted geometric
   mean (Achterberg 2007, PhD thesis).

No priority claim depends on these; they attribute standard tools.

## Integration notes for the root

- `sections/discussion.tex` says the precursor's "final solves were not
  faster"; the evidence review asked for "the final-solve savings did not
  offset the root and OBBT cost", since the final-solve ratios include
  0.96--0.98. Consider aligning.
- `sections/constraints.tex` line 143 cites `gleixner2017enhancements`, which
  is no longer a key in `references.bib`.
- Foundations item (b) names reference-family products `w_ij`; certificates and
  algorithms use `y_k`.
- The statement that the measured policy uses no all-future certificates now
  appears in certificates (end of `sec:cert-cost`), residual, constraints,
  algorithms (`What the policy uses from the theory`, with reasons), and
  experiments (interpretation). Root may shorten some occurrences.

## Verification actually performed

No numerical experiment, solver, archived analyzer, reference fixture,
project-wide check, or CI status/log was run or inspected. Commands:

1. Read-only inspection (`cat`, `sed`, `grep`, `find`) of the October and
   September reports, frozen source, protocol, manifest, summaries, raw JSON,
   and the September CSV/JSONL; of `research-20261003-adaptive-obbt/solver/
   adaptive_obbt.py`, `theory/certified_driver.py`, `theory/certificates.py`,
   and the saved driver outputs.
2. Standard-library Python heredocs reading archived JSON/CSV/JSONL to derive
   and then recheck the statistics above. The final consolidated check:
   `python3 -I -B /tmp/alg-checks/check_derived.py
   research-20261003-adaptive-obbt/experiments/runs/campaign-01
   research-20260922/iterated-obbt/results` printed
   `DERIVED_STATISTICS_CHECK=ok` (script reproduced below).
3. Inspection of the campaign interpreter's `subprocess.Popen._wait` source via
   `code/minlp_solver_lab/.venv/bin/python -c "import inspect, subprocess; ..."`
   (Python 3.13.11), and of `src/scip/tree.c` in a local SCIP 10.0.3 source tree.
4. LaTeX builds in disposable directories under `/tmp`: a standalone harness of
   my files, and a copy of the integrated manuscript with all existing sections
   and both appendices (`pdflatex`, `bibtex`, `pdflatex` twice). The final copy
   built 91 pages with no undefined references or overfull boxes from my files.
5. `python3 -I -B verification/check_sources.py` on that copy. Its only
   findings were outside my files (the citation key above; earlier, the then
   missing discussion section).

File digests at completion (SHA-256): algorithms
`8980d76a4a5af79fcedb2dfe77e5ca75ee4f67bfd4a62bce18060383918d2cff`, effort
`ca0ba9755fdf4a77c66da96b57c905c97c16ca3cf28a5f4bae9b50b0198dec69`,
experiments
`abe0b42d717253b046e7b59e24031278038086afd213aa5bdde1c252d3845e39`,
precursor appendix
`625d05a78116cd39127adadefdd8b7a6496d47eb11364ced28e9f3ad305b8610`.

### Consolidated check script

```python
"""Re-derive the post-hoc statistics quoted in sections/experiments.tex and
appendices/precursor-study.tex from archived records. Reads files only."""
import csv, glob, json, math, os, statistics as st, sys
OCT = sys.argv[1]  # .../research-20261003-adaptive-obbt/experiments/runs/campaign-01
SEP = sys.argv[2]  # .../research-20260922/iterated-obbt/results
rows = list(csv.DictReader(open(os.path.join(OCT, 'outcomes.csv'))))
summ = json.load(open(os.path.join(OCT, 'summary.json')))
raw = {}
for f in glob.glob(os.path.join(OCT, 'raw', '*.json')):
    r = json.load(open(f)); raw[r['task']['key']] = r
assert len(rows) == 120 and len(raw) == 120

# Table tab:campaign transcription
S = summ['strata']
exp = {('all','native'):(14,13.855,5.957,0.20351), ('all','fixed'):(14,13.988,6.285,0.18438),
       ('all','adaptive'):(14,13.997,6.265,0.18806), ('public','native'):(2,18.964,10.248,0.33408),
       ('public','fixed'):(2,18.999,10.297,0.30209), ('public','adaptive'):(2,19.026,10.324,0.30798),
       ('synthetic','native'):(12,6.192,2.384,0.00767), ('synthetic','fixed'):(12,6.471,2.772,0.00782),
       ('synthetic','adaptive'):(12,6.453,2.733,0.00818)}
for (c,a),(sv,p2,sg,gs) in exp.items():
    d = S[c][a]
    assert d['solved']==sv and round(d['mean_par2_seconds'],3)==p2 and round(d['sgm_process_seconds_shift1'],3)==sg and round(d['mean_gap_score'],5)==gs, (c,a)

# Work table (tab:work)
work = {}
for arm in ('fixed','adaptive'):
    c = dict(); tot = lpt = evt = 0.0; n0 = []; one_node_ok = True
    for k, r in raw.items():
        if r['task']['arm'] != arm: continue
        o = r['outcome']['obbt']; tot += o['time']; lpt += o['lp_time']; cnt0 = 0
        for e in o['events']:
            evt += e['time']
            if e['stop'] == 'unbounded_current_box': key = 'unsupported'
            elif e['depth'] == 0: key = 'root'
            elif e['node'] == 0: key = 'probing'; cnt0 += 1
            else: key = 'tree'
            v = c.setdefault(key, [0,0,0,0.0]); v[0]+=1; v[1]+=e['lp_calls']; v[2]+=e['tightened']; v[3]+=e['time']
            if r['outcome']['nodes'] == 1 and e['depth'] > 0 and e['node'] != 0: one_node_ok = False
        n0.append(cnt0)
    work[arm] = (c, tot, lpt, evt, max(n0), one_node_ok)
fc, ftot, flp, fev, fmax0, fok = work['fixed']; ac, atot, alp, aev, amax0, aok = work['adaptive']
r3 = lambda v: [v[0], v[1], v[2], round(v[3], 3)]
assert r3(fc['root']) == [100,1150,62,8.224] and r3(fc['tree']) == [166,662,50,5.485]
assert r3(fc['probing']) == [90,360,0,3.684] and r3(fc['unsupported']) == [48,0,0,0.068]
assert r3(ac['root']) == [98,336,62,3.554] and r3(ac['tree']) == [505,1203,244,13.287]
assert r3(ac['probing']) == [90,180,2,2.593] and r3(ac['unsupported']) == [48,0,0,0.066]
assert round(ftot-fev,3) == 2.069 and round(atot-aev,3) == 3.623
assert round(ftot,3) == 19.530 and round(atot,3) == 23.123 and round(flp,3) == 12.818 and round(alp,3) == 10.393
assert fmax0 == 3 and amax0 == 3 and fok and aok
assert round(flp-alp,2) == 2.43 and round(ftot-flp,2) == 6.71 and round(atot-alp,2) == 12.73
assert round(1000*(ftot-flp)/404) == 17 and round(1000*(atot-alp)/741) == 17
assert round(1000*flp/2172) == 6 and round(1000*alp/1719) == 6

# Budget-binding runs, stops, counters
def runs(arm): return [r for r in rows if r['arm']==arm]
assert sum(int(r['obbt_calls'])==64 for r in runs('fixed')) == 27
assert sum(int(r['obbt_calls'])==64 for r in runs('adaptive')) == 5
assert sum(int(r['obbt_callbacks'])==24 and r['name']!='qp3' for r in runs('adaptive')) == 20
assert sum(int(r['obbt_callbacks'])==24 and r['name']!='qp3' for r in runs('fixed')) == 0
stops = {arm: {} for arm in ('fixed','adaptive')}
cnt = {arm: dict(proposed=0, tightened=0, lp_failures=0, rejected_cutoffs=0, no_incumbent_calls=0, screened=0) for arm in stops}
for r in raw.values():
    arm = r['task']['arm']
    if arm == 'native': continue
    for e in r['outcome']['obbt']['events']: stops[arm][e['stop']] = stops[arm].get(e['stop'],0)+1
    for k in cnt[arm]: cnt[arm][k] += r['outcome']['obbt'][k]
assert stops['adaptive'] == {'unproductive_pilot':574,'lp_budget':113,'time_budget':6,'unbounded_current_box':48}
assert stops['fixed'] == {'lp_budget':349,'time_budget':7,'unbounded_current_box':48}
assert cnt['fixed'] == dict(proposed=200, tightened=112, lp_failures=4, rejected_cutoffs=0, no_incumbent_calls=124, screened=0)
assert cnt['adaptive'] == dict(proposed=470, tightened=308, lp_failures=26, rejected_cutoffs=0, no_incumbent_calls=120, screened=2)
side = {arm: [float(r['obbt_seconds']) for r in runs(arm)] for arm in ('fixed','adaptive')}
assert round(max(side['fixed']),3) == 1.004 and round(max(side['adaptive']),3) == 1.005
assert sum(t>1 for t in side['fixed']) == 7 and sum(t>1 for t in side['adaptive']) == 11
proc = {arm: sum(float(r['process_seconds']) for r in runs(arm)) for arm in ('native','fixed','adaptive')}
assert round(100*sum(side['fixed'])/proc['fixed'],1) == 6.2 and round(100*sum(side['adaptive'])/proc['adaptive'],1) == 7.4
over = [float(r['process_seconds'])-float(r['call_seconds']) for r in rows]
assert round(min(over),2) == 0.41 and round(max(over),2) == 0.59
assert round(max(float(r['call_seconds']) for r in rows),3) == 10.093 and round(max(float(r['process_seconds']) for r in rows),3) == 10.606
assert sum(r['status']=='timelimit' and float(r['call_seconds'])>10 for r in rows) == 78

# Solved-run totals and PAR-2 deltas
solved = {arm: [r for r in runs(arm) if r['solved']=='True'] for arm in ('native','fixed','adaptive')}
assert all(len(v)==14 for v in solved.values())
keyset = {arm: {(r['name'],r['seed']) for r in v} for arm, v in solved.items()}
assert keyset['native'] == keyset['fixed'] == keyset['adaptive']
tot = {arm: round(sum(float(r['process_seconds']) for r in v),2) for arm, v in solved.items()}
assert tot == {'native':34.21,'fixed':39.52,'adaptive':39.88}, tot
assert round(sum(float(r['obbt_seconds']) for r in solved['fixed']),2) == 5.23
assert round(sum(float(r['obbt_seconds']) for r in solved['adaptive']),2) == 5.72
P = summ['paired']['all']
assert round(P['fixed']['mean_paired_par2_delta'],3) == 0.133 and round(P['adaptive']['mean_paired_par2_delta'],3) == 0.142
assert (P['adaptive']['par2_wins_5percent'],P['adaptive']['par2_losses_5percent']) == (2,11)
assert (P['fixed']['par2_wins_5percent'],P['fixed']['par2_losses_5percent']) == (1,10)
by = {(r['name'],r['seed'],r['arm']): r for r in rows}
wins = [(r['name'],r['seed']) for r in runs('adaptive') if float(r['par2']) < 0.95*float(by[(r['name'],r['seed'],'native')]['par2'])]
assert sorted(wins) == [('synthetic_bilinear_cycle_12_20261003','0'),('synthetic_bilinear_cycle_12_20261003','1')]
for arm in ('fixed','adaptive'):
    for s in (0,1):
        ev = raw[f'synthetic_bilinear_cycle_12_20261003__{arm}__{s}']['outcome']['obbt']['events']
        root = [(e['reason'], e['tightened']) for e in ev if e['depth']==0]
        assert root == [('first_visit',0),('incumbent_improvement',6),('domain_reduction',6)], root
        assert raw[f'synthetic_bilinear_cycle_12_20261003__{arm}__{s}']['outcome']['nodes'] == 1
    assert all(raw[f'synthetic_bilinear_cycle_12_20261003__native__{s}']['outcome']['nodes'] == 7 for s in (0,1))

# Gap statements
pub = lambda arm, ex: [float(r['gap_score']) for r in runs(arm) if r['kind']=='public' and r['name'] not in ex]
g = {arm: round(st.mean(pub(arm, {'bayes2_50'})),3) for arm in ('native','fixed','adaptive')}
assert g == {'native':0.274,'fixed':0.282,'adaptive':0.289}, g
for arm in ('fixed','adaptive'):
    losses = [(r, by[(r['name'],r['seed'],arm)]) for r in runs('native') if r['normalized_gap'] and by[(r['name'],r['seed'],arm)]['normalized_gap']
              and float(by[(r['name'],r['seed'],arm)]['normalized_gap']) > float(r['normalized_gap'])+1e-4]
    assert len(losses) == 12
    assert sum(float(b['dual_min']) < float(a['dual_min']) for a,b in losses) == 11
b2 = [r for r in rows if r['name']=='bayes2_50']
assert all(round(float(r['primal_min']),3) == (6.825 if r['arm']=='native' else 0.520) for r in b2)
q = {r['arm']: r['dual_min'] for r in rows if r['name']=='qp3' and r['seed']=='1'}
assert q['fixed'] != q['native'] and int(raw['qp3__fixed__1']['outcome']['obbt']['lp_calls']) == 0

# September corrections
fo = list(csv.DictReader(open(os.path.join(SEP, 'final_outcomes.csv'))))
sc = [r for r in fo if r['solver']=='scip']
def solved_count(arm): return sum(r['solved']=='True' and r['wrong']=='False' for r in sc if r['arm']==arm)
assert solved_count('pipe-none') == 573 and solved_count('pipe-r5') == 563
def sgm(ts): return math.exp(sum(math.log(t+1) for t in ts)/len(ts))-1
base = {(r['name'],r['seed']): float(r['total']) for r in sc if r['arm']=='base'}
for arm, old, new in (('pipe-none',1.157,1.162),('pipe-r5',1.231,1.235)):
    a = {(r['name'],r['seed']): r for r in sc if r['arm']==arm}
    idx = sorted(a)
    t_old = [float(a[k]['total']) for k in idx]; t_new = [600.0 if a[k]['wrong']=='True' else float(a[k]['total']) for k in idx]
    tb = [base[k] for k in idx]
    assert round(sgm(t_old)/sgm(tb),3) == old and round(sgm(t_new)/sgm(tb),3) == new
wrong = sorted((r['name'],r['arm'],r['seed'],round(float(r['total']),1)) for r in sc if r['wrong']=='True')
assert wrong == [('crudeoil_lee1_05','pipe-none','1',30.8),('crudeoil_lee1_09','pipe-r5','1',105.0)], wrong
base_rows = {(r['name'],r['seed']): r for r in sc if r['arm']=='base'}
hard = {n for (n,s),r in base_rows.items() if float(r['total'])>=10 or r['solved']!='True'}
assert len(hard) == 122
def sgm10(ts):
    ts = list(ts); return math.exp(sum(math.log(t+10) for t in ts)/len(ts))-10
nr = []
for arm in ['pipe-'+x for x in ('r1','r5','ad0.5','ad0.8','fp')]:
    a = {(r['name'],r['seed']): r for r in sc if r['arm']==arm and r['name'] in hard}
    both = [k for k in a if a[k]['solved']=='True' and base_rows[k]['solved']=='True']
    nr.append(sgm10(float(a[k]['nodes']) for k in both)/sgm10(float(base_rows[k]['nodes']) for k in both))
assert round(min(nr),2) == 1.06 and round(max(nr),2) == 1.27

# Added after review: per-run sidecar shares, exact maximum, September trajectory counts
shares = {arm: max(float(r['obbt_seconds'])/float(r['process_seconds']) for r in runs(arm)) for arm in ('fixed','adaptive')}
assert 0.40 < shares['fixed'] < 0.41 and 0.40 < shares['adaptive'] < 0.41, shares
assert round(max(side['adaptive']),5) == 1.00501
one = dict(done0=0, cap0=0, capch=0); two = dict(done=0, cap=0); nk = 0
for line in open(os.path.join(SEP, 'obbt.jsonl')):
    r = json.loads(line)
    if r.get('status') != 'ok' or r.get('src') != 'known': continue
    nk += 1; H = r['trajs']['full']['hist']
    if len(H) == 1:
        h = H[0]; key = ('cap0' if h['nchanged'] == 0 else 'capch') if h['capped'] else ('done0' if h['nchanged'] == 0 else None)
        one[key] += 1
    elif len(H) == 2 and H[0]['nchanged'] > 0 and H[1]['nchanged'] == 0:
        two['cap' if H[1]['capped'] else 'done'] += 1
assert nk == 339 and one == dict(done0=97, cap0=3, capch=4) and two == dict(done=22, cap=1), (one, two)

assert round(tot['fixed']-tot['native'],2) in (5.31,5.32) and round(sum(float(r['process_seconds']) for r in solved['fixed'])-sum(float(r['process_seconds']) for r in solved['native']),2) == 5.32
assert round(sum(float(r['process_seconds']) for r in solved['adaptive'])-sum(float(r['process_seconds']) for r in solved['native']),2) == 5.67
assert 0.33 < (ftot-flp)/ftot < 0.35 and 0.55 < (atot-alp)/atot < 0.56
print('DERIVED_STATISTICS_CHECK=ok')
```
