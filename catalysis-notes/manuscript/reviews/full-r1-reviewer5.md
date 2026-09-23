# Full manuscript review, round 1 — reviewer 5

**Verdict: suitable as a proposed research portfolio, with minor revisions. No major findings.** The four developed programs explain their prior work, consequential decisions, conditional original contributions, and interpretation limits. The six reserves remain appropriately short. The manuscript does not present the proposed experiments as completed work or require their hypotheses to be true. None of the findings below requires additional experiments or an enlarged reserve program.

## Minor findings

### 1. Identify the established roles of the two polymer catalyst components before discussing selective initiation loss

**Location:** `sections/03-polymer.tex:8–14`, especially line 8; PDF p.17, Section 3.1.

The opening defines isomerizing ethenolysis and names WO3/SiO2 and Na/alumina, but does not explicitly connect each material to its established tandem function. The next paragraphs discuss unchanged W function, fresh-Na rescue, unsaturation supply, and selective initiation loss. A reader outside this particular system must infer the basic division of labor before evaluating those distinctions.

**Evidence:** Conk et al.'s original article, PDF p.2 / printed p.1323, identifies WO3/SiO2 as the olefin-metathesis component and the basic Na/alumina material as an olefin-isomerization component. The same page discusses chain scission, which is separate from those established roles. This supports a short explanation without resolving the disputed initiation mechanism. Source checked: `literature/papers/conk2024-polyolefin-waste-to-light-olefins/original.pdf`; [published article](https://doi.org/10.1126/science.adq7316).

**Remedy:** Add one or two sentences after the component names explaining these established functions and how migration plus metathesis repeatedly shortens a reactive chain. Retain the existing uncertainty about how saturated PE first acquires reactive unsaturation and about which functions change during reuse. The current qualifications are sound; this addition makes them easier to understand.

### 2. Explain chlorine deposition and removal before introducing chloride policies as the decisive Ag alternative

**Location:** `sections/04-silver.tex:12–16`, with the operational consequences at lines 28–32 and 60–70; PDF pp.23–24, 26–27.

The chapter makes chloride operation central to its originality and comparison design, but the initial explanation moves directly from an organochloride selectivity increase to chlorine-exchange models and lower-chloride aging policies. It does not first state that the gas modifier deposits surface chlorine and that competing removal processes change that coverage. The later statement that ethane removes chlorine is useful but arrives as a carbon-accounting caveat. As written, the reason chloride adjustment can change both activity and selectivity is less accessible than the corresponding physical explanation in the water chapter.

**Evidence:** Iyer and Bhan's original article, PDF pp.1–2 / printed pp.14864–14865, introduces gas-phase alkyl-chloride deposition, alkane-mediated removal, the effect of surface chlorine on oxidation kinetics, and the need to regulate coverage. These are established background points, distinct from the manuscript's conditional Ni-specific mechanism. Source checked: `literature/papers/iyer2021-interdependencies-among-ethylene-oxidation-and/original.pdf`; [published article](https://doi.org/10.1021/acscatal.1c03493).

**Remedy:** Add two or three sentences near the first chloride discussion explaining this deposition/removal balance and why its operating optimum can trade selectivity against useful rate. Cite the already included Iyer reference. Do not expand this into a new mechanistic section or imply a universal chloride optimum.

### 3. Add References to the document navigation

**Location:** `main.tex:44–46`; PDF p.3 contents and pp.31–34 bibliography.

The bibliography is absent from both the contents and the PDF outline. All five scientific sections and the overview have navigation entries, so the final four pages are the only major document component without direct navigation. Citation links still work; this is a usability issue, not a citation failure.

**Evidence:** The independently built PDF's contents page and `mutool show main.pdf outline` both omit References.

**Remedy:** Add one correctly anchored References entry to the contents/PDF outline at the bibliography start, and verify that it lands on p.31. No bibliography package migration is needed.

## Scientific and document checks

- Read `main.tex`, every section, all 42 bibliography entries, and `README.md`. Read `literature/AGENTS.md` and used the library without mutation. Evidence notes for the first two programs helped locate primary materials; no prior or peer review files were read.
- Built a fresh copy of the source, sections, and bibliography in `/tmp/catalysis-full-review5-702THh` using the README's `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` command. The build succeeds at 34 pages with no final LaTeX warnings, undefined citations/references, or overfull/underfull box reports. All 42 citation keys resolve, and all 42 bibliography entries are used.
- Compared layout-preserving extracted text from the fresh PDF and retained `manuscript/main.pdf`: identical. Inspected PDF metadata and outline. Visually inspected pages 1, 3, 5, 7, 12, 19, 24, 29, 31, and 34, covering the title/overview, contents, equations, experimental tables, prose, shortlist, and bibliography. Text, mathematical notation, tables, links, and margins are readable, with no clipping found on those pages.
- Checked Fang's original HTML for the 0.025 g PDVB/0.5 g catalyst configuration, 44.1% starting conversion, 1200 h result, and approximately 80/175 s outlet-water decays. Reran the supplied water-output calculation: 116.0352 versus 219.8266 feed-carbon hours, ratio 1.89448 and additive-mass-adjusted ratio 1.80427. The stated rounding and limitations are appropriate. This rerun verifies the retained data and calculation, not an independent reacquisition of the source spreadsheet.
- Checked Brody's original PDF for the one/five/five/five-minute cycle, Ar experimental purges versus modeled steam heat exchange, 53.2% and 47.24% C2+ yields, and the 10 wt% methods / 20 wt% conclusion discrepancy. The manuscript preserves these distinctions. Independently recalculated the 2.02-minute recovery headroom.
- Checked Conk's original PDF, particularly Figure 4B and caption, for the fresh 0.4 g Na/alumina addition only before the second of three PE charges. Checked Chen's final published model for ethylene inhibition, omission of deactivation, the slow-isomerization applicability limit, and the role of the quasi-equilibrium numerical comparison. The manuscript does not transfer that molecular model's prediction to aged Na/W as an established result.
- Checked Kemp's original HTML for Table II composition differences, the solvent control's lack of aging data, and Table III's 4.3 versus 6.1 percentage-point selectivity losses after 50 accelerated-aging days. Independently recalculated the approximately 1:835 Ni:Ag bulk ratio and the Ag chapter's selectivity-based reactant/CO2 percentages. These agree with the manuscript.
- Reviewed the proposed balances, contrasts, normalization bases, and conditional validation logic across the complete text. I found no material inconsistency in the two-pool counterexample, steam timing interaction, two-source isotope allocation under its stated assumptions, or complete-clock output comparisons. Pilot qualification and withheld validation remain proposed dependencies, as they should.

## Verification limits

This was a whole-document review with targeted primary-source verification, not a fresh exhaustive novelty search or a complete audit of every cited supplement. Live access attempts to the Nature article, Kemp patent, Conk dissertation record, and Chen DOI failed or encountered browser/access checks; I did not bypass them. Primary-source checks therefore relied on the available local originals. No claim of current dissertation access or newly verified embargo status follows from this review. Unchecked bibliographic metadata and reserve-source details remain outside the direct source-verification scope. The experiments, instrument access, attainable uncertainty, and practical benefits remain untested; this does not invalidate a clearly conditional research proposal.
