# Automatic joint convexification: development program

Status: completed for the supported classes below. Final document and evidence
review is closed with no unresolved consistency issue. The
[closeout](CLOSEOUT.md) records the delivered results, verification, negative
performance evidence, and remaining research boundaries.

The user authorized completing the recommended work and promising extensions
of topic 1: automatic joint convexification of small nonlinear blocks. This
is distinct from the earlier decomposition continuation's historical topic 1.

The starting evidence includes the composite-univariate handler, simultaneous
univariate-curve separator, separable concave row hulls, and their recorded
positive and negative experiments. These are completed foundations, not new
discoveries of this continuation.

## Deliverables

1. A rigorous support-cut kernel for supported univariate expressions and
   polynomial blocks. Final coefficients, domains, and model bindings must
   be checked. Resource exhaustion must not be interpreted as hull membership
   or feasibility. Certificates must retain the whole proof domain.
2. Automatic block discovery, efficient repeated separation, bounded work,
   and an explicit activation rule inside a solver integration. Reuse native
   model enforcement and measure preprocessing, generation, and checking.
3. A complete useful extension to coupled two-variable blocks, including
   proofs, exact diagnostic examples, an implemented oracle, and precise
   limits on composing overlapping block hulls.
4. A bounded comparative campaign with baseline, reformulation, unconditional
   activation, and automatic activation controls. Preserve timeouts, rejected
   domains, unfavorable results, and numerical-versus-certified distinctions.
5. A primary-source comparison, independent actual-file reviews, and an
   integrated research document with an exact claim/evidence map.

The program is complete when these deliverables have been implemented,
checked, evaluated, and documented within explicit supported classes.
Completion does not imply that arbitrary overlapping nonlinear hulls can
be separated efficiently or that a universal solver speedup has been proved.
If a promising extension fails, preserve the obstruction and assess a
concrete alternative before closing that investigation.

## Work ownership

| Directory | Responsibility |
| --- | --- |
| `solver/` | Rigorous numerical kernel, discovery, cached separation, solver integration |
| `numerics/` | Certification mathematics and numerical scope |
| `implementation/` | Integration choices and performance mechanisms |
| `theory/` | Coupled-block theorems, exact support oracle, composition limits |
| `experiments/` | Frozen protocol, bounded runs, original-model checks, analysis |
| `literature/` | Primary texts, bibliography, attribution and novelty limits |
| `reviews/` | Independent mathematical, software and integration reviews |
| `document/` | Integrated research report and claim/evidence map |

## Local safeguards

Only targeted verification for this topic is run. Project-wide checks and
CI inspection are excluded by `AGENTS.md`. Initial unrelated changes are
recorded in `baseline-status.txt`; ongoing campaigns in other directories
are not part of this task. New solver runs use explicit resource limits
and leave no unmanaged background processes. Historical evidence is not
overwritten. No commit, pull request, publication, or external message is
needed to complete this request.

Research-agent reviews are internal reviews, not journal peer review.
Finite tests support implementation and algebra; universal mathematical
claims require proofs. An unsuccessful source search does not establish
publication priority.
