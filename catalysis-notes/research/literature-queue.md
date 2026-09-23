# Identified-source registry and historical audit trail

Updated 2026-09-16. The [current literature status](literature-status.md) and [missing-material snapshot](reviews/post-upload-missing-sources.md) supersede the earlier request states below. Many formerly queued works now have retained, read primary texts. Do not resubmit the whole historical registry or interpret its old unread descriptions as current gaps.

## Current handling

The existing proposals incorporate the post-upload corrections. The sole reusable literature worker handles any remaining identified additions and source-note curation sequentially using the `lit` skill. No discovery campaign or new research direction is scheduled. Retained non-text artifacts are processing cases, while metadata-only records identify source-content gaps. Failed retrieval does not remove a relevant bibliographic entry.

Lundin2024 is now retrieved and read; the linked Shimura2026 SI remains a separately recorded missing source at the last completed intake. The [implementation record](implementation-report.md) gives final curation and review outcomes. The complete current acquisition list belongs in the snapshot rather than being reconstructed from the historical requests.

## Direction-search identified sources (2026-09-16)

The eleven-plus-two direction-search screens and their reviews cite several hundred sources not yet in the knowledge base, almost all at abstract or metadata level. The consolidated list, with the screens that cite each identifier and one knowledge-base correction, is in the [direction-search literature handoff](reviews/direction-search-literature-handoff.md). No direction was promoted, so ingestion is low priority; metadata-only records are sufficient unless a retained program cites the source.

## Historical requests before the upload correction

The entries below preserve identifiers, reasons for inclusion, temporary research artifacts and the sequence of earlier requests. Their access/reading language applies to the recorded stage only. Source articles, supporting files and preprints must still be distinguished when matching a particular citation.

## Recovered polymer primary benchmark

