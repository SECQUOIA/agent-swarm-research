# Second independent review: joint nomination and resistance optimization

Date: 2026-09-05. Verdict: **PASS**, with a statement correction applied.
The intended connected-network proof has no substantive defect. The author
added the missing explicit connectivity hypothesis after this review.
The separate novelty question is outside this verdict.

Reviewed: [joint-resistance candidate](potential-flow-joint-resistance-investigation.md),
in its simplified version transferring the nomination-face theorem by
fixing the resistances of a joint optimum. The reviewer also read the
bounded-block-rank face proof and cactus aggregation/sensitivity antecedent,
and previously independently reviewed the fixed-core/polyhedral-block
theorem used here.

## 1. The joint optimal-face argument is valid

For a connected network, positive finite resistance intervals and a compact
balanced nomination box give a compact parameter domain. Physical flow and
normalized potentials are continuous on this domain: any convergent parameter
sequence has bounded physical flows, and every flow subsequential limit
satisfies the limiting conservation and cycle equations. Strict convexity
of the positive-resistance energy makes the limiting physical flow unique.
Summing limiting edge drops along a spanning tree recovers continuous
normalized potentials. Thus a joint maximizer exists.

Fix its resistance vector `beta*`. The maximum over nominations at this
fixed vector equals the joint optimum: it is at least the value of the
chosen joint maximizer, and it cannot exceed the unrestricted joint maximum.
The already reviewed fixed-resistance face theorem therefore supplies a
nomination on one of its faces with exactly the joint-optimal value.

This transfer requires the **entire enumerated family** to be independent
of resistances. It is: the family enumerates topological path threshold
patterns and rational nomination-bound choices, rather than computing
threshold locations from a particular adjoint. The selected-block and
bounded-free-coordinate properties thus transfer together. No simultaneous
resistance KKT conditions, new perturbation limit, or zero-containing
nomination intervals are needed.

## 2. Separation after fixing a face

Branches outside the objective-terminal block path attach at one core
vertex. Their contribution to core conservation is the sum of their
nominations, independently of their internal resistances. With no additional
physical bounds, every admissible aggregate nomination can be disaggregated
and its attached branch can carry its own unique passive flow. Arbitrary
positive resistances on those off-path branches do not change the objective.

A selected face fixes all nominations outside its active block and fixes
the active block total by balance. Each other block consequently has fixed
effective loads. This includes the potentially delicate articulation case:
changing the active block's exit-vertex nomination while compensating at
another active vertex cannot change the total load seen across the adjacent
block cut. The neighboring block's effective articulation load is fixed
by conservation of its own fixed outside component.

Each inactive block's flow then depends only on its own resistance variables
and fixed effective loads. Potential drops telescope across blocks, and
resistance boxes share no variables between blocks. The maximum over a
selected face is therefore the sum of one active joint optimum and the
inactive resistance-only optima. Summing independently optimized local
drops is exact under these assumptions.

## 3. The mapping to fixed-core optimization is exact

Conservation permits a tree-routing particular flow plus fundamental
circulations. With at most `8r-2` free active nominations, eliminating one
by balance and adding at most `r` circulation coordinates gives the stated
fixed nonlinear dimension. A face without free nominations needs no such
elimination. Inactive blocks have only their bounded number of circulations.

The routing coefficients are rational affine functions of the nomination
coordinates. Normalize the fundamental cycle matrix so that each circulation
coordinate is its own chord flow; the tree particular flow is zero on all
chords. Every physical edge flow is bounded in absolute value by total
possible injection: orient its nonzero flow downhill in potential, producing
an acyclic flow that decomposes into injection-to-withdrawal paths. This
bound is independent of all resistance values. Thus a rational circulation
box is valid uniformly; no resistance-dependent core bound is being hidden.

On a flow-sign cell the edge law is `beta_e * sign_e * x_e(z)^2`.
Conservation is already satisfied. Vanishing sums of these drops around a
fundamental cycle basis are necessary and sufficient for a node potential
vector to exist. These are exactly the remaining physical equations, not
merely a relaxation. Positivity of resistances gives the unique passive
solution for each nomination/resistance pair.

