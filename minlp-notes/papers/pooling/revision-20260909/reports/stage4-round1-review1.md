# Independent Stage 4 review 1

I recommend proceeding with Stage 4. I found no major or minor correction that is required for the mathematical claims I reviewed. One optional attribution improvement is listed below. This is an independent review, not proof certification or a presumption that the other reviews will reach the same conclusion.

I reviewed the frozen `revision-20260909/stage4-round1/` sources and the 104-page PDF at `revision-20260909/checks/stage4-author-build/source/main.pdf`. I did not read current author or reviewer reports, change the manuscript, or delegate review work. All paths below are relative to `papers/pooling/` unless identified as repository paths.

## Coverage and mathematical assessment

### Introduction, synthesis, and dependencies

I read all of `sections/00-introduction.tex` and `sections/06-synthesis.tex`, including the abstract, contribution statements, physical-boundary table, literature comparisons, and open-question discussion. Their summaries retain the important distinctions: threshold versus zero-lower-bound feasibility; actual feed/outlet degree versus bypass degree; fixed quality rank versus two complete input vectors; standard economics versus arbitrary arc costs; fixed-dimensional certificates versus algorithms; and explicit response size versus optimization complexity.

I checked the relevant earlier-section dependencies against the actual statements and, where used by Stage 4, their arguments:

- Section 1: the standard physical model, homogeneous zero-flow conventions, common throughput bounds, finite rational encoding, active-quality normalization, and the identity `s1:rank-one-form`. These support the physical reconstruction and isolated-block normalization in the appendices.
- Section 2: the two ETR-complete class statements, the single-pool correspondence, the algebraic-witness theorem and its stated source scope, and the full basis-index certificate and pooling NP-membership arguments. The introduction does not convert the certificate result into polynomial optimization or infer nonmembership in NP from irrationality alone.
- Section 3: the simultaneous all-two degree family, pure-mode replacement and approximation transfer, the explicit positive-product estimate `s3:matsui`, the full explicit Hoffman bound `s3:hoffman`, and the fixed-data contracted construction and subsequent completion objective `s3:constant-thm`. The Hoffman constant used in Appendix A follows by putting its integral coefficient bound equal to one. The contracted feasibility comparison in the introduction agrees with the physical threshold already encoded before completion.
- Section 4: the full fixed-core proof, including parameter-dependent local vertices, uniform support formulas, compact optimization, and common-field recovery; the planar-composition and balanced path-projection proofs; and the bounded-attachment/objective-scope and degree-two/three comparison statements. The dense objective retained by Appendix A's shadow is outside the two-endpoint projection theorem, as the manuscript says.
- Section 5: the scope table, general quasipolynomial parameter-path proof, strip statement and construction, bounded-exception quality-space proof, restrictive common-throughput argument and optimization corollary, and the complete two-vector convex-QP correspondence and endpoint treatment. The synthesis does not combine hypotheses from these distinct algorithms. I did not independently reprove every earlier-stage gadget and every earlier-stage literature theorem; this was a Stage 4 review with dependency checks, not a new complete review of Sections 1–5.

The shared-helper counterexample in Section 6 preserves the distinction between a private midpoint supply equation and a shared total. The proposed open structural question is not contradicted by the retained hardness statements: those statements either let the relevant dimensions grow or allow degree-three external coupling. The text correctly keeps feasibility and dense economic optimization separate.

### Appendix A: response geometry and physical realizability

I checked every proof and concluding scope statement in `appendices/A-response-geometry.tex`.

