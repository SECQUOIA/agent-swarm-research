# Investigation: Geoffrion's Property (P) without compactness

Date: 2026-09-05.

## Source and scope correction

The earlier open-problem list described the issue as an unresolved
first-half-implies-second-half conjecture without compactness. This wording
is too broad unless the two properties are distinguished.

[Geoffrion (1972), author-hosted full text](https://www.anderson.ucla.edu/faculty_pages/art.geoffrion/home/docs/GBD.pdf)
defines computational Property (P) at printed p. 251: for each multiplier,
the supremum can be taken essentially independently of the complicating
variables and its whole value function obtained with little extra effort.
At printed pp. 256–257 he defines the precise common-optimizer Property
(P′), equations (22-1) and (22-2), for cases with attained extrema. He then
states the conjecture about (P), verifies it under compactness and continuity
using (P′), and says boundedness can be weakened along the lines of §4.1.
He does not claim that no noncompact positive cases are known.

The new [result note](../results/geoffrion-property-p-conjecture.md) disproves
the exact common-optimizer implication (A) ⇒ (B). It **does not disprove the
informal computational claim**. Its feasibility value functions are
constant and explicitly known. This qualification is essential.

## Candidate and significance

The counterexample has one binary variable and four continuous variables,
with a closed convex SOC-representable continuous domain. The objective and
coupling function are affine for each binary assignment. All individual
maxima are attained and each fixed-binary subproblem is strictly feasible.
The two feasibility argmax sets are nonempty but disjoint. For every finite
nonnegative objective multiplier, a common Lagrangian maximizer exists.

This is stronger than a nonattainment example such as maximizing \(-1/x\)
on \([1,\infty)\). It identifies nonclosed joint images as the obstruction,
even when each coordinate maximum is attained. The likely value is a short
theoretical clarification or a lemma in a broader noncompact decomposition
analysis. It is not presently a high-impact algorithmic result.

## Open-literature search

Searches performed 2026-09-05 included:

- `Geoffrion "Property" "conjecture" Benders`
- `"generalized Benders" "P'" compact`
- `"Geoffrion" "first part" "second part"`
- `"property (P')" "Benders" counterexample`
- `"Benders" "common maximizer" compact`

The exact conjecture searches principally returned Geoffrion's own paper.
No openly indexed source resolving this exact noncompact common-optimizer
implication was located. This is limited search evidence, not proof that
the example or its implication is absent from the literature.

The primary later discussion located was
[Sahinidis and Grossmann (1991), *On the Generalized Benders Decomposition*](https://www.sciencedirect.com/science/article/pii/009813549185015M),
which discusses pitfalls of substituting primal solutions into Lagrangian
minimization in nonconvex GBD implementations. Its accessible text addresses
a different issue and does not settle the present implication. A later
[Barton presentation on nonconvex GBD](https://minlp.cheme.cmu.edu/2014/papers/barton.pdf)
uses Property P in the separable case. Neither source is evidence of novelty.

The positive limiting and closed-image arguments in the result are standard
optimization mechanisms. They are retained for completeness without
independent novelty claims. Related background worth checking before any
publication claim includes closed linear images of cones, recession analysis,
and vanishing regularization / lexicographic scalarization.

## Remaining work

- An [independent proof and source review](review-geoffrion-property-p.md)
  verified every result and the distinction between (P) and (P′).
- Audit classical regularization and conic image examples before claiming
  novelty of the construction.
- Do not call this a resolution of a long-open conjecture in status summaries.

## Added positive case

The aggregate-attainment criterion yields a positive implication on continuous
domains defined by convex polynomial inequalities when coupling functions are
concave polynomials and the finite collection of feasibility suprema is finite.
This follows directly from
[Belousov–Klatte (2002)](https://link.springer.com/article/10.1023/A:1014813701864),
whose abstract attributes the underlying attainment result to work from 1977.
The more general no-flat-asymptote characterization is given in
[Martínez-Legaz, Noll, Sosa (2018), Theorem 1](https://arxiv.org/html/1805.03451).
These are useful established consequences, not new attainment theory.
