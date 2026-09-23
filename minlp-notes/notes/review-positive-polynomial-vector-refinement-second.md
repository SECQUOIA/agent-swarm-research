# Second independent review: vector powers and scalar proof mechanisms

Date: 2026-09-05. Verdict: **PASS** for
[the candidate note](positive-polynomial-vector-refinement-obstruction.md).
The example does not settle the additive-constant comparison with the
true unrestricted-integer convex-lift minimum. No implementation or
new numerical test is needed for the following exact inequalities.

## Constants and non-midpoint witnesses

The degrees `D_j=128*1024^(j-1)` are positive integers and the selected
rational inputs `x_j=1-64/D_j` increase strictly from `1/2` toward one.
For `j<ell`, Bernoulli's inequality applies to the integer power `D_j`
and gives `x_ell^D_j>=1-64*D_j/D_ell>=15/16`.

For `xi=(x_j+2*x_ell)/3`, its distance below one is at least
`64/(3D_j)`. The base in that comparison is positive because
`D_j>=128`. Hence `xi^D_j<=exp(-64/3)<=3/67`. Dropping the nonnegative
term `F_j(x_j)/3` is safe. The resulting lower bound is exactly

```
(7/4)*(5/8-3/67)=2177/2144=1+33/2144>1.
```

Thus every selected pair has a forbidden convex combination with
weights one third and two thirds. This argument works uniformly for
every pair, not merely consecutive degrees.

Choose one actual integer/continuous lift of each exact graph witness.
Equal integer residues modulo three make the same one-third/two-thirds
combination integral in every integer coordinate. Convexity of the
lifted set would then include a projected point outside the admissible
error band. Consequently all `M` selected lifts have distinct residue
vectors, proving `3^p>=M`. Neither bounded integer ranges nor closedness
of the lift is used in this finite argument.

For a binary lift, two equal binary labels remain equal under every
convex weight, including these weights. Hence the witnesses require
distinct labels and `2^p>=M`. Any binary formulation is also an
unrestricted-integer formulation with explicit coordinate bounds, so
`p_conv<=p_bin`. The case `M=1` causes no exception: the lower bounds
are zero and need not be tight.

## Why all exact-graph midpoint tests pass

For a differentiable convex function, differentiating its midpoint
Jensen gap shows it is nonincreasing in the lower endpoint and
nondecreasing in the upper endpoint. The maximum over subintervals
of `[0,1]` is therefore at `(0,1)`. Here that value is
`7/8-(7/4)*2^(-D_j)`, which is nonnegative and strictly below `7/8`.
The midpoint error is upward because every component is convex,
so this is also its absolute component error.

This statement concerns pairs of exact graph points. It does not
claim that all pairs in the entire admissible error band, or in every
possible approximate formulation, have admissible midpoints. Nor does
it assert that repeated arbitrary convex combinations are compatible:
the explicitly forbidden non-midpoint combinations already show why
that would be false.

## Finite vector upper formulation and chord-cover count

Every half-height knot `a_j=2^(-1/D_j)` is a real algebraic number in
`(0,1)`, and these knots are distinct. On a subinterval of their common
partition, a given component never crosses its own half-height knot
in the interior. Its entire range therefore has length at most `7/8`.
The input interval times the product of these ranges contains the
full vector graph over that interval. At any admitted input, both the
true and admitted output coordinates lie in the same component range,
so their absolute difference is at most `7/8`. This verifies containment
and the error bound for all points of every rectangle, not only knots.

For completeness, assign distinct binary codes of length
`ceil(log2(M+1))` to these `M+1` bounded rectangles and take the convex
hull of each rectangle paired with its code. This is a finite polytope,
hence has a finite linear description. Restricting the code coordinates
to binary selects precisely the corresponding rectangles: a binary
vector cannot be a nontrivial convex combination of different binary
vectors. Unused codes yield no feasible point. This proves the upper
integer count without adding hidden integer selector coordinates.
The coefficients can be real algebraic; neither rational encoding nor
polynomial formulation size is being claimed here.

The full-domain chord error is nonnegative and at most `7/4<2`, so
`N_F(2)=1`. If an admissible interval contained two selected witnesses,
its component chord would lie above their smaller chord. Indeed, the
larger chord lies above the convex graph at both selected endpoints;
subtracting the smaller affine chord preserves a nonnegative value
between them. At `xi` its error therefore exceeds one by the already
proved margin. Every admissible interval covers at most one selected
witness, giving `N_F(1)>=M`. This applies to covers with overlapping
intervals as well as partitions.

## Signed scalarizations

For every real `lambda` of one-norm one, the reference function
`Psi=sum |lambda_j| F_j` is continuous and strictly increasing from
zero to `7/4`. There is one half-height knot. On either side, the
variation bound
`|g_lambda(b)-g_lambda(a)|<=Psi(b)-Psi(a)` shows that the actual
scalar output range has length at most `7/8`. Taking its true minimum
and maximum on each compact interval gives two valid graph-containing
rectangles. The same code construction uses one binary coordinate.
Negative scalarization coefficients require no convexity assumption
on `g_lambda` because this is a range argument.

