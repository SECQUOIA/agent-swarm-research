# Final manuscript verification

The final manuscript has 75 pages, 40 cited works, 244 labels, and 14 TeX
inputs. The author field is blank. Its mathematical and editorial reviews
used GPT only in the final rounds, as requested. The review disposition is
in `REVIEW-DISPOSITION.md`; detailed reports and accepted source hashes are
under `reviews/`.

## Targeted commands and results

Commands below were run for this manuscript. No project-wide verification,
CI status/log inspection, or experimental rerun was performed.

1. `python3 verification/check_sources.py`, from `paper-sparse-sos`:
   exit 0, `SOURCE_CHECK=ok`; 14 inputs, 244 unique labels, and 40 cited
   keys. Required inputs exist; references and citations resolve; duplicate
   labels/keys and active draft markers are absent.
2. `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`,
   from `paper-sparse-sos`: exit 0; 75-page PDF. The final build log and
   BibTeX log contain zero LaTeX errors, undefined references/citations,
   overfull boxes, and BibTeX warnings/errors. The last local build output
   is `build/latexmk-final.stdout`.
3. `python3 verification/package_sources.py`: exit 0; packaged 17 source
   files plus an embedded hash manifest. The ZIP contains the complete
   manuscript, macros, bibliography, one appendix, build instructions,
   and optional source checker. Internal reviews and research records are
   excluded from the submission archive.
4. Extracted the archive into the fresh directory
   `/tmp/sparse-sos-standalone-blwx6dkn`. Verified every source file's byte
   length and SHA-256 against the manifest. Ran
   `python3 verification/check_sources.py` and
   `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` there:
   both exited 0. The build used only extracted sources and the installed
   LaTeX tools/packages.
5. `pdftotext` on the standalone and local PDFs: their full extracted text
   is identical. The delivered PDF is copied from the standalone build.
6. `pdfinfo delivery/sparse-sos.pdf` and
   `pdffonts delivery/sparse-sos.pdf`: 75 pages, correct title metadata,
   blank author metadata, and all 23 fonts embedded.
7. `pdftoppm` and visual inspection: the title/abstract page, result table,
   bibliography, and the new constrained-certificate statement and proof
   render cleanly. The added development was inspected on pages 60–61.
   Mathematical reviews read the source throughout; visual sampling is
   not described as inspection of every rendered page.

The archive check commands and exact results are recorded in
`standalone-build.json`. `final-artifact-checks.json` records diagnostics,
PDF metadata, embedded fonts, byte lengths, and final hashes.

An independent final GPT delivery audit,
`reviews/delivery-consistency-gpt-r1.md`, accepted these records. It checked
actual archive members, current and standalone source bytes, artifact
hashes, PDF metadata, fonts, labels, citations, and build receipts without
rerunning the builds or experimental work.

## Delivered artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `delivery/sparse-sos.pdf` | 849825 | `15b408477d6b4defda9580eceb34e9570c595efc10447b0bd49d6416ac851621` |
| `delivery/sparse-sos-source.zip` | 110853 | `6f1721b447ca6c4957a8f439727b758bbf74af3ffb284d0cba96a6980066c871` |
| `delivery/source-manifest.json` | 2303 | `0ab9e0a621675aa107b50285160c5dd6c2ba17748e5530e52a864ca6ad84ea64` |

## What the checks establish

These checks establish source completeness, internal reference consistency,
a successful standalone document build, and the correspondence between the
reviewed source and delivered files. Mathematical correctness was assessed
by independent GPT proof reviews, including degree, positivity, separation,
approximation, exact-certificate, and encoding arguments. Those reviews
found no unresolved mathematical defect. They are internal reviews and do
not constitute external peer review or journal acceptance.

Existing computational results were retained under the user's instruction
to trust them. No new experiment was needed. Higher-order SDP/local-measure
equality is explicitly a conjecture; the paper does not present the
retained floating-point evidence as a proof.

Primary-source contracts and full-text access limits are in `LITERATURE.md`
and its three Luna lane ledgers. The sole owner's `LITERATURE-KB.md` receipt
records all 29 requested package outcomes, source-note checks, access states,
and preserved candidate/decision/result archives.

## Serialized literature check

The single shared Luna lead, rather than a second session, ran
`/workspace/local-home/repo/skills/literature/scripts/lit.py check /workspace/minlp-notes/literature`
directly after its latest package-note edits. At 05:59 UTC on 6 October 2026
it exited 0 with `KB_CHECK=ok`, `UNREAD=197`, and `READ_UNCITED=770`.
Three existing unrelated preview warnings are preserved in the receipt.
The lead verified the archived round copies and Kahl PDF against their
retained originals. No manuscript or bibliography source changed during
this final maintenance step, so the accepted standalone artifacts remain
current. The document builds and the literature check establish separate
properties; neither substitutes for the other.

The independent GPT review `reviews/final-literature-receipt-gpt-r1.md`
accepted all 29 work mappings, archived outcomes, actual reading/access
states, source-file hashes, and the receipt chronology. Root also preserved
15 earlier raw search/metadata files under `literature-discovery/`, comparing
every copied file byte for byte and recording its hash in
`earlier-artifact-manifest.json`. Those incomplete earlier artifacts are
not described as completed discovery rounds or intake outcomes.
