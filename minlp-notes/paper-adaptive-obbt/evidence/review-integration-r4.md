# Focused final integration review, round 4

**Accepted.** The requested minor prose fixes and software citations are closed in the snapshot recorded at **2026-10-06 03:32:51 UTC**. No remaining material claim, attribution, or front-to-body mismatch was found in this scope. The earlier independent mathematical reviews remain the basis for accepting the underlying results.

I read the Opus round-2 recommendations, the changed passages and their theorem context, both approved bibliography supplements, and the final software audit in full. The original 37-source scientific audit is unchanged from the accepted round-3 snapshot. This review uses the literature lead's evidence; it does not independently retrieve sources or establish publication priority.

| Finding | Closure in the reviewed sources |
| --- | --- |
| N1, Coffrin wording | The paragraph uses the lead's checked description: feasibility-based bound consistency without an incumbent objective cutoff. This review uses that precise scope when assessing the prior-work relation. |
| N3, Belotti attribution | Foundations now jointly cites the published 2010 chapter and the read 2012 manuscript, as the scientific audit requires. Their bibliographic status remains distinct. |
| N5, software and test set | All nine approved software and benchmark keys are merged and cited in the evidence section. The Suite 10.0 report, recorded software stack, and release-specific default settings have separate appropriate sources. |
| N6, moved proposition | The constraints section points to the contraction subsection, and the local-theory roadmap identifies the restricted tangent contraction as its closing result. |
| N7, stall summary | The discussion states the general negative face-witness condition, sufficiently small scales, and cutoffs at least the optimum. It separately cites the exact quadratic row criterion for fixedness at every scale. |
| N8, singleton bound | Introduction and local rates now say that the bound is exact **if** the iterates converge to the protected singleton. They do not assert an equivalence. |
| N9 and N10, introductory summaries | The upper-order bounds motivate reconsideration after an incumbent improves; exact shrinking orders are confined to the model example. The introduction now identifies three limits on further tightening. |
| N11 and N12, numerical interpretation | The maximum is reported as at most 1.00501 seconds. Number-zero callbacks are the recorded category in the text and table; the probing interpretation remains an explicitly qualified inference. |
| Optional N4, Collatz–Wielandt terminology | Retained with a self-contained definition and elementary comparison proof. The manuscript does not claim a new general spectral theorem or rely on an unstated external theorem. |

The additional cost-paragraph correction is also closed. Both discussion and evidence now report the extra callbacks and pilot-stop counts without attributing the extra callbacks specifically to early stopping. The explicit limit on causal conclusions without ablation remains. The author-name accent and bibliography process-note issues found during this review were corrected: João Pedro is preserved, the Suite report is identified neutrally as an arXiv preprint, and the PySCIPOpt source-version note is bibliographic.

The paper contains **46 unique bibliography keys**, exactly the union of the approved 37 scientific and nine software keys. There are no missing, duplicate, or extra keys, and all nine software keys resolve and are cited in the reviewed evidence section. The scientific entries retain the three previously accepted presentation changes. The four software entry differences are harmless: formatting the MINLPLib overview's date/hash, marking the Suite report as a preprint, using Unicode for the corrected PySCIPOpt author accent and shortening its submitted-version note, and shortening the Gurobi versioned-documentation note. Bibliographic identities agree with the approved records.

The final software audit supports the three pinned SCIP defaults: LP-based OBBT at the root, nonlinear OBBT disabled, and generalized variable bound propagation enabled. The paragraph attributes these to **v10.0.2**, rather than to the Suite 10.0 report or to OBBT in general. All three source entries now have year 2026, consistent with the audit's verified April 2, 2026 release timestamp. The Suite report remains a 2025 preprint. The text assigns neither an unrecorded HiGHS version nor a Gurobi patch version; installed versions remain archived environment facts rather than facts inferred from the older software articles.

The software audit leaves one qualified gap: the immutable historical MINLPLib snapshot underlying the precursor cohort was not identified. The added MINLPLib citations identify the collection and current overview; the cohort counts remain facts from the archived study. I found no claim that the 2003 paper or current overview verifies that historical inventory. This acceptance does not clear its exact database lineage. The scientific audit's previously disclosed access limits also remain in force.

Checks actually performed were targeted reads with `cat`, `sed`, and `rg`, Python bibliography/key and SHA-256 comparisons, and a targeted comparison of proof and displayed-math blocks in the six prose-edited files against the retained Opus round-2 ZIP (SHA-256 `6c72defff87757048136b0e304b9ffa3116153c1f9aa157a3c708897682b6521`). Those blocks were byte-identical. I did not repeat the parent agent's later full environment/package checks. I performed no experiment, build, project-wide verification, CI inspection, or independent literature search, and edited only this report.

Reviewed SHA-256 identities follow; paths are relative to `paper-adaptive-obbt`.

```text
f75cb5164d64ebc45ae450352fab170a68e99c1199589cc9f369ca02ea4fea4d  abstract.tex
65804b25d528c8fb9ff4048c8f288e95e7cade9474d5f8db50106837e71f3878  references.bib
e06be0f0ff6a7c59c643196e7a973aac1f607f8609170cbad691d97b6393805a  sections/introduction.tex
b66cbbf71454523877ee7e62234c479ab221b871338ebf2022c7c5c265c605d3  sections/related.tex
aaf522d28bf81036fa538d50183a7c98827b049ffbec03c71ba38db07c143edb  sections/foundations.tex
8f2c7d6fc44054e67a826c49969caf2786571fa47ea5fe0a8d4095eb8987b2bb  sections/local-rates.tex
1506f7c8e0e765ec0694edab086c5dd2ac424f596b891dff6e43559efa6feee7  sections/constraints.tex
0163c7386f68777249e083990a218ea49e277b4f24675e9584a16af4541113d8  sections/discussion.tex
7a483f55a61e0be6fe35266b70922cafebbae3b8f93321830e0d87cd211e5525  sections/experiments.tex
a7dd809513f3eb9b2a23695a3327bd99c1a64de610eb5417ef679a18c0611c61  appendices/precursor-study.tex
5ffcc29f326ad1b5a5d724b32acd7dbd276449accc4b2e77a541115ef51a0ac9  evidence/literature-references.bib
3a109aebf9c7c03959083abd6da9b0ba2438c283cbe8f213b0c24502807a9aa8  evidence/literature-audit.md
67012ffe7e76de23cc812bcb0ebd7d6bf367aca9480c08948778afb694b554a7  evidence/literature-software.bib
e492bb3d1f2128a5ff9eda96dc6785dc649e442f61ab271010a7c8a251b12ddf  evidence/literature-software-audit.md
```
