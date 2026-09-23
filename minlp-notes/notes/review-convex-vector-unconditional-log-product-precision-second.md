# Second audit: convex vectors with unconditional error bodies

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** I independently checked
[the candidate](convex-vector-unconditional-log-product-precision.md),
including its use of the [rational log-product allocation lemma](rational-log-product-convex-body-oracle.md).
The finite and constructive bounds hold as written:

```
p_bin <= p_conv + ceil(log2(4m-1)),
p_out <= p_conv + 14 + ceil(log2 m).
```

The second bound assumes densely encoded rational componentwise convex
polynomials, a rational strong separation oracle of polynomial complexity,
and the stated rational inner and outer radii. No correction was required.
This audit establishes correctness, not literature priority.

## Exact allocation and finite comparison

Compactness gives a maximizer of the product over the nonnegative part of
`K`. The inner ball supplies a feasible point with every coordinate positive,
so every maximizing point has strictly positive coordinates. Unconditionality
puts every sign flip of this point in `K`; convexity then puts its entire
coordinate box in `K`.

For a maximizing vector `b`, differentiating the feasible segment from `b`
toward any `v>=0` in `K` gives

```
sum_i (v_i-b_i)/b_i <= 0.
```

The derivative is defined even if some coordinates of `v` are zero, since
`b` is strictly positive. This proves the positive functional bound `m`.

At the endpoints of each parity-support hull, the midpoint Jensen vector
belongs to `K`. Witness approximation and closedness of `K` suffice;
closedness of the lift, bounded integer ranges, and measurability of the
chosen supports are unnecessary. Componentwise convexity makes this vector
nonnegative. The scalar sum `Psi=sum F_i/b_i` consequently has midpoint gap
at most `m` and full chord gap at most `2m`.

The direct scalar level refinement with factor `H` uses at most `2H-1`
intervals. Its application with `H=2m` is valid, including equality at an
integer level, flat maxima, and degenerate hulls. Positive weights and
nonnegative component gaps imply that scalar chord error at most one bounds
each component error by `b_i`. The resulting downward chord bands contain
the exact graph and have their full error vectors in the inscribed box.
There are at most `(4m-1)2^p` bands. Their finite binary linear disjunction
proves the first bound; real coefficients are permitted in this part.

## Rational oracle specialization and exact feasibility

Apply the allocation lemma with `r=m`, matrix `C=R I`, original body `K`,
inner radius `rho`, and accuracy `nu=1`. Its allocation variable `p` has
coordinate cap one. The correspondence `b=R p` identifies its feasible set
with the nonnegative part of `K`, because every coordinate of a nonnegative
point in `K` is at most `R`. Product objectives differ by the constant `R^m`.
Thus the oracle returns exactly feasible rational `b>0` satisfying

```
product b_i >= exp(-1) max_{v in K, v>=0} product v_i.
```

I reread the full supporting oracle proof. Its positive coordinate lower
bound excludes no maximizer. The explicit center and radius lie inside the
bounded log-product hypograph: coordinate, body, log-product, and lower
objective margins all have the stated slack. The constants and their
reciprocals have polynomial bit length, also for `m=1` and small `rho/R`.
Rational tangent coefficients and certified logarithm intervals give weak
separation with the claimed vertical-distance guarantee.

