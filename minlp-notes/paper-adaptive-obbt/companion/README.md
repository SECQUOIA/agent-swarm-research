# Adaptive and iterated OBBT: reproducibility companion

This companion contains byte-identical archived evidence and reference source.
No numerical experiment or archived analysis was rerun while preparing it.
`archive.tar.gz` preserves the original repository-relative layout. Extract it
into a new directory before using any of the documented commands below.
`MANIFEST.json` lists each member's original path, size, and SHA-256 digest;
`SEPTEMBER-INPUTS.json` records retained input coverage and source locations.
Every September result file is included.
Read [ERRATA.md](ERRATA.md) for mathematical corrections to the older reports;
the manuscript contains the revised statements and proofs.
The manifest does not hash itself. It hashes the archive, this README,
the retained-input record, the verification script, and the errata.

## What is included

The October archive contains the complete `campaign-01`: all 120 raw outcomes,
120 full logs, the exact pre-campaign source snapshot, task/configuration and
machine metadata, summaries, diagnostics, and original hash records. All frozen
normalized inputs, compressed original OSiL inputs, the pre-outcome admission
manifest, and authoritative frozen protocol are present. The separate four-model
pilot and its own source snapshot are also present, but pilot outcomes do not
enter campaign summaries. The campaign driver log, original report, and
independent solver review are retained.

The rational reference implementation is under
`research-20261003-adaptive-obbt/theory/`: `certificates.py`,
`certified_driver.py`, related mathematical descriptions, targeted check scripts,
and the saved reference-check outputs. The original sibling-module layout is
preserved, so its direct imports work when scripts are invoked by their paths.
These exact checks concern their explicitly defined rational lifted relaxation
family. They do not prove exact feasibility of numerical incumbents or certify
native SCIP relaxations or an entire MINLP solve.

The September material contains the original report and its correction review,
the seven experiment modules plus the existing tangent-map module, the entire
`results/` directory, all three raw JSONL streams, and historical metadata and
probe-pool inputs. The complete results include all 4,589 tightened boxes,
377 FBBT boxes, 640 root solution vectors, and 339 final solution vectors.
The 377 candidate OSiL files and every locally retained solution/cache-marker
file for those candidate names are also included.
The September study uses external OBBT preprocessing and restarts, realistic
root-incumbent cutoffs, and separate known-optimum diagnostic trajectories.
October instead adds a local propagator to SCIP and uses no supplied optimum
or external feasible point. Native SCIP LP-based OBBT remains enabled in every
October arm. Neither empirical policy implements the reference all-future
protected-box or matrix-tail machinery.

September's corrected SCIP solved counts are 573 for the control and 563 for
`pipe-r5`. The archived table still says 574 and 564: `solved=True` must be
combined with `wrong=False` in `final_outcomes.csv`. The original time/node
summaries also use the old success rule and remain uncorrected. Round one
changes a bound on 239 of 339 known-cutoff trajectories. The report's Section 0
and independent review explain these and other corrections; the unchanged body
is not authoritative where it conflicts with them.

October has 14/40 solves in each arm, with no new/lost solves. Adaptive uses
1,719 directional LPs versus 2,172 fixed, but propagator time is 23.123433 versus
19.529969 seconds. Short timings on a shared machine establish no total speedup
and no statistically established slowdown. The cohort is selected: 12 public
models admitted using historical outcomes, eight synthetic stress models, and
two repeated seeds per model. Historical family labels can still separate
closely related applications.

## Dependencies and exclusions

Archive inspection and digest verification need only Python's standard library.
The exact certificate module uses standard-library rational arithmetic. The
reference driver's default floating-point proposal mechanism additionally needs
SciPy; exact rational replay decides whether a proposed proof is accepted.
Its saved driver checks use SciPy and are distinct from the SCIP campaign.

The October campaign environment is recorded in `campaign.json`: Python
3.13.11, NumPy 2.5.3, SciPy 1.18.1, PySCIPOpt 6.2.1, SCIP 10.0.2, one thread
per solver/numerical library, and two workers. The Python environment and solver
binaries are not bundled. Install compatible versions separately; there is no
promise of bit-for-bit timings or identical numerical solver outcomes across
machines. Normalized October inputs suffice without a MINLPLib cache. Frozen
`prepare.py` documents original model selection, but input regeneration needs
the original metadata/cache paths or an explicit relocation to the included
retained inputs.

The September analyzer's complete saved input set is included: CSV metadata,
raw streams, and boxes used to identify shared final runs by their hashes.
Running that analyzer needs NumPy and pandas, and writes tables. Numerical
solver reruns also need SciPy, Gurobi 13 with a valid license, SCIP 10 and
PySCIPOpt; solver binaries, licensed software, and the original Python
environment are not bundled.

Historical `instancedata.csv` and `pool.csv` retain their repository-relative
paths. Cache files are relocated under `retained-inputs/september/osil/` and
`retained-inputs/september/sol/`, with their original cache-relative paths and
hashes in the manifest. Scientific source is unchanged: `qcqp.py` still defaults
to the original user cache, and `setup_instances.py` still contains its original
absolute metadata path. The validation command below explicitly relocates the
cache module constants before executing the unchanged script. Selection
regeneration would additionally require arranging the metadata path used by
`setup_instances.py`; saved `results/instances.csv` already records its decisions.

