# Stage 6, round 1: independent review 05

**Verdict: PASS.** I found no demonstrable major or minor defect in the assigned frozen manuscript. The additional XOR and monomial focus survives the falsification attempts described below. This is a review of the stated models and claims, with the source and verification limits recorded below; it is not a claim of formal verification or a substitute for the separate final whole-paper review.

## Coverage

The reviewed artifact is `process/snapshots/stage06-round01/main.pdf`, 111 pages, SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`. I independently computed this hash. All manuscript locations below refer to that snapshot.

I read the frozen `process/review-protocol.md`, `process/stage-06-review-assignment.md`, `process/stage-06-author-assignment.md`, `process/stage-06-author.md`, `process/scope-proposal.md`, and `process/claim-coverage.md`. I read `main.tex`, `macros.tex`, and the complete `references.bib`, together with the complete contents of these manuscript files:

- `sections/01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, and `06-treewidth-two.tex`;
- `sections/07-positive-boxes.tex`, `08-exact-complexity.tex`, `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, and `12-relative-blocks-cuts.tex`;
- `sections/13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, and `17-synthesis.tex`;
- `sections/appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, and `appendix-integer-comparison.tex`.

The file prefixes correspond to repository filenames, not the printed section numbering. This includes every proof, appendix, and bibliography entry, not only Stage 6 additions or the assigned focus.

I also read the frozen `verification/schoenebeck-source.json`, `verification/stage05-primary-sources.json`, `verification/stage06-author-validation.json`, and `verification/build-report.json`, and the current source-access records `verification/primary-source-checks.md` and `verification/stage03-primary-checks.md`. Those records supplied source locations; their conclusions were not treated as proofs. I did not read other current-round reviewer reports, spawn agents, or modify the manuscript or snapshot.

I read `literature/AGENTS.md` before consulting original papers. The following table records direct primary-source inspection. Local library papers mean the corresponding `literature/papers/<paper>/original.pdf`; temporary originals are identified by their actual filename. Page numbers are PDF pages unless a printed page is specified. These are targeted dependency checks, not assertions that I read every page of every external paper.

| Source | Directly checked passages and role |
|---|---|
| Schoenebeck, `schoenebeck-full.pdf` | pp. 6–11 and 17–19: distinct-variable random model, Definition 10, Theorems 11–12, Lemma 13, signed-vector construction and width argument. This is the author full version used by the manuscript. |
| Luedtke–Namazifar–Linderoth | 23-page author manuscript, pp. 8–11, 15–16, 22: Theorems 4–5 and 8, half-integrality input, and Conjecture 1. |
| Boland et al., gap paper | pp. 4–6 and 10–11: Lemma 1, Corollary 1, signed-cycle characterization and its proof. |
| Davidson–Donsig | pp. 4–7: Theorem 1.2, Theorems 2.3–2.4, and the quantitative row/column decomposition statements. |
| Sherali, convex envelopes | pp. 8–9, printed 252–253: equation (13), Theorem 3, and the beginning of its proof. |
| Cornuéjols, `cornuejols-packing-covering.pdf` | pp. 78, 84–85, printed 76, 82–83: Camion's criterion, Theorem 6.13 and the balanced-matrix consequences. |
| Hassin–Tamir, `hassin-tamir.pdf` | Visually read scanned pp. 2–3, printed 380–381: series-parallel definitions and Theorems 3.1–3.2. |
| Grötschel–Lovász–Schrijver, `gls1988.pdf` | pp. 191–192, printed 179–180: Theorem 6.4.9 and its strong optimization/separation proof. |
| Potechin, `potechin2019.pdf` | pp. 8 and 18: Example 18's cardinality moments and Theorem 44's degree range. The manuscript's Gram proof was checked separately. |
| Altschuler–Boix-Adserà | p. 55: Theorem 7.4 and the historical question about logarithmic accuracy dependence. |
| Anstreicher | pp. 12–13: Conjecture 4 and its exact model conventions. |
| Khajavirad | Original [arXiv HTML v1](https://arxiv.org/html/2404.03091v1), model definitions and Propositions 1(i–ii), 3(i–ii), including the relevant proof passages and symmetry/secant conventions. These already establish the four packing values; the manuscript credits them accordingly. |
| Kronqvist–Misener–Tsay, published P-split paper | pp. 4–7 and 15–16: assumptions, minimal sharing and retained domain, Definition 4, Theorem 6, and the strict Jensen/outward perturbation proof. |
| Balas | pp. 5–7, printed 7–9: Section 2, Theorem 2.1 and its homogenization proof, including the nonclosed unbounded distinction. |
| Starr, `starr1969.pdf` | pp. 12–13, printed 35–36: Appendix 2, Lemma 2 and corollary, including the finite-dimensional rounding argument. |
| Wu et al. | p. 12: Lemma 3 and Theorem 3. Their proofs refer to supplemental material not independently checked here. |
| Fawzi–Parrilo | p. 3: Theorem 1 and the fixed block-size/SOCP interpretation. |
| Braun et al., `braun2013-approxlp.pdf` | p. 18: hard pair and Theorem 6(i), in the author version cited by the manuscript. |
| Lee–Raghavendra–Steurer, `lrs-sdpsize.pdf` | p. 23: Theorem 3.8 and equation (3.11); pp. 32–34: Theorems 5.3–5.4 and the pseudo-density construction. |
| Etessami–Yannakakis, `ey-rmc.pdf` | pp. 26–28: Theorem 5.2, normalized positive/negative circuits, detector, and amplifier. |
| Stewart–Etessami–Yannakakis | pp. 21–22: Section 4.1 and equation (18), with the repeated-squaring construction. |
| Esparza–Kiefer–Luttenberger | p. 34: Section 7, Theorem 7.1 and equation (14), including the relevant iteration proof. |
| Belotti et al., FBBT paper | pp. 1–2: the stated distinction between limit computation and iterative bound propagation. |
| Lubin–Vielma–Zadik | p. 12: Lemma 4.1 and the parity-midpoint proof. |
| Beach et al. | Combined 2022 preprint, p. 21, Section 5.1.1: exact upper and lower errors. I checked the preprint version explicitly identified in the manuscript, not the differently numbered published Part I. |

I did not independently consult every primary source in the bibliography. In particular, the published/review-version identity for Coniglio remains unverified, as the manuscript itself states. I did not independently audit the Ahmadi, Beame, or Fleming source papers in full, or reprove the classical matching, PARTITION, Khintchine, Grothendieck, or external conic-rank theorems from their original proofs. Their mathematical use and the manuscript's stated boundaries were reviewed, with those established results treated as inputs. I did not exhaustively read the canonical repository notes behind every coverage-ledger entry.

## Findings

None. There are no major or minor finding IDs and no required repair from this review.

The deliberately narrow distinctions in the manuscript matter to this verdict: the quadratic hull is the hull of the entire product domain; its realizing law need not satisfy graph identities pointwise; the parity count uses rank rather than the number of restricted lifted coordinates; the P-split counterexample retains the source's domain; the conic bounds measure their stated lift resource; and the FBBT iteration bound concerns the specified primitive contractors. Removing those distinctions would change the claims.

## Independent verification

### XOR source and exact quadratic realizability

For Section 16, I reconstructed the width-to-degree transfer directly from the source construction. Closure under symmetric difference gives values in `{0,1,-1}`. On supports of size at most `floor(w/2)`, the intermediate symmetric differences needed for transitivity have size at most `w`. A signed equivalence-class Gram representation therefore proves positivity of the whole quadratic form for arbitrary polynomials of that degree. It is not merely a family of consistent distributions on small coordinate sets. The conversion from source width to the manuscript's total character degree preserves the required factor of two.

I independently reconstructed Lemma 16.2: unit vectors whose pairwise inner products are in `{0,1,-1}` are parallel with a sign or orthogonal. Assign one independent fair sign to each orthogonal class except the class containing the constant vector; fix that class's sign to one. The resulting finite Boolean law reproduces every first and second moment. A coordinate with mean `+1` or `-1` is deterministic, so the construction fits the permitted endpoint of each restricted coordinate, even for nonclosed coordinate sets. No unsupported general statement that every PSD matrix is a Boolean moment matrix is used.

For the source family, I checked the distinct-variable sampling convention and the stated specialization of Theorem 12. At density eight, the relevant numerical inequality is `8 >= 1 + 8 log 2`; the denominator in the displayed width parameter remains positive. For each fixed assignment the signed clauses are independent, and the union estimate over all assignments gives more than `2n` violations with probability tending to one. The high-occurrence deletion estimate has expected loss below `n/8`; deleting clauses touching degree-above-64 variables loses fewer than `n` clauses with probability above `7/8`. Intersecting this with the width and violation events gives the required bounded-occurrence family for every sufficiently large `n`, without assuming the deletion event tends to probability one. Deletion preserves the source functional on retained clauses.

The resulting `m >= 7n`, maximum occurrence `64`, and at least `n` violations imply `OPT >= 1/8`. Certification at target `1/16` consequently gives the unlifted exponent `7n/1024`. I also checked that substituted cubic costs lie in `[0,1]`: the degree-six squares needed for this step are available within source degree `4r` for `r >= 2`.

### Monomial transfer and both order-one bounds

For Theorem 17.1, fixing the originals in the union `C` of restricted supports to a contained Boolean witness is deterministic substitution, not conditioning. Graph identities vanish as literal pulled-back polynomials. If a localizer has univariate-factor degree sum `a` and squared-polynomial degree `d`, its budget is `a+2d <= 2r`. After replacing univariate factors by Boolean endpoint indicators, the square that proves positivity has degree at most `D(a+d) <= 2rD`; its square is within source degree `4rD`. This checks products of local factors and arbitrary globally coupled squares, including repeated and overlapping supports. Equality multipliers obey the separate stated degree bound.

The augmented matrix of lifted first and second moments is PSD, has diagonal one and all entries in `{0,1,-1}`. Lemma 16.2 thus supplies precisely the full-box quadratic law requested by the oracle. The graph equations are satisfied by the functional; the proof does not silently require that law to be supported on the graph.

The restricted monomial endpoints are a consistent binary linear system of rank `q`. Its exact witness fraction is `2^-q`. Selecting `q` basis rows from the original support rows shows that the union of all nonzero columns equals the union of those basis supports, so `|C| <= Dq`. It would be insufficient simply to count restricted auxiliaries; the printed argument correctly uses rank. Affected-clause charging yields `Delta |C|/m`, giving the exponent `m T_*/(Delta D)`. Repeated monomials or redundant restrictions do not weaken this count.

At order one the condition `rD >= 2` supplies cubic-square positivity after pullback. For the explicit pair-and-clause graph with `D=3`, source degree twelve suffices, and the count is `2^(7n/3072)`. Since the construction has `N <= 17n`, the stated lower bound in `N` is `2^(7N/52224)`. This conversion would not be valid for arbitrarily inflated auxiliary dimension; the manuscript expressly retains that distinction.

For Proposition 18.2, let `h=2/ceil(3/epsilon)` and `a` be the original-coordinate lower corner. A full-box quadratic law and the two graph moment equations give

`|L[v]-a_i a_j a_k| <= |L[u(x_k-a_k)]| + |a_k| |L[x_i x_j]-a_i a_j| <= h+2h`.

Thus the averaged objective is at least the corner value minus `3h/2`, hence at least `OPT-epsilon`. The explicit cut in equation (18.6) is quadratic and valid over the full product box, and subtracting the two graph identities gives equation (18.7) exactly. This proves the stated order-one upper certificate while leaving all auxiliary intervals unchanged. At tolerance `1/16` it gives `48^n` boxes. The separate order-two Bernstein proof uses three bound factors and degree-three graph identities within degree four; it is not needed to justify the order-one claim.

The halfspace obstructions in Section 18 were also checked. The original uniform quadratic moments have `L[S]=0` and `L[S^2]=n`, incompatible with an actual law supported on `S>=0`. The indicator test for deterministic substitution gives the stated `min(r-1,ceil(n/2))` necessary cost. These arguments only delimit the presented proof mechanism; the manuscript does not turn them into a general affine-branching lower bound.

### Full manuscript and Stage 6 checks

I reconstructed the vertex-law formulation and the positive-deficiency reduction, including the direction of the termwise inequality when physical monomials are expanded. For the signed section, I checked the half-integral cut formula, the passage from cells to the full cube, and the weighted-density orientation argument. The Schur-multiplier theorem is appropriately an established comparison; the local argument does not rest on prior review labels.

For the positive degree bounds, I followed the marginal completion, dyadic/radix coupling, harmonic mixture, Lambert-function optimization, and coefficient-removal argument. I checked the symmetric-envelope interpolation against Sherali's statement. The two printed finite programs were rerun from the actual manuscript text, including all finite cubic certificates. Their exact rational outputs match the displayed cases.

For the structural results, I checked the rank argument that confines fractional slab components to odd cycles, the frequency-two rounding with retained baseline terms, and the matching reduction with its mandatory-slot bonus. I followed the series/parallel active-versus-blocking invariant and the use of Camion's criterion in the width-two proof. For positive boxes, I checked the finite spreading construction against the global physical minimum/maximum, the fixed-ambient restriction, the shifted coefficient bound, and the predecessor examples. The exact-complexity argument distinguishes polynomial bit complexity and weak PARTITION hardness from a claim of strong hardness.

For the cardinality and spatial sections, I reconstructed the falling-factorial Gram decomposition, the homogeneous degree bounds, indicator conditioning, full-preordering transfer, block tensor positivity, and endpoint interpolation for coordinatewise lifts. The tensor argument uses the total-degree principal submatrix of a PSD tensor product. The degree-free coordinatewise transfer is not incorrectly reused for multivariable monomials. The relative-tolerance normalization and clique-cut escape have the stated family and oracle scope.

For Appendix F, the upper variance bound follows from `k tr(X)-e^T X e <= k L s-s^2 <= k^2 L^2/4`. I checked the proposed block covariances, the minimum pair values, and the `n>=2`/`n>=5` ranges. The four packing values agree with the primary statements. Recomputing diagonal secants and RLT on the shortened symmetry intervals is essential and is explicit.

For Appendix G, I checked compact homogenization, endpoint mixtures, multiplicity mixtures, the common intensive variable, and the zero-scale slice. The diagnostic scale cost detects a failure of rectangularity; repeated mixtures and closedness provide the reverse implication. The aggregate formula only needs integrality of the count polytope, and the Shapley–Folkman replacement bound follows by replacing at most `min(d,n)` summands. The qualifications about added balances and relative normalization are necessary and present.

For Appendix H, I checked the counterexample directly against the published P-split assumptions and Theorem 6. The retained box and shared transverse square prevent the source proof's strict Jensen/outward perturbation argument. The displayed auxiliary witness is feasible while the original projection remains the box. For the separated balls, fixing the transverse sum leaves a truncated square in the two longitudinal auxiliaries; its hull gives (H.3). Completing the square yields the cylinder/ellipsoid intersection, and differentiating in the squared transverse radius gives the stated Hausdorff error and limit. The coordinate-change example distinguishes the transformed retained diamond from a new box. The exact-image strengthening and the finite directional condition are separately scoped.

For Appendix I, I verified the trace-face generators, the paired correlation-polytope inverse map, and the exposure inequality `g >= B+D`. I followed the rounding constants through `(136m+10)g` and the stronger outer-transfer constant `(184m+6)epsilon`, including the block map's additional factor `m`. I checked the shifted Braun hard pair and independently substituted the LRS pseudo-density parameters into the quantitative rank theorem: the polynomial prefactor and the `2/13` stretched-exponential power are consistent. The lift-to-slack factorization uses the minimal PSD face and an extra scalar factor, so it does not need an unasserted strict-feasibility assumption on the initial lift. Exact SOCP total dimension and the number of bounded-size blocks are kept distinct.

For Appendix J, I checked that sound contractions preserve the least fixed point and that fairness gives domination of each finite Kleene iterate. The PosSLP construction has polynomial description length, the stated coefficient set, distinct product names, and components of size at most four. The detector has roots `1` and `d/c`; the amplifier separates output `1` from at most `1/8`, giving the additive-quarter decision gap. The primitive iteration invariant yields `l_z <= 1-c^K <= Kb`; with the encoded doubly exponential reciprocal scale this gives the displayed update lower bound. The rationality and at-most-two-fixed-points assertion is consistent with the detector roots. No conclusion about accelerated or symbolic contractors is needed.

For Appendix K, I checked the closure of parity classes, the square midpoint diameter, the product area integral `16 epsilon log 2`, the simultaneous graph width-to-volume step, and the shared binary expansion error `2^(-p_i-p_j)/4`. These statements measure integer precision and do not establish the spatial-region results by substitution of resource names.

### Executed and rendered checks

The independent checker is `verification/reviewer05/stage06-round01/check_focus.py`; its machine-readable result is `check_focus.json` in the same directory. It completed successfully with the `minlp-notes` Python environment. All arithmetic checks are exact, using rational arithmetic, integer GF(2) operations, or symbolic polynomial identities:

- All 729 symmetric 4-by-4 augmented sign-matrix candidates with diagonal one were tested by all principal minors. The 49 PSD matrices were realized exactly as finite laws for three Boolean coordinates and the constant coordinate, and every augmented moment was checked.
- All 16,384 families of distinct nonempty supports of size at most three on four originals were enumerated. Every consistent parity right-hand side has exactly the rank-predicted number of witnesses, and the support-union bound holds.
- The order-one polynomial identity was checked symbolically. Nonnegativity was checked at all 5,152 full-box vertices for grids of sizes 1, 2, 3, and 5, both clause signs, and both auxiliary endpoints. For each selected box, multiaffinity makes this an exact box-validity check.
- The localizer inequalities were checked for 1,417 degree budgets with `1<=r,D<=7`, including order one and `D=2`. The deletion estimate's sufficient integer inequality `384*3^24 < 2^64` also passed.
- Both verbatim finite-certificate programs were extracted from the frozen appendices and executed, not copied from an author result file.

These finite checks are falsification attempts and reproducibility checks, not proofs for unbounded parameters. The general arguments above supply the mathematical review.

I visually inspected rendered PDF pages 1, 4, 72–76, 93, 97, 99, 101, 103, 105, 107, 109, and 111. The inspected formulas, tables, proofs, and bibliography were readable without clipping or missing symbols. The rendered images are retained under the assigned verification directory. The frozen build report records successful compilation, no warnings, and no duplicate labels; I did not independently recompile the manuscript.

## Remaining limits

This review reads the entire manuscript source and directly checks the identified primary-source passages, but it is not an exhaustive audit of the proofs of all external theorems. The external conic-rank bounds, classical optimization and discrepancy inputs, and uninspected contextual papers remain dependencies at the level stated above. Some original papers are scanned or have imperfect text extraction; Hassin–Tamir was therefore checked visually. I did not establish an exhaustive priority search or identity of unverified publication versions.

The finite checker does not generate a large random XOR instance, prove the asymptotic width theorem, enumerate arbitrary-dimensional PSD matrices, or formally verify the whole paper. The rendered inspection covers the listed pages rather than all 111 pages. I did not run every author verifier or a fresh LaTeX build. None of these limits supplied evidence of a defect in the frozen stage, but they should remain visible when combining reviews and conducting the separate final whole-paper loop.
