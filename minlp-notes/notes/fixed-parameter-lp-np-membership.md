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

Combining this lemma with the independently reviewed bypass-copy
hardness construction gives NP-completeness for one pool and two upper-
bound quality coordinates with exact supply/demand contracts and arbitrary
bypasses. With the convention counting one physical quality with lower and
upper specifications as one coordinate, it gives the corresponding
one-quality statement. It does not assert NP membership for unrestricted
pool and quality counts, and it does not upgrade ordinary hardness to
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
[fixed-core constructive theorem](../results/fixed-core-block-polyhedral-optimization.md).
Independent reviews: [first](review-fixed-parameter-lp-np-membership.md),
[second](review-fixed-parameter-lp-np-membership-second.md). Both PASS. The
[novelty search](pooling-fixed-quality-np-membership-novelty.md) records no
matching exact predecessor found; the proof is presented as a standard
structural upper bound, with novelty unclaimed.
