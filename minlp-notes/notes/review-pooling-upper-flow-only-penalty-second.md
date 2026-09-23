# Second review: eliminating lower flow bounds by a penalty

Date: 2026-09-05. Verdict: PASS for
[the exact-penalty draft](pooling-upper-flow-only-penalty-hardness.md),
including its use with the separately reviewed single-upper-quality
cyclic construction. No substantive defect found.

## Explicit polyhedral bound

The proposed constant `H=N(NK)^(N-1)` is valid when the inequality rows
are integer vectors of magnitude at most `K>=1`. For the Euclidean
projection `v` of `w`, write `h=w-v=B^T lambda`, where `lambda>=0`
and the active rows of `B` are linearly independent. Such a representation
follows by repeatedly eliminating a dependence from a conic representation
of the projection normal, preserving nonnegative coefficients until at
most `N` independent rows remain. This works also for lower-dimensional
polyhedra described using opposite inequalities.

Every selected row is tight at `v`, so
`||h||_2^2<=eta ||lambda||_1`, with `eta` the largest positive
inequality residual at `w`. Full row rank gives
`||lambda||_1<=sqrt(N)||h||_2/sigma_min(B)`. The integer Gram
determinant `det(B B^T)` is positive and at least one. Since all singular
values are at most `NK`, its product identity implies
`sigma_min(B)>=(NK)^(-(r-1))`. Cancelling the nonzero norm of `h`
and converting to the one-norm proves the stated bound. Zero residual
therefore forces zero distance, as required.

The classical existence result is correctly attributed to
[Hoffman (1952), Section 2](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf).
I inspected that primary source. The explicit coefficient bound here is
justified by the direct argument above; the reduction does not assume
that an optimal Hoffman constant can be computed efficiently.

In the application, keep every contract row `E,-E` unscaled. These rows
have integer zero/one coefficients. All other violated-row candidates
already have zero positive residual because the relaxed point satisfies
`A`. Clearing those rows' denominators therefore cannot amplify a positive
residual. The maximum residual is at most the sum of contract deficits.
Row-wise denominator products and the resulting integer coefficient
bound have polynomial bit length. Consequently `log H` is polynomial,
even though `H` is numerically large.

## Correct copy subsystem and radial repair

The polytope must contain the physical, homogeneous output-quality rows,
using actual output throughput after lower demands are deleted. With
exact output demands these coincide with the previous gadget rows. The
draft's definition of `A` as the retained physical constraints has this
meaning. No pool-quality variable belongs in this copy-only polytope.
The total intake bound `T<=2` is linear and remains valid. Finite arc
bounds ensure boundedness. The zero original-intake signal assignment
extends to every gadget and proves nonemptiness even if the normalized
source polytope is empty.

For original qualities `a_i>1`, the two primary outlets accept exactly
the nonnegative intakes satisfying `T<=2` and
`F(x)=S(T-1)-T<=0`, where `S=a^T x`. For positive throughput the
second outlet accepts at most one unit, and the first accepts at most
`T/S`; its anchor fills the remaining unit capacity. These bounds are
attainable. The zero vector is feasible separately.

On `x>=0,T<=2`, the derivative bound
`|a_i(T-1)+S-1|<=3a_max+1=L` is valid. Thus a polyhedral repair
`x'` can violate `F` by at most `L H delta`. If it does, then
`T'>1,S'>1`, and scaling to total throughput `1+T'/S'` removes
exactly `F(x')/S'` mass. In particular the repair estimate does not
divide by a quantity tending to zero. Homogeneity of the encoded source
cone makes the scaled vector valid. Rebuilding the copy network from
that vector, rather than scaling all gadget flows, is essential and is
done explicitly in the draft.

## Objective, encoding, and combined scope

The intake objective changes by at most
`C delta`, with `C=b_max(1+L)H`. Setting `M=C+1` gives strict
dominance of any point with a positive contract deficit by its repaired
exact-contract point. Hence the optimal value identity with offset
`B0=M sum e_j` holds exactly, with a polynomially encoded threshold.
There is no precision gap assumption in this argument.

The private-source cost realization also works. Its relaxed flow need
not equal the intake; compare it first with the polyhedral repair using
the full-vector one-norm bound. Only at that exact-contract point use the
copy identity, and then use the radial estimate. This is precisely the
two-step argument in the draft. Source throughput rewards and output
throughput rewards have ordinary input-cost/output-revenue form. A common
charge and revenue cancel by total physical mass balance and can make
both costs and revenues nonnegative.

The cyclic construction uses the same type of nonempty rational copy
polytope, the same integer contracts, and the same homogeneous cone
projection. Therefore this proof applies to it without introducing a
lower quality bound or another quality coordinate. The combined theorem
has all lower flow bounds zero, one scalar upper-bound quality, input
out-degree and output in-degree at most three, and two pool outlets.
The pool's input degree remains unrestricted. This is ordinary, not
strong, NP-completeness when combined with the reviewed NP upper bound.

## Separate checks

[independent_penalty_bound_review.py](../code/pooling_bypass_copy/independent_penalty_bound_review.py)
passed 500 exact rational radial and error estimates, including 183
nontrivial repairs, and 12 explicit encoding bounds for `H`, including
258-bit coefficients. These checks test the formulas; the proof above
establishes the general bound.

[independent_upper_quality_review.py](../code/pooling_bypass_copy/independent_upper_quality_review.py)
also passed eight assembled-network penalty LPs, covering both intake
and private-source rewards, with all contracts restored at the tested
moderate penalty. These numerical experiments do not validate the much
larger theoretical constant and are not used for its proof.
