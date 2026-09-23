# Mathematical claim review

Reviewed on 2026-09-16 against the complete
[paper source](../../../paper-multilinear-gap/main.tex), its
[coverage map](../../../paper-multilinear-gap/formal/COVERAGE.md), and the
canonical Lean statements and proofs. The review checked definitions and
hypotheses directly; it did not infer coverage from the module list.

Status: mathematical statement review passed. This report does not certify
the integrated build, axiom audit, kernel replay, export, or paper build.
Those checks must be recorded separately before this topic is marked complete.

## Findings and their resolution

| Mathematical claim | Review result |
|---|---|
| General vertex-law representation and extrema | `Attainment` proves cube and original-box representations and attained endpoints. Box hypotheses allow fixed coordinates and arbitrary finite real endpoints. |
| Convex/concave envelope terminology | `EnvelopeFunctions` proves convexity/concavity, under/overestimation, and comparison with every competing convex/concave function. The graph-hull interpretation is now an explicit theorem. |
| Individual monomial envelopes | `MonomialEnvelope.monomial_minimum` is the full lower formula; its law preserves all ambient coordinate means. Real subtraction in `s.card - 1` also gives the correct empty-support value one. The existing common upper law completes both endpoints. |
| Original scaled terms and `0 ≤ H_B ≤ T_B` | `PaperFoundations` identifies weighted widths with widths of the original scaled monomials and proves the comparison on boxes. It does not replace the original terms by their cube expansion in the definition of `T_B`. Zero coefficients and fixed coordinates are included. |
| Dyadic construction and exact size | The original support construction matches the consecutive blocks after converting from zero-based Lean levels. Distinctness and interiority were already proved. `ExactSize` now proves support count, an attained maximum degree, occurrence count, and literal `O(n_L log n_L)` sparsity. |
| Family termwise gap, positivity, cap certificate and unboundedness | Existing statements concern the original continuous graph hull. The disproof uses a documented alternative finite bound, with the same conclusion and domains. |
| Exact finite gap and attaining law | Existing cutoff, mixture, residue, and exact-minimum proofs supply the stated law. `Examples.adjacent_cutoff_values` supplies the boundary identity. |
| Actual family asymptotics | `ExactAsymptotics` proves an absolute logarithmic error at most three and the normalized limit of the actual termwise-to-hull ratio. This closes the previous gap between a lower comparison function and the actual family. |
| Printed examples | All four `Examples` statements give the actual hull width and ratio, rather than checking only the displayed scalar expression. |
| Universal finite upper bound | Parameters, support-independent common law, probability bounds, marginal preservation, harmonic integration, easy cases, and mixture match the manuscript. The transfer applies to original terms, including zero hull gap. |
| Degree and dimension limits | The final suprema range over all allowed nonnegative boxes. Dimension is exactly the ambient coordinate count; unused coordinates, boundary points, and fixed coordinates are permitted. The limits hold along all integer allowances tending to infinity. |

The intermediate failure-count and deficiency identities are distributed
through the existing construction, expectation, common-maximum, and exact-law
proofs. They are not each exposed as a separate named endpoint. The coverage
map states this explicitly. General attainment now justifies the maxima in
these identities. Alternative formal proof routes do not require reproducing
every algebraic step of the written proof.

No incorrect mathematical statement or remaining unverified substantive
endpoint was identified in the reviewed paper scope. The exclusions for
optimized fixed-point bounds, second-order terms, coefficient removal,
homogenization, arbitrary recursive formulations, and publication priority
are consistent with the manuscript.

## Review scope and verification handoff

The reviewer independently inspected `Attainment`, `PaperFoundations`,
`MonomialEnvelope`, `ExactSize`, `ExactAsymptotics`, and `Examples`, together
with the existing proof endpoints. The reviewer implemented
`EnvelopeFunctions`; that module's review here is therefore a self-review,
not an independent implementation review. Its generic hull arguments and
four cube/box specializations passed a targeted warning-free Lake build.

The source counts observed during review were 147 canonical proof modules
and 48 standalone modules, including 41 multilinear and seven shared modules.
The updated appendix and coverage map use these counts. The standalone export
must be refreshed after the final source edits before checking byte equality.

Required completion evidence remains the integrated warning-free build,
complete imports, transitive axiom audit, kernel replay, matching standalone
export, and successful paper/bundle checks. Consult the topic's verification
record for the final outcome; this report intentionally does not anticipate it.

## Independent review of the envelope interpretation

A second agent independently reviewed `EnvelopeFunctions.lean`, which was
implemented by a different agent. This review closes the self-review
qualification above for that module; the second reviewer implemented
`Attainment`, whose independent review is recorded above.

The generic lower theorem proves all three defining properties: convexity
on the domain, underestimation of the original function, and pointwise
domination of every convex underestimator. The upper theorem proves the
corresponding concavity, overestimation, and minimality properties. The
proofs use the actual graph convex hull and its attained slice endpoints;
they do not substitute a closure, a relaxation, or an assumed envelope.

The cube and box specializations discharge attainment through `Attainment`.
Their finite-coordinate hypotheses cover the paper's multilinear
polynomials. The box statements require only finite real endpoints with
`l i ≤ u i`, so they include all nonnegative boxes in the paper, fixed
coordinates, boundary points, and unused coordinates. No positivity of
coefficients or box widths is introduced. The inequalities concern points
inside the stated domain, as the paper's definitions require.

No defect or missing hypothesis was found. The independent targeted check
`lake build Formal.MultilinearGap.EnvelopeFunctions` completed successfully
on 2026-09-16. The full project and standalone checks remain governed by
the topic's verification record.
