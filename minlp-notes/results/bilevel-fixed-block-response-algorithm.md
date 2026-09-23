# Fixed-dimensional quadratic follower blocks

Date: 2026-09-05. Status: independently reviewed theorem.
[First independent audit](../notes/review-bilevel-fixed-block-response.md) and
[second independent audit](../notes/review-bilevel-fixed-block-response-second.md).
The scalar theorem has two independent full audits and a separate
bit-complexity audit, linked from its result file.
This extends [the scalar response theorem](bilevel-fixed-aggregate-response-algorithm.md)
from individual rates to fixed-dimensional local operating decisions.
The additional argument is rational elimination of a strictly convex local
quadratic program through independent active normals. That local technique
is classical; the proposed contribution remains its use in exact global
nonconvex bilevel response optimization.

## Statement

Fix leader dimension `r`, maximum local block dimension `d`, aggregate
row count `s`, and shared resource row counts `k_eq,k_in`. Let the follower
variables be `z=(z_1,...,z_B)` with `z_b in R^(d_b)`, `d_b<=d`; both the
number of blocks and total follower dimension may grow.

For each block let

```
P_b(x)={z_b: E_b z_b=e_b(x), G_b z_b<=h_b(x)}.
```

The matrices `E_b,G_b` are rational and independent of the leader. Their
numbers of rows may grow. Include finite polynomial lower and upper bounds
on every coordinate among the inequalities, valid for every leader
`x in C`, with `C` compact. Inconsistent local fibers are permitted.
The follower additionally obeys fixed-count shared rows

```
A z=b(x), H z<=d(x),
```

with fixed rational matrices `A,H`. Its objective is

```
f(x,z)=sum_b [z_b^T Q_b(x) z_b/2+c_b(x)^T z_b]
       +phi(x,U(x)z),
```

where each symmetric polynomial matrix `Q_b(x)` is positive definite on
`C`, `U(x)` has `s` rows, and `phi` is any polynomial, possibly nonconvex.
All data have the explicit polynomial representation and polynomial-degree
encoding condition in the scalar theorem. Upper constraints and objective
are arbitrary explicitly supplied polynomials under the same condition.

**Theorem.** Exact optimistic bilevel feasibility and attained
global optimization are polynomial in rational input bit length for these
fixed dimensions. An exact optimizer and value admit polynomial-size
representations in one common real-algebraic field.

The number of rows in a block is not a parameter. The fixed local dimension
is what bounds the size of the active normal subsets needed below.

## 1. Local rational response list

Use the same global compressed coordinates

```
v=(x,w,lambda,mu),  w=U(x)z,
```

as in the scalar theorem. For each block define its effective linear cost

```
q_b(v)=c_b(x)+U_b(x)^T grad_w phi(x,w)
                 +A_b^T lambda+H_b^T mu.
```

A follower KKT point satisfies, within every block, the optimality
conditions of the strictly convex quadratic program

```
min {y^T Q_b(x)y/2+q_b(v)^T y: y in P_b(x)}.       (1)
```

The global objective need not be convex. The block assertion follows
because the global gradient and the gradient in (1) agree at the proposed
point. For fixed `v`, (1), when feasible, has exactly one minimizer because
of positive definiteness and boundedness of the local polytope.

Choose once an independent row basis `Ebar_b` of `E_b`, of rank `t_b<=d_b`,
and retain all original equality rows as feasibility tests. Enumerate
subsets `J` of inequality rows such that the rows of

```
V_J=[Ebar_b; (G_b)_J]
```

are independent. Then `|J|<=d_b-t_b`, so there are at most
`sum_{j=0}^{d_b-t_b} binom(m_b,j)` choices, polynomial since `d` is fixed.
For each such subset solve

```
[Q_b(x)  V_J^T] [y    ] = [-q_b(v)]
[V_J       0 ] [theta]   [rho_J(x)],              (2)
```

where `rho_J` contains the corresponding equality and active inequality
right-hand sides. The matrix in (2) is nonsingular for every `x in C`:
if `Q_b y+V_J^T theta=0` and `V_J y=0`, multiplication by `y^T` gives
`y^T Q_b y=0`, so `y=0`, then `theta=0` by row independence.

Cramer's rule therefore gives rational functions of `v`. Replace the
possibly signed determinant denominator `Delta_J` by `Delta_J^2>0`,
multiplying every Cramer numerator by `Delta_J`. Denote the positive
polynomial denominator by `D_J` and the resulting vector numerator by
`Y_J`. The formula is a valid local response exactly when its candidate
satisfies every original local equality and inequality and the components
of `theta` corresponding to inequality rows are nonnegative. All these
tests become polynomial conditions after multiplication by `D_J`.

