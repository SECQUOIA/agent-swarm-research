**These are diagnostic measurements of the completed implementations.** They
compare the archived phase-one grid solver with the new automatic decomposition
and shared tree engine, then separately exercise exact reconstruction, recourse,
TU constraints, and compact optimal-set certificates. They do not establish
competitive performance against production solvers.

The final evidence comprises **84 configurations: 73 main runs and 11
[extension runs](extensions/README.md)**. There are 82 valid certificate replays:
68 requests are completed and 14 return checked partial or unsupported-class
bounds. One invalid input is rejected and one boundary search is inconclusive
without an exact-output certificate. The [combined counts](combined-summary.json)
exclude every exploratory archive. Independent reference checks cover 62
numerical bound enclosures and two exact implicit-optimizer patches.

[Findings](FINDINGS.md), [results](RESULTS.md), and [machine-readable totals](summary.json) count only the
final runs in `results/`. The original 74 phase-one runs remain unchanged.
`results/pilot_baseline/` contains an initial harness pilot;
`results/archive_pre_sparse/` contains the runs made before the final sparse
polishing change; `results/archive_pre_recourse_fix/` contains the initial
recourse runs that exposed costly candidate ordering. These exploratory runs
are excluded from the final totals, and their source snapshots are retained.

Every configuration uses a two-second cooperative solve budget, a five-second
hard solver-process deadline, a separate five-second proof-replay deadline,
one thread, and a 512 MiB address-space cap. The saved result gives solve,
checking, total subprocess time, certificate size, and the separate peak
resident memories. A checked partial bound at a resource limit does not count
as completion of the requested solve. See the [protocol](PROTOCOL.md).

The box-QP corpus contains 25 original or generated models, 17 with independent
exact face-enumeration references. Generated random paths, bands, trees and
mixed instances use new fixed seeds without planted optima. Analytic recourse
and optimal-set fixtures are labeled explicitly. The constrained corpus has
separate exact references from exhaustive rational face KKT systems. The narrow
reference oracle checks that equality rows are independent.

The public inputs are from [QPLIB](https://qplib.zib.de/) (Furini et al.,
2018), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The two binary QPLIB models are the entire original problems. An independent
[coefficient audit](review/REVIEW.md) compares their parsed objectives against
separately retained GAMS equations. Current [QPLIB metadata](https://qplib.zib.de/instancedata.csv) contains three
continuous bound-only models, with 14,400–39,204 variables; one is not compact.
They exceed the declared 512-variable input screening cap. These
[screening refusals](data/continuous_input_audit.json) are not solver runs, and
there is **no solved continuous public-instance evidence** in this suite.
The metadata and source URLs are retained; public models were not sliced,
sparsified, or given artificial finite bounds.

Each final lane has immutable Python sources under `frozen/<lane>/`, a source
manifest, the exact rational proof artifacts, and replay outputs. The runner
checks source hashes before and after each lane and binds every produced proof
to the intended input model. The baseline input binding was independently
rechecked after its original run. Later documentation edits do not change the
archived code that actually ran.

To reproduce a lane without changing any saved evidence, run, for example:

```bash
python3 reproduce.py completed_sets /tmp/minlp-sets-reproduction
```

The destination must not exist. This restores the exact lane-specific runner,
corpus, references and solver snapshot in a fresh directory, then executes its
bounded configurations. The reproduction wrapper was checked on all five
optimal-set configurations, including their exact proof and membership checks.
The runner deliberately refuses to overwrite existing results or source
snapshots. Rebuild the final tables with `python3 summarize.py`.
