# Certified MINLP independent review

Status: complete. All 49 mathematical obligations were compared with the
actual definitions and theorem statements by independent subagents.

- [Analytic review](REVIEW-ANALYSIS.md): exact suprema, cut examples,
  composition rules, quadratic and monomial recognition, linear fractions,
  interval arithmetic, and domain examples.
- [Propagation and discrete review](REVIEW-DISCRETE.md): rational updates,
  integral rounding, assumption tracking, full-list checking, checked
  incumbents, bounds, and infeasibility.
- [Integration review](REVIEW-INTEGRATION.md): normalization, extended-real
  infima, derivative support, master identity, explicit graph embedding,
  objective constants, and bound transfer.

No unresolved mathematical defect or unmapped mathematical obligation was
found. The [coverage map](COVERAGE.md) records exact premises rather than
treating every theorem as unconditional.

The main representation boundaries are material. The monomial Hessian is
represented by the actual second derivative in every direction and its matrix
quadratic form. The master theorem permits any list of justified rows;
omitting restrictions weakens the relaxation, but the theorem does not prove
exporter completeness. The master matcher receives a typed bijection and
checks its rational row-scaling witness. The Lean discrete checker consumes
structured values and does not verify VIPR text parsing or Python execution.

Accepted nonlinear evidence must supply actual segment derivatives, valid
enclosures, and equality to the intended original expression. The proofs
derive support, underestimation, and master inclusion from those facts; they
do not establish that external libraries produced them. All eight software
boundaries in the inventory remain explicit.

Independent review is a source-to-statement assessment, separate from the
targeted Lean build and axiom audit recorded in [VERIFICATION.md](VERIFICATION.md).
It is not external peer review.
