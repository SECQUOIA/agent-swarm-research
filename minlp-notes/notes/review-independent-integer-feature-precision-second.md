# Second review: independent integer-feature quadratic precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/independent-integer-feature-quadratic-precision.md`.
Verdict: **PASS** for the finite bounds and polynomial rational construction
under the stated feature-representation and error-body assumptions.

This is a correctness and scope audit. It makes no publication-priority
claim for the result or its classical determinant and quotient ingredients.

## The normalized domain has the claimed volume lower bound

For each row, the exact range of `T_i x` on the unit cube is
`[ell_i,ell_i+w_i]`, including for mixed-sign integer rows. Full row rank
makes every row nonzero, hence `w_i>=1`. The coordinate normalization
therefore maps the cube onto a compact convex, full-dimensional zonotope
`Omega subset [0,1]^r`.

Choose any nonsingular set of `r` columns and fix the other cube variables
to zero. The resulting subset of the image is a translated parallelotope
with linear part `diag(w)^(-1) T_I`. Its volume is exactly

```
|det T_I|/product_i w_i.
```

The translation by `-diag(w)^(-1)ell` changes no volume and does not affect
containment. Integer entries imply the nonzero determinant has absolute
value at least one. Thus `V>=1/product_i w_i`, with no disjoint-support,
total-unimodularity, or whole-zonotope volume-computation assumption.
The optional improvement using the chosen minor's actual determinant is
valid. Gaussian elimination finds a nonsingular column set and computes
its determinant in polynomial rational bit complexity; the note does not
claim a maximum-volume minor can be found this way.

## Quotient, Hessian coefficients, and rank

Substitution gives exactly

```
g_j(u)=(1/2)sum_i a_ji(w_i u_i+ell_i)^2,
nabla^2 g_j=diag(a_ji w_i^2)=diag(C_j).
```

The shifts introduce only affine and constant terms in addition to the
stated diagonal quadratic part. These terms are handled exactly by the
square-prefix construction and cancel in the Jensen comparison.

After the original cube constraints are imposed, subtract the original
affine output before projecting to `u`. This preserves the exact reduced
graph, reaches every reduced-domain point, and preserves all admitted
error vectors. In the reverse direction, the original continuous cube
variables and the rational normalization equation restore the domain and
the original affine outputs. Both operations add no integer variables and
preserve convex lifts and binary linear lifts. The formulation minima are
therefore equal, even with affine variation along quotient fibers.

The sum of all original Hessians is
`T^T diag(sum_j a_ji) T`, with strictly positive diagonal weights because
every feature is active. Its kernel is `ker T`. PSD implies this kernel
is also the intersection of the individual Hessian kernels, giving common
nonlinear input rank `r`. The argument does not require any one output to
use all features.

## Count comparison and rational implementation

The reduced domain is convex and lies in the unit cube, so the reviewed
diagonal covariance argument applies to compact parity supports within it.
Its expected nonnegative Jensen vector is `(1/4)C diag(Sigma)` and belongs
to the closed convex error body. The allocation `p_i=Sigma_ii/4` is capped
by one and has `Cp in K`. Hadamard and the volume-covariance inequality
give support volume at most `2^(A_r) sqrt(D)`. Summing the parity cover
over the actual volume `V` proves the stated finite lower bound.

The whole-cube shared square-prefix model has at most `Phi+r` bits and
componentwise error bounded by `Cp/8`. Unconditionality of `K` puts these
errors inside `K`. Restricting with the exact original-variable domain
lift proves the finite upper bound. No product-domain assumption is made
for `Omega`.

The reviewed rational log-product oracle applies without modification and
adds at most `1/(2 ln 2)` to the count. The lower-volume estimate gives
`-log2 V<=sum_i log2 w_i`; together with `A_r<4r` this yields

```
p_out<=p_conv+5r+sum_i log2 w_i+1.
```

The algorithm need not compute `V`. It uses the supplied feature matrix,
rational coefficients, and the body's strong separation and known-radius
data. Row sums, shifts, squared widths, normalization equations, and
chosen minors all have polynomial bit length. The allocation oracle's
positive lower bounds ensure polynomial prefix depths, and exact rational
comparisons choose them. Thus model size and runtime are polynomial in
the full representation, with no efficient MILP solution claim.

## Representation scope is stated correctly

A given rational feature row may be multiplied by a common denominator
`d` and divided by the resulting integer gcd `g`. With
`T_i'=(d/g)T_i`, replace its quadratic coefficient by
`a_ji'=a_ji(g/d)^2`. These are exact rational operations of polynomial bit
complexity. They preserve full row rank and positive activity. The
resulting integer widths can be large; polynomial bit length does not
make their logarithms bounded independently of the data.

Accordingly, linear-rank overhead follows from bounded integer row widths,
not from arbitrary rational feature changes. Forest incidence rows have
width two and reproduce the `6r+1` bound. The thin-domain example's rows
`(1,0)` and `(M,1)` have width term `log2(M+1)`, so there is no conflict
with its unbounded fixed-dimension product-domain loss. Discovery of a
favorable positive square representation is explicitly outside the
algorithm's scope. No unresolved mathematical or encoding defect was
found.

I inspected and reran `code/quadratic_rank/check_integer_feature_precision.py`.
All 30 exact cases passed the minor-volume bound, normalized coordinate
ranges, nonlinear rank, quotient identity, and rational row-rescaling
identity. These arithmetic checks supplement the universal proof above.
