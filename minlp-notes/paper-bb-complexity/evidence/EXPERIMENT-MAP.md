# Experiment map: archived computational evidence for the branch-and-bound complexity manuscript

Date: 2026-10-05. Scope: the archived computations that the manuscript may
cite, with their configurations, provenance, supported and unsupported claims,
caveats, display proposals and companion contents. No experiment, optimizer or
instance generator was rerun. The audit consisted of reading notes, logs,
summaries, protocols and code, plus accounting arithmetic on retained outputs
(Section 10 lists every command). This file is evidence for the writers and
reviewers; it is not submission text.

Source snapshots. All sources are committed and the working tree is clean for
them: `research-20260928b/` at `a2abf970c` (2026-09-29) and
`research-20260929/` at `a0b2eebe6` (2026-10-01). Paths below are relative to
the repository root unless stated.

Study labels used throughout:

| Label | Study | Primary note |
|---|---|---|
| S1 | SCIP node counts against predicted tolerance exponents (20 synthetic instances) | `research-20260928b/bb-complexity/solver-validation/scip-node-exponents.md` |
| S2 | Branching-point parameters of SCIP on 57 MINLPLib instances | `research-20260928b/bb-complexity/minlplib-branching/branching-point-study.md` |
| S3 | Safe ("robust") branching points: synthetic kinks in SCIP and a second MINLPLib campaign | `research-20260928b/bb-complexity/robust-branching-points/robust-branching.md` |
| S4 | Random sparse regression: perspective B&B, conflict cliques, stronger relaxations | `research-20260928b/bb-complexity/sparse-regression/phase-transition.md` (Section 6), `.../stronger-relaxations/thresholds.md` (Section 7) |
| S5 | Random binary least squares (MIMO): box relaxation, C1, trees, SDP | `research-20260928b/bb-complexity/binary-least-squares/certification-thresholds.md` (Section 7) |
| S6 | Path-structured scaling: single-tree SCIP versus a chain DP branch and bound | `research-20260929/computation/scaling-study.md`, `tables.md` |
| S7 | Single-tree termwise McCormick on the path family: toy B&B and SCIP minor cuts | `research-20260929/theory-face-exact/face-exact-exponential.md` (Section 7) |
| S8 | Supporting proof-model computations (inventory only) | several notes; Section 4 |

Units used below. SCIP "nodes" are processed nodes (`SCIPgetNNodes` in S1,
`getNTotalNodes` in S2/S3); theory counts "leaves" of a certificate; the S6
prototype counts "pair bounds"; S4/S5 B&B count nodes of their own Python
codes. SCIP times are CPU seconds; S6 prototype times are Python wall-clock
seconds on a loaded machine. These units must never be mixed in one ratio.

## 1. Main computational conclusions

1. **The tolerance exponent is set by the geometry of the near-optimal set, and
   a real solver shows it once its search matches the model (S1).** On 20
   synthetic instances with exact optima, SCIP 10.0.2 with best-first search,
   the optimum supplied and heuristics off (setting `model`) gives log-type
   growth at isolated nondegenerate minima (9, 10, 40, 92 nodes per decade for
   iso2, iso2c, iso3, iso4), fitted slopes 0.50–0.52 for one-dimensional
   optimal sets, 1.01–1.05 for two-dimensional sets (2–3 decades only), and
   slopes near `n/2 - sum_i 1/q_i` for flat quartic directions. No run on the
   seven instances where the integral bound applies has fewer final leaves than
   the bound (smallest ratio 1.59).
2. **Default-solver departures have identified causes, and each points to the
   relaxation or its representation, not to branching (S1).** Plunging
   saturates counts at the feasibility-tolerance scale; objective-cutoff
   propagation on an instance outside the gap hypothesis gives 15 nodes for
   every `eps`; shared auxiliary variables (condisk2), an unexpanded square
   (ring2) or variable-lock presolve (mccaxis2) give 1 node where the expanded
   or unshared form follows `eps^(-1/2)`.
3. **Branching changes constants, not exponents, except on face-exact
   (McCormick) instances (S1, S3).** On the aligned McCormick instance
   mccaxis2 at `eps = 1e-7`: LP-point branching 3 nodes, x1-only bisection 45,
   bisection on both variables 10,469. On the transversal instance mccdiag2 no
   setting is `O(1)`.
4. **The branching-point theory does not transfer to MINLPLib as a rule change
   (S2, S3).** Moving SCIP's split to the LP point is neutral within seed noise
   (1.03, CI 0.83–1.26); safe variants are neutral (randomized clamp
   0.95–1.00; recentring 0.94 against the same-selection clip, 0.92 against
   SCIP's default); removing the clamp doubles node counts (2.19 and 2.00, in
   two separate campaigns) through LP values that sit on variable bounds; pure
   midpoint splitting is 1.15 times worse (p = 0.009). Seed noise is large: the
   median per-instance max/min ratio over three seeds is 1.51 under default.
5. **The model-level branching-point results do appear in SCIP on synthetic
   kinks (S3).** The clamp's trap shows (1D kink at `a = 1/6`: 3, 7, 9, 13
   nodes at `eps = 1e-2 ... 1e-8`; McCormick kink: 7,190 nodes at `1e-8`),
   recentring stays bounded (5 nodes in 1D; 16–88 on every McCormick kink), and
   the randomized clamp is heavy-tailed under widest-side selection (mean 766,
   range 7–3,443, against 26 for the fixed clamp at `a = 0.0102`).
6. **Random designs show finite-size transitions that agree with the theory in
   direction but not yet in constants (S4, S5).** Sparse regression: linear
   variable-branching trees are certified (condition C1) in every run from
   `alpha ≈ 1.5–1.75`, while the root is certified exact in at most 4 of 8 runs
   in any cell; observed C1 sits at about half the first-order constant. MIMO:
   the box relaxation is root-exact only with the predicted probability
   (`2^-N`), C1 needs SNR linear in `N` (transition near `rho/N ≈ 0.4–0.5` at
   `N <= 800` against 0.25 asymptotically), and most-fractional trees at
   `rho = 4 log N` grow 44, 97, 509, 15,765 for `N = 32, 64, 128, 256`.
7. **Stronger relaxations help at moderate `p/n` and lose their advantage as
   `p/n` grows (S4), while in MIMO the SDP removes the box relaxation's gap for
   tall systems (S5).** At `n = 20` the optimal-perspective SDP closes 51%,
   25%, 12%, 3% of the perspective root gap at `p = 40, 80, 160, 320`; at
   `n = 40`, `p = 3200` (inside the C1 window) explicit points certify that
   the pairwise lifted hull `L_2` is root-inexact in 4 of 6 runs. For
   `beta = 2` the SDP becomes exact at a median `rho* ≈ 4.4 log N`.
8. **Problem structure matters by orders of magnitude on path-structured
   problems (S6, S7).** On a family with a certified unique, interior,
   nondegenerate minimizer, SCIP's node count grows about 5 times per two
   added variables on `n = 4..10`, no tested setting solves `n = 14` within
   300 CPU s, and a decomposition-aware DP branch and bound with valid bounds
   solves the same instances to the same absolute tolerance up to `n = 8192`
   with fitted work `n^1.6–1.8`. A termwise-McCormick toy B&B on the same path
   family grows 2.7–3.1 per variable against the proved base 5/3; SCIP's
   default PSD-minor cuts, which lie outside the theorem's relaxation class,
   lower its rate to 2.1–2.3 per variable.
9. **What the computations do not show.** No count is certified in exact
   arithmetic (except where stated in S3 and S7 rechecks); no asymptotic
   constant is measured; no exponential growth is proved from solver data; no
   general speedup or solver recommendation follows; all solver runs use one
   solver family (SCIP 10.0.x via PySCIPOpt 6.2.1) on one shared machine.

## 2. Study inventory

| ID | Question | Code and solver | Instances | Runs | Independent review | Audit here |
|---|---|---|---|---|---|---|
| S1 | Do SCIP node counts follow the predicted `eps`-exponents? | SCIP 10.0.2, SoPlex 8.0.2, Ipopt (version not recorded), PySCIPOpt 6.2.1 | 20 synthetic CIP instances, exact optima | 2,134 | None (the synthesis says "not independently reproduced"; the cutoff review only cross-read three numbers) | status/run/time/warning accounting; leaf-ratio recomputation; slope and factor checks against `summary.md` |
| S2 | Does splitting closer to the LP point help SCIP on real instances? | SCIP 10.0.2, SoPlex 8.0.2, Ipopt 3.14.19, PySCIPOpt 6.2.1 | 57 nonconvex MINLPLib instances (1–20 s under default) | 1,927 recorded (855 main, 171 optional, 228 sweep, 486 screen, 187 trace) | None of the aggregates; default and LP-point node counts reproduced exactly by S3's separate runs, confirmed by S3's reviewer | all seven aggregate ratios and CIs recomputed from `runs.jsonl`; subgroup figures recomputed; trace median recomputed |
| S3 | Is there a branching-point rule safe against boundary LP points and competitive on kinks? | same software as S2; ctypes branching plugin | 57 MINLPLib (same set); 2 synthetic kink families × 8 positions | 2,052 MINLPLib + 3,840 synthetic; exact-model simulations | Yes (`research-20260928b/reviews/robust-branching-review.md`, closing audit A item 3): 11 MINLPLib pair ratios recomputed, plugin counters and 1e-8 synthetic tables confirmed | spot checks of tables against `results/summary.md` |
| S4 | Where are root exactness and C1 for perspective B&B at finite size; do stronger relaxations move them? | Python 3.13, NumPy 2.5, SciPy 1.18, Clarabel 0.11; cvxpy 1.9.3 and SCS for SDPs | Gaussian designs, `p <= 3200`, `k <= 20` | see Section 3.4 | Tables 6.1–6.3 recomputed (75/75 decisions); 6.4–6.5 light check; 6.6 never checked; stronger-relaxation computations "reproducible" per review and recheck | Table 6.6 checked against raw data (one text error found, Section 6) |
| S5 | Root exactness, C1, tree sizes and SDP thresholds for box-relaxation B&B in MIMO detection | Python 3.13, NumPy 2.5, SciPy 1.18, CVXPY 1.9, Clarabel 0.11 | Gaussian `H`, `N <= 1600` | see Section 3.5 | Two reviews, recheck and closing audit B; tables unchanged by review; Fincke–Pohst comparison reproduced exactly by the recheck | tables and check logs read against the note |
| S6 | Single-tree SCIP versus decomposition-aware DP on treewidth-1 instances | SCIP 10.0 (patch not recorded) via PySCIPOpt 6.2.1; Python prototype | probe3 chain (amp 0.3, 0.2), lot-sizing chain | several batches (Section 3.6) | Yes (`research-20260929/reviews/computation-review.md`): SCIP counts reproduced exactly on 10 reruns; prototype bounds validated by an independent method; the post-review revision was not rechecked | geometric means, fits and local exponents recomputed from `data/` |
| S7 | Does single-tree B&B with termwise McCormick need exponentially many leaves on a path; what does SCIP do? | Python toy B&B with certified node bounds; SCIP 10 via PySCIPOpt 6.2.1 | PROGRAM path family (`b = 0.8`, `kappa = 0.1` or 0) | see Section 3.7 | Review and recheck (exact rational B&B reproduced counts, no flipped pruning) | tables read against logs and note |

## 3. Study records

### 3.1 S1: SCIP node counts against the predicted tolerance exponents

