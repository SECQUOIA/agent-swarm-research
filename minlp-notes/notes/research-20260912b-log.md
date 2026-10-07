# Research log: continuation started 2026-09-12 (evening)
**Later certification audit:** this is a historical log. The certified-MINLP implementation and claims were corrected on September 13; the current record is [repair and replay](certified-minlp-repair-and-replay.md).

Scope: new MINLP results relevant to Bernal Neira's interests, with priority
on algorithmic advances that come with an implementation and solver
comparisons. The previous closeout
([research-20260912-closeout.md](research-20260912-closeout.md)) noted that
the repository had no broadly useful solver contribution; this continuation
targets that gap.

## Environment (verified)

- 36 cores, 30 GB RAM. Python 3.13 via `uv` project
  `code/minlp_solver_lab/` (pyomo 6.10.1, gurobipy 13.0.3, pyscipopt 6.2.1 /
  SCIP 10.0, gamsapi 54.4, gdplib from the SECQUOIA GitHub source as an
  editable path dependency, numpy/scipy/sympy).
- GAMS 54.3.1 with a full academic license: BARON 26.5.27, ANTIGONE, SCIP,
  DICOPT, SBB, KNITRO, SHOT, LINDO, CPLEX, COPT, CONOPT, IPOPT, MINOS, SNOPT
  all solve a test MINLP/NLP/MIP. Gurobi 13.0.2 CLI and gurobipy 13.0.3 use
  the academic license. Ipopt and CBC executables in the conda environment
  `solvers` (`/workspace/local-home/miniconda3/envs/solvers/bin`).
- MINLPLib catalogue (`instancedata.csv`, 1633 instances): 299 convex
  discrete instances (`convex=True`, probtype in MINLP/MIQCP/MBNLP/MBQCP/
  MBQCQP) downloaded in `.gms` and Pyomo `.py` form to
  `code/minlp_solver_lab/instances/`.

## Direction selection

Three scouting reports were commissioned:
[convex MINLP/GDP algorithms](scout-20260912-convex-gdp-algorithms.md),
[nonconvex PSE classes](scout-20260912-nonconvex-pse-classes.md),
[software and verification](scout-20260912-software-verification.md).

Selected streams:

1. **LB-ESH for convex GDP** (multi-tree and single-tree), see
   [lbesh-20260912-method.md](lbesh-20260912-method.md). Prototype works on
   a synthetic instance (matches BARON). Benchmark harness pending.
2. **Certified lower bounds for convex MINLP** (VIPR certificate of the
   rationalized OA master plus exact checks of every nonlinear cut row).
   Depends on a SCIP 10 build with exact mode (in progress); shares the cut
   generator of stream 1.
3. **HENS (SYNHEAT) homogeneity lift**: `A * LMTD(dt1, dt2) = LMTD(A dt1,
   A dt2)` moves the area into the concave LMTD argument, leaving two
   bilinears with common factor `A` whose convex hull is the Balas hull of
   the two end slices. Assigned to an agent together with a singularity audit
   of MINLPLib `heatexch_gen*` (see below).

## Findings so far

- **Baseline run.** A 60-second, 4-thread run of BARON, SCIP, DICOPT, SBB,
  SHOT, ANTIGONE and Gurobi (all via GAMS) over the 299 convex discrete
  MINLPLib instances is in progress (`code/minlp_solver_lab/baseline/`).
- **LD-SDA and discrete convexity.** Bernal Neira's LD-SDA paper
  (arXiv:2405.05358, §6) lists as future work the relation between convex
  GDP and integrally convex reduced objectives. Joint convexity is not
  sufficient: the convex MINLP `min t s.t. t >= (2k1 - k2)^2 + (k1^2 + k2^2)/100`,
  `k` integer, has reduced objective `v(k) = (2k1-k2)^2 + |k|^2/100` for
  which `k = (1,2)` (value 1/20) is a strict local minimum over the
  ∞-neighbourhood (all neighbours have value >= 101/100) while the global
  minimum is `v(0,0) = 0`. Verified in exact rational arithmetic. So LD-SDA's
  i-local optimality does not imply global optimality even for convex
  MINLPs with two ordered integer variables; a positive result needs more
  structure (e.g. L♮- or M♮-convexity of the value function). Recorded as a
  small negative result; not pursued further today.
- **MINLPLib `heatexch_gen1` guard singularity (suspected).** The LMTD row
  `x85 = (x37 - x38)/log(x37/(1e-6 + x38))` with `x37, x38 >= 10` unbounded
  above lets `x85 -> +inf` as `x37 -> x38 + 1e-6`, which drives the area
  `x97 = 2 x25/(0.01 + x85)` to zero. If confirmed, the recorded 30% gap is
  partly an artefact of the guard rather than a HENS difficulty. Under
  audit by the HENS agent.

