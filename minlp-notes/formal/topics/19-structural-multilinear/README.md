# Structural multilinear gaps

Status: complete within the frozen gap scope. This is topic 19 of the
[recommended sequence](../../RECOMMENDED-TOPICS-PLAN.md). Topics 20–26 have
not been started by this work.

The package covers feedback-variable, frequency-two and incidence-treewidth-two
gap bounds, including the stated sharpness and box extensions. The
[claim inventory](CLAIMS.md) fixes the full scope. The
[independent source review](SOURCE-REVIEW.md) identifies the mathematical
sources, manuscript labels, adjacent results and important scope distinctions.

The live manuscript is
[Convex relaxation gaps and spatial certificates](../../../paper-relaxation-limits/README.md),
principally sections 5 and 6. Existing standalone multilinear and cubic exports
have different scopes and are not topic-19 proof bundles.

- [Claim-to-declaration coverage](COVERAGE.md).
- [Independent reviews](REVIEW.md).
- [Targeted verification record](VERIFICATION.md).

The completed proofs establish the feedback bound `T <= 2^f H`, the
frequency-two bound `T <= 3/2 H` with odd-girth refinement and bipartite
exactness, and the incidence-treewidth-two bound `T <= 2H`. They construct
the needed laws, cycle decompositions, coloring and TU classes from the
actual graph hypotheses. Sharpness and the stated cardinality and box
extensions are included. All 25 obligations have declaration mappings and
independent review records. Original monomial factors are retained under
box normalization.

The package has 66 Lean modules. Run its targeted checks from the repository
root with `python3 formal/topics/19-structural-multilinear/verification/run_checks.py`.
The module list, declaration audit, logs and source fingerprints are retained
under [verification](verification/). These checks do not build the full
project root.

The feedback bound concerns all finite nonnegative boxes. Positive-box
frequency-two and treewidth-two extensions require a common aspect ratio
within each original scope after fixed coordinates are removed. The general
unequal-aspect frequency-two bound remains unresolved in the source notes;
bipartite exactness fails there. Sharpness at constant two means a supremum.

The separate optimization/separation algorithms and rational bit-complexity
claims are outside this package, as are the manuscript’s width-three and
signed-factor extensions. Generic-payoff sharpness does not establish
positive-monomial sharpness for arbitrary feedback size.

All local checks are targeted. CI handles project-wide verification; no CI
status or logs are inspected for this work.
