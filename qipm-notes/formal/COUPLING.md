# Exact-center Newton coupling

Source: Theorem 5.1 and Proposition 5.2, the exact-center coupling subsection
and sparse sharpness witnesses in
[`paper/sections/05-beyond-kappa.tex`](../paper/sections/05-beyond-kappa.tex).
The Lean development is in [`QipmFormal/Coupling/`](QipmFormal/Coupling/).

## Mathematical scope

For the active/inactive decomposition of an exact LP normal equation, write

\[
H_\mu=\begin{pmatrix}
\mu^{-1}C_\mu+\mu D_\mu^U&\mu F_\mu^*\\
\mu F_\mu&\mu E_\mu
\end{pmatrix},\qquad b\in U\setminus\{0\}.
\]

The Schur variables are those in the manuscript, not independently chosen
approximations. The development checks the actual inverse identities

\[
H_\mu^{-1}b=\mu(p_\mu,-g_\mu),\qquad
H_\mu^{-2}b=(\mu^2q_\mu,-E_\mu^{-1}g_\mu
                 -\mu^2E_\mu^{-1}F_\mu q_\mu).
\]

The second formula has a potentially cancelling lower block. Its lower norm
bound uses the upper block as well. This yields the two-sided estimates

\[
\|H_\mu^{-1}b\|=\Theta(\mu),\qquad
\|H_\mu^{-2}b\|=\Theta(\|g_\mu\|+\mu^2).
\]

Consequently a norm-tight normalization gives

\[
\xi=\Theta(1),\qquad
\rho=\Theta(1+\|g_\mu\|/\mu^2).
\]

The non-tight formula retains the normalization factor:
`rho = Theta(alpha(mu) * (mu + norm(g(mu))/mu))`.
Bounded filtering is equivalent to `g(mu) = O(mu^2)`. A continuous zero limit
is precisely the condition for improvement to `o(mu^-2)`. Differentiability
at a zero limit gives `O(mu^-1)` filtering. For an analytic coupling, a
nonzero first derivative gives `Theta(mu^-1)`; a zero constant and first
derivative give bounded filtering.

## Representation and assumptions

- `LP.lean` constructs `A * diagonal(x/s) * A.transpose` and derives its
  active/inactive split from coordinatewise complementarity. It derives the
  centering RHS from the actual linearized primal, dual, and complementarity
  equations. `Paper.lean` checks invariance under nonzero RHS scaling.
- The block algebra uses real linear maps. Its inverse is constructed by
  proving bijectivity, rather than postulating the displayed solution.
  The inactive block and the Schur factor are explicitly invertible;
  `positive_blocks_have_factors` derives both factors from positivity of
  the original block quadratic form in finite dimension.
- `blockNorm u v = sqrt(norm(u)^2 + norm(v)^2)` is the Euclidean norm of
  an orthogonal sum. The algebraic product type's default maximum norm is
  not substituted for this norm in the inverse parameters.
- The nonzero limiting second-inverse coefficient follows from the adjoint
  relation and self-adjointness of the inactive block. The proved inner
  product is `norm(p)^2 + norm(g)^2`; it is positive for nonzero `p`.
- `UniformBounds` bounds the Schur variables and inactive inverse. The
  finite norm estimates derive the inverse and parameter bounds from this
  data. `uniformBounds_of_block_continuity` supplies the bounds from actual
  block continuity and the nonzero RHS. It does not assume the conclusion
  about filtering. Continuous and analytic inversion also derive the
  regularity of the Schur variables from that of the block data.
- Asymptotic statements use Lean's `IsBigO`, `IsLittleO`, and `IsTheta`.
  Endpoint behavior is taken through positive parameters; values at zero
  need not represent a nonsingular Newton matrix.

## Claim map

Names are in `QipmFormal.Coupling`; family results additionally use
`BlockFamily`, and the concrete LP results use `Witnesses`.

