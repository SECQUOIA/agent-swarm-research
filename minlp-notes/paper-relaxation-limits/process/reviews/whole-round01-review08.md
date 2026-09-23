# Independent whole-paper review 08

**Verdict: PASS.** No major or minor findings. The additional focus was the published P-split nonexactness claim, retained domains, its directional repair, and the exact two-ball relaxation. That focus did not narrow the manuscript reading.

## Coverage

The reviewed target is `process/snapshots/whole-round01/main.pdf`, 111 pages, with SHA256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. I verified the hash. All manuscript references below concern this frozen snapshot.

I read the entire manuscript source, including every proof, remark, displayed certificate, appendix, and bibliography: `main.tex`, `macros.tex`, `references.bib`, and the following files under `sections/`:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`;
- `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `appendix-finite-signings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-couplings.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I also read the frozen review protocol, whole-paper assignment, scope proposal, claim-coverage ledger, stage-06 author record, stage-06 correction log, README, and relevant source/version records. I checked the reviewer-focus assignment. The coverage ledger's distinctions between completed results, bounded developments, source corrections, and open questions agree with the manuscript. I did not read another report from this final round or rely on prior PASS labels.

I read `literature/AGENTS.md` before consulting local originals. Primary-source checks included the following passages; these are targeted source checks, not claims to have read every cited work in full.

- Kronqvist–Misener–Tsay: the original's retained compact convex domain, component bounds, minimal-sharing Assumption 3 and Remark 1, epigraph construction, Corollary 3, Definition 4, and Theorem 6 with its complete proof. I inspected the relevant original pages visually as well as in text, and checked the publisher's version metadata. The original PDF hash was `0122c8371b2d7114dddc6e01de3408295438864b94970fbb65d71857b5aaf46d`. The [publisher version](https://link.springer.com/article/10.1007/s10107-025-02232-1) is consistent with the manuscript's citation and the challenged statement.
- Schoenebeck: Definition 10, Theorems 11–12, Lemma 13 and its proof, and Remark 1 in the recorded author full version. I checked the closure width and level conventions used in the transfer.
- Cornuejols: Theorem 6.5 and its surrounding Camion argument, and Theorem 6.13 with its balanced-matrix statement and proof. Hassin–Tamir: the scanned original's printed pages 381–382, including Theorem 3.1 and the series-parallel terminal conventions. Text extraction of that scan was empty, so I used rendered pages.
- Davidson–Donsig: the real projective/Grothendieck statement, weighted estimates, and surrounding row-norm discussion in the local source extraction. Some equations in that extraction were absent; this source check has that limitation. Luedtke et al.: the original's concluding Conjecture 1. Sherali: the symmetric-box formula and Theorem 3 in the original.
- Lee–Raghavendra–Steurer: the quantitative rank theorem, the pseudo-density result and normalization, and the relevant exact corollary in the original. Fawzi–Parrilo: Theorem 1 and the fixed-block and Lorentz-cone conventions. Braun et al.: Section 4.1 and Theorem 6(i) in the explicitly cited July 2, 2013 version; a different local version has different theorem numbering.
- Belotti et al.: Theorem 4.1 and its nonempty-limit condition. Etessami–Yannakakis: Theorem 5.2's circuit normalization, complementary monotone construction, detector, and amplifier. Lubin–Vielma–Zadik: Lemma 4.1 and its parity proof.
- Altschuler–Boix-Adsera: Section 7.2, Theorem 7.4 and the following precision question, Corollary 7.5, and the arithmetic convention. Khajavirad: the four stated packing values and their parameter ranges in Propositions 1 and 3 of the primary arXiv version. Beach et al.: the cited combined preprint's sawtooth-error comparison in Section 5.1.1.

Other cited classical dependencies were assessed through their stated hypotheses and their use in the manuscript, without independently reading or reproving all their original sources. I have not performed a comprehensive priority audit of all related literature.

## Findings

None. No repair is requested. In particular, the retained-domain correction is a demonstrable counterexample to the universal source statement, and the text confines that correction to the theorem's scope. It does not claim that P-split formulations are invalid.

## Independent verification

### Whole-paper mathematical review

I reconstructed the proof chains and attempted to break their hypotheses and endpoint cases, rather than treating the supplied scripts as proof.

- The vertex-law envelope representation, induced-cut reduction, squared-weight local cut estimate, fractional orientation, and density constants are consistent. The positive-coefficient normalization preserves inactive mass; the harmonic fixed-point argument and the asymptotic denominator are consistent. The dyadic/radix capacity arguments keep the required marginal probabilities.
- The cubic mixture and scalar-minorant arguments cover their stated cases. The finite certificates, witness normalization, equal-mean specialization, and distinctions between limits and attained finite values are consistent.
- Incidence ownership, the feedback repair, frequency-two half-integrality, and the odd-cycle argument retain the baseline coverage contribution. The convex-table/matching reduction and the series-parallel coloring argument use the needed integrality statements. I checked that the balanced-matrix comparison is not substituted for the stronger total-unimodularity statement required elsewhere.
- The positive physical-box coupling uses the full ambient law and the global lower and upper endpoints. Its finite-spreading argument and unequal-box counterexamples do not assert an unjustified common relative-coordinate law. The PARTITION expansion and rational certificate support exact complexity; the manuscript does not promote this to a fixed-additive-error lower bound.
- The spatial-cardinality endpoint exclusion, tolerance boundaries, and first SDP witness are consistent. In the preordering argument, repeated equality-slack factors and the degree remaining for all localizers are accounted for. The tensor argument handles squares coupling distinct blocks, rather than only blockwise squares. The coordinate-graph endpoint interpolation preserves the complete product identities needed for the stated comparison.
- The XOR character closure and Gram construction fit the source width. The occurrence deletion and degree losses are explicit. The quadratic realization is correctly distinguished from membership in the original product graph. The parity-basis support count and both order-one monomial bounds use their stated normalization and certificate classes.
- The packing, scaling, and rank-one comparisons preserve their different feasible sets and notions of complexity. In particular, the universal scale-hull result retains the rectangularity hypothesis, the perspective cost correction handles zero scales, and the rank-one face and stability arguments keep the sum and error constants. The LP, fixed-block SOC, and PSD lower bounds are not conflated with pointwise width or a single-node bound.
- The FBBT construction specifies primitive contractors and fair schedules; the source fixed-point statement's nonempty hypothesis is retained. The PosSLP encoding and slow-update construction are scoped separately. The integer-convex comparison applies midpoint parity only under the stated mixed-integer representation assumptions.

### P-split reconstruction and falsification attempts

For the exact retained box, both disjuncts are nonempty, disjoint, and strictly convex quadratic sublevel sets before intersecting the box. Their union contains every box vertex. Thus its convex hull is the box, forcing any valid convex relaxation that retains the box to be exact. The proposed lift `(3t, 9-3t, 1)` is the indicated convex combination of auxiliary feasible points; all three epigraph links hold throughout the box. The higher-dimensional weighted-square construction preserves this argument. In the source proof, equal transverse coordinates defeat strict componentwise Jensen slack, and an outward perturbation can leave the retained domain. Both issues are real and directly visible in the example.

For the directional repair, convexity supplies the interpolated auxiliary point. Finiteness supplies a common radius for all positive-slack links, continuity preserves those links, and the hypothesis explicitly preserves every zero-slack link and the domain. The supporting functional then increases strictly. The assumption that the relaxation contains the entire true feasible set is necessary for the claimed strict containment and is present.

For the balls, fixing the transverse auxiliary vector reduces the auxiliary disjunction to two rectangles, with thresholds `h = r^2 - sum(c_i)` and `U = (d+r)^2`. Their convex hull is exactly the square truncated by `a+b <= U+h`; each vertex is in one rectangle. Downward closure permits substitution of the actual squares. Completing the square gives the claimed cylinder intersected with an ellipsoid, which also implies every retained box bound. The two-group model reduces to the same inequalities even though its initial transverse global upper bound is larger.

At transverse radius `rho`, the left boundary has outward displacement `e(rho)`. The derivative of `e(rho)^2 + rho^2` with respect to `rho^2` is `1/2 + d/(4 sqrt((d/2+r)^2-rho^2/2))`, which is positive under the stated assumptions. Thus the largest capsule distance occurs at `rho=r`; the displayed Hausdorff formula and its `sqrt(2)-1` normalized limit follow. This also checks the end-cap geometry and the zero distance at `rho=0`.

I checked the rational orthogonal map, original witness, exact transformed domain argument, and constant aligned error. The strongest auxiliary-only comparison uses just the two center images, so convexity alone preserves the witness. In aligned coordinates the decreasing concave envelope in the transverse square yields the two end-cap bounds and hence the capsule. This does not confuse the convex hull of auxiliary values with the full original–auxiliary graph hull.

### Exact and numerical artifacts

All artifacts are under `verification/reviewer08/whole-round01/`.

- `check_independent.py` independently enumerates vertices of the proposed ball auxiliary polyhedron using rational Gaussian elimination and exact inequalities. It covers one, two, and three transverse auxiliaries at three rational radius/separation pairs, giving 8, 11, and 14 vertices respectively. Every enumerated vertex lies in an original auxiliary disjunct. These nine finite exact checks supplement the general rectangle proof; they do not prove it for arbitrary parameters or dimension.
- The same checker uses symbolic algebra to verify the square completion, radial derivative identity, orthogonality, determinant, and rational witness coordinates. These are exact identities.
- A numerical grid of 10,001 radial values at each of seven separation/radius ratios, from 2.00001 through 1000, found no larger distance than the claimed endpoint maximum, with comparison tolerance `1e-11`. These are finite floating-point falsification attempts, not universal certificates.
- I extracted and ran the actual printed finite-signing and cubic-certificate code from the frozen appendix files. The signing output is `[1, 2, 4, 4, 5, 8]`; every printed cubic certificate passed. This is explicitly a replay of the manuscript's exact integer/rational computation, not an independently designed implementation of those enumerations. `checks.json`, `checks-output.txt`, and the two `*.tex.printed.py` files record the checks.

### Build and visual review

I copied the frozen TeX inputs into my own `build/` directory and ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with that explicit working directory. The build succeeded and produced 111 pages. Its layout-preserving extracted text is byte-for-byte identical to the frozen PDF's extracted text (`build-text.txt` and `manuscript.txt`). This comparison establishes text/layout-extraction agreement, not PDF-byte identity.

The final build has no unresolved reference/citation warnings or overfull-box diagnostics. There are three underfull-box diagnostics. I found no associated clipping or material readability problem.

I visually inspected contact sheets covering every page, 1–111, and higher-resolution pages 97–100 containing the P-split development. The whole-document contact sheets support a layout and pagination check; they are not a claim that every small equation was readable at thumbnail scale. The complete mathematical reading used source and extracted text. I also inspected the original P-split theorem pages and the relevant scanned Hassin–Tamir pages at readable resolution.

## Remaining limits

The review found no contradiction, missing necessary hypothesis, unsupported scope expansion, or required coverage omission in the frozen paper. This is a mathematical review with exact finite checks and selected primary-source verification, not a formal proof certification. I did not independently reprove the external Grothendieck, algorithmic optimization, SOS lower-bound, or extension-complexity theorems, and did not read every cited original in full. The source-extraction limitation for some Davidson–Donsig equations is stated above. Numerical grids certify only their sampled instances. Visual inspection was exhaustive at overview scale and selective at full reading scale.

The manuscript's explicitly open questions remain open; the bounded results do not purport to resolve them. These limits do not require a change to the reviewed claims.
