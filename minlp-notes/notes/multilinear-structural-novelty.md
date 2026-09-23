# Independent novelty screen for structural positive multilinear gap bounds

Date: 2026-09-04. This is a bounded primary-literature comparison, not proof of novelty. It concerns the scalar, pointwise term-by-term versus convex-hull gap, with prescribed original coordinates. It does not audit the proofs afresh.

## Findings

Latest extension: [the sharp incidence-growth theorem](../results/positive-multilinear-incidence-sharp-growth.md) proposes worst-case ratios asymptotic to `k`, with leading constant one, for incidence treewidth, degeneracy, and minimum maximum orientation outdegree. The additional screen below found no exact antecedent. Known bounded-incidence-width extended formulations already compute the full hull; they do not quantify the original termwise relaxation. The earlier statements about unresolved sharp sparsity dependence below are superseded by this extension. Final proof status follows the separate mathematical audit.

| Local statement | Closest verified prior mechanism | Assessment from this screen |
|---|---|---|
| [Frequency two: sharp `3/2`, refined to `g/(g-1)` by dual odd girth](../results/positive-multilinear-frequency-two-gap.md) | Fractional matching half-integrality, bipartite dependent rounding, and exact cycle-hypergraph hulls | No exact quantitative all-dual-graph statement found. The bipartite exactness corollary follows directly from classical dependent rounding. The half-integral reduction and odd-cycle rounding are classical combinatorial ingredients. |
| [Feedback-variable bound `2^f`, sharp supremum two for `f=1`](../results/positive-multilinear-feedback-gap.md) | Forest marginal gluing and conditioning on a feedback set | No exact fixed-singleton-marginal domination or resulting gap bound found. Conditioning and forest inference alone do not establish the bound. |
| [Incidence orientation: `r+s+2/(1-e^-1)` and its refinement](../results/positive-multilinear-incidence-sparsity-gap.md) | Sparsity orientations, disjoint allocation rounds, and elementary coverage estimates | No matching fixed-marginal scalar-gap theorem found. Final mathematical status must follow its separate audit; this screen does not validate an unaudited candidate. |

The orientation theorem, if verified, is the broadest structural statement among these: it gives a degree-independent constant for bounded incidence degeneracy and thus bounded incidence treewidth. This differs from known exact algorithms that introduce stronger formulations. The feedback result remains useful because it handles positive lower bounds on the original box and gives the sharp one-feedback-variable constant. The frequency-two theorem provides a substantially better sharp constant than the general orientation argument.

## The comparison quantity matters

For a positive unit-box polynomial, put `p_i=1-x_i`, and write

`U(p)=sum_e a_e min(1,sum_(i in e) p_i)`,

`L(p)=sum_e a_e max_(i in e) p_i`,

`M(p)=max E[sum_e a_e 1{some i in e fails}]`,

where the maximum preserves every failure marginal. Then

`tbtgap=U-L`, and `chgap=M-L`.

A ratio bound `tbtgap <= C chgap` is equivalent to

`M >= U/C + (1-1/C)L`.

An ordinary coverage bound `M >= U/C` lacks the second term and therefore does not prove the claimed ratio. Nor can an algorithm freely shrink or enlarge the marginals. This distinction must remain explicit in comparisons with coverage approximation and correlation-gap results.

The distinction already appears for one bilinear term. Set failure marginals to `(1-epsilon,epsilon)`, with `0<epsilon<=1/2`. Here `U=1`, `L=1-epsilon`, and optimal excess coverage is `epsilon`. Independent rounding gives coverage `1-epsilon+epsilon^2`, whose excess is only `epsilon^2`. Thus independent coverage can be close to optimal in its absolute value while its excess above the baseline has an arbitrarily bad ratio.

Equivalently, the local deficiency `g_e(X)=X_(anchor)-product_(i in e) X_i` is a nonnegative, generally nonmonotone submodular function. Negative monomial indicators are submodular, and adding a modular function preserves submodularity. The two-variable obstruction is the familiar directed-cut example.

