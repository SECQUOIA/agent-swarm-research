# The sharp gap constant for incidence treewidth two

Status: the graph lemma, two-TU-block corollary, and sharp unit-box gap theorem passed two independent full-written audits: [first review](../notes/review-multilinear-treewidth-two-coloring.md) and [second review](../notes/review-multilinear-treewidth-two-second.md). The second review also covers the complete convex-cardinality and common-ratio positive-box extensions, including sharpness at every fixed bound ratio. A [focused primary-literature screen](../notes/multilinear-treewidth-two-novelty.md) found no exact antecedent for the one-sided two-color theorem, two-TU-row partition, or sharp gap consequence; novelty remains provisional. The integrality criteria and the series-parallel graph characterization used below are classical.

## Main theorem

Let f(x)=sum_{e in E} a_e product_{i in e} x_i on the unit cube, with a_e≥0. If the bipartite incidence graph of its monomial scopes has treewidth at most two, then, at every point,

**The termwise gap is at most twice the full convex-hull gap.**

The constant two is best possible, even for incidence graphs that become forests after deleting one variable vertex. Thus the worst ratio at incidence treewidth at most two is exactly two. At zero-gap points the displayed inequality applies without forming a ratio.

The theorem also holds on boxes with zero lower bounds and finite nonnegative upper bounds, by scaling the variables. The convex-cardinality corollary below also covers strictly positive boxes with a common bound ratio within each monomial. Arbitrary unequal positive bound ratios remain outside the theorem.

The main new proof ingredient is the following graph statement, which is stronger than the balanced-factor partition needed for the optimization theorem.

## A two-color theorem for one side of a bipartite series-parallel graph

**Graph lemma.** Let G=(V,F;I) be a finite simple bipartite graph of treewidth at most two. Its F vertices admit a two-coloring such that every cycle whose F vertices have a single color contains an even number of F vertices.

Consequently each color induces a totally unimodular incidence matrix, and in particular a balanced one. To verify total unimodularity, use Camion’s criterion for 0,±1 matrices: every submatrix with an even number of nonzeros in each row and column must have entry sum divisible by four. The bipartite support graph of such a submatrix has even degrees and hence decomposes into edge-disjoint cycles. Each cycle has an even number of F vertices by the graph lemma, so its length is divisible by four. The submatrix therefore has a number of ones divisible by four, as required. The claim also covers rectangular Eulerian submatrices; thus it covers every square submatrix in the criterion.

In particular, any 0/1 matrix whose bipartite support has treewidth at most two admits a partition of its rows into two totally unimodular submatrices. Balancedness alone would suffice for the optimization argument. A forbidden odd special Berge cycle corresponds to an induced incidence cycle with an odd number of F vertices; the graph lemma excludes all such monochromatic cycles, including cycles that are not induced.

We prove the lemma by an explicit invariant for two-terminal series-parallel networks. A network begins with a single edge and is formed by series composition, which identifies the sink of the first network with the source of the second, or parallel composition, which identifies both pairs of terminals. The component networks otherwise have disjoint vertex sets. Every intermediate network is bipartite and simple. A parallel composition in a simple graph cannot combine two networks that both have a direct edge between their terminals.

A coloring is **good** if every monochromatic-F cycle has an even number of F vertices. Only F vertices receive colors, denoted 0 and 1. A terminal path is called c-monochromatic if every F vertex on the path, including its terminals when they belong to F, has color c. Its parity is the number of F vertices on the path modulo two.

For every network there is a parity ε in {0,1} for which the following alternatives are available. Each alternative means a possibly different good coloring of the entire network.

| Terminal types | Required colorings |
| --- | --- |
| V,V | For either c, there is at least one c-monochromatic terminal path, every such path has parity ε, and there is no (1−c)-monochromatic terminal path. If ε=0, there is also a coloring with no monochromatic terminal path of either color. |
| V,F or F,V | For either prescribed color c of the F terminal, there is at least one c-monochromatic terminal path and all such paths have parity ε. If there is no direct terminal edge, there is also a coloring with that F-terminal color and no monochromatic terminal path. |
| F,F | For either prescribed common color c of both terminals, there is at least one c-monochromatic terminal path and all such paths have parity ε. If ε=1, there is also a coloring with these terminal colors and no monochromatic terminal path. For either choice of distinct terminal colors, a good coloring exists as well. |

