# Limits on approximating the minimum integer precision dimension

Date: 2026-09-05. Status: independently reviewed twice; audit links below. This complements the reviewed
[polynomial-time additive construction](../results/quadratic-weighted-precision-polynomial-construction.md).

The graph formulation and Max-Cut hardness used here are established.
The result concerns the number of integer coordinates needed
to represent an approximate quadratic graph, rather than the difficulty
of optimizing its quadratic objective.

## Zero integer dimension already encodes Max-Cut

For an unweighted graph `G=(V,E)`, let `n=|V|` and define the convex
quadratic

```
f_G(x)=sum_({i,j} in E)(x_i-x_j)^2,       x in [0,1]^n.
```

Let `M(G)` be its maximum cut size. A convex function on a box attains
its maximum at a vertex: successively move each coordinate to an
endpoint without decreasing its value. At Boolean vertices `f_G`
counts cut edges. Therefore

```
max_(x in [0,1]^n) f_G(x)=M(G),
f_G(1-x)=f_G(x),        f_G((1/2)1)=0.                  (1)
```

For a positive rational tolerance `epsilon`, define `p_conv` and `p_bin`
as in the finite covariance theorem, using absolute graph error
`|w-f_G(x)|<=epsilon`.

**Lemma.** `p_conv=0` if and only if `p_bin=0` if and only if
`M(G)<=epsilon`.

**Proof.** If `M(G)<=epsilon`, the LP
`0<=x<=1, 0<=w<=epsilon` contains the entire graph and has absolute
error at most `epsilon`, since both `w` and `f_G(x)` belong to the
same interval. Thus no binary or general integer coordinate is needed.

Conversely, choose a Boolean maximum-cut vector `v`. A convex lift with
no integer coordinates containing the graph contains the midpoint of
any graph lifts of `(v,M(G))` and `(1-v,M(G))`. Its visible midpoint
is `((1/2)1,M(G))`, whose absolute graph error is `M(G)` by (1).
Consequently `epsilon>=M(G)`. Continuous lifting cannot change this
argument. No closure assumption is needed. ∎

For an integer Max-Cut target `k>=1`, take `epsilon=k-1/2`. The lemma
gives `p_conv=p_bin=0` exactly when `M(G)<k`. Thus recognizing zero
integer dimension is coNP-complete on this restricted family. The
complement has the ordinary cut witness, so the coNP membership claim
is only for this family; no general membership claim about arbitrary
convex-lift minimization is made.

## No finite multiplicative approximation

Suppose a polynomial-time algorithm always constructs a valid graph
relaxation and guarantees that its integer count is at most a finite
multiple of the minimum. On a zero-optimum instance it must output
zero integer coordinates; on a positive-optimum instance every valid
output has at least one. The preceding reduction would decide Max-Cut
in polynomial time.

Therefore no such finite multiplicative approximation exists unless
`P=NP`. This holds whether the benchmark is `p_conv` or `p_bin`, and
already for a single convex quadratic with integer coefficients. It
applies to a formulation-construction algorithm whose output includes
the number of integer coordinates; no efficient optimization of the
constructed formulation is assumed.

## Polynomial replication rules out a sublinear power additive guarantee

Take `t` independent input blocks, each with a separate copy of `f_G`
and the same tolerance `epsilon=k-1/2`. The total input dimension is
`N=tn`; the number of outputs is `t`, and every output is convex and
depends only on its own block.

If `M(G)<k`, the product of the zero-integer LPs proves
`p_conv=p_bin=0` for this vector graph.

If `M(G)>=k`, choose a maximum-cut vector `v`. There are `2^t` graph
points obtained by independently using `v` or `1-v` in each block.
Any two distinct points differ in some block. The midpoint in that
block has quadratic value zero, while its midpoint output is `M(G)`.
Thus the midpoint violates the tolerance in that output.

Each of these `2^t` graph points has a feasible lift in any proposed
formulation. Two lifts with the same parity of their `p` general
integer coordinates would have an integer midpoint, contradicting
the preceding incompatibility. Hence the `2^t` points require distinct
parities and

```
p>=t.                                                   (2)
```

This is the established parity argument applied to a direct product;
it does not assume bounded integer ranges or binary variables.

**Theorem.** For every fixed `delta>0`, unless `P=NP`, no polynomial-time
algorithm can always construct a valid graph relaxation using at most

```
p_min + O(N^(1-delta))
```

integer coordinates, where `p_min` is either `p_conv` or `p_bin`.
The statement already holds for disjoint blocks of convex quadratic
outputs with unweighted graph coefficients.

