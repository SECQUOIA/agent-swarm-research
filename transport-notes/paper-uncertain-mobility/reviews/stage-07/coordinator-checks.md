# Coordinator checks: Stage 07

Date: 2026-09-07. Stage 06 accepted before assignment of sole author paper_stage7_author. Read all historical uncertainty prior-art notes and manuscript bibliography; historical unresolved-X1/X2/finite-bulk comments in those notes are superseded by the accepted paper proofs. No literature package was modified.

## Independent primary-source audit

- Dill and Brenner, *A general theory of Taylor dispersion phenomena: III. Surface transport*, JCIS 85(1), 101–117 (1982), DOI [10.1016/0021-9797(82)90239-9](https://doi.org/10.1016/0021-9797(82)90239-9). Publisher abstract and metadata inspected. Surface adsorption, diffusion and convection in generalized Taylor dispersion are established. Full text not retrieved; do not infer absence of particular formulas from the abstract.
- Levesque, Bénichou, Voituriez and Rotenberg, [arXiv1211.5224](https://arxiv.org/pdf/1211.5224), PRE 86, 036316 (2012), DOI 10.1103/PhysRevE.86.036316. Independently read full-PDF pp. 1–3, equations 3–12: constant exchange rates, stationary transverse state, covariance/pseudo-Green formula, and additive kinetic/bulk stationary dispersion. These are direct physical precedents. The PDF's generated 2018 date does not change its 2012 publication year. No random spatial killing/mobility budget result occurs in the inspected model.
- Alexandre, Guérin and Dean, [arXiv2105.06212v2](https://arxiv.org/pdf/2105.06212), Physics of Fluids 33, 082004 (2021), DOI 10.1063/5.0057584. Read pp. 1–5, equations 5–15. General transverse diffusivity, wall interaction potential and flow yield an equilibrium current-integral formula for longitudinal dispersion, with finite-time correction. This supports the broad physical motivation; it is not an uncertainty-dependent mobility-budget optimization.
- Buttazzo and **Maestre**, [arXiv1002.2770](https://arxiv.org/abs/1002.2770): original author metadata confirmed; an assignment typo Maiale was explicitly corrected. The random-forcing conductivity-design framework is already recorded and inspected in earlier-stage notes.
- Alphonse, Kunštek and Vrdoljak, [arXiv2602.19869v1](https://arxiv.org/html/2602.19869v1): independently read introduction and equations 1–2. Two fixed strictly positive conductivities are mixed under uncertain forcing; generalized risk objectives and relaxed existence/stationarity are established there. These assumptions differ from the present zero-baseline unbounded mobility and random vanishing reaction field.

For relevance to the original intended reader, Purdue's [faculty profile](https://engineering.purdue.edu/ChE/people/ptFaculty/ptProfile?group_id=3905&resource_id=169352) and [2025–26 project description](https://engineering.purdue.edu/Engr/Research/GilbrethFellowships/ResearchProposals/2025-26/particles-polymers-and-compliant-boundaries-at-the-intersection-of-fluid-mechanics-and-soft-matter-) explicitly cover particle transport, fluid mechanics and interfacial phenomena. This supports scope suitability; no authorship, endorsement or experimental validation is inferred. These personal/context sources need not be cited in the scientific manuscript.

- Yüksel and Linder publisher metadata verified: SICON 50(2), 864–887 (2012), DOI 10.1137/100808976. Observation-channel optimization is established.
- Saldi, Yüksel and Linder, [author-hosted published PDF](https://mast.queensu.ca/~linder/pdf/SaYuLi17.pdf), IEEE TAC 62(5), 2360–2373 (2017), DOI 10.1109/TAC.2016.2613902. Independently read printed 2360–2364, including Theorem 4 and Assumption 2. The paper proves quantized-policy approximation and includes unbounded costs under extra continuity and integrability hypotheses. Do not describe it as bounded-cost-only. Its result does not supply the current uniform vanishing-budget PDE law; here some individual design/offset pairs have infinite cost.
- Conti, Held, Pach, Rumpf and Schultz, [publisher record](https://epubs.siam.org/doi/10.1137/070702059), SIOPT 19(4), 1610–1632 (2009), DOI 10.1137/070702059. Publisher abstract and metadata read; combines two-stage stochastic programming and shape optimization under random loading. Full-text access remains limited, so specific uninspected theorem exclusions are not asserted.

## Numerical-method checks before the new driver

Read the existing `scripts/check_uncertain_center_design.py` and `check_risk_sensitive_design.py` in full. For center masses p on the unit simplex, the face operator coefficient is p/h³, and differentiating the discrete inverse objective yields minus the averaged squared face gradient. The tangent gap `g·p−min(g)` therefore gives the discrete convex lower value `F(p)−gap`. This requires actual feasibility of the returned masses. Numerical floating-point evaluation is not an interval-verified certificate and does not enclose the continuum optimum.

The exact averaged exterior reciprocal response for zero mobility outside [-L,L] is `2/eta log((L+eta/2)/(L−eta/2))`, tending to 2/L at eta = 0; direct integration verifies the formula. Domain refinement still matters because optimization over that supported coefficient family restricts the continuum class. Existing eta = 0 finite-volume values slightly below Cpl are a concrete reason not to interpret a discrete tangent bracket as a continuum bracket.

The sole author independently found that the existing circle face samples do not impose exactly identical discrete masses. New comparisons will normalize sampled face fields to the same discrete budget and disclose the normalization. The root communicated the feasibility/roundoff and continuum-bound cautions before numerical text was written.

## Additional novelty searches and exclusions

Searches on 2026-09-07 included `optimal fin internal heat generation variable heat transfer coefficient constant slope profile`, `quadratic heat generation optimal fin thickness`, `random killing optimal diffusivity`, `vanishing reaction conductivity optimal design`, `compliance small mass reaction optimization`, and `moment 8/5 dispersion optimization`. No direct match to the specified moment or resolution theorem emerged. This is a limited search result, not proof of global originality.

Primary abstracts identify substantial older fin work with internal generation and variable heat-transfer coefficients (e.g. DOI 10.1016/S0017-9310(02)00189-8 and DOI 10.1016/0017-9310(87)90178-5). These were inspected only at abstract/introduction level; full-text exclusions remain unverified. Marck, Nadin and Privat [arXiv1310.2214v2](https://arxiv.org/abs/1310.2214) prove nonexistence and optimal-value results for geometrically coupled fin conductivity/loss and inlet heat flux under volume/surface constraints; abstract read. This reinforces the need to credit the broader conduction-with-loss optimization literature rather than call the general mechanism new. The current exact quadratic example is only one ingredient of the paper.

A recent adjacent result is Nickl and Seizilles, [arXiv2503.14978v3](https://arxiv.org/abs/2503.14978), last revised 2026-08-06. Its primary abstract concerns inference of unknown diffusivity from binding/killing locations through a Schrödinger inverse problem. It does not address the prescribed quantizer followed by spatial mobility design studied here. It is a screening lead, not a source used for a scientific claim or an alleged full-text comparison.

## Independent numerical and model cross-checks

The current author center objective was independently checked using a dense incidence-matrix assembly at n37,eta2,L7,nq16 and a nonsymmetric positive simplex coefficient. Relative objective discrepancy was 2.22e-16; maximum linear residual 8.88e-16; directional finite-difference gradient discrepancy 3.96e-10. Detailed values are in `coordinator-numerical-checks.json`. Twenty feasible sampled comparison points obeyed the tangent lower bound; the analytic convexity proof, not that sampling, establishes its discrete scope.

Re-read the entire accepted model/transfer section during synthesis. The physical coefficient is derived from stationary displacement before using the form supremum; the energy-space finite-response Schur identity does not require an L2 corrector; positive-background mixtures preserve the exact budget and observation. Units, nonzero V, connected one-dimensional wall and fixed positive bulk diffusion must remain in any overview of the optimized transport laws. No new defect found.

## Complete-draft visual inspection

After the Stage 07 author stopped, the coordinator rendered every page of the 54-page PDF with `pdftoppm -r 72 -png main.pdf /tmp/transport-paper-page`. All 54 pages were visually inspected in nine six-page sheets, with the two figure PDFs also inspected separately at higher resolution. No clipped text, equation-number collision, overlapping elements, blank pages, missing glyphs, or broken figure/table layout was found. The manuscript has a dense proof-based article layout; the last page contains the final two references. This inspection applies to the Stage 07 reviewed PDF and must be updated for any later layout changes.

PDF SHA256: `ddad6440a0506f546abf8f6a315de066a441110bfbe8cab976c43dd1a6ae2b05`.

## Minor documentation finding for adjudication

Several newly authored audit paragraphs omit spaces before numerals, for example `and16 references`, `reran11`, `the2026`, `all9` in the Stage 07 handoff and `with54 pages` in the build record. These do not affect the LaTeX manuscript or results, but should be corrected by the separate fixer together with any valid reviewer findings. Restrict changes to actual prose; identifiers, code, equations, version strings and historical snapshot IDs must remain exact.
