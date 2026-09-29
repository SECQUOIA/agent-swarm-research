# Publication disposition of the supporting investigations

Reviewed 25 September 2026. This assessment covers the supporting September 25
work, not the main penalty, three-variable cut, or indicator-star hierarchy
packages. It closes the supporting investigations at their proved scope;
the open questions listed below are not assertions awaiting a missing proof.

The supporting results are ready to be used with the qualifications below.
They are not collectively a set of new standalone papers. Several are
classical consequences, explicit examples of known obstructions, or records
of approaches that did not settle their motivating question. Preserving that
distinction is part of publication readiness.

## Disposition

| Investigation | Accepted content | Recommended use |
|---|---|---|
| Common-denominator graph hull | Exact finite rational SOC formulation, completed zero-throughput face, degree-two optimizer, fixed-row size bound | Credited formulation lemma or appendix; do not present the classical edge reduction as new |
| Signed low-rank indicator quadratics | Fixed-rank matroid algorithm and near-diagonal positive-rank-one weak hardness | Modest supporting propositions; no substantial standalone novelty claim |
| Local continuous moment gluing | Exact three-variable local inconsistency and careful comparison with dense SDP | Motivating example and negative archive |
| Continuous five-variable star | Explicit rational SDP–RLT gap derived from Drury's copositive example | Reproducible counterexample or benchmark; not a new copositive/SPN obstruction |
| Four-variable continuous star | Binary-center exactness and one-sided sufficient conditions | Supporting lemmas; the unrestricted four-variable question remains open here |
| Component elimination and treewidth | False maximum-width bound, valid product bound, and growing-width family | Source-specific correction with versioned attribution |
| Bounded faces of indicator-star epigraphs | Objective-dependent cube decomposition and quadratic-size LP lifts for every bounded face | Supporting structural lemma that rules out a proposed proof route |

## Common-denominator graph hull

The [proof and formulation](pooling-hull-review.md) are complete under the
stated compact-polytope assumptions. In particular, the proof includes the
full zero-throughput face, constant-throughput edges, degenerate polytopes,
and zero disjunct weights. The conic formulation is rational and exact.
The degree-two optimizer and fixed-number-of-noncoordinate-rows consequences
follow from the displayed elementary arguments.

The [literature audit](pooling-hull-literature.md) identifies the main
mechanism in Cambini–Martein's 2009 Theorem 8.3.1. Simultaneous retention of
several ratios follows by scalarizing their common denominator. Tawarmalani's
2010 inclusion-certificate framework is another direct precedent. The
publication-readiness source refresh checked the latter primary manuscript;
the open book URL again failed to load, so the earlier successful full-book
inspection remains the evidence for its precise theorem and page attribution.

There is no identified proof blocker. A standalone originality claim is not
supported. An abstract-only 2026 common-variable bilinear lead remains
unresolved, but this does not prevent using the result as a credited
consequence. Arbitrarily many capacities destroy the fixed-row guarantee;
arbitrary mixed flow/ratio side constraints and several independent
denominators are outside the theorem. No general pooling algorithm or
polynomial-size formulation for arbitrary input polytopes follows.

## Signed low-rank indicator quadratics

The [two propositions](integer-structure-exploration.md) have complete
proofs and prior independent reviews. The readiness audit rechecked the
variational identity, matroid greedy selection, lower-dimensional arrangement
faces, extraneous lifted samples, and exact recovery of a candidate optimum.
The positive-update construction uses a vanishing exact gap, so its
well-conditioning statement does not imply approximation hardness.

