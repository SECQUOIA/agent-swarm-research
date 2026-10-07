# Independent Stage 2 review 2

## Verdict

**No major issue found in the developed Stage 2 results.** The weighted sharpness proof, scalar comparison and rational certificates, distribution estimates, dyadic construction, and arbitrary-label finite-sequence proof are mathematically sound under their intended hypotheses. I found two minor statement-scope issues to repair. In particular, the short conic-interpretation paragraph should explicitly retain the section's unit-scale spectral-barrier setting; the conic gap identity alone does not imply its conclusion.

Read all new section and appendix mathematics, both scripts, the integrated main file, bibliography, source map, literature ledger, and the root's additional-literature ledger. Rechecked compatibility with the corrected Stage 1 distance and movement results. Did not read other reviewers' reports or communicate with reviewers. Did not edit the manuscript or run a competing build. Inspected the existing final build log, which contains no warnings or unresolved references/citations.

## Findings

### MINOR 1 — State the restricted-barrier hypothesis in the conic numerical-rank interpretation

Location: `sections/03a-distribution.tex`, lines 94–100, following Corollary `cor:numerical-rank`.

The sentence “If a conic central path has gap `nu/eta`, [the L2-tail bound] also applies to its primal projection ...” omits the additional condition that the projection follows the unit-scale spectral central path and is measured in the metric considered in this section. The gap identity alone is insufficient. The beginning of the section establishes the intended restricted setting, so this looks like a local scope ambiguity rather than a defect in the distribution theorem itself.

Concrete reason: duplicate each inequality of the scalar interval `(-1,1)` M times in an orthant representation with its standard log barrier. The restricted barrier is `M b(x)` and the conic parameter is `nu=2M`. With objective weight one, at `eta=nu/epsilon` the primal center is `q(2/epsilon)`, independent of M, whereas the projected length in the restricted barrier metric is `sqrt(M) rho(q(2/epsilon))`. For fixed epsilon this grows as `sqrt(M)`, and the cited unit-scale one-channel bound would grow only as `log M`. Such conic representations all have the stated gap identity.

Suggested fix: write “For a conic representation whose restricted barrier is the unit-scale product barrier considered here (up to an additive constant), the primal projection follows this path. If its full central gap is `nu/eta`, substitute `eta_f=nu/epsilon` ...”. Equivalently require the central projection and metric to coincide with the already-derived spectral ones. The later conic residual-transfer paragraph already uses an appropriate explicit restriction hypothesis and provides a good consistent formulation.

### MINOR 2 — Explicit radius ranges for new sampling and unequal-scale statements

Locations: `sections/03a-distribution.tex`, lines 92–93; `sections/03b-discrete.tex`, lines 246–258.

The sampling statement uses a forward-R count without declaring R's range locally, and the unequal-scale discrete statement says only “For fixed R, delta” before using `-log(1-R)`. The equal-scale discrete theorem explicitly imposes `0<R<1`, but that is a theorem-local hypothesis. These informal standalone quantitative statements should retain it explicitly. The latter should also write `delta>=0`, although existence of its tube implicitly forces that.

Suggested fix: add “For `0<R<1`” to the sampling sentence and “For fixed `0<R<1` and `delta>=0`” to the unequal-scale statement. The proofs and constants are unaffected.

## Independent mathematical checks

### Weighted prefix and exact worst ratio

The initial-coordinate decomposition and weighted Cauchy–Schwarz yield exactly `Gamma^2=sum d_i^2/alpha_i`. The fixed-order equality construction sets endpoint radial coordinates proportional to `d_i/alpha_i`, which are strictly decreasing for every positive scale vector. The translated velocity differs in L1 from a step by a finite amount, so its integrated weighted length differs by an M-independent bound for fixed rank and scales. Consequently the limiting ratio really is Gamma, and the common signed spectral frame needed for exact endpoint distance is preserved within each equal-scale factor. The adjacent-exchange ordering proof correctly uses the common increment sum and concavity of tanh. Its first term and factor `1/4` are consistent.

### Scalar dilation and rational certificate

