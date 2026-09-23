# Stage 4 author handoff

Stage 4 drafting is complete and awaiting the fifteen-reviewer gate. I was the sole author of this stage and used no delegated authors or reviewers. The root agent independently read the draft and source mathematics in parallel; that preliminary reading is not the requested independent review round.

## Files and coverage

Created `sections/04-vector.tex`, `abstract.tex`, `sections/00-introduction.tex`, and `sections/05-conclusion.tex`. Appended seven primary-source bibliography entries and completed all ten canonical and eleven substantive supporting stage 4 mappings in `coverage.md`. Root wired these files into `main.tex`. The accepted sections 01–03 and `macros.tex` were preserved byte-for-byte, verified against their accepted SHA-256 values.

The mathematical draft covers every canonical stage 4 result and the eleven explicitly identified supporting developments. I read the canonical mathematical sources and substantive supporting notes, reconstructed their arguments and constants, and used prior reviews as leads rather than certificates. Promoted notes were checked as pointers; source-comparison notes were inspected for close antecedents and scope qualifications. Earlier numerical versions of the same degree-32 construction are superseded by the exact product-count family; the distinct hinge geometry and Bernstein stability argument are retained.

The proof organization is:

1. Direct scalar level refinement; finite vector/facet overlay; deterministic ordering of approximate quantiles; exact implicit multiset order statistics, duplicates and metadata; compact convex-vector overlay.
2. Exact and rational approximate bases of original convex output rows; box and facet curvature-rank comparisons; weighted l1 specialization; the separate maximum-product-box transfer.
3. Effective nonlinear coordinates; a fixed-grid, exactly feasible rational spanner implementation; support optimization and positive-polar weak separation; explicit inner parallelotope bands and finite/compiled oracle-rank counts.
4. One common basis across every separable coordinate; original-vector product packing; all finite and compiled box, facet and oracle comparisons, including the finite +7n and +8n companions.
5. Positive-power failure of separate scalarizations and uniform refinement; thirds residues, cap sets and the direct arbitrary-label three-witness obstruction; exact convex product counts; hinge/Bernstein stability; nonconvex scalar degree gaps; arbitrary polynomial-vector compilation; tilted-body and fixed-conditioning comparisons; the remaining one-input box question.

## Mathematical reconstruction and refinements

The draft explicitly checks zero curvature/rank, affine-only inputs, singleton and repeated cells, unused codes, a common polynomial-bit denominator, directed rounding, simultaneous graph containment, effective-image rounding and all band sums. It maintains the paper's binary-linear meaning of `p_bin` and states when a lower bound extends to arbitrary convex binary lifts. Finite real-coefficient existence, dense/sparse encoding, rational construction and solving complexity are distinguished.

The rational spanner proof uses one predetermined output grid and repair weight throughout all determinant exchanges. Feasibility is proved by an inner-ball convex combination, and the resulting additive 1/4 support loss yields coefficient bound 9/4 (safely rounded to three in the graph theorem). The positive polar is accessed by a weak separator; approximate support is never called exact membership. Both effective primal and projected polar spanning seeds are explicit. The final formulation has only rational linear bands, with no oracle constraints.

The separable proof uses one concatenated output basis and compares its product packing with the original vector lift. Its exact capacity factors are 108r, 180r, 87480r, 157464r and 1277208r^2 for the stated finite/compiled cases. The finite conditioning proof was developed to state its valid nonsymmetric extension explicitly: only an outer bound for midpoint vectors and an inner ball for final errors are needed. The default error-body convention remains symmetric elsewhere. The distinct simplex-band Euclidean improvement and unconditional inner-crosspolytope normalization are retained even though the maximum-product theorem gives a stronger dimension-only unconditional count.

Root's preliminary suggestions led to an explicit input-box normalization before the introductory covariance program, complete bibliographic page ranges, and correction of stale stage 3 awaiting-review coverage suffixes. These are pre-freeze author revisions, not post-review corrections.

## Primary sources checked

I directly read the relevant primary passages below. This is a bounded source assessment, not an exhaustive priority search or a claim to have audited every proof in every cited paper.

