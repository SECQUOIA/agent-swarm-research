# Cactus flow region and scenario recovery: bounded source assessment

Date: 2026-09-05. Candidate:
[cactus flow region and optimization](potential-flow-cactus-flow-region-and-optimization.md).
This is a source review, not a full mathematical audit.

No matching primary-source statement was located for the complete combination
of an affine-box attainable flow region, equality with the convex hull under
finite resistance uncertainty, polynomial exact endpoint-scenario recovery
for every rational linear flow objective, and square-root-sum hardness of
exact scalar value comparison. The geometry itself is an elementary
consequence of scalar cycle freedom and independent cactus blocks. Position
it as a useful structural corollary with explicit computational output
guarantees, not a wholly new circuit-geometric mechanism.

## Closest literature and its scope

Randal E. Bryant, J. D. Tygar, and Lawrence P. Huang, *Geometric
Characterization of Series-Parallel Variable Resistor Networks* (1994), DOI
10.1109/81.331520, is a direct predecessor to geometric descriptions of
uncertain resistor behavior. It studies linear circuits through equivalent
characteristics and range computations. Earlier full-text inspection is
recorded with locators in the
[series-parallel source audit](potential-flow-series-parallel-envelope-novelty.md).
No whole-flow-vector cactus parallelotope theorem for common quadratic
laws was found in the inspected material. The prior geometry nonetheless
precludes presenting geometric uncertainty analysis itself as new.
[Author manuscript](https://people.eecs.berkeley.edu/~tygar/papers/Geometric_characterization_of_series-parallel/Bryant_Journal_preprint.pdf).

Rico Konrad Béla Raber, *Optimization, Reduction, and Robustness of
Potential-Based Flow Networks* (TU Berlin dissertation, 2022), contains
Section 5.3.3 on recovery of cactus networks. The primary repository abstract
and an indexed passage from that section were inspected. The question there
is reconstruction from effective-resistance measurements, with restrictions
on terminals and topology. It is different from varying independent
resistance intervals at fixed nominations and describing all resulting
flows. A full PDF open initially succeeded, but subsequent targeted reads
timed out; this assessment does not claim a complete search of the thesis.
[Primary repository record](https://depositonce.tu-berlin.de/items/a02ed62b-daa7-445a-b496-d8c3019382d5),
[open thesis](https://d-nb.info/1258349914/34).

The uncertain gas-flow setting already appears in Aßmann, Liers, Stingl,
and Vera, *Deciding Robust (In-)Feasibility Using Set Containment: An
Application to Uncertain Gas Networks*, arXiv:1808.10241, Section 4.1.4.
Its inspected fixed-nomination interval-resistance formulation and cycle
reductions are documented in the
[discrete-resistance source audit](potential-flow-discrete-resistance-hardness-novelty.md).
They establish the model and relevant algebraic methods, but did not supply
the present explicit full-region statement in the portions read.
[Primary preprint](https://arxiv.org/pdf/1808.10241).

The nonlinear circuit-tolerance source gap remains: Hasler and Wang,
*Parameter tolerances in non-linear resistive circuits: worst case analysis
based on monotonicity*, NOLTA 1993, pp.841–846, has not been retrieved.
Its existence is confirmed by Pastore's primary manuscript, reference 2.
The positive scalar-envelope step may have direct antecedents there;
priority for that step remains unresolved. The current product construction
does not remove that caveat.
[Pastore manuscript](https://arts.units.it/retrieve/e2913fde-d2e2-f688-e053-3705fe0a67e0/2869823_10.1002-cta.2098-PostPrint.pdf).

## What is elementary and what deserves explicit documentation

Conservation gives one scalar circulation per cactus cycle. Fixed effective
nominations and edge-disjoint blocks make those scalar choices independent.
A continuous scalar image of a connected resistance box is an interval;
the convex hull of a finite scalar set is the interval between its extrema.
Combining those facts gives the affine-box description and finite-set convex
hull. The nonlinear part lies in finding and realizing each cycle extremum;
the proposed piecewise-quadratic scalar envelope provides that step.

The geometry also yields endpoint attainment for convex flow objectives.
This is the familiar convex-function-on-polytope vertex argument. It gives
no polynomial algorithm for arbitrary convex maximization over many cycle
coordinates. Likewise, a rational-flow feasibility LP under interval
resistances is not cactus-specific and should remain separately credited as
a generic observation.

The exact algorithm returns rational resistance endpoints. It may also
return each physical flow coordinate in its own quadratic algebraic
encoding. Selecting the maximizing circulation endpoint depends only on the
sign of a rational objective coefficient for that cycle. Thus it never
needs to compare independent sums of radicals. Describing the output merely
as “exact optimization in polynomial time” would hide this essential scope;
use “exact optimizing-scenario recovery” and state the value output format.

## Arithmetic distinction and its antecedent

Kousha Etessami and Mihalis Yannakakis, *On the Complexity of Nash Equilibria
and Other Fixed Points* (2010), DOI 10.1137/080720826, Section 1, PDF p.4,
defines the positive-integer square-root-sum problem. It notes that even
evaluating the length of a specified geometric spanning tree or tour
against a threshold entails radical-sum comparison. That provides direct
primary context for why a finite structural solution and exact numerical
threshold evaluation are different tasks. This portion was reopened and
read in the present audit.
[Primary accepted manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/14011363/nash_focs07_full_j_spec_issue_sub.pdf).

The candidate's triangle-chain realization specializes this established
arithmetic obstacle to passive quadratic flows. With fixed resistances,
scenario selection is trivial, while the positive weighted flow sum
encodes a square-root sum. No equivalent triangle-chain encoding was
located. The reduction is elementary and is useful chiefly to prevent an
incorrect exact-value complexity claim. Square-root-sum hardness is not an
NP-hardness assertion, and it is compatible with polynomial additive
evaluation in the requested precision bits.

Recommended wording: “For fixed nominations on a cactus, independent
resistance intervals give an affine-box flow region, and finite resistance
sets have the same convex hull. Cyclewise algebra yields an exactly optimal
endpoint scenario for every rational linear flow objective in polynomial
bit time. Exact scalar threshold evaluation remains square-root-sum hard,
already without uncertainty.” Retain qualified priority and the separate
proof-review status.

Fresh queries covered cactus graphs and resistance uncertainty, attainable
current sets, flow polytopes, nonlinear circuit tolerance geometry, and
structural solution versus radical-sum value comparison. Unrelated plant
hydraulics and circuit design results were discarded. The search was bounded;
earlier primary reads are explicitly identified, and the unread sources are
not used to assert absence of overlap.
