# Independent whole-manuscript review 2

Review date: 2026-09-20.

## Decision and findings

**No major issues identified. No remaining actionable minor issues identified.** I found no incorrect theorem, unsupported transition essential to a proof, contradiction between the main text and appendices, or novelty claim requiring correction in the reviewed version. No manuscript changes are requested by this review.

This is a whole-manuscript review, not a review confined to barrier theory. I personally read `main.tex`, `macros.tex`, and every statement and proof in all 35 files under `sections/`, including the introduction, synthesis, and all four appendices. I also inspected the bibliography and the attribution/scope discussion. I did not read another reviewer's report, author/helper report, review assessment, preparation checks, or workflow conclusions. No subagents were used. No manuscript source was edited.

The judgment concerns the mathematical claims actually made, including their explicit optimization classes and access contracts. The stated narrow-cap barrier intervals, nonsymmetric parameter intervals, and broader unrestricted kernel questions are delimited open extensions; the manuscript does not rely on their resolution. I found no basis to turn these openly stated limits into a claim that a proved result is incomplete. At 183 pages, this is a substantial manuscript whose fit will depend on a journal's length policy; length alone does not expose a mathematical or expository defect that calls for a correction here.

## Verification scope

The following is the full reading inventory. File prefixes identify the reviewed source files unambiguously.

| Material | Files personally read in full |
| --- | --- |
| Framing | `00-introduction`, `13-synthesis`, `main.tex`, `macros.tex` |
| Local curvature and certificates | `01-foundations`, `02-certificate-rank`, `03-products` |
| Global regularity and affine barriers | `04-global-regularity`, `05-support-orbits`, `06-restricted-barriers`, `07-concrete-barriers`, `08a-general-topology`, `08b-product-orbits`, `08d-full-fibers` |
| Formulation families | `09a-whole-rows`, `09b-face-sharing`, `09c-balance-slices`, `09d-lp-power`, `09e-spectral-chordal`, `10a-nonsymmetric-barriers`, `10b-entropy-aggregation` |
| Approximation and compilation | `10c-conditioned-approximation`, `10d-exact-compilers`, `10e-projected-compilers` |
| Metric movement | `11a-exposed-movement`, `11b-primal-dual-movement`, `11c-concrete-movement`, `11d-tree-distance` |
| Computational contracts | `12a-resource-ledgers`, `12b-work-contracts`, `12c-newton-comparisons`, `12d-query-output`, `12e-active-compilers` |
| Four appendices | `08e-topology-refinements`, `08c-restricted-kernels`, `10f-approximation-refinements`, `10g-conditioning-counterexamples` |

I inspected the allowed source-map material for scope, but did not independently reread all repository workbench notes. Thus this report verifies the submitted manuscript's internal development and selected source attribution; it does not certify an independent line-by-line extraction audit of every repository note. The literature checks below are selective primary-source checks, not a claim to have independently reproved every external theorem or exhaustively searched all prior literature.

## Mathematical checks and reasons for the decision

### Curvature, genuine fibers, and global topology

In `01-foundations`–`03-products`, I checked the radial directions removed in the dimension-minus-two estimate, the complementary-rank Peirce count, the order of the quantifiers in the minimum-rank invariant, and the passage from semialgebraic/definable local selections to a generic lower bound. The upper construction covers the simple symmetric families, including the exceptional family. The product arguments use genuine rows from the original slice; they do not extend certificates that were valid only after restricting the other source variables. The distinction between minimum fiber rank and the existence of a useful aggregate certificate is retained.

In `04-global-regularity`, `05-support-orbits`, `08a`, `08b`, and `08d`, I checked the uses of saturation, covering maps, and cohomology against the hypotheses on the entire support manifold. Local regular selections are not silently upgraded to global ones. The active-pattern argument uses finite clopen pieces in the relevant saturated situation, and the exceptional real PSD cases are handled separately. The stronger assumptions on entire fibers in `08d` are explicit and are used to obtain rigidity; they are not asserted for arbitrary lifts.

For `08e`, I checked the distinction between a tangent subbundle and a trivial tangent subbundle, the clutching argument, the Euler obstruction at the balanced endpoint, and the conditional uses of sphere-fibration restrictions. The real Grassmannian exceptions are not lost by replacing integral information with an oversimplified rational argument. For `08c`, I checked the phase-embedding obstruction, the additive result in its prescribed positive-block model, and the separate general-kernel interval. The latter is not presented as an equality. The cylinder/range argument and the independent-transversal estimate retain their stated dimensions and support restrictions.

