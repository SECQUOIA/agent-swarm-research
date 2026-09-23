# Stage 5, round 1 — reviewer 4

**Verdict: approve, with one minor wording clarification.** The overview, six reserves, withdrawn claims, and integration form a coherent portfolio. No major scientific or prioritization defect requires restructuring.

## Major findings

None.

## Minor finding

**Define the tungsten control when introducing its numerical comparison.** `manuscript/sections/05-shortlist.tex:7`.

“Ni/M” is a source-specific material label that is not defined elsewhere in the manuscript. Its role matters: the baseline is the supported-Ni control without intentionally added W, rather than a generic Ni/W catalyst. Readers should not need to retrieve the source to understand why the 27.1% baseline changes the interpretation of the 29.5% result.

**Remedy:** introduce it as “the W-free supported-Ni control (Ni/M)” or briefly identify the MIL-125(Ti)-derived support if that material detail is desired. Retain the original identifier so the comparison remains traceable. This requires only a short phrase, not a longer tungsten program.

**Evidence:** Li's original Table 1 reports 27.1% EG for Ni/M, while original SI Table S3 reports 29.5% for Ni/M plus the preleachate. The existing numerical interpretation is correct. [Li primary source](https://doi.org/10.1021/acssuschemeng.0c00836).

## Portfolio judgment

The four-program order is defensible as the stated scientific-development priority. Water combines a substantial reported formulation effect with an unresolved history-dependent functional question. Cyclic oxides address a specific experimental/process-model gap. Polymer provides a concrete fresh-material decision but with close pressure and rescue precedents. Ag has the strongest directly overlapping retention and operating-policy prior art, justifying its narrower position. These are qualitative priorities, not measured probabilities of success or economic rankings; `00-introduction.tex:22` makes that distinction and permits established laboratory platforms to change the first experiment.

The main-program summaries at lines 14–24 preserve the decisive comparisons in the completed chapters. They do not reintroduce the withdrawn mechanism claims or erase controls added during development. The text also distinguishes prioritizing four developed ideas from authorizing four simultaneous experimental campaigns. No claim of verified reactor access, measurement precision, practical savings, or competitive lifetime is implied.

The six reserves are appropriately bounded. Tungsten remains on hold because its proposed intervention is missing, despite its first position among ideas for reconsideration. The Ti-zeolite entry is a conditional liquid-system prediction, not an unqualified transfer of vapor-fed kinetics. Zirconia requires useful product-containing operation and a chemical balance. The zeolite-assay question separates pre-assay function from capacity measured after a common terminal treatment. Methane explicitly needs a relevant NO-poor sulfur duty, and Ga requires a regeneration decision beyond correcting an oxygen inventory. None warrants six additional full programs in this document.

The withdrawn-claims section correctly separates invalid inference from invalid topic. Faster water clearance, fresh-Na rescue, and historical Ni retention cannot support the original stronger claims. Hot mannose conversion contradicts treating mannose as an inert default feed reservoir, while the epimerization and inactive-fraction qualifications prevent overclaiming a uniquely identified cleavage pathway. The reserves retain specific conditions for reopening rather than disguising missing evidence as either success or final rejection.

## Evidence and integration checks

Read the new overview, shortlist, Stage 5 evidence note, main document, selected reference entries, and README. Used the four chapters and my earlier independent reviews as context; no peer reports were consulted.

Checked the tungsten baseline and preleachate values directly in the original main paper and SI. Checked the El Mohammad primary discussion of mannose conversion and the SI S7–S8 descriptions, which support retaining the route ambiguity. Checked Class-Martínez's original experimental section: repeated NH3-TPD/water/thermal sequences are indeed part of the aging protocol. Checked the Ryu primary text for NO present during the sulfur interval.

The Ga patent directly discloses reducing the lengthy post-regeneration oxygen treatment, so the shortlist correctly treats this intervention as prior art and seeks a further complete-cycle prediction. [Primary disclosure](https://patents.google.com/patent/US20220126281A1/en). These were targeted checks, not exhaustive new reviews of all six fields.

The mandatory section inputs include the overview, four programs, and shortlist in the intended order. README navigation and the main document agree. The existing build log contains no warning, undefined-reference, overfull, or underfull entries. I did not rebuild or modify the manuscript; only this review file was written.
