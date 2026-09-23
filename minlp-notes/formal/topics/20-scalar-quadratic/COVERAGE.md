# Topic 20: claim-to-proof coverage

This map covers every obligation in [CLAIMS.md](CLAIMS.md). It records the actual
lift theorems, their construction and geometric dependencies, and independent
review reports. The final source-frozen build, axiom audit and all 57 kernel
replays passed; results and fingerprints are in [VERIFICATION.md](VERIFICATION.md).

All modules below are in [`Formal/QuadraticPrecision`](../../Formal/QuadraticPrecision/).
Declarations are in the `QuadraticPrecision` namespace unless another namespace
is shown. A linked review covers the scope stated in that report; it does not
replace the final verification record.

## Models and transformations

| Claim | Actual declarations and coverage | Independent review |
|---|---|---|
| M1 | [Model](../../Formal/QuadraticPrecision/Model.lean): `ConvexIntegerLift`, `HasGraphLift`, `HasEpigraphLift`, `HasHypographLift`. [Parity](../../Formal/QuadraticPrecision/Parity.lean): `card_parityCode`, `ConvexIntegerLift.rawContact_cover`, `rawContact_midpoint`. Integer witnesses are arbitrary elements of `Fin p → ℤ`; the modulo-two proof includes negative and unbounded coordinates. | [Lifts and parity](reviews/lifts-parity.md) |
| M2 | [Parity](../../Formal/QuadraticPrecision/Parity.lean): `ConvexIntegerLift.compact_parity_cover`, `graph_compact_parity_cover`, `epigraph_compact_parity_cover`, `hypograph_compact_parity_cover`. Closure preserves the closed midpoint relation and the compact domain; the resulting compact sets are measurable. The original carrier and raw contacts need not be closed or measurable. | [Lifts and parity](reviews/lifts-parity.md), [lower bounds](reviews/lower-bounds.md) |
| M3 | [LowerPullback](../../Formal/QuadraticPrecision/LowerPullback.lean): `HasGraphLift.pullback`, `HasEpigraphLift.pullback`, `HasHypographLift.pullback`. [OutputReflection](../../Formal/QuadraticPrecision/OutputReflection.lean): the convex and binary `reflect_relaxation` theorems, one-sided `.neg` transformations, and `BinaryLinearLift.reflect_rowCount`. [Product](../../Formal/QuadraticPrecision/Product.lean): `product_hypograph_of_epigraph`; [ProductLinear](../../Formal/QuadraticPrecision/ProductLinear.lean): `product_binary_hypograph_of_epigraph`. These implement the required affine restrictions and output/sign changes with unchanged discrete dimension. [LinearSystem](../../Formal/QuadraticPrecision/LinearSystem.lean), [BinaryModel](../../Formal/QuadraticPrecision/BinaryModel.lean), and [UpperAssembly](../../Formal/QuadraticPrecision/UpperAssembly.lean) retain actual finite affine rows. | [Lifts and parity](reviews/lifts-parity.md), [product](reviews/product.md), [spectral upper](reviews/spectral-upper.md) |

## Exact square precision

| Claim | Actual declarations and coverage | Independent review |
|---|---|---|
| S1 | [IntervalLower](../../Formal/QuadraticPrecision/IntervalLower.lean): `interval_parity_lower`, `square_graph_integer_lower`. Every full-domain convex integer lift satisfies `ε ≥ (1/4)^p/4`. The proof selects `2^p+1` actual graph witnesses and uses their parity midpoint; it assumes neither a diameter cover nor a finite sampled approximation model. | [Square](reviews/square.md) |
| S2 | [SquareConstruction](../../Formal/QuadraticPrecision/SquareConstruction.lean): `squareRelaxation_contains_graph`, `squareRelaxation_error`, `squareRelaxation_attains`. [SquareSystem](../../Formal/QuadraticPrecision/SquareSystem.lean): `squareSystem`, `squareSystem_feasible`. [SquareLift](../../Formal/QuadraticPrecision/SquareLift.lean): `squareBinaryLift_graph`, `square_hasBinaryGraphLift`, `squareBinaryLift_attains`. The concrete system has `p` binaries, `2+2p` continuous auxiliary coordinates, and `11+10p` rows. The prefix construction includes depth zero and input one. | [Square](reviews/square.md) |
| S3 | [IntervalLower](../../Formal/QuadraticPrecision/IntervalLower.lean): `squarePrecisionCount`, `squarePrecisionCount_le_iff`, `squarePrecisionCount_sufficient`. [SquareMinimum](../../Formal/QuadraticPrecision/SquareMinimum.lean): `square_binary_feasible_iff`, `square_integer_feasible_iff`, `square_binary_minimum`, `square_integer_minimum`, `square_no_exact_integer_lift`. [CountMinimum](../../Formal/QuadraticPrecision/CountMinimum.lean) defines attained `IsMinimumCount`. The natural ceiling gives exactly the maximum with zero and handles equality at thresholds. | [Square](reviews/square.md), [precision arithmetic](reviews/precision-arithmetic.md) |

