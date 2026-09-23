# A degree-independent gap bound from incidence orientations

Date: 2026-09-04. Status: full written proof independently audited; no unresolved mathematical issue identified. Novelty is provisional.

## Theorem

Let p be a positive-coefficient multilinear polynomial on the unit cube, and discard affine terms. Its incidence graph has one node for each variable, one node for each remaining monomial, and an edge for each variable occurrence.

Suppose this graph has an orientation such that every variable node has outdegree at most r and every factor node has outdegree at most s, where r and s are nonnegative integers. Put κ=2/(1−exp(−1)). Then

    tbtgap_p(x) ≤ (r+s+κ) chgap_p(x)                       (1)

at every point x. The constant does not depend on degree, dimension, number of terms, or coefficients.

In particular:

- If every variable occurs in at most r monomials, the ratio is at most r+κ.
- If the incidence graph admits an orientation with all outdegrees at most k, the ratio is at most 2k+κ.
- Incidence degeneracy at most k implies the preceding orientation and hence the same bound. Incidence treewidth at most k also suffices.

Consequently incidence treewidth two gives the finite universal bound 4+κ<7.165. Whether its sharp value is two remains unresolved here. The [feedback-variable result](positive-multilinear-feedback-gap.md) gives a width-two family with ratio approaching two.

Combined with a variable-radix lower construction, the refined bound below proves [sharp asymptotic growth](positive-multilinear-incidence-sharp-growth.md): the worst gap ratios under incidence treewidth k, incidence degeneracy k, or maximum orientation outdegree k are all asymptotic to k, with leading constant one.

The theorem also applies to boxes with zero lower bounds, by coordinate scaling and removal of fixed variables. Positive lower bounds require a separate argument and are not covered by this theorem.

## Deficiency representation

For each term e, choose an anchor a(e) with smallest mean u_e=x_(a(e)). Put p_i=1−x_i. Its individual gap is

    T_e=min(u_e, Σ_(i∈e\{a(e)}) p_i).

For any Bernoulli coupling with means x, define the nonnegative deficiency

    D_e=X_(a(e))−∏_(i∈e)X_i.

Its expectation is the probability that the anchor succeeds and at least one other coordinate fails. The complete hull gap is

    chgap_p(x)=max_(P: E X=x) Σ_e a_e E_P D_e.              (2)

This follows because all positive monomials simultaneously attain their concave-envelope values under the comonotone Bernoulli coupling.

Call a variable low if x_i≤1/2 and high otherwise. Terms with exactly one low variable are called hard. Their anchor is that low variable. Other terms will be handled by independence.

## Independence handles the other terms

Write c=1−exp(−1). Under independence,

    E D_e=u_e[1−∏_(i≠a(e)) x_i].

If every coordinate is high, u_e>1/2, and

    E D_e≥u_e c min(1,Σ_(i≠a(e))p_i)≥c T_e/2.

Here 1−exp(−t)≥c min(1,t) was used. If there are at least two low coordinates, one nonanchor mean is at most 1/2, so

    E D_e≥u_e/2≥T_e/2≥c T_e/2.

Thus independence gives deficiency at least T_e/κ for every nonhard term.

## Splitting a hard term by the orientation

For a hard term e, split its high variables into

    I_e={i∈e\{a(e)} : the incidence edge points from i to e},
    O_e={i∈e\{a(e)} : the incidence edge points from e to i}.

Every high variable belongs to at most r of the sets I_e, while |O_e|≤s. Define

    T_e^I=min(u_e,Σ_(i∈I_e)p_i),
    T_e^O=min(u_e,Σ_(i∈O_e)p_i).

Then

    T_e≤T_e^I+T_e^O.                                     (3)

It remains to construct global couplings guaranteeing the two parts.

## Incoming incidences: r rounds of disjoint ownership

Assume r≥1. For each high variable, assign distinct labels in {1,...,r} to its incoming-to-factor incidences among hard terms. Labels may be assigned independently for different variables.

In round h, give a high variable to its incident hard term labeled h, if one exists. Each high variable has at most one owner in that round. Thus the owned sets J_(e,h) are pairwise disjoint over e. For each fixed term e, they partition I_e as h runs from 1 to r.

Use a common uniform U in (0,1), and set all low variables to X_i=1[U≤x_i]. For a term e with anchor mean u_e>0, arrange failures of its owned high variables so that

    Pr(U≤u_e and some owned variable fails)
       =min(u_e,Σ_(i∈J_(e,h))p_i),                       (4)

while preserving every failure marginal p_i.

An explicit construction proves feasibility. Within the interval [0,u_e], place consecutive circular arcs of lengths min(p_i,u_e), one for each owned variable. The union of those arcs has length min(u_e,Σ_i p_i). If p_i>u_e, its arc already covers the whole interval; give that variable an additional failure set of length p_i−u_e outside [0,u_e]. Such a set exists because p_i≤1. If u_e=0, the requested deficiency is zero and any marginal-correct failure set can be used. High variables without an owner can also use arbitrary marginal-correct failure sets.

