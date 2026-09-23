# Independent review of the full-block design FPTAS

Date: 2026-09-12. Reviewed §§1–3 of
[the full-block approximation-scheme draft](research-20260912-full-block-design-fptas.md).
The corollary is correct under its explicit input promises. Both block
dimension `d` and parameter dimension `p` may be part of the explicitly
encoded rational input. I found no substantive correction needed.

This review uses the previously independently reviewed block covariance
theorem. It does not establish research priority or practical performance.
No code or literature knowledge-base entry was changed.

## Rational promises and the approximation proof

The transition promise is exactly the needed spectral-norm condition:

```text
A_t V_(t-1) A_t^T <= rho0^2 V_t
  => T_t T_t^T <= rho0^2 I,
T_t = V_t^(-1/2) A_t V_(t-1)^(1/2).
```

Similarly, `P_t<=B0 V_t` gives the whitened unconditional latent covariance
bound `V_t^(-1/2) P_t V_t^(-1/2)<=B0 I`. These implications do not require
Euclidean conditioning bounds on `V_t`. The independence and complete-block
observation assumptions match the reviewed theorem.

Whitening is used only to prove the error bound. The local residuals and
sensitivities transform together, and the congruence factors cancel in
`G^T D^(-1)G`. Consequently, the original-coordinate rational calculation
produces exactly the same surrogate information matrix. No square root of
`V_t` must be computed by the algorithm.

Each local conditional covariance is positive definite because it is the
sum of `V_t>0` and a positive-semidefinite conditional latent covariance.
Thus all displayed local solves are defined, including with singular
initial or process covariance. The contribution `G^T D^(-1)G` is PSD;
applying `W>=0` gives a nonnegative scalar weight. The common prior
`tr(WJ0)` is also nonnegative, without requiring `W` and `J0` to commute.

The uniform relative precision bound passes through congruence and this
positive trace functional. Exact surrogate maximization therefore gives the
stated factor `(1-delta)/(1+delta)`, and `delta<=epsilon/2` is sufficient
for `1-epsilon`. The proof never divides by the optimum. Its separate
positive-optimum condition for the logarithmic assertion is appropriate.

## State count and accuracy dependence

One decision selects the entire block. Its future surrogate contributions
depend only on the preceding `L` time-selection bits and the remaining
cardinality. They do not depend on the accumulated information matrix or
on individual coordinates within previously selected blocks. Thus retaining
one best scalar reward at each time/mask/count state is valid.

The state and arc count is `O(n(k+1)2^L)`. Mandatory and forbidden times only
remove arcs; the feasibility promise handles contradictory restrictions.
The explicit `k=0`, `n=0`, and `n=1` cases are sufficient.

Minimality of the accuracy-based `L` gives

```text
2^L <= max(1,(C0/eta)^a0),
a0=log(2)/log(1/rho0).
```

The full-history cap reduces this bound and makes the approximation exact.
Using exact full history at very small requested error is therefore
consistent with a bound polynomial in `1/epsilon`. For a bound uniform over
all `0<epsilon<1`, one may write
`L=O(1+log(1/epsilon))`; the draft's asymptotic shorthand does not affect
the argument.

The exponent in the mask factor depends on the fixed contraction bound,
not on `d` or `p`. Dense matrix work adds polynomial factors in `d`, `p`,
and `L`; it does not place `d` or `p` in a combinatorial exponent. This
depends on acquiring a full block with one decision. Arbitrary coordinate
selection within a block is outside the statement.

## Exact PSD checks and bit complexity

Positive definiteness of each `V_t` and positive semidefiniteness of all
other covariance, weight, and promise matrices can be checked in polynomial
time using exact rational symmetric elimination. No approximate eigenvalue
oracle is necessary. For example, for a symmetric PSD test, a negative
diagonal or a zero diagonal with a nonzero off-diagonal entry certifies
failure. Otherwise one may pivot on a positive diagonal and recurse on its
Schur complement, stopping at the zero matrix. The relevant rational bit
lengths have the usual polynomial determinant bounds.

The covariance-encoding argument remains valid for dense, variable-size
state matrices. Expanding a covariance recurrence yields monomials with
degree `O(n)` in the original rational entries. Although there can be
exponentially many coordinate paths, the logarithm of their number is only
`O(n log(d+1)+log(n+1))`. A common denominator formed from all input
denominators to an `O(n)` power has polynomial bit length. Each monomial's
scaled numerator and the sum of all such numerators consequently have
polynomial bit length. This is a size bound on the expanded expression;
the algorithm computes it by matrix recurrences and never enumerates those
monomials.

Every local inverse has dimension at most `d(L+1)`. Clearing denominators
and bounding determinants and cofactors therefore gives polynomial-size
rational solve results. Exact elimination provides polynomial bit running
time. An exponentially large floating-point condition number can demand
large numerical values, but their binary encoding is still covered by these
input-dependent bit bounds.

