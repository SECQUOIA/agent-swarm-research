# Targeted verification

Verified on 2026-10-06. All checks concern this manuscript and its submission
archive. No computational experiment or existing result checker was rerun.
No project-wide verification, CI status inspection, or CI-log inspection was
performed.

## Proof and source review

The three source audits, two independent main mathematical review streams,
focused class-transfer and gap-zero reviews, and editorial review are in
`../reviews/`. Their findings and dispositions are in
`../evidence/review-resolution.md`. These were analytical checks, not formal
proof verification. The literature review used GPT Luna with max reasoning;
source locators and access limits are in `../evidence/literature-audit.md`.

## Manuscript build

The final command, run from the paper directory, was:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Output was saved in `final-build.txt`; the command exited 0. The final
`build/main.log` and `build/main.blg` contain no warnings, errors, undefined or
multiply defined references, overfull boxes, or underfull boxes. Earlier draft
build logs are retained separately. The initial primed-transpose syntax error
was corrected before the successful builds.

The structural command was:

```sh
python verification/check_document.py
```

It exited 0. `static-check.txt` records 10 manuscript files, 70 explicit labels,
and 21 cited sources; no duplicate labels, missing references, missing citation
keys, duplicate bibliography keys, or unfinished markers were found. The
manuscript bibliography matches the literature owner's final BibTeX fragment.

## PDF inspection

The commands actually run were:

```sh
pdftotext -layout build/main.pdf build/main.txt
pdfinfo build/main.pdf
```

`pdf-info.txt` records 26 pages and an empty author field. The extracted text
was read for the introduction, definitions, final discussion, and bibliography.
The title, class table, certificate proofs, rank-one examples, and final
bibliography page were also inspected visually. For each page in
`1, 4, 17, 21, 26`, the render command was:

```sh
pdftoppm -f PAGE -l PAGE -scale-to 1400 -png -singlefile build/main.pdf build/page-PAGE
```

All five renders succeeded. No clipped table, equation, text, or reference was
found. The displayed mathematical symbols and hyperlinks are legible.

## Portable source archive

The archive was created and integrity-checked with Python's standard-library
`zipfile`. It contains exactly the 12 files in `submission-manifest.txt`:
the 10 TeX files, `references.bib`, and standalone `README.md` build
instructions. It contains no internal notes, reviews, local literature files,
absolute-path dependencies, or generated build files.

The archive was extracted into the new empty directory
`/tmp/binary-separation-submission-check.biolh0ip`. The exact standalone command
was then run there:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

It exited 0. `clean-archive-build.txt` and `clean-archive-receipt.json` record
the result. The clean TeX and BibTeX logs contain no warnings. The resulting
PDF has 26 pages, no author metadata, and exactly the same `pdftotext -layout`
output as the distributed manuscript. The archive's CRC check passed.

`artifacts.sha256` records the checksums of `main.pdf` and
`submission-source.zip`. The distributed PDF is the final successful build.
After the literature audit was finished, a targeted Python consistency check
confirmed that the final bibliography still matches its audited fragment,
every archived file matches the current submission source, both artifact
checksums match, and the required local evidence files are present. No
manuscript change or additional build was needed for the audit record.

## Shared literature ownership

The literature owner's active ingestion completed safely, followed by its one
required check with exit 0 and `KB_CHECK=ok`. The root did not run a second KB
check. At the user's request, ownership was released to the existing reusable
Luna-max lead and both named threads were notified. The exact receipt and
notification IDs are in `../evidence/kb-handoff.md`. No KB mutation or check
was performed by this task after release.
