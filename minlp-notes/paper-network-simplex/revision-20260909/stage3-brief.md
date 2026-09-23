# Stage 3 brief (planning; begin only after Stage 2 acceptance)

Prepare standalone exposition, anonymous submission files, and a reproducible
computational supplement. Preserve the accepted mathematics and qualified
literature positioning. Do not add unsupported performance or novelty claims.

## Manuscript

- Polish the computational narrative for a reader without development history.
  Distinguish the current reduced and unreduced algorithms and the elementary
  baseline reductions without requiring the reader to know internal stages.
  Preserve negative comparisons, exact/numerical distinctions, platform limits,
  all quantitative evidence, and the component-hull scope of added side rows.
- Reproduction must refer to the accompanying computational supplement, whose
  layout supports every documented command. Keep detailed archival chronology
  outside the manuscript. No unfinished placeholders or repository-only links.
- Retain an empty author/date and set anonymous PDF metadata. No invented
  affiliations, acknowledgments, contact address, public repository or DOI.
- Check notation, tables, figures, bibliography and cross-references throughout.
  Mathematical changes require a specific reason and explicit report.

## Delivery

Build a current manuscript PDF and a standalone LaTeX source archive, containing
all source, bibliography, vector figures/tables, and a concise build README.
Create a separate computational-supplement archive with runnable source, tests,
independent exact checks, the canonical raw measurement data and table generator,
and a README distinguishing numerical and exact outputs. Include dependencies
and precise commands; preserve reported timings as historical measurements.

Keep the current layout inside the supplement (code/ and paper-network-simplex/
verification/) because existing imports resolve from script paths. In particular,
paper_stage06.py needs verification/reference/stage06/flat_chain.py loaded as
network_simplex._stage06_unreduced. stage04-recovery.py needs
code/network-simplex-bounded-rank-verify.py. The table generator writes to a tables/
directory relative to paper-network-simplex/. Include all dependencies of named
commands and avoid documentation links to omitted notes/results/old archives.
Package copies of documentation may be rewritten without changing production
code. Do not ship unrelated research folders, copyrighted literature PDFs,
internal reviews, private paths, or giant obsolete archives.

A small deterministic package-building script and SHA-256 manifests are useful
for reproducibility. Do not claim the entire revision accepted before final
review. Update active README.md and PROCESS.md so they no longer advertise the
old 48-page closeout as the current version. Preserve historical review records
and manifests unchanged. The revision STATUS.md is maintained by the root.

## Validation

Test extraction and a clean LaTeX build outside the repository. Test the extracted
supplement: principal 23-test suite, documented independent checks, table regeneration
byte-for-byte from canonical data, and at least a meaningful benchmark smoke run.
Include latest independent exact checks from this revision where useful and
explain their finite scope; no need to ship every internal review artifact.
Scan PDF metadata and package text for identifying paths or author metadata.
Verify every input referenced by LaTeX and each documented command is included.
Record actual commands/results and any limits in stage3-author.md, with private
build and test evidence. No external submission. Stage 3 is followed by five
independent frozen-stage reviews, then a separate whole-manuscript review cycle.
