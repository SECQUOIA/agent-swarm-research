# Arithmetic complexity of optimization: completion program

The user authorized completing the recommended work and promising extensions
of topic 2: the distinction between approximating optimal values, recovering
optimizer coordinates, and making exact comparisons. This resumes that topic
after the earlier stopping points. Other research and running experiments are
outside this scope.

## Required work

1. Reconcile the existing results with primary literature, especially Slot,
   Steurer, and Wiedmer's *Hesse's Redemption*. Compare theorem statements,
   proof machinery, input representations, and output guarantees.
2. Independently audit the existing point-output and exact-arithmetic results
   that will support the integrated document. Resolve substantive findings.
3. Develop point approximation for globally convex polynomials beyond the
   current bounded, fixed-degree statement. Investigate unbounded rational
   polyhedra and explicit degree dependence.
4. Investigate full-point output for residual-convex cubics without a joint
   core convexifier. Seek an algorithm with a sound stopping certificate,
   all-draw correctness, and justified expected complexity.
5. Investigate exact polyhedrally constrained strongly convex quartic
   comparison without a constraint-rank bound. Develop useful extensions
   where the unrestricted target cannot be established.
6. Integrate the mathematical results, precise boundaries, source comparisons,
   reproducible checks, and practical output interfaces in a coherent report.
   Give new proofs independent review before treating them as established.

## Completion standard

The deliverable is a complete and reviewable research package. A mathematical
question is solved only by a complete proof under explicit assumptions.
Completing an investigation does not turn an unresolved question into a
theorem. Any remaining general question must be identified together with the
strongest proved result and the exact reason a proposed method stops short.
Do not claim that the field is exhausted or that an unsuccessful literature
search establishes publication priority.

Distinguish ordinary binary computation, arithmetic-circuit computation, and
oracle computation. Distinguish an objective-gap point, distance to the
optimizer set, distance to one fixed selected optimizer, exact implicit
output, and expanded rational/algebraic output. Supplied structure and the
cost of verifying it belong in the input contract.

## Work organization and verification

New work lives under this directory. Historical results are cited rather than
silently relabeled. Necessary corrections to them must be explicit. The root
agent integrates results; separate agents own literature, global point
extensions, cubic recourse, constrained exact comparison, and independent
audits. Research-agent review is internal review, not journal peer review.

Run only targeted checks for changed mathematics, implementations, and report
files. Record commands and their actual outcomes. Finite diagnostics do not
prove universal theorems. No project-wide local checks or CI inspection.
Existing unrelated dirty files are recorded in `baseline-status.txt` and must
be preserved. No public upload, submission, commit, or external message is
part of this request.
