# Targeted manuscript verification

Verification is confined to this manuscript and its submission package. No
computational experiment was rerun. No project-wide code checks or CI status
or logs were inspected.

## Checks and results

From `paper-separator-certificates/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex > verification/build.stdout 2>&1
python3 verification/check_manuscript.py > verification/source-check.txt
pdfinfo build/main.pdf
pdftotext -layout build/main.pdf verification/main.txt
```

The complete build passed. The final log has no warnings, undefined references,
undefined citations, overfull boxes, underfull boxes, or errors. The PDF has
60 pages and a blank author field. The source checker reports
`MANUSCRIPT_CHECK=ok`: 16 TeX inputs, 185 distinct labels, and 29 cited sources.
It also checks input existence, reference and bibliography identifiers,
control characters, trailing whitespace, and internal placeholders.

Representative pages were rendered with:

```sh
pdftoppm -f PAGE -l PAGE -scale-to 1600 -png -singlefile build/main.pdf verification/page-PAGE
```

Pages 1, 4, 18, 28, 39, 50, and 60 were visually inspected. The inspected
pages cover the title and abstract, literature comparison, main theorem,
denominator proof, rational dynamics, conclusion and appendix transition,
and bibliography. Equations, links, margins, and page breaks render correctly.
Pages 4 and 60 were rendered and inspected again after the final related-work
sentence and bibliography entry were added.
An initial request for page 61 was corrected to the last page, 60.

From the repository root:

```sh
git diff --check -- README.md paper-separator-certificates
```

This scoped tracked-diff check passed. The source checker separately checks
the new untracked TeX files' whitespace. An initial overly broad warning
detector matched TeX package metadata; the detector was corrected to match
actual diagnostic forms, and the final check passed.

## Portable package

The archive was created with Python's standard `zipfile`, using explicit
relative paths and fixed archive timestamps. `ZipFile.testzip()` and an
exact expected-member comparison passed: `ARCHIVE_CHECK=ok`, 19 source
entries. The package contains the 16 TeX files, `references.bib`, generated
`main.bbl`, and a build README. It contains no research notes, review
reports, build debris, or absolute file dependencies.

After extraction into a clean temporary directory, the following targeted
build passed:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > portable-build.stdout 2>&1
pdftotext -layout main.pdf main.txt
```

The final portable build has no LaTeX diagnostics. Its extracted PDF text was
compared byte for byte with the main build in Python; they match exactly. The
temporary path is recorded in `portable-build-path.txt`. Archive checks are in
`archive-check.txt`; delivered-file hashes are in `../delivery/SHA256SUMS`.
Final Python standard-library checks compared every archive member with its
current source, the delivered PDF with the build PDF, and both delivered-file
hashes with the manifest. They also checked the local links in the repository
and manuscript README files. All passed (`DELIVERY_CHECK=ok`).

## Mathematical and literature verification

All stated mathematics was checked analytically against the source notes and
again through fresh manuscript reviews. The model, construction and inexact
oracles, polynomial arithmetic, consistency and scalar covering, dynamics,
and dynamics arithmetic each have independent reports under
`../evidence/reviews/`. The integrated editorial report and
`../evidence/REVIEW-RESOLUTION.md` record the final wording and scope repairs.
No remaining blocking defect was identified in the stated results.

All literature discovery, retrieval, and claim-level review used GPT Luna at
max reasoning through the supplied literature skill. The literature lead
owns the serialized KB checks; final source locators, run records, counts,
and the exhaustive access-gap list are recorded in
`../evidence/LITERATURE.md`. This is distinct from code or CI verification.
