The formalization targets `thm:exact-box-gap` in
[`sections/04-vector.tex`](../paper-integer-dimension/sections/04-vector.tex)
and the mathematical results, including the monotone variant, in
[`convex-polynomial-box-error-exact-integer-gap.md`](../results/convex-polynomial-box-error-exact-integer-gap.md).

| Mathematical obligation | Lean declaration | File |
|---|---|---|
| Exact graph, cube, unit componentwise error, arbitrary auxiliaries and unbounded integer codes | `Admissible`, `HasIntegerLift`, `HasBinaryLift` | [Model](Formal/Model.lean) |
| Rational box constants | `constants` | [Scalar](Formal/Scalar.lean) |
| Every graph point belongs to an appropriate box | `graph_in_box` | [Scalar](Formal/Scalar.lean) |
| Every point of each box satisfies unit error | `inBox_valid` | [Scalar](Formal/Scalar.lean) |
| Every real weighted mixture at an integer label satisfies unit error, including the middle slice | `integer_mixture_valid` | [Scalar](Formal/Scalar.lean) |
| Convexity of both polynomial components | `leftValue_convex`, `rightValue_convex` | [Scalar](Formal/Scalar.lean) |
| Rational polynomial representation and exact degree 32 | `aeval_leftPoly`, `aeval_rightPoly`, `leftPoly_natDegree`, `rightPoly_natDegree` | [PolynomialFamily](Formal/PolynomialFamily.lean) |
| Finite rational affine inequalities define convex feasible sets | `rationalPolyhedron_convex` | [RationalPolyhedron](Formal/RationalPolyhedron.lean) |
| Integer construction equals its explicit affine inequalities | `integerRows_iff` | [IntegerPolyhedron](Formal/IntegerPolyhedron.lean) |
| Integer upper bound, graph coverage and universal slice validity | `integerSystem_admissible`, `rational_integer_upper` | [UpperBounds](Formal/UpperBounds.lean) |
| Explicit integer formulation with 3n continuous auxiliaries and 13n inequalities | `integer_upper_linear_size` | [UpperBounds](Formal/UpperBounds.lean) |
| Exact incompatibility of all distinct scalar contacts under oriented thirds combinations | `contact_eq_of_thirds` | [LowerBounds](Formal/LowerBounds.lean) |
| Equal residues modulo three produce integer thirds combinations, including negative codes | `integer_third_codes` | [LowerBounds](Formal/LowerBounds.lean) |
| All-dimensional unrestricted-integer lower bound | `integer_lower_bound` | [LowerBounds](Formal/LowerBounds.lean) |
| All-dimensional arbitrary-convex binary lower bound | `binary_lower_bound` | [LowerBounds](Formal/LowerBounds.lean) |
| Binary mixtures use only identical codes on positive-weight terms | `binary_weight_support` | [UpperCore](Formal/UpperCore.lean) |
| Binary upper bound with complete graph coverage and slice validity | `binarySystem_admissible`, `rational_binary_upper` | [UpperBounds](Formal/UpperBounds.lean) |
| Explicit binary inequalities and their count | `mem_binaryRows`, `binary_row_count` | [UpperBounds](Formal/UpperBounds.lean) |
| Counting threshold equals the real logarithmic ceiling | `binaryCount_eq_natCeil`, `binaryCount_eq_intCeil` | [CountArithmetic](Formal/CountArithmetic.lean) |
| Exact minima for convex integer, convex binary, rational integer and rational binary classes | `exact_box_counts` | [ExactBoxCounts](Formal/ExactBoxCounts.lean) |
| Strict separation in every positive dimension | `strict_count_separation` | [ExactBoxCounts](Formal/ExactBoxCounts.lean) |
| Requiring closed lifted sets leaves both minima unchanged | `closed_integer_exact_count`, `closed_binary_exact_count` | [ClosedLifts](Formal/ClosedLifts.lean) |
| Invertible output shear preserves the actual graph-error contract | `shearedAdmissible_iff`, `admissible_sheared_preimage` | [AffineShear](Formal/AffineShear.lean) |
| Convex, closed, and rational lift counts are unchanged by rational shear | `sheared_exact_counts`; each class also has a bidirectional lift-existence equivalence | [AffineShear](Formal/AffineShear.lean) |
| Rational row substitution preserves all row and auxiliary counts | `eval_shearSubst`, `rationalPolyhedron_shearSubst`, `sheared_integer_linear_size` | [AffineShear](Formal/AffineShear.lean) |
| Monotone variant has derivative 56(1-(1-x)^31), convex components, and exact degree 32 | `hasDerivAt_monotoneLeftValue`, `monotoneLeftValue_monotone`, `rightValue_monotone`, `monotoneLeftValue_convex`, `monotoneLeftPoly_natDegree` | [MonotonePolynomial](Formal/MonotonePolynomial.lean) |
| Monotone variant does not have all nonnegative coefficients | `monotoneLeftPoly_coeff_three`, `monotoneLeftPoly_not_nonnegative_coefficients` | [MonotonePolynomial](Formal/MonotonePolynomial.lean) |
| Exact counts and linear-size construction for the actual monotone graph | `shearedGraph_monotone`, `monotone_exact_box_counts` | [ExactCountConsequences](Formal/ExactCountConsequences.lean) |
| One-input example and linear additive gap | `one_input_exact_counts`, `count_gap_formula`, `count_gap_linear_bounds`, `count_gap_slope_pos` | [ExactCountConsequences](Formal/ExactCountConsequences.lean) |
| Every box and every admitted integer slice has strict error below one | `inBox_strict_valid`, `integer_mixture_strict_valid`, `integerSystem_strict_sound`, `integerRows_strict_sound` | [StrictError](Formal/StrictError.lean) |
| Weighted-box projection equals the actual labeled-box convex hull | `weightedBoxes_iff_mem_convexHull`, `one_coordinate_weighted_hull`, `binarySystem_projection_iff_hull` | [BoxHull](Formal/BoxHull.lean) |
| Labeled-box hull is the convex hull of finitely many rational vertices and is compact | `labeledBoxes_convexHull_vertices`, `labeledBoxVertex_rational`, `isCompact_labeledBoxes_convexHull` | [BoxHull](Formal/BoxHull.lean) |
| Every feasible binary slice is exactly its selected product box; general integrality gives the same slices | `binarySystem_exact_slice`, `binarySystem_exact_integer_slice` | [BoxHull](Formal/BoxHull.lean) |
| Numerical data of the integer formulation are fixed independently of dimension | `integerRows_data_subset`, using one finite `integerDataAlphabet` for all n | [FixedData](Formal/FixedData.lean) |

All lower bounds quantify over arbitrary finite continuous auxiliary
dimension and every convex lift satisfying the representation contract.
The constructions prove both containment directions required by that
contract; checking only selected feasible points would be weaker.

The completed scope is the focused exact-count result note, including its
monotone affine shear. The hinge precursor, later Bernstein constructions,
and other theorems in the full integer-dimension manuscript are separate results.
Literature attribution, novelty, open-problem status, and the historical checker's
reported experiment counts are not mathematical conclusions of Lean proofs.

Equivalent proof routes need not match the note line by line: exact rational
normalization proves its numerical inequalities, and the weighted-box formulation
provides the same mathematical construction with fewer continuous variables.
The number of inequalities, auxiliaries, and dimension-independent numerical
literals are verified. No claim of linear serialized bit length or solver running
time is added. The original eleven proof modules remain unchanged; completion
proofs are in the additional modules listed above.

The [exact-count package](topics/00-exact-counts/README.md) collects the completion
and its verification record. No manuscript was written or edited.