- [WO2026011187A2, Conversion of polyolefins](https://patents.google.com/patent/WO2026011187A2/en), Hartwig/Conk et al., published January 8, 2026. Authentic patent HTML retained at `/tmp/polymer-primary-gap/WO2026011187A2.html`; experimental methods and results read by root. Submitted to the sole literature worker, with original PDF/figures requested because the HTML omits figures and some equations. The [benchmark accounting](reviews/polymer-patent-benchmark-accounting.md) preserves reuse, contaminant-dose, waste-preparation and scale-up distinctions. This is a separate source; Science 2024 and its SI remain unresolved.

- Akin et al., [10.1016/j.jaap.2023.106036](https://doi.org/10.1016/j.jaap.2023.106036), *Chemical recycling of plastic waste to monomers: effect of catalyst contact time, acidity and pore size on olefin recovery in ex-situ catalytic pyrolysis of polyolefin waste*. [Official open accepted-manuscript record](https://biblio.ugent.be/publication/01H8KCCAZPFQH7N44KMQAYSF6A). Authentic accepted manuscript subsequently retrieved to `/tmp/polymer-primary-gap/akin2023.pdf`; methods and selected results read. Its [comparison limits](reviews/polymer-patent-benchmark-accounting.md#an-external-light-olefin-comparator-requires-a-different-comparison) preserve the catalyst-rich microreactor conditions, analytical closure and lack of a sustained-lifetime result. Submitted to the sole literature worker; SI remains to be assessed.

- The [new polymer value review](reviews/polymer-value-after-patent.md#literature-handoff-and-source-limits-at-the-original-review) requested van Schalkwyk et al., [10.1016/S0926-860X(03)00536-2](https://doi.org/10.1016/S0926-860X(03)00536-2), for reversible oxygenate inhibition/recovery on W at different conditions, and Maksasithorn et al., [10.1016/S1872-2067(12)60760-8](https://doi.org/10.1016/S1872-2067(12)60760-8), for composition-dependent Na/W modification. Both remain abstract/excerpt-level evidence in that review; full-text requests and links were routed to the sole literature worker.

- Related open dissertation: Surasa Maksasithorn (2014), *Metathesis of ethylene and 2-butene for propylene production using NaOH modified WO3/SiO2 catalysts*, [Chulalongkorn institutional record](https://digital.car.chula.ac.th/chulaetd/73676/). Abstract and access/license record inspected; full body not yet read by root. Requested separately as a source of full experimental details, not a substitute silently promoted as the journal article.

- Moodley et al., *Coke formation on WO3/SiO2 metathesis catalysts*, [10.1016/j.apcata.2006.10.053](https://doi.org/10.1016/j.apcata.2006.10.053). Root read exposed original methods/results on the [author-upload page](https://www.researchgate.net/publication/254787291_Coke_formation_on_WO3SiO2_metathesis_catalysts); the original PDF returned 403 and figures were not visually inspected. Relevant low-dose oxygenate/coke prior art: coke suppression does not by itself establish a productivity gain or transfer to Na/W polymer conversion. Sent to the sole worker.
- D. Lokhat, *Metathesis of 1-Hexene over a WO3/SiO2 Catalyst in a Gas Phase Fixed Bed Reactor*, reportedly a 2008 UKZN thesis; title-page metadata still to be verified. The [indexed institutional bitstream](https://researchspace.ukzn.ac.za/bitstreams/d2093ea9-a16f-4cae-9086-651199b8547a/download) redirected root to a login HTML page, despite HTTP200. Full text remains unread. Requested for supported-W reactor/exposure methods; the misleadingly named temporary `.pdf` is not an article artifact and must not be ingested.

The [recovered-polymer batch](../literature/runs/2026-09-15-polymer-recovered/run.md) now records completed patent-HTML and Akin-manuscript ingestion/reading. Patent original figures and Akin SI remain requested. The substantive carbon-origin and benchmark corrections to the patent note and topic are confirmed in the [status report](literature-status.md#source-corrections).

The [WO3 metathesis batch](../literature/runs/2026-09-16-wo3-metathesis/run.md) recovered the Lokhat thesis through its institutional API and added/read selected relevant sections. Root's earlier login response is superseded by that authentic recovery. Moodley remains centrally metadata-only/unread despite exposed primary passages read by researchers; the complete original artifact remains missing.

## Latest chlorine and methane-aromatization handoffs

- Artiglia et al., *Reaction Mechanism and Role of Chlorine in Ethylene Epoxidation Revealed by in situ XPS*, Research Square preprint, [10.21203/rs.3.rs-7141633/v1](https://doi.org/10.21203/rs.3.rs-7141633/v1), posted August 12, 2025. CC-BY original retained at `/tmp/ag-aging-prior-art/chlorine-xps-preprint.pdf`; [public PDF](https://assets-eu.researchsquare.com/files/rs-7141633/v1/2196fca9-c9ae-497f-9950-c318b2cddc48.pdf?c=1758026032). Root read main results and methods; SI remains requested. Retain preprint/version distinctions. Relevant defect-driven combustion and chlorine-induced structural alternatives; not evidence on Ni/Cs/Re retention.
- *From single crystals to working catalysts: integrating in-situ spectroscopy and computational modeling to bridge the pressure gap in ethylene epoxidation*, review, [10.1007/s44251-026-00147-3](https://doi.org/10.1007/s44251-026-00147-3). Bibliographic map for chlorine/titration/pressure questions. Only search excerpts inspected; secondary numerical summaries do not validate unread primary sources.
- The [MDA challenge's complete ten-source handoff](working/mda-consequential-uncertainty.md#complete-durable-source-request-record) preserves exact identifiers, retrieval leads and reading limits, including the unresolved identifier for the 2025 C1-intermediate paper and the long-duration periodic CH4/H2 paper. All requests were sent to the same sole literature agent; none is a completed-ingestion claim.

The [Ag chlorine/XPS batch](../literature/runs/2026-09-15-ag-chlorine-xps/run.md) subsequently added and read the Artiglia preprint and its original linked SI DOCX. The Qin review remains metadata-only and unread. The original SI figures are retained even though its plain-text conversion omits them; independent checking of the relevant graphical evidence is recorded separately.

## Wet methane combustion follow-up

The [complete methane-screen handoff](working/wet-methane-value-screen.md#historical-literature-handoff) preserves 19 newly identified primary/source requests and three historical kinetic/transport sources already queued by root. Four authentic original PDFs were supplied. The [independent-review handoff](reviews/wet-methane-independent-value.md#historical-literature-handoff-and-retained-artifacts) adds recovered Ryu SI, Figure 6 data and public review files, plus Sadokhina2017/2018 direct NO prior art. These artifacts were inspected and sent to the sole worker. The Auvinen NO/sulfate main article, Sadokhina full texts and several comparator methods remain unread. All requests went to the same sole literature worker; this is not a completed-processing claim. The proposed study concerns transfer of a strong wet sulfur result to low-NOx operation, while generic NO promotion and sulfur-storage strategies are already prior art.

The [first wet-methane batch](../literature/runs/2026-09-16-wet-methane/run.md) has now processed ten core candidates; the [status report](literature-status.md) records seven read text packages, retained unread workbook and all confirmed main/SI gaps. The larger source handoff remains queued.

Further methane primary recovery: [Seipel et al., CIMAC2025 paper178](https://doi.org/10.5281/zenodo.15191505), *Experimental Long-Term Study of a Methane Oxidation Catalyst on a Medium-Speed Dual-Fuel Engine*, original supplied at `/tmp/wet-methane-screen/cimac2025-178.pdf`. The actual operating comparison spans roughly 32 h, not validated service life. The [coupled-catalyst source check](reviews/wet-methane-coupled-catalyst-prior-art.md) preserves the recovered Nevalainen 2021 UEF thesis, its complete Auvinen 2021 Fuel appendix [10.1016/j.fuel.2021.120223](https://doi.org/10.1016/j.fuel.2021.120223), and the unresolved submitted Publication III. Both artifacts and their reading/version limits were sent to the sole worker. The cited CEJ NO-promotion article remains unretrieved in full.

The [application-boundary review](reviews/wet-methane-low-no-relevance.md#historical-literature-handoff-and-reading-limits) adds two recovered originals (Tomin2024 engine measurements and Villamaina2018 MOC/SCR ordering) and three direct sulfur/thermal-management precedents. All were sent to the sole worker; complete identifiers and reading limits remain in the review. The resulting priority downgrade is reflected in the decision brief.

## Carbonylation follow-up

The [complete carbonylation handoff](working/carbonylation-value-screen.md#source-record-and-access-update) preserves 19 main/patent requests, three additional current precedents, all supplied original artifacts and linked SI requests. Fan's dry H2-containing benchmark and Han's wet CO2 tandem route are distinct comparisons. Their numerical interpretation has now passed a [fresh independent review](reviews/carbonylation-benchmark-review.md), with corrected Fan GHSV transcription and qualified hydrogen-feed, Han mass-normalization and finite-stability claims. The review also supplied Han’s recovered source-data workbook to the same worker. The same sole worker received all additions; unread and unresolved versions remain in the handoff.

## Oligomerization follow-up

The [root source handoff](working/oligomerization-source-handoff.md) records cofeed kinetics, competing acid-site interpretations, bifunctional modeling, historical process evidence and a recovered mixed-feed fuel benchmark. The independent [opportunity screen](working/oligomerization-value-challenge.md) records additional current transport, operating-state and practical comparators. Requests from both went to the same sole literature agent. The [first twelve-source batch](../literature/runs/2026-09-15-oligomerization/run.md) is now complete: five read sources, including both dissertations, and seven unread main/SI packages. Additional current papers from the opportunity screen remain queued. The [benchmark audit](reviews/oligomerization-benchmark-accounting.md) preserves the distinction between high ethylene conversion, declining desired-product fraction and actual fuel properties. Only the named batch report establishes completed processing; other requests remain queued.

## Aging, recovery and Cu chemistry

| Identifier or source | Why it was requested |
|---|---|
| 10.1016/j.apcatb.2026.127245 | High-water Cu migration/stability prior art; metadata-only outcome recorded. |
| [AIChE 2025 contribution](https://proceedings.aiche.org/conferences/aiche-annual-meeting/2025/proceeding/paper/influences-al-density-and) | Closest CHA aging conference precedent; distinguish a complete abstract from a presumed missing full paper. |
| 10.1016/j.jcat.2026.116848, linked SI | Serial assay and recovery controls; SI now ingested/read. |
| 10.1039/C8RE00281A | Cu interparticle migration and support-transfer alternatives. |
| 10.1016/j.ces.2018.06.015 | Aging/NH3-TPD sequence dependence or contrary evidence. |
| 10.3390/catal15121130 | NH3 protection during steaming and aqueous recovery; lawful publisher PDF supplied. |
| 10.1016/0927-6513(94)00056-2 (verify identity) | Stockenhuber/Lercher acidity recovery without unique lattice reconnection. [Author-repository PDF](https://ris.utwente.nl/ws/files/6515540/Stockenhuber95characterization.pdf). |
| 10.1039/C9CY00624A | Collective action of water during dealumination. |
| [Dynamic evolution of H-ZSM-5 during steam, PDF](https://f.oaes.cc/xmlpdf/6107d319-be87-4dc6-8ef5-642c7c0df1ae/cs3055.pdf) | Resolve identity; dynamic Al evolution/recovery prior art. |
| 10.1021/jp001620p | Wouters: transient Al species and NH3-induced coordination changes. |
| 10.1021/ja907696h | Wet-cooldown Al migration as an intervention confounder. |
| 10.1039/D2QI00750A | CHA Al evolution; [author PDF](https://dmto.dicp.ac.cn/2022-9.pdf). |
| 10.1016/j.micromeso.2024.113007 | Oxygen exchange and hydrothermal interpretation. |
| 10.1021/acscatal.5b01496 | Contrary/alternative CHA dealumination kinetics. |
| 10.6100/IR302523 | Kraushaar 1989 thesis, NH3/recovery prior art; [full text](https://pure.tue.nl/ws/portalfiles/portal/1979092/302523.pdf). |
| 10.1039/C6RE00198J | 2017 aged Cu-zeolites change during subsequent SCR; generic testing-history novelty constraint. |
| 10.1016/0021-9517(91)90128-Q | NH4NaY hydrothermal kinetics, self-steaming and cation compensation. |
| 10.1021/jacs.6c11402 | Cooperative Cu/Brønsted-site SCR roles; newest directly relevant group prior art. |

## Polyolefin conversion

| Identifier or source | Why it was requested |
|---|---|
| 10.1038/s41467-025-57158-1 | External acidity/accessibility descriptor; now read. |
| 10.1002/cmtd.202500157 | Selective external H+ exchange; lawful repository promotion now read. |
| 10.1126/science.adq7316, including SI | Base-metal ethenolysis methods, inventories and impurity tests; article remains unread. |
| [Conk 2025 dissertation](https://escholarship.org/uc/item/7v07b7c8) | Initiation and DME regeneration prior art; body embargoed. |
| 10.1002/anie.202317526 | Consumer-grade Ru hydrogenolysis and nitrogen poisoning; repository promotion now read. |
| 10.1016/j.cattod.2025.115492 | Impurity poisoning of Ru; unread. |
| 10.1038/s41893-023-01147-z | Two-stage chlorine removal already established; now read. |
| 10.1038/s41467-026-77736-1 | PVC-derived chlorine and regeneration; full text unresolved. |
| 10.1016/j.apcatb.2022.121873 | 4A trapping of oxygenates already protects conversion catalysts. |
| 10.1021/jacs.2c07781 | Partner interaction and durability are prior art; supplied [ChemRxiv preprint](https://chemrxiv.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/6331eff7fee74e83a04b709d/original/chemical-recycling-of-polyethylene-by-tandem-catalytic-conversion-to-propylene.pdf). Preserve version distinction. |
| 10.1126/science.add1088 | Early tandem ethenolysis and isotope carbon accounting; [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11723507/). |
| 10.1002/cssc.202502353 | Recent polymer conversion comparator and prior art. |
| 10.1038/s44286-025-00290-y | Closed-loop plastic conversion/process comparator. |

## LOHC and oxide dehydrogenation

| Identifier or source | Why it was requested |
|---|---|
| WO2022132843A1 | Oxide DME activation/regeneration prior art. |
| J. Catal. 2025, PII S0021951725006402 | Toluene hydrogenation kinetics, ensemble and temperature effects; DOI to verify. [Public preprint](https://www.cambridge.org/engage/api-gateway/coe/assets/orp/resource/item/66d6c72312ff75c3a13ff115/original/toluene-hydrogenation-catalyzed-by-pt-nanoparticles-kinetically-relevant-steps-binding-ensembles-and-temperature-effects-on-turnover-rates.pdf). |
| 10.1021/acscatal.6c01477 | First-principles MCH dehydrogenation mechanisms. |
| 10.1016/j.jcat.2026.116959 | Support-dependent LOHC deactivation; close overlap. |
| 10.1016/j.apcata.2026.121061 | Support acidity and coke; close overlap. |
| 10.1038/s41467-024-55370-z | Pt–Fe/MFI lifetime benchmark; [repository PDF](https://ira.lib.polyu.edu.hk/bitstream/10397/113525/1/s41467-024-55370-z.pdf). |
| 10.1039/D6CY00183A | Sulfur/Pt model and poisoning prior art. |
| [Chiyoda TOCAT8](https://www.shokubai.org/tocat8/pdf/Plenary/PL9.pdf) and [current product page](https://www.chiyodacorp.com/en/service/lowcarbon/hydrogen/lohc-mch/) | Attributed industrial LOHC durability claims; distinguish promotional evidence. |
| 10.1039/D5CY00173K | Mechanochemical Pt/TiO2 performance comparator; [open copy](https://cris.vtt.fi/ws/files/118922639/D5CY00173K.pdf). |
| 10.1016/S1872-2067(25)64829-7 | MoOx/Pt performance/interface comparator. |
| 10.1016/j.fuel.2025.137649 | Pt particle-dependent performance comparator. |
| 10.7868/S3034554526020032 | Low-Pt loading comparator. |
| PII S2095927326005785 | Pt/TiOx interface comparator; identify DOI. |

## Styrene mechanism and process

| Identifier or source | Why it was requested |
|---|---|
| 10.1021/acscatal.5c04904.s001 | Focal SI, now ingested/read; ppm basis and X assumption. |
| WO2024177986A2 | Cleanup products and feed poisons already anticipated. |
| 10.1021/ie100023s | Luyben styrene process coupling of steam, conversion, recycle and reactor size. |
| 10.1021/acs.iecr.8b05560 | Dimian/Bildea heat integration and process benchmark. |
| 10.3390/catal15040308 | Industrial MacroCat report; full PDF supplied. Actual long-term S/O≈1.2 differs from abstract1.0. |
| [Clariant StyroMax](https://www.clariant.com/en/Business-Units/Catalysts/Petrochemical-and-Refining-Catalysts/Styrene-Catalysts/StyroMax-Catalyst-Portfolio) | Attributed low-steam commercial alternative. |
| 10.1021/acs.iecr.4c01175, including SI | Existing steam-free fixed-bed process and transport comparator. |
| 10.1039/F19848000895 | Rutile/propene oxygenate chemistry as a limited analogy, not proof of zirconia products. |

## Emissions challenge

| Identifier or source | Why it was requested |
|---|---|
| 10.1016/j.jcat.2025.116071 | High-water Cu SCR prior art; [full text](https://research.chalmers.se/publication/545758/file/545758_Fulltext.pdf). |
| 10.1007/s40825-024-00242-7 | Dynamic ammonia dosing already addresses water/feed changes. |
| 10.1007/s11244-025-02131-x | Ammonia-engine emission-control benchmark. |
| 10.1039/D0RA10177J | HCN removal versus storage; [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8695306/). |
| 10.1016/j.fuel.2025.137480 | Mn/Co HCHO/HCN cleanup prior art. |
| 10.1115/1.4069586 | Ammonia-engine operating benchmark. |
| 10.1038/s41598-025-28647-6 | N2O kinetics and product-accounting comparator. |
| 10.1021/acsanm.5c01442 | Pt/Rh ammonia oxidation prior art. |
| 10.1177/14680874261460191 | Ammonia/diesel emission-control comparator. |
| 10.1007/s11783-016-0872-8 | HCN hydrolysis prior art. |

## CO/CO2 practical challenge

| Identifier or source | Why it was requested |
|---|---|
| 10.1016/j.catcom.2021.106284 | Badoga isotope evidence qualifies direct-route claims; author-posted preproof supplied. |
| 10.1021/acscatal.1c05634 | Carbide carbon exchange confounds isotope intermediate lifetimes; [full text](https://pure.tue.nl/ws/portalfiles/portal/199708150/acscatal.1c05634.pdf). |
| [Shiyue Li 2025 thesis](https://pure.tue.nl/ws/portalfiles/portal/360421007/20250630_Li_S._hf.pdf) | Phase-pure carbide CO2-FT and carbon-pool isotope experiments already studied; local copy supplied. |
| 10.1021/jacsau.4c01097, including SI | NH3 inhibition/deactivation and mitigation already studied; [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11937992/). Methanol and hotter RWGS findings must remain distinct. |
| 10.1038/s41586-024-08078-5 | Phase-pure carbide α-olefin practical comparator. |
| 10.1016/j.jcat.2025.116030 | Carbon-deposit removal/regeneration prior art. |
| 10.1021/acs.langmuir.3c03902 | Integrated capture/hydrogenation with tertiary amines; contrary to blanket incompatibility. |
| 10.1016/j.jcat.2025.116384 | Polar additives and methanol durability prior art. |
| 10.1002/anie.202423281 | Zn working state at high conversion. |
| 10.1002/advs.202500118 | Supercritical-CO2 activation/working-state prior art. |

## Corrections to existing read notes

- Chen 2025: PA is propionic acid.
- Fischer 2023: 13CHD is positional 1,3-cyclohexadiene, not a 13C tracer.
- Martínez 2026: the assay counts recoverable framework-associated Al and is an intervention in the specimen history.
- Wang 2024, DOI10.1021/jacs.4c13212: paired-signal survival differs from individual paired-site survival; preserve random-loss interpretation.

These are verified or proposed research corrections supplied for the maintenance agent's own source check; completion must be recorded in its report.

## Thermochemical data for the styrene cleaning screen

- Taylor, Wagman, Williams, Pitzer and Rossini, *Heats, Equilibrium Constants, and Free Energies of Formation of the Alkylbenzenes*, J. Res. NBS 37 (1946), 95–122, RP1732. [Public full text](https://nvlpubs.nist.gov/nistpubs/jres/37/jresv37n2p95_A1b.pdf). Toluene gas entropy in Table 8; distinguish this old experimental evaluation from newer data.
- NIST Chemistry WebBook gas thermochemistry entries, [ethylbenzene example](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100414&Mask=1), plus IDs `C71432`, `C64175`, `C7732185`, `C1333740`, `C98862`, `C108883`, `C67561`. Formation enthalpies, entropies, Cp tables and Shomate coefficients for the explicitly balanced route calculations. Preserve selected evaluations rather than treating all entries as interchangeable.
- NIST CCCBDB experimental H/S entries, [benzene example](https://cccbdb.nist.gov/exp2x.asp?casno=71432&charge=0), also CAS digits `64175` and `67561`. These supply selected benzene/alcohol entropies and formation enthalpies.
- NIST Chemistry WebBook [styrene gas thermochemistry](https://webbook.nist.gov/cgi/cbook.cgi?ID=C100425&Mask=1), CAS 100-42-5. Added for the independent E → S + H2 equilibrium check that sets interpretable product-cofeed conditions. Preserve the chosen enthalpy/entropy/Cp evaluations; historical formation enthalpies on the page are discrepant and must not be averaged.
- NOAA/CAMEO CHRIS *Acetophenone* sheet (June 1999), [public PDF](https://cameochemicals.noaa.gov/chris/ACP.pdf), section 9.27. Partial ideal-gas Cp table only covers approximately 272–400 K. It does not close the 400–773 K data gap or supply a full uncertainty evaluation.

A validated acetophenone gas Cp(T) evaluation through 773 K remains a **data need**, not an invented missing paper. The open database's liquid Cp must not be substituted for gas Cp.

### Additional full text supplied for an existing comparator request

Tang 2024, DOI `10.1021/acs.iecr.4c01175`: the main article remains unretrieved, but its complete public SI is available at [ACS Figshare](https://ndownloader.figshare.com/files/47301420), article 26124831. Local artifact `/tmp/styrene-steam-free-benchmark/ie4c01175_si_001.pdf`, metadata `figshare.json` in the same directory. This is a linked SI addition, not a substitute for the article. It supplies experimental aromatic-composition/conversion/selectivity tables; missing main methods prevent a matched benchmark. Sent to the sole maintenance agent.

## Additional assay-intervention prior art

- DOI [10.1021/ja982082l](https://doi.org/10.1021/ja982082l), Wouters et al., *Reversible Tetrahedral–Octahedral Framework Aluminum Transformation in Zeolite Y*. Relevant to reversible coordination changes and what an ammonia assay can count; not evidence by itself for altered future H-CHA aging.
- DOI [10.1007/s11244-015-0387-8](https://doi.org/10.1007/s11244-015-0387-8), Di Iorio et al., work on the dynamic nature of Brønsted acid sites in Cu zeolites during ammonia titration. Relevant assay-state prior art. Verify exact metadata and distinguish Cu-containing systems from H-CHA.

Both requests were sent to the sole literature-maintenance agent before this registry update.

## Liquid-phase challenge: complete bounded handoff

- DOI [10.1021/acssuschemeng.5c06986](https://doi.org/10.1021/acssuschemeng.5c06986), prior candidate `2026-09-09-gounder-iglesia-additional-R1-N175`. [Verified open original](https://burjcdigital.urjc.es/server/api/core/bitstreams/faf9c304-78d0-4b24-8792-9a0fab58fc43/content). Continuous hemicellulose conversion and contrary fragment-feeding/deactivation evidence. José Iglesias is not Enrique Iglesia.
- DOI [10.1021/acssuschemeng.3c07356](https://doi.org/10.1021/acssuschemeng.3c07356), [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10880092/). Recombination can preserve useful pentose carbon, narrowing indiscriminate fragment-removal proposals.
- DOI [10.1073/pnas.1516466112](https://doi.org/10.1073/pnas.1516466112), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4586831/). Separate retro-aldol/hydride-shift catalysts already demonstrated for lactate production.
- DOI [10.1111/ijfs.12776](https://doi.org/10.1111/ijfs.12776), [primary full HTML](https://academic.oup.com/ijfst/article/50/7/1625/7866063). Concentrated-lactulose competitor; relevant to the negative selection decision, not a request for a broad enzyme literature search.

## Fresh methane-to-methanol cycle/extraction challenge

- Heyer et al., DOI [10.1021/jacs.4c06010](https://doi.org/10.1021/jacs.4c06010), *Spectroscopic Investigation of the Role of Water in Copper Zeolite Methane Oxidation*. [Open article](https://pmc.ncbi.nlm.nih.gov/articles/PMC11808935/), [author manuscript](https://backoffice.biblio.ugent.be/download/01JC5E3TF0XY6MS36YMA8K82NZ/01JC5E5GAS19QYX3PY24B64X6E), local `/tmp/stronger-direction-read/heyer2024.pdf`. Priority source check: qualify the Sushkevich 2017 note's unqualified water-reoxidation interpretation. No measurable Cu oxidation was found under the tested steam treatments; hydrogen evolution has competing carbon-product explanations. Preserve material/site dependence and the unresolved disagreement described by Fischer 2026; do not declare all water reoxidation disproven.
- Tomkins et al., DOI [10.1039/C8SC02795A](https://doi.org/10.1039/C8SC02795A), *Increasing the activity of copper exchanged mordenite in the direct isothermal conversion of methane to methanol by Pt and Pd doping*. [Europe PMC XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6330690/fullTextXML); extracted body `/tmp/stronger-direction-read/tomkins2018.txt`. The faithful original XML is retained as `tomkins2018.xml` in that directory after retrieval through `lit.py get`. Existing isothermal cycles, dopants and steam extraction constrain novelty.
- Álvarez, Marín and Ordóñez, DOI [10.1016/j.mcat.2020.110886](https://doi.org/10.1016/j.mcat.2020.110886), *Direct oxidation of methane to methanol over Cu-zeolites at mild conditions*. [Publisher](https://www.sciencedirect.com/science/article/abs/pii/S2468823120301383); possible full text in [author thesis](https://digibuo.uniovi.es/dspace/bitstream/handle/10651/70372/TD_MarinoMauroAlvarezIzaguirre.pdf?isAllowed=y&sequence=2). Article body not yet retrieved by researcher. Direct prior art for extraction water/flow and regeneration optimization; include metadata even if the full article remains unavailable.

All three were sent to the sole maintenance agent. Source qualification is useful even if the candidate screen ends negatively.

## Ethylene epoxidation intervention and practical comparison

These identified sources were sent as one sequential batch to the existing maintenance agent. Their presence here does not mean their full text has been read.

| Source | Reason for inclusion |
|---|---|
| [10.1016/j.jcat.2019.09.037](https://doi.org/10.1016/j.jcat.2019.09.037) | Harris–Bhan chloride deposition/removal kinetics; direct prior art for dynamic moderator control. |
| [10.1002/chem.201801356](https://doi.org/10.1002/chem.201801356) | Product and chloride cofeeds on a highly promoted catalyst; fair comparison requires optimized chloride and product conditions. |
| [10.1021/acs.iecr.9b04312](https://doi.org/10.1021/acs.iecr.9b04312) | Existing kinetic models of chlorine coverage and electronic versus geometric effects. |
| [10.1016/j.jcat.2024.115583](https://doi.org/10.1016/j.jcat.2024.115583) | Chloride coverage as an explanation for Ag particle-size effects; constrains a metal-efficiency proposal. |
| [10.1016/j.jcat.2026.117129](https://doi.org/10.1016/j.jcat.2026.117129) | Cs interactions with gaseous co-promoters; very recent prior art for chloride removal and secondary EO combustion. |
| [10.1016/j.jcat.2018.08.021](https://doi.org/10.1016/j.jcat.2018.08.021) | Ethane oxychlorination and quantitative chloride inventory measurements. |
| [10.1021/acscatal.4c01764](https://doi.org/10.1021/acscatal.4c01764) | Industrial chlorine dynamics perspective; tests whether a proposed operational uncertainty is already resolved. |
| [10.1039/D4CY00858H](https://doi.org/10.1039/D4CY00858H) | Re/Cl experimental prior art; [institutional full text](https://research-portal.uu.nl/files/258324469/d4cy00858h.pdf). Distinguish online 2024 from the 2025 journal issue. |
| [Berg 2025 thesis, 10.15480/882.14136](https://doi.org/10.15480/882.14136) | Spatial chlorine accumulation, moderator interruption, and pilot thermal profiles already measured. [Full text](https://d-nb.info/135281773X/34), local `/tmp/epoxidation-process/berg2025.pdf`. Root inspected selected sections, not the complete thesis. |
| [10.1002/cctc.202201511](https://doi.org/10.1002/cctc.202201511) | Commercial-conditions guide for researchers; nearest practical comparison requirements. |
| [Shell EO process description](https://www.shell.com/business-customers/catalysts-technologies/licensed-technologies/petrochemicals/ethylene-oxide-production.html) | Current supplier-reported cycle-average selectivity and catalyst life. Preserve supplier provenance; not an independent matched trial. |

The epoxidation researcher directly sent the same sole maintenance agent these further sources; the [full handoff](working/epoxidation-opportunity.md#source-handoff-and-remaining-access-limitations) preserves reading/access distinctions:

- [Jalil 2025, 10.1126/science.adt1213](https://doi.org/10.1126/science.adt1213), Ni promotion and Ni/Cl cooperation. [Public author manuscript](https://www.osti.gov/servlets/purl/2564884) retained at `research/working/source-artifacts/jalil2025-nickel.pdf`; read by researcher, SI not obtained.
- [Easton 2026, 10.1021/acs.jpcc.5c08033](https://doi.org/10.1021/acs.jpcc.5c08033), low-temperature NiAg oxygen activation. [Open source](https://pmc.ncbi.nlm.nih.gov/articles/PMC12990106/); distinguish cryogenic surface evidence from reacting catalyst state.
- [10.1007/s10562-017-2211-5](https://doi.org/10.1007/s10562-017-2211-5), Re deposition-order prior art; abstract inspected.
- [10.1002/zaac.202200267](https://doi.org/10.1002/zaac.202200267), Ag/ethylenediamine/perrhenate precursor; metadata/abstract only.
- [US20260027557A1](https://patents.google.com/patent/US20260027557A1/en), Ni–Ag with additional Cs/Re/Cl disclosure. Relevant to novelty of formulation combinations; not independent evidence of durability.
- Conditioning disclosures [US8815769B2](https://patents.google.com/patent/US8815769B2/en), [EP3548471A1](https://patents.google.com/patent/EP3548471A1/en), and [US20070225511A1](https://patents.justia.com/patent/20070225511), including steam/oxygen pretreatment. Preserve inventor claims as such.
- Hwang et al., *Roles of Re and Cs Promoters and Organochlorine Moderators in the Synthesis of Ethylene Oxide on Ag-based Catalysts*, ChemCatChem 16 e202301369 (already present in the knowledge base under an online-2023 slug; check before adding). Iyer/Bhan 2021, *Interdependencies among ethylene oxidation and chlorine moderation catalytic cycles*, ACS Catalysis 11, 14864–14876 (identifier verification requested). These are identified references, not permission to invent metadata.

Additional mechanistic constraint and SI requests were sent sequentially to the same agent:

- [10.1016/0021-9517(86)90341-6](https://doi.org/10.1016/0021-9517(86)90341-6), *The mechanism of ethylene epoxidation*, 1986. Isotope evidence explicitly considers direct use of preadsorbed oxygen versus recombination before epoxidation; prevents a false novelty claim. Abstract inspected, full text not retrieved by root.
- Existing Pu 2024 [10.1021/acscatal.3c04361](https://doi.org/10.1021/acscatal.3c04361): main article read; SI requested for the mixed-O2 signal and its detection limits (Fig. S16).
- Existing Hwang 2026 [10.1016/j.jcat.2026.117021](https://doi.org/10.1016/j.jcat.2026.117021): main article read; SI requested to resolve whether O2 conversion is directly measured or reconstructed from products. These SI requests do not make either main article unread.

Hwang SI was subsequently retrieved from the [public publisher file](https://ars.els-cdn.com/content/image/1-s2.0-S0021951726003568-mmc1.pdf), retained at `/tmp/epoxidation-process/hwang2026-si.pdf` and `.txt`, and submitted to the sole agent. Complete extracted text inspected by root. It does not explicitly resolve the analytical conversion calculation; S4 also documents ambiguity among fitted primary/secondary rate models.

- [Brandão and Reece 2024, 10.1039/D4CY00052H](https://doi.org/10.1039/D4CY00052H), *Non-steady state validation of kinetic models for ethylene epoxidation over silver catalysts*. [Open journal PDF](https://pubs.rsc.org/en/content/articlepdf/2024/cy/d4cy00052h). Direct transient-model prior art; distinguish qualitative discrimination from quantitative reproduction. Root inspected exposed primary sections; full ingestion requested. The linked [preprint](https://doi.org/10.26434/chemrxiv-2024-1f185) is a fallback version, not a separate independent result.

Jalil SI remains a separate pending retrieval request. The [publisher SI URL](https://www.science.org/doi/suppl/10.1126/science.adt1213/suppl_file/science.adt1213_sm.pdf) returned HTTP 403 to the root researcher. The sole maintenance agent was asked to seek an open alternative and retain an unresolved request if unsuccessful. Particle-size averaging, preparation details and Fig. S21 remain to be checked there; the main author manuscript has been read.

Keijzer [10.1039/D4CY00858H](https://doi.org/10.1039/D4CY00858H) main article is now centrally ingested/read. Its linked ESI was requested separately for preparation and Figs. S14–S17, which delimit EO deoxygenation, O2 release and chloride preconditioning. The no-ethylene EO tests and deliberately high Re loadings cannot directly quantify secondary loss in the proposed working Ni/Cs/Re catalyst.

Pu, Keijzer, Carbonio and Esposito SI were subsequently recovered and read in the [four-supplement batch](../literature/runs/2026-09-15-si-recovery/run.md). All four SI retrieval requests are resolved. Esposito's derivation is direct prior art for a model-dependent reversibility bound; Pu's absent reported calibration remains a scientific limitation after reading the SI.

### Older Ni preparation and multi-promoter calculation prior art

- [US9018126B2](https://patents.google.com/patent/US9018126B2/en): Ni co-impregnation with Ag/promoters and accelerated sintering comparison. Primary description/examples inspected. Supports a preparation/structural alternative, not working-condition lifetime.
- [US5380885A](https://patents.google.com/patent/US5380885A/en): older Ni post-addition route with actual Ag/Cs/Re aging examples. Root subsequently retrieved complete primary HTML at `/tmp/epoxidation-process/us5380885a.html` and derived `.txt`, read the preparation/testing/Table III sections, and supplied both to the maintenance agent. This is stronger prior art than composition disclosure; independent review is underway. Central ingestion/reading remains separately tracked.
- [Keivanimehr et al., 2025, 10.1038/s41598-025-95642-2](https://doi.org/10.1038/s41598-025-95642-2), *Synergistic effect of Ag(111) and transition metal promoters toward optimization of catalytic ethylene epoxidation selectivity*. Open DFT study of Cs and metal combinations; abstract/conclusion inspected. Constrains generic multi-promoter computational novelty, not evidence of working Ni/Cs/Re performance.

All were sent to the sole maintenance agent for sequential processing.

## Propylene-transfer screen: complete handoff

The [13-item source handoff](working/propylene-transfer-screen.md#exact-literature-handoff-retained-for-the-root-registry) is part of this registry. It preserves every exact DOI/retrieval URL, two dissertation requests, three linked-SI requests, supplied artifacts and reading limits already sent to the sole maintenance agent. Key additions are older direct Ni/Ag propylene epoxidation ([2005](https://doi.org/10.1016/j.apcata.2005.06.026)), Ni-core/Ag-shell material ([2018 online](https://doi.org/10.1016/j.apcatb.2018.10.061)), selective SO4/Cl oxygen ([2023](https://doi.org/10.1021/acscatal.3c00297)), and the [2024 isotope study](https://doi.org/10.1021/acscatal.4c04218). The latter also constrains the novelty of generic CO2-exchange/gas-O2-scrambling arguments in the EO branch. No quantitative result from that different catalyst/feed is transferred to Ni/Cs/Re–EO conditions.

## Lower-recycle alkylation and cross-topic sources

The [18-item handoff](working/stronger-practical-program.md#exact-literature-handoff-to-the-sole-literature-agent) is also part of this registry. It preserves the identified alkylation mechanism, Al-location, OSDA-free Beta, reactor/recycle and regeneration sources, two primary developer reports, and six relevant oxide/peroxide/SCR sources encountered during screening. Requests were already sent to the sole maintenance agent with supplied artifacts and explicit full-text gaps; this link does not create duplicate requests. The negative candidate decision does not remove their relevance or the requirement to retain inaccessible metadata.

## N2O pathway identifiability follow-up

The [four-item handoff](working/n2o-mechanism-opportunity.md#6-exact-literature-handoff-and-reading-record) preserves nitrate-preload isotope prior art, ammonium-nitrate titration, Cu-SSZ-13 SSITKA and the competing Cu/nitrate structural interpretation. Negahdar 2021 overlaps the preceding batch; its additional full-text artifact is a promotion aid, not a duplicate request. The same sole maintenance agent received all identifiers, lawful full-text links and reading limits. Existing Gao and Collier main papers require no duplicate ingestion.

## Further Ag site-counting and cross-olefin prior art

- Iyer and Bhan 2021, *Interdependencies Among Ethylene Oxidation and Chlorine Moderation Catalytic Cycles Over Promoted Ag/α-Al2O3 Catalysts*: the previously queued identity is now resolved as [10.1021/acscatal.1c03493](https://doi.org/10.1021/acscatal.1c03493). Publisher abstract and official group bibliography examined; main and SI requested. Coupled chlorine kinetics, support EO degradation and reactor predictions are already explicit prior art.
- Esposito, Parekh and Bhan 2026, *Common Active Sites and Oxidants within Ethylene and Propylene Epoxidation on Promoted Silver Catalysts*, [10.1021/acscatal.5c08223](https://doi.org/10.1021/acscatal.5c08223). Publisher and institutional abstracts examined; main and SI unread. Direct shared-site/oxidant and NO-derived promoter-retention prior art constrains generic cross-olefin transfer. These abstract claims are not transferred quantitatively to Ni/Cs/Re.
- Iyer and Bhan 2023, *Chemical Titration of Promoted Ag/α-Al2O3 Ethylene Epoxidation Catalysts*, [10.1002/cctc.202300329](https://doi.org/10.1002/cctc.202300329). Institutional abstract examined; main and SI unread. Working-feed trifluoroethanol titration differs from ex-situ N2O site counts, relevant to site-loss versus site-chemistry interpretations. Its stoichiometry and selectivity for sites must be checked before adaptation to Ni/Re.
- Esposito and Bhan 2023, *Critical Role of Chlorinated Hydrocarbons in Propylene Epoxidation over K-Ag/CaCO3*, [10.1021/acscatal.3c00915](https://doi.org/10.1021/acscatal.3c00915). Identity verified in the official group bibliography; body not examined. Direct predecessor for chloride-dependent propylene epoxidation, included for a fair prior-art comparison.

All four requests were sent to the existing sole maintenance agent, with the first updating an existing queued identity. Retrieval status is separate from abstract inspection.

## Ag working-state spectroscopy and operating-aging evidence

- Amy Ruby Marsh, 2024 Durham thesis, *Understanding the Roles of Promoters and Oxygen Species in Ethylene Epoxidation by Ex situ and In situ Spectroscopic Techniques*: [repository PDF](https://etheses.durham.ac.uk/id/eprint/15818/1/Marsh000892601.pdf). The [measurement reviewer](reviews/ag-working-state-measurement.md) read relevant primary sections and supplied PDF/text. The [central batch](../literature/runs/2026-09-15-marsh-thesis/run.md) subsequently retained the complete original and added a read package. Direct dilute-Re working-spectrum precedent with unresolved environment assignment.
- [US20240279193A1](https://patents.google.com/patent/US20240279193A1/en), *Process for reducing the aging-related deactivation of high selectivity ethylene oxide catalysts*. Public original HTML retained at `/tmp/ag-aging-prior-art/US20240279193A1.html`, derived `.txt`; original PDF also supplied. The [completed independent review](reviews/ag-operating-aging-prior-art.md) distinguishes actual 28-day aging data from a hypothetical example and lifetime extrapolation. Relevant chloride-policy comparator, with unmatched flows/work rates.
- [US20240025869A1](https://patents.justia.com/patent/20240025869), *Process for the production of ethylene oxide*. The same completed review inspected primary examples/figures. Fluoride-mineralized support and modifier operation through aging; stable optimum location is not stable activity/selectivity. Initial Justia curl retrieval failed, but the reviewer retrieved a lawful Google-patent HTML and original PDF and supplied both to the maintenance agent.
- Jeffrey William Kloosterman, Purdue dissertation, *The chemical role of rhenium in the epoxidation of ethylene and butadiene*, [repository record AAI3124172](https://docs.lib.purdue.edu/dissertations/AAI3124172/). Abstract/record inspected; full text requested. Relevant earlier Re chemistry; exact metadata to be verified during ingestion.
- [EP0737099B1](https://patents.google.com/patent/EP0737099B1/en), *Epoxidation catalyst and process*, [official PDF](https://data.epo.org/publication-server/rest/v1.2/publication-dates/19980708/patents/EP0737099NWB1/document.pdf). Group IVB oxo-salt/promoted-Ag stability prior art. Search passage only; actual examples unread.
- *Rhenium as a promoter for ethylene epoxidation*, 1992, [PII 0926860X9280307X](https://www.sciencedirect.com/science/article/pii/0926860X9280307X). Abstract inspected; DOI identity and original requested. Relevant low-loading Re/oxygen-adsorption precedent.
- *Rhenium promotion of Ag and Cu–Ag bimetallic catalysts for ethylene epoxidation*, [PII S0920586106004809](https://www.sciencedirect.com/science/article/abs/pii/S0920586106004809). Identified alloy/Re compatibility precedent; full abstract/body and exact DOI/year remain to be checked.

All were routed to the same sole agent. These requests do not assert full-text reading or verified performance from the uninspected entries.

## Peroxide/zeolite tandem challenge

The [nine-item handoff](working/peroxide-tandem-challenge.md#exact-literature-handoff-and-access-limits) is part of this registry. It preserves direct coupled PO/EG studies, alkaline TS-1 and crossover control, peroxide-decomposition and solvent studies, a long-duration HPPO comparator, supplied original artifacts and SI gaps. The starting AIChE paper was already queued; the handoff identifies that overlap. Every request went to the sole maintenance agent. The negative candidate decision does not remove the requirement to retain relevant unread metadata.

## Further oxygen-state and Ag-alloy comparators

- Dorst et al., 2026, *Controlling Heterogeneous Catalysis With Subsurface Oxygen*, [10.1002/anie.202524699](https://doi.org/10.1002/anie.202524699), [lawful repository original](https://pure.mpg.de/rest/items/item_3696777_2/component/file_3713600/content), PMC13134625. Root inspected the abstract and exposed method passages; complete body unread. Rh model-surface evidence is relevant to stationary oxygen changing reactivity without serving as a continuing oxygen sink. No quantitative transfer to NiAg is claimed.
- Soni et al., 2025, *Structure and Reactivity of AgCu/SiO2 Bimetallic Catalysts for Alkene Epoxidation*, [10.1002/cctc.202500921](https://doi.org/10.1002/cctc.202500921). Primary abstract inspected; main/SI unread. Direct preparation and state comparator for bimetallic Ag across ethylene and propylene epoxidation.
- Svintsitskiy et al., 2023, *Room temperature epoxidation of ethylene over delafossite-based AgNiO2 nanoparticles*, [10.1039/D3CP01701J](https://doi.org/10.1039/D3CP01701J), [linked SI](https://www.rsc.org/suppdata/d3/cp/d3cp01701j/d3cp01701j1.pdf). Primary abstract inspected; main and SI requested. Distinct Ag/Ni oxide oxygen-delivery and phase-change comparator. Room-temperature oxygen consumption alone does not establish sustained turnover or transfer to dilute NiAg.

These were sent to the same sole maintenance agent. A further public OSTI-record check exposed the Jalil main manuscript but no SI link; the existing Jalil SI gap remains open.

### Brandão–Reece preprint recovery

Root recovered the original 23-page preprint for [10.26434/chemrxiv-2024-1f185](https://doi.org/10.26434/chemrxiv-2024-1f185) through the [public Cambridge archive](https://www.cambridge.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/659ff20be9ebbb4db9ee8a3c/original/non-steady-state-validation-of-kinetic-models-for-ethylene-epoxidation-over-silver-catalysts.pdf), using `lit.py get`. PDF and extracted text are `/tmp/ag-aging-prior-art/brandao2024-preprint.pdf` and `.txt` and were supplied to the sole agent. Selected methods/discussion/conclusions were read by root; centralized promotion and reading are now complete in the [Brandão/Svintsitskiy batch](../literature/runs/2026-09-15-brandao-svintsitskiy/run.md). The old ChemRxiv host returned 403, while Cambridge returned the PDF. This recovers the alternative version, not the inaccessible [journal version](https://doi.org/10.1039/D4CY00052H). The landing page also exposes simulation code/input files, whose retrieval remains optional and unconfirmed.

## Light-alkane dehydrogenation follow-up

The [current PDH source record](working/dehydrogenation-consequential-screen.md#current-source-record-and-remaining-limits) updates the original handoff covering Ga hydrogen/redox chemistry, competitive catalysts, regeneration patents and process benchmarks. The sole worker received all identifiers and available originals. Fresh independent review subsequently recovered Wu's exact SI and Malizia's SI, with originals supplied to that worker. The [completed independent review](reviews/dehydrogenation-fresh-value.md) preserves the confirmed subtraction omission, unresolved magnitude and cycle chronology, explicit chlorine-conditioning precedent and corrected Cheng Pt normalization. The initial SI-unavailable statements in the screen are superseded.

## Ammonia-cracking kinetics and attainable hydrogen removal

The [current ammonia source record](working/ammonia-kinetics-screen.md#current-sources-and-unresolved-content) updates the original handoff, including Qiu2026 main/SI, recent kinetic studies, two theses and direct model-nonuniqueness prior art. All were sent to the sole worker. The [completed fresh review](reviews/ammonia-hydrogen-inference.md) independently checks the reactive-probe inference, physical hydrogen-pressure bound and printed-model consistency; its additional direct membrane precedents were routed to the same worker. The current source record distinguishes completed ingestion from the remaining unread theses. The conditional study has not been promoted to a substantial research program.

The [closing ammonia batch](../literature/runs/2026-09-16-ammonia-kinetics/run.md) completed Qiu2026 main/SI, the distinct conference record, Prasad2009 and Napolitano2025. Other ammonia, PDH, carbonylation, methane-context and older requests remain unprocessed unless a separate completed report above states otherwise. No additional batch is scheduled.
