# Stage 1, round 1 — independent review 3

Reviewed frozen snapshot `process/snapshots/stage01-round01`. I read the entire
stage, including every proof and the bibliography, without consulting any other
current-round report. Emphasis: attribution, novelty boundaries, and source
versions.

## Verdict

**No major issues. Accept after one minor source-locator correction.** The
mathematical foundations are sound, and the manuscript correctly treats the
general disaggregation and shared-simplex gluing as known results. It does not
claim new general polynomial separation. The qualification about additional
side constraints is also correct and useful.

## Enumerated findings

1. **S01-R1-R3-01 — Minor: identify the electronic companion explicitly.**
   In `sections/01-foundations.tex:63–70`, the phrase “their Appendix,
   equation (25)” is followed by the statement that published-version numbering
   is used. Equation (25) is indeed correct, but in the published source it
   occurs on p.1 of the **Electronic Companion**, not in the main article.
   The bibliography URL points to the 24-page NSF copy of the published main
   article, which contains a cover sheet and 23 article pages and no appendix.
   The local literature original is a different, 31-page arXiv v2 file, whose
   Appendix on printed p.30 has equation (25). I independently opened the
   [published electronic companion](https://pubsonline.informs.org/doi/suppl/10.1287/moor.2023.0001/suppl_file/moor.2023.0001.sm1.pdf)
   and verified both the disaggregation and projection claims there. Change the
   locator to “their electronic companion, p.1, equation (25)” and provide the
   companion link in the citation entry or a source note. This is a local
   discoverability/version correction, not an attribution or mathematical error.

No other required corrections were identified. The present lack of detailed
contribution statements for future results is intentional at this stage.

## Mathematical checks actually performed

- Re-derived both directions of Proposition `prop:disaggregation`, including
  empty flow domains, zero individual weights, a zero residual weight, and
  `m=0`. Boundedness makes every zero-weight state flow zero; one positive
  weight excludes feasibility when the underlying flow domain is empty.
- Checked the reference-flow construction and the spanning-forest proof of
  Lemma `lem:block-factorization`. Fundamental cycles remain within cyclic
  blocks. Extending a block circulation by zero causes no hidden imbalance at
  articulation vertices. Loops, parallel-edge two-cycles, disconnected graphs,
  bridges, isolated vertices, and an empty family of blocks are handled.
- Reconstructed the proportional refinement in
  Theorem `thm:block-state-reduction`. Different blocks may merge different
  labels because refinement gives a common global weight for each state.
  Nonzero reference flows outside the capacity box cause no problem: the
  translated domains, rather than the reference alone, enforce capacities.
- Verified the stated linear scaled-block system at zero weight, the absence
  of extra conditions for unobserved blocks, and the bridge-product equations.
- Recomputed the common-matrix counterexample: both original intervals are
  `[0,1]`; the averaged rows permit `q=2`. The stronger homothetic-set identity
  used by the theorem remains exact, including a zero total weight.
- Checked the McCormick formulas, residual-flow bounds, and the warning about
  intersecting a hull with side constraints.

## Primary-source checks actually performed

- **Davarnia (2016), Proposition 2.6:** read the original dissertation pages
  28–30 using `pdftotext`, in addition to the local extraction. The proposition
  is the Cartesian shared-simplex gluing statement attributed here. Its
  separation from the 2017 journal citation is correct. The SIAM primary page
  independently supports the journal article's model and bibliographic data.
- **Khademnia–Davarnia:** inspected the local arXiv original, downloaded the
  open NSF published main article, and opened the published companion. The
  distinction between the complete projection framework and the restricted
  explicit forest construction is supported; the source itself says its
  pairwise-cancellation family need not be complete. The published main article
  and companion confirm the balance-inequality model.
- **Kis–Horváth (2022):** inspected the [open primary article](https://link.springer.com/article/10.1007/s10107-021-01652-z),
  especially Section 2, equation (7) and its following paragraph, and Section
  5.7. The common-matrix aggregation warning and transportation-projection
  comparison are accurately stated. Journal, year, pages, authors, and DOI match.
- **Almoghrabi–Skutella–Warode (2026):** inspected Theorem 1 and Remark 1 in
  the [open primary article](https://link.springer.com/article/10.1007/s10107-026-02392-8).
  The individual-commodity versus total-flow distinction is explicit there;
  the author names, DOI, and June 29, 2026 publication date match.
- Publisher pages support the stated broad roles and metadata of
  Liberti–Pantelides, Gritzmann–Sturmfels, De Loera–Onn, and Balas. I did not
  locate a metadata error among the entries checked. The references to
  classical mechanisms are appropriately restrained.

## Build and limitations

Built a private copy with the documented `latexmk` command. Exit status was
zero; the final seven-page build had no warnings, unresolved references, or
overfull/underfull boxes. Initial-pass citation warnings disappeared during
the normal reruns. The private build and machine-readable check record are in
`verification/reviewer3/stage01-round01/`.

This review did not re-audit every theorem in every classical reference, and
it is not a proof of literature priority. In particular, the future compressed
formulation, coefficient, and computational results are not present in this
snapshot and receive no implicit approval here. No manuscript files were
edited. Downloaded source copies and temporary extracts were removed after
inspection; the check record retains source URLs, locators, and the NSF file
hash.
