# Documentation follow-up to completed Lean verification

Date: 2026-09-20. The original follow-up below incorporates the mathematical corrections,
proof details and stronger results identified while comparing completed Lean
topics 00–18 with the current notes and manuscripts. It does not start topics
19–26 or change Lean sources. Compilation of the Lean developments was assumed;
no Lean checks or CI inspection were performed in this follow-up.

A subsequent, separate [topic-19 verification](../formal/topics/19-structural-multilinear/README.md)
completed the structural multilinear gap proofs and updated the four related
result notes and sections 5–6 of the relaxation-limits manuscript. Its current
PDF is 113 pages. The historical 112-page build below predates that update.
See topic 19's [coverage](../formal/topics/19-structural-multilinear/COVERAGE.md)
and [verification record](../formal/topics/19-structural-multilinear/VERIFICATION.md)
for its independent reviews, Lean checks and paper build.

The subsequent [topic-20 verification](../formal/topics/20-scalar-quadratic/README.md)
completed all 24 scalar quadratic obligations, updated three result notes and
the scalar section of the integer-dimension manuscript, and rebuilt its current
88-page PDF. It made the contact-volume hypothesis `δ≥0` explicit and clarified
construction sizes, folding depth and finite linear product slack. Its
[verification record](../formal/topics/20-scalar-quadratic/VERIFICATION.md)
records independent reviews, the 57-module build and kernel checks, and the
979-declaration axiom audit.

The subsequent [topic-21 verification](../formal/topics/21-dag-spectral/README.md)
completed all 33 explicit-DAG spectral-cover obligations, updated the spectral
and D-optimality source notes, and rebuilt the correlated-measurements paper
as a 66-page PDF. It makes the actual rational construction, dictionary and
storage charges, and exact criterion comparisons explicit. The costed core
takes verified topological vertex indices; finite-memory transfer assumes a
separately supplied PSD sandwich. Its
[verification record](../formal/topics/21-dag-spectral/VERIFICATION.md) records
independent reviews, 124 module builds and kernel replays, 20 preserved review
clients, and the 3,483-declaration axiom audit. Topics 22–26 remain queued.

## Mathematical changes

- Restricted the positive-box bilinear scaling argument to a common interval;
  unequal widths do not preserve its ratio. The lower bound two is unchanged.
- Completed the switching paper's cutoff and boundary arguments and added the
  arbitrary-grid one-switch half-mesh certificate.
- Supplied the FBBT upper-endpoint convergence proof, separated finite-prefix
  bounds from fairness, and stated the exact circuit counts and finite
  nonattainment consequence.
- Added the rational-partition approximation argument establishing completeness
  of reciprocal-anchor cuts at real candidates. The hull theorem permits real
  endpoints; the rational algorithm and cut family retain rational endpoints.
- Clarified the analytic cubic minorant's domain and the distinction between
  limiting lower certificates and actual family ratios. Promoted the verified
  lower bound `1610000/743033` in the older summaries.
- Required componentwise feasibility in the potential-flow setup and added the
  quantitative cubic bound for support-set convergence.
- Added the exact-count weighted-box formulation with `3n` continuous
  auxiliaries and `13n` inequalities, and clarified its size model.
- Separated incidence-coupling assumptions from the stronger treewidth
  assumptions, explained positive-box transfer with fixed coordinates, and
  summarized the sharper network–simplex results in the older result note.

The coverage descriptions retain exclusions for unverified implementations,
broader manuscript claims, historical runtime measurements and novelty. The
[topic index](../formal/topics/README.md) and
[recommended sequence](../formal/RECOMMENDED-TOPICS-PLAN.md) at that checkpoint distinguished completed topics 00–18 from unfinished
topics 19–26. Their current status also includes the subsequent completions
of topics 19–21.

## Independent review

After the topic edits, separate agents reviewed the changed mathematics and
coverage statements against the Lean declarations and current source text.
The review assignments paired reciprocal hulls with FBBT, exact counts with
network–simplex, potential flow with certified MINLP, and positive-box results
with core multilinear coverage; switching, cubic results and the central
inventory each received a separate review. Reviewers did not author the edits
they checked. No unresolved mathematical defect was found in the revised scope.

The follow-up incorporated their remaining wording findings: the `rho>1`
domain in the overview, narrower attribution of the derivative counterexample,
and explicit restriction of cubic mixture optimality to the three stated laws
and uniform termwise guarantees. These are internal agent reviews, not journal
peer review or new kernel-verification results.

## Targeted validation and current PDFs

All six affected manuscripts were built from clean source copies with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=BUILD_DIR main.tex
```

`BUILD_DIR` was a separate directory for each paper under
`/tmp/minlp-doc-review-iy96938f/`. Source copies omitted existing auxiliary and
bibliography-output files. The final logs contained no undefined references or
citations, duplicate labels, or overfull boxes. An initial build had reused stale
bibliography outputs in two papers; the clean builds resolved those citations.
A long path in the new switching paragraph was replaced by a short link to
remove an overfull box. Existing bibliography outputs were refreshed from the clean builds.

| Manuscript | Current PDF | Pages |
|---|---|---:|
| Certified MINLP | [PDF](../paper-certified-minlp/main.pdf) | 33 |
| Integer dimension | [PDF](../paper-integer-dimension/build/main.pdf) | 88 |
| Network–simplex | [PDF](../paper-network-simplex/main.pdf) | 51 |
| Potential flow | [PDF](../paper-potential-flow/complexity/main.pdf) | 216 |
| Relaxation limits | [PDF](../paper-relaxation-limits/main.pdf) | 112 |
| Switching control | [PDF](../paper-switching-control/main.pdf) | 56 |

Additional targeted checks used `git diff --check` on changed files, read-only
Python checks of 1,320 local links and changed TeX structure, `pdfinfo` for page counts,
and `pdftotext` to confirm readable output. TeX links were resolved from the
manuscript directory; Markdown links were resolved from their source directory.
These checks cover documentation and manuscript builds, not mathematical
reverification, experiment reproduction or a complete visual page inspection.

The current PDFs include this source revision. Submission archives, completion
PDFs explicitly labeled historical, old build directories not used as current
deliverables, frozen review snapshots and verification fingerprints retain their
original contents and scope. They do not certify these later prose edits.
