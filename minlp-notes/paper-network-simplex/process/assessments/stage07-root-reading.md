# Stage 7 — root integration checks

Stage6 is accepted. The sole author is preparing the final exposition; no
Stage7 source is accepted until its five independent reviews finish.

## Integral-flow consequence checked before drafting

For integral b,u, every vertex of the bounded flow polytope is integral:
incidence together with signed coordinate rows is totally unimodular. Thus
P=conv(P intersect Z^E). At a simplex vertex, each retained product is either
the corresponding flow or zero, so this affine map preserves the integral-flow
vertex decomposition. The known disaggregation then proves equality between
the original hull and the hull with integral flow required before taking the
convex hull. Empty P is immediate. This applies to arbitrary orientations,
loops and disconnected networks, not only acyclic unit-flow examples.

The existing at-most-m+1 decomposition consists of continuous graph points.
Requiring integral flow in every decomposition point may need more points:
m=0 and a fractional point of an integral interval already demonstrates this.
The final corollary must not transfer that cardinality bound.

## Main integration checks

- All claims of remaining coordinates refer to the stated construction or
  ambient individual-coordinate reconstruction, not extension complexity.
- Three observed labels suffice for unit flat-chain descriptions, with a
  four-label counterexample; arbitrary graphs already fail at two labels.
  Graph structure and observation structure are independent parameters.
- The Fibonacci family has sparse original encoding and large coefficient
  magnitudes, while coefficient bit lengths and generic hull optimization
  remain polynomially bounded in the usual sense.
- Final computational metrics come from the accepted fixed-weight controls.
  General global merging can win; local compression has a separate measured
  benefit on the all-labels-observed control. Exact certificates remain a
  distinct output from numerical LP feasibility.
- Literature attribution, section scope, zero states, fixed arcs and outer
  side-constraint limitations must survive shorthand in abstract and tables.
- Final prose describes methods and evidence; process files retain review
  chronology, rejected baseline interpretations, and source corrections.

## Initial draft reading

Read the new introduction, structural table, conclusion, graph figure source,
abstract, and complete integral-flow corollary. The corollary's direct signed-
cycle perturbation proof is correct, including loops, disconnected graphs and
capacity degeneracy; its decomposition-size qualification is correct. Fiorini
is accurately positioned as a predecessor, not an alternative proof of the
restricted selected-product construction. Hoffman–Kruskal bibliographic pages
and year were independently checked against the primary published chapter
listing and openly accessible reprint.

Two pre-freeze precision requests were sent to the author: restrict the intro's
blanket arbitrary-orientation statement to the relevant general/block results,
and remove an unsupported comparative 'much larger magnitude' phrase from
the conclusion. Both are local scope/exposition corrections. The remaining
count, coefficient-normalization and practical-summary statements are accurate.

Both requested precision changes are present in the current author draft.
I also read the complete computation section after the integration edits: it
retains native fixed-weight bounds, correct zero-state historical distinctions,
the all-labels-observed control, exact/numerical semantics, and the outer-budget
convexification limitation. The completed coverage map accounts for every listed
source family. Rendered scope-table, graph-diagram and bibliography pages are
legible with no clipped material. Author-rendered front-page images may precede
last wording edits; the final frozen source/PDF will control review.

## Frozen-stage checks

The author completed the stage before reviewers were dispatched. I froze
`stage07-round01` and independently verified all 20 snapshot hashes and all
88 source/evidence hashes in the author validation. I reran the author's exact
integral-hull check successfully (78 vertices and 54 refined mixtures); this
is reproduction, distinct from my proof review and the reviewers' new checks.
I read the current foundations and universality sections in full again, checking
the new integrality corollary against the coordinate-section claims and the
primary-source positioning. No integration error was found.
