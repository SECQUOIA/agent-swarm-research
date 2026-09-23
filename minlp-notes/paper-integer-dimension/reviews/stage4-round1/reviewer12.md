# Stage 4 round 1 — reviewer 12

Major findings: 0
Minor findings: 0

No concrete major or minor defect was identified in this review. This is a bounded review of the frozen stage, not a guarantee of correctness, novelty, or publication acceptance.

## Scope and evidence

I read `PROCESS.md`, `reviews/PROTOCOL.md`, `STAGE4-TASK.md`, `STAGE4-LENSES.md`, and the snapshot. I read all 1,297 lines of `sections/04-vector.tex`, the complete abstract, introduction, and conclusion, the bibliography, macros and main driver, and the coverage inventory. I checked the accepted dependencies for parity contacts, finite disjunctions, scalar chord refinement and packing, indexed compilation, the hybrid polynomial compiler, Jensen superadditivity, and rational log-determinant allocation with central-ball repair. Earlier complete reviews of stages 1–3 informed dependency navigation; the stage-4 arguments were reconstructed independently.

I compared the ten stage-4 canonical result statements and their proof mechanisms with the corresponding `results/` sources. I checked the eleven named supporting developments against their `notes/` sources, with full readings of the conditioning, tilted-body, hinge/stability, finite separable, lattice-boundary, cap-set, and three-witness notes. The promoted nonconvex note is only a pointer; its substantive argument appears in the canonical polynomial-gap source and the manuscript. I did not treat existing audit verdicts or root's source audit as mathematical evidence.

