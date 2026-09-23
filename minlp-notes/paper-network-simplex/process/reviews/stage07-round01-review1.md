# Stage 7, round 1 — independent review 1

Verdict: accept Stage 7. I found no valid major or minor issue in the assigned changes or their integration with the accepted manuscript.

## Findings and scope

1. **S07R01-R1-F00 — no outstanding finding.** The new integral-flow statement is correct, including its decomposition-count limitation. The abstract, introduction, scope table and conclusion accurately summarize the actual results and computational evidence. No correction is requested.

I read the complete Stage 7 source diff and frozen snapshot additions, the affected accepted sections, the author record, completed coverage map, README and historical pointers. I checked the stated contributions against their theorem statements and supporting scope qualifications, not merely against the author's account. I did not read another current-round review or coordinate conclusions with reviewers.

## Integral-flow corollary

The new `cor:integral-flows` in `sections/01-foundations.tex` has a valid self-contained proof. At a nonintegral feasible flow, any nonintegral arc is strictly between its integer bounds. A vertex incident with exactly one nonintegral non-loop arc cannot have integral balance. Therefore, if the fractional support has no loop, every incident vertex has degree at least two and the finite undirected multigraph contains a cycle. Parallel arcs can form a two-edge cycle. Arbitrary orientations only change the signs of its circulation. A sufficiently small perturbation in both circulation directions preserves all bounds and balances, so the point is not a vertex. A fractional loop gives the same conclusion directly through its zero incidence column. Zero capacities cause no problem because such arcs cannot belong to the fractional support.

Boundedness then gives integral-vertex decompositions of all feasible flows. Refining each positive-weight normalized state flow preserves every observed product because products at a fixed simplex vertex are linear in x. The mixture coefficients remain nonnegative and sum to one. Zero-weight states need no normalized flow or refinement, and the proof explicitly handles an empty flow polytope. A zero-edge feasible system likewise presents no exception.

The adjacent paragraph correctly limits the at-most-m+1 decomposition statement to continuous graph points. A fractional feasible flow on two parallel unit-capacity arcs with total flow one gives the stated m=0 counterexample to an integral one-point representation. The corollary does not imply integrality of fractional coordinate sections. This distinction is also preserved in the README.

My independent exact check, `verification/stage07-review1/integrality-check.py`, does not import the author's new verifier or a production oracle. It examines fractional grid flows on five directed multigraphs, including loops, parallel arcs, disconnected vertices and zero capacities. For every tested flow having integral balances and a nonempty fractional support, it computes a rational kernel direction supported there and checks a strict two-sided feasible perturbation. It checked **282 flows and 22 distinct fractional supports**. It also exactly verified **three refined state decompositions** with zero states and sparse observations, and the m=0 integral-count counterexample. These finite checks support the proof steps; they are not used as a proof of the general corollary.

## Claims, scope and exposition

I checked the introduction's residual-coordinate count against `thm:observed-compression` and its completion claim against `prop:minimum-completion`. The text appropriately limits the count to the supplied construction and the completion minimum to individual products on the ambient circulation space. It does not claim an extension-complexity optimum or a lower bound on a degenerate capacity slice.

The bounded-rank summary preserves both operation bounds, the observation-grouping proviso, rational arithmetic, compact rather than dense output, and the distinction between separation and recovery. The scope table states the flow/product coefficient convention and does not silently impose the same bound after clearing simplex denominators. Its structural locators match the relevant statements.

The fixed-label summary matches the reduced profile theorem and observed-label corollary: local checks and bound grouping precede the five tests; three labels use the 16 circuits and balance repairs; the unit-coefficient guarantee is limited to the specified flat chain; four labels admit a counterexample. The growing-label Fibonacci family and unrestricted-network two-label obstruction support the conclusion about treewidth and label count separately. The manuscript does not infer a negative result for bounded labels on every nested series–parallel graph, nor infer difficult separation or large extension complexity from coefficient magnitudes.

The new computational summaries use the accepted strengthened baseline evidence: 7,215 full/global variables, 495 initial variables and 367 after elimination in the all-labels-observed control, with roughly 30 versus 10 milliseconds for full/global versus initial compression. The text retains the less favorable runtime results and synthetic/shared-host limitations. The revised reproduction paragraph preserves the material fact that optimization and membership records were collected separately. The component-hull/intersection qualification remains explicit.

The diagram is mathematically consistent with G4: four forward parallel pairs and one forward bypass, all capacities and total source–sink flow one. Its state-flow equations and caption agree with the preceding definition. I visually checked the private PDF's first page, structural table and diagram; the figure is readable and appears after the graph definition.

## Attribution and source consistency

The added Fiorini comparison is accurate: the primary author manuscript explicitly transfers facets of 0/1 polytopes to acyclic-subgraph facets, while the current paper describes a different coordinate-section transfer. I checked the [author PDF](https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf) and [publisher metadata](https://www.sciencedirect.com/science/article/pii/S1572528606000168), including year, volume, pages and DOI.

The [Hoffman–Kruskal primary reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/kruskalhoffman.pdf) supports the classical integrality attribution and identifies the original 1956 chapter and pages 223–246. The manuscript also supplies its own network proof, so no hidden citation hypothesis is needed.

I checked Khademnia–Davarnia Section 4.2 in the repository's primary-paper full text. Its service-conflict transportation model supports the new attribution as motivation for the explicitly stated two-supplier/common-simplex specialization. The manuscript does not claim to solve that source's unrestricted conflict model.

The coverage map now provides manuscript locators for the retained developments and limitations. The README distinguishes current results, exact certificates, numerical evidence and historical records. The added historical-note pointers preserve their old content while marking the superseded conclusions.

## Verification and limits

I verified all **88 dependency hashes** in `verification/stage07-validation.json`. A private snapshot build completed with **48 pages**, no LaTeX warnings, unresolved references, overfull boxes or underfull boxes. My independent evidence and private build are in `verification/stage07-review1/`.

This review checks the full assigned Stage 7 and its dependencies. It does not replace the separately required whole-manuscript round, repeat every accepted numerical experiment, or assert exhaustive literature priority. I found no newly exposed error in the accepted results needed by the new exposition.