### Affine and intrinsic barriers

In `06-restricted-barriers`, I checked that boundary vanishing-order estimates hold along every relevant completion and that the recession estimate addresses the restricted standard barrier. The wide-cap equality uses the additional whole-fiber rigidity it needs. The remaining narrow-cap interval is stated in the introduction as well as in the body and synthesis.

The partial-minimization argument in `07-concrete-barriers` is valid with its bounded-fiber assumptions. In particular, an unbounded sequence over bounded projected points would produce a nonzero vertical recession direction, contradicting boundedness of a fiber. This supplies the compactness needed for boundary blow-up of the projected barrier. Strict convexity, the Schur complement for the Hessian, and the third-derivative cancellation give the required differential properties. The manuscript does not claim general barrier-parameter monotonicity under arbitrary unbounded-fiber projection.

The grouped, packed, and balance-domain intrinsic bounds are supported by appropriate sections or projections and by the displayed upper barriers. They are not deductions solely from ambient Jordan rank. In `09b`, the common-annihilator budget limits sharing. In `09c`, the alternate diagonal-minus-identity slice has its actual affine dimension; it is not incorrectly identified with a different balance body. In `09e`, spectral contact dimensions include the relevant phase directions, and the PSD-completion discussion retains boundedness and the standard separator/maximal-determinant interpretation.

### Nonsymmetric cones and entropy

In `09d` and `10a`, the power-cone statements distinguish logarithmically homogeneous barriers from arbitrary barriers. The cross-ratio branch needed for additive product bounds is used in the appropriate range. Duality handles the other exponent range. Characteristic-barrier formulas and boundary exponents concern the specified family; the text does not convert those tests into optimality over all barriers. The pointwise limiting cases and the role of auxiliary minimization in the displayed power barrier are stated with their needed conditions.

In `10b`, I checked the closure of the relative-entropy perspective at zero coordinates, including zero columns of the aggregation matrix. The lower bound on each perspective term prevents cancellation of a divergent positive term. Inactive columns retain their own nonnegative rays, so the all-zero aggregation case is covered. The intrinsic lower certificate still counts independent output inequalities when aggregation rows coincide or vanish. The cone-valued concavity/compatibility argument and the block Hessian factorization are consistent with this closure. The explicit third-derivative expression for the weighted geometric mean has the correct mixed moment terms.

### Approximation and compilers

In `10c` and `10f`, pointwise closeness, derivative control, continuous bundle data, and singular-value margins are distinguished. An arbitrary pointwise low-rank approximation is not used as if it supplied a continuous subbundle. The robust submersion argument needs the stated one-sided derivative bound; the separate total derivative bound has its additional term. The rank-one dropout examples and the higher-rank limitations support the scope of the positive results.

In `10d`, compiler lower bounds retain their actual restrictions: common cone orientation, continuous encoders, reusable summaries, and the specified finite-dimensional transformation families. The vector-lattice/simplicial argument and finite-dimensional dilation argument have the hypotheses they use. The quantum-relative-entropy moment identity preserves the correction term for the convention in use. The scalar/conic resource counts do not overlook free linear inequalities or a homogenizing ray.

In `10e`, recourse is taken relative to its actual compatibility space, including rank-deficient cases. The safe approximate Gram construction gives a conservative feasible model with the stated relative objective guarantee only in the pure least-squares setting. The convolution and Fourier arguments are about the stated reusable or separable interfaces. The exact quadratic-epigraph and matrix-quadratic parameter claims use appropriate sections; they are not general lower bounds on arbitrary equivalent formulations.

### Movement and resource/work contracts

In `11a`–`11d`, I checked the exposed-minor identity, weighted determinant metric estimates, and the difference between primal distance and primal-dual gap movement. Intermediate ambient metric paths are not silently required to remain feasible where the stated distance allows otherwise. The tree theorem fixes the tree, weights, and objective before taking the accuracy limit. Its lower potential and constructed upper path give the same active-plus-half-inactive coefficient, while the central route has the separate sum-of-weights coefficient. The claimed error term allows the logarithmic drift used for inactive subtrees.

In `12a` and `12b`, the resource ledgers distinguish necessary constraints from attainable resource vectors. The integer and continuous optimizations use the correct feasible ranges. Curvature and movement are combined using the same certificate. The fresh charge per round is an assumption of the work composition theorem, not a consequence of a one-shot query bound.

