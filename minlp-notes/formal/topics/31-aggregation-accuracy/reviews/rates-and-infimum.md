# Review of the accuracy constants, rates, and infimum

Reviewer: independent agent assigned the constants, rate consequences, and
final passage from family bounds to the optimal error. This review checks
mathematical meaning against the source and frozen claims; it does not
replace the package author's targeted Lean builds.

Status: pass. The constants, generic rate lemmas, and concrete final
interface in `Accuracy.lean` satisfy the mathematical obligations reviewed
here. A06 and A10 pass semantic review. Targeted machine verification is
recorded separately by the package author.

The reviewed files are `AccuracyConstants.lean`, `AccuracyRate.lean`,
`Accuracy.lean`, and the definitions and infimum lemmas in
`AccuracyModel.lean`. The comparison
sources are Sections 1–3 of
[the accuracy note](../../../../notes/research-20260922-aggregation-accuracy.md)
and obligations A02, A06, and A10 in [CLAIMS.md](../CLAIMS.md).

The advertised constants are preserved exactly:
`accuracyLowerBound N = sqrt(2)*(log 2)^2/(1600*N^2)` and
`accuracyUpperBound N = 5*sqrt(2)*pi^2/(16*(N-1)^2)`.
The denominators use real arithmetic after casting `N`. The upper-bound
comparison to `C/N^2` is guarded by `N>=2`, so its use of
`N^2<=4*(N-1)^2` and positive denominators is justified. The lower constant
is strictly positive for every positive `N`. The rational comparisons
bound the advertised lower constant from above; using a stronger rational
lower bound to imply the source lower bound therefore has the correct
direction.

`inverse_square_theta` states the actual mathlib `Theta` relation along
`atTop`. It requires both explicit bounds only for `N>=2` and uses their
positivity to pass correctly from absolute-value estimates to ordinary
inequalities. Both comparison constants are independent of dimension.
There is no claim at `N=0` or `N=1` concealed in the asymptotic statement.

For positive `epsilon`, `accuracyBudget epsilon` is
`ceil(sqrt((5*sqrt(2)*pi^2/16)/epsilon))+1`. The lemmas prove this is at
least two, its explicit upper-error bound is at most `epsilon`, and its
size is strictly less than that square root plus two. The necessary
budget lemma inverts the positive source lower bound to give
`sqrt((sqrt(2)*(log 2)^2/1600)/epsilon)<=N`. Its positivity assumptions
exclude division by zero. These explicit inequalities have the intended
`epsilon^(-1/2)` scale. The concrete
`exists_family_for_tolerance` theorem supplies that family using
`angleCuts (accuracyBudget epsilon)` and bounds its cardinality and actual
extended Hausdorff error. It does not infer a minimizer from an infimum
bound.

`hausdorffError` takes extended Euclidean Hausdorff distance, and
`optimalError` takes an `ENNReal` infimum over all finite families satisfying
source goodness and the at-most-`N` cardinality restriction. Invalid
families contribute no value to the inner infimum. The family upper-bound
lemma uses an actual admissible family; the lower-bound lemma applies the
bound to every admissible family. Neither lemma assumes that the infimum
is attained. The separate unbounded-relaxation theorem proves error is
infinite rather than passing prematurely to `toReal`, which would turn
infinity into zero.

The final `optimalError_bounds` theorem combines the universal lower
bound with the concrete angle-family upper bound in `ENNReal`, retaining
exactly the two source constants for every `r>=2` and `N>=2`.
`optimalError_ne_top` first proves finiteness from the finite upper bound.
Only then does `optimalError_toReal_bounds` transport the lower bound to
real numbers using that finiteness proof. Its upper conversion also
requires a nonnegative real bound. `optimalError_theta` specializes the
generic rate theorem to this correctly converted error. Possible special
values at `N=0` or `N=1` do not affect its eventual assertion.

`necessary_family_budget` applies to every admissible finite family of at
most a positive budget `N`, provided its actual Hausdorff error is at most
positive `epsilon`. It composes extended-error inequalities directly and
uses no real conversion or attainment assumption. The restriction `N>=1`
is explicit; the universal bound still includes empty families through
`W.card<=N`. Together with the constructive sufficient-budget theorem
and `accuracyBudget_size`, this proves the claimed necessary and
sufficient small-tolerance scale. None of these constants depends on
`r`. The result concerns uniform approximation by one common cut family,
not a prescribed objective, cut-generation iterations, or computational
runtime.

No substantive defect or missing hypothesis was found in this review.
The companion reviews cover the full geometric upper and lower bounds,
the exact hull transport, and the rational construction. No build,
project-wide verification, CI inspection, or numerical check was run by
this reviewer.
