# Compact computational record

These compressed JSONL exports retain every saved run from campaigns v3,
v3d, v4 and v5, including smoke tests and diagnostic reruns. Each line keeps
the run status, errors, bounds, timings, seed, primal-check result, observed
cut count and compact per-cut row digest and certificate metadata. Failed
runs and unsuccessful comparisons remain included. An incomplete cut log
remains marked incomplete; its observed count does not establish the number
of cuts actually produced.

The 33 exports contain 3,817 records and 279,930 observed cuts, using
11,558,549 compressed bytes. The manuscript's primary populations account
for 274,489 cut records and 92,222 distinct rows; the remaining exports keep
the separate scans, smoke tests and diagnostic reruns.

`manifest.json` records the source ledger SHA-256, source size, export
SHA-256, export size, run count, observed cut count and status counts for
every campaign. The exports use the existing independent numbers extractor
in `verification/R10_numbers_extract.py`; they omit full support witnesses
and repeated models.

From the repository root, verify the saved exports and independently
recompute the numeric appendix tables using Python's standard library:

```sh
python paper-certified-support-cuts/verification/export_compact.py --verify
python paper-certified-support-cuts/verification/R10_numbers_tables.py paper-certified-support-cuts/experiments/compact
```

The table checker also reads the retained campaign `cases/*.json` files and
`sections/B-tables.tex`. It exits unsuccessfully if a checked cell disagrees.
For the broader numerical audit, including recorded replay totals and
distinct rows:

```sh
python paper-certified-support-cuts/verification/R10_numbers_check.py paper-certified-support-cuts/experiments/compact
```

That audit also reads the retained `replay.json`, case descriptors and
session records at their original campaign paths. It prints its findings;
the export verifier and appendix checker provide explicit failure exits.

## Targeted verification on October 5, 2026

All three commands above completed successfully. The export verifier checked
all 33 exports. The appendix checker checked 1,988 cells with zero
mismatches. The broader audit recovered the manuscript's cut totals with
zero replay-record mismatches and no uncovered runs in its primary
populations. Its saved output is [numerical-audit.txt](numerical-audit.txt).

The audit retains the original eight incomplete campaign-v5 cut logs and
the failing numerical incumbent check for `waternd2` in the campaign-v4
root `baseline-extra` run. These observations remain in the computational
record. This verification did not repeat support-certificate replay or any
optimization run, and did not inspect CI.

The compact record supports numerical analysis. Full independent replay of
every support certificate requires restoring the raw campaign archive,
including `records.jsonl`, per-run JSON, original inputs and exact frozen
snapshots, and then following the campaign README's replay command. Saved
replay receipts report the original checks; compact digests do not repeat
those checks. See the repository's storage documentation for archive
locations and restoration.

To regenerate all exports from restored raw campaigns, first preserve the
existing compact directory elsewhere, create a new `compact/` directory,
and run:

```sh
python paper-certified-support-cuts/verification/export_compact.py
```

The exporter refuses to overwrite existing exports or their manifest and
never changes the raw campaigns. These commands verify this computational
record only; they do not run project-wide checks or inspect CI.
