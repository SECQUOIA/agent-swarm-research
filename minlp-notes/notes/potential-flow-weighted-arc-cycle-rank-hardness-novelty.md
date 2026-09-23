# Two-arc flow objective at rank two: bounded source assessment

Date: 2026-09-05. Candidate:
[weighted arc cycle-rank hardness](potential-flow-weighted-arc-cycle-rank-hardness.md).
This is a source assessment, not the requested independent proof audit.

No matching primary-source theorem was located for a fixed linear objective
of two arc flows, common quadratic passive laws, fixed small nominations,
independent two-point positive resistances, and global cycle rank two. The
candidate is plausibly useful as an objective-dependent complexity boundary.
General circuit-extrema hardness, uncertain resistor models, and series-path
Subset Sum encodings are established antecedents and should not be presented
as new ideas.

## Exact contribution being compared

The candidate uses the fixed objective `F=-9 x_02+5 x_23` on one theta core.
Its physical performance curve has a strict interior maximum at a rational
effective cross resistance. A subdivided cross path encodes a subset sum in
that effective resistance. The proposed NP-completeness statement combines
this construction with the repository's fixed-rank exact algebraic verifier.
No claim that physical states have rational certificates is needed or made.

The complementary rank-one observation is elementary once the single-arc
algorithm is available: a fixed-nomination unicyclic network has one
circulation coordinate, so every linear arc-flow objective is affine in that
coordinate. Rank two allows an objective to prefer a joint flow state that
does not maximize either coordinate separately. This distinction is why the
proposed theorem is compatible with the repository's positive single-arc
results on series-parallel graphs.

Relative to existing local results, this adds an intermediate boundary:
weighted potential objectives already admit hardness on a single cycle;
one designated arc has the reviewed rank-three hardness construction; a
weighted objective supported on two arcs now has a rank-two construction.
The two-arc claim concerns **global** cycle rank. It does not establish exact
polynomial optimization of sums over arbitrarily many separate unicyclic
blocks; exact addition of unrelated algebraic optima needs separate care.

## Primary-source comparisons

**Older general circuit uncertainty hardness.** Lawrence P. Huang and
Randal E. Bryant, *Intractability in Linear Switch-Level Simulation* (1993),
has a primary institutional abstract reporting NP-completeness for extremal
steady-state voltages in general linear switch-level MOS networks. The
abstract was reopened in this audit; the full proof remains unread. It does
not specify the present two-current objective or common quadratic
fixed-rank model. It prevents a broad claim of first hardness for uncertain
resistive-network performance.
[IBM primary abstract](https://research.ibm.com/publications/intractability-in-linear-switch-level-simulation).

**Series-parallel linear tolerance geometry.** Randal E. Bryant, J. D. Tygar,
and Lawrence P. Huang, *Geometric Characterization of Series-Parallel
Variable Resistor Networks* (1994), DOI 10.1109/81.331520, treats uncertain
linear circuits through geometric descriptions of their equivalents. The
previous full-text assessment and exact locators are retained in the
[series-parallel source audit](potential-flow-series-parallel-envelope-novelty.md).
The author PDF had been read in that audit; reopening it in this pass
returned an internal retrieval error. Its inspected results do not give the
present nonlinear, two-arc, rank-two theorem.
[Author manuscript](https://people.eecs.berkeley.edu/~tygar/papers/Geometric_characterization_of_series-parallel/Bryant_Journal_preprint.pdf).

Our comparison: a theorem computing each individual component's range does
not generally compute extrema of a linear combination, because the component
extrema may occur in different scenarios. Likewise, two-terminal equivalent
circuit geometry is not automatically a description of every chosen pair
of internal currents. A claimed implication would need the actual joint
attainable set and its complexity, not just individual bounds.

**Nonlinear tolerance envelopes.** Stefano Pastore, *DC tolerance analysis
of electronic circuits by polyhedral circuits*, DOI 10.1002/cta.2098,
develops methods using strips of nonlinear characteristics. Its bibliography
confirms Hasler and Wang, *Parameter tolerances in non-linear resistive
circuits: worst case analysis based on monotonicity*, NOLTA 1993, pp.841–846.
The full Pastore manuscript was inspected in earlier audits; a fresh exact
title search again did not locate the Hasler–Wang text. The latter remains
an unresolved primary-source gap, especially for positive monotonicity and
envelope identities. Neither its title nor its citation establishes a
fixed-rank complexity result for weighted currents.
[Open Pastore manuscript](https://arts.units.it/retrieve/e2913fde-d2e2-f688-e053-3705fe0a67e0/2869823_10.1002-cta.2098-PostPrint.pdf).

**Uncertain gas-flow and discrete sizing models.** Aßmann, Liers, Stingl,
and Vera, *Deciding Robust (In-)Feasibility Using Set Containment: An
Application to Uncertain Gas Networks*, explicitly studies fixed nominations
and positive interval pressure-loss factors in Section 4.1.4. That source
establishes the uncertain-resistance model; the inspected sections did not
contain the present two-point weighted-current reduction.
[Primary preprint](https://arxiv.org/pdf/1808.10241).
The separate [discrete-resistance audit](potential-flow-discrete-resistance-hardness-novelty.md)
records older tree pipe-sizing hardness and its primary sources. A design
cost objective constrained by pressure feasibility is different from the
present unconstrained worst-case physical-state objective. Neither the word
“discrete” nor tree-sizing hardness gives this rank boundary directly.

Classical confluence and series-parallel network structure, with verified
Duffin and Eppstein sources, are recorded in the linked series-parallel
audit. They underpin the positive single-arc side. They do not assert that
all weighted arc objectives share the same extremal resistance scenario.

## Numerical and complexity scope

The base reduction's fixed-small-nomination gap has polynomial **binary
length**, which need not be inverse-polynomial in input length. It supports
the proposed obstruction to polynomial dependence on precision bits.

The candidate correctly uses a different homogeneity for absolute-error-one
hardness: multiplying all nominations by `N` multiplies every quadratic-law
flow by `N` and potentials by `N^2`, with resistances fixed. Its choice
`N=16H^2` turns `Delta=1/(4H^2)` into a gap of at least four. The coefficients
`(-9,5)` remain fixed, but the nominations cease to be fixed small constants.
This scaling has polynomial bit length and concerns unnormalized inputs.

In contrast, common resistance scaling leaves all flows unchanged and
therefore cannot amplify this objective gap. That scaling only clears
resistance denominators here. The potential-objective scaling discussion in
older local notes must not be transferred to arc objectives. No strong
NP-hardness, relative approximation lower bound, or normalized-data
constant-error lower bound follows from these arguments.

Recommended priority wording: “For common quadratic passive laws, a fixed
linear objective supported on two arc flows has an exact finite-resistance
complexity boundary between global cycle ranks one and two. The hardness
construction uses fixed small nominations and a theta subdivision; its
continuous interval counterpart is tractable at fixed global rank. We did
not locate an equivalent restricted theorem in the primary sources checked.”
Use this only after the separate mathematical audits pass.

The bounded search combined weighted or linear combinations of currents,
worst-case resistor tolerance, NP-completeness, nonlinear passive flows,
discrete resistance, cycle rank, and the exact Hasler–Wang title. Most new
results were unrelated circuit design or sensitivity studies. They are not
used as evidence. This assessment reuses explicitly identified prior full
reads and does not certify exhaustive novelty.
