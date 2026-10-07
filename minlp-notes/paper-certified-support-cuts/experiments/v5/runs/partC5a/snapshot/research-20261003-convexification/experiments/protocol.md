# Prospective native-model campaign

Frozen on 2026-10-03 before any new-holdout optimization outcome. This
campaign tests whether cuts on the original model improve outcomes after the
first campaign found an unfavorable default-activation result. A negative
result is a completed experiment; it does not trigger instance replacement or
an outcome-tuned second selection.

The new population contains 30 cached MINLPLib OSiL models. Exclude all 123
names excluded by the first campaign and every model in that campaign. Retain
models with at most 120 variables, 180 constraints and 250,000 OSiL bytes,
at least two nonfixed variables with finite declared bounds, and at least one
quadratic, polynomial or general nonlinear function according to the archived
metadata. The legacy OSiL parser must read the file; this is a syntax filter,
not a filter for the new importer or separator. The frozen selection file
records parser errors. It includes all failures after selection in the results.

Stratify by archived metadata into convex models, nonconvex models without
integer variables, and nonconvex models with integer variables. Select ten
per stratum in ascending SHA256 order of `convexification-holdout-v2:` plus
the instance name. Run the selected 30 in that same hash order. There are
422 eligible models, with stratum counts 85, 208 and 129. The exact selected
files, hashes, excluded names and eligible ranking are saved in
`holdout-selection.json`. Public instances may appear elsewhere in this
repository; "new holdout" refers to the named previous convexification
campaigns, not to all historical work on MINLPLib.

Compare three modes: `baseline` with native nonlinear constraints, `all` with
bounded original-row cut generation, and `auto` with the frozen admission
policy. Every mode uses the same original-model builder, including any source-domain
auxiliaries required to preserve implicit log, division or power restrictions.
These common domain auxiliaries are recorded and checked. There is no separate
reformulation control because cut activation introduces no nonlinear feature
equalities or graph-variable reformulation. If the final method does require
such structural changes, amend this protocol before the first outcome to add
an explicit control. Do not label an identical mode as a separate control.

Primary runs use seed 0, a 30-second soft total budget including source loading, exact model serialization and hashing,
analysis, certificate generation, model construction and solving, one SCIP
thread, one BLAS/OpenMP thread, and relative gap tolerance 1e-4. A single worker
runs at a time. Imports and independent result checking are included in outer
wall time but excluded from the solver budget. A 30-second full-run process has a 45-second
hard wall limit; ten-second mechanism processes have 20 seconds and five-second
root processes have 15 seconds. Nonpreemptive calls may overshoot the soft budget, and these
overshoots must be reported. Missing cut logs imply unknown counts.

Run phases in this fixed order:

1. Full runs on all 30 new holdout models, all three modes.
2. Full diagnostic runs on the previous lost solve `genpooling_lee2`, prior
   importer failures `syn15m`, `cvxnonsep_psig30r`, `cvxnonsep_pcon40r`,
   `syn10hfsg`, `btest14`, `ghg_2veh`, and `chp_partload`, and previous hard
   cases `kall_circles_c6b` and `waterno2_06`. These ten results remain separate
   from the new holdout. Run all three modes at 30 seconds.
3. Full mechanism runs at ten seconds on the 13 original synthetic cases in
   `cases.py`, all three modes. Their known optima and feasible witnesses are
   independent checks, not evidence of population performance.
4. Root-only runs on the new holdout and five mechanisms
   (`quartic_balance_8`, `exp_pair`, `simplex_quadratic_vector`,
   `overlapping_products`, `star_marginal_inconsistency`) at five seconds and
   one node, all three modes.
5. Seed-1 30-second full repeats on the first six hash-ranked new holdout
   models, all three modes. This fixed small subset measures sensitivity; it
   does not estimate a broad population effect.

Within each phase and model, rotate mode order by model index: baseline/all/auto,
all/auto/baseline, then auto/baseline/all. The total campaign has a 150-minute
emergency aggregate wall cap, exceeding the 142.75-minute sum of all 282
phase-specific per-process hard timeouts. This cap is a fault safeguard; completing all scheduled jobs is the
objective. Record every unstarted job after that cap as
`campaign_budget_exhausted`. Never omit these jobs from the completion table.
The fixed phase order prioritizes complete new-holdout comparisons.
The environment hosts unrelated jobs; subsecond timing differences are
descriptive, and no unrelated process is terminated.

Freeze and copy the source before the first primary run. Save source hashes,
dependency versions, original OSiL files and hashes, exact binary64-tagged
parsed models, solver statuses, bounds, original-variable incumbent values,
nodes, cuts and certificates, rejected/accepted structures, timing and
selection work. A preflight can exercise syntax, known synthetic models and
record serialization but must not optimize any new-holdout model. Correctness
or instrumentation repairs after the freeze preserve all old output and
document why affected runs were repeated; performance-only changes cannot
replace this prospective campaign.

Evaluate every returned incumbent against all original rows, bounds,
integrality restrictions, domains and objective using an evaluator independent
of the model builder. Scaled numerical tolerance is 1e-5. Check all recorded
dual and root bounds against known synthetic optima or archived feasible
MINLPLib bounds with explicit tolerance. A reference conflict is a flag,
not automatic proof of a solver bug or of an inaccurate reference. These
checks do not certify a complete SCIP solve.

Replay each saved added cut in a fresh process against its archived original
model and the actual binary64 row supplied to SCIP. Missing or failed replay
must be counted explicitly and excludes a certification claim. Include
tampering checks. The independent reviewer owns replay and metric checks;
the campaign owner reports complete raw output, coverage, solved counts,
paired final/root bound comparisons, time, overhead and all adverse outcomes.
The prospective default decision is native baseline unless auto gives
credible benefit without invalid cuts, model changes or lost solves. A small
favorable count alone is insufficient for a general deployment claim.

Verification is restricted to this topic. Do not run project-wide tests or
inspect CI status or logs.
