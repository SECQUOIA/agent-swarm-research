# Exact incidence-treewidth-two gap: investigation

Status: the sharp constant two is now proved in [the exact treewidth-two theorem](../results/positive-multilinear-treewidth-two-exact.md), whose core graph and unit-box statements passed two independent full-written audits. This note records the investigation leading to that result. The established general bound and asymptotic result are in [the incidence theorem](../results/positive-multilinear-incidence-sparsity-gap.md) and [the sharp-growth theorem](../results/positive-multilinear-incidence-sharp-growth.md). This note preserves useful reductions and failed proof routes. The two elementary lemmas below passed a [separate full written independent audit](review-multilinear-treewidth-two-elementary-lemmas.md). They are auxiliary observations, not dependencies of the canonical exact treewidth-two theorem.

Throughout, a positive multilinear polynomial is evaluated at prescribed singleton means in the unit cube. Its termwise gap is T and its full convex-hull gap is H. Equivalently, for failure means p_i, the termwise contribution of scope e is min(1,sum_{i in e} p_i)−max_{i in e} p_i. Under any common joint law its contribution is Pr(at least one failure in e)−max_{i in e} p_i. Coefficients are nonnegative.

## A canonical-pair lemma on a forest

Let a forest have binary variables Y_i with prescribed means p_i. On each edge ij, let Q_ij be the midpoint of the two endpoints of the Fréchet interval of pair laws with these means. In particular,

q_ij = Q_ij(1,1) = [min(p_i,p_j)+max(0,p_i+p_j−1)]/2.

For every target subset S, there is a joint law M with these canonical edge marginals such that

Pr_M(there exists i in S with Y_i=1)
≥ [min(1,sum_{i in S}p_i)+max_{i in S}p_i]/2.

For S empty both terms on the right are defined as zero.

Proof. Every cell probability of a binary pair is affine in its (1,1) probability. Its canonical value is therefore the midpoint of its minimum and maximum feasible values. All cell probabilities are nonnegative, so Q_ij dominates half of every feasible pair law entrywise.

Choose a law P attaining target union probability c=min(1,sum_S p_i). Such a law exists by arranging target events to cover as much of the probability space as possible; auxiliary variables can be added with their prescribed means. The pair measures R_ij=2Q_ij−P_ij are nonnegative probability measures with singleton means p_i. On a forest these pair measures extend to a joint law R: root each component, sample the root, and sample children conditionally using the prescribed edge laws. Zero-probability conditioning states can be assigned arbitrarily. The mixture M=(P+R)/2 has all the canonical edge marginals. Every law with the target means has union probability at least b=max_S p_i, so M has target union at least (c+b)/2. This proves the claim.

The same argument gives a more general statement: for any nonnegative function g of an arbitrary target subset, a joint law with canonical forest-edge marginals attains at least half of the unconstrained prescribed-singleton maximum of E g. The union lemma improves this by retaining the unavoidable baseline b.

The forest hypothesis matters to this proof. On three fair bits, let P put probability one half on each constant assignment. The residual canonical pair laws 2Q_ij−P_ij require perfect anticorrelation on every pair. They cannot extend to a joint law on a triangle. This is a failure of the residual-gluing argument, not a counterexample for positive multilinear deficiencies.

## Compression of variables with identical factor neighborhoods

Suppose a nonempty block B of variables appears together: each positive monomial contains either all of B or none of B. Let

w = max(0,sum_{i in B} x_i−|B|+1).

Replace B by one binary variable W of mean w in each incident monomial, obtaining a reduced positive polynomial at reduced means. Then the original and reduced convex-envelope lower values coincide. Their termwise lower values also coincide. If Δ is the original concave-envelope value minus the reduced one, then Δ≥0 and

T_original = T_reduced+Δ,

H_original = H_reduced+Δ.

Consequently any valid ratio bound at least one for the reduced instance holds for the original instance.

Proof of the lower-value equality. In any original law define W as the product of the bits in B. Its mean is at least w by the Fréchet lower bound. If this mean exceeds w, independently thin its ones until the mean is w. Positivity of the reduced polynomial means this thinning cannot increase the objective; coordinates outside B retain their means. Thus the reduced lower optimum is no larger than the original one.

Conversely, choose a law of the bits in B with the original means whose product has mean w. Such a law exists because the Fréchet bound for one monomial is attainable. Given any reduced law, sample the bits in B conditionally on its value of W, using this local law. The product equals W almost surely and each original singleton mean is recovered. This lifts the reduced law without changing the objective and proves the reverse inequality. Conditional laws on null states are irrelevant.

