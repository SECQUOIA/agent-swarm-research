# Stage 3 integration and submission preparation

Stage 3 author work is complete and ready for the required five independent reviews. No subagents were used by this author. The separate whole-manuscript review gate remains after Stage 3 acceptance. No author identity, affiliation, funding statement or submission declaration has been invented; author metadata remains blank pending the user's details.

## Integration changes

- Rewrote the abstract around the solution-preserving electrical construction and the main simultaneous graph/data theorem. It now explicitly states independent voltage and injection intervals with simultaneous singletons, separates real angles from principal-angle winding, advertises the accepted quadratic linear-count ETR encoding, and distinguishes the ordinary residual family from the planar universality construction.
- Updated the introductory result map with the proved linear variable/predicate/monomial counts, retaining polynomial bit length and the accepted prior-work qualification. Preserved the carefully reviewed literature positioning and bibliography; no new priority claim or new mathematical dependency was introduced.
- Revised the conclusion to distinguish the new electrical realization from established arithmetic/topological tools, carry the operating assumptions into the takeaway, and state the ordinary residual scope and separate AC transfers accurately. Incorporated root's precision improvement: other operating models may exclude the prescribed voltage/injection combinations used by the reduction.
- Made the final membership-proof sentence explicitly refer to crossing variables and vertex shifts. No theorem statement or mathematical proof content was changed.
- Removed repository chronology, old winding-suite references, and the unrerun solver anecdote from the verification appendix. Retained the four portable current checkers, verified counts, and eight self-contained analytic source examples, with a direct exact AC consequence. Renamed the table label and subsection accordingly.
- Replaced the repository-oriented README with standalone source/build/check instructions and verified coverage counts. Documented the local sibling import and the requirement to run with assertions enabled (no `-O`/`-OO`, `PYTHONOPTIMIZE` unset), as root requested.

Read the current manuscript, appendices, Stage 1/2 author reports and adjudications, and status record for cross-section consistency. Preserved the accepted mathematical results, definitions, proofs, model restrictions, all other paper folders, and historical snapshots. The existing order remains coherent: ordinary electrical realization; AC definitions and transfers; stronger structural realization; algebraic implications; numerical implications; conclusion; full arithmetic proof and exact-check supplement. No speculative extension or new development was necessary for integration.

## Submission artifacts and provenance

- `build/main.pdf`: final integrated 31-page manuscript.
- `submission.zip`: 18 entries: `main.tex`, `macros.tex`, `references.bib`, `README.md`, eight section sources, two appendix sources, and four exact checkers. No PDF, cached literature, primary-source PDFs, review records, build artifacts, or external repository dependencies are included.
- `stage3-manifest.json`: exact SHA-256 of every archived file and the archive, the isolated extraction directory, and assertion-mode environment evidence.
- `stage3-validation.json`: resolved reference/citation counts, manuscript hygiene and build diagnostics, extracted/source hash comparison, and current compiled PDF hash.
- `stage3-layout/`: all 31 page renders and three contact sheets. `stage3-layout.txt` contains the full PDF text extraction.

The bundle was extracted to `/tmp/power-flow-submission-eg1j676p` and built there from source. After final prose-only precision changes, the bundle was regenerated, extracted sources refreshed, their hashes compared with the final source manifest, and the isolated build rerun. The checker bytes were unchanged by those final edits; their successful isolated runs remain valid.

## Actual validation

1. Local and isolated source builds both succeeded using the README's exact `latexmk` command. Final TeX logs have no warnings, overfull/underfull boxes or unresolved references/citations. Logs are `stage3-build.log` and `stage3-isolated-build.log`.
2. All four checkers succeeded from the extracted bundle, with Python assertions enabled and `PYTHONOPTIMIZE` unset. This one rerun was justified by standalone portability, not by changed mathematics. Logs are `stage3-isolated-resistive.log`, `stage3-isolated-ac.log`, `stage3-isolated-developments.log`, and `stage3-isolated-arithmetic.log`. Counts agree with the revised README/appendix, including 4,166 vertex-shift cases and 1,090 consistent cases.
3. Citation/reference scan found 97 unique labels, no duplicate/unresolved labels, 20 cited bibliography entries, no missing citations and no uncited entries. The manuscript scan found no TODO/FIXME/placeholder, legacy/repository/worktree, or stage/reviewer prose. `git diff --check -- .` passed within the paper directory.
4. Visually inspected all 31 pages using three contact sheets. Inspected enlarged pages 1, 3, 7, 11, 15, 16, 22, 24, 25, 27, 29, 30 and 31, covering the title/abstract, comparison table, gadget table/figure, winding proof, crossover, planar-data table, dense numerical displays, conclusion, arithmetic chains, exact examples, and bibliography. All fit inside margins, with readable figures and equations, resolved hyperlinks and no clipped text or misplaced section heading. Normal theorem/proof continuations across pages remain.

An initial README write used a duplicated relative directory and failed without changing the source; the corrected write succeeded. PyMuPDF was unavailable, so rendering used the installed `pdftoppm` plus Pillow instead. The first log scan matched the harmless package description `info/warning/error`; narrowing to actual diagnostic prefixes left no build warning. These tool-level corrections do not affect the final deliverables.

The literature foundation and mathematical verification remain those accepted after Stages 1 and 2. This stage supplies integration and portability evidence, not external peer review, formal proof certification, or proof of exhaustive publication priority.
