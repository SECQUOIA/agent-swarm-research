# Stage 7, round 1 — independent reviewer 3

**Verdict: no major or minor issues identified.** The new abstract, introduction,
scope table and conclusion accurately describe the accepted results and their
limits. The integral-flow corollary and its proof are correct. The added
literature comparisons and modeling attribution are supported by the inspected
primary sources. The integration is ready for the separate whole-manuscript
review required by the process.

I reviewed the complete frozen Stage 7 at
`process/snapshots/stage07-round01`, comparing it with `stage06-accepted` and
the supplied `verification/stage07/source.diff`. I also reviewed the coverage
map, README, historical-note pointers, relevant original topic notes, the new
verification scripts, and the 88-hash manifest. No other current-round report
was consulted, no findings were coordinated, and no shared manuscript, code or
data was edited. My evidence is under `verification/stage07-review3/`.

## Findings

1. **Major findings: none.**
2. **Minor findings: none.**

There is no requested correction from this review. The checks and limits below
state what this verdict covers.

## New integral-flow corollary

The corollary in `sections/01-foundations.tex`, `cor:integral-flows`, is a correct
consequence of integrality of a bounded equality-flow polytope and the existing
simplex-vertex disaggregation.

The direct vertex argument covers the permitted multigraphs. Consider the
subgraph of nonintegral arcs of a feasible flow with integral balance and
capacity data. If it has a nonintegral loop, that loop itself gives a feasible
perturbation direction. Otherwise, a vertex incident to exactly one fractional
arc would have a nonintegral balance, so every incident vertex has degree at
least two. A finite nonempty such multigraph contains an undirected cycle,
including the two-edge cycle formed by parallel arcs. Its signed circulation
is nonzero and has zero incidence balance regardless of the original arc
orientations. All involved values lie strictly between integral bounds;
sufficiently small perturbations in both signs are feasible. Thus a
nonintegral feasible flow cannot be a vertex.

Boundedness then gives integral-vertex decompositions of every normalized
positive-weight state flow. Pairing each refined flow with its original simplex
vertex preserves all selected products because those products are linear in
the flow at a fixed simplex vertex. The refined weights sum to the old state
weight. Summing over states preserves x, y and z. The reverse containment is
immediate, and the explicit empty-domain qualification is correct.

The following paragraph correctly prevents two possible overinterpretations:
the at-most-`m+1` continuous graph-point representation need not survive
refinement into integral flows, and fractional coordinate sections need not
be integral. The `m=0` example is a valid minimal demonstration of the first
limitation. This qualification is consistent with both the compact recovery
results and the universality section's fractional sections of 0/1 hulls.
The corollary is presented as classical, not as a new integrality theorem.

### Independent exact check

I wrote a separate cycle-rounding verifier, importing neither the author check
nor a repository oracle. It finds a signed cycle in the fractional support and
splits a rational flow in both directions at the nearest integer values. Each
child has fewer fractional arcs, so recursive splitting terminates in integral
feasible flows. The verifier checks exact balances, bounds, weights and
reconstruction throughout; it then refines disaggregated states and verifies
all original coordinates and sparse products.

It passed on **48 generated multigraphs**, with **432 rational state flows**,
**1,188 fractional-cycle splits**, and **144 complete integral graph-point
refinements**. Three additional explicit cases exercise parallel arcs,
oppositely directed arcs, and a loop. Zero capacities and zero state weights
occur in the generated cases. These finite checks support the proof; the
signed-cycle argument is the general justification.

Evidence: `check_integral_rounding.py`, `integral-rounding.json`.

## Abstract, introduction, scope table and conclusion

I checked each new contribution statement against its main theorem and the
accepted Stage 6 text.

- The residual-coordinate count is explicitly the count of the supplied
  observation-sensitive construction, not minimum extension complexity.
  The individual-product completion statement is qualified by reconstruction
  on the ambient circulation space. The forest-complement conclusion and unit
  coefficient statement match the TU elimination result.
