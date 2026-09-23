# Stage 1 author record

Date: 2026-09-05. Author stage complete and ready for the coordinator's 15 independent reviewers. This record reports author verification, not completed independent review.

## Artifacts and build

- `main.tex`: provisional title, accurate current abstract and introduction, complete current input list.
- `macros.tex`: shared packages, theorem environments, notation contract.
- `sections/01-foundations.tex`: probability/envelope foundations and the signed bilinear density chapter (two numbered sections following the introduction).
- `references.bib`: paper-local bibliography; no generated literature file was edited.
- `build/main.pdf`: 10-page compilable current manuscript.
- `process/scope-proposal.md`: comprehensive core claim/source inventory and six-stage outline.

Command: `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` from this paper folder. Build passed; all references and citations resolved. The final LaTeX log has no overfull, underfull, undefined-reference, or package-warning entries. A first shell redirection used a wrong relative directory and failed before writing the section; the corrected command wrote the complete file and rebuilt successfully. That failed preliminary build is not the verification result.

## Claims written and checked

1. Compact scalar graph-hull vertical sections and specified factorwise gap; explicit distinction between exact monomial convexification and recursive McCormick products.
2. Vertex-distribution envelope lemma, attainment and continuous piecewise-affine boundary behavior; full elementary proof.
3. Exact single-product unit-cube envelopes with explicit consecutive failure intervals on a circle; compatible common upper attainment for positive sums.
4. Deficiency representation, independent rounding for easy support classes, and correct positive expansion comparison on nonnegative boxes. Domain scaling does not silently preserve factor incidence.
5. A precise region-certificate definition and normalized relative-gap convention, without claiming any spatial theorem before its writing stage.
6. Exact induced-subgraph cut characterization with a self-contained half-integral cell argument, including outside fixed-one coordinates and zero-support conventions. This fills in the reference-only convexity step in the result notes.
7. Exact polarization identity; sharp Khinchin row estimate; local squared-weight cut giving the 1/4 sum-of-row-norm bound.
8. Fractional-orientation existence/minimality via an explicit max-flow proof; density 4 sqrt(rho), degeneracy 4 sqrt(d), maximum degree 2 sqrt(Delta), and sharp bipartite sqrt(2 min Delta) bounds.
9. Distinct direct degeneracy coloring proof.
10. Finite random-sign lower on each graph; exposing a densest induced face; whole-center supremum equality; nonzero-support perturbation handled without assuming continuity of c* across disappearing coefficients.
11. Graph-family, density/degeneracy/arboricity, average-density, scale-invariance, coefficient-sensitive, planar/series-parallel/complete-bipartite corollaries; scope limited to scalar vertical gaps.
12. Classical positive-bilinear coloring bound, factor-two limiting family, and full signed-cycle exactness proof.
13. Exact density constant left in [2,4] and degeneracy constant in [sqrt(2),4]; finite versus growing-parameter distinction retained.
14. Complete Schur-to-cut transfer with explicit real projective norm, correct weighted source theorem, rectangle/induced density equality, and Sidon comparison. Older density order is explicitly credited.

## Fresh source checks

Read the complete two canonical bilinear result files and their actual proof chains. Read the relevant local primary fulltexts, not only their package summaries. Important source formulas were also checked in rendered original PDF pages; those images are retained in `process/source-checks/`.

