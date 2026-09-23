# Priority audit for the four-aggregation PDLC bound

Date: 2026-09-22. Independent literature review of
[the candidate strict-system transfer](research-20260922-pdlc-frontier.md).
This review checks sources and proof dependencies, not the new proof.

The fully verified published four-aggregation theorem retains both geometric
assumptions that the candidate seeks to remove. Dunbar's dissertation states
a stronger theorem without the infinity assumption, but its proof invokes
results that explicitly require that assumption. The dissertation therefore
creates a priority issue that must be reported; it does not supply a verified
proof of the stronger statement from the text inspected here.

## Verified published statements

[Blekherman–Dey–Sun, arXiv v2](https://arxiv.org/html/2210.01722v2),
Theorem 2.18 and Corollary 2.20, give six good aggregations for three strict
quadratics under homogeneous PDLC, nonempty proper convex hull, and the
theorem's `n >= 3` setting. Example 2.21 requires four. Conjecture 3.2 asks
for a six-necessary example. These are the locators in the inspected v2;
the repository's journal extraction uses different theorem numbering.

[Blekherman–Dunbar, published version](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full),
SIAM Journal on Applied Algebra and Geometry 9(2), 310–342, DOI
[10.1137/24M1668445](https://doi.org/10.1137/24M1668445), was published online
6 May 2025. Theorem 1.4 treats the nonstrict set `C={x:f_i(x)<=0}`. It
assumes PDLC, nonempty interior, `C=cl(int C)`, and no nonzero homogeneous
feasible point in the hyperplane at infinity. Its closed convex hull needs
at most four good aggregations. Section 7 explicitly does not assume spectral
smoothness. The theorem's proof invokes Propositions 7.7, 7.8, and 7.11.

[The arXiv history](https://arxiv.org/abs/2405.18282) lists only v1,
28 May 2024. Its [full text](https://arxiv.org/html/2405.18282v1) gives the
same assumptions in Theorem 1.4. The relevant proofs are in Section 8 there,
rather than Section 7 of the published version. Do not mix these locators.

## Dissertation: full text obtained, stronger statement not justified by its dependencies

Alex Dunbar, *Leveraging Algebraic and Geometric Structures in Optimization*,
Emory dissertation, Summer 2025:
[record](https://etd.library.emory.edu/concern/etds/vq27zq10w),
[original PDF](https://etd.library.emory.edu/downloads/2j62s637x?locale=en),
[public full-text reader](https://r.jina.ai/https://etd.library.emory.edu/downloads/2j62s637x?locale=en).

Theorem 5.0.5, printed page 97, states four aggregations under PDLC,
`C=cl(int C)`, and nonempty interior, omitting the infinity assumption.
The subsequent paragraph still contrasts this regular nonstrict case with
BDS's strict-system conjecture.

The proof on pages 124–126 uses Proposition 5.3.13 for one case and
Proposition 5.3.12 for connectedness in the other. Both propositions,
pages 121–122, explicitly require no points at infinity. The proof of
5.3.12 uses that condition to force components of the aggregation intersection
to meet `C`. I found no standing assumption in the chapter or Section 5.3.3
that supplies it to Theorem 5.0.5. Thus the displayed theorem is stronger
than its cited argument supports; an omitted hypothesis is a plausible
explanation, not an established author correction.

The text extraction loses some bars and inequality slashes, including in
the nonempty-interior condition. The independently indexed theorem passage
confirms that condition. An original-PDF visual check remains desirable.

## Retrieval record and remaining limits

Direct web retrieval of the Emory PDF failed with HTTP 405; direct Python
requests returned 403. Locale variants, the public file-set page, and JSON
record also failed. The public reader returned the complete 155-page
extraction, with filename `Dunbar_PhD_Thesis_Final_Final.pdf` and reported
source modification time 2 July 2025. It was saved outside the repository
as `/tmp/dunbar-thesis-priority.txt`; all Chapter 5 theorem and dependency
passages discussed above were read from that full extraction, not merely
search snippets. No PDF binary was obtained.

The [author's page](https://alex-dunbar.github.io/) links the published
article and arXiv. Its public GitHub repository's complete `gh-pages` tree
was inspected and contains no thesis mirror. Searches of the exact title,
the theorem number, PDLC, and strict/four-aggregation variants found no
further theorem resolving the unrestricted strict case. Several queries
returned irrelevant results, so this absence is weak evidence.

The candidate should be described as a proposed extension of the published
four-bound to arbitrary strict systems, while acknowledging the stronger
dissertation statement and its unresolved proof dependency. It should not
claim that removing points at infinity was never previously stated. Removing
closed-set regularity and handling strict inequalities remain additional
issues even if the dissertation's stronger statement is eventually verified.
Novelty requires further checking; unsuccessful retrieval or search never
establishes it.

Targeted verification: direct inspection of the cited statements and proof
dependencies, full Chapter 5 text search, arXiv version history, and public
author-repository file listing. No mathematical tests, Lean checks,
project-wide checks, or CI inspection were performed for this audit.
