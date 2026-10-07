# Independent review of affine repair for regridded certificates

Date: 2026-10-02. Verdict: no blocking mathematical issue in the reviewed
[affine-repair exploration](../new-direction/affine-repair-exploration.md).
The result proves a sufficient extension for box-preserving affine
retractions. It does not prove an extension to arbitrary affine constraints
intersected with a box, or to general inequalities.

I read the author's note, the unconstrained regridding proof, and the
underlying decomposition-certificate definitions. I independently derived
the cancellation and drift estimates before reading the completed author
note. A delegated check separately audited the dynamics example. I did
not read other review reports or conduct a literature search.

## Multiplier identity and repair estimate

The author's broader affine-retraction formulation is valid. If
`R(x)=Lx+d` maps the ambient space into `Ax=b` and fixes that affine
space, then `L` fixes `ker A`, `L^2=L`, and `Ld=0`. Therefore
`(L^T-I) grad F(c)` belongs to `range(A^T)`, even if the constraint rows
are redundant. The multiplier equation is solvable with the stated sign.

For the right-inverse special case `R(x)=x-K(Ax-b)`, `AK=I`, the explicit
choice is `mu=-K^T grad F(c)`. The adjusted global gradient is then
`(I-KA)^T grad F(c)`, which annihilates `x-R(x)`. No multiplier-size bound
is needed for the exact-arithmetic argument.

Adding each assigned multiplier term to its own bag changes the bag
gradient but vanishes at every locally feasible configuration point and
at every repaired point. It also changes no Taylor remainder, because
the added term is affine. Applying the existing separator telescoping
identity to these adjusted gradients gives precisely equation (3.2).
The sign of the separator correction and the multiplier equation both
check out. Feasibility of the center is useful for the iteration and
incumbent, but cancellation does not require stationarity of that center.

The residual estimate uses each constraint row once, in its assigned bag:

```
||Ax-b||^2 <= (max_t ||A_t||)^2 E_x.
```

The top-copy representative is in the original box. Box preservation
therefore makes its repair feasible. Stacking the bag restrictions of
`x-y` costs at most `sqrt(k)`, so Minkowski's inequality yields

```
E_y <= (1+sqrt(k) H max_t ||A_t||)^2 E_x <= D Q.
```

The repaired point need not remain in the selected leaves or separator
cells. The proof requires only its membership in the full box. In the
grading calculation, the bag-plus-separator copy-error sum is at most
`2E_y`; equality would generally be false because repair can alter
private coordinates. The author states this distinction correctly.

These observations justify replacing `C0` by `D` in both inequalities
that drive the original contraction proof. Quadratic growth is applied
only to the feasible repaired point. The consistent configuration at a
feasible optimizer supplies `LB<=f*`, so the contraction and computable
gap estimate follow without a further feasibility-error term.

## Infeasible cells and computational scope

Infeasibility flags are a necessary extension of the original certificate
definition, which used finite affine minorants on every cell. With those
flags, the constrained dynamic program remains valid:

- A local pair with empty box/equality intersection has value `+infinity`.
- A child cell with no finite configuration has no feasible actual
  subtree at any separator point in that cell. It can be ignored when
  minimizing finite child intercepts.
- If every child cell meeting a parent leaf is flagged, the parent leaf
  cannot contain a feasible full solution and can also be flagged.
- A globally feasible optimizer supplies a finite configuration, so the
  root minimum is finite and attained.

Finite local problems have compact feasible sets and continuous convex
objectives, as in the inherited assumptions. The oracle contract should
be read as including a correct report of infeasibility, as well as a value
and attaining point for every nonempty local problem. Stating that
contract in one explicit sentence would remove any ambiguity.

Intersecting a pair with its assigned equalities creates no extra
bag/separator incidences, so the stated bounds on boxes and local oracle
calls are unchanged apart from the grading constant. Full arithmetic
complexity also includes evaluating and applying the repair, assembling
the global gradient, and obtaining multipliers. Those costs need not be
linear for a general dense retraction. The author's explicit scope
paragraph correctly avoids claiming such a bound. Redundant or numerous
constraint rows and their input costs likewise remain outside the box
and oracle-call counts.

## Dynamics example

For the convention `A_t x=s_(t+1)-a s_t-b u_t`, forward repair has errors
`e_0=0`, `e_(t+1)=a e_t-r_t`. The geometric convolution estimate gives
`H<=1/(1-|a|)` in Euclidean norm. The coefficient condition preserves
the full box, and `||A_t||=sqrt(1+a^2+b^2)`. The displayed backward
multiplier recurrence has the correct sign and makes every noninitial
state component of the adjusted gradient zero. Its remaining components
equal `L^T grad F(c)`. All these operations take linear arithmetic work
in the horizon.

For the objective in Section 4, assign the initial-state square to the
first bag and each later state square to its preceding transition bag.
Then `F>=3||x||^2/4`, with unique feasible minimizer zero. Each bag Hessian
has eigenvalues in `[-1,2]`, so `M=2`. Keeping the state squares exact and
using alphaBB coefficient `1/2` on each unary control factor gives
`A0=1/2`. All constants are independent of the horizon for the fixed
choice `a=b=1/2`.

That choice is nonconvex even after restricting to the feasible set.
Keep all earlier variables zero and vary the final control and final
state together. The restricted objective is
`(5/4)u^2-u^4/4`, whose second derivative at `u=15/16` is `-35/256`.
This verifies the stronger claim beyond ambient nonconvexity of a factor.
The general coefficient conditions alone would not ensure that claim:
`a=0,b=1` instead makes the reduced objective convex.

One minor wording correction is appropriate: the path has occurrence
bound `k<=2`; its actual maximum is `k=1` when the horizon is one. Using
the upper bound two in every displayed theorem constant is valid.

The example has an explicit optimizer and illustrates the theorem's
nonconvex constrained class. It does not by itself establish computational
hardness, a separation from other algorithms, or a novelty claim. The
author does not make those claims.

## Targeted verification

The command actually run was

```
python research-20261002/reviews/affine-repair-review-check.py
```

It passed 300 exact rational configuration-identity checks, with horizons
`1,2,3,7,12` and positive, negative, or zero state coefficient. The same
instances passed the residual, repair, and stacked-drift bounds. The
nonconvexity calculation above was checked exactly. Results are in
[`affine-repair-review-check.json`](affine-repair-review-check.json).
These checks support the algebra; they do not implement the constrained
dynamic program or establish its end-to-end runtime. No project-wide
verification or CI checks were run.
