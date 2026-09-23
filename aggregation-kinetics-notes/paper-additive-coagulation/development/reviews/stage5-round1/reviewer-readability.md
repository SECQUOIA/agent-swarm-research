# Stage 5 independent review: mathematics, integration, and readability

Reviewed the frozen Stage 5 snapshot recorded in development/reviews/stage5-round1/snapshot.json. All recorded file hashes matched. I read the new Fourier section, observation-design appendix, introduction and abstract, discussion, main source, bibliography, README, coverage map, and Stage 5 author report, and checked the new arguments against their accepted prerequisites. I did not read another current review report or change manuscript sources, builds, or numerical data.

The new mathematics is sound on the stated hypotheses. The exposition distinguishes exact identification, pointwise statistical estimation, and finite-vessel observations carefully. One minor qualification should be added to the abstract.

## Actionable findings

1. **S5-RD-01 — MINOR: state critical balance in the abstract's finite-population claim.**

   **Location:** sections/introduction.tex, lines 14–17, beginning “In a physical finite population”; compare sections/finite-population.tex, proposition prop:finite-count and theorem thm:finite-discrepancy.

   **Reason:** The normalized-count accuracy on every sublinear horizon and the accompanying logarithmic-time mass-distribution discrepancy are proved for the critical physical system, with \(\sigma=\lambda m\). The abstract starts with general constant per-particle fragmentation, and subsequently includes results for both general controls and noncritical constant rates. Its finite-population sentence therefore reads as an unqualified assertion for that broader setting. The later introduction and assumptions table supply the restriction, but the abstract should state it independently. This is a scope clarification, not a defect in the finite-population theorem.

   **Correction:** Begin the sentence “At critical balance, a physical finite population has normalized count that remains accurate on sublinear time horizons, although …”, or add an equivalent explicit critical-rate qualification covering both conclusions.

## Mathematical verification

- **Fourier factorization:** The normalized bounded-test equation gives the source term with the stated coefficient and sign. The paired logarithmic increment estimate and accepted half-moment bound yield \(|r_t(k)|\leq |k|a_0e^{-\omega t}\). Integrating the variation-of-constants tail gives both displayed errors with \(\delta(k)=\omega+\operatorname{Re}\psi(k)\). Continuity and uniform convergence near zero justify the nonvanishing amplitude without logarithmic moments or a probability interpretation of that amplitude.
- **Identification:** The quotient error, eventual uniform nonvanishing, and logarithm anchored at zero follow from the factorization. In the one-sided uniqueness proof, the lower half-plane has the correct sign for negative jump support; exponential damping justifies differentiation without moments. Reflection across a zero boundary segment and Fourier uniqueness give the stated conclusion. Recovery of \(\sigma\), \(B\), and separately \(\lambda\) uses precisely the observations stated. The zero-selection case, invisible zero jumps, expected-daughter scope, and variation-norm instability example are handled correctly.
- **Sampling:** The four-component Hoeffding calculation gives the stated \(\varepsilon_n\). Both quotient identities and their denominator conditions are correct. The attenuation estimate gives the displayed bias–noise bound. Since \(\delta+d=\omega\), the proposed deterministic schedule balances the two bounds and eventually satisfies the signal condition, including \(d=0\). This is pointwise in a predetermined frequency and time; the text correctly avoids adaptive, simultaneous-frequency, minimax, or full daughter-recovery claims.
- **Preparation algebra:** The projection formula for \(\mathsf A_0\), the implication \(Q\mathsf KQ=0\), and the skew correction give the full finite-shell converse under the stated full-rank, nonzero-\(h\), and positive-interior assumptions. The continuum family is correctly labeled sufficient and conditional on an applicable forward solution and count balance. The known- and unknown-source gauges, third-concentration conclusion, reconstruction formulas, parameter-count bound, deterministic error constants, and finite-difference balance all check algebraically. Physical positivity and preparation limitations are not omitted.

## Integration, literature, and presentation

The title describes the central estimates without claiming a solution to the remaining tail-exponent or full noisy inversion problems. The introduction explains number versus mass sampling and separates the auxiliary process, physical particle system, and independent continuum samples. The assumptions table is useful for navigating the different scopes. The discussion preserves the distinctions between instantaneous sharpness and exact long-time rates, conditional large-size formulas and calendar-time tails, and a sufficient breakdown horizon and first failure time.

I independently checked the direct transform-quotient precedent in [Garnier, Section 2.2](https://arxiv.org/html/2405.10588v1), the independent log-size Fourier sampling framework in [Hoang et al., Sections 3.1.1–3.1.4](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf), and the asymptotic-profile setting in [Doumic–Escobedo–Tournus (2018)](https://ems.press/content/serial-article-files/16864). Their roles are described accurately. The short-time inverse reference and its bibliographic data agree with the [published record](https://www.numdam.org/articles/10.5802/ahl.207/). The constant-count historical statement is expressly supported by the [McCoy–Madras introduction](https://www.sciencedirect.com/science/article/abs/pii/S0009250903001593). The separate finite-system comparison is supported by the [D'Orsogna–Lei–Chou paper](https://www.math.ucla.edu/~tchou/pdffiles/JCP_LEI.pdf), without being presented as the same growing-time theorem.

A fresh isolated copy at /tmp/stage5-readability-4c40wc33 completed make -B successfully. Its final main.log reports 55 pages and contains no undefined-reference, citation, overfull-box, underfull-box, or other warnings. I visually inspected pages 1, 3, 38, 40, 41, 50, 51, 52, and 55, covering the abstract, roadmap table, Fourier proofs and certificate, discussion, new appendix, and bibliography ending. Mathematical displays and the table are readable; no clipping or broken layout was found. Accepted numerical files were unchanged and were not rerun.

## Optional preferences

The final page contains only the last two lines of the final bibliography entry. Avoiding that split would improve the final submission's appearance, but this is cosmetic and is not counted as a finding.

**MAJOR issues: 0. MINOR issues: 1. Recommendation: accept Stage 5 after the abstract's critical-balance qualification is added.**