All 377 OSiL inputs named by the archived candidate table are retained. The
current local solution cache contains `.p1.sol` for 364 candidate names; the 13
missing names are recorded in `SEPTEMBER-INPUTS.json`. These gaps do not prevent
the original Gurobi-reference fallback in `validate.py`, whose saved vectors
are included. Only 44 candidate `.done` download markers are present, so calling
`setup_instances.py` may attempt downloads even with retained solution files.
No downloads were made while packaging. The retained cache and metadata have
no pre-campaign September hash record; their current bytes are hashed for
lineage, without claiming that every cache file is a frozen September input.
The original September report notes incomplete reference-solution downloads.

General repository files, literature, unrelated studies, current unfrozen
October solver/driver code, and September ancillary mathematical review/proof
scripts are excluded. The frozen campaign and pilot remain separate from
current source. The original campaign source predates the later interrupted-run
recovery fix; its scientific behavior is preserved unchanged. Replays below
start with an empty result directory and should not reuse an interrupted replay.

## Package verification

The following package-only check was run successfully during preparation. It
uses the standard library, reads the manifest and archive without extracting
anything, and verifies every included byte. It executes no scientific code.

```sh
python verify_archive.py
```

The exact `certificates` and `certified_driver` modules were also imported from
a temporary extraction under their preserved sibling layout, without calling
any LP proposal or driver routine.

## Documented commands (not executed during packaging)

All paths below are relative to the newly extracted archive root. These commands
are instructions for future independent use; they do not report fresh results.
Use a disposable extraction whenever a script writes summaries or check outputs.

```sh
mkdir extracted
# Run this from the companion directory.
tar -xzf archive.tar.gz -C extracted
cd extracted
```

The exact reference checks can be invoked by their preserved paths after
installing SciPy if needed. They print their results; redirects can save new
output separately from the original archived reports.

```sh
python research-20261003-adaptive-obbt/theory/check_remaining_benefit.py
python research-20261003-adaptive-obbt/theory/check_certified_driver.py
python research-20261003-adaptive-obbt/theory/check_constrained_obbt.py
python research-20261003-adaptive-obbt/theory/check_effort_allocation.py
```

To repeat the October schedule with its exact archived sources, first prepare a
new campaign directory containing only the old configuration and sources. The
recorded environment metadata in the copied configuration describes the original
campaign; record the actual replay environment separately when publishing a
replay. The original driver accepts `--resume` to use the copied task schedule
rather than snapshotting current sources. Do not rerun this command on an
interrupted replay; choose a fresh directory/name instead.

```sh
experiment=research-20261003-adaptive-obbt/experiments
mkdir -p "$experiment/runs/replay-01/raw" "$experiment/runs/replay-01/logs"
cp "$experiment/runs/campaign-01/campaign.json" "$experiment/runs/replay-01/"
cp -R "$experiment/runs/campaign-01/source" "$experiment/runs/replay-01/"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python "$experiment/runs/campaign-01/source/run.py" \
  --experiment-root "$experiment" --campaign replay-01 --resume
```

Recompute the archived analysis only in a disposable extraction; it writes
summary files. This reproduces the stored analysis rule, including the original
numerical success criteria, rather than proving exact optimality.

```sh
python research-20261003-adaptive-obbt/experiments/runs/campaign-01/source/analyze.py \
  campaign-01 --experiment-root research-20261003-adaptive-obbt/experiments
```

The September analyzer can now consume its complete saved input set in the
preserved layout. It reproduces the original table rules, including the
wrong-success issue described above; it does not generate corrected counts.
Use a disposable extraction because it rewrites summaries.

```sh
python research-20260922/iterated-obbt/code/analysis.py
```

To use the retained model/solution cache for the original reference-point
validation without changing scientific source, explicitly redirect its cache
constants before running it. This also rewrites `validity.csv`, so use a
disposable extraction. This command is documentation, not a check executed
while packaging.

```sh
python - <<'PYTHON'
from pathlib import Path
import runpy
import sys
root = Path.cwd()
source = root / "research-20260922/iterated-obbt/code"
sys.path.insert(0, str(source))
import qcqp
qcqp.OSIL = str(root / "retained-inputs/september/osil")
qcqp.SOLDIR = str(root / "retained-inputs/september/sol")
runpy.run_path(str(source / "validate.py"), run_name="__main__")
PYTHON
```

## Artifact lineage

The October frozen manifest SHA-256 is
`efd5727e9a427a1a8238ff0ff0a34809a7c9ca64ab65476d96539cb421591b73`.
`campaign.json` binds each of 120 tasks to a frozen normalized-model digest and
binds the worker, policy, validator, analyzer, protocol, and saved test source to
digests. `artifact_hashes.json` additionally binds raw records and full logs.
These hashes were checked directly before packaging. Every selected source file
was copied unchanged; archive member digests permit later comparison. September
has no equivalent pre-campaign source-freeze record, so this companion documents
its retained repository files and saved output rather than claiming prospective
source locking for that earlier study.

## Public export

This public copy contains privacy and redistribution edits. Current package hashes describe the exported files; `original_sha256` records identify the original committed bytes when an exported file changed. Historical experiment and review hashes remain provenance records. Scientific result values were retained, and the experiments were not rerun. Repository-level `THIRD_PARTY_NOTICES.md` records licenses for retained third-party material.
