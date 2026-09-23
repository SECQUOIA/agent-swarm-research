# Priority review: exact smoothed messages at fixed treewidth

Date: 2026-09-22. Independent literature and significance review of the
[fixed-treewidth result](../results/smoothed-fixed-treewidth-indicator-dp.md),
the [support-moment lemma](research-20260922-envelope-higher-moments.md), and
the [approximation-to-exact extension](research-20260922-approximation-exact-smoothing.md).
This review compares statements and proof mechanisms. It is not an integrated
proof review or an implementation check.

The final addendum below assesses the broader
[spectral-bound theorem](../results/smoothed-spectral-indicator-messages.md).
Earlier paragraphs retain the assumptions of the direct dynamic-programming
construction being reviewed at that stage.

The strongest defensible contribution is a specified penalty-noise model
under which exact continuous separator value functions can be constructed
in expected polynomial bit time on every fixed-treewidth graph. The
general Lipschitz support-count lemma is a potentially reusable contribution.
Both combine established ideas in a way not directly stated by the primary
sources inspected here. That is evidence for pursuing the result, not a
priority determination. The optimizer-only consequence has a particularly
close connection to established approximation-to-exact smoothing machinery
and should carry a correspondingly modest novelty claim.

## Closest exact indicator-quadratic results

**Trees are already solved without smoothing.** Bhathena, Fattahi, Gómez,
and Küçükyavuz give an exact quadratic arithmetic-time algorithm when the
positive-definite Hessian has tree support. Their parametric representation
is central to that algorithm. The present theorem is weaker on this graph
class, since it adds numerical bounds and random perturbations. The original
preprint is April 2024; the journal article was published online in May 2025,
with a 2026 issue date. These dates describe the same line of work, not three
separate advances. See [the preprint](https://arxiv.org/abs/2404.08178) and
[the journal article](https://link.springer.com/article/10.1007/s10107-025-02222-3).

**The March 2026 structured-graph paper is the direct algorithmic antecedent.**
Its Definition 5, Lemma 9, and Theorem 1 give exact parametric pruning and
dynamic programming under a uniform bound on nearly optimal local support
multiplicity, together with polynomial graph growth. The complexity depends
on the support-margin parameters, numerical bounds, and the decomposition.
It already distinguishes small representations from algorithms that construct
them. [Primary text](https://arxiv.org/html/2603.02103v1).

The candidate replaces this deterministic margin hypothesis by independent
penalty perturbations and needs no uniform degree or graph-growth bound.
Fixed treewidth permits arbitrarily large biconnected blocks. Those are
substantive extensions of the preceding local bounded-block result. Numerical
restrictions remain: the current direct message recursion uses strict diagonal
dominance. It does not subsume the earlier theorem in every parameter regime.
Its large-degree algebraic algorithm also does not improve the earlier paper's
practical implementation or its favorable linear-time regimes.

The [arXiv record](https://arxiv.org/abs/2603.02103) inspected on this date
lists only the March 2, 2026 version. Searches containing “smoothed” also
retrieve this paper's application of exponential smoothing to forecasting;
that is not a smoothed-complexity theorem.

## Approximation results limit the optimizer-only novelty

[Bienstock and Chen, Theorem 1.4](https://arxiv.org/html/2411.11722v1)
already give polynomial approximation algorithms for convex quadratic models
with indicator-controlled variable blocks and structured constraints. Their
graph is the constraint-block intersection graph. The displayed general
guarantee is superoptimality with bounded mixed-constraint infeasibility,
while preserving the combinatorial constraints. It must not be silently
quoted as the exact feasible additive oracle used in the local conversion.
Any application requires checking the formulation and its error transfer.
The paper's Section 2.2 treats banded indicator quadratics explicitly.

Gómez, Han, and Lozano give a banded-matrix decision-diagram approximation
method, including additive error control under numerical bounds. This is an
important existing approximation route for the bounded-bandwidth subclass.
[Primary preprint](https://arxiv.org/html/2405.03051).
The August 2026 decision-diagram paper broadens approximation guarantees
through spectral decay and graph growth, and covers sparsity in a Hessian
or its inverse. It does not state the present exact penalty-smoothed message
theorem. [Primary text, Theorem 4 and Section 8](https://arxiv.org/html/2608.22815v1).

The local approximation-to-exact proof now supplies its own feasible additive
oracle by ordinary finite-domain tree-decomposition dynamic programming.
For a spectral bound `mu I <= Q <= H I`, fixed support minimization gives
`||x||_2 <= ||c||_2/(2 mu)`; a rational enclosing box and a fine grid provide
an oracle with polynomial dependence on inverse accuracy when treewidth and
the numerical parameters are controlled. Fixed-bit restrictions preserve
this construction. This argument is elementary approximation theory, not
a new approximation frontier.

Consequently, the broader proposed optimizer-only theorem for spectrally
bounded positive-definite matrices is useful but is best positioned as a
concrete extension/application of established smoothed-complexity methods.
The distinction between that spectral theorem and the current direct SDD
message recursion should remain explicit.

## Higher gaps and expected running time are established tools

[Röglin and Teng, FOCS 2009, Lemma 6.1 and Theorem 6.2](https://www.roeglin.org/publications/FOCS09.pdf)
give generalized winner-gap estimates and an expected-polynomial-time
conversion from randomized pseudopolynomial binary linear optimization.
Their proof conditions on coordinate pattern classes and uses rank to obtain
several small independent linear differences. Their finite-input discussion
already considers discretized coefficients. The 18-page April manuscript has
different numbering: generalized winner gaps are Lemma 3.2, and the
expected-time application is in Section 6.1. [April manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2009/04/Pareto.pdf).

The local deterministic-offset extension preserves this mechanism. After
conditioning on the other coordinates, the nonlinear support cost enters
only the class minima. Affine differences can eliminate a reference value.
Thus a claim that nonintegral support costs fundamentally prevent the
classical method would now be false. The previous absence of a unary-cost
pseudopolynomial oracle only blocked an immediate application of the theorem
as stated; it did not block this proof adaptation.

The first-difference partition used to extract several near-optimal supports
is also standard ranked-solution enumeration. The potentially useful addition
is the certified additive-oracle version and its integration with continuous
quadratic support evaluation. Do not call the partition or the general idea
of approximation-to-exact smoothing new. Dughmi and Roughgarden already
state an FPTAS-to-exact smoothed conversion for binary linear maximization
in Proposition II.3. [Primary manuscript](https://www.math.uwaterloo.ca/~cswamy/courses/co759/agt-material/blackbox.pdf).

## What the Lipschitz support-moment argument adds

The candidate uses one shared random linear penalty `xi dot z` and an
arbitrary deterministic uniformly Lipschitz family `q_z(t)` on a compact
parameter domain. It bounds all fixed moments of the number of distinct
supports that minimize somewhere. It includes supports occurring only at
ties. For atomic noise, the interval-mass hypothesis accounts directly for
these ties.

The proof's distinctive intermediate statement is a bound on the probability
that a narrow near-optimal set shatters a specified coordinate subset. Its
conditional zero-pattern and unit-pattern minima turn shattering into an
axis-aligned small-box event. Classical Sauer--Shelah counting then controls
the size of the near-optimal set; a parameter net captures every active
support. The set-system inequality, conditioning method, and net argument
are established ingredients. The explicit combination and the finite-grid
conclusion are the candidate additions.

This must be compared with the much older polynomial moment bounds for
Pareto sets. [Moitra and O'Donnell, Section 2](https://www.cs.cmu.edu/~odonnell/papers/pareto-optima.pdf)
allow one arbitrary deterministic objective and several independently
perturbed linear objectives. [Brunsch and Röglin, Theorems 3–4](https://arxiv.org/pdf/1111.1546)
sharpen count and moment bounds. Their zero-preserving extension and
polynomial-objective corollary perturb the relevant nonzero coefficients;
they do not permit replacing all these directions by one random intercept
penalty while retaining arbitrary deterministic parameter functions.

There is no immediate reduction from the candidate to these stated Pareto
theorems: different deterministic quadratic coefficients would require
several unperturbed objective directions, and the general Lipschitz family
need not have a finite-dimensional coefficient representation at all. This
is a comparison of hypotheses, not a proof that no indirect reduction or
equivalent theorem exists. Conversely, the candidate's bound is much coarser
and depends on compact-domain covering numbers; it should not be advertised
as an improvement of the established Pareto bounds.

Smoothed parametric enumeration itself has clear precedent. For example,
[Applegate et al., Section 6](https://arxiv.org/html/1805.06420)
bound parametric shortest-path complexity by perturbing a two-objective
projection and invoking earlier shadow bounds. Its affine parameter model
and angular perturbations differ from the candidate's arbitrary Lipschitz
branches and independent coordinate penalties.

The strongest reusable claim is therefore specific: an explicit support
moment bound for a uniformly Lipschitz binary family under a single shared
random linear penalty, with a direct atomic version. The search did not
identify an earlier identical statement or a Sauer-based proof, but that
negative search result does not establish novelty.

## A stronger enumeration route identified during review

The coordinator has derived a route combining the moment bound with the
restricted additive oracle to list all supports active over a compact
parameter domain. At each point of a sufficiently fine deterministic net,
a certified partition procedure lists a superset of the narrow near-optimal
supports. Every emitted support remains within a slightly larger controlled
gap. The expected list size is therefore polynomial. Taking the union over
the net captures every active support; exact quadratic formulas can then
be retained or pruned.

This could construct all separator messages under spectral bounds without
the invariant-box requirement of the direct recursion. It is undergoing
separate proof and bit-complexity review and is not established by this
priority note. If verified, it should become the primary scope statement;
the SDD recursion would remain an alternative construction. In that case the
contribution's distinguishing capability would still be exact parametric
enumeration, not merely exact optimization of one sampled instance.

## Search record and limits

The sources above were opened and relevant theorem statements or proof
sections examined. The arXiv histories for the March structured-graph paper,
the tree paper, the banded paper, and Bienstock--Chen were also checked.
Searches included combinations of “smoothed”, “indicator quadratic”,
“fixed treewidth”, “parametric optimization”, “near-optimal solutions”,
“Sauer”, “shattering”, and “generalized winner gap”. Most unrelated learning
and analytical-smoothing hits were excluded. One guessed author-hosted
Brunsch--Röglin PDF endpoint failed; the arXiv full text was read instead.

No result here proves absence from the literature. In particular, a broader
search of parametric enumeration and ranked approximate optimization could
reveal an equivalent general transfer theorem. A final publication claim
should await that comparison and the separate adversarial proof reviews.
No computational or repository-wide verification was performed for this
literature-only review.

## Final addendum: spectral bounds and first-moment enumeration

The stronger construction is now written in the
[oracle message theorem](research-20260922-oracle-all-messages.md), with
independent proof reviews recorded separately. It supersedes the earlier
scope assessment that treated diagonal dominance, higher moments, and CAD
as necessary for the strongest local algorithm. It constructs exact full
quadratic dictionaries on prescribed bounded separator boxes for
`mu I <= Q <= H I` and every fixed treewidth. The dictionary includes every
support attaining the message anywhere, including ties and boundary-only
occurrences; it may also contain inactive supports. This is not a minimal
dictionary or an explicit decomposition into connected optimality regions.

The final proof needs only

```
E |{z:g(z)+xi dot z <= min_y(g(y)+xi dot y)+a}|
    <= (1+2 phi a+tau)^m.
```

The upper half of the classical sandwich inequality bounds a binary
family's size by its number of shattered coordinate subsets. Conditioning
on coordinates outside each subset bounds its shattering probability.
The certified approximate partition procedure has work proportional to its
output count, up to deterministic polynomial factors. A parameter net then
captures all active supports. Thus first moments suffice, and a uniform
noise grid with `N>=2n` points suffices. Neither CAD nor a limiting
continuous-noise argument is used. Correctness holds for every sample;
the expected runtime is polynomial in the numerical spectral bounds,
coefficient bounds, box radius, and inverse noise scale, at fixed width.

The contribution should be stated as this concrete count-and-enumeration
theorem and its exact indicator-QP message application. The sandwich
inequality is classical; [Kozma and Moran, Theorem 5](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v20i3p44/pdf)
states it and credits earlier work. The partition method is classical;
[Lawler's original article](https://pubsonline.informs.org/doi/10.1287/mnsc.18.7.401)
gives ranked enumeration from an exact optimization procedure. The present
use of certified additive lower bounds gives a controlled superset of
near-optimal supports, which is sufficient for the parametric conclusion.
Ordinary treewidth grid optimization supplies the restricted oracle.

Compared with the March 2026 exact parametric algorithm, this establishes
expected complexity under a specified penalty-only perturbation model
without its deterministic support-margin or graph-growth assumptions.
Compared with the established Röglin--Teng conversion, it explicitly
constructs complete bounded-parameter dictionaries, uses arbitrary
deterministic support offsets, and handles a linear-size atomic noise grid
through a direct count. The main novelty claim should not be the broad
principle that approximation becomes exact under smoothing, nor the
existence of smoothed parametric enumeration in general.

A final targeted search combined “sandwich inequality/theorem”,
“shattered sets”, “isolation lemma”, “bounded density”, “expected number”,
and “near-optimal solutions”. It found no directly matching published
near-optimal-count statement or this sandwich application. The newly
opened primary sources were Kozma--Moran and Lawler; unrelated hits were
not treated as evidence. This limited negative result leaves priority
unresolved. The proof is a short synthesis of established tools, so an
equivalent statement under different terminology remains a material
possibility. The substantive, reviewable claim is the stated theorem and
its assumptions, rather than an assertion that its ingredients or general
research approach are new.
