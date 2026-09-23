# Stage 1 independent review: measure construction and whole-draft check

I reviewed `main.tex`, `sections/model.tex`, `sections/fractional-moments.tex`, `appendices/wellposedness.tex`, `references.bib`, and `development/COVERAGE.md`. I did not consult other current review reports or use repository research notes as proof authority. The intentionally unwritten later stages and front matter are outside this review.

The main mathematical claims in the current draft withstand my checks. I found one minor mismatch between a general lemma's stated setting and the particular proof supplied for it. I found no major issue.

## Issue MEASURE-01 — MINOR: state the local loss bound used in the integrating-factor proof

**Location:** `appendices/wellposedness.tex`, lines 28–48 and Lemma `lem:weighted-comparison` (lines 66–81).

**Issue.** The general setting assumes that the nonnegative loss coefficient satisfies

\[
\int_0^T a_s(x)\,ds<\infty\quad\text{for every }x,
\]

and that the weighted variations of \(H_s\) and \(a_sd_s\) are integrable in time. The text then says that the loss coefficient is integrably bounded on bounded size intervals *in the application*. However, the proof of the general integrating-factor identity restricts to \(x\le R\) and asserts that multiplication by \(a_s\) is bounded there by an integrable time function. This does not follow from the general assumptions that precede the lemma.

For example, take \(a_s(x)=1/x\), \(H_s=0\), and

\[
d_t(dx)=\mathbf 1_{(0,1)}(x)e^{-t/x}\,dx.
\]

These data satisfy the stated weak loss equation, have finite weighted initial variation, and satisfy the required time-integrability condition because

\[
\int_0^T\int_0^1(1+x)x^{-1}e^{-s/x}\,dx\,ds
=\int_0^1(1+x)(1-e^{-T/x})\,dx<\infty.
\]

Nevertheless, multiplication by \(1/x\) is unbounded on every output restriction \((0,R]\). Thus the specific Volterra-series justification given does not cover the full stated setting. This example does not refute the integrating-factor identity or comparison inequality; it identifies an assumption missing from the supplied proof.

**Suggested fix.** The simplest repair is to make the bound already used in the application an explicit assumption of this setting: for every finite \(R,T\), require an \(A_{R,T}\in L^1(0,T)\) such that \(a_s(x)\le A_{R,T}(s)\) for \(0<x\le R\). The later coefficient \(a_t(y)=\lambda(t)(\bar m(t)+\bar N(t)y)+\sigma(t)\) satisfies it. Alternatively, retain the broader setting and supply a general weak-integral integrating-factor argument that does not rely on bounded multiplication on \((0,R]\). No change to the existence theorem's hypotheses is needed.

## Checks supporting the main results

- **Weak measure integrals.** On the standard Borel space \((0,\infty)\), the kernel formulation, variation bound, and composition with arbitrary measurable daughter kernels are appropriate. Integrating the norm bound gives continuity of integral iterates without assuming Bochner measurability of the instantaneous vector field. The moving-atom warning is relevant and does not obstruct the construction.
- **Comparison without derivatives of measures or norms.** Subject to the minor localization clarification above, the positive majorant argument is valid. The balance for \(z\), together with \(|d|\le z\), gives both the endpoint norm bound and the required negative loss term. It does not require a derivative of a Hahn sign or a Banach-space derivative. The weighted cancellation in `eq:weight-cancellation` is correct: its coagulation integrand reduces to \((x+y)(1+2x)\). Local second-moment bounds make the event integrals and stability coefficient integrable.
- **Positive cutoff construction.** With \(k_r\le r\), the nonlinear field is locally Lipschitz in variation weighted by \(1+x^3\). The scalar loss shift gives a positive fixed-point map on a sufficiently short interval. Daughter mass conservation and \(z<x\) give the stated polynomial moment estimates. In particular, the third-moment coagulation bound is \(3\lambda(mM_3+M_2^2)\le6\lambda mM_3\).
- **Cutoff Cauchy estimate.** The cutoff forcing estimate uses only the second and third moments, with the displayed double integrals expanding correctly. Its time integral is uniformly \(O(r^{-1})\) on compact intervals. Applying the full-equation stability estimate to two forced cutoff solutions is legitimate and gives the claimed weighted-variation Cauchy property.
- **Finite-second-moment initial data.** Truncating the initial measure yields finite third moments, while the second moments and stability coefficients remain uniformly bounded. Stability allows unequal masses, so \(m_j\ne m_k\) causes no gap. Weighted-variation convergence passes mass and all bounded Borel tests, including tests composed with discontinuous parent-dependent daughter laws. The stated finite-time boundary conclusions follow from this convergence and continuity.
- **Fractional moments and separation.** The pair inequality proof, its strict equality case, and the bounded concave-test argument are correct. The normalized decay coefficients have the stated signs and values. Monodisperse initial data with equal daughters give the required instantaneous equality. In this example, the constructed weighted continuity and the constant equal-split operator justify the right derivative used for sharpness. The critical weak limits, moving-window exponents, and sufficient perturbed-rate nonstationarity criterion follow with the stated moment assumptions.
- **Scope of the literature claims.** I checked the primary sources cited by the draft. [Cepeda's paper](https://arxiv.org/pdf/1301.1934) supports the discussion of a homogeneity-moment framework with a parent-independent law of daughter ratios and a Wasserstein-type distance. The [Deaconu–Fournier–Tanré paper](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf) supports the cited mass-sampling process interpretation. Their bibliographic details match the supplied entries. These citations are context; the present measurable-parent construction is established by the appendix itself.

**Major issue count: 0. Minor issue count: 1. Recommendation: accept Stage 1 after the local loss-bound clarification in MEASURE-01; no major mathematical revision is required.**
