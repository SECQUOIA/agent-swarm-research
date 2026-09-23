# Reviewer 2 evidence

All work here uses private extractions of the frozen delivery archives. No frozen source or other review report was edited or read. `reviewed-artifacts.json` records the input archive/PDF hashes. The referee report is `../final-review2.md`.

Logs record actual executions, including the principal unittest suite, supplied mathematical and contract audits, table regeneration, manifests before/after, standalone LaTeX build, and matching PDF hashes. The extracted directories preserve the runnable inputs and audit-generated JSON reports. `own-k4-grid.json` records a separate reviewer-written Fraction calculation of the printed K4 witness and balances; it did not import the supplied implementation.

Primary-source checks were made September 9, 2026. Online source passage locators and local corresponding texts:

- Khademnia–Davarnia: publisher DOI 10.1287/moor.2023.0001; local `../literature/khademnia-readable.txt`, Theorem 1 around line 203 and Example 2 around line 625. The NSF web fetch timed out; the locally preserved published PDF/text supplied the detailed theorem/example check. The publisher record and author preprint abstract were reached online. The first theorem is a complete EC&R hull theorem; the example specifically concerns a nonunit dual aggregation weight.
- Davarnia dissertation: https://ufdcimages.uflib.ufl.edu/UF/E0/05/02/79/00001/DAVARNIA_D.pdf ; local `davarnia-dissertation.txt`, Proposition 2.6 around line 1234. The proposition gives shared-simplex Cartesian-component convexification.
- Liberti–Pantelides: DOI 10.1007/s10898-006-9005-4, confirmed on the author publication page https://www.lix.polytechnique.fr/~liberti/publications.html . Local `liberti-pantelides.txt`, Theorem 3.1 at lines 348–399 and relaxation caveat at lines 423–430. An attempted guessed direct PDF URL failed; detailed content was checked in the preserved primary-author manuscript.
- Kis–Horváth: https://link.springer.com/article/10.1007/s10107-021-01652-z ; Section 5.9, Proposition 22 and equations (30)–(31). Both online full article and local primary text were checked.
- Onn–Rothblum: https://arxiv.org/pdf/math/0309083 ; edge-direction zonotope refinement and its use in the algorithm proof, PDF pages 3–7. This supports the classical status of the support-refinement ingredient.
- De Loera–Onn: https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf ; Theorems 1.1–1.2, printed pages 807–808; explicit injection into the first layer on printed page 816; composition and complexity discussion at pages 817–818. Online full PDF and local primary text checked.
- Almoghrabi–Skutella–Warode: https://link.springer.com/article/10.1007/s10107-026-02392-8 ; Theorem 1 and Remark 1. Online full text distinguishes the aggregate vector from the commodity-flow vector.
- Davarnia–Rahimian: https://arxiv.org/html/2510.15861v2 and https://arxiv.org/abs/2510.15861v2 ; introduction’s explicit comparison and Section 3 target. Online full text confirms binary simplex variables and projection to x-space.

No failed retrieval is treated as a successful primary-text check. The report states the limits of the literature and implementation review.
