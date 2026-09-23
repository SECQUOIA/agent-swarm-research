# Stage 2, round 1, independent review 4

Verdict: no major proof error found. Three minor statement/definition issues should be corrected. In particular, the explicit witness diagonal and the high-accuracy product survive independent algebraic reconstruction; the distributional composition argument uses the requisite fixed inner hard distributions rather than inferring them from a bare worst-case composition theorem.

## Findings

1. **Minor — explicitly retain the parameter range in the coherent counting corollary.** `sections/04-lower-bounds.tex:364–368` states only the population requirement. Taken as a standalone statement under the paper's global convention kappa >= 1, its lower bound is false at kappa = 1: every sign block is the identity, so the inverse form is public and needs no hidden queries. Begin the corollary with “Under the parameter assumptions of Theorem [statistical-lower], and for ...,” or repeat kappa >= 4 and 0 < epsilon <= 1/128. Also identify constant bounded failure explicitly. This is a repair to the stated scope; the proof in the preceding theorem's range is sound.

2. **Minor — define the second-kind Chebyshev polynomial before using it.** `sections/05-composition.tex:225` introduces U_(r-1) without a definition. The later constant-path determinant uses the same family. Define T_j and U_j as the first- and second-kind Chebyshev polynomials, with U_j(cos phi) = sin((j+1)phi)/sin phi (continuously extended at the endpoints), or give its recurrence and initial values. This is particularly useful because U_t already denotes circuit gates in the preceding clock construction. The relevant identities are correct with the standard second-kind convention.

3. **Minor — make “oracle-preserving” a quantitative hypothesis in the general product theorem.** `sections/05-composition.tex:100–108` uses “oracle-preserving SPD realization” without defining that phrase. The proof needs every granted matrix access operation, including nonzero-location/count queries and SQ operations, to be simulated with O(1) hidden-input queries, with public vector access. Public norm metadata alone does not formally say this. Add that explicit requirement to the theorem or define the phrase immediately before it. The specific clock families do meet this requirement, so the applications are unaffected. The analogous conditional compiler can refer to the same definition.

## Independent checks

- Verified reciprocal minimax scaling and the cited Corollary 2.2 against the local Kraus–Vassilevski–Zikatanov primary full text. Checked the source lower-bound formula, Forrelation promise, and even-clock queried positions against the Montanaro–Shao primary PDF extraction.
- Read the primary Ben-David–Blais proof of Theorem 35, its Definitions 33–34 and Theorem 24. The fixed hard pair is indeed chosen before the outer function distribution, as required here. Checked Theorem 2 and Observation 23 in the local Chakraborty et al. source.
- Reconstructed the witness proof: the phase formula, signs of the barycentric residues, annihilated moments, positivity and normalization of the measure with an atom at zero, the degree and leading sign of the penultimate orthonormal polynomial, and the partial-fraction derivative formula for the diagonal. Both queried diagonal masses agree, and d' = CA/(A^2-1) follows. The restricted interval is used only to make a full-domain dual witness; no unjustified full-domain minimax claim appears.
- Recomputed the path determinant and cofactor formulas, the kappa^(-3/2) boundary prefactor, chi_n/c_n, the 3 ell + 2 transitions, the attainable coefficient spacing, and the resulting kappa^2 block count. The condition and source-depth bookkeeping are consistent.
- Checked the concentration constants: n >= 200 keeps the outer weights interior; the displayed Hoeffding tail is below 0.004, the realization fluctuation is S/8, and S > 14 epsilon d leaves adequate estimation slack.
- Checked the sparse Gram factors, rational rounding margins, stopped-Hamming transcript argument, high-confidence separation, cyclic dilution, and Schur-complement condition-budget inequality. These limitations are correctly restricted to their stated construction classes.
- Ran `checks/check_lower_identities.py` with `/home/sgusev/miniconda3/envs/qipm/bin/python`: all 25 witness realizations and 25 constant paths passed. Numerical checks supplement, rather than replace, the algebraic review.

Read the Stage 2 author record and source map. No other review reports were read, and no manuscript or supporting-code files were edited.
