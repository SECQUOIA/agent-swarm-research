# Independent whole-manuscript review 3

Reviewed 20 September 2026. This review concerns `main.tex`, `macros.tex`, all 35 files in `sections/`, and `bibliography.bib`. I personally read every section, statement, and proof, including the introduction, synthesis, and all four appendices. I did not delegate the review, edit the manuscript, or consult other reviewers' reports, author/helper reports, root checks, assessments, or workflow conclusions.

## Verdict and actionable finding

**No major issue found. One minor hypothesis omission should be corrected in two places.** The omission does not affect the intended integer-cap results or any of the three principal contributions. I found no mathematical reason to stop development of the paper or withdraw its principal claims.

### Minor 1: make the dimension cap explicitly integral in two standalone statements

Locations:

- `sections/07-concrete-barriers.tex:113`, Corollary `cor:tree-cap-parameter`, beginning “Fix a Lorentz dimension cap ...”.
- `sections/12d-query-output.tex:379`, the several-independent-search-diagnostics construction, beginning “for ...”, immediately before the formula for the number of groups.

Both places use arithmetic formulas requiring an integer cap, but neither states integrality locally. Other main cap theorems explicitly include this hypothesis, and the conventions do not impose it globally.

This is a genuine statement-scope problem, although a small one. In the first corollary, take `N=4` and `d=3.5`. Then `A=1.5`, `E=3`, `L_0=2`, `sigma=0`, and `chi=0`. The stated answer is therefore 3. In fact every allowed Lorentz factor has dimension at most 3; the tree is binary and must have three internal nodes. A balanced binary tree has an all-internal root and parameter `2*3-2=4`, which is the actual minimum by the preceding theorem. Similarly, at the second location, `s=4,d=3.5` produces three groups. A balanced partition has a group of size 2, requiring a dimension-4 paraboloid Lorentz factor and violating the stated cap.

**Fix:** write “Fix an integer Lorentz dimension cap ...” in the corollary, and “for an integer ...” at the search construction. Alternatively, declare once that every dimension/order cap is integral, but the two local edits are clearer and smaller. If real caps are intentionally allowed, replace the arithmetic cap by its floor consistently. No proof change is needed for the intended integer statements.

## Mathematical review

### Parts I and II: local certificates, regularity, and barriers

I checked `01-foundations`, `02-certificate-rank`, and `03-products`, including minimal-face reduction, genuine certificate fibers, finite differentiable selections, the mixed curvature identity, the dimension-minus-two bound, the complementary-rank Peirce bound, attaining constructions, and sequential rank accumulation. The generic minimum-rank selection argument supplies the claimed lower bound on the entire fiber on its regular set. It does not silently replace the fiber minimization by the rank of one chosen certificate. The sequential compression statement properly claims existence of an aggregate certificate, rather than minimum rank over an aggregate fiber. Exceptional Jordan arguments use valid quadratic-representation or rank-two identities and do not require an associative global matrix model.

I checked `04-global-regularity`, `05-support-orbits`, `06-restricted-barriers`, `07-concrete-barriers`, `08a-general-topology`, `08b-product-orbits`, and `08d-full-fibers`. The distinctions among local smooth selections, global contact maps, and entire smooth fibers are maintained. The no-sharing step, fixed support patterns, top-class arguments, real order-three exclusion, product support obstructions, and the additional accessibility hypothesis for full-fiber results are not conflated. The restricted nullity and recession tests apply with the stated quantifiers. The root-slice norm-tree parameter calculation, grouped and packed intrinsic parameters, and projection of barriers retain the needed coercivity and Hessian conditions. Apart from Minor 1, I found no defect in the exact resource arithmetic or its attainment arguments. The bounded narrow-cap interval is explicitly delimited rather than presented as an exact frontier.

### Part III: formulation families

