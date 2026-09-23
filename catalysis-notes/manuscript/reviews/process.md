# Manuscript development and review record

Requested process: finish each stage before starting the next; one author agent, then five independent reviewers; parent adjudication; a separate correction agent addresses every accepted issue. Repeat five-reviewer review after any accepted major issue. Resolve accepted minor issues before closing the stage. Apply the same procedure to the complete manuscript.

## Planned stages

1. LaTeX scaffold and physical water management.
2. Cyclic oxides: steam compatibility and recoverability.
3. Polymer ethenolysis: retained output and fresh-catalyst demand.
4. Promoted Ag: Ni-dependent selectivity retention.
5. Introduction, portfolio assessment, shorter considered ideas, and synthesis.
6. Complete-manuscript scientific, evidence, experimental, and presentation review.

The manuscript describes proposed research. Literature results, new analytical deductions, design choices, and experimental unknowns must remain distinguishable. A completed proposal does not imply that its experimental hypotheses have been validated.

## Status

Stages 1–5 CLOSED. Complete-manuscript review and corrections CLOSED. Final manuscript complete.

## Review criteria and adjudication

Each five-agent review is independent: reviewers read the stage and primary evidence, do not read one another's reports, and write separate reports with file/line locations, severity, evidence, and proposed remedies. Emphases cover prior art and source fidelity; causal experimental design; quantitative balances and practical value; scientific coherence and falsifiability; and reader comprehension, citations, and typesetting. Every reviewer may raise issues outside their emphasis.

Major issues change the validity of a central claim, experimental inference, material balance, originality case, or decision criterion, or leave the requested program materially incomplete. Minor issues affect precision, explanation, citation completeness, or presentation without overturning the scientific inference. The parent records accepted/rejected findings and reasons; labels from reviewers are advisory. No-major closure means no accepted major issue remains in that review round, not experimental validation or proof of exhaustive novelty.

## Parent verification during stage 1

- Read the latest portfolio, water first-test design, two-pool identifiability derivation, particle/film transport analysis, and published-output calculation.
- Retrieved the official Fang source spreadsheet from the publisher to `/tmp/manuscript-ft-source.xlsx`; reran its integration read-only using the repository script. Reproduced the 25–585 h integrals 116.0351956683 and 219.8266193204, ratio 1.8944822565, and mass-adjusted ratio 1.8042688157. These remain reported-output proxies, not validated economic performance.
- Online search surfaced the 2025 JACS Au water-affinity paper, DOI 10.1021/jacsau.5c01157. Shared it with the author; access limits require a narrow claim if only abstract text is available.

## Stage 1 review round 1

Author: `stage1_author`. Five independent reports: `stage1-r1-reviewer1.md` through `stage1-r1-reviewer5.md`. All verdicts: no major issues, minor revisions. Parent accepted the consolidated corrections in `stage1-r1-adjudication.md`; separate agent `stage1_fix` is implementing them. No repeated review required unless correction verification exposes a new major issue. Parent reproduced the numerical check and inspected rendered PDF page 4; build clean.

Stage 1 CLOSED. Parent read the revised chapter and correction mapping; all nine accepted corrections and two concise optional improvements are implemented. The quantitative reproduction still passes and the final build log is clean. No new major issue arose. Proceed to stage 2.

## Stage 2 author and parent verification

Reused `stage1_author` for cyclic-oxide drafting after stage 1 closure. Parent checked Brody original Methods/Table 1/process modeling and the 10 wt% methods versus 20 wt% conclusion discrepancy; actual measured loading must govern experiments. Reproduced 2.018628 min/cycle illustrative allowance, 18.785 mg Li per gram of hypothetical 10 wt% material, and 2.04248 mol CO2/mol ethane for one hypothetical five-minute purge at z=1/3. None predicts steam damage or process economics.

Retrieved and selectively read Fanxing Li's January 17, 2024 NETL presentation, `https://netl.doe.gov/sites/default/files/netl-file/24RCC/24RCC_Li.pdf`, especially slides 20–30. Slide 25's carbonate replenishment refers to carbonation contact/residence, not demonstrated fresh-lithium makeup. It reinforces existing regeneration precedent and does not supply the proposed steam-timing result. Checked Chacko original title and unbalanced Eq. 7 (printed p.101): the balanced carbonation requires 2XOH. Shared findings with author; library unchanged.

Stage 2 author complete; integrated PDF 14 pages. Dispatched five independent reviews (`reviewer1`–`reviewer5`) for round 1. Closed water chapter unchanged. Parent read cyclic draft and verified core arithmetic; author incorporated parent notation and quench-validity clarifications before review.

