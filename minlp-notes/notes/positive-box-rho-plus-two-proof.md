# Coefficient proof of the positive-box bound rho plus two

Date: 2026-09-04. Status: the finite-comparison proof passed fresh independent
agent review by `review_extension`; 1,589 independent exact coefficient and induction
checks also passed. See [the first audit](review-positive-box-rho-plus-two.md)
and [the second audit](review-positive-box-rho-plus-two-second.md). This is not
external peer review. This improves the earlier coarse positive-box
bounds. The coefficient reduction was proposed by the multilinear author; the
minimum/maximum spreading induction below establishes it.

## The coefficient statement

Fix `u∈[0,1]^n`. For every integer `j≥0`, let `C_j`, `P_j`, and `O_j` be the
expectations of `binom(K,j)` under common-threshold rounding, independent Bernoulli
rounding, and fair endpoint-orientation rounding, respectively. The last law uses
one uniform variable, with an independent fair choice between the success intervals
`[0,u_i]` and `[1−u_i,1]` for each coordinate. Let `S=Σu_i`, `k=floor S`, and
`θ=S−k`, and set

\[
V_j=(1-\theta)\binom kj+\theta\binom{k+1}j.
\]

Moments of order zero equal one; moments above dimension equal zero. Set moments
of negative order equal zero. Define

\[
F_{n,j}=2C_j+V_j-P_j-2O_j+C_{j-1}-P_{j-1}.
\tag{1}
\]

**Claim:** `F_{n,j}≥0` for every `n,j,u`.

The adjacent-count distribution defining `V_j` can always be realized with the
individual means `u`: the cube slab `floor S≤ΣY_i≤ceil S` is integral and contains
`u`. Also, `binom(K,j)` is discretely convex for `j≥2`. Thus `V_j` is the minimum
expectation of the elementary symmetric polynomial of degree `j` at these means.

## Base moment orders

Directly, `F_{n,0}=F_{n,1}=0`. For `j=n+1`, the expression is `C_n−P_n≥0`;
common-threshold rounding maximizes the product, while independent rounding is
feasible. Orders greater than `n+1` vanish.

For `j=2`, write

\[
L_2=\sum_{a<b}\max(0,u_a+u_b-1).
\]

Each pair has equal endpoint orientations with probability one-half and opposite
orientations with probability one-half. Its orientation expectation is therefore
one-half its upper Frechet value plus one-half its lower Frechet value. Summing,

\[
2O_2=C_2+L_2.
\]

Consequently

\[
F_{n,2}=(C_2-P_2)+(V_2-L_2)\ge0.
\tag{2}
\]

The first term is nonnegative by maximality of common-threshold rounding; the
second is nonnegative because every feasible law, including the adjacent-count
law, must respect each pair's lower Frechet bound.

## Spreading the minimum and maximum

We prove the remaining orders by induction on `n`. A coordinate with mean zero
is deterministic under every law, and deleting it gives

\[
F_{n,j}(u,0)=F_{n-1,j}(u).
\tag{3}
\]

A coordinate with mean one is also deterministic. Pascal's identity, including for
the adjacent-count moment after its mean shifts by one, gives

\[
F_{n,j}(u,1)=F_{n-1,j}(u)+F_{n-1,j-1}(u).
\tag{4}
\]

Thus all boundary points follow from lower dimension. Dimension one is immediate.

Now suppose all coordinates are strictly between zero and one and `3≤j≤n`.
Choose distinct coordinates whose means are a minimum `x` and a maximum `y`.
Move them to `x−s,y+s`, leaving all other coordinates fixed, until one reaches zero
or one. The sum of means remains fixed, so `V_j` is constant along this path.
For positive `s` before its endpoint, these two coordinates are the unique minimum
and maximum, even if there were ties initially.

The common-threshold moment satisfies

\[
C_j(u)=\sum_{i=1}^n u_{(i)}\binom{n-i}{j-1},
\qquad u_{(1)}\le\cdots\le u_{(n)}.
\]

For any step `h` with `0≤h≤min(x,1−y)`, decreasing the minimum to `x−h` and
increasing the maximum to `y+h` therefore changes `2C_j+C_{j-1}` by exactly

\[
-2h\binom{n-1}{j-1}-h\binom{n-1}{j-2}.
\tag{5}
\]

This also holds with ties: the chosen minimum can be placed first and the chosen
maximum last in their tied groups before the move. Since `j≥3`, both relevant
moments assign coefficient zero to that last coordinate.

Write `E_r` for the elementary symmetric polynomial of degree `r` in the other
`n−2` means. The sum of the moved coordinates is unchanged, while their product
changes from `xy` to `xy−h(y−x+h)`. Hence the exact change in `−P_j−P_{j-1}` is

\[
h(y-x+h)(E_{j-2}+E_{j-3})
\le h\binom{n-1}{j-2}.
\tag{6}
\]

