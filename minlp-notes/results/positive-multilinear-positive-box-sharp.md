# Positive-box gap bound: aspect ratio plus two

Date: 2026-09-04. Status: complete proof and canonical text passed two fresh independent audits: `notes/review-positive-box-rho-plus-two.md` and `notes/review-positive-box-rho-plus-two-second.md`. The lower construction has a separate independent audit. This replaces the earlier asymmetric estimate, preserved in `notes/positive-box-asymmetric-upper-predecessor.md`.

## Main result

Let `f` be a multilinear polynomial with positive coefficients on a box `B=∏[ℓ_i,r_i]`, where `0<ℓ_i≤r_i`, and let `ρ>1` bound every ratio `r_i/ℓ_i`. Fixed coordinates are allowed. At every evaluation point in `B`,

\[
\operatorname{tbtgap}_B f\le(\rho+2)\operatorname{chgap}_B f.
\]

Here `tbtgap` is the sum of the exact concave-minus-convex envelope gaps of the individual monomials, including their coefficients; `chgap` is the concave-minus-convex envelope gap of the entire polynomial. Dimension, degree, number of terms, coefficients, and evaluation points are unrestricted. Constant and affine terms have zero gap.

Let `C_box(ρ)` be the supremum of this ratio over such positive boxes, polynomials, and points with positive hull gap. Together with the independently audited [lower construction](positive-multilinear-positive-box-lower.md), the theorem gives

\[
\boxed{\max\{2,\rho\}\le C_{\rm box}(\rho)\le\rho+2.}
\]

Consequently `C_box(ρ)=ρ+O(1)` as `ρ→∞`. On `[1,2]^n`, the upper bound is four. The exact finite-aspect-ratio optimum remains undetermined.

The upper proof supplies a common rounding law: use independent endpoint rounding with probability `ρ/(ρ+2)` and fair endpoint-orientation rounding with probability `2/(ρ+2)`. This law depends only on the normalized evaluation point and `ρ`; it captures at least `1/(ρ+2)` of every individual monomial's gap simultaneously.

## Envelope facts and attribution

For a multilinear function, its convex and concave envelope values at a point are the minimum and maximum expected binary-vertex values among laws with the prescribed coordinate means. Common-threshold rounding simultaneously maximizes every positive monomial, so it also attains the concave envelope of a positive polynomial.

For one physical product on `[1,ρ]^n`, the exact convex envelope depends on the sum `S` of its normalized means: it is `ρ^floor(S)[1+(ρ−1)(S−floor(S))]`. This envelope formula is classical; see Proposition 4.1 in [Adams, Gupte, and Xu, Error bounds for monomial convexification in polynomial optimization](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf), which also attributes the relevant earlier envelope results. The elementary-symmetric envelope underlying the proof is classical as well; see Theorem 3 and Eq. (13) in [Sherali's 1997 paper](https://math.ac.vn/uploads/files/9701245.pdf). The proof below includes the cardinality argument needed here. Novelty is sought in the coefficient inequality and its dimension-independent comparison of full and termwise gaps, not in these envelope formulas. A bounded literature search cannot certify absolute novelty.

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
positive box with coordinate aspect ratios at most `rho`, including fixed
coordinates. Each original monomial
becomes a positive polynomial in physical `[1,rho]` variables, its exact gap is at
most the sum of the expanded monomial gaps, and the full hull gap is affine invariant.

## Transfer to unequal positive boxes

For completeness, retain fixed coordinates and set

\[
s_i=\frac{r_i/\ell_i-1}{\rho-1}\in[0,1],\qquad
z_i=\ell_i[(1-s_i)+s_i x_i],\quad x_i\in[1,\rho].
\]

This is an affine surjection onto the original box. A fixed coordinate has
`s_i=0`, and the expanded function is independent of `x_i`. At any preimage
of the evaluation point, pushing a law forward preserves its objective
expectation. Conversely, a law on the original box lifts through the inverse
maps on nonfixed coordinates; the unused coordinates can be assigned the
chosen preimage means. Thus the full polynomial's hull gap is unchanged.

Each original monomial becomes a multilinear polynomial in the physical `x`
variables with nonnegative coefficients. Its concave envelope equals the sum
of the expanded concave envelopes: one common-threshold law attains every
summand's upper value. Its convex envelope is at least the sum of the expanded
convex envelopes. Therefore its gap is at most the sum of the expanded gaps.
Summing yields `tbtgap_original≤tbtgap_expanded`. Applying the common-aspect
theorem to the expansion proves the bound on the original box, including when
some or all coordinates are fixed.

The expansion is only a proof device. Independent and orientation rounding on the ambient box pull back to the same endpoint laws in the original coordinates. Sampling the certificate therefore requires no expanded polynomial. Moreover, common-threshold rounding attains the concave envelopes of all expanded positive monomials simultaneously, so the original monomial's deficiency under either rounding law equals the sum of the expanded deficiencies. Thus the stated guarantee also holds separately for each original monomial.

## Reviewed finite-dimensional refinement

The [closing proposition and independent audit](../notes/review-positive-box-balanced-orientation-closure.md)
complete the balanced-orientation refinement proposed during development. For
`N>=2` nonfixed coordinates, the bound improves to `rho+beta_N`, where
`beta_N=2-2/N` for even N and `beta_N=2-2/(N+1)` for odd N. All monomial supports
use restrictions of one fixed ambient balanced-orientation law. The linked proof
checks the induction under restriction and the unequal-box transfer. This is an
upper-bound refinement, with no claim of exact finite-dimensional optimality.

## Verification and scope

The [topic-18 Lean package](../formal/topics/18-positive-box/README.md)
formalizes the coefficient inequality, original-box transfer, the two-sided
aspect bound, and the finite-dimensional refinement. The
[coverage map](../formal/topics/18-positive-box/COVERAGE.md) states the exact
hypotheses, including nonnegative coefficients, fixed coordinates and zero
gaps. The [independent review](../formal/topics/18-positive-box/REVIEW.md)
records the resolved findings, and the
[verification record](../formal/topics/18-positive-box/VERIFICATION.md)
separates historical checks from subsequent additions. Neither the exact
fixed-ρ optimum nor minimality of `beta_N` is claimed.

The coefficient proof was developed in `notes/positive-box-rho-plus-two-proof.md`. The finite-step comparison deliberately avoids differentiability assumptions: orientation moments can have breakpoints along a proposed spreading path. Arbitrary mean-preserving spreading is insufficient; the proof specifically moves a global minimum and a global maximum. The development note retains an exact counterexample to the stronger Schur-concavity claim and a possible cardinality-potential corollary.

Fresh independent reviews are recorded in `notes/review-positive-box-rho-plus-two.md` and `notes/review-positive-box-rho-plus-two-second.md`; both include final canonical-text approval. The first also records 1,589 exact rational checks, with script `code/audit-positive-box-coefficients.py`. Earlier independently audited proofs remain in [the coarse positive-box result](positive-multilinear-positive-box.md) and the predecessor note. The lower construction establishes a supremum limit, and the upper bound does not assert that either endpoint of the displayed interval is the exact answer for fixed `ρ`.
