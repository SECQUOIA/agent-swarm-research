# Stage 1 author record

Date: 2026-09-07. Author agent: `paper_author`. Status: authored and locally
checked; awaiting the required five independent reviews.

## Scope completed

- Compilable article skeleton, introduction, abstract, notation, and references.
- Complete proof of the known exact simplex disaggregation, including empty
  flow domains, zero state weights, and a decomposition using at most `m+1`
  graph points.
- Complete circulation-space factorization proof using a fundamental-cycle
  basis. The proof covers articulation vertices, bridges, disconnected graphs,
  parallel edges, and independent self-loops.
- Complete block-local state-merging theorem with an explicit global-state
  refinement formula. The theorem retains all scaled domain bounds and does
  not merge observed slices.
- A short counterexample explaining why a shared constraint matrix alone
  does not justify right-hand-side aggregation.
- Explicit model and interpretation limits: equality balances, finite rational
  nonnegative capacities, residual state, sparse original coordinates, ambient
  cycle rank, arithmetic versus bit complexity, and intersecting side
  constraints after convexification.

The introduction and abstract are deliberately short. Stage 7 will replace
them with a synthesis of the accepted complete manuscript. This is recorded
here rather than displayed as a TODO in the paper. Later stages will add
separate section inputs; no empty sections appear in the compiled paper.
Author metadata is empty because the user's name and preferred authorship
statement have not been supplied for this manuscript.

## Source coverage and attribution

Read the paper-readiness record, reopened literature audit, compressed-hull
proof, reaggregation boundary note, original cycle/theta and parallel-path
results, and the general universality construction. The other accepted
developments are mapped for later stages in the root's `coverage.md`.

| Source | Verification and use |
|---|---|
| Khademnia–Davarnia 2025 | Read local full text, Appendix equation (25), and the audited version distinction. Checked arXiv metadata. Cite the published article and its numbering. The full EC&R projection is not portrayed as merely a restricted forest family. |
| Davarnia–Richard–Tawarmalani 2017 | Checked the SIAM primary article page and local metadata. It is cited for simultaneous convexification generally. |
| Davarnia dissertation 2016 | Read the local original's title and Proposition 2.6, printed pp. 28–29. Added a separate thesis BibTeX entry; the local package's article metadata is not used for the proposition locator. |
| Kis–Horváth 2022 | Opened the primary article. Its publication record distinguishes online 2021 and volume-year 2022. Network Cayley hulls, transportation projection, and the Section 2 reaggregation boundary are credited. |
| Liberti–Pantelides 2006 | Checked primary publisher metadata and abstract; used the existing theorem-level literature audit. The current section makes only the supported broad reduced-RLT comparison. An attempted direct thesis PDF open failed; no new theorem locator is asserted from that failed retrieval. |
| Gritzmann–Sturmfels 1993 | Read local metadata and the repository's source locators for normal fans and zonotope refinement. Cited as a classical ingredient, without redistributing the user-supplied PDF. |
| Onn–Rothblum 2004 | Checked the open arXiv primary record and local source summary. Cited for edge-direction geometry only. |
| De Loera–Onn 2006 | Checked SIAM primary DOI/title record and existing transportation proof. The detailed coordinate-preserving transfer is reserved for Stage 5. |
| Alon–Vu 1997 | Checked primary ScienceDirect search result, volume/pages/title and DOI `10.1006/jcta.1997.2780`; cited only as the classical large-coefficient background. |
| Almoghrabi–Skutella–Warode 2026 | Checked the primary open article and online-publication date. The precise relevant comparison is Remark 1's aggregate-versus-individual-flow distinction. No volume/page numbers are invented for the online article. |
| McCormick 1976 | Checked primary Springer record. Correct first page is 147; some secondary/local bibliography entries give 146. |
| Balas 1998 | Checked local DOI-matched article metadata. Cited for disjunctive hull formulations. |

The nearby chance-constraint simplex framework is not needed for these
foundations and is not cited. The root notes that its current local copy is
arXiv 2510.15861 v2; any later comparison must use that version explicitly.

## Author verification

The full proofs were reconstructed for this paper rather than copied:

1. In the disaggregation converse, zero-weight flows vanish because capacities
   are finite; at least one positive weight proves the empty-domain case.
2. The block split follows from fundamental cycles, each contained in one
   cyclic block; the converse verifies incidence at articulation vertices.
3. A reference flow need not be capacity-feasible. Block domains are shifted
   and may omit zero; the state proof uses `f^k - lambda_k v` consistently.
4. The local merged weight is the sum of exactly those global weights being
   refined. If it vanishes, all constituent weights vanish. Different block
   partitions are compatible because circulation coordinates are independent.
5. Bridge bounds and products are enforced separately. Blocks with no observed
   labels impose exactly their existing domain constraints.
6. In the counterexample both component polytopes are `[0,1]`, while their
   averaged rows permit `q=2`; this is a known limitation, not a new result.

Build command, run from the manuscript directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The final author build exits successfully and produces a seven-page PDF.
The log has no undefined references/citations, LaTeX warnings, or overfull
boxes. `verification/stage01-validation.json` records source hashes and build
checks. No numerical experiment is used as a substitute for the proofs, and
no independent review is claimed before the five-reviewer stage occurs.

## Remaining uncertainty

No unresolved mathematical issue was identified in this stage. The usual
bounded-literature-search limitation remains: these foundations are explicitly
credited as established material, and later structural novelty claims need
their own precise comparisons. No claim of manuscript completion is made by
this stage alone.
