# Sharp asymptotic gap growth in incidence treewidth and sparsity

Date: 2026-09-04. Status: full written proof independently audited; no unresolved mathematical issue identified. Novelty is provisional.

## Main theorem

Consider positive-coefficient multilinear polynomials on the unit cube. Let:

- W(k) be the supremum of tbtgap/chgap over support incidence graphs of treewidth at most k.
- D(k) be the corresponding supremum for incidence degeneracy at most k.
- P(k) be the corresponding supremum for incidence graphs admitting an orientation with every outdegree at most k.

All suprema range over arbitrary dimensions, degrees, coefficients, and points with positive hull gap. Then

    W(k) ~ k,       D(k) ~ k,       P(k) ~ k.               (1)

Each leading constant is one. More precisely, for every integer k≥2,

    W(k)≥k,       D(k)≥k+1,       P(k)≥k+1,                (2)

while

    W(k)≤D(k)≤P(k)
         ≤k+min{k,B(k+1)}+κ,                              (3)

where κ=2/(1−exp(−1)) and B(d) is any proven uniform degree-d gap bound. The sharp degree theorem supplies B(d)∼ln d/ln ln d, so (3) is k+o(k).

These statements also apply to zero-lower-bound boxes by scaling. General positive-lower-bound boxes are outside the present structural theorem.

Apart from W(2)=2, established by the [treewidth-two theorem](positive-multilinear-treewidth-two-exact.md) on the same unit-cube class, the exact fixed-k values are not determined. The inequalities in (2) are supremum statements obtained by allowing the radix, and hence the dimension, to increase.

## A variable-radix lower construction

Fix integers L≥2 and b≥L. Set m=b^L. There are m leaf variables z_i and L anchor variables a_j. Label the leaves by words of length L over {0,...,b−1}. At level j, partition them into b^j blocks according to their first j digits. Let P_j be this partition and define

    p_(L,b)(a,z)=Σ_(j=1)^L Σ_(B∈P_j) a_j ∏_(i∈B) z_i.

Every coefficient is one. Evaluate at

    a_j=b^−j,       z_i=1−1/m.                            (4)

Each level-j term has concave-envelope value b^−j and convex-envelope value zero: its block contains m b^−j leaves, whose failure marginals sum to b^−j. Since level j contains b^j terms, its total term-by-term gap is one. Thus

    tbtgap=L.                                            (5)

We will show the exact hull gap

    chgap=1+(L−1)/b.                                     (6)

Consequently the ratio is L/[1+(L−1)/b], which tends to L for fixed L as b tends to infinity.

The coupling calculation has weaker hypotheses than the treewidth argument:
the upper bound (8) holds for integers `b≥1, L≥1`, and equality (6) is attained
for `b≥2, 2≤L≤b+2`. The construction above retains `b≥L≥2` because the exact
incidence-treewidth conclusion below uses that regime. No necessity claim is
made for the broader attainment range.

## Upper bound on the hull gap

In any admissible binary coupling let R be the total number of failed leaves, and let N_j count the level-j blocks containing a failed leaf. Then E R=1 and

    N_j≤min(b^j,R).

The total deficiency equals Σ_j A_j N_j, where A_j is the binary anchor. Hence the hull gap is at most the maximum of

    E Σ_j A_j min(b^j,R)

over all joint distributions with E R=1 and Pr(A_j=1)=b^−j.

For any fixed distribution of R, a nondecreasing function of R has largest expectation against an anchor of prescribed mean when the anchor selects the upper tail of R. This follows by exchanging selected probability at a smaller R with unselected probability at a larger R. All anchors can select their upper tails simultaneously.

Thus use a nonincreasing quantile R(U), U uniform, and set A_j=1[U≤b^−j]. On an interval where exactly the first l anchors are selected, put

    S_l(r)=Σ_(j=1)^l min(b^j,r).

For l≥1,

    S_l(r)≤r+Σ_(j=1)^(l−1)b^j.                            (7)

For l=0, S_0(r)=0≤r. Integrating (7) and using E R=1 gives

    chgap≤1+Σ_(j=1)^(L−1)b^j Pr(U≤b^(−j−1))
          =1+(L−1)/b.                                    (8)

This upper bound is sufficient for all the asymptotic lower claims.

## Exact attainment

Here is an explicit attaining law. Let l be the number of selected anchors under the preceding nested coupling. Its probabilities are

    w_l=(b−1)b^(−l−1) for 0≤l<L,
    w_L=b^−L.

Define two integer-valued failure-count profiles

    R_l^(1)=b^l for l≥1, and 0 for l=0;
    R_l^(2)=b^(l−1) for l≥2, and 0 for l≤1.

Their means are

    B_1=[(L−1)(b−1)+b]/b,
    B_2=[(L−2)(b−1)+b]/b².

For `b≥2` and `2≤L≤b+2`, we have `B_2≤1≤B_1`: the first inequality is
equivalent to `L≤b+2`, and the second follows from `L≥2`.
Mix these two profiles with a probability chosen so that E R=1. Both profiles
attain equality in (7) at every l, including l=0; at l=1 the two values are b
and zero. Therefore their mixture gives the objective in (8) exactly.

It remains to realize all block hit counts simultaneously. For a fixed integer R, take the first R leaves in base-b digit-reversal order. At level j their first j digits range over exactly min(b^j,R) distinct words. Apply a uniformly random coordinatewise digit shift modulo b. It preserves the number of hit blocks at every level and gives each leaf failure probability R/m.

Conditional on l and the chosen profile, use this failed-leaf set and put A_j=1[j≤l]. Since E R=1, every leaf has the required failure marginal 1/m, and the anchor means are b^−j. Thus this coupling attains (8), proving (6).

