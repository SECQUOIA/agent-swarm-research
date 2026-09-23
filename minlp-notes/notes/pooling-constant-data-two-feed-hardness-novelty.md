# Source audit: constant-data pooling with two pool feeds

Date: 2026-09-05. This is a bounded primary-source novelty audit of
[the reviewed theorem](../results/pooling-constant-data-two-feed-np-completeness.md),
not a third proof audit. No matching published theorem was found for its
combined restrictions. This does not certify priority.

The strongest defensible contribution is **strong NP-completeness with one
pool, one upper-only quality, two arcs entering and leaving the pool, bounded
external-node degrees, zero flow lower bounds, and fixed finite alphabets
for all local numerical data**. The total number of bypass sources and
outputs grows. The integer decision threshold is only linear in network
size. The fixed-alphabet arithmetic encoding is a substantive strengthening
of the repository's earlier ordinary NP-completeness result.

## Closest prior claims and exact model distinctions

**Baltean-Lugojan and Misener (2018), Remark 4.6, is the closest prior
hardness assertion.** Their model permits direct source-output arcs.
Assumption 2.2 removes feed availability and pool capacities and fixes
positive product demands. Remark 4.6 asserts NP-hardness when these
restrictions are relaxed. Its argument passes to bivariate rational
polynomials or polynomial systems and cites Garey–Johnson; the inspected
text gives no explicit reduction establishing the precise restricted
pooling class. It states neither constant alphabets nor the simultaneous
degree bounds. A resulting polynomial system alone does not establish a
hardness reduction. Thus credit the prior broad boundary assertion while
distinguishing this explicit strong classification.
[Open primary PDF](https://d-nb.info/1149002905/34), Assumption 2.2 and
Remark 4.6; [publisher version](https://doi.org/10.1007/s10898-017-0577-y).
The supplied local full text was also checked.

**Haugland and Hendrix (2016) explicitly identify the bypass distinction.**
The discussion immediately following Theorem 4.1 says the preceding
fixed-source, fixed-output, and fixed-quality single-pool algorithms are
not proved under the alternative convention allowing direct arcs. It asks
whether polynomial solvability holds when one of those counts is fixed
and only one pool has more than one entering and more than one leaving
arc. The new theorem answers the fixed-quality branch negatively, with
the stated stronger restrictions. Their pseudo-polynomial result concerns
two total sources and two total terminals, one quality, and additional
cost assumptions; it does not apply to unbounded bypass networks.
[Primary article](https://doi.org/10.1007/s10957-016-0890-5), Sections 4.5
and 5; the bypass question is on PDF p.17, printed journal p.607,
after Corollary 4.1 and before Remark 4.1. This is a precise earlier open
question, not a claim that the question remained unmentioned until now:
the later Baltean-Lugojan–Misener assertion must still be acknowledged.

**Alfaki and Haugland (2013) already prove strong one-pool hardness.**
Their independent-set construction has one quality coordinate per source
vertex, growing pool degrees, and quality bounds depending on graph size.
It therefore does not give a fixed-quality, fixed-alphabet, bounded-degree
result. It also establishes polynomial solvability with one pool and fixed
qualities in the model without direct arcs.
[Primary article](https://doi.org/10.1007/s10898-012-9875-6), supplied full
text pp.5–7. Strong one-pool hardness by itself is established prior art.

**Haugland (2016) proves several other strong restrictions separately.**
Its one-quality reductions permit many pools. Its bounded-degree
reductions do not impose one quality and one pool together. The
two-source/two-terminal/one-quality reduction establishes ordinary
NP-hardness and uses growing numerical input. Most importantly, its model
excludes direct source-terminal arcs; replacing one by a degree-one pool
changes the pool count. Upper and lower quality specifications are
counted as two attributes in its upper-only convention. The new theorem
requires only upper specifications in one coordinate, so that counting
issue does not arise.
[Primary article](https://doi.org/10.1007/s10898-015-0335-y), supplied full
text Sections 2–5. See also the
[earlier source-model audit](pooling-single-quality-bypass-novelty.md).

**Boland, Kalinowski, and Rigterink (2017) fix the total number of inputs.**
Their single-pool polynomial theorem and complexity table use the
no-direct-arc convention. Two arcs entering the unique mixing pool in the
new theorem leave an unbounded number of external bypass sources. This is
not the fixed-total-input parameter in that theorem.
[Open primary preprint](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf),
model definition and Section 3. Its degree-related open problems should
not be silently identified with the new mixed degree bounds: output
in-degree here is three, not two.

## What the fixed-data encoding establishes

Matsui's positive-product reduction is the established source of hardness,
not a new source problem. Its coefficients have polynomial binary length
but grow numerically, so applying that reduction directly proves only
ordinary NP-hardness.
[Matsui, METR95-13](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf),
Sections 2–3, Theorem 3.1.

The new construction replaces those coefficients by a polynomial-size
network of bounded linear signal gates. Repeated averaging encodes dyadic
weights by their bits. The nonlinear interface then needs just two pool
feeds. Finally, an objective attains its explicit upper bound exactly
when all temporary exact supply and demand contracts hold. This removes
positive flow lower bounds without a large penalty coefficient.

Repeated doubling or averaging to encode binary numbers, introducing
auxiliary variables for linear arithmetic, and summing nonnegative
contract deficits are elementary established techniques. They should not
be claimed as new in isolation. The potentially new representation result
is their realization inside this particular blending network while
simultaneously preserving one-sided quality constraints, the fixed
quality palette, input out-degree two, output in-degree three, and two
pool feeds. No matching pooling circuit representation was found in the
inspected sources or targeted searches.

The theorem uses normalized quality alphabet
`{0,1/66,1/33,1/22,1/11,1/2,1}`, capacities in `{0,1,2,3,4}`, production
costs in `{0,1}`, and revenues in `{1,2}`. Since the remaining threshold is
linear in the number of nodes, unary encoding has polynomial size. The
strong-hardness conclusion is therefore supported by the output instance
encoding even though the initial Matsui family has large numbers.

This conclusion concerns **exact threshold attainment**. Small local
coefficients can still encode exponentially small differences in feasible
flows through long averaging chains. Strong NP-completeness here does not
by itself imply an inverse-polynomial objective gap, hardness under fixed
feasibility tolerances, or absence of an FPTAS for continuous objective
values. Such claims require a separate gap argument. Existing pooling
inapproximability results do not automatically supply that argument for
this class: the stable-set reduction used by Dey and Gupte has growing
quality dimension.
[Dey–Gupte primary preprint](https://optimization-online.org/wp-content/uploads/2013/04/3849.pdf),
Section 4.1, Theorem 2 and its reduction.

## Search scope and proposed attribution

The audit checked the primary sources above and searched combinations of
pooling with `one pool`, `one quality`, `two feeds`, `two inputs`, `bypass`,
`strongly NP-hard`, `constant data`, `bounded coefficients`, `arithmetic
circuits`, and `universality`, including searches for later work through
2026-09-05. Most newer hits concerned relaxations, numerical methods, or
different uses of the word pooling. No exact matching restricted theorem
or fixed-data blending circuit construction was found. This search is not
a complete forward-citation census.

Suggested claim after the mathematical audits:

> We prove strong NP-completeness for one-pool, one-quality pooling with
> two pool feeds and two pool outputs, bounded external-node degrees,
> zero lower flow bounds, and fixed finite local data. The proof encodes
> binary coefficients through the bypass topology. It strengthens and
> makes explicit a hardness boundary previously asserted by
> Baltean-Lugojan and Misener, and answers the fixed-quality bypass
> question stated by Haugland and Hendrix.

Avoid claiming the first one-pool hardness result, the first assertion of
one-pool/one-quality hardness, hardness with two total inputs, or hardness
with all node degrees at most two.