For a monomial consisting of B and another set C, the two termwise lower values are

max(0,sum_B x_i+sum_C x_i−|B|−|C|+1)

and max(0,w+sum_C x_i−|C|).

They agree: if sum_B x_i−|B|+1 is nonnegative, substitute its value; otherwise both expressions are zero because sum_C x_i≤|C|. The reduced concave monomial value is min(w,min_C x_i), whereas the original is min(min_B x_i,min_C x_i). The first is no larger because w≤min_B x_i. Empty C means the reduced monomial is affine W. Summing establishes all claims.

This reduction removes pure large twin-variable intersections, such as two factor nodes sharing many variables. It does not remove intersections whose variables have different attached factor neighborhoods. No extension to arbitrary local payoff functions is asserted.

## Numerical checks and limitations

[The numerical search](../code/search_multilinear_treewidth_two.py) checked 1,800 prescribed-mean instances on 150 generated support hypergraphs with five to nine variables. It optimizes over all joint binary laws and all nonnegative coefficient choices through a max-min LP. The largest numerical ratio observed was 1.5625; see [the recorded output](multilinear-treewidth-two-search.jsonl). This finite search does not establish a universal bound and does not contain large flower examples approaching two.

The graph test repeatedly removes a vertex of degree at most two, filling its two neighbors when necessary. It certifies incidence treewidth at most two. The known orientation/degeneracy-two example with ratio 15/7 has incidence treewidth three and therefore does not settle this question.

## A possible balanced-matrix route

A sufficient graph statement would be: every bipartite graph of treewidth at most two admits a two-coloring of its factor side such that each resulting incidence subgraph is balanced, meaning it has no induced cycle of length congruent to two modulo four. Classical sign-pattern exactness for positive minimization on balanced hypergraphs would then supply a coupling for each color, and mixing the two couplings would give T≤2H.

This graph-coloring statement was subsequently proved in stronger form in [the exact treewidth-two theorem](../results/positive-multilinear-treewidth-two-exact.md): each factor color has no cycle with an odd number of factor vertices, and its incidence matrix is in fact totally unimodular. The proof uses a two-terminal series-parallel active/blocking parity invariant. The discussion below records the original route to the result. It is weaker than partitioning the factors into incidence forests: K_(2,m) is balanced despite requiring arbitrarily many factor colors for such a forest partition. The optimization implication follows directly from Theorem 6.13 in Cornuéjols, [Combinatorial Optimization: Packing and Covering](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf), printed p.82 (PDF p.84), which establishes integrality for balanced matrices with any mixture of packing and covering rows and unit-cube bounds. Its stronger TDI form for 0/1 matrices is Theorem 6.17, credited to Fulkerson, Hoffman and Oppenheim. Thus this exactness mechanism is classical.

To see the application, let A be the scope incidence matrix and p the failure means. Impose sum_{i in e} z_i≤1 when sum_{i in e}p_i≤1, and the reverse inequality otherwise. The resulting integral polytope contains p. Decomposing p into its binary vertices gives union probability sum_{i in e} p_i on a packing row and one on a covering row, simultaneously attaining every termwise lower monomial value.

[A separate combinatorial search](../code/search_multilinear_balanced_partition.py) generated 5,000 incidence-treewidth-two supports, enumerated their induced odd-half-length cycles, and checked whether their factor-node sets admit a nonmonochromatic two-coloring. Every generated instance admitted such a coloring; [the output](multilinear-balanced-partition-search.jsonl) records the count. This remains finite evidence only. The source of the support generator and the numerical search's range limit apply here too.

A stronger experimental variant forbade monochromatic induced cycles of every length at least six, by replacing the script's cycle acceptance condition `len(cycle) % 4 == 2` with `len(cycle) >= 6`. All 5,000 generated supports also passed that two-chordal-bipartite-class test; [the output](multilinear-chordal-bipartite-partition-search.jsonl) is retained. The analytic theorem does not prove this stronger induced-cycle statement, which remains an unresolved possible strengthening. The investigation was closed at the user's stop request.

The proposed broader shortcut through arbitrary nonnegative local payoffs is false already at incidence treewidth two. An independent agent found three mutually incompatible local parity payoffs, each locally attainable with probability one and fair singleton means, whose global sum is at most one. See [the exact counterexample](../results/binary-factor-width-two-counterexample.md). It does not use positive-coefficient monomials.
