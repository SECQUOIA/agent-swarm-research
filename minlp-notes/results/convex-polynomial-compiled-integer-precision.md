# A compact graph formulation for any dense convex polynomial

Date: 2026-09-05. Status: independently reviewed result. Two full audits
passed, including the signed monotone-curvature integration dependency.

Let `f(x)=sum_(k=0)^D c_k x^k` be a rational dense polynomial convex on `[0,1]`,
and let `epsilon>0` be rational. There is a deterministic polynomial-time
construction of a rational MILP containing its entire graph, with absolute
output error at most `epsilon`, whose integer count satisfies

```
p_out<=p_conv+11.                                                   (1)
```

The comparison allows every convex lift, with unrestricted continuous size and
general integer variables. Construction time and formulation encoding length
are polynomial in the dense polynomial input and the tolerance encoding. No
coefficient-sign or monotone-curvature assumption is imposed. Convexity may be
supplied as a promise or checked by exact univariate polynomial sign testing.
Affine polynomials need no integers; hence assume `D>=2` and `f` is not affine.

## 1. Existing scalar ingredients

Write `N_eta` for the smallest number of chord intervals with maximum chord
error at most `eta`. For every continuous convex function,

```
N_eta<=3N_(2eta),             N_(2epsilon)<=2^(p_conv).              (2)
```

The [reviewed scalar argument](../notes/scalar-convex-graph-two-bit-gap.md) proves these
finite inequalities, without a computability assumption. In particular,

```
N_(epsilon/4)<=9N_epsilon,
N_epsilon<=3*2^(p_conv).                                            (3)
```

For a rational polynomial whose nonnegative curvature is monotone on a rational
interval, reflect its input if necessary and normalize the interval to `[0,1]`.
The [signed monotone-curvature integration lemma](../notes/certified-monotone-polynomial-curvature-quantiles.md)
and the [compiled scalar construction](../results/compiled-curvature-quantile-precision.md)
give a random-access rational polygonal graph description with `K=2^L` cells.
At local tolerance `epsilon` its count obeys

```
K<=5M_epsilon+2<=120N_epsilon(local interval)+2.                    (4)
```

Here `M_epsilon` is the accuracy-dependent curvature mass. The first inequality
follows directly from `L=max(0,ceil(log2((5/2)U)))` and
`M<=U<=M+1/256`; the second uses the finite `M<=24N` theorem.
Each cell's exact endpoint chord error is at most `13epsilon/16`.
Endpoint polynomial values can be rounded downward with error at most
`epsilon/8`, yielding the uniform band

```
y-13epsilon/16 <= w <= y+epsilon/8,                                 (5)
```

where `y` interpolates the rounded endpoint values. This band contains the
exact graph over the cell and has absolute error at most `15epsilon/16`.
The compiled knots need not be monotone: consecutive knots form a continuous
polygonal path joining the interval endpoints, which suffices for coverage.
Affine local polynomials use one cell and satisfy the same bounds.

## 2. A rational grid on which greedy segmentation is efficient when small

Set the rational derivative bound

```
M=max(1,sum_(k=1)^D k|c_k|)>=max_[0,1]|f'|.
```

Choose an integer `B>=2` such that `h=2^(-B)<=epsilon/(32M)`. The bit length of
`B` and the value of `B` are polynomially bounded in input encoding. Consider
the uniform grid `G={j h: j=0,...,2^B}` only through its binary indices.

We first record a perturbation bound. If an interval `[a,b]` has chord error
at most `eta`, every subinterval of

```
[max(0,a-h),min(1,b+h)]
```

has chord error at most `eta+2Mh`. To prove it, compare the old and expanded
chords at `a` and `b`. Each endpoint value changes by at most `Mh`, and each
chord slope has absolute value at most `M`; hence the difference is at most
`2Mh` at those two points and throughout `[a,b]`. On either added strip of
length at most `h`, chord error is at most `2Mh`, using the same slope and
Lipschitz bounds. Restricting a convex function's chord to a smaller interval
can only decrease the chord error.

Take an optimal `epsilon/4` chord partition and round each knot down to `G`.
Keep `0` and `1` exact and discard repeated knots. Every resulting interval
comes from an adjacent pair of original knots at a change of rounded value,
and lies in that original interval expanded by at most `h` at each end.
It therefore has error at most

```
epsilon/4+2Mh<=5epsilon/16<epsilon/2.
```

There is consequently a grid partition with at most `N_(epsilon/4)` cells
and chord error at most `epsilon/2`.

Starting from `a=0`, choose the largest grid point `b>a` for which the chord
error on `[a,b]` is at most `epsilon/2`. Continue from `b` until reaching `1`,
or stop after `9D` cells if they do not yet cover the domain. Each extension
is found by binary search over at most `B+1` index decisions. A one-step grid
interval is always feasible because its error is at most `2Mh<epsilon/2`.

