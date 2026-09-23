# Second review: constant-data hardness with two pool feeds

Date: 2026-09-05. Verdict: PASS for the mathematical construction in
[the constant-data candidate](pooling-constant-data-two-feed-hardness.md).
The claimed strong NP-completeness follows if the model and source family
are stated exactly as in that note. Literature priority is not assessed
by this proof audit.

## Source normalization

The source is the previously audited Matsui family. I reopened the
[primary manuscript](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf)
and checked its factors against the repository's explicit simplex
embedding. Its bounded base polytope has variables in `[0,1]`; replacing
these by scaled simplex coordinates gives generator values with the
stated bounds on `U_i,V_i`.

The new normalization bounds are valid. With `P4=p^(4n)` and
`s<p^n`,

```
U_i <= 2P4-p+s p^(2n)+2s p^(3n) < 5P4,
u0=2P4-p > P4.
```

The largest dyadic `D<=u0/2` obeys `u0/4<D<=u0/2`, hence
`D>P4/4`, `D<P4`, and `2<=U_i/D<20`. Also
`V_i<3P4`, so `D V_i<K=4P4^2`. Thus `a_i in [1,19)` and
`b_i>0`. The latter are integers; the former have dyadic denominators.
The weights `(a_i-1)/32` are nonnegative dyadic numbers less than one.
No assumption that all unrestricted generator values of `V` are positive
is needed for these inequalities; positivity on the source polytope is
part of the already reviewed source result.

All these arithmetic operations have polynomial bit complexity. In
particular `log p=O(n^4 log n)` and the factor/threshold lengths are
`O(n^5 log n)`. Numerical magnitude is large at this intermediate stage,
but it need not become a physical coefficient.

## Binary circuits and bounded signals

The full and half cycle lemmas apply unchanged. Every requested port is
allocated separately, so using one signal repeatedly creates a number of
physical copies linear in its number of occurrences. It does not expand
a shared arithmetic circuit into an exponentially large expression tree.
Full/half coupling is required and is included. All conversion endpoint
qualities used later are positive, which is the needed hypothesis for
the full-cycle upper-quality tightness proof.

The four gate identities are correct. The addition gate's supply is
`u+v+(2-w)=2`, so it forces `w=u+v`; feasibility restricts the sum to
the allowed signal range. The inequality gate has only an upper supply
of two and gives `u+(2-v)<=2`. It is not one of the contracts that the
completion objective must restore.

The dyadic multiplier reads bits in the correct order. After `k` steps,
its value is `x*(sum_(j<k) c_j 2^j)/2^k`. After all `L` steps this
is the desired multiplier. Every averaging input is between zero and
two, so all intermediate values remain in that range. Zero and unit
signals are enforced by the stated constant-capacity physical sources.

For a signed row, clearing rational denominators is polynomial in the
explicit row encoding. The chosen power of two exceeds
`sum |c_i|+|d|`, so each side of the normalized comparison, including
its constant, is strictly less than two for every original signal vector
in `[0,2]^m`. Nonnegative partial sums cannot exceed their final sum.
Thus addition gates do not introduce an unintended restriction. Both
signs of the constant are handled by placing it on the appropriate side.
The number of bit gates and port occurrences is polynomial in the row's
binary encoding length. In contrast to the earlier unary row expansion,
this argument applies to the large threshold coefficients as well.

## Two-feed interface and threshold equivalence

The total `T=sum x_i` is a bounded signal, so its addition gates enforce
`T<=2`. With nonnegative weights at most one, all intended partial sums
for `h=sum r_i x_i` are also at most two. The equation `l+h=T` is
implemented physically, and its nonnegative solution is valid because
`h<=T` for every intended original assignment.

The only actual pool inputs have qualities one and 33 and flow `l,h`.
Their mass is `T` and their quality mass is
`T+32h=sum a_i x_i`. The original signals themselves have no direct
pool arcs. This distinction is important: the total number of external
inputs is unrestricted, despite the pool having only two incoming arcs.
There is no conflict with algorithms fixing the total input count.

For an active composition `z=x/T`, the two primary outlets admit
throughput exactly up to `1+1/a(z)`. The boundary `a(z)=1` is valid:
both unit outlets can then be filled, and no positive anchor flow is
needed. The threshold circuit forces positive throughput because
`b^T x>=K>0`. Homogeneity of the source-cone rows therefore recovers
`z in P`. The algebra

```
(K-DV(z)) * (1+1/(U(z)/D-1)) >= K
iff U(z)V(z) <= K
```

is valid because `U(z)/D-1>=1`. Conversely the maximal admissible
throughput supplies a valid original signal vector, all intermediate
sums, both actual feeds, and the threshold circuit. The contracted
network is deliberately infeasible for a source no-instance; its
nonemptiness is not assumed anywhere in the last step.

## Degree bounds and constant physical data

The previous three-port splitter works for addition as well as averaging.
For addition, capacities `(2,2,2)` and original supply two yield a new
collector demand four. For averaging/coupling, `(2,1,1)` yield demand
two. Each split source has exactly its port capacity as supply, and the
collector receives the complementary residual. This proves both
projection directions with no new nonconstant bound.

