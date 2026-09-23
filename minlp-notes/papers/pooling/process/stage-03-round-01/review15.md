# Stage 03, round 01 — independent review 15

Reviewed the complete frozen `sections/03-restricted-hardness.tex`, lines 1–1286. The working file agrees byte for byte with `process/snapshots/stage-03-round-01.tex`. Focus: global consistency, quantified restriction classes, feasibility versus threshold decision, certificates, and bit complexity. No manuscript edits or other current-round reports were consulted.

## Findings

### 1. Major: explicitly exclude additional lower quality specifications in the two initial NP-completeness statements

**Locations:** `s3:local-degrees`, lines 76–82, and `s3:all-two-thm`, lines 163–170; membership arguments at lines 116–117 and 249–251. Compare the endpoint certificate scope in section 1 immediately before `s1:endpoint-or` (lines 653–655).

Section 1's model permits lower and upper output quality specifications. These two theorem statements restrict the upper specifications to zero and one, but do not say that lower quality specifications are absent or redundant. The proofs construct the upper-only class and invoke a certificate whose stated hypothesis is that **no additional nonredundant quality restrictions** occur. The final claim at lines 249–251 that this proves membership for the “full stated zero-tolerance restriction class” therefore needs that restriction in the statement.

This distinction has mathematical content. A quality-zero input sending positive flow to an output with upper bound one and lower bound one-half satisfies the endpoint support disjunction but violates the lower specification. Thus the endpoint certificate cannot simply be applied to the larger class obtained by retaining the model's arbitrary lower quality bounds. The reduction establishes hardness for that larger class, but its NP membership does not follow from the argument given.

**Correction:** Add “upper output quality specifications only” to both theorem statements, or explicitly require every lower quality specification to be redundant for qualities in `[0,1]`. No reduction changes are needed. I classify this as a missing hypothesis for the stated NP-completeness/certificate scope, rather than a counterexample to the intended upper-only hardness results. If the author intends an earlier convention to supply this hypothesis, that convention needs to be stated explicitly: the present section 1 convention permits both kinds of specification.

### 2. Minor: preserve optional physical arc capacities in the weighted matching reduction

**Location:** `s3:weighted`, lines 255–256 and 270–274.

The proposition allows integer arc capacities. Its fixed-mode flow proof gives the replacement edge the pool capacity as its upper bound, without retaining the two constituent arc bounds. For example, a single pool and all external nodes may have capacity two, while the clean intake arc has capacity one. With rewards `alpha=1, beta=0`, the described clean-mode flow problem with edge bound two selects throughput two, which cannot be restored to that physical intake arc.

**Correction:** Set the mode edge bound to the minimum of the pool capacity, its intake-arc capacity, and its outlet-arc capacity, omitting an arc bound when it is not imposed. This minimum is integral, so the same network integrality proof establishes the proposition. This is a local omission in the proof, not a failure of the proposition.

### 3. Minor: name threshold decision in the same two theorem statements

**Location:** lines 76 and 163.

Both statements say that “pooling is strongly NP-complete,” whereas later statements consistently say “pooling threshold decision.” Their proofs use cost/profit thresholds, and their zero lower flow bounds make feasibility trivial. Section 1 carefully distinguishes these problems; the theorem statements should retain that distinction when read or cited independently.

**Correction:** Write “One-attribute pooling threshold decision is strongly NP-complete” in both places. This does not alter the intended result.

## Verified scope

I checked the occurrence-cycle SAT reduction, private triangles, subdivision direction, both orientation-to-pooling constructions, capacity omission arguments, and ordinary partition specializations. I checked the all-degree-two cleanup, matching integrality, conflict graph, constructive identity `alpha(H)=n/2+alpha(G)`, output merging, approximation loss, positive-tolerance loss estimates, and the `K4` fractional example. “Strict output” is used as a name for a restrictive upper specification; the displayed quality inequalities remain non-strict, as required.

I checked the explicit Matsui determinant bound, largest-fractional-index estimate, product identity, positive factors, yes/no separation, and polynomial coefficient lengths. The report's printed arbitrary-`p` estimate and the manuscript's counterexample agree with the cited original PDF: for `n=5,p=2`, the stated half-integral point has `X=31`, `Y=682`, and `Y-X^2=-279`, whereas the printed claimed bound is `-99/2`.

I checked the two-pool normalization and simplex embedding, row-attribute equivalence, tree topology, zero-throughput case, radial maximum, threshold-product equivalence, and the represented-family FPTAS. Its restriction to supplied representations is explicit, and its ordinary hardness does not conflict with its approximation scheme.

I checked full and half port equations, separate closed-cycle saturation, coupling, source splitting, row projection in both directions, the explicit polyhedral error bound, radial repair, objective repair, and the separate input-economics estimate. I checked binary multiplier bit order, denominator clearing, bounded partial sums, dyadic factor normalization, two actual feeds, the normalized quality alphabet, contract-completion objective, offset economics, and the five-exception transformations. The fixed-data proofs put the large source coefficients in polynomial-size circuit topology and retain only a linear-size threshold; their strong-hardness claims do not rely on a numerical approximation gap. The final feasibility proof physically implements its threshold row and permits the positive contracts it needs.

I compared the certificate invocations with `s2:pooling-np` and the accepted model conventions in sections 1–2. I consulted the relevant constant-data and five-exception source notes/results without treating their prior PASS labels as evidence. After reading `literature/AGENTS.md`, I checked the Chlebík–Chlebíková author-manuscript discussion on pp.25–26, including the original PDF's p.26 statement that the constructed graphs are edge-three-colored and three-regular and preserve the gap. I also checked the cited Matsui report and the relevant published Haugland 2016 discussion, Haugland–Hendrix p.607 bypass question, and Baltean-Lugojan–Misener Remark 4.6. The scope paragraph does not overclaim first general one-pool hardness.

## Limits and verdict

This is a mathematical review of the whole frozen stage, with selected original-source verification. I did not independently reproduce the PCP/amplifier source theorem, rerun every repository verification program, or conduct an exhaustive priority search. I found no counterexample to the intended upper-only reduction family or to the later constant-data/five-exception constructions.

**Verdict: major findings present**, because finding 1 leaves the NP membership of the literally stated initial restriction classes unsupported. The intended restriction is repaired by an explicit upper-only hypothesis. Findings 2 and 3 are minor.
