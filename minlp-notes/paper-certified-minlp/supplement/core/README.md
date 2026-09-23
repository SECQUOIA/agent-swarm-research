# Reproduce the certified convex MINLP experiments

Start with the small core archive. It contains the checker, all 289 interpreted
input models, compact original records, source and primal audits, and four small
complete example bundles. The bulk certificate archive adds all historical
completed proof artifacts and uniform-campaign attempts, the twelve producer-repair cases, and both targeted
reporting-repair proofs. Extract both into the
same directory only when full proof replay is desired. No private repository or
vendor solver is needed for checking completed proofs.

Use Python 3.13 and the five pinned checker dependencies:

```sh
python3 -m venv replay-env
replay-env/bin/python -m pip install -r requirements-checker.txt
replay-env/bin/python reproduce.py verify
replay-env/bin/python reproduce.py summaries --out /tmp/minlp-summary.json
replay-env/bin/python reproduce.py small --out /tmp/minlp-small-checks
```

`small` checks the quadratic optimum 1/4, the exact `clay0204m` optimum 6545,
`batchdes`, and the repaired-generation `risk2bpb` bound. It independently reruns
the original-variable feasibility and GAMS/Pyomo source comparison for the two
saved solver discrepancies. Reports go to the new output directory. Archived
records are unchanged. The objective values of master solutions or MINLPLib
references are not treated as nonlinear primal certificates.

After extracting the bulk archive, full replay is optional and can require
substantial time, memory, and tens of gigabytes of extracted disk space:

```sh
replay-env/bin/python reproduce.py replay historical --jobs 6 --out /tmp/historical-replay.jsonl
replay-env/bin/python reproduce.py replay uniform --jobs 6 --out /tmp/uniform-replay.jsonl
```

These calls create a new environment/input manifest and check every attempt,
including missing and rejected evidence. The old manifests contain absolute
paths from the producing machine for provenance. The portable commands use the
layout relative to this script; those old paths are not required. The historical
saved outcomes used optional external `viprchk` corroboration as well as internal
proof replay; these portable commands use the internal proof kernel alone.
Differences in environment or checker changes require a new output campaign.

The input models and recorded library reference values carry MINLPLib attribution
and exact source hashes; see ATTRIBUTION.md. The baseline run scripts are stored
for provenance and contain the original machine paths; `reproduce.py` is the
portable checker/audit entry point. Baseline solvers and proof generation are
separate from replay and may require licensed dependencies.

New generation uses `experiments/run_uniform.py`, `scip-uniform.set`, and the
frozen protocol. It additionally needs the solver-lab generation dependencies,
Gurobi, IPOPT, exact SCIP, viprcomp and viprchk. Supply local tool paths through
CLI arguments and use a new output directory. The included `lab/pyproject.toml`
and `uv.lock` record the original broader development environment; they are not
required to run the checker-only commands above. All attempts and the 360-second
outer cap must remain in the denominator when regenerating the campaign.

The paper's generated tables are derived from saved records using the accompanying
analysis script. Timing records describe the recorded machine and workloads;
reproduction is not expected to return identical timing or numerical-search
artifacts. Exact replay of fixed evidence has a specified acceptance contract.

To regenerate the exact tables from the compact saved records:

```sh
replay-env/bin/python experiments/analyze.py --lab lab --campaign experiments/uniform-20260913 --out /tmp/reproduced-tables
```

After extracting the bulk archive, `reproduce.py verify --bulk` checks every
archived file against its manifest. This reads all large proof files. Core
verification and the four representative replays do not require that archive.
The exact first-failed proof-step extracts are also recomputed by `small`.

To reproduce numerical generation with locally installed solver tools, add
`gurobipy==13.0.3` to the five checker dependencies, arrange a working Gurobi
license, and provide exact SCIP's `scip`, `viprcomp`, `viprchk` executables in one
directory and IPOPT as a separate executable. For example:

```sh
replay-env/bin/python experiments/run_uniform.py --lab lab --out /tmp/new-uniform-campaign --scip-bin /local/scip-exact/bin --ipopt /local/ipopt
replay-env/bin/python experiments/verify_protocol.py /tmp/new-uniform-campaign
replay-env/bin/python experiments/select_replay.py /tmp/new-uniform-campaign
```

The five-package checker environment, plus the explicitly optional generator
package and solver executables, is sufficient for this pipeline. The broader
`uv.lock` includes unrelated development packages with local source references
and is provenance, not an installation recipe for the standalone supplement.
The recorded hashes identify the tested external executable builds. Numerical
generation can differ on another machine even with the same requested budgets.