I independently derived `E=y/v` and `dE/dlog(y)=E-K`, including the stated expression for K. The polynomial proving `rho<B` is positive throughout `(0,1)`. The sharper K bound on `E>2` follows from the monotonicity of E, the verified threshold at x=4/5, and the logarithmic derivative estimate for G. Integration of the two differential inequalities gives the displayed h_1 and h_k, with the correct factors and strict directions. The rational logarithm lower bounds have the proper series-tail direction. The lower certificate correctly checks a feasible witness in P coordinates before passing through its monotone inverse. Attainment, rather than a claimed unique stationary point, justifies the strict global upper enclosure.

Executed `scripts/verify_scalar_certificate.py` under `/workspace/local-home/miniconda3/envs/qipm/bin/python`; every exact Fraction/radical/series-tail check passed. Separately evaluated the displayed transform using 65-digit standard-library Decimal arithmetic and an independent golden-section search in `(0.93,0.96)`, obtaining a local maximizing candidate

`v = 0.94675629219174803551305297151585184...`

and ratio

`1.37486420044155170757084893154598737...`.

Also independently checked the elasticity differential identity at five Decimal points. These numerical checks are supporting evidence only; the appendix's finite rational argument supplies the proof. An initial attempt to use mpmath found that it is not installed; no package was installed, and Decimal supplied the independent check.

### Distribution and endpoint certificates

Both Q1 and Q2 constants follow from their scalar inequalities, including the small-parameter integrability. The numerical-rank tail bounds correctly distinguish l1 and l2 control. The geometric and polynomial examples impose sufficient finite-rank hypotheses and use valid lower-bound indices. The polynomial lower-bound logarithm is at least log 2 because `m <= (4 epsilon)^(-1/(b-1))`. The stronger determinant-profile failure example is valid: its exact logarithmic allocation diverges as `sqrt(log r)`, while the all-m uniform geometric-mean ratio tends to a constant strictly below one. The Schur-complement argument for compressed Hessian domination has the correct convexity direction.

### Dyadic lengths and finite sequences

The integer encoding claims, bounded rounding error, tail estimates, and actual accuracy window are consistent. Rounding must be summed by parts in the central-length lower bound; the manuscript does so, retaining the harmonic main term. The endpoint lower bound uses only genuine accuracy and the coordinate objective gaps, not a prescribed terminal label.

The metric-tube proof correctly clips labels, uses positive velocity to bound label displacement, and then controls progress by `O(C sqrt(1+C))`. The first cutoff gaps have a uniform positive spacing; the cutoff remains `Theta(r^(2/3))` before the terminal threshold. Initial progress is negligible even for the stated growing tube. The proof sums absolute increments and therefore tolerates backtracking. The decrement-to-tube conversion uses the starting norm and the correct threshold beta<1/2. The conic residual pullback and weak-duality argument have the correct sign. Spectral embedding works for arbitrary off-frame iterates because both needed ingredients—center-label distance and the largest spectral coordinate forced by accuracy—follow from the existing contraction and trace inequality.

The unequal-scale construction explicitly assumes label crossing rather than borrowing the equal-scale accuracy-forced crossing claim. Each core has a weighted coordinate gain comparable to H_0; a bounded center-to-center jump cannot cross three cores, and the sum of at most two gains is bounded by `sqrt(2) C`. Thus its claimed discrete separation is valid.

Executed `scripts/verify_standard_geometry.py` in qipm. Its weighted-prefix/permutation checks, convergence example, and scalar distribution checks passed. The proof audit above does not rely on those sampled checks.

## Scope, coverage, and prior work

The new material covers the Stage 2 entries identified in the source map: exact velocities, weighted prefix sharpness and scale order, same-accuracy scalar dilation, numerical-rank and decay laws, determinant-certificate limits, rational dyadic lengths, arbitrary-label tubes, decrement/conic transfer, and unequal-scale finite movement. No substantive Stage 2 source-map development is silently omitted. Formulation and general primal–dual results are explicitly reserved for Stage 4.

The text credits the classical Lorentz norm ingredient and the earlier Nesterov–Todd/Nesterov–Nemirovski geometric comparisons while identifying the specific sharp realization rather than the elementary prefix inequality as its contribution. It does not currently make an unsupported unqualified first-result claim. The final synthesis still needs the planned broader literature positioning, as the author audit already states; the intentionally incomplete introduction/abstract is not a Stage 2 defect.
