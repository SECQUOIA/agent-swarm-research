# Stage 1 corrections

Completed 2026-09-13 by a correction agent distinct from the Stage 1 author.
Scope: all three accepted minor findings in `stage01-adjudication.md`.
The five reviews and adjudication were read before editing. No checker code,
future manuscript section, unrelated folder, or acceptance status was changed.

## Finding-to-change map

1. **R1/R2/R4/R5: proof-language terminology.** In
   `sections/01-introduction.tex`, the Python kernel now “checks complete proofs
   in a restricted subset of VIPR.” The inventory describes an arithmetic/parser
   contract for complete proofs in a restricted subset of VIPR 1.0/1.1, and the
   literature map uses the same distinction. Completeness describes submitted
   proof artifacts, not logical completeness or full format coverage.
2. **R2/R4/R5: publication metadata.** Added Coey volume 12, pages 249–293;
   Bentkamp LNCS volume 13994, pages 74–92; Narkawicz LNCS volume 8164, pages
   326–343; and Solovyev LNCS volume 7871, pages 383–397 to `references.bib`.
   Added the LNCS series to the three proceedings entries. Independently reopened
   all four publisher records and checked those fields. Publication years were
   preserved, including Narkawicz 2014 despite the VSTTE 2013 event label.
   Primary sources:
   [Coey](https://link.springer.com/article/10.1007/s12532-020-00178-3),
   [Bentkamp](https://link.springer.com/chapter/10.1007/978-3-031-30820-8_8),
   [Narkawicz](https://link.springer.com/chapter/10.1007/978-3-642-54108-7_17),
   [Solovyev](https://link.springer.com/chapter/10.1007/978-3-642-38088-4_26).
3. **R3: timing population.** In `evidence/repository-inventory.md`,
   7,987.954 seconds is now explicitly the summed checker time for the 188
   verified records. The separate campaign elapsed time remains 1,465.381
   seconds. Recomputed the verified-record sum directly from
   `code/minlp_solver_lab/results/cert_replay_20260913_complete.jsonl`:
   188 records, 7,987.953598855151 seconds before rounding. No raw result was
   modified and no large-proof campaign was repeated.

## Validation

Built a fresh isolated source copy in `build/stage01-corrections/` using
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. This prevents
reuse of the older bibliography in the paper root. The build exited with code
0 and produced an eight-page PDF. The complete build transcript is
`process/stage01-corrections-build.log`; the final LaTeX log has no warnings,
undefined references/citations, or overfull/underfull boxes. Checked that all
new volume/page fields appear in the generated bibliography, extracted the PDF
text successfully, and verified that the ambiguous “restricted complete”
phrase no longer occurs in the current sections or either evidence map.

These edits do not change mathematical claims or accepted results and revealed
no additional issue. Stage acceptance remains the coordinator's decision.