The first alternative in each row is the **active** alternative, and an alternative with no monochromatic terminal path is the **blocking** alternative. For mixed terminals, a path of the other color is automatically impossible. For F,F terminals with different colors, every monochromatic terminal path is automatically impossible.

A network with a direct terminal edge must have mixed terminal types. For this case the invariant will always use ε=1.

### Base edge

For a single edge, prescribe either color to its unique F endpoint. The single terminal path has one F vertex. Thus ε=1 satisfies the mixed-terminal invariant. No blocking alternative is required because the terminal edge is present.

### Series composition

Let the common vertex have type δ, where δ=0 means V and δ=1 means F. If the two component parities are ε_1 and ε_2, use

ε = ε_1 XOR ε_2 XOR δ.

Every terminal path in the result concatenates one terminal path of each component, counting the common vertex twice before the correction δ. Every cycle lies in one component. Therefore compatible good component colorings always yield a good global coloring.

The active alternatives concatenate. When the common vertex is F, use the same color c there and at any outer F terminal. When the common vertex is V, choose the component active alternatives of the same color c. This produces at least one terminal path of color c, gives every such path parity ε, and excludes any other-colored terminal path where required.

We check all required blocking and endpoint-color alternatives explicitly.

1. **Outer terminals V,V, common vertex V.** Choose opposite active colors in the two components. No color has a terminal path through both components. This supplies the blocking alternative whenever it is required.

2. **Outer terminals V,V, common vertex F.** A blocking alternative is required only when ε=0, which means ε_1 and ε_2 are different. The even-parity component has mixed terminal types and cannot contain a direct terminal edge, because a network with such an edge uses odd parity. Prescribe the same color to the shared F vertex in both components, use the even component's blocking alternative, and use an active alternative in the other component.

3. **Outer terminals mixed, common vertex V.** One component has V,V terminals and the other has mixed terminals. Prescribe the outer F-terminal color c, use the opposite active color in the V,V component, and use an active coloring of the mixed component. This blocks every monochromatic terminal path in the series composition.

4. **Outer terminals mixed, common vertex F.** One component has mixed terminals and the other has F,F terminals. Give the common F vertex the color opposite to the outer F terminal. The F,F component has a good coloring with these distinct endpoint colors; choose a compatible active coloring of the mixed component. Again no monochromatic terminal path passes through both components.

5. **Outer terminals F,F with common color c, common vertex V.** A blocking alternative is required only when ε=1, so ε_1 and ε_2 are different. The even mixed-terminal component has no direct terminal edge and hence has a blocking alternative with its outer F terminal colored c. Use it, with a compatible active coloring of the other component.

6. **Outer terminals F,F with common color c, common vertex F.** Give the common vertex color 1−c. Both components then have distinct F-terminal colors, so both admit good colorings and neither admits a monochromatic terminal path.

7. **Outer terminals F,F with different colors.** If the common vertex is V, choose an active coloring in each mixed component with its prescribed outer F color. If the common vertex is F, prescribe any color to it, and use the active alternative or the distinct-endpoint alternative in each F,F component as appropriate. These choices are compatible and good.

These cases cover every terminal-type triple. A nontrivial series composition has no direct terminal edge, so all its required mixed-terminal blocking alternatives have been supplied.

### Parallel composition

Any new cycle consists of a terminal path in each component. If these paths are monochromatic in the same color, the number of F vertices in the cycle modulo two is

parity(first path) XOR parity(second path) XOR τ,

where τ is the number of F terminals modulo two. There are two F terminals or none when the terminal types agree, giving τ=0; mixed terminals give τ=1.

The following choices preserve the invariant.

- **V,V terminals.** If both component parities are even, use the same active color in both to obtain an even active coloring, or block both to obtain a blocking coloring. If both parities are odd, use the same active color in both, obtaining an odd active coloring. If one parity is odd and the other even, use an active coloring of the odd component and a blocking coloring of the even component. Thus the output parity is ε_1 OR ε_2. Whenever both components contribute monochromatic paths, their parities agree, so every new monochromatic cycle is even.

