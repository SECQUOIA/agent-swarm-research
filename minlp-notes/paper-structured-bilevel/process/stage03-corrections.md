# Stage 3 corrections

Correction agent: `correction_agent`, distinct from the stage author and all
five reviewers. Date: 2026-09-07. Authority:
`process/assessments/stage03-round01.md`. Both accepted minor issues are fixed;
no accepted issue remains unresolved. Stage acceptance remains the root's
decision.

## Changes and verification

| Issue | Change | Verification |
| --- | --- | --- |
| S3-1 | Replaced the preprint-only `ArnstromAxehill2020` entry with `ArnstromAxehill2022`, an article in IEEE Transactions on Automatic Control 67(6):2758–2770 (2022), DOI `10.1109/TAC.2021.3090749`, in `references.bib:97–101`. Updated its sole manuscript citation key consistently. | Verified the publication metadata against the primary sources below. The compiled entry on PDF page 26 has the correct journal, volume, issue, pages, year, DOI, and author accents. No scientific attribution or final-paper theorem locator was added or changed. |
| S3-2 | Wrapped the complete statement of Theorem 3.1 in the standard LaTeX `samepage` environment, `sections/03-robustness-screening.tex:49–63`. | The theorem and its final qualification concerning unrelated witnesses now appear together on PDF page 14. Removing the wrapper and reverting the citation-key rename gives byte-identical stage 3 section content to the frozen source. No mathematical wording, proof, package, or hard page break changed. |

## Primary metadata and full-text provenance

The publication year and journal are listed on
[Arnström's publications page](https://darnstrom.github.io/publications/).
The full page range and DOI are also given on
[Axehill's institutional publications page](https://staff.gitlab-pages.liu.se/publications/en/liu/isy/rt/danax42/),
which I opened successfully. The
[IEEE CSS June 2022 contents digest](https://ieeecss.org/sites/ieeecss/files/documents/pcd/CSS_Publications_Content_Digest_062022_0.pdf),
PDF page 3, confirms volume 67, issue 6, and the article's starting page 2758;
the next article starts on page 2771. The search-indexed cover of the
[institutional postprint](https://www.diva-portal.org/smash/get/diva2%3A1669297/FULLTEXT01.pdf)
independently supplies the complete citation.

Direct institutional PDF access failed, and the linked IEEE article page
returned a bot-verification screen. I do not claim to have inspected the
final journal full text. The scientific attribution was reviewed using
[arXiv:2003.07605v2](https://arxiv.org/abs/2003.07605v2), as recorded in the
stage 3 root-reading record and independent review reports. In particular,
reviewer02's Section IV/Algorithm 2 locators refer to that preprint. Those
provenance records remain unchanged. This correction verifies publication
metadata without transferring preprint locators to an uninspected version.

## Build, layout, and source integrity

Before editing, all eight live source files and their frozen counterparts
matched `process/snapshots/stage03-round01/SHA256.json`. Its SHA-256 was and
remains `0d1eb5b7c2a0869ef020289146fcd8c44227b95aef249b2ed3bb3bbdc3b0f956`.
Every frozen file still matches its recorded hash. I inspected the complete
diff: only `references.bib` and `sections/03-robustness-screening.tex` changed,
and only as listed above. All previously accepted mathematical content is
preserved.

The live clean build succeeded with:

```sh
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The resulting `build/main.pdf` has 27 pages. The final log has no warnings,
undefined references or citations, overfull or underfull boxes, or fatal
errors. I visually inspected PDF pages 14 and 26: the full theorem statement
and corrected bibliography entry are legible with no clipping or overlap.
No mathematical tests were needed for these metadata and layout changes.

Evidence is retained in `verification/correction-agent/stage03/`:

- `build-command.log` and `final-main.log`: full rebuild transcript and final log.
- `source.diff` and `checks.json`: complete source changes, snapshot checks,
  unchanged mathematical content, and final diagnostics.
- `rendered.txt`, `theorem-page14.png`, and `references-page26.png`: PDF text
  and inspected layout.

Remaining accepted issues: **none**. Root status, assessments, and frozen
snapshots were not edited. Stage 4 was not started, and no work was delegated.
