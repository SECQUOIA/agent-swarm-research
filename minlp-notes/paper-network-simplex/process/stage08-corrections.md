# Whole-manuscript round 1 correction

Status: the separate correction agent resolved W1-01 and completed the checks
below. Root verification and final whole-manuscript acceptance remain pending.
The manuscript README and process status were not changed by this correction.

## Issue and disposition

The oracle README and retained literature audit incorrectly combined Section
5.7 with Proposition 22 and equations (30)–(31) of Kis–Horváth. Both exact
locators now say **Section 5.9**. In the two related manuscript paragraphs,
the broader predecessor comparison now identifies Sections 5.7 and 5.9, and
the lower-bound shift/transportation comparison specifically identifies
Section 5.9, Proposition 22, and equations (30)–(31).

Only these four current source files changed:

- `code/network_simplex/README.md`;
- `notes/network-simplex-reopened-literature.md`;
- `paper-network-simplex/sections/01-foundations.tex`;
- `paper-network-simplex/sections/03-structured-oracles.tex`.

The source attribution and contribution boundary are unchanged. No mathematical
statement, proof, executable algorithm, model, observation, benchmark result,
or generated table changed.

## Independent source verification

The correction agent inspected the openly accessible
[published article](https://link.springer.com/article/10.1007/s10107-021-01652-z)
and the repository's retained primary extraction. The former places Proposition
22 and the two equations under Section 5.9; the preceding paragraph shifts
the positive lower bounds before applying the cut projection. Section 5.7
contains the related union-of-simplices construction. This independently
confirms the reviewer and root's locator diagnosis. The verification JSON
records the URL, exact locators, and local source hash.

## Freeze preservation and checks

Before any edit, all 88 dependencies in the Stage 7 validation manifest matched
their recorded hashes. Copies and hashes of the four modified sources are
preserved under
[`verification/stage08-corrections/reviewed-source/`](../verification/stage08-corrections/reviewed-source/).
Old review snapshots and validation manifests remain unchanged. Their checks
describe their frozen versions: the Stage 7 unchanged-section/dependency guard
does not apply verbatim after these authorized citation-only edits. It was not
silently relaxed or used to overwrite earlier evidence. The current correction
record instead identifies every changed file and verifies the remaining frozen
dependencies, all mathematical environments, and all unchanged section/table
sources directly.

A clean `latexmk -C` followed by the standard PDF command produced a **48-page
PDF**, with no final warnings, undefined references/citations, or overfull/
underfull boxes. The corrected paragraphs were checked in extracted text and
on rendered pages 4 and 20. Local Markdown links in the modified documentation
and this record resolve; the cited publisher link was opened successfully.

The diff, before/after hashes, build logs, rendered pages, source verification,
and current integrity results are retained under
[`verification/stage08-corrections/`](../verification/stage08-corrections/).
This minor citation correction does not require a numerical rerun or another
five-reviewer round under the root's adjudication.