I also reopened the primary
[Grötschel–Lovász–Schrijver paper](https://ir.cwi.nl/pub/10046/10046D.pdf).
Definition (5), printed page 172, requires a rational point within the
requested distance of the original body and an objective value within the
same additive tolerance of its optimum. Theorem (3.1), page 177, supplies
the weak separation–optimization equivalence for bodies with known inner
and outer balls. These are the conventions used by the supporting lemma.

The subsequent rational central-ball repair is exact. If `y` lies within
`eta` of the hypograph `Q`, `z` is a nearby point of `Q`, and `(p_0,t_0)`
is the known center with radius `sigma`, then

```
[sigma*y + eta*(p_0,t_0)]/(sigma+eta)
```

is a convex combination of `z` and the point
`(p_0,t_0)+(sigma/eta)(y-z)` in the known inner ball. It is therefore in
`Q` exactly, although `z` need not be computed. The written choice of
`eta` bounds the objective loss by `nu`. This is not an approximate-membership
claim for `b`; the final rational box is exactly contained in `K`.

## Approximate product to positive functional bound

Let `a_i=v_i/b_i`, `S=sum a_i`, and, for `m>=2`, `s=1-1/m`.
The feasible point `w=s b+v/m` is strictly positive. Approximate product
optimality gives `product(w_i/b_i)<=e`. Expanding its product gives

```
product(s+a_i/m) >= s^m + s^(m-1) S/m.
```

Every omitted term is nonnegative. The inequality
`log(1-1/m)>=-1/(m-1)` follows by bounding the integral of `1/(1-t)`
on `[0,1/m]`; hence `s^(m-1)>=e^(-1)`. Rearranging proves

```
S <= m(e^2-1)+1 < 7m.
```

The final strict inequality holds already at `m=2`, since `e^2<15/2`,
and becomes weaker for larger `m`. For `m=1`, direct product optimality
gives `S<=e<7`. Thus neither dimension one nor dimension two leaves a
missing case. Coordinates of `v` may vanish. The argument needs no
approximate derivative or first-order stationarity guarantee from the
allocation algorithm.

## Scalar compiler, vector bands, and bit count

The rational scalar polynomial `Psi` has polynomial encoding length.
A positive sum of convex components is affine only if every component is
affine, so the stated affine bypass is valid. Every parity hull has scalar
midpoint gap at most `7m`, hence full chord gap at most `14m`. Refinement
at tolerance one and conversion of an interval cover into a partition give

```
N_1(Psi) <= (28m-1)2^p.
```

This is a direct comparison with the original vector lift; it does not
assume that scalarization preserves the original unit tolerance.

The previously reviewed scalar hybrid supplies actual cell count
`K_cells<=486 N_1(Psi)` and exact scalar chord error at most `13/16`.
The selected positive scaling makes each normalized component gap
nonnegative and no larger than this scalar gap. Downward endpoint rounding
by at most `1/8` gives interpolant error in `[-1/8,13/16]`. The bands
`[y_i-13/16,y_i+1/8]` therefore contain the exact graph and admit normalized
absolute error at most `15/16`. Rescaling puts the full vector error in
`(15/16) product[-b_i,b_i]`, a subset of `K`.

All outputs share the same input cell and interpolation weight. Coverage
therefore holds simultaneously, including repeated or reversed cells.
Rational input knots have the scalar compiler's polynomial-bit common
denominator. Dense endpoint polynomial evaluation, fixed dyadic rounding,
fixed offsets for signed output numerators, reciprocal scaling by `b_i`,
and final rescaling all have polynomial bit complexity. The lower bound
on the oracle's positive coordinates prevents a hidden superpolynomial
reciprocal encoding.

The existing indexed circuit uses only its index inputs as declared binary
variables. Its other gate wires and products with the interpolation weight
remain continuous, forced by the binary inputs. Additional components add
polynomially many rows and continuous variables. The construction does not
query `K` during optimization or describe or approximate its facets.

Finally,

```
K_cells <= 486(28m-1)2^p < 13608m 2^p < 16384m 2^p.
```

Taking the ceiling of the binary logarithm proves the stated `14+ceil(log2 m)`
overhead. The algorithm computes actual cell counts and needs neither the
comparator lift nor its unknown integer minimum.

## Independent checks and scope

Exact rational tests covered 741 positive allocations in unconditional
cross-polytopes of dimensions 1 through 12. Their products were at least
`3/8>e^(-1)` of the known optimum. All 2,902 support-vertex inequalities
passed, including allocations with one small coordinate and all other
coordinates compensating. Product-expansion identities were checked exactly.
Another 500 integer count checks covered dimensions 1 through 100 and
comparator counts zero through four. These finite checks supplement the
uniform proofs above.

The integer overhead has no facet-count or radius-ratio factor. Running
time still includes the radii's binary lengths and the strong oracle's
polynomial query and output costs, as stated. The result requires an
unconditional full-dimensional error body, componentwise convexity, and one
input. It makes no claim for arbitrary symmetric tilted bodies, multivariate
inputs, sparse huge-degree encoding, or necessity of the logarithmic output
term.
