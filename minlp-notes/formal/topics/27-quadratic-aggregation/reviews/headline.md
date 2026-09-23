# Independent headline and scope review

Date: 2026-09-22. Reviewer: the independent inventory/review subagent.
Reviewed the complete topic source chain, the actual headline theorem types,
and all twelve [frozen claims](../CLAIMS.md). This is a semantic source review;
the reviewer did not run a Lean build or axiom audit for this review. Passing
machine checks must be recorded separately by the coordinator.

## Verdict

No mathematical or statement mismatch was found in the reviewed source.
The full equivalence, its source-sequence form, and its HHC specialization
have the intended assumptions and conclusion. No conditional certificate
oracle or unproved closed-cone premise replaces the main theorem. All twelve
obligations have exact declaration mappings in [COVERAGE.md](../COVERAGE.md).

This verdict concerns the written Lean source. It does not assert successful
elaboration, absence of nonstandard axioms, a passed CI run, or verification
of the source note's excluded corollaries and examples.

## Original-system semantics

`System` stores real symmetric matrices `A_i`, real vectors `b_i`, and real
constants `c_i`. `eval` is precisely `x^T A_i x+2 b_i·x+c_i`.
`homEval` is precisely the associated form at `(x,t)`, with cross term
`2t b_i·x` and constant term `c_i t^2`. `feasible` uses every strict
inequality. The conclusion refers to the ordinary `convexHull ℝ`, without
silently closing it.

`Certificate` requires coordinatewise nonnegative weights, a nonzero weight
vector, `Matrix.PosSemidef` for the aggregate quadratic part, and a nonzero
quadratic or linear part. This rules out constant-only aggregations exactly
as the source requires. Matrix symmetry is input data and retained under
aggregation, not inferred from a quadratic-value condition alone.

HHC is expressed by the images of kernels of all nonzero real linear
functionals, the standard description of linear hyperplanes in this finite
dimension. Sweeping hyperplanes are shown to have that form. The model's
unbounded-level version of asymptotic convexity is explicitly equivalent to
the source's strictly increasing sequence tending to positive infinity;
the sequence headline exposes the source convention directly.

The headlines have only the system, strict nonemptiness, and the appropriate
convexity hypothesis as inputs. The difficult implication additionally takes
properness of the hull, as expected. No `n>=3`, `m>=2`, regularity, boundedness,
Slater condition beyond the stated strict feasible point, or rational-data
restriction is added.

## Dependency review

The easy implication constructs the actual convex aggregate strict sublevel
set and proves it proper. Its helper first shows that an everywhere negative
PSD quadratic cannot have a nonzero linear part, then that its quadratic
part must also vanish. Both source cases are covered without an eigenvector
premise or hyperplane-convexity assumption.

The recession proof uses continuity at the homogeneous points `(v,0)` and
`(-v,0)`, chooses a common positive sufficiently small parameter for all
finitely many constraints, dehomogenizes, and takes a midpoint. It yields
the full-hull result, not just an asymptotic direction estimate. Supporting
separation uses openness of the actual convex hull. `sweep_disjoint` handles
`t=0` through the recession result and any nonzero `t` through multiplication
by the positive square, with no incorrect division by a signed inequality.

Separation from the open negative orthant constructs the weights. Their
nonnegativity follows by testing an increasingly negative coordinate;
their positive sum follows from the all-negative vector. The final
normalization is proved and does not become a premise. The homogeneous
image contains zero, and separation is applied only after the swept
hyperplane is proved disjoint from strict homogeneous feasibility.

Closedness of the coefficient cone is proved from finite generation.
`ConeClosed.lean` reduces dependent generators to a finite union of smaller
cones and treats an independent family by a closed linear embedding. It
does not use the false general assertion that every linear image of a closed
cone is closed. `Coefficients.lean` identifies this cone with the actual
nonnegative aggregates and preserves symmetry.

The constant-elimination step has the correct inequality direction. At a
fixed strict feasible point, `c_lambda` is bounded above by
`-q_(A_lambda)(x0)-2 b_lambda·x0`. Its multiplier in the hyperplane inequality
is a square, so replacement preserves nonnegativity. A zero coefficient
pair is excluded before normalization, by strict negativity of the constant
and a nonzero supporting normal.

The compactness lemma then normalizes nonzero pairs in the actual closed
cone. A subsequence converges on its unit sphere; continuous evaluation and
the reciprocal-level limit make both perturbations vanish. The limit has
norm one and nonnegative quadratic values everywhere. The coefficient-cone
witness supplies nonnegative weights; the nonzero pair rules out zero
weights, and symmetry turns nonnegative quadratic values into matrix PSD.
The final proof therefore constructs a certificate directly, a valid
strengthening of the source's final contradiction argument.

Uniform cone separation is also proved as the separately frozen Lemma 3,
including the distance-to-set form. Its assumptions give closed cones and
nonnegative scaling, and the zero case is handled. Neither convexity nor a
nearest-point theorem is assumed.

## Integration requirement and limits

`ConeGeometry.lean` is not needed by the simplified headline proof. The
coordinator must therefore import and audit it separately in the topic's
verification suite; otherwise the suite would omit frozen claim Q07 even
though its source is present. This is an integration requirement, not a
mathematical defect in the headline.

The formal result does not establish that globally convex aggregations
describe the entire hull or recover every valid linear inequality. It gives
existence of at least one nontrivial globally convex aggregation exactly
when the hull is proper, under the stated hypotheses. Related documentation
and the developing paper must retain that distinction and keep claims about
the remaining corollaries separate from this verification package.
