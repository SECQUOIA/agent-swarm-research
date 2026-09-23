# Stage 5 author handoff: synthesis and complete draft

Status: complete author draft, ready for the prescribed five independent Stage 5 reviewers. The later whole-manuscript five-reviewer cycle remains separate and has not been declared complete.

## Manuscript presentation

The manuscript title is **Finite reservoirs at phase coexistence: full-state accuracy and phase correlations**. No authors or affiliations have been invented.

Added sections/introduction.tex, sections/numerics.tex, and sections/conclusions.tex. The abstract now covers the sharp support and two-phase criteria, both microscopic realizations, physical boundary optimization, and the shared-bath full-state/information result. A compact introduction table distinguishes the physical N, N^(3/2), and N² requirements and names the actual hypotheses.

The main route is physical framework, sharp criteria, microscopic realizations, shared baths, smooth/physical boundary laws, deterministic illustrations, and discussion. The detailed short-range contour proof is Appendix A; exact Gaussian geometry is Appendix B; capillarity and accuracy diagnostics are Appendix C. All proofs remain in the same PDF.

The short-range proof was moved intact except for heading levels and a short appendix introduction. I reconstructed the original microscopic section by removing the new main-text proof guide, returning the appendix material, and changing its subsection headings back to subsubsections. Its SHA-256 exactly matches the Stage 2 round-2 frozen file:

    4f6cfab2a45063487df9a706731ca9a670f7231f4825410a72c518e3c9061fe2

This verifies that the accepted microscopic mathematics was not silently changed during relocation. The Gaussian and capillarity sections were moved through main.tex input order rather than copied or rewritten. Their stable labels remain available. One capillarity forward pointer was updated to its appendix reference; the Gaussian contact-set paragraph gained literature attribution.

## Literature and physical interpretation

The introduction distinguishes the work from established:

- finite power-law reservoirs and Gaussian ensembles;
- two-Gaussian coexistence descriptions and their incorrect microscopic valley scale;
- energy-range-squared strong-distance sufficient bath bounds;
- growing-block conditioning in regular exponential families;
- physical finite-bath Potts comparisons using optimized comparison temperature and histogram Euclidean norms;
- generalized and squeezed ensembles used for macrostate/entropy reconstruction or selected coexistence states;
- ensemble-dependent correlations, opposite-phase locking, and phase contributions to shared information;
- supporting-quadratic and Delaunay geometry and exponential-family face closures.

The narrower contribution is stated as exact optimized full-state asymptotics for the prescribed canonical target, with separate necessity, positive-tail sufficiency, and verified microscopic input. No claim that these general mechanisms were discovered here is made. No claim of exhaustive historical priority is made.

refs.bib is complete for all cited keys. The plainurl style prints clickable primary URLs and DOI links. Main source additions and verification:

| Source | Verification and use |
|---|---|
| Challa–Hetherington 1988 PRA, DOI 10.1103/PhysRevA.38.6324 | Retained full primary text, metadata and page span 6324–6337; Gaussian reservoir and finite-size fluctuations. |
| Challa–Landau–Binder 1990, DOI 10.1080/01411599008210236 | Publisher abstract inspected; Phase Transitions 24–26, 343–369. Full text remains unavailable. Only its stated review scope is used; no exhaustive comparison of its derivations is asserted. |
| Campisi 2007, DOI 10.1016/j.physleta.2007.01.082 | Retained primary preprint and earlier source audit; finite-capacity power-law setting. |
| Riera–Gogolin–Eisert 2012, DOI 10.1103/PhysRevLett.108.080402 | Retained primary Appendix A/B entropy-remainder and squared-range bound; arXiv journal record checked. |
| Diaconis–Freedman 1988, DOI 10.1007/BF01048727 | Berkeley primary report and repository metadata checked; regular growing-block conditional variation results. |
| Griffin–Matty–Swendsen 2017, DOI 10.1016/j.physa.2017.04.143 | Coordinator independently read retained primary Eq.23 and Section VI: Euclidean energy-probability distance and optimized comparison temperature. Direct Potts precedent is acknowledged. |
| Costeniuc–Ellis–Touchette 2006, DOI 10.1103/PhysRevE.74.010105 | Retained primary text and arXiv journal metadata; nonconcave entropy via Gaussian ensemble. |
| Costeniuc–Ellis–Touchette–Turkington 2005, DOI 10.1007/s10955-005-4407-0 | Retained primary text and arXiv journal record; generalized ensemble and macrostate equivalence. |
| Yoneta–Shimizu 2019, DOI 10.1103/PhysRevB.99.144105 | Coordinator primary reading and author metadata check; selected first-order states and finite-size conversions. |
| Lebowitz–Percus–Verlet 1967, DOI 10.1103/PhysRev.153.250 | Retained primary text; ensemble-dependent fluctuations and correlations. |
| Cohen–Rittenberg–Sadhu 2015, DOI 10.1088/1751-8113/48/5/055002 | Retained primary text, earlier Section 4.3 audit, and arXiv journal record; shared information and degeneracy. |
| Mishin 2015, DOI 10.1016/j.aop.2015.09.015 | Coordinator inspected primary Section 10; single-phase finite-reservoir covariance corrections. |
| Corti–Ohadi–Fariello–Uline 2023, DOI 10.1021/acs.jpcb.3c00455 | Local open paper package and institutional primary record; finite ideal-gas contact and entropy conventions. The paper does not endorse a universal entropy-definition claim. |
| Edelsbrunner–Seidel 1986, DOI 10.1007/BF02187681 | Author-hosted primary PDF, institutional publication record and coordinator audit; classical Voronoi/Delaunay construction. |
| Csiszár–Matúš 2005, DOI 10.1214/009117904000000766 | Retained primary text and arXiv publication record; face-supported variation closures. The current proof does not require this theorem as an unverified black box. |

