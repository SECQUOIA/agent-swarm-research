# Primary-source checks during manuscript preparation

## Schoenebeck's signed-character input

The author-hosted full version of Grant Schoenebeck, *Linear Level Lasserre Lower Bounds for Certain k-CSPs*, was retrieved from <https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf>. Retrieval details and the SHA-256 digest are in `schoenebeck-source.json`. This is the full version linked by the repository, rather than an assumption based on its abstract.

The coordinator read printed pages 7–11 and visually inspected page 7. Theorem 11 supplies a positive linear width at fixed density. Theorem 12 and Lemma 13 connect this to Lasserre feasibility; the latter uses half the resolution width. For three-variable XOR, density 8, delta=1/4, epsilon=0, and gamma=1/4 meet the stated requirements. Choosing gamma=1/4 avoids the denominator boundary in the source's illustrative gamma=1/2 choice.

On pages 10–11, signed equivalence classes define character vectors. Their product inner-product formula supplies character moments in {0,-1,1} through the available width. Positivity follows for arbitrary linear combinations of those vectors, not only individual local functions. Stage 5 must explicitly translate width into original degree 4r or 4rD and verify the separate spatial transfer.

## Initial current-literature checks

The coordinator also retrieved Cornuéjols's July 2000 author manuscript, *Combinatorial Optimization: Packing and Covering*, <https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf>, with its hash in `cornuejols-source.json`. Printed page 76, Theorem 6.5, gives Camion's criterion for every Eulerian submatrix, including the rectangular formulation needed here. Printed page 82, Theorem 6.13, gives mixed packing/equality/covering integrality for balanced matrices with its specified right-hand sides and unit bounds. These support distinct arguments; balancedness alone must not be substituted for total unimodularity when arbitrary integer slab bounds are used.

Primary search results confirmed the distinct signed-bilinear scope of Boland et al., *Bounding the gap between the McCormick relaxation and the convex hull for bilinear functions*, <https://arxiv.org/abs/1507.08703>, and the older Schur-multiplier setting of Davidson and Donsig, <https://arxiv.org/abs/math/0506073>. The retrieved metadata alone is not a proof audit; Stage 1 checks their local full texts.

The 2026 preprint by Ahmadi, Dash, Hua, and Stellato, *Disjunctive Sum of Squares*, remains relevant related work: <https://arxiv.org/abs/2605.28674>. The local source record identifies its simplicial/spherical certificate setting. Stage 5 and final integration must compare the actual region and oracle models without claiming that the present box lower bounds apply to all disjunctive SOS algorithms.

No search in this record establishes publication priority.

## A related source with incomplete access

The direct OpenReview PDF for Stefano Coniglio, *Solving the 2-norm k-hyperplane clustering problem via multi-norm formulations* (ICLR 2026), redirected to a browser-verification challenge: <https://openreview.net/pdf?id=VJAqqtVXfD>. The challenge was not bypassed. The author's publication page confirms the paper and points to OpenReview: <https://stefanoconiglio.github.io/publications.html>. Search results expose portions of the primary paper, but the coordinator has not checked its full appendix. The manuscript must acknowledge the related spatial lower bound recorded in the repository, restrict any comparison to inspected statements, and avoid an exhaustive-priority claim. A complete primary comparison remains an external source-check limit unless a later stage obtains another legitimate open copy.
# Additional direct checks during Stage 1 corrections

- Sherali (1997), local original PDF pp.252–253 (PDF8–9): read equation (13) and Theorem3 directly. They concern the complete elementary symmetric polynomial, not arbitrary sparse positive polynomials. The equal-marginal optimization formula in the repository is correctly positioned as a consequence. Original: https://math.ac.vn/uploads/files/9701245.pdf.
- Hassin–Tamir, *Efficient Algorithms for Series-Parallel Graphs*: retrieved the open author scan, SHA recorded in `hassin-tamir-source.json`, and visually read printed pp.380–381 (PDF2–3). Theorem3.1 states the biconnected-component characterization by absence of a subdivision of K4, credited to Dirac and Duffin; the same pages give edge series/parallel constructions and terminal conventions. This supports the decomposition input for the one-sided coloring proof. The browser screenshot endpoint failed, but the direct open-author download succeeded; no access control was bypassed. Original: https://www.math.tau.ac.il/~hassin/sp.pdf.

## Later access update: Coniglio's review version

On 2026-09-05, the indexed anonymous ICLR2026 review version was readable
through the browser at
<https://openreview.net/pdf/369974754b073802afab412ee5f715561c39adbc.pdf>
(19 pages). Root read Assumption1 and Proposition2 on printed page6,
Propositions3–4 on page8, and their AppendixC proofs on pages16–17.
The baseline statement assumes midpoint splits of symmetric coordinate
domains. The proof uses the surviving lineality of partially restricted
normal vectors and separately convexified norm constraints. This is a
related coordinate-branching obstruction, not the paper's arbitrary-split,
fixed-order localizer theorem. Do not import the review version's precise
counts or stronger phrasing into our theorems.

