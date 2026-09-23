# Second audit: exactly feasible rational polar spanners

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** I independently checked every section of
[the supporting oracle](rational-polar-spanner-oracle.md). The generic
`9/4` barycentric-spanner construction, positive-polar access, and effective
primal-body application are valid with polynomial rational encoding.
There is no hidden exact linear-optimization oracle or strong separation
oracle for the polar.

The author added the explicit dimension-one padding requested during this
audit. This matches the stated dimension convention of the primary GLS
source. No change of constants or mathematical construction was needed.

## Imported optimization and source scope

I reopened the primary [GLS paper](https://ir.cwi.nl/pub/10046/10046D.pdf).
Definition (5), printed page 172, compares the returned objective with the
optimum over the original body, while allowing the point to be within the
requested distance of that body. Theorem (3.1), page 177, supplies weak
separation–optimization equivalence under explicit inner and outer balls.
These are exactly the guarantees used in (A).

For a one-dimensional body, the added product with `[-1,1]` has a weak
separator inherited from its two factors, inner radius `min(sigma,1)`,
and outer radius `R_0+1` about `(c,0)`. The objective `(d,0)` and projection
preserve both guarantees in (A). Thus dimension one is covered without
assuming an unstated version of the source theorem.

I also read section 2.3 of the primary
[Awerbuch–Kleinberg manuscript](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf).
Proposition 2.2 proves the maximum-determinant spanner property, and
Proposition 2.4 gives determinant exchange with a linear-optimization oracle.
The candidate correctly credits these ingredients. Its explicit rational
repair and precision analysis are supplied in the note rather than assumed
from an exact-oracle statement.

## Uniform bounds and fixed precision

For every `lambda in P`, each coordinate is bounded in absolute value by
`Z`. The resulting image coordinates are bounded by `W`; the formula is
conservative. Cofactor expansion bounds inverse entries by
`(r-1)! W^(r-1)/Delta_0`, and hence by the stated `U`, whenever the
determinant has not decreased below its initial value. This includes `r=1`.

For `d_i=V B^(-1)e_i`, summing absolute values gives
`||d_i||_1<=U sum|V_ij|`, which is bounded by the stated `L`.
The weaker written bound therefore holds at every stage. All parameters
have polynomial bit length in the original rational data and the initial
seeds. A very small seed determinant affects their binary lengths and the
precision but does not create an exponential running-time dependence on
its reciprocal value.

The two conditions on `delta` can be satisfied with polynomially many
binary digits. With optimizer accuracy `eta=n delta`, coordinate rounding
adds Euclidean error at most `n delta`, so the rounded point `q` is within
`epsilon=2n delta` of `P`. The condition `epsilon<=1` justifies the bound
`||c-q||<=R_0+1`.

The repair

```
lambda=(sigma q+epsilon c)/(sigma+epsilon)
```

is exactly feasible. If `x` is a nearest point of the compact body, its
alternative convex-combination expression uses `x` and a point in the
known inner ball. Existence suffices; no nearest point is computed.
Furthermore,

```
||lambda-z||_2
 <= n delta + 2n delta(R_0+1)/sigma.
```

Combining this with `||d||_2<=||d||_1<=L` and the original objective gap
`n delta` gives additive loss at most `1/4`, as written. No direction
normalization or unknown Lipschitz constant has been omitted.

Because `q` is on one fixed dyadic grid and all repair coefficients are
fixed, every possible returned coordinate has one common rational
denominator of polynomial bit length. Its numerator is bounded using the
fixed body radius. Including all finitely many seed denominators preserves
this property. Multiplication by the fixed rational image matrix preserves
polynomial bit length for basis entries. This is the required uniform
bound across exchanges; merely bounding each oracle call in terms of its
current input would have been insufficient.

## Exchange, coefficient bound, and termination

The `i`-th coefficient of an image row `lambda^T V` is precisely
`lambda^T d_i`. Replacing the corresponding basis row multiplies the
absolute determinant by the magnitude of this coefficient. An exchange
triggered by a value greater than two therefore more than doubles the
determinant and preserves invertibility.

When both signed optimization calls for every position fail to find such
an exchange, their additive `1/4` guarantees give

```
sup_{lambda in P} |lambda^T d_i| <= 2+1/4.
```

Thus the final rows are a `9/4` spanner, and every row belongs to the image
of the exact body. The argument does not require that this image contain
a neighborhood of zero or be symmetric; the supplied seeds certify its
linear span.

The determinant upper bound `r! W^r` and lower starting value `Delta_0`
give the stated polynomial exchange count. A complete unsuccessful scan
adds only `2r` calls. Exact inverses, objectives, comparisons, and all oracle
inputs have uniform polynomial encoding because of the fixed-denominator
argument above. The proof does not assert strongly polynomial complexity.

## Exactly feasible support points of the original body

Section 2 uses only strong separation of `K`, its known inner ball about
zero, and weak optimization. A weak optimizer `z` satisfies
`||z||<=R+eta`. The repair `x=rho z/(rho+eta)` is exactly feasible by the
same inner-ball argument. Its support loss is bounded by

```
eta + ||a||_1 eta(R+1)/rho,
```

when `eta<=1`. Choosing `eta` as prescribed therefore gives the two-sided
support enclosure in (F). Directions of arbitrary rational magnitude and
the zero direction are handled. The body need not be symmetric.

The output need not have the generic spanner's fixed denominator, because
this support routine is internal to a separation call. Its bit length is
polynomial in that call's direction and accuracy. The generic algorithm
has already bounded its own query encodings uniformly; composing the two
levels of oracle reductions preserves polynomial complexity.

## Positive-polar weak separation

The proposed positive-polar center `a 1` and radius `a/2` are valid.
The radius gives strictly positive coordinates, and the norm of every
point in the ball is less than `1/R` by `a<=1/(8Rm)`. Hence its original
body support is at most one. Conversely, `rho B_2 subset K` implies
`K^circ subset (1/rho)B_2`. The written outer radius about the shifted
center is therefore valid.

Coordinate bounds `[0,1/rho]` are valid for the exact positive polar.
After those checks, the query norm is at most `m/rho`. The exactly feasible
primal support point from (F) has the following two consequences:

- If `lambda^T x>1`, the inequality `x^T mu<=1` is valid for every polar
  point and strictly separates the query. The normal is nonzero and
  rational. Rescaling it by its nonzero infinity norm gives the required
  weak-separation normalization.
- Otherwise `h_K(lambda)<=1+tau`. The nonnegative point
  `lambda/(1+tau)` belongs to the positive polar, and its distance from the
  query is at most `tau m/rho<eta/2` for the chosen `tau`.

Both branches are valid for the entire exact body. In particular, the
separating point `x` is not merely close to `K`; that distinction is
necessary for validity of the polar cut. The construction never makes an
exact decision whether `h_K(lambda)>1` when the support estimate straddles
one. It correctly returns weak membership in that case.

All inner support calls have polynomial-bit accuracy, so this is a rational
weak separator of polynomial query and output complexity. It works even
when `K` is nonsymmetric; unconditionality is needed only by later graph
applications, not by this oracle construction.

## Seeds and the effective primal body

For the polar-image application, `2a e_(j_s)` is exactly feasible because
`2a R<=1`. Independent rows of `V` give independent image seeds, scaled by
the same nonzero rational number. Their determinant and encoding are
polynomially computable. The generic theorem consequently returns
nonnegative exact polar weights whose image rows form the claimed spanner.

For `K_eff={z:Vz in K}`, a rational left inverse exists and has polynomial
encoding by rational elimination. The elementary operator-norm bounds
justify the stated inner and outer radii. Pulling back a strict separator
from `K` is valid. Its pulled-back normal cannot be zero: that would make
the query value zero, while zero is a feasible point and so has support
value at least zero, contradicting strict separation.

The seeds `sigma_eff e_i` are exactly feasible and independent. Thus the
generic theorem with image matrix identity applies. If `K` is symmetric,
convexity contains the crosspolytope generated by the signed basis vectors,
and the coefficient bound gives the outer parallelotope. The row/column
orientation used for this last statement is consistent when the returned
vectors are placed as columns.

## Independent exact checks

I saved [a reproducible checker](../code/quadratic_rank/check_rational_polar_spanner_second.py).
It uses rational boxes and a synthetic weak optimizer with a controlled
approximately feasible output; it does not implement the GLS algorithm.
All checks use exact rational arithmetic:

- 16 generic systems in dimensions one through four;
- 93 repaired optimizer calls with exact feasibility and additive-error
  verification;
- 11 determinant-increasing exchanges and 120 complete image-vertex
  coefficient checks;
- one fixed output denominator verified across each entire exchange run;
- 347 positive-polar separation or membership cases for asymmetric boxes
  in dimensions one through six, including support values close to one.

All passed. These checks supplement the bit-complexity and continuum
arguments above. No strong polar oracle, exact optimization, or hidden
polyhedral assumption is used.
