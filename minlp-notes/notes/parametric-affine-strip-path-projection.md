# Polynomial elimination for affine interval transitions on a path

Date: 2026-09-05. Status: independently reviewed supporting lemma by root. No novelty claim. This is a direct use of difference constraints,
recorded as an alternative to the specialized pooling flow transformation.

Let t have a fixed number of real coordinates. Consider a scalar path
x_0,...,x_n with rational polynomial coefficient functions and constraints

```
l_i(t) <= x_i <= u_i(t),
a_i(t) x_(i-1)+b_i(t) <= x_i <= a_i(t) x_(i-1)+c_i(t).
```

All bounds are finite. Polynomial degrees may grow under dense encoding.
On any supplied sign cell for the a_i, the path has a polynomial-size
semialgebraic projection onto t and its two endpoints. The polynomial
degrees and coefficient bit lengths of this description are polynomial in the
input size. With fixed-dimensional t, enumerating realizable sign cells
and combining this projection with fixed-dimensional polynomial constraints
therefore gives a polynomial bit-time exact feasibility algorithm, and
exact infimum and attainment analysis for an objective on the retained
coordinates. A returned optimizer is claimed only when the infimum is
attained, for example on a nonempty compact closed original feasible set.
Arbitrary dense
objectives or aggregate constraints involving eliminated states are excluded.

## Nonzero gains reduce to ordinary difference constraints

First assume all a_i are nonzero on the cell. Put

```
A_0=1, A_i=product_(h=1)^i a_h, y_i=x_i/A_i.
```

The transition becomes

```
alpha_i <= y_i-y_(i-1) <= beta_i,
```

where alpha_i and beta_i are b_i/A_i and c_i/A_i in the order specified
by the known sign of A_i. Likewise every coordinate interval becomes
L_i<=y_i<=U_i, with the order reversed when A_i<0. Require every lower
bound to be at most its upper bound. All quantities are rational functions
with polynomial degree and coefficient encoding length. Products of the
input denominators and gains have polynomial degree and bit length; their
signs are fixed on the current cell.

For i<j define directed path lengths

```
d(i,j)=sum_(h=i+1)^j beta_h,
d(j,i)=-sum_(h=i+1)^j alpha_h,
d(i,i)=0.
```

Each two-edge directed cycle has nonnegative length because alpha<=beta.
Every walk on a bidirected path reduces to the unique simple path plus
such nonnegative excursions. Thus d is the directed shortest-path distance.
The bounded difference system is feasible exactly when

```
L_i <= U_j+d(j,i)        for every i,j.                (1)
```

Necessity follows by summing transition inequalities. For sufficiency set

```
y_i=min_j (U_j+d(j,i)).
```

Condition (1) gives y_i>=L_i, and j=i gives y_i<=U_i. The directed triangle
inequality gives y_i<=y_h+d(h,i), so in particular all adjacent transition
inequalities hold. This proves sufficiency and gives exact recovery.

To project onto x_0,x_n, replace the coordinate intervals at those nodes
by their fixed prospective values y_0=x_0 and y_n=x_n/A_n. Keep the original
endpoint bounds as separate inequalities. Formula (1) then gives only
O(n^2) inequalities in t,x_0,x_n. Clear denominators using their known signs.
The resulting polynomial degrees and coefficient bit lengths remain
polynomial. The recovery formula uses rational arithmetic and minima in
the same real algebraic field as the retained coordinates.

## Zero gains and sign cells

If a_i=0 on a sign cell, its transition is simply b_i<=x_i<=c_i and imposes
no relation on x_(i-1). Split the path there and intersect the new interval
with the ordinary coordinate interval by keeping both sets of bounds.
For each resulting subpath apply the preceding construction. Components
with no retained endpoint are tested for feasibility; components with one
or two retained endpoints give the corresponding projection. Multiple
bounds at a coordinate may be represented by all lower/upper pairs in (1),
so no additional choice of an active maximum or minimum is necessary.

