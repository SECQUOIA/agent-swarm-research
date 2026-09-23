# Small exponents obstruct compact rational graph formulations

Date: 2026-09-05. Status: independently reviewed supporting theorem.
Two full proof audits and a bounded source comparison are complete.

A bound on integer dimension does not alone ensure a short rational
formulation. The following elementary LP certificate argument separates
these issues for concave powers with a small binary-encoded exponent.
The small-denominator property of rational LP solutions is classical.

## Statement

Let `D>=2` be an integer and let

```
f_D(x)=x^(1/D),       0<=x<=1.
```

Suppose a rational mixed-integer linear formulation, with any finite number
of continuous auxiliaries and unrestricted integer variables, projects to a
set `S` satisfying

```
{(x,f_D(x)):0<=x<=1} subset S
subset {(x,y):0<=x<=1, |y-f_D(x)|<=1/16}.              (1)
```

Write `s` for its ordinary explicit binary encoding length, counting all
rows, variables, and rational coefficients. Then

```
s >= Omega(D).                                (2)
```

The constant is universal under a standard explicit rational matrix encoding.
The bound uses total coefficient encoding, rather than a separate worst-case
height bound for each row. In particular, with `D=2^B`, no formulation of
size polynomial in `B` satisfies even this fixed absolute graph accuracy.
This holds regardless of its integer dimension and includes unbounded
integer coordinates. No lower bound against real-coefficient formulations
is asserted.

## Freeze an integer witness and solve a rational LP

The exact graph point `(x_*,y_*)=(2^(-D),1/2)` belongs to `S`. Choose one
integer witness `z_*` and continuous witness for that point, and fix all
integer coordinates to `z_*`. The remaining system is a rational polyhedron.
Add the rational inequality `y>=1/4` and minimize `x` over it.

The LP is feasible because it contains the chosen graph point. Its objective
is bounded below by zero by (1), so a finite optimum is attained. The optimal
value is strictly positive: if it were zero, attainment would give a
projected point with `x=0,y>=1/4`, whereas (1) forces `|y|<=1/16` at zero.
Consequently its optimal value `v` satisfies

```
0<v<=2^(-D).                                        (3)
```

The magnitude of `z_*` need not have any bound. The denominator estimate
below is independent of it.

## A positive rational LP optimum has a uniform denominator bound

Clear denominators separately in each original row and in the added
inequality. Let `ell_i` be the sum of numerator and denominator bit lengths
of the coefficients in row `i`, including the integer columns and right-hand
side, and let `t_i` count its nonzero coefficients. Their total is `O(s)`.
After multiplying that row by the product of its positive denominators,
its continuous coefficients are integers of magnitude at most `2^(ell_i)`.
The right-hand side after fixing `z_*` is integral. Its numerators may be
arbitrarily large; this does not affect the coefficient matrix.

Convert free continuous variables to differences of nonnegative variables,
add slacks, and remove dependent equations if necessary. Splitting at most
doubles each row's nonzero count; a slack contributes at most one more.
The Euclidean row norm is therefore at most

```
sqrt(2t_i+1) * 2^(ell_i).
```

A feasible LP with a finite optimum has an optimal basic feasible solution
in this standard form. Its basic coordinates have one common denominator
dividing the nonzero integer determinant of its basis matrix. The objective
`x`, possibly the difference of two basic coordinates, therefore has the
same denominator bound.

By Hadamard's inequality, every such determinant has binary logarithm at most

```
sum_i ell_i + (1/2)sum_i log2(2t_i+1) <= C s,         (4)
```

for a universal encoding constant `C`. Restricting to a basis only removes
rows or columns and cannot increase this row-norm estimate. The sum of
nonzero counts is bounded by the explicit encoding length, so the second
sum is also `O(s)`.

Since the optimal numerator is an integer and `v>0`,

```
v>=2^(-C s).                                        (5)
```

Large integer witnesses can enlarge the numerator but cannot enlarge the
basis determinant. Combining (3) and (5) gives `C s>=D`, proving (2).