In `12c`, I checked the exact allocation identity underlying the first-power projected-Hessian comparison and the feasible sharpness example. Approximate metadata receives its own factor. The reduced right-hand side is handled separately from the Hessian quotient. Sparse elimination invokes the needed indefinite/quasidefinite arguments rather than assuming that arbitrary leaf elimination is safe. Exact-arithmetic flop counts are not presented as finite-precision stability results. Dynamic fresh-update lower bounds have their own interface and are not asserted for every trajectory of a fixed optimization problem.

In `12d`, state preparation, readable scalar output, classical full-vector output, and objective accuracy are separated. The lower-bound constructions supply the objective scale and public/hidden information claimed. The one-query projected-state constructions do not imply the same cost for a classical answer. The final comparisons take maxima of independently applicable costs rather than multiplying unrelated lower bounds.

In `12e`, exact source-free reusable compilers have a sufficiently strong output contract to support the decoding reductions. Acquisition and bounded-fan-in loading costs are separated from the smaller compiled problem. Natural and compiled central metrics, and matched gaps versus matched multipliers, are not conflated. The appendix `10g` correctly distinguishes raw KKT conditioning, an invariant reduced Schur operator, parameterization effects, and sensitivity assumptions.

## Primary literature and novelty checks

I checked the following primary sources against the corresponding uses, with the indicated scope:

- Fawzi and Saunderson, [arXiv:2205.04581v4](https://arxiv.org/html/2205.04581v4), especially the optimal barrier statements and the recession certificates in Theorems 3.9–3.10. These support the use of certificates for arbitrary self-concordant barriers, rather than only logarithmically homogeneous ones, and the input/output counting in the entropy discussion.
- Hildebrand, [A Lower Bound on the Barrier Parameter of Barriers for Convex Cones](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf), especially Theorem 5.4 and Corollaries 7.1–7.2. I checked the branch condition and power-cone formulas used in `10a`; the manuscript preserves their logarithmic-homogeneity scope.
- Lee and Yue, [Universal Barrier is n-Self-Concordant](https://arxiv.org/abs/1809.03011), together with the [published record](https://pubsonline.informs.org/doi/10.1287/moor.2020.1113). The general dimension upper bound is attributed to prior work; it is not presented as a new intrinsic lower bound.
- Scheiderer, [arXiv:2509.17121v2](https://arxiv.org/html/2509.17121v2), particularly Theorem 1.2. Its second-order-cone representability of compact convex semialgebraic sets with Nash-smooth positively curved boundary is compatible with the paper's resource lower bounds. The manuscript does not claim that positive curvature prevents such representations.
- Gouveia, Parrilo, and Thomas, [Lifts of convex sets and cone factorizations](https://arxiv.org/abs/1111.3164), for the general prior-work framing; and He, Saunderson, and Fawzi, [Interior Point Methods for Structured Quantum Relative Entropy Optimization Problems](https://arxiv.org/abs/2407.00241), for the comparison with structured quantum-entropy methods. These checks covered the primary abstracts/records and scope, not a complete independent reconstruction of those papers.

The introduction identifies concrete quantified contributions instead of claiming that conic factorization, barrier projection, chordal completion, or metric lower bounds are new in general. I found no checked source that establishes the three specifically highlighted formulas in their stated classes. That is evidence consistent with the manuscript's qualified positioning, not proof of exhaustive priority. I did not find an unsupported broad novelty claim requiring a correction.

## Independent compilation check

I copied only `main.tex`, `macros.tex`, `bibliography.bib`, `Makefile`, and `sections/` to `/tmp/conic-final-review2-k31enjga` and ran `make` in the `qipm` environment. The clean build succeeded and produced a 183-page PDF. The final TeX log contained no warnings, undefined references, multiply defined labels, overfull boxes, or underfull boxes. Shared manuscript build artifacts were not changed by this check.

Combined source SHA-256 for that snapshot, computed over the sorted section files after `main.tex`, `macros.tex`, and `bibliography.bib`, with relative path and NUL before each file's bytes:

`de0d53299a1fa27c385f98ca2e14dabafb0b1c485ff8b83ce95a0a58886c41fd`

This build check supplements the proof reading; it is not a substitute for mathematical verification or a claim that every page was visually inspected. Within the scope above, I recommend accepting the current manuscript for the final assembly stage without mathematical revisions from this review.
