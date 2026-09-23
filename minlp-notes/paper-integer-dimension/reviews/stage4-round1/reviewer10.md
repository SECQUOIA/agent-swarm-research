# Stage 4 round 1 — reviewer 10

Major findings: 0
Minor findings: 0

No concrete MAJOR, MINOR or QUESTION finding remains from this review. The cap-set restriction and exact convex box separation are supported by their proofs, with the correct distinction between arbitrary convex binary lower bounds and rational linear upper constructions. This is a bounded review, not formal verification or a publication-priority verdict.

## Coverage

I read all 1,297 lines of `sections/04-vector.tex`, the entire abstract, introduction and conclusion, the stage task/lenses, protocol and process, current coverage mappings and open-boundary inventory, bibliography and main file. I compared all ten canonical stage 4 result texts and all eleven explicitly substantive supporting texts. Their distinct mechanisms are retained, including finite output/facet overlays, maximum-product transfer, hinge geometry and Bernstein stability, repeated convexification, cap sets, simplex bands, and the lattice-free route limitations. Superseded numerical choices for the same degree-32 construction need not be separate theorems.

Accepted dependencies checked were the section 1 graph-sandwich definition, finite mixtures and convex integer sections, parity contacts, affine changes and finite linear disjunction; section 2's rational scalar logdet allocation and exact feasibility repair; and section 3's scalar chord/packing comparison, certified monotone mass algorithm, indexed compiler, dense convex hybrid counts, and Jensen superadditivity. I read the stage 3 correction record and checked its rational-input clarifications against the current source. This does not constitute a fresh review of all unrelated results in accepted sections 1–3.

## Independent proof reconstruction