The new comparison text is supported by reviews/stage-5-coordinator-literature-audit.md. Literature/AGENTS.md was read; no literature knowledge-base file or generated index was edited.

## Reproduction bundle and figures

Added:

- code/potts_finite_bath.py: copy of the independently checked original exact algorithm, with standalone command-line/output controls.
- code/check_potts_finite_bath.py: explicit labeled-spin enumeration and independent density quadrature.
- code/make_figures.py: standard Matplotlib plots using archived sums and proved formulas.
- data/potts-finite-bath-results.json: unchanged 18-point archival data, including two N=12000 boundary points.
- data/potts-original-independent-check-results.json: retained earlier independent checks.
- data/potts-independent-check-results.json and data/potts-recomputed.json: fresh small checks and N=300 recomputation.
- data/figure-derived-values.json and data/boundary-optimization.csv.
- figures/potts-scaling.pdf/.png and figures/boundary-optimization.pdf/.png.
- README.md and requirements.txt: build/setup, quick checks, optional full enumeration, data provenance/hash, numerical scope, and internal-review qualifications.

Figure 1 is exact mean-field spin–momentum TV from occupation sums and Gamma/Beta CDFs. Its dotted lines are the physical boundary limits. Figure 2 is an evaluation of a limiting formula for balanced equal-variance phases, not finite-size Potts data. Captions and reproduction instructions make that distinction explicit.

The archived large-N data were not needlessly recomputed. The standalone --all-archived option reproduces their exact size/regime plan to a separate output. N=300 was rerun in all four regimes and agrees with the archive within 1e-11. The algorithm reports spin-configuration marginal TV separately from full-state TV; the figure uses the latter. The historical JSON capacity field is documented as c=C_B/k_B in the surface-entropy convention.

## Coverage and status updates

COVERAGE.md now maps every relevant research note to stable manuscript theorem/equation labels, records strengthened and completed results, and gives precise reasons for exclusions.

Updated current repository README.md and research/results-summary.md. Added supersession notices to the earlier finite-bath, Gaussian-scouting, Potts benchmark, short-range route, and Markdown manuscript files. Corrected the original anisotropic effective metric/semidefinite remark and replaced the old unproved Gaussian optimal-loss claim with the completed proof link. Corrected the old implication that kinetics are required for the mean-field exponent. The short-range route explicitly identifies its former sufficiency gap as resolved and labels its old next-step analysis historical.

Historical independent review reports were not rewritten. Unrelated directions and literature generated indices were not touched. WORKFLOW.md remains coordinator-owned.

## Final validation

- All small labeled-spin enumeration and direct-density checks pass.
- All Stage 4 weighted-normal/physical compensation checks pass.
- The N=300 exact archival recomputation agrees in all four regimes.
- Figures regenerated from standalone code and visually inspected by author and coordinator.
- Representative PDF pages inspected: title/abstract/contents, result table, main mathematics/numerics transition, and bibliography.
- The relocated microscopic mathematics reconstructs exactly to the accepted SHA-256.
- git diff --check passes.
- Final build command: latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex, from this folder.
- Final PDF: **47 pages**, including the main text, three appendices, and references.
- Final log: no undefined references/citations, overfull/underfull boxes, or hyperref warnings.

No known author issue remains in the synthesis. Stage 5's five reviewers and the later whole-manuscript five reviewers must still complete the user's required process before the paper is declared finished.
