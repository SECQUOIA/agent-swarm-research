# Stage 4 round 1 — reviewer 04

Major findings: 0
Minor findings: 0

No concrete correction was identified in this review. I read the entire `sections/04-vector.tex` (1,297 lines), abstract, introduction and conclusion, and reconstructed the stage's mathematical arguments. The primary lens was the maximum-product transfer for unconditional error bodies. This is a bounded no-findings verdict, not a guarantee of correctness or external priority.

## Findings

No MAJOR, MINOR, or QUESTION findings.

## Primary-lens reconstruction

I checked `prop:vector-log-product`, its proof and its accepted allocation dependency in detail.

1. The finite optimum exists by compactness and is positive because the body contains a positive point. Unconditionality and convexity put the entire signed box `[-b,b]` inside `K`. Differentiating the feasible segment from an exact product maximizer toward any nonnegative feasible `v` gives `sum(v_j/b_j) <= m`; the segment remains positive for sufficiently small parameter even when `v` has zero entries.

2. Exact first-order optimality is not asserted for the rational approximate optimizer. Instead, approximate product optimality bounds the product ratio at the feasible point `(1-1/m)b+v/m`. Expanding the product and discarding nonnegative terms is legitimate, including zero coordinates of `v`. With `s=1-1/m`, the estimate `s^(m-1) >= exp(-1)` yields `S <= m(exp(2)-1)+1 < 7m` for every `m >= 2`. The last strict inequality holds already at `m=2`. The separate `m=1` argument is necessary and correct.

3. The scalar-block specialization of accepted `lem:block-logdet-oracle` applies with linear map `p -> Rp` and cap `p <= 1`. The output-radius assumption ensures that no positive feasible `b` is lost after scaling. Product approximation is preserved by the constant factor `R^m`. The output is exactly feasible and rational. Its polynomial encoding controls the lengths of its positive coordinates' reciprocals; no assumption of a numerically well-conditioned allocated box is being made. Consequently the dense normalized polynomials `F_j/b_j` and their evaluation precision retain polynomial encoding.

4. On each parity hull the approximate supporting inequality gives scalar midpoint gap at most `7m`, hence full scalar gap at most `14m`. Arbitrary-factor refinement gives at most `28m-1` pieces at scalar tolerance one. The hybrid construction's `486 N_1` cell bound therefore gives a total below `2^14 m 2^p`. The comparator lift is used only for the proof; the algorithm never needs its count or witnesses.

5. Componentwise nonnegative chord gaps make every normalized component gap no larger than their sum. Downward endpoint rounding by at most `1/8`, followed by the `13/16` and `1/8` directed band, contains the entire graph and admits errors in `(15/16)[-b,b]`. All components use the same input cell and continuous interpolation weight. This verifies simultaneous containment, rather than separate scalar existence. Affine graphs are handled exactly.

The manuscript's predecessor attribution is accurate at the level used here: Kelly–Maulloo–Tan Section 2, NETWORK and equation (1), identifies the log-utility optimum with the proportional-fairness supporting inequality for unit weights. The manuscript proves the general-body application and the approximate-product factor itself.

## Full-stage proof coverage

- **Refinement and overlay (lines 17–172).** I checked arbitrary integer-factor level cuts, plateaus and equality at the maximum, cover trimming, component/facet overlays and the need for a half-body band under coupled budgets. The ordered mass routine uses one canonical deterministic evaluation at each node; this is enough for monotonic target outputs without requiring approximate mass values at different nodes to be ordered. Integer numerator searches correctly recover multiset order statistics on a fixed common denominator. Duplicate endpoints, endpoint one, source-cell recovery, zero-length cells, invalid codes and shared weights are covered.
- **Original-output bases and rank (lines 174–280).** Exact maximum determinants give coefficient bound one; determinant-doubling exchanges among original rational rows give bound two with polynomial bit length. Retaining original convex functions is what permits domination despite signed representation coefficients. I checked the box/facet constants, normalized rounding, explicit coupled bands and rank-zero implication from compact nonnegative facets.
- **Rational spanners and positive-polar access (lines 341–491).** Seed determinants and cofactors give uniform objective bounds. The grid and repair weights are fixed before exchanges, so later inverses cannot accumulate uncontrolled denominators. Repair is exactly feasible by the inner-ball convex-combination argument; its objective loss is at most one quarter. Optimizing both signs gives the stated `9/4` coefficient bound on termination. The dimension-one padding preserves the imported oracle guarantee. Feasible support optimization yields a genuine weak positive-polar separator, and its membership branch certifies distance by scaling the query. Both polar and primal seeds are rational, feasible and independent. No strong polar oracle or exact support optimizer is assumed.
- **Effective-image graph bands (lines 493–579).** The effective body has valid explicit balls, and a strict exterior separator pulls back nontrivially. Positive polar scalarizations span the nonlinear image and preserve convexity. The separate primal spanner gives `P subset K intersect S subset drP`. I checked finite `8r^2-1`, the compiled scalar tolerance, gap `13P/64`, effective-coordinate rounding `P/16`, center error `17P/64`, and admitted error `49P/64`. Rounding takes place inside the effective coordinate system, so no error is inadvertently introduced outside `S`.
- **Separable vectors (lines 581–742).** One concatenated basis works in all coordinates. Jensen superadditivity gives the product-index separation, and the geometric-series bound on the integer l1 ball supplies the packing denominator. I checked all six finite/compiled comparisons and their numerical capacity constants, the common coordinate indices and weights, the summation of local rounding errors, inactive coordinates and rank zero. No arbitrary mixed-coordinate polynomial extension is inferred.
- **Positive-power and cap-set obstructions (lines 744–887).** I checked the uniform midpoint bound, all signed normalized scalarizations, separated-layer Bernoulli estimates, oriented thirds combinations and residues modulo three. The binary lower applies to every convex binary section. The cap-set reduction also handles three distinct zero-sum residues and obtains the stated generating-function bound. The direct one-integer proof treats arbitrary distant labels and then repeated convexification of three consecutive labels. These statements are correctly distinguished from an unbounded difference between the two optimum dimensions.
- **Exact convex product counts and stability (lines 889–1009).** The rational three-box construction controls the entire middle integer section with weights `(t,1-2t,t)`. The thirds obstructions give distinct product residues and binary codes, proving the exact counts. The binary upper's potentially exponential continuous size is explicitly acknowledged. I also checked the monotonicity shear, hinge precursor, Bernstein variance estimate, convexity-preserving second differences and thickening stability.
- **Nonconvex scalar family and arbitrary vectors (lines 1011–1152).** The Bernstein triangular-wave approximation has the stated rational degree/encoding and uniform error. Period plus orientation uses at most two general integers; distinct peaks require distinct binary sections. The actual-degree lower and upper support the worst-case logarithmic order. For arbitrary vector outputs, rational root brackets and sign-constant complements give the claimed counts; convex, concave and bracket flags select correct directed bands. Restricted source cells preserve the required error bounds, including at repeated merged endpoints.
- **Tilted bodies, conditioning and the open boundary (lines 1154–1297).** The common quadratic makes both components convex while the narrow difference direction retains the scalar lower bound. The second-difference identity proves growing condition ratio. Downward boxes and simplex bands give the stated finite conditioning comparisons, including nonsymmetric bodies containing the given inner ball. Axis normalization of unconditional bodies is justified. Strict upper-violation sets and their projections are convex and lattice free; their union need not be. The mixed Helly and integral Radon discussions correctly identify missing implications rather than claiming an obstruction theorem.