- **Shared partitions, lines 17–168.** Arbitrary-factor refinement follows from the ranges of the concave gap between successive strict levels. The interval-cover trimming argument uses closed finite covers and preserves component gaps under restriction. The sorted overlay uses a common fixed denominator and multiplicities; a positive merged cell cannot contain a source knot in its interior. Canonical approximate-mass comparisons partition targets into ordered left/return/right ranges, so this particular finite search tree returns ordered knots even if node estimates are not monotone. Source-cell lookup, final endpoints, zero-length cells and invalid codes fit the construction.
- **Original-output rank, lines 170–276.** Maximum-volume bases give coefficient bound one, while rational exchanges give bound two and polynomial determinant growth. Choosing original convex rows makes signed representation coefficients compatible with nonnegative chord-gap domination. Box/facet counts and rounding budgets agree with the claimed constants. Compactness of the nonnegative-facet body forces every column to be measured and justifies its rank-zero claim.
- **Allocation and oracle constructions, lines 278–582.** The approximate product optimum gives the stated factor seven, with the one-dimensional case separate. Effective-image radii and pulled-back separators are valid. The generic spanner's precomputed determinant/cofactor bounds control every objective; fixed grid and repair weights prevent recursive denominator growth. Repair returns exactly feasible points with objective loss at most 1/4. The positive-polar separator certifies proximity on its membership branch, not exact membership. The two spanners yield an explicit inner image parallelotope, and effective-coordinate rounding keeps errors in the nonlinear image. I recomputed the center error 17P/64, final error 49P/64 and capacity factor 69,984r².
- **Separable vectors, lines 584–746.** One concatenated basis supplies the same coefficients in every input block. Jensen superadditivity and deletion of an integer l1 ball compare the product packing to the original vector lift. The six factors are 108r, 180r, 180r² for finite bounds and 87,480r, 157,464r, 1,277,208r² for compiled bounds. Local bands share each coordinate's input and weight; rounding is divided by input count before summation. Affine blocks and rank-zero cases are consistent.
- **Positive-power obstruction, lines 748–819.** Bernoulli's bound on the later inputs and the exponential bound on the thirds average give 2177/2144>1. Distinct residues modulo three are necessary even with unbounded integer labels. Equal binary assignments permit arbitrary convex weights and yield the stronger binary lower bound. Midpoint compatibility, individual signed scalarizations with one binary, and joint refinement failure have their stated separate quantifiers.
- **Cap sets, lines 821–902; primary lens.** Three distinct zero-sum residues would admit the uniform lifted average. In the component belonging to the smallest input index, the other two inputs contribute at least 15/16 each before scaling; the averaged input has the same 3/67 upper bound as the pairwise thirds argument. This proves the cap-set hypothesis. In characteristic three a zero-sum triple with two equal members has all three equal, matching the imported theorem's hypothesis. The generating-function indicator bound has the correct direction for 0<t<1. Differentiating its logarithm gives 4t²+t−2=0, with the unique positive root in (0,1); the base is below three. The prefactor three is retained. The p=0 case is trivial, and cap(1)=2 gives exact count two at M=3. The direct arbitrary-label argument handles gaps at least three, then the entire middle section through repeated convexification. None of these bounds proves a growing binary/general-integer difference for this one-input family.
- **Exact convex box counts, lines 904–1009; primary lens.** The rational inequalities A−1<L<1, d<1/4 and (A+d)/2<1 hold. At label one, all possible mixtures consolidate to weights (t,1−2t,t), not merely a few tested pairwise chords. Their inputs stay in [c,1−c] and outputs in [0,max(L,(A+d)/2)], so every admitted middle-section output and every true output lie below one and above zero. Outer sections are exactly their valid boxes. This proves the one-integer upper for the whole graph. Every pair of the three contacts has a forbidden orientation of the thirds combination. Product contacts therefore require distinct residues modulo three, giving p≥n, and distinct binary assignments, giving 2^p≥3^n. The matching product and coded-box formulations are rational polyhedral lifts; only the first has the asserted linear continuous size. The affine monotonicity shear preserves the counts. Hinge thickening and Bernstein approximation retain their strict margins and do not need to prove a new degree-32 case.
- **Nonconvex and signed overlays, lines 1011–1139.** Bernstein's variance bound gives uniform error 1/32 at degree (32M)²; peak/trough alternation forces degree growth. One period integer and one orientation bit give the stated upper, while whole binary-section chords give the lower. Convexity pieces yield the finite degree bound. In the rational vector overlay, source-cell curvature flags and directed rounding give the displayed intervals, including root brackets and singleton cells; offset selection requires no additional declared integers.
- **Error geometry and open scope, lines 1141–1297.** The tilted-body projection preserves the scalar lower bound, while the common output band absorbs the convexifying quadratic. The centered second difference gives radius ratio at least 8+60M². Downward boxes and the sharper simplex band respect the inner balls; their proof also permits the expressly stated nonsymmetric case. Unconditional axis normalization and the direct product-allocation bound are distinct arguments. Strict upper-violation projections are convex and lattice free, but their union need not be; Helly and Radon statements do not supply the missing interval cover. The open one-input convex box question is not claimed solved.

The abstract, introduction, result table and conclusion agree with these scopes. They distinguish integer count, finite real existence, rational encoding, construction time and solution time, and distinguish the growing-input convex product separation from one-input nonconvex or tilted-body separations.

## Primary evidence and limitations

I read the cached Ellenberg–Gijswijt primary manuscript, including Theorem 4 and its proof and Corollary 5 on printed pages 2–3. I also rendered and visually checked PDF page 2 to verify the theorem's hypothesis and monomial bound. Taking field size three and coefficients alpha=beta=gamma=1 gives exactly the imported bound. The manuscript separately proves the finite generating-function estimate and its graph-contact reduction, and credits the cap theorem.

I reread GLS Definition (5)/(6), its known-ball convention on printed page 172, and Theorem (3.1) on page 177 in the cached primary text. The objective comparison is against all exact feasible points, as needed by the repair argument; dimension-one padding is supplied. Other predecessor attributions were checked for consistency with the source inventory and the proofs, not through an exhaustive independent literature/metadata search. Existing root and historical audits were leads, not proof certificates.

No complete circuit compiler, certified integration routine or general GLS optimizer was implemented here. I did not run a shared LaTeX build or review every page of the manuscript PDF. A first attempt to render the cap source with Python failed because PyMuPDF was unavailable; `pdftoppm` succeeded. The finite tests below support specific algebra and boundary cases and do not replace the universal arguments.

