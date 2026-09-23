# Independent audit of the approximate SDP lower bound

Date: 2026-09-04. Reviewer: independent `review_fbbt` agent, reassigned to this result.

The mathematical argument in `results/rank-one-approximate-sdp-lower-bound.md` passes this independent audit, including its revised parameterized bound, stronger stretched-exponential accuracy point, and vanishing-error family corollary. This review checked the primary lower-bound theorem and its quantitative hypotheses, rather than inferring robustness from the exact correlation-polytope lower bound. The final factor `A_m=m(184m+6)` matches the separately audited stability file. Novelty remains a separate question.

**Stronger final result.** The signed-correlation projection described in the final section below permits `epsilon<=1/(2A_m)=Theta(m^-2)` while retaining PSD order `exp(Omega((m/log m)^(2/13)))`. The reviewer derived this strengthening, and the result's author independently checked it before incorporating it. Earlier unsigned-correlation estimates below remain correct but give weaker consequences.

## Primary theorem and parameters

The primary source inspected was Lee, Raghavendra, and Steurer, [*Lower bounds on the size of semidefinite programming relaxations*](https://www.dsteurer.org/paper/sdpsize.pdf), particularly Theorems 3.1, 3.8, and 5.3. The full PDF was downloaded and its theorem statements read locally.

To avoid the source's reused dimension names, this review uses `m` for the correlation-polytope dimension and `k` for the number of coordinates in each restricted slack function. For odd `k>=3`, the source supplies a degree-`k` pseudo-density `D` with normalized expectation one, infinity norm at most `k^(3/2)`, and zero expectation against the centered square. Consequently its expectation against

`f_k(z) = [(sum z_i-k/2)^2-1/4]/k^2`

is `-1/(4k^2)`.

The quantitative PSD-rank inequality used in the draft is exactly the consequence displayed in source equation (3.11). It follows directly from the contrapositive of Theorem 3.1. Thus it needs only a degree-`d` pseudo-density with sufficiently negative expectation; it does **not** require identifying the shifted function's exact sum-of-squares degree. The opening part (3.10) of Theorem 3.8 mentions that additional degree equality, so explicitly identifying the quantitative consequence avoids a possible ambiguity in source scope.

## Affine slacks and the error metric

The draft uses the entrywise matrix l1 norm, meaning the sum of absolute values of all entries. Its dual coefficient norm is the maximum absolute entry. For a subset `S` of size `k`, the affine expression

`L_S(X) = k^-2 sum_(i,j in S) X_ij - k^-1 sum_(i in S) X_ii + (k^2-1)/(4k^2)`

has value `f_k(x_S)` at `X=xx^T`. Its diagonal coefficient is `(1-k)/k^2`, and its off-diagonal coefficient is `1/k^2`. Therefore its coefficient infinity norm is at most `1/k`, including when the perturbed matrices are nonsymmetric. There is no missing factor of two: the displayed sum and the norm both range over the full matrix entries.

For `COR(m) subset R subset COR(m)+eta U_1`, the slack `L_S+theta`, with `theta=eta/k`, is nonnegative throughout `R`. Its vertex-value matrix is exactly the restricted-function matrix for `f_k+theta`; no arbitrary perturbation of individual slack entries is introduced.

The condition actually needed is `eta<=1/(8k)`. It yields `theta<=1/(8k^2)`, so the pseudo-density expectation of the shifted function is at most `-1/(8k^2)`. Choosing the theorem parameter `delta=1/(16k^2)` satisfies its **strict** negative-expectation hypothesis. The shifted function is nonnegative and its maximum is below one quarter, hence its range is within `[0,1]`. Its ordinary uniform mean is at least `(k-1)/(4k^2)>=1/(6k)`.

## Factorization from a possibly nonregular SDP lift

The draft's factorization lemma is sound. Let a nonempty set have an exact PSD lift of order `q`, and consider affine functions nonnegative on its image. Compress the lift to the smallest face of the PSD cone containing its feasible matrices. This face is isomorphic to a PSD cone of order `r<=q`. A finite average of feasible matrices whose ranges span all feasible ranges is positive definite on that subspace. The compressed primal problem therefore satisfies Slater's condition.

For each valid affine slack, its infimum over the lift is finite: it is nonnegative, and evaluation at any feasible matrix supplies a finite upper bound. Primal strict feasibility gives an attained dual optimum and zero duality gap. On the affine constraint subspace, the slack is consequently

`<B_s,Y>+tau_s`, with `B_s` positive semidefinite and `tau_s>=0`.

Appending a scalar coordinate gives PSD factors `diag(B_s,tau_s)` and `diag(Y_t,1)` of order at most `q+1`. This argument does not presume a strictly feasible original lift, attainment of the primal infimum, bounded lift variables, or closedness of arbitrary PSD projections. It also handles affine output maps. The extra scalar coordinate must be retained unless an additional normalization argument removes it; the asymptotic lower bound absorbs it.

## Quantitative calculation

Substituting `d=k`, `delta=1/(16k^2)`, `||D||_infinity<=k^(3/2)`, and the mean bound into the primary theorem gives universal positive constants with

`q+1 >= c_2 k^(-23/4) [c_3 m/(k^(13/2) log m)]^(k/4)`.

The powers check independently:

- The denominator in the exponential base is `k * k^2 * k^(3/2) * k^2 = k^(13/2)`.
- The factor `(delta/||D||)^(3/2)` contributes `k^(-21/4)`.
- The square root of the mean contributes `k^(-1/2)`, giving `k^(-23/4)` in total.

Choose odd `k` comparable to `a(m/log m)^(2/13)`, where the universal constant `a>0` is sufficiently small. For all sufficiently large `m`, `3<=k<=m/2`, and the base is at least sixteen. The lower bound is then `c_2 k^(-23/4)2^k`, which is `exp(Omega(k))`. Both the polynomial prefactor and the additive one can be absorbed by lowering the absolute exponential constant and raising the minimum dimension. The logarithm retained in this argument is justified directly by the quantitative source theorem.

## Strengthenings identified during the audit

The draft initially imposed `eta<=1/(8m)`. This is sufficient but stronger than necessary. With the selected `k`, one may allow

`eta = Theta((log m/m)^(2/13))`

with a sufficiently small absolute constant. If the independent face transfer has amplification factor `A_m`, the corresponding rank-one-hull error is

`epsilon = Theta(A_m^-1 (log m/m)^(2/13))`.

For a verified `A_m=Theta(m^2)`, this becomes `Theta(m^(-28/13)(log m)^(2/13))`. This paragraph is conditional on that improved stability constant; it does not independently establish it.

The parameterized inequality also gives a useful family-level statement. If `eta_m -> 0`, choose odd integers `k_m -> infinity` with

`k_m <= min(1/(8eta_m), m^(1/13))`.

Then the exponential base is at least a positive constant times `m^(1/2)/log m`, and the bound is `m^(Omega(k_m))`. Thus every such family needs superpolynomial PSD order. Through `A_m=Theta(m^2)`, any error sequence `epsilon_m=o(m^-2)` would preclude a polynomial-size SDP family. At zero error the first bound on `k_m` is simply omitted.

## Scope and remaining dependency

The result concerns a uniform outer approximation in the explicitly defined entrywise l1 norm. An error bound in the entrywise maximum norm requires conversion and does not have the same numerical scale. The output lower bound is PSD matrix order, with multiple blocks counted by total order; scalar inequalities are cone factors too.

No error was found in the SDP/slack argument. The conversion from a close approximation to the rank-one hull into a close approximation to `COR(m)` depends on the separate quantitative face-stability theorem. The final files were checked for consistency: both use `A_m=m(184m+6)`, and the stability file records its own independent audit. This review does not duplicate that separate geometric proof audit.

## Stronger transfer using signed correlations

Define the signed-correlation polytope

`SCOR(m)=conv{yy^T : y in {-1,1}^m}`.

For a `2m` by `2m` matrix `W`, define the linear map

`Phi(W)_ij=m[W_ij-W_(i,m+j)-W_(m+i,j)+W_(m+i,m+j)]`.

On a face generator `W=(1/m)(x,1-x)(x,1-x)^T`, this gives

`Phi(W)=(2x-1)(2x-1)^T`.

Thus `Phi(F)=SCOR(m)`. The map need not be injective: complementary binary vectors have the same signed outer product. Injectivity is not required for transferring a lower bound through a linear image.

Every entry of the source matrix occurs with coefficient `m` or `-m` in exactly one target entry. Therefore

`||Phi(U)-Phi(V)||_1 <= m ||U-V||_1`.

This is the same entrywise-l1 operator bound as the old map extracting a principal block and multiplying by `m`. In particular, one should apply `Phi` **directly** to the rank-one face; mapping through the unsigned-correlation coordinates first would introduce an unnecessary norm loss.

The separately audited stability proof establishes, before taking any image, that every point `Z` in the sliced outer approximation has a point `V in F` with

`||Z-V||_1 <= (184m+6)epsilon`.

Applying `Phi` consequently produces a convex set `R` with a PSD lift of the same order and

`SCOR(m) subset R subset SCOR(m)+A_m epsilon U_1`,

where `A_m=m(184m+6)`.

For odd `k`, use the affine signed-correlation slack

`J_S(Y)=[sum_(i,j in S)Y_ij-1]/(4k^2)`.

At `Y=yy^T`, where `y=2x-1`, it equals exactly `f_k(x_S)`. Since an odd sum of signs has absolute value at least one, this slack is nonnegative on `SCOR(m)`. Crucially, its coefficient infinity norm is `1/(4k^2)`, with no diagonal coefficient of order `1/k`.

If `R` is within entrywise-l1 distance `eta` of `SCOR(m)`, then

`J_S+eta/(4k^2)`

is a nonnegative affine slack on `R`. For any fixed `eta<=1/2`, its value at the signed binary vertex indexed by `x` is `f_k(x_S)+theta`, with `theta<=1/(8k^2)`. All quantitative pseudo-density calculations above now hold for **every** permitted `k`, without an error-dependent upper bound on `k`.

The slack matrix is precisely the source matrix indexed by `x in {0,1}^m`. Although complementary `x` values give repeated signed vertices, their slack columns are identical, and listing the same point twice is allowed in the factorization lemma. Hence no source matrix is lost by passing to signed outer products.

Choosing `k` comparable to a sufficiently small constant times `(m/log m)^(2/13)` proves

`q >= exp(c(m/log m)^(2/13))`

for some universal `c>0`. The rank-one-hull hypothesis needed is now simply

`epsilon<=1/(2A_m)`.

The constants, strict negative-expectation gap, range of the shifted function, mean factor, facial-reduction argument, and matrix-order interpretation are unchanged. This strengthening replaces the previous vanishing-error restriction by an explicit fixed multiple of `m^-2`.
