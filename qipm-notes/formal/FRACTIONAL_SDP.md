# Explicit fractional SDP spectrum

Source: “Four reduced-Hessian scales,” label `thm:fractional-spectrum`, in
[`conditioning-paper/sections/07-fractional-sdp.tex`](../conditioning-paper/sections/07-fractional-sdp.tex).
The corresponding discussions are in
[`paper/sections/03-conditioning.tex`](../paper/sections/03-conditioning.tex)
and [`paper/sections/04-spectra.tex`](../paper/sections/04-spectra.tex).
Lean sources are in [`QipmFormal/FractionalSDP/`](QipmFormal/FractionalSDP/),
in namespace `QipmFormal.FractionalSDP`.

The target is the actual log-det central path and its equality-reduced
Hessian in the inherited Frobenius metric. The development connects the
optimization problem, directional second derivative, metric, characteristic
polynomial, and asymptotic limits. It includes the restricted problem and
coverage of every sufficiently small central parameter and objective gap.

## Problem and exact center

The full problem minimizes `X₂₂` over real symmetric positive semidefinite
`3 × 3` matrices with `tr X = 1` and `X₃₃ = X₁₂`. The restricted problem
also requires `X₁₃ = X₂₃ = 0`. The central objective on positive-definite
feasible matrices is `−log(det X) + X₂₂/μ`, equivalent to the usual
`X₂₂ − μ log(det X)` for `μ > 0`.

`Geometry.lean` proves that the objective is nonnegative on the PSD cone
and that `diag(1,0,0)` is the unique feasible zero-objective matrix in both
problems. `center_objective_gap` therefore identifies `g` with the actual
objective gap from the attained optimum.

Using one-based manuscript indices, every interior feasible matrix is

\[
X=\begin{pmatrix}1-g-b&b&t\\b&g&e\\t&e&b\end{pmatrix}.
\]

The Lean proof uses a rational path parameter `r = g/b`, called `t` in
`Defs.lean`; it is distinct from the off-block entry `t` above. With
`d = r² + 2r + 3`, the center is

\[
X(r)=\begin{pmatrix}a&b&0\\b&g&0\\0&0&b\end{pmatrix},\qquad
 a=\frac{r+3}{d},\quad b=\frac r d,\quad g=\frac{r^2}{d},
\]
\[
 q=ag-b^2=\frac{r^2(r+2)}{d^2},\qquad
 \mu=\frac{q}{1-b-2g}
     =\frac{r^2(r+2)}{d(3+r-r^2)}.
\]

For `0 < r < 1`, `center_posDef` proves positive definiteness and
`center_unique_minimizer` proves global optimality with its equality case
against every positive-definite feasible matrix in these coordinates.
`feasible_eq_point` proves that the coordinates cover all such matrices, and
`center_unique_minimizer_matrix` states the result directly for matrices.
Thus the proof establishes the unique central point, beyond merely checking
stationarity. `center_unique_fixed_gap` also proves the unique minimizer
of the barrier on its objective slice. The same center belongs to the
restricted problem and is its unique minimizer as well.

The closed form

\[
 b=\frac{-g+\sqrt{3g-2g^2}}3
\]

is `center_positive_root`. It agrees with the manuscript's formula.

`Parameter.lean` proves that every gap and every central parameter in
`(0, 1/6)` occurs for some `r ∈ (0,1)`. This follows from continuity and
endpoint values, without assuming an inverse formula or monotonicity.
The bounds `r² ≤ 6g(r)` and `r² ≤ 12μ(r)` imply that the selected inverse
parameters `gapParameter` and `muParameter` tend to zero through positive
values. Consequently, the asymptotic statements apply to the entire tail,
not just to a chosen sequence of centers.

`Paper.lean` defines `centralPoint μ` and `gapCenter g` using these inverse
choices. `centralPoint_unique_minimizer` states uniqueness for every
`μ ∈ (0,1/6)` directly against every positive-definite matrix satisfying
the original equalities.

## Hessian and metric

`tangent_characterization` covers the complete four-dimensional equality
tangent space. `restricted_tangent_characterization` covers the restricted
two-dimensional space. In coordinates `(u,v,w,z)` their ambient matrix is

\[
 U=\begin{pmatrix}-u-v&u&w\\u&v&z\\w&z&u\end{pmatrix},\qquad
 \|U\|_F^2=4u^2+2uv+2v^2+2w^2+2z^2.
\]