## Executed checks

- All eleven frozen SHA-256 values matched, both before review and before saving this report.
- `python code/positive_vector_obstruction/check_box_gap_root.py`: PASS — 72 middle-slice vertices, 2,048 exact integer-slice mixtures and 390 product-contact pair obstructions.
- `python code/quadratic_rank/check_implicit_knot_overlay.py`: PASS — 2,304 ordered-search checks, 60 exact order statistics, 180 source-cell containments, 8 large implicit-grid rank queries and 99 directed bands.
- `python code/quadratic_rank/check_rational_polar_spanner_second.py`: PASS — 16 generic systems, 93 exact repaired optimizer calls, 11 exchanges, 120 full-image vertex checks and 347 positive-polar cases.
- Independent inline exact Python check: for p=0,...,60, convolution computed m_p=number of alpha in {0,1,2}^p with sum alpha≤floor(2p/3), and verified m_p³16^p≤343^p, the t=1/2 generating bound cubed. It also checked the rational inequality ((7/4)2^(2/3))³<(14/5)³. Exhausting all 522 subsets in dimensions 0–2 gave cap values [1,2,4]. All passed.

## Reviewed-file SHA-256 values

Paths are repository-relative. Supporting hashes record inspected versions; primary-file hashes identify the text/PDF evidence above.

