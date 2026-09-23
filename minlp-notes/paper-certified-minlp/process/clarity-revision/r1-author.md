# R1 author report: scientific problem and contribution framing

Author: `/root/formal_author`. R1 is authored and ready for the coordinator's
five independent reviewers; this is not stage acceptance. No future review
reports were consulted and no work was delegated.

## Changes and rationale

Only `main.tex` (its abstract), `sections/01-introduction.tex`, and
`sections/07-discussion.tex` were edited as manuscript sources. The required
clean-build script updated the review PDF, bibliography, and build logs. The
source archive and current evidence documentation are intentionally reserved
for R2, so the older archive does not yet represent this intermediate revision.

1. **Problem first.** The opening paragraph now identifies the two obligations
   left by an exact MILP proof: nonlinear-cut validity for the stated model and
   identity of the proved master with the justified relaxation. The introduction
   states the concrete implemented interface and its objective-preserving
   soundness argument before the literature review.
2. **Separate kinds of contribution.** The early contribution subsection
   explicitly distinguishes method, empirical findings, validation, and reusable
   artifacts. It states the scoped mathematical implication and operational
   significance without promoting tests, Lean validation, or catalogue coverage
   into a new general optimization theorem. The test statement describes 161
   tests, not 161 independently identified mathematical contracts.
3. **Abstract focus.** The abstract follows problem, method, soundness, principal
   evidence, and significance. It retains 203 accepted artifacts among 289
   attempted models in separate replay and the three completed proofs with
   external acceptance despite invalid supplied steps. Historical label/count
   accounting, repair cohorts, catalogue bookkeeping, and example objective
   values are omitted. The limited formal/software boundary is one sentence.
4. **Precise attribution with less repetition.** Halbig et al. remains the
   closest computational comparison. Their continuous convex plane check and
   integer-freeness optimization are explicitly contrasted with recomputation
   of rigorous enclosures at supplied support points and replay of rational
   inferences. Baes's point-count/bit-length distinction, established support
   minimization, rigorous-bounding precedents, and prior executable/formal
   verification work remain attributed. Repeated priority disclaimers were
   shortened; no first-system or absence claim was added.
5. **Scientific conclusion.** The discussion now draws lessons about consistent
   model interpretation, mathematical classification of failures, original-model
   primal feasibility, capability and representation costs, and complementary
   validation. It removes the chronology of historical labels and repair cohorts
   while preserving the limits on what those findings establish. Local invalid
   inference is still distinguished from a false final bound; sufficient
   rejection from refutation; and shared-machine timing from solver superiority.

## Scope and source checks

No mathematical theorem, executable rule, formal proof, reference entry,
experimental record, table, population denominator, or supported novelty claim
changed. The 203/289 capability statement and three-proof audit are the existing
Section 6 findings. The 222-model catalogue appears only as an explicitly
nonuniform reusable collection in the introduction. Original-model witnesses
remain necessary for optimality statements. The actual loaded-expression
semantics, incomplete admission rules, restricted model class, mathematical
premises, and unmechanized software trust boundary are preserved.

Comparative statements use the already checked primary sources and accepted
literature map. In particular, the revision preserves Halbig's Algorithm 3
comparison, the Baes point bound, Jansson/Messine--Trombettoni support-bounding
attribution, QIBEX-R as a reported approach, and the specific CvxLean/CakeML/Wood
coverage distinctions. No new source fact required an additional search, and
no additional primary-source content or bibliography metadata was introduced.

## Validation and handoff

Ran `bash scripts/build-paper.sh`, which compiles a fresh source directory.
The final PDF has **31 pages**. The final log contains no warning, undefined
citation/reference, or overfull/underfull box. PDF text extraction succeeds.
Copied immutable R1 review logs to `r1-author-build.log` and `r1-author-main.log`,
and PDF text to `r1-author-main.txt` in this directory. No checker tests, Lean
rebuild, numerical experiment, full proof replay, or bulk archive read was needed.

Reviewed-source/build fingerprints:

| File | SHA-256 |
|---|---|
| `main.tex` | `13f1381f1434aa843f79336f7960815b8e5b97b335ece14607d13bc7ee81fd49` |
| `sections/01-introduction.tex` | `4a3f4e07636d0c582dce7aefacea71657b507f40873a175b575a3c9f9c3f86ee` |
| `sections/07-discussion.tex` | `67332af75f4212c53b243858b824b81d130134cabf5435eae562618e15e17134` |
| `main.pdf` | `6497c2d72a9a9b8ee9a885fb09d9cdf7cffc3dc307243423969ce6b1944e7cf9` |
| `main.bbl` | `273e543afebe7494fe9c8c8995e34e7081f83e8c5e0bc692d46ca4e02c192f69` |
