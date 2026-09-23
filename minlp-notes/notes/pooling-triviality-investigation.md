# Pooling triviality: source audit and explicit polynomial consequence

Date: 2026-09-04. This investigation concerns row 9 of
[open-problems-from-literature.md](open-problems-from-literature.md).
The mathematical result is saved in
[pooling-triviality-polynomial.md](../results/pooling-triviality-polynomial.md).

**Conclusion:** the exact zero-optimality question in Gupte et al.'s Remark 2.2
has an affirmative polynomial-time answer under the model stated there. Two
independent agents checked the core proof. One also checked the shortest-path,
sparse-witness, and conic-hull consequences and ran 250 exact rational random-DAG
decomposition checks. However, destination disaggregation is established prior
art, and standard pooling already has a polynomial approximation theorem that
implies the sign test. This should be retained as an explicit consequence of known
formulation machinery, with a self-contained proof, rather than promoted as a
new decomposition method. The sign and cone conclusions were not located
explicitly in the targeted open-source search.

## The source question and its exact assumptions

Gupte, Ahmed, Dey, and Cheon, *Relaxations and discretizations for the pooling
problem*, Journal of Global Optimization 67 (2017), 631–669, DOI
[10.1007/s10898-016-0434-4](https://doi.org/10.1007/s10898-016-0434-4),
ask the question in Remark 2.2, PDF p.6, printed p.5 of the
[open manuscript](https://www.pure.ed.ac.uk/ws/files/136877755/4883.pdf).
The mathematical model and surrounding observations were read in the local
fulltext and independently checked in the PDF. See
[[gupte2017-relaxations-and-discretizations-for-the]] p.4-6.

The graph is acyclic and may have pool-to-pool arcs. Flows and costs are continuous
and linear in the objective, all flow capacities are upper bounds, and the only
quality restrictions are on final output mixtures. Pooling is lossless and follows
linear blending. The zero flow is feasible, so the minimum cost `z*` is at most
zero. Triviality means deciding whether this minimum is zero, not testing whether
the feasible region consists only of the zero flow. Positive output demands,
minimum operating rates, fixed charges, quality restrictions inside the network,
and nonlinear mixing are outside this question's model.

The proof does not require a bounded number of pools or qualities. It permits
direct input-output arcs, signed costs and quality data, zero flows, zero
capacities, and arbitrary nonnegative rational upper-capacity magnitudes.

## What the argument gives

For each final output, restrict flow to that output and write one ordinary network
LP. Its quality is the total input-quality mass divided by total delivered flow;
the resulting quality inequalities are linear in source withdrawals and output
flow. A topological pass reconstructs all pool qualities from any such LP flow.

Every physical multi-output flow decomposes into feasible single-output flows.
The correct multiplier on an arc `u→v` is the fraction of flow at its **head** `v`
that ultimately reaches the chosen output. At a pool, this scales every incoming
arc by a common factor, retaining that pool's quality. Reverse flow conservation
ensures that the new total outgoing flow matches the scaled incoming flow. Thus
the decomposition preserves mixing and upper capacities. Costs add, so a negative
total cost has a negative single-output component.

Three useful consequences are proved in the result file:

1. At most `|J|` single-output LPs decide triviality and produce a profitable
   physical flow whenever one exists. Selecting the best output gives an
   output-count profit approximation.
2. For the sign test alone, delete zero-capacity resources, compute shortest
   input-output path costs, and solve small convex blending LPs. All strictly
   positive capacity magnitudes can be handled by a common final scaling.
   A negative witness needs at most `K+1` input-output paths, where `K` is the
   number of qualities.
3. Without upper capacities, the convex conic hull of physical flow is exactly
   the Minkowski sum of the single-output polyhedral cones. This gives a compact
   linear lift for every homogeneous valid inequality in the original flow space.
   It does not give the capacitated convex hull; a five-node strict counterexample
   is included.

The shortest-path reduction and the cone formulation were independently suggested
by the root agent and both proof reviewers as well as checked against the main
argument. They are recorded because they make the scope and algorithm clearer,
not because simultaneous internal discovery establishes novelty.

## Prior art found before assigning any novelty status

**The standard case is already covered.** Dey and Gupte, *Analysis of MILP Techniques
for the Pooling Problem*, Operations Research 63 (2015), 412–427, DOI
[10.1287/opre.2015.1357](https://doi.org/10.1287/opre.2015.1357), prove a polynomial
output-count approximation by one-output rounding. Their
[article manuscript](https://optimization-online.org/wp-content/uploads/2013/04/3849.pdf),
Section 1.1, explicitly excludes pool-to-pool arcs. Theorem 2 in Section 4 gives
the approximation; Section 6 notes that one-output pooling is polynomial.
The sign test for standard pooling follows immediately. The local package is a
slide presentation, so the article manuscript was consulted for the exact scope.

**The generalized destination variables are already known.** Boland, Kalinowski,
and Rigterink, *New multi-commodity flow formulations for the pooling problem*,
Journal of Global Optimization 66 (2016), 669–710, DOI
[10.1007/s10898-016-0404-x](https://doi.org/10.1007/s10898-016-0404-x),
introduce terminal-commodity fractions and flows for generalized networks. Their
[open manuscript](https://optimization-online.org/wp-content/uploads/2015/06/4959.pdf),
Section 4.2.1, PDF p.8-9, uses precisely the head-indexed commodity fraction in our
proof. Equations (18)–(21) encode commodity conservation, output quality,
bilinear consistency, and summation. The model, relevant formulation section,
and conclusion were checked. The paper's emphasis is equivalence and strength
of formulations; the searched sections do not state the zero-optimality or cone
conclusion. That absence does not make the representation new.

The zero-optimality conclusion can also be obtained by taking this established
terminal disaggregation, dropping its bilinear consistency constraints, solving
the resulting LP with capacities on the sum of commodities, and selecting a
negative-cost output commodity. Every selected commodity is itself physically
realizable because it has just one destination. This is the cleanest explanation
of why the result is a consequence of existing machinery.

## Later primary sources screened

[Cheng, Tang, and Li, *New Multi-Commodity Flow Formulations for the Generalized
Pooling Problem*](https://skoge.folk.ntnu.no/prost/proceedings/ADCHEM-2018/media/files/0042.pdf)
(2018), abstract and introduction, explicitly build on the input- and
terminal-commodity work above. The stated aim is formulation design and
computational performance. The screening did not find a triviality theorem.

[*On the P-formulation and the split-fraction-formulation for the generalized
pooling problem*](https://www.sciencedirect.com/science/article/pii/S0098135422002319)
(2022), accessible abstract and introduction, compares formulation strengths
under bound-consistency conditions. Its model discussion and references confirm
the established role of source and destination disaggregation. This was an
introductory scope screening, not a complete proof audit.

[*Improved Rank-One-Based Relaxations and Bound Tightening Techniques for the
Pooling Problem*](https://link.springer.com/article/10.1007/s11081-025-09997-6)
(2025), introduction and Sections 3.1–3.2 and 4.1, discusses generalized pooling
and source/terminal formulations. Its model permits positive lower bounds on
node and arc throughputs, so the present zero-feasible scaling argument cannot
be applied to that broader class without checking those bounds. The sections
screened concern stronger rank-one relaxations rather than the sign test.

Queries included the exact word “triviality,” zero optimal cost, negative-cost
pooling, single-output polynomial algorithms, generalized-network approximation,
terminal disaggregation, uncapacitated pooling convex cones, shortest-path
blending, and output-commodity formulations. Most exact-triviality hits led back
to the source question. This search is targeted and not exhaustive.

## Verification and research status

The mathematical reviews are
[review-pooling-triviality.md](review-pooling-triviality.md) and
[review-pooling-triviality-second.md](review-pooling-triviality-second.md).
The first includes the later theorem extensions; the second covers the main
sign proof and shortest-path criterion. Neither review is external peer review.

The result answers the mathematical question posed in the specified model.
It should not be described as resolving fixed-quality pooling optimization,
pooling with positive demands, or a general MINLP zero-optimality problem.
No new hardness or tractability theorem for those broader classes was obtained
in this bounded investigation. The principal useful additions to the repository
are the explicit proof, the precise prior-art classification, and the capacity
and formulation distinctions that prevent overclaiming.
