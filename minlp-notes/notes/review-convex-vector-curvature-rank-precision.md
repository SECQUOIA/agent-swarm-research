# Independent audit: convex-vector precision and curvature rank

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** I independently checked the full proof in
[the candidate](convex-vector-curvature-rank-precision.md), including its
polynomial rational construction. I found no mathematical defect. This is a
correctness audit, not a certification of literature priority.

The verified statements are the finite real-coefficient comparison

```
p_bin <= p_conv + ceil(log2(4r-1)),
```

and, for rational dense polynomial outputs and rational positive component
tolerances, the polynomial-time rational MILP construction

```
p_out <= p_conv + ceil(log2 r) + 12.
```

Here `r>=1` is the dimension of the component functions modulo affine
functions. The comparison permits arbitrary convex continuous lifts and
unrestricted integer ranges. Rank zero has an exact linear graph formulation.
The binary upper bounds are realized by linear lifts.

## Scalar refinement

I checked the direct refinement factor `2H-1`, including maxima exactly on
an integer level and flat maxima. For a nonnegative concave chord gap bounded
by `H*tau`, the two boundary points of every nonempty strict superlevel set
at levels `tau,...,(H-1)tau` give at most `2H-2` cuts. Outside the highest
retained superlevel set, consecutive pieces have gap range at most `tau`.
Subtracting the affine interpolation of their endpoint gaps cannot exceed
that range. The middle piece has equal endpoint gaps and maximum at most
one additional `tau`. Ignoring levels equal to the maximum is valid. When
no level is retained, the initial gap is already at most `tau`.

The finite interval-cover to partition conversion is also valid. Finitely
many closed covering intervals permit a greedy interval extending beyond
each current endpoint until the right domain endpoint is reached. Each
selected interval is used at most once, and restricting a convex chord
interval cannot increase its error. Singleton intervals do not obstruct
this conversion.

## Basis and nonnegative gaps

An exact maximum-volume basis exists because the set of candidate row
subsets is finite and has at least one nonsingular member. Replacing a
basis row multiplies its determinant by the corresponding representation
coefficient. Thus every coefficient has absolute value at most one. This
argument is coordinate-independent in the quotient by affine functions.

The use of original normalized convex outputs as basis functions is
essential and is respected throughout. Their chord gaps are nonnegative.
Consequently, even when representation coefficients are negative,

```
0 <= g_j = sum_s c_js g_(i_s) <= sum_s g_(i_s)
```

for the exact basis, and the last upper bound becomes twice that sum for
the constructive basis. No positivity of the coefficients themselves,
pointwise domination of the functions, or positivity of polynomial
coefficients is assumed. Affine parts cancel exactly in chord gaps.

## Comparison with arbitrary integer lifts

For each parity class, only the closure of its projected graph-contact
inputs is used. Its hull endpoints can be approached by original inputs
in that class. Midpoints of their lifted witnesses have integral integer
coordinates. The component error inequalities therefore give normalized
midpoint Jensen gaps at most one. Taking limits uses only continuity of
the functions; there is no assertion that limiting lifts exist.

For `Psi` equal to the sum of the `r` selected normalized outputs, its
midpoint gap is at most `r` and its full chord gap at most `2r`. The latter
is the elementary concave-gap midpoint bound. Refinement with `H=2r` and
`tolerance=1` gives at most `4r-1` intervals per parity class. The component
chord bands have unit normalized accuracy and contain the exact graph.
Their finite union needs at most the claimed number of binary coordinates.

For the constructive basis, the same midpoint estimate still uses `r`,
not a representation-coefficient norm. Refinement with `H=4r` and
`tolerance=1/2` gives

```
N_(1/2)(Psi) <= (8r-1) 2^p.
```

This comparison is made directly with the original vector lift. It does
not assume a scalar lift at tolerance `1/2` with the same integer count.
This distinction avoids an incorrect tolerance reduction in scalarization.

## Polynomial basis construction

Selecting independent coefficient columns preserves all row relations:
every omitted column is a linear combination of the retained columns.
Rational elimination therefore computes the correct quotient rank and
supports the proposed determinant exchanges.

An exchange triggered by a coefficient of magnitude greater than two
strictly more than doubles the absolute determinant. A row already in the
basis cannot trigger such an exchange. Let `L` bound the complete binary
encoding length of the retained rational matrix. The product `q` of all
positive entry denominators satisfies `q<=2^L`. Every nonsingular row minor
has magnitude at least `q^(-r)>=2^(-rL)`, since multiplying its matrix by
`q` gives an integer matrix. The upper bound `r! 2^(rL)` follows from the
determinant expansion. Thus the stated bound
`2rL+log2(r!)+1` on the number of exchanges is valid.

Every intermediate basis uses original rows. Exact determinants, inverses,
coefficients, and comparisons have polynomial bit length by the same
bounds. Checking all rows after each exchange is polynomial time. This
proves the variable-rank bit claim without a maximum-determinant oracle.
Summing normalized basis polynomials preserves a rational dense encoding
of polynomial length. That sum is nonaffine when the rank is positive:
a sum of convex functions can be affine only if all summands are affine.

## Compact grid, output rounding, and count

The imported scalar hybrid proof supplies actual cell count
`K<=486 N_(1/2)(Psi)` in both branches: its greedy branch has the stronger
factor nine, and its curvature-splitting branch has factor less than 486.
At scalar tolerance `1/2`, each exact chord gap is at most `13/32`.
The constructive basis inequality consequently bounds every normalized
component gap by `13/16` on the same interval.

Evaluating every dense normalized polynomial at each indexed rational
endpoint has polynomial bit complexity. Its signed values can be encoded
with a fixed rational or integer offset and a common fixed dyadic output
precision. The scalar compiler already supplies a polynomial-bit common
denominator for the rational input knots. Additional output evaluations
increase circuit size, not the number of declared integer inputs.

If `T_j` is an exact component chord and `y_j` interpolates endpoint values
rounded downward to error at most `1/8`, then

```
y_j-G_j(x) in [-1/8,13/16].
```

Thus the proposed band `[y_j-13/16,y_j+1/8]` contains the exact graph and
admits absolute error at most `15/16`. All outputs share the same segment
and continuous interpolation weight. This guarantees simultaneous graph
containment, including reversed or repeated knots. Each scalar local path
covers its interval, so global coverage does not require monotone knots.

The exact gate formulations force continuous internal circuit wires to
Boolean values once the index inputs are binary. Interpolation products
with those wires use the exact binary-product hull. No hidden selector
or output bits must be declared integer. Invalid index codes are excluded.
Finally,

```
K <= 486(8r-1)2^p < 3888r 2^p < 4096r 2^p,
```

which gives the stated integer count after rounding its logarithm. The
construction computes actual cell counts and never needs the unknown
optimal lift or its integer dimension.

## Independent checks and scope

I ran exact rational checks separate from the author's checker:

- 24 systems of 13 convex polynomial outputs with curvature rank three,
  including normalization by different rational scales;
- 77 determinant exchanges and 233 negative representation coefficients;
- 936 exact chord identities and coefficient-bound domination checks;
- 120 exact concave piecewise-linear level refinements, including threshold
  equality and asymmetric gaps.

All passed. These checks supplement the proofs above; they do not replace
the variable-dimension bit argument or the continuum error bounds.

The result concerns one input and componentwise box errors. Dense encoding
is needed by the compact endpoint-evaluation step. The theorem makes no
claim for arbitrary coupled output error bodies, multivariate inputs,
sparse huge-degree encoding, necessity of the logarithmic rank overhead,
or an unbounded binary-versus-general-integer gap for convex vectors.