Stage 2 round 1 complete. Parent accepts R4's untreated steam-policy gap as major; related null-scope concerns also appear in R1/R3/R5. Nine consolidated minor corrections accepted. See `stage2-r1-adjudication.md`. Separate correction agent `stage1_fix` is implementing a bounded ordinary steam-versus-Ar comparison before special restoration, preserving the existing treatment-order test. Five independent reviewers will repeat after correction.

Stage 2 major and minor corrections complete by separate agent. Updated PDF 16 pages, clean build; water unchanged. Parent read revised policy comparison, terminal-reset cadence and claim limits. All five independent reviewers dispatched for round 2 on the entire revised stage, with no access to one another's reports.

Stage 2 round 2: all five reviews found no remaining major issue. Parent accepted the single overlapping minor contrast-interval correction; separate agent implemented it in `stage2-r2-corrections.md`. Parent verified the revised closing rule, clean build, and unchanged water stage. Stage 2 CLOSED. Proceed to stage 3.

## Stage 3 author and parent verification

Author started after stage 2 closure. Parent checked original Conk Figure 4B and SI: three charges, 0.4 g each initial catalyst solid, fresh 0.4 g Na material only before charge 2; charge 3 adds polymer only. Published isotope percentages refer to a specific isotopomer calculation, not automatically carbon-atom fractions. Any new two-source tracer calculation needs calibrated atom fractions and consistent enrichment across all catalyst/feed histories, with other carbon inputs controlled. Shared these points with author.

Parent also checked SI pressure conventions: batch ethylene/methane charges are specified near room temperature; semibatch SI reports 19 bar gauge, 100 sccm ethylene and 5 sccm methane, 12-minute GC intervals. These are not interchangeable fixed hot partial pressures. A same-mode reuse/makeup baseline and complete-charge pressure comparison are required. Official Conk dissertation page still presents an access check; no body-reading claim or access bypass.

Stage 3 author complete; integrated PDF 22 pages. Five independent reviewers dispatched for round 1. Parent read the full chapter and evidence note, checked the catalyst-solid arithmetic and two-source isotope algebra, and confirmed the same-mode reuse qualification and withheld-dose decision. Public patent regeneration disclosure is credited without claiming demonstrated restoration of the exact unmodified Na/W mixture.

Stage 3 round 1 complete. Parent accepts the shared R1/R2 pressure–makeup screening issue as major and all four localized R4/R5 corrections. See `stage3-r1-adjudication.md`. Separate correction agent assigned; repeat five-reviewer review required after corrections.

Stage 3 round 1 corrections completed by the separate agent; parent read the revised pressure/dose design, paired withheld-dose validation and bounded replacement extension. Five independent reviewers dispatched for round 2. Integrated PDF remains 22 pages; closed chapters unchanged.

Stage 3 round 2: all five independent reports approve, with no remaining major or minor issue. Parent read all reports and verified the corrections. See `stage3-r2-adjudication.md`. Stage 3 CLOSED. Proceed to stage 4.

## Stage 4 author and parent verification

Author started only after stage 3 closure. Parent read the current Ag program, historical Ni review, ordinary-aging prior art and latest uploaded-source audit. Checked the original Kemp patent experimental section/Table III: A/C have different Cs and post-treatment, B was not aged, 50-day losses are 4.3 versus 6.1 percentage points, not exact final-selectivity differences or a steady decay-rate advantage. Computed bulk Ag/Ni = 834.73 and reaction-only 90% to 91% selectivity savings: ethylene 1.0989%, CO2 10.9890%, O2 4.3956% at fixed EO output.

Parent read Hwang original methods and mechanism framing, and Jalil main/SI. Rendered original SI Figure S21 (PDF p. 30, printed p. 29): both rates evolve substantially after chloride addition; NiAg EO increases initially then declines through roughly 20 h. No stationary-rate or lifetime conclusion follows. Hwang's proposed microscopic shunt and Jalil's model-surface oxygen assignments must stay hypotheses for the full promoted material.

Primary online search additionally found US20260027557A1 (published January 29, 2026), a Jalil/Christopher-associated NiAg composition disclosure. Its broader high-selectivity claims and >12 h conditioning discussion do not supply verified Cs/Re-promoted Ni retention. Shared the primary link with author for scoped novelty checking; no new performance number is imported and no legal-status assessment is made. Local literature remains unchanged.

Stage 4 author complete: chapter, evidence and nine selected references; integrated PDF p. 30 pages, clean build. Parent read the full draft and requested explicit conditioning clocks, both-material recovery controls, absolute policy comparisons and unfiltered EO alongside acceptance criteria; author incorporated these before review. Five independent reviewers dispatched for round 1.

