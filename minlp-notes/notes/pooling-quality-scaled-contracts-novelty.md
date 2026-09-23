# Quality-scaled fixed-contract pooling: bounded source assessment

Date: 2026-09-05. Source review by `joint_flow_novelty`, coordinated with
`pooling_all_two_review` and `pooling_degree_two`.

The proposed polynomial algorithm is for one pool, scalar quality (or an
affine-rank-one quality description), degree-two bypass graph, exact input
supplies, and exact product throughputs and quality masses. Feed and outlet
counts are unrestricted; common pool-throughput bounds must be redundant.
The complete new proof in
[the quality-scaled flow investigation](pooling-quality-scaled-path-flow.md)
was read after the source search, together with the preceding model and conservation proof in
[the fully contracted investigation](pooling-all-product-contracts-quasipolynomial.md)
and the authors' description of the strengthening. This is not a mathematical
review of the new transformation or the contract-exception extension.

No matching restricted theorem was found. The candidate should be positioned
as a pooling tractability result built from classical circulation cuts and
quality-mass reformulations. Neither a new Hoffman theorem nor a general
polynomial parametric-network-flow algorithm is claimed.

## Closest polynomial pooling results

Natashia Boland, Thomas Kalinowski, and Fabian Rigterink, *A polynomially
solvable case of the pooling problem*, arXiv:1508.03181, explicitly excludes
input-to-output bypass arcs from the model used for its complexity results,
PDF p.2. Replacing bypasses by auxiliary pools is valid as a modeling
operation, but does not preserve the one-pool parameter. The paper's main
polynomial result fixes the number of inputs; it also summarizes earlier
fixed-quality one-pool results within that no-bypass convention. Its model
and relevant parameter scope were reread, PDF pp.1–3 and 6–7.
[Primary preprint](https://arxiv.org/pdf/1508.03181).

Our comparison: those results do not establish the present arbitrary-feed,
arbitrary-outlet bypass theorem. In particular, citing a headline
“one pool and one quality is polynomial” without its arc convention would
incorrectly erase the very restriction at issue here.

Radu Baltean-Lugojan and Ruth Misener, *Piecewise parametric structure in the
pooling problem: from sparse strongly-polynomial solutions to NP-hardness*,
uses the pool concentration as a parameter and studies direct feeds.
Assumption 2.2 in the open preprint, PDF p.5, fixes product demands while
dropping feed-availability and pool-capacity constraints. Section 4 extends
the positive result to multiple outputs; Remark 4.6, PDF p.24, discusses
the role of the assumptions. These passages were reread. The PMC version
requested a CAPTCHA, so the openly accessible preprint was used instead;
no restriction was bypassed.
[Primary preprint](https://optimization-online.org/wp-content/uploads/2016/05/5457.pdf).

Our comparison: fixing product throughput is already a known favorable
assumption. Here, however, exact shared input supplies remain, individual
arc bounds remain, and exact output quality masses enable global
conservation to remove the dense pool equations. The new theorem exchanges
the earlier feed-availability relaxation for more restrictive contracts and
bypass topology. It is not a direct extension of every earlier polynomial
subclass. Nor does a broad hardness statement after relaxing earlier
assumptions imply hardness of every more specialized fixed-contract case.

## Quality-weighted flow variables are established

James Luedtke, Claudia D'Ambrosio, Jeff Linderoth, and Jonas Schweiger,
*Strong Convex Nonlinear Relaxations of the Pooling Problem*,
arXiv:1803.02955, Section 2, PDF pp.3–4, explicitly introduces excess quality
relative to product specifications, separates the pool and bypass excess
contributions, and records quality-times-flow relations. Those definitions
were read in the primary manuscript. They are used to derive relaxations,
not the current exact contract algorithm.
[Primary preprint](https://arxiv.org/pdf/1803.02955).

Our comparison: interpreting concentration differences times flow as signed
attribute mass is standard. The proposed specialization
`w_ij=(C_i-q) z_ij` instead measures relative to the variable common pool
quality. The potentially useful step is proving that, after treating
exceptional concentrations and using degree-two local equations, it yields
an ordinary signed transshipment with low-degree parameter-dependent
bounds. This search did not find that exact signed-network reduction in the
pooling sources inspected. Absence from these sources is not exhaustive
priority clearance for the variable substitution itself.

## Hoffman cuts and parametric feasibility

Alexander Schrijver, *Combinatorial Optimization*, Part I, Corollary 11.2i,
printed p.175 (PDF p.91 of the linked part), explicitly characterizes signed
arc flows with lower/upper bounds and interval node imbalances by cut
inequalities. Corollary 11.3a, printed p.176 (PDF p.92), gives the associated
algorithm through a maximum-flow reduction. Both statements and proofs
were independently read. This is an established theorem reproduced in a
standard reference, not a claim to have inspected Hoffman's original paper.
[Open reference](https://www.lamsade.dauphine.fr/~cornaz/Enseignement/M2_MODO/DATA/A1.PDF).

The pooling proposal uses degree-two bypass components to reduce the needed
inequalities to polynomially many connected path or cyclic intervals. Once
their coefficients are quadratic in one parameter on each sign chamber,
root isolation and testing the resulting intervals are standard univariate
algebraic operations. The theoretical contribution would be the exact
pooling-to-network reduction and its coefficient-degree control, not the
cut characterization or root-isolation machinery.

Searches for pooling with Hoffman cuts, signed quality flows, and parametric
circulation did not locate a matching primary result. General parametric
flow results with monotone affine capacities or parametric quadratic costs
cannot be imported merely because of their titles: they parameterize
different data or require additional structure. No broad impossibility or
general parametric-flow claim follows from this bounded search.

## Output and exception scope

In the fully contracted base model, ordinary input costs and product revenues
are constant because every external throughput is fixed. The positive base
statement is feasibility and witness recovery, not arbitrary arc-cost
optimization. The degree-at-most-two concentration witness in Section 7 would
be a useful explicit arithmetic refinement if the independent proof audits pass.

The authors also propose a fixed number of external contract exceptions,
retained as a fixed-dimensional core, to recover nonconstant standard-profit
optimization. This extension was described to this reviewer but its full
new proof was not yet available during the source search. No specific prior
fixed-exception theorem was found; its scope should be stated by listing
exactly which supplies, throughputs, or quality contracts may vary. A fixed
number of exceptions is not the same parameter as a fixed total number of
pool feeds or outlets.

Nonredundant common pool capacity and general dense arc costs require
separate arguments. Affine-rank-one quality compression is an elementary
linear dependence reduction and should not be advertised as a distinct
novel algorithm. Exceptional values `q=C_i`, equal source qualities, inactive
pool throughput, and missing pool arcs belong in proof review, since the
signed scaling must not discard such cases.

Recommended wording: “Exact supply and product contracts expose a signed
quality-flow structure in one-pool instances with degree-two bypass graphs.
Combining that reduction with classical circulation cuts gives a
polynomial feasibility algorithm despite unrestricted feed and outlet
counts. No equivalent restricted result was located in the primary sources
checked.” Keep the contract-exception claim separate until its exact scope
and proof are available.

This bounded review used primary manuscripts for definite model comparisons,
and the original reference statement for the known circulation machinery.
It neither certifies exhaustive novelty nor substitutes for independent
mathematical verification.

## Later complete extension drafts: scope update

The complete drafts
[bounded contract exceptions](pooling-bounded-contract-exceptions-algorithm.md)
and [fixed affine quality rank](pooling-fixed-rank-contract-exceptions-algorithm.md)
were subsequently read on 2026-09-05. This replaces the earlier
unavailable-full-proof caveat for purposes of source comparison; independent
proof audits were still in progress when this addendum was written.

The scalar extension fixes the number of exceptional external nodes, not
the total feed or outlet count. Ordinary nodes retain exact supplies or
exact demand and quality contracts. Exceptional inputs can have supply
intervals, and exceptional outputs can have demand and quality intervals.
Only their incident flows and the common concentration remain in the
algebraic core, together with global mass and quality identities. The
objective is standard throughput revenue minus source cost. Thus this is
nonconstant economic optimization, not merely the base model's
constant-profit feasibility.

The second extension fixes both the exception count and the affine rank
of input quality vectors, while allowing the total number of qualities to
grow. Its scalar projections are computation charts: every remaining vector
quality equation is retained as an arc-bound or parameter condition. It
does not assume that a single projected quality equation physically replaces
all quality balances. Its exact algebraic optimizer has polynomial encoding;
the scalar base's degree-at-most-two witness guarantee is not asserted here.

The earlier source comparisons still apply. BKR's no-bypass convention does
not cover these classes; Baltean-Lugojan–Misener's relaxed feed availability
is different from exact supplies with finitely many exceptions. Luedtke and
coauthors establish excess-quality mass variables and convex relaxations,
but the checked passages do not give these fixed-exception classifications.
No matching theorem was found in that bounded set of sources. This addendum
is a scope comparison using those readings, not a new exhaustive search of
all fixed-rank pooling literature.

The fixed-rank extension is more than elementary rank-one compression:
its treatment of the additional equations needs its own mathematical proof.
Still, affine-basis computation, a finite family of separating directions,
Hoffman cuts, and fixed-dimensional algebraic elimination are established
tools. The possible contribution remains their combination for this
contracted physical model. Neither extension establishes general
uncontracted degree-two pooling tractability, nonredundant common-pool
capacity optimization, or unrestricted dense arc-cost optimization.
## Later arbitrary-quality theorem and five-exception boundary

The complete promoted
[contract-exception algorithm](../results/pooling-contract-exceptions-algorithm.md)
was read on 2026-09-05. It removes both fixed quality count and fixed
input-quality affine rank. All other key hypotheses remain: one pool,
bypass maximum degree two, fixed many exceptional external contracts,
exact ordinary supplies and product demand/quality vectors, standard
economics, and a redundant common pool-throughput bound. It gives exact
polynomial-bit optimization and common real-algebraic flow recovery; the
runtime exponent may depend on the exception count.

The scope change has a concrete reason. Any ordinary product receiving
positive pool flow confines the pool-quality vector to the affine span of
its contracted quality and at most two bypass source vectors. The algorithm
enumerates these polynomially many spaces of dimension at most two. If no
ordinary product receives pool flow, only the fixed exceptional receivers
remain active, permitting a fixed-dimensional output-fraction representation.
Every ambient quality equation is retained. This is stronger than merely
assuming that the input qualities have low affine rank.

The earlier primary-source distinctions continue to apply: the checked
Boland–Kalinowski–Rigterink model excludes bypasses, the checked
Baltean-Lugojan–Misener tractable model drops feed availability constraints,
and the checked Luedtke excess-quality construction addresses relaxations.
These facts do not by themselves prove novelty, but none supplies the
arbitrary-quality fixed-contract-exception theorem. A short fresh search
for degree-restricted pooling with exact contracts and growing quality
dimension found no closer matching primary theorem. This is a bounded
scope update, not an exhaustive new literature review.

The promoted
[five-exception feasibility theorem](../results/pooling-five-exception-feasibility-hardness.md)
provides a complementary restriction: one scalar quality, two pool feeds
and outlets, input total out-degree at most two, output total in-degree
at most three, and only five exceptions to exact external contracts. It
asserts strong NP-completeness with fixed finite flow-bound and quality
alphabets and no economic threshold objective. Its complete statement and
source/reduction interface were read; mathematical audits remain separate.

The positive and negative topology requirements must be stated precisely.
The positive algorithm bounds bypass degrees at both sides by two; the
hard instances contain ordinary products with three bypass inlets. Pool
attachments also contribute to total degree, so bypass degree and total
degree must not be interchanged in a claimed boundary. Positive exact flow
contracts are present in the hardness theorem; zero-flow feasibility with
all lower bounds zero is not claimed hard.

General one-pool pooling hardness is prior. The potential distinct
contribution is this matched contract/topology classification and its
arbitrary-quality positive side, not a first general hardness theorem or
a new circulation criterion. Neither the number five nor fixed exception
count is claimed minimal. No broad uncontracted degree-two tractability
claim follows from the result.


## Closure: two distinct source-quality vectors

The final [two-quality convex feasibility theorem](../results/pooling-two-source-qualities-convex-feasibility.md)
uses a different restriction from the preceding degree-two algorithms.
It permits arbitrary bypass topology and arbitrary source supply intervals,
while fixing every product's demand and complete quality vector. There
are at most two distinct complete source-quality vectors. Pool-outlet and
common pool lower bounds are zero; restrictive upper bounds are retained.
A signed scaling and one shared quadratic epigraph give an exact convex-QP
feasibility formulation, with polynomial-encoding rational physical
witnesses. Two independent final-scope proof audits passed.

The [separate focused comparison](pooling-two-source-qualities-convex-feasibility-novelty.md)
checks Boland–Kalinowski–Rigterink, Baltean-Lugojan–Misener, Luedtke and
coauthors, and Dey–Kocuk–Santana against this precise class. No matching
theorem was located in those primary sources. Convex-QP solvability,
quality-mass variables, and convexification of pooling substructures are
established; the potential contribution is their exact combination for
this complete physical subclass. Variable source costs are not constant,
so this theorem does not inherit the standard-profit objective of the
fixed-exception theorem.


## Closure: common throughput intervals for contracted degree-two pooling

The [common-capacity algorithm](../results/pooling-contracted-common-capacity-algorithm.md)
now removes the redundant common pool-capacity requirement from the scalar
exact-contract, degree-two bypass class. It permits arbitrary common
throughput lower and upper bounds, including a positive lower bound,
while retaining every individual arc bound. The same affine-rank-one
quality compression applies. Its witness field has polynomial degree;
the earlier degree-at-most-two bound is not asserted for this extension.

The previously missing support calculation is now complete and twice
independently audited. Bounded-flow divergences form a box-truncated
submodular base polyhedron. Sorted reciprocal source-quality costs
express maximum and minimum total bypass flow through its prefix rank
values. On bypass paths and cycles those rank values are binary
submodular cut problems whose exact symbolic minima have polynomially
many univariate pieces. The common pool interval is feasible precisely
when its complementary bypass interval meets the attainable support
interval. This is an additional aggregate test, not a claim that local
path feasibility alone had enforced shared capacity.

The [specific source note](parametric-path-cut-box-truncation-source.md)
locates the exact box formula and greedy rule in Shioura–Shakhlevich–
Strusevich (2013), Theorems 1–2 and equation (11). Those tools are prior.
The earlier pooling source comparisons remain applicable: the inspected
BKR model excludes bypasses, and the inspected Baltean-Lugojan–Misener
positive model drops source availability and pool-capacity constraints.
No matching contracted degree-two common-capacity theorem was located
in those checked sources. This is a bounded scope comparison, not an
exhaustive new search or a novelty claim for generic parametric flow.

Arbitrary external interval contracts and dense individual arc-cost
optimization remain outside this capacity theorem. These are recorded
limits of the finished investigation, not pending algorithm claims.