- **F,F terminals.** For prescribed equal endpoint colors, two even components can both be active, giving an even active coloring. Two odd components can both be active or both be blocked, giving the odd active and blocking alternatives. If one component is even and the other odd, activate the even component and block the odd one. Thus the output parity is ε_1 AND ε_2. For prescribed distinct endpoint colors, use the corresponding good coloring in both components; no new monochromatic cycle can cross between them because it would contain both terminals. Again every new monochromatic cycle formed from active components has even parity.

- **Mixed terminals with no direct terminal edge.** Both components have blocking alternatives with either prescribed F-terminal color. To obtain an active alternative, activate one component and block the other; choose either component's parity for the output. To obtain the blocking alternative, block both. No new monochromatic cycle crosses the components.

- **Mixed terminals with a direct terminal edge.** Simplicity ensures exactly one component contains that edge. Its invariant uses odd parity. Activate that component and block the component without a direct terminal edge. The output has odd parity, as required; a blocking alternative is not required.

This proves the invariant for every simple bipartite two-terminal series-parallel network.

### From networks to all graphs of treewidth two

A graph has treewidth at most two if and only if it has no K_4 minor; each of its nontrivial blocks is a two-terminal series-parallel graph. We use this standard characterization, not a new decomposition theorem. Apply the invariant to every block. A bridge is a base edge. At an articulation vertex in F, swap the two colors throughout a child block when necessary to match the already assigned articulation color. At an articulation vertex in V, no color needs matching. The block-cut graph is a forest, so this process is consistent. Color isolated F vertices arbitrarily. Every cycle lies in one block, and hence the resulting global coloring is good. This proves the graph lemma.

## Transfer from the graph partition to the gap

Let p_i=1−x_i. For each color class C of monomials, its scope incidence matrix A_C is totally unimodular by the graph lemma. Consider the polytope of failure vectors z in [0,1]^n defined by

sum_{i in e} z_i ≤ 1 if sum_{i in e} p_i ≤ 1,

sum_{i in e} z_i ≥ 1 if sum_{i in e} p_i > 1,

for all e in C. It contains p. Total unimodularity, preserved by row sign changes and by adding unit-vector rows, implies that this polytope is integral. Alternatively, the classical mixed packing/covering integrality theorem for balanced matrices gives the same conclusion. Therefore p is a convex combination of its binary points.

Use this convex combination as a joint distribution of the failure indicators. A packing row has at most one failure, so its union probability equals sum_{i in e}p_i. A covering row always has a failure, so its union probability is one. Thus the common distribution attains every individual monomial lower envelope in its color class at the prescribed means.

Equivalently, if u_e=min_{i in e}x_i and k(e) is an index attaining that minimum, the deficiency

d_e(X)=X_{k(e)}−product_{i in e}X_i

is nonnegative on binary points. The color-class distribution has E d_e=T_e for each e in that class, where T_e is its termwise gap. All other term deficiencies remain nonnegative. Mixing the two color-class distributions equally preserves every singleton mean and gives

sum_e a_e E d_e ≥ (1/2) sum_e a_e T_e.

For a positive multilinear polynomial, its concave envelope is sum_e a_e u_e, attained simultaneously by the comonotone distribution. Maximizing the displayed total deficiency over all common-marginal laws gives its full hull gap. This proves T≤2H. Constant and affine monomials have zero gap and may be discarded.

## Sharpness

For n≥2, use

f_n(a,x)=a sum_{i=1}^n x_i + product_{i=1}^n x_i,

at a=1/n and x_i=1−1/n. Its termwise gap is 2−1/n and its hull gap is exactly one. For completeness, if R is the number of failed x variables and A the binary anchor, then E R=1 and E A=1/n, and the total deficiency is

E[A R]+Pr(R≥1)−1/n.

