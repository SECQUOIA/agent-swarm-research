# Yang (2009): source access status

Checked 2026-10-03. **The full primary manuscript was not obtained. The
theorem-level comparison remains open.** This note records the bounded search;
it does not certify any theorem statement from Yang's paper.

The work is W. H. Yang, *Error Bounds for Convex Polynomials*, SIAM Journal on
Optimization 19(4), 1633–1647, DOI
[10.1137/070689838](https://doi.org/10.1137/070689838). The publisher records
online publication on 21 January 2009. Some citing bibliographies use 2008,
consistent with the journal volume's 2008–2009 label; this search found no
evidence of two different papers.

## What was accessible

The [publisher abstract](https://epubs.siam.org/doi/10.1137/070689838)
describes a structural decomposition and error bounds for unconstrained and
polyhedral-constrained convex polynomials. It does not expose the degree
exponent, theorem hypotheses, constants, or their algorithmic construction.
The [publisher-supplied ResearchGate preview](https://www.researchgate.net/publication/220133028_Error_Bounds_for_Convex_Polynomials)
contains the first page, with abstract and introduction; it does not supply
the later theorem statements. The
[author's Fudan profile](https://sklcam.fudan.edu.cn/50/6c/c26373a282732/page.htm)
confirms the publication but offers no full-text link.

## Routes checked

| Route | Observed result |
| --- | --- |
| SIAM DOI landing page and `/doi/pdf/10.1137/070689838` through the web tool | Abstract/access page; the PDF route redirects to `/doi/abs/10.1137/070689838?journalCode=sjope8`. |
| SIAM `/doi/full/10.1137/070689838` and `/doi/epdf/10.1137/070689838` through the web tool | Inaccessible; no full text returned. |
| Ordinary HTTP requests to those three SIAM document routes | HTTP 403 challenge pages, not PDFs. |
| [Crossref DOI record](https://api.crossref.org/works/10.1137/070689838) | Supplies the same SIAM PDF URL; no separate accepted manuscript. |
| [OpenAlex DOI record](https://api.openalex.org/works/https://doi.org/10.1137/070689838) | Reports `is_oa: false`, `oa_status: closed`, and `any_repository_has_fulltext: false`; only the DOI location is listed. |
| [Semantic Scholar DOI record](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/070689838?fields=title,openAccessPdf,url) | Reports `openAccessPdf.status: CLOSED` with an empty PDF URL. |
| Fudan author profile and publication list | Bibliographic confirmation, no accessible manuscript. |
| Exact-title/DOI and author-name searches, including Optimization Online, HAL, CUHK, and the Tsinghua mathematical archive | Other papers citing Yang, bibliographic records, and a conference schedule; no full Yang manuscript found. |

No author was contacted, no purchase was made, and no institutional access or
access-control bypass was attempted. The index records describe the search
state; they do not prove that no public manuscript exists elsewhere.

## Consequence for the topic-2 literature comparison

Do not describe the dimension-independent degree exponent, a constrained
version, coefficient-dependent constants, or an effective constant-computation
procedure as absent from Yang (2009) on the evidence of this search. The
abstract is insufficient for any of those conclusions. Likewise, do not
promote a later survey's attribution to a checked primary-source theorem.

The missing comparison requires the full paper, specifically:

1. Exact hypotheses and quantifiers of its unconstrained and polyhedral
   error bounds.
2. Whether the exponent concerns a single globally convex polynomial, a
   polynomial restricted to a polyhedron, or a system.
3. How the constants depend on coefficients, degree, dimension, and the
   polyhedral constraints.
4. Whether the proof constructs constants with polynomial binary size and
   a polynomial-time procedure, or establishes existence only.
5. Whether the output controlled is distance to the optimizer set or to
   one optimizer selected consistently at every requested precision.

Until those items are checked, the correct status is **source access gap**,
not verified novelty or verified redundancy. The existing
[literature record](../../literature/papers/yang2009-error-bounds-for-convex-polynomials/paper.md)
remains appropriately marked unread.

## Related primary source located

Huynh Van Ngai's author preprint,
[*Global Error bounds for systems of convex polynomials over polyhedral
constraints*](https://optimization-online.org/wp-content/uploads/2011/11/3237.pdf),
is publicly accessible through its
[Optimization Online record](https://optimization-online.org/2011/11/3237/).
It is a useful separate comparator, not a replacement for checking Yang's
manuscript. This note does not audit its theorem statements.

## Checks performed

Read the existing Yang literature record; inspected the primary abstract,
preview, author profile, and DOI-index responses; searched the public routes
listed above. No mathematical theorem verification or project-wide checks
were run for this source-access task.
