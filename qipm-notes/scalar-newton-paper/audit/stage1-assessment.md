# Stage 1 assessment, round 1

All five independent reports found no major mathematical issue. Root also
checked the scalar variance, residual, rejection law, and precision proof.

Accepted minor corrections:

1. Define the approximate estimator at zero coordinates, require arithmetic
   error only on support, and explicitly phrase the comparison as a coupling.
   This resolves reviewer 1 item 1, reviewer 2 item 1, reviewer 3 item 2,
   reviewer 4 item 3, and reviewer 5 item 1.
2. State the ideal random-real and comparison convention for exact rejection.
   This resolves reviewer 3 item 1 and reviewer 4 item 4.
3. Name and cite the classical Kantorovich inequality while retaining its
   proof. Root checked Lin's original PDF, equation (1.1), which states the
   classical inequality. Its substitution x=P^(1/2)b/sqrt(b*Pb) yields the
   inequality used here. This resolves reviewer 1 item 2 and reviewer 4 item 2.
4. Make the Andoni–Krauthgamer–Pogrow relationship precise: their Section 1.4
   poses the sampler-to-sampler question; their main results concern other
   output guarantees. Reviewer 4's suggestion that no such antecedent exists
   is not sustained by the full text (also checked by reviewers 3 and 5).
   The proposed wording clarification is nevertheless useful and accepted.

A separate fixer is assigned all four changes, build/diagnostic verification,
and a correction record. No major finding means a second five-reviewer round
is not required for this stage. Root will check the fixes before Stage 2.
