# Second independent review: NP membership with fixed real parameters

Date: 2026-09-05. Verdict: **PASS**. Novelty is not claimed for this
standard-structure upper bound.

Reviewed: [fixed-parameter LP lemma](fixed-parameter-lp-np-membership.md),
including its pooling consequence. This review was requested while auditing
the bypass-copy hardness construction.

## Certificate and exact verification

For any parameter point with a nonempty bounded fiber, that fiber is a
closed bounded polyhedron and has an extreme point. At an extreme point,
active normals span the entire ambient flow space: otherwise a sufficiently
small segment in an orthogonal direction remains feasible in both directions.
This argument also covers lower-dimensional fibers and singletons.

Hence `n` active rows have a nonsingular square matrix at that parameter
point. Their indices are a certificate of length at most `O(n log M)`.
Although there can be exponentially many candidate bases, an NP verifier
checks only the guessed one. An objective threshold must be included in
the fiber before selecting its vertex; the lemma explicitly allows this.
Intersecting with that additional halfspace preserves boundedness.

For the guessed basis, Cramer's rule gives `x=N(q)/D(q)` whenever
`D(q)!=0`. For every original row, the correct denominator-cleared test is

```
[A_j(q)N(q)-b_j(q)D(q)] D(q) <= 0.
```

It multiplies the original residual by `D(q)^2`, so the inequality direction
is correct regardless of the sign of `D`. The separate test `D^2>0`
rejects the singular locus. Acceptance is therefore equivalent to existence
of a genuine feasible point for this basis. The verifier does not need a
certificate encoding the real parameters themselves or all flow coordinates.

## Polynomial determinant construction

Let the input coefficient degrees be at most `d`. A basis determinant
and each Cramer numerator have total degree at most `n*d`; the verifier
polynomials have degree at most `(2n+1)*d`. By hypothesis these quantities
are polynomial in the input length, and the parameter count `r` is fixed.
Thus each dense coefficient array has polynomial length.

The coefficient-height argument is also valid. Each determinant coefficient
is a sum of products of `n` original coefficients. The number of terms is
bounded by `n!` times a polynomial-monomial-count factor raised to `n`;
the logarithm of that number is polynomial. Clearing rational denominators
first has polynomial bit cost. Determinant coefficients consequently have
polynomial bit length despite the factorial number of formal terms.

For an explicit construction, evaluate on the tensor grid
`{0,...,n*d}^r`. Its size is polynomial at fixed `r`, and all evaluations
have polynomial bit length. Compute ordinary rational determinants at
these grid points and interpolate one coordinate at a time. The interpolation
matrices, their determinants, and recovered coefficients have polynomial
bit length. The same procedure applied to the `n` column-replacement
matrices computes every Cramer numerator. Thus the argument does not
merely bound the output size; it gives a polynomial method to obtain it.

After these constructions the acceptance test is a semialgebraic feasibility
problem in exactly the fixed number of real parameters, with polynomially
many explicit polynomials of polynomial degree and coefficient length.
Fixed-dimensional real-algebraic decision gives polynomial verification.
The relevant quantifier-elimination and bit bounds in
[Basu, Pollack, and Roy's primary paper](https://www.math.purdue.edu/~sbasu/jacm95.ps)
were directly checked in this reviewer's earlier fixed-core audit. No new
unbounded-dimensional real-algebraic subproblem is introduced here.

## Pooling consequence and limits

With fixed numbers of pools and quality coordinates, their pool qualities
form a fixed-dimensional real parameter vector. At fixed qualities, all
remaining standard-pooling equations and inequalities are linear in the
flows, including arbitrary bypass arcs, exact or bounded supplies/demands,
pool quality balances, output specifications, and the objective threshold.
Finite flow upper bounds make every fiber bounded.

Input-quality minimum/maximum bounds are valid for active pools. For
inactive pools every pool outflow vanishes, so their otherwise free quality
coordinates can be chosen in these intervals without changing feasibility.
Pools with no incoming route are inactive and can be assigned fixed values.
Thus the parameter domain has the stated rational fixed-dimensional
description. This proves NP membership for the bounded-flow class even
when bypass coupling is unrestricted.

Combined with the independently verified bypass-copy construction, the
corresponding one-pool/one-physical-quality decision class is NP-complete
when lower and upper quality bounds and the stated fixed supply/demand
contracts are allowed. Equivalently the two-coordinate upper-quality-only
class is NP-complete. The result does not establish strong NP-hardness,
NP membership for unbounded pool/quality counts, or a polynomial algorithm
without the certificate's nondeterministic basis choice.

## Additional parameterizations

The subsequently added fixed-`p,J` output-fraction corollary also passes.
Use `theta_lj>=0`, summing to one over each pool's allowed outgoing
arcs, as at most `pJ` parameters. Its total intake is
`T_l=sum_i y_il`, its flow to output `j` is `theta_lj T_l`, and its
attribute mass to that output is `theta_lj sum_i C_ik y_il`.
These substitutions make every remaining standard three-layer pooling
constraint and objective threshold linear in intake and bypass flows.
Active physical pools recover these fractions by division by throughput;
inactive pools may choose any legal fraction vector. A pool with no
outgoing arcs must have zero flow, and any incompatible positive pool or
incident-arc lower bound must cause rejection before that pool is removed.
The revised statement correctly includes this check. Finite upper bounds
make the fibers bounded. The corollary therefore supplies NP membership,
and the reviewed two-pool/two-output hardness becomes NP-completeness.
Pool-to-pool arcs are outside this standard three-layer parameterization.

The fixed pool count and fixed affine quality rank corollary also passes.
Choose a rational affine basis `C_i=C_0+B a_i`. Its coordinates have
polynomial encoding length by exact rational Gaussian elimination.
Each active pool uses the convexly averaged coordinate vector of its
inputs, within coordinatewise input minima and maxima. Mass balance and
the coordinate quality balances imply all original attribute balances
after multiplication by `B` and addition of `C_0` times mass balance.
Conversely an original mixture has those coordinates. Every output
specification substitutes its own affine attribute expression, retaining
linearity in flows once the fixed number of pool coordinate parameters
is fixed. Inactive pools admit arbitrary boxed coordinates, and the
rank-zero case is simply a linear fiber with no quality parameters.
Empty-input instances must be checked directly, as the statement says.
