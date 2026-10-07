Targeted verification is complete for this benchmark package. No project-wide
verification or CI inspection was performed.

The final main suite runs these six commands, each from the repository root,
after its source owners' final readiness signal and an immutable `--freeze`
snapshot:

```sh
python3 research-20261002-decomposition/completion/benchmarks/run_benchmarks.py --run baseline
python3 research-20261002-decomposition/completion/benchmarks/run_benchmarks.py --run completed_grid
python3 research-20261002-decomposition/completion/benchmarks/run_benchmarks.py --run completed_exact
python3 research-20261002-decomposition/completion/benchmarks/run_benchmarks.py --run completed_recourse
python3 research-20261002-decomposition/completion/benchmarks/run_benchmarks.py --run completed_constraints
python3 research-20261002-decomposition/completion/benchmarks/run_benchmarks.py --run completed_sets
```

These commands produced 73 configurations and 72 successful independent proof
replays. Sixty-one completed the requested mathematical result. Eleven returned
valid partial bounds at resource limits, and one invalid TU input was correctly
rejected. The [artifact audit](review/REVIEW.md) checks original-model binding,
exact references, replay outputs, source hashes, table-state counts, recorded
times and archive exclusion. The [extension verification](extensions/README.md)
adds 11 configurations, seven completed results, and ten valid proof replays.
Its independent audit also repeated all ten retained proof checks under the
same process limits.

Additional targeted checks actually run:

- Independently compared every coefficient and binary domain in the two full
  QPLIB inputs against their retained GAMS equations, and checked source byte
  equality and the current continuous-input metadata screen.
- Computed independent exact stationary-face references for all 17 eligible
  small box models and all eight constrained models. Constrained references
  check independent equality rows and exact feasibility.
- Validated 120 fixed-seed random decompositions, for one through twelve
  variables, using `BoxQP` tree, running-intersection and factor-coverage checks.
- Ran `python3 research-20261002-decomposition/completion/benchmarks/reproduce.py completed_sets /tmp/minlp-completion-sets-reproduction`.
  All five restored configurations passed their proof and membership checks.
  This separate reproducibility run is excluded from benchmark totals.
- Parsed the benchmark entry-point Python files, resolved all 13 local links
  in the top-level benchmark documents, and checked the combined 84/82 counts
  against the separately audited main and extension artifacts.
- Ran `python3 research-20261002-decomposition/completion/benchmarks/summarize.py`.
  The independent review confirms the final aggregates: 84 configurations,
  82 replayed certificates, 68 completed outcomes, 14 checked incomplete bounds,
  and two outcomes without certificates.

The initial baseline pilot, runs before sparse polishing, runs before recourse
candidate-ordering fixes, and the extension run before integer-lattice stopping
are retained in explicitly named archive directories and excluded from final
counts. The original 74 phase-one runs and snapshots were not changed. Later
documentation-only changes to producer files do not alter the source snapshots
that were measured; reviewers checked that no executable dependency change was
hidden by that distinction.
