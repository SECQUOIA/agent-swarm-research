# Independent full-manuscript review, round 1 — reviewer 4

**Verdict: accept with minor revisions.** The manuscript supplies four complete proposed experimental research programs and six proportionately brief reserve ideas. I found no major scientific or design defect that requires reopening a program. The remaining changes concern the accuracy of the overview and making the experimental sequence easier to follow.

This verdict concerns a research-program manuscript, not completed experimental evidence. The text consistently attributes published results, labels its calculations, and presents new experiments prospectively. It does not imply that the proposed late-PDVB intervention, steam compatibility, pressure-enabled catalyst saving, or Ni-dependent operating advantage has been demonstrated.

## Overall scientific assessment

The four chapters have coherent arguments linking an important limitation, close prior work, a distinct unresolved question, a controlled intervention, a useful output measure, and a prospective decision. They do substantially more than prescribe additional characterization. Their strongest common feature is requiring a measurement to change a material or operating choice, while allowing a precise negative result to close the tested branch.

- **Water:** The distinction between equilibrium water loading, exchange rate, source strength, and local exposure is clear. The two-pool counterexample properly limits inference from outlet data without denying the published formulation effect. Common conditioning, matched handling, the challenge-by-additive comparison, and absolute integrated output make the late-addition experiment interpretable. The later reversible-pulse prediction is a separate, credible operating study. Its scope should remain distinct from predicting protection against lasting damage.
- **Cyclic oxides:** The ordinary steam-versus-Ar comparison directly addresses the gap between a measured Ar-purged experiment and a proposed steam duty. Pre-reset performance, recovery after a terminal reset, and the steam-dependent timing contrast answer different questions, and the chapter correctly preserves those differences. Inventories, carryover qualification, and complete-cycle time prevent an apparently better material state from being mistaken for better operation. The conditional alternating-history prediction supplies a substantive extension beyond familiar carbonate stabilization.
- **Polymer:** Carbon-origin accounting gives the fresh-catalyst-demand objective a defensible denominator. The sealed-batch/semibatch distinction, pressure-by-makeup design, independent validation at both pressures, and bounded replacement extension address realistic ways an apparent saving could disappear. The proposed result need not establish selective initiation loss to matter. The comparison also allows the simpler result that less makeup suffices at either pressure.
- **Silver:** The chapter recognizes unusually close historical Ni-retention prior art. Untreated, sham, and Ni materials, followed by ordinary and recovery policies, make the proposed additional contribution specific. Absolute output ranking and the preparation-cost boundary keep a large recovery increment from being confused with the best catalyst policy. The calibrated chlorine baseline is an appropriate hurdle for an additional mechanism claim.

The first-to-fourth ordering is defensible as an editorial and feasibility priority: a large published water-management effect and a specific steam-process gap motivate the first two programs, while closer intervention prior art raises the contribution threshold for polymer and Ag. The manuscript appropriately avoids claiming that this ordering is an established cost or laboratory-readiness ranking. The reserves have sufficient scope for their intended role; they do not need six more full experimental programs.

## Major findings

None. In particular, absent measurements, unknown pilot variance, conditional instrument access, and unverified positive outcomes are openly stated dependencies of proposals. They are not defects that can be repaired by adding invented parameter values or requiring successful experiments before accepting this document.

## Minor findings

### 1. Make the water overview distinguish the protection test from the predictive branch

**Location:** `sections/00-introduction.tex:14`; compare `sections/01-water.tex:101–107`.

The overview summarizes the first program as “Predict when a separately mixed hydrophobic material protects useful Fischer–Tropsch output.” A reader could reasonably understand this as a prediction of damage protection across histories. The chapter instead tests protection at one defined state and disturbance, then conditionally predicts a nearby reversible pulse's output deficit. It explicitly says that the latter does not validate a damage law at higher exposure.

**Remedy:** Change the table entry to distinguish these two deliverables, for example: “Test whether late PDVB addition protects useful output under one water challenge, then conditionally predict output during a reversible humidity pulse.” Keep the chapter's existing limitations. No additional damage-model campaign is needed.

### 2. Give the cyclic-oxide chapter a compact map of its three experimental sequences

**Location:** `sections/02-cyclic-oxides.tex:43–48`, `:80–86`, and `:98–124`.

All the necessary distinctions are present, but readers must assemble them across several pages: ordinary cycling is measured before a terminal reset; the five-arm timing diagnostic uses a different exposure schedule and a common reset; usable policies have their own treatment cadence and are ranked on output before the final analytical reset. Because these boundaries determine what “compatibility,” “recovery,” and “protection” mean, a compact visual or short sequence table would materially improve understanding.

**Remedy:** Add a small map identifying, for each sequence, its exposure, whether/when a special reset occurs, and its primary endpoint. It should summarize the existing design without adding arms or duplicating the analytical qualifications. This is a presentation improvement; the prose already contains the correct design.

### 3. Clarify what “strongest reserve” means for an already selected main program

**Location:** `sections/00-introduction.tex:22`; compare `sections/05-shortlist.tex:4`.

Calling cyclic oxides the “strongest reserve” immediately after selecting it as the second main program creates a small terminology conflict with the six reserve ideas. The intended distinction appears to be the next campaign to launch after the water feasibility test, rather than inclusion in the brief shortlist.

**Remedy:** Use “second feasibility priority” or “next launch choice” for cyclic oxides, or specify explicitly that it is the reserve for experimental launch. No reranking or numerical scoring system is necessary.

## Verification and limits

I read the overview, all four program chapters, and the entire shortlist, and checked the manuscript entry point and supporting evidence notes. I did not read previous or peer review reports, communicate with peer reviewers, modify the literature library, or edit the manuscript.

I read targeted passages in the local Fang 2026 and Brody 2022 primary-source extractions to check the principal published platform descriptions. These checks agreed with the distinctions retained in the manuscript. I reran `evidence/check_water_output.py`: the reference and promoted integrals were 116.0352 and 219.8266 feed-carbon hours, with ratios 1.89448 and 1.80427 after charging the additional polymer mass. Those results support the rounded secondary calculation, not its experimental uncertainty or a lifetime forecast.

The retained PDF has 34 pages. Text extraction showed no unresolved `??` references, and all 42 citation keys used in the section sources have bibliography entries. This was not a fresh LaTeX build or a page-by-page visual typesetting inspection. I did not independently re-audit every publication, supplement, bibliographic field, or evidence-note assertion, and I did not undertake an exhaustive novelty search. No experiments, equipment qualification, cost validation, or confirmation of proposed mechanisms was performed.
