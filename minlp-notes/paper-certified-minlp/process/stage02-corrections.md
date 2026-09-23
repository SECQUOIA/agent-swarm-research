# Stage 2 corrections

Completed 2026-09-13 by a correction agent distinct from the Stage 2 author.
Read the adjudication and all five independent review reports. Implemented all
six accepted minor corrections. No behavioral code, later manuscript section,
other paper folder, or acceptance status was changed.

## Finding-to-change map

1. **R1: even-power index.** The scalar composition table now states
   `k in Z_{>0}`, making positivity and integrality explicit even for a base
   that changes sign.
2. **R1/R5: quadratic domain.** The equivalence between quadratic convexity
   and positive semidefiniteness is now expressly global on the ambient real
   space. It is identified as a sufficient test on every certified box,
   including a box with fixed coordinates. The PSD lemma and proof are unchanged.
3. **R2: monomial attribution.** The recognition paragraph now cites
   Lundell–Westerlund, Theorems 2.1–2.2, printed page 507, and explicitly records
   their attribution to earlier work. Added the published article to the paper
   bibliography and an inspection record to `evidence/literature-review.md`.
   The self-contained Hessian proof remains intact; no first-discovery claim
   was added.
4. **R2: inference order.** Proposition `prop:vipr-invariant` itself now assumes
   that every inference reference points to a strictly earlier row, making the
   induction premise locally explicit.
5. **R3: summaries.** The provenance paragraph now states that summaries
   report whether all expected record indices occur exactly once. It explicitly
   allows incomplete summaries with a false completeness flag.
6. **R3: resume settings.** The provenance paragraph names artifact fingerprints
   and manifest-pinned inputs, source/environment identifiers, external checker,
   and timeout, and states that worker parallelism may change.

## Primary-source verification

The web-tool PDF request timed out, but direct HTTPS retrieval of the
[author-hosted published original](https://users.abo.fi/twesterl/some-selected-papers/26.%20OMS-AL-TW-2009.pdf)
succeeded. The first-page text confirms Andreas Lundell and Tapio Westerlund,
*Convex underestimation strategies for signomial functions*, Optimization
Methods & Software 24(4–5), 505–522 (2009), DOI
[10.1080/10556780802702278](https://doi.org/10.1080/10556780802702278).
Read the extracted theorem text and rendered and visually inspected PDF page 3
(printed page 507). Theorems 2.1–2.2 give exactly the stated sufficient exponent
conditions, after omitting zero exponents and changing the coefficient sign for
concavity. The page explicitly attributes the conditions to an earlier reference.
The downloaded original has SHA-256
`4354fd8166275ecad09455bdfef338f7fd4004d12db35d77519b79b3d067f65d`.
Temporary research files are outside the paper and literature directories;
no original PDF was added to the distributable supplement.

## Validation

Built a fresh isolated source copy in `build/stage02-corrections/` with
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. The build
returned zero and produced a 21-page PDF. The transcript is
`process/stage02-corrections-build.log`. The final LaTeX log has no warnings,
undefined references/citations, or overfull/underfull boxes. PDF text extraction
succeeded; the new citation and worker-parallelism qualifier are present.

Inspected `recheck.environment_manifest` and the summary return path to verify
the operational wording. Recomputed the seven checker source hashes recorded
in `process/stage02-analytic-validation.json`; every hash still matches. The
changes clarify hypotheses, attribution, and existing behavior, so no code test
rerun or large-proof replay was needed. No new issue was found, and stage
acceptance remains the coordinator's decision.