## Graph precision and Hessian rank

| Claim | Actual declarations and coverage | Independent review |
|---|---|---|
| R1 | [ContactVolume](../../Formal/QuadraticPrecision/ContactVolume.lean): `contact_volume_bound`, supported by its maximal determinant enclosure, polarization, and Gram determinant estimates and by [ContactNondegenerate](../../Formal/QuadraticPrecision/ContactNondegenerate.lean). The conclusion has the source constant `2^d (3 sqrt(d) δ)^(d/2) / sqrt(abs(det M))`. The corrected premise is `δ ≥ 0`; empty and zero-volume contacts and `δ=0` are included. | [Contact volume](reviews/contact-volume.md) |
| R2 | [PrincipalMinor](../../Formal/QuadraticPrecision/PrincipalMinor.lean): `exists_principal_minor_rank`, derived from the symmetric matrix's characteristic polynomial and actual rank. [LowerPrincipal](../../Formal/QuadraticPrecision/LowerPrincipal.lean): `exists_principal_coordinate_rank`, `coordinateMatrix_hessian`, `graph_principal_pullback`. The original complementary coordinates are fixed inside their intervals and the integer dimension is preserved. | [Principal minor](reviews/principal-minor.md), [principal lower bound](reviews/principal-lower.md) |
| R3 | [LowerPrincipal](../../Formal/QuadraticPrecision/LowerPrincipal.lean): `principalErrorConstant`, `graph_principal_error_lower`, `graph_principal_log_lower`, `graph_principal_error_pos`. These apply to the actual original-box graph lift and each injectively indexed nonsingular principal submatrix. [LowerContact](../../Formal/QuadraticPrecision/LowerContact.lean), [LowerVolume](../../Formal/QuadraticPrecision/LowerVolume.lean), and [LowerDeterminant](../../Formal/QuadraticPrecision/LowerDeterminant.lean) provide parity coverage, measure conversion, and exponent arithmetic. The explicit denominator remains `48 sqrt(r)`. | [Lower bounds](reviews/lower-bounds.md), [principal lower bound](reviews/principal-lower.md) |
| R4 | [Spectral](../../Formal/QuadraticPrecision/Spectral.lean): `spectral_signed_decomposition_nonzero`, `spectral_rank`, `spectralNormalized_mem`, coefficient sign/zero equivalences. [SpectralUpper](../../Formal/QuadraticPrecision/SpectralUpper.lean): `spectral_polynomial_decomposition`. The nonzero eigenvalue subtype has exactly `H.rank` elements. Its affine coordinates and positive normalization radii are constructed from the Hessian and box, rather than supplied as headline assumptions. | [Spectral](reviews/spectral.md), [spectral upper](reviews/spectral-upper.md) |
| R5 | [SpectralUpper](../../Formal/QuadraticPrecision/SpectralUpper.lean): `quadratic_graph_binary_upper`, `quadraticGraphLift`, `quadraticGraphLift_rowCount`, `quadraticGraphLift_auxCount`. [PrecisionArithmetic](../../Formal/QuadraticPrecision/PrecisionArithmetic.lean): `precisionDepth`, `precisionDepth_sufficient`. For the positive total spectral weight `A`, depth `precisionDepth A ε` is the required natural ceiling and gives error at most `ε`, `rL` binaries, `r(3+2L)` auxiliaries, and `2n+r(11+10L)+2` rows. [UpperBounds](../../Formal/QuadraticPrecision/UpperBounds.lean) constructs witnesses at the same original input, so normalized coordinates may be dependent. | [Spectral upper](reviews/spectral-upper.md), [precision arithmetic](reviews/precision-arithmetic.md) |
| R6 | [ScalarHeadline](../../Formal/QuadraticPrecision/ScalarHeadline.lean): `scalar_quadratic_graph_rank_law`, `scalar_quadratic_rank_zero_exact`. [LowerPrincipal](../../Formal/QuadraticPrecision/LowerPrincipal.lean): `graph_rank_lower`, `no_exact_graph_of_positive_rank`. [AffineBoundary](../../Formal/QuadraticPrecision/AffineBoundary.lean): actual zero-binary affine graph systems. `HasPrecisionRate` gives attained minima and uniformly bounded additive error for every sufficiently small positive real tolerance. | [Headlines](reviews/headlines.md), [principal lower bound](reviews/principal-lower.md), [precision arithmetic](reviews/precision-arithmetic.md) |