The decision predicate is exact and polynomial time: form the rational
polynomial `chord_(a,b)(x)-f(x)-epsilon/2` and decide whether it is nonpositive
on `[a,b]` by univariate real-root isolation and sign testing. All coefficients
have polynomial bit length. The condition is monotone as `b` increases, by
convexity and interval inclusion. No approximate comparison at an equality
threshold is used.

Greedy largest-endpoint segmentation minimizes the number of intervals among
grid partitions with this error. Inductively, its `k`-th endpoint is no earlier
than that of any feasible grid partition: if the comparison endpoint is already
behind the current greedy point the claim is immediate; otherwise the remaining
part of that comparison interval is feasible by restriction. Thus its count `G`
satisfies

```
G<=N_(epsilon/4)<=9N_epsilon.                                      (6)
```

If it finishes within `9D` intervals, enumerate those polynomially many rational
chord bands and encode the union using `ceil(log2 G)` binaries. They can all
use band (5), with endpoint values rounded downward by at most `epsilon/8`;
their exact chord error is at most `epsilon/2<13epsilon/16`. Equations (3),(6)
give

```
G<=27*2^(p_conv),           ceil(log2 G)<=p_conv+5.                 (7)
```

If the greedy procedure has not finished after `9D` cells, then (6) implies

```
N_epsilon>D.                                                       (8)
```

This lower estimate licenses the second branch; the algorithm does not need
to know `N_epsilon` itself.

## 3. Polynomially many monotone-curvature pieces

Isolate the distinct roots of `f'''` in `(0,1)` in disjoint rational brackets,
each of width at most `h`. Exact rational endpoints can be chosen so that every
bracket contains one root and no endpoint is a root. Roots at `0` and `1` need
no bracket. The zero polynomial `f'''` requires no splitting.

The brackets and the closed intervals between them partition `[0,1]` into at
most `2(D-3)+1` pieces when `D>=3`; in all cases the number `b` is at most `3D`.
Zero-length intervals can be omitted. On each complementary interval `f'''`
has a constant sign, so `f''` is monotone and nonnegative. Each bracket itself
has chord error at most `2Mh<=epsilon/16`, and hence needs only one rational
chord cell. The intervals between brackets use the monotone-curvature procedure
in Section 1. If one has decreasing curvature, reflect its normalized input.

The splitting, endpoint encodings, affine substitutions, and sign decisions
have polynomial complexity by exact univariate root isolation. No inverse root
separation appears in a running-time exponent: the relevant complexity depends
on the logarithm of separation and required bracket width.

Let `n_j` be the optimal `epsilon` chord count on piece `j`. Splitting a globally
optimal partition at the `b-1` piece boundaries gives

```
sum_j n_j<=N_epsilon+b-1.                                         (9)
```

Every resulting subinterval preserves its original error bound. Every monotone
piece has a compiled cell count at most `120n_j+2` by (4), and every bracket's
single cell also satisfies this bound. Therefore the total number of cells is

```
K_total<=120N_epsilon+122b
       <=120N_epsilon+366D
       <486N_epsilon,                                             (10)
```

where the last step uses (8). Combining with (3),

```
K_total<1458*2^(p_conv)<2048*2^(p_conv).                            (11)
```

## 4. One global binary index for all pieces

Counting the sum of cells in (10), rather than the number of pieces times their
largest grid, is essential. Compute each local integer cell count and their
cumulative sums, all of polynomial bit length. A binary global index
`k in {0,...,K_total-1}` identifies its piece by comparison with these cumulative
sums and gives the local index by subtraction. This is a polynomial-time
rational computation and hence has a polynomial-size Boolean circuit. Invalid
codes are excluded by a binary comparison.

The circuit computes the two local rational knots, maps them back to original
input coordinates (reversing orientation on reflected pieces if needed), and
computes downward-rounded endpoint values of `f` to error `epsilon/8`. It may
run every piece's polynomial algorithm and select the indicated output; there
are only polynomially many pieces, so this remains polynomial. Exact evaluation
of a dense rational polynomial at a rational knot has polynomial bit length.

The original-coordinate knots need not be dyadic. Fix a common denominator
consisting of the product of all rational piece-endpoint denominators times
`2^Q`, where `Q` is the largest local dyadic knot precision. This denominator
has polynomial bit length and represents every computed input knot exactly.
The circuit outputs its nonnegative integer numerator in binary. Endpoint
output values use a fixed dyadic precision and a fixed integer offset larger
than `sum_k |c_k|`, so their encoded numerators are also nonnegative. Their
linear decoding uses known rational coefficients; it has the same gate and
interpolation proof as the dyadic compiler.

