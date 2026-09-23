# Stage 6, round 1 — independent review 07

**Verdict: PASS.** I found no demonstrable major or minor defect. This verdict concerns the assigned frozen integration stage; it does not replace the separate final whole-paper review.

## Coverage

I reviewed the frozen manuscript at `process/snapshots/stage06-round01`. Its 111-page `main.pdf` has independently checked SHA-256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

I read `main.tex`, `macros.tex`, `references.bib`, and every section and appendix source in full:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`;
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

All these names are relative to the snapshot's `sections/` directory. Full source reading included the abstract, introduction, roadmap, synthesis, qualifications, executable appendix material, and bibliography. I visually inspected rendered PDF pages 95–98, covering the scaling appendix and the beginning of the P-split appendix. Those pages are readable, with no observed clipping. I did not visually inspect every page or rebuild the PDF.

I read the frozen review protocol, Stage 6 review and author assignments, author record, scope proposal, complete coverage ledger, README, and author validation record. I used relevant portions of `results/scaling-disjunctions-hull.md` and read the earlier scaling audit and characterization notes for provenance. Those notes and prior acceptance labels were not substitutes for checking the printed proofs. I did not read another current-round reviewer report.

I read `literature/AGENTS.md` before inspecting original sources. The following table records fresh primary-source inspection, rather than merely bibliography or author-ledger inspection. PDF page numbers below are one-based pages of the inspected file; printed pages are distinguished where useful. Local package names identify `literature/papers/<package>/original.pdf` in the repository root.

| Source inspected | Locator and purpose |
| --- | --- |
| Balas, `balas1998-disjunctive-programming-properties-of-the` | PDF pp. 5–7, printed pp. 7–9, Section 2, Theorem 2.1 and proof: classical disjunctive convexification. |
| Wu et al., `wu2026-variable-aggregation-based-perspective-reformulation` | PDF p. 12, Section 4.1, Lemma 3 and Theorem 3: contextual aggregation comparison, explicitly subject to Assumption 1. Supplementary proofs were not inspected. |
| Starr, saved original `starr1969.pdf` | PDF pp. 12–13, printed pp. 35–36, Appendix 2, Lemma 2 and corollary, including proof: number of exceptional summands. |
| Kronqvist et al., `kronqvist2026-p-split-formulations-a-class` | PDF pp. 4–7, Assumptions 1–4, Remark 1 and formulation; pp. 15–16, Definition 4, Theorem 6 with proof and Corollary 3: published domain and separability scope. |
| Anstreicher, `anstreicher2009-semidefinite-programming-versus-the-reformulation` | PDF pp. 12–13, Section 4, Conjecture 4 and adjacent discussion: point-packing values and separate moment matrices. |
| Khajavirad, original author HTML | [arXiv:2404.03091v1](https://arxiv.org/html/2404.03091v1), formulation, Remark 1, Propositions 1 and 3: exact LP values and the effect of adding RLT. |
| Fawzi–Parrilo, `fawzi2013-exponential-lower-bounds-on-fixed` | PDF p. 3, Theorem 1 and Lorentz-cone discussion: fixed-block constants and scope. |
| Lee–Raghavendra–Steurer, saved original `lrs-sdpsize.pdf` | PDF p. 23, Theorem 3.8 and (3.11); pp. 32–34, Theorems 5.3–5.4 and quantitative density argument: PSD-rank input and its parameters. |
| Braun et al., saved original `braun2013-approxlp.pdf` | PDF p. 18, hard pair and Theorem 6(i): fixed-dilation LP lower bound. |
| Schoenebeck, saved original `schoenebeck-full.pdf` | PDF pp. 6–12, random-instance model, Definition 10, Theorems 11–12 and Lemma 13: width, degree and signed Gram construction. |
| Etessami–Yannakakis, saved original `ey-rmc.pdf` | PDF pp. 26–28, Theorem 5.2 construction: normalization, sign detector and amplifier. |
| Stewart et al., `stewart2015-upper-bounds-for-newtons-method` | PDF pp. 21–22, Section 4.1, (18) and surrounding Newton/conditioning discussion. |
| Esparza et al., `esparza2010-computing-the-least-fixed-point` | PDF p. 34, Section 7, Theorem 7.1 and (14), including proof. |
| Belotti et al., `belotti2012-on-feasibility-based-bounds-tightening` | PDF pp. 1–2, abstract and introduction: linear FBBT fixed-point and iteration context. |
| Lubin et al., `lubin2022-mixed-integer-convex-representability` | PDF p. 12, Lemma 4.1 and proof: parity obstruction. |
| Beach et al., `beach2024-enhancements-of-discretization-approaches-for` | PDF p. 21 of the combined 2022 author version, Section 5.1.1: over- and underapproximation errors. |
| Boland et al., `boland2017-bounding-the-gap-between-the` | PDF pp. 4–6, Lemma 1, its primal/dual proof and Corollary 1: cut-width formula and all-point transfer. |
| Davidson–Donsig, `davidson2007-norms-of-schur-multipliers` | PDF p. 4, Theorem 1.2; pp. 6–7, Theorem 2.4; p. 11, relevant proof: weighted row-norm and density mechanism. |
| Luedtke et al., `luedtke2012-some-results-on-the-strength` | PDF p. 22, Conjecture 1 and conclusion: positive-coefficient constant-factor question. |
| Sherali, `sherali1997-convex-envelopes-of-multilinear-functions` | PDF pp. 8–9, printed pp. 252–253, (13), Theorem 3 and initial proof: symmetric multilinear envelope predecessor. |
| Cornuéjols, saved original `cornuejols-packing-covering.pdf` | PDF p. 78, printed p. 76, Theorem 6.5; PDF p. 84, printed p. 82, Theorem 6.13: Camion's criterion and balanced-matrix distinction. |
| Hassin–Tamir, saved scan and `hassin-02.png`, `hassin-03.png` | Visually read PDF pp. 2–3, printed pp. 380–381, definitions and Theorems 3.1–3.2: series-parallel decomposition. Text extraction was empty, so the scan images were used. |

Saved originals named without a literature package were read from `/tmp/minlp-relaxation-limits-sources/`. I did not copy or modify originals. Source inspection limits, including the distinction between checking a cited input and independently proving it, are stated below.

## Findings

No major or minor findings. No manuscript repair is requested.

## Independent verification

### Scaling, zero scales, costs and rectangularity

I reconstructed `prop:scale-hull` by holding the per-unit point fixed and interpolating only the scale. The map from the per-unit coordinates to a fixed slice is linear, including its intensive coordinates. Thus convexification of a slice commutes with that map, and compactness makes the two-slice hull closed. Equal extreme scales cause no division because that case is explicitly separated. For multiplicities at a positive integer count, averaging the same-scale points associated with individual units proves one inclusion; identical copies prove the other. The shared intensive coordinate is preserved by this averaging. At count zero, the declared projection off-state is necessary and is consistently used.

I separately checked the conic zero-weight argument. A feasible homogeneous lift at weight zero adds to a feasible lift at weight one along every nonnegative multiple because the target is a convex cone. A nonzero projected direction would make the projected slice unbounded. Compactness therefore forces the projected direction to be zero even if the auxiliary lift is unbounded. Conversely the all-zero homogeneous vector is feasible. This avoids assuming compactness of the lift itself.

The scale-cost example does not follow merely from nonconvexity: its per-unit set is convex. Mean scale one forces the zero- and two-scale masses to agree; the target has extensive-minus-intensive coordinate one-half, which requires at least one-half mass at scale two. Consequently the cost is at least one, and the displayed endpoint mixture attains one. The separately convexified scale cost at one is zero. My exact finite-atom LP enumeration reproduced this value.

For `prop:scale-perspective`, I derived the operating-cost lower bound with weights proportional to mass times scale, and the scale-cost lower bound with the original masses. The converse works because the extensive-only domain is independent of scale: the product of an attaining per-unit distribution and an attaining scale distribution has the desired extensive mean and attains both costs simultaneously. This argument would not preserve an arbitrary unscaled intensive mean, explaining the manuscript's restriction. At mean scale zero, every active scale is zero, so the correct value is the original zero-scale cost. Convexifying the per-unit cost graph before taking a perspective is also necessary, as the absolute-value two-point example shows.

For `prop:scale-rectangularity`, the diagnostic cost is nonnegative and vanishes only at the interior catalogue scale. Attainment of zero cost therefore confines every atom to that scale. Endpoint mixing then puts `alpha*T1 + (1-alpha)*T0` into the fibre at a fixed extensive point. Iteration multiplies the remaining displacement from `T0` by `alpha^j`; compactness closes the limit and makes the fibre equal to the entire intensive projection. The converse uses the same per-unit point at every scale of an attaining scale-cost representation, followed by decomposition into original per-unit atoms. The statement's zero-scale off-state and interior-scale hypotheses are used essentially. With only two scales, the scale masses are fixed by the mean, so universal scale-cost separation does not imply rectangularity. Affine costs likewise cannot diagnose it.

The integral-count hull requires integrality of the count polytope, not an integer-decomposition property: fix a per-unit convex-hull point for each type while decomposing the count vector into integral vertices. The Shapley–Folkman comparison has at most `min(d,n)` replacements; each replacement costs at most the diameter in the chosen norm. The stated Lipschitz and relative-gap qualifications, and the warning that added balances can invalidate rounded feasibility, are needed and present. Balas and Starr receive classical credit; the local cost counterexample and criterion are proved rather than asserted to follow from those sources.

### Whole-manuscript checks

- I reconstructed the induced-cut expression, the half-integral-cell transfer, and the orientation/row-norm estimates. The manuscript distinguishes its graph translation from the classical Davidson–Donsig mechanism. I checked the positive common-upper coupling, the dyadic count cap and digit-reversal construction, and the harmonic argument's inactive-mass normalization. The cloning argument needs concentration uniform over the finite vertex set, which the proof supplies.
- I followed all three cubic coupling cases and the scalar certificate, including the determinant and Bernstein slack, and checked the adjacent-count equal-mean argument. The finite certificates supplement the universal argument; they do not purport to establish it by enumeration.
- I checked the incidence orientation arguments, feedback-frequency restriction, and the series-parallel active/blocking invariant through both composition operations. The ambient balanced orientation is fixed before restriction. The use of Camion's all-Eulerian-submatrix criterion is not conflated with balancedness. The coefficient-spread conclusion uses a global extremal ratio and does not require a false Schur-concavity assertion.
- I followed the falling-factorial moment construction, degree-preserving endpoint interpolation, and repeated localizers for cardinality nodes. The tensor construction preserves positivity for global squares and the required localizers. The relative-block argument retains its target and feasible-witness normalization.
- I checked the XOR degree budgets before and after monomial lifting, including degrees `4r` and `4rD`, the constant signed Gram class, deletion of high-degree variables, and the rank bound from the union of basis supports. The full-box quadratic graph hull is correctly distinguished from the graph over feasible XOR points. I also checked the separate order-one upper-quadratic argument.
- I reconstructed the supporting point-packing covariance construction, including diagonal and all coordinate-pair RLT bounds. The exact arithmetic check below covers these inequalities; positive semidefiniteness follows separately from the projection-block covariance argument. The cited values agree with the inspected Anstreicher and Khajavirad formulations.
- For P-split, I checked the global-domain obstruction, the retained-box repair and the fixed-coordinate Jensen step. I followed the translated-ball truncated-square auxiliary hull, projection distance and positive Hausdorff derivative, and the rational rotation calculation. The counterexample concerns the published assumptions actually inspected in Theorem 6; the repaired coordinate-domain assumptions are explicit. The auxiliary-only and aligned-image examples address different relaxations.
- For rank-one formulations, I checked the correlation face and exposure argument, rounding of approximate rank-one factors, and propagation of the constants `136m+10` and `184m+6`. The LP and SDP conclusions use different sandwich assumptions. The PSD signed-slack shift and its prefactor, and the extra `q+1` block after facial reduction, are retained. These are global lift-size comparisons, not spatial-node lower bounds.
- For FBBT, I followed sound monotone primitive updates to the least fixed point under fairness, and checked the sign detector and repeated-squaring amplifier. The slow primitive-update lower bound is schedule independent within the stated model. The manuscript distinguishes residual from distance and does not transfer the claim to accelerated or Newton updates. The cited predecessor constructions support the attribution without supplying the manuscript's entire primitive-schedule proof.
- I checked the integer parity closure argument, the geometric diameter/area/width consequences, exact square discretization errors, and the simultaneous tolerance normalization. These compare precision and geometry with separately specified certificate resources.

The abstract, roadmap and synthesis preserve the main distinctions between pointwise widths, node oracles, global extension sizes and primitive iterations. The coverage ledger's bounded and open developments remain qualified in the manuscript; in particular, the manuscript does not claim the arbitrary-affine extension or a solver-independent complexity result.

### Executed checks and their limits

I wrote and ran `verification/reviewer07/stage06-round01/check.py`; output is saved in `results.json` in the same directory. It uses Python integers and `Fraction`, with no floating-point optimization solver.

The independent scale-cost routine enumerates affinely independent feasible supports and solves their equality systems exactly. A minimum over these supports gives the finite LP optimum. It checks the nonrectangular scale-cost gap, 25 rational rectangular diagnostic targets, and 117 extensive-only perspective targets. The latter use per-unit points `{-1,2}`, operating costs `{3,-2}`, catalogue `{0,1,3}`, and scale costs `{1,-3,1}`. They include scale zero, negative costs, and both linear pieces of the lower scale-cost envelope.

For point packing it checks 10,990 ordered coordinate-pair instances for sizes 5 through 25, all four RLT inequalities, diagonal identities, and the minimum pairwise distance. It does not use a numerical eigenvalue test or establish positive semidefiniteness computationally.

The same script extracts and executes both complete printed cubic checker blocks. They pass all their stated finite grids, including the three-group grids of sizes 7, 9 and 65 and the two-group grids of sizes 5, 9, 13 and 17. This is a replay of the printed algorithm, not an independently designed verification of every cubic certificate. All checks completed successfully. None of these finite runs establishes a universal theorem.

## Remaining limits

This review includes a complete manuscript source reading and targeted primary-source checks, not a fresh proof of every external theorem or a complete reading of every bibliography original. In particular, I did not independently reprove the deep PSD-rank lower bounds, the random-XOR expansion input, the sharp Khintchine theorem, or optimization/separation equivalence. I checked the inspected quantitative inputs and their use in the manuscript. The manuscript's local derivations remain the basis of the other proof checks.

Originals not freshly inspected include McCormick, Szarek, Hoeffding, Del Pia–Khajavirad, Barrus, Adams–Gupte–Xu, Edmonds, Deza–Onn, GLS, Karp, Altschuler–Boix-Adserà, Jarre, Grigoriev, Potechin, Padberg, Coniglio, Ahmadi et al., Beame et al., and Fleming et al. This is an explicit source-verification limit, not an assertion that those references are wrong. The Coniglio publication-identity qualification and the Wu supplementary-proof access limit have not been independently removed by this review. I did not attempt exhaustive priority clearance.

I did not rerun every historical repository experiment, test solver licenses, or reproduce a clean TeX installation. The rendered inspection is limited to pages 95–98; the rest was read as complete source. The supplied build and author-validation records are secondary evidence, distinct from the executed reviewer checks. No formal proof verification or exhaustive search over arbitrary affine reformulations was performed.