The pointwise inequality A R+1[R≥1]≤R+A bounds this by one. Equality is attained by choosing exactly one failed x variable uniformly and an independent anchor A. Its incidence graph becomes a tree after deleting a and has treewidth two. Thus the ratios tend to two.

## Convex cardinality factors and common-ratio positive boxes

The stronger two-TU-block graph statement yields the same sharp constant for a larger class of factors. For each scope e, let φ_e(0),...,φ_e(|e|) be any discrete-convex sequence: its successive differences are nondecreasing. Let f_e be the unique multiaffine function whose binary vertex values are φ_e(sum_{i in e}X_i), and let f=sum_e f_e. Nonnegative factor weights can be absorbed into the sequences. These functions are multiaffine interpolants of the vertex costs; they need not equal a continuous extension of φ_e evaluated at sum_i x_i.

**Corollary.** If the factor incidence graph has treewidth at most two, then

sum_e [cav f_e(x)−vex f_e(x)] ≤ 2[cav f(x)−vex f(x)].

Proof. Write s_e=sum_{i in e}x_i and let ψ_e be the piecewise affine interpolation of φ_e at consecutive integers. The individual lower envelope is ψ_e(s_e), attained by any prescribed-mean law whose scope cardinality belongs to {floor(s_e),ceil(s_e)}. Jensen's inequality proves the lower bound; the two adjacent cardinalities make ψ_e affine on the support and give equality.

For either TU row class C, the polytope

{z in [0,1]^n: floor(s_e)≤sum_{i in e}z_i≤ceil(s_e) for all e in C}

is integral and contains x. Its binary-vertex decomposition therefore attains all local lower envelopes in that class simultaneously. Discrete convexity makes the vertex costs supermodular. Uncrossing two incomparable support sets into their intersection and union preserves singleton means and cannot decrease any factor expectation. A maximizing chain-supported law is the common-threshold law, so every factor's upper envelope is attained simultaneously and cav f=sum_e cav f_e. These single-factor facts are also proved in [the independently audited convex-cardinality note](convex-cardinality-frequency-two-gap.md).

Mix the two class distributions equally. Each factor contributes its full local range under its own class distribution, and contributes a nonnegative range under the other distribution because every prescribed-mean expectation is at most its individual upper envelope. The mixture therefore attains at least half of the sum of local ranges as a total deficiency from the common upper value. This proves the corollary. Its constant is sharp because positive monomials are included: on binary points, product_e X_i equals the discrete-convex cardinality sequence 1[k=|e|].

For the positive-box application, suppose 0<L_i<U_i and, within each original monomial scope e, all ratios U_i/L_i have a common value r_e. After normalization to binary box coordinates Z_i, that monomial's vertex table is

(product_{i in e}L_i) r_e^{sum_{i in e}Z_i},

a positive multiple of a discrete-convex cardinality sequence. Thus the original monomial factorization on such a box has the same factor-two gap bound whenever its incidence graph has treewidth at most two. The ratio condition applies to the original scopes and does not require expanding their products into new monomials.

**Sharpness at every fixed positive bound ratio.** For every fixed ρ>1, the supremum is still exactly two when every original variable has box [1,ρ]. The following equivalent construction on [ε,1], with ε=1/ρ and α=1−ε, proves the lower bound. Use

f_n(a,x)=(1/α) a sum_{i=1}^n x_i + product_{i=1}^n x_i,

and prescribe normalized means E A=1/n and E X_i=1−1/n, where a=ε+α A and x_i=ε+α X_i. All these means are strictly inside the box for n≥2. The incidence graph is unchanged from the preceding flower example and has treewidth two.

The normalized nonlinear part of each bilinear summand is α A X_i, so these summands contribute total termwise gap α. On binary vertices the large product equals ε^R, where R is the number of failed leaf bits. Its local lower envelope at E R=1 is ε; its upper envelope is 1−(1−ε^n)/n. Consequently

T_n=2α−(1−ε^n)/n.

Canceling the affine parts gives the exact hull-gap representation

H_n=max E[α A R+1−ε^R]−(1−ε^n)/n,

where the maximum is over the original common-marginal laws; in particular E R=1 and E A=1/n.

