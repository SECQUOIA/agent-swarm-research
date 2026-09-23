# Independent whole-paper review 09

## Verdict: PASS

I found no major or minor defect requiring repair in the assigned frozen manuscript. This verdict follows a fresh reading and reconstruction of the arguments, not the acceptance labels in the author record. The additional P-split focus did not narrow the review.

Target: `process/snapshots/whole-round01/main.pdf`, 111 pages, SHA256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. I verified this hash before and after the review work. I did not edit the manuscript or snapshot, consult another final-round report, or delegate any review work.

## Coverage

I read the complete frozen `main.tex`, `macros.tex`, and `references.bib`, including the introduction, roadmap, conclusion and all bibliography entries. I read every statement, proof, remark and printed checker in these 28 section files, under the frozen `sections/` directory:

```text
01-foundations.tex
02-universal-positive.tex
03-cubic-equal-means.tex
04-incidence-interiority.tex
05-feedback-frequency.tex
06-treewidth-two.tex
07-positive-boxes.tex
08-exact-complexity.tex
09-cardinality-spatial.tex
10-cardinality-preordering.tex
11-coordinate-domains-lifts.tex
12-relative-blocks-cuts.tex
13-xor-quadratic-hulls.tex
14-monomial-reformulations.tex
15-finite-certificates-affine.tex
16-supporting-comparisons.tex
17-synthesis.tex
appendix-finite-signings.tex
appendix-positive-couplings.tex
appendix-cubic-certificates.tex
appendix-structural-auxiliary.tex
appendix-positive-box-predecessors.tex
appendix-scaling.tex
appendix-point-packing.tex
appendix-p-split.tex
appendix-rank-one.tex
appendix-fbbt.tex
appendix-integer-comparison.tex
```

I also read the frozen review protocol, whole-paper assignment, focus JSON, scope proposal, claim-coverage ledger, `stage-06-author.md`, and `stage06-corrections.md`, together with the build instructions and build-checking script. I checked coverage against the ledger and proposal rather than inferring it from the section titles. I found the stated distinctions among pointwise envelope width, scalar exact evaluation, local relaxation strength, spatial certification, integer precision and global lift size consistently maintained. The supporting comparisons remain comparisons, with their own assumptions, rather than being used to infer unproved lower bounds for the spatial model.

I read `../literature/AGENTS.md` before accessing local originals. The following primary-source checks were made directly; repository source records helped locate versions but were not used as substitutes for the source statements:

