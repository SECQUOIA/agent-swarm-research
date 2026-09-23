# Lean proofs for the cubic paper

This directory contains a 61-module exported dependency closure of the repository's
canonical Lean sources. Develop proofs in the canonical `formal/` project;
refresh the export instead of editing independent copies here.

The [coverage map](COVERAGE.md) connects the paper to declarations. The
[verification record](VERIFICATION.md) records the final checks and counts.
The [export manifest](verification/export.json) lists every source fingerprint
and the endpoint modules that determine this package.

The toolchain and Mathlib dependency are pinned by `lean-toolchain`,
`lakefile.toml`, and `lake-manifest.json`. With Lean installed, run:

```sh
lake exe cache get
bash scripts/verify.sh
```

The script checks that every proof source is imported, builds with warnings
as failures, audits all package declarations transitively, and replays the
proofs with `leanchecker`. It accepts only `propext`, `Classical.choice`, and
`Quot.sound`; an unfinished proof or additional axiom fails the audit.
Kernel replay uses the installed Lean kernel, not an independent kernel
implementation. Cached standard dependencies may be reused; the verification
record explains how the local check was performed.
