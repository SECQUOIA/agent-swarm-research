# Stage 07 independent review — reviewer 2

Snapshot: `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`.
All 27 manifest file hashes match; checked again before submitting this report.

**Verdict: no major issues. One minor numerical rounding correction remains.** The new trial asymptotics are justified by the accepted results, the numerical normalization and discrete certificates are correct, and the introduction and discussion keep the scientific claims within the proved scope. This is a review of Stage 07, not a substitute for the requested final whole-manuscript review.

I read the new introduction, numerical section, and discussion, their handoff and literature audit, the bibliography and reproducibility instructions, the numerical program and its two imported repository scripts, and the saved numerical evidence. I checked the relevant accepted theorem statements and proofs. I did not read other reviewers' reports or coordinator checks and did not edit manuscript sources.

## Finding requiring correction

### Minor M1 — refinement percentage rounds incorrectly

**Location:** `sections/07-numerics.tex:136`, the first percentage in the spatial-refinement paragraph.

The saved mean-trial values give

\[
100\left|\frac{P_{65536,48}}{P_{32768,48}}-1\right|
=0.015841231081359375\%.
\]

This rounds to `0.0158\%`, not `0.0159\%`, at the precision used in the sentence. Replace that number by `0.0158\%` (or use the less precise `about 0.016\%`). This has no effect on the numerical conclusions. The other two percentages in that sentence round correctly.

## Independent mathematical checks

### Two additional continuum trial assertions

For the unrounded mean profile, let
\(D_U=M|\sin s|^{-2/5}/Z_0\) and let the accepted rounded profile be
\(D_R=M(|\sin s|+R)^{-2/5}/Z_R\).
Then \(Z_R\to Z_0\), \(Z_R\le Z_0\), and

\[
\frac{D_U}{D_R}
=\frac{Z_R}{Z_0}
\left(1+\frac{R}{|\sin s|}\right)^{2/5}
\ge\frac{Z_R}{Z_0}\longrightarrow1.
\]

The form inequality, including the nonnegative reaction term, gives
\(J_c(D_U)\le (Z_0/Z_R)J_c(D_R)\). The universal sharp lower bound supplies the reverse leading inequality for the mean. The unrounded profile is integrable and its isolated infinite point values are irrelevant to the coefficient as an almost-everywhere function. Thus the claimed coefficient \(K_1\) is valid.

For the critical distance profile, both normalization integrals are
\(4\log(1/R)+O(1)\). On the retained fold annuli,
\((r+R)/(\sin r+R)=1+O(r_*^2)\). The separated-root contribution outside a fixed small fold neighborhood is \(O(a_R^{-2/5})\), lacking the leading logarithm. The inner region is covered by the same graded estimates as the accepted critical proof. Taking the small-budget limit before \(r_*\downarrow0\) recovers the same critical coefficient. The discussion of the third-moment distance trial correctly claims only its order; it does not identify the trial value with the sharp variational constant \(\mathcal S_3\).

### Circle finite-volume normalization

I derived the reflection and probability factors independently. On the half-wall, the matrix has reaction \((c+\cos s_i)^2\), off-diagonal conductance \(-D/h^2\), and the corresponding diagonal conductance sum. The full response is \(2h\sum_i u_i\). The imposed discrete resource is \(2h\sum D_i=M\), including for the constant comparison field. With only interior faces, its constant value differs slightly from \(M/(2\pi)\) at finite grid size and converges to it as stated.

Reflection in the offset reduces the density-\(1/4\) average over \([-2,2]\) to \((1/2)\int_0^2\), matching the transformed Gauss weights in the implementation. The grading exponents, cutoff scales, subdivision widths, and the distinction between the unrounded mean profile and a quadrature cutoff agree between prose and code. The observed trial assigns half the resource to each reflected simple root and uses the correct radius \((40M/(3a))^{1/5}\). It is clearly separated from both the rigorous asymptotic policy and a finite-budget optimized value.

### Uncertain-center objective, derivative, and tangent lower value

For face mass \(p_i=hD_i\), the matrix conductance is \(p_i/h^3\). Differentiating \(h\mathbf1^TA^{-1}\mathbf1\) gives

\[
\partial_{p_i}F_h
=-\sum_z w_z\left(\frac{u_{z,i+1}-u_{z,i}}h\right)^2,
\]

with no missing mesh or probability factor. Convexity of the inverse quadratic form and minimization of its tangent over the unit simplex give
\(F_h(p)-g\cdot p+\min_i g_i\). Hence the stated gap and its sign are correct. The code restores feasibility and then recomputes the value and derivative, as required for this inequality.

