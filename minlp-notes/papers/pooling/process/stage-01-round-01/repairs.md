# Stage 1, round 1 repairs

A separate correction agent implemented the root's accepted findings after reading the adjudication, the relevant review reports, and the complete foundations section. Only `sections/01-foundations.tex` and `bibliography.bib` were edited, apart from this record and the requested compilation artifacts. Historical snapshots and reviews were left unchanged.

## Changes

1. **M1, endpoint quality scope:** The endpoint specialization now requires that product quality restrictions consist only of coordinate upper bounds in `{0,1}`, with no additional nonredundant quality restrictions. The text expressly retains lower flow bounds. This hypothesis governs the disjunction, branch enumeration, MILP and certificate conclusions that follow. The existing full proof is preserved.
2. **Effective finite flow bounds:** The model conventions now require a finite rational effective upper bound on every arc in every capacitated model, either directly or through node capacities. The expressly uncapacitated sets are exempt. The compactness paragraph puts finite flow bounds before its bounded-lift assertion. The facial-integrality proof uses the sum of effective arc upper bounds for the return arc when source upper bounds are not supplied.
3. **Scaling before reconstruction:** The shortest-path converse now routes the mixture, scales to every capacity, and only then invokes the capacitated single-product lemma. The scale is explicitly `min({1} union {U_r/a_r : a_r > 0})`, with capacity row loads `a_r`; zero-load rows are excluded. Positivity and polynomial rational encoding are retained.
4. **Absorption conventions:** Before the cyclic component formula on the whole arc set, the proof sets absorption fractions to zero on removed circulation components and inactive pools, and gives their Kronecker values at products.
5. **Demand notation:** Exact product demand is now the scalar `d_j`, with `t_j=d_j` and `m_j=d_j B_j`; `b_j` remains the polyhedral right-hand-side vector.
6. **Dual-cone direction:** The text states that profitable flow corresponds to cost-vector nonmembership in the dual cone, and membership means absence of profitable flow.
7. **Bibliography:** Corrected the given names to Akshay Gupte and Myun-Seok Cheon. All four entries now have separate journal, volume, number and page fields, using BibTeX double hyphens for ranges. The records are Boland–Kalinowski–Rigterink, `66(4):669–710`; Dey–Gupte, `63(2):412–427`; Dey–Kocuk–Santana, `77(2):227–272`; and Gupte–Ahmed–Dey–Cheon, `67(3):631–669`.

## Verification

The endpoint counterexample in the reviews has a nonredundant lower quality bound, so it is outside the corrected specialization. Within the corrected scope, zero upper quality requires each positive contribution to have zero quality in that coordinate; upper quality one accepts every mixture. This rechecks both directions of the disjunction and the bound on both sums by pool throughput, including zero flow. Lower flow bounds remain ordinary constraints in each support branch.

The reordered path construction satisfies all hypotheses of the cited reconstruction lemma. Every positive capacity-row load is scaled below its strictly positive retained bound; rows with zero load already satisfy their upper bound. The cyclic component formula is now defined for every possible arc head. The demand and dual-cone corrections change notation and answer direction without altering any displayed result.

Publication data were checked against the [Boland publisher record](https://link.springer.com/article/10.1007/s10898-016-0404-x), [Dey–Gupte publisher record](https://pubsonline.informs.org/doi/10.1287/opre.2015.1357), [Dey–Kocuk–Santana publisher record](https://link.springer.com/article/10.1007/s10898-019-00844-4), and [Gupte and coauthors publisher record](https://link.springer.com/article/10.1007/s10898-016-0434-4), together with the publisher-deposited Crossref records for these DOIs. The latter confirmed all four issue numbers. The local Gupte article title page independently confirms the corrected given names and the existing author order. The spelling Myun-Seok is also used on the [author-posted Optimization Online record](https://optimization-online.org/2015/04/4883/).

Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in `papers/pooling`. It completed with exit status zero and produced `main.pdf`, 11 pages, 334787 bytes. The final `main.log` and `main.blg` contain no warnings, undefined references, errors, overfull boxes, or underfull boxes. `git diff --check` also returned zero. These are compilation and local repair checks; they do not replace the next full mathematical review.

## Freeze for the next review round

No further edits are planned by this correction agent. Corrected file SHA-256 values:

- `sections/01-foundations.tex`: `999fa47848161c0c3b75611ce69389fc8ce36eb144d7bdb6b9609ee7388e1db2`
- `bibliography.bib`: `a7d23306b23d21acf15ac8c89eee661ea248d9b595dc3d0517254007012d86e4`

The root's required second round of 15 reviews remains pending. No later writing stage was started.