`center_logdet_second` computes the actual derivative of the first
derivative of `s ↦ −log(det(X(r) + sU))` at zero. It is not a definition
of the Hessian quadratic form. `reducedOperator_second_derivative` identifies
this derivative with the Frobenius pairing against `reducedOperator r`;
`reducedOperator_symmetric` proves symmetry in that same metric.
`coordinateTangent_injective` and `coordinateTangent_range` identify its
coordinate space with the full equality tangent space.

`logdet_contDiffAt` proves smoothness of the actual matrix function near
each center. `reducedOperator_iteratedFDeriv` identifies the operator's
quadratic form with its second Fréchet derivative (`iteratedFDeriv ℝ 2`),
using the Frobenius matrix norm. `restrictedOperator_iteratedFDeriv` gives
the corresponding identity on the restricted tangent space.
`tangent_eigenvalue_iff` and `restricted_tangent_eigenvalue_iff` also realize
each spectral value by a nonzero feasible tangent matrix and exclude any
other tangent eigenvalues.

For the `(b,g)` block, write `q_b = −g−2b`, `q_g = 1−b−2g`. Its coordinate
Hessian and metric are

\[
 K=\begin{pmatrix}
 b^{-2}+q_b^2/q^2+2/q&q_bq_g/q^2+1/q\\
 q_bq_g/q^2+1/q&q_g^2/q^2+2/q
 \end{pmatrix},\qquad
 G=\begin{pmatrix}4&1\\1&2\end{pmatrix}.
\]

`gram_mul_diagOperator` proves `G · diagOperator = K`, and
`diagOperator_generalized_eigenvector` equates its eigenvector equation
with `Kv = λGv`. For the off-block coordinates, the Frobenius metric is
`2I`, so the operator is `A₂⁻¹/b`, where
`A₂ = [[a,b],[b,g]]`. Using eigenvalues of `K` alone would give the wrong
normalization. The development includes this metric conversion explicitly.

`LimitsEntries.lean` also verifies the intermediate asymptotic calculations
in the manuscript: `a → 1`, `b/√(g/3) → 1`, `b/√(μ/2) → 1`,
`q/g → 2/3`, `μ/g → 2/3`, and `q/μ → 1`. For the coordinate Hessian
it proves `μ K_bb → 6`, `μ√μ K_bg → −√2`, `μ² K_gg → 1`, and
`μ³ det K → 4`.

## Complete spectra and asymptotics

`reduced_charpoly` factors the degree-four characteristic polynomial as

\[
 (x-\lambda_{\mathrm{diag},-})(x-\lambda_{\mathrm{diag},+})
 (x-\lambda_{\mathrm{off},-})(x-\lambda_{\mathrm{off},+}).
\]

`diag_charpoly` gives the restricted problem's two factors.
These identities account for algebraic multiplicities, while
`mem_reduced_spectrum_iff` and `mem_diag_spectrum_iff` identify the spectra.
`eventually_spectrum_positive` and `eventually_spectrum_ordered` give
positivity and strict increasing order on a sufficiently small tail:

\[
 \lambda_{\mathrm{off},-}<\lambda_{\mathrm{diag},-}
 <\lambda_{\mathrm{off},+}<\lambda_{\mathrm{diag},+}.
\]

Thus all four eigenvalues are eventually simple. Their limits are:

| Ordered eigenvalue | Scaled limit as `μ ↓ 0` | Lean result along the rational parameter |
|---|---|---|
| `λ₁ = offLow` | `√μ λ₁ → √2` | `limit_mu_offLow` |
| `λ₂ = diagLow` | `μ λ₂ → 1` | `limit_mu_diagLow` |
| `λ₃ = offHigh` | `μ√μ λ₃ → √2` | `limit_mu_offHigh` |
| `λ₄ = diagHigh` | `μ² λ₄ → 4/7` | `limit_mu_diagHigh` |

The resulting condition-number limits are

\[
 \mu^{3/2}\kappa\to\frac{2\sqrt2}{7},\qquad
 g^{3/2}\kappa\to\frac{3\sqrt3}{7},
\]
\[
 \mu\kappa_0\to\frac47,\qquad g\kappa_0\to\frac67.
\]

They are `limit_mu_condition`, `limit_gap_condition`,
`limit_mu_restricted_condition`, and `limit_gap_restricted_condition`.
Here `κ = diagHigh/offLow` and `κ₀ = diagHigh/diagLow` on the ordered,
positive tail. The restricted spectrum retains exactly the `(b,g)` block.

