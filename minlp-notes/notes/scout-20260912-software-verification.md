# Scout: software, methodology and verification directions for MINLP
**Historical scout, superseded for certification.** This search missed Halbig et al. (2024), who already compute convex-MINLP optimality certificates. The numerical novelty scores below are not current assessments. See [the primary-literature audit](certified-minlp-literature-audit.md) and [the repair/replay record](certified-minlp-repair-and-replay.md) for the corrected scope and evidence.

Date: 2026-09-12. Status: bounded literature scout, no implementation. Scope
is software/methodology/verification work for convex MINLP, nonconvex MINLP
and GDP that fits the Pyomo/MindtPy/GDPopt/GDPlib/MINLPLib line of work.
Quantum computing, machine learning and privacy are out of scope.

Every "not found" below is the result of web searches on 2026-09-12 and a
grep of this repository; it does not establish a literature gap or novelty. Each
candidate needs a direct check with the closest groups (ZIB exact-MIP group,
KTH/Åbo OA group, IIT Bombay Minotaur group) before investment.

## Summary and recommendation

| # | Candidate | Importance | Feasibility | Novelty confidence |
|---|---|---|---|---|
| 1 | Machine-checkable lower-bound certificates for MINLP (VIPR extended with nonlinear cut rules) | 9 | 6 | 8 |
| 2 | A posteriori exact audit of OA / LP-NLP-B&B decisions plus safe cut rounding in MindtPy | 7 | 8 | 7 |
| 3 | Sound structure recovery in Pyomo: big-M to GDP, semicontinuous to perspective/conic hull, with coverage statistics on MINLPLib and GDPlib | 7 | 7 | 5 |
| 4 | Verified reference values and convexity audit for the convex-MINLP and GDPlib benchmark sets | 8 | 8 | 5 |
| 5 | MINLP delta debugging and metamorphic testing (MIP-DD extended to nonlinear models) | 7 | 8 | 6 |
| 6 | Parallel / asynchronous multi-tree OA | 5 | 7 | 4 |

Recommended order: **1, 2, 3.** Candidate 2 is the natural first phase of
candidate 1 (same instrumentation, faster publishable result). Candidate 3 is
the best reformulation-side project and connects to the existing exact hull
reformulation work. Candidates 4 and 5 are high-value engineering with lower
novelty; they become much stronger once candidate 1 supplies certified
reference bounds. Candidate 6 is deprioritized: its theory is trivial and the
prior art is closer than it first appears.

## Repository overlap check

The repository contains many exact-rational certificate tools, but all are
problem-specific: potential-flow envelopes, correlated measurement design,
network-simplex hulls, rational affine ODE flows
([`notes/research-20260912-rational-flow.md`](research-20260912-rational-flow.md)),
and a Lean project for a fixed-degree convex box family (`formal/`). None
addresses solver-level certificates for general MINLP. The
[algorithm-opportunities note](research-20260912-algorithm-opportunities.md)
rejected "residual-certified inexact OA/Benders cuts" because the *theory*
of inexact value-function cuts is covered by Guigues; candidate 2 below is
distinct: it is an auditing tool, a safe-rounding option and an empirical
study, not a new cut theorem. The literature agenda
[`literature/topics/bernal-minlp-gdp-research-agenda-2026-09-10.md`](../literature/topics/bernal-minlp-gdp-research-agenda-2026-09-10.md)
(Priorities 3 and 5) and
[`literature/topics/open-theory-challenges.md`](../literature/topics/open-theory-challenges.md)
(item 12) already call for numerical contracts and certificate standards;
candidates 1, 2 and 4 answer those calls. Neither
[`notes/candidate-directions.md`](candidate-directions.md) nor
[`notes/candidate-directions-2026-09-05.md`](candidate-directions-2026-09-05.md)
lists a software/verification direction. The lab environment in
`code/minlp_solver_lab/pyproject.toml` already pins Pyomo 6.9+, gurobipy 13,
GAMS API 54, PySCIPOpt 5.5, highspy, sympy and gdplib, so all candidates can
start without new infrastructure.

## Candidate 1: machine-checkable certificates of global lower bounds for MINLP

### Technical content