- Luedtke–Namazifar–Linderoth: local package `luedtke2012-some-results-on-the-strength`, fulltext pp. 5–9, 15–17 as relevant; original p. 9 rendered and inspected for the positive affine-expansion argument. Theorem numbers 4, 5, and 8 in the manuscript explicitly refer to the authors' technical report version, whose numbering differs from the published article. Published metadata: Mathematical Programming 136(2), 325–351 (2012), DOI 10.1007/s10107-012-0606-z.
- Boland–Dey–Kalinowski–Molinaro–Rigterink: local package `boland2017-bounding-the-gap-between-the`, fulltext pp. 3–6 and 10–11; original PDF p. 6 inspected for Corollary 1 and its preceding gap identity. Complete cut characterization is proved in our text, rather than delegated to the source. Published volume/pages independently corroborated through Crossref: 162(1–2), 523–535, journal issue year 2017 (online-first date is 2016), DOI 10.1007/s10107-016-1031-5.
- Davidson–Donsig: local package `davidson2007-norms-of-schur-multipliers`, fulltext pp. 3–7; original pp. 6–7 rendered and inspected. Theorem 2.4, not the integer-rounded Theorem 2.3, gives Schur norm <=2 sqrt(beta). Theorem 1.2 supplies the real Grothendieck/projective comparison. Metadata is 51(3), 2007, DOI 10.1215/ijm/1258131101. The local package and Crossref do not give pages; an author publication page says 785–807, whereas bibliographies elsewhere say 743–766. Pages were therefore omitted rather than guessed. The final reference audit should resolve this small bibliographic discrepancy from the published original if available.
- Szarek's sharp Khinchin inequality is an explicit established input, not reproved. Publisher metadata verified at https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/all/58/2/101277/on-the-best-constants-in-the-khinchin-inequality : Studia Mathematica 58(2), 197–208 (1976), DOI 10.4064/sm-58-2-197-208. The publisher PDF download returned an access failure in the web screenshot tool; no access controls were bypassed. The exact theorem and 1/sqrt(2) constant were independently verified in the primary research article Eskenazis–Nayar–Tkocz, *Distributional stability of the Szarek and Ball inequalities*, arXiv:2301.09380v2, introduction equation (1), https://arxiv.org/html/2301.09380v2 . The original theorem is cited in the manuscript; the access limitation is confined to this audit record.
- McCormick's 1976 article metadata and existing local primary source record were checked. It is cited only for the historical recursive relaxation mechanism. Its user-supplied original has not been copied into the paper directory.

Established inputs intentionally not re-proved: sharp real Khinchin inequality, max-flow/min-cut, and the two Schur-multiplier norm theorems. Every claimed bilinear gap consequence and every envelope/compatibility lemma is proved in the paper. No novelty claim is made for standard envelope facts, positive-bilinear/cycle results, norm inequalities, or the general density order.

## Bounded attempt on the remaining density constant

I examined whether the local squared-weight cut and fractional-orientation proof could directly improve 4 to 2. Its certified steps are

`R >= max(X,Y)/sqrt(2) >= (X+Y)/(2sqrt(2)) >= (sum_i ||a_i||_2)/4`,

followed by `L <= sqrt(rho) sum_i ||a_i||_2`.

The Khinchin constant is sharp for two equal coefficients. The passage from max(X,Y) to half their sum is sharp for balanced sides. The local cut certificate guarantees only half each vertex's squared incident weight crosses. A fractional orientation controls unweighted loads, but does not guarantee that the retained weighted square mass at each vertex is at most half its full row norm. In a star, leaves carry almost all edge load in a low-load orientation and their weighted square fractions can approach one. Thus the tempting uniform half-square-mass replacement is false. Replacing max by a sum or replacing these fractions by 1/2 would be an unjustified improvement. These losses might not be simultaneously extremal for the final ratio, so this is a limitation of the checked chain, not proof that the constant four is optimal. No new universal constant was established.

The full cell proof, explicit cut exactness proof, and careful continuous Schur transfer are concrete completed developments of previously compressed dependencies. The true best density constant remains open and is not needed for the validity of any stage-1 theorem.

## Verification and pending review

The coordinator independently reran the repository's exact cut-identity checker and reports it passed. Its coverage includes polarization, row/local-cut and density inequalities. The coordinator also independently checked the half-integral cell argument. These are supporting checks; the required 15-agent review gate has not yet run.

No mathematical defect remains known to the author. Review attention should focus on: the cell's half-integral vertex proof; distinction between coefficient/full-support suprema; real-versus-complex norm conventions in the Schur transfer; the sharp Khinchin dependency; and whether the explanatory gap/oracle distinctions are clear for nonlinear-optimization readers. Later-stage claims are not asserted in this initial draft.