## One-sided precision and inertia

| Claim | Actual declarations and coverage | Independent review |
|---|---|---|
| I1 | [SpectralSlice](../../Formal/QuadraticPrecision/SpectralSlice.lean): `negativeEmbedding_injective`, `negativeEmbedding_coercive`, `negativeEmbedding_small_box`, `negativeSliceMap_injective`. [LowerNegativeSlice](../../Formal/QuadraticPrecision/LowerNegativeSlice.lean): `exists_negative_quadratic_slice`. The actual negative eigenspace, positive curvature modulus, and positive-width affine box inside the original box are constructed from the Hessian. | [Spectral](reviews/spectral.md), [inertia slice integration](reviews/inertia-slice-integration.md) |
| I2 | [LowerNegativeSlice](../../Formal/QuadraticPrecision/LowerNegativeSlice.lean): `epigraph_negative_inertia_lower`, using actual epigraph pullback and parity. The exact Euclidean constant is a separate theorem in [LowerIsodiametric](../../Formal/QuadraticPrecision/LowerIsodiametric.lean): `negative_contact_volume_sharp`, `epigraph_negative_volume_sharp`, `epigraph_strong_curvature_error_lower`, and `epigraph_negative_inertia_sharp_lower`, supported by [LowerEuclidean](../../Formal/QuadraticPrecision/LowerEuclidean.lean) and [Isodiametric](../../Formal/QuadraticPrecision/Isodiametric.lean). It gives `(μ/2)(volume(D)/ω_d)^(2/d) 2^(-2p/d) ≤ ε` for positive-volume compact domains and curvature `vᵀMv ≤ -μ‖v‖²`. It uses the Euclidean unit-ball volume, not a coordinate-box substitute. No upper output bound is imposed. The last theorem constructs the negative slice from the original Hessian and gives the sharp bound with slice volume `(2ρ)^k`; it has no assumed slice premise. The sharp-constant modules and their original-Hessian specialization passed independent review. | [Lower bounds](reviews/lower-bounds.md), [inertia slice integration](reviews/inertia-slice-integration.md); [sharp isodiametric review](reviews/isodiametric.md) |
| I3 | [Folding](../../Formal/QuadraticPrecision/Folding.lean): `foldSum_eq_sum`, `exactFold_eq_iterate`, `foldApprox_error`, `foldObjective_le`, `foldEpigraph_iff`. The exact iterated-tent sum and error are proved, as is dominance over every relaxed folding witness. Consequently the claimed projected lower boundary follows from optimization, not just feasibility of exact folds. | [Folding](reviews/folding.md) |
| I4 | [FoldingLift](../../Formal/QuadraticPrecision/FoldingLift.lean): `foldingSystem`, `foldingSystem_rowCount`, `foldingBinaryLift_relaxation`, `foldingBinaryLift_isEpigraph`, `square_has_zeroBinary_epigraph`. The formalized implementation uses depth `L+1`; `foldError_succ` gives error `2^(-2L-4)`, with zero binaries, `L+1` auxiliaries, and `3(L+1)+3` rows. | [Folding](reviews/folding.md) |
| I5 | [SquareConstruction](../../Formal/QuadraticPrecision/SquareConstruction.lean): `squareHypograph_contains`, `squareHypograph_error`. [SquareLift](../../Formal/QuadraticPrecision/SquareLift.lean): `squareBinaryLift_hypograph`, `square_hasBinaryHypographLift`. The output has only the hypograph upper restriction, so every downward ray remains feasible. Depth `L` uses `L` binaries and has error `(1/4)^L/4`. | [Square](reviews/square.md) |
| I6 | [UpperSquares](../../Formal/QuadraticPrecision/UpperSquares.lean): `signedSquares_epigraph`, `SignedEpigraph.bits_count`. [SpectralUpper](../../Formal/QuadraticPrecision/SpectralUpper.lean): `quadratic_epigraph_binary_upper`, `quadraticEpigraphLift_rowCount`, `quadraticEpigraphLift_auxCount` and their upper bounds. The actual system uses `k_-L` binaries, `k_-(3+2L)+k_+(L+1)` auxiliaries, and `2n+k_-(11+10L)+k_+(3L+3)+2` rows. Both positive continuous folding blocks and negative binary blocks use depth `L`, matching error `A(1/4)^L/4`; I4's finer depth `L+1` is not required here. The assembly lifts the entire epigraph, including arbitrarily large outputs. | [Spectral upper](reviews/spectral-upper.md), [folding](reviews/folding.md) |
| I7 | [ScalarHeadline](../../Formal/QuadraticPrecision/ScalarHeadline.lean): `scalar_quadratic_epigraph_inertia_law`, `scalar_quadratic_epigraph_zero_minimum`. [SpectralConvex](../../Formal/QuadraticPrecision/SpectralConvex.lean): `negativeInertia_zero_exact_epigraph`. These give both actual count minima, the uniform inertia rate, zero binaries for every positive tolerance at zero negative inertia, and an exact zero-integer convex lift in that case. | [Headlines](reviews/headlines.md), [spectral](reviews/spectral.md), [inertia slice integration](reviews/inertia-slice-integration.md) |
| I8 | [OutputReflection](../../Formal/QuadraticPrecision/OutputReflection.lean): convex and binary sign transformations. [SpectralUpper](../../Formal/QuadraticPrecision/SpectralUpper.lean): `quadratic_hypograph_binary_upper`, `quadraticHypographLift_rowCount`, `quadraticHypographLift_auxCount`. [LowerPositiveSlice](../../Formal/QuadraticPrecision/LowerPositiveSlice.lean): `hypograph_positive_inertia_lower`. [ScalarHeadline](../../Formal/QuadraticPrecision/ScalarHeadline.lean): `scalar_quadratic_hypograph_inertia_law`, `scalar_quadratic_hypograph_zero_minimum`; [SpectralConvex](../../Formal/QuadraticPrecision/SpectralConvex.lean): `positiveInertia_zero_exact_hypograph`. The corresponding counts use `k_+`, and output reflection preserves finite descriptions and coordinate counts. | [Headlines](reviews/headlines.md), [spectral upper](reviews/spectral-upper.md), [inertia slice integration](reviews/inertia-slice-integration.md) |

