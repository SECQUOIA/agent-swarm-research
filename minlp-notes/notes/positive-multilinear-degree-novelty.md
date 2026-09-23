# Novelty audit: sharp degree growth and simultaneous Fréchet approximation

Date: 2026-09-04. This is a targeted primary-source literature audit by a separate
agent. It is not external peer review, a proof audit, or an exhaustive priority search.
The candidate is [positive-multilinear-sharp-degree-growth.md](../results/positive-multilinear-sharp-degree-growth.md),
with the earlier [degree bound](../results/positive-multilinear-degree-upper-bound.md)
and [lower construction](../results/positive-multilinear-gap.md).
The [first novelty audit](positive-multilinear-novelty.md) records the original
conjecture and detailed correlation-gap and directed-hypergraph comparisons.

**Assessment:** no prior theorem giving the claimed asymptotic degree bound, its
leading constant, or its equivalent simultaneous Bernoulli-coupling guarantee was
found in the searches described below. The results remain plausible new results,
conditional on their separate mathematical audits. The evidence supports saying
“we did not find this in the open literature searched”; it does not establish
publication priority. The simultaneous approximation statement is a useful way to
seek further probability literature that may not cite multilinear optimization.

## Exact target of the search

For a positive multilinear polynomial of maximal degree at most `d`, let the numerator
be the width of the relaxation that uses the exact envelope of each monomial, and
let the denominator be the width of the convex hull of the entire graph at the same
point. The candidate worst-case ratio, allowing arbitrary dimension, is

```
R(d) ~ ln(d)/ln ln(d).
```

The same leading asymptotic is claimed for the worst ratio in dimension `n`, with
`d` replaced by `n`. The class includes all nonnegative boxes. The candidate lower
bound already uses the unit box and sparse unit coefficients. Thus a result about
mixed signs, additive envelope error, a fixed polynomial, or an unrestricted
optimization objective does not settle this claim.

There is a stronger constructive formulation. Given any vector of Bernoulli means
`x∈[0,1]^n`, define for every nonempty subset `e`

```
u_e = min_{i∈e} x_i,
l_e = max{0, Σ_{i∈e} x_i − |e| + 1}.
```

The candidate constructs one joint law, depending only on `x,d`, such that

```
P(X_i=1 for every i∈e) ≤ (1−α_d)u_e + α_d l_e
                       for every e with 2≤|e|≤d,
α_d ~ ln ln(d)/ln(d).
```

The constant is asymptotically optimal in the worst case over means and dimension.
The law is independent of the nonnegative coefficients and of which subsets occur
in a polynomial. The statement concerns upper bounds on all these intersections;
it does not assert that the interpolating formula itself is a compatible vector
of intersection probabilities. Nor does it construct one copula valid at all
possible marginal vectors simultaneously: its law may change with `x`.

## Direct multilinear followups

The original conjecture is Luedtke–Namazifar–Linderoth, Conjecture 4.1 in the
published paper, journal p.349; it is Conjecture 1 on printed p.22 of the
[author-hosted report](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf).
It asks for a uniform bound for positive coefficients on nonnegative boxes, without
fixing the degree. Its exact scope and distinction from recursive McCormick
relaxation are documented in the first audit.