**Question.** For relaxations with gap at least `alpha sum_i (y_i - l_i)(u_i - y_i)`
(hypothesis (G_alpha)), the theory predicts `Theta(log(1/eps))` at isolated
nondegenerate minima, `Theta(eps^(-p/2))` for a `p`-dimensional optimal set,
`eps^(-(n/2 - sum_i 1/q_i))` for growth `sum_i |t_i|^(q_i)`, and for
McCormick relaxations a rule-dependent rate governed by alignment of the
optimal set with box faces. Does SCIP 10 follow these rates?

**Configuration.**
- SCIP 10.0.2 (optimized, 8-byte precision), SoPlex 8.0.2, Ipopt as NLP solver
  (version not recorded in `results/meta.json`), PySCIPOpt 6.2.1, Python
  3.13.11, NumPy 2.5.1, mpmath 1.3.0, Linux 6.18 (WSL2) x86_64. Single-threaded
  runs, at most 4 in parallel; total SCIP solving time 1.76 CPU hours over
  2,134 runs (recomputed).
- Formulation `min t s.t. f(x) - t <= 0` (+ constraints) over a box, written as
  CIP so that SCIP sees a fixed expression form.
- Every run: `limits/absgap = eps`, `limits/gap = 0`, `numerics/feastol = 1e-9`
  (with `epsilon 1e-12`, `sumepsilon 1e-10`, `dualfeastol 1e-9`),
  `limits/nodes = 100000`, `limits/time = 120 s`, `randomization/randomseedshift = 0`.
  `eps` runs from `1e-1` to `1e-7` in half-decade steps, so the smallest `eps`
  is 100 times the feasibility tolerance.
- 23 settings. The key ones: `default`; `model` = best-first
  (`nodeselection/bfs/stdpriority = 1e6`, plunge depths 0), heuristics off,
  known optimum supplied (`t = f(x*) + 1e-15`); `modelnoprop`; `toy` = `model`
  + no propagation + widest-side bisection + presolve off; `lppoint`
  (`branching/midpull = 0`); `midpoint`; `widestbisect`; `noprop`;
  `nocutoffprop`; `noweakdual` (`misc/allowweakdualreds = False`); `obbtall`;
  `obbtoff`; `noexpand` (`expr/pow/expandmaxexponent = 1`); `withlocks`;
  `smallstreps`; x1-priority and external-branching variants on mccaxis2.
- Fits: least squares of `log10(nodes)` on `log10(1/eps)`; tail slope over the
  (up to) 5 smallest `eps <= 1e-3` without a limit; wide slope over every such
  run with `eps <= 1e-2`; "nodes per decade" for logarithmic growth.