The focused checker tests are included under `lab/certify/tests`. They use an
optional pytest dependency, separate from the five-dependency replay environment:

```sh
python3 -m venv test-env
test-env/bin/python -m pip install -r requirements-tests.txt
cd lab
../test-env/bin/python -m pytest -q certify/tests -p no:cacheprovider
```

The saved primary replay has **203 verified, 19 rejected, and 67 missing**
records under source version V1. Two ordinary representation defects were then
repaired in separately recorded stages. V2 replaces Python's guarded decimal
integer conversion in producer proof normalization with FLINT rational parsing;
all twelve affected generation cases and their separate replays succeeded. V3
repairs parsing and serialization of unusually long rational bound reports and
makes optional binary64 displays unavailable when out of range. Both affected
completed proofs, for `tls12`, passed full targeted replay under V3. None of
these changes modifies the mathematical proof, curvature, domain, propagation,
or master-matching rules.

The default `lab/certify` sources are V3. Consequently a fresh full replay of the
fixed primary artifacts is expected to produce **204 verified, 18 rejected,
and 67 missing**, subject to the documented timeout and environment limits.
The saved V1 counts remain the experiment's original outcome. `summaries` and
`analyze.py` summarize these saved records and do not silently replace them.
Complete V1, V2, and V3 module/test copies are in
`evidence/source-snapshots/{primary,producer-repair,reporting-repair}`. To recover
a historical version, make a separate copy of this evidence tree and follow
`evidence/source-snapshots/README.md`: replace the versioned `lab/certify` and
`lab/lbesh` directories, then copy the separately hashed `shared-data/certify/`
fixtures and quadratic example into `lab/certify/`. The original snapshot
manifests and version-specific test source remain unchanged. Expected restored
test counts are 152 (V1), 153 (V2), and 161 (V3), and `reproduce.py small` works
with each version. Do not restore versions into the tree whose core manifest
you intend to verify.

The repair wrappers used in the actual runs are preserved under their source
snapshots' `experiments` directories, with hashes matched to the frozen
protocols. The top-level repair wrappers additionally accept the portable
layout and local tool paths. These portable path and environment-provenance corrections were
made after timing; the producer and checker snapshots identify the actual
versions measured. Frozen manifests' absolute paths are provenance.

The best-available bound catalog merges 405 accepted proof records into 222
model entries, requiring matching original model hashes and objective senses
and selecting the strongest exact signed normalized bound. This is a catalog,
not a uniform success rate. All candidate records and selected proof provenance
remain available. Recreate it from compact saved records with:

```sh
replay-env/bin/python experiments/bound_catalog.py --lab lab --paper . --out /tmp/reproduced-catalog
```

`tables/repair-summary.json` and `repair-results-text.tex` state the separately
preserved V2/V3 outcomes. Optional regeneration uses the current V3 producer;
recover the V1 snapshot in a separate tree to reproduce its precise behavior.

To verify the entire compressed bulk archive without extracting tens of
gigabytes, run the streaming readback below. It checks every archived byte and
symlink against the manifest, without depending on the original repository.

```sh
replay-env/bin/python experiments/verify_archive.py /path/to/certified-minlp-certificates.tar.gz bulk-manifest.json --out /tmp/bulk-readback.json
```

Regenerate the separate repair summaries with:

```sh
replay-env/bin/python experiments/analyze_repairs.py --experiments experiments --out /tmp/reproduced-repairs
```

After bulk extraction, replay the twelve producer-repair bundles with the final
checker using explicit relative paths (all twelve are expected to verify):

```sh
cd lab
../replay-env/bin/python -m certify.recheck --records ../experiments/producer-repair-20260913/generation.jsonl --outroot ../experiments/producer-repair-20260913/replay-artifacts --instances instances/py --out /tmp/producer-repair-replay.jsonl --jobs 6 --timeout 1200
cd ..
```

Replay exactly the two reporting-repair targets, including the secondary failed
default attempt, without any optimization tools:

```sh
replay-env/bin/python experiments/replay_reporting_repair.py --lab lab --primary experiments/uniform-20260913 --secondary experiments/producer-repair-20260913 --out /tmp/reporting-repair-replay
```

Both commands create new records. The second additionally repeats the recorded
selection audit across all primary rejections and secondary attempt reports.