The closest primary comparisons were reopened: [Gao–Li's author
manuscript](https://optimization-online.org/wp-content/uploads/2010/09/2721.pdf)
already gives the fixed-eigenvalue arrangement mechanism and a closely
related binary-enforcing sum-of-squares reduction; [Del Pia–Dey–Weismantel](https://www2.isye.gatech.edu/~sdey30/SubsetSparse.pdf)
gives a related support-enumeration algorithm with low-dimensional shared
coupling. The matroid and individual-cost extension may be a useful modest
addition, but the present record does not clear its priority as a standalone
result.

The former inline arithmetic checks are now reproducible in
[check_integer_structure.py](check_integer_structure.py). They verify both
the rank-one identities and the pseudopolynomial dynamic program, and test
the greedy implication for independent-set and basis constraints. They do
not implement the arrangement enumeration. The result is polynomial for
each fixed rank, not a fixed-parameter algorithm with rank-independent
exponent. Neither general knapsack activation nor an arbitrary linear
optimization oracle is covered. No known proof gap blocks use of the
stated propositions as supporting material.

## Continuous quadratic stars and local moments

The [fresh independent review](publication-continuous-star-review.md)
accepts the mathematics and exact certificates in
[disjunctive-exploration.md](disjunctive-exploration.md),
[star-hull-proof-exploration.md](star-hull-proof-exploration.md), and
[four-star-analytic.md](four-star-analytic.md).

The three-variable path example separates exact edge hulls from a common
global distribution. It is detected by dense PSD plus nonedge McCormick
constraints and must not be used as a dense-SDP counterexample. Exactness
for forests on at most three vertices is a corollary of the current
Burer–Natarajan–Willemsen theorem. The four-variable-path finite-linear-cut
obstruction belongs to Zhang–Wang; it is a prior result being applied,
not an original result of this batch.

The five-variable star has a self-contained proof of minimum zero and a
strictly feasible rational SDP–RLT point of value `-9337/250000`. The
underlying matrix is Drury's published book-graph example, and the general
copositive-to-box transfer is close to a direct specialization of
Qiu–Yıldırım. The useful artifact is the explicit star translation and its
exact verification. No broad claim of first discovery or new SPN theory
is supported.

The four-variable analytic note proves two restricted statements: a binary
center moment face is exact in every star dimension, and a one-sided
three-leaf domain is exact by the corrected `T_5` SPN theorem. It also gives
a sufficient box condition under which releasing leaf bounds preserves the
minimum. These proofs are complete. They do not settle fully bounded
four-variable stars with a positive-curvature center and leaves whose
unconstrained responses cross both bounds. Numerical searches in that case
are discovery records only. No exactness or impossibility claim depends on
their failure to find an example.

These materials need no further mathematical work to serve their stated
supporting roles. Solving the unrestricted four-variable question or proving
a new scalable strengthening would be additional research, not preparation
required to publish the accepted restricted results.

## Component elimination and treewidth

The [mathematical note](treewidth-elimination-review.md) and
[new independent review](publication-treewidth-review.md) establish the
counterexample and repaired bound. The graph-theoretic repair is classical;
the useful contribution is detecting a false assumption in the specified
optimization arguments and replacing it safely.

A substantive source-version correction was necessary. The April 2026
Lehigh report used the false bound in Theorem 1. The [August 19 revision](https://arxiv.org/html/2604.25033v2)
instead assumes residual torso treewidth directly in Theorem 1; the same
false Lemmas 3–4 are now used in Corollary 1. The reviewer and coordinator
independently checked that distinction. The February SDP preprint still
contains the original faulty graph argument.

The counterexample disproves the graph bound and the specified implication
between width assumptions. It does not establish that the optimization
classes have no polynomial algorithm or small extended formulation. The
padded family proves large assignment tables for the indicated decomposition
method, not arbitrary extension-complexity lower bounds. Those restrictions
must accompany any public correction. The higher-degree part of the August
preprint has not been fully audited here.

The correction is complete at this scope. No author communication has been
sent. Source versions should be checked again immediately before submitting
a correction, because the attribution is version dependent.

## Bounded faces of indicator-star epigraphs

The [face-decomposition note](../notes/research-20260925-star-epigraph-faces.md)
and its [independent review](../notes/review-20260925-star-epigraph-faces.md)
contain complete proofs. The readiness audit reread the closure argument,
the finite number of minimizing center values, tied-indicator cube images,
and the containment of every bounded face in a positive-epigraph-weight
exposed face. No gap was found.

This is a useful safeguard against transferring a hard inverse-matrix
polytope through a bounded face of the original epigraph hull. It supplies
neither a compact formulation nor an impossibility theorem for the full
hull. The formulations depend on the exposing objective. Unbounded faces
and arbitrary affine sections are not covered. Existing polynomial-time
optimization on trees already supplies the broader algorithmic result;
the added observation concerns face structure. Use it as a supporting
lemma without claiming cleared standalone priority.

## Verification performed in this readiness pass

The coordinator ran:

```text
python research-20260925/check_integer_structure.py
python code/check_star_epigraph_faces.py
```

The first passed 852 positive-update instances, 11,820 exact support checks,
and 1,400 exact principal-system solves across 40 signed rank-two partition-
matroid instances with both activation variants. A fresh reviewer also read
and ran this checker and confirmed its limited verification scope. The
second passed 77 cases and 3,232 exact support checks.

Independent reviewers ran:

```text
python research-20260925/check_star_counterexample.py
python research-20260925/check_star_independent_review.py
python research-20260925/verify_disjunctive_review.py
python research-20260925/check_treewidth_elimination.py
```

All passed. Their review files record the particular rational witnesses,
matrix conditions, graph sizes, and source comparisons checked. Exact finite
checks establish the tested identities and certificates; the universal
statements rest on the written proofs. No project-wide verification, CI
inspection, or new Lean formalization was performed for this supporting
assessment.

A targeted standard-library check also passed for trailing whitespace,
final newlines, and all 32 local Markdown links in the seven files changed
or added by this supporting audit. The tracked-file `git diff --check` was
also clean; the explicit file check is the relevant one for untracked files.