**Proof.** It suffices to consider `0<delta<=1`. Suppose the guarantee
is `p_out<=p_min+C N^(1-delta)` for a fixed constant `C`. Choose a
fixed integer `q>1/delta` and set `t=n^q`. For sufficiently large `n`,

```
C(tn)^(1-delta)/t
 = C n^(1-delta-q delta) < 1.
```

In the zero case the constructed count is strictly below `t`; in the
positive case (2) forces it to be at least `t`. This decides Max-Cut
in polynomial time, because `t` is a fixed polynomial in `n`. The
finitely many smaller dimensions can be solved by enumeration or
handled by padding with isolated vertices. All repeated coefficients
and the rational tolerances have polynomial total encoding length. ∎

Every tolerance can instead be fixed at one: replace each output by
`f_G/(k-1/2)`. The graph remains a rational convex quadratic of polynomial
encoding length, its zero case is unchanged, and every incompatible
midpoint in the positive case has error `M(G)/(k-1/2)>1`. Thus none
of the hardness relies on specifying very small or unequal tolerances.

This rules out every fixed sublinear power improvement over the
reviewed `O(N log(N+1))` additive construction. It does not prove an
`Omega(N)` lower bound on the attainable additive guarantee; for
example, an `N/log N` guarantee is not excluded by this argument.

## The same barrier holds when the minimum is positive

The amplification need not rely on a zero minimum. After normalizing
the graph-output tolerances to one, append one input `z in [0,1]`
and the output `8z^2`, also with tolerance one. This scalar graph has
minimum integer dimension exactly one. Its endpoint graph points have
midpoint `(1/2,4)`, while `8(1/2)^2=2`, forcing at least one integer
coordinate. For a one-binary LP construction, write

```
z=(beta+r)/2,      beta binary,      0<=r<=1,
v=beta r  (its exact four-inequality binary product formulation),
s>=0,     s>=2r-1,     s<=r,
w=2(beta+2v+s).
```

Since the residual square triangle has absolute error at most `1/4`,
the output error is at most `1/2`, and every exact graph point is
contained. Thus one binary suffices.

In the low-MaxCut case, the augmented vector graph has optimum one:
combine the zero-integer LPs with this construction, and use the
scalar midpoint obstruction for the lower bound. In the high-MaxCut
case, independently choosing the two extra scalar endpoints doubles
the incompatible graph packing to `2^(t+1)`, forcing at least `t+1`
integer coordinates. The total input dimension is now `N=tn+1`.

The same polynomial choice of `t` therefore proves both of the following,
unless `P=NP`, even with a promise that `p_min>=1` and all tolerances one:

- No polynomial-time construction has additive error `O(N^(1-delta))`
  for any fixed `delta>0`.
- No polynomial-time construction has multiplicative approximation
  factor `O(N^(1-delta))` for any fixed `delta>0`.

For the first claim, a low-case output has count at most
`1+C N^(1-delta)<t+1`; for the second it has count at most
`C N^(1-delta)<t+1`. Every high-case output has count at least `t+1`.
This proves the distinction without using a zero-optimum convention.

## Sources and verification boundary

The Max-Cut encoding by a positive semidefinite graph quadratic is
standard. The unweighted Max-Cut completeness result used here is
Garey, Johnson, and Stockmeyer, *Some simplified NP-complete graph
problems*, [open primary paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid2.pdf).
The integer parity method is from Lubin, Vielma, and Zadik,
[*Mixed-integer convex representability*](https://arxiv.org/abs/1706.05135).
The [first proof audit](../notes/review-quadratic-precision-approximation-hardness.md)
and [second proof audit](../notes/review-quadratic-precision-approximation-hardness-second.md)
both passed, including the positive-optimum amplification and unit
accuracy normalization. `code/quadratic_rank/check_precision_hardness.py`
passed 48 exhaustive small Max-Cut gadgets, 5,040 augmented incompatible
point pairs, and 260 extrema of the one-binary scalar lift.

The [independent novelty assessment](../notes/quadratic-precision-approximation-hardness-novelty.md)
compares prior integrality-number and implied-integrality hardness,
convex-cover hardness, and mixed-integer extension lower bounds. The
candidate contribution is the positive-optimum `1` versus `t+1` gap
for quadratic graph precision across arbitrary convex lifts, and its
consequence for polynomial-time integer-count approximation. The bounded
search did not locate this guarantee; it does not establish priority.
