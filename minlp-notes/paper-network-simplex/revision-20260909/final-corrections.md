# Final whole-manuscript correction

Completed 9 September 2026 by the separate correction author under
`final-adjudication.md`.

## Disposition

**R5-O01 — adopted and completed.** Added
`figures/observation-completion.tex`, a two-panel TikZ illustration of the
existing individual-product completion proposition and K4 example. Added
one short cross-reference and the figure input immediately after
`ex:forest-k4` in `sections/02-compression.tex`.

For one fixed label, the first panel observes 13 and 14. Its unobserved
edges 12, 23, 24, 34 have cycle rank one; selecting spanning tree 12, 23, 34
leaves 24 as the completion edge. The second panel also observes 24 and
has precisely the existing example's forest complement, with cycle rank
zero. Every arc points from its smaller endpoint to its larger endpoint.
Solid, dashed, and dotted lines distinguish observed edges, the unobserved
spanning tree, and the completion edge in grayscale.

**R1-O1 and R4-O1 — not adopted, as adjudicated.** No qualifications were
removed. No reviewer identified a required scientific correction. The
diagram adds exposition of existing mathematics, not a new result.

The example text and all theorem, lemma, proposition, corollary, and proof
environments are unchanged. No code, canonical data, tables, bibliography,
package-builder logic, status documentation, historical reviews, frozen
snapshots, or other paper folders were edited. The manuscript remains
anonymous.

## Artifacts and validation

Rebuilt `delivery/submission.pdf`, `delivery/latex-source.zip`,
`delivery/computational-supplement.zip`, and `delivery/manifest.json` with
the existing `delivery/build-packages.py`, then copied the submission PDF
to `main.pdf`. The resulting manuscript has 50 pages. The computational
supplement ZIP is byte-identical to its preceding version, with SHA-256
`7ca8a25ec3e0f1baa20e91b92d9dd9aae7b0218f020f5f95dc3e5ba5845c01a6`.

Evidence is retained in `final-correction-evidence/`:

- `manuscript.diff` contains the complete two-file manuscript change.
- `figure-page.png` renders PDF page 16. I inspected the actual rendering:
  both K4 drawings are planar, arrow directions are correct, all vertex
  labels and line styles are readable, the legend is distinct, and the
  caption and surrounding text have no collisions or clipping.
- `standalone/latex-source/` is a fresh extraction of the source archive.
  `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`, with the
  builder's fixed-time environment, succeeds. Its final log has no warnings,
  undefined references or citations, box diagnostics, missing characters,
  or TeX errors. Its PDF is byte-identical to the delivered PDF.
- `rebuild/` contains a second independent package-builder run. Both ZIPs,
  the PDF, and the outer manifest are byte-identical across runs. Every
  inner archive manifest and every outer input, payload, and artifact
  hash was checked. The source archive contains the new figure and has
  21 payload files; the supplement has the same 40 payload files as before.
- `validate.py` and `validation.json` retain reproducible checks. All 66
  formal environments match the final-round snapshot byte for byte, and
  all 102 frozen snapshot hashes match. Of the 55 preceding delivery
  inputs, only `sections/02-compression.tex` changed; the figure is the
  sole new source input. This also verifies unchanged code, canonical
  data, and tables. The script checks the unobserved edge sets, connected
  spanning tree, and cycle ranks one and zero independently of TikZ.
- `git diff --check -- paper-network-simplex` passes. The unchanged
  computational suite was not rerun for this illustration-only correction.

The root's final artifact inspection and acceptance decision remain separate
from this correction record. Nothing was submitted externally.
