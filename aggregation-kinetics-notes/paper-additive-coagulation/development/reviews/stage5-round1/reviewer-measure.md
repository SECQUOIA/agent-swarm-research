# Stage 5 independent review — measure and identification

Reviewed the frozen Stage 5 source, including `sections/fourier-identification.tex`, `appendices/observation-design.tex`, the introduction, discussion, `main.tex`, added bibliography entries, README, coverage map, and author handoff. I also checked the accepted bounded-test normalized log equation, solution definition, and half-moment estimate where the new proofs use them. All 36 files listed in `stage5-round1/snapshot.json` match their recorded SHA-256 hashes. I did not read another current Stage 5 report, communicate with another reviewer, change manuscript sources or data, or run a shared build.

The new theorems are mathematically sound under their stated assumptions. There is one minor inaccurate boundary claim after the identification theorem.

## Actionable findings

### 1. S5-MEASURE-01 — MINOR: strict daughter reduction is not essential to identifiability under both normalization constraints

**Location:** `sections/fourier-identification.tex:211–212`, immediately after `thm:fourier-identification`; the corresponding “strictly smaller daughter boundary” description in `development/COVERAGE.md:55` should reflect the correction.

The text says: “Strictly smaller daughters are essential: a daughter atom at one would produce an invisible jump at zero.” The observation about the zero jump is correct for an unrestricted jump measure, and the support hypothesis in `lem:one-sided` is correct. But the assertion of essentiality is too strong for the normalized daughter class used here. If one allows a finite daughter measure on `(0,1]` while retaining both

\[
B((0,1])=2,\qquad \int\theta\,B(d\theta)=1,
\]

then exact local exponent data still identify the entire daughter measure and the selection rate whenever the rate is positive.

Indeed, write

\[
\nu_- = \sigma(\log)_\#\bigl(B|_{(0,1)}\bigr).
\]

The one-sided lemma identifies this visible measure from the exponent. The two constraints then imply

\[
\int_{(-\infty,0)}(1-e^y)\,\nu_-(dy)
 =\sigma\int_{(0,1]}(1-\theta)\,B(d\theta)
 =\sigma.
\]

Thus the rate is determined even though half the visible jump mass is no longer the correct rate formula. For positive rate,

\[
B=\sigma^{-1}(\exp)_\#\nu_-
 +\left(2-\frac{\nu_-((-\infty,0))}{\sigma}\right)\delta_1.
\]

All integrands in this argument are bounded, so no logarithmic moment is needed. An example in the enlarged class is `B = (1/2) delta_1 + (3/2) delta_(1/3)`: its invisible atom is recovered by the displayed constraints.

**Suggested fix:** Retain the paper's existing `(0,1)` scope, but replace “essential” with the precise statement that excluding an atom at one makes the jump measure directly identifiable by `lem:one-sided` and permits the formula `sigma = nu((-infinity,0))/2`. A short sentence can acknowledge that, if fraction one were allowed while both daughter constraints were retained, the constraints would recover its otherwise invisible mass. There is no need to extend the formal theorem or any forward construction. Update the coverage description if it is intended to claim a necessary identifiability boundary.

**Impact:** This is a qualification of the explanatory paragraph, not a defect in any stated theorem or the sampling analysis.

## Independent mathematical checks