## Product precision and continuous LP row complexity

| Claim | Actual declarations and coverage | Independent review |
|---|---|---|
| P1 | [ProductLower](../../Formal/QuadraticPrecision/ProductLower.lean): `productAntidiagonal`, `product_epigraph_integer_lower`, `product_hypograph_integer_lower`. The original product epigraph is restricted to the actual antidiagonal; the hypograph uses the actual diagonal. [ProductExact](../../Formal/QuadraticPrecision/ProductExact.lean): `product_epigraph_lift_iff`, `product_hypograph_lift_iff`. Both best errors equal `(1/4)^p/4` for arbitrary integer convex lifts. | [Product](reviews/product.md) |
| P2 | [Product](../../Formal/QuadraticPrecision/Product.lean): `productUpperCarrier_convex`, `product_epigraph_of_square_hypograph`, `productUpperLift_attains`, `product_hypograph_of_epigraph`. [ProductExact](../../Formal/QuadraticPrecision/ProductExact.lean): `product_epigraph_integer_upper`, `product_hypograph_integer_upper`, `productExactEpigraphLift_attains`. The exact convex positive square and binary negative-square hypograph implement the stated `u,v` identity and lift every epigraph output; attainment is at a valid original product input. | [Product](reviews/product.md) |
| P3 | [ProductExact](../../Formal/QuadraticPrecision/ProductExact.lean): `product_epigraph_count_iff`, `product_hypograph_count_iff`, `product_one_sided_minimum`. [ProductLinear](../../Formal/QuadraticPrecision/ProductLinear.lean): `product_epigraph_binary_slack`, `product_hypograph_binary_slack`. The convex minima have the exact natural-ceiling formula; actual finite linear lifts approach the fixed-`p` error with every prescribed positive extra slack and no extra binaries. | [Product](reviews/product.md), [precision arithmetic](reviews/precision-arithmetic.md) |
| Z1 | [RowLower](../../Formal/QuadraticPrecision/RowLower.lean): `affine_minimum_with_equalities`, `square_epigraph_row_lower_bound_algebraic`, `square_epigraph_row_lower_bound`. [Polyhedron](../../Formal/QuadraticPrecision/Polyhedron.lean) and [PolyhedronAffine](../../Formal/QuadraticPrecision/PolyhedronAffine.lean) prove scalar projection closedness by Fourier–Motzkin elimination and actual minimum attainment. [RowLowerContact](../../Formal/QuadraticPrecision/RowLowerContact.lean) and [RowLowerCounting](../../Formal/QuadraticPrecision/RowLowerCounting.lean) prove the active-pattern separation and exact grid count. The headline has no attainment premise, allows lineality and unbounded auxiliary fibers, and counts only the `M` inequalities; finite equalities are uncounted. It yields `M ≥ (1/2)log₂(1/ε)-1`. I4 supplies matching logarithmic row order. | [Polyhedron](reviews/polyhedron.md), [row lower bound](reviews/row-lower.md) |

