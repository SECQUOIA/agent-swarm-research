# Stage 4 corrections after round 1

The separate correction agent addressed all three accepted minor findings from
the root adjudication. No mathematical statement or proof changed.

| Finding | Resolution |
|---|---|
| R1-F01 / R4-01 / R5-02 | The symmetric-reference remark now states that the five-product construction changes both `v_01` and the induced balances `b=Av`, and hence the flow domain. It explicitly distinguishes this modification from translating the cycle coordinates of one fixed domain. |
| R3-01 | The bibliography now uses the published author list, Michal Melamed and Shmuel Onn, in that order, and DOI `10.1016/j.laa.2014.01.007`. The citation key is `MelamedOnn2014`. A versioned open preprint link is retained and identified as the 2012 preprint by Shmuel Onn and Michal Rozenblit. |
| R5-01 | The Khademnia–Davarnia comparison now says that equality balances are represented by opposite inequality pairs. It retains the substantive distinction between a projection-cone multiplier and an unavoidable observed-product coefficient ratio. The local sentence also now reads “the related example of” for grammatical agreement. |

For the metadata correction, the correction agent independently retrieved the
publisher-deposited [Crossref record](https://api.crossref.org/works/10.1016/j.laa.2014.01.007)
and inspected the [versioned arXiv record](https://arxiv.org/abs/1208.5639v1).
Direct web-tool access to the DOI and Crossref endpoint failed; Python's URL
retrieval succeeded for Crossref. The retrieved fields are preserved in
`verification/stage04-corrections/published-reference-metadata.json`.

A clean `latexmk -C` followed by the documented PDF build succeeded. The result
has 27 pages and no final LaTeX warnings, undefined references/citations, or
overfull/underfull boxes. Extracted text and rendered pages 25–27 were inspected;
the corrected discussion and bibliography are legible and within the margins.

The final diff changes only `sections/04-bounded-rank.tex` and `references.bib`.
Earlier section files match the review snapshot byte for byte. The diff, clean
and build logs, extracted text, page images, and source/PDF hashes are preserved
under [`verification/stage04-corrections/`](../verification/stage04-corrections/).
Root acceptance remains a separate step.
