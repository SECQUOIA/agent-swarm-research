# Stage 1, round 1: independent review 3

## Verdict

No major issues found. The delivered models and classical results are mathematically sound under their stated ideal-arithmetic interpretation. Two small model/statement clarifications should be made before acceptance. I read no other reviewers' reports and made no manuscript edits.

## Numbered findings

1. **Minor: state the random-arithmetic primitive used by the exact rejection sampler.** In `sections/03-classical.tex`, Lemma `lem:rejection` accepts with arbitrary real probabilities and samples from a newly materialized column distribution. The input SQ interface grants exact samples from the input vector, but `sections/02-models.tex` does not explicitly grant exact random-real comparisons or arbitrary Bernoulli draws at unit cost. With unbiased random bits alone, these are expected-bit operations rather than a literal fixed number of arithmetic operations for unrestricted real input. The theorem is correct in the usual randomized ideal-real model, but that convention should be written down, especially because exact output sampling is expressly distinguished from approximate sampling. **Exact fix:** add to the cost-model paragraph that an independent uniform random real in `[0,1]`, and comparisons with computed real probabilities, are unit-cost primitives in the ideal-arithmetic model. Alternatively explicitly count ideal Bernoulli draws. Keep the existing statement that this is not a bit-complexity bound.

2. **Minor: complete the approximate-sampling convention at zero coordinates and phrase the coupling explicitly.** In Proposition `prop:precision`, total-variation approximation allows a sample outside `supp(b)`, whereas the displayed estimator divides by `b_i` and is only defined on that support. The proof is valid because all such draws fall into the coupling-failure event, but the algorithm and the perturbation hypothesis should still be defined on those draws. Also, the comparison with “the exact-oracle output” is a coupling statement, not a claim about two independent executions. **Exact fix:** define the ideal estimator as zero when `b_i=0`, have the approximate implementation return zero on such a sample, and write “There is a coupling with the exact-oracle execution for which ...”. This leaves the proof, sample count, and failure bound unchanged.

## Mathematical checks

- Checked the Chebyshev residual construction, cancellation of the numerator at zero, ceiling and `K=1` boundary, and the claimed degree without an extra `log K`.
- Checked the complex sampling identity and support-restricted second moment. The endpoint-weight example gives exact equality in the Kantorovich bound, and the text correctly confines sharpness to this estimator.
- Checked all median-of-means constants. A group of size `64 C kappa / epsilon^2` gives failure at most `1/4`; total scalar error is at most `17 epsilon q / 32`. The additional finite-error allowance is therefore valid.
- Checked energy-normalized bilinear variance and deterministic bias, including real/imaginary median estimates and the noncancellation promise for relative overlap error.
- Checked the complete raw rejection probability and the expected trial bound. Sparse rows and columns are both needed and are supplied.
- Checked the nonnormal normal-equation identity `P b - x = -r(A* A)x`, singular values of `P`, and the unitary `K=1` case. Squaring the local materialization bound remains within the stated exponent.
- Checked the norm-sensitive general-overlap bound and its dependence on the supplied `R_e`.
- Checked the finite-error coupling argument and the Lipschitz property of the median. Rational residual coefficients are consistent with rational spectral bounds. The final paragraph properly declines to infer a uniform bit bound from ideal query complexity.
- The necessary conditioning scales follow from the upper bound for fixed sparsity and accuracy; these are properly described as necessary conditions rather than uniform hardness claims.

## Literature checks

Read `notes/literature/AGENTS.md` before consulting the primary local texts.

- `[[gharibian2023-dequantizing-the-quantum-singular-value]] p.20-22`: Theorem 4.1 and Lemma 4.2 supply precisely the sparse-polynomial local evaluation and importance-sampling antecedents cited in the section. The manuscript does not claim those ingredients as original.
- `[[andoni2019-on-solving-linear-systems-in]] p.9`: Section 1.4 explicitly asks about constructing an l2 sampler for the solution from an l2 sampler for the right-hand side. The cautious “antecedents” sentence is accurate; it does not mistakenly attribute the present rejection theorem to that paper.
- `[[li2016-gaussian-quadrature-for-matrix-inverse]] p.3-4`: The Lanczos/quadrature formulation supports the matrix-vector-product comparison. The paper also gives the broader inverse-form background on p.1-2.
- `[[cifuentes2024-quantum-computational-complexity-of-matrix]] p.1-2`: The matrix-element/local-measurement and sparse/Pauli-access classification supports the limited contextual attribution.

These checks support the current section's cautious attribution; they do not certify any novelty claim that later stages may add.

## Diagnostic

Ran `/home/sgusev/miniconda3/envs/qipm/bin/python scalar-newton-paper/scripts/verify_classical.py` successfully. Output: `PASS: residual, complex/support moments, sharp variance witness, rejection law, and arithmetic transfer`. These numerical examples supplement the algebraic checks above.