1. The weighted identity in `s6:certificate` telescopes with the stated coefficient `(1-epsilon) epsilon^(2(n-j)-1)`. Its zero set is precisely the endpoint vertices, and the squared-distance exposure argument is valid. Distinct terminal values follow by reversing the two disjoint branch intervals.
2. The physical internal product has exactly the capacity inequality `t_j >= t_(j-1)` and the midpoint-quality inequality `t_j <= s_j-t_(j-1)`. The scaling therefore realizes the specified Klee–Minty path, with all remaining flows uniquely determined.
3. The economic coefficients in `s6:price-response` are consistent with ordinary product revenues: `d_j/s_j=3s_j`, and the base constant is independent of the varied terminal price. Exposure persists into the interior even for the first and last vertices. The two-quality reset relays copy the intended signal. After dropping lower contracts, every deleted equation has a nonnegative deficit; the two revenue bonuses reward exactly source throughput and reset-product throughput. The uniform Hoffman repair and `M=3H+1` therefore force every optimizer back onto the contracted face. Large revenues have polynomial encoding; the result does not assert bounded revenue magnitudes.
4. The explicit-formula lower bound counts distinct line factors in the product of the defining polynomials. It concerns price and value alone, and does not rule out the given linear-time support recurrence, extended formulations, or circuits. The fixed-objective message has one fewer interval than the price-response value function, consistently with its projected vertex count.
5. The two-variable-per-row coordinate-port obstruction is valid under coordinate projection. It would not be a valid objection to arbitrary linear images, which the manuscript explicitly excludes.
6. The interface in `s6:vertex-forcing` forces `AP=t`, `BP=PW=1-t`, `PV=BW=t`, and active quality `q=2-t`. Its remaining nonredundant quality constraint is exactly `z >= t-t^2`. All physical arc bounds, exact supplies, product contracts, and the unit pool throughput are compatible, including `t=0,1`. The ordinary economic objective equals the claimed `d^T x-z`. The only undirected cycle is the triangle B–P–W–B; the attached path introduces none.
7. The local-optimum perturbation preserves nonnegative bounded prices. The denominator bound separates every pair of distinct terminal values sufficiently for the directional derivative to be strictly negative on every incident edge. The tangent-cone argument then yields strict local maxima in the complete feasible set, including the clean-flow coordinate.
8. The integer-coordinate lower bound is an application of parity to lifts of all `2^n` distinct optimal points. The binary convex-hull construction gives the matching upper bound without claiming a polynomial formulation size.
9. The LP hull identity follows by vertex decomposition on its lower affine boundary and interpolation to the upper boundary. Every hull vertex is physically feasible. The instruction to return an optimal vertex, rather than an arbitrary point on an optimal LP face, is necessary and is present.
10. The relay version uses the same physical interface and price telescoping. For general supplies the unweighted physical identity also telescopes, with coefficients `s_(j+1)-s_j`; strict supply growth separates the endpoint branches. The fixed numerical perturbation is correctly restricted to the geometric supplies.
11. The explicit counterexample after `s6:alphabet-geometry` shows that the nonlinear interface's lower throughput contract cannot simply be dropped. For example, the profitable point also works at the smallest permitted dimension n=2.
12. The dense-slab reduction correctly rounds its endpoint bits, retains a nonempty compact domain, and gives polynomial binary encoding in both variants. The padding version must retain the singleton upper bounds on padding coordinates, which the statement allows. Nothing in this abstract proof establishes a physical degree-two slab realization or strong hardness.
13. The rank-one matrix-parameter argument is exactly a union of two LP projections, with the zero aggregate handled separately. The rank-two observation and Square-Root Sum example are properly confined to their abstract models. The singleton nonlinear leaves give an arithmetic implication, not an NP-hardness claim.

A fresh independent exact checker, `checks/stage4-review1/check_physical.py`, assembled the original descending-path and interface flows, all supply and product totals, pool mass and quality, product-quality inequalities, and the original source/product economics. It passed **2,556 rational cases for n=2 through 7**, including all vertices, convex combinations of distinct vertices, and three clean-flow values per path point. It also checked every endpoint-bit edge derivative for the stated local perturbation. These finite checks supplement the general arguments; they do not certify arbitrary dimensions, global optimization by a numerical solver, or the relay penalty theorem.

### Appendix B: isolated rank-one block

I checked every proof in `appendices/B-rank-one-costs.tex`.

- The double-centering formula gives the least residual rank after additive row/column subtraction. Its rational factorization is computable with polynomial encoding.
- The projected boxes have fixed dimension for fixed interaction rank. Incremental segment addition retains polynomially many vertices and witnesses. Every slice vertex lies on an original vertex or edge. Enumerating all pairs includes all needed edges and adds only feasible candidates; equal-total edge interiors are not required.
- On each common-total interval the objective has precisely the form `alpha S+beta+gamma/S`. The treatment of endpoints, positive stationary minima, constant cases, zero total, comparisons between quadratic algebraic values, and original-margin recovery is complete. The dimension dependence is polynomial for fixed rank, without an FPT claim.
- The rank-one-cost specialization checks all four endpoint products, including signed factors, and has the stated sorting-and-sweep operation count when the factorization is supplied. Dense input/output work is disclosed separately.
- The Lagrangian cost has interaction rank at most the number of attribute columns; the oracle retains only the isolated margin constraints and does not assert zero duality gap.
- The maximum-edge-biclique reduction accommodates arbitrary unequal graph-margin totals using dummy margins. The sign threshold is unchanged by division by positive total. A selected nonedge has enough positive cost to destroy a threshold witness, and the no-instance gap follows from binary minimization of the bilinear numerator.
- The unit-margin repair covers positive totals above and below one, as well as zero. The exact penalty has the correct sign and magnitude, preserves a negative threshold, and retains strong encoding bounds.
- The rational-threshold certificate argument is stronger than rationality of an optimizer and does not conflate them: after multiplying by positive total, a quadratic sublevel test has a rational interval minimizer or rational stationary minimizer. When the pattern interval reaches zero, its zero endpoint has zero numerator, so it cannot improperly supply a strict negative minimum. The field and bit bounds are consistent with irrational exact optimizers.
- The one-fixed-margin-dimension algorithm needs only exponentially many patterns in that dimension; its other dimension enters through affine weight crossings and greedy prefix breakpoints. The stated FPT dependence is supported.

