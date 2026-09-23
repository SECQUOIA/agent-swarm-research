# Stage 1, round 1, independent review 2

Verdict: **pass with one minor attribution clarification; no major issue found**.

Scope: foundations, source inventory, literature evidence, and scaffold. I did
not treat absent proofs, consequences, an abstract, or submission metadata as
defects because those belong to later stages. I did not read other reviewers'
reports or edit the manuscript.

## Findings

### Minor: distinguish the original dimension conventions from the paper's extension

- Location: `sections/01-setting.tex:79`–95, with the global convention at
  line 4 and the background attribution at lines 105–106.
- Reason: the manuscript works with all `n,m >= 1` and labels the resulting
  question directly as BDS Conjecture 3.3. BDS arXiv v2 introduces its system
  with the standing restrictions `n >= 3, m >= 2` on PDF page 3. Its diagonal
  Theorem 2.12 explicitly assumes `n >= 2`. The mathematics being proposed is
  not wrong, but the attribution presently obscures that the dimension-free
  formulation is the present manuscript's extension of the cited setup.
- Fix: add a short sentence after the conjecture explaining BDS's standing
  dimension conventions and that the present formulation includes the smaller
  dimensions. Qualify the diagonal attribution by the cited theorem's
  `n >= 2` restriction, or explain separately that `n = 1` is elementary.
  This is an attribution precision issue, not a request to restrict the new
  theorem.

## Findings that support acceptance

- The exact BDS version is handled carefully. Its current arXiv record has
  only v1 (October 4, 2022) and v2 (May 29, 2023); the manuscript's v2
  locators match Definition 2.1, Theorem 2.9, Theorem 2.12, Proposition 2.14,
  and Conjecture 3.3 in the downloaded primary text. The conjecture's
  negative-constant formulation is equivalent to the manuscript's
  `(A_lambda,b_lambda) != (0,0)` under the stated strict feasibility.
- The distinction between globally convex certificates and good
  aggregations is correct, including the latter's eigenvalue condition,
  hull containment, and the `n >= 3` restriction on the cited hull theorem.
- The elementary reverse direction is valid: a nonconstant convex quadratic
  cannot be strictly negative everywhere. The homogeneous scaling,
  hyperplane notation, HHC definition, and implication to hidden convexity
  for domain dimension at least three are correct.
- BDS already covers the no-PSD-multiplier case under convexity of the image
  on `t = 0`. The manuscript accurately isolates the unresolved all-trivial
  multiplier case and credits the diagonal and two-constraint cases.
- The Blekherman–Dunbar full text inspected here addresses three-quadratic
  hull descriptions, spectral conditions, and finiteness; it does not state
  a resolution of Conjecture 3.3. The arXiv record still supplies v1 only.
  The stage correctly distinguishes this accessible version from its 2025
  journal publication and does not invent journal theorem locators.
- The DMS introductory discussion and Theorem 2.4 support the manuscript's
  restrained prior-work account. They also independently confirm Yildiran's
  two-aggregation result. The manuscript does not attribute novel status to
  the two-form result, a classical cone-separation lemma, or the classical
  aggregation/SDP connection.
- The record appropriately bounds the online search and leaves source
  followups concerning Polyak, Sheriff, and the delicate SDP closure issue
  for the stages that will actually use those results. None is imported as
  an unverified theorem in the stage 1 manuscript.
- The coverage inventory includes the corrective audit and explicitly
  retires the invalid complete-hull and numerical-certification claims.

## Independent checks and evidence

- Read all current manuscript source files, `PROCESS.md`, the author report,
  coverage map, and literature record.
- Used targeted `rg`/`sed` reads of the canonical result and earlier review
  note, the BDS v2 extraction in
  `/tmp/quadratic-paper-literature/bdsv2.txt`, the Blekherman–Dunbar primary
  extraction in `/tmp/quadratic-paper-literature/bd.txt`, and the local DMS
  journal extraction.
- Independently opened the primary arXiv records:
  <https://arxiv.org/abs/2210.01722> and
  <https://arxiv.org/abs/2405.18282>.
- Ran targeted web searches for `"hidden hyperplane convexity"
  "Conjecture 3.3" solution` and `"quadratic" "Blekherman" "Dunbar"
  "2026" convex hull`, as well as the Yildiran title. These found no
  subsequent resolution. This remains a bounded search, not proof of
  priority. The author-maintained Blekherman page
  <https://sites.google.com/site/grrigg/> lists the 2025 Blekherman–Dunbar
  publication consistently with the bibliography.
- Attempted an Oxford abstract URL for Yildiran; that particular request
  failed. I do not represent it as an independent full-text verification.
  The primary DMS and BDS discussion corroborates the limited claim used.
- Ran `rg -n 'Warning|Overfull|Underfull|undefined'
  paper-quadratic-aggregation/build/main.log`: no matches (exit 1, as
  expected). I inspected the existing topic build log, not CI; I did not
  rerun the build or run project-wide verification.

No other correction is requested for stage 1. The absence of a significant
stage 1 issue is not a correctness verdict on the later proofs.
