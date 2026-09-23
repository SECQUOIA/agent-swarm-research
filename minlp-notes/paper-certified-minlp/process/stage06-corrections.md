# Final whole-manuscript corrections

Completed 2026-09-14 by the correction agent, distinct from the manuscript
author. Read `stage06-adjudication.md`, `stage06-review4.md`, and
`stage06-root-findings.md`. Both accepted minor findings are resolved. No new
major issue was identified. Acceptance status remains the coordinator's decision.

## Finding-to-change map

1. **Reviewer 4: model-status interpretation.** Section 6.3 now identifies the
   selected codes as GAMS model statuses 1 (Optimal), 2 (Locally Optimal), and
   8 (Integer Solution). Independently opened the official
   [GAMS 53 output documentation](https://www.gams.com/53/docs/UG_GAMSOutput.html)
   and checked its Model Status table. Added a concise linked footnote to that
   primary source. The one-sided comparison criterion, eighteen flagged pairs,
   and interpretation as investigation candidates remain unchanged.
2. **Coordinator: current artifact map.** Updated
   `evidence/repository-inventory.md` to the current core size **6,478,681
   bytes** and its latest rebuild during Stage 5's campaign-caption correction.
   The map also states that bulk contents were not reread in Stages 5 or 6.
   Prior dated reports and their historical artifact values were preserved.

## Clean build and source delivery

After both edits, ran `scripts/build-paper.sh` to replace root `main.pdf` and
`main.bbl` from a clean source directory. The delivered PDF has **32 pages**
and **524,977 bytes**, SHA-256
`7bbea1c89b3936361101dd7a21c1c1e5710d2f08827ad7a3814172882788d840`.
The final LaTeX log has no warnings, undefined references/citations, or
underfull/overfull boxes. The linked documentation footnote compiles correctly.

Regenerated `PAPER-SHA256SUMS`, the paper source archive, and its index using
`scripts/package-source.py`. The source archive has **49 entries** and is
**477,110 bytes**, SHA-256
`849b1b5a8e1eea818a5a4548b618c89bc2ca25f86aa5bc0a5643d99e80324c67`.
Repackaging unchanged sources gives the identical archive and index.

Extracted that archive to a fresh temporary directory. Every source-manifest
entry and all thirteen formal-package hashes pass. The extracted build script
runs without the parent repository and produces a warning-free PDF whose
extracted text matches the delivered PDF exactly. Its generated bibliography
bytes also match. Detailed artifact statistics and the extraction path are in
`stage06-corrections-source-extraction.json`; hash and build logs use the
`stage06-corrections-` prefix. Current root logs/text remain under `build/`.

## Unchanged evidence and metadata consistency

Scanned the current root README, evidence maps, manuscript sections, outer
supplement README, and core README for prior core sizes and hashes. No stale
current reference remains. Current exact size/hash references agree with
`supplement/archives.json` and the filesystem byte counts:

| Artifact | Bytes | Retained SHA-256 |
|---|---:|---|
| Experimental core | 6,478,681 | `d2805b1cfead992904b840d4a63c913287d42aec309f1502b1d4e90e9d2e9f1b` |
| Experimental bulk | 30,664,561,063 | `88c23497c2d20c76b3ac25cfc2c60a529aecb35da98e8de00213f4513ed314d4` |

These experimental archives and their index were not rebuilt or rehashed.
The size check is not a new integrity verification. The prior preservation
manifest confirms unchanged production modules, formal sources, generation/
replay records, original bulk manifest, and original full-readback record.
No mathematical proof, checking rule, numerical input/result, or frozen protocol
changed. No checker tests, Lean build, solver run, full replay, or bulk readback
was repeated for these two local prose/metadata corrections.
