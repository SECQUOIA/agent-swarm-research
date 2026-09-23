# Stage 2, round 1 — reviewer 4

**Verdict: revise before closing stage 2.** The timing experiment and conditional research program are scientifically credible. One major, localized design gap prevents the proposed steam-compatibility conclusion: the program lacks an operating steam control without added CO2 protection or restoration. This does not invalidate the equal-dose timing contrast.

## Major issue — essential correction

**1. A null after CO2 treatment cannot establish compatibility of the modeled steam substitution.** `manuscript/sections/02-cyclic-oxides.tex:4`, lines 57–61, 66–82, 92–94, and 118.

The motivating process substitution is steam in place of Ar. Both wet arms in Table 2 receive added CO2, either during or after steam, and every arm then receives the common carbonation/oxidation reset before its functional assay. Experiment 2 again compares protection, delayed restoration, and dry Ar. Thus the program measures steam exposure under two CO2-management policies; it never directly measures the steam substitution without either policy. Equal wet and Ar outputs after these treatments could mean benign steam, complete CO2-mediated repair, or protection afforded by both schedules. Those outcomes lead to different operating decisions.

The first-segment sister specimens help locate changes during steam but do not fill this gap: they are specified as material-state endpoints, whereas the stated compatibility and policy conclusions depend on persistent cycle output. Nor does applying the same reset to every arm remove the issue. The reset is itself a treatment that can conceal the need for recovery.

**Evidence:** Brody's original PDF pp.4–6 documents Ar purging and O2 regeneration in the experiment, with steam introduced in the model. It does not include the proposed CO2 reset. Chacko's original PDF pp.110–117 independently shows that CO2-containing regeneration participates in coating/carrier chemistry. The chapter correctly recognizes that coupling; it must also account for its effect on the compatibility inference. [Brody primary source](https://doi.org/10.1021/acs.energyfuels.2c01293), [Chacko dissertation](https://repository.lib.ncsu.edu/items/f251e28c-eff7-48f8-89a5-4d2ed038155c).

**Remedy:** retain the existing factorial timing experiment and its common-reset assay. Add a bounded operating comparison of the chosen steam purge against Ar under the ordinary cycle, without supplementary CO2 management, with function measured before any special restorative treatment. Follow a matched specimen/block with the qualified reset to distinguish tolerance from recoverability. Include this untreated steam policy in Experiment 2 when claiming that protection is unnecessary or worthwhile. If the authors prefer not to add this comparison, narrow the contribution and all null conclusions explicitly to compatibility under the tested CO2 policies; the modeled steam-only substitution remains untested. This is a missing comparison, not a demand that steam damage already be demonstrated.

## Minor issue — essential correction

**2. Separate a predictive state indicator from a causal determinant.** `manuscript/sections/02-cyclic-oxides.tex:114–116`.

The proposed withheld alternating history, independent aged specimens, and comparisons with carrier-state-only and cycle-count models are strong. However, a single-valued Li-inventory/output relation that predicts a new history establishes predictive sufficiency over the tested range, not that Li inventory determines function. Li retention may covary with unmeasured coverage, salt composition, or carrier/interface evolution. The chapter itself identifies those competing explanations at lines 34 and 41.

**Remedy:** change “identify which measured state determines persistent function” to a claim about predicting function or identifying a useful state indicator. Reserve causal dominance for additional discriminating evidence. The replenishment operation at line 94 could contribute such evidence if the measurements establish what it changed, but it should not automatically be treated as a selective Li-inventory intervention. No expanded mechanism campaign is required to support a useful predictive rule.

## Optional clarification

At `manuscript/sections/02-cyclic-oxides.tex:78–82`, explicitly include residual O2 in the washout qualification, alongside CO2. The common reset contains O2, and residual gaseous oxidant could influence the initial ethane pulse independently of selective carrier-oxygen delivery. O2 is already monitored, so this is a small clarification of the functional assay rather than a new measurement program.

## Scientific coherence, originality, and expansion judgment

The chemical equations are balanced and the activity/fugacity interpretation is correct. The manuscript does not transfer equilibrium direction into an unsupported five-minute reaction rate or a LiOH-volatility claim. It correctly distinguishes Li export, redistribution, reversible coating chemistry, and carrier changes. Its interpretation of the common reset is appropriately conditional on process-compatible treatment and independent species/state checks.

Originality is specific and potentially consequential. Carbonate stabilization by CO2, incomplete delayed recovery, and carbonate/LSF regeneration are established. The proposed advance is a tested operating consequence for the lower-loading coating, followed by a prospective prediction of recoverability and useful output. Experiments 2 and 3 clearly extend beyond a diagnostic: they charge recovery time and gas/heat burden, test a competing replenishment policy conditionally, and require prediction to change an operating decision.

The stop rules are generally sound. Failure to resolve a consequential effect does not justify an expanded materials campaign, and an effective protection treatment can still fail the complete-cycle value test. Full recovery closes a claim of persistent protection after that reset, although recovery cost can remain an operating question. The benign-steam branch needs the untreated comparator described above. None of the unmeasured proposed effect sizes, reset times, or assay limits is independently fatal.

## Evidence checked

Reviewed the chapter, `manuscript/evidence/stage2-cyclic.md`, and the selected bibliography. Checked Brody's cycle sequence, steam-model substitution, product definition, and Table 1 directly from the original PDF; checked Chacko's formulation, cycling, and coupled regeneration discussion directly from PDF pp.110–117. Checked Gao's 0.42 wt% oxygen result and CO2-inhibition discussion against the original XML. Fereres' extracted primary text supports the limited prevention/incomplete-recovery precedent. The current Barckholtz publisher text confirms the mixed Li/Na formulation, hours per condition, and lack of calibrated absolute Raman concentrations; it supports the chapter's restrained use of that study. [Barckholtz primary source](https://doi.org/10.3389/fenrg.2021.669761).

Independent arithmetic reproduces the 2.019-minute illustrative recovery headroom and 2.042 mol CO2 circulation per mol ethane calculation. These are correctly labeled as illustrations rather than predicted steam performance. No chapter, bibliography, or knowledge-base files were changed.
