# Stage 6 independent review 2

## Assessment

No major issue found. One minor wording issue should be corrected before
accepting the integration. The abstract, contribution table, introduction and
roadmap otherwise preserve the locality and approximation theorems' actual
quantifiers, dimensions, representation requirements and singular-information
scope. This is an integration review, not the separately required final
whole-manuscript review.

## Finding R2.1 — minor: distinguish decay assumptions from the abstract cover assumptions

**Location:** `sections/06-discussion.tex:69–80`, especially lines 73–75.

After summarizing both weighted trace and the fixed-dimensional nonlinear
cover, the discussion says: “Complete packets, rational representation, and
fixed decay promises are essential parts of these statements.” This merges
the hypotheses of two different results. The abstract additive graph and
represented-matroid cover theorems impose no covariance-decay assumption and
do not require a temporal packet interpretation. Complete packets and fixed
decay promises belong to the correlated temporal FPTAS and its transfer
corollary. The introduction and technical sections correctly distinguish these
scopes, so this is a local clarification rather than a mathematical gap.

**Remedy:** State separately that the correlated temporal schemes require
complete packets and the stated fixed promises, whereas the abstract additive
cover requires fixed information dimension and the specified explicit rational
feasibility representation. Preserve the following warning about grid
refinement and the explicit prohibition on transferring arbitrary matroid
constraints to correlated histories.

## Checks supporting the assessment

- Read the entire new abstract/introduction, contribution table and
  discussion/conclusion, the Stage 6 author report, manuscript README,
  supplement README, and both relevant source-provenance instructions.
- Read all of `sections/03-approximation.tex` and the scalar-predecessor and
  represented-matroid proof appendix. Checked the introduction's all-target
  quantifier against the actual normalization/profile construction: one
  returned actual object approximates each target in both directions; exact
  kernels are retained; a fractional mixture is not substituted for that
  object. The forced-owner normalization, exact range filters and signed
  floor profiles substantiate the reported guarantee.
- Checked the four locality theorem hypotheses and their interface with the
  trace FPTAS. The introductory weighted-trace claim allows input-sized packet
  and parameter dimensions only under the stated fixed promises. Its exact
  count, mandatory/forbidden and minimum-spacing summary matches the explicit
  counter/history graph. It does not imply a polynomial algorithm for arbitrary
  binary budgets. The partial-packet wording does not claim full latent-state
  observation or positive definite latent covariance.
- Checked the spectral consequences and matroid scope. Fixed information
  dimension, rational PSD atoms, an explicit acyclic graph or characteristic-zero
  rational matroid representation, exact feasible objects and exact singular
  ranges are all retained in the new introduction. No independence-oracle,
  finite-field, matroid-intersection, arbitrary correlated-matroid, or
  dimension-independent polynomial-exponent extension is claimed.
- The abstract's criterion list agrees with the separate determinant,
  minimum-eigenvalue, inverse-trace and estimable-contrast conclusions.
  Multiplicative determinant information is not relabeled as a multiplicative
  log-determinant guarantee. The introduction properly distinguishes PSD priors
  in the theory from the positive definite priors of the practical logdet and
  separator certificates.
- Revisited the preserved primary Brown–Laddha–Singh final PDF extraction,
  especially Theorems 2–3 and the guessed-basis normalization passages. Its
  general independence-oracle matroid scope and randomized PTAS predecessor
  are correctly credited; the new claim is narrower in representation and
  stronger only in the specifically identified all-target and accuracy
  dependence guarantee. No claim of inventing normalization, PSD decomposition,
  profile interpolation or objective independence appears in the integration.
- Read the local Mahalanabis–Stefankovic primary extraction around the
  bounded-width approximation and Theorem 43, alongside the manuscript's
  focused-target reduction. The introduction correctly describes an adaptation
  yielding a scalar predecessor guarantee, rather than claiming the source
  literally states this design theorem or silently inheriting a rational
  rounding-net implementation. The technical appendix retains the cardinality-only
  boundary and the documented local-cost inverse/block issue.
- Checked the new empirical summaries against Section 5: 2,347 source
  schedules and 33 formula-comparison decisions; one changed trace choice;
  no changed D/A choices at the eleven budgets; ten all-scalar and one
  all-diagonal separation; strict matched nested-anchor hull intervals;
  retained full-packet and fixed-grid negative evidence. The integration
  does not reinterpret historical timing as a controlled solver comparison.
- Checked that the introduction's anchor statement concerns nested anchor
  sets and complete feasible-schedule hulls. The discussion retains both the
  empty-anchor integrality gap and lack of universal runtime superiority.
- Independently checked all 204 labels and integration references: no duplicate
  labels or unresolved references. The saved build log contains no warning,
  undefined-reference, overfull or underfull messages. All eleven accepted
  technical, appendix, macro and bibliography files remain byte-identical to
  Stage 5's accepted snapshot. The check record is
  `verification/stage06-review2/integration-check.json`.
- The package docs accurately distinguish exact replay from numerical search
  reproduction, full validation from `--quick`, anonymous authorship from
  invented metadata, and internal review records from external peer review.

## Limits

No frozen manuscript, executable, manifest or scientific artifact was edited.
I did not repeat the full computational validation, reproduce historical
optimizers, or perform a new unrestricted literature search in this integration
review. The primary sources inspected above support the relevant predecessor
comparisons; they cannot establish exhaustive absence from the literature.
The manuscript appropriately uses a precise qualified novelty statement.
The final whole-paper gate remains necessary.