The use of basic feasible solutions does not assume the original lifted
polyhedron has a vertex: splitting free variables and adding slacks gives
an equivalent standard-form LP with a pointed nonnegative feasible set.
A finite optimum is attained at a basic feasible solution there.

## Matching upper bound with four binaries

The order `D` in rational encoding is attainable at the same error. Set
`M=16` and use the 17 rational knots

```
a_j=(j/16)^D,       j=0,...,16.
```

For segment `j`, let `0<=theta<=1` and write

```
x=(1-theta)a_j+theta a_(j+1),
t=(j+theta)/16,
t<=y<=t+1/16.                                      (6)
```

The root function is concave, so `f_D(x)>=t`. Monotonicity also gives
`f_D(x)<= (j+1)/16 <=t+1/16`. Both the true graph value and every output in
(6) thus lie in an interval of width `1/16`. The segments cover the full
input interval because their increasing input endpoints run from zero to
one. Their union satisfies (1).

This union has a rational MILP with four declared binaries. For completeness,
assign each of the 16 segments its distinct four-bit code. Introduce continuous
selectors `lambda_j in [0,1]`, require `sum_j lambda_j=1`, and bound each
selector above by each matching bit literal of its code. When the four bits
are integral, every selector except the matching one is zero, so the matching
selector is one. Introduce `0<=v_j<=lambda_j` and set

```
x=sum_j [a_j lambda_j+(a_(j+1)-a_j)v_j],
t=sum_j [j lambda_j+v_j]/16,
t<=y<=t+1/16.
```

Only the selected segment contributes, with `v_j=theta`. The row and variable
counts are constant, and every knot coefficient has `O(D)` rational bits.
The total encoding length is therefore `O(D)`.

Combining the two directions gives total rational MILP encoding length
`Theta(D)` at fixed error, while four binaries suffice for every `D`.
The lower bound continues to hold when arbitrarily many integer variables
are allowed; changing their count cannot avoid this encoding obstruction.
The logarithmic disjunction encoding used in the upper bound is established.

## Scope and implications

- The exponent `1/D` has `O(log D)` binary length. The lower bound is
  exponential in that length even at fixed error `1/16`.
- This does not contradict compact pure-power formulations for exponents
  greater than one. Their sharp transition occurs near an endpoint at
  distances with manageable binary encoding. Here the point with output
  one half lies at `x=2^(-D)`.
- This does not contradict a short formulation with an exponentially tiny
  real coefficient treated as a unit-cost input. Rational bit length is
  the central restriction.
- Fixing the exponent, excluding a neighborhood of zero, or permitting a
  larger error changes the question. No claim for those regimes is made.
- The proof applies more generally whenever a graph tube excludes
  `(0,y>=a)` but exact coverage forces some `y>=a` at a positive input
  much smaller than any rational LP basis denominator permits.
- Mixed-integer convex formulations with nonlinear constraints are outside
  this rational MILP size lower bound. For example the hypograph of this
  concave power is convex, though its full narrow graph tube is a different
  set.

The rational-LP determinant argument is established. This note retains its
specific consequence for sparse exponent encoding; source novelty is pending.


The first independent reviewer identified the sharper row-wise determinant
accounting used here; the original draft used a weaker `2^{O(s^2)}` bound.
Both bounds already exclude polynomial encoding in `log D`, but the
row-wise estimate gives the displayed linear lower bound in `D`.


## Review and attribution

Both the [first full audit](review-small-exponent-rational-formulation-barrier.md)
and [second full audit](review-small-exponent-rational-formulation-barrier-second.md)
passed through the final tight `Theta(D)` statement and four-binary upper
construction. The [bounded source assessment](small-exponent-rational-formulation-barrier-novelty.md)
identifies classical rational-LP denominator bounds as the proof mechanism.
It found no matching fixed-error small-power formulation statement in the
sources checked; this is not proof of publication priority.

The [twice-reviewed conic separation](../results/small-exponent-milp-soc-encoding-separation.md)
gives polynomial-size second-order cone formulations for `D=2^B`, with the
same four-binary count. Exact conic feasibility and explicit rational
encoding are essential to that comparison.
