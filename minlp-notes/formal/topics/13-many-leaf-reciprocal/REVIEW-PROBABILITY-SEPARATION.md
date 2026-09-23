# Independent probability and separation review

The reviewer read `ManyProbability`, `ManyQuantile`,
`ManyProbabilitySelection`, `ManyProbabilityIntegral`, `ManyProbabilityEndpoints`,
and `ManySeparation`
in [the proof directory](../../Formal/ReciprocalAnchor), comparing their
statements and constructions with the source note and `CLAIMS.md`.
This is a semantic source review, not a compiler or CI result. The authors
reported passing targeted warning-free builds; the verification record owns
the exact commands and logs.

The reviewed probability and lower-cut results have the intended scope.
General-probability endpoint domination was added and reviewed to close MR22.
The complete rational oracle and its declared complexity accounting were
subsequently completed and reviewed in [REVIEW-ORACLE.md](REVIEW-ORACLE.md).
Those MR37 results are separate from the lower-cut results below.

## Obligation map

| Obligation | Reviewed declarations and conclusion |
|---|---|
| MR07 | `probabilityCall_integrable`, `probabilityCall_left`, `probabilityCall_right`, `probabilityCall_slope`, and `probabilityCall_convex` concern arbitrary probability measures with almost-everywhere support in the stated interval. There is no finite-support restriction. The slope assertion is the precise secant inequality between minus one and zero. |
| MR09 | `probability_selection_bound` proves the inequality for almost-everywhere strongly measurable selectors bounded in `[0,1]` almost everywhere; integrability of both the selector and selected first moment is proved. |
| MR10 | `probability_upper_tail_threshold` constructs an actual threshold by the cumulative distribution function. `probability_threshold_selection` constructs a measurable upper-tail selector, including a fractional threshold atom. `probability_upper_selection_isLeast` proves attainment of the infimum over all real thresholds, and `probabilityUpper_isGreatest` identifies the greatest realizable moment. |
| MR11 | `ProbabilitySelectable.complement`, `ProbabilitySelectable.interpolate`, `probabilityLower_isLeast`, and `probability_selectable_interval` prove the complementary minimum and every intervening value. Coincident extremes and endpoint masses are included. |
| MR12 | `probability_selection_iff` proves both directions of the two call-inequality criterion, given `q` in `[0,1]`. Its selector is globally measurable and globally bounded; no desired selector or threshold is an input premise. |
| MR13 | `probability_simultaneous_selection` chooses all individually admissible measurable selectors on the same law. It applies to any index type and therefore every finite family; no independence is assumed. |
| MR18 | `probability_reciprocal_fubini` proves integrability on the product measure from compact support and positive endpoints before swapping integrals. `probability_reciprocal_identity` proves the general-law reciprocal identity from the pointwise identity and that swap. |
| MR22 | `probability_mean_bounds` proves the supported law's mean bounds. `probabilityCall_le_endpoint_formula` integrates the pointwise chord inequality with proved integrability. `probabilityCall_le_endpoints` identifies the dominating function as the actual finite `Law.endpoints` call function. Its consequences for the least envelope and leaf realization are supplied by the finite-law core. |
| MR35 | `RationalCut.value_le_lowerMoment` proves global validity of every chosen-line rational partition, even for other candidate coordinates outside the leaf bounds. `segmentForm_eval_eq_integral` and `RationalCut.coefficients_eval` prove that this integral expression has explicit rational affine coefficients. |
| MR36 | `RationalCut.value_eq_lowerMoment_of_active` proves equality at the candidate whose envelope is followed. `RationalEnvelopeCertificate.toCut_exact` applies it to a valid rational envelope certificate. The existence and correctness of the certificate producer belong to the algorithm package. |
| MR37 | `exists_rational_separating_cut` proves lower-bound separation. The completed `ManyOracle`, `ManyOracleSize`, and `ManyOracleBitCost` integration supplies the complete executable dispatch, actual returned coefficients, and declared polynomial accounting; see `REVIEW-ORACLE.md`. The lower-cut existence theorem alone is not used to claim these results. |
| MR38 | `exists_rationalCut_approx` and `all_rationalCuts_iff_lowerMoment` prove completeness even at arbitrary real candidate coordinates, for rational positive interval endpoints and leaf masses in `[0,1]`. This resolves the real-candidate issue identified in the initial inventory. |

## Probability boundary checks

The support assumption is almost-everywhere membership in a compact interval,
which is appropriate for integrals and includes arbitrary atoms and continuous
laws. `IsProbabilityMeasure` supplies finite total mass one. No integrability
premise conceals a missing boundedness argument: the identity, call kernels,
selectors, selected moments, and reciprocal are each proved integrable before
their integral equalities or comparisons are used.

The quantile proof allows `q=0`, `q=1`, and `a=b`. It uses the left limit and
right continuity of the cumulative distribution function, so it distinguishes
strict and inclusive tails correctly at atoms. When the threshold atom has
zero mass, the two tail inequalities force the unallocated selected mass to
zero. The proof explicitly handles this case before using a nonzero
denominator identity.

The selector criterion uses globally measurable representatives bounded at
every real input. This is a valid sufficient construction for the source's
fractional submeasure statement. The inequality for an existing selector is
also proved under the weaker almost-everywhere measurability and boundedness
hypotheses. The model therefore does not accidentally exclude non-atomic
laws or rely on an unproved finite approximation.

## Rational cuts at real candidates

`RationalCut` fixes rational knots and an input-line index on each interval.
Its affine coefficients are independent of later candidate coordinates.
The cut's global validity follows from pointwise domination of every input
line by the maximum; it does not assume that the chosen lines stay active
away from the construction point. Duplicate knots are allowed and contribute
zero integrals. Positive left endpoints are derived from the interval bounds
where inverses are used.

Completeness at real candidates is not inferred from rational candidates.
`active_line_error` bounds the loss from retaining an active line at a left
grid endpoint by the cell length. The integrated loss is at most
`2*delta*(b-a)/a^3`; uniform rational knots make it tend to zero. Choosing a
mesh smaller than a strict violation produces a rational affine separator.
The active index may depend noncomputably on the real candidate, which is
appropriate for this existence and completeness theorem. Polynomial-time
separation is the distinct rational-input algorithm obligation.

The completeness theorem assumes the leaf mass bounds. This matches its use
within the full hull description, where those affine bounds are checked
separately. Its validity direction holds globally without that restriction.

## Interfaces closed after the initial review

The initial MR22 finding is resolved by `ManyProbabilityEndpoints`. The
reviewer read the added proofs and found their supported-measure, integral,
and endpoint-law interfaces correct. The author reported that
`lake build Formal.ReciprocalAnchor.ManyProbabilityEndpoints --wfail` passed.
The initial review also identified MR37's complete-oracle requirement:
failed mean or leaf inequalities, the upper secant, and the exact lower cut
must all be connected to a sound rejection or correct membership acceptance,
with the claimed operation and bit-size bounds. That integration has now
passed the separate oracle review, including zero leaves, repeated envelope
construction, actual output coefficient sizes, and operand widths. Its bit-work
claim uses the declared schoolbook model, with no backend refinement claim.

No other semantic gap was found in the modules reviewed here. No
project-wide verification or CI inspection was performed.
