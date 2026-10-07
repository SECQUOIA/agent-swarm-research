# Editorial-draft layout check

The immutable complete-editorial-draft-r1 sources were copied to
`/tmp/smoothed-editorial-typeset-r1-z8y6j8rf` and compiled with two targeted
`pdflatex -interaction=nonstopmode -halt-on-error main.tex` passes. Both
passed. The first produced 150 pages; final page numbers and bibliography
remain pending. The second pass was redirected to `second-pass.stdout`.

The title/abstract and full results table were rendered with `pdftoppm`
and inspected visually. The table fits one page and is legible; there was
no oversized-float warning. The title page ran into the start of the
contents, so the live main file now places page breaks before and after
the contents. The final build must check the resulting pagination again.

The eight overfull mathematical lines match the earlier frozen-proof
diagnostic; their owning authors are revising the affected appendices.
There were no new overfull lines in the completed front/boundary block.
Undefined citations are expected because its bibliography is pending.
This check does not establish final submission readiness.

An attempted PDF text read while the second TeX pass was still writing
failed transiently. It succeeded after that pass completed. No source
change was needed for that read.

No optimization experiment, project-wide verification, or CI inspection
was performed.
