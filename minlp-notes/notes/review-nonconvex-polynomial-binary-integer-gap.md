# Independent audit: polynomial binary-versus-integer gaps

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS after an explicit output-denominator clarification.** Reviewed [the nonconvex polynomial candidate](nonconvex-polynomial-binary-integer-gap.md), including its added one-bit-tight family upper bound and compact construction for all dense polynomials.

Here the binary lower bound applies even to arbitrary convex continuous lifts with binary integer coordinates. The upper constructions are linear mixed-integer formulations, so they also apply to the more restrictive binary-MILP minimum. The distinction from general integer coordinates is essential.

## Bernstein polynomial family

The triangular wave is continuous and `2M`-Lipschitz, including period boundaries. At the Bernstein grid its values are rational with polynomial bit length. The binomial expectation identity gives the asserted polynomial, and Cauchy--Schwarz applied to the binomial variance gives uniform error at most `M/sqrt(N)=1/32` for `N=(32M)^2`.

Both stated encodings are finite rational polynomial inputs. Expanding the Bernstein basis creates at most polynomially many operations on integers with polynomially many bits: binomial coefficients have `O(N)` bits, and all sampled wave values have denominators dividing a common polynomial-bit integer. Even a coarse bound on the expanded coefficient magnitudes gives `O(N+log N+log M)` bits per coefficient. The dense expansion therefore has polynomial total encoding length in `N` and `log M`.

The period formulation has exactly two declared integer coordinates: the bounded period index and the orientation bit. Its two linear branches describe the triangular wave exactly. At an interior period boundary either neighboring period representation gives zero; at `x=1`, the final period with `t=1` is feasible. Both orientations agree at `t=1/2`. A constant number of big-M inequalities with global bounds describes the two branches, independently of the number of periods.

The band of radius `1/32` around the exact triangular wave contains every exact polynomial graph point. Its admitted error relative to the polynomial is at most `1/16`, strictly below the fixed tolerance `1/4`. This proves the two-general-integer upper bound.

At each selected peak the polynomial value is at least `31/32`, and any two peaks have an intervening trough with value at most `1/32`. If two peak lifts had the same full binary assignment, every convex combination of those lifts would retain that same assignment. Evaluating their chord at the trough input gives error at least `30/32`, which violates the tolerance. Thus each peak needs a distinct binary assignment. This is correctly a full-assignment argument, not a general-integer parity argument: arbitrary convex combinations of distinct general integer vectors need not stay integral.

Encoding the bounded period index with `ceil(log2 M)` bits, excluding codes above `M-1`, and keeping one orientation bit gives the added upper bound. Hence

```
ceil(log2 M)<=p_bin<=ceil(log2 M)+1,
p_conv<=2.
```

The family therefore proves an unbounded gap between the optimal counts, not merely inefficiency of a proposed formulation.

The degree translation has the correct direction. The actual degree is at most `1024M^2`, so `log2 M>=0.5 log2(degree)-5`. It also tends to infinity: the alternating trough and peak values give at least `2M` distinct crossings of the level one half. This supplies a logarithmic lower bound in actual degree along the family without assuming that every Bernstein expansion has its nominal full degree. No sparse-input complexity reduction is asserted.

## Finite upper bound by convexity intervals

Restricting an admissible global convex integer lift to an input interval preserves its integer count and convex continuous feasible set. Negating the output on a concave interval makes its graph convex and preserves absolute error. The previously audited parity-span and three-piece refinement argument therefore supplies at most `3*2^p` epsilon-accurate chord intervals on each piece.

Concave pieces use the reversed chord band after restoring the output sign. Combining all piecewise bands gives at most `3s*2^p` bounded polyhedra. A finite disjunction with unused binary codes excluded proves `p_bin<=p_conv+ceil(log2(3s))`. No rationality of piece boundaries is needed in this finite real-coefficient statement.

A nonaffine degree-`D` polynomial has a nonzero second derivative with at most `D-2` distinct roots. Their partition yields at most `D-1` convex or concave pieces; endpoint roots or tangencies can only reduce the necessary count. Thus the displayed logarithmic degree upper bound is valid. Together with the family, it establishes the worst-case order of the finite gap, without identifying an optimal leading constant.

## Compact rational construction for arbitrary dense polynomials

The rational brackets around roots of `f''` can be chosen disjoint, inside the domain, and of the required width with polynomial bit lengths. Endpoint roots need no brackets. The standard root-isolation and augmented endpoint-separation arguments used in the independently audited convex hybrid theorem apply unchanged. There are at most `2D` positive-length pieces.

On a complementary piece, a rational affine input normalization and, when needed, output negation give a convex polynomial. Restricting a global `p`-integer lift gives a local lift with at most `p` integers. The reviewed convex hybrid construction consequently has at most `p+11` binary coordinates and at most `2^(p+11)` local cells or index capacity. The actual local counts are computable by the algorithm; knowledge of `p` is not required.

A root bracket may contain both curvature signs, but the derivative bound still controls the absolute chord error by `2M_1 h<=epsilon/16`. A symmetric band of radius `epsilon/16` around that exact chord contains its graph and admits error at most `epsilon/8`. Its rational endpoints and exact polynomial endpoint values have polynomial encoding length.

The total local cell count is at most `2D*2^(p+11)`. A single global index selects a piece and its local index using the same polynomial-size arithmetic and Boolean compilation as the hybrid theorem. Reflected asymmetric bands on concave pieces can be selected by continuous internal wires already forced Boolean. Their offsets are rational computed data and require no additional integer declarations. The total binary count is therefore at most `p+12+ceil(log2 D)`.

I requested one explicit encoding clarification: exact bracket endpoint values are rational, whereas local hybrid endpoint values use fixed rounded encodings. The final text now includes the polynomially many exact bracket value denominators, together with the local fixed denominators, in a common output denominator. This is the same valid construction used for input coordinates. A fixed integer offset makes all encoded numerators nonnegative. Taking a product over polynomially many polynomial-bit denominators preserves polynomial total bit length, so the bracket error constant is retained exactly.

Every piece is covered by its local cells. Convex, concave and bracket bands all contain the exact graph and obey the prescribed error. The union can therefore be compiled with polynomial rational size without enumerating exponentially large local grids. The bound is with respect to the global minimum over general convex integer lifts, even though the algorithm only computes its local cell counts.

## Independent exact checks

An independent implementation evaluated **eight Bernstein polynomial values exactly**, including peaks and troughs, through nominal degree 9,216. It used a common-denominator integer recurrence for binomial weights and checked that their sum was the exact denominator power. Every approximation and peak/trough bound passed, as did an entire peak-to-peak chord violation.

A further **72 exact periodic branch and binary-period-index cases** checked period boundaries, both orientations at the peak, the final endpoint and bounded-index decoding. These finite checks supplement the uniform probabilistic approximation proof. The compact upper uses the independently audited root, greedy and compiler machinery; it does not rely on these sampled polynomial values.

No substantive mathematical defect was found. The result concerns integer count and finite or polynomial encoding size under the specified models, not solver runtime, ideality of relaxations, or the number of continuous variables. Literature priority remains outside this proof audit.