Extend the VIPR certificate format and checker
([Cheung, Gleixner, Steffy 2017](https://arxiv.org/abs/1611.08832);
[scipopt/vipr](https://github.com/scipopt/vipr)) from MILP to MINLP by adding
*nonlinear cut rules* whose validity an independent checker verifies in exact
rational arithmetic plus verified interval enclosures. VIPR already has the
three ingredients a branch-and-bound proof needs: derived rows obtained as
nonnegative combinations of earlier rows (`lin`), integer rounding (`rnd`),
and case splits with assumptions (`asm`/`uns`). What is missing is a way to
introduce a *linear* row that is valid because of a *nonlinear* original
constraint. The proposed rules, each with a checker procedure:

1. **McCormick** rows for `w = x*y` over a rational box: the checker verifies
   the algebraic identity exactly (Fractions). Same for `w = x^2` secants and
   for products with bound-dependent coefficients after a spatial split.
2. **Tangent** rows `a*x + b <= f(x)` for a convex function `f` from a fixed
   library (`exp`, `log`, `x^p`, `sqrt`, `1/x` on positive domains, convex
   quadratics): the producer supplies rational `a` and `b`; the checker
   verifies `b <= min_{x in [l,u]} (f(x) - a x)`. For convex `f` this
   minimum is bracketed by evaluating `f - a x` on a verified grid with
   outward rounding (mpmath `iv` or python-flint/Arb), so the check is cheap
   and needs no derivative of the producer. Rounding the slope is harmless
   because the intercept is recomputed by the checker.
3. **Convex quadratic** tangents: validity needs `Q` PSD; the certificate
   carries a rational `L D L^T` factorization, verified exactly.
4. **Secant** (chord) rows for concave univariate pieces over `[l,u]`, using
   verified upper bounds on `f(l)`, `f(u)` and a concavity witness.
5. **Perspective / rotated-SOC** tangents for hull reformulations, which
   reduce to rules 2 and 3 after scaling; this is where the conic exact hull
   of [Gusev and Bernal Neira 2025](https://arxiv.org/abs/2508.16093) enters.
6. **Spatial branching** as VIPR assumptions (`x <= c` or `x >= c`), so that
   McCormick rows can depend on the current box.

Everything after the nonlinear rows is ordinary VIPR, so the MILP part of the
proof can be produced by SCIP's exact mode
([Hojny et al., SCIP 10, 2025](https://arxiv.org/abs/2511.18580);
[Eifler and Gleixner 2023](https://arxiv.org/abs/2101.09141)). A clean
composition for convex MINLP: run OA (MindtPy) to termination, rationalize the
final master MILP including all cuts, solve that rational MILP with SCIP
exact to obtain a VIPR file, and attach a lemma file that justifies each cut
row by rules 1–5. The MINLP certificate is then "VIPR file + lemma file", and
the combined checker is the VIPR checker plus a small Python nonlinear-rule
checker. This is also the shape of Szeider's black-box VIPR construction
([CP 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2026.52)),
which rationalizes floating-point solver output by cascaded continued
fractions rather than requiring an exact solver; that trick applies directly
to floating-point OA cuts.

Upper bounds must be treated separately and honestly: a rational feasible
point exists for inequality-constrained models with rational data but not in
general for nonlinear equalities; the certificate should carry a rational
point with a verified residual bound, and the claim should be stated as a
certified lower bound plus an epsilon-feasible incumbent, as
[Füllner, Kirst, Stein 2021](https://doi.org/10.1007/s10107-019-01444-6)
and the repository's numerics note already require.

### Gap it fills

Every existing certificate/verification line stops at linear problems:
VIPR (2017), SMT-based VIPR checking
([Mendes, Pulaj, Tran, Wu, Zhou; arXiv 2312.10420](https://arxiv.org/abs/2312.10420);
[J. Symbolic Computation 2025](https://www.sciencedirect.com/science/article/abs/pii/S0747717125001257)),
certified propagation and dual proof analysis
([Borst, Eifler, Gleixner 2024](https://arxiv.org/abs/2403.13567)), safe and
verified Gomory cuts ([Eifler and Gleixner, SIOPT 2024](https://arxiv.org/abs/2303.12365)),
VeriPB-based presolve certificates for 0-1 programs
([ISMP 2024 session WC266](https://ismp2024.gerad.ca/schedule/WC/266)),
and the SCIP 10 exact mode, which the report itself restricts to MILP. The
2026 [Kronqvist, Bernal Neira, Grossmann 50-year review](https://doi.org/10.1016/j.ejor.2025.07.016)
distinguishes a strong incumbent from a certified bound but cites no
verifiable-certificate work for MINLP. On the rigorous-numerics side, safe
LP bounds ([Neumaier and Shcherbina 2004](https://link.springer.com/article/10.1007/s10107-003-0433-3)),
rigorous convex-program bounds ([Jansson 2004](https://link.springer.com/article/10.1023/B:JOGO.0000006720.68398.8c)),
validated linear relaxations ([Kearfott 2005](https://doi.org/10.1137/030602186))
and numerically safe Gomory cuts ([Cook, Dash, Fukasawa, Goycoolea 2009](https://doi.org/10.1287/ijoc.1090.0324))
make bounds *safe inside the solver* but produce no independently checkable
artifact. Conic OA certificates ([Coey, Lubin, Vielma 2020](https://arxiv.org/abs/1808.05290))
are dual rays used for cut generation, not proofs. Exact SOS certificates
([Peyrl and Parrilo 2008](https://www.sciencedirect.com/science/article/pii/S0304397508006452);
[Kaltofen et al. 2012](https://www.sciencedirect.com/science/article/pii/S0747717111001143))
cover polynomial nonnegativity but not branch-and-bound trees. Searches for
proof logs of spatial branch-and-bound or McCormick-based global optimization
returned nothing.

### Closest prior work and what it did not do

- VIPR and its checker: MILP only; no nonlinear rows.
- Borst–Eifler–Gleixner 2024 and SCIP 10 exact mode: exact MILP with
  certificate output; nonlinear constraints and NLP subsolvers stay
  floating-point.
- Szeider CP 2026: reconstruction of VIPR certificates from floating-point
  ILP output; no nonlinear cut rule.
- VeriPB "nonlinear" pseudo-Boolean certificates cover products of Boolean
  literals only.
- Kearfott's GlobSol and Neumaier's COCONUT produce validated bounds
  internally; no exchangeable proof format, no MILP integration.
- CvxLean ([Bentkamp, Fernández Mir, Avigad, TACAS 2023](https://arxiv.org/abs/2301.09347);
  [repo](https://github.com/verified-optimization/CvxLean)) provides
  Lean-verified DCP transformations; it does not verify solver bounds, but it
  is a possible later backend for machine-checked convexity witnesses in rule
  2, and the repository already has a Lean project.

### Risk of being already known

Moderate-low. The ZIB group is the obvious competitor; the SCIP 10 report
lists no nonlinear plan for exact mode, but a private project may exist.
Ask before investing. The nonlinear checker rules themselves are elementary;
the contribution is the format, the checker, the producer integration and
the empirical result (fraction of MINLPLib convex instances whose MindtPy /
SHOT-style bound can be certified, and at what overhead).

### Effort (Python, this environment)

- Nonlinear-rule checker with Fractions + verified intervals: 2–3 weeks.
- Producer hooks in MindtPy OA (Python, straightforward) and the
  rationalize-then-SCIP-exact pipeline for the master MILP: 2 weeks.
  SCIP exact mode and VIPR need the SCIP suite built from source; PySCIPOpt
  5.5 is present but exact mode may require a command-line run.
- Experiments on the 366-instance MINLPLib convex subset (Pyomo versions
  exist in [SECQUOIA/pyomo-MINLP-benchmarking](https://github.com/SECQUOIA/pyomo-MINLP-benchmarking))
  and GDPlib: 2–3 weeks. Nonconvex extension via McCormick rows on a small
  in-house rational spatial B&B: additional 3–4 weeks.
- Realistic first paper (Math. Prog. Comp. or INFORMS JOC) in 3–4 months.

Scores: importance 9, feasibility 6, novelty confidence 8.

## Candidate 2: a posteriori exact audit of OA / LP-NLP-B&B decisions, and safe OA cuts

### Technical content

The MINLP analogue of [Hoen and Gleixner, CPAIOR 2025](https://arxiv.org/abs/2412.14710)
([bnbanalyzer](https://github.com/alexhoen/bnbanalyzer)), who checked every
critical MILP branch-and-bound decision a posteriori (integer-feasible
acceptance, LP infeasibility, pruning) and found that errors are rare but
real. For OA, ESH and LP/NLP-B&B the decisions to audit are: (i) each cut is
a valid underestimator (rule 2/3 of candidate 1, checked in rational
arithmetic with the original expression, not the solver's linearization);
(ii) each master MILP bound is justified (re-solve the rationalized master
with SCIP exact, or accept its dual bound from a VIPR file); (iii) each
fixed-integer NLP "optimal" claim has a KKT residual and a constraint
qualification diagnostic, using the separation-failure criterion of
[Tamm and Kronqvist, June 2026](https://arxiv.org/abs/2606.26897), who show
that near Slater violations approximate NLP solutions can fail to separate
the master iterate and cause cycling; (iv) the final gap claim survives
rationalization. Second deliverable: a `safe_cuts` option in MindtPy that
computes the tangent in floating point and then lowers the intercept by a
verified interval margin so the rational cut is guaranteed valid (the OA
analogue of safe Gomory cuts), with measured cost in iterations and bound.

### Gap it fills

The 2019 convex-MINLP comparison ([Kronqvist, Bernal, Lundell, Grossmann](https://link.springer.com/article/10.1007/s11081-018-9411-8))
already showed solvers reporting solutions within 0.1% without verification,
and the SCIP 8 global comparison ([Bestuzheva et al. 2025](https://arxiv.org/abs/2301.00587))
counted 16 inconsistent optimal values plus 23 infeasible returns for SCIP
and 26 inconsistent values for BARON on 1,000 runs. Nobody has measured how
often OA-type solvers' termination claims are exactly justified, nor which
component (cut rounding, master tolerance, NLP inexactness, CQ failure) is
responsible. Tamm–Kronqvist give the theory of the failure mode but no
auditing tool and no exact arithmetic. The repository's earlier rejection
concerned the inexact-cut *theorem*; this candidate is tooling and evidence.

### Closest prior work

- Hoen–Gleixner 2025 (MILP audit, SCIP only).
- Tamm–Kronqvist 2026 (cycling/CQ theory, ECP fallback; floating point).
- Coey–Lubin–Vielma 2020 (tolerance scaling for conic OA certificates).
- Hijazi–Bonami–Ouorou style CQ failures documented in the repository's
  numerics note; Neumaier–Shcherbina, Cook et al. (safe cuts, linear only).
- [Wei, Liu, Zeng, Feb 2026](https://arxiv.org/abs/2602.04122) (KKT-based
  cuts for nonsmooth convex MINLP) is a producer whose cuts would also be
  auditable by the same tool.

### Risk, effort, scores

Risk low: no MINLP audit tool found; the KTH group could add one to SHOT, but
SHOT is C++ and closed to a Pyomo-level audit. Effort: 4–6 weeks for the
audit tool on MindtPy (OA, ECP, LP/NLP-B&B via Gurobi callbacks) plus 2 weeks
for the safe-cut option and experiments. Scores: importance 7, feasibility 8,
novelty confidence 7.

## Candidate 3: sound structure recovery in Pyomo (big-M to GDP, semicontinuous to perspective / conic hull)

### Technical content

A Pyomo transformation that scans a flat MI(N)LP and (a) recovers disjunctive
structure from big-M rows `g(x) <= M (1 - y)` grouped by indicator, emitting
`Disjunction` blocks; (b) detects semicontinuous variables (`L y <= x <= U y`)
and convex constraints whose nonlinear variables are all semicontinuous on
the same indicator, and rewrites them with the perspective or the conic exact
hull (CEHR) of Gusev–Bernal Neira; (c) emits a *witness* for every rewrite.
Soundness for (a) is easy and should be stated: the recovered disjunction
`[y=1: g(x) <= 0] or [y=0: g(x) <= M]` is always equivalent; the residual
`g(x) <= M` is dropped only when interval/FBBT bounds prove it redundant. The
research content is: coverage statistics on MINLPLib and GDPlib-exported
big-M models (what fraction of instances hide GDP structure), the effect of
hull/CEHR reformulation on root gap and solve time with Gurobi/SCIP/BARON,
and where recovery is inconclusive (Sharma–Mahajan note that finding all
on/off sets can be as hard as solving the problem; the transformation must
return a safe fallback).

### Gap and closest prior work

- [SUSPECT (Ceccon, Siirola, Misener 2019)](https://link.springer.com/article/10.1007/s11590-019-01396-y)
  detects convexity/monotonicity on Pyomo DAGs but performs no reformulation
  and no disjunction recovery.
- [Sharma and Mahajan, SEA 2022](https://www.ieor.iitb.ac.in/files/faculty/amahajan/papers/sharma2022automatic.pdf):
  automatic perspective and separability detection inside Minotaur (C++,
  convex MINLP), 45% and 88% improvements on some instance classes. Closest
  prior work; no Pyomo/GDP counterpart, no big-M-to-disjunction recovery,
  no conic hull.
- [Bestuzheva, Gleixner, Vigerske 2023](https://www.researchgate.net/publication/373283652_A_computational_study_of_perspective_cuts)
  and SCIP's `nlhdlr_perspective` ([SCIP 8 MINLP paper](https://arxiv.org/abs/2301.00587)):
  semicontinuous detection and perspective cuts inside SCIP, including for
  nonconvex constraints; solver-internal, not a modeling-level transformation.
- [Belotti et al. 2016](https://link.springer.com/article/10.1007/s10589-016-9847-8)
  and [Bonami et al. 2015](https://link.springer.com/article/10.1007/s10107-015-0891-4):
  indicator detection and handling in MIP presolve, linear constraints only.
- `pyomo.contrib.preprocessing` plugins (`induced_linearity`,
  `var_aggregator`, `bounds_to_vars`, `equality_propagate`, ...) contain no
  structure recovery ([plugin list](https://github.com/Pyomo/pyomo/tree/main/pyomo/contrib/preprocessing/plugins)).
- Pyomo.GDP transformations ([Chen et al. 2022](https://link.springer.com/article/10.1007/s11081-021-09601-7))
  go in the forward direction only.

### Risk, effort, scores

Risk moderate: solver-internal detection exists, so a reviewer will ask what
is new beyond porting; the answers are the GDP recovery, the witness/fallback
contract, the conic hull option and the dataset-level coverage result.
Effort: 3–4 weeks for detection and transformation, 3 weeks for experiments.
Scores: importance 7, feasibility 7, novelty confidence 5.

## Candidate 4: verified reference values and convexity audit for benchmark sets

### Technical content

A methodology paper plus dataset: (i) re-audit the MINLPLib "convex" flags
with exact checks (rational `LDL^T` for quadratics, DCP-style rules on the
expression DAG); SUSPECT reported that 53 of 82 non-recognized instances
failed because of eigenvalue round-off and that trim-loss instances are
convex but undetected, so the current labels are known to be noisy;
(ii) publish certified lower bounds (from candidate 1) and rational-residual
incumbents for as many convex instances and GDPlib models as possible;
(iii) a cross-solver disagreement matrix (BARON, SCIP, Gurobi 13, SHOT,
DICOPT, SBB, MindtPy, GDPopt) evaluated on the *original* model in rational
arithmetic, in the spirit of PAVER's examiner but solver-independent and
Pyomo-native; (iv) instance-family gap analysis for convex GDP: conic
disjuncts, semicontinuous-heavy process models, multi-period GDP, which are
under-represented in both libraries.

### Gap and closest prior work

- [PAVER 2.0 (Bussieck, Dirkse, Vigerske 2014)](https://www.gams.com/~svigerske/publications/paver2_paper.pdf)
  is GAMS-trace based and checks against known bounds, not certificates.
- [Lundell's minlpbenchmarks](https://andreaslundell.github.io/minlpbenchmarks/)
  publishes PAVER reports for 2018–2020 studies; no methodology beyond that.
- [GDPlib](https://github.com/SECQUOIA/gdplib) (40+ models, GAMS/DICOPT,
  Gurobi, BARON benchmark profiles, AIChE 2024 talk) has a harness but no
  published paper, no certified values and no convexity metadata.
- Bestuzheva et al. 2025 and Kronqvist et al. 2019 supply the two large
  comparisons; both report inconsistent optima among failures.
- The [MIPLIB 2017](https://link.springer.com/article/10.1007/s12532-020-00194-3)
  selection methodology is the model for a principled instance selection.

### Risk, effort, scores

Risk: low for being scooped, moderate for reviewer perception ("engineering").
The value to the GDPlib maintainers is direct. Effort: 4–8 weeks, mostly
runtime; depends on candidate 1 for certified values. Scores: importance 8,
feasibility 8, novelty confidence 5.

## Candidate 5: MINLP delta debugging and metamorphic testing

### Technical content

Extend [MIP-DD (Hoen, Kamp, Gleixner, IJOC 2025)](https://doi.org/10.1287/ijoc.2024.0844)
([arXiv](https://arxiv.org/abs/2405.19770)) to nonlinear models at the Pyomo
level: modifiers that fix variables, drop constraints, replace nonlinear
subexpressions by their McCormick or tangent linearizations, tighten bounds,
or collapse expression trees, while preserving an oracle failure (solver
disagreement, violation of a certified bound from candidate 1, or an
infeasible "optimal" point). Add metamorphic relations specific to MINLP
(variable scaling, affine substitution, monotone objective transforms,
redundant constraint insertion, permutation as already used by Bestuzheva et
al.) and run BARON, SCIP, Gurobi 13, SHOT and DICOPT on the convex and QCQP
subsets.

### Gap and closest prior work

MIP-DD is MIP-only and contributed to 24 of 51 documented SCIP MIP fixes;
SCIP 10 ships it with SCIP/SoPlex interfaces. No delta debugger or fuzzer
for MINLP solvers was found; fuzzing literature covers SMT, CHC, MaxSAT and
compilers. Bestuzheva et al. 2025's failure counts show the target is not
empty.

### Risk, effort, scores

Risk low; the ZIB group might extend MIP-DD to SCIP's nonlinear constraints,
but a Pyomo-level, solver-independent tool is a different artifact. Effort:
3–5 weeks. Scores: importance 7, feasibility 8, novelty confidence 6.

## Candidate 6: parallel / asynchronous multi-tree OA (deprioritized)

### Technical content

Solve the fixed-integer NLPs for several solution-pool assignments in parallel
processes, inject cuts asynchronously into a single-tree LP/NLP-B&B via
Gurobi callbacks, and share cuts across OA variants (OA, L-OA/Q-OA
regularized, ESH) running as a portfolio.

### Why deprioritized

MindtPy already has a serial solution-pool option (default five assignments
per iteration, [docs](https://pyomo.readthedocs.io/en/stable/explanation/solvers/mindtpy.html));
SHOT runs single-tree with commercial MIP threads
([SHOT README](https://github.com/coin-or/SHOT)); DiPOA
([Olama, Camponogara, Mendes 2022](https://arxiv.org/abs/2210.06913))
already gives a multi-core distributed OA for separable convex problems; an
asynchronous parallel Benders method exists for stochastic network design
([Computers & OR 2023](https://www.sciencedirect.com/science/article/abs/pii/S0305054823003234));
and GPU spatial B&B work is under way elsewhere
([UConn STOGO talk 2025](https://psor.media.uconn.edu/wp-content/uploads/sites/1972/2025/10/2025-09-04-STOGO-Presentation.pdf)).
The convergence theory is trivial (cuts are valid in any order), so the
contribution would be purely empirical scheduling. Worth revisiting only if
candidate 2 shows that NLP time dominates on GDPlib-scale models.

Scores: importance 5, feasibility 7, novelty confidence 4.

## Other 2025–2026 items checked and not adopted

- [Tamm, Eichfelder, Kronqvist, warm-starting OA (2025/2026)](https://arxiv.org/abs/2507.08595):
  cut reuse across parameterized instances; complete, and a natural consumer
  of certified cuts from candidate 1.
- [Dai, polyhedral OA for MISOCP (Aug 2026)](https://arxiv.org/abs/2608.10055):
  cut-selection geometry; no verification aspect.
- [Göß, PWL versus global parabolic relaxations (Mar 2026)](https://arxiv.org/abs/2603.16505)
  and [Zha, Villanueva, Houska, Chachuat, superposition relaxations (May 2026)](https://arxiv.org/abs/2605.10854):
  relaxation-strength studies; certificates for their rows would fit rule 4.
- [Nguyen and Pulsipher, infinite-dimensional GDP (Aug 2026)](https://arxiv.org/abs/2608.27707):
  Julia, out of this scope.
- [Hoen and Gleixner analysis](https://arxiv.org/abs/2412.14710) and
  [Szeider CP 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2026.52)
  are the two templates candidates 1–2 imitate.

## Suggested next step

Start candidate 2 on MindtPy with the convex MINLPLib subset already ported
to Pyomo, because it yields the instrumentation, the rationalization
pipeline and a first empirical result within weeks; design the lemma format
of candidate 1 at the same time so that audited cuts become certificate rows
without rework. Contact the ZIB exact-MIP group before announcing candidate 1.