- The bounded-block-rank separation and recovery costs are correctly separated
  as `2^{O(r^2)} N` and `2^{O(r^3)} N`, with the stated observation-grouping
  proviso. The existing theorem includes finite-library construction and the
  compact-output qualification. The introduction does not equate rational
  arithmetic counts with bit complexity or promise a practical general-rank
  implementation.
- The coefficient bound refers to the defined `H_r`; `H_3=2` and the five-product,
  two-explicit-label, unit-capacity K4 example agree with the accepted sharp
  example. The scope-table caption clearly restricts unit/bounded coefficients
  to flow and product coordinates in the stated rational row scaling. It does
  not include data-dependent simplex coefficients or subsequent denominator
  clearing in that unit guarantee.
- The flat-chain claim uses the number of labels observed anywhere, rather
  than the original simplex dimension or a local count that might vary by
  gadget. The exact unit coefficient guarantee through three labels and its
  four-label counterexample are correctly restricted to the canonical directed
  unit-data chain with one bypass. The five-vertex, nine-arc count is correct.
  The five tests and 16 circuits are stated after local checks and grouping.
  No extension to arbitrary nested series–parallel networks is inferred.
- The Fibonacci statement concerns growing label count, sparse observations
  and the simple maximum-degree-three realization. The general two-label
  universality result is explicitly on unrestricted graphs. The coordinate
  section retains the two relevant products, so it is not an unsupported
  transfer through projection. Unit network data in that result means the
  normalized original model; rational constants defining the section are
  separate, as the main proof explains.
- The conclusions distinguish coefficient ratios/magnitudes from coefficient
  bit lengths, separation difficulty and extension complexity. The negative
  coefficient results therefore do not contradict the polynomial extended
  formulation or the structural separation algorithms.
- Equality balances, arbitrary orientations in general graph results,
  transformation-dependent graph assumptions, and the narrower canonical
  flat-chain scope are all stated. Adding outer constraints is consistently
  described as intersecting the exact component hull to obtain a relaxation,
  not automatically convexifying the complete coupled nonlinear model.

The introductory practical comparison reproduces the accepted all-labels
control: full/global models have 7,215 state-flow variables, initial compression
has 495 total variables, and observed elimination has 367. The rounded medians
of about 30 and 10 milliseconds are correct. The text retains the stronger
global-merger baseline, cases where simple LPs are faster, the fact that the
smallest formulation can be slower, and the exact-certificate versus numerical
feasibility distinction. No new runtime advantage is inferred from an
unmeasured implementation or an industrial application.

## Primary-source checks