I checked `09a-whole-rows`, `09b-face-sharing`, `09c-balance-slices`, `09d-lp-power`, `09e-spectral-chordal`, `10a-nonsymmetric-barriers`, and `10b-entropy-aggregation` in full. The whole-row dimension bounds and rigidity use the stronger stated hypotheses. Face-sharing counts common annihilator dimensions; it does not incorrectly count arbitrary private face dimensions as a direct sum. The balance-slice extreme-point argument, rank-two paths, and frame restrictions support the claimed intrinsic barrier parameters. The power-cone discussion separates arbitrary exact lifts from restricted direct or graph-based representations and treats the low-dimensional exceptions. Spectral and chordal calculations distinguish ambient and restricted parameters and credit standard completion results. Nonsymmetric characteristic barriers are not asserted to be cheaply evaluable or optimally parameterized in the remaining intervals. The entropy closure and recession arguments retain the zero-column rays and the actual finite-entropy lower bounds needed in the proofs.

### Part IV and approximation appendices

I checked `10c-conditioned-approximation`, `10d-exact-compilers`, and `10e-projected-compilers`, together with `10f-approximation-refinements` and `10g-conditioning-counterexamples`. Finite-radius estimates retain their radius and conditioning assumptions. Approximate complementarity and mixed slack derivatives are distinguished from diagonal identities. The compiler dimension results use continuous finite-dimensional summaries; the exponential feature-rank statement is not promoted to an exponential cone-factor bound. Exact, approximate, and local compiler models remain separate. Projected recourse, rank-deficient compatibility, Gram inflation, and least-squares accuracy are treated in the appropriate spaces. The counterexamples correctly prevent Euclidean contact conditioning from being promoted to barrier-metric conditioning.

### Part V: barrier movement and the weighted-tree asymptotic

I checked `11a-exposed-movement`, `11b-primal-dual-movement`, `11c-concrete-movement`, and `11d-tree-distance` in full, with particular attention to constants and the metric being used.

- The exposed-minor covector norm uses the same weighted log-determinant metric as the distance statement. The weights in the effective accuracy scale are necessary and are present. Compression gives a valid metric contraction; the sharp full-cone route is not claimed to lie in an arbitrary affine slice.
- The affine PSD exposure profile uses the reference normalization consistently. Geometric and polynomial spectral tails and their joint dimension/accuracy regimes are delimited. The primal–dual barrier-height argument keeps both feasibility and the signed Legendre convention straight and is credited to the classical framework.
- The grouped, packed, entropy, balance, and spectral calculations refer to the displayed barriers. Neither intrinsic parameter optimality nor central-route optimality is inferred merely from a displayed route.
- In the weighted-tree theorem, the active block pairings telescope exactly to the objective gap. Inactive child axes are bounded by that gap through their active parent, and this bound propagates down each inactive subtree. Thus the inactive log-determinant terms in the lower potential really contribute one half of their weights. The ambient inverse Lorentz Hessian identity gives the claimed potential norm; restriction can only reduce the dual norm.
- For the upper route, active residuals scale as `h`, inactive residuals as `h/(log(1/h))^2`, and inactive axes scale as `sqrt(h)/log(1/h)`. The squared speed therefore approaches the active weight sum plus half the inactive weight sum. The error integrates to the stated `O(log log(1/epsilon))`, and the gap is comparable to `h`. Fixed objective and fixed weights are essential and are stated. Zero objective factors and product composition are handled separately. I found no gap in either direction of the exact leading-coefficient proof.

### Part VI: resource, work, Newton, and query contracts

I checked `12a-resource-ledgers`, `12b-work-contracts`, `12c-newton-comparisons`, `12d-query-output`, and `12e-active-compilers` in full.

The resource lower bounds are distinguished from attainability. The same aggregate certificate is used when composing curvature and movement. Movement is multiplied by a per-call work charge only when that charge is part of the stated contract; preprocessing, implicit records, and reuse are not silently charged afresh.

For the allocation-aware PSD quotient, eliminating residual directions gives the stated Gram matrix and quadratic form. Its positive definiteness follows because every source owns a column. The first-power comparison uses positivity of `E D E` even when `E` is indefinite, followed by the exact allocation identity. This is precisely the additional information that avoids a squared eccentricity bound. The center is evaluated at the same projected `W`, and the reduced gradient is retained away from the center. The two-source example attains the comparison and demonstrates the claimed obstruction to reconstructing off-center Newton states from projected records alone.

