# Stage 5A: primal–dual movement author audit

Authored `sections/11b-primal-dual-movement.tex` only; no main, bibliography, source-map, or other agent's section was edited. The section compiles as a five-page standalone temporary wrapper with the manuscript macros, with no overfull boxes. Undefined citations and cross-references in that isolated wrapper are expected; main integration remains the stage author's responsibility. No formal five-review cycle is claimed by this author audit.

## Sources read and disposition

- Read repository AGENTS.md and the complete current root-stage5 preparation.
- Read the complete dimension-only arbitrary-cone primal–dual movement note. Retained its integer envelope, ordinary operational dimension argument, coupled-barrier orthant-section proof, and precise bounded-move consequence. The manuscript's already proved minimum-dimensional rigidity supplies the dimension bound, avoiding duplicate treatment of free variables. Exact integer envelope is not asserted to be an attained lift frontier.
- Read the complete barrier-independent primal–dual Dikin note. Retained its classical gap-set theorem, finite-chord conversion, definable curvature transfer, globally smooth Lorentz transfer, sharp shared product-ball charge, and distinction from restricted slice metrics. The PSD order-cap transfer is deferred to Stage5B's integer ledger rather than duplicated here; the general theorem proves the required substitution immediately. Retained the pointwise Dikin/determinant/gradient countermodel with an explicit statement that it is not a global Hessian. The failed coupled surrogate barriers and proposed tangent-barrier compactness program are not results needed in the paper: no all-barrier primal theorem under objective nondegeneracy is claimed or used.
- Read the complete exact speed-splitting/product-ball counterexample note, including all of Section8. Retained orthogonal velocity allocation, Schur formula, progress identities and convergence conditions, exact q_eff, one-active and positive-tail unique-optimizer examples, Q1/Q2 sharp constants, explicit piecewise integral, head-tail and full-gap l2-tail bounds, bounded-Dikin sampling schedule, and geometric-weight actual central-arc order. Exact center sampling is a mathematical schedule, not an assertion of finite-time exact numerical inversion of arbitrary real integrals. Weight reading, center evaluation, output materialization, and precision are separate costs.
- Read the complete companion `sections/06-formulation.tex`; additionally read companion `sections/05-primal-dual.tex` and the relevant distribution-law/head-tail/geometric sections of `03a-distribution.tex`. This revealed broader overlap than the preparation initially mentioned: **all main formulas allocated to 11b already occur in the existing companion**, not only the arbitrary-cone envelope. No novelty is claimed for them. Their role here is self-contained background and the transfer to this manuscript's proven lift-frontier theorems.
- Actual compiled companion sections are **5** (distribution), **9** (primal–dual), and **10** (formulation), checked in companion `main.aux`. The file prefixes are not section numbers. Citations use these actual numbers.

## Proof checks and qualifications

1. Independently derived conjugate Hessian `F_*''(s)=eta^2 H^-1`, derivative `eta sdot=F'-H xdot`, and orthogonal decomposition. Confirmed progress signs for minimizing primal/maximizing dual.
2. Reproved central gap-sublevel minimization from the first derivative and feasible cross-pairing zero. No terminal centrality is required; terminal strict primal and dual feasibility is required. Curves may leave affine equations. Integrating the ambient potential gives `sqrt(nu/2) log(Delta0/epsilon)`.
3. Checked integer envelope at d=2, residue0, residue1, residue>=2. Kept rays in orthant section. Coupled LHSC barriers are allowed because this is one interior section of the whole product, not an unsupported optimal-parameter additivity claim.
4. Recomputed radial central profile, its log-parameter derivative, and squared radial speed. Explicit unique-optimizer weights depend on requested epsilon, so the result is not a fixed-instance asymptotic disproof.
5. Rechecked both sharp scalar lower constants at z=1; early-time square-speed control, full-gap tail bound, and convergence at eta=0. Checked the elementary antiderivative.
6. For geometric weights, the displayed order is for the actual central arc to eta_f=2m/epsilon. The dyadic lower sum uses j<=m<=k and the remaining interval uses q_eff<=2m. No shortest-distance claim is made here (the companion has stronger spectral distance results, handled separately in this project).
7. Pointwise countermodel inverse diagonals, determinant, diagonal speed, and gradient dual norm all recomputed. Its distinction from an integrable barrier is explicit.

## Primary literature and integration keys

Opened the primary full texts through web tools:

- Nesterov–Todd, *On the Riemannian Geometry Defined by Self-Concordant Barriers and Interior-Point Methods*, Foundations of Computational Mathematics2 (2002),333–361, DOI10.1007/s102080010032. Primary: https://people.orie.cornell.edu/miketodd/NTRiemann.pdf . Classical Sections3–5 support the chord comparison, constant speed, and feasible gap-sublevel geometry. Requested central bibliography key: `NT2002`.
- Nesterov–Nemirovski, *Primal Central Paths and Riemannian Distances for Convex Sets*, Foundations of Computational Mathematics8(5) (2008),533–560, DOI10.1007/s10208-007-9019-4. Primary: https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf . Cited only for the established general distinction and primal comparison, not as a source of the explicit product-ball formulas. Requested key: `NesterovNemirovski2008`.
- Existing keys used: `NN1994`, `Hildebrand2013`, `CentralPathCompanion`.

No new reference was added directly to bibliography; the stage author owns central bibliography integration.
