# Many-leaf reciprocal hull: targeted verification

All 67 topic modules passed the final warning-free targeted build. The axiom
audit passed for 1,936 declarations, including private and generated
declarations. Only `propext`, `Classical.choice`, and `Quot.sound` are allowed.

The root agent ran the following commands from `formal/`:

```sh
lake build --wfail $(cat topics/13-many-leaf-reciprocal/verification/modules.txt)
lake env lean -DwarningAsError=true topics/13-many-leaf-reciprocal/verification/Audit.lean
```

The [module list](verification/modules.txt) contains only the modules belonging
to this topic. The [build log](verification/build.log) records a successful
build. Its Lake job total includes cached dependencies; it is not a count of
changed modules or evidence of project-wide verification. The
[audit source](verification/Audit.lean) selects declarations by their owning
module, and the [audit log](verification/axioms.log) records the result.
All 67 modules are imported by the canonical `Formal.lean` entry point;
that project-wide entry point was not built locally.

## Executable examples

Before the final grouped build, the root agent also ran targeted builds of
`ManyResults`, `ManyMembership`, `ManyMembershipExamples`, `ManyOracleExamples`,
`ManyFastLawSize`, `ManyWitnessLists`, and `ManyWitnessExamples`, each with
`--wfail`. Their final runs passed.

The example modules use Lean kernel reduction, not native-computation axioms:

- The membership checker accepts the exact two-leaf minimum `31/50` and
  rejects `3/5`. Zero-leaf acceptance and mean-bound rejection also pass.
- The oracle returns a cut violated by exactly `1/50` for the counterexample.
  Mean, leaf, and upper-reciprocal rejection branches are checked separately.
- The executable witness has total mass one, mean two, reciprocal mean
  `31/50`, and the exact two leaf and two product moments in its actual output.

The algorithm review's additional focused executable checks are retained in
[ReviewAlgorithm.lean](verification/ReviewAlgorithm.lean) and
[review-algorithm.log](verification/review-algorithm.log).
Independent statement and cost-model reviews are linked from [REVIEW.md](REVIEW.md).

## Source and scope

[Source fingerprints](verification/SOURCES.sha256) identify the checked proof
sources, toolchain, manifest, audit, and package documents.
The [delivery record](verification/delivery.json) records the module/import
match and entry-point fingerprint at the time of the check, complete obligation
IDs, local documentation links, and fingerprint check.

Complexity bounds use the documented schoolbook arithmetic cost model. They
do not claim refinement to compiled Lean arithmetic, machine instructions, or
the existing Python script. Empirical solver comparisons and novelty remain
outside the mathematical verification claim.

No project-wide build, project-wide verification, full-project kernel replay,
or CI status/log inspection was run. CI handles project-wide verification
under the [local verification rule](../../../AGENTS.md).

## Audit rerun on 2026-09-25

Commit `fa2a6f42` split the audit's final `PASS` message across two source
lines; the declaration selection and axiom check did not change. For
consistency the audit was run once more from `formal/` at `d85171b8`, with
`$HOME/.elan/bin` on `PATH` and `LEAN_NUM_THREADS=4`:

```sh
lake env lean -DwarningAsError=true topics/13-many-leaf-reciprocal/verification/Audit.lean
```

It exited 0 in 17.6 s and printed
`PASS: audited 1936 declarations in 67 extension modules; only propext, Classical.choice, Quot.sound are allowed.`,
matching the [delivery audit log](verification/axioms.log). Beforehand,
`lake build --no-build` on the 67 listed modules reported all targets up to
date, so the audit read outputs built from the current sources. The build and
examples were not rerun.

The [source fingerprints](verification/SOURCES.sha256) are a delivery-time
snapshot. Checked from the repository root with
`sha256sum -c formal/topics/13-many-leaf-reciprocal/verification/SOURCES.sha256`,
they now report three mismatches:

| File | Reason for the mismatch |
|---|---|
| `formal/topics/13-many-leaf-reciprocal/VERIFICATION.md` | This dated section was added to the record. |
| `formal/topics/13-many-leaf-reciprocal/verification/Audit.lean` | The message rewrap in `fa2a6f42` described above. |
| `results/common-factor-reciprocal-anchor-full-hull.md` | Commit `367fcbc8` corrected the result note: the hull statement allows real endpoints, and exact rational evaluation assumes rational endpoints and coordinates. |

No Lean proof source, toolchain file or `lake-manifest.json` differs. No project-wide
verification or CI inspection was run.