- Awerbuch–Kleinberg, STOC 2004 author manuscript: Section 2.3, Propositions 2.2/2.4, Observation 2.3, Figure 2 and determinant-exchange argument. Primary manuscript: `https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf`. The primary author publications page `https://www.cs.cornell.edu/~rdk/pubs_topic.html` confirms proceedings pages **45–53**; the PDF filename `p20` is not pagination.
- Ellenberg–Gijswijt: primary arXiv 1605.09223, Theorem 4 and its proof on printed pp.2–3, plus Corollary 5. Publisher metadata at `https://annals.math.princeton.edu/2017/185-1/p08` confirms Annals 185(1):339–343 (2017), DOI 10.4007/annals.2017.185.1.8. The cap-set theorem is imported; the graph-contact residue reduction is proved in the manuscript.
- Lyu–Hicks–Huchette: local primary manuscript Section 3, Proposition 1 and following shared-SOS2 discussion, with root's regenerated primary text available in `build/source-cache/lyu2026.txt`. Publisher page `https://pubsonline.informs.org/doi/10.1287/opre.2023.0187` and local checked metadata identify Operations Research 74(1):484–499 (2026). The cited proposition is the numbering of the checked manuscript.
- Kelly–Maulloo–Tan: primary PDF cached by root as `build/source-cache/kelly1998.txt`, Section 2, Eq.(1) and its equivalence to unit-weight log-utility maximization; Eq.(2) gives the weighted form. Cambridge's endpoint failed, while the Stanford-hosted primary copy was available. Publisher metadata verifies JORS 49(3):237–252 (1998), DOI 10.1057/palgrave.jors.2600523.
- Plevrakis–Hazan: primary arXiv 2010.13178v2, Section 3.2 pp.8–9, explicitly using separation, ellipsoid approximate optimization and a constant approximate spanner. Cache `build/source-cache/plevrakis2020.txt`. This is credited as a close predecessor, not merely general background.
- Grötschel–Lovász–Schrijver: accepted primary weak-optimization interface, with direct additional reading of the cached polar and anti-blocker Corollaries (3.4)–(3.5), printed pp.178–179. These establish the preexisting positive-polar access principle; the draft gives its required rational repair/interface.
- Hartman: primary publisher PDF `https://msp.org/pjm/1959/9-3/pjm-v9-n3-p09-p.pdf`, introduction on p.707 and local/global difference-of-convex statements on pp.707–708. The last article page in the primary text is 713, so the bibliography uses 707–713. Only the general classical framework is attributed, while the quadratic convexification used here is proved directly.
- Averkov–Weismantel: primary arXiv 1002.0948v2, Theorem 1.1 Eq.(3) on p.2, surrounding Helly definition and Radon discussion. The primary author department list `https://www.b-tu.de/fg-algorithmische-mathematik/publikationen-alt/2012` confirms Advances in Geometry 12(1):**19–28** (2012), DOI 10.1515/advgeom.2011.028. Publisher search extracts attached an unrelated 43–61 page range to a neighboring issue entry; it was not used.

Established shared-breakpoint formulations, scalar segmentation, Boolean compilation, spanners, approximate-oracle exchange, polar equivalences, proportional fairness, Bernstein approximation, difference-of-convex geometry, parity and cap-set estimates are credited as such. No claim of a new general oracle, selection, spanner, coding or approximation primitive is made.

## Checks and build

The root's nine selected stage 4 supplementary scripts all passed; their immutable script hashes, individual output paths and limitations are in `verification/stage4-20260905T194349Z/manifest.json`. These exercise overlays, shared output bases, effective bands, mixed coordinates, exact box gaps, nonconvex encoding and rational spanners. They do not establish universal proofs or independently verify the imported GLS theorem.

I also performed an independent exact enumeration of all 522 subsets of F_3^p for p=0,1,2. The maximum cap sizes are 1,2,4 (2,7,172 cap sets including the empty set). Exact integer arithmetic checked the five displayed separable capacity constants against their power-of-two bounds. The results and limited scope are recorded in `verification/stage4-author-exact-checks.json`; these small cases do not prove the general cap-set theorem.

After root integration, `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` succeeds. The final build is **84 pages**. `verification/check_manuscript.py` reports **258 labels, 39 bibliography entries, no duplicate labels/keys and no unresolved references/citations**. The final log contains no Warning, Overfull, Underfull or undefined matches. The introductory result table was changed to ragged-right columns to remove underfull paragraph warnings.

I rendered and visually inspected every stage 4 mathematical page (64–80), the title/abstract page 1, introduction/result-map pages 4–5, the stage transition on page 63, conclusion/references page 81 and bibliography end page 84. The pages have legible formulas, complete bands/tables, consistent numbering and no visible clipping or overlapping text. This is a visual inspection of those pages, not an image-level audit of every page inherited from earlier stages. Images are ignored build artifacts named `build/stage4-page-N.png`. The root retains whole-paper review and final PDF audit responsibility.

## Limits and handoff

The one-input constant additive box-gap question, necessity of the logarithmic curvature-rank penalties, general mixed-coordinate vector construction, and smooth rank-changing boundaries remain explicitly open. Finite box counts do not claim a compact optimal-count binary construction. Dense vector evaluation is not promoted to sparse huge-degree complexity. The tilted example is not a fixed or uniformly conditioned error-body separation. No external peer review, formal proof verification, solver guarantee or guaranteed journal acceptance is claimed.

Final source and PDF hashes are in `verification/stage4-author-hashes.json`. The author stops editing at this handoff so the root can freeze the complete stage for fifteen independent reviewers.