The dynamic compilation proof uses a complete nondestructive value object and restores its backing access; that contract is strong enough for the subsequent distinguishing argument. The manuscript explicitly separates this universal service contract from the cost of a particular client. Sparse factorization results concern exact arithmetic unless further stability assumptions are supplied. Full classical directions and quantum states are not treated as identical outputs. The search, counting, interrogation, and diagnostic lower bounds have explicit input/output promises. Separate lower bounds are combined by a maximum where a product is not justified. The consensus and active compiler examples retain their different feasible bodies and access models. Other than the repeated integer-cap omission, I found no unsupported work or query conclusion.

### Remaining appendices and synthesis

I read every proof in `08e-topology-refinements` and `08c-restricted-kernels`. The plane-field construction checks the actual clutching obstruction, and the rational product obstruction is not presented as a complete topological classification. The restricted kernel arguments retain the relevant derivative and nullity qualifications. I also read `13-synthesis` against the precise proved statements. Its account of exact frontiers, conditional consequences, and remaining parameter intervals is consistent with the body of the manuscript.

## Literature and originality

I read the whole bibliography and the introduction's comparison with prior work. As primary-source checks, I consulted:

- [Nesterov–Todd, On the Riemannian Geometry Defined by Self-Concordant Barriers and Interior-Point Methods](https://csclub.uwaterloo.ca/~pbarfuss/digitalocean/Nesterov-Todd2002_OnTheRiemannianGeometryDefinedBySelfConcordantBarriers.pdf), especially Theorem 5.1(c), Theorem 5.2, and Corollary 5.1. These support the manuscript's attribution of classical primal–dual geometry.
- [Nesterov–Nemirovski, Primal Central Paths and Riemannian Distances for Convex Sets](https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf), including the introduction, Theorem 4.1, and Theorem 5.3. The current paper does not claim that the general distinction between central-path length and shortest distance is new.
- [Scheiderer, Smooth Hyperbolicity Cones Are Second-Order Cone Representable, version 2](https://arxiv.org/html/2509.17121v2), Theorem 1.2. Its SOC existence theorem is accurately described and distinguished from quantitative factor and certificate frontiers.

I also compared the local companion's exposed-minor theorem and norm-tree calculations (`central-path-cost/sections/06-formulation.tex` and the relevant part of `appendix-formulations.tex`) with the attribution in the introduction. The overlap is acknowledged and the needed proofs are reproduced. I inspected the permitted source-map orientation material but did not independently audit every workbench note against the paper; this report is not a claim of exhaustive source-inventory coverage.

The three specifically identified novelty claims concern precise formulas and quantifiers: entire-fiber minimax rank, active/inactive weighted-tree distance, and feasible allocation-aware quotient transfer. The paper does not claim novelty for general cone factorizations, elementary positive trace inequalities, or barrier geometry. I found no prior result contradicting these delimited claims in the checked sources. My targeted searches do not establish global priority, and I do not treat the absence of a search result as evidence of priority.

## Independent verification and presentation

- A source-only isolated copy was built under the `qipm` environment with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. It completed successfully at `/tmp/final-review3-h9kl5k54`, producing 183 pages. The final log had no undefined references, duplicate labels, overfull/underfull boxes, or actual LaTeX warnings. No shared build artifact was changed.
- An independent source check found 35 section files, 499 labels, no duplicate labels, and no unresolved `ref`/`eqref`/`cref` targets.
- As a supplemental check of the most delicate matrix comparison, I generated 120 random feasible PSD allocations with three sources and six columns. The first-power Gram inequalities held, as did the projected quotient bounds on 960 random directions. These checks supplement, rather than replace, the proof analysis above.

The introduction's model distinctions and the part structure make the long manuscript navigable. Its length is closer to a research monograph than a conventional short article, but comprehensive coverage was an explicit objective; length alone is not a correctness or completeness defect. I found no additional actionable readability, consistency, or self-containment issue. After the small integrality edits, my review has no unresolved major or minor mathematical criticism. This conclusion records the result of this review, not a guarantee against errors or a prediction of journal acceptance.
