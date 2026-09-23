# Stage 3 author audit

Status: complete and frozen for independent review, 2026-09-22.

Implemented `sections/06-lp-application.tex`, included it from `main.tex`, and
added the Brassard--Høyer--Mosca--Tapp bibliography entry. Earlier mathematical
sections were not changed.

## Coverage and development

- Read the complete sparse-LP source note, paper model and fixed/joint results,
  source map, literature audit, and root preparation note. Proposition
  `prop:lp-center` proves the orthonormal construction, rank, bounded entries,
  constant sparsity, compact nontrivial feasible segment, nonconstant objective,
  exact primal--dual centrality, predictor equations, and dual Newton solution.
- The full normal-matrix, rectangular Halmos, and right-side preparation
  unitaries are specified, including padding, public bases, counted controlled
  inverse queries, and withheld hidden scalar data. The exact right-side norm
  is explicitly withheld because it would reveal the parameter.
- Theorem `thm:lp-state` proves both endpoint hybrid lower bounds with all
  right-side queries counted. Its target is the normalized dual Newton
  direction and its fixed trace error is less than one quarter of the endpoint
  separation. Measurements, discarded estimates, and failure probability are
  included in the output density operator.
- Replaced the source's logarithm-suppressed rectangular-solver upper bound
  by direct amplitude estimation. Success probability is `t^2` for the normal
  oracle and `t` for the factor oracle. The BHMT estimate, clipping, median
  repetition, angle derivative, and averaged trace error give sharp
  `Theta(delta^-1)` and `Theta(delta^-1/2)` orders at fixed error. There is no
  appeal to an unproved overlap-free generic QLSA bound. The optional
  pseudoinverse identity and its actual support overlap are stated separately.
- Theorem `thm:lp-compiler` transfers every positive fixed-accuracy tier,
  threshold equality, high-accuracy law, and low-continuum lower proof. It
  also explains the inherited intermediate-accuracy bounds and limitations,
  sublinear-error consequence, and finite-query exact impossibility.
  The compiler input is matrix-only; the extra right-side oracle is not
  silently included in the trigonometric-polynomial reduction.
- Factor complement synthesis is exact in two queries by the bounded even
  polynomial `1-s^2`, on the left singular-vector space. An independent
  projector-compression identity gives an explicit two-query realization.
- Direct digital value access and normalization-two LCU bypasses are shown
  explicitly. The text excludes unconditional sparse-input, LP-solver,
  end-to-end QIPM, and classical runtime interpretations.

## Corrections and scope

The specialized LP family has public spectral projectors. For
`K >= G0 = (rho-1)/2`, the public contraction `(1-m_rho delta)P_minus`
has the requested error with **zero** oracle queries. Thus this family does
not inherit the general model's nonzero constant coarse tier, although it
inherits all positive tiers. Root preparation and the source's unqualified
"complete hierarchy" transfer required this correction. The high band is
the singleton `{1}`, so a positive-width logarithmic coarse tier would also
be incorrect.

The feasible segment and primal predictor do not depend on the hidden `t`;
the representation of the equalities and the dual Newton direction do.
The manuscript now makes this explicit. Sparsity is a constant degree fact
in fixed dimension, not a dimension-growing hardness claim.

## Literature checks

Read the local BHMT full text at Theorem 12 and the explicit accuracy bound
in its introduction. Read Orsucci--Dunjko Sections 1.4, 4.3 (including the
diagonally dominant digital construction), and 5.4--5.5. Their normalized
complement requirement, factor advantage, and overlap caveat are prior art
and are cited accordingly. Publisher/arXiv pages were checked for metadata.
No generic factor speedup or general normalization obstacle is claimed new.

## Validation

Analytically checked the complete unitaries, endpoint operator differences,
trace distance, predictor signs, clipping estimates, and conditional-to-mixed
output error. A qipm-Python numerical diagnostic at rho=2 and delta equal to
1e-2, 1e-4, and 1e-6 checked the LP identities, normal equation, primal
feasibility of the direction, Halmos unitarity, projector-compression formula,
endpoint state distance, and successful-estimate angle bound. Maximum identity
residual was 1.06e-15. These checks are diagnostics, not proof certificates.

Built with `conda run -n qipm --live-stream make`. Final output is a 25-page
PDF. The final LaTeX log has no warnings, undefined references, overfull boxes,
or underfull boxes. Build output is recorded in `audit/stage3-build.log`.
