# NP membership for linear fibers with a fixed number of parameters

Date: 2026-09-05. Status: two independent mathematical reviews PASS.
Novelty is unclaimed.

This note gives an NP upper bound complementary to the stronger polynomial
algorithm requiring fixed block dimensions. Here the linear fiber may
have arbitrarily many coupled variables and constraints.

**Lemma.** Fix the number `r` of real parameters. Consider
feasibility of

```
q in Q subset R^r,
A(q)x <= b(q),     x in R^n,
```

where `Q` has a rational polynomial inequality description, `A,b` have
rational polynomial entries, and all polynomials are explicitly represented
with polynomially bounded degree and coefficient encoding length. Assume
each nonempty fiber in `x` is bounded. Then feasibility is in NP.
An additional linear objective threshold can be included among the rows.
The dimension `n` and number of rows are unrestricted.

**Proof.** If feasible, choose a parameter value `q` with nonempty fiber.
Its closed bounded polyhedron has a vertex. At that vertex, `n` active
inequality normals contain a linearly independent subset, even if the
fiber is lower-dimensional; otherwise a nonzero direction orthogonal to
all active rows permits a sufficiently short feasible segment through
the point, contradicting extremality.

A certificate guesses the indices of these `n` rows. Let `B(q)` be their
square coefficient matrix and `d(q)` their right-hand vector. Define

```
D(q)=det B(q),
N(q)=adj(B(q)) d(q).
```

The certificate is accepted exactly when the following system in the
fixed `r` real variables is feasible:

```
q in Q,
D(q)^2 > 0,
[ A_j(q)N(q) - b_j(q)D(q) ] D(q) <= 0   for every row j.    (V)
```

When `D!=0`, the reconstructed point is `x=N/D`, and the last condition
is equivalent to `A_j x<=b_j`, because it multiplies that inequality by
the strictly positive `D^2`. Thus acceptance produces an actual feasible
point; the certificate need not identify its parameter coordinates or
encode arbitrary algebraic flow values.

If entry degrees are at most `d`, determinants and Cramer numerators have
degree at most `nd`; verification polynomials have degree `O(nd)`.
Because `r` is fixed, a dense polynomial of degree `O(nd)` has only
`O((nd+1)^r)` monomials. The determinant coefficients have polynomial
bit length: each coefficient is a sum of at most factorially many products
of `n` input coefficients and monomial terms, whose logarithmic count is
polynomial in the explicit input size. They can be computed in polynomial
time, for example by exact determinant evaluation on a sufficiently large
integer grid followed by multivariate interpolation. At fixed `r`, both
the grid size and evaluation bit lengths are polynomial. Apply the same
argument to the `n` Cramer determinants forming `N`.

Feasibility of (V), a rational semialgebraic system in fixed real dimension
with polynomially many explicitly represented coefficients and polynomial
degree, is decidable in polynomial bit complexity by established
fixed-dimension real-algebraic algorithms. The row-index certificate has
polynomial length, and its verification is polynomial. This proves the
NP upper bound. If `n=0`, direct fixed-dimensional feasibility suffices. □

Equalities may be represented as opposite inequalities. The bounded-fiber
assumption is satisfied when finite flow upper bounds are explicit. It can
also be replaced by a separately proved existence of a suitable basic
feasible solution, but that generalization is unnecessary here. Merely
having a fixed number of parameters does not imply a polynomial algorithm:
the nondeterministic choice of basis can have exponentially many options.

## Pooling consequence

For fixed numbers `p` of pools and `k` of quality coordinates, the
standard pooling decision problem with rational data and finite flow
bounds is in NP, including arbitrary direct input-output arcs and lower
flow bounds. Use the `pk` pool qualities as `q`. Once they are fixed,
all pool blending equations, output quality constraints, flow bounds,
conservation equations, and a linear cost threshold are linear in flows.
Their coefficients have degree at most one in `q`.

Pool quality coordinates can be bounded between the minimum and maximum
input values of the corresponding quality. Active pools obey these bounds
by blending. Inactive pools can be assigned arbitrary values in the same
interval; their qualities do not affect output constraints. A pool with
no input route is inactive and can be given any fixed quality. Thus the
parameter domain has a rational fixed-dimensional description. The fibers
are bounded because all flows have finite bounds.

