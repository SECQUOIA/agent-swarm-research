# Source inventory for finite aggregation accuracy

The authorized source is Sections 1–3 of
[the reviewed accuracy note](../../../notes/research-20260922-aggregation-accuracy.md),
including its exact rational construction and its stated rate and
accuracy-count interpretation. The user explicitly selected the earlier
two-package recommendation: exact hull/SDP, then accuracy bounds. Topic 30
has completed the hull dependencies; no different research topic is part
of this continuation.

The source fixes the actual closed hull, arbitrary finite good cut families,
and Euclidean distance in all `2r` original variables. Its infimum over
families does not assert attainment. Extended Hausdorff distance handles
unbounded relaxations. The implementation must preserve these definitions
when transporting from the existing raw pair-vector representation, whose
default norm is not the desired Euclidean norm. Compactness, nonemptiness,
and inclusion of the true hull are part of the distance argument.

The advertised bound for every `N≥2` is

`sqrt(2)*(log 2)^2/(1600*N²) ≤ e_N ≤ 5*sqrt(2)*pi²/(16*(N-1)²)`.

Both constants are independent of `r≥2`. The lower bound allows arbitrary
interior or extreme cone multipliers, positive rescaling, zero coordinates,
and unrestricted ratios. It cannot be replaced by a theorem about one
particular mesh, only boundary rays, or bounded cut ratios. The source
constructs perturbed Gram witnesses in dimension two and embeds them in
larger dimensions; another proved construction is acceptable if it yields
the complete lower bound with at least the stated constant.

For the upper bound the angle interval includes both coordinate endpoints.
Their cuts bound the two unit balls. The source obtains a uniform angular
defect from a second-derivative bound and repairs every relaxed point by
radial contraction. Its two-by-two matrix is tested only on nonnegative
directions and need not be PSD. The Euclidean radius is `sqrt(2)`, which is
essential to the stated constants. Any equivalent proof must cover the
whole relaxation, not just a finite test set.

The rational family uses two integer parameter branches and identifies the
shared midpoint at `j=m`. Therefore the number of distinct cuts is exactly
`2*m+1`, including both endpoints. Its coefficients are exact nonnegative
integers at most `2*m²`; the rank-one cone identity holds exactly. The
source error bound is `5*sqrt(2)/(4*m²)`. For
`m=floor((N-1)/2)` and `N≥3`, the cut budget is at most `N` and both the
quadratic error rate and logarithmic binary coefficient-size bound must be
derived. No floating-point rounding or numerical solution claim is involved.

The `Theta(N^-2)` interpretation follows from the exact sandwich and a
uniform comparison between `N` and `N-1`. Its equivalent small-error cut
count requires care: lower bounds apply to every family, while upper bounds
must exhibit a family rather than assume the infimum is attained. Explicit
quantified inequalities are sufficient formal rate statements; notation
alone is not a substitute for those conclusions.

Section 4's support-function statement and single-objective proposition
are excluded because they were not part of the recommended quantitative
package. Their discussion explains why a uniform approximation lower bound
does not imply a prescribed-objective cut-iteration lower bound. The
package must retain this limitation without claiming to have verified the
separate proposition. Literature priority and numerical solver benefits
are likewise outside the frozen scope.