`SpectralCondition.lean` defines condition numbers as the ratio of the
supremum and infimum of the actual operator spectrum. It proves that these
extrema are the displayed eigenvalue branches on the ordered tail and
transfers all four limits to those definitions. This closes the connection
between the branch-ratio calculations and spectral condition numbers.

`Paper.lean` states the whole-tail results in the original parameters:
`centralPoint_spectrum`, `centralPoint_restricted_spectrum`,
`centralEigenvalues_ordered`, and `centralEigenvalues_positive` identify and
order the eigenvalues; `paper_first_eigenvalue` through
`paper_fourth_eigenvalue` prove the four scaled limits.
`paper_mu_spectralCondition`, `paper_gap_spectralCondition`,
`paper_mu_restrictedSpectralCondition`, and
`paper_gap_restrictedSpectralCondition` give the corresponding limits using
the extrema of the actual operator spectra.

## Source map and proof choices

| Module | Responsibility |
|---|---|
| `Defs.lean` | Rational center, coordinate matrices, Hessian entries, and scalar roots. |
| `Center.lean` | Feasibility, positive definiteness, stationarity, and closed-form center. |
| `Geometry.lean` | Attained unique zero optimum and identification of the objective gap. |
| `CenterOptimality.lean` | Global minimization and equality cases over the full interior and fixed objective slices. |
| `Parameter.lean` | Coverage of small `μ` and `g`, inverse choices, and their limits. |
| `HessianCalculus.lean` | Scalar logarithm and determinant-polynomial differentiation; connection between a line derivative and the second Fréchet derivative. |
| `Hessian.lean` | Complete tangent spaces, Frobenius metric, determinant along a line, smoothness, and actual second Fréchet derivative. |
| `Spectrum.lean` | Metric conversion, exact characteristic polynomials, and spectra. |
| `SpectrumBridge.lean` | Identification of both spectral operators with the actual Frobenius-metric Hessians; realization by nonzero tangent eigenvectors. |
| `Limits.lean` | Rational-parameter spectral limits and eventual positivity. |
| `LimitsTransfer.lean` | Leading constants in `μ` and `g`, strict ordering, and both condition numbers. |
| `LimitsEntries.lean` | Central-entry limits, coordinate-Hessian limits, and its determinant limit. |
| `SpectralCondition.lean` | Actual spectral extrema, their identification with the computed branches, and condition-number limits. |
| `Paper.lean` | Original-parameter central point, uniqueness, Hessian, spectrum, ordering, and full-tail limits. |

The formal proof uses the rational parametrization to reduce the main
asymptotic calculations to limits of rational functions and square roots.
Global minimization follows from explicit determinant inequalities and the
scalar logarithm tangent inequality, including equality cases. This avoids
building general self-concordant-barrier or matrix log-det convexity theory.

No leading constant in the conditioning paper required correction.
The main paper's former numerical `0.40` is now the exact `2√2/7`, and its
four-window observation is stated with proved constants. The conditioning
paper now includes the rational parametrization and explicit tail coverage.

## Scope and reproduction

This verifies the explicit log-barrier spectral theorem. It does not verify
these other claims from the same section or related papers:

- Singularity degree two, facial reduction, or failure of strict complementarity.
- Sharp sublevel diameters and the general diameter law.
- Transfer to every fixed self-concordant barrier.
- Quantum running time, oracle constructions, or iterative-solver guarantees.

Those remain separate results. In particular, the four log-barrier constants
are not claimed to be invariant under a change of barrier.

From `formal/`, run:

```sh
env PATH="$HOME/.elan/bin:$PATH" lake build
./scripts/verify.sh
```

The verification contract is in [README.md](README.md): every imported
project declaration is checked against the axiom allowlist `propext`,
`Classical.choice`, and `Quot.sound`; project axioms and dependencies on
`sorryAx` or native evaluation are rejected. The optional
`./scripts/verify.sh --replay` rechecks the import closure in a fresh Lean
kernel environment.

## Validation

The integrated build and axiom audit passed on 2026-09-20 for 2,549 project
declarations, including all 14 modules in this development. Only `propext`,
`Classical.choice`, and `Quot.sound` occur in their axiom dependencies.
Two independent reviews checked the correspondence between the manuscript
and the final Lean statements. Both affected manuscripts were rebuilt.
The optional fresh-environment kernel replay was not run.