The estimate uses `0≤y−x+h≤1`, `E_r≤binom(n−2,r)`, and Pascal's identity.

The orientation moment is coordinatewise nondecreasing, with coordinate Lipschitz
constant `binom(n−1,j−1)`. Indeed, couple two versions using the same uniform
variable and orientation coins. Increasing one mean by `h` only changes its binary
coordinate from zero to one, with probability exactly `h`. On that event,
`binom(K,j)` increases by `binom(K_rest,j−1)`, between zero and
`binom(n−1,j−1)`.

Perform the move in two steps: first decrease the minimum, then increase the
maximum. The first step reduces `O_j` by at most `h binom(n−1,j−1)`; the second
cannot reduce it. Therefore the full change in `−2O_j` is at most
`2h binom(n−1,j−1)`. Adding this bound to (5) and (6) proves directly

\[
F_{n,j}(u\text{ after the move})\le F_{n,j}(u).
\]

Take `h=min(x,1−y)`, reaching a boundary point. Its coefficient is nonnegative by
(3), (4), and the induction hypothesis, so the initial coefficient is nonnegative.
This proves the claim in all dimensions and orders.

The finite comparison above incorporates an independent review correction to an
earlier derivative presentation. Coordinate partial derivatives need not exist on
a prescribed path that remains on an orientation breakpoint. The finite coupling
argument avoids that problem and covers every such path without regularity assumptions.

## Converting the coefficients into a physical-box inequality

Fix `rho>1`, put `t=rho−1`, and consider one physical product on `[1,rho]^n`.
At a binary vertex its value is `(1+t)^K`. Thus its common-threshold, independent,
and orientation expectations are the polynomials

\[
C(t)=\sum_j C_jt^j,\qquad
P(t)=\sum_j P_jt^j,\qquad
O(t)=\sum_j O_jt^j.
\]

Its exact convex envelope is `V(t)=Σ_j V_jt^j`, because the adjacent-count law
minimizes `(1+t)^K` and is feasible with all prescribed coordinate means.
The coefficient of `t^j` in

\[
(\rho+1)C+V-\rho P-2O
=(2+t)C+V-(1+t)P-2O
\]

is exactly `F_{n,j}`. All coefficients are nonnegative and `t>0`, so

\[
C-V\le\rho(C-P)+2(C-O).
\tag{7}
\]

One common mixture of independent rounding with probability `rho/(rho+2)` and
orientation rounding with probability `2/(rho+2)` therefore captures at least
`1/(rho+2)` of every physical monomial's true gap. Summing with positive coefficients
proves the universal polynomial bound

\[
\operatorname{tbtgap}_{[1,\rho]^n}f
\le(\rho+2)\operatorname{chgap}_{[1,\rho]^n}f.
\tag{8}
\]

In particular, the constant on `[1,2]^n` is four.

The previously proved positive affine expansion transfers this to any strictly
positive box with coordinate aspect ratios at most `rho`. Degenerate coordinates
can be removed. This is not an argument by box inclusion: each original monomial
becomes a positive polynomial in physical `[1,rho]` variables, its exact gap is at
most the sum of the expanded monomial gaps, and the full hull gap is affine invariant.

## A failed stronger monotonicity statement

The proof requires spreading the global minimum and maximum. Arbitrary
mean-preserving spreading does not work: the coefficient is not Schur-concave.
For `n=4,j=3`, exact rational evaluation gives

\[
F_{4,3}(2/5,7/10,24/25,97/100)=\frac{6201}{12500},
\]
\[
F_{4,3}(2/5,7/10,959/1000,971/1000)=\frac{4961031}{10000000}.
\]

Moving `1/1000` from the third coordinate to the fourth therefore increases the
coefficient by `231/10000000`. This refutes the stronger Schur-concavity claim,
while leaving the minimum/maximum argument intact.

Independent skewed numerical coefficient searches over 7,000 vectors in dimensions
3 through 35 found no negative coefficient. Subsequent minimum/maximum derivative
checks motivated the proof above. These searches are not premises of the proof.

## A coefficient-regularity corollary for cardinality potentials

The proved coefficient inequality also controls a broader class of terms. Let

\[
\psi(K)=\sum_{j=0}^d a_j\binom Kj,\qquad a_j\ge0,
\]

and suppose `a_(j+1)≤L a_j` for every `j≥2`, taking coefficients past the degree
as zero. The corresponding multilinear extension is `Σa_j E_j(u)`. This is not the literal
function `ψ(Σu_i)` evaluated on continuous points. Its convex
and concave envelopes are simultaneously attained by the adjacent-count and common
threshold laws, respectively, because every nonnegative binomial component has
those extrema. Multiplying the coefficient inequality

\[
P_j-V_j\le2(C_j-O_j)+(C_{j-1}-P_{j-1})
\]

by `a_j` and summing gives