The zero-mobility exterior contributes
\(1/(L-z)+1/(L+z)\) for fixed center. Its uniform average is exactly
\((2/\eta)\log[(L+\eta/2)/(L-\eta/2)]\), with continuous limit \(2/L\). Thus the code does not silently omit the reciprocal-potential tail. The finite-domain restriction is appropriately described as a restriction on mobility placement.

## Independent numerical audit

I recomputed all nine saved uncertain-center fields using a separately assembled sparse matrix and sparse linear solver, rather than the optimization routine's banded implementation. Recomputed objectives match the saved values to at most approximately \(8.5\times10^{-15}\) relative; recomputed tangent gaps differ by at most approximately \(2.4\times10^{-14}\) absolute. All reconstructed face masses are nonnegative and sum to one to floating-point precision. This verifies the normalization and reported derivatives independently of the optimizer status.

I also recalculated all reported ratios and refinement changes from the saved data. In particular:

- The mean trial/uniform ratios are about 1.03313 at \(10^{-3}\) and 0.978607 at \(10^{-9}\), consistent with the prose.
- The third-moment trial/uniform ratio decreases from about 0.914129 to 0.0348144 over the displayed range.
- Critical scaled trial values decrease from about 9.49458 to 3.70190; they remain above the proved coefficient 2.02233076.
- Spatial refinement changes the critical trial by about 0.00839274% and the third-moment trial by about 0.118360%. The mean value gives M1 above.
- The separate circle quadrature changes and the larger observed-policy quadrature change agree with the saved values.
- The deliberately underresolved center calculation increases by about 11.5703% when its fixed field is evaluated with 384 nodes, supporting the stated approximately 11.6% example.

The numerical section explicitly distinguishes the finite-dimensional tangent certificate from a continuum certificate and from interval arithmetic. It also discloses that the known-center computed value lies below the exact continuum value. The domain-refinement difference is smaller than the optimization gaps and is expressly not claimed as a rigorous tail-error bound. These qualifications are necessary and adequate. I visually inspected both figures; their labels and captions preserve these distinctions and agree with the saved evidence.

## Scope, physical interpretation, and literature

The introduction and discussion correctly distinguish disorder moments of a quenched dispersion coefficient from higher displacement moments of one tracer. They retain the assumptions of fixed positive bulk mixing, constant affinity, nonzero wall velocity scale, and a nondimensional small resource. Exact observation and deterministic quantization are not presented as noisy-sensor results. Generic-fold statements are order estimates, whereas sharp coefficients are assigned to the proved cosine setting. The attainability assertions do not claim experimentally realizable fields under an unmodeled amplitude cap or fabrication constraint.

The novelty language is bounded and recognizes the relevant preceding ideas. I checked primary accessible sources supporting the newly emphasized comparisons:

- [Alphonse–Kunštek–Vrdoljak](https://arxiv.org/html/2602.19869v1) treats random forcing and risk measures for positive two-phase conductivity design; the narrower distinction drawn in the introduction is supported.
- [Buttazzo–Maestre](https://arxiv.org/pdf/1002.2770) likewise uses positive conductivity bounds in a random-load design setting.
- [Newman–Girvan–Farmer](https://arxiv.org/pdf/cond-mat/0202330) already connects resource allocation, risk-sensitive utility, and altered large-loss statistics; the paper appropriately credits that general principle.
- [Berry–Keating–Schomerus](https://michaelberryphysics.wordpress.com/wp-content/uploads/2013/07/berry320.pdf) explicitly discusses moment exponents selected by competition between bifurcations, supporting the limited analogy rather than an assertion that singularity-selected moment regimes are new in general.
- [Alexandre–Guérin–Dean](https://arxiv.org/abs/2105.06212) supports the stated context of generalized Taylor dispersion with spatial diffusivity and wall interactions.
- [Yüksel–Linder](https://arxiv.org/abs/1009.3824) supports the general observation-channel/quantization context.

I do not treat a literature search as a proof of absolute novelty. The manuscript does not require that inference: its comparisons identify concrete differences and its audit records access limits. I found no unsupported mathematical borrowing or overstatement in the new synthesis sections.

## Disposition

Correct M1 before accepting Stage 07. No additional five-reviewer round is needed on the basis of this report because I found no major issue. The separate final full-paper review remains necessary under the user's requested process.
