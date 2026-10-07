# Final bibliography-only Sol recheck

Date: 2026-10-05. **Pass. Opus R3 items S2 and B1 are resolved in the
actual bibliography, vetted source record, generated main.bbl and extracted
PDF text. No further bibliography finding remains in this scope.** This is
a metadata and rendering-text review, not a new source investigation or
mathematical review. Opus R3's closed S1 disposition is unchanged.

The final typography-only follow-up also passes. It adds protected proper
names and acronyms in eight titles and changes no source fact, citation key, version note
or manuscript body. The final snapshot below includes this follow-up.

I read the R3 findings and their record context in
evidence/reviews/opus-final-scope-r3.md, the three current bibliography
entries, the corresponding literature rows and access notes, and the actual
generated bibliography/PDF text. A delegated independent read-only check
also accepted the source-entry and literature-record changes. I authored
only this assigned evidence file.
For the typography follow-up I inspected only the eight literal title
changes and their final main.bbl/PDF text; I did not re-review sources,
metadata facts or proofs. A second delegated literal-case check agreed.

## Dispositions

**S2, inspected versions and theorem numbering: resolved.**

- GrigorievPasechnik2005 identifies cs/0403008v3 in its eprint and URL and
  prints “arXiv version 3; theorem numbering refers to that version.”
  The vetted sampling row at literature-review.md:88 explicitly identifies
  that inspected version. Access item 12 at line 131 states that the
  journal full text was not retrieved or inspected and that the theorem
  statement and locator refer only to the inspected v3 preprint.
- DedieuMalajovichShub2005 identifies math/0312083v2 and prints the date
  19 July 2004 with the same theorem-numbering qualification. The vetted
  row at line 89 and access item 13 at line 132 agree. They do not claim
  inspection of the journal text or its numbering.

The plainnat bibliography actually prints these notes and version-specific
URLs: DMS in reference [29] and GP in [48]. They also appear in the text
extracted from the rebuilt PDF. Thus the fix does not depend on plainnat
printing an eprint field that it normally omits. The journal identities and
metadata remain present; the notes identify the versions supplying the
numbered statements. This is version-safe attribution and preserves the
recorded access gaps. I accepted Luna's version inspection record without
retrieving or checking either primary source myself.
The final typography refresh leaves both printed version notes identical.

**B1, Roman numerals in titles: resolved.** GP protects {I} in its title;
Renegar1992QE protects {Part III}. The generated main.bbl preserves both,
and PDF reference [48] prints “quadratic maps I” while [102] prints
“Part III: Quantifier elimination.” The Renegar source row continues to
identify Part III, Theorem 1.1; no source contract or body citation changed.

The eight additional literal-case protections print correctly in the final
main.bbl and extracted PDF:

- DawsonNielsen2006 protects {Solovay--Kitaev}; reference [28] prints
  “The Solovay–Kitaev algorithm.”
- GranotSkorinKapov1990 protects {Tardos}; [47] prints
  “An extension of Tardos’ algorithm.”
- HildebrandKoeppe2013 protects {Lenstra}; [55] prints
  “A new Lenstra-type algorithm.”
- Serre2008 protects {Galois}; [110] prints “Topics in Galois Theory.”
- EklundJostPeterson2013 protects {Segre}; [37] prints
  “A method to compute Segre classes of subschemes of projective space.”
- JeyakumarLi2014 protects {SOS}; [58] prints
  “A new class of alternative theorems for SOS-convex inequalities and
  robust optimization.”
- KrickPardoSombra2001 protects {Nullstellensatz}; [72] prints
  “Sharp estimates for the arithmetic Nullstellensatz.”
- Kollar1999 protects the whole word {{\L}ojasiewicz}; [68] prints
  “An effective Łojasiewicz inequality for real polynomials.” A brace
  around the single \L command had allowed BibTeX to lowercase that
  initial; protecting the whole word preserves the printed uppercase Ł.

The actual Dawson and Serre keys are DawsonNielsen2006 and Serre2008.
The original I/Part III protections remain unchanged and printed correctly.

A full diff against the frozen bibliography baseline
/tmp/exact-paper-submission-final-w6exg0zd/references.bib, whose hash is
20dbe6573a5b4be6749c6c188a6adbfe3a123e21d7599d14a07ca1fd67e3f7a5,
contains changes in exactly eleven entries: the three original fixes plus
the eight proper-name and acronym protections. The added eight changes
consist only of title braces. Author names, journal
names, years, volumes, issues, pages and DOIs are unchanged.

## Version and key checks

The targeted document inventory finds **126 entries, 126 unique keys, 120
distinct cited works, and no unresolved citation key**. It reads only the
manuscript bibliography and the 25 section/appendix sources. A separate
document hash comparison reads the 27 frozen body-source hashes in Opus R3
and compares them with the actual files: **27 match, zero differ**. The
abstract/00/08 hashes also remain those accepted in final-scope-sol-r1.md.
No body proof was reopened.
All counts and the 27-file hash comparison were refreshed after the final
eight title protections. Citation keys and all body files are unchanged.

The current main.bbl and PDF hashes were refreshed after root confirmed the
build was complete. I extracted the PDF myself with pdftotext -layout and
read the eleven changed bibliography entries from that extraction. The check
covers the printed wording, names, acronyms and numerals, not a new visual
or whole-PDF inspection.

```text
9e27da1a5d46804a20667ae02e43ce80b3d738d7cda4e67ab4b46cc21085d4ae  references.bib
30b015fcfcef4e216d5fca14250dc9c298b43f4acc2950ff6677b212bd92b28b  evidence/literature-review.md
c7408972e745bfd43d25874a6e0514ce97967b1c99662d4a75af5026abd5e593  main.bbl
3aa61cc15fef24f3e35f2a18c6084b23200a9b862ac6538d3b0ea24e319d1ad8  main.pdf
b186fe9caa83d2927827e217ea9506178b5a4e90f30b9a700592577fed582350  evidence/reviews/opus-final-scope-r3.md
491f90e98658426866e4755c8b3b5f4d84d85569f02e083241d5f2cdd4a7cca8  sections/abstract.tex
32a473010509ff4930f8dfa4d67fd1f1efdf014723c23fba142967a388f17f92  sections/00-introduction.tex
1c3b8d8123348933fecdae6a5b6ed677ef6ffc46010782b0005999e925e121be  sections/08-fields.tex
```

## Actual targeted checks and limits

Checks run were scoped rg/rg --files, cat, nl -ba/sed, diff -u against the
named baseline, and sha256sum; pdftotext -layout main.pdf wrote
/tmp/exact-arithmetic-bibliography-sol-r1.txt for the requested text
inspection. An inline Python document-only inventory parsed bibliography
and citation keys and compared SHA-256 strings against the Opus R3 body
snapshot. It performed no mathematical computation or test.

This report's git diff --no-index --check /dev/null check emitted no
whitespace diagnostic; exit 1 is the new-file difference from /dev/null.
I did not edit manuscript, bibliography, literature records or build
outputs, browse, research sources, compile, run mathematical scripts,
experiments, CAS, historical diagnostics, project-wide checks or inspect CI.
The build was root's action. Archive/package hash refresh remains root's
separate task; this review makes no claim that an archive was regenerated.
It supplies internal review evidence, not external peer-review approval or
a guarantee of journal acceptance.
