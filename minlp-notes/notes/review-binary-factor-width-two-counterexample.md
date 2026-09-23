# Independent audit: binary factor counterexample at incidence width two

Date: 2026-09-04. Reviewer: independent `fbbt` agent. Target: [binary-factor counterexample](../results/binary-factor-width-two-counterexample.md).

**Verdict: the counterexample is correct.** Its sum of local maximum payoffs is three, its jointly achievable maximum is one, and its incidence graph has treewidth exactly two. It also yields a literal termwise-envelope-gap to full-hull-gap ratio of three for the factors' multiaffine extensions. It does not resolve the positive-monomial-deficiency question.

## Payoffs and incompatible requirements

There are six binary variables, ordered as `AB1,AB2,BC1,BC2,CA1,CA2`, each with mean `1/2`. Write `E_AB` for equality of the AB pair and `N_AB` for inequality, and similarly for the other pairs. The factor payoffs are

`g_A=1[E_AB and E_CA]`,

`g_B=1[N_AB and E_BC]`,

`g_C=1[N_BC and N_CA]`.

Every payoff is either zero or one. Factors A and B cannot both equal one because they require opposite AB parities. B and C require opposite BC parities; A and C require opposite CA parities. Therefore `g_A+g_B+g_C<=1` at every binary vertex.

Each factor can attain one in expectation under its prescribed local singleton marginals. Choose any satisfying assignment of its four variables and mix it equally with its bitwise complement. Pair equality and inequality are unchanged by complementing both bits, so the factor stays one while each coordinate becomes fair. Thus all three independent local maxima equal one and their sum is three.

For the global maximum, mix `000000` and `111111` equally. All coordinates are fair, A equals one, and B and C equal zero. The expected sum is one and attains the pointwise upper bound. Hence the ratio of summed local maxima to the global maximum is exactly three.

## Literal hull gaps

Each factor also has a local fair law attaining zero: use any nonsatisfying assignment and its complement. Consequently each local envelope interval at the fair point is `[0,1]`.

The global sum has a fair zero-payoff law as well. Choose pair parities AB unequal, BC unequal, CA equal, for example assignment `010100`, and mix equally with its complement `101011`. A fails its AB condition, B fails its BC condition, and C fails its CA condition. Thus the full envelope interval at the six-dimensional fair point is exactly `[0,1]`, while the termwise relaxation interval is `[0,3]`. The gap ratio is therefore three, not merely a comparison between two payoff maxima.

For an explicit multiaffine polynomial representation, define

`E(s,t)=st+(1-s)(1-t)=1-s-t+2st`, and `N(s,t)=s+t-2st`.

Then use `g_A=E_AB E_CA`, `g_B=N_AB E_BC`, and `g_C=N_BC N_CA`. Each product involves disjoint pairs and is multiaffine. Its vertex values are precisely the stated binary payoff. These functions are nonnegative on the full cube. The graph's convex hull equals the convex hull of its vertex graph, so the binary marginal calculations establish the asserted continuous envelope values.

## Incidence treewidth

The incidence graph is bipartite between the three factor nodes and the six variable nodes. Each AB variable is adjacent to A and B, each BC variable to B and C, and each CA variable to C and A. Each factor has arity four, and each variable occurs in exactly two factors.

A tree decomposition consists of central bag `{A,B,C}` and six leaves, one bag `{A,B,ABr}`, `{B,C,BCr}`, or `{C,A,CAr}` for each `r=1,2`. Every incidence edge is in its corresponding leaf. Every variable occurs in one bag; each factor occurs in the center and its incident leaves, a connected subtree. Maximum bag size is three, proving width at most two.

The incidence graph contains the six-cycle `A-AB1-B-BC1-C-CA1-A`. Forests are exactly the graphs of treewidth at most one; therefore its treewidth is at least two. The incidence width is exactly two. The central bag need not induce a clique in the original graph; tree-decomposition bags have no such requirement.

Suppressing variable nodes gives a triangle of factor nodes with two parallel edges per pair. This is not a forest. The repeated shared-variable pairs are compatible with incidence width two and force nontrivial correlations beyond singleton means.

## Scope and prior mechanisms

The construction disproves a universal factor-two comparison for arbitrary nonnegative binary factor payoffs at incidence treewidth two, including the literal multiaffine envelope-gap version above. It does not disprove a theorem restricted to positive-coefficient monomials or to their specific deficiencies. Equality/inequality payoffs expand with signed coefficients and impose parity correlations; they are not instances of `X_anchor-product_e X_i` with positive monomial coefficients.

The mechanism is a small inconsistent local-correlation construction, closely related to standard constraint-satisfaction and marginal-consistency examples. No novelty claim is made for that general mechanism. The value here is a concrete exact obstruction to the proposed unrestricted factor argument.

## Exhaustive check

An independent enumeration of all 64 binary assignments found exactly 16 vertices with each payoff pattern `(1,0,0)`, `(0,1,0)`, `(0,0,1)`, and `(0,0,0)`, and no other pattern. Complement invariance held for every assignment. The seven-bag decomposition was also checked for all twelve incidence edges. The proof above is exact and does not depend on numerical optimization.

## General independent-set extension

The subsequent graph family also passes. Give each edge of a finite simple graph two fair bits, demand opposite pair parities at its endpoints, and let factor `v` pay `w_v>=0` precisely when all its demanded parities hold. Its local optimum is `w_v` by a satisfying assignment and complement. Satisfied factors always form an independent set, so their total payoff is at most `alpha_w(G)`. Conversely a maximum-weight independent set has no conflicting demands on an edge, and can be satisfied simultaneously; complement mixing makes all singleton marginals fair. Thus `T=sum_v w_v` and `H=alpha_w(G)` exactly. Extra satisfied factors cannot increase the total beyond the already maximal independent-set weight. Isolated vertices produce constant factors and cause no exception to this payoff formula.

For a graph with an edge, replacing every edge by two length-two paths has treewidth exactly `max(2,tw(G))`. An original tree decomposition plus attached endpoint-variable bags gives the upper bound. Contracting one path per edge and deleting the other makes `G` a minor; each doubled path also yields a four-cycle. These prove the two lower bounds.

For `G=K_(k+1)` **with unit vertex weights**, `k>=2`, the incidence width is `k`, arity is `2k`, variable frequency is two, and the payoff ratio is `k+1`. The unit-weight qualifier is necessary: arbitrary clique weights give `sum_v w_v/max_v w_v`, not necessarily `k+1`. This clarification was sent to the author. The general graph argument concerns the payoff comparison; its statement does not automatically assert that every graph's global minimum payoff is zero. The literal hull-gap conclusion proved earlier is independently valid for the explicit triangle.