For fixed-dimensional t, a sign-invariant semialgebraic decomposition for
polynomially many input gains has polynomial complexity in the dense input
size, with an exponent depending on that dimension. Lower-dimensional and
zero sign cells must be retained. This is an established fixed-dimensional
real-algebraic operation, not a new algorithm claimed here.

## Relevance and limitations

An exactly contracted two-input scalar-quality output is a deterministic
affine transition away from concentrations equal to its input qualities.
An exactly supplied degree-two input is an interval transition of slope -1.
Thus these pooling paths have more structure than arbitrary two-variable
inequalities. Their endpoint elimination need not inherit the more general
quasipolynomial bound. The separate transformed-flow proof may give a
simpler description and lower algebraic degrees for that particular model.

This note does not permit an arbitrary two-variable polygon at each step:
both transition bounds must have the same gain a_i. Nor does it eliminate
a dense accumulated cost. The difference-constraint normalization and
shortest-path feasibility principle are classical; the purpose is to retain
the precise parameter and endpoint encoding argument for future use.

## Independent verification

The [full audit](review-parametric-affine-strip-path-projection.md) passed,
including negative and zero gains, same-field recovery, and fixed-dimensional
sign-cell complexity. Its exact checker compares 1,200 rational systems
against independent forward interval propagation in the original variables;
all decisions and recovered witnesses passed. The audit also gives a
single common-prefix denominator bound and checks the relevant primary
real-algebraic algorithm statements. No novelty claim is added.

## Reviewed tree and fixed-cycle-rank corollaries

The difference-constraint proof does not depend on maximum degree two.
Suppose the gain-interval constraints are placed on an arbitrary tree,
with arbitrary original edge orientations. Delete each zero-gain edge
after imposing its interval b_e<=x_v<=c_e at its original head v.
For a nonzero original edge u->v choose normalization factors satisfying
A_v=a_e A_u. Rooting each remaining tree assigns these factors as products
of gains and reciprocal gains along root paths. Dividing x_v by A_v
therefore gives a bounded difference constraint y_v-y_u, with bound order
chosen from the sign of A_v. No zero-gain row is silently reversed.
The transformed system is bounded difference constraints on a bidirected
tree. A common product of nonzero gains, together with coefficient
denominators, clears all rational functions with polynomial degree and
coefficient bit growth.

There is a unique simple path between any two vertices; every directed
walk reduces to that path plus nonnegative two-edge excursions. Define
d(u,v) by summing the upper difference bounds in the direction from u
to v. The same O(N^2) inequalities L_v<=U_u+d(u,v) characterize feasibility,
and y_v=min_u(U_u+d(u,v)) recovers a feasible assignment. Retaining any
specified fixed number of states replaces their intervals by exact values
and gives a polynomial-size projection onto those states and the fixed
parameter vector. Branching creates no new disjunctions or products of
candidate bounds. Prefix products, path sums, and denominator clearing
have polynomial degree and coefficient bit length.

More generally, let the undirected interaction graph have fixed total
cycle rank c. Remove c edges to obtain a spanning forest and retain both
endpoints of every removed edge, along with any original objective states.
There are at most 2c additional retained states. Project the forest by
the preceding argument and put the removed original gain-interval rows
back as constraints on these retained states. The remaining dimension
is fixed when the parameter dimension, c, and the number of original
retained states are fixed. Fixed-dimensional real-algebraic optimization
therefore supplies polynomial bit-time feasibility, exact infimum and
attainment analysis for continuous parameters and objectives depending only
on retained coordinates. It returns an optimizer when one exists. Pointwise
finite state bounds alone do not bound the parameter domain or imply
attainment; compact closed original feasible sets suffice.

This is a direct structural corollary, not a new general difference-
constraint algorithm. It does not cover arbitrary two-variable polygons,
dense state objectives, discrete local transitions, or fixed maximum
block rank in place of fixed total cycle rank. The [independent corollary audit](review-parametric-affine-strip-tree-cycle-rank.md)
passed after explicitly clarifying original edge directions and the
infimum-versus-attainment distinction.
