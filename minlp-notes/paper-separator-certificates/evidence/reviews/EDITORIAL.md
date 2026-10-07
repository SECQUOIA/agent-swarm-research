# Independent editorial and integration review

Reviewed the complete manuscript assembled by `main.tex`: the abstract,
introduction and prior-work section, all nine substantive sections, conclusion,
and both appendices. Also read the manuscript brief, Luna's current
`LITERATURE.md`, the independent mathematical review reports, the compiled
60-page PDF's metadata and log, and its extracted text. No independent
literature research, computational experiment, or project-wide check was
performed.

## Verdict

The paper has a coherent dependency order and a clear central result. It
distinguishes the finite certificate from the work needed to construct it,
then develops aggregate copy control, certified inexact evaluation, rational
implementation, and the constrained dynamics extension. The appendices are
useful complementary results rather than hidden hypotheses of the main
algorithm. I found no major structural omission or further mathematical
development required for this stated scope.

The writing is direct, technical terms are generally defined before use, and
the proofs supply the intermediate arguments an expert needs. Novelty is
restricted to the precise combination of hypotheses, representation, and
construction bounds. The current literature account is still being finalized
by Luna, so final acceptance of the source comparisons depends on that
closeout. The manuscript does not rely on the unretrieved historical source
identified in the current evidence file.

## Necessary corrections found and already applied during this review

1. The abstract initially said that no local nonlinear optimization routine
   was needed. The oracle theorem does require local convex minimizations,
   which can be nonlinear. The current source correctly says that no
   nonconvex local search is required. This matches the actual algorithm and
   avoids overstating the rational specialization's benefit.

2. The introduction initially described the band identity as a distance from
   the child conditional value function to the band. That value function is
   itself in the band, so this would describe zero. The current introduction
   correctly gives twice the distance from the permitted linear shift class
   to the band, and distinguishes the largest cell bracket. This now agrees
   with the one-separator theorem, including its factor two and the role of
   independently balanced cell pieces.

## Remaining narrow revisions

1. **Normalize the asymptotic logarithms.** In the abstract, the expressions
   `O(N log(N/epsilon))` and `O(N log^3(N/epsilon))` implicitly concern small
   accuracy. The theorems themselves allow every positive tolerance, so use
   `1+log_+(N/epsilon)` consistently or explicitly state an accuracy
   asymptotic. The same issue occurs in the introduction's description of
   `J`. This is a notation correction, not a failure of the explicit stage
   bounds. A prose alternative is: “For fixed bag dimension, coordinate
   occurrence, and conditioning, the final partition is linear in the number
   of bags and logarithmic in reciprocal accuracy; the number of local convex
   minimizations has the corresponding cubed logarithm.”

2. **Cite or remove the existing coordinate-grid comparison.** The paragraph
   in `sections/limitations.tex` on other optimal sets states that
   shared-coordinate methods retain anchors or unions and have
   several-minimizer bounds depending on projected optimal sets. These are
   concrete antecedent claims without a citation in the current manuscript.
   The brief identifies an existing coordinate-grid companion manuscript,
   but the generated Luna evidence does not yet give its manuscript metadata
   or a source locator. If this comparison is retained, route its provenance
   through the same literature lead and give an accurate manuscript citation.
   Otherwise replace the uncited result claims by the fully supported scope
   statement: “An extension to several minimizers would need a different
   progress argument that tracks the optimal set or several centers. The
   present single-center contraction does not provide such an argument.”
   The same provenance decision should establish whether the earlier
   certificate-existence manuscript is an independently submitted companion
   requiring an explicit citation. Do not invent publication metadata or
   present unpublished parallel results as established published work.

## Integration observations

- The table separates final partition size, cumulative creation, and local
  optimization count. The surrounding prose correctly excludes unspecified
  oracle work and charges explicit terms in the polynomial realization.
- The scope of the unknown-parameter searches is unusually clear: soundness
  holds for every trial, but the sharp fixed-ratio partition formula is not
  attributed to an arbitrary earlier successful trial.
- Point growth is explicitly global and implies uniqueness. Boundary
  minimizers are covered through algebraic cancellation, not an unstated
  stationarity assumption.
- Occurrence is kept separate from bag width. The explanation that star
  decompositions can have bounded width and unbounded occurrence prevents a
  misleading treewidth-only reading of the complexity result.
- The consistency theory is not claimed to supply inexpensive value-function
  oracles. The scalar covering appendix explicitly counts exact-bag separator
  pieces rather than all local certificate leaves.
- The rational realization chooses its own affine bag model and does not claim
  to implement every factorwise relaxation. The sound computable Hessian
  bound, endpoint rule, common denominator, and independent checker are
  connected clearly.
- In the dynamics extension, the adjusted gradients affect slopes while the
  original objective models remain in the local programs. The exact residual
  identity explains the extra multiplier term rather than hiding it.
- The finite-precision result distinguishes a feasible recurrence from rounded
  centers and approximate state enclosures. All input coordinates are reset,
  while the retained incumbent inputs define the exact trajectory. Soundness
  promises and rate promises are explicitly separated.
- The nonlinear example demonstrates nonconvex reduced dynamics with
  horizon-uniform constants, without making an empirical performance claim.
- The localization counterexample does not overclaim a lower bound for a
  specified algorithm or the smallest certificate. The finite-state allocation
  example is explicitly outside the continuous single-minimizer theorem.
- The conclusion's open questions are independent extensions. They do not
  leave a needed proof or implementation step unfinished within the proved
  scope.
- No internal research chronology, agent references, source-file paths,
  placeholders, or unsupported practical speedups occur in the scientific
  text I reviewed.

## Targeted artifact checks

`pdfinfo build/main.pdf` reported a 60-page PDF. A targeted search of the
current build log found no overfull or underfull boxes, undefined references,
or errors; the sole displayed warning was the harmless absence of an author.
The extracted PDF still contained older abstract and introduction wording
when inspected, whereas the current TeX sources had already received the two
corrections above. Rebuild and regenerate the extracted text after final
integration so the deliverable matches the approved sources. No verification
outside this manuscript was run.
