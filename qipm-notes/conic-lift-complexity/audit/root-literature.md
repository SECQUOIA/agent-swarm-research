# Root literature verification

Date: 2026-09-20. This is a targeted source comparison, not a guarantee of priority. Local package notes were used to locate primary texts; their assessments do not substitute for the original theorem.

## Foundational distinctions

- Gouveia, Parrilo, and Thomas, *Lifts of Convex Sets and Cone Factorizations*, Mathematics of Operations Research (2013), DOI 10.1287/moor.1120.0575, arXiv:1111.3164. Local full text, Definition 2.1 and Theorem 2.4: proper conic lifts correspond to slack factorizations; the forward direction uses Slater duality. Corollary 2.6 addresses nice cones. Theorem 2.12 concerns equivariant lifts. These are the foundational framework, not new results of the proposed paper. The paper's cone-rank invariant minimizes a cone-family size; it does not by itself compute the minimum certificate rank at a fixed support.
- Cardoso and Vieira, *On the optimal parameter of a self-concordant barrier over a symmetric cone*, European Journal of Operational Research 169 (2006), 1148–1157, DOI 10.1016/j.ejor.2004.11.027. Local primary text, Sections 2–3: Jordan determinant barrier, logarithmic homogeneity, and ambient optimal rank parameter. This does not identify the optimal parameter of that barrier after an arbitrary affine restriction, or optimize that restricted parameter over lifts.
- Kummer, *Two Results on the Size of Spectrahedral Descriptions*, SIAM Journal on Optimization 26 (2016), 589–601, DOI 10.1137/15M1030789, arXiv:1506.07699. Theorem 2.1 gives direct real LMI size obstructions for balls. Direct spectrahedra and projections of products of cones must be distinguished.

## Extension-complexity comparators checked online

- Fawzi and Parrilo, *Exponential lower bounds on fixed-size psd rank and semidefinite extension complexity*, arXiv:1311.2571. Counts fixed-size PSD factors in lifts; a close comparator for factor count, not the same support-wise certificate objective.
- Averkov, *Optimal Size of Linear Matrix Inequalities in Semidefinite Approaches to Polynomial Optimization*, SIAM Journal on Applied Algebra and Geometry 3 (2019), 128–151, DOI 10.1137/18M1201342, arXiv:1806.08656. Extension degree minimizes largest block size while permitting products; Theorem 2.1 uses prescribed polynomial zero patterns.
- Saunderson, *Limitations on the Expressive Power of Convex Cones without Long Chains of Faces*, SIAM Journal on Optimization (2020), DOI 10.1137/19M1245670, arXiv:1902.06401. Neighborliness versus short face chains obstructs all finite product lifts in the stated classes. This is distinct from an exact count or barrier cost when a lift exists.
- La Piana and Müller-Hermes, *Annihilating and breaking Lorentz cone entanglement*, Linear Algebra and its Applications (2026), DOI 10.1016/j.laa.2026.03.012. The primary publisher text studies positive maps factoring through Lorentz cones and operator-ideal norms. Lemma 4.2 reduces an intermediate Lorentz dimension for a positive-map composition. This is a relevant modern comparator but does not state the affine ball-lift certificate-rank minimax.

## Searches

Queries included combinations of Euclidean ball, lift, barrier parameter, support certificate rank, affine restriction, smooth factorization, semidefinite extension degree, and Lorentz positive-map factorization. Exact-phrase searches were weak and mostly returned unrelated complementarity algorithms. Broader searches found the comparators above. A failure to find a matching theorem is not evidence that no such theorem exists.

## Writing consequence

State any proposed novelty at the level of the precise invariant, quantifiers, model, and exact formula proved. Attribute the general lift correspondence, ambient symmetric-cone barrier optimality, Peirce calculus, standard topological tools, and bounded-movement conversion. Do not present them as new. Separate arbitrary lifts from lifts admitting global differentiable choices, ambient barriers from restricted standard barriers, and mathematical movement from arithmetic or quantum query cost.

## Accessible Jordan source added during verification

Gowda and Sznajder, *Schur complements, Schur determinantal and Haynsworth inertia formulas in Euclidean Jordan algebras*, Linear Algebra and its Applications 432 (2010), 1553–1559, DOI 10.1016/j.laa.2009.11.015. Author-hosted primary PDF: https://userpages.umbc.edu/~gowda/papers/GOW10-01.pdf. Printed pp. 1554–1555 define the Peirce Schur complement, give determinant/inertia/rank formulas, and state positivity of quadratic representations; Proposition 1 verifies the complementary Peirce location. These statements apply to all Euclidean Jordan algebras. They avoid relying on associative octonionic matrix arithmetic. The author website also supplies *More results on Schur complements in Euclidean Jordan algebras* (2012) and *On the bilinearity rank of a proper cone and Lyapunov-like transformations* (2014); neither title alone is evidence for a claim in this manuscript.

The local Faraut–Korányi chapter packages contain metadata only, with `access: none`. They have not been read from that local source. Do not cite invented chapter theorem locators as if verified.

## Barrier literature checked during Stage 2

- Hildebrand, *A lower bound on the barrier parameter of barriers for convex cones*, Mathematical Programming 142 (2013), DOI 10.1007/s10107-012-0576-1. Original preprint titled *A lower bound on the optimal self-concordance parameter of convex cones*, https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf, Section 6, Theorem 6.1, pp. 9–10: the extra radial unit concerns logarithmically homogeneous barriers on a regular polyhedral cone at a nonzero point with independent active facets. It must not be transferred to arbitrary barriers. The preceding paragraph identifies the ordinary polytope result as Nesterov–Nemirovskii Proposition 2.3.6.
- Hildebrand, *Projectively self-concordant barriers*, Mathematics of Operations Research 47(3) (2022), 2444–2463, DOI 10.1287/moor.2021.1215; arXiv:1909.01883v2 (2021), https://arxiv.org/abs/1909.01883. After the initial abstract check, the local primary `fulltext.md` was inspected at Theorem 1.5 and Sections 6–7. Theorem 1.5 relates projective self-concordance to homogeneous conic extensions; Section 6 treats affine sections, projective images, and products; Lemma 7.1 specializes to proper cone sections. These statements provide important prior context but do not compute the least affine parameter of the particular restrictions in this manuscript.
- Hildebrand, *Three Different Views on Barrier Functions in Conic Optimization*, JOTA 209, article 36 (2026), DOI 10.1007/s10957-026-02986-4: publisher abstract checked; geometric interpretations of logarithmically homogeneous barriers. Full text is subscription-only in the checked source, so no theorem-level exclusion of overlap is asserted.
