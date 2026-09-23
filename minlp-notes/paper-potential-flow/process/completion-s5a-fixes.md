# S5a correction record

The separate correction agent applied all three minor repairs accepted in
`completion-s5a-adjudication.md`. Manuscript edits are confined to
`complexity/sections/08-design.tex` and `complexity/references.bib`.

1. The independent-cycle proof now bounds scalar evaluation error by
   `sum_C |gamma_C| width(I_C)`. It specifies rational representatives
   within the endpoint enclosures, such as midpoints, and stops when the
   bound is at most the requested error. Refining every enclosure to width
   at most `epsilon / (1 + sum_C |gamma_C|)` is an explicit sufficient rule.
   The triangle inequality proves the bound for coefficients of either
   sign, including zero; the number of required precision bits remains
   polynomial. The exact optimizing parameter scenario is unchanged.
2. The same proof dispatches `B=0` before invoking the root theorem.
   Physical flows and reference circulations are zero, capacities become
   constant tests, and rational linear feasibility supplies admissible
   profiles in the cycle and variable bridge parameter polytopes. The
   connected edgeless case is included. The remaining proof explicitly
   assumes `B>0`, providing the required positive-width bracket.
3. The Ferrez–Fukuda–Liebling bibliography entry retains its published
   2005 journal metadata and DOI. Its URL now points to
   `https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf`, and
   its note identifies the April 29, 2004 author revision. The stale failed
   retrieval comment now records the lead's inspection of that revision
   and Section 3, PDF pages 4–6. The restrained predecessor statement is
   unchanged; this repair adds no literature or priority claim.

Before editing, all 15 manuscript input hashes matched the reviewed build
record. After editing, importing `verification/build_and_check.py` and
calling only `build('complexity')` rebuilt Paper A successfully. The
refreshed `completion-s5a-build.json` records all 15 input hashes and
confirms an existing PDF, return code zero, zero errors, zero undefined
references, zero undefined citations, zero duplicate labels, and zero
overfull boxes. The other 13 manuscript input hashes are unchanged.

The nine diagnostic scripts still match the hashes in the previously
passing `completion-s5a-checks.json`. They were not rerun because no
algorithm or diagnostic code changed. The arithmetic bound and zero-flow
dispatch were checked directly in their proof context. Earlier accepted
sections, the fixed-measurement extension and other new results, Paper B,
and the literature store were not edited. Existing uncommitted work was
preserved. No commit was made.

Final corrected freeze:

- `complexity/sections/08-design.tex` SHA-256:
  `b925b27dbe642e21ec7001d2e260d2f2b2622baadd28667d32c58a88c07e949b`
- `complexity/references.bib` SHA-256:
  `48544e93e84d7643fe9cd7366d1040983bc1664fb857fbea421451f46b075a13`

Authored or refreshed files are the two manuscript files above,
`process/completion-s5a-build.json`, and this correction record. The build
also refreshed generated outputs under `complexity/build/`.

Limitations: the build verifies document compilation, not mathematical
correctness. The previously recorded diagnostic limitations remain in
force. The source revision details rely on the lead's recorded primary
source inspection; the correction agent did not repeat that inspection.
Original Mignotte access limitations remain as adjudicated. Final stage
acceptance, coverage, and plan updates remain with the lead.
