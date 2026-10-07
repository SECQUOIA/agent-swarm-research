# Targeted document verification

The completed report builds to **22 pages**. Verification was restricted to
this document and its linked topic evidence; no project-wide checks or CI
inspection were performed.

The command actually run from the repository root was:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  research-20261002-convexification/document/main.tex \
  > research-20261002-convexification/document/build.log 2>&1
```

Result: exit status zero. The final LaTeX log contains no warnings, undefined
references, missing citations, overfull boxes, or underfull boxes. BibTeX uses
the audited bibliography at `../literature/references.bib`.

A focused Python check read every Markdown link in this directory and
confirmed that every local target exists. It also searched the final LaTeX
log for warnings and layout problems. The result and document source/PDF
hashes are saved in [verification.json](verification.json).

The PDF was converted with `pdftotext -layout` to check its text and table
locations. The first page and final primary-results table page were rendered
with `pdftoppm` and inspected. The table fits the page and distinguishes
selected, admitted, and solved cases. Temporary rendered images were removed.

The [independent document review](../reviews/document-review.md) checks the
mathematical claims and final report against the actual source and raw
experiment records. Its [saved evidence checks](../reviews/document-evidence-checks.json)
recount selected/admitted populations, numerical outcomes, recorded cuts,
replay coverage, and the native sampling table. This is internal
research-agent review, not formal verification or journal peer review.

The [topic verification record](../VERIFICATION.md) contains the distinct
solver, mathematics, certificate, model-binding, and experiment-harness
commands. Their results are not inferred from this successful PDF build.