**Instances.** iso2, iso3, iso4, iso2c (isolated minima); isofbbt2 (the cutoff
review's instance, outside (G_alpha)); linediag2, lineaxis2, ring2 (`p = 1`);
sphere3, plane3 (`p = 2`); qflat1, qflat2a, qflat2b, qflat3 (quartic growth);
mccaxis2, mccdiag2 (McCormick, aligned and transversal); conexp2, conexp4
(optimal set on a curved active constraint); condisk2, condisk2soc (shared
subexpressions). Optimal values are exact by construction; `f(x*) - f* <= 2.2e-16`
in 40-digit arithmetic (`results/instances_check.log`). Boxes are asymmetric.
A root-relaxation check shows SCIP's root bound equals an independent
secant/McCormick bound within `1e-9` on four instances and is `9.5e-5` lower on
linediag2 (`results/relax_check.log`).

**Results under `model`** (`results/summary.md`; counts at `1e-1, 1e-2, ..., 1e-6`
or `1e-7`):

| Class | Instances | Prediction | Fitted tail/wide slope (`model`) | Per-decade node factor |
|---|---|---|---|---|
| isolated minimum | iso2, iso2c, iso3, iso4 | `log(1/eps)` | 0.06–0.10; 9, 10, 40, 92 nodes per decade | additive |
| `p = 1` | linediag2, lineaxis2, ring2, mccdiag2, conexp2 | 1/2 | 0.50–0.52 | 2.7–4.0 (predicted 3.16) |
| `p = 2` | sphere3, plane3, conexp4 | 1 | 1.01–1.05 (2–3 decades) | 9.0–11.1 (predicted 10) |
| `q = (2,4)`, `(4)` | qflat2a, qflat1 | 1/4 | 0.27, 0.31 (bisection `toy`: 0.24, 0.25) | qflat2a 1.8–2.1 (predicted 1.78) |
| `q = (4,4)`, `(2,4,4)` | qflat2b, qflat3 | 1/2 | 0.49–0.51 | 2.8–3.3 |

Example counts (`model`): linediag2 89, 359, 1115, 3805, 11893, 38073;
ring2 99, 353, 1155, 3769, 11857, 37439; sphere3 79, 747, 7475, 76699;
iso2 15, 25, 33, 45, 55, 63, 75. Per-decade factors were recomputed here from
these rows (p = 1 range 2.68–4.03; p = 2 range 9.0–11.1).

On the three `p = 1` instances linediag2, lineaxis2 and ring2, 35 of 39
setting sequences (all but `noexpand`) have a wide slope in 0.43–0.60; the four
exceptions are widest bisection under the default selector (0.63–0.66, three
instances) and `midpoint` on linediag2 (0.39). Verified here from the summary.

**Integral lower bound.** The bound
`(n/pi^2)^(n/2) prod_i alpha_i^(1/2) integral (f - f* + eps)^(-n/2)` (the
anisotropic form of the constrained note's Theorem 3.1; the S1 note calls it
"Theorem B") applies to seven instances. Final leaves (open nodes at
termination plus processed leaves) never fall below it; the smallest ratio is
1.59 (qflat1). Under `model` the ratio stays within narrow ranges over six
decades: iso2 6.8–9.8, linediag2 15.9–23.7, lineaxis2 27.9–40.7, qflat2a
6.8–9.4 (the note says 7.4–9.4; see Section 6), qflat2b 6.2–9.7.

**Departures of default SCIP and their causes.**

| Departure | Evidence | Cause identified in the note |
|---|---|---|
| Counts stop depending on `eps` at isolated minima | iso2 95 nodes from `1e-6`, iso3 341 from `1e-4` (status optimal) | plunging dives to the feasibility-tolerance scale (incumbent about `9e-10` below `f*`) |
| Short-window slope below 1/2 for `p = 1` | default tail 0.33–0.36 on linediag2/lineaxis2 (wide 0.46–0.53); excess over `model` 3.6, 2.2, 1.7 times at `1e-4, 1e-5, 1e-6` | default node order processes nodes already within `eps`; `model` also supplies the incumbent and turns heuristics off (three changes not separated) |
| `eps`-independent count | isofbbt2: 15 nodes for every `eps` in `1e-2 ... 1e-7`; 37 with `noweakdual` | objective-cutoff propagation; isofbbt2 violates (G_alpha) (secant gap `O(w^4)`), so no proved bound is escaped |
| 1 node | condisk2 (every setting); condisk2soc (default, `model`); ring2 `noexpand` | relaxation exact on the optimal set through shared auxiliaries, FBBT on a shared sum, or an unexpanded convex outer function; `nonlprop` restores slope 0.54–0.57 on condisk2soc |
| 1 node | mccaxis2 under SCIP's default `checkvarlocks = t` | variable-lock presolve makes `x2` binary (the problem changes); McCormick runs use `checkvarlocks = d` |

**McCormick instances** (counts at `1e-1 ... 1e-7`): mccaxis2 `lppoint` 1, 3, 3,
3, 3, 3, 3; x1-only bisection (`xprioexttoy`) 5, 11, 17, 25, 31, 37, 45;
bisection on both variables (`exttoy`) 7, 27, 91, 379, 1017, 2803, 10469;
widest bisection (`toy`) 5, 17, 59, 367, 1363, 4677, 21191. mccdiag2: best-first,
default and LP-point settings give slopes 0.49–0.59; `model` reaches 3505 at
`1e-7`; no setting finds an `O(1)` certificate. Default mccaxis2 stalls at 5
nodes until `eps` falls below the dual-bound offset `2.4e-6`, then jumps (211,
1041); the cause of the stall was not identified.

**Component effects.** Presolve: identical counts on all 9 core instances. OBBT
at every node: 1.5–3.4 times fewer nodes at `1e-3` (linediag2 961 against
3291), exponent unchanged. Branching point (midpoint, widest bisection): 1.5–5
times more nodes than default at `1e-3`; no exponent change under best-first.

**Numerics.** Status counts (recomputed): 1,655 gap limit, 420 exhausted trees
(status optimal), 59 node limit, 0 time limit; no errors or restarts. Incumbents
lie up to `5.5e-9` below `f*` (constraint violation within `feastol`); no dual
bound exceeds `f*` by more than `1e-15`. SoPlex refused LP tolerances below
`1e-10` in 219 runs (up to 33,456 messages in one run). With the default
`feastol = 1e-6`, linediag2 ends at 38,766 nodes for both `eps = 1e-6` and
`1e-8` (tolerance-bound); with `1e-9`, 13,751 at `1e-4` and 66,001 at `1e-6`
(`results/tolerance_probe.log`). Five reruns reproduced node and LP-iteration
counts exactly (`results/determinism_check.log`).

**Supported claims.** On these instances and this SCIP version, node counts
follow the predicted tolerance exponents once node order, incumbent and
heuristics match the theory's model; branching rules change constants, not
exponents, outside the face-exact case; each default-solver departure has a
named mechanism (plunging, node order, cutoff propagation, shared
subexpressions/FBBT, expansion of squares, variable-lock presolve); the
McCormick alignment regimes (3 nodes, `log`, `eps^(-1/2)`) appear when the
branching rule is controlled.

**Unsupported claims.** That SCIP satisfies (G_alpha) or the theorems'
hypotheses in general; any statement about MINLPLib or industrial instances;
certified counts; that the fits prove the rates; speed comparisons. "Default
SCIP follows the exponents" holds only on the wide window for `p >= 1`
instances, not at isolated minima.

**Caveats.** One solver version; small instances; fits over 1.5–6 decades and
only 2–3 decades for `p = 2`; qflat1 under `model` gives 0.31–0.33 against 0.25
(bisection gives 0.24–0.25), and whether SCIP's LP-biased rule loses a slowly
growing factor was not resolved; counts in the 420 runs that exhausted the
tree do not depend on `eps`; `model` conflates three changes; `limits/absgap`
is a global stopping rule, not a pruning tolerance.

**Artifacts.** `solver-validation/{instances.py, run_one.py, sweep.py,
analyze.py, thm_bounds.py, relax_check.py, tolerance_probe.py}`, `cip/`,
`transformed/`, `results/{runs.jsonl (2.3 MB), summary.md, runs_fits.json,
thm_bounds.json, meta.json, *_check.log, *_probe.log, sweep*.log}`.

### 3.2 S2: Branching-point parameters of SCIP on MINLPLib

**Question.** The theory predicts that splitting closer to the relaxation (LP)
point, with less midpoint pull and less clamping, reduces node counts on sharp
or face-aligned instances. Does this hold for SCIP 10 on real nonconvex
instances?

**Configuration.**
- SCIP 10.0.2, SoPlex 8.0.2, Ipopt 3.14.19, PySCIPOpt 6.2.1, Python 3.13.11;
  Intel Xeon w5-2565X (36 logical CPUs), Linux 6.18 (WSL2); single-threaded,
  OMP/OpenBLAS/MKL threads 1, at most 6 runs in parallel, `timing/clocktype = 1`
  (CPU), `limits/memory = 4000` MB, otherwise SCIP defaults including
  `limits/gap = 0` and `limits/absgap = 0` (`results/meta.json`).
- The split-point formula (`SCIPbranchGetBranchingPoint`, `cons_nonlinear.c`,
  `branch_pscost.c`) was read in the SCIP **10.0.3** source while the runs used
  the **10.0.2** binary; no difference was checked.
- Settings (midpull, midpullreldomtrig, clamp): `default` (0.75, 0.5, 0.2);
  `lp` (0, ·, 0.2); `lp_noclamp` (0, ·, 0); `mix_noclamp` (0.75, 0.5, 0);
  `mid` (1, 0, ·); optional seed-0 settings `trig0` (0.75, 0, 0.2), `couenne`
  (0.75, 0, 0.05; emulates only Couenne's point rule), `lp_c05` (0, ·, 0.05).
- Seeds: seed 0 is SCIP's default; seed `k = 1, 2` sets
  `randomization/permutationseed = k`, `permutevars = TRUE`,
  `randomseedshift = k`.
- Limits: 120 CPU s for main and optional runs; 60 s for the absolute-gap sweep
  (`limits/absgap = delta * max(1, |best known|)`, `delta` in `1e-2, 1e-4, 1e-6`);
  30 s for diagnostic traces.
- Aggregation: per instance, shifted geometric mean over seeds (shift 10
  nodes); across instances, shifted geometric mean; 95% CI by bootstrap over
  instances (5,000 resamples, seed 1); two-sided Wilcoxon signed-rank p
  (normal approximation); unsolved runs counted at their node count at the
  limit (understates losses); win/loss = per-instance ratio beyond 10%;
  "separated" = all 3 seeds of one setting beyond all 3 of the other by >10%.

**Instances.** Local MINLPLib copy (1,632 OSiL files; metadata
`code/minlp_solver_lab/instances/instancedata.csv`, 1,633 rows, SHA-256 prefix
`dbe97fdc90ba6b66`). Filter (convex flag, solved status, continuous variable in
a nonlinear term, at most 1,000 variables/constraints) leaves 486 candidates;
a 20 s default screen solves 360; a family cap of 3 per family gives **57
instances** (`selected.txt`): 18 NLP, 13 MBNLP, 12 QCP, 7 MBQCP, 2 MIQCP, 2 QP,
1 MBQCQP, 1 QCQP, 1 MINLP; 24 with integer variables; median 49 variables
(1–936); default screen time median 3.3 s (1.0–19.3 s); default nodes median
2,326 (59–79,035). Instances needing 20–120 s under default are not
represented. Five instances do no continuous branching at all.

**Run accounting** (verified): 855 main (5 settings × 3 seeds × 57) + 171
optional + 228 sweep = 1,254 in `results/runs.jsonl`; 486 screen; 171 + 16
trace; total 1,927 recorded runs; 5.6 CPU hours. 28 trace records from a
stopped first batch were discarded (a runner bug overwrote a field); the main
records were rewritten once to rename that flag, with no value changes.

**Results** (`results/summary.md`; ratios recomputed here from
`results/runs.jsonl`, Section 10):

| Setting | Seeds | Nodes vs default | 95% CI | Wilcoxon p | Wins / losses (>10%) | Separated wins / losses | Unsolved runs (of 171) |
|---|---|---|---|---|---|---|---|
| `lp` | 0–2 | 1.033 | 0.83–1.26 | 0.18 | 13 / 22 | 4 / 5 | 5 |
| `lp_noclamp` | 0–2 | 2.185 | 1.43–3.39 | <0.001 | 11 / 32 | 5 / 19 | 33 (32 time limit, 1 LP-solver crash) |
| `mix_noclamp` | 0–2 | 1.348 | 1.03–1.85 | 0.75 | 9 / 14 | 2 / 7 | 17 |
| `mid` | 0–2 | 1.150 | 1.03–1.28 | 0.009 | 12 / 30 | 5 / 8 | 2 |
| `trig0` | 0 | 1.139 | 0.96–1.41 | 0.046 | 12 / 23 | – | 1 (of 57) |
| `couenne` | 0 | 1.014 | 0.90–1.13 | 0.14 | 12 / 20 | – | 0 |
| `lp_c05` | 0 | 1.225 | 0.92–1.61 | 0.087 | 14 / 27 | – | 0 |
| `default` | – | 1 | – | – | – | – | 1 |

- Restricted to instances where every run of both settings solved: `lp` 0.95
  (0.78–1.10, 53 instances), `lp_noclamp` 1.08 (0.81–1.40, 41), `mix_noclamp`
  1.00 (49), `mid` 1.15 (1.03–1.29, p = 0.011, 55). The no-clamp penalty comes
  from failures; excluding them is a selection effect.
- 44 continuous-heavy instances: `lp` 1.04, `lp_noclamp` 2.73, `mix_noclamp`
  1.48, `mid` 1.19 (1.04–1.36, p = 0.013).
- Seed noise under default: per-instance max/min over 3 seeds has median 1.51,
  75th percentile 2.04, 90th 5.65; two seeds of the same setting differ by
  >10% on 42 of 57 instances; null comparisons: seed 1 vs 0 gives 19 wins / 23
  losses (ratio 0.999), seed 2 vs 0 gives 19 / 19 (1.021). Extremes: ex14_1_7
  solves at the root for seeds 1, 2 and needs 167–26,262 nodes for seed 0;
  st_e03 default 79,035 / 54,205 / 1,063,341.
- Mechanism of clamp removal: on 11 of the 16 instances with an `lp_noclamp`
  failure, the branching variable's LP value lies on its bound in 42–100% of
  bounded continuous branchings (including pseudo-solution nodes, where the
  value is a bound); without the clamp SCIP splits about
  `1.01e-9 max(1,|l|,|u|)` from the bound, producing chains of nearly identical
  nodes. ex4_1_5 (infinite bounds): a single path of 378,210 nodes at depth
  378,209 in the main seed-0 run, with every branching through the
  external-candidate `pscost` path (a 30 s re-trace has 102,573 nodes at depth
  102,572).
- The default is already close to the LP point deep in the tree: the pull is
  scaled by the local/global width ratio below 1/2; a per-instance median of
  70% of continuous splits happen at such widths (recomputed: 0.701 over 52
  instances with bounded continuous branchings).
- Where the theory's direction shows: on the 19 continuous instances with at
  most 20 variables, `mid` needs 1.43 times the nodes of `lp` (CI 1.03–2.22,
  p = 0.036), while `lp`/default is 0.81 (CI 0.50–1.12; not significant)
  (recomputed: 1.436 and 0.811, same CIs). mathopt5_4 (1 variable): `lp`
  543/543/537 against default 31,282/31,297/31,249 and `mid` 18,204/18,474/18,673;
  prob09: `lp` about 1,700 against about 4,900. Both are zero-optimum
  instances closed at the feasibility-tolerance scale (incumbent about `-9.7e-7`).
- Where it does not: gsg_0001 (44 variables) default 5,761/7,209/6,811, `lp`
  184,845 (limit)/141,397/196,294 (limit); 42% of `lp` splits land on the
  clamp; nous1 `lp` 4,631/4,251/4,349 against default 2,642/1,457/2,705.
- Tolerance sweep (seed 0, 13 instances solved by every setting at every
  `delta`): `lp`/default 0.95, 0.86, 0.84, 0.76 at `delta = 1e-2, 1e-4, 1e-6, 0`;
  without mathopt5_4 0.95, 0.91, 0.90, 1.04; `mid`/`lp` 1.68, 1.64, 1.80, 1.70
  with no trend. The predicted separation growing with `log(1/eps)` is not
  visible beyond mathopt5_4.
- Correctness: 967 optimal runs; no primal value worse than the MINLPLib best
  known by more than `2.2e-10` (relative); no dual bound excludes it by more
  than `1e-6`; values below the best known are mostly within `1.4e-5`
  (feasibility tolerance), hs62 at `-5e-5` (within MINLPLib's own gap),
  hybriddynamic_varcc at `-4.25e-4` in all 18 optimal runs (setting-independent).
- Node counts are deterministic: 154 of 154 comparable trace runs reproduced
  the main runs' node and LP-iteration counts.

**Supported claims.** For SCIP 10.0.2 on this 57-instance set: LP-point
splitting is neutral within seed noise; removing the clamp roughly doubles node
counts and the penalty comes from failures caused by LP values on variable
bounds and pseudo-solution nodes; pure midpoint splitting is about 15% worse;
LP-point splitting helps clearly only on very low-dimensional smooth instances
that close at the tolerance scale.

**Unsupported claims.** Any general solver recommendation; results for harder
instances (20–120 s and beyond) or other solvers; separation of split-point
effects from variable-selection effects (the parameters change pseudocost
scoring); "the theory's predicted gains grow with `log(1/eps)`"; time speedups
(times are noisier, 6 runs in parallel); Couenne's actual behavior.

**Caveats.** Benchmark shaped by the 20 s screen, family cap and "solved"
filter; 3 seeds (1 for optional settings and the sweep); censoring at time
limits; source-version mismatch for the code reading; no independent review of
aggregates or interpretation.

**Artifacts.** `minlplib-branching/{run_one.py, runner.py, select_candidates.py,
select_benchmark.py, features.py, analyze.py, candidates.csv, selected.txt,
*_jobs.txt}`, `results/{runs.jsonl, screen.jsonl, trace.jsonl, trace2.jsonl,
features.json, summary.md, meta.json, *.log}`, `results/sols/` (57 default
seed-0 solutions). MINLPLib instance files are external (Section 8).

### 3.3 S3: Safe branching points, synthetic kinks and a second MINLPLib campaign

**Question.** Is there a split rule that is both safe against boundary LP
points (every child keeps a `theta0` fraction of its parent) and competitive on
kink instances? What happens in SCIP?

**Configuration.**
- SCIP 10.0.2 (bundled `libscip` of PySCIPOpt 6.2.1), SoPlex 8.0.2, Ipopt
  3.14.19, Python 3.13.11; same machine as S2, shared; single-threaded, at most
  6 in parallel, CPU clock, 4,000 MB; seeds as in S2; clamp draws seeded from
  the run seed (`results/meta.json` records SCIP's branching defaults).
- Arm P (SCIP's own selection and point formula): `default`, `rclamp`
  (`branching/clamp` redrawn from `U[0.1, 0.3]` at every focused node via an
  event handler), `c10` (clamp 0.1), `lp`, `lp_rclamp` (midpull 0).
- Arm X (branching plugin with priority `1e6` via `ctypes` access to
  `SCIPgetExternBranchCands`, `SCIPgetBranchingPoint`, `SCIPbranchVarVal`;
  selection re-implements `cons_nonlinear` scoring from the 10.0.3 source):
  `x_default`, `x_rclamp`, `x_lp`, `x_lp_rclamp`, `x_recenter` (recentring
  clamp `RC_0.2`), `x_inc` (incumbent coordinate if inside, else clip),
  `x_noclamp`.
- MINLPLib: S2's 57 instances, 12 settings × 3 seeds, **60 s** limit
  (2,052 runs, 5.5 CPU h).
- Synthetic kinks: `k1:a` (1D, `2|x - a| - (x - a)^2` with secant relaxation;
  same open nodes and minimizers as the exact-gap model) and `mc:a` (McCormick
  kink, `L = 2`, `c = -1`, `b = sqrt 2 - 1`), 8 kink positions, `eps = 1e-2,
  1e-4, 1e-6, 1e-8`, 12 settings, 5 seeds: 3,840 runs, 60 s limit; settings as
  S1's `modelnoprop` plus `misc/allowweakdualreds = FALSE` (otherwise presolve's
  cutoff propagation solves `k1` at the root), `feastol 1e-9`,
  `checkvarlocks = d`.
- Exact-model simulations (not SCIP): `sim_kink.py` (20,000 runs per entry in
  1D, 1,000 on McCormick), `sim2d.c` (`10^6` runs per entry), `exact2d.py`
  (exact rationals), `chain1d.py` (trap points, Theorem B, price of safety).

**MINLPLib results** (`results/summary.md`; recomputed independently by the
reviewer for 11 pairs, agreement to 3 decimals):

| Comparison (S3, 60 s) | Ratio | 95% CI | p | Separated wins / losses |
|---|---|---|---|---|
| `rclamp` / `default` | 0.963 | 0.87–1.06 | 0.58 | 0 / 0 |
| `c10` / `default` | 1.015 | 0.96–1.08 | 0.24 | 0 / 1 |
| `rclamp` / `c10` | 0.948 | 0.85–1.05 | 0.32 | 0 / 2 |
| `lp` / `default` | 1.010 | 0.81–1.21 | 0.20 | 4 / 5 |
| `lp_rclamp` / `lp` | 0.996 | 0.90–1.09 | 0.77 | 1 / 2 |
| `x_default` / `default` (plugin reproduction) | 1.005 | 0.84–1.13 | 0.016 (6 wins / 19 losses) | 1 / 0 |
| `x_rclamp` / `x_default` | 0.996 | 0.88–1.12 | 0.91 | 0 / 0 |
| `x_lp_rclamp` / `x_lp` | 1.001 | 0.93–1.07 | 0.59 | 0 / 1 |
| `x_recenter` / `x_lp` | 0.939 | 0.86–1.01 | 0.29 | 0 / 1 |
| `x_inc` / `x_lp` | 1.047 | 0.95–1.17 | 0.74 | 0 / 1 |
| `x_noclamp` / `x_lp` | 1.999 | 1.43–2.96 | 3e-5 | 2 / 18 |
| `x_recenter` / `default` | 0.923 | 0.71–1.14 | 0.52 | 3 / 5 |
| `x_recenter` / `x_default` | 0.920 | 0.75–1.09 | 0.25 | 1 / 4 |
| `x_inc` / `default` | 1.032 | 0.81–1.27 | 0.14 | 4 / 4 |

- Plugin counters: under `x_lp` the clamp moves the split in 50% of
  continuous branchings (488,850 of 968,098) and the LP value lies on a bound in
  33%; recentring changes the point in 9.8% (88,273 of 901,422); only 675 of
  about 1.03 million `x_inc` branchings split at the incumbent; under
  `x_noclamp` 2.54 million of 3.84 million continuous branchings create a child
  below 1% of its parent; 41 `x_noclamp` runs hit the time limit.
- On the 12 instances with LP values on a bound in at least 10% of `x_lp`'s
  branchings: `x_recenter`/`x_lp` 0.77 (0.56–1.03, p = 0.21);
  `rclamp`/default 0.81 (0.62–1.08). Not significant.
- Status: optimal runs per setting 129 (`x_noclamp`) to 170 (`rclamp`) of 171;
  five LP-solver crashes on wastewater05m1/05m2; correctness deviations as in
  S2 (worst primal and dual deviation above best known `4.5e-8` relative).
- Cross-check with S2: `default` and `lp` node counts identical in every run
  optimal in both studies (168 of 168, 163 of 163).

**Synthetic kinks in SCIP** (mean over 5 seeds, range in brackets; `eps = 1e-8`):

| Instance | default | `lp` (`C_0.2`) | `lp_rclamp` | `x_lp` | `x_lp_rclamp` | `x_recenter` | `x_inc` | `x_noclamp` |
|---|---|---|---|---|---|---|---|---|
| 1D, `a = 1/6` | 15 | 13 | 5 [3–9] | 13 | 5 [3–9] | 5 | 3 | 3 |
| McCormick, `a = 1/6` | 4,791 | 7,190 | 228 [3–1,091] | 9,743 | 86 [3–383] | 21 | 2,565 | 47 |
| McCormick, `a = 0.0102` | 6,515 | 26 | 766 [7–3,443] | 33 | 1,164 [25–5,385] | 33 | 22 | 17 |
| McCormick, `a = 1/3` | 3,847 | 10 | 10 | 88 | 88 | 88 | 15 | 88 |

- `C_0.2` at the 1D trap point `1/6`: 3, 7, 9, 13 nodes at `1e-2 ... 1e-8`;
  on the McCormick kink 61, 541, 7,190 at `1e-4, 1e-6, 1e-8` (about
  `eps^(-1/2)`). Recentring: 5 nodes in 1D at every `eps`; 16–88 on every
  McCormick kink. SCIP's default point grows on every kink, including `a = 1/3`
  where no clamp binds (5, 9, 13, 17 in 1D), because of the midpoint pull;
  1,587–6,828 nodes at `1e-8` on the McCormick kinks with or without `rclamp`.
- The incumbent rule falls back to the clip when SCIP's selection splits `y`
  first (2,565 nodes at `a = 1/6`); in 1D it takes 3 nodes.
- No clamp is harmless here (17–99 nodes): in the kink models the relaxation
  point is never on a bound, so the benefit of the clamp cannot show.
- Exact-model numbers: `C_0.2` at `a = 1/6`, widest side, `eps = 1e-8`:
  19,537 leaves in exact rational arithmetic (19,541 in floating point was a
  tie artifact); randomized clamp `[0.1, 0.3]` at `a = 1/6`: mean 391.6 ± 1.0
  (`10^6` runs), 99% quantile 3,721; expected splits in 1D at `a = 1/6`: 2.02.

**Supported claims.** In SCIP, on exact kink instances with propagation and
cutoff reductions off, the clamp's trap, recentring's boundedness and the
randomized clamp's 1D fix and widest-side heavy tail all appear as the model
predicts; on MINLPLib, no safe variant differs from its reference beyond seed
noise, and removing the clamp is harmful again (2.00) through boundary chains.

**Unsupported claims.** That recentring improves SCIP on MINLPLib (0.92–0.94,
CIs contain 1); that SCIP's default is kink-robust; any claim about SCIP's
defaults with propagation on for the kink instances (cutoff propagation solves
`k1` at the root); comparisons across arms without stating the reference (Arm
X selection is close to but not SCIP's: 6 wins / 19 losses, p = 0.016, +7.5%
time from Python callbacks).

**Caveats.** 60 s limit (S2 used 120 s), so S2 and S3 ratios are distinct
measurements even for the same pair (`lp`/default: 1.033 in S2, 1.010 in S3);
only the window `[0.1, 0.3]` tested; 12 settings without multiplicity
correction; review left time ratios, subgroup ratios and correctness deviations
unrecomputed.

**Artifacts.** `robust-branching-points/{scip_run.py, runner.py, summarize.py,
minlplib_jobs.txt, synthetic_jobs.txt, chain1d.py, check_A2d.py, exact2d.py,
sim_kink.py, sim_keyed.py, sim2d.c, run_sim2d.py}`, raw
`results/{minlplib.jsonl (1.2 MB), synthetic.jsonl (2.1 MB), summary.md,
meta.json, *.log}`, `sim_kink.jsonl`, `sim_keyed.jsonl`, `sim2d.jsonl`, chain
logs. The `sim2d` binary is not kept (rebuild from `sim2d.c`).

### 3.4 S4: Random sparse regression (perspective B&B and stronger relaxations)

**Questions.** (a) Where do root exactness and condition C1 (every single wrong
fixing prunable at the root, hence at most `2p + 1` nodes for every
variable-branching rule with the incumbent available or best-bound search) sit
at practical sizes? (b) Do pure-noise and low-SNR instances force large
certified conflict cliques? (c) Do stronger convexifications move the
thresholds?

**Configuration (phase-transition note, Section 6).** Python 3.13, NumPy 2.5,
SciPy 1.18, Clarabel 0.11, single-threaded. Gaussian `X`, `beta*_i = ±b` on
`S*`, `b = 1`, `sigma = 0.5` (per-entry SNR `b/sigma = 2`),
`n = round(alpha k log p)`; scaled ridge `lam = 1.5 sigma sqrt(2 n log p)/b`
("`tau0 = 1.5`") or `lam = sqrt n`. Pruning and C1 decisions use the certified
dual bound of Lemma 1.1 (a node passes if a dual vector certifies a bound
`>= f(S*)(1 + 1e-9)`; C1 fails if a primal node value is below
`f(S*)(1 - 1e-7)`). 31 runs originally recorded as "capped" were re-decided
exactly (dual-vector pool plus column generation; at most 109 node solves and
180 s per run): 30 satisfy C1, 1 fails (`p = 3200`, seed 1007). Cliques are
greedy cliques in a pool of near-optimal supports, each edge checked by the
exact midpoint formula against the exact `OPT`, hence valid lower bounds on
the leaves of every convex-piece certificate for that instance.

**Results.**
- Table 6.1 (`k = 8`, scaled ridge, 8 seeds; `p = 100, 200, 400, 1600`): C1
  holds in every run from `alpha ≈ 1.5` (`p = 100, 200`) and `1.75`
  (`p = 400, 1600`; 7 of 8 at `alpha = 1.5` for `p = 1600`); the PWE root
  certificate holds in at most 4 of 8 runs in any cell and at most 1 of 8 for
  `alpha <= 2`; the root gap is positive in every run without the certificate.
  C1 appears at realized `tau^2 ≈ 3.5–5`, about half of `2 log(p lam/n)`;
  first-order predictions for this ridge rule are `alpha ≈ 2.6, 2.8, 2.9, 3.2`
  (C1) and 5.1 (root). The empirical C1 threshold rises with `p` at fixed `k`.
- Table 6.2 (`p = 400`, `k = 20`, `gamma = 0.5`, 6 seeds): C1 in every run from
  `alpha = 1.5` (5 of 6 at 1.25, 2 of 6 at 1.0); root certificate once (at
  2.5). Corollary 3.3's optimal-ridge C1 threshold is `2 - gamma = 1.5`.
- Table 6.3 (`lam = sqrt n`, `k = 5`, `alpha = 3`, 8 seeds): C1 in 8/8 runs at
  `p = 50, 200, 800` and 7/8 at `p = 3200`; mean root gap 0.7, 1.3, 2.9, 5.4.
  At seed 1007 four forced-in nodes fail (null ranks 1, 5, 6, 50); all 3,195
  forced-in nodes were solved in the closing audit (largest margin 2.79; the
  relaxation recovers at least 61% of the budget price for every forced-in
  null): the finite-size many-violator mechanism.
- Table 6.4 (pure noise `b = 0` versus planted `b = 1` on the same designs,
  `p = 10k`, `lam = 0.75 sqrt(2 n log p)`, 4 seeds, node cap 30,000/40,000):
  in pure noise, trees and certified cliques grow quickly with `k`; at `k = 8`
  the median certified clique is 44, 74, 112 for `alpha = 1, 2, 4` (maximum
  195; one `alpha = 4` run hit the cap). With signal, the clique is 1 for
  `alpha >= 2` and trees have at most 17 nodes at `alpha = 4`.
- Table 6.5 (planted, `alpha = 0.35, 0.5`, below the empirical recovery
  threshold; `n/n_IT` 0.92–1.71): cliques grow from 2.5 to 11.5 at
  `alpha = 0.5` as `k` goes 3 → 8; trees 8 → 100 nodes.
- Table 6.6 (`p = 100, 200`, 6 seeds): most-fractional and largest-`z`
  branching give similar trees; no rule-dependent window is visible at these
  sizes. One sentence of the note is contradicted by its own data (Section 6,
  item E2).
- Section 6.7: the second-order heuristic agrees with the exact C1 outcome in
  207 of 232 runs (reproduced independently by the review).

**Stronger relaxations (thresholds note, Section 7).** cvxpy 1.9.3, Clarabel
(tolerance `1e-9`) for `p <= 100`, SCS (`eps = 1e-7` or `1e-6`) above; `k = 3`
with `OPT` by enumeration of all triples; exactness of `zb`/`sdp_2` means
within solver accuracy (about `1e-5` relative); `SDP1` exactness decided by
Dong's exact certificate (agreement with the solver rule on all 73 rows where
both exist).
- Nested designs, `n = 20` (`p = 40 ... 2560`, 8 seeds; `p = 2560` 4 seeds):
  `sdp_2` root-exact in 5/8 runs at `p = 40, 80` against 1/8 and 0/8 for the
  perspective relaxation; `zb` 8/8; `SDP1` closes a median 51%, 25%, 12%, 3%
  of the perspective root gap at `p = 40, 80, 160, 320`, tracking the design
  quantity `delta` of the note's Proposition 3.1 (medians 1.12, 0.53, 0.29,
  0.14). Caveat: `S*` stops being optimal as `p` grows (0/8 from `p = 1280`).
- `n = 40` (`S*` optimal by enumeration up to `p = 1600`; at `p = 3200` only
  the 6 of 8 runs where C1 certifies `S*` are kept): at `p = 100`, `SDP1`,
  `sdp_2` and `zb` are root-exact in 8/8 against 2/8 for the perspective
  relaxation; at `p = 3200`, explicit feasible points certify that the `L_2`
  root is inexact in 4 of 6 runs (hence also `sdp_2`, free-sign 2×2
  decompositions and the optimal perspective relaxation). Restricted to `S*`
  plus the 60 strongest nulls, `sdp_2` and `zb` are exact
  (`|value - f(S*)| <= 4e-5`): the failure uses the many `z = 0` helpers.
- Pure noise (Table 7.3, 71 runs): `zb` exact in 40, inexact (gap > `1e-4`)
  in 28, unclear in 3 (one SCS/Clarabel sign disagreement); where inexact its
  gap is 2.9–403 times smaller (median 14) than the perspective relaxation's;
  inexact in every run with `k = 8`, `alpha <= 2`.
- `p = 100` family of the parent note (Table 7.4, 20 runs): root-exact counts
  perspective 0, `SDP1` 4, `sdp_2` 11, `zb` 19; no case where a stronger
  relaxation provably restores C1 when the perspective relaxation lacks it.

**Supported claims.** At finite sizes, linear variable-branching trees are
certified in a range where the perspective root is not exact; pure noise
produces large certified conflict cliques at every tested `alpha` while the
planted problem on the same designs does not; stronger SDP convexifications
make large finite-size gains when `n/p` is not small and lose them as `p/n`
grows; at an accessible size inside the C1 window the pairwise lifted hull is
certified root-inexact, through the mechanism of the proof.

**Unsupported claims.** Any measurement of the asymptotic constants (all runs
lie outside assumption (A), which needs `p >= e^17 ≈ 2.4e7`); the asymptotic
clique theorem (its explicit conditions are vacuous at practical sizes);
evidence for Conjecture 5.2 from Table 6.5; that `zb` is exact at `p = 3200`
(only restricted values were computed).

**Caveats.** Floating point (certified dual bounds, not exact arithmetic);
greedy cliques from a 300-support pool are weak lower bounds at larger `k`;
small `k`; Table 6.6 unreviewed; some runs were stopped for time and omitted
(stated in the notes' appendices).

**Artifacts.** `sparse-regression/code/` (`core.py`, `bnb.py`, `hard.py`,
`exp_*.py`, `summ_*.py`, `redecide_c1.py`, `check_*.py`, `predict_c1.py`,
`make_tables.py`, `regen_tables.py`), `data/*.jsonl`, `data/check_s1007.log`;
`stronger-relaxations/code/` and `data/` (raw JSONL, `table_*.md`, check logs).
Exclude `__pycache__/`.

### 3.5 S5: Random binary least squares (MIMO detection)

**Question.** For B&B with the box relaxation on `min ||y - Ax||^2` over
`{-1,1}^N` (`A = sqrt(rho/N) H`, `M = beta N`), when is the root exact, when
does C1 hold, how large are trees between the regimes, and does the SDP
relaxation remove the obstruction?

**Configuration.** Python 3.13, NumPy 2.5, SciPy 1.18, CVXPY 1.9 with Clarabel
0.11, single-threaded, at most 6 processes; instance generator identical to the
scout's `bls.py` (same seeds give the same instances). Node relaxations by
NNLS with an upper-bound active-set loop and BVLS fallback; every pruning
bound and every C1 decision uses the certified Frank–Wolfe bound at the
computed point; B&B is best-first with incumbent `x*`; node caps `2·10^5`
(`beta = 1`, `N <= 128`) or `10^5` (`N = 256` and `beta = 2`). Tags: `rK` means `rho = N/K`, `cK` means `rho = K log N`.

**Results** (`data/tables.txt`, `data/predict_trees.log`, check logs):
- Root (Table 7.1a, 20,000 trials per cell, `N <= 8`): `P(x* box minimizer)`
  matches `2^-N` in every cell; vertex minimizers never exceed Theorem 1.2's
  bound. Table 7.1b (`N = 50, 200, 800`): mean root gain `G/N ≈ 0.50`,
  `var/N ≈ 1.2–1.3` (one 40-sample cell 1.81), active set `Bin(N, 1/2)`;
  `G = G_inf` in 3,519 of 3,520 instances.
- C1 (Table 7.2, `N = 100 ... 800`, 2–8 runs per cell): every instance decided
  (certified or refuted). Transition for `beta = 1`: about `theta = rho/N = 0.5`
  at `N = 100, 200`, about 0.4 at `N = 800` (theory `0.25`); `beta = 2`:
  0.12–0.17 at `N <= 400`, 0.10–0.12 at `N = 800` (theory `0.083`). Node values
  follow the exact law within 0.03 per cell; every node problem box-inactive;
  the linearized predictor agrees with the exact outcome in 310 of 330.
- Trees (Table 7.3; geometric means over 2–6 seeds): at `rho = 4 log N`,
  `beta = 1`: static order 90, 246, 2,000, >`10^5` (4/4 capped) and most
  fractional 44, 97, 509, 15,765 for `N = 32, 64, 128, 256`; at `8 log N`:
  static 65, 135, 387, 4,642, most fractional 34, 68, 157, 570. In the C1
  regime (`rho >~ N/3`) static trees have `2N + 1` nodes up to a few. Fixed
  `N/rho`: static growth from `N = 64` to 256 corresponds to polynomial degree
  1.04 (`r = 4`) and 1.78 (`r = 8`) against predicted 1 and 2. Tall systems
  (`beta = 2`) have much smaller trees.
- Sphere decoding on the same square instances (`rho = 4 log N`, 6 seeds,
  natural-order Fincke–Pohst with radius `f(x*)`): 839, 7,937, 61,289 nodes
  against 90, 168, 246 for static-order box B&B at `N = 32, 48, 64`
  (`data/check_revision_D.log`). Node costs differ; in single-thread Python the
  sphere decoder was faster in wall-clock time at `N = 64` (0.8 s against
  3.4 s for six instances, measured by the recheck).
- Exact-law tree predictor: within about a factor 2 of real static-order trees
  over three orders of magnitude (Table 7.3b); its knapsack extrapolation
  (heuristic, not a bound) gives `e^80` nodes at `N = 3000` for
  `rho = 4 log N`.
- Single-coordinate law (Table 7.4, up to `N = 10^5`): one-bit flips stop
  beating `x*` near `c = rho beta/log N = 2`, half moves near `c = 8`.
- SDP (Table 7.5a): per-instance exactness threshold `c* = rho*/log N`,
  medians for `N = 100, 400, 1600`: `beta = 2`: 4.62, 4.42, 4.38 (heuristic
  4.0; proved sufficient 135.9); `beta = 3`: 1.42, 1.33, 1.38 (1.5); `beta = 4`:
  0.71, 0.74, 0.70 (0.89); `beta = 1.5`: 20.3, 17.8, 17.3 (heuristic 12,
  loose); `beta = 1`: `log rho*/log N ≈ 2.75–3.11`. Square systems
  (Table 7.5b, `N = 16–40`): the SDP is exact in 0 of 96 runs; its root gap is
  about half to two thirds of the box gap (seed-dependent).
- Eigenvalue-shift relaxation (`beta = 2`, `N = 200`): root gap 0.066, 0.034,
  0.010, `4.7e-4` at `rho = 30, 60, 130, 300`, exact in 4/4 at `rho = 600`; box
  gap 0.232 throughout (`data/check_revision_EFG.log`).

**Supported claims.** The box relaxation's root exactness has no SNR
threshold at the planted point (finite-`N` probabilities match `2^-N`); C1
needs SNR linear in `N` and its finite-size transition moves down towards the
asymptotic value as `N` grows; trees at `rho = c log N` grow faster than any
fixed power over `N <= 256` (consistent with, not proof of,
`exp(Theta(N log log N/log N))`); for tall systems the SDP is exact at
`rho = Theta(log N)` per instance; in node count the box relaxation beats
natural-order sphere decoding by a wide margin on the same square instances.

**Unsupported claims.** That the asymptotic constants are observed; that the
superpolynomial lower bound is visible (its constant is about `1.4e-4` and it
is positive only for `N ≳ 1.7e7`); wall-clock superiority of box B&B over
sphere decoding; SDP-based B&B behavior for square systems.

**Artifacts.** `binary-least-squares/code/` (`core.py`, `exp_*.py`,
`predict_trees.py`, `knapsack_predictor.py`, `summarize.py`,
`check_revision.py`, `check_lemmas.py`, `check_node_inactivity.py`,
`test_core.py`), `data/*.jsonl`, `data/tables.txt`, non-empty `data/*.log`
(several `.log` files are empty and can be dropped).

### 3.6 S6: Path-structured scaling, single-tree SCIP versus a chain DP branch and bound

**Question.** On chain-structured (treewidth 1) nonconvex problems with a
unique nondegenerate global minimizer, does single-tree spatial B&B (SCIP)
scale exponentially in `n`, and does a decomposition-aware B&B scale
polynomially?

**Configuration.**
- SCIP **10.0** via PySCIPOpt 6.2.1 (the patch level is not recorded in this
  study's outputs; S1–S3 record 10.0.2 for the same PySCIPOpt version), single
  thread, default settings unless stated; `limits/absgap = eps`,
  `limits/gap = 0`, CPU-time limit 300 s (1800 s for extended runs),
  `timing/clocktype = 1`; default `feastol = 1e-6`. Machine: 36 cores shared,
  load average 17–130; SCIP's CPU clock appears to count user time only
  (about 25% extra system time not counted).
- Variants (probe3, `eps = 1e-4`, seeds 0–2): `single` (objective as one
  constraint), `bestfirst`, `obbt` (OBBT at every node with a solved LP; 228 of
  320 nodes at `n = 6`), `emph_opt` (64 parameters; aggressive separation incl.
  interminor cuts at the root, RLT every 20 levels), `combo` (all four),
  `warm` (optimal point supplied). Default runs already apply 2×2-minor
  (SDP-type) cuts (184 cuts at `n = 6`) and RLT at the root.
- Prototype (`chain_bb.py`): cell partitions per variable, min-sum DP with
  min-marginal pruning, exact reparametrization of pieces (modes `plain`,
  `affine`, `quad` for probe3, `split` for lot-sizing), local search for upper
  bounds, `theta = 1` refinement, cap `3e7` pair bounds per iteration, 600 s
  (900 s for lot-sizing); Python wall-clock seconds, single thread per
  process. Bounds are floating point with subtracted safety margins (no
  interval arithmetic); measured DP rounding at `n = 8192` at most `1.8e-13`
  (bound) and `3.2e-13` (marginals), against a first-order bound `4.4e-11`.

**Instances.** `F(x) = sum_i (x_i^2 - 0.1 x_i^4 + c_i x_i) + 0.8 sum_i x_i x_{i+1}`
on `[-1,1]^n`, `c ~ U(-amp, amp)` from `numpy.random.default_rng(seed)`,
nested in `n`; `amp = 0.3` is PROGRAM.md's probe3; `amp = 0.2` uses the same
stream times 2/3. The amp 0.2 family has a certified unique, interior,
nondegenerate global minimizer for all 75 tested instances (`n <= 1000`, 5
seeds; certificate eigenvalue at least 0.244, reproduced independently by the
review), while `F` is nonconvex on the box for `n >= 3`. Probe3 (amp 0.3) has
boundary global minimizers for some seeds from `n = 12` on (rigorous for 9
instances via the review's restricted-box bound). Lot-sizing chain (`T`
periods, economies of scale): optima are strict, nondegenerate boundary
minimizers (reduced-Hessian eigenvalues 0.80, 0.80, 0.85 at three optima).

**Results** (`tables.md`; geometric means, fits and local exponents
recomputed here from `data/scip_default_amp0.{2,3}.jsonl`):

| Family, `eps` | `n = 4` | 6 | 8 | 10 | 12 | 14 | Fit (`n = 4..10`) |
|---|---|---|---|---|---|---|---|
| amp 0.2, `1e-4` (SCIP nodes, geo. mean) | 218 | 1,504 | 7,084 | 29,169 | 0/5 solved | 0/5 solved | 5.07 per +2 variables (R² 0.9947); `n^5.30` (R² 0.9961) |
| amp 0.3, `1e-4` | 238 | 1,822 | 7,773 | 37,311 | 1/5 solved | 0/5 solved | 5.27 per +2 (0.9943); `n^5.42` (0.9944) |

- Local power-law exponents `ln(ratio)/ln((n+2)/n)` rise with `n`: amp 0.2,
  `1e-4`: 4.77, 5.39, 6.34; amp 0.2, `1e-2` (solved to `n = 12`): 4.69, 5.29,
  7.70, 8.13; amp 0.3, `1e-4`: 5.02, 5.04, 7.03 (flat on the first two steps).
  An exact 5-per-two-variables exponential gives 3.97, 5.59, 7.21, 8.83.
- Extended runs (1800 CPU s) at `n = 14`: all six runs unsolved after
  327k–435k nodes with gaps `3.6e-3` to `1.0e-2`, which is 1.7–2.5 times the
  power law's predicted total (152k–195k) and below the exponential's
  (844k–1.12M). At `n = 12`, two of six finished (116k and 204k nodes).
- After 300 s, the largest remaining gap grows with `n`: about 0.06–0.08
  (`n = 14`), 0.24–0.25 (16), 0.46–0.47 (18), 0.7 (20), while optimal values
  are between -0.05 and -0.48.
- All six variations grow 4.6–5.6 per two variables; `obbt` and `combo` need
  3.5–6 times fewer nodes but each node is 2–15 times slower; none solves
  `n = 14`; only `bestfirst` and `obbt` solve `n = 12`. The warm start leaves
  counts identical for `n <= 6` and changes them by -27% to +19% at `n = 8, 10`.
- Prototype, amp 0.2 (`quad`): 5/5 solved at every `n` up to 8,192 at
  `eps = 1e-4` and `1e-6`; median pair bounds 5,825,535 and 5,837,943 at
  `n = 8192`; median wall time 12.8 s and 19.1 s there; below 0.1 s up to
  `n = 128`. Fitted median work `n^1.80` (`1e-4`) and `n^1.60` (`1e-6`) on
  `n = 16..8192`.
- Prototype, amp 0.3: `n^2.38–2.43` up to `n = 1024`; 4 of 5 seeds at
  `n = 2048` (one exceeds the pair cap); no refinement setting solves
  `n = 8192`; max/median cost over seeds up to about 1,800 (`n = 12`).
- Ablation (amp 0.2): without transfers (`plain`) the DP reaches `eps = 1e-6`
  only up to `n = 4–8` (0/5 at `n = 10`); `affine` solves everything up to
  `n = 256` with work `~n^1.9`; `quad` uses 7,000–10,000 times fewer pair
  bounds at `n = 256`.
- Lot-sizing: SCIP grows 2.78 per period on `T = 4..9` (R² 0.9945; power law
  `T^6.28`, R² 0.9813), 4/5 solved at `T = 10`, none at `T >= 12` (gaps
  0.36–0.60 at `T = 12`); the prototype solves `T = 128` in 21–25 s (wall) and
  4/5 at `T = 256`, work `T^2.43–2.55`.
- Consistency: where both solved, SCIP's value minus the prototype's UB lies
  in `[-6.9e-6, -1.9e-8]` (SCIP below because of its feasibility tolerance;
  confirmed by evaluating `F` at SCIP's points and by the review's rigorous
  lower bounds).
- Determinism: 144 solved SCIP runs repeated with identical node counts.
- Unexplained: at `n = 12` SCIP's node rate collapses by a factor of about 50
  late in the search (it does not affect solved counts used in the fits).

**Supported claims.** On these path-structured instances, including a family
with a certified unique, interior, nondegenerate minimizer, SCIP 10's node
count grows about 5 times per two added variables over `n = 4..10`, faster
than a fixed-degree polynomial over this narrow range, under every tested
setting; a decomposition-aware DP branch and bound with valid (floating-point)
bounds closes the same instances to the same absolute tolerance with fitted
polynomial work up to `n = 8192`; exact reparametrization of the pieces is
essential to that.

**Unsupported claims.** Exponential growth of SCIP asymptotically; any ratio
of SCIP nodes to pair bounds; any CPU-time speedup figure (SCIP CPU user
seconds against Python wall-clock seconds on a loaded machine); claims about
other solvers (BARON, Gurobi, Couenne, ANTIGONE not run) or untested SCIP
features (quadratic intersection cuts, RLT/minor at every node, other
branching rules, convex-part reformulation); the prototype's generality (paths
only, problem-specific bounds, no integer variables).

**Caveats.** One solver version (patch unrecorded); 5 seeds and a narrow
solvable range; single seeds deviate from the geometric mean by up to 3.1
times at `n = 10`; prototype heavy tails and failures on amp 0.3; the
post-review revision of the note (Section 9) was not independently rechecked.

**Artifacts.** `research-20260929/computation/*.py`, `data/*.jsonl` (including
`data/wallclock/`, used only for the determinism check), `logs/`, `tables.md`.
Total about 1.4 MB.

### 3.7 S7: Single-tree termwise McCormick on the path family

**Question.** Does single-tree spatial B&B with termwise McCormick relaxations
need exponentially many leaves in `n` on a path problem with a unique
nondegenerate interior minimizer, and how do a toy B&B and SCIP compare with
the proved bound `0.57 (5/3)^n` (`eps <= 1e-4`)?

**Configuration.** Toy B&B `bb_path.py`: incumbent fixed at `f*`
(multi-start L-BFGS-B), pruning only on certified weak-duality bounds with tie
tolerance `1e-12` (separable dual function of the McCormick relaxation, dual
ascent, Clarabel fallback; Frank–Wolfe for alphaBB); relaxations `mc`
(secant of `-kappa x^4`, McCormick), `mcx` (Kelley cuts for `g_i`), `abb`,
`abbU`, `abbS`; rules `bisect`, `oracle`, `vw`, `viol`. SCIP 10 via PySCIPOpt
6.2.1, one thread, `absgap = 1e-4`, PROGRAM model (same as S6's probe3).

**Results.**
- Toy leaves at `eps = 1e-4` (certified reruns): termwise rules grow
  2.7–3.1 per added variable on every instance (e.g. `mc` bisect seed 0: 249,
  738, 2,254, 7,121, 21,001, 64,518, 198,363 at `n = 4..10`); alphaBB 2.4–2.9;
  Theorem 1's bound 4.4, 7.4, 12.3, 20.5, 34.2, 56.9, 94.9 (base 5/3). Counts
  are linear in `log10(1/eps)` with slope `B_n` growing about 3 per variable.
- Minimal grid-restricted certificates (upper bounds on the optimum): 4, 10,
  32 leaves at `eps = 1e-2` for `n = 2, 3, 4`; 4, 8, 12 at `n = 2` for
  `eps = 1e-2, 1e-4, 1e-6`.
- SCIP (nodes; seed 0 = probe3 amp 0.3 seed 0, matching S6): default 217,
  1,055, 4,447 at `n = 4, 6, 8`; with the minor separator off
  (`separating/minor/freq = -1`) 529, 4,367, 36,081. Convex variant
  (`kappa = 0`, `c = 0`): default 1 and 21 nodes at `n = 4, 8`; minor off 21 and
  14,011. Growth per variable: default 2.1–2.3; minor off 2.9–3.5 (the toy's
  range). Counts are identical for `absgap = 1e-4, 1e-5, 1e-6` because SCIP's
  incumbent sits a few `1e-6` below `f*`.

**Supported claims.** Termwise McCormick B&B grows exponentially in `n` on
this family in the tested range, faster than the proved base; SCIP's default
PSD-minor cuts escape the theorem's relaxation class and explain most of
SCIP's lower growth; the escape is a property of the relaxation class (Lemma
9.1 / Consequence A of the note, Griewank–Toint), not of branching.

**Unsupported claims.** That SCIP satisfies (M_b); that the observed bases
2.7–3.5 are proved; that the grid optima are lower bounds.

**Caveats.** Floating point (the recheck's exact rational B&B reproduced the
counts it tried); two seeds; first-version logs in `logs/v1/` are superseded
(they pruned on HiGHS values up to `1.5e-4` too high) and must not be cited.

**Artifacts.** `research-20260929/theory-face-exact/{bb_path.py, bounds.py,
checks.py, chordal_checks.py, grid_dp.py, analyze_leaves.py, make_tables.py,
summarize.py, scip_runs.py, jobs_v2.txt, jobs_v3.txt, run_jobs_v2.sh,
run_jobs_v3.sh, run_grid_v2.sh, scip_jobs.txt, run_scip.sh}`, `logs/`
excluding `logs/v1/` (or including it, labelled superseded).

## 4. S8: Supporting proof-model computations (inventory, not audited in depth)

These computations illustrate or check theorems in models; they are not solver
experiments. Headline numbers are as stated in each note and its review.

| Source | What it shows | Headline numbers | Status |
|---|---|---|---|
| `research-20260928b/bb-complexity/spatial-constrained/` Section 9 (`sbb_sphere.py`, `logs/sweep_*.jsonl`) | exponents `0, 1/4, 1/2, 1` with constraints and strata, exact-alphaBB toy B&B, bisection | e.g. `S2_circ` 273, 3,359, 29,465 nodes at `1e-2, 1e-4, 1e-6`; leaves/LB ratio 30–45 (2D), 100–125 (3D), roughly constant in `eps`; dual bounds validated on 582 boxes | reviewed note; floating point |
| `research-20260929/rlct/` Section 10 (`run_sweep.sh`, 231 bisection runs) | RLCT exponents, boundary counterexample | fitted slopes match predicted exponents within 0.021; leaves/bound within a factor 2.2 over 5–11 decades; 0 undecided nodes | reviewed and rechecked |
| `research-20260928b/bb-complexity/cutoff-propagation/` Section 7 (`bb.py`, `fbbt.py`, `logs/tables.md`) | same function and relaxation: 1 node or `eps^(-1/2)` depending on the expression DAG | linediag, expanded `exp` with fixed-point FBBT: 469, 4,035, 42,345 nodes at `1e-2, 1e-4, 1e-6`; one-sided `s`: 1 node (5,920 HC4 rounds at `1e-6`) | reviewed; SCIP numbers cross-read against S1 by the review |
| `research-20260928b/bb-complexity/integer-core/` Section 3.7 (`cvp_summary.log`) | random CVP class-number checks, `n = 8..32` | 420 instances; no violation of the stated inequalities | reviewed |
| `research-20260928b/bb-complexity/branching-competitiveness/` | exact computations for the competitive-ratio theorems; SCIP rule check | e.g. SCIP default rule's `log(1/eps)` loss on an explicit instance (exact arithmetic); Lean formalization of Theorem 1 elsewhere | reviewed; contains compiled `.so` files (rebuild from `gdp.c`, `gdp_sep.c`) |
| `research-20260928b/bb-complexity/spatial-face-exact/` (`rules_table_*.jsonl`, `clamp_cantor.py`) | branching-point placement on McCormick kinks; clamp Cantor set | e.g. clamp 1/5 at `a = 1/6`: at least `0.0745 eps^(-1/2)` nodes against `N_opt = 2` | reviewed |
| `research-20260929/theory-decomposition/` Section 5 (`run_experiments.py`, `logs/E*.log`) | decomposition-certificate sizes and validity | size per bag about `3.7e4` at `eps = 1e-6`; total `Theta(n log(n/eps))`; the single-tree integral bound overtakes the computed certificates only near `n ≈ 45–50` | reviewed in several rounds |

Note: `paper-decomposition-aware/experiments/` contains a different
algorithm (certified coordinate grids, "CT") and its own SCIP comparison on a
planted family. It is not S6 and must not be merged with it.

## 5. Rules for using several studies together

1. **No pooled ratios across studies.** S2 (120 s) and S3 (60 s) measure even
   the same pair differently (`lp`/default 1.033 against 1.010). Report each
   with its own time limit, seeds and reference rule.
2. **No cross-unit comparisons.** SCIP nodes, toy-B&B leaves, prototype pair
   bounds and Python B&B nodes are different units. S6's comparison is about
   growth in `n` and about solved/unsolved status at a fixed budget, not about
   per-unit cost or speedup.
3. **No time-based speed claims across codes.** SCIP CPU seconds (user time)
   and Python wall-clock seconds on a loaded machine are not comparable. The
   only time statements the evidence supports are within one code (e.g. node
   throughput of SCIP variants in S6) or qualitative (milliseconds versus
   unsolved after 300 CPU s).
4. **State SCIP's `eps` semantics.** `limits/absgap` is a global stopping
   test; nodes are pruned against the incumbent with no `eps` slack; the
   incumbent can sit up to about `feastol` (or `n · feastol`) below `f*`. S1
   and the S3 synthetic runs use `feastol = 1e-9` and `eps >= 1e-8`; the
   MINLPLib runs of S2/S3 use default tolerances with gap limits 0; S6/S7 use
   the default `feastol = 1e-6`.
5. **Separate "theory-model" runs from "solver" runs.** S1 `model`/`toy`,
   S3 synthetic runs and S7 toy B&B match the theorems' node model; S1
   `default`, S2, S3 MINLPLib and S6 SCIP runs do not. Exponent agreement is
   claimed only for the former.
6. **Keep the instance families distinct.** S6's amp 0.2 family carries the
   certified premise; probe3 (amp 0.3) does not for `n >= 12`. S7's seed-0
   instance is probe3 seed 0 (S6 and S7 SCIP counts agree: 217, 1,055, 4,447).
7. **Use certified or reviewed numbers.** Prefer the post-review tables
   (S3 Section 11, S4 revised Tables 6.1–6.3, S5 tables, S6 Section 9 tables,
   S7 certified reruns). Never cite S7 `logs/v1/` or the pre-revision S4
   "capped" decisions.

## 6. Discrepancies, errata and label mapping found in this audit

- **E1 (brief path).** `research-20260929/theory-single-tree/` named in
  `BRIEF.md` does not exist. The single-tree lower bound and its computations
  are in `research-20260929/theory-face-exact/face-exact-exponential.md`
  (Theorems 1–2, Section 7) and the decomposition note
  `research-20260929/theory-decomposition/decomposition-certificates.md`
  (Section 2.1, Section 4).
- **E2 (S4, Table 6.6).** The sentences "The removal half fails whenever C1
  fails" (Section 6.6) and "the removal half fails whenever C1 fails" (Question
  5.1) are contradicted by the table and raw data: 3 of 72 runs have the removal
  half holding while C1 fails (`p = 100`, `alpha = 1.0`, seed 4000: 3 failing
  forced-in nodes; `p = 100`, `alpha = 1.25`, seed 4001: 1; `p = 200`,
  `alpha = 1.25`, seed 4005: 2). In those runs `maxz` used exactly `2k + 1`
  nodes (13, 13, 17), as Lemma 1.3 allows, and `maxfrac` 23, 17, 23. The
  conclusion (no rule-dependent window visible at these sizes) is unaffected.
  Table 6.6 was never independently reviewed. Correct wording: "In 3 of the 72
  runs the removal half holds while C1 fails; there, both rules need at most
  23 nodes."
- **E3 (S1 leaf ratio).** The note's table gives qflat2a 7.4–9.4 under
  `model`; over all 13 tolerances the retained summary gives 6.76–9.41 (7.4–9.4
  holds only over full decades). Other rows use all tolerances. Use 6.8–9.4.
- **E4 (S1 labels).** S1 uses the scout's labels. Mapping to the reviewed
  constrained note: Theorem B → Theorem 3.1 (integral lower bound; S1 uses its
  anisotropic form with per-coordinate `alpha_i`), Theorem D → Theorem 3.2,
  Theorem A → Theorem 3.3, Theorem C → Theorem 3.5, Lemma 0 → Lemma 2.1
  (corrected). "Low-rank remark" refers to the scout's remark on gaps in a
  subset of coordinates (constrained note, Theorem 3.1 remark).
- **E5 (S6/S7 version).** S6 and S7 record "SCIP 10.0"/"SCIP 10" with
  PySCIPOpt 6.2.1, not the patch level. Report them as SCIP 10.0 (PySCIPOpt
  6.2.1). The S7 note cites `sepa_minor.h` from the 10.0.3 source (read by
  the recheck).
- **E6 (S3 Section 7).** "On MINLPLib, midpull 0 is neutral in aggregate (1.01,
  CI 0.81–1.21, as in the earlier study)": the 1.01 figure is S3's own 60 s
  measurement; S2's is 1.03 (0.83–1.26) at 120 s. Cite each separately.
- **E7 (S2 review status).** S2 states that nothing was independently
  reviewed. Partial cross-validation now exists: S3's runs reproduced S2's
  `default` and `lp` node counts exactly (168/168, 163/163), confirmed by S3's
  reviewer, and this audit recomputed all seven aggregate ratios (within
  0.005), CIs (identical), the small-instance subgroup and the trace median.
  The interpretation of S2 remains unreviewed.
- **E8 (source reading versus binary).** S2's split-point description and S3's
  plugin selection are read from the SCIP 10.0.3 source; runs used 10.0.2.
- **E9 (S1 Ipopt).** S1's `meta.json` does not record the Ipopt version (S2/S3:
  Ipopt 3.14.19).
