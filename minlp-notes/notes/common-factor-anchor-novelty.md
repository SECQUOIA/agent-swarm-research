# Independent novelty audit: a convex anchor and common-factor products

Date: 2026-09-04. Scope: [the exact reciprocal-anchor hull](../results/common-factor-reciprocal-anchor-full-hull.md), including its extension to one continuous convex anchor. This note complements [the author's literature audit](common-factor-literature-audit.md). It is a bounded open-literature search, not a certificate of novelty.

## Assessment

No exact antecedent was found for the explicit original-space hull test based on the upper envelope of `2n+2` affine functions, together with exact rational separation and decomposition for arbitrarily many leaves. This remains a plausible useful specialization. Its classical probabilistic foundations are strong enough that the general convex-anchor theorem should be presented as an application of existing theory, not a new theorem about convex order.

Two additional qualifications are material:

1. SOCP representability of the entire reciprocal block already follows from an existing theorem on a single bipartite bilinear equality. Its generic formulation has exponential size.
2. Linear optimization over the block is already an elementary scalar problem with at most `n` thresholds. Thus mere polynomial weak optimization or generic weak separation would be a weak novelty claim. The explicit rational membership test, separator, common distribution, and decomposition are the more specific potential contribution.

The ongoing Oh–Wiecek–Yang work below is a direct unresolved application-overlap risk. No claim of certain novelty or publishability is supported by this audit.

## Classical mechanism and limits of a general claim

For fixed mean `m`, each prescribed leaf pair `(q_j,w_j)` asks that `(q_j,w_j)` belong to the lift zonoid of the common law. Its two call-function inequalities are precisely the upper- and lower-tail selection bounds. Taking their least simultaneous dominating call function is the fixed-mean convex-order join. Minimization of every convex anchor under that least law then follows from the definition of convex order. The existence of the join and the lift-zonoid characterization are established results, with primary references and theorem numbers in [the author's audit](common-factor-literature-audit.md).

Tehranchi's *A Black–Scholes inequality: applications and generalisations* gives another explicit presentation of the same threshold transform: the upper boundary is `inf_s {q s + E[(X-s)_+]}` and the lower boundary is obtained by complementing the selection. See [the primary Cambridge manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/faec2798-4aff-4ed4-afd4-5d81976ad605/content), also [arXiv:1701.03897](https://arxiv.org/abs/1701.03897). This reinforces that the local fixed-law selection lemma is classical.

The genuinely application-specific work is converting these facts into a complete convex hull in MINLP coordinates, integrating the envelope for the reciprocal, and furnishing explicit certificates. Whether that specialization has appeared elsewhere remains uncertain.

## A known theorem already gives SOCP representability

Dey, Santana, and Wang, *New SOCP relaxation and branching rule for bipartite bilinear programs*, Theorem 1, considers a box-domain bipartite bilinear graph with all selected product coordinates and one linear equality in the original variables and products. It proves that its convex hull is SOCP representable. Remark 1 explains the endpoint-fixing disjunction and its exponential number of pieces. [Primary manuscript, pages 2–3](https://optimization-online.org/wp-content/uploads/2018/03/6542.pdf).

Here is the exact reduction, supplied in this audit. Set the bipartition to `{X}` and `{T,Y_1,...,Y_n}`, retain all products `XT,XY_1,...,XY_n`, and impose the single equality `XT=1`. Use `X in [a,b]`, `T in [1/b,1/a]`, and `Y_j in [0,1]`. After ordinary affine box normalization, this is an instance of that theorem. The coordinate `XT` is fixed and can be projected out. The resulting hull is exactly the reciprocal-anchor hull.

Consequently, SOCP representability alone is already known for every `n`. This reduction does not provide the local original-space formula or a polynomial-size SOCP formulation. The explicit line-envelope algorithm can still improve substantially on the generic disjunction. Do not confuse a polynomial separation algorithm with a polynomial-size SOCP extended formulation.

## Exact projective equivalence to a square-anchor star

He, Liu, and Tawarmalani, *Convexification techniques for fractional programs*, Theorem 2.1 and Remark 1, establish the positive projective convex-hull correspondence and transfer of separation. Section 5 develops inverse-function moment hulls. Section 6.3 convexifies several univariate reciprocals jointly and then applies McCormick inequalities to their products with leaf variables; the latter step is explicitly a relaxation. [Primary manuscript, arXiv:2310.08424v2](https://arxiv.org/html/2310.08424).

The following application is useful for searching equivalent formulations. At a graph point, division of all coordinates by `X>0`, with reordering, takes

`(X,1/X,Y,XY)` to `(s,s^2,Y,sY)`, where `s=1/X`.

At the convex-hull level the precise coordinate map is

`Phi(m,t,q,w) = (1/m, t/m, w/m, q/m)`.

It maps the reciprocal-anchor hull bijectively onto

`conv{(s,s^2,Y,sY): 1/b <= s <= 1/a, 0 <= Y <= 1}`.

This statement follows either from the cited projective theorem or directly by reweighting a mixture: replace weight `lambda_k` by `lambda_k X_k/m`, and then put `s_k=1/X_k`. The new weights sum to one and yield exactly the displayed transformed coordinates. Applying the same construction with `s` gives the inverse. This is not a claim that reciprocal expectation equals reciprocal mean under the original law.

Thus a pre-existing hull description for a square moment and a star of cross moments would also settle the reciprocal case. Targeted searches for a square anchor, quadratic star hull, one diagonal moment, and common-variable quadratic convexification found no exact envelope/oracle antecedent. The projective correspondence itself must not be claimed as new.

## Why polynomial linear optimization is already simple

The following calculation is elementary and does not use the proposed hull theorem. Minimize an arbitrary linear functional over the graph:

`alpha X + beta/X + sum_j (gamma_j + delta_j X)Y_j`.

For fixed `X`, choose `Y_j=0` when its coefficient is positive and `Y_j=1` when negative; ties do not matter. The remaining objective is

`F(X) = alpha X + beta/X + sum_j min{0,gamma_j+delta_j X}`.

There are at most `n` interior breakpoints, the valid roots of `gamma_j+delta_j X=0`. Sorting them partitions `[a,b]` into at most `n+1` intervals. On each interval, `F(X)=A X+B+beta/X`. Its minimum is attained at an endpoint or at `sqrt(beta/A)` when `A,beta>0` and that point lies in the interval. If `beta<=0`, the function is concave or affine, so interval endpoints suffice; the other sign cases are monotone. Sorting and updating the active affine sum gives `O(n log n)` arithmetic work and at most `O(n)` quadratic-algebraic candidates. Rational data permit weak optimization to any specified precision with polynomial bit work.

For a fixed convex anchor `h`, replace `beta/X` by `beta h(X)`. If `beta>=0`, each interval asks for scalar convex minimization; if `beta<0`, endpoints suffice. Computational claims then depend on the representation and evaluation/optimization access to `h`.

These observations do not replace exact rational membership, separation, or decomposition. They do limit the significance of claiming only polynomial optimization. They also cease to justify simple threshold enumeration if extra leaf-linking constraints are imposed.

## Adjacent simultaneous-convexification work

Tawarmalani, *Inclusion Certificates and Simultaneous Convexification of Functions* (2010), supplies a general framework and a mixed fractional/bilinear example demonstrating that separate envelopes can miss a joint inequality. Targeted inspection did not find the arbitrary-leaf anchored hull or its call-envelope formula. [Primary manuscript](https://optimization-online.org/wp-content/uploads/2010/09/2722.pdf). A general simultaneous-convexification framework is prior theory, but a generic characterization by all supporting functionals is not the same algorithmic statement as the proposed finite envelope calculation.

Oh, Wiecek, and Yang, *Convexification of a Class of Bilinearly Constrained Sets Sharing a Common Variable*, announce extreme-point and facet characterizations plus separation for box domains with common-variable bilinear inequalities. The [SIAM Optimization 2026 abstract, PDF page 70](https://www.siam.org/media/r0be0xtr/op26_abstracts_v3.pdf) and [INFORMS Optimization Society 2026 program](https://ios2026.isye.gatech.edu/sites/default/files/2026-03/program-book.pdf) give no detailed model or proofs. No full manuscript was found through the title and author searches. The abstract is too broad to prove or exclude overlap, especially because reciprocal equality can be expressed with a common-variable bilinear equality. This is an unresolved comparison, not evidence that the local formula is already published.

## Search scope and recommended positioning

Searches covered reciprocal/common-variable hulls, simultaneous convexification, square-anchor and quadratic-star moment hulls, bilinear functions with a univariate convex term, lift zonoids, convex-order joins, threshold selection, and current author/title searches for the 2026 announcement. Relevant primary theorems were inspected; search misses have no implication of absence from the literature.

A defensible working description is: **an explicit exact rational convex-hull oracle and constructive distribution recovery for a reciprocal-anchored bilinear star, derived from classical lift-zonoid and convex-order theory, with no exact application antecedent found in the current search**. The broader convex-anchor statement is a natural consequence of the same classical order structure. Its utility can be real without treating it as a new probabilistic mechanism or a new tractability discovery.

## Follow-up: binary leaves and an integer common factor

The author's [integer-anchor extension](../results/common-factor-integer-anchor-hull.md) was flagged near the end of this audit. Binary leaves do not alter the graph hull because, at each fixed value of the common factor, the leaf box and all retained coordinates are affine in the leaves. Endpoint randomization therefore realizes every continuous leaf point. This is an elementary multilinear/affine convexification fact, not a separate source of novelty.

Additional searches for common-continuous-variable indicators, convex univariate functions with multiple binary products, and square-anchor indicator hulls found standard perspective and mixing-set literature, but no exact arbitrary-star formula. This follow-up was limited; it does not exclude an equivalent indicator formulation.

The easy optimization observation extends to a common factor restricted to integers, even when its range is huge. Intersect each of the at most `n+1` threshold intervals with the integer domain. On a nonempty resulting integer interval, check its two endpoints and, if `A,beta>0`, the feasible integers immediately below and above `sqrt(beta/A)`. Convexity in that case and monotonicity/concavity in the other cases prove sufficiency. Integer square-root calculations and rational comparisons use polynomial work in the input bit length. Thus exact linear optimization is already polynomial in the logarithm of the range. The proposed integer call-envelope membership test and compressed telescoping separator remain more specific constructive contributions, subject to their mathematical reviews and a broader novelty comparison.
