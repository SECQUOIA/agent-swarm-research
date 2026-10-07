# Late source and mathematical review dispositions

The final manuscript is `snapshots/submission-addendum-r2/`, manifest SHA256
`0f1ff4db085a5d732b4e476309deafd2a2793225103a7a0773ae3ae84c2c2d94`.
Its predecessor release and verification records are preserved in
`release-history/final-submission-r4/`. The scientific-source changes are recorded in
`submission-addendum-r1.diff` (R4 to R1) and
`submission-addendum-r2.diff` (R1 to final R2). The last diff contains only
two introduction clauses; every mathematical environment is unchanged from R1.

## Companion attribution

Luna's current source audit and dated correction establish the following
antecedents. The manuscript credits them in the introduction and directly
where they are used:

| Finding | Final resolution |
| --- | --- |
| Fixed-feasibility value-function curvature | The curvature part of `lem:rec:value` is attributed to the companion's value-function lemma. No residual convexity is needed for that deterministic fact. |
| CORE | The exact-oracle retention, value-interval and witness layer is inherited. The paper also allows certified errors and gives finite-law expected counts without a supplied growth premise. It does not claim to reproduce CORE's additional lower-bound-record item. |
| Certified bag-local filtering and B10 | Parts (a), (b) are inherited deterministic filter guarantees; part (c) is the expected tuple count. No efficient general outside-value oracle is supplied. The old front report's novelty wording is explicitly withdrawn. |
| Star examples | Both the original star and the positive-definite family at mesh 1/4 are credited. The every-draw small-noise persistence and level-zero nonclosure are the extension. Luna's follow-up supersedes its initial overly broad claim that family B was absent. |
| TU coupling | The exclusion concerns this paper's smoothed guarantees for constraints on the searched coordinates. The companion's deterministic approximation certificates and rational quadratic exact output are credited. Set growth controls exact-search levels; the operation bounds also require a bound on the size of each optimal coordinate projection. Separate positive TU recourse results remain explicit. |
| TU rounding | The deterministic dyadic rounding, full-Hessian allowance and sound pruning specialize the companion's results. Classical integral-vertex attribution is retained. The missing general-TU part is the smoothed count and closure/tail control. |
| Closure | Strongly convex face enclosures are inherited. The contribution is the noise-dependent count, bounds on closure failure, margin tails and exact same-draw fallback composition. No blanket originality claim is made for closure certificates. |

The original major editorial findings on the cubic/quartic distinction,
growth-bound integration, numerical parameterization, sparse-indicator
comparison and potential uses remain resolved. This addendum does not
broaden those claims. The integer-related results retain their explicit
subsections and introduction map; a wholesale rearrangement is unnecessary
for these local corrections. The compact uniform-resolution proposition is
a specialization of the later counting corollary, whose full proof is
referenced. Earlier snapshot editorial suggestions are assessed against the
actual candidate rather than mechanically applied to the old draft.

## Late mathematical findings

The complete Opus R1 mathematical report arrived after its interrupted run
resumed. Sol independently assessed its six new findings and the actual
Opus repairs. The final frozen Opus and Sol reviews confirm the repaired
arguments and their downstream uses:

| Finding | Final resolution |
| --- | --- |
| NEW-1 affine-margin proof | The path follows a coordinatewise minimizing point for positive values, with zero slopes fixed; negative values use the symmetric argument. The constant and empty-zero cases are explicit. The unchanged lemma and bilinear-flow/TU sampling bounds survive. |
| NEW-2 aligned law | The lattice theorem uses an explicit row-scaled extension with specified scales and one common resolution. The uniform-resolution proposition retains every row scale; the lattice introduction points to the extension. General counting lemmas retain their broader marginal hypotheses. |
| NEW-3 lattice search reference | Already repaired in R4; the summary and appendix use the corrected-corner search. The additional corollary citation is optional because the appendix already identifies it. |
| NEW-4 encoding length | Already repaired in R4 by the parameter-dependent sampling exception. |
| NEW-5 FPT summary | Low-rank FPT wording is restricted to aligned and Gaussian-like noise, jointly with numerical parameters. Uniform ambient noise retains its dimension-dependent exponent. |
| NEW-6 regret width | The subsidiary ambient regret bound now uses original-domain coordinate widths, or relaxation upper bounds, rather than auxiliary search widths. The Gaussian support factor and correct aligned widths are retained. |

No optimizer or runtime theorem is invalidated. The sole changed proof is
the affine-margin proof; the other 137 are byte-identical to R4. The
uniform-resolution proposition has a marginal-scale clarification and the
regret remark has a corrected bound. All other mathematical environments,
410 labels, and all bibliography bytes are unchanged.

An obsolete front-R2 writer resumed after the provider quota reset and
overwrote Section 2. Its intermediate work is preserved in
`concurrent-front-r2-preserved/`. Root stopped it and restored the reviewed
R4 section before the scoped repairs. Other superseded writers were also
stopped. The final diff contains no stale replacement.

The PDF builds cleanly at 182 pages. The fresh 23-file archive extraction
build reproduces the complete live PDF text. No optimization experiment,
project-wide verification or CI inspection was performed. All literature
comparison work in this addendum was assigned to Luna at maximum reasoning;
no new bibliography key or KB mutation was required.

## Final review closure

The completed independent reports are:

- `reviews/post-addendum-final-opus-r1.md`: scoped PASS for the changed
  attribution, model clauses, mathematical repairs and affected PDF passages
  on frozen addendum R1.
- `reviews/post-addendum-final-opus-r2.md`: scoped PASS for final R2, after
  independently checking the two prose changes, all source identities and
  the updated PDF page. All 329 mathematical blocks, including 138 proofs,
  are byte-identical to R1.
- `reviews/post-addendum-final-sol-r1.md`: scoped PASS with an explicit final
  R2 follow-up. Sol independently checked the repaired affine argument and
  downstream sampling bound, row-scaled model, regret bound, attribution,
  source comparison and actual final PDF.

The two R2 refinements name the added bounds on closure failure and the
required bound on each optimal coordinate projection's size. Both reviewers
found no remaining defect within their stated scopes. Earlier reviews retain
their original targets; unchanged content is carried forward by verified
source identity. These reports do not certify absolute priority or journal
acceptance. The separately checked source archive builds successfully and
reproduces the full final PDF text. All authors and final reviewers have
stopped editing this manuscript.