[Adams, Gupte, and Xu, *Error bounds for monomial convexification in polynomial
optimization*](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf),
DOI [10.1007/s10107-018-1246-8](https://doi.org/10.1007/s10107-018-1246-8),
is a particularly relevant degree-dependent followup. Its introduction explicitly
distinguishes the relative gap used by Luedtke et al. from its own absolute
convexification error. Definitions, Theorem 1.1, and Corollaries 1.2–1.3 were checked.
Bounds on the largest vertical error or the additive optimization gap do not give
a bound relative to the full-hull width, which can itself be arbitrarily small.
No claim of the candidate relative rate was found in those sections.

[Ben-Ameur, Ouorou, and Wang, *Convex and concave envelopes: Revisited and new
perspectives*](https://www.sciencedirect.com/science/article/abs/pii/S0167637716301572),
Operations Research Letters 45 (2017), 421–426, was screened through its accessible
abstract and introduction. Its approximation comparison concerns bilinear
functions and semidefinite/linear relaxations. This screening is not a full-paper
audit and gives no basis for attributing the higher-degree theorem to that paper.

The earlier audit also checked the relevant statements in Boland et al.'s
mixed-sign bilinear paper, Schutte–Walter's recursive/flower-relaxation paper,
Khajavirad's recursive-relaxation work, and He–Tawarmalani's composite-relaxation
manuscript. Those comparisons should be retained in a future manuscript rather
than replaced by a claim that the positive multilinear case has no literature.

## A misleading local source summary was corrected

The full local source for Sherali (1997) was checked, including its definition of
a complete multilinear function and the positive and negative envelope theorems.
Its complete degree-`m` function includes **every** squarefree degree-`m` monomial
with coefficient one. The simple formulas are for that complete homogeneous
support, not for arbitrary sparse positive-coefficient polynomials. Definition (3)
is on PDF pp.2–3 (journal pp.246–247); Theorems 3–4 and their development occupy
PDF pp.8–17. See [[sherali1997-convex-envelopes-of-multilinear-functions]] pp.2–3,
8–17 and the [open paper](https://math.ac.vn/uploads/files/9701245.pdf).

The scope in
[the local paper note](../literature/papers/sherali1997-convex-envelopes-of-multilinear-functions/paper.md)
and [the topic synthesis](../literature/topics/polynomial-qcqp-and-structured-relaxations.md)
was corrected. This matters because the dyadic candidate is sparse and has varying
degrees; the former broad wording could incorrectly suggest that its full envelope
was already covered by the simple complete-support formula.

## Why several approximation literatures do not directly imply the claim

The first audit derives the coverage identity

```
ratio = (U_C−L_C)/(C⁺−L_C),
L_C = Σ_e a_e max_{i∈e}p_i,
U_C = Σ_e a_e min{1,Σ_{i∈e}p_i},       p=1−x.
```

Here `C⁺` is the largest expected coverage under the prescribed means. Standard
monotone coverage correlation gaps compare an unshifted expected value with `C⁺`.
Subtracting `L_C` invalidates the inferred multiplicative bound. Searches for
coverage, Lovász extensions, concave closures, and correlation gaps found no theorem
controlling precisely this normalized difference with the candidate sharp rate.

Another exact representation is the directed-hyperedge deficiency. Choose a
minimum-mean vertex `r` in a monomial and write `B=e\{r}`. On a binary success set `S`,

```
D_{r,B}(S) = 1[r∈S] 1[B⊄S].
```

The candidate compares the sum of individual concave closures of these predicates
with the concave closure of their sum, at fixed means. Its proof uses the
minimum-mean choice of `r`; a theorem for arbitrary oriented hyperedges should not
be asserted from it without an additional argument. Ordinary maximum directed
hypergraph cut, minimum hypergraph cut, and Max Horn-SAT approximation results
usually have different constraints, a different cut predicate, or a different
objective direction. The precise source checks are in the first audit.

There is also a matroid-rank interpretation that helps identify a tempting false
shortcut. If `k=|e|`, put

```
r_e(S) = min{|S∩e|,k−1}.
D_{r,B}(S) = r_e(S) − |S∩B|.
```

Thus each deficiency is a uniform-matroid rank function minus a modular function.
It is nonnegative but generally nonmonotone: adding the last missing member of
`B` when `r` is present changes its value from one to zero. Adding modular functions
preserves the discrete exchange inequalities, so each predicate is also
M♮-concave. The difficulty is not the individual predicate's concave closure but
compatibility of many such predicates at the same means.

[Shioura, *On the Pipage Rounding Algorithm for Submodular Function Maximization—A
View from Discrete Convex Analysis*](https://www.dais.is.tohoku.ac.jp/~shioura/papers/dmaa09.pdf)
(2009), pp.1–4, was read in the author manuscript. Theorem 1.3 explicitly assumes
the component M♮-concave functions are nondecreasing and normalized. Its framework
optimizes over a matroid polytope. Dropping that assumption to apply it to the
deficiency predicates is unjustified. Similarly,
[Lv et al., *Efficient Submodular Maximization for Sums of Concave over Modular
Functions*](https://proceedings.iclr.cc/paper_files/paper/2026/file/eb7389b039655fc5c53b11d4a6fa11bc-Paper-Conference.pdf),
Section 2, Definition 1, requires monotone components. Those assumptions were
checked rather than inferred from the titles.

[Kazemi et al., *Regularized Submodular Maximization at Scale*](https://proceedings.mlr.press/v139/kazemi21a/kazemi21a.pdf)
(2021), introduction and problem formulation, treats a monotone submodular reward
minus a modular cost under a cardinality constraint. This is conceptually close
to the rank-minus-modular identity, but it does not impose an arbitrary vector
of exact inclusion marginals or compare the two concave-closure quantities above.
Its discussion of additive shifts also reinforces why an unshifted guarantee
cannot simply be reused here.

## Fréchet classes, negative dependence, and transport

[Altschuler and Boix-Adserà, *Hardness results for Multimarginal Optimal Transport
problems*](https://arxiv.org/pdf/2012.05398), Section 6.2, especially (6.3) and
Proposition 6.3 on PDF pp.11–12, explicitly studies optimization of a set function's
expectation over Bernoulli laws with specified means. It distinguishes tractable
submodular minimization from hard supermodular minimization. This confirms that
the candidate convex-envelope problem is a known transport model. Its hardness
result for general oracle costs and additive accuracy neither supplies nor rules
out the candidate relative width bound for positive multilinear costs.

[Fontana and Semeraro, *Computational and Analytical Bounds for Multivariate
Bernoulli Distributions*](https://link.springer.com/article/10.1007/s42519-021-00231-x)
(2022), introduction and Sections 2–3, studies the same finite Fréchet polytope,
its generators, and bounds on functions of Bernoulli variables. Its computational
and exchangeable-case bounds are relevant background; no simultaneous
degree-dependent interpolation theorem was identified there.

[Puccetti and Wang, *Extremal dependence concepts*](https://sas.uwaterloo.ca/~wang/papers/2015Puccetti-Wang-STS.pdf),
Sections 3.1–3.3, explains why multivariate lower Fréchet bounds generally fail
to define a joint law and describes pairwise countermonotonicity and joint
mixability. The author-hosted copy checked here has references and clarifications
from 2025, although the original article is from 2015. No quantitative guarantee
for a fraction of every subset's Fréchet interval was found in the checked sections.
Qualitative nonattainability is much weaker than the candidate sharp asymptotic.
The manuscript's updated claims should not automatically be dated to 2015.

[Erdely, *A Subcopula Characterization of Dependence for the Multivariate Bernoulli
Distribution*](https://link.springer.com/article/10.1007/s44199-025-00157-4)
(published January 2026), Sections 2–5 and the conclusion, gives an explicit
all-orders dependence parametrization and compatibility procedure. Section 5
uses the same subset Fréchet bounds. Its procedure chooses joint masses and then
derives compatible interaction parameters; it does not state the candidate
uniform approximation guarantee for arbitrary prescribed means. This is a source
scope check, not an endorsement of every claim or formula in that paper.

## Search record and remaining uncertainty

Targeted queries included multilinear-envelope gap versus degree; the original
authors and conjecture; logarithmic and log-log degree growth; coverage concave
closures; fixed-marginal directed hypergraph cuts; Horn predicates; nonmonotone
matroid-rank sums; regularized submodular maximization; positive Bernoulli chaos;
aggregation and compatibility of Fréchet bounds; approximate countermonotonicity;
simultaneous lower intersection bounds; negative orthant dependence; and
simultaneous interpolation between lower and upper Fréchet bounds. The last
probability queries were added after the coefficient-independent formulation
emerged. Searches using “Fréchet” and logarithms also return many unrelated
Fréchet-distribution and geometric-distance papers; those were not counted as
relevant evidence.

The evidence reviewed here does not identify a known theorem that gives even the
claimed order by a direct substitution, unlike the separate McCormick density
investigation where an older operator-theory theorem did yield the same order.
Nevertheless, the remaining risk is a theorem under different terminology about
simultaneously realizing marginal intersections or rounding sums of nonmonotone
discrete-concave functions. An eventual paper should state the precise
Fréchet-interpolation theorem and the positive multilinear specialization, cite
the established coupling/envelope identities, and keep the priority qualification
until a wider citation review is complete.
