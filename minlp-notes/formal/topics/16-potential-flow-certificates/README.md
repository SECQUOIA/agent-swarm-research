# Deterministic potential-flow certificates

Status: complete and independently reviewed. Verified 2026-09-20.

This is topic 16 of the [recommended-topic sequence](../../RECOMMENDED-TOPICS-PLAN.md).
It verifies the remaining mathematics of
[Appendix K of Paper A](../../../paper-potential-flow/complexity/sections/11-certified-computation.tex),
"Certified computation from rational witnesses", beyond the energy witness and
uniform flow radius already verified in [topic 3](../03-potential-flow/README.md).

All forty frozen obligations are discharged by Lean theorems; the checks
actually run are recorded in [VERIFICATION.md](VERIFICATION.md), and four
independent reviewers found no blocking or significant defect. (This sentence
previously said "three independent reviewers". Those three covered CC01-CC39
only; CC40 fell outside all three groups and was reviewed afterwards.) A later
audit of the package's own prose found scope wording to correct or clarify in
[COVERAGE.md](COVERAGE.md) and wrong numeric records in
[VERIFICATION.md](VERIFICATION.md); they are corrected in place, each recording
what it previously claimed, and none of them changed a Lean statement.

- [Mathematical obligations](CLAIMS.md), frozen before the proofs.
- [Claim-to-declaration coverage](COVERAGE.md).
- [Independent review](REVIEW.md).
- [Verification record](VERIFICATION.md).
- Canonical sources: [`Formal/PotentialFlow`](../../Formal/PotentialFlow).

## Scope

Given a finite directed network with positive asymmetric cubic edge energies,
a conserved rational trial flow `y`, and a verified energy gap `delta`, this
package proves four further families of a posteriori guarantees about the
unique physical flow `x*`:

| Certificate | Guarantee |
|---|---|
| Separate-edge Bregman intervals | Rational endpoints passing two divergence tests enclose `x*_e`, and the edge law encloses the physical drop. |
| Posterior endpoint scenarios | A selected resistance scenario loses at most `sqrt((2/beta_L) sum_e r_e)` in flow, and is exactly optimal under stated sign compatibility. |
| Support certificates for linear goals | Rational dual data bound `w^T x` over the conserved energy sublevel set; the rational bounds are complete, and they converge to `w^T x*` as trial energies decrease. |
| Conservation-aware curvature | Interval curvatures and a conserved residual bound `|w^T(x* - y)|`; the optimal Laplacian factor is exactly sharp for that quadratic information, and its zero-curvature obstruction is characterized. |

The two-path example of the appendix is verified exactly: its physical flow,
energy gap, exact support interval, attaining rational dual, and the
asymptotic widths of the separate-edge and Laplacian intervals, including
stability when endpoint and root rounding errors are `o(eps)`.

Verification does not establish novelty; the appendix itself credits Bregman
divergences, Fenchel duality, primal-dual a posteriori bounds and the
electrical cut/cycle projection as classical. The envelope mapping from an
original uncertainty instance stays outside the package, as in topic 3.
`CLAIMS.md` lists every exclusion.
