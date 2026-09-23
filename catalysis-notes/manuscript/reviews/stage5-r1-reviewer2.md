# Stage 5, round 1 — independent reviewer 2

**Verdict: approve with one minor clarification. No major issue identified.**

The overview accurately represents the four developed chapters and their current causal comparisons. It presents the ranking as a manuscript-development and feasibility judgment, not an experimentally established ranking of opportunities or a commitment to run four campaigns. The explicit dependence on reactor access, reproducibility, uncertainty, and costs is appropriate. The distinction between published results, calculations, and proposed measurements is preserved.

The six shortlist entries are reasonably brief. They identify specific missing decisions without pretending to provide six additional developed programs. The tungsten entry correctly remains a hold because an actionable intervention is missing; the Ti-zeolite and Ga entries require predictive value beyond refitting existing kinetics or correcting an assay; the zirconia entry connects chemical accounting to useful product-containing operation; the CHA entry distinguishes function before terminal titration from capacity after it; and the methane entry makes a material-choice application boundary an entry condition.

## Minor finding

**Identify the two Pd/SSZ-13 treatment variants in the methane comparison.** Location: `manuscript/sections/05-shortlist.tex:19`; corresponding evidence summary: `manuscript/evidence/stage5-portfolio.md:47–50`.

The text asks whether “the relative sulfur-tolerance advantage of the reported Pd/SSZ-13 material” survives removing NO, but does not say which Pd/SSZ-13 material has the advantage or which material supplies the comparison. This is substantive enough to clarify even in a brief entry because the source includes multiple Pd/SSZ-13 preparation histories with sharply different sulfur responses.

Ryu's original PDF p.9 and Fig. 6m compare the steam/CO/N2/O2-treated material, labeled ST-CO-N2-O2, against ST-CO-O2. The former retains the reported high methane conversion during the sulfur interval, whereas the latter loses substantial activity. Both share the Pd/SSZ-13 name. Naming only that support/formulation therefore fails to identify the preparation decision being retested without NO.

**Remedy:** state that the crossed NO/sulfur comparison applies to both ST-CO-N2-O2 and ST-CO-O2, briefly explaining that the former includes the extra N2 treatment. For example: “Test whether the sulfur-tolerance advantage of the extra-N2-treated Pd/SSZ-13 material over its ST-CO-O2 counterpart survives NO removal…”. Keep the existing water, sulfur-history, temperature, inventory, and application constraints. This requires a short wording change, not a new full experimental program or a broader material screen. Source: [Ryu et al., Nature Communications](https://doi.org/10.1038/s41467-024-52698-4).

## Integration and causal assessment

- `00-introduction.tex:24` correctly describes late PDVB addition, ordinary steam-versus-Ar cycling before analytical reset, crossed polymer pressure/makeup doses, and untreated/sham/Ni silver comparisons with ordinary and recovery policies. These agree with the reviewed final chapters.
- The overview's proposed predictive standard does not imply that local water exposure, Li escape, selective polymer initiation loss, or Ag–Re oxygen transfer has already been identified. Its finite-null and qualified-characterization language is consistent with the chapters' limits.
- The tungsten leachate comparison does not credit the full mixed-system glycol yield to exported W. The mannose statement also preserves the distinction between a productive feed and proof of a direct cleavage route.
- The Ti-zeolite entry requires liquid-system component qualification before transferring a network prediction. It does not treat a vapor-fed model or a residual as a unique mechanism.
- The zirconia pilot names relevant styrene/hydrogen burdens and includes assay perturbation and oxygen-exchange controls before isotope attribution. These are the material causal boundaries for a brief entry; a full isotope protocol is not needed here.
- The CHA proposal includes uninterrupted aging and a thermal/water sham, then measures function before the potentially restorative terminal assay. That comparison addresses the missing assay-history question without inferring intermediate lifetimes from a null.
- The Ga entry correctly treats oxygen/CO2 subtraction as an incomplete redox balance, while making a useful regeneration decision depend on complete-cycle output and a withheld spent history. It does not claim that correcting the balance invalidates all published performance.
- `main.tex` includes the overview, four developed chapters, shortlist, and bibliography directly. The overview and shortlist references point to existing section labels; no causal inconsistency was found in the integration.

## Evidence and review limits

Read the full overview, shortlist, integration file, stage 5 evidence note, and added bibliography entries. Consulted the Ryu local full text and directly extracted original PDF pp.8–9; inspected Class-Martínez's original experimental pages for repeated assay histories; and consulted the Wu and Artsiusheuski primary full-text descriptions of oxygen accounting and proposed water scavenging. The Ryu publisher page could not be retrieved through the web tool, so the retained original supplied the substantive evidence. Earlier reviewed chapters supplied the integration comparison. No other reviewer report was read, and no manuscript chapter or literature file was edited.

No experimental success is needed to justify the overview or these conditional shortlist positions. Beyond naming the methane treatment pair, the brief proposals identify meaningful missing tests at the intended level of detail.
