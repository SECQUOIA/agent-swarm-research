# Verification record

## Current mathematical completion

The completion adds seven modules, for 48 bundled proof modules and 827
audited declarations. The warning-free build, full import coverage, and
transitive axiom audit and full kernel replay have passed. The
[completed log](verification/completion-run.log) records the successful run.

The local standalone project cache was initially absent. Its proof modules
were built from the exported sources, with an ignored symlink reusing only
the canonical installation’s pinned standard dependency packages and their
caches. No canonical project proof objects were copied into this package.
This is not a new dependency download or a from-source Mathlib rebuild.

All 48 exported proof sources and pinned configuration files match the
canonical source manifest. The rebuilt paper has 11 pages and no unresolved
references, overfull boxes, or layout/package warnings. Its changed appendix
pages were rendered and inspected. The local bundle check covers source
fingerprints, local links, four printed examples and 330 cutoff-law states.
The examples additionally have universal-theorem instantiations checked by
Lean; their verification no longer rests only on supplemental arithmetic.

The [completion review](../verification/completion-review.md) records the
mathematical statement review. The [coverage guide](COVERAGE.md) includes
general envelopes, actual original-box term gaps, exact construction sizes,
sparsity, family asymptotics, and every printed example.

## Historical 41-module verification

Local verification on 2026-09-13, using pinned Lean 4.33.1 and Mathlib
v4.33.1. The [coverage guide](COVERAGE.md) states the mathematical scope.

| Check | Result |
|---|---|
| Standalone build, warnings treated as failures | PASS: all 41 proof modules, compiled outside the parent repository |
| Explicit root import coverage | PASS: all 41 proof modules |
| Transitive axiom audit, including private helpers | PASS: all 733 bundled declarations |
| Printed principal endpoint axiom sets | Only `propext`, `Classical.choice`, and `Quot.sound` |
| Kernel replay of the complete standalone project | PASS: all 41 proof modules and the root import module; process exit status zero |
| Export comparison against canonical sources | PASS: all 41 proof files and pinned dependency configuration |

## Isolation and reproduction

The test copied the standalone package to a temporary directory outside the
repository. Its project build cache was initially empty. The pinned standard
dependencies and their existing compiled caches were copied into that
directory to avoid downloading them again. No project proof objects or
symlinks into the original repository were supplied. This is a fresh build
of the exported project sources against cached standard dependencies, not a
fresh download or a from-source rebuild of all dependencies.

The [complete run log](verification/run.log) records the unchanged bundled script:

```sh
bash scripts/verify.sh
```

Run it from this directory after the initial `lake exe cache get` described
in [README.md](README.md). The script checks module coverage, builds the
root with `--wfail`, executes `Verify.lean`, and runs
`LEAN_NUM_THREADS=1 lake env leanchecker -v Formal`.

The axiom audit rejects unfinished proofs, custom axioms, and
native-computation axioms transitively. Kernel replay uses the installed
Lean kernel, including the project's private compiled declarations, with
imported Mathlib and standard dependencies as its base. It is not a separate
kernel implementation and does not replay Mathlib from scratch. No external
solver or finite numerical sample is a trusted theorem premise.

## Source provenance and companion paper

The [export manifest](verification/export.json) records the endpoint modules,
source count, and hashes of the canonical files copied into this project.
The only canonical dependency cleanup moved the unchanged `CubicGap.hullGap`
definition from `CubicGap/Results.lean` into `CubicGap/Envelope.lean`, retaining
its explicit typeclass parameters, and narrowed the import in
`MultilinearGap/EnvelopeBounds.lean`. This removes unrelated cubic example
modules without changing any theorem statement or mathematical definition.

After that cleanup, the original project's 140-module root build and its
14,663-declaration transitive axiom audit also passed. Earlier topic manifests
describe historical source snapshots; this standalone distribution has a
fresh export manifest and its own delivery fingerprints.

The paper was compiled in the standalone directory and in the isolated
copy. Both builds have 11 pages and identical extracted text, with no
unresolved references/citations, duplicate labels, overfull boxes, or
remaining LaTeX warnings. All pages were rendered and inspected. The
[paper build report](../verification/paper-build.json) and
[isolation record](../verification/isolation.json) record the checks.
The [bundle check](../verification/bundle-check.json) validates local links,
exported source fingerprints, four printed table rows, and 330 cutoff-law
states with exact rational arithmetic. These finite calculations supplement
the universally quantified Lean proofs. The
[review record](../verification/review.md) states the written-proof and
layout review scope.

This preparation included a local mathematical and specification review;
it did not commission new independent reviewers or establish publication
priority. The antecedent formalizations had internal agent reviews. Neither
those reviews nor the local build are external peer review or a hosted CI run.
The general individual-envelope identity and the elementary size calculations
are distinguished from the Lean endpoints in [COVERAGE.md](COVERAGE.md).
