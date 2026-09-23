# Independent review of the model and indispensable rays

Reviewer: the topic 29 source-inventory agent. Date: 2026-09-22.

Status: semantic review complete for the model, real witnesses, ray
cardinality, and final strict and closed obstruction interfaces. No defect
or coverage gap remains. Final package machine checks are separate.

## Exact model and Gram realizations

`Model.lean` uses `qnorm u=dot u u` and the real dot product, so its
inequalities are the source's Euclidean quadratic inequalities, despite the
maximum norm instance on the ambient function space. The two-vector model
has exactly `2r` free real coordinates. `eval`, `homEval`, `aggregate`, and
`homAggregate` have the source constants and cross-term factors; the
displayed aggregation formulas and `homEval_one` prove their consistency.
`HHC` quantifies every nonzero linear-functional kernel in the homogeneous
space, which is the actual source hyperplane condition.

`feasible_nonempty` uses the simpler rational witness
`u=v=(3/4)e_1`: its squared lengths and mutual inner product are `9/16`,
strictly between `1/2` and `1`. The source's square-root witness is not
needed. `feasible_bounded` derives coordinate bounds from the Euclidean
squared lengths before proving boundedness in the maximum product norm.
This preserves the finite-dimensional boundedness claim rather than
substituting a different norm into the inequalities.

`gram_realization` constructs actual vectors using the first two distinct
coordinate basis vectors. It assumes a positive first Gram diagonal and
a nonnegative determinant, and realizes the second vector using
`sqrt(q-c²/p)`. Positivity of `p` justifies division and the square root;
the determinant condition gives the remaining nonnegative radicand.
Thus it covers singular as well as positive-definite witness matrices
for every `r≥2`, without a higher-dimensional completion assumption.

## Scalar ray and cardinality statements

`ray_slack_nonpos` and `ray_slack_eq_iff` prove the weighted AM–GM
inequality and its equality case directly from the rotated-cone
discriminant. Equality plus nonnegative nonzero weights forces the third
weight positive and identifies the positive scale as `w_3/2`. The
conclusion is equality to a positive multiple of `(tau,1/tau,2)`, not
merely membership in its span. The boundary parameter is positive; the
later interval `[1,2]` supplies that hypothesis at both endpoints.

`sameRay_unique` uses the fixed third coordinate `2` to identify scales,
then the first coordinate to identify parameters. It covers all vectors
admitting the two positive-ray representations. `exists_omitted_ray`
and `exists_omitted_ray_countable` consequently apply to arbitrary finite
or countable sets of weights, including repeated or zero-ray candidates.
They do not assume the desired omitted parameter as input.

`witness_gram_bounds` proves a positive first diagonal and strictly positive
determinant throughout `[1,2]`, using uniform lower diagonal bounds `4/5`.
`witness_exists` combines this with `gram_realization` to construct actual
source witnesses. `witness_eval_formula` states their literal residual
vector, and `witness_aggregate_formula` gives the aggregate identity for
every multiplier. No Gram-feasibility premise remains in the final witness
existence theorem.

`normalizeRay w=(2/w_3)w` sends any weight on the prescribed positive ray
exactly to `(tau,1/tau,2)`. `ray_cover_uncountable_normalized` proves that
the image of the weight family under this normalization is uncountable.
This is stronger than merely proving an uncountable indexing type and
addresses the source's distinct-ray requirement. `normalizeRay_pos_smul`
explicitly proves invariance under positive scaling, including the zero
third-coordinate case. Weights with that coordinate zero normalize to
zero; collapsing them cannot introduce spurious uncountability.

## Final strict and closed statements

`witness_slack` gives both nonpositivity and the exact positive-ray equality
condition. `witness_separates` uses the point's own strictly hull-valid ray
to exclude it from the ordinary hull, while proving strict satisfaction
of every other good-cone ray. `strict_description_contains_rays` then takes
the actual equality of that hull with a strict aggregation intersection;
if the family omits a ray, the corresponding actual point lies in the
intersection but outside the hull. `good_strict_description_contains_rays`
uses the proved classification to expose this conclusion for the original
spectral `Good` predicate, not just the derived cone predicate.

`good_strict_description_uncountable_rays` composes that exact-set theorem
with normalized-image uncountability. The countable and finite obstruction
theorems have the corresponding family cardinality and actual goodness as
their only additional premises. They do not assume ray coverage or an
unproved hull formula. The conditional cardinality conclusion does not
assert existence of an exact representation.

`finite_slack_perturbation` handles any finite indexed family, including
an empty one, by simultaneous continuity of its strict affine slacks.
`perturbed_gram_bounds` now proves a strict positive determinant for every
`0≤eta<1/10`. `finite_goodCone_closed_obstruction` first chooses an omitted
ray, then derives a common `eta>0` preserving every selected strict slack.
It constructs actual vectors from the perturbed Gram data and computes the
omitted aggregate as `2 eta`. That aggregate is nonpositive on the closed
hull by continuity, so the point lies outside it. Weak satisfaction of the
finite family follows from strict satisfaction. The proof does not infer
closed-hull exclusion merely from the unperturbed zero slack.

`finite_good_closed_obstruction` and `no_finite_good_closed_description`
give this construction and set-inequality conclusion for actual good
multipliers. `good_closedHull_valid` independently extends their strict
ordinary-hull validity to weak validity on its closure. The closed hull
is exactly `closure(convexHull S)`, without an assumed equality to the hull
of the original weak feasible system.

The model also proves `convexHull_bounded`, `convexHull_proper`, and
`convexHull_nonempty`. Properness follows from boundedness and the
nontrivial ambient real vector space for `r≥1`, so it covers all required
dimensions. All witness and final obstruction theorems retain only `r≥2`;
the four-variable case is included.

No mathematical defect was found in these final interfaces. The
review ran no Lean builds. Author builds and final package machine checks
remain separate evidence.
