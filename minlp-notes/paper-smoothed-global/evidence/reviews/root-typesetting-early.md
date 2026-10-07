# First typesetting diagnostic

The immutable complete-proof-draft-r1 sources were copied into a temporary
directory and built with `pdflatex -interaction=nonstopmode -halt-on-error
main.tex`. The pass succeeded and produced a 145-page draft. Bibliography
and cross-reference warnings are expected on this initial pass, with the
audited bibliography still pending. This is not a final build or publication
approval. No optimization experiment or project-wide check was run.

The following overfull lines need inspection after final references and
scientific revisions. Locations refer to the frozen snapshot.

| Source | Lines | Excess |
| --- | --- | ---: |
| Appendix A | 329–342 | 0.67 pt |
| Appendix E | 209 | 28.35 pt |
| Appendix E | 296 | 39.09 pt |
| Appendix E | 398 | 6.08 pt |
| Appendix E | 503–512 | 107.83 pt |
| Appendix E | 656–666 | 39.80 and 40.55 pt |
| Appendix F | 376–380 | 15.09 pt |

Break long displayed or inline formulas across lines with aligned equations
and short definitions. Preserve every term and inequality; avoid shrinking
the whole mathematical text. The Appendix A warning may change when the
actual citation is resolved. The final PDF needs visual inspection of the
main tables, long theorem statements, and these formula pages.

The separate targeted command
`python3 paper-smoothed-global/verification/check_sources.py` was run before
this pass. It found no missing TeX files, undefined labels, duplicate labels,
unfinished markers, internal proof paths, or unpaired environments. Its
exit code was 1 because `references.bib` had not yet been produced; the
listed citations were therefore unresolved. A complete final check remains
required after literature integration. CI was not inspected.
