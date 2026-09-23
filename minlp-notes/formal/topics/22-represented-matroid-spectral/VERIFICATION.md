# Topic 22 verification

Date: 2026-09-22. **PASS.** The final source-frozen run completed successfully.
All 37 [frozen claims](CLAIMS.md) have Lean proofs and
[independent reviews](REVIEW.md).

| Targeted check | Result |
|---|---|
| Explicit topic build with warnings as errors | Passed: 65 modules |
| All-owned-declaration axiom audit | Passed: 1,680 declarations |
| Original-input execution examples | Passed: all three |
| Individual kernel replay | Passed: all 65 modules |
| Source and verification-helper hashes unchanged | Passed |
| Module discovery and canonical import coverage | Passed |

Run from `formal/`:

```sh
python3 topics/22-represented-matroid-spectral/verification/run_checks.py
```

The [runner](verification/run_checks.py) uses the pinned Lean 4.33.1 toolchain
and `LEAN_NUM_THREADS=1`. It checks that the explicit
[65-module inventory](verification/modules.json) equals the topic source
directory and that every module occurs in the canonical `Formal.lean`
imports. It builds those explicit targets with `lake build --wfail`.
Dependencies may be built or replayed by Lake; no project-root build is run.

The [axiom audit](verification/AuditMatroid.lean) checks all declarations
owned by these modules, including private and generated helpers. Its
[log](verification/axioms.log) records 1,680 declarations. Only `propext`,
`Classical.choice`, and `Quot.sound` are permitted. Production proofs use
no admitted declarations, custom axioms, or `native_decide`.

The preserved [execution client](verification/ExecutionExamples.lean) runs
with warnings treated as errors and checks exact original bases in three
assembled-producer examples: matroid rank zero with a nonzero prior,
positive matroid rank with zero information, and positive scalar information.
All three passed in the [execution log](verification/execution-examples.log).
The final case exercises normalization, shifted-label caching, the owner
marker, determinant interpolation, and deletion recovery. These finite
checks supplement the universal proofs; they do not establish complexity.

The runner invokes `lake env leanchecker` separately for every topic module.
It checks unchanged hashes for all topic sources, the audit, execution
client, inventory, and runner. The [manifest](verification/manifest.json)
records the exact modules, hashes, toolchain, Lake manifest hash, and
completion time. The independent review's
[source snapshot](REVIEW-FINAL-SOURCES.json) is recorded separately.

The counted original-input producer is `representedInputRun`.
Its value theorem identifies its output set with `representedSpectralCover`;
`representedInputRun_polynomial_work` bounds its charged work from original
matrix dimensions and input widths, with accuracy parameter `ceil(1/eta)`.
Only the information dimension is fixed. Schoolbook arithmetic and explicit
finite scans, storage, and copies are charged. Construction of proof and
cost-observer transcripts is excluded; no Lean wall-clock bound is claimed.
The scope does not include arbitrary independence-oracle inputs, finite-field
representations, intersections, or arbitrary correlated-history models.

The related source note and manuscript use the verified owner-count variant.
From `paper-correlated-measurements/`, this command passed:

```sh
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The [67-page paper](../../../paper-correlated-measurements/paper.pdf) rebuilt
without LaTeX warnings, undefined references, or overfull/underfull boxes.
Pages 1 and 28 were rendered and inspected. The manuscript source archive
was refreshed, and every archived source was checked against the repository
copy. [Paper build hashes](verification/paper-build.json) record source and
artifact hashes. The numerical supplement was unchanged; its experiments
were not rerun for this proof and documentation change.

All 37 claim IDs have coverage entries, and all 65 independent final-review
source hashes match the verified sources. Targeted local Markdown links and
`git diff --check` passed. `sha256sum -c artifacts.sha256` passed for the
paper deliverables.

No project-wide local verification was run. CI status and logs were not
inspected.