## Exact incidence treewidth

The incidence graph of this family has treewidth exactly L when b≥L.

For the upper bound, eliminate all leaf-variable nodes first. Each has exactly L factor neighbors, one from each level along its nested block chain. Eliminating the leaf only fills that chain into a clique.

Next eliminate factor nodes from level L down to level one. At the time a level-j factor is removed, its remaining neighbors consist of at most:

    j−1 factor nodes for its strict ancestor blocks,
    L−j+1 anchor nodes from levels j,...,L.

There are at most L such neighbors. This description follows by downward induction: eliminating a descendant factor only connects deeper anchors to its ancestor chain and to one another; it does not connect unrelated factor nodes. Finally eliminate the L remaining anchors, whose degree is at most L−1. This is an elimination order of width at most L.

For the lower bound, select one level-(L−1) block, containing b leaves. Each leaf is adjacent to the L−1 factor nodes on that block's ancestor chain. Its deepest bilinear factor also connects it to anchor a_L. Contract each of these deepest factors into its leaf. The resulting minor contains K_(L,b), with the L−1 ancestral factors and a_L on one side and the b leaves on the other.

When b≥L, K_(L,b) has a clique minor on L+1 nodes: pair L−1 distinct nodes from its two sides into connected branch sets, and leave one unused node from each side as the final two branch sets. All branch sets are pairwise adjacent. Treewidth is minor-monotone and a clique of size L+1 has treewidth L, so the original graph has treewidth at least L.

Taking L=k and then b→∞ proves W(k)≥k.

## Stronger finite lower bounds for orientations and degeneracy

For k≥2, use L=k+1 levels. Orient every deepest bilinear factor toward both its leaf and its anchor. Orient all other leaf incidences from the leaf to its factor, and orient each remaining factor toward its anchor.

Every leaf then has outdegree L−1=k. A deepest factor has outdegree two, every other factor has outdegree one, and anchors have outdegree zero. Thus the maximum outdegree is at most k. Equation (6) gives P(k)≥k+1 after b→∞.

The graph also has degeneracy at most k. Delete all deepest factor nodes, each of degree two; then delete their now-isolated anchor. Every leaf now has degree L−1=k. Delete the leaves, leaving only disjoint anchor-factor stars, which can be removed with degree at most one. Therefore D(k)≥k+1 by the same limiting argument.

This stronger finite bound does not apply to treewidth k: this L=k+1 family has treewidth exactly k+1.

It also disproves the possible finite bound tbtgap≤k chgap under incidence degeneracy k or maximum orientation outdegree k. Choose b>k². Then

    (k+1)/[1+k/b]>k.

For example, L=3 and b=5 give ratio 15/7>2 with incidence degeneracy at most two and an orientation of maximum outdegree two. This example has incidence treewidth three, so it does not disprove a factor-two conjecture at treewidth two.

## Matching upper asymptotics

A graph of treewidth at most k is k-degenerate, and a degeneracy ordering supplies an orientation of maximum outdegree k. Hence W(k)≤D(k)≤P(k).

Apply [the incidence-orientation theorem](positive-multilinear-incidence-sparsity-gap.md) with variable outdegree r=k and factor outdegree s=k. Its optional degree refinement gives exactly (3). Since B(k+1)∼ln k/ln ln k=o(k), (2) and (3) imply all three limits in (1).

## A sharp intermediate coupling parameter

The same construction also determines an intermediate parameter exactly. Fix a point where every term has exactly one low coordinate, with mean at most 1/2, and all other coordinates have means greater than 1/2. Suppose each high variable belongs to at most r terms, while low-anchor frequency is unrestricted.

The incoming-ownership construction, with all high incidences assigned to owners, gives

    tbtgap≤r chgap

without an independence component. In the radix family, every leaf is high and appears in L terms, while every anchor is low. Taking L=r and b→∞ proves that the supremum is exactly r for each integer r≥2. For r=1 the same upper bound is one, attained by a single nondegenerate monomial.

This parameter is not ordinary variable frequency: the deepest anchor in the lower family appears in b^L terms.

## Verification and novelty scope

The [topic-18 coverage map, PB37](../formal/topics/18-positive-box/COVERAGE.md)
links the radix incidence upper bound and exact attainment to
`Radix.incidence_expect_le_of_means` and `Radix.isGreatest_incidenceValues`.
Their respective hypotheses are `b≥1, L≥1` and `b≥2, 2≤L≤b+2`.
The [verification record](../formal/topics/18-positive-box/VERIFICATION.md)
reports the targeted builds, axiom audit and kernel replays. This coverage
concerns the coupling calculation; it does not establish the treewidth,
degeneracy, orientation or sharp structural asymptotics in this note.

The lower construction changes the radix of the earlier dyadic construction. A large radix was ineffective for sharpening degree-dependent asymptotics because it increases log degree; it is effective here because the number of levels controls incidence width and high-variable frequency.

The exact hull calculation, ownership interpretation, both treewidth bounds, orientation and degeneracy refinements, and all asymptotic claims passed [independent full written audit](../notes/review-multilinear-variable-radix.md). The treewidth argument was also checked by the root investigation. [An exact verification script](../code/verify_multilinear_variable_radix.py) checked 28 profile parameter pairs and five explicit graph eliminations; these checks supplement the analytic proof.

The earlier literature establishes bounded-incidence-treewidth tractability and classical forest exactness. The proposed new statement is the sharp leading-order growth of the original pointwise term-by-term gap ratio. Novelty remains provisional; see [the structural literature screen](../notes/multilinear-structural-novelty.md).