For any M>0, the inequalities 1−ε^r≤α r for integer r≥0 and 1−ε^r≤1 give

E[1−ε^R]≤α(1−E[R;R>M])+1/M,

α E[A R]≤α M/n+α E[R;R>M].

Thus H_n≤α+α M/n+1/M. Taking M=sqrt(n) gives limsup H_n≤α. Conversely, choose exactly one failed leaf uniformly and an independent anchor A. This feasible law has R=1 and yields

H_n≥α+α/n−(1−ε^n)/n.

It follows that H_n→α, while T_n→2α, and therefore T_n/H_n→2. Scaling every physical variable by ρ changes only the positive monomial coefficients and maps the box to [1,ρ]. The factor-two constant is therefore sharp for every fixed strictly positive common bound ratio, not only in the zero-lower-bound limit.

## Sources, verification, and scope

- Cornuéjols, [Combinatorial Optimization: Packing and Covering](https://www.andrew.cmu.edu/user/gc0v/webpub/notes.pdf), July 2000 author manuscript, Theorem 6.13 on printed p.82 (PDF p.84), proves the balanced-matrix mixed inequality integrality theorem used above. The stronger 0/1 TDI statement is Theorem 6.17, credited to Fulkerson, Hoffman and Oppenheim. Camion’s criterion used for the stronger two-TU-block graph corollary is Theorem 6.5, printed p.76. These integrality criteria are established theory.
- Hassin and Tamir, [Efficient Algorithms for Series-Parallel Graphs](https://www.math.tau.ac.il/~hassin/sp.pdf) (1986), printed pp.380–381 and Theorem 3.1, give the edge-based series/parallel construction and the characterization through biconnected components and exclusion of a subdivision of K_4. Eppstein, [Parallel Recognition of Series-Parallel Graphs](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf), Information and Computation 98 (1992), supplies the classical algorithmic framework. No new graph decomposition or recognition result is claimed.
- The exact finite-state search in [the discovery script](../code/search_series_parallel_factor_colors.py) closed under composition at 73 attainable signature types, with ten minimal types under containment. [Its output](../notes/series-parallel-factor-color-state-search.txt) is retained as proof-discovery evidence. The analytic invariant above supplies the proof and does not rely on accepting the computer search as a certificate.
- The result concerns positive monomial coefficients. Arbitrary nonnegative local factors can have gap ratio three at the same incidence treewidth, as shown by [the separately audited parity counterexample](binary-factor-width-two-counterexample.md).

The [earlier investigation](../notes/multilinear-treewidth-two-investigation.md) records complementary reductions and failed routes. The mathematical audits are linked above. The focused novelty screen is linked above; it found no exact match, and mathematical verification does not establish novelty.

## Lean verification

[Topic 19](../formal/topics/19-structural-multilinear/COVERAGE.md) formalizes the
one-sided all-cycle coloring theorem from an actual tree decomposition of
width at most two. Elimination and graph gluing supply the coloring; a
series-parallel representation or a TU partition is not an additional input.
The two TU classes then supply the cardinality-slab laws and the factor-two
gap bound, including the positive-monomial and common-aspect original-box
specializations.

The formal matrix argument uses an alternative to the Camion proof above:
pair selected rows within each column, leaving at most one unpaired row.
The incidence-cycle parity condition makes the graph of pairs bipartite.
Opposite signs on each pair give the Ghouila-Houri signing condition, whose
sufficiency for total unimodularity is proved in Lean. The subsequent slab
integrality argument is also proved, rather than assumed.

The unit flower has exact gaps and incidence treewidth exactly two. The
positive-box flower uses the same original scopes and proves the stated
termwise gap, attainable payoff representation, truncation bounds, eventual
positive hull gap and ratio limit two. Scaling proves supremum sharpness on
every fixed `[1,rho]` box with `rho>1`; no finite flower is claimed to attain
ratio two.

The [verification record](../formal/topics/19-structural-multilinear/VERIFICATION.md)
identifies the checks and reviewed source snapshots. Algorithm implementation,
recognition complexity and optimization/separation bit complexity are outside
this gap-verification package. The broader open questions above are unchanged.