The constants in this scalar formulation may be arbitrary real numbers
when `lambda` is arbitrary real; this is permitted by the finite-count
definition. The induced error interval is exactly `[-1,1]`, since
the support function of `[-1,1]^M` at `lambda` is its one-norm.
Thus the scalar/vector distinction is not an inconsistent choice of
scalar tolerance.

## Conclusions and prior scope

The verified bounds are exactly those stated: both vector integer
counts grow, every fixed scalarization has binary count at most one,
every pairwise exact-graph midpoint test passes, and halving the chord
error can require arbitrarily many pieces as output dimension grows.
These facts do **not** imply an unbounded difference `p_bin-p_conv`:
the unrestricted-integer lower bound `log_3 M` and binary bounds near
`log2 M` leave that comparison unresolved. Dense polynomial encoding
also does not invalidate the example, although its length grows much
faster than the sparse degree encoding. No computational hardness or
polynomial rational construction follows from these finite counts.

I inspected the primary
[Lubin–Vielma–Zadik text](https://arxiv.org/html/1706.05135),
Lemma 4.13 and its proof. Its midpoint-rank bound uses the familiar
selection of integer witnesses and parity argument. The present
modulo-three step is the same elementary convex-combination mechanism
with a different denominator; it should not be presented as a new
general representability principle. This review verifies the specific
positive-power family and combined separation, while leaving its
publication priority qualified as in the candidate note.

## Addendum: finite upper bounds relative to the convex-lift minimum

I independently reviewed the appended box and unconditional-polytope
corollaries. Verdict: **PASS**, retaining continuous componentwise
convex outputs on one compact input interval and the unrestricted
finite real-coefficient formulation-count interpretation.

For each of the at most `2^p` parity classes, collect input coordinates
of exact graph witnesses and take its closure in the compact domain.
The minimum and maximum of any nonempty closure are limits of original
witness inputs in that same class. Midpoints of their actual lifts
have integer coordinates; their projected errors belong to `K`.
Continuity of `F` and closedness of `K` place the limiting endpoint
midpoint gap in `K`. No limit of the auxiliary lift coordinates is
required, so their possible unboundedness is harmless.

On the interval between those limiting endpoints, every component
chord gap is concave, nonnegative, and zero at its endpoints. Joining
its maximizer to the farther endpoint proves its midpoint value is
at least half its maximum. Thus the component gap is at most twice
its allowed midpoint error. These parity interval hulls cover the
whole input domain, including any singleton classes.

For a scalar gap bounded by `2*epsilon`, two cuts at level `epsilon`
suffice when the maximum exceeds that level. On any subinterval the
new chord gap equals the old concave gap minus the affine interpolation
of its values at the subinterval endpoints. On either outer interval,
this subtracts a nonnegative quantity from a gap already at most
`epsilon`. On the middle interval, it subtracts exactly `epsilon`,
again leaving at most `epsilon`. If no cut is required the bound
already holds. Concavity and continuity justify the two crossings,
including non-strict or flat maximum cases.

For a box error body, overlaying at most two cuts for each output
gives at most `2m+1` pieces per parity class. Further restriction of
an interval only lowers each convex function's local chord. On a
piece with chord `T`, both the exact graph and the entire band
`T_j-epsilon_j<=w_j<=T_j` have the stated box error: its error ranges
from `g_j-epsilon_j` to `g_j`, contained in `[-epsilon_j,epsilon_j]`.
The previously verified binary code construction applies to these
bounded polyhedral bands. Counting at most `(2m+1)*2^p` bands proves
`p_bin<=p_conv+ceil(log2(2m+1))`.

For `K={e:A|e|<=b}` with `A>=0`, the component bound implies
`A g(x)<=2 A g(mid)<=2b`. Each row of `AF` is convex, and its chord
gap is exactly that row of `A g`. Two successive scalar refinements
reduce its maximum first to `b_k`, then to `b_k/2`; at most nine
intervals, hence eight cuts, suffice for that row. Overlaying all
row cuts yields at most `8q+1` intervals per parity class. Restriction
preserves every previous row bound.

On each final interval, `g>=0` and `A g<=b/2` imply `g in K/2`.
The band `w-T in K/2` contains the graph because `F-T=-g`, and
its admitted error is `(w-T)+g in K/2+K/2=K`. Symmetry and convexity
justify this last equality. Nonnegative `A` makes the usual continuous
absolute-value auxiliaries an exact linear representation. Compactness
of `K` makes each band bounded. Binary coding therefore proves
`p_bin<=p_conv+ceil(log2(8q+1))` with no hidden integer auxiliaries.

The extra half-body step is necessary for this proof: two arbitrary
vectors from the nonnegative part of a coupled unconditional body
need not have their difference in that body. The stated unit-l1-ball
example verifies the failure of that shortcut. Neither reviewed
upper bound asserts rational knot construction, polynomial formulation
size, or necessity of its output-dependent overhead. They preserve,
rather than resolve, the open additive-constant target for arbitrary
positive polynomial vector outputs.
