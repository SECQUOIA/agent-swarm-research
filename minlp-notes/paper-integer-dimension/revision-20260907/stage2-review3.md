# Stage 2 independent review 3

**Assessment: no supported major or minor finding.** The stage can proceed on the basis of this review. No manuscript edits were made, and no other current reviewer report was consulted.

## Coverage

Read the entire frozen `reviews/revision-stage2-round1/source/sections/01-foundations.tex` (1,296 lines) and `sections/02-quadratic-finite.tex` (1,571 lines), including proofs, examples, unnumbered constructions, computational qualifications and concluding scope statements. Compared both files and their bibliography with the stage 1 snapshot; read `stage2-author.md` and `stage2-literature.md`.

Reconstructed the mathematical dependencies from parity contacts through the quadratic law, smooth/constant-rank/perspective transfers, finite covariance comparison, rational algorithm, output and input reductions, positive structure and hardness. The author's reports were not treated as proof or as a substitute for reading the sources.

## Critical checks

- **Contact and rank arguments:** compact closures preserve the midpoint restriction without requiring measurable witness choices; the indefinite simplex estimate, covariance fourth-moment identity and whitening-volume argument supply the stated constants. Principal Hermitian compression and real symmetric shrinking supply the claimed lower slice and matching precision allocation. The smooth tensor-phase proof controls arbitrary compact contacts, and the constant-rank argument establishes error on whole polyhedral tubes in original coordinates.
- **Rational finite construction:** checked the homogeneous exact penalty, trace-one gradient bounds, polynomial-radius region, inexact subgradient recurrence and its constants, fresh rational rounding, scalar feasibility repair, and rational orthogonal near-diagonalization. The proof does not assume a spectral gap or transfer an arithmetic-operation bound directly to a bit-complexity conclusion. PSD-order energy monotonicity justifies its final matrix sandwich even for indefinite Hessians.
- **Output bodies:** grouped energies remain positive sums after a conceptual real factorization, while the implementation uses rational unfactored sums. The total-absolute-error proof's correlation repair gives exact feasibility and a certified upper objective value. Effective-output restriction preserves both minima, including when an original lift admits errors outside that image. Ellipsoid centering is eliminated correctly by symmetry; the effective dimension bound removes ambient output count from the additive loss.
- **Input quotient:** subtraction of the original affine output before projection is necessary and present. The rational zonotope separator, LDL normalization and contained-cube volume estimate justify the domain loss. The exact original-domain lift is retained in the final formulation.
- **Positive structure and computational model:** the logdet hypograph has the asserted interior ball; its rational tangent oracle meets the cited weak-separation convention. The central-ball repair gives exactly feasible rational blocks without symmetry or boundedness of the output set. Positive block, diagonal and integer-feature arguments use unconditional domination in the required direction. Independent block quotients retain a product domain; the forest-volume proof and thin-domain example preserve the relevant distinctions. Hardness uses a polynomial replication exponent for each fixed delta and does not claim to exclude every sublinear additive function.

The changed positive-product Hessian factorization is valid at every point of a positive box. The revised square discussion correctly converts the prior dyadic interpolant into a graph-containing band.

## Independent primary-source checks

- **GLS 1981**, original PDF, printed p.172, Definitions (5)–(6), and Theorem (3.1): the weak-optimization convention compares against the actual body, as required by the correlation and logdet repairs. This avoids importing a different inner-core convention. Source: https://ir.cwi.nl/pub/10046/10046D.pdf.
- **Dadush–Peikert–Vempala**, original PDF, Theorem B.5 on PDF p.39: checked the rational ellipsoid matrix, possibly real center, factor `(d+1)sqrt(d)`, and small-volume alternative. The manuscript removes that alternative using its known inner ball. Source: https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf.
- **Zhang–Sra 2016**, freshly downloaded primary PDF pp.8–9, Corollary 8 and its proof: checked that the curvature factor uses the comparison-point distance and that nonexpansive projection permits the recurrence used here. Source: https://proceedings.mlr.press/v49/zhang16b.pdf.
- **Garg et al.**, local original PDF p.5 and pp.26–27: checked Theorem 1.4's evaluation/shrinking equivalence and Theorem 2.18's integral capacity bound. The manuscript's scaling exponent `D_H^(-2r)` is correct.
- **Ivanyos–Qiao–Subrahmanyam**, local original PDF p.7 and local full text at Lemma 5.3: checked the constructive rational shrunk-subspace guarantee, polynomial intermediate encoding, and field-extension invariance.

These are proof and source checks, not a claim of formal verification. No additional computation was necessary to decide a suspected issue, and no duplicated numerical test suite was added.

## Optional preferences

None required for acceptance.
