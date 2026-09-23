# Stage 3, round 1 — independent reviewer 2

**Verdict: revise one major design gate. The proposal is otherwise coherent and appropriately bounded.**

The chapter frames a meaningful catalyst-saving decision. It uses the correct once-only Na addition as the published comparator, separates catalyst-solid from elemental demand, attributes accepted product carbon to polymer rather than gross propylene, and includes handling and complete time. The semibatch qualification avoids transferring sealed-batch reuse behavior to a different reactor mode. The isotope-source history and atom-fraction calculation are substantially more defensible than assigning every product the fresh experiment's labeled-polymer fraction.

The controls are proportionate to the stated claims. Common conditioning before assignment, independent sequence replication, fresh mixtures at both ethylene conditions, a handling control, and a limited support/contact control support an operating comparison without claiming selective loss of initiation. Quench qualification and the caution about polymer access appropriately limit chain-state and small-molecule probe interpretations. A mechanistic campaign is not required before accepting a useful empirical operating rule.

The remaining problem is that the proposed first screening gate can reject the very partial catalyst substitution that the chapter is intended to test.

## Major finding

**M1. Do not require benefit without makeup before testing whether pressure can reduce the makeup requirement.** Locations: `manuscript/sections/03-polymer.tex:77`, `manuscript/sections/03-polymer.tex:81`, and `manuscript/sections/03-polymer.tex:83`; related prediction dependency at lines 97–99 and closure statement in `manuscript/evidence/stage3-polymer.md:41`.

The retained-mixture pressure comparison begins “initially without makeup.” Line 81 then makes the dose bracket conditional on a successful lower-ethylene result, while line 83 says a precise negative result closes the chosen pressure intervention. But pressure benefit at zero makeup is not a necessary condition for pressure to substitute for *part* of a fresh Na addition. Pressure and makeup can interact through exactly the tandem-function and contact effects discussed in the chapter. The source's rescue experiment establishes that makeup changes function, but does not establish an additive pressure response independent of makeup.

For a concrete counterexample, suppose normalized accepted polymer-carbon outputs under the time ceiling are:

| Makeup before charge 2 | Reference ethylene | Lower ethylene |
| --- | ---: | ---: |
| 0 g | 0.40 | 0.40 |
| 0.2 g | 0.80 | 1.00 |
| 0.4 g | 1.00 | 1.00 |

If the accepted-output requirement is 0.95, the proposed no-makeup screen gives an exact null and closes the branch. Yet the lower-ethylene midpoint policy meets the requirement while saving the chapter's stated 25% fresh Na/alumina and 16.7% total catalyst solids relative to the full supplement. These numbers illustrate a logically permissible response, not a prediction of the actual catalyst. The manuscript's mechanism cautions and cited molecular model do not rule it out.

This is major because the gate can prevent the decisive catalyst-saving comparison and makes its negative conclusion broader than the sampled dose supports. It does not mean the proposal needs another pressure, another material, or a positive result before review can be completed.

**Concrete remedy:** carry at least the preselected reduced makeup dose into the two-pressure comparison irrespective of the no-makeup result, alongside the full-dose reference policy and the already planned reference-pressure reduced-dose comparator. The cleanest implementation is to cross the existing finite 0/0.2/0.4 g bracket with the two already selected ethylene conditions on independently conditioned inventories, preserving the charge-1 history and once-only addition. The zero-makeup arm can remain an informative preliminary result, but its null may close only the no-makeup rescue claim. Close the broader tested catalyst-saving intervention only when the measured reduced-dose policies cannot meet the output, specification, time, and material-demand requirements within informative uncertainty. The existing withheld-dose prediction can then use the measured pressure-by-dose response without requiring an unsupported gate.

## Minor findings

None requiring a separate correction. The proposal already identifies analytical access, adequate isotope resolution, solid recovery, and semibatch reuse behavior as experimental qualifications. Those are legitimate dependencies rather than missing positive evidence. The extension to further PE charges is appropriately presented as necessary for a sustained policy claim, while three charges can establish a bounded inventory saving.

## Evidence checked and limits

- Followed the previously read `literature/AGENTS.md`; read no other reviewers' reports and made no chapter or library edits.
- Read the full stage 3 chapter, evidence note, and stage 3 bibliography entries.
- Directly extracted Conk 2024 original PDF p.4/Fig. 4B. It specifies one fresh 0.4 g Na/alumina addition before charge 2 and PE alone before charge 3, supporting the manuscript's comparator. Reviewed the local full text's component, isotope, reuse, and semibatch discussion. The reported semibatch pressure and flow changes do not identify a pressure effect at fixed makeup or establish pressure–makeup separability. Source: [Conk et al., Science](https://doi.org/10.1126/science.adq7316).
- Consulted the local Conk supporting information for gas analysis and semibatch setup. It confirms methane/FID analysis, gauge-pressure notation, and 12-minute sampling. Replacing methane with a carbon-free tracer requires the requalification already specified; the chapter does not assume an unchanged analytical method is sufficient.
- Reviewed the Chen 2024 local full text's model definition, concentration dependence, restricted physical regime, and conclusion. Its finite-isomerization model, ethylene gradients omission, and catalyst-specific interpretation are represented accurately. Its dependence on relative tandem catalyst amounts reinforces the need not to assume a pressure response is independent of makeup; it does not predict the numerical counterexample above. Source: [Chen et al., ACS Catalysis](https://doi.org/10.1021/acscatal.4c00465).
- Checked the isotope algebra and three-charge solid-demand arithmetic independently. Both are internally consistent under the stated assumptions. The chapter appropriately limits isotope allocation when additional carbon reservoirs or unbounded isotope discrimination are present.
- The dissertation and patent access limitations are candidly stated. This review does not claim to have accessed the embargoed dissertation body or independently established the efficacy of its regeneration procedures.

With M1 corrected, the initial program would directly test its intended partial catalyst-substitution claim while retaining its small pressure search and conditional mechanistic scope.