| Claim | File and principal declarations |
|---|---|
| Actual LP normal split and centering RHS | [LP.lean](QipmFormal/Coupling/LP.lean): `normalMatrix_split`, `exact_center_newton_rhs` |
| Active support, nonzero RHS, Gram positivity | [LPGeometry.lean](QipmFormal/Coupling/LPGeometry.lean): `supported_rhs_mem_active_range`, `rhs_ne_zero_of_strict_dual`, `weightedGram_pos_on_range`, `inactive_weightedGram_pos`, `active_weightedGram_eq_mask` |
| Orthogonal realization of the original normal operator | [Realization.lean](QipmFormal/Coupling/Realization.lean), namespace `OrthogonalRealization`: `coordinates_norm`, `offDiagonal_adjoint`, `normalOperator_coordinates`, `realizeFamily_valid`, `realized_firstInverseNorm`, `realized_secondInverseNorm` |
| Invertibility from the original positive quadratic form | [Positivity.lean](QipmFormal/Coupling/Positivity.lean): `positive_blocks_have_factors` |
| Actual inverse and second inverse | [Block.lean](QipmFormal/Coupling/Block.lean): `blockOperator_bijective`, `first_inverse`, `second_inverse` |
| Noncancellation and exceptional RHS space | `Block.lean`: `coupling_inner_identity`, `couplingQ_ne_zero`, `couplingG_eq_zero_iff`, `couplingG_all_eq_zero_iff` |
| Finite Euclidean inverse-norm estimates | [Bounds.lean](QipmFormal/Coupling/Bounds.lean): `firstInverse_bounds`, `secondInverse_bounds` |
| Two-sided scales and rate criteria | [Asymptotics.lean](QipmFormal/Coupling/Asymptotics.lean): `filtering_tight`, `filtering_nontight`, `filtering_bounded_iff`, `filtering_full_scale`, `filtering_improves_iff` |
| Composition for the actual inverse parameters | [Paper.lean](QipmFormal/Coupling/Paper.lean): `xi_tight`, `rho_tight`, `rho_nontight`, `rho_bounded_iff`, `rho_full_scale`, `rho_improves_iff`, `xi_smul`, `rho_smul` |
| Actual block continuity and analyticity | [Regularity.lean](QipmFormal/Coupling/Regularity.lean): `continuous_schurFactor`, `analytic_schurFactor`, `continuous_coupling_variables`, `uniformBounds_of_block_continuity`, `analytic_coupling` |
| Primitive endpoint coupling and actual parameter conclusions | `Regularity.lean`: `endpoint_coupling_formula`, `exact_center_continuous_law`, `rho_firstOrder_bound`, `rho_analytic_zero_cases`, `rho_bounded_iff_deriv_zero` |
| Derivative-dependent coupling rates | `Regularity.lean`: `coupling_isBigO_of_differentiable`, `coupling_isTheta_of_hasDerivAt`, `coupling_isBigO_sq_of_analytic`, `analytic_coupling_rate_cases` |
| Actual operator-norm and condition-number scales | [Spectrum.lean](QipmFormal/Coupling/Spectrum.lean): `ringInverse_newtonCLM`, `newton_norm_theta`, `newton_condition_theta`, `normTight_theta_inv` |
| Sparse LP centers, optima, inverses, parameter correspondence | [Witnesses.lean](QipmFormal/Coupling/Witnesses.lean): `coupled_dual_feasible`, `coupled_complementarity`, `coupled_unique_optimum`, `decoupled_unique_optimum`, `coupled_normal`, `coupled_inverse`, `coupled_normalized_direction`, `paperT_domain`, `paperT_parameter` |
| Scalar spectral certificates and slow-eigenvector overlap | [WitnessLimits.lean](QipmFormal/Coupling/WitnessLimits.lean): `scaledKappa_eq`, `xiCertificate_eq`, `scaledRhoCertificate_eq`, `slowEigenvector_eigen`, `slowAmplitude_eq_overlap`, `slowAmplitude_limit` |
| Complete spectra and induced Euclidean norms | [WitnessSpectrum.lean](QipmFormal/Coupling/WitnessSpectrum.lean): `coupled_spectrum`, `coupled_operatorNorm`, `coupled_inverse_operatorNorm`, `coupled_conditionNumber`, `decoupled_conditionNumber` |
| Actual LP parameter limits in the paper's central parameter | [WitnessParameters.lean](QipmFormal/Coupling/WitnessParameters.lean): `paperH_normal`, `coupled_parameter_certificates`, `coupled_parameter_limits`, `decoupled_parameters`, `paperSlowVector_eigen`, `slowSolutionAmplitude_limit` |

The formalization separates the classical LP facts, the block operator
calculation, and the consequences of block regularity. Its theorem statements
retain the hypotheses at each interface. It is not one unconditional theorem
constructing an analytic central path from arbitrary LP input.
The orthogonal realization itself is proved: the coordinates preserve the
original inner product and both inverse norms, and the projected blocks
have the required adjoint relations. The original normal operator is
identified with the block family by conjugation through these coordinates.
`realized_xi` and `realized_rho` transfer the parameter formulas back to
the actual inverse acting in the original space.

## Sparse witnesses

