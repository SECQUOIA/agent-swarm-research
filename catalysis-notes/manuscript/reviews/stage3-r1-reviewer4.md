# Stage 3, round 1 — reviewer 4

**Verdict: approve with minor revisions.** The chapter defines a coherent, consequential operating question and a credible route beyond diagnosis. I find no major scientific defect. Two localized clarifications are needed to distinguish a pressure-enabled material saving from ordinary dose optimization and to make the longer-run comparison executable.

## Major findings

None. Failure to observe a beneficial pressure response, establish carbon attribution, or qualify chain-state measurements would close the stated branches; their present absence does not invalidate a proposal.

## Minor findings — essential corrections

**1. Require evidence that the pressure change enables the reduced dose, rather than merely discovering a lower adequate dose.** `manuscript/sections/03-polymer.tex:97–99`, read with lines 4 and 81.

The dose brackets at both pressures and the best-tested comparator are useful. However, a successful withheld dose at lower ethylene, compared with a larger *tested* dose at the reference pressure, does not necessarily show that the reference pressure needs the extra material. The same withheld dose might also satisfy the output, specification, and time requirements at the reference pressure. In that case, part or all of the apparent saving would be ordinary dose optimization. The early no-makeup pressure response establishes an operating response at that inventory; it does not automatically establish the minimum adequate makeup at the validation inventory.

**Remedy:** specify that the pressure-substitution claim requires uncertainty-qualified separation of the adequate-dose regions. If the existing dose brackets already establish that distinction under a justified monotonic response, they may suffice. Otherwise test the selected withheld dose at both pressure conditions with matched histories and acceptance criteria. This is one targeted comparison, not a pressure or dose library. If both pass, report a lower-dose policy and any independently measured pressure benefit, without claiming that pressure was necessary for that dose saving. A global optimum is unnecessary.

**Evidence basis:** the chapter itself limits three tested doses to a bracket at line 63. The published full supplement is a demonstrated rescue schedule, not a demonstrated minimum dose; Conk's original Fig. 4B contains no smaller-dose comparison. [Conk primary source](https://doi.org/10.1126/science.adq7316).

**2. Define what happens at the first intervention threshold in the extension.** `manuscript/sections/03-polymer.tex:101`.

The extension currently says to stop when output requires intervention, compare cumulative demand at a common accepted-output target, and reject a sustained advantage if earlier W replacement or extra regeneration erases it. These are different endpoints unless the post-threshold action is specified. An earlier-stopping arm may never reach the common output target, and a first-threshold experiment does not measure the cost of the replacement or regeneration that would follow.

**Remedy:** freeze a simple continuation rule with the extension: specify the allowed makeup/replacement action at the output trigger and count it until both policies reach the same accepted-output target, or explicitly end the extension at first intervention and report a bounded service-interval saving. Full-mixture replacement is an acceptable conservative action if selective W replacement or regeneration is unqualified. No speculative regeneration development is required. Keep a maximum duration/charge bound so an arm that cannot meet the common target is reported as failing that comparison rather than extrapolated.

This concerns the definition of the sustained-policy test. It does not weaken a properly measured three-charge inventory saving.

## Scientific coherence and originality

The proposed contribution has practical substance. Na/alumina demand, W/silica demand, and accepted polymer-carbon productivity are defined separately, with the correct published once-only supplement as a comparator. Charging all fresh solids and complete elapsed time avoids an apparent gain created by ignoring support mass, recovery delays, or reduced final-charge output. Polymer-carbon attribution also addresses the real possibility that increased gross propylene partly reflects additional ethylene-derived carbon.

The isotope mixing equation is sound under its stated two-reservoir and fractionation assumptions. Constant ethylene enrichment across conditioning and reuse, removal/requalification of the methane standard, retained-carbon accounting, and calibrated atom fractions are substantive safeguards. The chapter does not confuse source attribution with identification of the PE charge that supplied a product molecule. These measurements are demanding, but the proposal supplies an explicit limit on the claim if they fail.

The operating intervention is appropriately modest. The sealed-to-semibatch qualification prevents a reactor-mode change from being interpreted as pressure-mediated rescue. Fixed total pressure and flow, inert replacement, common charge-1 history, fresh controls, and complete-charge output support an operational comparison. They do not isolate an intrinsic reaction order, and the text does not pretend otherwise. Lower ethylene can inhibit metathesis, initiation, swelling, or access; the negative branch is credible rather than treated as an inconvenient outcome.

The chapter fairly credits earlier pressure studies, population models, fresh-Na rescue, and regeneration disclosures. Selective initiation loss is neither assumed nor needed for the operating result. Conditional feed-state and component-probe experiments preserve the distinction between rescue and identification of a single failing function. Quench qualification is particularly important because the cited earlier tandem system continued isomerization and recombination during recovery.

Experiment 3 is a genuine predictive step: an independently tested, withheld dose must satisfy an output lower bound, product specification, complete time, and attributed material demand. It is a bounded operating prediction rather than a new mechanistic model. That is a legitimate contribution if the saving is consequential. The stronger state-based prediction in line 103 remains a conditional scientific extension; I do not require an expanded campaign to make the initial operating result useful.

## Evidence checked

Read the full chapter, `manuscript/evidence/stage3-polymer.md`, and its selected bibliography entries. Checked Conk's original PDF pp.4–5 for the precise three-charge supplementation schedule, labeling interpretation, and simultaneous pressure/flow changes. Checked the original SI at S16–S18 for semibatch gas delivery, 12-minute sampling, and the explicit gauge-pressure example. These support the chapter's cautious treatment of the source benchmark.

Read the relevant Chen final-paper primary text for finite isomerization kinetics, its physical regime, ethylene inhibition, and omitted gradients/deactivation. Checked Wang's original PDF pp.78–79, printed pp.73–74, for recovery-induced isomerization/recombination and the confounded pressure comparison. The manuscript's restrictions are justified.

Checked the public patent text for the oxidative/DME sequence and the Na–Fe formulation named in Fig. 21. Its identity and treatment caveats are correctly retained; I did not verify a numerical regeneration efficacy. [Primary patent disclosure](https://patents.google.com/patent/WO2026011187A2/en). The eScholarship page again presented a browser check, so I did not access the embargoed dissertation body or independently verify its full protocol.

The inventory arithmetic and two-source mixing equation are internally correct. No peer reports were consulted, and only this review file was written.