The primary-source checks included Awerbuch–Kleinberg, Section 2.3, Propositions 2.2 and 2.4, for the classical maximum-determinant spanner and exchange method; GLS, printed page 172, Definitions (5)–(7), Theorem (3.1), and Corollary (3.5), for the stated weak optimization convention and anti-blocker background; Ellenberg–Gijswijt, Theorem 4, for the cap-set estimate; Averkov–Weismantel, Theorem 1.1, for the mixed Helly identity; and Hartman, printed page 707, for the historical difference-of-convex framework. I read the supplied primary text extracts and opened the original Awerbuch–Kleinberg and Hartman PDFs online. The primary passages support the qualifications in the manuscript. In particular, the common-quadratic convexification is proved directly here and does not depend on an unstated Hartman theorem. Sources: [Awerbuch–Kleinberg](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf), [GLS](https://ir.cwi.nl/pub/10046/10046D.pdf), [Ellenberg–Gijswijt](https://arxiv.org/abs/1605.09223), [Averkov–Weismantel](https://arxiv.org/abs/1002.0948), [Hartman](https://msp.org/pjm/1959/9-3/pjm-v9-n3-p09-p.pdf).

## Independent mathematical assessment

1. **Refinement and simultaneous interpolation.** The level cuts produce at most `2H−1` intervals: the new error is the old concave gap minus its endpoint interpolant. Restriction and finite closed-cover trimming preserve the bound. The finite output and facet overlays count cuts correctly. For implicit arrays, integer numerator selection preserves multiplicity; positive merged cells cannot cross any source knot. Source metadata handles duplicates and endpoints. Using one deterministic bisection tree for all mass targets establishes ordered returned knots without requiring monotone approximate mass estimates. Known common denominators and the shared interpolation weight satisfy the indexed compiler's hypotheses.

2. **Box and facet curvature rank.** A maximum-volume original-row basis has coefficients bounded by one, while rational determinant doubling gives factor two without changing the represented quotient by affine functions. Signed coefficients cause no problem because the selected chord gaps are nonnegative. The finite factors `4r−1` and `8r−1`, and compiled factors below `2^12 r` and `2^13 r`, follow at the stated tolerances. The half-body facet band is necessary for coupled errors and is used correctly. Compactness and nonnegative facet weights justify rank-zero affine degeneracy.

3. **Maximum-product allocation.** The first-order supporting inequality gives the finite dimension bound. The approximate-product comparison is valid: testing `(1−1/m)b+v/m`, expanding the product, and using `(1−1/m)^(m−1)≥e^(−1)` gives a bound strictly below `7m`; dimension one is handled separately. The accepted allocation lemma supplies exactly feasible rational coordinates, so this is not an assumption of an exact product optimizer. The resulting box band lies inside the unconditional body.

4. **Oracle rank construction.** The effective image eliminates affine directions. The pullback body has explicit inner and outer radii, and violated pullback separators have a nonzero normal. For the rational spanner, the initial determinant gives uniform inverse/objective bounds. A single rational grid and fixed central repair keep denominator lengths bounded across exchanges. The loss at most `1/4`, exchange threshold two, and final coefficient bound `9/4<3` are consistent. GLS weak optimization compares the returned objective against the full body, as required; its dimension convention is addressed by the product trick. Positive-polar access gives weak separation, not an unjustified strong oracle. The seeds are feasible and span the effective image.

5. **Explicit oracle bands.** With the two spanners, `P⊂K∩S⊂drP`. The finite scalar tolerance `1/(2r)` and compiled tolerance `1/(36r)` give the claimed counts. Effective-coordinate rounding contributes `P/16`; the compiled center error is `17P/64`, and adding the band `P/2` yields only `49P/64⊂K`. Rounding in the effective image, followed by exact affine restoration, is essential and is preserved.

6. **Separable vectors.** The same concatenated original-row or positive-polar basis is used across coordinates. Jensen superadditivity turns index distance into a scalar midpoint gap. The deleted lattice ball bound `[3(2q+1)]^n` gives all six finite/compiled comparisons with the stated tolerances. Per-coordinate bit ceilings are absorbed through capacities `12P_i` and `5832P_i`. Affine-only coordinates are removable, and the count constants `7n`, `8n`, `17n`, `18n`, and `21n` are supported.

7. **Power obstruction and cap sets.** The midpoint bound does not imply simultaneous refinement. The oriented thirds error is exactly bounded below by `2177/2144>1`; residue and binary-fiber arguments apply to arbitrary convex lifts. Every separately chosen signed scalarization has a two-rectangle construction because its oscillation is controlled by the positive absolute-weight sum. The cap-set reduction excludes nontrivial zero-sum triples; Theorem 4 specializes to the stated monomial count. Minimizing its generating-function bound gives `4t²+t−2=0`. The repeated-convexification proof also handles arbitrary one-dimensional integer labels, not merely labels initially chosen as 0, 1, 2.

8. **Exact convex separation and stability.** For the degree-32 boxes, the entire middle integer section has outer weights `t,t`, input in `[c,1−c]`, and both admitted and true outputs in `[0,1)`. Thus validity covers all convex mixtures. The oriented thirds contacts yield the exact product residue lower bound `p_conv=n` and the stronger binary count `ceil(n log₂3)`. The rational binary upper may have exponential continuous size, as stated. The affine monotonicity shear preserves errors and count and has nonnegative derivative. The hinge precursor and Bernstein convexity/stability proof survive as distinct mechanisms.

9. **Nonconvex polynomials and signed overlay.** The Bernstein error is `1/32` at degree `1024M²`, and the period/orientation formulation includes period endpoints. Peak contacts require distinct binary fibers. Alternating peaks and troughs force at least `2M` zeros of `q_M−1/2`, supporting logarithmic degree order without confusing degree with exponent bit length. The arbitrary polynomial overlay uses rational root brackets, curvature-sign complements, source-type flags, and correctly directed endpoint rounding. The bracket error and both signed bands contain the graph and remain within tolerance; the flags add no declared integers.

10. **Tilted body — principal lens.** In `prop:tilted-gap`, `F_M=(q_M+C_M x²,C_M x²)` is componentwise convex because `|q_M''|≤C_M−1`; the actual second derivative of the added term is `2C_M`, so the bound is conservative. The scalar projection `s=w_1−w_2` preserves the full graph and has error at most `1/4`. Conversely, the two-integer scalar band and `0≤w_2≤C_M` admit every exact vector graph point and satisfy both tilted error inequalities. No nonlinear equality is imposed in this upper construction. The body contains `(C_M,C_M)` but not its first-coordinate sign flip.

    The centered second-difference estimate is `−15/8`, and the triangular kernel has integral `h²`, with `h=1/(2M)`. Hence `max|q_M''|≥(15/2)M²` and `C_M≥1+(15/2)M²`. The common direction gives outer radius at least `sqrt(2)C_M`; the difference strip gives inner radius at most `1/(4sqrt(2))`. Their ratio is therefore at least `8+60M²`. The manuscript correctly presents this as a family with deteriorating conditioning, not a counterexample for a fixed well-conditioned body or unconditional body.

11. **Conditioning and normalization — principal lens.** In `prop:conditioning`, the parity midpoint vector is nonnegative. Infinity containment gives scalar midpoint gap at most `mb`; Euclidean containment gives at most `sqrt(m)b`. Doubling to full chord gap and refining to `a` or `a/sqrt(m)` yields the first comparison. In the simplex band, `g_F` and `v` are nonnegative with total mass at most `s`, so their nonnegative dot product gives `||g_F−v||₂²≤2s²`. Setting `s=a/sqrt(2)` yields precisely the sharper Euclidean factor. Only the outer bound on midpoint vectors and the centered inner ball for final errors are needed, so the nonsymmetric extension is valid. For unconditional normalization, sign averaging yields every `±e_j`, hence `B_1⊂K'⊂B_infinity`; the cube and simplex comparisons give the displayed `4m²−1` and `8m−1` factors. These are finite real constructions, and the text does not promote them to rational polynomial algorithms.

12. **Scope and synthesis.** The strict upper-violation set is convex; its projection contains no integer point, while unions across outputs need not be convex. The Helly identity concerns infeasibility certificates, and the Radon discussion correctly identifies missing ordering/error implications. The abstract, introduction, and conclusion distinguish the fixed-degree growing-input product separation, the nonconvex degree family, and the tilted-body transfer. They do not claim that these resolve the one-input convex box question. Count, rational length, construction time, and optimization complexity remain distinct.

## Focused computation

I wrote and ran `verification/reviewer12-stage4-conditioning.py`, using exact `Fraction` arithmetic. It passed 4,608 middle-section vertex mixtures, three thirds-incompatible contact pairs, 4,877 simplex error pairs in dimensions 1–5, 39 monomial second-difference identities, 99 tilted-radius constant checks, and seven compiled count constants. These finite checks corroborate the analytic arguments above and do not replace them. No manuscript file or shared LaTeX build was changed.

## Findings and limitations

There are no numbered MAJOR, MINOR, or unresolved QUESTION findings. I did not implement the complete oracle algorithms or compile the exponentially indexed MILP constructions. I did not rerun a whole-paper LaTeX build or conduct a fresh exhaustive priority search. Earlier sections were revisited at the dependency interfaces listed above, not reviewed afresh line by line in this stage. The original research comparison checks preservation of all named mechanisms; it is not a claim to have audited every historical note or alternative numerical variant.

## Frozen-file verification

All eleven actual SHA-256 hashes matched `reviews/stage4-round1/snapshot.json`.

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
