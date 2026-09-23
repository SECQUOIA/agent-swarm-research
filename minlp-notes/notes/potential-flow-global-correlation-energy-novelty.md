# Correlated cactus energy design: focused source addendum

Date: 2026-09-05. Bounded assessment by `joint_flow_novelty`. The complete
[energy companion](potential-flow-global-correlation-energy-design-hardness.md)
was read. Mathematical verification is assigned separately. The source
distinctions in the [global-correlation assessment](potential-flow-global-correlation-novelty.md)
remain applicable.

No matching bounded-data theorem was located for the precise combination
of a fixed simple degree-three cactus, fixed unit source/sink nominations,
common quadratic law, resistance values in `[1,3]`, and one global rational
resistance polytope, with minimum source-to-sink potential drop as objective.
The companion turns the earlier total-arc-flow example into a more directly
interpretable performance objective: prescribed-throughput dissipation,
equivalently the source-to-sink potential difference. It is a supporting
restriction theorem using established concave minimization and MaxCut.

## Classical energy geometry

Ghosh, Boyd and Saberi, *Minimizing Effective Resistance of a Graph*,
[primary author copy](https://web.stanford.edu/~boyd/papers/pdf/eff_res.pdf),
Section 2.7, printed p.44/PDF p.8, proves convexity in edge conductances
and explicitly credits Shannon and Hagelberger for concavity in edge
resistances. Its bibliography identifies *Concavity of Resistance Functions*,
Journal of Applied Physics 27 (1956), 42–43. Section 2.7 and the bibliographic
entry were read; the 1956 original was not read in this audit. The earlier
source spells the second surname “Hagelberger”; the original author's name
is D. W. Hagelbarger.

Groß, Pfetsch, Schewe, Schmidt and Skutella,
*Algorithmic Results for Potential-Based Flows: Easy and Hard Cases*,
[primary preprint](https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf),
Section 3, Equation (7), PDF p.7, recalls the classical convex flow-energy
problem `min_{Ax=b} sum beta_e Psi(x_e)`, with `Psi` the integral of the
strictly increasing constitutive function. Its KKT equations recover the
physical state. The paper credits earlier work for this variational
formulation. The displayed formulation and surrounding proof were read.

Comparison: because that feasible flow set is independent of resistance,
its optimum is an infimum of affine functions of `beta`, hence concave in
`beta`. For a common homogeneous quadratic law, multiplying the integral
energy by three gives dissipation, so it has the same concavity. This is
an immediate mathematical consequence of the classical formulation. Neither
resistance concavity nor endpoint attainment when minimizing over a polytope
is a new result of the companion.

The network identity `sum_e x_e (pi_tail-pi_head)=pi^T b` is the incidence
balance identity. With unit source/sink nominations, it yields the prescribed
potential difference. In a gas interpretation the potentials are squared
pressures; avoid calling this the ordinary pressure difference or identifying
it without qualification with actual compressor power.

## Earlier design hardness and a recent close model

Chan, Lau, Schild, Wong and Zhou, *Network design for s-t effective
resistance*, [primary preprint](https://arxiv.org/pdf/1904.03219), studies
choosing a subgraph under an edge budget to minimize linear effective
resistance. Its introduction reports NP-hardness and an FPTAS on
series-parallel graphs. Section 2.2, Fact 2.1, PDF pp.8–9, states the
unit-flow minimum-energy characterization; Facts 2.2–2.3 distinguish
resistance monotonicity and conductance convexity. The model, introduction,
and these facts were read; its full hardness proof was not audited here.

Klimm, Pfetsch, Skutella and Strubberg,
*Approximating the Network Design Problem for Potential-Based Flows*,
[April 2026 primary preprint](https://arxiv.org/pdf/2604.26882), model (2),
PDF p.2, chooses edge installation and continuous conductances, with fixed
and linear investment costs, to carry unit flow within potential bounds.
Corollary 4, PDF p.8, gives convex optimization when fixed costs vanish.
Theorem 12, PDF pp.20–21, proves approximation hardness using Steiner Tree.
Theorem 13, PDF pp.21–22, gives NP-hardness on series-parallel graphs through
Partition/Knapsack constructions. The model, results table, Corollary 4,
and these theorem statements and reduction setups were read. The full
approximation algorithms were not audited.

Comparison: general effective-resistance or potential-flow network design
hardness is already known, including simple series-parallel topology. The
companion's distinctions are a graph with every edge already present and
bounded positive resistance, no installation decisions or investment
objective, and linear cross-cycle constraints in the resistance coordinates.
Those constraints are not preserved as linear constraints after transforming
to conductances, so the convex continuous-design result does not contradict
the proposed hardness. Conversely, a general design-hardness statement must
not be promoted as new by suppressing these distinctions.

## What the supporting construction adds

The paired prefix bridges represent the uncertain coordinates as actual
edge resistances while contributing constant dissipation. This removes the
variable bridge bias that would otherwise disturb the MaxCut objective.
The paired triangles then make each comparison edge contribute one of two
fixed energy values at cube vertices. This is a concrete bounded passive
network realization of a classical concave cube optimization mechanism.

Quadratic nonlinearity is not essential to that mechanism. As an independent
scope observation, the same triangle with a linear law has effective
resistance `e_1(s)=2s/(1+s)`, which is strictly concave. Its paired values
are `2e_1(2)=8/3` at an uncut edge and `e_1(1)+e_1(3)=5/2` at a cut edge.
Their difference is `1/6`. Thus an analogous elementary reduction is
available already for linear resistors. This observation is not a completed
priority assessment or independent audit of a new linear-law theorem; it
shows why the claimed source of difficulty should be the correlated design
constraints, not the quadratic exponent.

The stated strong hardness and fixed absolute gap concern unnormalized
total dissipation, with a growing number of triangles and growing global
cycle rank. The restricted NP-completeness certificate uses the fixed
algebraic field generated by `sqrt(2)` and `sqrt(3)` at binary designs.
Do not extend that membership claim to arbitrary rational-profile radical
sums or infer relative-error, normalized-objective, or fixed-global-rank
hardness from it.

The candidate is best described as a precise structural hardness refinement
and a useful energy-objective companion to the existing correlation example.
The checked literature does not settle exact priority for this restricted
family. Classical energy variational principles, concavity, cube vertices,
and MaxCut must remain explicitly credited.
