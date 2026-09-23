# Stage 1, round 1, independent review 4

Reviewer: `/root/stage01_review4`. Date: 2026-09-13.
Scope: substantive repository coverage, source-model versus synthetic-model
distinctions, withdrawn novelty and negative results, foundation correctness,
and interfaces to the planned later stages. No manuscript edits were made and
no other Stage 1 reviewer reports were read. No subagents were used.

## Verdict

**No MAJOR issue found. One MINOR handoff/documentation issue should be fixed
before accepting the stage.** The completed foundations are mathematically
sound on the stated domains. The coverage plan captures every substantive
measurement-development family I identified. Missing sections expressly assigned
to later stages are not defects of this stage.

## MINOR R4-1: record the precise prior-art reductions in the stage handoff

**Locations:** `process/coverage.md:82–93`, especially the general-covariance
row at line 86; `process/literature.md:124–126` and its concluding candidate-
contribution paragraph.

The map correctly credits inverse decay and Vecchia and includes the relevant
source-note names. It explicitly highlights all-subset uniformity and the
absence of a diagonal upper bound, but does not carry over two concrete
qualifications that substantially narrow the meaning of those distinctions.
They are developed in `notes/research-20260912-general-covariance-memory-bound.md`,
Section 8, beginning at line 377, and in
`notes/research-20260912-covariance-decay-priority-audit.md:34–55`:

1. Independent dummy blocks at deleted calendar positions transfer a suitable
   **class-uniform full-calendar** local-conditional theorem to every selected
   subset. Subset uniformity alone is therefore not a novelty distinction from
   such a theorem.
2. Block-diagonal normalization gives bounded spectrum from the stated lower
   eigenvalue and off-diagonal-decay promises. Allowing unbounded original
   diagonal blocks alone does not prevent use of older bounded-spectrum theory.

A closely related qualification should accompany the planned KL/Vecchia
comparison: `notes/research-20260912-noisy-markov-fsai-priority-audit.md:196–221`
derives that a *global* Gaussian KL bound already implies a relative precision
and Fisher-information sandwich through
`sum_j [lambda_j-log(lambda_j)-1] = 2 KL`. The distinction is the hypotheses,
constants, chronological window, and dependence on horizon; it is not a
categorical inability of KL control to imply Fisher control. The map currently
records the repeated-pair metric example but not this complementary implication.

**Requested fix:** add these explicit qualifications to the coverage/literature
handoff, with their source sections, and assign the short arguments or precise
explanations to the later locality comparison. Also make explicit in the
general-covariance row that its Section 6 supplies the inherited input-dimension
weighted-trace FPTAS, under fixed decay and conditioning promises; the current
generic phrase “weighted-trace schemes” covers it only implicitly. Do not
upgrade any of these qualifications into a claim that prior work already proves
the entire specialized result. This is a minor inventory precision issue, not
an identified error or unsupported novelty claim in the present foundations.

## Coverage assessment

I compared the map against the September 12 contribution map, completion audit,
principal result and priority notes, all September 12 note filenames, the
implementation filenames in `code/research_20260912`, and searches for adjacent
measurement/covariance/Fisher-information developments elsewhere in `notes/`
and the root index. I inspected the strengthened theorem/result sections most
likely to be lost in condensation.

- The mapping retains scalar gain and spacing improvements, nonstationary far-
  pair versus stationary near-pair assumptions, full-block noise whitening,
  general covariance, partial latent observation, normalized residuals, supplied
  rational metrics and input-size limitations.
- The scalar FPTAS priority withdrawal is explicit. The strengthened relative
  matrix approximation set supersedes the narrower D-only development, and the
  represented-matroid extension is properly separated from correlated subset
  optimization. Complete-packet versus selectable-coordinate hardness is kept.
- Exact Markov path convexification, forward/reverse equivalence, singular-
  transition continuity, and the separate regular Markov expected-Fisher scope
  are represented without revival of the withdrawn hull claim.
- Certificates cover integer interval pricing, spacing, true-covariance
  transfer, continuous dense-relaxation certificates, all-scalar and
  all-diagonal split barriers, robust standardization, polished robust designs,
  and the nested latent-separator hierarchy.
- Negative evidence is retained: precision-oracle instability, mixed schedule
  comparisons, incumbent costs, failed physical-grid targets, separator cost
  and remaining gap, partial/full-block limits, and conservative theoretical
  constants. The all-diagonal barrier is confined to its relaxation family.
- The public-source comparison is separate from temporal synthetic kinetics;
  exact trace conclusions are distinct from the currently numerical D/A
  conclusions. The count of 2,347 nonempty source-feasible schedules and the
  33 criterion-budget comparisons match the source recheck note. No assertion
  about the source authors' stored selected designs or physical sensitivity
  provenance is imported.
- ODE relaxation/validated-flow, storage, quadratic-conflict and unrelated
  solver projects have justified exclusions. Independent kinetic sensitivity
  validation remains included. The unproved direct-sum/factorization proposal
  is explicitly excluded as a theorem.

## Foundation correctness assessment

I independently checked the score and fixed-covariance Fisher formula, the
parameter-dependent covariance term, conditional-noise versus conditional-
response distinction, block-inverse information increment, gated PSD inflation
and equality condition, operator Kantorovich proof with PSD prior, common
kernels, rank-dependent log bound, optimizer transfer for D/trace/A, rational
sharpness sequence, diagonal/block coordinate invariance, and certificate
efficiency formula. No mathematical error was found. The positive-definiteness
requirements and singular-prior distinction are adequate.

The source time-block repair is a valid finite pattern construction. The text
does not mistake it for an independent-chain formula under cross-channel
correlation. The regularization, local-information interpretation, rate-swap
ambiguity, and limited physical meaning of rational stored inputs are clear.

As a finite independent check, exact SymPy calculations on all 15 nonempty
subsets of a rational four-observation/two-parameter example with a singular
prior passed both PSD inequalities, common-kernel and rank checks, and the
exact Schur-gap identity. The source covariance's three leading minors were
also recomputed exactly as `1`, `399/100`, and `791/25`. Results are in
`verification/stage01-review4/exact-checks.json`. These checks supplement the
algebraic review and are not substitutes for proof.

## Review limits and later-stage interface

This review did not certify every archived numerical witness or reread every
external primary proof; those tasks belong to their planned author/reviewer
stages. The foundations provide usable stable definitions and certificate
contracts for that work. Later-stage review should verify final theorem
constants and bit complexity directly, recheck portable exact certificates,
and substantiate scoped novelty against the now-available local full texts.
No current-stage defect is assigned merely because those later tasks remain.
