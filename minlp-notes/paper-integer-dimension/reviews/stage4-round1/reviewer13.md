# Stage 4, round 1 — reviewer 13

Major findings: 0
Minor findings: 0

No concrete major or minor defect was identified in the frozen stage. The open-boundary discussion preserves the limitations of the lattice arguments, and the constructive and separation statements examined have the stated scope. This verdict is bounded by the coverage below; it is not a guarantee of mathematical correctness, priority, or publication acceptance.

## Coverage and dependencies

I read all 1,297 lines of `sections/04-vector.tex`, the complete abstract, introduction and conclusion, the stage task/lenses, process and protocol, snapshot, bibliography, and coverage inventory. I reread the relevant accepted foundations (graph sandwich, affine transformations, parity and finite disjunction), the scalar specialization and feasibility repair of the stage-2 allocation oracle, and the stage-3 indexed compiler, scalar chord and packing lemmas, hybrid count, and Jensen superadditivity. I checked the accepted stage-3 correction record; its rational-data clarification is consistent with stage 4's computational hypotheses.

I compared the statements, scope and mechanisms of all ten canonical stage-4 results against the manuscript. I inspected all eleven explicitly substantive supporting developments, with full readings of the lattice investigation, one-bit precursor investigation, conditioning and tilted-body notes, positive-power/refinement and source-scope notes, three-witness and cap-set notes, and rational polar-spanner note. The finite separable companion and promoted nonconvex pointer were also checked. Canonical-source comparison included statement/section inspection across the whole set and targeted proof comparison; I did not reread every historical canonical proof or every audit in full. The manuscript proofs themselves were read and reconstructed throughout.

The inventory retains the stronger output-count finite overlay, direct maximum-product transfer, the six separable comparisons, the general polynomial overlay, and the distinct precursor arguments even when stronger results supersede their quantitative conclusions. The earlier numerical degree-32 variant is correctly treated as superseded by the exact product family; the hinge and Bernstein stability mechanisms remain separately explained. I found no missing substantive stage-4 development in these comparisons.

## Primary lens: lattice-free boundaries and precursor completeness

1. **Strict violation sets, lines 1271–1280.** The strict epigraph inequality for a convex component defines a convex subset of the lift. Its integer-coordinate projection is convex and has no integer point, since any such point would supply an invalid integral witness. No closedness of the lift or projection is needed for this statement. The discussion correctly refrains from applying a theorem requiring a closed full-dimensional maximal lattice-free body to that projection without further work.

   The warning about taking the convex hull across outputs is substantive. As an independent check, let the exact vector graph be `F(x)=(0,0)` on `[0,1]`, use unit box error, and let the convex lift have `-1/2 <= z <= 1/2` and `w=(-4z,4z)`. Its only integral section is `z=0`, where the exact graph is retained. The two upper-violation projections are `[-1/2,-1/4)` and `(1/4,1/2]`. Each is integer-free; their convex hull contains zero. Thus the asserted obstacle occurs in an admissible graph lift, not just in an unrelated union of convex sets.

2. **Helly versus covering, lines 1282–1286.** I checked Averkov–Weismantel Theorem 1.1 and its definition of the Helly number in the cached primary paper. The formula `(q+1)2^p` concerns finite intersection/infeasibility certificates. It does not by itself produce an error-preserving interval cover, and the manuscript does not discard the unrestricted continuous dimension from that formula. The source supports the stated distinction.

3. **Integral Radon, lines 1287–1297.** I checked the definition following Theorem 1.4 in the same primary source: disjoint witness subsets need a common integer point in their convex hulls. A same-parity pair only gives an integral midpoint; it does not supply the required disjoint Radon partition or a common input for two lifted mixtures. Interleaved input supports therefore remain an unproved step in the proposed route. The manuscript identifies gaps in particular arguments and makes no impossibility claim about other lattice methods.

4. **Precursor mechanisms, lines 848–876 and 963–1000.** The direct three-witness argument handles arbitrary integer labels: a difference at least three admits a forbidden rational chord weight, while three remaining distinct labels must be consecutive. The midpoint of the extreme labels can be mixed again in the middle section to produce equal thirds. This additional convexification is retained separately from the cap-set shortcut. The hinge construction verifies the entire middle integer section, and its Bernstein transfer preserves convexity and the strict error margins. These mechanisms are not lost behind the sharper degree-32 product theorem.