Each resistance is a continuous scalar interval leaf. The cycle equations
provide at most `r` aggregate rows, and the path-drop objective is linear in
the leaves with quadratic core coefficients. All resistance box constraints
remain local. The closed sign-cell/core-box intersection is compact and
semialgebraic. On sign-cell boundaries, the two polynomial pieces both
vanish at a zero flow, so closure introduces no invalid physical solution.

Accordingly, every hypothesis of the fixed-core theorem is satisfied. There
is no unbounded collection of nonlinear core variables, leaf integrality
condition, or cross-leaf capacity hidden in the construction. Actual flow
and potential bounds would require a new audit and are explicitly excluded.

Bridge blocks can be handled directly. Their signed flow is affine in the
one independent nomination coordinate. Since `beta*q*abs(q)` is increasing
in `q` for every positive `beta`, use the largest feasible `q`; then use
the upper resistance endpoint if `q>=0` and the lower endpoint if `q<0`.
Zero flow permits either endpoint. This also covers a bridge with fixed
effective nominations and avoids negative dimension formulas.

## 4. Algebraic encoding and global values

Each local call returns an exact algebraic optimizer with polynomial encoding
length, including all its resistance coordinates. Its resistance leaf
vertices are rational interval endpoints, so there are no parameter-dependent
vertex denominators in this application.

There may be many local algebraic fields. The algorithm does not need to
combine them into one primitive extension, which could have large degree.
Instead, approximate each local value and coordinate separately. Add rational
value intervals blockwise and compare the resulting rational enclosures
across the polynomially many faces. An extra factor from the number of
blocks in the error allowance costs only logarithmically many precision
bits. Exact comparison of an unbounded sum of algebraic local values is
correctly avoided.

For each face, enclose its optimal value to width `eta`. The interval formed
by the largest lower endpoint and largest upper endpoint over all faces
also has width at most `eta` and contains the global optimum. Selecting a
face with the largest lower endpoint loses at most `eta` before rounding.
These statements do not assume the objective or local drops are nonnegative.

## 5. Independent derivation of resistance sensitivity

For the smoothed law, write `g(x)=x*abs(x)+rho*x` and
`D=diag(beta_e*(2*abs(x_e)+rho))`. Differentiating at fixed nominations gives

```
B dx = 0,
B^T d(pi) = D dx + diag(g(x)) d(beta).
```

Thus `L d(pi)=B D^{-1} diag(g(x)) d(beta)`, where `L=B D^{-1} B^T`.
For `L h=e_s-e_t`, symmetry yields

```
d(pi_s-pi_t)/d(beta_e)
  = ((B^T h)_e / D_ee) * g(x_e).
```

The sign in the draft's formula is therefore correct. The first factor is
the signed ordinary unit electrical adjoint current. Orient its nonzero
edges downhill in `h`; the resulting flow is acyclic and has one unit of
total injection. Hence its absolute value on any edge is at most one.
This gives the uniform derivative bound `B^2+rho*B`.

Integrating along a resistance-box segment and passing to the unsmoothed
limit gives the resistance term `B^2*||beta-gamma||_1`. Combining this with
the previously reviewed nomination bound, uniformly using resistance upper
bounds along one fixed objective path, proves (4). The reasoning permits
negative sensitivity and does not assume resistance monotonicity. Zero-flow
edges cause no derivative singularity before the limit. If the nomination
bound `B` is zero, the objective is identically zero and recovery is trivial.

## 6. Rational recovery preserves the right constraints

The required output constraints are only rational nomination intervals,
exact nomination balance, and rational resistance intervals. Refine isolating
intervals for active nominations, intersect them with the original bounds
and balance equation, and solve the resulting rational LP. It is nonempty
because it contains the algebraic nomination sample. Hence it has a rational
point of polynomial encoding length, including when some true coordinates
are at bounds. Its coordinate errors are controlled by interval widths.

Every resistance can be rounded independently inside its original interval
and its refined isolating interval. Different blocks' coordinates can be
processed in separate algebraic fields. Dividing the total error allowance
by the number of resistance coordinates adds only logarithmic precision
overhead. All Lipschitz constants have polynomial rational bit lengths.