- **E10 (PROGRAM figure).** PROGRAM.md's "factor 2–3 per two added variables"
  for SCIP on probe3 understates its own table (3.1–8.4 per two variables);
  use S6's numbers.
- **E11 (solver correctness elsewhere).** `paper-open-minlplib` documents
  wrong optimal values from SCIP 10.0.2 (and later versions) on waterno2
  period subproblems through an invalid in-tree bound reduction. No such error
  appears in S1–S3 (all optimal runs checked against known optima), but the
  manuscript should not call SCIP outputs certificates.
- **E12 (S6 premise).** PROGRAM.md's claim that probe3 has a unique interior
  minimizer is false for some seeds from `n = 12`; use the amp 0.2 family for
  any premise-dependent statement.

## 7. Proposed displays (built only from retained outputs)

The recommended set is D1–D4. If the theorem spine includes the single-tree
versus decomposition separation, replace D3 by D5 and summarize the
branching-point evidence in text.

**D1. Figure: tolerance exponents in SCIP when the search matches the model
(S1).**
- Panel (a), log–log: nodes against `1/eps` under `model` for linediag2,
  ring2, conexp2, mccdiag2 (`p = 1`), sphere3, plane3, conexp4 (`p = 2`),
  qflat1, qflat2a (`1/4`), qflat2b, qflat3 (`1/2`), with dashed reference
  slopes 1/4, 1/2, 1. Mark node-limit runs as censored or omit them.
