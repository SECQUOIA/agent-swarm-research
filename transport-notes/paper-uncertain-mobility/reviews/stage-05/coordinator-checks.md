# Coordinator checks: Stage05

Date: 2026-09-07. Stage04 was accepted before this stage's sole author was assigned. These checks concern exact observation and local quadratic placement only.

## Independent local-model derivation

Read the placement note, its complete localization review, the robust-design note and review, and the placement prior-art audit. General-power and joint-flow material belongs to the companion deterministic topic; the current stage uses the quadratic theorem and relevant compact/physical consequences.

With p(y)=y−3y³+2y⁴, the proposed coefficient has flux D*h*′=−R p(y) for 0<x<R. Since p′+y²(9−8y)=1, its weak equation is correct. Flux vanishes at zero and both support endpoints, so the derivative cusp and slope changes create no delta source. The budget integral is 3aR⁵/80. The inside and outside source integrals are 10/(aR) and 2/(aR), respectively. The global derivative bound is 8/(aR³), attained in the interior, and the exterior derivative is strictly smaller.

The global lower certificate is valid for every L1 mobility: truncate the integrable inverse tail, then mollify. Derivatives stay bounded by the central slope plus a vanishing error and converge almost everywhere, so the arbitrary mobility term is controlled by dominated convergence. Source and reaction tails are integrable. Completion of the square and the zero-flux weak identity provide the matching upper value. Equality forces zero mobility outside the support and makes h* a maximizer for the competing field. Variation yields a distributional flux equation; the zero exterior flux determines the coefficient by integration on each open half-support, giving uniqueness almost everywhere.

The compact-wall lower proof must use actual local masses m_j, not assume localization. Cutoffs operate only on the fixed tails for all 0<m_j≤M once M is small, so cutoff load/reaction errors remain bounded independently of m_j, and the central slope remains the global Lipschitz bound. Disjoint tests add. A zero local mass is treated by an auxiliary shrinking radius. Convex allocation of a_j^(-4/5)m_j^(-1/5) gives m_j proportional to a_j^(-2/3). For upper bounds, the direct zero-flux completion of the square on each support plus reciprocal-potential integration outside avoids an assumed domain decomposition.

## Domains and physical trial remainder

The explicit derivative preform is closable: on every compact subinterval where D>0, a putative derivative limit for an L2-null Cauchy sequence must vanish; on {D=0} every weighted derivative already vanishes. These sets cover almost every point. The center behaves as |x|, with logarithmically diverging integral of 1/D; logarithmic transition profiles have vanishing energy there. At outer quadratic zeros, a transition of fixed height over width epsilon costs O(epsilon). Thus the minimal closed domain permits separate traces at those zero-capacity points. No path-transmission claim or stationary infinite-wall process is required.

For fixed separated quadratic zeros, local comparison gives 0≤h≤h_* for a lower comparison curvature. Hence kh is bounded independently of small M on each trial support, and kh=1 outside. The support has total length O(M^(1/5)), so ||kh−1||_2→0. The bulk load converges in its energy dual norm. For fixed smooth bulk test f, the Schur penalty is at most M||partial_s f_Gamma||_infinity² and tends to zero. Dropping that nonnegative penalty gives the upper limit, and fixed smooth tests plus density give the lower limit of the bulk remainder, equal to the R0 already defined in Stage02. This is a fixed-realization trial result, not a uniform-in-disorder bounded correction or an additive estimate for the optimized value.

## Measurable oracle construction

For separated cosine roots let a=1−c² and sigma=M/a^(7/2). The author's proposed lower comparison curvature is b=a(1−eta), eta=sigma^(1/10). Each half-budget quadratic profile has support radius divided by root distance O(sigma^(1/5)). The relative Taylor error is of this order, which is smaller than eta when sigma is sufficiently small. A fixed sufficiently large fold cutoff t≥L M^(2/7) enforces that condition and eta≤1/2 uniformly. For each fixed regular c, eta→0 and the correct sharp local coefficient follows.