Compile this circuit using only the `ceil(log2 K_total)` input index bits as
integer variables. The internal Boolean wires remain continuous and are forced
binary by exact gate inequalities. Products of endpoint output bits with a
continuous interpolation weight are represented by their exact binary-product
hulls. This yields the line segment between the two rational endpoint data,
together with band (5). The
[reviewed compiler](../results/rational-power-compiled-integer-precision.md) supplies this standard
construction; branching and local indices introduce no additional declared
integer variables.

Each original piece is covered by its local polygonal path. The union therefore
covers `[0,1]`, and (5) proves exact graph containment and the prescribed output
error. Equation (11) proves (1). The large numerical value of a local grid count
does not require enumerating its knots or cells.

## 5. Separable convex sums and independent outputs

The same algorithm gives polynomial rational constructions for densely encoded
rational convex coordinate polynomials `phi_i`, with arbitrary coefficient signs
and no curvature-monotonicity assumption. For `r>=1` active coordinates,

```
p_out<=p_conv+16r       for f(x)=affine+sum_i phi_i(x_i),
p_out<=p_conv+13r       for independent outputs
                        f_i(x)=affine_i+phi_i(x_i).                (12)
```

The original input domain is `[0,1]^r`; affine-only coordinates are continuous.
All coefficients and positive tolerances are rational. The scalar sum has one
absolute output tolerance; independent outputs have separate componentwise
tolerances. No arbitrary coupled multi-output budget is asserted.

Here is the count transfer, using the
[reviewed separable packing theorem](../results/separable-convex-graph-linear-dimension-precision.md).
For each coordinate and local tolerance `tau`, let `P` be a finite maximal set
of pairwise midpoint-incompatible points. The continuous-convex interval and
refinement arguments give `N_tau<=6P`. The actual hybrid cell count obeys
`K<=486N_tau` in either branch: the small branch has `K<=9N_tau`, and the large
branch has (10). Its binary-index capacity therefore satisfies

```
2^L<=2K<=972N_tau<=5832P.                                         (13)
```

For independent outputs, choose each local tolerance equal to its output
tolerance. The product of coordinate point sets is incompatible, so
`2^(p_conv)>=product_i P_i`. Summing (13) gives an overhead less than
`r log2(5832)<13r`.

For a scalar sum, choose all local tolerances equal to `epsilon/r`. Direct
superadditivity of scalar Jensen gaps along an ordered interval and a product
code give `2^(p_conv)>=product_i P_i/6^r`. Thus the total overhead is less than
`r log2(6*5832)<16r`. Summing the local errors preserves the prescribed scalar
tolerance and exact graph containment. The general proof uses only convexity;
the oracle and construction proof above supplies its dense-polynomial bit
complexity. When `r=0`, the exact affine graph needs no integers.

## Scope

The finite scalar two-bit comparison is already known within this repository.
The added conclusion is a uniform rational construction in polynomial time for
every dense convex polynomial. The hybrid avoids an assumption that an optimal
partition can be indexed efficiently: when its count is small it is enumerated;
when it is large, the cost of splitting at polynomially many curvature changes
is absorbed by a proved lower bound on the required count.

The theorem does not yet claim sparse binary-degree complexity, multivariate
nonseparable polynomial coverage, or a fast practical implementation. The source review distinguishes this construction from prior explicit
segmentation algorithms; no unrestricted publication-priority claim is made.


## Supporting verification

The [exact checker](../code/quadratic_rank/check_convex_polynomial_hybrid.py)
passes 70 interval expansion and rounding bounds, 14 greedy-versus-optimal
grid comparisons using 2,040 exact Sturm-based chord predicates, and 11 global
index checks, including a piece with `2^40` cells. It does not implement the
full certified quadrature algorithm. The
[source review](../notes/compiled-convex-polynomial-hybrid-novelty.md) credits the
existing greedy segmentation, per-segment dichotomy, and convexity-piece
splitting methods; the target here is the uniform compact integer-count bound.


Two independent full proof audits passed, including the signed-coefficient
adaptive integration algorithm and the separable consequences:

* [First audit](../notes/review-compiled-convex-polynomial-hybrid-precision.md).
* [Second audit](../notes/review-compiled-convex-polynomial-hybrid-precision-second.md).

Greedy maximal segmentation, dichotomy, and the additive cost of partitioning
into convexity intervals have direct precedents in
[Codsi, Ngueveu, and Gendron's LinA report](https://www.cirrelt.ca/documentstravail/cirrelt-2021-39.pdf),
Sections 3--5. Its logarithmic search complexity is per enumerated segment.
The theorem here adds a compact representation polynomial in input and
precision encoding, compared with every convex integer lift.


The [nonconvex degree-gap theorem](polynomial-graph-binary-integer-degree-gap.md)
shows why convexity matters: a fixed-error univariate polynomial family has
at most two general integers but an unbounded binary count. For arbitrary
dense polynomials, a compact logarithmic-degree overhead is both sufficient
and necessary in worst-case order.
