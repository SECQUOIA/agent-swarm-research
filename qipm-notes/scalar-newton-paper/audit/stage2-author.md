# Stage 2 author record

Scope: classical inverse-form lower bounds and composition. New files:
`sections/04-lower-bounds.tex`, `sections/05-composition.tex`, and
`checks/check_lower_identities.py`. Both sections are included by `main.tex`.
Stage 1 mathematical sections were not changed. The source map has been
updated for every Stage 2 source.

## Results reconstructed

- The normalized reciprocal minimax degree is explicitly attributed to Kraus–Vassilevski–Zikatanov, Corollary 2.2. The exponential engine is attributed to Montanaro–Shao, arXiv:2311.06999, Theorem 1.8 and Section 5.1, with the exact degree parameters and denominator. The new reduction proves polarization, full-SQ simulation and the box-LP factor, rather than assuming a sparse-oracle lower bound survives matrix norms or sampling.
- Dyadic rounding is checked by a contraction-preserving Perron bound and the resolvent identity, with explicit slack below the Forrelation promise gap. Rational unit vectors use 3/5 and 4/5. The exact rational constraint factor uses positive rational block LDL pivots followed by four squares. The public table is finite and effectively enumerable, but is not claimed to have polynomial-time preprocessing or a stable inverse-spectral generator.
- The finite-population statistical proof uses stopped hypergeometric transcripts. Stopping at t/2 observed ones prevents the KL argument from crossing a support singularity; the omitted stopping event is explicitly bounded. The small-population regime is handled separately by zero-versus-one search.
- The confidence lower bound uses product Bernoulli laws, concentration of the finite population, and binary data processing. The necessary population assumption is explicit. The coherent sign-block lower uses Nayak–Wu and its matching upper uses amplitude estimation, with a canonical oracle-completion contract.
- The exact/narrow-level product compiler uses the partial-outer theorem of Chakraborty et al., Theorem 2, only after verifying linear outer randomized complexity. The unconditional single-form product uses the fixed inner hard distributions provided by the proof of Ben-David–Blais Theorem 35, combined with their Theorem 24 and the minimax observation following Definition 34. It does not incorrectly infer a product-form hard distribution from a worst-case composition bound alone.
- The restricted-interval construction is proved as a full-domain dual witness, then realized by an explicit positive spectral measure and its Jacobi matrix. Both diagonal entries and the cross entry are proved. The closed diagonal is derived from partial fractions, not asserted from numerical evidence.
- The constant-path theorem rederives endpoint cofactors, Chebyshev values, the genuine Forrelation circuit depth and its source denominator. The outer factor is kappa squared. Clock length is genuine increasing circuit size, not public padding of a fixed hard instance.
- Cyclic holonomy dilution, two-cluster contrast, and Schur condition-budget obstructions are proved separately with their exact hypotheses. The final envelope is a maximum over families and explicitly does not claim the full joint product.

## Corrections and carefully narrowed statements

1. The source distributional proof used epsilon <= chi/24 and admitted the edge case n=24, where its two outer weights are zero and all-one. Those two weights are distinguishable with one query, not linear cost. Although the asymptotic family could be repaired by a sufficiently large unspecified constant, the explicit source choice was insufficient for its stated Hamming-sphere argument. The manuscript uses epsilon <= chi/200, ensuring genuinely central weights with a square-root gap and linear outer complexity. This in turn changes the convenient high-accuracy path threshold from kappa >=128 to kappa >=1024. No exponent or polynomial factor is changed.
2. The source's coherent amplification discussion asserted a Theta(log(kappa/epsilon)) black-box lower cost without a precise theorem covering its entire stated transformation model. The manuscript retains the proved clock-budget implication for a chosen repetition/amplification procedure and the standard logarithmic-cost construction. It does not assert a universal lower bound against structure-aware amplification.
3. The constant-path boundary factor kappa^(-3/2) shortens the available hard circuit at fixed target coefficient by order sqrt(kappa) log(kappa). It should not be described as extra length needed to reach the same coefficient. The text uses the former wording.
4. The coherent numerical-output paragraph in `04-lower-bounds.tex` preserves the source note's q_* denominator and explicitly distinguishes estimating numerical forms from deciding the Forrelation promise. This is a retained qualification, not a newly repaired source error. A uniform O(1/epsilon) claim is not made without the additional noncancellation condition or the high-accuracy regime kappa epsilon=O(1). Stage 3a will integrate and check this existing paragraph within the full coherent-access comparison.
5. The general-inner-small-success-composition note is not required: its winner-finding relation is not the scalar averaging task. It is explicitly routed out of this stage rather than transferred without its subtractive baseline.
6. All clock theorems are worst-case families at parameter-selected dimensions. The statistical family separately states its finite-M saturation and confidence population threshold.

## Primary-source inspection

Read the local literature instructions and primary full texts for Ben-David–Blais (Definitions 33–34, Theorems 24 and 35, including the fixed-distribution proof), Chakraborty et al. (Theorem 2, Observation 23), and the Montanaro–Shao original PDF extraction at `/tmp/qipm-ms.txt` (Theorem 1.8, Corollary 5.1, Section 5.1, and the inverse-Jacobi construction). Root independently verified the matrix-function theorem locator and supplied current bibliography metadata. Existing bibliography entries were reused without mutation.

## Validation

- `checks/check_lower_identities.py` independently constructs 25 finite Jacobi matrices from their spectral measures via reorthogonalized Lanczos and compares direct dense inverse entries with the claimed cross coefficient and both diagonals. It also checks 25 constant-path inverses against the endpoint formulas. Parameters include kappa=4,16,128,1024,10000 and witness degrees 1,2,3,6,8. All passed using the qipm interpreter.
- The integrated LaTeX manuscript builds through the project Makefile under `conda run -n qipm --live-stream make -C scalar-newton-paper`. The final log is checked for undefined references, citations, and overfull boxes.
- These numerical examples validate identities and indexing; the manuscript proofs, not the diagnostics, establish the theorems.

The stage is ready for the prescribed five independent reviews. This author record does not substitute for them.
