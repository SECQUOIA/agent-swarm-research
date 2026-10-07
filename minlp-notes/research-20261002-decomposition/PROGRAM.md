# Decomposition-aware global optimization: continuation

The user authorized finishing the recommended work and promising extensions
of topic 1, decomposition-aware global optimization and certification. This
resumes that topic after the October 2 stopping point. Other research topics
and their running experiments are outside this continuation.

## Questions and deliverables

1. Implement the corrected-grid and min-marginal pruning method with
   independently checkable bounds. Evaluate complete runtime, memory,
   width, conditioning, and accuracy dependence against useful baselines.
2. Investigate continuous sparse QP with a parameter based on negative
   curvature divided by global growth. Preserve the distinction between
   structural inequalities, a complete algorithm, and obstructions to a
   particular representation.
3. Develop conditional recourse or message-error bounds that can improve
   the global discretization allowance in the sparse smoothed method.
4. Extend the sparse methods to meaningful coupled constraints, with an
   explicit account of feasible rounding, repair, and integer preservation.
5. Investigate unknown nonunique optimal sets and deterministic polynomial
   boundary certificates beyond the existing convex-patch assumption.
6. Integrate the resulting theory, implementation, evidence, and limits in
   one coherent research document, with a source comparison and targeted
   reproducibility commands.

The continuation must account for the current October 2 results before
reopening a historical question. A mathematical question counts as solved
only with a complete argument under explicit assumptions. A failed method,
counterexample, or unfinished proof must retain that status; finishing an
investigation does not resolve every open problem in the subject.

## Working organization

Each workstream owns its directory and records its claims, proofs, code,
targeted checks, prior comparisons, and remaining limits. Independent
reviews read the actual saved work. Research-agent review is not journal
peer review, and finite checks do not establish universal theorems or
publication priority.

| Directory | Scope |
| --- | --- |
| `solver/` | Implementable certified sparse optimization and benchmarks |
| `negative-curvature/` | Retaining convex energy while discretizing nonconvexity |
| `conditional-messages/` | Local conditional error and recourse |
| `constraints/` | Coupled feasible sets |
| `degeneracy/` | Optimal sets and boundary output |
| `literature/` | Primary-source comparison of the final contributions |
| `reviews/` | Independent cross-checks and integration reviews |
| `completion/` | Second-phase implementation, new theory, frozen benchmarks, and reviews |

Only topic-specific verification is run. No project-wide verification or
CI inspection is authorized. Existing dirty files and background solver
jobs from other topics are left alone. New experiments must have explicit
limits, record incomplete runs, and leave no unmanaged background work.

No commit, public upload, submission, or external message is part of this
request.

## First report and subsequent completion

The six workstreams produced the deliverables indexed in the
[result map](README.md): an executable rational solver and checker,
bounded comparative experiments, restricted negative-curvature and
conditional-recourse algorithms, exactly feasible TU-fiber optimization,
three optimal-set/boundary extensions, and an integrated technical report.
Proofs and implementation claims are separately identified in the report's
[coverage map](document/COVERAGE.md). Independent reviews and targeted
checks accompany each workstream.

The first report left engineering gaps: general exact rational output,
automatic integrated recourse, reusable constrained and optimal-set methods,
decomposition construction, and explicit polynomial/boundary algorithms.
The user's renewed instruction authorized completing these and promising
extensions. The [completion record](completion/README.md) identifies the
resulting implementations, further theorems, independent reviews, and new
bounded experiments. Earlier benchmark snapshots remain historical evidence.

The program does not resolve all the general problems motivating it. The
result map names the remaining questions and the assumptions under which
each extension works. A successful subclass or a counterexample to one
proposed method is not recorded as a solution of the unrestricted
negative-curvature, coupled-constraint, or optimal-set complexity problem.
