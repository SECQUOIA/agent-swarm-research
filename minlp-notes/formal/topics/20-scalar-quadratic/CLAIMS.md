# Topic 20: scalar quadratic precision — frozen claims

Scope fixed on 2026-09-20 from the independent [source review](SOURCE-REVIEW.md).
Status: implementation in progress. The obligations below remain required until
proved and independently reviewed. Equivalent proof routes are allowed;
conditional interfaces do not discharge their own missing hypotheses.

| ID | Source statement and required conclusion |
|---|---|
| M1 | Arbitrary convex integer lifts produce at most `2^p` parity contact classes. Same parity makes the midpoint integer, including negative and unbounded integer coordinates. |
| M2 | Closing each contact inside the compact box preserves the midpoint error, supplies compact measurable sets, and preserves coverage. No measurability of the original contact or closedness of the lift is assumed. |
| M3 | Affine output changes and affine input restrictions preserve the represented-set and error assertions without adding integer coordinates. The binary-linear specializations retain finite affine descriptions. |
| S1 | For the square on `[0,1]`, every convex lift with `p` arbitrary integers has error at least `2^(-2p-2)`. The conclusion concerns every full-domain lift. An exact parity pigeonhole argument on a `2^p+1` grid is an equivalent proof; fixed numerical examples alone are insufficient. |
| S2 | An explicit binary linear square graph formulation has exactly `p` binary coordinates, `O(p+1)` continuous variables and rows, contains the graph, and admits only error at most `2^(-2p-2)`. The upper error is attained. Empty depth and the endpoint `x=1` are included. |
| S3 | For every `eps > 0`, both square count minima equal `max(0, ceil((log2(1/eps)-2)/2))`. This includes coarse accuracies and the exact threshold cases. |
| R1 | For symmetric nonsingular `M` of order `d > 0` and `delta >= 0`, compact `S` with `abs((s-t)^T M (s-t)/2) <= delta`, its volume is at most `2^d (3 sqrt(d) delta)^(d/2) / sqrt(abs(det M))`. The empty, lower-dimensional, and `delta=0` cases are covered. |
| R2 | A symmetric rank-`r` matrix has a nonsingular principal submatrix of order `r`. Fixing complementary coordinates in the original box creates an actual rank-dimensional slice with this Hessian and unchanged integer dimension. |
| R3 | For every nonsingular principal submatrix `H[I,I]` of order `r > 0`, every admissible convex `p`-integer graph lift satisfies `eps >= abs(det H[I,I])^(1/r) (product_i_in_I (u_i-l_i))^(2/r) / (48 sqrt(r)) * 2^(-2p/r)`. The displayed constant is part of the source claim. |
| R4 | Every real symmetric rank-`r` quadratic on the box admits a normalized representation `affine + sum_j c_j y_j^2`, with exactly `r` nonzero terms and affine `y_j` in `[0,1]`. The coordinate widths are positive. The decomposition must be obtained from the Hessian, not supplied as a new headline premise. |
| R5 | For `A=sum_j abs(c_j) > 0` and `L=max(0,ceil(log2(A/(4 eps))/2))`, an actual binary linear graph lift has error at most `eps`, uses `r L` binaries, and `O(n+r(L+1))` rows/variables. Dependent affine square coordinates do not obstruct graph containment. |
| R6 | Both graph minima equal `(r/2) log2(1/eps)+O_(H,B)(1)` as `eps` decreases to zero. Rank zero gives an exact affine graph with zero integers and binaries. Positive rank precludes finite exact graph lifts by R3. |
| I1 | The negative eigenspace of a Hessian with negative inertia `k > 0` contains an actual `k`-dimensional affine box inside the original domain. The restricted quadratic is strongly concave with some positive modulus. Neither the slice nor the curvature bound may be assumed at the original headline. |
| I2 | The same unrestricted-integer parity argument for epigraphs controls the downward chord-midpoint error on that negative slice. It gives the rate `(k/2) log2(1/eps)-O(1)` without any upper output bound. The note also states the explicit strong-curvature bound `eps >= (mu/2)(volume(D)/omega_k)^(2/k) 2^(-2p/k)`. |
| I3 | The dyadic folding interpolant `F_L(t)=t-sum_(j=1..L)4^(-j)G^[j](t)` satisfies `0 <= F_L(t)-t^2 <= 4^(-L)/4`. The relaxed continuous folding inequalities actually project to the stated lower epigraph boundary; this requires the optimization/dominance argument, not only feasibility of the exact folds. |
| I4 | An actual continuous linear square epigraph construction has error `2^(-2L-4)` and linear size in `L+1`, with zero binaries. The manuscript obtains this via depth `L+1` in I3. The note's enhanced depth-`L` construction is a different valid implementation with the same required bound. |
| I5 | The upper half of an explicit depth-`L` binary square construction contains the entire square hypograph and has overerror at most `2^(-2L-2)`. In particular, its output must not retain a lower bound that truncates the hypograph. |
| I6 | Combining positive continuous folding blocks (I3–I4) and negative I5 blocks gives a real binary linear epigraph lift with `k_- L` binaries, error at most `A 2^(-2L-2)`, and `O(n+(k_++k_-)(L+1))` rows/variables. Every exact epigraph point lifts and arbitrarily large outputs remain feasible. |
| I7 | Both epigraph minima are `(k_-/2) log2(1/eps)+O_(H,B)(1)` for `k_->0`. If `k_-=0`, both minima vanish for every positive tolerance, and the exact convex-lift minimum vanishes too. This does not assert an exact finite LP description of a curved convex epigraph. |
| I8 | Apply the proved sign/output transformation to obtain every hypograph conclusion with `k_+`. This includes output direction, the zero-inertia cases, and the compact linear upper formulations. |
| P1 | For `xy` on `[0,1]^2`, the exact best epigraph and hypograph errors with `p` arbitrary integers and convex constraints are both `2^(-2p-2)`. The lower bound follows on the actual slice `y=1-x`, not on an independently assumed univariate problem. |
| P2 | The matching product lift uses `u=(x+y)/2`, `v=(x-y+1)/2`, the identity `xy=u^2-v^2+v-1/4`, an exact convex positive-square epigraph and the binary square hypograph. It contains the full epigraph and attains the stated error at valid original inputs. The affine hypograph transformation preserves accuracy and integer dimension. |
| P3 | The exact product one-sided convex minima equal `max(0,ceil((log2(1/eps)-2)/2))` for `eps>0`. Purely linear lifts approach the same fixed-`p` error with arbitrarily small positive extra slack and no additional binaries. Exact finite-LP attainment at every threshold is not claimed. |
| Z1 | Every finite continuous linear extended formulation of the square epigraph with error `eps>0` and `M` inequalities satisfies `M >= (1/2)log2(1/eps)-1`. The source uses a projected polyhedral lower boundary and at most `2^M` exposed faces. An equivalent proof via attained minimum lifts and their active row patterns is allowed. Equalities and lineality must be allowed. I4 gives matching logarithmic order. |


All final bounds refer to actual finite-dimensional convex integer lifts or
actual finite binary linear systems. Their required laws, decompositions,
optimal lifts and finite descriptions must be constructed. The asymptotic
claims require a bounded additive error for all sufficiently small positive
accuracies, not just a subsequence or a ratio limit.

Topic 26 retains general vector covariance, noncommutative-rank and nonlinear
precision theory. Topic 20 does not claim novelty, priority, numerical solver
correctness, or rational spectral/optimization algorithms. Original inputs
range over nondegenerate boxes; affine, empty-dimensional, zero-rank and
zero-inertia cases remain included as stated above.
