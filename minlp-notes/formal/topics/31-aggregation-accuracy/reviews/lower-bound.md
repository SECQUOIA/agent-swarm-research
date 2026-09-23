# Independent lower-bound review

Status: approved for mathematical content and source correspondence.

Scope: frozen obligation A05 and the lower-bound argument of Sections 1–3
of `notes/research-20260922-aggregation-accuracy.md`, including the lower
half of the A06 infimum conclusion. This is a semantic review. Build,
axiom-audit, and kernel results belong to the package verification record;
this reviewer has not run duplicate builds or project-wide checks.

Reviewed `AccuracyLowerPigeonhole.lean`, `AccuracyLowerGap.lean`,
`AccuracyLowerLipschitz.lean`, and `AccuracyLower.lean`, plus the relevant
lower constants in `AccuracyConstants.lean`. Also inspected the reused
actual good-multiplier classification, Gram realization, perturbed Gram
estimates, and the Euclidean distance and Hausdorff-witness interfaces in
`AccuracyModel.lean`.

The finite-grid argument is a valid replacement for the source's logarithmic
interval covering. There are `N+1` parameters in `[1,2]` with pairwise spacing
at least `1/N`. For perturbation `eta=1/(400*N²)`, the algebraic gap estimate
shows that each selected good aggregate excludes at most one parameter.
The pigeonhole lemma consequently leaves a parameter that satisfies every
selected weak inequality.

The gap estimate assumes only coordinate nonnegativity and
`c²≤4*a*b`. It therefore applies to interior and boundary multipliers,
without normalizing coefficients or bounding their ratios. A positive
violation forces `c>0`; cuts with `c=0`, including either coordinate ray,
cannot exclude a parameter. Positive rescaling preserves the argument.
The counting lemma uses the original finite family and its cardinality;
there is no requirement that cuts have distinct rays. The assembly obtains
these cone hypotheses from the original source `Good` predicate through
`good_iff_goodCone` for every `r≥2`.

`accuracy_lower_witness` realizes the surviving parameter's perturbed Gram
matrix as actual vectors in the original dimension, using the first two
coordinate vectors in `gram_realization`. This explicitly covers `r=2`
and embeds the same construction in every larger dimension. Positive first
diagonal and determinant are proved from the parameter and perturbation
bounds, not assumed. The residual identity establishes membership in the
actual selected weak relaxation.

The witness and every hull point lie in the product of the two unit balls.
The valid multiplier `(tau,1/tau,2)` evaluates to `2*eta` at the witness
and is nonpositive at every point of the actual closed hull. The latter
uses the established equality of `closedRegion` and the closure of the
ordinary convex hull of the strict feasible set.

The Lipschitz estimate uses quadratic norms of both component differences
bounded by `D²`. In the assembly, `D` is the full Euclidean distance in all
`2r` coordinates. Both component inequalities follow from its proved
squared-distance identity and nonnegativity of the other component norm.
The Lipschitz constant is 10 and is independent of the dimension. The older
raw product/Pi norm does not replace Euclidean distance.

It follows that every hull point is at distance at least
`eta/5=1/(2000*N²)` from the admitted witness. The extended Hausdorff
interface converts this directly to a family lower bound. No boundedness,
compactness, or finite-Hausdorff-distance hypothesis is imposed on the
relaxation, so unbounded families are included. The result also covers the
empty family and all families with fewer than the allowed number of cuts.

The exact source expression is retained by `accuracyLowerBound`:
`sqrt(2)*(log 2)²/(1600*N²)`. The comparison theorem uses established
analytic bounds for `log 2` to prove `(log 2)²<1/2`, together with
`sqrt(2)≤3/2`. These give the advertised constant no larger than the proved
rational lower constant. This comparison assumes only `N>0`; the final
family theorem works for `N≥1` and therefore specializes to every required
`N≥2`.

`accuracy_lower_le_hausdorffError` quantifies over every finite family with
the original goodness predicate and cardinality at most `N`.
`accuracy_lower_le_optimalError` then applies the universal lower bound to
every term of the extended-real infimum. It neither selects an optimal
family nor assumes that the infimum is attained.

No mathematical defect, omitted boundary case, extra family restriction,
or unresolved source-fidelity issue was found. This approval does not
replace the package's separate compiler, axiom, and kernel checks.
