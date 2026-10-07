# Review of the explicit polynomial component budget

Date: 2026-10-02.

**Verdict: the current Section 7 passes this focused arithmetic review.**
The stated implementation convention gives a predetermined component base
`c_d=2^(10000 D)`, where `D` is the least even integer greater than the
fixed degree bound. No correction is needed. This is a review of the
actual inserted appendix in
[strong-field-component-polynomial.md](../new-direction/strong-field-component-polynomial.md),
using the construction in
[polynomial-component-primitive-limit.md](../new-direction/polynomial-component-primitive-limit.md).
It does not replace the separate review of algebraic completeness or the
component probability argument.

## Degree, height, and query ledger

Write `S=H+q+d+2`, `B=2^(Dk)`, and `U=BS`. For a face of dimension
`r<=k`, both the memoized monomial count and quotient dimension are at
most `B`. Since `d` is fixed, substitution of rational box endpoints
admits one common coefficient denominator of `O_d(H)` bits: use the
product of the original coefficient denominators and the product of the
endpoint denominators raised to degree `d`. Each normal-form reduction
path has `O_d(k)` steps. The logarithm of its branching count is
`O_d(k log(H+1))`. Thus the appendix's quadratic bound in `H+k+1` for
normal-form coefficient heights is valid; it does not require clearing
unrelated denominators afresh at each recurrence.

The interpolation grid for one determinant has `O_d(k N^3)` points.
At consecutive integer sample nodes, entry heights remain polynomial in
`H+k+1`, and the determinant height is bounded by its order times the
entry height, with the usual factorial contribution. These bounds fit
within `O_d(U^5)`. Tensor interpolation in three fixed variables fits
within the stated `O_d(U^8)` coefficient height bound. For example,
successive integer differences and factorial denominators provide a
direct implementation with polynomial intermediate heights.

The subsequent degree bounds remain constant multiples of `N`, except
for the harmless fixed factor from objective composition. Subresultant
and Sylvester minor bounds control rational gcds, exact quotients,
Bezout coefficients, and modular inverses. They fit within `O_d(U^12)`
for reconstructed coordinate polynomials. Clearing coordinate
denominators together, composing an objective of fixed degree, and
forming its value resultant fit within `O_d(U^18)`. No product of
independent coordinate extension degrees occurs.

Cauchy bounds and squarefree root separation require polynomially many
precision bits. A coarse separation estimate of order
`degree^2 * (coefficient height + 1)` already suffices here. Add the
logarithmic derivative bound for polynomial evaluation, the requested
`q` bits, and the same bounds for products of two value polynomials used
in comparisons. The resulting precision fits within `O_d(U^25)`.
Isolating endpoints must be included in the primitive inputs, as the
appendix explicitly requires. Multiplying the scalar height bounds by
the numbers of entries in dense matrices, coefficient arrays, root
lists, and interpolation tables still leaves the full query encoding
within `C_d U^50`.

The query count also has sufficient slack. For example, multiplying
the numbers of faces, forms, coordinate directions, and determinant
sample nodes gives `O_d(B^6 S^3)` sampled determinant queries. Candidate
roots, coordinate sign checks, value comparisons, interpolation calls,
and memoized table operations fit within the looser common count
`C_d U^10`. Comparisons can scan candidates while retaining the current
minimum; they do not require a Cartesian product of representations.

## Fixed elementary routines

The exponent `100` is a valid conservative common budget for the
specified elementary implementations. It is not a conclusion from the
phrase "polynomial time" alone. Fraction-free determinant and
subresultant intermediate values have polynomial bit lengths given by
minor bounds. Schoolbook arithmetic on those values has polynomial
cost. Fixed-variable interpolation has polynomially many entries and
polynomial intermediate heights.

For the root routines, squarefree Sturm bisection retains only intervals
with positive root count. At each depth there are only linearly many
such intervals in the degree. Cauchy bounds and the coarse separation
estimate above give a polynomial depth bound. Sturm evaluations and
exact zero tests use the same controlled rational arithmetic. These
elementary counts, including denominator clearing and supplied
endpoint lengths, stay well below a per-query exponent of `100` in
the full input length plus requested precision. Refinement and root
matching use these same routines; they introduce no unbounded search
for equality.

## Effective sampler constant

Applying `A(L+2)^100` to at most `C_d U^10` queries of encoding length
at most `C_d U^50` gives `C'_d U^5010`. Since

`U^5010 = 2^(5010 D k) (H+q+d+2)^5010`,

the displayed bound

`C''_d 2^(10000 D k) (H+q+1)^10000`

follows after absorbing only degree-dependent factors into `C''_d`.
Hence `c_d=2^(10000 D)` is fixed before sampling. The component cost
prefactor occurs once per solved component; it need not be included
in every vertex weight. This constant is a conservative proved
implementation bound and makes no claim about practical running time.

## Verification scope

This review read the completed Section 7 and checked its arithmetic
ledger against Sections 5–6 of the component construction. No executable
tests, external research, project-wide verification, or CI inspection
were performed. No delegation was used for this fresh appendix review.

Targeted document check run:

```sh
git diff --no-index --check /dev/null research-20261002/reviews/strong-field-polynomial-budget-review.md
```

It reported no whitespace errors. Exit status `1` reflects the new-file
comparison, not a test failure.
