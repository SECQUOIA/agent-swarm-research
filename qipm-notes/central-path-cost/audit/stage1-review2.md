# Independent Stage 1 review 2

Reviewed `main.tex`, `macros.tex`, `sections/01-foundations.tex`, `sections/02-exact-distance.tex`, `bibliography.bib`, `audit/source-map.md`, and `audit/literature.md`. Consulted `literature/README.md` and the local full texts of Nesterov–Todd (2002) and Nesterov–Nemirovski (2008). Did not read other reviews, consult other reviewers, edit the manuscript, or treat future-stage placeholders as defects.

**Verdict: no major issue found.** The spectral metric and allocation results are correct under the intended hypotheses. Two minor missing explicit hypotheses should be repaired before carrying the statements into the completed paper.

## Findings

### MINOR 1 — Restate the accuracy range in the logarithmic-allocation corollary

Location: `sections/02-exact-distance.tex`, lines 326–347, Corollary `cor:water-movement`.

The corollary does not explicitly assume `0 < epsilon < W_0`, although its positive-multiplier characterization requires this. The immediately preceding paragraph discusses `epsilon >= W_0` and `epsilon = 0`, making it particularly easy to read the corollary as covering those cases. At `r=1`, `w_1=alpha_1=1`, and `epsilon=1`, the unique allocation is `s_1=0`; no `gamma>0` satisfies `s_1=W(gamma)`. At `epsilon=0`, there is no feasible finite scalar allocation.

Suggested fix: start the corollary with “Let `0<epsilon<W_0`.” The boundary cases already have a suitable separate discussion. This is a missing statement hypothesis, not an error in the proof on its intended range.

### MINOR 2 — Make the step-radius range explicit in both movement corollaries

Locations: `sections/01-foundations.tex`, Corollary `cor:optimal-movement`; `sections/02-exact-distance.tex`, lines 348–355, Corollary `cor:water-movement`.

Both statements use `-log(1-R)` without explicitly imposing `0<R<1`. This range occurs earlier in the chord lemma, but the subsequent definition of a forward-`R` sequence does not carry a stated global restriction. For example, `R=1` makes the displayed denominator undefined. The issue is especially visible in the later corollary, several pages after the lemma.

Suggested fix: add “Fix `0<R<1`” to the first corollary and “For `0<R<1`, if all scales ...” to the later one, or establish an unmistakable section-wide convention. No proof changes are needed.

## Mathematical checks supporting the verdict

- **Forward-norm direction.** The logarithmic norm-distortion argument yields `||y-x||_x <= exp(length)-1` in the correct starting norm. Integration of the segment estimate gives the correct `-log(1-R)` lower-count constant. Partitioning a shortest curve gives the correct `log(1+R)` upper-count constant.
- **Hermitian dilation.** For `g=b/2`, the two eigenvalues `+sigma_i` and `-sigma_i` supply exactly `2g''=b''`; there is no extra factor two in the complex case because the complex matrix space is explicitly a real inner-product space. Positive divided differences justify discarding off-frame directions. At repeated eigenvalues, diagonalizing the compressed derivative gives the required almost-everywhere lower bound. Singular values equal to zero cause no problem: their scalar paths are absolutely continuous and differentiable almost everywhere, and the dilation includes the full zero eigenspace.
- **Jordan normalization.** With the trace inner product, primitive idempotents have squared norm one; the Peirce off-diagonal term is the divided difference times `||h_ij||^2`, with no additional factor two. In real-symmetric or complex-Hermitian realizations that norm already includes both matrix entries. The inverse derivative coefficients follow directly from differentiating `z circ z^{-1}=e`: on `V_ij`, the quotient of the coefficients of `L(z^{-1})` and `L(z)` is `1/(z_i z_j)`. This verifies the formula without relying on the manuscript's more compressed alternative power-series/scaling explanation. The same rules hold in the exceptional algebra.
- **Ambient versus frame distance.** The contraction is established along every absolutely continuous ambient curve before exhibiting a frame curve that attains it. Thus the argument genuinely proves a global distance formula from zero, not just a distance within the frame. Coordering suffices for the stated two-endpoint equality and is preserved under interpolation of transformed coordinates.
- **Exact gradient parameter.** The gradient/frame Hessian block gives `alpha sum_i 2t_i^2/(1+t_i^2)`. Its supremum is `alpha p` or `alpha n`, approached simultaneously in all active spectral slots. Affine logdet restriction establishes standard self-concordance at scale one; scaling by at least one and product addition preserve it. Arbitrary positive scales are correctly allowed for the metric-only assertions.
- **Weighted endpoint allocation.** The trace/rearrangement argument permits signs and repeated or zero objective eigenvalues. Inactive spectral coordinates can be zeroed. Within each factor the common scale ensures the allocation is ordered with objective weights. Strict convexity and boundary divergence establish existence and uniqueness; the KKT argument excludes zero active coordinates and a zero accuracy multiplier on `0<epsilon<W_0`. The logarithmic surrogate has the displayed Lambert-W equation, including the correct absorbed factor two and the necessary exclusion of its extraneous zero root.

As an independent normalization check, used `/workspace/local-home/miniconda3/envs/qipm/bin/python` to compare the direct determinant Hessian with the Hermitian-dilation divided-difference formula on real and complex `2 x 3` matrices, with singular spectra `(0.3,0.7)`, `(0.6,0.6)`, `(0,0.6)`, and `(0,0)`, and random tangent vectors. All comparisons agreed to below `1e-10`. Building and inverting the complete real-coordinate Hessian also recovered the displayed gradient dual norm to below `1e-12` for all eight cases. These checks corroborate the analytical proof rather than replacing it.

## Prior-work check

The local Nesterov–Todd text supports the attribution of the short-step interpretation, product-distance rule, scalar hypercube flattening, and same-endpoint primal–dual `sqrt(2)` theorem. Nesterov–Nemirovski Theorem 4.1 (local extracted p.18 / printed p.550) has the stated `log 2 + nu^(1/4) sqrt(D(D+log 12))` bound; its target-set comparison carries a separation hypothesis as the manuscript says. Stage 1 makes no unsupported first-result claim. The direct trace Hessian derivation appropriately carries the complex extension rather than attributing that extension verbatim to the real-symmetric Lewis–Sendov theorem. Baes is cited as prior subject literature, with no unread theorem number claimed.