The explicit formulas, roots arccos(−c), finite regime cuts, and patch indicator yield a Borel L1 policy with exact budget. In the fold layer use a constant mobility patch of radius O(M^(1/7)) and height O(M^(6/7)); the bounded scaled quartic parameter gives response O(M^(−3/7)). On rootless offsets any exact-budget design has the reciprocal-potential upper bound. These three regions give the common integrable envelope M^(1/5)J≤C|1−|c||^(−4/5). The fold layer contributes only O(M^(−1/7)) to the mean. Lower bounds hold for every policy pointwise and can be integrated without asserting an unproved measurable selection or equality of infimum and expectation.

## Current primary-source check

Independently inspected Alexandersen and Sigmund (2021), *Revisiting the optimal thickness profile of cooling fins: A one-dimensional analytical study using optimality conditions*, DOI 10.1109/ITherm51669.2021.9503196, proceedings pages 24–30. The accepted manuscript's printed pages1–3, equations1,3,5, show selectable conduction thickness with a distributed constant loss term, prescribed base flux, fixed volume, and constant-gradient/polynomial optimality conditions. Those design ideas precede the current quadratic-killing, spatially uniform-source calculation. They must not be claimed as new principles.

Working institutional full-text URL: https://findresearcher.sdu.dk/ws/portalfiles/portal/191660127/ITherm2021_revised.pdf . The web fetch failed, but Python requests downloaded the PDF successfully for local read-only inspection in /tmp; pdftotext supplied the checked text. No source PDF was redistributed in the repository. The older joealexandersen.com URL redirects to a new site. Metadata was also verified at https://orbit.dtu.dk/en/publications/revisiting-the-optimal-thickness-profile-of-cooling-fins-a-one-di/ . Searches of variable-loss/internal-generation fin design show a large neighboring literature and are not evidence of exhaustive absence; the final novelty audit must retain that boundary.

## Complete source pass before author freeze

Read the first complete Section05, including the added uniqueness/domain/fixed-profile bulk-correction corollary and explicit oracle policy. The principal mathematical arguments check. At fixed regular c, the shrinking comparison neighborhood delta is of order M^(1/10), while the placement radius is of order M^(1/5); the exterior error O_c(delta^(-1)) is consequently smaller than the leading response. The support Taylor inequality follows from (1−eta/4)²≥1−eta for eta≤1/2.

Sent two author-cleanup points before freeze: remove a carriage-return corruption in the Borel-policy formula and scan control characters; and explain that the uniform-mobility comparison for the merely continuous compact rate uses the earlier proposition's potential-bracketing proof, since its formal statement assumes C². Neither requires changing the earlier accepted proposition. Suggested writing the shrinking-neighborhood error explicitly. These are part of the author's ongoing self-audit, before the five-reviewer snapshot.

Independent SymPy/mpmath checks are in coordinator-sanity-checks.json: polynomial residual0, mass integral3/20, inside source10, derivative energy12/5, inside reaction38/5 and total reaction48/5; Cpl=6.22282373601989, Kobs=22.4046282307491, oracle/blind coefficient1.21856579293469. These algebra checks do not substitute for the variational and policy proofs.

## Frozen-source layout and pending minor clarification

Frozen snapshot: b10b05d41199399897fdd9cc7cc6eab8d0fe2ae90e96c6ff4fa8d7d2ef68b42c. Visually inspected PDF page35 after freeze: the policy and fold estimates are readable and within margins.

Coordinator finding C-01 (minor, for adjudication after all five reports): in the fold-patch proof, the sentence “The derivative energy has the same scale r^4” uses the operator scale for an integrated energy. For a rescaled unit-amplitude test v(s)=f((s-s0)/r), the derivative and reaction energies both carry r^5, while the differential operator carries r^4. The response r/r^4=r^(-3) is correct, so no theorem or estimate changes. Replace “derivative energy” by “derivative part of the operator”, or explicitly give the common r^5 quadratic-energy factor and r source factor. This is a terminology clarification, not a gap in the scaling proof. Keep the source frozen until all reviews are complete and assign any accepted correction to the separate fixer.
