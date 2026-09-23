# Review of the manuscript's formal-verification section

Date: 2026-09-22. Reviewed
`paper-quadratic-aggregation/sections/90-formal-verification.tex` against the
eleven Lean modules, the frozen scope, and the paper's current setting
section. No paper or mathematical source files were changed by this reviewer.

No correction is needed. The displayed theorem has the original strict
system, ordinary hull, nonnegative nonzero weights, PSD quadratic part, and
nonzero quadratic or linear part. Its unbounded-level hypothesis is exactly
the formal definition, and the stated equivalence with increasing sequences
is separately proved. The HHC specialization has the assumptions of the
paper's displayed certificate question; its omission of a separate
`lambda!=0` in that question is harmless because the nonzero coefficient
pair already implies it. The easy implication correctly drops both HHC and
nonemptiness.

The shorter proof matches the implementation. Replacing the constant by
its upper bound from strict feasibility preserves the inequality; the square
multiplier has the necessary sign. Zero coefficient pairs are excluded
before normalization. Closed finite generation, compactness, and continuous
evaluation produce an actual nonnegative aggregate representation with PSD
quadratic part and nonzero coefficient pair. The proof does not assume the
potentially false boundedness of the original constant divided by that
pair's norm. The norm discussion correctly distinguishes the implementation's
entrywise and product maximum norms from the paper's Euclidean and
Frobenius conventions without changing the theorem.

The checking paragraph matches the verification driver and audit source:
all eleven modules are explicit build and kernel-replay targets, including
the separately proved uniform cone-separation lemma. The owned-declaration
audit permits only `propext`, `Classical.choice`, and `Quot.sound` and includes
private and generated declarations through module ownership. The distinction
between replay by the pinned Lean kernel and an independent checker is
accurate. The final paragraph clearly excludes ancillary corollaries,
counterexamples, numerical certification, and priority claims.

Evidence inspected: the build log reports successful completion, the axiom
log reports 178 declarations across eleven modules, and the verification
manifest records the eleven module targets. The driver writes that manifest
only after successful exits from every build, audit, and module replay.
A separate read-only SHA-256 comparison made during this review confirmed
that all eleven current source files match the manifest. The reviewer did
not repeat the coordinator's Lean commands or inspect CI. This review does
not certify the remaining paper sections or its staged development process.
