# Stage 2 author report

Status: complete draft, ready for the required independent fifteen-reviewer round. This is an author handoff, not a passed review gate.

## Files and scope

Drafted `sections/02-quadratic-finite.tex`, updated the stage-2 rows and dependencies in `coverage.md`, and added ten primary-source bibliography entries to `references.bib`. The accepted stage-1 section and macros were not changed. Root wired the stage-2 input into `main.tex`. No existing research or literature files were edited.

The complete current manuscript has 41 pages. Stage 2 occupies five main sections, numbered 5–9 in this build: finite covariance geometry, rational constructions, output bodies and input quotients, positive quadratic structure, and approximation hardness. The stage is about 1,550 source lines, with full proofs and explicit algorithmic error budgets.

## Coverage and independent reconstruction

All thirteen stage-2 canonical result rows now have precise manuscript locations. The earlier finite and asymptotic results are integrated rather than repeated as independent notes:

- `thm:finite-covariance` proves the finite unequal-tolerance determinant law with explicit constants, arbitrary-convex-lift lower bound and shared compact binary grid. `eq:finite-domain-volume` records the domain-volume variant. The operator/Frobenius ellipsoid comparison is retained explicitly.
- `prop:commuting-covariance` gives the determinant-preserving geodesic sign-symmetrization, scalar linear allocation and one-Hessian water filling. `eq:covariance-graph-lp` identifies the weighted graph LP. `ex:covariance-gap` proves the unconditional dimension gap of the Frobenius benchmark at fixed unit accuracy.
- `thm:rational-ncrank` supplies the previously deferred full proof of stage-1 `eq:rational-rate-preview`: rational maximal shrinking, rational orthogonal subspace bases without orthonormalization, enclosing-box heights, exact dyadic depths, row and coefficient lengths, integral capacity scaling by the power `2r`, endpoint-denominator slice volume, and an explicit uniform lower bound. It also records how principal rank restrictions can be found by rank-preserving coordinate deletion.
- `lem:rational-jacobi`, `eq:matrix-function-bounds`, and `thm:rational-finite` include exact rational orthogonal rotations, contraction, common-denominator growth, matrix-function perturbation estimates, Rayleigh branches without eigenvalue gaps, global exact penalty, polynomial radius, inexact projected recurrence on the actual rational iterates, fresh dyadic rounding, feasibility repair, and final rational grid construction. The proof uses a slightly more conservative branch-error allocation than the notes: `tau=1/(512n)`, `nu=1/[128(D+1)]`, so `3n tau+D nu<1/32` even with the Rayleigh shortfall.
- `thm:grouped-covariance` proves correlated, Euclidean, overlapping and singular positive semidefinite budgets with a common residual matrix and rational double-sum gradients. The unbounded closed-error-set convention for unmeasured directions is explicit; no compact-body theorem is silently applied to those sets.
- `thm:l1-covariance` retains the specific correlation-SDP invariant and dimension-independent Grothendieck factor, with a short proof of that established bound. It supplies rational negative-vector separation, weak optimization and exact correlation repair, certified lower/upper objective values, and geodesic near-active gradients. Transformed and multiple l1 budgets are included.
- `thm:general-quadratic-body` proves exact nonlinear-output-image reduction, its pulled-back strong oracle and radii, rational ellipsoid rounding after symmetry removes the real center, and the finite count loss from norm distortion. The final MILP uses rational shared-monomial error bands rather than attempting an exact LP description of an arbitrary oracle body.
- `thm:input-quotient` proves exact equality of minima through the common Hessian-kernel quotient, including affine output variation along fibers. It constructs the zonotope separator, explicit rational radii, rational LDL/dyadic normalization, domain-volume comparison, effective-output reduction and the `O(r log(r+1))` count guarantee.
- `lem:block-logdet-oracle` gives the full rational convex hypograph solver, known interior ball, exact inverse tangents and central-ball feasibility repair. Scalar log-product allocation is explicitly its rank-one-block special case, preserving the dependency needed by forest/features and later nonlinear stages.
- `thm:block-psd` proves componentwise and unconditional-body allocation together, via the expected nonnegative Jensen vector and the block determinant inequality. Both algorithmic routes are retained: the direct Euclidean oracle and the product-cone geodesic specialization. Blockwise common-kernel quotients retain product domains and charge each intrinsic block rank separately.
- `cor:diagonal-psd` proves the explicit `5r+1` rational guarantee. The separate scalar log-coordinate projected-subgradient algorithm is included, not merely replaced by the general oracle. The trace/Frobenius distinction is explicit.
- `thm:integer-features` gives independent overlapping integer features, the actual-minor and row-length volume estimates, exact quotient, `5r+sum log w_i+1` count, primitive-row normalization and the representation-supplied qualification. `cor:forest-precision` retains the sharper exact incidence-domain volume, with its face tiling and unimodular-minor proof, and the `6r+1` bound.
- `ex:thin-domain` reconstructs the unbounded gap between an actual thin domain and its containing product, with a concrete L-binary formulation and parity lower bound. It explains why copied variables and arbitrary simultaneous diagonalization do not provide independent domains.
- `lem:zero-count-maxcut` and `thm:count-hardness` prove restricted-family zero recognition, failure of all-instance finite multiplicative approximation, polynomial replication, unit-tolerance normalization, the one-binary scalar appendage, positive-optimum additive and multiplicative hardness, and transfer to common nonlinear input rank. The theorem does not claim that an `N/log N` additive algorithm is excluded or that the separate-output reduction proves single-l1-budget hardness.

