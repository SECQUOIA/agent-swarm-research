# Whole-manuscript review 3, round 1

Reviewed the complete source of all eleven sections, `main.tex`, `macros.tex`, and `bibliography.bib`. This review was independent of the other final-review reports. Particular attention was given to Sections 8–9 and their dependence on the cyclic constructions and access contracts in Sections 2 and 7.

## Verdict

No concrete major or minor issue identified. No manuscript correction is requested by this review. This verdict concerns the stated mathematical results and output contracts; it is not a prediction of journal acceptance or a claim that all general parameter regimes are classified.

## Mathematical checks

- Recomputed the box trajectory increment formula and leakage bound. The choices of Γ, the low/high amplitude promise, and the two numerical accuracy levels leave the asserted decoding margins. Approximate-center transfer uses the inverse-transpose readout norm, charges both checkpoints, and does not silently assume a condition bound along the entire trajectory.
- Checked the distributional direct-sum simulation. Under the product distribution the hidden target index is independent of the assembled input, including its query transcript, which justifies the expected target charge. The truncation success 7/12 exceeds the hard-distribution threshold 9/16. Public nonuniform block-sampling weights do not invalidate the averaging argument.
- Differentiated the SOCP predictor response and checked the diagonal sensitivity, off-diagonal tail estimates, small-step bound, and Boolean-representative accuracy. The dynamic block-norm result correctly charges setup plus all responses rather than claiming a setup-only lower bound.
- Checked both branches of the threshold LP, uniqueness, strict relative feasibility, inequality count, XOR projection and objective-gap propagation. The finite readout perturbation narrows the effective gap before choosing the threshold constants. The proof does not reuse the uncoupled central-path scaling identity after adding the XOR facets.
- Checked the fixed KKT ray, the postselection probability, the hard-tree dimension and conditioning, and its width-three bags. The local-movement statement is appropriately restricted to bounded Dikin chords and is not promoted to an arbitrary algorithmic iteration lower bound.
- Verified the robust residual thresholds: acceptance gives true residual at most 7η/8 and rejection gives minimum residual greater than η/2. The innovation lower bound applies to normalized approximate columns, and the QR-volume/singular-value comparison gives precisely the displayed strict width condition and 2r−1 refresh bound. If 2r exceeds ambient dimension, the assumed sequence of 2r strictly innovating columns is already impossible.
- Checked the stronger adaptive coefficient-stability condition, the holomorphic width estimate, the strict-complementarity counterexample, and the distinction between cheap normalized-state preparation and dense classical output. The coefficient-only residual-testing example explicitly withholds the norm oracle that would reveal the answer.
- Across the other sections, checked the positive-form importance-sampling identity, Kantorovich relative moment, Chebyshev residual contracts, statistical finite-population reduction, single-form composition concentration constants, path-clock endpoint formula, plain block-oracle hybrid bound, cyclic inverse and public tilt normalization, and the structured Woodbury/error/rejection calculations. The structured output stays one fixed approximate vector on the good setup event; neither a transformed-column norm oracle nor successful unbounded retries is assumed.
- Checked the connection between the cone-system relative vector budget and the scalar estimator, the generalized-power clipping interval, and the stated full-output spectral/profile comparisons. The exact-field and input-acquisition limitations are preserved in the concluding claims.

## Independent source and diagnostic checks

The primary published [Brody et al. article](https://theoryofcomputing.org/articles/v019a011/v019a011.pdf), Theorem 1.1, supports the expected-query partial-function XOR theorem used in Section 8. The separate expected-to-worst-case constant-error conversion in the manuscript is valid.

The primary author-hosted [Buhrman et al. manuscript](https://homepages.cwi.nl/~rdewolf/publ/qc/robust_journal.pdf), Corollary 3 and the preceding bounded-error oracle model, supports joint recovery of all Boolean instance answers in linear total query cost. The manuscript correctly limits this benefit to outputs represented by those Boolean answers; it does not apply it to arbitrary numerical amplitude estimates.

Consulted the repository's Parks et al. literature record when assessing the reuse discussion. Existing Krylov recycling is expressly acknowledged, and the new claim is restricted to the residual/checkpoint contract and its proved quantitative bounds.

Ran `checks/check_temporal_identities.py` with `/home/sgusev/miniconda3/envs/qipm/bin/python`. It passed its kernel, threshold/XOR, sparse KKT, and rank/volume diagnostics. These numerical checks supplement the algebraic inspection above and are not treated as proofs.

## Overall fit and scope

The introductory rate table, core theorems, optimization examples, reuse section, structured comparisons, and conclusion agree on their interfaces and requested outputs. The central novelty paragraph is qualified and identifies precise developments while assigning the underlying approximation, Forrelation, composition, scalar-optimization, cone-algebra, and recycling ingredients to prior work. The paper is long but its three-part progression is explicit and consistent with the requested comprehensive treatment.

The unmatched general joint classical rate, unmatched generic coherent-sparse rate, ideal arithmetic, supplied structured-system access, and absence of a generic quantum interior-point speedup are disclosed scope limitations. They do not leave a proof obligation within the stated results unresolved.