| File | SHA-256 |
| --- | --- |
| `paper-integer-dimension/abstract.tex` | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| `paper-integer-dimension/coverage.md` | `d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf` |
| `paper-integer-dimension/macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `paper-integer-dimension/main.tex` | `026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c` |
| `paper-integer-dimension/references.bib` | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| `paper-integer-dimension/sections/00-introduction.tex` | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| `paper-integer-dimension/sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `paper-integer-dimension/sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `paper-integer-dimension/sections/03-scalar-nonlinear.tex` | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| `paper-integer-dimension/sections/04-vector.tex` | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| `paper-integer-dimension/sections/05-conclusion.tex` | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |
| `results/convex-polynomial-box-error-exact-integer-gap.md` | `ae13f424087b15394c1d3a0f77a00d1481b2a533f284bad275f384b12f4e9bb7` |
| `results/convex-separable-vector-curvature-rank-precision.md` | `15661dcb32c4e550ecc94ec10e73595e9065c9ca5fdb6c28e29feca97bf1ae4c` |
| `results/convex-separable-vector-oracle-curvature-rank-precision.md` | `da064fe378f6025832ccf5438ad04ea63696e3c37f8b22b68a409813e9caddd2` |
| `results/convex-vector-compiled-integer-precision.md` | `b386100062ef4954259af78c1bd992bbdd592f6db3d421082f77470756c2ba99` |
| `results/convex-vector-curvature-rank-precision.md` | `51c6fd200ffd3021db783ae221008bc59c35f88363d807a2c5a45426a0e2e33b` |
| `results/convex-vector-facet-curvature-rank-precision.md` | `386fb0c3c6a6178d4303da236ff1562dc931277e656b6f4e93a2688786922724` |
| `results/convex-vector-oracle-curvature-rank-precision.md` | `c407278ce18bdc9dd2366856660608555640d1e80bb58abe19ad6489543a22f1` |
| `results/convex-vector-unconditional-compiled-precision.md` | `f619051ab08440db35c5ed2c8905c4bfb07dfec446eddad6943c71e288f06135` |
| `results/polynomial-graph-binary-integer-degree-gap.md` | `37a21762fcff55c96c401e6cf39bdca10863ae0977964738f59a6b2172e6e85b` |
| `results/polynomial-vector-compiled-integer-precision.md` | `a9dbbfa1062a8b258a871471dbb39ff47391819c9ef14220444901865d5b5ea8` |
| `notes/componentwise-convex-fixed-condition-integer-gap.md` | `3f94e9f6ca96cec6e834e70f12ce8c31418b00f9d04472bf961372ea7178b97e` |
| `notes/convex-separable-vector-finite-rank-precision.md` | `b7cefbe2c0998e9df9285eaee492474c5f3ab0f2ecbff43c72941ae456cb3443` |
| `notes/convex-vector-box-gap-lattice-investigation.md` | `f4f2b1615e501ebeccf3909ab8c50e67957d09849b346834175d5796ffdd7de8` |
| `notes/convex-vector-one-bit-box-gap-investigation.md` | `fcc173227768881a7871f063d120137315e6fa720d772252dde0ae0c291bee7c` |
| `notes/convex-vector-tilted-error-integer-gap.md` | `245d72da78dbae9d0f125b4e332426441b6686ad676ed34b9c05c401db68493d` |
| `notes/nonconvex-polynomial-binary-integer-gap.md` | `723e842b316bf04a4bb9d592ebceea38445f8e1a3ffbced7ef6744142171864d` |
| `notes/positive-polynomial-vector-refinement-novelty.md` | `f16f587c00c18f3aafabba00f5a9712cacf148fa86a955012a304f41d3822979` |
| `notes/positive-polynomial-vector-refinement-obstruction.md` | `7122bf4008829ef741804c9cd669731f4f8b6d1f64939bcb6885505ccfd894f4` |
| `notes/positive-vector-capset-integer-lower-bound.md` | `d0045e403a8b84c9e1981445fc6cc9f6004d9c5fe81dfdde239245593ac9b108` |
| `notes/positive-vector-three-witness-integer-obstruction.md` | `4588e80af0b7e14f5964117a9dc88a0fe26d5fdf314b9a047391c232131f9fe7` |
| `notes/rational-polar-spanner-oracle.md` | `26395653886631083d14bd10f081705969140c0ce38c1fc20abc859ec60b0cb9` |
| `paper-integer-dimension/reviews/STAGE4-TASK.md` | `f9b7bc842ba1255856501cb672987e5355bce3f1f025c7260466ebded1868ae7` |
| `paper-integer-dimension/reviews/STAGE4-LENSES.md` | `632a30a15f43fae207079169dd043e3f74ac9ce726a7763d1a403356fd44b19a` |
| `paper-integer-dimension/reviews/PROTOCOL.md` | `9ca1d0f1c48bf807c7634ccc5c93f541ac374a70b0d2be3875e57e74f6755d57` |
| `paper-integer-dimension/PROCESS.md` | `0a77aedc588ad95ed4bf5865d9f48ee85874e16f980a9270e2ccecf6c73fff26` |
| `paper-integer-dimension/verification/stage4-root-source-audit.md` | `bc96d6a58c4e272f3a11386fb84e94a11f7553a2aa19e6eed614fd32cf629cc2` |
| `paper-integer-dimension/verification/stage3-corrections.md` | `747e1b323a3ef6e99095d2366ccce59a24a5362a78a1f7cedba260a88c1a4ad1` |
| `paper-integer-dimension/build/source-cache/ellenberg2016.txt` | `ec12f6179b90fed288965fdec6cb57840d0910ac691de0f1c8e3c9147f5e35bd` |
| `paper-integer-dimension/build/source-cache/ellenberg2016.pdf` | `3cd77ddab97f046121ef684d68cea9d175b438363ee60b2abe1faa0db05f116b` |
| `paper-integer-dimension/build/source-cache/gls1981.txt` | `60eb7ffdfab378197ca6209c9ef6e2ae490dd7a88ad018624cb8a4c5ede7ac31` |
| `literature/AGENTS.md` | `40da10e6e5f7c5dd120f5c789bda7d20aae6b07acdb781aaec4c7b3f5af02916` |
| `code/positive_vector_obstruction/check_box_gap_root.py` | `fc5d83634787f9e3216932c7c81ac64b6cb94dffd79cad8551eafd2615bf571b` |
| `code/quadratic_rank/check_implicit_knot_overlay.py` | `71e13a8e4a3aff18a7abeb93a4409f63f9067f2ea82036e82d3d4d31b7f5cd0c` |
| `code/quadratic_rank/check_rational_polar_spanner_second.py` | `57bec7920f0958ad2375486d2539684c776c4bf4a448bc5128d162c071326fcc` |
