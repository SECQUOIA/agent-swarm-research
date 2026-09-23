# Stage 1 author report

Stage 1 is complete and ready for five independent reviews. No subagents were used by this author; root will dispatch the reviewers after this report.

## Changed files

- `sections/00-introduction.tex`: rewrote the contribution statement, result map, significance and prior-work explanation. Added a compact comparison table. Made the distinctions between modulo-2π recovery and real zero winding, generic root counting and prescribed-set realization, and known general separation and the new electrical family explicit. Preserved singleton voltage/injection, angle, residual-box and gap-promise assumptions.
- `references.bib`: added Farivar–Low, Delabays–Coletta–Jacquod, Jafarpour–Huang–Smith–Bullo, Mareček–McCoy–Mevissen, and Bienstock–Del Pia–Hildebrand. Pinned Dynamic Toolbox to v1 because its broad universality statement is discussed.
- `revision-20260907/literature-audit.md`: detailed query/source/page/version record, with access and reading limits. Open-source caches and diagnostic images are under `revision-20260907/sources/`.

No core theorem, proof, checker, abstract, or conclusion was changed. Concurrent `paper-integer-dimension` edits were present in the shared workspace and were left alone. Literature packages and historical snapshots were preserved.

## Scientific assessment

The main contribution is the solution-preserving electrical arithmetic construction under simultaneous graph/data restrictions. It identifies existential-real completeness in a different physical subclass from earlier AC hardness and does not subsume tree hardness or establish a strict separation of complexity classes.

Adding the closest cycle/winding predecessors is a substantive correction to positioning. Winding flows, cycle consistency and uniqueness in monotone angular cells are established. The additional result is an explicit rational polynomial encoding with variable magnitudes and rational short-arc limits, followed by the stated complexity transfers.

Jeronimo–Perrucci–Tsigaridas already give a repeated-power separation example. Our electrical fixed-data realization and the actual gadgets' residual transfer are the additional developments. Short rational certificates under a supplied gap promise come from a direct bounded-quadratic rounding argument, now presented as a supporting certification result.

Dynamic Toolbox v1 asserts rational universality for arbitrary compact semialgebraic sets using rational coordinate homeomorphisms. The manuscript proves a basic-closed invariant and supplies an explicit nonbasic compact example. The introduction now explains why the conjunction-only proof is needed, while triangulation gives topological universality separately. It does not rely on the source's Boolean preprocessing.

## Verification

Read foundations, algebraic and numerical sections in full, and inspected the arithmetic appendix plus relevant AC/structural statements to align the introduction with theorem scope. This is not a new proof-by-proof verification of every gadget; that belongs to Stage 2.

Conducted fresh web searches and inspected primary local/source texts as detailed in the audit. Visually checked the original JPT repeated-power example where extraction loses exponent structure.

The corrected build command from `paper-power-flow`, `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`, succeeded: 30 pages. Final log `revision-20260907/stage1-build.log`. No unresolved references, citation warnings, or overfull/underfull box warnings appeared. Visually inspected the table page, which fits cleanly. An initial invocation from repository root failed because there was no `main.tex` there; the corrected invocation succeeded. An initial report-write command similarly used doubled relative paths; no manuscript changes were lost, and reports were then written from the proper directory.

No new tests are warranted for prose/bibliography changes. Root reports running the existing exact-arithmetic suites separately.

## Next-stage review targets

These are targets for the planned development stages, not identified counterexamples:

1. Recheck gadget ranges, unique extensions, bounded planar crossover, degree/size counts, connectors, subdivision and residual constants. In particular, the imported planar source uses a promise formulation, so the manuscript needs its own bounded solution-set proof.
2. Check the AC encoding at branch boundaries and unequal magnitudes. Root has identified a potential simplification using real vertex potentials instead of a fundamental-cycle list; incidence-potential algebra is not a novelty claim.
3. Verify or qualify the JPT locator in the numerical section: local arXiv Theorem 1 versus cited journal Theorem 1.1.
4. Add the new winding lineage near the Section 4 statements if appropriate for readers starting there; it is already explicit in the introduction.
5. Replace legacy experiment/internal chronology language with standalone illustrative examples and reproducibility statements during final synthesis.
6. Align abstract and conclusion after the core scientific review. Preserve the distinction between the ordinary residual family and the simultaneously planar/unit-conductance theorem.

No unresolved mathematical contradiction was found during this stage. The evidence supports precise, qualified contribution claims and does not prove exhaustive publication priority.
