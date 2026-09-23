# Independent audit: forest-Laplacian quadratic precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the forest-Laplacian precision candidate](forest-laplacian-quadratic-precision.md). The exact incidence-domain volume, affine-fiber quotient, trace allocation bounds, and polynomial rational construction establish the stated `p_out<=p_conv+6r+1` guarantee. No correction was needed.

## Incidence quotient and nonlinear rank

With oriented incidence matrix `B`, every edge coordinate `z=Bx` belongs to `[-1,1]`. Normalization `u=(z+1)/2` maps the domain into the unit `r`-cube. The quadratic output becomes `g_j(u)=.5 sum_e a_je(2u_e-1)^2`, whose Hessian diagonal is exactly `C_je=4a_je`. Its new affine terms are represented exactly by the diagonal quadratic construction.

Subtracting the original affine output, restricting to the original cube, and projecting through the incidence map preserves approximation errors and maps the exact graph onto the reduced graph. Reintroducing the original continuous variables and affine equations gives the reverse reduction. This proves equality of both formulation minima even when the affine output varies along incidence fibers. No integer variable is added in either direction, and all maps are rational for rational data.

After deleting edges absent from every output, the common Hessian kernel is exactly `ker B`. Indeed, positive weighted quadratic forms can vanish simultaneously only if every active edge difference vanishes; conversely such a vector belongs to every Hessian kernel. The kernel consists of vectors constant on each forest component. Therefore the common nonlinear input rank is `n-number_of_components=r`. Isolated vertices contribute only affine fibers and cause no exception.

## Exact volume by face tiling

For one connected tree, subtracting the minimum coordinate from any cube point leaves its incidence image unchanged and keeps the point in the cube. The resulting representative has minimum zero. It is unique: equal incidence images differ by a constant vector, and two zero minima force that constant to be zero.

Thus the incidence image is the union of the images of all coordinate faces `x_v=0`. Restriction to one face is an invertible linear map with matrix obtained by deleting column `v`. Its determinant has absolute value one. The leaf-elimination proof is valid: a tree with at least two vertices has a leaf different from the omitted vertex; expanding its column removes that leaf and its incident row, leaving the smaller tree minor. The base case is immediate.

Every face image consequently has volume one. If two distinct face images overlap, their unique minimum-zero representative has at least two zero coordinates. The set of such representatives has dimension at most `s-2`, so its linear image has zero volume in dimension `s-1`. There are finitely many such intersections. Additivity of volume therefore gives tree-image volume exactly `s`.

Different components use disjoint input and edge coordinates, so the forest image is their Cartesian product. A singleton component contributes zero dimension and volume factor one. Normalization by one half in each of the `r` image coordinates gives precisely `V_F=2^(-r) product_c n_c`. In particular `V_F>=2^(-r)`. The domain is full-dimensional, compact, and convex, as required by the subsequent support argument.

## Lower and upper precision bounds

The reduced midpoint discrepancy is the nonnegative Jensen vector `J_j=(1/8)sum_e C_je Delta u_e^2`. Its expectation on a compact parity support is `C diag(Sigma)/4`. Since `K` is closed and convex, the expectation belongs to it. Hence `p_e=Sigma_ee/4` is a feasible allocation, with the cap following from the unit-cube variance bound. Hadamard's inequality yields the stated support-volume bound `2^(A_r) sqrt(D)`.

The supports cover the actual correlated domain of volume `V_F`, giving `p_conv>=Phi-A_r+log2 V_F`. The sign of the volume term is correct: a smaller domain weakens the lower bound. The argument does not assume that incidence coordinates are independent or that their domain is the full cube. Closure of parity supports preserves the continuous Jensen condition, as in the previously audited base proof.

For the upper construction, use the diagonal square grid on the containing unit cube and then impose the exact incidence-domain lift. Its errors satisfy `|e|<=Cp/8`; unconditionality of `K` makes them valid simultaneously. Domain restriction removes no exact graph point. The binary count is at most `Phi+r` for an optimal allocation. The reviewed rational allocation oracle gives product at least `exp(-1)D`, adding at most `1/(2ln2)` to this real-valued count bound.

Combining the finite lower and constructive upper bounds gives the first inequality in (2). Using `A_r<4r`, `-log2 V_F<=r`, and `1/(2ln2)<1` gives `p_out<=p_conv+6r+1`. The component-sensitive bound is valid and can be sharper. The resulting coefficient sizes and row counts are polynomial because the only new domain equations use the rational incidence matrix, while the scalar allocation and prefix constructions were already verified in the full bit model.

## Checks and boundaries

I ran `code/quadratic_rank/check_forest_laplacian_precision.py`. All 36 exact forest cases, 216 incidence-minor checks, and 288 quotient/Jensen/canonical-representative checks passed. The tiling argument above proves the volume identity in all dimensions; the finite checks support its algebraic ingredients.

The result is not restricted to small original Hessian blocks: a large connected tree has full tree rank, and distinct weighted Laplacians on it need not commute. The forest structure instead provides independent edge coordinates and a normalized domain losing at most a linear number of volume bits. The candidate correctly avoids extending the diagonal argument to cyclic graphs or arbitrary linear changes of input coordinates without a separate domain analysis. Novelty assessment remains separate from this correctness audit.
