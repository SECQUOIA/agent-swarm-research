# Primary-source verification for stage 5

The author accessed these primary sources on 2026-09-07. PDFs were downloaded
to a temporary directory for checking and are not redistributed.

- Bestehorn and Kirches, *The integrated control deviation of mixed-integer
  optimal control problems with vanishing constraints*, PAMM 20(1),
  e202000022, DOI `10.1002/pamm.202000022`. The PDF labels the volume 2020
  and copyright/publication 2021; the bibliography explicitly records this
  distinction. Open PDF: https://d-nb.info/122645075X/34.
  SHA-256 `3a271643ad4346f8065cea5262046faf509b097e15e014a7291c599fa2a094ad`.
  The author read the formulation and matching construction on pp.1–2 and
  checked Corollary 2.7 on p.2: an equidistant-grid rounding preserves positive
  cell support and has error at most the cell width. The following paragraph
  proves sharpness of that unrestricted support-rounding constant. The paper
  here credits that established ingredient and separately proves temporal
  subsequence preservation and the sharp instance-optimum gap under a switch
  budget; no priority claim is made for matching rounding.

- Bestehorn, Hansknecht, Kirches, and Manns, *Mixed-integer optimal control
  problems with switching costs: a shortest path approach*, Mathematical
  Programming 188, 621–652 (2021), DOI `10.1007/s10107-020-01581-3`.
  The publisher page https://link.springer.com/article/10.1007/s10107-020-01581-3
  verifies the volume, pages, authors, and issue year, with online publication
  on 2020-10-24. The open final article is https://d-nb.info/1223084523/34.
  Section 1.1 states the exact DAG algorithm and the bound
  O(N(2 theta+3)^(2M)), where its M is the number of modes. It also explicitly
  discusses adaptations for minimum dwell, vanishing constraints, and CIA
  objectives. The manuscript does not claim the first exact CIA dynamic
  program or the first treatment of dwell constraints.

- Zeile, *Combinatorial Integral Decompositions for Mixed-Integer Optimal
  Control*, doctoral thesis, Otto-von-Guericke-Universität Magdeburg (2021).
  Open PDF: https://mathopt.de/publications/Zeile2021a.pdf.
  SHA-256 `63a4ef7d16df0fbbaa6093a9e350018b681c622e101901965ad9dd5d8099c4b3`.
  The title and submission year were checked on the title page. Section 6.4.3,
  printed pp.78–80 (PDF pages86–88), gives switching-time branch and bound;
  Remark 6.3 immediately preceding it on p.78 counts word/time possibilities.
  This is credited as prior enumeration. The paragraph immediately before
  Conjecture 7.1 on printed p.139 (PDF page147) argues for a half-maximum-width
  instance correction by moving each switch independently. The manuscript's
  counterexample addresses that argument, not a proved transfer theorem.

- Sager and Zeile, final published article, DOI
  `10.1007/s10589-020-00244-5`, publisher PDF
  https://link.springer.com/content/pdf/10.1007/s10589-020-00244-5.pdf.
  SHA-256 `f4dfdfdc761de38dafeea5dd9eafb5bbf3c637a39dc7ee2ff1432a9803996770`.
  Printed p.615 (PDF page41), paragraph immediately preceding Conjecture 1,
  gives the same half-mesh argument for continuous versus grid instance
  objectives. The author checked the complete paragraph and conjecture
  hypotheses. The four-mode/five-cell/three-switch example satisfies the
  stated budget range and has an instance gap at least 9/16 on a unit grid.
  This source interpretation is separate from the finite-grid minimax
  corrections recorded in stage 4.

This is a targeted attribution and source audit, not an exhaustive claim of
publication priority for the specialized algorithm or coarsening consequence.