## Interpretation, corrections, and boundaries

`IsMinimumCount` includes feasibility and minimality over natural discrete
counts. `HasPrecisionRate` includes existence of such a minimum at every
sufficiently small positive real accuracy and one uniform bound on its additive
difference from the rank/inertia logarithm. It is stronger than a statement
along dyadic tolerances or a ratio limit. The asymptotic wrappers use the always
positive weight `spectralWeight + 1`; this only changes the additive constants.
The separate total-weight construction in R5 retains its sharper depth.

The source contact-volume lemma needs `δ ≥ 0`. Without it, an empty contact
satisfies the pair condition even when the claimed real upper bound is negative.
The precision applications already use `δ=4ε ≥ 0`. The formal proof fixes a
base contact point before maximizing the simplex determinant, an equivalent
route to the same constant. The exact finite-grid arguments for S1 and Z1 are
also equivalent proof routes, not numerical evidence or weaker sampled claims.

For I4, the proof follows the manuscript's depth-`L+1` folding construction.
It does not claim to formalize the note's distinct enhanced depth-`L` formula.
For I6, depth-`L` continuous blocks already meet the weaker shared error budget;
using them avoids an unnecessary off-by-one depth claim. Hypograph blocks and
all one-sided assemblies preserve the unbounded output direction.

The finite systems allow arbitrary real coefficients. The spectral construction
is mathematical, not a rational eigensolver or a bit-complexity algorithm.
Graph lower bounds assume positive box widths; the upper constructions also
allow fixed or empty boxes. Rank zero and empty input dimension have exact
affine graph systems. Zero inertia gives an exact convex one-sided lift, but
no exact finite LP representation of a curved epigraph is asserted. Product
finite-LP results allow positive extra error; exact LP attainment at every
optimal convex threshold is not asserted.

Topic 26 remains outside this work: general vector covariance,
noncommutative-rank, and nonlinear precision theory are not included. Neither
novelty/priority nor numerical solver correctness is a claim of this package.
