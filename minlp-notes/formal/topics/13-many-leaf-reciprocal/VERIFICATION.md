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
