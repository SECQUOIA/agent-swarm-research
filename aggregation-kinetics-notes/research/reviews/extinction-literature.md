# Literature critique: extinction with unknown daughter coupling

Date: 2026-09-06. Scope: finite multitype binary branching with independently specified symmetric daughter transport polytopes. This is a novelty review, not an independent proof certification.

The elementary sharp bounds in [the candidate note](../results/extinction-coupling.md) are useful, but the current theorem is a specialization of established branching decision process and rearrangement results. The search did not identify a paper spelling out exactly the same daughter-marginal formulation. That absence is insufficient to claim a new substantial theoretical result: the reduction to known results is immediate. Retain this as a rigorously motivated application and a starting point for extensions.

## Decisive overlap

### Branching decision processes

Kousha Etessami, Alistair Stewart, and Mihalis Yannakakis, *Polynomial Time Algorithms for Branching Markov Decision Processes and Probabilistic Min(Max) Polynomial Bellman Equations*, Mathematics of Operations Research 45(1), 34–62 (2020), [open accepted manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/68952841/Polynomial_Time_Algorithms_for.pdf), [preprint](https://arxiv.org/abs/1202.4798), [DOI](https://doi.org/10.1287/moor.2018.0970).

Inspected the abstract, definitions, Theorem 2.5, and BMDP discussion. The theorem states that a min/max probabilistic polynomial system has a policy whose least fixed point equals the system's least fixed point. Optimality is componentwise. The BMDP interpretation gives pure static optimal extinction policies. The paper also supplies polynomial time approximation in an explicitly encoded action system. Theorem 2.5 credits Etessami and Yannakakis, *Recursive Markov Decision Processes and Recursive Stochastic Games*, JACM 62(2), 2015, Theorem 2. [Original paper's publication record](https://www.research.ed.ac.uk/en/publications/recursive-markov-decision-processes-and-recursive-stochastic-game-2).

Our reduction is short. Each symmetric transport polytope has finitely many vertices. Choose one vertex as the action of each parent type. Because the generating function is linear in the coupling, its minimum and maximum over the polytope equal their extrema over vertices. This is precisely a finite-action BMDP. Consequently the Bellman characterization, simultaneous optimality for all initial types, and existence of a stationary optimizer are already covered. This also covers independently imposed linear pair-observation or allowed-support constraints. Rational coefficients are needed for the cited bit-complexity statement; the basic finite-action interpretation does not create novelty for real probabilities.

### Rearrangement and dependence extrema

Giovanni Puccetti and Ruodu Wang, *Extremal Dependence Concepts*, Statistical Science 30(4), 485–517 (2015), [open author manuscript](https://www.math.uwaterloo.ca/~wang/papers/2015Puccetti-Wang-STS.pdf), [preprint](https://arxiv.org/abs/1512.03232).

Inspected Theorems 2.1 and 3.1 and their historical discussion. Comonotonicity maximizes expectations of supermodular functions under fixed marginals; in two dimensions countermonotonicity minimizes them. The paper explicitly includes the product function as supermodular and describes quantile pairing with a uniform variable and its reflection. It traces these facts to much earlier work.

Apply those classical extrema to the scalar daughter values z_J and z_K. The lower expression is the antithetic quantile integral, and the upper is the second moment for identical scalar marginals. A diagonal coupling of type labels realizes the upper bound for every z. Symmetrizing a minimizing type coupling preserves marginals and objective. These are direct deductions, so neither the antithetic formula nor the diagonal maximizing mechanism is independently novel.

### Mean growth versus extinction

Peter Olofsson, *Branching Processes with Local Dependencies*, Annals of Applied Probability 6(1), 238–268 (1996), [open author copy](https://www.stat.rice.edu/~olofsson/local.pdf).

Inspected the indexed primary-source text of the introductory examples and discussion around pages 241–242. It explicitly contrasts changed extinction probabilities with unchanged growth rates under sibling dependence and develops a general marginal-based growth theory. Its local dependence model is broader in some respects than dependence between daughter types at one birth. It precludes presenting the qualitative phenomenon as new. Exact population-balance and single-lineage observational equivalence are useful explanations in the present finite model, but alone do not overcome this overlap.

## Adjacent results inspected

- Etessami, Stewart, and Yannakakis, *Greatest Fixed Points of Probabilistic Min/Max Polynomial Equations, and Reachability for Branching Markov Decision Processes* (ICALP 2015), [open preprint and abstract](https://arxiv.org/abs/1502.05533). Optimal probability that a population ever contains a target type is already addressed through greatest fixed points of non-reachability Bellman systems. Replacing extinction by resistant-type emergence would therefore be an application, not automatically a new fixed-point theorem. Only the abstract was inspected for this adjacent result.
- Cindy Courtois, Michel Denuit, and Sébastien Van Bellegem, *Discrete s-convex extremal distributions: Theory and applications*, [open manuscript](https://citeseerx.ist.psu.edu/document?doi=fe765a9a7342795df4087f106c68e42cedf0cd5b&repid=rep1&type=pdf). The indexed manuscript abstract explicitly applies moment-constrained discrete distribution extrema to Galton–Watson extinction bounds. This concerns offspring-count moments rather than multitype daughter marginals, but rules out claiming the broad idea of sharp extinction bounds from partial offspring information as new. Abstract and introductory excerpt inspected.
- *Extinction in a branching process: why some of the fittest strategies cannot guarantee survival* (2014), [open original research article](https://link.springer.com/article/10.1186/2195-5832-1-10). Inspected the abstract and section 2.3. It uses s-convex order and offspring moments for best- and worst-case extinction scenarios, with acknowledgment of earlier branching literature. This supplies additional direct application precedent.

## What might justify further development

These are research questions, not established new contributions.

1. **Implicit transport algorithms.** Enumerating transport-polytope vertices can be expensive. A certified algorithm whose complexity depends polynomially on the type count and marginal encoding, without enumerating actions, could add something beyond the direct BMDP reduction. Sorting makes one Bellman evaluation cheap, but does not itself provide a rate of convergence or a polynomial precision bound. A useful target is an explicit error certificate that remains informative near criticality. It must be compared with the existing generalized Newton algorithms.
2. **Mechanically consistent admissible laws.** Real partition kernels may satisfy additive conservation, which can eliminate the diagonal optimizer and can even uniquely determine the second daughter from the first. Classify when daughter uncertainty remains after measured traits and conservation are imposed. For independently constrained finite polytopes the Bellman theorem remains prior art; a substantive result would need an explicit solution or new physical consequence.
3. **A common mechanism shared across parent types.** If one unknown partition parameter or copula determines every C_i, choices cannot be made separately for each type. Coordinatewise Bellman optimization then optimizes a larger admissible family. A sharp description of the resulting gap or of the attainable extinction-vector set might be useful. Even a counterexample to simultaneous stationary attainment under shared constraints would clarify a material modeling assumption. This direction requires a separate search on nonrectangular robust MDPs and parametric branching processes before novelty is claimed.
4. **Measured sister statistics and experimental design.** A new result could quantify which pair measurements most reduce extinction uncertainty, with attainable nonasymptotic bounds and a concrete measurement budget. Merely adding linear moment constraints and reusing the Bellman argument would not suffice. Near-critical asymptotics and extinction sensitivity already have substantial literature, so those ingredients also require targeted review.
5. **Continuous traits with certified discretization.** Extending finite formulas by replacing sums with integrals is not by itself compelling. Uniform approximation bounds for extinction envelopes, especially under conservation or near-critical slowing, could be substantive if correct and absent from prior work.

## Search record and limits

Queries included branching Markov decision process extinction stationary policies; branching extinction fixed marginals; offspring dependence Fréchet bounds; branching countermonotonic/comonotonic; extinction convex order; multitype branching supermodular; branching dependence uncertainty; distributionally robust branching extinction; and population balance daughter correlation extinction. Primary open papers were preferred. General search terms concerning robust branching produced many unrelated optimization and geological hits and no directly matching dependence-uncertainty theorem.

This was a bounded search, not an exhaustive bibliographic review. The JACM author's PDF timed out when opened; its cited result was verified through the full 2020 accepted manuscript, not through independent inspection of the JACM proof. No conclusion here depends on claiming that a search miss establishes novelty. The current evidence supports downgrading the basic theorem to a known-method corollary with a useful population-balance interpretation.

## Follow-up: exact antithetic policy near criticality

The follow-up candidate fixes an irreducible critical mean matrix M_0 and daughter marginals and scales division probabilities so M_ε=(1+ε)M_0. With positive Perron vectors normalized by uᵀv=1, it proposes a coupling-uniform expansion

\[
 1-q_C=\frac{\varepsilon v}{D_C}+O(\varepsilon^2),\qquad
 D_C=\sum_i u_i b_i^0\,\mathbb E_{C_i}[v_Jv_K].
\]

If all relevant reproductive values v_j are distinct, their order determines the exact antithetic optimizer for every sufficiently small positive ε, because the survival-vector ordering stabilizes. The word *exact* distinguishes this from merely optimizing the leading expansion coefficient.

### Explicit prior asymptotics

Michel Durinx, Johan A. J. Metz, and Géza Meszéna, *Adaptive dynamics for physiologically structured population models*, IIASA interim report IR-07-027 (2007), [open report](https://pure.iiasa.ac.at/8430/1/IR-07-027.pdf). Downloaded and inspected equations (14)–(17), rather than relying only on search snippets. Equation (14) gives the multitype establishment approximation 2εv_l/B+O(ε²), where B contracts offspring second factorial moments with stable type frequencies and reproductive values. It credits Athreya (1993) and Eshel (1984). For the binary offspring law here, B=2D_C at criticality. This report is primary adaptive-dynamics work but is not the original source of the asymptotic theorem.

The original references are Krishna B. Athreya, *Rates of decay for the survival probability of a mutant gene II: The multitype case*, Journal of Mathematical Biology 32, 45–53 (1993), [publisher record](https://link.springer.com/article/10.1007/BF00160373), and Ilan Eshel, *On the survival probability of a slightly advantageous mutant gene in a multitype population: A multidimensional branching process model*, Journal of Mathematical Biology 19, 201–209 (1984), [publisher record and abstract](https://link.springer.com/article/10.1007/BF00277746). The publisher records and abstracts were inspected; these original full texts were not openly obtained in this search. Their asymptotic subject clearly overlaps, while their exact uniform assumptions need full-text comparison before a uniform-error novelty claim.

### What the search did and did not establish

Additional queries combined near-critical/slightly-supercritical multitype branching with optimal policy, perturbation, reproductive value, covariance, antithetic, countermonotonic, and Blackwell optimality. No direct matching primary theorem was located for *explicit antithetic pairing of Perron reproductive values being exactly extinction-optimal throughout a supercritical interval*. The general BMDP papers already cover existence of stationary optima. A search hit concerning Blackwell optimality and Markov branching decision chains discussed discounted reward and small interest rates, not extinction; it does not establish direct overlap with the candidate.

The narrower claim is therefore plausible as an unreported useful consequence, with novelty confidence still limited. The potentially distinctive content is the explicit optimizer determined from first-moment reproductive values, plus a verified interval or quantitative uniform error bound. The basic asymptotic coefficient and rearrangement principle remain classical.

### A further caution about claiming policy stabilization alone

The following is a reviewer deduction, not an independently certified research result. In a finite-action BMDP whose rule probabilities depend polynomially or rationally on a scalar ε, each fixed policy's extinction-vector graph is semialgebraic: write its fixed-point equations and quantify over all fixed points in the unit cube to enforce leastness. Finite-policy optimality regions are consequently semialgebraic. A semialgebraic subset of the line is a finite union of intervals and points. Since some static policy is optimal at every parameter, at least one policy is optimal throughout a sufficiently small punctured parameter interval. Thus bare existence of an eventually unchanged optimal policy is not special to antithetic daughter transport. The candidate adds explicit identification from the Perron ordering. This deduction should receive proof review if it is promoted from literature critique into a result.