Every feasible local optimizer appears in this list. Indeed, the
polyhedral normal cone gives its negative gradient as an equality-normal linear
combination plus a nonnegative combination of active inequality normals.
In the quotient by the equality row space, the conic combination can be
chosen with linearly independent generators: if its positive-support
generators are dependent, move their coefficients along a dependence,
choosing the sign and step so coefficients remain nonnegative and at least
one positive coefficient vanishes; repeat. The lifted rows together with
`Ebar_b` are then independent and number at most `d_b`. These are one of
the enumerated subsets `J`. Their stationarity system is (2).

Conversely, every feasible branch with nonnegative inequality multipliers
satisfies the sufficient KKT conditions for the strictly convex problem
(1). Thus all valid branches at the same `v` return the same `y`. No
uniqueness of multipliers or nondegeneracy of the polytope is needed.

## 2. A polynomial number of global response regimes

Let `delta` bound actual input degree. The matrices in (2) have size at
most `2d`. Their determinants, adjugates, numerators, and all feasibility
tests have degree `O(d delta)` in the fixed-dimensional vector `v` and
polynomial coefficient bit length. Across all blocks and active subsets,
the number of these test polynomials is polynomial in the original input
for fixed `d`.

Enumerate their realizable sign conditions, including zero signs. Their
number and enumeration cost are polynomial because ambient dimension is
fixed. Within one sign condition, validity of every block branch is fixed.
Discard the condition if any block has no valid branch; otherwise choose
the first valid branch in a fixed ordering for each block. This rule loses
no point because all valid branches of a block give its same unique local
response. It avoids enumerating a Cartesian product of the branch lists.

On one resulting regime each block is a rational function of `v` with a
positive denominator. Taking the product `Q` of the selected block
denominators produces common polynomial numerators for all follower
coordinates. Their degrees and expanded bit sizes are polynomial: there
are polynomially many factors of polynomial degree in fixed dimension.

Add `w=U(x)z`, shared resource feasibility and complementarity `mu>=0`,
`mu_j((Hz)_j-d_j(x))=0`, and the follower value equation. Clearing the
positive common denominator produces a polynomial-size fixed-dimensional
formula `E(v,tau)` for precisely the feasible follower KKT points and their
values.

## 3. Global response, upper optimization, and attainment

Every global follower minimizer has multipliers for its fixed-normal
polyhedral feasible set, hence has a compressed representation above.
Every represented point is follower-feasible. Thus the same quantified
comparison as in the scalar theorem is exact:

```
E(x,w,lambda,mu,tau)
AND forall w',lambda',mu',tau':
   E(x,w',lambda',mu',tau') implies tau<=tau'.
```

Only the global compressed coordinates are quantified; the number of
blocks and their active subsets do not add variables. Substituting the
common rational response into the upper polynomials, with positive
denominator clearing, gives a polynomial-size formula in a fixed total
number of variables. Fixed-dimensional quantifier elimination and
algebraic sampling return feasibility, exact optimum, and a common-field
optimizer in polynomial bit time.

The full follower matrix, including all local and shared rows, is fixed
with respect to the leader. Although its size grows with the instance,
Hoffman's bound is uniform in its right-hand side for each instance. The
same limiting argument as in the scalar theorem shows the global response
graph is closed. Continuous coordinate bounds on compact `C` give uniform
boundedness. The optimistic feasible graph is therefore compact, and a
continuous upper polynomial attains its minimum whenever feasible.

## Attribution and scope

[Megiddo and Tamir (1993), Section 4](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf)
already eliminate fixed-dimensional convex quadratic blocks with local
polyhedral constraints in a fixed resource-multiplier space. Their
single-level convex construction fixes local row counts as well; the
present polynomial-time enumeration allows those counts to grow while
keeping block dimension fixed. Their construction is a direct antecedent
of the local
active-normal lists. The present proof adds polynomial leader dependence,
a fixed-dimensional possibly nonconvex aggregate term, and quantified
comparison of all global stationary candidates for exact bilevel
optimization. No claim is made that active-set enumeration, local
quadratic elimination, or quantifier elimination is itself new.

Positive definiteness ensures a unique rational local response for each
compressed coordinate vector. Replacing it by arbitrary convex local
polynomials reintroduces the sum-of-square-roots arithmetic barrier in
[the scalar theorem](bilevel-fixed-aggregate-response-algorithm.md).
Allowing block dimension to grow invalidates the polynomial active-subset
count. Allowing constraint normals to depend on the leader can destroy
attainment, as the scalar counterexample shows.

A process-design interpretation uses many operating units with a fixed
number of coupled local decisions each, such as throughput, utility use,
and recycle rate. Their local quadratic cost matrices may be dense within
a unit. Arbitrarily many local linear operating limits are allowed; the
number of shared resources, nonlinear aggregates, and leader parameters
stays fixed. This is a structural applicability statement, not a practical
solver-performance claim.
