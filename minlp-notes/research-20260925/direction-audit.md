# Research direction audit, 2026-09-25

This is a selection assessment, not a proof review or a novelty certificate.
It reads the repository as a whole: the separate `research-20260922` folder
does not include all of the September 22 theory. Historical closeout notes
also contain open labels that later result files have resolved.

The best opportunities require a new mechanism for preserving information
when combining nonlinear subproblems. Another envelope formula, restricted
hardness gadget, or small improvement to a finite aggregation count is
unlikely to exceed the strongest existing work.

## Strongest existing work to exceed

| Work | What makes it substantial | Material limit |
| --- | --- | --- |
| [Four strict PDLC aggregations](../results/four-aggregation-strict-pdlc.md) and [infinite HHC aggregation](../results/infinite-quadratic-aggregation-hhc.md) | Sharp geometry and an explicit counterexample to a published conjectural assertion; substantial parts have formal verification. | The positive theorem builds on the published four-bound. No efficient multiplier-construction algorithm is established. Infinite representation need does not imply poor fixed-objective optimization or exclude a small SDP lift. |
| [Smoothed spectral indicator messages](../results/smoothed-spectral-indicator-messages.md) paired with [bandwidth-two hardness](../results/indicator-quadratic-treewidth-two-hardness.md) | A meaningful exact-hardness/smoothed-tractability boundary, including construction of complete parameter-dependent dictionaries. | Fixed treewidth; polynomial dependence on numerical bounds and inverse perturbation scale; no practical performance claim. Generic additive approximation is already established. |
| [Relative spectral approximation sets](../notes/research-20260912-contribution-map.md) | A reusable integral matrix sandwich for paths and represented matroid bases, preserving singular ranges. | Fixed information dimension, potentially large polynomial exponents, substantial classical approximation/profile machinery. |
| [Structured bilevel optimization](../results/bilevel-fixed-block-response-algorithm.md) and [potential-flow structural algorithms](../results/potential-flow-bounded-block-rank.md) | Positive tractability results for meaningful nonlinear models, with explicit parameter and arithmetic boundaries. | Numerous adjacent extensions are already developed. A new restriction alone is unlikely to produce comparable insight. |

The strongest recent computational evidence is different: row hulls,
curve hulls for water networks, and correlated-quality pooling strengthen
specific important models. Their base hull principles are established.
The [September 22 folder summary](../research-20260922/README.md) correctly
records negative timing evidence for external OBBT and neural-network ridge
cuts. These are reasons to demand a new mechanism before investing in more
variants, not reasons to discard the correct underlying theory.

## Highest-potential targets

### 1. Exact compact convexification of tree quadratic indicators

Determine whether the closed epigraph hull

`cl conv{(x,z,t): x_i(1-z_i)=0, z in {0,1}^n, t >= x^T Q x}`

has polynomial-size SOCP or SDP lifts for arbitrary positive-definite tree
matrices `Q`, starting with stars. A positive theorem would supply an ideal
formulation for a widely useful MIQP primitive; an unconditional negative
theorem would expose a serious limit of conic reformulation despite efficient
optimization. Both outcomes are more consequential than another exact-state
count.

The current primary-source boundary is clear. [Choi et al., August 2026,
Section 7.2](https://arxiv.org/html/2608.22815v1#S7.SS2) construct exact SOCP
formulations of size `O(n^(k+1))` for a rooted tree with `k` leaves and explicitly
note exponential size for stars. [Bhathena et al.](https://arxiv.org/abs/2404.08178)
already optimize the unconstrained tree indicator QP in `O(n^2)` time and
memory. Therefore a new tree optimization algorithm alone is not a new
tractability theorem.

The repository's [star inverse-polytope obstruction](../notes/research-20260922-frontier-scout.md)
is a useful warning: the full intermediate inverse-principal polytope has a
correlation-polytope face. Its hard leaf-to-leaf inverse coordinates disappear
in the original epigraph projection. Transferring that obstruction without a
new argument is invalid. Objective-dependent message breakpoints also do not
directly yield one compact formulation valid for every objective.

**Recommendation:** pursue as a main theoretical target, with a deliberate
early test of whether a common scalar distribution can coordinate all leaf
perspectives. A quadratic substitution into the repository's existing
reciprocal-anchor mechanism would be a supporting lemma, not the main advance.

### 2. Exactly feasible decomposition for constrained hybrid dynamics

Seek a theorem that turns a sparse local-measure relaxation into an exactly
feasible integer trajectory while allowing state-dependent guards, active
state constraints, and useful terminal requirements. The error should be
controlled by a computable separator discrepancy and grow mildly with horizon.
This would address a major limitation of current state discretization and
moment decompositions in scheduling/control MINLP.

The existing [moment-control investigation](../notes/research-20260922-moment-control.md)
repairs dynamics by replaying controls. Its [source screen](../notes/research-20260922-separator-novelty.md)
already explains why contraction alone does not preserve logical feasibility.
New work must prove checkable recourse at active guards or identify a meaningful
class where such recourse is automatic. Assuming an arbitrary Lipschitz
feasible-control selector and summing a geometric series would probably be a
modest synthesis of established ideas.

Strong sources requiring direct comparison include incremental-stability and
tube-tightening methods in [Köhler et al.](https://arxiv.org/abs/1910.12081),
neighboring feasible trajectories under inward-pointing conditions in
[Frankowska, Marchini and Mazzola](https://www.numdam.org/item/10.1051/cocv/2017032.pdf),
and [Kirches, Lenders and Manns](https://optimization-online.org/wp-content/uploads/2016/04/5404.pdf)
on mixed-integer control with state constraints. These cover major parts of
the repair logic; they do not by themselves provide the proposed local-measure
rounding theorem. [Vasudevan et al.](https://arxiv.org/pdf/1208.0062) already
obtain exactly feasible pure switched controls by creating strict margin before
projection. [Shin, Anitescu and Zavala](https://optimization-online.org/wp-content/uploads/2021/01/8199.pdf)
give exponential sensitivity decay for graph-structured nonlinear programs
under uniform regularity. Neither exact feasible rounding nor locality alone
can therefore carry a new claim.

**Recommendation:** a high-payoff parallel scout, with exact guard and terminal
counterexamples before a general theorem. Its application importance exceeds
that of universal feature-count lower bounds on a cancellation example.
The most credible target is a checkable active-face/controllability condition
for switched-affine dynamics with polyhedral guards, yielding exact repair
with constants independent of horizon. Finite moment matching alone controls
average transport, not the uniformly small perturbations such repair may need.
For example, a stage forcing state `epsilon>0` must use a cost-one mode when
the cheap mode is legal only at zero. The next-stage local measure assigning
mass `1-epsilon` to the cheap mode at zero and `epsilon` to the expensive mode
at one matches the forced state's mean, costs only `epsilon`, and has transport
distance `2 epsilon(1-epsilon)` from it. Both state maps can be constant resets.
Thus perfect contraction and vanishing transport error do not imply vanishing
repair cost. This scout example must be excluded by a positive theorem's
actual geometry, not by informal regularity language.

### 3. Correlated-quality pooling hulls with a scalable structural description

The [multiattribute assessment](../research-20260922/pooling-multiattribute/assessment.md)
identifies a real information loss: a pool's quality vector belongs to the
convex hull of its source qualities, not an independent box. The corrected
record contains a safe improved bound for `pooling_sppc0pq`; the analogous
best-bound claim for `sppb0pq` was refuted.

The promising target is a structural hull or separation theorem whose cost
depends on intrinsic source-quality dimension rather than enumerating every
attribute combination, ideally extending to coupled outputs or shared pools.
That could make an existing useful bound available cheaply during a solve.
A fixed-number-of-attributes union-of-SOC-pieces construction is a reasonable
milestone, but may only combine the existing common-factor oracle with
standard disjunctive convexification. The box-quality special case has weak
experimental value and is a poor main target.

**Recommendation:** prioritize only if the next step escapes generic cell
enumeration and explains the observed correlation benefit. This is the most
credible near-term bridge from theory to an important application among the
unfinished local candidates.

## A fresh literature trap: sparse box quadratic hulls

[Dey and Khajavirad, August 2025](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/25/25T_014.pdf)
give SOC hulls when positive-diagonal vertices form a stable set and leave
adjacent-positive cases open. That boundary is already superseded:
[Khajavirad, February 2026, Theorems 5–6](https://arxiv.org/html/2601.18545v2#S4)
gives SDP hulls when every connected component of the positive-vertex subgraph
has size at most two. It also claims polynomial formulations under logarithmic
treewidth and positive-vertex degree bounds; the dependency issue below means
that complexity claim should not yet be taken as verified. Exactness of the
paper's particular SDP for three positive vertices remains a stated question.
However, [Anstreicher and Burer, Section 4, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf)
already give an exact SDP lift of the full three-variable box moment hull by
triangulating the cube into tetrahedra. Thus arbitrary finite SDP
representability in dimension three is not open. Conditioning on binary
nonpositive neighbors extends the component-piece construction to three
positive vertices by classical methods. This observation does not address
complete hypergraphs containing a cubic moment of the three positive variables.

**Concrete source issue, independently reconstructed:** Khajavirad's Lemma 7
claims that deleting a connected vertex set `C` and cliquing its neighborhood
gives treewidth at most `max(tw(G), |N(C)|-1)`. Take `G=K_(2,3)` and let `C`
contain one vertex on its two-vertex side. The original graph has treewidth
two: three bags consisting of the two-vertex side and one remaining vertex
give an upper bound, and a cycle gives a lower bound. After the deletion and
clique completion, the surviving vertex on that side and its three neighbors
form `K_4`, of treewidth three. The claimed bound is only two. This refutes
the lemma as written; it does not refute every conclusion of Theorem 6.
A valid replacement must be checked before using its polynomial-size guarantee.
The independent scout `box3_source_screen` found this issue; the author of
this audit reconstructed the graph calculation separately.
The scout also identified a safe bag-expansion bound after contracting positive
components: torso treewidth at most `(tw(G)+1) max(1,d)-1`, where `d` is the
largest component boundary. This supports polynomial size when treewidth is
fixed and boundary size logarithmic, but supplies only a quasipolynomial
estimate when both grow logarithmically. It is a repair route to check, not a
proof that the paper's stronger conclusion is false.

## Areas to deprioritize

- More unary/ridge envelope variants without a new coupling mechanism:
  probabilistic envelope cores and curve hulls have strong antecedents, while
  the repository already records neutral or negative solver timings.
- More restricted spatial-branching lower bounds: existing results already
  survive SDP/RLT, higher SOS and bounded-degree monomial lifts. General affine
  branching remains an important harder question, but the existing witness
  argument demonstrably fails there.
- Improving `2k` to `2k-2` for many quadratics in a three-dimensional span:
  mathematically interesting, but only a count refinement unless accompanied
  by an effective separator or a new structural principle.
- Further degree-two pooling hardness variants, fixed-grid switching values,
  or integer-precision refinements that do not change the application class
  or approximation model. These areas are extensively developed locally.
- Treating the nuclear benchmark bounds as a current route to global solution:
  the follow-up already finds the bound-driven search impractical.

## Evidence and checks

Inspected the main README, September 22 folder README, September 22 theory
closeout, recent result statements, the older open-thread audit, and the linked
source/experiment assessments above. Fresh searches checked tree indicator
hulls and sparse quadratic hull terminology, then opened the named primary
sources. This was an assessment of statements and opportunity, not a reproof
of existing results. Independent scouts checked constrained-control antecedents
and the low-dimensional quadratic comparison. The graph counterexample above
is a proof by explicit graph identification, with no numerical reliance.
No mathematical computation, solver run, project-wide
verification, or CI inspection was performed. Current publication priority
remains provisional throughout.

Targeted document check actually run: a Python scan of this file's relative
Markdown links and trailing whitespace passed. It checks document hygiene
only; the comparisons and counterexamples require mathematical reading.