- **Weak-measure Fourier equation:** Real and imaginary parts of `exp(ik log x)` are admissible bounded Borel tests. The coagulation source is absolutely integrable locally using finite number and conserved mass. Its stronger paired-increment bound uses `sqrt(xy)`, whose double integral is `H(t)^2`; it does not split the increment into two unbounded logarithmic integrals.
- **Factorization and continuity:** Integrating `exp(-s psi) r_s` gives the stated denominator `delta = omega + Re psi` and both remainders with the correct exponents. The estimates are uniform on a compact neighborhood of zero. Uniform convergence of the continuous finite-time functions proves amplitude continuity, and its value one at zero supplies local nonvanishing. This requires neither initial nor daughter log moments. No positive definiteness or independent random shift is used.
- **Late-time quotient:** The denominator is bounded before division. Subtracting the two amplitude errors gives exactly the factor `exp(h Re psi)(1 + exp(-delta h))` in the bias bound. The continuous logarithm anchored at zero is unambiguous on the stated neighborhood.
- **One-sided uniqueness:** The lower half-plane has the correct sign: for `y <= 0` and `Im z < 0`, `|exp(izy)| <= 1`. Interior damping bounds all powers of `|y|`, while dominated convergence gives continuity to the boundary. Schwarz reflection across an interval of zero boundary values, the identity theorem, and Fourier uniqueness for finite signed measures establish the lemma. Subtracting the signed mass at zero and finally restricting to the open negative half-line are both necessary and correctly performed.
- **Structural observations:** Intersecting candidate models' neighborhoods is sufficient for the uniqueness argument. The theorem distinguishes zero selection, separate mass/count observations for coagulation recovery, expected daughters rather than daughter correlations, and exact frequency continua. The moving-atom example has variation norm four and uniformly convergent exponents on bounded frequency intervals, so the stated strong-metric instability is valid.
- **Sampling:** Hoeffding's bound for each real or imaginary component at threshold `epsilon/sqrt(2)` is `2 exp(-n epsilon^2/4)`. The four-component union bound gives the displayed constant eight. Both quotient identities and both denominator bounds are correct. The sufficient time schedule balances `exp(-delta t)` against `epsilon exp(dt)` because `delta+d=omega`; it eventually meets the signal condition, including when `d=0`. The certificate remains pointwise, with predetermined observations, and does not assert simultaneous frequency control or a finite-reactor sampling approximation.
- **Finite-shell converse:** The relatively open positive shell justifies polynomial continuation to the full affine space. The restricted Hessian gives `Q K Q=0`. Direct expansion of the proposed `A_0` gives `C^T A_0+A_0^T C=K`; the residual lies in the row space of `C`, and the specified skew correction has `L^T h=gamma`. Full row rank and `h != 0` are used where required. The rank bound is properly distinguished from sufficiency.
- **Trajectory caveat:** The continuum two-constraint family supplies the displayed scalar count equation. Under the explicitly conditional valid mass-conserving balance and locally integrable coefficient, initial count `c` is preserved. The text does not infer a continuum converse or a new existence theorem from the finite-dimensional result.
- **Dilution and tomography:** Substitution into the quadratic rate verifies the one-concentration additive gauge, the two-concentration unknown-source gauge, and its elimination at a third concentration. The monodisperse/equal-mixture formulas recover every symmetric grid coefficient, including diagonal entries. The measurement count matches the dimension of the open finite-dimensional parameter space. The stated deterministic error constants, source interpolation constant seven, and finite-difference minimum follow directly from the linear formulas and Taylor's estimate. The text states the required curvature, preparation, and coefficient-preservation hypotheses.
- **Integration and attribution:** The introduction and discussion distinguish auxiliary paths, physical particles, and independent continuum samples; they preserve the accepted limitations on critical-tail rates, logarithmic limits, and finite-population comparison. The direct two-time quotient/logarithm antecedent is present in [Garnier, Section 2.2](https://arxiv.org/html/2405.10588v1). The descriptions of independent log-size profile sampling and Fourier estimation agree with [Hoang et al., Sections 3.1.1–3.1.4](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf). The narrower asymptotic-profile and short-time attribution agrees with the primary records for [Doumic–Escobedo–Tournus 2018](https://arxiv.org/abs/1804.08945) and [2024](https://www.numdam.org/articles/10.5802/ahl.207/). No current-source novelty or priority claim depends on the repository review notes.

## Optional preferences

None. No additional theorem, numerical experiment, or change to the accepted simulator is needed for this Stage 5 review.

**MAJOR issue count: 0. MINOR issue count: 1. Recommendation: accept Stage 5 after correcting S5-MEASURE-01.**
