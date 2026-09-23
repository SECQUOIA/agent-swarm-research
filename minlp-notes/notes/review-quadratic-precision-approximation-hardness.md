# Independent audit: hardness of approximating integer precision dimension

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the precision approximation hardness note](quadratic-integer-precision-approximation-hardness.md). The zero-dimension equivalence, restricted coNP-completeness statement, multiplicative obstruction, polynomial direct-product amplification, and fixed-unit-tolerance variant are correct. This is a proof audit, not a certification that the result is absent from all literature.

## Exact zero-dimension threshold

The positive semidefinite graph quadratic `f_G(x)=sum_edges(x_i-x_j)^2` has maximum equal to the maximum cut size `M`. Convexity permits successive endpoint choices on the cube; Boolean objective values count cut edges. Complementing every coordinate preserves the objective and the cube center has objective zero.

If `M<=epsilon`, the rectangle `0<=x<=1, 0<=w<=epsilon` contains the complete graph and has vertical error at most `epsilon`. If a convex lift with no integer coordinates contains the two maximum-cut graph points at complementary Boolean vectors, their lifted midpoint projects to the cube center with output `M`. Its error is exactly `M`. Thus zero integer dimension is equivalent to `M<=epsilon`, including equality and arbitrary continuous lifting.

Taking `epsilon=k-1/2>0` for integer `k>=1` makes the zero case precisely `M<k`. Recognition of zero dimension on this graph-encoded family is coNP-complete: its complement is the ordinary NP-complete cut decision problem, with a Boolean cut as certificate. The note correctly makes no coNP membership assertion for unrestricted formulation inputs.

I checked the first page of the scanned primary [Garey, Johnson and Stockmeyer paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/JohnsonDavid2.pdf), which states completeness of Simple Max Cut with all edge weights one. This is the precise unweighted source needed here. The graph-quadratic identity is proved directly in the note. The midpoint parity argument is elementary and its prior provenance is acknowledged.

## Multiplicative and additive construction guarantees

Any finite multiplicative upper guarantee forces a valid constructed formulation to use zero integers on zero-optimum instances. Positive-optimum instances cannot have a valid zero-integer output. Counting the output integer coordinates therefore decides the cut problem. The argument only requires that the construction always produces a valid relaxation and reports its integer coordinates; it does not require solving that relaxation or checking its validity efficiently. The zero-optimum convention is essential to this obstruction and is stated explicitly.

For `t` independent copies with separate output error bounds, choose in each block either a maximum-cut Boolean vector or its complement. This gives `2^t` graph points. Every pair differs in at least one block; in that block its midpoint has true quadratic output zero and stored midpoint output `M>epsilon`. Hence no two selected graph lifts can share the parity of all integer coordinates. There are at most `2^p` parity vectors, even for unrestricted signed or unbounded integer variables, so `p>=t`. No closure or measurable-support argument is needed for this finite set.

For an assumed bound `p_out<=p_min+C N^(1-delta)`, put `N=tn`, `t=n^q`, with fixed integer `q>1/delta`. The ratio of the additive allowance to the no-case lower bound is `C n^(1-delta-q delta)`, which tends to zero. Consequently large instances distinguish output counts below `t` from counts at least `t`. Replication has polynomial encoding size because `q` is fixed. Constant-size dimensions can be enumerated or padded with isolated vertices. The unknown constant `C` in a hypothetical algorithm only determines a fixed threshold in this contradiction; it does not require a growing amount of advice. Values `delta>1` are already covered by the impossibility of a constant additive guarantee.

The benchmark can be either the binary minimum or the unrestricted-integer convex-lift minimum: both equal zero in the yes case and both are at least `t` in the no case. The statement is about the original input dimension `N`; it must not be silently replaced by the number of variables in the constructed lift or by its total encoding length.

Scaling every output by the positive rational `1/(k-1/2)` fixes every error tolerance at one. It preserves convexity and polynomial coefficient encoding. The incompatible midpoint error becomes `M/(k-1/2)>1`. Thus the fixed-accuracy variant is valid, though its coefficients are rational rather than the unscaled integer graph coefficients.

The limitations are accurately stated: polynomial replication rules out every fixed additive power `O(N^(1-delta))`. It does not by itself rule out all sublinear functions, such as `N/log N`, nor establish a linear additive lower bound.

## Exact finite checks

I enumerated all 75 simple labeled graphs on one through four vertices. Their Boolean maximum-cut values and complement identities passed. For every nonempty graph, I formed the eight selected graph points of a three-block product and checked every pair's differing-block midpoint. All 1,988 incompatibility checks passed at tolerance `M-1/2`. These finite checks support the reduction's identities; the dimension-independent proof supplies the complexity result.

## Positive-optimum strengthening: independently checked

The later section adjoining `8z^2` at unit tolerance also passes. Its two endpoint graph points force at least one integer coordinate: their midpoint output is four at input one half, where the true output is two. The displayed construction `z=(beta+r)/2`, exact `v=beta r`, and residual square triangle gives `w=2(beta+2v+s)` with absolute error at most one half. Every exact graph point is included, so both integer minima are exactly one.

Appending this scalar block to the replicated normalized graph instance gives low-case optimum exactly one and high-case lower bound at least `t+1`. The extra two endpoint choices multiply the pairwise midpoint-incompatible graph packing by two: pairs differing in a graph block violate that block's budget; pairs differing only in the scalar block violate its unit budget. The parity lower bound therefore applies without any direct-sum assumption about optimal integer counts.

With `N=tn+1`, the same fixed polynomial replication makes `C N^(1-delta)<t` eventually. Thus both additive error `O(N^(1-delta))` and multiplicative factor `O(N^(1-delta))` are impossible for valid polynomial-time construction under the promise that the optimum is positive, unless `P=NP`. This includes constant-factor impossibility on positive optima by taking `delta=1`. All tolerances remain exactly one and all coefficients remain rational with polynomial encoding. The stronger claim removes reliance on the zero-optimum convention; the proof and its stated scope are correct.