The published PDF endpoint still returned a verification challenge. Direct
download of the review PDF returned403 and its browser screenshot failed;
no local copy/hash or visual inspection is claimed. The readable extracted
review text narrows the prior access limitation but does not establish
identity with the published version or validate every statement in it.

## Karp reprint visual check

Root downloaded the authorized reprint linked in the bibliography and visually
read original pages94,97,100 (PDF pages14,17,20). The Main Theorem, PARTITION
item20, and KNAPSACK-to-PARTITION reduction were checked directly. The latter
adds b+1 and sum(a)+1-b to the input numbers, so positive subset-sum instances
with0<=b<=sum(a) give positive PARTITION inputs. The source lists general
integer inputs; positive hardness suffices here. The SHA and locators are in
karp-source.json. OCR was used only to find pages; the recorded statements
were checked on the rendered scans.

## Potechin's classical fractional-cardinality input

Root read Potechin (ITCS2019), Theorem1 and its knapsack setup,
Example18, and the knapsack part of Theorem44/Corollary45 with its proof.
Example18 was also visually checked on printed61:8 (PDF8): its general
moment is binomial(k,|I|)/binomial(n,|I|), equivalently the falling-factorial
ratio. The source explicitly attributes the stronger knapsack SOS bound to
Grigoriev. This supports classical attribution of the moments; our elementary
Gram proof uses a sufficient, weaker degree range and proves its own
continuous spatial transfer and localizer constraints. Root did not audit the
entire general symmetry theorem. Original URL and SHA are in
potechin-source.json; temporary original and extracted text are outside the
paper directory.

## Stage 4 clique-cut primary attribution (coordinator)

Directly checked the local original Padberg (1989), *The Boolean quadric
polytope: Some characteristics, facets and relatives*, Mathematical
Programming 45, 139–172, DOI 10.1007/BF01589101. PDF page 11, printed
page 149, Lemma 2, equation (17), states
`alpha*x(S)-y(E(S)) <= alpha*(alpha+1)/2` for integer
`1<=alpha<=|S|-1`. The formula is absent from the extracted local text;
the coordinator read the rendered original page and its short validity
proof. Taking the full coordinate set and alpha=k gives exactly the
Stage 4 cut. Its continuous multiaffine extension and root exactness
are independently proved in the manuscript. Theorem 4's facet context
was read but no facet theorem is needed for this application.

As a cross-check, directly read Saito, Fujie, Matsui and Matuura (2004),
*The Quadratic Semi-Assignment Polytope*, METR 2004–32, June 2004,
https://www.keisu.t.u-tokyo.ac.jp/data/2004/METR04-32.pdf .
Section 4, equation (9), PDF page 10/printed page 8, has the same cut
with beta=k+1 and explicitly credits Padberg. Both browser text and
rendered PDF were inspected. The local Padberg original is preferable
for direct manuscript attribution. No source PDF was copied into the
paper folder or modified in the literature collection.

## Original fractional-cardinality provenance (coordinator)

The coordinator read the local Grigoriev (2001) original's setup, main
refutation-degree theorem on PDF page 5, and functional construction plus
Lemmas 1.3–1.4 on PDF page 7, checking both pages visually. The original
defines the normalized Boolean-reduced functional by
`B(X^I)=(r)_{|I|}/(n)_{|I|}` and proves the demand-times-polynomial
identity in Lemma 1.3. Lemma 1.4 states positivity of its degree-l square
form for `l-1<r<n-l+1` (with the surrounding `l<=floor(n/2)` range).
The full subsequent positivity proof was not independently audited here;
Stage 4 supplies its own sufficient positive-Gram proof and the additional
assignment-indicator localizer argument required by its full preordering.
A stronger square-positivity range alone does not automatically extend
that full preordering range, whose products can have degree 2r.
The file is an author manuscript with its own page numbers, not the
journal pagination; use the lemma numbers for precise attribution.

The coordinator also read Laurent (2003), introduction and the hierarchy
definitions through Theorem 5; visually checked PDF page 2/printed page
872. Its opening paragraph explicitly credits Grigoriev's argument for
the fractional-cardinality knapsack hierarchy obstruction and distinguishes
the Lasserre and semidefinite Lovasz–Schrijver interpretations. This is
provenance for a discrete hierarchy result, not a spatial region-count
theorem. The main cut-polytope PSD proof was not audited for this task and
is not needed by Stage 4. Potechin's modern account was checked separately.