- Panel (b), semi-log: nodes against `log10(1/eps)` for iso2, iso3, iso4 under
  `model` (straight lines; 9, 40, 92 nodes per decade) and default (saturation
  at 95 and 341 nodes).
- Inline table or caption: predicted versus fitted slope (`runs_fits.json`)
  and the leaves/integral-bound range under `model` (`summary.md`).
- Data: `solver-validation/results/runs.jsonl` filtered by `setting`;
  `runs_fits.json`; `thm_bounds.json`.
- Caption must state: SCIP 10.0.2; 20 synthetic instances with exact optima;
  best-first, optimum supplied, heuristics off; `feastol = 1e-9`;
  `eps >= 1e-7`; floating point; fits over 1.5–6 decades (2–3 for `p = 2`).

**D2. Table: what changes the node count, and by how much.** One row per
intervention, each labelled by study, instance and `eps`; the point is that
relaxation and representation change counts by orders of magnitude while
search choices change constants.

| Intervention | Study, instance, `eps` | Count before → after | Exponent |
|---|---|---|---|
| node order and incumbent (default → `model`) | S1, linediag2, `1e-4` | 13,751 → 3,805 | wide slope 0.46 → 0.51 |
| branching rule under best-first without propagation (`modelnoprop` → `toy`: widest-side bisection; `toy` also turns presolve off, which alone changes no count on the core instances) | S1, ring2, `1e-5` | 11,847 → 44,705 | 0.50 → 0.54 (tail) |
| OBBT at every node | S1, linediag2, `1e-3` | 3,291 → 961 | no reduction (wide slope 0.46 → 0.59) |
| same problem: `x_i^2` shared by objective and constraint (condisk2, every setting) versus norm constraint without propagation (condisk2soc `noprop`) | S1, `1e-6` | 1 vs 53,700 | 0 vs 0.49–0.55 |
| unexpanded square | S1, ring2 `model` vs `noexpand`, `1e-6` | 37,439 → 1 | 0.50 → 0 |
| objective-cutoff propagation (instance outside (G_alpha)) | S1, isofbbt2, all `eps` | 37 (`noweakdual`) → 15 (default) | `eps`-independent |
| one-sided expression DAG with fixed-point FBBT | S8 cutoff toy, linediag, `1e-6` | 42,345 (`exp`) → 1 (`s`) | 0.51 → 0 |
| branching point on an aligned McCormick face (LP point under default search; the three bisection rules under best-first without propagation) | S1, mccaxis2, `1e-7` | 21,191 (widest bisection) / 10,469 (bisection on both) / 45 (x1 only) / 3 (LP point) | about 0.6 / 0.5 / log / 0 |
| PSD minor cuts on the path family | S7, seed 0, `n = 8`, `1e-4` | 36,081 (minor off) → 4,447 (default) | per-variable growth 2.9 → 2.1 |
| variable-lock presolve | S1, mccaxis2 | 1 node at every `eps` (problem changes) | – |

Data: `solver-validation/results/summary.md`, `cutoff-propagation/logs/tables.md`,
`theory-face-exact/logs/scip_runs.log` and `scip_nominor_*.log`.

**D3. Table: branching-point rules, model behavior and MINLPLib outcomes.**
- Part A (S3 synthetic, `eps = 1e-8`): the four kink rows of Section 3.3 with
  columns default, `C_0.2`, randomized clamp, recentring, incumbent, no clamp,
  each column labelled with its arm (P or X).
- Part B (MINLPLib, two separate blocks): S2 (120 s, 3 seeds): `lp`,
  `lp_noclamp`, `mid` versus default with ratio, CI, p, unsolved runs; S3
  (60 s, 3 seeds): `rclamp`/default, `x_recenter`/`x_lp`, `x_recenter`/default,
  `x_noclamp`/`x_lp`. Add one row with the seed-null comparisons (0.999, 1.021)
  and the median seed spread 1.51.
- Footnote: LP values on bounds in 42–100% of branchings on the failing
  instances; ex4_1_5's single path of 378,210 nodes.
- Data: `minlplib-branching/results/summary.md`,
  `robust-branching-points/results/summary.md`.

**D4. Figure: finite-size certification transitions in random designs (S4,
S5), two panels with separate axes.**
- Panel (a), sparse regression (`k = 8`, scaled ridge): fraction of 8 runs
  with C1 certified against `alpha`, one line per `p = 100, 200, 400, 1600`,
  with markers for the fraction root-certified; vertical marks at the
  first-order C1 predictions for this ridge (2.6, 2.8, 2.9, 3.2).
- Panel (b), MIMO: fraction of runs with C1 certified against `theta = rho/N`,
  lines per `N` for `beta = 1` and `beta = 2`, with vertical marks at
  `theta_c = 0.25` and `0.083`.
- Optional inset or caption rows: most-fractional tree sizes at
  `rho = 4 log N` (44, 97, 509, 15,765) and the stronger-relaxation facts at
  `n = 40` (`p = 100`: SDPs 8/8 exact vs perspective 2/8; `p = 3200`: `L_2`
  certified inexact in 4/6).
- Data: the reviewed Tables 6.1 and 7.2 (`binary-least-squares/data/tables.txt`);
  build from the tables, not by re-deduplicating the sparse JSONL files (the
  note's tables were regenerated after exact re-decisions).

**D5 (alternate). Table: path-structured instances, single tree versus
decomposition.** For amp 0.2 (`eps = 1e-4`, 5 seeds): SCIP geometric-mean
nodes and solved counts at `n = 4..14`, the gap after 300 CPU s at
`n = 14, 16, 20`, and prototype median pair bounds and solved counts at
`n = 4..8192`, in separate column groups with units in the header; one row
with S7's toy leaves and Theorem 1's bound on probe3 seed 0 for context (a
different relaxation, labelled as such). Data:
`research-20260929/computation/tables.md`, `theory-face-exact/logs/tables.md`.

## 8. Portable companion: what to package

All retained outputs are small; no trace dump needs to be excluded for size.
The largest files are S1 `results/runs.jsonl` (2.3 MB), S3
`results/synthetic.jsonl` (2.1 MB), S3 `results/minlplib.jsonl` (1.2 MB) and
S5 `data/root.jsonl` (0.8 MB). The study directories total about 12 MB
uncompressed (S1 2.7 MB, S2 1.5 MB, S3 3.8 MB, S4 1.0 MB, S5 1.4 MB, S6 1.4 MB,
S7 0.5 MB).

Proposed layout (each folder: scripts, raw JSONL, generated summary, `meta`,
check logs, and a short README mapping manuscript displays and claims to
files):

| Companion folder | Contents | Notes |
|---|---|---|
| `S1-scip-exponents/` | Section 3.1 artifacts, including `cip/` and `transformed/` | self-contained; instances are CIP files |
| `S2-minlplib-branching/` | Section 3.2 artifacts, `results/sols/` | MINLPLib OSiL files not included: cite MINLPLib and list the 57 names (`selected.txt`) and the metadata file hash |
| `S3-robust-branching/` | Section 3.3 artifacts | rebuild `sim2d` from source |
| `S4-sparse-regression/` | `code/`, `data/`, `stronger-relaxations/{code,data}` | drop `__pycache__/` |
| `S5-binary-least-squares/` | `code/`, non-empty `data/` files | drop empty logs |
| `S6-chain-scaling/` | `research-20260929/computation/` without `__pycache__/` | `data/wallclock/` optional (determinism check only) |
| `S7-single-tree-path/` | Section 3.7 artifacts | exclude `logs/v1/` or mark it superseded |
| `MANIFEST.sha256` | full SHA-256 of every file | prefixes below |

External inputs: MINLPLib (local copy of 1,632 OSiL files under
`~/.cache/minlplib/minlplib/osil`, not in the repository) and the metadata file
`code/minlp_solver_lab/instances/instancedata.csv` (in the repository; SHA-256
prefix `dbe97fdc90ba6b66`). The companion should state the MINLPLib access
date or version if it can be established; it is not recorded in S2/S3.

Keep out of the submission companion: the review documents and review check
scripts (internal process; they stay in the repository and in this evidence
folder); S8 binaries (`*.so`).

SHA-256 prefixes (16 hex digits) of the key outputs at the source commits:

| File | SHA-256 prefix |
|---|---|
| `research-20260928b/bb-complexity/solver-validation/results/runs.jsonl` | `3e79309ca7044082` |
| `.../solver-validation/results/summary.md` | `3fdfe1ea314a6781` |
| `.../solver-validation/results/runs_fits.json` | `357a7a877a1e0a82` |
| `.../solver-validation/results/thm_bounds.json` | `556064978a18736a` |
| `.../minlplib-branching/results/runs.jsonl` | `26247e80991f0beb` |
| `.../minlplib-branching/results/screen.jsonl` | `4c9be81037e198ee` |
| `.../minlplib-branching/results/trace.jsonl` | `663bf2b511aa9010` |
| `.../minlplib-branching/results/summary.md` | `756e956673f69984` |
| `.../minlplib-branching/selected.txt` | `4a874fa0ceadd06e` |
| `.../robust-branching-points/results/minlplib.jsonl` | `41700b0c56ccc6bf` |
| `.../robust-branching-points/results/synthetic.jsonl` | `eadf9bad3847e134` |
| `.../robust-branching-points/results/summary.md` | `0fca5272d28c8da6` |
| `.../sparse-regression/data/c1_redecided.jsonl` | `73171966e9ae3568` |
| `.../sparse-regression/data/hard_k3-8.jsonl` | `1b5f1a8dd5a7bf60` |
| `.../sparse-regression/stronger-relaxations/data/table_hardzb.md` | `07b5f8549db48aa4` |
| `.../binary-least-squares/data/tables.txt` | `66a08c7e8336fe0b` |
| `.../binary-least-squares/data/c1.jsonl` | `80bbbad09aa03cf1` |
| `research-20260929/computation/tables.md` | `5d80923e551af4c7` |
| `research-20260929/computation/data/scip_default_amp0.2.jsonl` | `af38dedd422d313c` |
| `research-20260929/computation/data/proto_amp0.2.jsonl` | `82b641fd140ae0e1` |
| `research-20260929/theory-face-exact/logs/tables.md` | `5adcf83048bf709e` |
| `research-20260929/theory-face-exact/logs/scip_runs.log` | `f7bbed4270698469` |

## 9. Material uncertainties

1. **One solver family and one machine.** Every solver result is SCIP 10.0.x
   through PySCIPOpt 6.2.1 on one shared machine; S6/S7 patch levels are not
   recorded. Other solvers and SCIP features were not tested.
2. **Independent reproduction is uneven.** S1 has no independent
   reproduction; S2's aggregates and interpretation are unreviewed (raw counts
   partly cross-validated by S3); S4 Table 6.6 is unreviewed; S6's post-review
   revision was not rechecked. S3, S5, the S4 C1 tables and S6's main claims
   were independently checked.