5. **Correct open question, lines 1259–1297 and the framing.** The product example increases input dimension; the tilted example changes the error body and has growing conditioning; the nonconvex scalar example drops convexity; the positive-power example does not determine a growing difference of the two optimum counts. The abstract, introduction and conclusion do not present any of these as resolving the one-input convex box constant-gap question. The text consistently calls that question unresolved here rather than asserting an exhaustive literature verdict.

## Whole-stage mathematical checks

- **Common partitions and rank transfer:** reconstructed the `2H-1` level refinement, cover trimming, deterministic ordered quantile tree, fixed common denominator, multiset order statistics, source-cell recovery and repeated endpoints. The compiler uses one common interpolation weight and excludes invalid indices. Original-output spanners preserve nonnegative component gaps despite signed representation coefficients. The finite/compiled box and facet constants follow from the stated scalar count.
- **Oracle construction:** checked the product-support inequality and factor-seven approximate version, including dimension one; effective-image radii and nonzero pulled-back separators; seed conditioning; fixed-grid exact feasibility repair; determinant-doubling termination; positive-polar weak separation; and both spanners. The rounding is performed in effective coordinates, keeping its error in the nonlinear image. The `17/64` center and `49/64` admitted-error bounds and the factor `69984 r^2` count are consistent.
- **Separable vectors:** the same concatenated row basis or nonlinear image is used for every coordinate. Product packing uses a sum of selected normalized outputs, rather than unrelated local bases. The capacities 12 and 5832 give the displayed six bounds; the compiled factors 87480, 157464 and 1277208 are below the corresponding powers of two. The supplied representation excludes mixed-coordinate nonlinear terms, and affine-only coordinates are removed.
- **Obstructions and exact counts:** checked the thirds margin `2177/2144`, the extended-weight margin `8785/8192`, the modulo-three and cap-set reductions, the complete middle integer section of the rational boxes, and the product contact lower bound. The binary lower bounds are explicitly valid for arbitrary convex binary lifts, while upper bounds are linear. The binary product construction is allowed exponential continuous size.
- **Nonconvex, signed overlay and conditioning:** checked the Bernstein approximation and rational encoding, whole-graph two-integer realization, peak/trough binary lower bound, convexity-piece upper, sign-specific bands and bracket errors, affine outputs and zero-bit cases. The tilted-body scalar projection and radius ratio `8+60M^2` follow from the centered second-difference estimate. The simplex and normalization arguments also support the nonsymmetric finite extension as stated.

For consequential imports, I independently inspected cached primary statements of GLS Definition (5)/Theorem (3.1), Ellenberg–Gijswijt Theorem 4, and Averkov–Weismantel Theorem 1.1 and integral Radon definition. In particular, GLS's objective comparison is with the entire body, and its dimension-at-least-two convention is addressed by the product embedding. I did not conduct a new literature search or verify every bibliographic publication detail. Root and historical audits were used as leads, not as substitutes for the proofs.

## Executed checks and limits

- All 11 snapshot SHA-256 hashes match.
- All 57 cross-reference targets and 22 citation keys used in stage 4 and the framing resolve.
- All 239 distinct relative source paths linked in `coverage.md` exist.
- `python code/positive_vector_obstruction/check_box_gap_root.py` passed: 72 middle-section vertices, 2,048 exact integer-section mixtures and 390 product contact-pair obstructions.
- `python code/positive_vector_obstruction/check_first_review.py` passed: 120 rational witness pairs, 15 actual-power gaps and 306 residue combinations.
- `python code/quadratic_rank/check_rational_polar_spanner_second.py` completed successfully: 16 generic systems, 93 repaired calls, 11 exchanges, 120 image-vertex checks and 347 positive-polar cases.

These finite checks supplement the general arguments; they do not establish the unrestricted statements by testing. I did not run a shared or isolated LaTeX build, inspect the rendered PDF, or claim formal proof verification. Only this reviewer report was written.

## Findings

None. No repair is requested.

## Frozen manuscript SHA-256 hashes

Paths are relative to `paper-integer-dimension`; all match `reviews/stage4-round1/snapshot.json`.

| File | SHA-256 |
| --- | --- |
| `abstract.tex` | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| `coverage.md` | `d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c` |
| `references.bib` | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| `sections/00-introduction.tex` | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| `sections/04-vector.tex` | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| `sections/05-conclusion.tex` | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |
