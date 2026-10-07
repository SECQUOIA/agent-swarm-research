# Archived empirical evidence

Prepared on 2026-10-05 from existing repository archives. No solver run, synthetic experiment, Monte Carlo trial, or mathematical experiment was rerun. New work consists of copying files, checking recorded counts and aggregation arithmetic, and presenting recorded node counts.

The portable package is `../reproducibility/`. `SOURCE-INVENTORY.json` identifies every copied original by its repository-relative path, byte count, SHA256 digest, and package path. The `archive/` tree preserves original paths and local imports. Original files were not changed. The package README, verifier, verification report, figure script, figure metadata, and figure files are new presentation or verification artifacts.

## Distinct recorded studies

| Study | Archived records | Cohort and protocol |
|---|---:|---|
| Synthetic SCIP tolerance exponents | 2,134 | 20 instances; seed 0; half-decade tolerances from 0.1 to 1e-7; different solver settings retained separately |
| MINLPLib branching-point study, retained runs | 1,254 | 57 instances; 855 core runs (5 settings, 3 seeds), 171 optional runs (3 settings, seed 0), 228 tolerance runs (19 small continuous instances, 4 settings, 3 nondefault tolerances) |
| MINLPLib branching-point study, other recorded batches | 673 | 486 screening runs, 171 diagnostic trace summaries, 16 additional diagnostic trace summaries |
| Robust branching MINLPLib study | 2,052 | Same selected names, separate study: 57 instances, 12 settings, 3 seeds; 60 CPU seconds per run |
| Robust branching synthetic SCIP study | 3,840 | 16 kink instances, 12 settings, 5 seeds, 4 tolerances (1e-2, 1e-4, 1e-6, 1e-8) |

The first MINLPLib note's 1,927 recorded runs reconcile exactly as 1,254 + 486 + 171 + 16. Only the 855 core records enter the five-setting, three-seed comparison. Screening and diagnostic batches must not enter its node ratios. The 128 KB `trace.jsonl` contains aggregated branch diagnostics, not raw node-by-node traces; it is included because the original analysis scripts use it.

The first study's core settings have respectively 170, 166, 138, 154, and 169 optimal runs out of 171 for `default`, `lp`, `lp_noclamp`, `mix_noclamp`, and `mid`. The no-clamp LP setting has 32 time limits and one crash. The separate robust study has 1,943 optimal records, 104 time limits, and 5 crashes. The synthetic exponent study has 1,655 gap limits, 420 optimal terminations, and 59 node limits.

Both MINLPLib comparisons use a shift of 10 nodes and bootstrap over instances. Their scripts differ at crashes: the first study averages available node counts within a setting's seed list, whereas the robust study omits an entire paired instance when a seed lacks nodes. Preserve these original conventions and the cohorts' separate 120/60 CPU-second limits. Reported limit counts are observations at termination, not completed-tree sizes; bootstrap intervals describe this selected benchmark and do not establish general solver superiority.

## Exact model evidence

The package also retains the original sparse regression and binary least-squares (MIMO) generation and presentation code, raw JSONL, and original numerical tables described in study-map sections S4 and S5. The 31 sparse C1 re-decisions supersede the corresponding earlier `capped` outcomes: 30 pass and one fails. Of 72 sparse branching-rule records, three have the removal half holding while full C1 fails; the source note's claim that removal fails whenever C1 fails is incorrect. Their `(p, alpha, seed)` identifiers are `(100, 1, 4000)`, `(100, 1.25, 4001)`, and `(200, 1.25, 4005)`. Largest-z trees have 13, 13, and 17 nodes, and most-fractional trees 23, 17, and 23. The new verifier checks these counts without solving any node.

The qflat2a `model` leaf-to-integral-bound range is 6.76–9.41 over all eligible half-decade observations. The narrower 7.4–9.4 statement in the source note covers full decades only and should not replace the all-record range. This arithmetic is checked in the package verifier. The binary least-squares C1 archive has 330 records, all decided (certified or refuted). These random-design studies illustrate finite-size transitions; they do not validate the asymptotic constants at their tested dimensions. Internal review scripts and logs are excluded from the portable archive.

`spatial-face-exact/kink_exact_runs.py` and its archived log use rational node data and exact width ties. At kink position 1/6, clamp 1/5, and tolerances 1e-2 through 1e-8, widest-side selection with ties to x has counts 13, 39, 167, 547, 1513, 4917, 19537; selection of x alone has counts 5, 9, 11, 13, 17, 19, 23. These support the distinction between multidimensional branching overhead and a single surviving chain. The incumbent example at position 1/3 distinguishes a coordinate-inside test from a whole-point-in-box test: with ties to y and incumbent (1/3, 0), their counts are respectively 7 throughout and 17, 49, 193, 513, 1537 at 1e-2 through 1e-6.

`robust-branching-points/exact2d.log` repeats the rational widest-side clamp counts and records finite recentring counts. `chain1d_D.log` records the recentring identity on 3,090 rational positions for each of five clamp parameters. Other `sim*.jsonl` files are archived summaries of floating-point or Monte Carlo model computations; these must not be called exact rational computations. Their original scripts and the C simulation source are included for provenance.

## Figure protocol

The node-scaling figure is derived only from `solver-validation/results/runs.jsonl`, with settings separated. It displays all available non-error records for selected named instances and settings, marks exhausted trees and node limits, and uses logarithmic tolerance axes. Node axes are logarithmic in panels (a), (b), and (d), and linear in panel (c), which shows additive growth per tolerance decade. Panel (c) displays model iso2/iso3/iso4 and default iso2/iso3, omitting default iso4 for legibility (its smallest-tolerance count is 3,431). No observations are averaged or pooled. Reference power curves describe theorem exponents, with an arbitrary vertical normalization; they are not fitted predictions of absolute counts. The plot script and metadata record every displayed record and the fit windows.

The original analysis rejects `nodelimit`, `timelimit`, and `error`, retains `optimal`, and groups by exact `(inst, setting, eps)`. A tail fit uses the last five available records after decreasing-eps sorting and filtering eps <= 1e-3; a wide fit uses all eligible eps <= 1e-2. Each fit needs at least three points and a log10 tolerance span of at least 0.99. Thus some tails use a short finite window and some fitted plateaus reflect exhausted trees. An exponent fit is descriptive and is not proof of an asymptotic theorem.

The archived `model` setting provides the known optimum as incumbent, disables heuristics, and uses best-first order. Its ordinary propagation remains enabled; the three changes were not separated. Calling it a rigorous numerical certificate would be inaccurate: SCIP works in floating point, feastol is 1e-9, and eps is a global absolute-gap stopping test. Default processing counts also reflect plunging, heuristic incumbents, propagation, and solver-specific reformulation. These are practical observations alongside idealized theorems.

`../reproducibility/FIGURE-CAPTION.md` supplies a complete caption. The figure contains 230 individual observations in 19 instance/setting curves, covering 14 of the campaign's 20 named instances. Its source line references and grouping were checked against the archived records by the read-only verifier.

## Availability and limits

SCIP 10.0.2 and PySCIPOpt 6.2.1 were used. The archived metadata report Python 3.13.11, SoPlex 8.0.2, and a Linux WSL2 x86-64 platform; MINLPLib metadata report Ipopt 3.14.19. The exponent note is dated 2026-09-28 and the branching studies 2026-09-29. The archive's files need not have been created on those exact note dates. Machine timing and deterministic counts should not be generalized to other installations.

External MINLPLib OSiL models and solver binaries are not included. Original scripts refer to `~/.cache/minlplib/minlplib/osil`; users seeking a fresh run would need those external inputs and the recorded solver stack. Repository metadata, selected-instance lists, original synthetic formulations, archived solutions used by feature extraction, and the local OSiL parser are included. Original generation scripts are preserved as evidence and were not executed during packaging. The new verifier requires only Python's standard library and never imports or invokes a solver.
