# Stage 4 primary-source and version audit

Read on 2026-09-22. This record concerns the Gram-map and infinite-aggregation
sections. It supplements earlier literature records and does not establish
priority by search failure. No managed literature files were edited.

| Source inspected | Exact content used and version distinction |
|---|---|
| Uhlmann, [author-hosted published PDF](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf), Reports on Mathematical Physics 45(3):407–418 (2000), DOI 10.1016/S0034-4877(00)80007-5 | Pages 408–410: separate concavity of transition probability, no trace normalization required, equation (14) at partial-fidelity index zero is the product-of-traces infimum. This matrix inequality and concavity are classical. |
| Ramachandran–Shu–Wang, [institutional published PDF](https://ir.cwi.nl/pub/35175/35175.pdf), Mathematics of Operations Research 50(2):1454–1477 (2025), DOI 10.1287/moor.2023.0114 | Lemma 1, printed 1460, credits the determinant-corrected SO(n) extremum to Farrell and coauthors. Appendix B relates rotation images to quadratic images of normalized spheres. Neither inspected statement is the present full Gram+scalar-square hyperplane formula. The manuscript independently proves the needed interval by pair rotations. |
| Beck, [author-hosted published PDF](https://www.tau.ac.il/~becka/14.pdf), SIAM J. Optim. 17(4):1224–1238 (2007), DOI 10.1137/05064816X | Definition of quadratic matrix programming and original strong-duality background. PDF header and later primary reference lists use 2007; one institutional metadata page labels it 2006. Manuscript uses the printed journal year 2007. |
| Beck, [author-hosted published PDF](https://www.tau.ac.il/~becka/22.pdf), JOTA 142(1):1–29 (2009), DOI 10.1007/s10957-009-9539-y | Root retrieved `/tmp/quadratic-paper-literature/beck2009.pdf` and `.txt`; author independently read §3, Theorems 3.1, 3.3, 3.4. Real Theorem 3.1 allows m<=r arbitrary QM functions and global image convexity. Theorem 3.4 allows m<=r+1 with row dimension>=2 and signed positive definite combination of quadratic blocks. These do not directly retain repeated structure after an arbitrary scalar hyperplane restriction. No general QM-convexity novelty is claimed. |
| Blekherman–Dey–Sun, [arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2), May 29, 2023 | Freshly inspected Definition 2.1, Theorem 2.9 and Conjecture 3.1. Hull theorem needs n>=3, nonempty strict S, proper hull and HHC. Conjecture 3.1 asks for HHC with no finite good-aggregation description. Journal metadata is separate 2024; numbered locators explicitly cite v2. |
| Dey–Muñoz–Serrano, local published PDF and root's fresh layout extraction `/tmp/quadratic-paper-literature/dms.txt` | Proposition 2.8 and §7.4, printed 681–682. Earlier infinite example is CLOSED and two-dimensional; displayed multipliers have leading diag(a−1,−a), hence outside BDS good-inertia class. The manuscript independently verifies failure of HHC on y=0. This is a direct comparison, not a broad first-infinite-aggregation claim. |
| Wang–Kılınç-Karzan, [arXiv:2403.04752v2](https://arxiv.org/html/2403.04752v2), March 20, 2024 | §4.1 and Assumption 1: replication count>=number of constraints plus a positive definite nonnegative leading combination give SDP epigraph-hull exactness. With zero objective, three constraints, A1+A2=I, it covers our closed fixed-level set for r>=3. This is not HHC or finite-quadratic impossibility. Version 1 used an appendix; v2 does not. |
| Wang–Kılınç-Karzan journal metadata | [Publisher-deposited Crossref record](https://api.crossref.org/works/10.1016/j.orl.2024.107108) freshly retrieved by urllib confirms ORL 54, article 107108, May 2024. DOI endpoint failed as full-text retrieval. Manuscript uses separate journal/preprint entries. |
| Brun–Sun–Watson, [arXiv:2603.18473v1](https://arxiv.org/html/2603.18473v1), March 19, 2026 | §3.2.1, Corollary 1: inner-product hypograph over two balls has a Shor hull for dimension>=2. This is related but fixing a level after convexification is not an automatic fixed-level hull proof. No solver conclusions are imported. |
| Dey–Han–Wang, [published open full text](https://link.springer.com/article/10.1007/s10898-026-01607-8), JGO 94:1099–1135 (2026) | Fresh primary publisher read of §§1.1–2, Theorem 2 and its xy1=xy2=.5 boxed example. Signed equality aggregates are each convexified before intersection. Confirms the theorem locator in the journal. The local original originates from arXiv and should not alone be described as the published full text; fresh publisher reading resolves that version issue. |
| Blekherman–Dunbar, local `/tmp/quadratic-paper-literature/bd.pdf` and [arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1) | Prior-stage inspected Theorem 1.4 retains homogeneous PDLC and regularity/infinity assumptions. Stage 4 attempted the suggested published eprint but the web tool returned an internal error; root reported the same result. The manuscript cites the inspected preprint for theorem numbering and separately the 2025 publication. Stage 6 will audit the four-bound in depth. |

Actual new discovery searches included `"Amir Beck" "Quadratic matrix
programming" pdf`, `"hidden hyperplane convexity" "Gram"`, `"Blekherman"
"Conjecture 3.1" infinite`, `"On semidefinite descriptions for convex hulls"
Wang journal`, the exact Beck2009 title with pdf, and Uhlmann/rotation-paper
bibliographic queries. Search results led to primary author, publisher,
institutional, arXiv, or publisher-deposited Crossref records. Exact theorem
claims rely on primary full text, not search snippets. No exact previous
resolution of the HHC+infinite-good-aggregation conjunction was identified
in this bounded investigation.

The contribution claim is the explicit HHC construction with its
indispensable continuum and original-variable quadratic obstruction.
The sharp Gram HHC theorem is a proved structural formulation/application
of classical matrix ingredients; the manuscript avoids claiming a new
fidelity inequality or new general SDP principle. A comprehensive priority
proof is not possible from a bounded search, so the narrow priority sentence
is expressly qualified.