The local weights use polynomially many rational operations in these
matrices and the explicitly supplied `F_t,W,J0`. Every stored path value
sums at most `n` local weights and one prior. The bit length of a product
of their denominators is the sum of their bit lengths, so exact path
comparison is polynomial. Taking a maximum chooses one path value; it does
not aggregate exponentially many numerators or denominators.

These facts establish polynomial bit complexity in the complete rational
input encoding and `1/epsilon`. Fixed `rho0` and `B0` are essential to this
claim. No exact spectral decomposition or irrational whitening primitive is
hidden in the implementation.

## Scope of the conclusion

The result is an approximation scheme for scalar information or a fixed
PSD-weighted trace of information. It does not yield one for arbitrary
multi-parameter logdet, inverse trace, or parameter-dependent covariance
information. Supplying rational sensitivities as input is also an important
qualification: the proof does not address the complexity of deriving them
from an arbitrary nonlinear process model.

The draft's statement about the particular earlier treewidth-based reduction
is appropriately limited. A dimension-dependent bound for that construction
does not establish a lower bound on other prior algorithms. This review
does not extend the publication-priority audit.

## Additional review: selecting individual coordinates

The parent researcher proposed the following boundary example after the
main review. The reduction is correct. Here the cardinality budget counts
**individual coordinates within one time block**, a different selection
rule from the full-block theorem.

Let `G` be a simple undirected cubic graph on `m` vertices, with adjacency
matrix `A`. Use one observation time, block dimension `d=m`, zero latent
covariance, measurement covariance

```text
V=R=I+A/12,
```

one scalar mean parameter with sensitivity vector `1`, and choose exactly
`k` coordinates. There are no transitions to check, and the latent
covariance promise holds for every positive fixed `B0`. The covariance is
rational and has a polynomial-size explicit encoding.

Since the maximum graph degree is three and `A` is symmetric,
`||A||_2<=3`. Therefore

```text
(3/4)I <= R <= (5/4)I,
cond_2(R) <= 5/3.
```

For a size-`k` selection `S`, let `A_S` be the induced adjacency matrix and
`x=(I+A_S/12)^(-1)1`. Its maximum absolute row sum satisfies
`||A_S/12||_infinity<=1/4`, so the convergent Neumann series gives
`||x||_infinity<=4/3`. The equation for each coordinate then yields

```text
x_i = 1-(1/12)sum_(j adjacent to i in S) x_j
    >= 1-(3/12)(4/3) = 2/3.
```

In particular, these coordinates are positive; positivity of the inverse
matrix itself is neither assumed nor needed. Summing the equations gives
the exact information identity

```text
I(S)=1^T x
    = k-(1/12)sum_(i in S) degree_S(i) x_i.
```

An independent set has `I(S)=k`. If the induced subgraph contains an edge,
its total degree is at least two, and therefore

```text
I(S) <= k-1/9.
```

Add scalar prior one and call the resulting objective `J(S)=1+I(S)`.
If an independent size-`k` set exists, the optimum is exactly `k+1`.
A deterministic FPTAS with

```text
epsilon = 1/[18(m+1)]
```

would return a size-`k` set with

```text
J(S_hat) >= (1-epsilon)(k+1)
         >= k+1-1/18 > k+1-1/9.
```

The returned set must consequently be independent. If no independent
size-`k` set exists, no feasible output can be independent. Inspecting the
returned induced graph would decide the independent-set instance in
polynomial time, because `1/epsilon` is polynomial in `m`.

The required source hardness is established directly by Mohar's
[*Face Covers and the Genus Problem for Apex Graphs*](https://www.sfu.ca/~mohar/Reprints/2001/BM01_JCT82_Mohar_ApexGraphs.pdf),
Theorem 4.1(a), inspected in the author PDF on pages 10–11: maximum
independent set remains NP-hard on 2-connected cubic planar graphs. The
corresponding threshold decision problem is in NP. Thus the coordinate-
selection problem above admits no deterministic FPTAS unless `P=NP`, even
with the displayed constant covariance condition bound.

This verifies why arbitrary coordinate selection cannot be added to the
full-block result without further structure. It does not claim novelty for
the reduction or classify every restricted partial-observation model. The
identified primary hardness literature was routed to the sole literature
maintenance agent for deduplication and inclusion.

### Strengthening to independent isotropic measurement noise

The same hard covariance has the decomposition

```text
V=(2/3)I,
P=(1/3)I+A/12,
R=P+V=I+A/12.
```

The cubic adjacency eigenvalue bound gives

```text
(1/12)I <= P <= (7/12)I = (7/8)V <= V.
```

Thus `P` is strictly positive definite, measurement noise is independent and
isotropic, and the latent/noise promise holds with the fixed constant
`B0=1`. There is still just one calendar time, so the transition promise is
vacuous for any fixed `0<rho0<1`. Both matrices are rational with the same
polynomial encoding bound as before.

This changes neither the observation covariance nor any selected-subset
information value. The exact `1/9` gap and the no-FPTAS conclusion therefore
persist with independent isotropic measurement noise and a strictly
positive-definite latent covariance. This strengthening was independently
checked algebraically; no numerical calculation is needed.