Stage 4 round 1 complete. Parent accepts R2 untreated-aging comparator and R5 omission of tested Ni recovery from final ranking as major. R3 acceptance-window and R5 symbolic-cost clarifications accepted as minor. Separate correction agent assigned; repeat five-reviewer review required. See `stage4-r1-adjudication.md`.

Stage 4 corrections complete by separate agent. Parent read the correction mapping and revised untreated policy, acceptance windows, cost boundary and both-material recovery identity/ranking. All five independent reviewers dispatched for round 2. Build remains 30 pages; stages 1–3 unchanged.

Stage 4 round 2 complete: all five approve, no remaining major or minor corrections. Parent read all reports; see `stage4-r2-adjudication.md`. Stage 4 CLOSED. Proceed to stage 5 portfolio/introduction/shortlist.

## Stage 5 author and parent verification

Author started after stage 4 closure. Parent reread the current decision brief and latest tungsten, liquid/polymer, CHA/styrene, methane, PDH and closed-screen audits. The editorial choice is four developed main programs; it does not elevate each to equal immediate experimental priority. Six compact reserves retain their narrower unresolved questions.

Parent checked Li 2020 original Table 1 (PDF p. 4): Ni/M alone gives 27.1% EG, versus 29.5% in SI Table S3 with preleachate. Zhang 2024 explicitly reports 70.4→61.4% combined glycols over five cycles. Neither supports the earlier stronger leachate or invariant-yield claim. Luo 2018 §3.4.2 applies an intermediate NH3-TPD to both reversed-aging histories; it is not an assay/no-assay control. These details were shared with author. Targeted primary online searching confirmed adjacent sugar coordination and Ti-solvent precedents and the original zirconia publication; no claim of exhaustive novelty or new experimental result is made.

Stage 5 author complete: ranked overview, six compact reserves, withdrawn claims, source notes, selected references, mandatory inputs and README navigation. Integrated PDF has 34 pages. Parent read the additions, checked the manuscript contents, and independently verified the hot-mannose and NO/sulfur source passages. Five independent reviewers dispatched for round 1.

Stage 5 round 1 complete: all five reports find no major issue. Parent accepts three minor clarifications (two source-specific material labels and one unexplained abandoned inference). Separate correction agent assigned; see `stage5-r1-adjudication.md`.

Stage 5 corrections complete by the separate agent. Parent read the corrected entries and evidence mapping; all three accepted clarifications are implemented, the build is clean at 34 pages, and the four program chapters are unchanged. Stage 5 CLOSED. Proceed to the complete-manuscript review with five fresh independent reviewers.

## Complete-manuscript review and parent verification

Five fresh reviewers (`full_reviewer1`–`full_reviewer5`) independently read the whole manuscript, without access to earlier or peer review reports. Their emphases cover primary sources and originality, causal design, quantitative inference, scientific coherence, and presentation/build.

Parent reread all six sections. Reproduced the water source-series integration, imposed-water ratios, cyclic time and circulation thresholds, polymer catalyst-solid savings, and Ag reaction-level selectivity arithmetic. Checked all 42 bibliography keys and all cross-references for undefined or duplicate entries, inspected overview and shortlist renders, and checked whitespace/newline consistency of authored text artifacts. These checks do not validate proposed experimental outcomes.

Complete-manuscript round 1 complete. All five fresh reviewers report no major finding. Parent accepts eight consolidated minor revisions covering overview scope/terminology, a cyclic sequence map, water source-data and stability qualifications, polymer and Ag background explanations, and bibliography navigation. Separate correction agent assigned; see `full-r1-adjudication.md`. No repeated five-reviewer round is required unless verification exposes a major issue.

Complete-manuscript corrections completed by the separate agent. Parent read all revised passages and the correction mapping, checked the rendered sequence map and contents, and accepted all eight revisions plus the final plain-language and caption refinements. No new major issue arose; all accepted minor issues are resolved.

Final independent build from only `main.tex`, `references.bib`, and `sections/` succeeded in a fresh temporary directory: 34 pages, no warnings, and extracted text identical to the retained PDF. All 42 bibliography entries are cited, cross-references resolve, and README links exist. References navigation lands at the bibliography on page 31. All nine review rounds contain five separate reports (45 reports total); every round with accepted major findings was repeated after correction. The full-manuscript round found no major issue.

MANUSCRIPT COMPLETE. The final deliverable is a developed research proposal with verified analytical deductions and corrected source interpretations. Proposed experiments and practical advantages remain untested; review closure does not imply experimental validation or exhaustive novelty. All new repository artifacts are under `manuscript/`; the source literature library is unchanged.