All other sources already have at most two outgoing arcs. Each gadget
or collector output has at most three incoming arcs. The pool has
exactly two input arcs and two output arcs. The physical flow and quality
alphabets stated in the draft contain every source, midpoint, collector,
constant generator, conversion, and primary-output value. Scaling the
quality alphabet by 33 is optional and has constant encoding cost.

## Completion objective and strong NP-completeness

After all lower bounds are removed, each old contract has a nonnegative
deficit because its upper bound remains. Therefore the sum of contract
throughputs reaches the sum of their upper bounds if and only if every
contract is satisfied. This exact threshold argument does not use a
penalty constant, an error bound, a positive gap, or a feasible reference
point. At completion, the full cycle and circuit proofs apply again.
A no-instance may approach completion closely, but cannot attain its
threshold; compactness and the exact decision formulation suffice.

Each arc is incident to at most one contracted input and one contracted
output, so the completion objective coefficients are at most two. In the
standard cost/revenue convention, the common unit offset cancels by total
external mass balance, including pool throughput and the anchor. It leaves
input costs in `{0,1}` and output revenues in `{1,2}` while preserving
the completion objective exactly.

There are polynomially many physical nodes and arcs. Every numerical
model coefficient is from a fixed finite alphabet except the integer
threshold, which is at most four times the number of contracted nodes.
Unary encoding therefore remains polynomial. The reduction proves strong
NP-hardness of this precise restricted family. The reviewed fixed-one-
pool, fixed-one-quality bounded-fiber lemma supplies NP membership, so
strong NP-completeness follows. This reasoning does not claim an
approximation gap or that hard instances use only two total inputs.

## Independent physical-network checks

[independent_constant_data_review.py](../code/pooling_bypass_copy/independent_constant_data_review.py)
constructs its own binary gates, signed rational rows, closed cycles,
two-feed interface, and both types of source splitter. Its network LP
contains only physical source/output/arc constraints and pool mass and
quality equations at a fixed pool quality. It inserts no circuit, source
cone, multiplier, or intended signal equation directly into that LP.

The checker passed 40 contracted-network feasibility comparisons against
the explicit original-signal reference: nine yes cases and 31 no cases.
It then passed 40 upper-only completion LPs with the same answers. Cases
include signed rational rows, dyadic and zero feed weights, duplicated
signals, impossible cones, and thresholds attained at equality. It checks
all claimed data alphabets and degree bounds. These are fixed-quality
comparisons; they complement the author's separate global pooling tests
and the general proof, rather than exhaust all possible pool qualities.

A negative control relaxes only the threshold-comparison source's upper
bound from two to four. An infeasible case then becomes feasible and
reaches full completion, confirming that this physical comparison is
actually needed. Exact large-integer checks also passed the source
normalization inequalities at `n=5,...,8`, including thresholds with up
to 786,435 bits. Those tests support the formulas; the inequalities above
establish them for every source dimension.

## Contracted feasibility and the output-degree boundary

Fresh audit on 2026-09-05: the following feasibility corollary passes.
Keep every exact source/output contract from the constructed network and
omit the contract-completion objective. Feasibility is already equivalent
to the source positive-product yes answer. In particular, the inequality
`sum b_i*x_i>=K` remains encoded by the binary signal circuit and its
physical comparison source; it is not an objective threshold or an
unrepresented side constraint of this contracted instance.

For the forward direction, the exact copy contracts force all intended
port identities. The physical comparison implies positive total intake
and the normalized product inequality as in the original proof. For the
reverse direction, a source yes point extends to the radial intake,
all bounded circuit signals, and all exact physical contracts. Splitting
the three-port sources preserves exact feasible projection. Economics
plays no role in either direction.

The instance has one pool, two actual pool feeds and outlets, one scalar
upper quality, input total out-degree at most two, and output total
in-degree at most three. Every lower or upper flow bound belongs to
`{0,1,2,3,4}`, and every quality value belongs to the fixed seven-value
palette of the original construction. All source-instance numerical
information is encoded in polynomially many circuit nodes. Thus the
feasibility reduction is strongly NP-hard. Membership in NP follows from
the reviewed fixed-one-pool/one-quality bounded-linear-fiber certificate.
The contracted feasibility problem is therefore strongly NP-complete.

Together with the [degree-two feasibility theorem](../results/pooling-degree-two-boundary-projection.md),
this gives a sharp output-degree boundary within the stated restricted
family: with input total out-degree at most two, output total in-degree
at most two admits a polynomial algorithm, whereas allowing output total
in-degree three admits the constant-data strong NP-completeness reduction.
The polynomial theorem in fact covers the broader restriction of bypass
degree at most two, including extra pool arcs at attachment nodes.

The feasibility hardness explicitly allows positive exact node contracts.
If every flow lower bound is zero and no additional requirement forces
positive flow, zero flow is feasible. No hardness of that trivial
upper-only feasibility question is implied. The earlier 40 independent
contracted-network comparisons and physical-comparator negative control
already test this corollary's network, so no duplicate numerical test is
needed for simply omitting the completion objective.
