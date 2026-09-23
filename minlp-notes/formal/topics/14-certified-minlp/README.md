# Certified MINLP mathematical verification

Status: complete on 2026-09-17. Work stops here; no other topic was started.

The source is the [Certified MINLP manuscript](../../../paper-certified-minlp/README.md),
especially its model, soundness, implementation, and formalization sections.
Proofs live in the existing standalone
[Lean project](../../../paper-certified-minlp/formal/README.md), under
`CertifiedMinlp/`.

This package extends the existing safe-cut and transfer proofs to the missing
propagation, exact correction, discrete inference, and curvature obligations.
The claim inventory and coverage map distinguish formalized mathematics and
executable Lean checks from the existing Python parser and runtime.

- [All 49 mathematical obligations](CLAIMS.md).
- [Claim-to-declaration coverage and software boundaries](COVERAGE.md).
- [Independent review](REVIEW.md).
- [Targeted verification record](VERIFICATION.md).

The extension adds 24 modules to the existing three. It covers propagation,
exact correction suprema, support calculus, all stated curvature tests,
structured discrete proof checking, master matching, and nonlinear bound
transfer. Main integration results are in
[`EndToEnd.lean`](../../../paper-certified-minlp/formal/CertifiedMinlp/EndToEnd.lean).
They construct the feasible graph point and apply the actual checked discrete
bound, including affine constants and maximization signs.

This completes the mathematical inventory, not formal verification of the
Python implementation or benchmark certificates. The parser, symbolic and
interval libraries, and their correspondence with the Lean inputs remain
explicit trust boundaries.

Local verification uses targeted module builds and topic-specific checks.
Project-wide verification belongs to CI; do not run it locally or check CI.
This follows the repository [local verification rule](../../../AGENTS.md).
