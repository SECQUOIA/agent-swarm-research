# Stage 2, round 1: independent review 4

Verdict: **0 major findings, 0 minor findings.** I found no mathematical or attribution defect requiring repair in the frozen Stage 2 material.

I read the full joint-accuracy section, the new parity results from the nonnegative even thresholds onward, the diagnostic script, the Stage 2 author audit, and the surrounding model and fixed-accuracy arguments on which these results depend. I did not read other review reports or change manuscript files. The assessment below concerns proof validity and stated scope; it does not certify novelty against every possible literature antecedent.

## Joint lower bounds and matched law

The exterior proof retains the correct sine target throughout. Its affine angle coordinate maps the correctness interval exactly, and convexity of arcsine gives the needed sign at the negative extrapolation point. The two Taylor remainders carry the growing constants inside powers and include their factorial denominators. Maximality of the odd index controls the sine remainder relative to K uniformly, even when log(1/K) grows arbitrarily fast. Solving the remaining obstruction gives the stated factor n and exponent n/(n+1).

The independent Fejér–Riesz argument is valid. The analytic composition has the stated disk growth, its Taylor remainder follows from Cauchy's estimate, and the squared Taylor polynomial is globally nonnegative on the real line. The finite-index proof first establishes the factor's endpoint variation and thus T >= r+1 under its stated index restriction. Its large-T*delta branch and adaptive-radius branch cover the alternatives. The all-index proof genuinely removes the restriction: the fixed-radius contradiction is uniform over every positive integer r once delta is sufficiently small. Taking the (r+1)-st root of the explicit threshold bound loses only constants depending on rho.

The integrated sign construction is contractive, has the correct signed integral identity, and attains absolute error eta on all of [delta,1]. Consequently the matched law for K <= delta^beta, and the full-complement version for eta <= delta^(1+beta), follow with the stated uniform constants. The high spectral interval is not needed by either lower bound, so the independence from c in the matched law is justified.

## Growing-index construction and intermediate comparison

I checked the gate degree, nearest-contact leakage, contact slack, and all three global regions. The displayed low leakage/slack ratio follows after substituting d <= C/r, k*delta <= 2A*delta^(1/(2r)), and G_r >= c*r^(-1)*R_0^(-2r). It tends to zero and supplies the signed error bound at the exact threshold, including the contacts.

The tail retains the necessary factor 2^(2r+4). In the outer contractivity region, the linear contribution is bounded by C*r^2*2^(2r)/k and tends to zero because r=o(D). The degree-2r contribution is controlled by one fixed large A. The high-band powers delta^(2r+2-2/r) and delta^(3-2/r) agree with the displayed expressions in n=2r; constants exponential in r remain harmless under the same hypothesis. The truncation length is O_c(D), since the minimal threshold index and G_r <= K imply L=O_rho(r+log r)=o(D).

The intermediate comparison correctly applies the finite-margin lower bound at index r-1. Its exponent agrees with the pinned upper exponent. A fixed relative margin makes (G_(r-1)-K)^(1/r) bounded below, leaving the claimed O(r^2) multiplicative gap. The ratio G_r/G_(r-1) tends to R_0^(-2), so exact lower thresholds satisfy this condition eventually. The manuscript correctly retains the margin factor near the upper tier boundary and explicitly declines to claim a uniform multiplicative optimum there.

## Even and odd parity

The implicit even staircase is supported by attainment, convergence, the even nonnegative Taylor limit, and the parity-preserving pinned construction. Plateaus cause no problem because the staircase uses the first attaining index. The convexity argument proves F_2=F_1=E_1. The explicit cubic in y^2 is globally positive, and its binomial-tail bound is below 1/32. These facts justify the matched even order delta^(-5/6) in the comparison table.

The odd lower bound retains the logarithmic factor: the exterior coordinate stays bounded in the required exponential scale uniformly in the Taylor index, and choosing that index proportional to D gives d*delta >= c*D. The sign-based upper polynomial is odd, contractive in both the transition interval and its complement, and accurate within K*delta. Thus its fixed-K order matches the lower bound.

The comparison concerns one definite-parity transform, including coherent real-part extraction. Arbitrary compositions remain within the unrestricted model. The new results do not make an unsupported lower-bound claim for those compositions, nor a classical phase-computation or gate-synthesis claim.

## Attribution and reproducibility

I checked [Gilyén et al., Lemma 25 and Theorem 30](https://arxiv.org/pdf/1806.01838) against the uses here. Lemma 25 gives a globally bounded odd sign approximant with the required degree. The amplification alternative is valid with amplification factor two, input singular values at most (1-delta)/2, and relative precision chosen at the target absolute-error scale. This gives the stated upper order after the constant-query encoding of (I-H)/2. These tools are attributed rather than presented as new.

The [proof of Motlagh–Wiebe Theorem 4](https://arxiv.org/pdf/2308.01501) contains the reciprocal-root and even-circle-multiplicity factorization argument cited for Fejér–Riesz. The manuscript explicitly identifies the underlying factorization as classical. The exterior Chebyshev inequality is both cited and proved in the fixed-accuracy section.

I ran the diagnostic script with the required qipm interpreter, directing all outputs outside the manuscript:

```text
/workspace/local-home/miniconda3/envs/qipm/bin/python spectral-shift-paper/scripts/joint_accuracy_diagnostics.py --output /tmp/qipm-review4-stage2-diagnostics
```

It completed successfully. The r=1 threshold was 0.021131013144337452; the exact/asymptotic ratio at r=32 was about 1.008362. The three sampled maximum normalized errors were 1, and the leakage/slack ratios were approximately 6.85e-25, 1.94e-46, and 3.33e-74, matching the author audit. The script correctly labels these as floating-point diagnostics and does not use the mesh as a feasibility proof. Its signed-error evaluation avoids subtracting two quantities close to one.

Required repairs: none.

Counts: **0 major, 0 minor**.
