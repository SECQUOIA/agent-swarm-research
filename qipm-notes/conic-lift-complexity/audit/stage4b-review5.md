# Stage 4B independent review 5

Reviewed all of `09a-whole-rows.tex`, `09b-face-sharing.tex`,
`09c-balance-slices.tex`, `09d-lp-power.tex`, and
`09e-spectral-chordal.tex`, together with their author handoff, relevant
source dispositions, bibliography entries, integration in `main.tex`, and
the foundational curvature, normalized-base topology, and bounded-fiber
projection results on which the new proofs rely. No other reviewer report
was read, and this review was not delegated. Manuscript files were not
modified.

**Finding: no major or minor issue identified.**

## Spectral and completion checks

- Independently reconstructed the spectral contact rank in Proposition
  `prop:spectral-contact`. In the standard contact coordinates, the
  off-axis skew-Hermitian, rectangular-tail, and imaginary-diagonal
  channels have real dimensions delta(r-1), delta(c-r), and delta-1.
  Their total is delta*c-1. The quaternionic gauge removes the common
  unit-scalar redundancy; the proof uses real pairings and does not
  require invalid quaternionic trace identities. The zero-rank real
  scalar case is allowed by the statement.
- Checked the cross-contact annihilation argument and the direct-sum
  face bound. It uses independent first derivatives, so neither a
  second derivative of a factor map nor a nonsingular full spectral
  contact pairing is being assumed. The incidence and capacity totals
  follow with the stated ceilings. No attainment or global topology
  consequence is claimed for these necessary local budgets.
- Verified the rank-h spectral support face: the supported singular
  corner and both cross rectangles are fixed, leaving
  delta(r-h)(c-h) free real dimensions. Its smallest codimension is
  delta(r+c-1), at h=1. This agrees with the universal whole-row
  theorem and all dimension/face caps in `cor:spectral-caps`.
- Checked the non-logarithmically-homogeneous lower bound in
  `thm:shared-spectral-parameter`, rather than inferring it from
  logarithmic degree. The displayed directions lie in the infinity
  norm cone; their positive coefficients sum exactly to the stated
  interior point. Every backward endpoint lies on the boundary. The
  recession certificate tends to r+1 and remains a single valid
  certificate after direct-sum placement, proving the coupled-product
  lower bound. The real diagonal sections meet the full interiors.
- Independently differentiated the fixed-scale spectral barrier. The
  Hessian preserves its real singular-diagonal subspace; the gradient
  lies there. Its squared dual norm is the stated sum
  2*sigma_j^2/(1+sigma_j^2). The cube section supplies the matching
  arbitrary-barrier lower bound. The restriction of a Hermitian log
  determinant establishes ordinary self-concordance, while this
  gradient calculation establishes the smaller sharp parameter.
- Verified closedness of the completion cone from bounded diagonal
  completions, the sign and additive constant of the Legendre
  conjugate, and uniqueness of the positive-definite maxdet
  completion. The diagonal orthant is a valid boundary-inheriting
  section, so the graph-order lower bound also permits coupled
  barriers. The clique/separator identity is asserted only for
  chordal graphs and counts separators with multiplicity.
- Checked block-star dimensions over both fields, its clique-tree
  determinant identity, the full rank-one polar certificate, and its
  invariance under the common phase of u and v. The identity-block
  section gives the claimed literal product of spectral balls.
  Sylvester's identity justifies either matrix orientation and the
  minimum of the two side dimensions in the parameter.
- Verified the displayed gradient, Hessian, Newton matrix, and residual
  in the final subsection. Their equality is stated after fixing the
  same retained coordinates, barrier, affine map, and objective. The
  manuscript correctly separates this equality from constructing an
  oracle from ambient data and from the cost of a general Newton solve.

## Checks on the other four sections

- The whole-row rank and contact-cylinder arguments work without
  regularity. The extremal-polar decomposition correctly controls
  nonextreme supporting normals of the homogenization cone. The
  factorization version of minimum-dimension rigidity uses both
  spanning canonical slack families, and the affine-lift version
  handles the nonzero hyperplane before extending its projection
  linearly. The normalized-base intersection-graph argument applies
  even when the extreme set is not closed. The recession criterion
  uses compact sublevels and a fixed vertical recession direction;
  the subsequent polytope transfer and the escaping-disk obstruction
  have the stated distinct scopes.
- The face-sharing proof obtains genuine direct sums, not merely a sum
  of dimensions. Exact-active-label pieces are clopen in the relevant
  closed equality locus, so their compact neighborhoods support the
  global cup-product argument. The piecewise count and capacity
  formulas include the cap transition. The dimension lower bound is
  monotone in the actual number of factors. Its ambient barrier lower
  bound uses product wedge sections, so it does not assume separable
  or logarithmically homogeneous competing barriers. The sharp-square
  example's dual, exposed-face dimensions, and star-completion barrier
  all agree.
- For balance slices, the minimal-face criterion gives exactly the
  listed one- and two-block extreme points. The sign-region paths and
  a second block connect the real rank-two exceptional zero set as
  well. The Albert chart uses only the associative subalgebra generated
  by its two octonions, and its limiting zero ray is correctly
  identified. The diagonal orthant/simplex supplies both lower bounds;
  the restricted gradient norm supplies rho-1 on the trace-one slice.
  The alternate classical moment is treated separately, and the
  matched-dimension comparison is explicitly between different bodies.
  The failed-log example's derivatives 13/4 and 25 check directly.
- The norm-ball capacity lower bound uses a smooth positive-curvature
  patch away from coordinate zeros. The chain realizes the precise
  count and total dimension, and zero-coordinate padding preserves
  strict feasibility. The global theorem differentiates primal and
  polar boundary charts independently and uses the reviewed covering
  theorem without differentiating the polarity map. Young's factors
  have the stated whole-slice multiplier normalization. The N=2
  power-cone exclusion correctly separates the non-C2-ray obstruction
  from the flat-axis obstruction for the Lorentz case. The generalized
  power-cone Hessian is the sum of a weighted variance and a spherical
  form; their common nullspace on the normalized tangent space is
  zero, including the m=1 or k=1 edge cases retained in the theorem.

## Literature and coverage

Read the local Fawzi--Saunderson and Grone--Johnson--Sa--Wolkowicz
literature records, then independently checked the primary sources:

- Fawzi--Saunderson, Theorem 3.9, states the recession-direction bound
  for any self-concordant barrier, with exactly the boundary and
  positive-coefficient hypotheses used here:
  https://arxiv.org/html/2205.04581v3.
- Andersen--Dahl--Vandenberghe, Section 1.2, defines the same signed
  conjugate and its maxdet-completion interpretation:
  https://arxiv.org/pdf/1203.2742.
- Coey's thesis, Section 2.6.1, equations (2.69a)--(2.69b), explicitly
  includes the real/complex rectangular spectral cone and parameter
  one plus its row dimension:
  https://chriscoey.github.io/assets/pdf/phd_thesis.pdf.

These checks support the manuscript's use and attribution of the
classical barrier formulas. The primary recession theorem also confirms
that the stronger arbitrary-barrier scope of the new explicit
certificate is justified. No unsupported priority claim was found.

The Stage 4B source dispositions distinguish completed formulation
results from the movement calculations routed to Stage 5 and the
nonsymmetric barrier questions routed to Stage 4C. Those deferrals are
explicit and consistent with the staged task; they are not presented
as completed results of this stage. The five sections are integrated
before the appendix and their forward dependencies are identified.
The abstract and whole-paper synthesis remain part of the later
integration stage, not an omission concealed by this review.