The coupled witness is first represented by its primal coordinate
`0 < t < 2/3`, with `mu(t) = 2*t*(1-t)/(2-3*t)`. Its actual primal and
dual feasibility and positive complementarity are proved. `paperT` is the
manuscript's radical formula; it lies in that interval for every positive
`mu`, satisfies `mu(paperT(mu)) = mu`, and tends to zero as `mu` tends to zero.
Thus the final limits concern the paper's central parameter, not only a
reparameterized collection of examples.
`paperT_quadratic_error` checks the displayed `t(mu) = mu + O(mu^2)`
expansion. The actual dual and slack limits and the displayed second-inverse
vector limit are `coupled_dual_limit_mu`, `coupled_slack_limit_mu`, and
`coupled_second_limit_mu`. Both optimal dual intervals are also characterized;
the proof does not replace them with a false dual uniqueness claim.

The formal parameters use `Matrix.toEuclideanCLM` for the operator norm and
`WithLp 2` for the vector norm. The complete spectra identify the positive
largest and smallest eigenvalues with the explicit roots. The coupled
limits are

\[
\mu^2\kappa(H_\mu)\to\tfrac12,\qquad
\xi(H_\mu,b)\to\tfrac{\sqrt5}{2},\qquad
\mu^2\rho(H_\mu,b)\to\tfrac1{2\sqrt5}.
\]

For the decoupled witness, Lean gives the exact formulas under `mu > 0`
and `2*mu^2 <= 1`. This is the same tail as `mu <= 1/sqrt(2)`.
The witness checks include the complete matrix inverse and its action
twice on the RHS, rather than just the roots of a characteristic polynomial.

## Corrections and qualifications

The formalization and source review prompted these manuscript changes:

1. The nonzero RHS is explicit, with the LP argument supplying it from
   strict dual feasibility and optimality.
2. The lower bound for the second inverse now explains why cancellation
   cannot invalidate the filtering law.
3. The analytic alternatives are expressed using the value and derivative
   at zero. This covers identically zero coupling without requiring a first
   nonzero Taylor coefficient to exist.
4. The coupled witness's normalized coordinate direction is exactly
   `(2,-1)/sqrt(5)`. Its amplitude in the moving slow eigenspace **tends to**
   `1/sqrt(5)`; that amplitude is not asserted to be constant.
5. The decoupled formulas `kappa = 1/(2*mu^2)` and `xi = rho = 1`, with
   normalization equal to the operator norm, require `0 < mu <= 1/sqrt(2)`.

The historical supporting note now carries a correction notice. In particular,
its arbitrary intermediate-power discussion and its claim of a unique
strictly complementary optimum are obsolete: the primal optimum is unique,
but the dual optima form an interval.

The other three current manuscripts do not state this coupling theorem or
these witness conclusions. Their unrelated uses of coupling require no edits.

## Scope boundary

General LP central-path existence, convergence, and boundary analyticity
remain mathematical inputs. Lean checks the consequences of the stated block
regularity; it does not reconstruct Halická's theorem from arbitrary LP data.
The identification of the filtering parameter with the cited QLS algorithm
is source correspondence, not a formalization of that quantum algorithm.

The later truncation transition, spectral-dimension laws, equilibration,
block-encoding construction, accuracy-dependent query counts, and end-to-end
QIPM runtime are outside this verification. A parameter estimate is not by
itself a quantum algorithm or a query lower bound.

## Reproduction

From `formal/`, in the repository environment:

```sh
conda run -n qipm --live-stream bash scripts/verify.sh
```

The build kernel-checks the proofs. The integrated audit rejects project
axioms, `sorryAx`, and `Lean.ofReduceBool`; only `propext`, `Classical.choice`,
and `Quot.sound` are permitted. The optional `--replay` is a separate
fresh-environment replay of the import closure.

## Validation completed on 2026-09-20

- All 14 coupling modules are included in the integrated project import
  closure. The final build completed without warnings.
- The integrated axiom audit passed for **2028 project declarations**,
  covering this development and all existing formalization topics. Every
  audited declaration uses only the three allowed standard axioms.
- Independent mathematical and statement reviews checked the LP/block
  correspondence, positivity, inverse identities, norms, regularity,
  actual witness parameters, and documentation. Earlier coverage concerns
  were closed by the orthogonal realization and the actual operator-norm
  and central-parameter bridges. No unresolved substantive issue remained
  within the reviewed scope.
- The main manuscript rebuilt to **198 pages**, without LaTeX warnings,
  unresolved references or citations, or overfull/underfull boxes. Pages
  **41–43**, containing the theorem, sparse witnesses, and verification
  scope, were rendered and visually checked.
- Report links and inclusion of every coupling module in the audit closure
  were checked. `git diff --check` passed.
- The optional fresh-environment replay was **not run**. The completed
  checks are the project build and declaration-level axiom audit.
