# Companion attribution addendum: review brief

The user requested a complete, submission-ready paper on smoothed exact
global optimization beyond convexity, with plain expert prose, full proofs,
careful comparisons, and qualified novelty claims. Opus is the main writer;
Sol and Opus provide independent review. All literature research is assigned
to Luna at maximum reasoning. No optimization experiments are required.

This follow-up addresses the user's late Opus editorial P2 addendum. The
reviewed predecessor is `snapshots/final-submission-r4/`, manifest SHA256
`0c48e0cda82b7a4f25be956980b536577311fa71d40220cc35c8d1a47d0af061`.
The completed predecessor release is preserved in
`release-history/final-submission-r4/`. Its full mathematical and editorial
review history remains evidence for unchanged material, not a fresh verdict
on this revision. The frozen successor is `snapshots/submission-addendum-r1/`,
manifest SHA256
`fc756e30029d3d1d430b6e77e1d6b557bbb7e7d7a55b24599b95be5cd28b87f9`.
The exact diff is `submission-addendum-r1.diff`; the protected-block record
is `../verification/addendum-source-comparison.json`.

## Prior findings and responses

The original editorial findings P1–P5 were resolved before R4: exact-arithmetic
companion overlap and its cubic positive theorem are credited; the quartic
obstruction is reused; the decomposition companion's graded-grid and
growth-dependent bounds are stated with their integration limitation;
sparse-indicator perturbations are described precisely; numerical ratios are
included in the parameter statements; potential uses respect the finite
algorithm-chosen law and fixed residual feasibility; and the conservative
strong-noise constant is disclosed. The final editorial R2 report passed its
source-contract, editorial and PDF scope. Preserve these qualifications.

The new addendum identifies further deterministic antecedents in the
decomposition-aware companion:

- Fixed-feasible-set value-function curvature: companion `lem:valuefunction`
  (a), our `lem:rec:value` (b).
- Certified bag-local filtering: companion `thm:cr-filter`, deterministic
  parts (a), (b) of our `prop:sp:conditional` and `prop:lim:conditional`.
  Part (c) is the finite-law expected near-optimal tuple count. No efficient
  outside-value oracle is supplied for general sparse problems.
- CORE: companion `thm:cr-search` and its growth query count, antecedents of
  our `prop:rec:search` (a)–(c). Our stochastic paragraph provides expected
  counts without a supplied growth premise. Do not imply that we reproduce
  all of CORE's additional lower-bound-record output.
- Star examples: companion family A is the deterministic example reprinted
  as `ex:rec:star`; `prop:lim:local` adds the small-noise every-draw conclusion
  and the level-zero nonclosure argument. The positive-definite example
  after it is an exact specialization of companion family B at mesh 1/4.
  Luna's dated follow-up supersedes the initial broader non-reproduction
  claim. Both families now receive direct credit.
- TU coupling: the companion has deterministic fixed-degree approximation
  certificates and rational quadratic exact output. Its quadratic exact
  procedure terminates without uniqueness or growth; set growth bounds its
  levels. The stated operation bounds additionally require finite optimal
  coordinate projections, bounded by a separate parameter. Our exclusion is
  from the present smoothed guarantees, not from all deterministic algorithms.

Luna's exact source contracts, versions and hashes are in
`companion-overlap-addendum-luna.md`. This is read-only local-source research;
no new source or citation key is required. The historical front author
report now explicitly withdraws its characterization of B10 as a new
manuscript statement. Review that withdrawal as well as the manuscript.

The deterministic strongly convex face enclosure already belongs to the
companion and is credited in the introduction. The claimed addition is the
finite-law count and noise-dependent margin/fallback/expected-work
composition. Do not accept a blanket originality claim for closure
certificates. This distinction must survive the expanded overlap paragraph.

## Requested review

Read the complete new attribution passages in Sections 1, 5, 6, 7 and 9,
their neighboring formal results, and the supplied Luna source audit. Verify
that the introduction and the direct local attributions agree about what is
inherited, what is re-proved, and what this paper adds. Check the degree and
growth qualifications of TU, oracle scope, exact versus certified CORE
mode, and the star specialization. Check for vague or inflated priority
claims, contradictory statements, repetitive prose, broken references, and
loss of the earlier qualifications.

Independently verify the successor manifest and the claim that mathematical
statements, displayed equations, labels and bibliography are unchanged,
apart from the corrected regret remark and explicit row-scaled marginal
clarification of `prop:model:uniform` (a). One affine-margin proof is also
repaired; the other 137 proof blocks should be byte-identical to R4.
A fresh build and PDF are being supplied by root; inspect the
changed passages in the actual PDF when available. This is a targeted
attribution and presentation review, not a fresh audit of every proof or a
new literature search. Do not browse, add literature, or mutate the KB.

Write only the assigned evidence review report. Identify your exact target,
what you read and checked, any concern and repair needed, and the limits of
your verdict. A scoped PASS requires no unresolved defect in these changes;
it does not promise journal acceptance or worldwide priority. Stop after
the report; do not edit manuscript sources.

## Late completed mathematical review

The previously interrupted Opus mathematical R1 review subsequently completed
as `reviews/opus-math-r1.md`. Its target is the original proof draft, but six
new findings include current-source issues. The independent Sol disposition
is `reviews/late-opus-math-disposition-sol-r1.md`; the scoped Opus response is
`author-reports/late-math-repairs-opus-r1.md`. Include them in this review:

- NEW-1: the affine-margin proof must follow the coordinatewise minimizer
  for a positive affine value, not an arbitrary vertex with nonpositive
  value. Handle zero-slope and constant cases, use the symmetric argument for
  negative values, and retain the empty-zero denominator bound. Verify the
  unchanged lemma and its bilinear-flow/TU sampling-precision dependency.
- NEW-2: the lattice theorem uses row-specific aligned marginal scales with
  one common resolution. Identify this as a stated extension of the common-
  marginal model without broadening every aligned theorem.
- NEW-3: the lattice-search reference is already repaired in R4.
- NEW-4: the closure template already states parameter-dependent sampling
  exceptions in R4.
- NEW-5: the model's FPT summary must distinguish aligned/Gaussian-like
  low-rank bounds from the ambient-uniform dimension-dependent count; retain
  the joint numerical-parameter qualification.
- NEW-6: the quadratic regret remark must use original-domain perturbation
  width, not auxiliary search-box widths. Retain the Gaussian support factor
  and the correct projected widths for aligned noise.

An obsolete front-R2 task resumed after the provider quota reset and made a
stale replacement of Section 2. Root preserved it in
`concurrent-front-r2-preserved/`, stopped the obsolete task and restored the
reviewed R4 file before the new narrow repairs. Other superseded writers have
also been stopped. Verify that the delivered source incorporates only the
identified attribution and mathematical repairs, with no stale rewrite.
