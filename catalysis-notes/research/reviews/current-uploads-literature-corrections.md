# Current-upload literature corrections

This is the bounded correction audit for the uploaded and otherwise identified program-development sources. It covers the final reviewer corrections and four supporting-information requests added after the main-source closeout. No new literature discovery was performed.

The durable intake records are in [`literature/runs/2026-09-16-current-uploads-corrections/`](../../literature/runs/2026-09-16-current-uploads-corrections/). The two rounds contain the candidate, decision, retrieval-attempt, and ingest records. The historical queue ledger remains the source for the older primary-body dispositions; this report gives the current artifact and interpretation limits after the uploaded-source corrections rather than repeating its superseded 66-identity gap count.

## Validation

The final command was:

```text
/home/sgusev/repo/skills/literature/scripts/lit.py check /home/sgusev/repo/catalisys-notes/literature
```

It returned `KB_CHECK=ok`, with `UNREAD=39` and `READ_UNCITED=196`. The package-directory scan at that point contained 35 `access: "none"` directories, including the Akin alias; these correspond to 34 distinct canonical missing materials. Four newly added supporting-information packages are included in that count. The unread count includes retained data artifacts and other sources outside this correction batch.

## Source-note repairs

The following notes were corrected against the retained originals or the supplied extracted text. The package slugs are stable KB identifiers.

| Package | Correction |
|---|---|
| [`zhang2024-durable-w20o58-species-catalyzed-cc`](../../literature/papers/zhang2024-durable-w20o58-species-catalyzed-cc/paper.md) | The note now reports the combined EG plus 1,2-PG carbon yield falling from 70.4 to 61.4 C% over five cycles, despite the source's stability wording. The W-loss, XRD, and vacancy claims retain their source locators. |
| [`al2016-ethylene-glycol-production-from-glucose`](../../literature/papers/al2016-ethylene-glycol-production-from-glucose/paper.md) | Corrected ammonium metatungstate (AMT), and distinguished the 2016 online date from the 2017 issue. The approximately 74% value is identified as the selected low-feed model result; the experimental/model comparison pools EG with small C3/C4 glycols and is not an unqualified EG-only demonstration. |
| [`al2022-paving-the-way-towards-an`](../../literature/papers/al2022-paving-the-way-towards-an/paper.md) | Standard cellulose and lignocellulosic feeds are described as ball-milled for 4 h. The explicitly unmilled cellulose control is kept as the exception. |
| [`li2020-enhanced-ni-w-ti-catalyst`](../../literature/papers/li2020-enhanced-ni-w-ti-catalyst/paper.md) and [`li2020-supporting-information-for-enhanced-ni`](../../literature/papers/li2020-supporting-information-for-enhanced-ni/paper.md) | The preleachate control is bounded correctly: Ni/M alone gives 27.1% EG, while Ni/M plus preleachate gives 29.5%; the solution alone gives trace EG. The 29.5% value is not assigned to a productive leachate, and the 2.4-point difference is not treated as proof of exported catalytic activity. The source's 40 mL method versus 100 mL Figure 3 caption conflict is retained rather than converted into a W balance. |
| [`record2023-torres-thesis-on-liquid-zeolite`](../../literature/papers/record2023-torres-thesis-on-liquid-zeolite/paper.md) | Corrected the title-page identity to Chris Torres, *Solvent and Surface Effects on Alkene Oxidation Catalysis over Transition Metal Incorporated Zeolites* (2023). The ATR-IR result is bounded to Ti-MFI at 313 K with 1.0 M water and 0.1 M 1,2-epoxyhexane; it is not recast as a BEA propylene-oxide reactor result. |
| [`chapter0000-chapter-4-tandem-polyethylene-ethenolysis`](../../literature/papers/chapter0000-chapter-4-tandem-polyethylene-ethenolysis/paper.md) | The retained dissertation is now marked read with the title-page identity Nicholas Mason Wang, 2022. Pressure comparisons use extracted/PDF pages 74–76; the 60-to-14.7 psi comparison also changes temperature and catalyst loading. Cooling and depressurization effects are located at pages 78–79 and retain the isomerization/recombination caveat. |
| [`zhao2023-hydrophobic-modification-for-co-photo`](../../literature/papers/zhao2023-hydrophobic-modification-for-co-photo/paper.md) | The paper reports water uptake (8.82 versus 4.41 cm³ g⁻¹) and WGS rates (1.47 versus 0.22 mmol g⁻¹ h⁻¹) per gram for a 1:1 LD-Co/PDVB mixture. The source does not establish whether the denominator is total mixture or catalyst mass; if it is total-mixture mass, dilution can explain the factor-of-two uptake change and gives the conditional 3.34-fold WGS correction. Intrinsic-Co normalization is not claimed. |
| [`yang2020-investigation-of-the-deactivation-behavior`](../../literature/papers/yang2020-investigation-of-the-deactivation-behavior/paper.md) | Faster water-vapor diffusion/local water removal is labeled as the authors' interpretation. Local site-water activity was not directly measured. |
| [`names1997-transient-and-steady-state-studies`](../../literature/papers/names1997-transient-and-steady-state-studies/paper.md) | Corrected the authors to Hanssen, Blekkan, Schanke, and Holmen; fixed the DOI and page locators. The unchanged intrinsic activity is methane-specific after drying and within the SSITKA model. N* is an inferred reactive-intermediate inventory, not an independently counted working-site population during wet treatment. |
| [`further1998-further-studies-on-ligand-promoted`](../../literature/papers/further1998-further-studies-on-ligand-promoted/paper.md) | Corrected the authors to Carrier, Lambert, and Che. The note separates preparation-stage ligand-promoted alumina dissolution from sugar-turnover W export and preserves the source's statement that direct adsorption/readsorption evidence was absent. |
| [`raun2019-modeling-of-the-molybdenum-loss`](../../literature/papers/raun2019-modeling-of-the-molybdenum-loss/paper.md) | Added author Sina Baier from the retained original title page. |
| [`ayla2020-alkene-epoxidations-with-h2o2-over`](../../literature/papers/ayla2020-alkene-epoxidations-with-h2o2-over/paper.md) | Corrected the journal issue year to 2021 while retaining the 2020 online date. |
| [`leonhardt2024-the-effects-of-tioh-site`](../../literature/papers/leonhardt2024-the-effects-of-tioh-site/paper.md) | The complete model result now states that coadsorbed epoxide narrows the accessible facet distribution and largely removes the predicted site-distortion dependence. |
| [`wang2007-deactivation-and-regeneration-of-titanium`](../../literature/papers/wang2007-deactivation-and-regeneration-of-titanium/paper.md) | Framework Ti leaching remains a structural/regeneration inference; the note no longer describes it as a directly measured dissolved-Ti assay. |
| [`data2026-source-workbook-for-hydrophobic-promoter`](../../literature/papers/data2026-source-workbook-for-hydrophobic-promoter/paper.md) | The package is read only for the Figure 1 sheet. The column mapping, common 25–585 h interval, 154 h exact duplicate, and Figure 1 calculation are recorded; Figures 2–3 and the other worksheets remain unread, and catalyst-versus-total-mixture normalization remains unresolved. |

