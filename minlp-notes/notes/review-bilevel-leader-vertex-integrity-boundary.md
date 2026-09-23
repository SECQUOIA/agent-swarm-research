# Independent audit: bounded leader components and path hardness

Date: 2026-09-05. Reviewer: potential_flow_review. Verdict: PASS.

I independently checked the complete proof in
[the candidate](bilevel-leader-vertex-integrity-boundary.md). This audit
addresses correctness and rational bit complexity; source priority remains
a separate question.

## Fixed core and bounded components

The response of a diagonal strictly convex box follower is exactly its
coordinatewise clipped rational affine response. A follower term involving
two distinct noncore components would join those components in the leader
interaction graph. Consequently the stated decomposition into core-only
terms and separate component objectives is valid, including arbitrary
signs in the leader objective and its direct affine terms.

For a fixed core point, a continuous piecewise-affine objective on a compact
component box has an arrangement-vertex minimizer. A bounded arrangement
cell, including a lower-dimensional one, has vertices with a full set of
independent active normals in the ambient component dimension. The box
faces supply any necessary boundary normals. Enumerating all independent
row subsets therefore captures a minimizing point; singular subsets and
zero normals can be omitted. Each matrix is constant in the core, so its
solution is rational affine in the core. Box feasibility suffices for
sound evaluation of every enumerated candidate.

For fixed component bound, the number of row subsets is polynomial. Rational
inversion, evaluated clipping forms, and summed candidate objectives all
have polynomial bit length. The fixed-dimensional core arrangement first
fixes box feasibility and clipping regimes, then pairwise affine comparisons
fix minimizing candidates. Both enumeration stages have polynomial size
for fixed core dimension. Iterating the second stage separately over each
first-stage cell still gives a polynomial bound.

The use of closures in the final LP is safe. Selected candidates remain
feasible at a limit point, and the affine clipping branches agree with the
continuous clipped function at their thresholds. Thus every LP solution
is a valid original leader choice, even if a previously excluded candidate
becomes feasible and improves at the boundary. Conversely, a global optimum
belongs to some enumerated relative cell, where minimizing candidates
reproduce its value; the LP over that cell's closure can do no worse. These
two inequalities prove exactness without requiring the selected candidates
to remain globally best at every boundary point.

The core box makes the LPs bounded. Rational LP optimizers and affine
candidate substitution give a polynomial-bit rational leader and follower
witness. Constant tests, zero-dimensional core space, core-only terms, and
isolated components have the stated treatment. Enumerating all leader
subsets of size at most a fixed constant also makes the decomposition
search polynomial. This is a fixed-parameter-value polynomial statement,
not a uniform fixed-parameter tractability claim.

## Exact path reduction

For `t in [-1,1]` and `0<r<=1`, all three positive parts in

```
-t+2clip(t)-2clip(t-r/2)+2clip(t-r)
```

are below their unit caps. Its slopes on the intervals separated by
`0,r/2,r` are `-1,+1,-1,+1`, with the correct values at every breakpoint.
It therefore equals `min(|t|,|t-r|)` throughout the required domain.

Choosing a nearest increment `delta_i in {0,r_i}` and telescoping proves
that the normalized distance to a subset sum is no greater than the
continuous leader objective. Conversely, normalized selected partial sums
give feasible leader states in `[0,1]`, eliminate all increment penalties,
and attain the distance to their total. This proves the exact optimal-value
identity, including both satisfiable and unsatisfiable instances.

Expanding the absolute value and summing the linear increment terms gives
the direct leader coefficients `2x_0-2x_n` in the displayed follower
realization. Every ramp has coefficients in `[-1,1]`; independent
`z_i^2/2-h_i(x)z_i` objectives have identity Hessian and unique responses.
The upper coefficients have magnitude at most two, and all nonunary ramps
join consecutive leader coordinates only. No hidden endpoint constraints
or nonbox upper constraints are used.

All normalized coefficients have polynomial rational encoding length.
Clipping-regime certificates reduce threshold feasibility to rational LP,
so a yes instance has a polynomial-bit rational witness. This establishes
NP membership as well as the stated exact-threshold hardness.

The gap is `1/W` before objective scaling and one after multiplying the
upper objective by `W`. Thus the bounded-coefficient reduction establishes
a precision obstruction and weak numeric hardness. It does not establish
strong NP-hardness or rule out a scheme polynomial in inverse tolerance.
The distinction between small coefficient magnitude and large denominator
encoding is correctly preserved.

## Independent exact checks

The separate checker
[check_leader_path_subset_sum.py](../code/bilevel_response/check_leader_path_subset_sum.py)
enumerates every vertex of the original continuous objective's clipping
arrangement for six small instances. Exact rational arithmetic verifies
the continuous minima against exhaustive subset sums, including positive
no-instance gaps. It also checks the expanded follower objective at all
837 feasible vertices and checks 153 signed-distance identities across all
branches and their endpoints. All checks pass. These finite checks support
the proof; they do not replace the general reduction.

## Exact elimination-message extension

The author's proposed extension also passes independently. With the final
state fixed to `t`, let `V_n(t)` minimize the initial-state penalty and all
increment penalties. The same telescoping inequality gives
`V_n(t)>=dist(t,S)`, where `S` is the normalized subset-sum set. For the
reverse inequality, choose a subset nearest to `t`, use its partial sums
through state `n-1`, and set the final state to `t`. The final increment's
penalty is no greater than its distance from the chosen final increment,
so `V_n(t)<=dist(t,S)`.

For `a_i=2^(i-1)`, the set `S` is exactly
`{j/(2^n-1):0<=j<=2^n-1}`. Its distance function on `[0,1]` has exactly
`2(2^n-1)` maximal affine intervals, with alternating slopes `+1,-1`.
This proves exponential growth in `n` for explicit piecewise-affine message
representations. It does not assert the impossibility of compressed
representations or exponential growth in the complete binary input length.

The stronger identical-factor version also passes. Replace each increment
penalty by `rho_(1/2)(x_i-x_(i-1)/2)`. With nearest choices
`delta_i in {0,1/2}` and residuals `e_i`, the recurrence gives
`t-s=2^(-n)x_0+sum_i 2^(-(n-i))e_i` for a reachable state `s`.
Every coefficient has magnitude at most one, so the objective bounds this
distance from below. Fixing a selected exact prefix and changing only its
final state proves the reverse inequality. The zero-cost reachable set is
`{j/2^n:0<=j<2^n}`. Its distance function has `2^(n+1)-1` maximal affine
intervals, including the final increasing tail. All local factors use the
same fixed coefficient alphabet and unit boxes. This strengthens the explicit
message-size obstruction without asserting hardness for that uniform family.
