# Stage 1 round 1 coordinator assessment

All five independent reports are complete. All find no major issue in the
foundations. Root read the foundations, the five reports and their supporting
evidence, checked the covariance determinant independently, and accepts the
following minor corrections. Repeated findings are consolidated below.

1. **Estimable-subspace qualification (review 5): accepted.** Mere compression
   onto an arbitrary estimable contrast subspace does not preserve inverse
   information when complementary parameters remain unknown. Restrict this
   statement to a declared reduced parameter model/common supported invariant
   range, and distinguish a nuisance-adjusted contrast covariance. The current
   full-parameter propositions do not rely on this sentence, so this is a local
   clarification rather than an invalidating theorem error.
2. **Corollary hypotheses (review 5): accepted.** Explicitly inherit the spectral
   enclosure and alpha from the preceding proposition.
3. **Sharpness wording (reviews 1, 2, 3, 5): accepted.** Efficiency has the stated
   infimum; log loss has the corresponding supremum. Correct the wording while
   preserving the rational limiting construction.
4. **Local-rank witness (reviews 1, 3): accepted.** Add the exact three-time
   sensitivity determinant at (A0,k1,k2)=(1,1,2), with columns in that order
   and times log(2),2log(2),3log(2). This completes the local/global example.
5. **Source-table locator (reviews 2, 3): accepted.** Identify SI Table S-1,
   the A-DCM/C-DCM transpose entries 0.01 and 0.1, and the inspected version.
6. **Rotary-bed code locator (review 1): accepted.** Correct the evidence record
   from lines 111–120 to lines 101–108 in the pinned source.
7. **Prior reductions and general-covariance FPTAS coverage (review 4): accepted.**
   Explicitly map dummy-block padding, diagonal normalization, and the existing
   global-KL-to-relative-Fisher implication as novelty qualifications, and map
   the general-covariance weighted-trace scheme to the approximation stage.

These changes do not alter the core established Schur/Kantorovich propositions,
the input statistical model or the certificate contract. A separate correction
author must address all seven items, compile cleanly, and document verification.
Because no major finding was accepted, another five-reviewer round is not
required by the requested process. Root will verify the correction before
accepting this stage and starting Stage 2.

## Correction verification and acceptance

The separate correction author completed all seven items. Root inspected the
changed statistical-subspace paragraph, explicit corollary hypotheses, sharpness
wording, source-table locator and the coverage/literature additions. Root also
independently recomputed the new sensitivity determinant as
`-log(2)^2/2048` and the nuisance example contrast variance `2/3` versus the
incorrect compressed-inverse `1/2`. The correction author's focused symbolic
checks passed. The final eight-page Stage 1 build has no warning, undefined
reference/citation, or over/underfull box matches. Stage 1 is accepted with all
valid findings resolved. Stage 2 may begin.