The Chacko dissertation's printed Eq. 7 was checked against the retained source. The equation is not used in the current KB note, so no chemistry was silently corrected there; if that equation is quoted later, the source's unbalanced form must be identified and the balanced carbonate relation used for interpretation.

## Current supporting-information gap list

These are the four newly identified, explicitly used artifacts whose lawful retrieval remained unresolved after one direct `lit.py get` attempt each. They are separate KB packages, linked to their read main sources, and intentionally retain no guessed SI DOI suffix.

| Main source | SI package | Exact attempted URL | Result and remaining limit |
|---|---|---|---|
| Zhao et al., 2023, `10.1016/j.nanoen.2023.108350` | [`zhao2023-supporting-information-for-hydrophobic-modification`](../../literature/papers/zhao2023-supporting-information-for-hydrophobic-modification/paper.md) | `https://www.sciencedirect.com/science/article/pii/S2211285523001878` | `lit.py get` returned HTTP 403; metadata-only and unread. |
| Kim et al., 2026, `10.1016/j.jcat.2026.116949` | [`kim2026-supporting-information-for-critical-role`](../../literature/papers/kim2026-supporting-information-for-critical-role/paper.md) | `https://doi.org/10.1016/j.jcat.2026.116949` | DOI landing returned HTTP 302 with no retained body; metadata-only and unread. |
| Murphy, Letterio & Xu, 2017, `10.1021/acscatal.6b03166` | [`murphy2017-supporting-information-for-catalyst-deactivation`](../../literature/papers/murphy2017-supporting-information-for-catalyst-deactivation/paper.md) | `https://doi.org/10.1021/acscatal.6b03166` | ACS main DOI landing returned HTTP 302 with no retained body; metadata-only and unread. The main paper gives the ACS DOI but no separate SI DOI. |
| Chi et al., 2026, `10.1002/anie.6752036` | [`chi2026-supporting-information-for-entropy-stabilized`](../../literature/papers/chi2026-supporting-information-for-entropy-stabilized/paper.md) | `https://doi.org/10.1002/anie.6752036` | Wiley main DOI landing returned HTTP 302 with no retained body; metadata-only and unread. The main text names `anie73019-sup-0001-SuppMat.docx`, which does not by itself establish a direct URL or DOI. |

The remaining supplied-queue artifact/version limits are unchanged and remain separate from the four metadata-only SI packages:

- Xu 2026: main article read; supplementary tables and detailed carbon-balance/volatile-loss accounting remain unavailable.
- Gao 2020 and Brody 2022: primary sources read, but the requested Gao supplement (melting/sequence details) and Brody SI (cycle/process details) were not retained.
- Mougel 2016: PMC main article read; ACS SI not retained.
- Fang 2026 source workbook: Figure 1 was mapped for the parent calculation; other worksheets remain unread and the water-uptake denominator is unresolved.
- Young 2020 carbonate manuscript: accepted manuscript read; publisher version and SI were not retained.
- Pang 2021: accepted manuscript read; publisher main/SI version was not separately retained.
- NSF STTR award record: project record read; underlying reports and results are unavailable.
- Unglaub 2023 wax-drainage papers: primary LIDSEN HTML is read for each; publisher PDF routes were unavailable.
- Zhang 2023 CF4 decomposition: main PDF read; supporting information was not retained.

The [current source snapshot](current-uploads-source-status.md) records the remaining main-source availability and current metadata-only inventory. The older program-development ledger records historical queue dispositions; those unresolved main works are not counted as newly missing artifacts in this correction report.

## Provenance and check notes

The four new SI records use the exact supplied publisher or DOI landing URLs and record their relation to the main DOI. No guessed `.s001`, `.s002`, or other suffix was introduced. The run account preserves both rounds and the HTTP outcomes. The retained original workbook remains authoritative for the inspected Figure 1 sheet; the parent calculation files are supporting analysis, not a claim that the whole dataset was audited.