### Appendix C: exact and approximate lifts

I checked every proof in `appendices/C-rank-one-convexification.tex`.

- Equality in the trace bound forces identical binary row and column margins. Successive nonnegative cross-pair and maximal-total face restrictions leave precisely one selected entry per pair. The displayed affine inverse reconstructs every block and is valid on the whole correlation face.
- Fixed-order PSD block bounds, Lorentz-cone decomposition, and unrestricted PSD order transfer through affine sections and images. Scalar inequalities are explicitly counted, avoiding a hidden uncharged polyhedral part.
- The two-by-two curved face proves nonpolyhedrality even under unit upper margins and zero lower margins. Hence the finite exact LP lift is impossible, independently of the asymptotic correlation transfer.
- I recomputed the rounding estimates: margin distance is at most `2SD`; binary rounding bounds are `6SD` and `8SD`; the generator estimate is `8mB+116mD+5|S-m|`; averaging the excess-total bound gives the final `28mB+156mD+5(m-T)`. The possibly negative final bracket is correctly identified and does not invalidate the bound.
- The section error is `(184m+6) eta`; multiplication by m gives the stated `A_m`. The LP sandwich uses coefficient infinity norm one and dilation factor two, exactly matching the cited fixed-factor result.
- The valid-slack factorization uses facial reduction to obtain strict feasibility, dual attainment, and a nonnegative constant. The extra scalar PSD coordinate accounts for that constant, so the bound is q+1 rather than an unjustified q.
- For the approximate SDP result, the shifted function remains in [0,1], has mean at least `1/(6k)`, and its pseudo-density expectation satisfies the strict hypothesis with `delta=1/(16k^2)`. Substitution gives the stated `k^(-23/4)` prefactor and `k^(13/2)` denominator inside the exponential base. The choice of odd k produces the claimed exponent including the logarithmic loss.
- The signed-correlation block map has entrywise operator norm m. It transfers the whole-matrix error bound without treating diagonal extraction as dimension independent. The final support-gap interpretation uses the specified dual norm and is a uniform, not objective-specific, guarantee.

## Source verification and novelty limits

I independently extracted text from the actual archived `original.pdf` files for Dey–Kocuk–Santana, Fawzi–Parrilo, Lee–Raghavendra–Steurer, Braun–Fiorini–Pokutta–Steurer, Gärtner et al., Lubin–Vielma–Zadik, and Punnen–Sripratak–Karapetyan. The new extractions are under `checks/stage4-review1/`. I did not rely on the repository's existing extracted text or paper metadata to resolve version-sensitive theorem numbers.

The following primary-source comparisons support the manuscript's scope:

- Gärtner et al., Section 4, uses the same recursively defined cube and the displayed powers in its shadow direction. The stated `1/15` parameter bound at epsilon=1/4 follows from its geometric sum. The manuscript credits the shadow phenomenon and supplies a separate physical realization and certificate.
- The Dey–Kocuk–Santana original PDF explicitly states the simultaneous-margin conjecture immediately after Theorem 4. Appendix B addresses that precise linear-objective set, rather than claiming to establish hardness of the separate squared-error approximation problem.
- The published [Jalilian–Kocuk PDF](https://research.sabanciuniv.edu/id/eprint/52174/1/Improved.pdf), Theorem 2, proves SOC representability and discusses its exponential construction. The archived original is the earlier version with this result as Theorem 1. The bibliography distinguishes these versions correctly. Published Lemma 1 is also the direct margin-pattern precedent relevant to the optional note below.
- Fawzi–Parrilo Theorem 1 has the fixed-PSD-order exponential block bound used here. The [46-page LRS full manuscript](https://www.dsteurer.org/paper/sdpsize.pdf) supplies the exact PSD exponent, the odd-dimensional pseudo-density norm, and equation (3.11) with the quantitative factors used in Appendix C. The archived original extraction agrees with those locators. The proof does not substitute the shorter conference version for the full result.
- The [BFPS author manuscript](https://www.bayesianestimation.org/paper/approxlp.pdf), Theorem 6(i), states the fixed-dilation sandwich lower bound for the correlation inequalities used by the manuscript. Its scope includes dilation two.
- Punnen et al.'s Sections 3.2–3.3 give fixed-rank and rank-one bipartite box precedents. The [Hladík–Černý–Rada paper](https://arxiv.org/pdf/1911.10877) concerns fixed-rank quadratic box optimization and zonotope methods. Neither inspected statement directly solves the shared-total normalized margin problem proved here.
- Lubin–Vielma–Zadik Section 4.2 supplies the midpoint/parity representability obstruction. The manuscript does not claim that general argument as new.
- The [Grothey–McKinnon preprint](https://arxiv.org/pdf/2002.10899v1), Section 3, contains the earlier small multiple-local-solution pooling example. The manuscript's comparison is explicitly restricted and avoids an exhaustive priority claim.
- The [Boveroux et al. 17-page preprint](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf), Section 3.3, treats the one-nonzero-column case. The manuscript's two-LP extension is stated for joint minimization; its exclusions concerning a direct parameter objective or genuine max–min problem are appropriate.
- The [Gillis–Glineur original manuscript](https://optimization-online.org/wp-content/uploads/2013/01/3718.pdf) studies the squared-Frobenius rank-one approximation connection to maximum-edge biclique. Appendix B describes that objective distinction accurately.

Peeters' publisher DOI did not return readable content in this browser session. The general maximum-edge-biclique NP-completeness input is standard and is also identified in the inspected Gillis–Glineur source, but I do not claim an independent line-by-line audit of Peeters' proof. I also did not independently reprove the cited conic lower-bound machinery. Targeted public searches did not identify a conflicting pooling ETR result or a prior theorem settling this exact margin conjecture; absence from that search is not proof of novelty. The manuscript's limited novelty language is warranted by the inspected sources and leaves that evidence limit visible.

## Standalone completeness and presentation

I read `main.tex`, all bibliography entries, `README.md`, and all of `source-index.md`. The main file includes all three appendices before the bibliography. The five incorporated companion-note groups now have proofs in those appendices, and the eight removed comparisons are not essential dependencies of retained Stage 4 claims. I verified all thirteen recorded source SHA256 values against the repository files; all match. I did not read the unrelated source notes merely to substitute them for the manuscript proofs.

The supplied PDF has 104 pages. Its retained build log contains no reported undefined-reference, missing-citation, or overfull-box warning in the checked categories. I inspected the rendered physical-interface figure and its surrounding theorem/proof on page 87; the drawing, labels, caption, formulas, and text are readable and agree with the source. This was selective visual inspection, not a page-by-page typography audit.

The README distinguishes finite exact checks from numerical LP checks and from general proofs. Its process links are evidence pointers, not proof dependencies. The frozen review copy is not itself a relocation of every repository check script; I evaluated its documentation links in their intended `papers/pooling/` location rather than reporting the snapshot's extra directory depth as a manuscript defect.

## Findings

### O1 — Optional: identify the immediate margin-pattern precedent

**Locator:** `appendices/B-rank-one-costs.tex`, lines 291–303, in the proof of `app:margin-certificates`; related comparison in `sections/06-synthesis.tex`, lines 92–97.

**Severity:** Optional scholarly clarification. This is not a proof gap, a false novelty claim, or a required correction.

**Rationale:** The proof's at-most-one-free-row/column margin pattern has a particularly close antecedent in published Jalilian–Kocuk Lemma 1 and the beginning of their Theorem 2 proof. The manuscript already cites their SOC theorem in the synthesis, but an adjacent citation in Appendix B would help readers see which structural observation is established and which arithmetic and algorithmic conclusions are supplied here. The new rational-threshold witness, quadratic-field output, and dimension-parameter conclusions remain separate claims.

**Concrete repair:** Add one sentence near the margin-pattern argument: “The same at-most-one-free-margin structure underlies Lemma 1 and the SOC construction of Jalilian and Kocuk; here we use the common-total parametrization to obtain exact arithmetic and certificate bounds.” Retain the present self-contained proof.

## Verdict

**Major findings: none. Minor findings: none. Optional findings: O1 only.**

For the reviewed Stage 4 scope, the current statements, proofs, encoding qualifications, physical reconstructions, and literature distinctions are coherent. No mandatory manuscript correction follows from this review. Remaining limits are the stated finite scope of computational checks, selective dependency verification of earlier stages, and the inability of a literature search or internal review to establish exhaustive priority or formal proof certification.
