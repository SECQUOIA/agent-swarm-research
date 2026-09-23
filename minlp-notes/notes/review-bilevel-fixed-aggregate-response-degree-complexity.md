# Independent degree and bit-complexity audit of the aggregate-response bilevel algorithm

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** This audit checks the growing-degree and exact-output claims in
[the aggregate-response candidate](bilevel-fixed-aggregate-response-investigation.md).
The two separate full audits cover the KKT characterization, global-response
comparison, and attainment proof. I inspected those steps for their arithmetic
consequences but do not present this as a third independent novelty review.

Only `r,s,k_eq,k_in` need be fixed. The algorithm is polynomial in explicit
rational input length and the actual maximum input degree `delta`. It is
therefore polynomial in input length under the stated dense or unary-exponent
encoding conditions. Polynomial box endpoints and polynomial aggregate
coefficients `U(x)` preserve this conclusion.

## Expansion occurs after dimension reduction

Let `h=r+s+k_eq+k_in` and let `L` be the full explicit input length. All
expanded polynomials use the fixed-dimensional vector
`v=(x,w,lambda,mu)`, sometimes with one or two scalar value coordinates.
The input may contain many follower variables in an upper polynomial, but
that polynomial is supplied as an explicit monomial list. The proof never
expands a general dense polynomial in all `N` follower variables.

For `delta>=2`, direct degree bounds are:

| Expression | Degree bound |
| --- | --- |
| `B_i`, including polynomial `U(x)` | at most `2 delta` |
| Clipping thresholds `B_i+a_i l_i`, `B_i+a_i u_i` | at most `2 delta` |
| `Q=prod_i a_i` | at most `N delta` |
| Each coordinate numerator `Z_i` | at most `(N+1) delta` |
| Aggregate and resource equations, including complementarity | `O((N+1) delta)` |
| Follower-value equation `tau Q^2=R_sigma` | `O((N+1) delta)` |
| Upper polynomial after multiplication by `Q^delta` | `O((N+1) delta^2)` |

The last bound follows monomial by monomial. An upper monomial
`c x^alpha prod_i z_i^e_i`, where `|alpha|+sum_i e_i<=delta`, becomes

```
c x^alpha prod_i Z_i^e_i Q^(delta-sum_i e_i).
```

All exponents are nonnegative. Its total number of factors, counting
multiplicity, is polynomial in `N` and `delta`. No substitution of
`phi(x,U(x)z)` into all follower variables is needed: aggregate consistency
allows the follower numerator to use `phi(x,w)` directly.

A polynomial of degree at most `M` in `h+2` variables has at most
`binom(M+h+2,h+2)` possible monomials. Since `h` is fixed and
`M=O((N+1)delta^2)`, dense expansion is polynomial. This remains true when
an upper monomial contains a growing number of distinct follower
coordinates. The number of explicit upper monomials and the number `N`
are bounded by the input length.

Coefficient growth is also polynomial. Clear the input rational coefficient
denominators by a common positive integer whose bit length is at most their
total input length. Every constructed coefficient comes from products of
polynomially many such coefficients and sums over the polynomially many
fixed-dimensional monomials. Derivatives add only exponent factors of bit
length `O(log delta)`. Products and powers in the displayed construction
therefore have polynomial coefficient bit length. This is a direct bound on
the expanded expressions; it does not assume that a general arithmetic
circuit can always be expanded efficiently.

## Regime enumeration and quantified formulas

The sign conditions concern `2N` polynomials of degree `O(delta)` in `h`
variables. Fixed-dimensional sign determination enumerates polynomially many
realizable conditions in time polynomial in `L,delta`. Conditions realized
only outside `C` can be retained because every use of the response formula
restricts the shared leader to `C`.

Producing the numerator and upper-constraint formulas for every retained
condition multiplies two polynomial bounds. In particular, neither the
`3^N` formal clipping assignments nor a list of independently chosen
coordinate roots is constructed.

The comparison against all follower KKT points adds only
`s+k_eq+k_in+1` quantified coordinates. The competitor uses the same leader
`x`. Formula length, degree, and coefficient bit length are polynomial, and
the total number of real coordinates remains fixed.

The primary algorithmic statements used here are the sign-sampling theorem,
quantifier-elimination bounds, and their intermediate coefficient bit bounds
in [Basu's survey, Theorems 2.15 and 2.18](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf).
Their dependence on degree is polynomial when all variable counts are fixed;
they do not require degree to be a constant. The same source defines real
univariate representations in Definition 2.12 and gives explicit sampling
and bit bounds through Theorem 3.6. Its discussion of dense encoding also
distinguishes these bounds from sparse representations with large binary
exponents. The original imported result is
[Basu, Pollack, and Roy (1996)](https://www.math.purdue.edu/~sbasu/jacm95.ps).

## Exact recovery in one algebraic extension

For clarity, the author adopted the following simultaneous sampling route
during this audit. Let `Psi(v,tau,eta)` be the complete compressed feasible
bilevel formula, including its universal follower comparison. Form

```
Psi(v,tau,eta)
AND NOT EXISTS vbar,taubar,etabar:
  [Psi(vbar,taubar,etabar) AND etabar<eta].
```

Bound variables inside the second copy are renamed. This duplicates the
formula only a constant number of times and introduces only a fixed number
of variables. Its realization is precisely the set of compressed optimal
solutions, and it is nonempty whenever the original problem is feasible,
by the separately proved attainment statement. Quantifier elimination and
sampling return `v,tau,eta` together in one real univariate representation
of polynomial degree and bit length.

Every follower coordinate is then `Z_i(v)/Q(x)` in this same extension.
Evaluating and reducing these rational functions requires only polynomially
many operations on polynomials of polynomial degree and height. The selected
value of `Q` is nonzero because `x in C` and every `a_i(x)>0`. If a sampled
defining polynomial has other factors on which a denominator vanishes,
ordinary gcd separation retains the factor containing the selected real
root before inversion; no factorization into independently represented
coordinate fields is required. Returning all `N` coordinates thus has
polynomial total encoding length.

Neither a numerical lower bound on `Q` nor a compact multiplier box is
required. Exact algebraic arithmetic handles a small nonzero denominator,
and fixed-dimensional sampling handles unbounded semialgebraic multiplier
sets. The compactness argument applies to visible leader-response pairs,
not to all possible multiplier witnesses.

## Why the binary-exponent exclusion is substantive

The exact-output claim cannot simply extend to exponentially large degrees
given by sparse binary exponents. Let the leader domain be

```
C={x in [1,2]: x^(2^t)=2},
```

with upper objective `x` and one independent box-bounded follower minimizing
`z^2/2`. All structural dimensions are fixed. The input uses `O(t)` bits for
the exponent, but its unique optimal leader value is `2^(1/2^t)`, whose
minimal polynomial has degree `2^t` by Eisenstein's criterion at the prime
two. It cannot have the promised polynomial-degree conventional algebraic
output representation. This is an output-size obstruction, not a decision
hardness claim. The candidate's explicit exclusion is therefore necessary
for its stated output guarantee.

No substantive degree, denominator, quantifier-dimension, or common-field
defect remains in the revised statement.
