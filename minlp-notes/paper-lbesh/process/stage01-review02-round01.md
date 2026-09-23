# Stage 1 independent review 02, round 1

Reviewer: `/root/reviewer02`. Date: 19 September 2026. Scope: all authored Stage 1 manuscript/scaffold material, with emphasis on primary-source literature and novelty. Later comment-only sections are intentionally outside this stage. No other reviewers' reports were consulted and no manuscript source was edited.

## Verdict

**Pass after two minor corrections; no major issue identified.** The manuscript makes a defensible, deliberately narrow empirical contribution. Its mathematical identities and literature distinctions in this stage agree with the checked primary sources. I found no evidence that the present contribution framing improperly claims a new cut family or first combination of ESH and disjunctions. The absence of broad algorithmic novelty is an explicit and appropriate scope decision, not a defect requiring artificial novelty claims.

## Major findings

None in the completed Stage 1 scope. Theorems, implementation correctness, raw-data reconciliation, and eventual submission completeness remain later-stage obligations rather than defects in these intentionally bounded sections.

## Minor findings requiring correction

1. **Add the directly relevant SHOT implementation paper to the related-work discussion.** Locations: `sections/related-work.tex:15`, `:29`, and `:34`; `references.bib` currently has no SHOT entry; `evidence/literature.md:7–23` omits it. Lundell, Kronqvist, and Westerlund, *The supporting hyperplane optimization toolkit for convex MINLP*, Journal of Global Optimization **84**, 1–41 (2022), DOI [10.1007/s10898-022-01128-0](https://link.springer.com/article/10.1007/s10898-022-01128-0), documents both ESH and ECP, single-tree callbacks, fixed-integer primal heuristics, and ECP fallback when a strict interior is unavailable. Section 7.2.4 also compares single- and multiple-tree execution. This is unusually close implementation context, and SHOT is an actual baseline in this repository, so it deserves more prominence than unexecuted current software documentation. A short paragraph or a few sentences plus a bibliography entry suffice: explain that the present comparison retains GDP term structure and isolates separation policies under matched settings. Do not imply the SHOT article already supplies this exact GDP experiment. This omission does not invalidate the carefully qualified contribution and is therefore minor.

2. **Name the timing statistic.** Location: `sections/introduction.tex:12`, “Common-solved timing averages favor ESH by approximately 4--6%”. The source result is a ratio of one-second-shifted geometric means of end-to-end wall time, not an unspecified ordinary average. Replace “timing averages” with “shifted geometric mean wall times” (the exact shift may be defined in the later experimental section). `notes/lbesh-study-results.md:93–105` supports this wording and gives single-tree ratios 0.941 (hull) and 0.957 (big-M). This is a clarity correction, not a numerical contradiction.

## Primary-source checks and accepted distinctions

- Checked the local Bestuzheva–Gleixner–Vigerske primary manuscript, section 3, Theorems 1–2. The stated equivalence between affine extension and perspective cuts is supported; the manuscript correctly refrains from calling original-space coefficient construction new. The displayed perspective tangent also follows directly by differentiating the perspective at positive weight.
- Read Kronqvist–Misener's [author manuscript](https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf), especially sections 2.2–3 and equations (11)–(13). Its normal is fixed while separate convex problems determine term coefficients. The distinction from term-specific radial tangents is accurate, and the draft correctly makes no dominance assertion.
- Checked Serrano–Schwarz–Gleixner's [publisher article](https://link.springer.com/article/10.1007/s10898-020-00906-y), sections 4.1–4.4, including the gauge construction and the discussion of representation-dependent numerical residuals. The related-work description is appropriately narrow.
- Checked the local Coey–Lubin–Vielma primary fulltext for conic separation, certificate scaling under numerical tolerances, and solver-driven implementation. The manuscript appropriately distinguishes the supplied exact-cone checks from an executed general conic-OA solver comparison.
- Checked the [Bernal Neira–Grossmann publisher record](https://link.springer.com/article/10.1007/s10589-024-00557-9) for the 2024 publication and broader cone-representable scope. The caution that nonquadratic does not imply nonconic is justified.
- Checked [Gusev–Bernal Neira v2](https://arxiv.org/html/2508.16093v2), including section 3.2's CEHR. The cited formulation and the distinction from earlier versions are correct. With positive weight, eliminating the lift yields the quadratic perspective inequality; scaled bounded-domain closure handles zero weight.
- Checked [Nguyen–Pulsipher v1](https://arxiv.org/abs/2608.27707v1) title/authors/date and abstract. The limited adjacent-work description matches its generalization of GDP methods to infinite-dimensional problems.
- Checked current official [discopt MIP–NLP documentation](https://kitchingroup.cheme.cmu.edu/discopt/mip_nlp.html), including GDP reformulation selection and SHOT-style ESH options. The manuscript does not improperly treat that documentation as peer-reviewed priority or benchmark evidence.
- Checked the SHOT article directly on its publisher site, including metadata, sections 2, 4.4, and 7.2.4, yielding minor finding 1.

## Actual verification and limits

Read `main.tex`, `README.md`, `references.bib`, both authored section files, both evidence maps, and the Stage 1 author report. Inspected relevant local primary fulltexts, the existing literature assessment, and study-results passages supporting the introductory claims. Conducted web searches combining “extended supporting hyperplane” with GDP/disjunctive and with ECP, then followed primary publisher, author, arXiv, and official documentation sources. A publisher fulltext request for the adjacent projected-cutting-plane paper returned an internal error; I draw no scientific conclusion from the inaccessible paper.

No full raw-data audit, optimizer run, LaTeX build, project-wide check, or CI inspection was performed. The author has already reported the targeted Stage 1 build; duplicating it would not add distinct confidence to this literature review. I did not exhaustively re-fetch metadata for every older foundational citation and found no contradiction among the metadata actually checked.