The same conclusion holds with a fixed affine rank `t` of the input-quality
vectors in place of fixed attribute count `k`. The number of attributes
may then be unrestricted. Use the independently reviewed rational
[quality-coordinate reduction](pooling-bypass-structure-algorithm.md#2-compress-the-quality-coordinates-exactly):
write each input vector as `C_i=C_0+B a_i`, with `B` having `t`
independent rational columns. Represent each active pool by `t` mixture
coordinates, bounded by the coordinatewise minima and maxima of the
`a_i`. Mass balance and these `t` quality balances imply every original
attribute balance. Each output attribute constraint substitutes its own
affine expression `C_0a+B_a q_ell`, so all constraints remain linear in
flows once the `pt` parameters are fixed. Inactive pools can receive any
boxed coordinates. The rational coordinate transformation has polynomial
bit complexity, and the preceding lemma applies with `r=pt`, without
any restriction on the bypass graph. Empty-input instances are checked
directly. This corollary is a composition of the reviewed coordinate
reduction and the lemma, rather than a new real-algebraic argument.

There is a second parameterization when the number `J` of outputs is
fixed together with `p`: use pool output fractions `theta_lj` as the
at most `pJ` parameters. For each pool with outgoing arcs, these fractions
are nonnegative and sum to one over those arcs. Let its total intake be
`T_l=sum_i y_il`; its output flow is `theta_lj T_l`. The quality mass
it sends to output `j` in attribute `k` is
`theta_lj sum_i C_ik y_il`. At fixed fractions, all output specifications,
input/output/pool/arc capacities, lower flow bounds, conservation equations,
and the linear objective threshold are linear in intake and direct-bypass
flows. Their coefficients are affine in the fractions. A positive-flow
physical pool has precisely this parameterization; an inactive pool may
choose any split vector. A pool without outgoing arcs has zero intake;
check its pool and incident-arc lower bounds against zero, rejecting the
instance if they require positive flow, before removing that pool and
its incident arcs. Finite bounds make the remaining fibers compact.
Consequently fixed `p,J` pooling is in NP even with unrestricted input
count, attribute count, affine quality rank, and bypass graph. This proves
an upper bound rather than a polynomial algorithm: the fiber basis is
still guessed. The two-pool/two-output hardness construction therefore
is therefore NP-complete. The original two independent reviewers checked
this output-fraction parameterization and the affine-rank corollary; the
first identified the required zero-flow check before removing pools.

Combining this lemma with the independently reviewed bypass-copy
hardness construction gives NP-completeness for one pool and two upper-
bound quality coordinates with exact supply/demand contracts and arbitrary
bypasses. With the convention counting one physical quality with lower and
upper specifications as one coordinate, it gives the corresponding
one-quality statement. It does not assert NP membership when both the
number of pools and affine quality rank are unrestricted, and it does not upgrade ordinary hardness to
strong hardness.

The only tools used here are basic LP vertex theory, Cramer's rule, and
fixed-dimensional real algebra. Basu's
[author survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf),
Theorem 2.18 on PDF page 13, states the quantifier-elimination arithmetic
complexity and intermediate coefficient bit bounds. With one quantified
block of fixed size `r` and no free variables, those bounds are polynomial
in the number of polynomials, degree, and input coefficient bit size. The
primary algorithmic paper is Basu, Pollack, and Roy,
[*On the combinatorial and algebraic complexity of quantifier elimination*](https://www.math.purdue.edu/~sbasu/jacm95.ps).
These are also the established tools used in the repository's
[fixed-core constructive theorem](fixed-core-block-polyhedral-optimization.md).
Independent reviews: [first](../notes/review-fixed-parameter-lp-np-membership.md),
[second](../notes/review-fixed-parameter-lp-np-membership-second.md). Both PASS. The
[novelty search](../notes/pooling-fixed-quality-np-membership-novelty.md) records no
matching exact predecessor found; the proof is presented as a standard
structural upper bound, with novelty unclaimed.
