# Independent second audit: leader components and path hardness

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS.** I independently checked the full argument in
[the candidate note](bilevel-leader-vertex-integrity-boundary.md): the
fixed-core algorithm, exact rational recovery, path reduction, gap
normalization, and explicit elimination-message lower bound. This is a
correct structural supporting result. This audit does not establish
publication priority.

## Exact algorithm with bounded remaining components

Dividing a diagonal follower's affine coefficient by its strictly
positive diagonal entry gives its unique clipped affine response, with
polynomial rational encoding length. A follower affine form cannot
involve two different components after deleting the core: its nonzero
coordinates would join those components in the defined leader graph.
The decomposition into core-only terms and independent local objectives
is therefore exact, including signed follower weights and direct affine
leader terms.

For each fixed core point, the local objective is continuous and affine
on each closed clipping cell in a compact box. A minimum exists at a
vertex of one such cell. Even a lower-dimensional bounded cell has a
vertex with a full-rank set of active normals in the ambient component
space; its affine-hull equations contribute to that rank. Thus enumerating
all independent subsets of local clipping and box hyperplanes captures
a local minimizer. The matrices in these systems are constant in the
core. Their inverses give rational affine candidate locations, with
polynomial count and bit length for fixed component dimension. Singular
subsets and zero component normals do not remove necessary candidates.

Requiring only box feasibility for an enumerated intersection is safe.
Such a candidate is an actual local leader choice regardless of which
clipping cells meet there. Correct objective evaluation supplies its
clipping regime; no unstated local optimality test is needed.

The first core arrangement fixes each candidate's box feasibility and
each evaluated ramp's branch. On every relative cell, all candidate
values are affine with polynomial rational encoding length. A second
arrangement of within-component pairwise comparisons fixes a minimizing
candidate for each component. A polynomial number of hyperplanes has
polynomially many realizable sign cells in fixed dimension, including
zero signs. Repeating the second arrangement separately for each first
cell still multiplies two polynomial bounds. Constant tests can be
handled directly, including the case of a zero-dimensional core.

The closure step is valid for two separate reasons. First, each selected
candidate stays in the closed component box at every limit point, and
its affine branch formula agrees with the clipped function at every
threshold. Therefore each final LP solution gives an actual feasible
leader and the stated objective value. A newly feasible boundary
candidate can improve the true local minimum, but cannot invalidate
the chosen feasible point. Second, a global optimum belongs to one
enumerated relative cell. The available candidates reproduce the local
minima there, and optimization over its closure can do no worse. These
two inequalities establish exactness without claiming that selected
candidates remain globally optimal along every boundary.

Every final LP is over a closed bounded rational polyhedron. Rational
LP vertices have polynomial bit length; substituting the affine local
candidates and then clipping gives a rational global optimizer of
polynomial encoding length. Enumerating potential core sets of size at
most fixed `c` costs a polynomial factor. The result is polynomial for
fixed `c,h`; no parameter-independent exponent or FPT claim follows.

## Exact path reduction and bounded coefficients

On `[-1,1]`, the three positive parts with arguments `t`, `t-r/2`, and
`t-r` never exceed one. The proposed capped-ramp expression for
`rho_r(t)` therefore has slopes `-1,+1,-1,+1` on the four intervals
separated by `0,r/2,r`, and agrees with the distance to `{0,r}` at all
breakpoints. It is the stated distance function throughout the domain.

For every feasible leader, choose a closest increment option
`delta_i in {0,a_i/W}`. Telescoping shows that its subset total differs
from the target by no more than the initial-state penalty, increment
penalties, and final target penalty. Conversely, normalized partial
subset sums are all in the unit box, start at zero, and make every
increment penalty vanish. Hence the minimum continuous objective is
exactly the normalized nearest-subset-sum distance, not merely bounded
by it in one direction.

Summing the `-t` terms gives `x_0-x_n`; adding the initial-state and
terminal absolute-value terms gives the displayed `2x_0-2x_n+tau`.
Each remaining ramp is realized by one independent box coordinate with
objective `z^2/2-h(x)z`. The Hessian is exactly the identity. Every
follower affine coefficient has magnitude at most one, and every upper
affine coefficient has magnitude at most two. The nonunary response
forms involve exactly consecutive leaders; the graph is the stated
path. No endpoint equalities or other upper constraints are hidden in
the construction. Optional follower coordinates for direct leader terms
are unary and preserve these properties.