The abstract, introduction and conclusion agree with these proved scopes and the accepted earlier stages. In particular, they distinguish finite count from rational encoding and construction, allow unrestricted comparator lifts, identify the multivariate nature of the exact product amplification, identify the growing conditioning of the tilted example, and leave the one-input convex-vector box constant-gap question open.

## Source and dependency coverage

I compared all ten canonical stage-4 result statements and their mechanisms against the corresponding manuscript statements: convex and arbitrary polynomial overlays; original-output box, facet and oracle curvature rank; direct unconditional allocation; both coupled separable rank results; exact convex box counts; and nonconvex scalar degree gaps. I checked all eleven explicitly substantive supporting developments in `coverage.md`: conditioning/simplex arguments, finite separable rank, lattice-route limits, the hinge/Bernstein precursor, tilted bodies, the promoted nonconvex pointer, vector-power source/quantifier assessment, vector-power obstruction and finite overlays, cap sets, the three-witness argument, and rational polar spanners. The direct allocation canonical source and rational-spanner supporting development received full proof comparison. I did not reread every line of every historical canonical derivation or audit; the complete manuscript proof reconstruction is the basis of the verdict.

Relevant accepted dependencies checked include the definitions and parity/disjunction mechanisms in section 01; the scalar-block log-determinant oracle and central repair in section 02; and indexed endpoint compilation, scalar chord geometry, the actual hybrid cell-count/error guarantees and Jensen superadditivity in corrected section 03. I read the bibliography's new entries and inspected primary passages for the consequential imports: Kelly–Maulloo–Tan's Section 2; GLS Definition (5) and Theorem (3.1), including comparison against all exact feasible points; Ellenberg–Gijswijt Theorem 4 and its finite-field specialization; and Averkov–Weismantel Theorem 1.1's mixed Helly identity. These passages are in the manuscript's primary-source cache. The paper proves its spanner exchange/repair and Bernstein/DC applications directly. Root's source audit and prior reviews were leads, not substitutes for proof.

## Executed checks

All of the following completed successfully:

- `check_implicit_knot_overlay.py`: 2,304 ordered-search checks, 60 exact order statistics, 180 source-cell containments, 8 large-grid ranks and 99 directed-band checks.
- `check_rational_polar_spanner_second.py`: 16 synthetic rational systems, 93 repaired optimizer calls, 11 exchanges, 120 full-image vertex checks and 347 positive-polar cases. This checks the repair/exchange interface, not the GLS algorithm itself.
- `check_box_gap_root.py`: 72 middle-section vertices, 2,048 exact integer-section mixtures and 390 product contact-pair obstructions.
- `check_oracle_curvature_rank_mixed_coordinates.py`: 70 positive-polar representations and 9,216 exact rounding/band checks remaining in a rank-two effective image.
- `check_separable_oracle_rank_precision.py`: 96 exact lattice-ball bounds and 1,536 coupled separable rounding/band checks.

I independently ran exact rational checks of the primary-lens constants: 511 dimensions `m=2,...,512` satisfied the factor-seven bound even after replacing `e` by the weaker upper bound `11/4` while retaining the exact `s^(m-1)`; 4,088 nonnegative product expansions satisfied the discarded-term lower bound; 1,024 dimensions satisfied the compiler-count inequality; and the directed-band constants were checked exactly. These are finite checks supplementing the analytic proof.

## Snapshot integrity

All eleven SHA-256 hashes were recomputed and matched `reviews/stage4-round1/snapshot.json`, including a final verification before writing this report. Paths are relative to `paper-integer-dimension`.

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

## Limits

I did not run a shared LaTeX build, perform a full PDF typography review, solve generated MILPs, or implement a complete GLS oracle and compiler. The cited scripts are finite exact/numerical checks with the scopes stated above. I did not repeat every accepted stage-1–3 proof or conduct an exhaustive external-priority search. No manuscript, bibliography, inventory, original research or other reviewer report was edited.