3. **Pre-asymptotic sizes.** S4 and S5 lie outside the theorems' regimes; the
   observed thresholds are at about half (S4) or above (S5) the first-order
   constants; no asymptotic constant or lower-bound constant is measured.
4. **Narrow fitting ranges.** S1 fits use 1.5–6 decades (2–3 for `p = 2`);
   S6's exponential-versus-polynomial evidence rests on `n = 4..12`, 5 seeds,
   rising local exponents and extrapolation failures, not on a proof.
5. **Small or selected benchmarks.** S2/S3 use 57 MINLPLib instances solvable
   in 1–20 s; effects on harder instances are unknown. Synthetic instances in
   S1/S3/S6/S7 were designed to isolate mechanisms.
6. **Seed noise.** MINLPLib per-instance differences below about 2 times are
   indistinguishable from seed noise on most instances; synthetic kink runs
   with the randomized clamp are heavy-tailed.
7. **Floating point.** The S6 prototype, S7 toy B&B, S4 and S5 bounds are
   floating-point certified (weak duality or safety margins), not interval or
   exact arithmetic, except where rechecks used exact rationals (S3 exact 2D
   counts, S7 recheck).
8. **Confounding.** S1 `model` changes node order, incumbent and heuristics
   together; S2's branching parameters change variable selection as well as
   split points; S3 Arm X selection differs slightly from SCIP's.
9. **Unexplained behavior.** S1's mccaxis2 stall at 5 nodes; S6's late node
   rate collapse at `n = 12`.

## 10. Audit commands run here

No experiment, optimizer or instance generator was run. All commands read
retained files; scratch scripts were written to `/tmp/bbmap/` (outside the
repository) and run with `python3 -I`.

| Command | Purpose | Result |
|---|---|---|
| `python3 -I /tmp/bbmap/minlp_small.py <minlplib-branching>` | S2 small-instance subgroup (19 instances, 3 seeds) | `mid`/`lp` 1.436 (CI 1.03–2.22); `lp`/default 0.811 (0.50–1.12): matches the note |
| `python3 -I /tmp/bbmap/minlp_main.py <minlplib-branching>` | S2 aggregate ratios, bootstrap CIs (5,000, seed 1), scipy Wilcoxon | 1.034, 2.190, 1.350, 1.150, 1.139, 1.015, 1.226; CIs identical to `summary.md`; p-values agree |
| inline `python3 -I -c` over S2 `results/trace.jsonl` | median share of default splits at width ratio < 1/2 | 0.701 over 52 instances |
| inline `python3 -I -c` over S2 `results/runs.jsonl` | run accounting by setting/seed/limit | 1,254 records = 855 + 171 + 228 |
| inline `python3 -I -c` over S1 `results/runs.jsonl` | status counts, CPU time, SoPlex warnings, bound offsets | 1,655 / 420 / 59 / 0; 1.76 h; 219 runs, max 33,456; incumbent ≥ `f* - 5.5e-9`; dual ≤ `f* + 1e-15` |
| inline `python3 -I -c` over S1 `runs.jsonl` and `thm_bounds.json` | leaves/integral-bound ratios under `model` | qflat2a 6.76–9.41 (E3); iso2 6.84–9.78; qflat2b 6.15–9.74 |
| inline `python3 -I -c` over S4 `data/rule_p*.jsonl` | removal half versus C1 (Table 6.6) | 3 runs with removal half and failed C1 (E2) |
| `python3 -I /tmp/bbmap/scaling_check.py <computation>` | S6 geometric means, fits, local exponents | 5.07 / `n^5.30` (amp 0.2), 5.27 / `n^5.42` (amp 0.3); local exponents as in `tables.md` |
| `sha256sum` on key outputs | manifest prefixes | Section 8 |
| `git log -1 -- <dir>`, `git status --short` | source snapshots | `a2abf970c`, `a0b2eebe6`; clean |

No project-wide checks were run and CI was not inspected. Nothing was
committed.
