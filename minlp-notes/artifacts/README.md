# Research evidence storage

Git retains research source, proofs, reviews, experiment protocols, inputs and
generators, source snapshots, compact results, tables and verification code.
Large raw traces, dense checkpoints and full support-cut records remain on the
local machine and are also preserved in the
[October 5 evidence release](https://github.com/sergey-gusev94/minlp-notes/releases/tag/research-evidence-20261005).
No raw research file was deleted during this cleanup.

`manifest.json` records archive sizes, SHA-256 checksums, release asset order,
the original local commit and the published base. `files.jsonl.gz` records the
repository-relative path, size and SHA-256 of every archived regular file.
Archives retain source snapshots, failed attempts, smoke tests and diagnostic
reruns as well as primary results. These populations remain distinct.

| Package | Preserved material | Files omitted from ordinary Git |
|---|---|---|
| `support-cuts-v3` | Complete `paper-certified-support-cuts/experiments/v3/` | Raw `records.jsonl`, per-run `runs/*.json` and driver locks |
| `support-cuts-v3d` | Complete post hoc diagnostic campaign | Same narrow exclusions |
| `support-cuts-v4` | Complete campaign 4, including smoke and screening runs | Same narrow exclusions |
| `support-cuts-v5` | Complete campaign 5, including amended smoke runs and diagnostic reruns | Same narrow exclusions |
| `scip-fidelity-traces` | 48 original `research-20261001/scip-rule-fidelity/logs/runs_minlplib/*.jsonl.gz` files | Those raw traces only |
| `sparse-audit-checkpoints` | 50 original `research-20261001/three-var-computation/logs/sparse_audit/*.base.npz` files | Those dense checkpoints only |

Support-cut cases, source manifests, all frozen source snapshots, job
specifications, session records, summaries and replay receipts stay in Git.
The [compact record](../paper-certified-support-cuts/experiments/compact/README.md)
supports table verification without downloading the raw campaigns. Its digests
are not substitutes for full support witnesses. Full certificate replay needs
the restored raw records and the corresponding verified frozen source.

**Download and verify.** Run from the repository root with Python 3.11 or newer;
GitHub CLI is needed only for the download. Asset links are also available on
the release page.

```sh
evidence_dir=/tmp/minlp-notes-evidence-20261005
mkdir -p "$evidence_dir"
gh release download research-evidence-20261005 \
  --repo sergey-gusev94/minlp-notes --dir "$evidence_dir"
python artifacts/verify.py "$evidence_dir"
python artifacts/verify.py "$evidence_dir" --contents
```

The first verifier checks every asset checksum against the committed index.
`--contents` additionally streams all six packages and checks every original
file against its recorded checksum, without extracting anything. It also
verifies member counts and symlink targets. The split trace package is read in
the order recorded in `manifest.json`; each release asset is below 2 GiB.

**Restore.** The archives contain repository-relative paths. To protect current
edits, first extract into a separate empty directory. The trace package is
split into two ordered parts; all other packages are single archives.

```sh
restore_dir=/tmp/minlp-notes-evidence-restored-20261005
mkdir -p "$restore_dir"
for package in support-cuts-v3 support-cuts-v3d support-cuts-v4 support-cuts-v5 sparse-audit-checkpoints; do
  tar -xzf "$evidence_dir/$package.tar.gz" -C "$restore_dir"
done
cat "$evidence_dir/scip-fidelity-traces.tar.gz.part000" \
    "$evidence_dir/scip-fidelity-traces.tar.gz.part001" \
  | tar -xzf - -C "$restore_dir"
```

Copy the required missing raw files from that directory into the matching
repository paths, preserving current code and compact records. The restored
campaign source snapshots have their original hashes and can also be used
directly in the isolated restoration directory. Follow each campaign README
for its complete environment and replay command. Numerical solver reruns may
require the original solver versions and licenses; checking a saved certificate
and rerunning an optimization experiment are different operations.

Raw-dump checks such as `scip-rule-fidelity/code/check_revision_r2.py` require
the trace package. `scip-rule-fidelity/code/summarize.py` uses retained compact
analyses. `three-var-computation/code/audit_table.py sparse` uses retained result
JSON and incumbent records; it does not need the dense checkpoints. Restore
checkpoints before workflows that use their saved matrices as initial points.

**Public copy.** This directory records upstream archive provenance. Local
backup paths and the ignored-workstation-file inventory are omitted from this
public transfer. External evidence archives are upstream originals, not rebuilt
or covered by the review of committed files in this copy.

**Future commits.** Keep compact results for all runs, including failures and
timeouts, in Git. Put new bulky evidence into separate versioned archives and
record retrieval locations, SHA-256 checksums, original inputs, source versions,
parameters and restoration commands. Do not ignore entire experiment trees or
all JSON, logs or NumPy files.

The repository includes a local commit guard for files at or above 100 MiB:

```sh
git config core.hooksPath .githooks
python artifacts/check_git_size.py --staged
python artifacts/check_git_size.py --base origin/main
```

The guard does not measure a push's compressed total size. Archive exclusion
must apply to every unpublished commit that contains a large blob; deleting a
file in a later commit does not remove its historical contents from the push.

Targeted storage checks and their actual results are recorded in
[verification.md](verification.md). No project-wide verification or CI checks
were run locally for this change.