\[
P_\psi-V_\psi
\le2D_{O,\psi}+\sum_{j\ge2}a_{j+1}D_{I,j}
\le2D_{O,\psi}+L D_{I,\psi}.
\]

All independent deficiencies `D_(I,j)` are nonnegative; orders zero and one vanish.
Therefore

\[
C_\psi-V_\psi\le(L+1)D_{I,\psi}+2D_{O,\psi}.
\]

A common mixture consequently gives factor `L+3` for sums of such cardinality
potentials, when each potential is treated as one term and the bound `L` applies to
all of them. This concerns the gaps of these entire potentials, not a termwise
relaxation of their elementary-symmetric expansions. The physical product
`rho^K` has `a_j=(rho−1)^j` and `L=rho−1`, recovering the positive-box theorem.

This corollary is a mathematical consequence of the coefficient theorem, with no
independent novelty claim. It may be useful for process models whose local costs
have positive, geometrically controlled discrete derivatives.

## Independent audit of fixed-mixture optimality

The multilinear author proposed two limiting obstructions to improving the constant
using a fixed mixture of independent rounding `I` and endpoint orientation `O`.
The following calculations were independently checked and prove that claim within
its stated scope. This is not a sharpness proof for the true worst polynomial gap.

Fix `rho>1` and write `alpha=1/rho`, `eta=1−alpha`, and
`beta=(1+alpha)/2`. For the bilinear means `(epsilon,1−epsilon)`, with
`0<epsilon<1/2`, direct expansion gives

\[
D_I/T=\epsilon,\qquad D_O/T=1/2.
\]

Thus a mixture with orientation weight `w` cannot guarantee a uniform captured
fraction above `w/2`.

For the second obstruction, use one mean `epsilon` and `k` means
`1−epsilon/k`, with integer `k≥1` and `0<epsilon<1/2`. The total mean is exactly
`k`. Divide all physical product values by `rho^(k+1)`. Exact formulas are

\[
V=\alpha,
\qquad C=\alpha+\epsilon\left[\eta-
 \frac{\alpha(1-\alpha^k)}k\right],
\]
\[
P=\alpha[1+(\rho-1)\epsilon]
       [1-\eta\epsilon/k]^k,
\]
\[
O=\alpha+\epsilon\left[\eta-
 \frac{2\beta(1-\beta^k)}k\right].
\]

The common-threshold and orientation expectations follow by splitting their
uniform-variable intervals at `epsilon/k` and `epsilon`; the independent product
is immediate. For each fixed `k`, as `epsilon→0`,

\[
\frac{T}{\epsilon}
=\eta-\frac{\alpha(1-\alpha^k)}k,
\]
\[
\frac{D_I}{\epsilon}\longrightarrow
\alpha\eta-\frac{\alpha(1-\alpha^k)}k,
\qquad
\frac{D_O}{\epsilon}
=\frac{2\beta(1-\beta^k)-\alpha(1-\alpha^k)}k.
\]

The denominator coefficient is at least `eta²>0`, since
`1−alpha^k≤k eta`. Taking `epsilon→0` first and then `k→∞` therefore gives

\[
D_I/T\longrightarrow1/\rho,\qquad D_O/T\longrightarrow0.
\]

The same fixed mixture consequently cannot guarantee a uniform captured fraction
above `(1−w)/rho`. Combining the two valid obstructions gives

\[
\inf_{\text{physical monomials and means}}D_{\rm mixture}/T
\le\min\{w/2,(1-w)/\rho\}.
\]

Its maximum over `w∈[0,1]` is exactly `1/(rho+2)`, at `w=2/(rho+2)`.
The coefficient theorem provides the matching guarantee at that weight. Thus the
constant is optimal among fixed mixtures of these two distributions when one
requires a uniform per-monomial guarantee over all dimensions. Neither obstruction
establishes a matching lower bound for the true polynomial hull-gap ratio.
Coefficient-dependent mixtures, other rounding laws, and arguments using several
terms together are outside this optimality statement.

## Balanced orientations: verification completed at shutdown

The finite-dimensional refinement proposed during this investigation is now
proved and independently reviewed in the [closing proposition and audit](review-positive-box-balanced-orientation-closure.md).
For an ambient dimension `N>=2`, choose a uniform orientation subset of size
`floor(N/2)` once and restrict that same law to each monomial support. Its pairwise
opposite-orientation probability is

```
p_N=2 floor(N/2) ceil(N/2)/[N(N-1)].
```

The coefficient induction with `beta_N=1/p_N` gives
`tbtgap <= (rho+beta_N) chgap`, including unequal strictly positive boxes.
Here `beta_N=2-2/N` for even N and `2-2/(N+1)` for odd N. The restriction issue
is resolved by retaining the ambient law throughout induction; deleting a
coordinate never resamples or conditions its orientation coins. The closing
note includes the pair base case, all boundary identities, finite spread
comparison, and positive affine transfer. This does not establish the exact
finite-dimensional optimum and carries no separate novelty claim.
