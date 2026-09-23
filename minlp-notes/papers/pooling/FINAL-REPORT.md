# Pooling manuscript: final delivery, 9 September 2026

The revision of **The Complexity of Pooling: Algebraic Barriers and Structural Algorithms** is complete. The manuscript contains its essential proofs, identifies established external inputs, and distinguishes its original results from their closest antecedents. All accepted findings from the requested staged reviews are resolved. No mathematical gap in a claimed result remains identified by this process.

- [Final paper](main.pdf): 105 pages, including three proof appendices and 39 cited references.
- [Portable LaTeX source](pooling-latex-source.zip): 16 files, including a standalone build README.
- [Stage status](revision-20260909/STATUS.md), [whole-manuscript adjudication](revision-20260909/reports/whole-round1-adjudication.md), and [root final audit](revision-20260909/reports/root-whole.md).

The paper is anonymous. Author names, affiliations and journal-specific submission metadata have not been invented. It has not been submitted or published.

## What changed

The introduction now leads with existential-real completeness and its consequences for exact certificates. It then explains the restricted physical hardness boundaries and structural and contract algorithms. A comparison table states the simultaneous restrictions, decision or objective scope, and relevant theorem. The synthesis explains why these distinctions matter for formulation and algorithm design. A new dependency table separates the three physical copy-construction routes, and reading guidance makes the long manuscript easier to navigate.

The work went beyond presentation. The structural proofs now account explicitly for singular bases, lower-dimensional parameter conditions, sequential redundancy deletion, and polynomial coefficient bit length in algebraic recovery. The parameterized path arguments include endpoint singletons and degenerate slices. Physical reductions, contract conservation identities, objective scope, finite-data encodings and witness representations were critically checked throughout the author stages and reviews.

Three appendices make the secondary results self-contained. Appendix A proves the physical response and optimum-geometry constructions. Appendix B includes the general-cost rank-one margin hardness reduction, the zero-lower/unit-upper refinement, exact certificates and fixed-interaction-rank algorithms. Appendix C includes the correlation-polytope face, quantitative rounding and slice estimates, and exact and uniform approximate conic size transfers. Five substantive companion-note results were incorporated with complete arguments. Eight tangential comparisons were removed; their repository notes remain unchanged. The manuscript no longer relies on thirteen unpublished companion-note citations. Their disposition is recorded in [source-index.md](source-index.md).

## Literature and contribution claims

The review used the local literature archive and targeted searches for primary papers, author manuscripts and publisher versions. Source-specific comparisons appear near the results they support. Version-sensitive theorem locators were checked against the original PDFs rather than inferred from repository metadata.

The paper credits Xiang et al. for the existing product-LP zero-optimum test, including pool-to-pool arcs. It credits prior broad capacitated one-pool hardness and states the additional simultaneous restrictions proved here. It identifies precisely the Dey–Kocuk–Santana general-cost margin conjecture resolved in Appendix B, and distinguishes that linear margin problem from earlier rank-one biclique approximation results. The exponential exact SOC representation of Jalilian–Kocuk is explicitly compatible with the manuscript's size lower bounds. Established shadow geometry, fixed-rank box methods, margin patterns, and extension-complexity machinery receive explicit credit; the physical realizations and margin transfers are identified separately.

The strongest priority statement is qualified by “To the best of our knowledge” and scoped to the specified pooling classes. No first sign algorithm, first broad one-pool hardness result, polynomial exact SOC hull, or full-pooling consequence from an isolated arbitrary-cost matrix block is claimed. The search is substantive but does not establish exhaustive priority certification.

One local item labeled Dey–Gupte is presentation slides; the article comparison was checked against the actual author manuscript and its electronic companion. Published and preprint versions of other sources sometimes have different theorem numbers or page counts. The bibliography records the inspected versions, and [the internal version manifest](revision-20260909/primary-source-versions.json) preserves hashes for the two conic sources with multiple local/author versions. Detailed evidence is in [the literature audit](revision-20260909/reports/root-literature.md), the stage reports, and the five complete whole-manuscript review reports.

## Review and verification

This revision completed the requested process in four development stages followed by one whole-manuscript stage. Each development author finished before five independent reviewers examined the stage. Root read and adjudicated their findings. A different correction agent then addressed all accepted items, including minor ones, and root verified the repairs before advancing. The completed manuscript received five fresh independent reviews covering every section, appendix and proof, followed by a separate correction pass.

The total for this revision is **25 independent reviews and five separate correction passes**. No review round produced an accepted major issue requiring another five-reviewer round. All accepted minor findings were corrected. The historical report and older review records are preserved as historical evidence; their review counts are not attributed to this revision.

Mathematical review was supported by distinct exact and numerical checks of physical networks, copy gadgets, orientation modes, cut signs, path projections, algebraic identities, margin penalties, cost optimizers and face-rounding estimates. For example, the appendix author checks include 4,482 exact physical cases, 2,000 rational penalty cases, and all equal-total quarter-grid margin pairs for one and two paired indices. Reports distinguish exact arithmetic from floating-point LP comparisons. These finite checks supplement the general proofs and do not certify external theorems or asymptotic complexity.

The final editorial pass preserved all mathematical expressions and all 92 theorem/lemma/proposition/corollary statements, three examples, two remarks and 93 proofs; formal prose changes were limited to physical-node terminology and article agreement. Root inspected the complete final diff and the new table against its cited proof dependencies. Layout checks covered the complete reviewed draft and 43 affected or adjacent pages after the final editorial changes, with additional readable-scale root inspection of the front matter, new table, algorithm guide and bibliography.

## Reproducible delivery

The source ZIP contains only `main.tex`, `bibliography.bib`, seven section sources, three appendix sources, three native figure sources and `README.md`. It contains no literature PDFs, internal reviews, old auxiliary files or verification dependencies. Root extracted it into an empty directory and ran its documented command:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The independent build produces 105 pages with zero LaTeX/BibTeX warnings, undefined references or citations, duplicate labels, or overfull/underfull boxes. All 39 bibliography entries are cited and all 273 source labels resolve. Its extracted text matches the reviewed corrected PDF. The delivered `main.pdf` comes from this source-archive build.

[Final validation](revision-20260909/checks/final-package-build/validation.json) records file hashes and checks; the [retained verification script](revision-20260909/checks/final-package-build/verify_delivery.py) checks the archive against the manuscript sources. The accepted source is frozen in `revision-20260909/whole-accepted/`.

The explicit remaining classification question concerns degree-two bypasses with unbounded pool attachments under the stated fixed-parameter and interval assumptions. It is outside the proved classification; no claimed theorem depends on resolving it. Internal review is not external peer review or formal proof certification, and the completed revision does not imply journal acceptance.