## Progress (21:55)

- LB-ESH prototype fixes after the first pass over the 28 convex GDP
  instances of the catalog: per-row supporting hyperplanes (one line search
  per violated row), LP-phase stall rule, adaptive NLP scheduling in the
  single tree, non-finite linearizations skipped with random restarts,
  interval and disjunctive bound propagation plus LP-based bound tightening
  for unbounded variables, epigraph rows always cut by tangents. The
  constrained-layout `l2` instances (Euclidean objective, `sqrt` singular at
  zero distance) now solve. `pyomo.batch_processing` has 111 variables
  without bounds in disjunctions; hull and big-M both need bounds, so it is
  excluded from LB-ESH runs (recorded limitation).
- First-pass observation: `gdplib.batch_processing` is dominated by the
  master MILP (BARON solves it in 103 s; LB-ESH single tree reaches a 9%
  gap in 100 s, LOA 28%). FLay05/06 are hard for every variant, as for
  OA-type solvers in MINLPLib.
- Certified-bound stream: `code/minlp_solver_lab/certify/` has (i) a
  rule-based exact-parameter convexity certifier (quadratic forms by exact
  rational LDL^T, perspective, monomials, norms, linear-fractional,
  exp/log/pow/sqrt compositions) that certifies 289 of the 299 MINLPLib
  convex discrete instances (7 fail to load: recursion depth in the Pyomo
  files; `cvxnonsep_nsig20`, `gams01`, `synthes1` not certified);
  (ii) safe rational cuts with mpmath interval enclosures (60 digits) and the
  convexity shift argument; (iii) a producer that writes the rational master
  MILP (`master.lp`, exact decimal expansions) and a lemma file, and an
  independent checker that re-derives convexity, recomputes every safe
  intercept and regenerates the LP byte-for-byte. `batch`: 74 cuts, all
  re-verified. SCIP 10 with exact mode and the VIPR tools were built in
  `/workspace/local-home/.local/opt/scip-exact`.

## Progress (22:40): reviews and corrections

- The user asked (22:15) to finish and verify the current ideas and not to
  start new ones. Remaining work from that point: review corrections, the
  final GDP comparison, the full certificate run, the HENS note, closeout.
- **LB-ESH review** ([review-20260912-lbesh.md](review-20260912-lbesh.md)):
  three blocking defects (OR disjunctions in the hull master, fixed-variable
  rows losing their constant, big-M cuts with infinite `M` silently
  dropped) and should-fix items; all fixed, the reviewer's scripts re-run
  (OR and unbounded cases now refused; fixed-variable case matches BARON).
  The method note was amended (hypotheses, per-row line search, hull-only
  LP-phase claim, corollary replaced by an approximate-feasibility remark).
- **Certificate review** ([review-20260912-certified-bounds.md](review-20260912-certified-bounds.md)):
  six blocking issues (unchecked linearization points, unsound perspective
  rule, wrong reciprocal rule, unsound SOL-dropping fallback, no VIPR-master
  comparison, lax verdict test); all fixed; the reviewer's 36 adversarial
  tests pass. Two further defects found while re-running: `viprchk` fails
  on non-canonical fractions printed by SCIP (`-5/10`), fixed by rewriting
  the certificate in lowest terms (value-preserving); and the producer's
  shift loop used the unclipped floating point, fixed.
- The MINLPLib baseline (299 instances, 7 solvers, 60 s) is complete;
  `baseline/summarize.py` reports per-solver counts and cross-solver
  disagreements (DICOPT "optimal" values far above others on several
  instances; SBB claims 5075 on clay0204m against 6545 from five solvers).
- Final GDP comparison (27 instances, 22 methods, 120 s) and the full
  certificate run (289 instances, 60 s OA, 180 s exact SCIP) are running.

## Progress (2026-09-13, 00:35)

- GDP comparison completed (594 runs); GAMS runs on the farm-layout models
  had to be repeated with interior starting values because Pyomo's GAMS
  plugin evaluates constraint bodies at the initial point (`1/x` at zero).
  The summary rule was revised twice: consensus reference (SBB's local
  values had polluted the "best" value) and a closed-bound requirement, with
  GAMS solvers that stop before the limit accepted on status because their
  bound field through Pyomo is unreliable (SHOT reports a root bound).
- Certificate run: the scale-invariant VIPR comparison was added after
  eight certificates had failed the checker only because SCIP scales input
  rows; `certify/recheck.py` re-verifies those entries. The run was
  restarted twice for throughput; the first 129 instances used an
  exact-SCIP limit of 180 s, the remaining 160 use 90 s (recorded per entry
  in `scip_attempts`). Interrupted exact runs still yield verifiable dual
  bounds when `viprchk` accepts the partial proof.