**Fiorini.** I inspected the open author manuscript of
[How to recycle your facets](https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf),
including its abstract and the introductory description of the facet-transfer
procedure, and checked published metadata against the
[publisher record](https://www.sciencedirect.com/science/article/pii/S1572528606000168).
The new statement that arbitrary 0/1 facet inequalities can be transferred to
acyclic-subgraph facets is supported. The comparison properly distinguishes
this earlier graph-polytope construction from preserving selected bilinear
coordinates in sections of the present continuous-domain hull. It does not
claim that facet transfer or large coefficients are new general phenomena.
The title, author, journal, year, volume, issue, pages and DOI agree.

**Hoffman–Kruskal.** The linked
[open reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/kruskalhoffman.pdf)
contains the authors' introduction explicitly describing integral vertices from
integer right-hand sides and total unimodularity. Its publication notice
identifies the original 1956 chapter, editors, publisher and pages 223–246.
The manuscript's historical attribution and original-chapter bibliography are
appropriate. The URL is a later reprint containing the original chapter; no
misleading original-page locator is used in the manuscript.

**Khademnia–Davarnia.** The web reader did not expose usable text from the NSF
copy on this call, so I downloaded the same openly available
[published primary PDF](https://par.nsf.gov/servlets/purl/10546393) to my private
evidence directory and inspected its extracted Section 4.2. It indeed concerns
transportation on a complete bipartite network, route-specific bilinear service
costs, and conflicts between service choices. The new manuscript sentence
identifies its two-supplier/common-simplex model as a motivated specialization,
not as the source paper's exact original model or benchmark dataset. That
wording is accurate. The existing explanation of common balances/capacities
and synthetic experiments remains intact.

I also read the repository's relevant literature audit and retained source
boundary notes. Their cautions about known disaggregation, RRLT,
transportation/Cayley projection, fan refinement, aggregate versus commodity
flow integrality, and restricted coefficient realizations are carried into
the manuscript. The new framing does not turn the absence of a located prior
statement into a certified claim of priority.

## Repository coverage and presentation

The coverage map supplies manuscript locators for the retained developments:
block and path suppression, homothetic local-state merging, observed-rank
elimination, minimum individual-coordinate completion, cycle/theta formulas,
parallel-path cuts, bounded-rank libraries and recovery, sharp K4 examples,
universality, balanced/Fibonacci and degree-three constructions, shared-profile
failure, reduced flat-chain circuits, exact code, compressed code, and the
strengthened experiments. I cross-checked the main source notes and the
mapped result statements; no material topic development omitted from this
stage was identified.

The older readiness and continuation records now clearly direct readers to
the manuscript before presenting their preserved historical conclusions.
This is appropriate for their old 41-circuit counts, larger K4 example,
earlier timings and superseded default-method assessment. Keeping those
records is useful provenance; the new README does not present them as current
results. Adjacent common-factor investigations outside the network–simplex
scope need not be imported into this manuscript.

The new graph figure correctly has five vertices, eight serial pair arcs and
one bypass, all oriented from source toward sink. Its common state-profile
identity and bypass remainder match the preceding equations. I inspected the
rendered figure page and structural-scope table page; labels, arrows, equations
and locators are legible and consistent.

## Reproduction and integration checks actually performed

- Recomputed **all 88 Stage 7 hashes**; all matched.
- Compared **42 code dependencies** with the accepted Stage 6 manifest;
  all are unchanged.
- Verified the four unchanged main proof files against `stage06-accepted` and
  examined all other substantive edits through the source diff.
- Independently traversed **17 LaTeX inputs**, checked **193 unique labels**,
  **124 referenced labels**, and **44 coverage locators**.
- Regenerated the five computational tables in a private copy. They are
  byte-identical to both the Stage 7 snapshot and the accepted Stage 6 tables.
- Checked the new introductory variable counts and rounded timings directly
  against the raw accepted benchmark JSON.
- Performed the independent exact cycle-rounding/refinement checks described
  above.
- Built a private copy with `latexmk -pdf -interaction=nonstopmode
  -halt-on-error main.tex`: **48 pages**, with no warnings, undefined references,
  overfull or underfull boxes. Inspected rendered pages 3 and 30 containing
  the new scope table and graph diagram.

Evidence includes `check_integration.py`, `integration-checks.json`, private
`build/`, `build.log`, `build-text.txt`, `scope-page.png`, and `diagram-page.png`.

## Limits and final disposition

This stage review is not a fresh proof audit of every unchanged earlier
section or a substitute for the required whole-manuscript round. I checked
the new theorem fully, the changed exposition against its theorem statements,
relevant source literature, repository coverage and the unchanged accepted
experimental evidence. I did not rerun unchanged numerical benchmarks or
assert new timing significance. Primary-source access was sufficient for the
new claims; the NSF web-reader limitation was resolved by reading its actual
open published PDF.

Finite checks do not establish priority or replace mathematical arguments.
The integral-flow result is explicitly classical, and the larger contribution
claims remain appropriately confined to the sparse structural realizations
and algorithms developed here.

**Disposition: accept Stage 7 from this review, with no requested revisions;
proceed to the separately required whole-manuscript review after root
adjudication of all five reports.**
