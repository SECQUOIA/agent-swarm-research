# Weighted passive-flow objectives: graph-characterization source audit

Date: 2026-09-05. Bounded source assessment of the
[weighted-potential tree characterization](potential-flow-weighted-potential-tree-characterization.md)
and [weighted-flow cactus characterization](potential-flow-weighted-arc-cactus-characterization.md).
Both complete drafts were read; the parent reports two passing mathematical
reviews for each. This note assesses sources, not proofs.

No directly matching characterization was found in the openly inspected
primary literature. The defensible potential contribution is the precise
objective-dependent boundary, under one fixed nonlinear quadratic law:

| Universally quantified objective | Proposed graph class |
| --- | --- |
| Every zero-sum linear functional of potentials | Trees |
| Every linear functional of arc flows | Cacti |

Here graphs are finite, connected, and simple; nominations are fixed and
balanced; positive resistance uncertainty is an independent product; and
the compared scenarios have no additional physical capacity or potential
constraints. The property is equality of extrema for compact scalar
resistance sets and their interval hulls, for every allowed nomination and
objective. It is stronger than an individual-output bound. A complete
priority claim remains premature because an unusually relevant older
nonlinear-tolerance source is still unread.

## Closest directly checked predecessors

Aßmann, Liers, Stingl, and Vera,
[Deciding Robust Feasibility and Infeasibility Using a Set Containment Approach](https://arxiv.org/pdf/1808.10241),
already studies fixed nominations and uncertain pressure-loss coefficients.
Its tree treatment, especially Corollary 4.3 and Lemma 4.6, uses fixed flows
and linear dependence of potentials on those coefficients. Proposition 4.9
and Lemma 4.10, PDF pages 20–21, express single-cycle flows as a fixed offset
plus a scalar circulation and characterize circulation intervals through
inequalities linear in the resistance coefficients. These are direct
antecedents to both positive directions. Extending the scalar cycle argument
to arbitrary linear flow objectives and independent cactus blocks is a short
consequence of that structure. The checked statements do not characterize
all graphs satisfying the weighted-objective hull property.

Duffin,
[Topology of Series-Parallel Networks](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf)
(1965, DOI `10.1016/0022-247X(65)90125-3`), Theorems 0–1, printed
pages 306–307, establishes classical confluence/current-direction topology;
Section 5, especially Theorem 4, treats monotone nonlinear resistor
characteristics. This is foundational attribution for topology-based sign
arguments. Its checked statements do not give the present all-linear-output
tree/cactus pair of characterizations. The repository's separate
[single-arc series-parallel theorem](../results/potential-flow-series-parallel-arc-characterization.md)
must likewise not be mistaken for a prior-literature theorem covering
arbitrary weighted sums.

Bryant, Tygar, and Huang,
[Geometric Characterization of Series-Parallel Variable Resistor Networks](https://people.eecs.berkeley.edu/~tygar/papers/Geometric_characterization_of_series-parallel/Bryant_Journal_preprint.pdf)
(1994, DOI `10.1109/81.331520`), gives polygonal sets of possible
Thevenin/Norton equivalents for uncertain linear circuits. Its grounded-tree
extension computes individual node ranges; the preprint also discusses the
straight-line locus resulting from changing one linear element. This is
established geometric tolerance analysis, with a different constitutive law
and output representation. Marginal ranges do not determine the extrema of
all weighted sums. The present nonlinear graph boundary must not be stated
as a boundary for linear Ohmic networks.

## What remains potentially distinct

The tree positive direction is elementary: conservation fixes flows and
every weighted potential becomes affine in resistances. On a cactus, a
weighted flow objective becomes a sum of affine functions of independent
cycle circulations. These observations deserve modest positioning, given
the direct scalar predecessors above.

The substantive converse is universal over graphs: every non-tree contains
a subdivided triangle obstruction for weighted potentials, and every
noncactus contains a theta obstruction for weighted flows. The drafts retain
strict interior advantages after restoring all extra edges with finite,
positive, polynomially encoded resistances. Their witnesses use one uncertain
resistance and fixed small nomination/objective supports. No matching
fixed-quadratic weighted obstruction and complete converse was located.
Subdivision and weak-conductance restoration are familiar methods; the
restricted physical realization and the resulting exact boundaries are the
contribution to assess.

For a fixed nomination and resistance product, equality for every linear
functional is the standard support-function characterization of equality
of convex hulls of attainable output vectors. That interpretation is not
itself new. It also explains why linear combinations of individually
monotone outputs need not inherit the property: their derivative signs and
magnitudes need not agree. Separate monotonicity here allows the direction
to depend on the other fixed resistance coordinates; it does not claim one
global sign vector throughout the whole box.

## Unresolved older circuit source and claim limits

Hasler and Wang, *Parameter tolerances in non-linear resistive circuits:
worst case analysis based on monotonicity*, NOLTA 1993, pages 841–846,
remains unread. Its bibliographic entry is confirmed in reference 2 of
Pastore's primary
[DC tolerance analysis of electronic circuits by polyhedral circuits](https://arts.units.it/retrieve/e2913fde-d2e2-f688-e053-3705fe0a67e0/2869823_10.1002-cta.2098-PostPrint.pdf).
The checked Pastore manuscript uses nonlinear characteristic strips and
polyhedral solution enclosures; it does not state this graph hierarchy.
An exact-title search again did not locate an open Hasler–Wang copy. The
related EPFL *Convexity of Resistive Circuit Characteristics* manuscript
also remained inaccessible: a public download request returned HTTP 429.
Indexed excerpts mention parameter dependence beyond source values, so it
cannot safely be dismissed as irrelevant. See the
[earlier circuit source audit](potential-flow-series-parallel-envelope-novelty.md)
for these retrieval limits.

Use qualified wording: “For fixed-nomination quadratic passive networks on
simple graphs, we characterize the graphs on which independent resistance
sets may universally be replaced by their interval hulls for all weighted
potential, respectively weighted flow, objectives. The positive mechanisms
build on classical tree/cycle reductions; explicit nonlinear obstructions
give the converses. No matching pair of characterizations was found in the
open primary sources inspected.” Avoid “first topology-based tolerance
theorem” or an unqualified priority claim.

These structural equivalences do not establish exact polynomial arithmetic
for sums of algebraic cycle extrema, or tractability of joint nomination
uncertainty. The simple-graph restriction is material to the potential
converse: two parallel edges on two vertices do not admit the required
three-vertex weighted objective. Computational hardness from finite
resistance choices is a separate result.
