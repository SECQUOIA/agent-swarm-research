# Frozen experiment source versions

- `primary`: V1, used for the uniform 289-instance campaign and original separate replay; 152 tests.
- `producer-repair`: V2, changes only long-rational proof normalization and adds its regression; 153 tests. All twelve observed producer conversion failures were regenerated.
- `reporting-repair`: V3, repairs exact rational report input/output and optional floating displays; 161 tests. Two affected completed proofs were replayed without optimization.

Each directory contains the complete certify/lbesh Python modules and tests plus its module manifest. V2 and V3 additionally retain the actual timed wrapper under `experiments`; its SHA-256 matches the relevant frozen protocol. Top-level portable wrappers were subsequently corrected to use supplied local paths and record the actual local package versions. Mathematical proof/domain/curvature/propagation rules are unchanged between these versions. The current distributed `lab` modules are V3. Original V1 saved primary counts are 203/19/67; V3 accepts the additional primary tls12 proof, giving an expected fixed-artifact replay count 204/18/67. Timings and original outcomes remain attached to their recorded version.


## Restoring a source version

The version directories preserve the frozen production modules, version-specific
test source, and original manifests unchanged. Shared test fixtures and fixture
helpers under `certify/tests/review_artifacts`, and the quadratic example under
`certify/examples/quadratic`, are supplied separately in `shared-data/`. Its
supplemental `manifest.json` identifies every shared file. These data are the
same as the default core's fixtures/example; they are not new historical source
files and do not alter any frozen module manifest. Existing V2/V3 fixture copies
are byte-identical to the shared copies. The quadratic README includes the
portable-supplement notice; model, lemma, master, and proof bytes are unchanged.

In a separate copy of the extracted evidence tree, run the following from its
root, choosing `primary` (V1), `producer-repair` (V2), or `reporting-repair` (V3):

```sh
snapshot_version=primary
rm -rf lab/certify lab/lbesh
cp -a "evidence/source-snapshots/$snapshot_version/certify" lab/certify
cp -a "evidence/source-snapshots/$snapshot_version/lbesh" lab/lbesh
cp -a evidence/source-snapshots/shared-data/certify/. lab/certify/
```

Restoration replaces versioned code rather than overlaying it, then restores the
common data needed by tests and `reproduce.py small`. Run the test and small-replay
commands in the main README. Expected test counts are 152 (V1), 153 (V2), and
161 (V3). Do not run restoration in the original manifest-verification tree:
its source files intentionally change when a different version is selected.