The input transformation has polynomial rational encoding length.
Guessing all clipping regimes produces rational linear constraints for
a threshold witness, so NP membership is justified by rational LP
witness bounds. Zero optimum is equivalent to the Subset Sum instance
being a yes instance. A no instance has optimum at least `1/W`.

This is an ordinary numerical hardness reduction with potentially large
denominators. Bounded magnitude is not bounded numerical encoding. An
additive error strictly below `1/(2W)` distinguishes the instances, so
the obstruction applies to polynomial dependence on accuracy bit count.
Multiplying the objective by `W` gives a constant gap while changing
upper coefficient magnitudes to as much as `2W`. Neither version proves
strong hardness with bounded numerical data or rules out polynomial
dependence on inverse additive tolerance.

## Exact message growth and source scope

Fixing the terminal state `t`, the same telescoping inequality gives
`V_n(t)>=dist(t,S)`. For any subset, use its partial sums through state
`n-1`, then replace only the terminal state by `t`. The last penalty is
at most the distance from `t` to that subset total. This proves the
reverse inequality and the exact message identity.

For powers-of-two weights, the subset-sum set is the uniform grid of
`2^n` points in the unit interval. Its distance function has one rising
and one falling affine piece between each pair of consecutive grid
points. At every grid point and every midpoint the slope changes, so
none of these pieces can be merged. The exact count is
`2(2^n-1)`. This is exponential in the number of local factors and
superpolynomial in their `O(n^2)` binary encoding length. It is an
explicit intervalwise-affine output-size lower bound, not a lower bound
for compressed representations or all optimization algorithms.

I also checked the primary
[Meuleau–Morris–Yorke-Smith paper](https://homepage.tudelft.nl/0p6y8/papers/n58.pdf),
Theorem 1 and the complexity discussion preceding Algorithm 1 on PDF
page 4. The theorem establishes piecewise-linear closure, while the
per-step bound counts pieces in current bucket functions. The present
example is compatible with that closure theorem and makes intermediate
piece growth explicit. The candidate's qualified comparison is sound;
it does not identify a false closure statement.

The existing first audit and exact diagnostics already test the relevant
finite arrangements and reduction identities. I did not add duplicate
computational tests; this second audit supplies a separate mathematical
and bit-complexity check.

## Addendum: identical factors and a fixed coefficient alphabet

The author's strengthening also passes. Replace the increment factor by
the same function `rho_(1/2)(x_i-x_(i-1)/2)` at every step and retain the
initial cost `x_0`. The zero-cost terminal states are precisely

```
S_n={j/2^n : 0<=j<2^n}.
```

Indeed, zero cost forces `x_0=0` and the recurrence
`x_i=x_(i-1)/2+delta_i` with `delta_i` either zero or one half. These
binary choices give exactly that dyadic grid, with every intermediate
state inside the unit box.

For an arbitrary trajectory choose the nearest option `delta_i` and
write `e_i=x_i-x_(i-1)/2-delta_i`. Telescoping gives

```
t-s=2^(-n)*x_0+sum_i 2^(-(n-i))*e_i,
```

where `s` is the grid state generated by those options. Thus the
distance to the grid is at most the weighted absolute error, which is
at most `x_0+sum_i |e_i|`, the actual cost. Conversely, follow the
zero-cost trajectory to any grid point until step `n-1`, and change
only the final state to `t`. Its cost is at most the distance to that
grid point. The exact message is therefore `dist(t,S_n)`.

There are two affine pieces between consecutive grid points and one
final increasing piece from the last grid point to one. The count is
exactly `2^(n+1)-1`. Every local scalar argument lies in `[-1/2,1]`,
so the earlier capped-ramp identity remains applicable. The factors
and all their coefficients now come from a fixed finite alphabet.
This strengthens the explicit-message obstruction without asserting
NP-hardness for the uniform family or ruling out a short implicit
representation of its dyadic-grid distance function.

The reviewed theorem and identical-factor extension are now included
in the promoted
[result](../results/bilevel-leader-vertex-integrity-boundary.md), which
links both independent audits. The scope of this verdict includes that
integrated extension.