The rounded point need not preserve the sampled circulation or original
cycle equalities. It has a new unique physical solution, and the joint
Lipschitz bound controls that solution's objective. This is the correct
recovery argument for the stated output; requiring the old algebraic flow
to survive rounding would be unjustified. Rational group disaggregation
and arbitrary positive rational off-path resistances then complete an
exactly admissible original-network parameter vector.

## 7. Statement correction and independent checks

The candidate opening initially omitted the word **connected**, although
its antecedent theorem and all subsequent block-path reasoning use this
hypothesis. For a disconnected graph global balance need not imply balance
on each component, and potentials between components have no defined
relative offset. The author added the explicit connected-network assumption.

The [reviewer's independent checker](../code/potential_flow_mpd/independent_joint_review.py)
builds its own incidence matrix, chord-normalized cycle coordinates, and
physical root solve. The test network contains a theta block, bridge,
triangle block, and attached off-path triangle. On 12 shifted balanced
nomination instances it passed:

- 156 resistance derivative finite differences; maximum error `4.44e-11`;
- 12 active-block changes, including its exit articulation nomination,
  preserving all inactive flows; maximum error `4.12e-12`;
- 12 off-path resistance changes preserving all objective-core flows;
- 12 joint rounding checks using newly solved physical flows and the
  claimed Lipschitz error bound.

The largest absolute unit adjoint current was one. These are numerical
checks of the identities and separation, not a certified global algorithm
or a substitute for the analytical proof.

## 8. Addendum: exact edge-flow extrema and robust capacity validation

The reviewer subsequently audited
[the exact arc-flow corollary](potential-flow-exact-arc-capacity-investigation.md).
Verdict: **PASS**, including the corrected optional rational-output argument.

An objective edge's endpoints lie in its single biconnected block, or its
bridge block. Every outside component attaches at one block vertex. The
same sum-interval aggregation therefore preserves the complete attainable
edge-flow set, independently of resistances outside the block. There is no
sum of independently optimized block drops in this objective.

Freeze the resistance vector of a joint edge-flow maximizer. At fixed
positive resistance on the objective edge, signed flow is a strictly
increasing function of its endpoint potential difference. The two objectives
have exactly the same nomination maximizers at that fixed vector. The
resistance-independent nomination-face family therefore contains a joint
edge-flow maximizer as well. It is essential to freeze resistance for this
step: globally maximizing potential difference while allowing resistance
to change need not maximize the edge flow.

On each face and sign cell, the edge flow is affine in the fixed core.
Set the fixed-core theorem's leaf objective coefficients to zero and put
this affine function in its core-only objective. The scalar resistance
leaves and bounded number of cycle equations are unchanged. Thus exact
local optimum values have polynomial algebraic descriptions. Pairwise
comparison of a polynomial number of such algebraic values is polynomial;
each comparison can work with the two representations at hand and need
not create a common field for all candidates. Reversing the objective
orientation gives the exact minimum. Bridges reduce directly to extrema
of a signed nomination sum and do not require algebraic optimization.

For a finite list of rational edge capacities, universal satisfaction is
equivalent to comparing each exact maximum with its upper bound and each
exact minimum with its lower bound. This requires only twice as many
optimizations as edges and preserves equality-sensitive decisions. With
unique passive flow and no other operating constraints, it also gives the
stated robust-feasibility interpretation. It does not optimize over a
scenario set already filtered by some capacities.

The initially informal rational-output sentence needed a quantitative
argument; the reviewer reported this and the author corrected it. For two
parameter scenarios write their objective-edge flows as `x,y`, endpoint
drops as `p,q`, and resistances as `beta,gamma`. Let
`g(t)=t*abs(t)`. The elementary inequality
`|g(x)-g(y)| >= |x-y|^2/2` follows by separating the same-sign and
opposite-sign cases. Since `p=beta*g(x)` and `q=gamma*g(y)`,

```
|x-y| <= sqrt(2*(|p-q|+B^2*|beta-gamma|)/beta_lower).
```

Combine this with the reviewed potential-drop Lipschitz estimate and round
the **exact edge-flow optimizer**, using interval/balance recovery as above.
Making the expression inside the square root at most `epsilon^2` requires
only polynomially many precision bits. This proves the optional rational
near-optimal parameter recovery; continuity alone would not have supplied
its bit-complexity bound. It is not obtained by substituting a joint
potential-difference optimizer for the edge-flow optimizer.
