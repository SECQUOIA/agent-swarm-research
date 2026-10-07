# Bibliography closeout after Opus final scope R3

The completed Opus R3 passes all four manuscript repairs and finds no new
mathematical defect. Its source-record item S1 was resolved during that
round: the height–Mahler identity is recorded with an elementary derivation
and explicit limits on textbook inspection. No theorem or proof changed.

## Findings and repairs

- **S2: exact source versions.** The GP entry now links to arXiv
  cs/0403008v3 and prints a note that the theorem numbering refers to that
  version. The DMS entry links to math/0312083v2 and prints the same note
  with its 19 July 2004 date. Luna confirmed these versions from the
  existing primary-text audits, without guessing from unversioned links.
  Journal publication metadata and DOI fields are retained. The source
  report now includes both uninspected 2005 journal texts in its access-gap
  list; their numbering is not claimed to have been checked.
- **B1: bibliography case.** The GP title protects I; the Renegar title
  protects Part III. A visual and title-field pass also identified names
  and acronyms needing the same sentence-case protection: Solovay–Kitaev,
  Tardos, Lenstra, Galois, Segre, SOS, Nullstellensatz and Łojasiewicz. Those
  literal title fragments are now protected. All 126 title fields were inspected.
  Nothing else in those eight additional entries changed.

Eleven bibliography entries differ from the R3 source snapshot: GP, DMS and
Renegar, plus the eight title-only entries. Citation keys, journal
publication facts and all 27 TeX files are unchanged. The bibliography
still has 126 records and 120 cited works. These repairs need a document
build, archive refresh and bibliography-scoped recheck; R3 explicitly
requires no mathematical re-review.

The first bibliography recheck passed the original three-entry repair.
The final refresh includes the eight capitalization entries as well.
The final scoped recheck passes all eleven entries, their printed forms and
the frozen body hashes (`reviews/final-bibliography-r1.md`).
Root builds and package checks are documented separately in
`verification/FINAL-VERIFICATION.md`; no computational experiment was rerun.

## Current source hashes

```
9e27da1a5d46804a20667ae02e43ce80b3d738d7cda4e67ab4b46cc21085d4ae  references.bib
30b015fcfcef4e216d5fca14250dc9c298b43f4acc2950ff6677b212bd92b28b  evidence/literature-review.md
b186fe9caa83d2927827e217ea9506178b5a4e90f30b9a700592577fed582350  evidence/reviews/opus-final-scope-r3.md
```