All choices are compatible globally because the owned sets are disjoint. The same low variable may anchor several terms: their constructions use its same success interval, which imposes no conflict between distinct owned high variables.

The full term deficiency dominates the event in (4). Averaging the r rounds gives

    E D_e ≥ (1/r) Σ_h min(u_e,Σ_(i∈J_(e,h))p_i)
            ≥T_e^I/r.                                    (5)

The last inequality is subadditivity of t↦min(u_e,t). This is a simultaneous guarantee for every hard term. If r=0, all I_e are empty and this component is omitted.

## Outgoing incidences: one threshold coupling

Set every low coordinate to X_i=1[U≤x_i], and make every high coordinate fail if and only if U≤p_i. This preserves all means. For each hard term with O_e nonempty,

    E D_e ≥min(u_e,max_(i∈O_e)p_i)
            ≥min(u_e,Σ_(i∈O_e)p_i)/s=T_e^O/s.             (6)

The second inequality follows from |O_e|≤s. If O_e is empty, T_e^O=0. If s=0, omit this coupling.

## Mixture and conclusion

Mix the incoming-round distribution, outgoing-threshold distribution, and independence with weights proportional to r, s, and κ, omitting a component with zero weight. Divide by Z=r+s+κ.

Equations (3), (5), and (6) give every hard term deficiency at least

    (T_e^I+T_e^O)/Z≥T_e/Z.

Independence gives every other term deficiency at least T_e/Z. All unused contributions are nonnegative. Multiply by the nonnegative coefficients, sum, and use (2) to prove (1).

For the graph corollaries, orient all incidence edges from variables to factors when variable frequency is bounded. A k-degenerate graph can instead be oriented from earlier to later in a degeneracy ordering, giving outdegree at most k at every node. The standard inequality degeneracy≤treewidth gives the stated treewidth corollary.

## Optional improvement using the degree bound

Let B(d) be any valid degree-dependent upper bound for positive multilinear gap ratios, and define B(1)=0. The same decomposition yields the stronger bound

    tbtgap_p(x)≤[r+min{s,B(s+1)}+κ] chgap_p(x).             (7)

To justify this without assuming a termwise guarantee from B, form the positive polynomial consisting, for each hard term e, of its original coefficient times the product on {a(e)}∪O_e. Its degree is at most s+1. Its term-by-term gap is Σ_e a_e T_e^O, and its hull gap is at most the original polynomial's hull gap: under every coupling its deficiency is at most the original full-term deficiency. Therefore Σ_e a_e T_e^O≤B(s+1) chgap_p(x). Equations (5) and the independence bound similarly bound the weighted incoming and nonhard gap sums by r and κ times the original hull gap. Combining with (3) proves (7); the threshold argument gives the alternative s.

The [sharp degree-growth result](positive-multilinear-sharp-degree-growth.md) supplies B(d)∼ln d/ln ln d asymptotically. Thus orientations with both outdegree bounds k give a bound k+O(ln k/ln ln k), improving the leading coefficient of the elementary 2k+κ bound.

## Frequency bounds and lower examples

Let R_freq(r) be the worst ratio among unit-box positive multilinear polynomials in which every variable appears in at most r monomials. Then, for every r≥2,

    2−1/r ≤ R_freq(r) ≤ r+κ.                              (8)

For the lower bound use the feedback example with n=r:

    p_r(a,x)=a Σ_(i=1)^r x_i+∏_(i=1)^r x_i,
    a=1/r,       x_i=1−1/r.

The anchor appears in r terms, and every other variable appears in two. Its hull gap is one and its term-by-term gap is 2−1/r. In particular frequency three permits ratio 5/3. The separate frequency-two investigation gives the sharper exact supremum 3/2 for r=2; (8) is not intended to replace that result.

The dyadic lower construction also shows R_freq(r)≥(1−o(1))ln r/ln ln r. Its maximum ordinary variable frequency is m=2^ell, attained by its deepest anchor, while the leaves have frequency ell. Choose the largest dyadic m≤r and use its ratio asymptotic to ell/log_2 ell. This ordinary frequency parameter is distinct from the frequency of high variables in the hard-term coupling argument.

## Scope and novelty

The structural parameter is the original incidence graph. Splitting a positive-lower-bound monomial into its positive expansion can introduce many new factors and increase incidence density or frequency, so that operation cannot establish a nonnegative-box extension of (1).

Bounded incidence treewidth is already known to support exact algorithms for binary polynomial optimization. The result here quantifies the original term-by-term relaxation's pointwise gap without adding variables or inequalities. No claim is made that bounded-width tractability or degeneracy orientations are new.

The low/high classification and independence estimate come from the earlier harmonic-coupling work. The present contribution is the finite ownership-round construction and its use with an incidence orientation. The complete written proof, zero-parameter cases, optional degree refinement, and frequency examples passed [independent audit](../notes/review-multilinear-incidence-orientation.md). The primary-literature screen is in [the structural novelty note](../notes/multilinear-structural-novelty.md).
