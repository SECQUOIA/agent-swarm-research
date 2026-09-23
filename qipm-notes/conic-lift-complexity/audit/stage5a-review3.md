# Stage 5A independent review 3

Reviewed all of `11a-exposed-movement.tex`, `11b-primal-dual-movement.tex`,
`11c-concrete-movement.tex`, and `11d-tree-distance.tex`, together with
`audit/stage5a-author.md`. I did not delegate, edit the manuscript, inspect
other reviewers' reports, or run a shared build.

## Assessment

No major mathematical, scientific, or attribution issue found. Three minor
notation/domain omissions should be corrected before closing the stage.

## Minor corrections

1. **Define the matrix in the compression example.** In
   `11a-exposed-movement.tex:268–274`, the determinant
   `det(I_r-U^*XX^*U)` uses `U` without introducing it. Define `U` as the
   `p` by `r` matrix consisting of the selected orthonormal coordinate
   vectors (over the same field as `X`). This makes both the compression
   and the identity unambiguous. The assertion and parameter `r` are correct.

2. **Exclude a zero chord radius in the divided bound.** In
   `11a-exposed-movement.tex:291–292`, write `0<R_0<1`, rather than only
   `R_0<1`. The displayed operation divides by `-log(1-R_0)`, which vanishes
   at zero. No proof change is needed.

3. **State the domain of the exact arc-to-accuracy formula.** In
   `11c-concrete-movement.tex:260–271`, explicitly state `0<epsilon<k` and
   `0<R<1` for the route and chord-count formula. The preceding definition
   gives `A(r)` only for `0<=r<1`, whereas `r=1-epsilon/k` is negative for
   `epsilon>k`. At `epsilon>=k` the analytic center is already accurate and
   zero chords suffice. Including this sentence, or restricting the formula
   to `0<epsilon<k`, resolves the omission. Later asymptotic uses already
   lie in the correct range.

## Substantive verification

- Recomputed the conjugate normalization, central identity
  `F(x)+F_*(s)=nu log(eta)-nu`, orthogonal primal/dual velocity splitting,
  Schur formula after redundant-row removal, and the signs in both objective
  progress identities. Strict feasibility gives the classical central path;
  the manuscript correctly conditions the integral identities on convergence.
- Checked the full feasible gap-set proof: primal and dual feasible
  differences are orthogonal, convexity gives the barrier-height minimum at
  the target center, and the ambient gradient norm is `sqrt(2 nu)`. Allowing
  infeasible intermediate curves/chords is valid. The proof does not infer a
  primal-only lower bound or a query bound.
- Verified the operational dimension argument and the interior planar
  sections used for coupled barriers. The integer minimization of `r+2q`
  subject to `r+dq>=D+1` gives the stated `Psi_d`, including `d=2` and
  remainder zero. The resulting charge is correctly distinguished from an
  attainable formulation frontier.
- Recomputed the shared-ball radial Hessian, effective activity, one-active
  and positive-tail examples, the sharp scalar constants `1-1/sqrt(2)` and
  `2-sqrt(2)`, both head/tail estimates, and the antiderivative. The
  accuracy-dependent weights are explicitly distinguished from fixed-instance
  asymptotics. The dyadic count on each interval is valid; the additional
  interval contributes lower order. The schedule is a movement construction,
  with scalar inversion and data costs separately identified.
- Rechecked the pointwise matrix example, including the inverse diagonal,
  determinant, common-direction norm, and gradient dual norm. Its absence of
  a claimed global integrable barrier is essential and is stated.
- Verified the all-EJA exposed-minor contraction from the quadratic
  representation identity, including the weighted AM–GM allocation and the
  actual weighted reference scale. The same certificate is retained when
  composing with earlier rank frontiers. Neither an arbitrary larger barrier
  parameter nor a minimum over the wrong certificate fiber is substituted.
- Checked the principal-compression Hessian domination via the matrix
  fractional Schur complement, the exposed spectral profile, both continuous
  maximizers and constants, integer rounding, and the finite diagonal-box
  matching-order paths. Fixed rank and growing rank are explicitly separated.
- Recomputed grouped and packed central stationarity with free completion
  entries, Hadamard/AM–GM endpoint estimates, heterogeneous entropy factors,
  and the packed logarithmic-vector contraction. The bounds do allow arbitrary
  feasible completion motion. The referenced matrix epigraph argument gives
  the required gradient parameter on these slices.
- Checked the weighted norm-tree profile and speed, exact arc integral,
  entropy bound, and all terms in the tube-increment argument. Backward
  transport of endpoint residuals and the geometric series give the stated
  `A_{rho,R,m}`. The tube gap correction and parameter threshold are valid.
- Checked the balance-slice certificate, center, full-slice stationarity,
  trace normalization, and arc integral. The lower/upper coefficients agree
  at `sqrt(rho-1)` only for the specified metric, as stated. For the spectral
  slice, von Neumann plus AM–GM gives the claimed determinant bound, and
  the shared/chordal realization uses the identical reduced barrier.
- Independently verified the new weighted tree theorem. The genuine active
  support pairings telescope to the full gap. At the first inactive child,
  orthogonality to the active support direction bounds its axis squared by
  a fixed constant times the gap, and descendants inherit this bound. The
  Lorentz inverse Hessian gives unit squared dual norm for an active support
  logarithm and squared norm two for a determinant logarithm. The combined
  potential therefore has squared dual norm
  `sum_active omega + (1/2)sum_inactive omega`, even before affine
  restriction. For the upper curve, subtree recursion gives exactly the
  prescribed positive determinants and root one. Active block squared
  speeds are `1+O(h+lambda^-2)` and inactive block speeds are exactly
  `2(1/2+1/lambda)^2`; the resulting remainder integrates to `O(log lambda)`.
  The arbitrary reference connection, synchronized product construction,
  zero-weight factors, and central-path excess conclusion follow. Constants
  are correctly allowed to depend on fixed nonzero subtree support norms.

## Sources and attribution

Read the relevant local companion text in `central-path-cost/sections/`
(`06-formulation.tex`, `05-primal-dual.tex`, and `03a-distribution.tex`) and
the earlier manuscript statements supplying minimal ambient dimension,
spectral barrier parameters, and column-packing parameters. Companion
section numbers 5, 9, and 10 match its compiled labels. The substantial
companion overlap is expressly acknowledged, with proofs retained for
standalone reading; the weighted inactive-subtree coefficient is identified
as the specific new result, without an unsupported comprehensive priority
claim.

Consulted the local literature instructions and read-only Hauser–Guler and
Nesterov–Nemirovskii literature records. Checked the primary online texts:

- Nesterov–Todd (2002),
  <https://people.orie.cornell.edu/miketodd/NTRiemann.pdf>, Section 3 and
  Theorem 5.1(c), Theorem 5.2, and Corollary 5.1. These support the classical
  attribution and the allowance for infeasible intermediate points.
- Hauser–Guler,
  <https://arxiv.org/pdf/math/0103196>, Theorem 5.5. Its irreducible-factor
  coefficients are at least one, exactly as used here; it does not classify
  arbitrary coupled barriers on affine slices.

No build or independent numerical experiment was needed for this review;
the substantive checks above were algebraic/proof-level checks of the
frozen source. I found no unresolved major issue.