- Kronqvist–Misener–Tsay, local published `original.pdf`: assumptions and epigraph formulation on PDF pages 4–7; Theorem 4 on page 13; Corollary 3, Definition 4, Theorem 6 and its proof on pages 15–16. I also rendered and inspected pages 15–16. This establishes the shared-function, retained-domain, bound and formulation conventions needed for Appendix H.
- Boland et al., local original, PDF pages 3–6 and 10–11: cut-range identity, induced-subgraph transfer and signed-cycle exactness, including the proof of Theorem 4. Luedtke–Namazifar–Linderoth, local original, PDF page 22: Conjecture 1 and its context. Davidson–Donsig, local original, PDF pages 4 and 6–7: the Schur/Grothendieck and weighted rectangular estimates used in the comparison.
- Cornuejols, July 2000 author manuscript: Theorems 6.5 and 6.13 and their surrounding statements (printed pages 76–82), including the Eulerian matrix criterion and mixed balanced unit-right-hand-side integrality. Hassin–Tamir, original scan, PDF page 3/printed page 381: series/parallel definitions and Theorem 3.1. I read that page as an image because its text extraction is empty.
- Altschuler–Boix-Adsera, local published original, PDF pages 55–56: Theorem 7.4, the logarithmic-accuracy open question and Corollary 7.5. I checked that the manuscript distinguishes ordinary encoded input complexity from an arithmetic-operation statement.
- Schoenebeck, author full version: random-model and width conventions, Theorems 11–12, the complete signed Gram argument of Lemma 13, and the expansion argument in the appendix, including the end of Proposition 22. This was direct reading of the original PDF text, not an invocation of a prior PASS label.
- Lee–Raghavendra–Steurer, author full version: Theorem 3.8/equation (3.11), PDF page 23, and Theorems 5.3–5.4 with their application/proofs on pages 32–34. Fawzi–Parrilo, local original, PDF page 3: Theorem 1 and Lorentz-cone discussion. Braun et al., July 2013 author version, PDF page 18: Theorem 6(i) and the hard inner/outer pair. These support the separate global-lift comparison; I did not reprove the external lower-bound machinery.
- Anstreicher, local author original, Section 4 and Conjecture 4, PDF pages 10–12; Khajavirad, [arXiv:2404.03091v1](https://arxiv.org/html/2404.03091v1), Propositions 1(i–ii) and 3 and their proofs. The attribution of the four point-packing values to established results is correct, including recomputed diagonal secants and RLT redundancy.
- Belotti et al., local original, PDF page 14: Theorem 4.1 and the infeasibility discussion. Lubin–Vielma–Zadik, local original, PDF page 12: Lemma 4.1 and its parity proof.

The limits of this source coverage are recorded below; this list does not assert that every cited paper was read in full.

## Findings

None. There are no finding IDs or required repairs.

## Independent verification

**Whole-paper mathematical checks.** I reconstructed the coupling interpretation and checked boundary means, zero terms and support/sign qualifications. For bilinear functions I checked the center cut-range identity, polarization factors, induced-cell transfer, fractional orientation and signed-cycle criterion. For positive products I checked inactive mass, the harmonic normalization, fixed-point/Lambert bound, dyadic and radix cutoffs, attainment and the coefficient-removal argument. I reconstructed the cubic three-law case division and minimax calculation, the Bernstein slack argument, and the relationship between analytic estimates and finite rational certificates.

For the structural claims I checked ownership and gluing, domination by feedback choices, half-integral odd-cycle components, matching formulations, and the full active/blocking invariant in the series-parallel construction. In particular the two-terminal induction needs both modes; using only a single active mode would not establish the stated conclusion. I checked the cardinality extension against its matrix integrality assumptions. For positive boxes I checked the finite extremal spreading while retaining the ambient law, the coefficient comparison, softened lower examples, and the unequal-box obstruction. For exact evaluation I checked the single-product PARTITION encoding and the precision needed to distinguish its two outcomes.

For the spatial sections I reconstructed the fractional-cardinality Gram expansion, its coefficient signs and assignment indicators, the preordering constraints, and the role of all valid local coordinate-domain polynomials. I checked that endpoint interpolation preserves the degree needed for coordinatewise graph auxiliaries, whereas general bounded monomial lifts consume the stated factor of D. I checked the global tensor positivity and relative-gap block count, strictly ordered costs and uniqueness, and the explicit quadratic escape cut. I reconstructed the XOR signed closure and quadratic probability realization, tracked the width and occurrence-deletion constants, and checked the parity-rank covering argument, lifted dimension bound, and finite upper certificates. The order-one lifted quadratic formulation and the unlifted cubic order-two certificate have distinct hypotheses, which the manuscript preserves. The affine-branching discussion is appropriately a barrier to this proof method.

For the supporting appendices I checked scaling and objective normalization, the point-packing attaining matrices, correlation-face exposure and stability estimates, and the separation between fine approximate global lifts and local certification. I checked the FBBT least-fixed-point/fair-update argument, the positivity detector and its rational encoding, and the restriction to primitive updates in the slow-convergence example. I checked that the integer-precision argument counts parity classes or binary assignments and does not identify them with spatially certified leaves.

**Additional P-split reconstruction.** Appendix H survives the following independent attempts to falsify it.

1. In the retained-box counterexample the four corners lie in the feasible union. The proposed auxiliary lift along the top edge satisfies its epigraph links because the residual is a multiple of t(3−t), nonnegative on the complete interval. Exact separate bounds over a retained box do not repair the missing coupling.
2. For aligned balls, fixing the common transverse value gives the union of two rectangles whose hull is the square cut by a+b≤U+h. Its vertices prove the asserted hull even at h=0; no interior-only decomposition is being used. Downward closure justifies substituting actual squares. Completing squares gives the cylinder/ellipsoid projection. Differentiation of squared distance with respect to the squared transverse radius is positive, so the Hausdorff maximum occurs at the stated cap, with limiting ratio √2−1.
3. The rational map M=[[3,4],[4,−3]]/5 satisfies MᵀM=I and det M=−1. It sends v=(3D,4D) to (5D,0) and p=(2D,4D/3) to (34D/15,4D/5). Every witness square is at most 4vᵢ²/9. The midpoint of the two center images has each corresponding entry vᵢ²/2, proving feasibility for every convex auxiliary set containing both center images. This is stronger than checking one basic hull. The exact transformed parallelogram, together with |w|≤1, controls the end regions by t²+w²≤2. The proof does not silently replace that parallelogram by a coordinate box or assume additive bounds after rotation.
4. For the aligned exact feasible image, f(c)=d²+1−c+2d√(1−c)=(d+√(1−c))² is decreasing and concave on 0≤c≤1. The hypographs contain the image hull. With c≥w², their epigraph projection forces precisely −√(1−w²)≤t≤d+√(1−w²). Conversely this convex relaxation contains both balls, hence their capsule. The endpoint c=1 is valid by continuity. The displayed conic representation has the correct signs. This argument concerns a hull in auxiliary values and does not imply equality with a hull in the full original/auxiliary graph.

**Exact and numerical computation.** My independent `verification/reviewer09/whole-round01/check.py` produced `checks.json`. It extracts and runs the two appendices' printed checkers directly from the frozen sources. Exact signing output is `[1, 2, 4, 4, 5, 8]`. All printed rational cubic primal/dual certificates passed, including the 18-, 24- and 192-coordinate cases. Further exact/symbolic checks verified the rational orthogonal map, center-image domination identities, f and its derivatives, nine small fractional-cardinality Gram cases, 2,501 rational retained-box mesh points, four truncated-square cases, and 820 rational capsule cap points. The finite sets supplement the preceding analytic arguments; they do not establish a universal theorem.

The only floating-point optimization in my added checker samples the Hausdorff radial profile at seven separation/radius ratios, from 2.0001 to 10,000. It agrees with the endpoint formula and approach to √2−1. I treat it as a diagnostic, not an exact or global proof.

**Build and PDF.** I copied the frozen inputs and needed build/checker files into `verification/reviewer09/whole-round01/build/` and built with that directory explicitly set as the working directory. The build exits successfully, reports no warnings or duplicate labels, confirms the printed checker match, and produces 111 pages. Its complete `pdftotext -layout` output is byte-identical to the frozen PDF extraction; `build-comparison.json` records this check. The rebuilt PDF hash differs because the generated file is a fresh build, so I do not claim binary PDF identity.

I visually inspected frozen pages 1, 2, 4, 86, 87, 97–101, 105 and 108–111, including the dense printed certificate material, the P-split proofs, and the bibliography. These 15 pages are readable without visible clipping or damaged mathematical layout. The rendered images and build outputs are retained in my assigned verification directory.

## Remaining limits

This is an independent mathematical review, not a proof-assistant formalization. I did not exhaustively enumerate the universal graph/hypergraph or spatial families, solve large SDP instances, or run every historical repository verification program. Exact finite checks and numerical diagnostics have the limited scopes stated above.

I did not reread every proof behind standard Khinchin/Grothendieck, matching, optimization/separation, Shapley–Folkman or global conic lower-bound results. I checked the particularly material formulations and source passages listed above and reviewed the manuscript's own derivations. I have not performed exhaustive bibliography-wide priority clearance. In particular, the manuscript's stated lack of verification that the anonymous Coniglio review version is identical to the published version remains unresolved by this review; the manuscript already discloses that limit.

The online P-split DOI open attempt failed, but the local published original was accessible and was directly inspected. Khajavirad's original version was accessible through arXiv HTML. My visual check covers the 15 specified manuscript pages, not every one of the 111 rendered pages; complete manuscript reading was from the LaTeX sources, with whole-PDF layout-text comparison as described above. None of these limits supplies a demonstrated defect in the frozen manuscript's correctly scoped claims.