Chekuri and Livanos, *On Submodular Prophet Inequalities and Correlation Gap*, Theorem 1.1, quantify the ordinary nonmonotone correlation gap with a factor depending on `1-max_i x_i`. Their Theorem 1.2 obtains a constant guarantee by moving to a smaller marginal vector. Their introduction and Appendix B explicitly discuss the two-variable directed-cut obstruction. These statements do not yield our structural, fixed-marginal comparison. [Primary manuscript, arXiv:2107.03662](https://arxiv.org/html/2107.03662).

Rubinstein and Singla, *Combinatorial Prophet Inequalities*, Definition 4.4 and Theorem 4.5, use a modified function that permits choosing a subset after independent sampling. This also changes the relevant feasible distribution and is not a theorem about preserving our original marginals. [Primary manuscript, arXiv:1611.00665](https://arxiv.org/pdf/1611.00665).

## Frequency two and dependent rounding

Gandhi, Khuller, Parthasarathy, and Srinivasan, *Dependent Rounding and its Applications to Approximation Algorithms*, Theorem 2.3, preserves every edge marginal and rounds each bipartite vertex degree to its floor or ceiling. Section 2.3, Theorem 2.5, treats general graphs with additive degree deviation at most two. Its algorithm eliminates even cycles and linked odd cycles, then rounds one edge of each remaining odd cycle and finishes on a forest. This is close classical cycle-based rounding machinery; its guarantee is not the present odd-girth excess-coverage inequality. [Primary author manuscript](https://www.cs.umd.edu/~srin/PDF/2006/depround-jou.pdf).

Version caution: an earlier conference-paper search extract described recursive bipartitions with a logarithmic degree error. Full inspection of the linked journal manuscript superseded that preliminary description with the sharper additive-two theorem above.

The exact reduction to the local bipartite corollary is immediate. Apply their theorem to the dual graph, with edge marginals `p_i`, and let `D_v` be the rounded degree at a monomial vertex. If `s_v=sum_(i incident v)p_i<1`, then `D_v` is zero or one and `Pr(D_v>=1)=E D_v=s_v`. If `s_v>=1`, then `D_v>=1` surely. Hence expected coverage at each term equals `min(1,s_v)`, simultaneously. This attains every individual positive-monomial convex-envelope bound and proves scalar gap equality. Dummy vertices cause no issue. Parallel edges can be handled by the same alternating-path rounding or by the standard integral bipartite degree polytope. This corollary should be attributed to classical rounding/integrality, even if its MINLP phrasing is useful.

The nonbipartite proof in the local note first decomposes into vertices of a degree-slab polytope, then rounds disjoint half-integral odd cycles. The vertex structure is classical fractional matching structure. Barrus, *On fractional realizations of graph degree sequences*, Theorem 2.1, records it for the bounded fixed-degree polytope. The degree-slab extension is elementary, as the local proof shows. [Open published paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf/).

What this screen did not locate in a prior statement is the combination that gives, at every term,

`Pr(covered) >= (1-1/g) min(1,sum p_i) + (1/g) max p_i`,

after averaging the fractional decomposition, and thus yields the sharp scalar gap factor. The matching/complement construction on an odd cycle and the bilinear odd-cycle extremal example are not by themselves new combinatorial objects. The potential contribution is this exact baseline-sensitive use of them for arbitrary frequency-two positive multilinear polynomials.

## Full multilinear hulls and the odd-cycle literature

Del Pia and Walter, *Simple odd beta-cycle inequalities for binary polynomial optimization*, Section 6, Proposition 17 and Theorem 18, give exact full multilinear-polytope descriptions for cycle hypergraphs using flower and odd-cycle inequalities. Their definition of cycle hypergraph restricts each hyperedge to meet only its predecessor and successor, with an additional triple-intersection restriction for triangles. [Open published primary article](https://link.springer.com/article/10.1007/s10107-023-01992-y).

Every variable having frequency two does not impose that restriction on the whole dual graph: a monomial can meet arbitrarily many other monomials. The local frequency-two proof instead reduces a marginal decomposition to disjoint odd cycles. Therefore the published cycle-hypergraph theorem is close prior structure, but its theorem statement is not the same all-frequency-two gap theorem.

This distinction is not a proof that no derivation from existing hull inequalities exists. The cycle inequalities may provide an alternative route to the same ratio. A publication would need a careful comparison with that possibility. In particular, do not claim a new full hull description or a new odd-cycle cut family on the strength of the scalar bound.

## Feedback sets, marginal gluing, and width

Pletscher and Ong, *Part & Clamp: Efficient Structured Output Learning*, uses feedback-vertex conditioning to obtain tractable forest inference. It establishes the standard status of this framework. The local theorem's additional claim is that one law, preserving the given singleton means, can repair all local laws with one uniform `2^-f` domination loss. A theorem about conditioning and computing a partition function does not itself imply that claim. [Primary conference paper](https://proceedings.mlr.press/v22/pletscher12a/pletscher12a.pdf).

Del Pia and Khajavirad, *Beyond hypergraph acyclicity: limits of tractability for pseudo-Boolean optimization*, reviews bounded incidence-treewidth tractability and distinguishes incidence and primal treewidth. This is relevant prior theory for exact algorithms, not a quantitative guarantee for the original termwise relaxation. [Primary author manuscript](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/24/24T_016.pdf).

The incidence-forest case is already known at the stronger lifted-polytope level through Del Pia and Khajavirad's *The Multilinear Polytope for Acyclic Hypergraphs*. The existing local notes correctly attribute this base case. Direct retrieval of [the primary NSF-hosted article](https://par.nsf.gov/servlets/purl/10081429) failed in this screen; the later primary papers corroborate the result. This retrieval limitation should not be reported as fresh full-text verification.

Searches through feedback-set conditioning, local marginal polytopes, fixed-marginal approximation, Bernoulli coupling, and Frechet domination did not find the exact universal repaired-law statement or the resulting `2^f` multilinear ratio. These misses are inconclusive. The generic nonnegative-payoff sharpness is a separate statement from sharpness for positive monomials and must remain separated, as in the current proof.

## Incidence orientations

The candidate uses variable outdegree at most `r` and factor outdegree at most `s`. It separates terms by low and high means, assigns incoming incidences to `r` rounds so each high variable has at most one owner, and handles the at-most-`s` outgoing high variables separately. No exact antecedent for its simultaneous fixed-marginal deficiency guarantee was found in the targeted coverage/sparsity/rounding searches.

The ownership labels are an elementary incidence allocation; bounded-outdegree orientations and the implication from degeneracy or treewidth are standard. The `1-e^-1` estimate is the usual independent coverage inequality. Those ingredients should not be presented as new. The proposed content is their assembly into a pointwise ratio for the original relaxation, with no dependence on monomial degree.

The refinement `r+min{s,B(s+1)}+2/(1-e^-1)` uses a separate degree-dependent result `B`. Its status inherits every hypothesis and review limitation of that result. This screen does not establish sharp dependence on incidence sparsity or frequency. In particular, the upper bound linear in frequency and the lower family approaching two leave a large unresolved gap.

## Coverage and limitations of the screen

Queries included term-by-term multilinear gaps, positive/read-twice/frequency-two multilinear polynomials, odd-girth coverage rounding, nonbipartite marginal rounding, balanced hypergraphs and convex envelopes, concave closures and sums of coverage functions, nonmonotone correlation gaps, feedback sets and local distributions, and incidence degeneracy/arboricity. Primary statements were inspected for the close results listed above. Several broad queries returned largely irrelevant material; they provide little negative evidence.

Current positioning: **no exact prior quantitative theorem found in this bounded screen; classical ingredients and exact special cases identified; potential new scalar-gap applications remain provisional pending broader literature comparison and the separate mathematical reviews**. Of the three, the orientation result offers the broadest new structural coverage, while frequency two and feedback one offer sharp constants. None should be described as certainly unknown solely because this search found no match.

## Extension: sharp leading growth in incidence width

The new result takes a supremum over all positive multilinear polynomials on unit boxes, all dimensions and degrees, and all points with positive hull gap, subject to a bound `k` on the stated graph parameter. If `W`, `D`, and `P` denote these suprema for incidence treewidth, degeneracy, and orientable maximum outdegree respectively, the current draft gives

`W(k) >= k`, `D(k) >= k+1`, `P(k) >= k+1` for integers `k>=2`,

and

`W(k) <= D(k) <= P(k) <= k + min{k,B(k+1)} + 2/(1-exp(-1))`.

Here the independently developed degree bound satisfies `B(k+1)=o(k)`. Consequently all three ratios to `k` tend to one. This is a sharp leading asymptotic, not an exact formula at each fixed `k`. The lower statements are suprema: the radix tends to infinity with the number of levels fixed. Scaling covers boxes with zero lower bounds; arbitrary positive lower bounds remain outside this result.

The variable-radix family has exact ratio `L/[1+(L-1)/b]` and incidence treewidth exactly `L` for `b>=L`. Its nested-block construction reuses the earlier local counterexample mechanism. Its additional content is the exact joint-distribution calculation, graph-parameter analysis, and matching with the incidence upper bound. The ownership-label allocation and elementary graph implications are classical; the sharp scalar-gap comparison is the candidate contribution. The final written construction was available to this screen; this is a literature comparison, not a substitute for its independent proof audit.

### Exact bounded-width formulations are already known

Capelli, Del Pia, and Di Gregorio, *A Knowledge Compilation Take on Binary Polynomial Optimization*, Theorem 1, gives polynomial-size extended formulations for the full multilinear polytope under bounded incidence treewidth, even allowing width logarithmic in a polynomial of the instance size. Theorem 7 gives a representation of size `2^{O(t)} poly(|V|,|E|)`; Section 6 turns the representation into an extended formulation. Theorem 2 extends their framework to literal monomials and additional cardinality conditions. This is direct prior theory for **incidence** width, so the local theorem must not be presented as the first way to optimize or represent the hull at bounded incidence width. [Primary manuscript, arXiv:2311.00149v2, Theorems 1, 2, and 7](https://arxiv.org/pdf/2311.00149).

The distinction is quantitative: an exact extended formulation adds global consistency information, whereas the local theorem bounds the loss from using the original sum of individual envelopes. Computing both endpoints efficiently does not establish a uniform relation between them. In particular, fixing singleton means in an exact hull formulation is legitimate but does not itself provide the comparison constant.

Kolman and Koutecky, *Extended Formulation for CSP that is Compact for Instances of Bounded Treewidth*, Theorem 1, proves a size `O(D^tau n)` formulation. Their constraint graph, defined in Section 1.1, joins variables appearing together in a constraint: its width is **primal** width. Section 2.1 explicitly distinguishes the locally consistent singleton/factor LP from the stronger bag-based formulation in Section 2.2. This source supports exact higher-order consistency, rather than a gap guarantee for the initial LP. [Primary manuscript, arXiv:1502.05361v2](https://arxiv.org/pdf/1502.05361).

A large monomial alone has incidence treewidth one and primal treewidth equal to its degree minus one. Thus replacing incidence width by primal width can materially weaken a degree-independent statement. Even so, the Capelli--Del Pia--Di Gregorio result already handles the correct incidence parameter, so parameter distinction alone is insufficient novelty positioning.

### A generic nonnegative CSP extension would be false

Here is a direct reformulation of the already reviewed generic-payoff example in [the feedback note](../results/positive-multilinear-feedback-gap.md). It is a scope check, not a separate priority claim.

Fix `k` binary variables, each with mean `1/2`. For every assignment `s` in `{0,1}^k`, introduce the nonnegative payoff `g_s(X)=1{X=s}`. A separate local law can give `g_s` expectation `1/2`, by assigning probability one half to `s` and one half to its bitwise complement. No local law preserving the fair means can exceed one half. Consequently the sum of independently optimized local payoffs is `2^(k-1)`.

Under every global law, however, `sum_s g_s(X)=1` identically. The optimum preserving all means is therefore one, and the fixed-marginal local/global ratio is exactly `2^(k-1)`. The incidence graph is `K_(k,2^k)`, of treewidth `k`. If distinct factor scopes are required, give every payoff its own private variable of mean one and multiply by that variable. This adds only pendant variable nodes and leaves both optima and the treewidth unchanged.

Thus there cannot be a generic linear-in-incidence-treewidth comparison for arbitrary nonnegative binary factor payoffs with fixed singleton marginals. The positive-monomial deficiency structure used by the new theorem matters. Indicator payoffs containing zero literals fall outside that structure. This also explains why generic local-polytope or CSP approximation results cannot automatically supply the claimed leading constant. Ordinary unconstrained CSP approximation may change the singleton marginals, which is another difference from the present comparison.

### Updated novelty assessment

Additional queries covered incidence treewidth and multilinear gaps, local-polytope approximation ratios under prescribed marginals, term-by-term gaps and treewidth, and incidence orientation or degeneracy in polynomial convexification. The close primary statements above concern exact formulations, hierarchical consistency, or standard coverage rounding. No inspected theorem supplies the local `k+o(k)` comparison or its matching positive-monomial lower family.

The defensible claim is therefore: **a candidate sharp asymptotic description of the original pointwise scalar relaxation gap in three incidence graph parameters, with no exact antecedent found in this bounded primary-literature screen**. It should be positioned alongside known exact bounded-width hull formulations and the older positive-coefficient constant-gap conjecture, while keeping its separate mathematical review status explicit. This is stronger evidence of a substantive distinction than merely noting that a search for its terminology failed; it remains insufficient to certify that the result has never appeared under another formulation.
