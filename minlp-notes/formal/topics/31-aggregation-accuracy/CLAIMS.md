# Topic 31 frozen claims

Status: complete. All ten obligations have proved declarations and
independent semantic review. These obligations were fixed from the
[source inventory](SOURCE-REVIEW.md), independently of proof convenience.

For every integer `r≥2`, let `C` be the closure of the ordinary convex hull
of the original strict three-inequality system. For a finite family `F`
of source-good nonzero multipliers, let
`P_F={x : ∀lambda∈F, aggregate(lambda,x)≤0}`. Use the Euclidean norm on
the full original variable space `R^(2r)` and its extended Hausdorff
distance `d_H`. Define `e_N=inf_{|F|≤N} d_H(C,P_F)`, without assuming
the infimum is attained. Write
`c=sqrt(2)*(log 2)^2/1600` and `B=5*sqrt(2)*pi^2/16`.

| ID | Required conclusion |
|---|---|
| A01 | Define finite weak aggregation relaxations and their actual Euclidean metric model. Prove agreement with the existing pair-vector residuals and source-good predicate. Establish the finite-dimensional Euclidean norm identity `||x||²=u·u+v·v` and any transport used for the actual closed hull. In particular a raw Pi/product supremum norm may not silently replace Euclidean distance. |
| A02 | Define extended Hausdorff error and `e_N` as the infimum over arbitrary finite source-good families of at most `N` cuts. Prove the target is nonempty and compact and is contained in every such relaxation. Unbounded relaxations must have infinite error, and the infimum must not require an optimal family. Duplicate cuts or arbitrary positive rescalings may not invalidate the quantification or improve the counted budget. |
| A03 | Prove the angle multipliers `(cos²(theta),sin²(theta),2*sin(theta)*cos(theta))` are source-good for `theta∈[0,pi/2]`, including both coordinate endpoints. Prove the actual closed hull equals the intersection of all their weak inequalities. The tested two-by-two matrix need only be nonnegative on nonnegative directions; do not incorrectly require it to be PSD. |
| A04 | For every `N≥2`, construct a family of at most `N` angle cuts including both endpoints and prove `d_H(C,P_F)≤B/(N-1)^2`. The bound must cover every point of the entire relaxation. Establish the Euclidean distance estimate through radial repair or an equivalent complete argument, rather than checking only sampled witnesses. |
| A05 | For every `N≥2` and every family of at most `N` arbitrary source-good cuts, prove `c/N²≤d_H(C,P_F)`, including unbounded relaxations. The proof must cover interior multipliers, zero-coordinate boundary multipliers, unbounded multiplier ratios, positive rescaling, and actual witnesses in every `r≥2`, including `r=2`. Any replacement for the source covering argument must imply the stated constant without adding a family restriction. |
| A06 | Prove the exact advertised sandwich `c/N²≤e_N≤B/(N-1)^2` for every `N≥2`, with constants independent of `r≥2`. Pass correctly from family bounds to the infimum in the extended real setting; do not assume optimal attainment. |
| A07 | For every `m≥1`, construct the exact rational/integer rays `(m²,j²,2*m*j)` and `(j²,m²,2*m*j)` for `0≤j≤m`. Prove source-goodness, exactly `2*m+1` distinct cuts (or positive rays, with the corresponding implemented family count), inclusion of both coordinate rays, and each coefficient a nonnegative integer at most `2*m²`. For `N≥3` and `m=floor((N-1)/2)`, prove `2*m+1≤N`. |
| A08 | Prove the rational family from A07 has actual Euclidean Hausdorff error at most `5*sqrt(2)/(4*m²)` for every `m≥1` and `r≥2`. Derive the angular coverage or an equivalent uniform approximation estimate for the exact coefficients. Independently rounding three real coefficients or assuming a mesh gap is insufficient. |
| A09 | Establish an explicit binary coefficient-size bound for the exact rational family that implies `O(log N)` bits per coefficient, together with its `O(N^-2)` Hausdorff error for `N≥3`. Include zero coefficients in the chosen bit convention. An asserted informal bit bound unsupported by a proved integer size bound and its logarithmic consequence is insufficient. |
| A10 | State and prove the quantitative rate and accuracy-count consequences: positive uniform constants bounding `e_N` above and below by constant multiples of `N^-2`, and corresponding necessary and sufficient `Theta(epsilon^-1/2)` cut budgets as `epsilon` tends to zero. Explicit two-sided inequalities with all quantifiers, positivity, and dimension independence suffice; a library asymptotic-notation theorem is optional. Sufficiency must provide an actual family and may not infer attainment from an infimum bound. |

Section 4's support-function equality and exact single-objective aggregation
proposition are excluded. So are arbitrary-quadratic approximation,
nonlinear objectives, Boolean descriptions, lifted approximation lower
bounds, numerical conditioning, solver performance, and runtime or
iteration lower bounds. No novelty or priority claim is formalized.
