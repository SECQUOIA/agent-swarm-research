# Stage 5A exposed-minor and affine-PSD author report

Authored `sections/11a-exposed-movement.tex`, without changing main.tex or bibliography.bib. The section compiles in isolation using the manuscript macros. Its first compile produced only expected absent-external-reference/citation warnings; the obsolete TeX fraction warning was corrected.

## Mathematical development and verification

- Re-derived the full weighted exposed-minor potential, squared ambient dual norm Q_alpha, affine restriction contraction, and the optimum gap allocation g_i=epsilon alpha_i q_i/Q_alpha. Retained the factor alpha_i^(-alpha_i q_i) in Delta_alpha.
- The proof uses the quadratic-representation fundamental identity and therefore covers all Euclidean Jordan algebras, including the exceptional algebra. It does not silently substitute an associative matrix formula.
- Added exact leading full-cone distance coefficient and explained why its upper path need not be feasible in a general affine slice.
- Stated the approximate-start and bounded-round displacement contracts. Added variable chord norms: sum[-log(1-r_j)] >= D and max r_j >= 1-exp(-D/M). These are metric statements, not query lower bounds.
- Composed with precisely the certificate used in earlier rank results. Product directions/certificates are existential, and only their fixed positive aggregate is used; no claim about the minimum rank in its aggregate dual fiber. Delta remains instance dependent. The smooth consequence requires genuine whole-slice selected certificates.
- Proved affine PSD Hessian contraction using the Schur complement and scalarized matrix-fractional convexity over both real and complex fields. Injective compression follows by QR. The sharper restricted gradient constant is stated separately from unreduced pencil order.
- Re-derived the reference-weighted exposure profile from eigenvalues of D^(1/2) Q* L(x0) Q D^(1/2). No commuting assumptions on D and the reference are made.
- Independently optimized geometric and polynomial profiles. Replaced the source's potentially ambiguous finite-rank condition involving an unspecified o(1) by explicit sufficient ranks with a fixed positive delta. Derived the polynomial uniform additive error O(log(m+1)/sqrt(m)), which makes the stated leading constant rigorous after maximization.
- Gave the diagonal box matching paths in Euclideanized coordinates. These match orders in specially constructed growing-rank families, not constants, central paths, or arbitrary affine-pencil distances.

## Source dispositions

1. `workbench/active/2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md`: weighted all-EJA movement, support-determinant scale, full-cone sharpness, self-scaled scope, and rank/movement composition retained here. Its rank frontier mechanisms are already proved in sections 02, 03, and 05 and are referenced rather than duplicated. Its joint fixed-factor-count/rank integer envelope and conditional work ledgers belong to Stage 5B; they are not implicitly claimed as covered here.
2. `workbench/active/2026-09-04-spectrahedral-principal-minor-dikin-contraction.md`: affine-pencil contraction, restricted gradient improvement, rank-profile bound, geometric/polynomial leading constants, finite-rank crossover, and matching box paths retained here. Matrix-ball application is retained as a short illustration. Detailed matrix-ball exact allocation and the companion's counterexample to universal profile tightness are part of the separate central-path program; this section explicitly calls the profile a lower envelope and never claims a universal-factor characterization.
3. `central-path-cost/sections/06-formulation.tex`: weighted exposed-minor theorem and classical-step application explicitly attributed to `CentralPathCompanion`; reproduced with proofs for standalone use. No novelty claimed for that theorem's mechanism. Other parts (dimension-only primal-dual estimate and concrete formulations) are assigned to the other Stage 5A authors.
4. `central-path-cost/sections/03a-distribution.tex`: matrix-ball compression and prior spectral decay orders explicitly acknowledged. Its full spectral centrality/allocation program is not duplicated. General affine-pencil exposure with reference slack is developed directly here.
5. Earlier conic-lift sections 02/03/05: theorem hypotheses and quantifiers personally checked before writing the corollary.

## Literature checks and citation keys

- Existing `FK1994`: standard Jordan spectral/quadratic-representation background, already verified in earlier stages.
- Existing `CentralPathCompanion`: unpublished local companion; credit is explicit in the opening and PSD discussion. Update its note eventually to mention distribution section as well as formulation section.
- New `HauserGuler2002`: direct primary PDF https://arxiv.org/pdf/math/0103196 checked, Theorem 5.5 (PDF page 18, printed page 16) states c_i >= 1, determinant decomposition, and converse. The local literature package `hauser2002-self-scaled-barrier-functions-on` was consulted read-only. Journal metadata supplied by parent/root: Foundations of Computational Mathematics 2(2) (2002), 121–143, DOI 10.1007/s102080010022.
- New `NT2002`: primary author PDF https://people.orie.cornell.edu/miketodd/NTRiemann.pdf checked. Chord mechanism credited specifically to Lemma 3.2 and Corollary 3.2; the elementary proof is included.
- New `BoydVandenberghe2004`: local literature fulltext inspected at Example 3.4, printed page 76: scalar matrix-fractional convexity by the Schur-complement epigraph. Public primary full text available at https://www.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf (the web.stanford.edu host timed out). The prose does not assert that the book independently states our Hessian contraction; the proof explains its operator extension by testing every vector. The same epigraph proof works over the complex field. DOI 10.1017/CBO9780511804441.

## Integration labels

- `sec:exposed-movement`
- `thm:movement-minor`, `eq:movement-delta`, `eq:movement-minor-distance`
- `cor:movement-rounds`, `eq:movement-variable-chords`
- `cor:movement-dictionary`
- `prop:movement-psd-compression`, `thm:movement-profile`
- `eq:movement-geometric-profile`, `eq:movement-polynomial-profile`

No unresolved mathematical issue identified in the author self-check. Formal five-agent stage review remains required.
