# Stage 1 corrections after round 1

A separate correction agent read the root adjudication, the relevant independent
reports, and the root's own reading. All three accepted minor findings are
resolved. No theorem statement or proof changed.

| Finding | Resolution |
|---|---|
| S01-R1-R3-01 | The prior-work subsection now locates equation (25) on p. 1 of the published electronic companion. A footnote links directly to that supplement. The text distinguishes the article and companion for numbering. The locator and URL are those independently checked by reviewer 3; the correction did not repeat that external source audit. |
| R5-S01-01 | The same paragraph now explicitly says that Section 3 of Khademnia–Davarnia represents equality balances by opposite inequality pairs, includes the present model, and that the present paper exploits its equality circulation space. The correction agent also inspected the retained primary-source extract, lines 202–206. |
| ROOT-1 | Example `ex:merger-boundary` now explicitly observes that its component sets are identical, so the homothetic set identity remains true. It distinguishes addition of different redundant RHS descriptions from scaling the single fixed block representation used in the theorem. |

Only `sections/01-foundations.tex` was changed among manuscript sources. The
snapshot-to-current diff is retained in
[`changes.diff`](../verification/stage01-corrections/changes.diff).

The documented `latexmk` command completed successfully and produced a seven-page
PDF. The final LaTeX log contains no warnings, undefined references or citations,
or overfull/underfull boxes. Extracted PDF text confirms that the corrections
appear as intended. Rendered pages 2 and 6 were visually inspected: the new
source footnote, prior-work paragraph, and example explanation are legible and
stay within the page boundaries.

Build output, extracted text, page images, source hashes, and the machine-readable
validation record are retained in
[`verification/stage01-corrections/`](../verification/stage01-corrections/).
The root's independent verification and stage acceptance remain separate steps.