I reconstructed the mathematical arguments from the canonical results and substantive supporting notes, using the associated audit records to identify previously sensitive steps: formulation-size notation, rational branch-gradient accuracy, exact oracle conventions, the real center in ellipsoid rounding, rational capacity determinant scaling, product-domain assumptions, and zero-rank branches. The independent root simultaneously checked the proof blocks and primary imports; its separate source and test records are cited below. Prior repository audit labels were not used as proof of validity.

## Additional development found during coverage audit

A fresh filename/content sweep found two relevant unindexed paths:

1. `notes/covariance-determinant-optimality-certificates.md`.
2. `notes/review-covariance-optimality-certificate-root.md`.

Both are now in the dependency inventory, and the first is an additional substantive row. Its `prop:covariance-certificate` was independently reconstructed: the geodesic Lagrangian lower inequality, determinant-controlled distance, nonnegative rational residual `tr(PRPR)`, sufficient complementarity/stationarity, convex multiplier refinement, and correlated-budget extension are included. This provides an a posteriori verification route distinct from running the conservative construction algorithm. Root also supplied a new independent exact/high-precision checker for it.

The inventory now has 43 canonical results, 33 explicit substantive supporting developments, and 196 supporting notes/audits. All 272 local links resolve. No stage-2 canonical row remains pending. The remaining filename candidates concern other topics or stage-1 novelty, and were not added to stage 2 merely because their names contain “quadratic.”

## Proof and exposition repairs made before handoff

No false canonical theorem or unresolved mathematical gap was found in this drafting pass. The proofs explicitly resolve the following boundaries rather than relying on context:

- All-affine and zero-rank cases are dispatched before divisions by rank or zero-dimensional constants, including block, diagonal and forest results.
- A domain projection subtracts affine output terms before projecting, so varying affine terms on a fiber do not invalidate equality of minima.
- Every rotated/enclosing grid retains the original domain equations and bounds.
- Semidefinite grouped energies are treated through conceptual factorizations for proofs and rational double sums for algorithms.
- The l1 oracle returns an exactly feasible rational correlation matrix, not only a nearby one; its upper objective certificate follows from the precise weak-optimization guarantee.
- Scalar and block log-determinant oracle repairs explicitly use the interior ball to turn weak feasibility into exact feasibility.
- Coefficient encoding, construction time, continuous formulation size, integer count and optimization time remain distinct throughout.

Root requested the local all-affine/zero-rank clarifications during drafting, and these were applied before any review snapshot. Several overfull displays were split; the final build has no reported box or reference warnings.

## Sources and attribution

The ten new entries are `sra2013`, `zhang2016`, `criscitiello2021`, `delpia2026`, `gls1981`, `dpv2011`, `briet2010`, `garey1976`, `cao2007`, and `vandenberghe1998`.

I checked official proceedings, author-hosted primary papers and publication pages for their stated role and metadata. Root independently downloaded/read the most delicate imported statements and recorded exact locations in `verification/stage2-root-source-audit.md`. These include Zhang–Sra Corollary 8 and the best-iterate telescoping argument, Criscitiello–Boumal Appendix I and the affine-invariant curvature normalization, GLS1981 Definition (5)/Theorem (3.1), DPV Definition B.2/Theorem B.5, IQS rational bit bounds and field extension, and GGOW integral capacity.

The Criscitiello–Boumal entry uses the published FoCM23 (2023),1433–1509 metadata and DOI, with the arXiv v2 Appendix I retained for exact numbering; the bibliography key is intentionally unchanged. DPV is cited as the checked April13,2011 full manuscript because that is the version containing the precise appendix theorem used. Briët–de Oliveira Filho–Vallentin uses its ICALP2010 publication. The Cao and MAXDET entries credit established anisotropic-ellipsoid and log-determinant methodology. A failed fetch of the Chen–Sun–Xu PDF was not treated as a successful source read and no new claim depends on it.

The manuscript does not claim that parity, interpolation, Jacobi rotations, geodesic optimization, MAXDET, Grothendieck approximation, weak optimization, zonotope geometry or Max-Cut encoding are new. Broad publication-priority synthesis remains part of stage 4 and the whole-paper review; the existing bounded repository novelty searches cannot establish exhaustive priority.

## Verification and limitations

The root-owned manifest `verification/stage2-20260905T182103Z/manifest.json` records twelve existing stage-2/dependency scripts and the new covariance-certificate checker; all thirteen passed. I inspected that manifest. It covers residual LP extrema, exact covariance and coordinate identities, matrix/Jacobi checks, grouped/l1 errors, input quotients, block and scalar central-ball repairs, forest minors, integer features and hardness packings. The new certificate checker verifies40 exact complementary optima and40 perturbed covariances. These are supplementary checks, not a formal proof or an implementation of the imported ellipsoid/geodesic optimization algorithms.

Author verification:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`: success; build log `build/stage2-author-build.txt`.
- `verification/check_manuscript.py`:125 unique labels,22 bibliography entries, no duplicate labels/keys or unresolved references/citations.
- Final `build/main.log`: no Warning, Overfull, Underfull or undefined messages.
- `pdfinfo`:41 pages, letter size,558224 bytes at the inspected build.
- Rendered and visually inspected pages24 and33, covering the spectral proof and matrix-oracle proof; equations, margins and page breaks are legible. Images and extracted text are in `build/stage2-author-page24.png`, `build/stage2-author-page33.png`, and `build/stage2-author-text.txt`.
- Active coverage links:272, all resolving;196 distinct note paths in the dependency index.

The user-required fifteen reviewers have not yet reviewed this draft. Root should freeze the completed sources, dispatch the review round, adjudicate findings, and use a separate correction agent before considering the stage gate passed.
