# Stage 7 independent review 2: novelty, priority, and claim scope

Date: 2026-09-22. Reviewer: `/root/s7_review2`.

**Recommendation: accept stage 7. No major or minor correction identified in the reviewed scope.**

## Scope and method

Read the frozen abstract, introduction, discussion, references, the relevant
novelty paragraphs in Sections 6–9, the Gram theorem and credited classical
inputs, and the stage 7 author/literature records. Consulted earlier primary
source audit records to distinguish previously inspected evidence from new
checks. This review did not rerun compilation or the proof supplement and
does not purport to independently verify every mathematical proof.

Freshly opened the following primary sources online:

- [BDS, arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2), especially
  the good-aggregation definition and Conjectures 3.1–3.3.
- [Blekherman–Dunbar, arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1),
  Theorem 1.4, Proposition 3.15 and its Section 8 proof, and the dimension
  discussion including Proposition 8.7.
- [Wang–Kılınç-Karzan, arXiv:2403.04752v2](https://arxiv.org/html/2403.04752v2),
  Section 4.1 and its replication-count condition.
- The [Emory dissertation record](https://etd.library.emory.edu/concern/etds/vq27zq10w)
  and primary-PDF search extraction of Theorem 5.0.5. Also inspected the
  saved public-reader extraction around that theorem. I did not visually
  inspect the dissertation PDF.

Additional bounded searches for the exact HHC conjecture terms, Gram-map
HHC, and strict four-aggregation results found no conflicting primary
result. Search non-discovery is not proof of priority.

## Findings

1. The three-conjecture mapping is accurate. Conjecture 3.1 asks for HHC
   with no finite good family; 3.2 proposes six necessary under three-row
   PDLC; 3.3 asks for the nonconstant convex certificate. The introduction
   identifies the respective affirmative, negative, and affirmative
   resolutions correctly and binds numbered locators to a fixed version.
   Nonemptiness makes the source's “not a negative constant” formulation
   equivalent to the manuscript's nonconstant aggregation formulation.

2. The strict PDLC priority claim is appropriately narrow. The manuscript
   credits the known four-bound, the BDS sharpness example, the existing
   negative-eigenvector limiting argument, and the dissertation's stronger
   stated regular nonstrict result. It claims the complete unrestricted
   strict transfer, including dependent triples. The external theorem is
   stated with independence, regularity, nonempty interior, and no points
   at infinity. No smooth spectral curve assumption has been silently
   imported or omitted. The cited preprint expressly treats dimensions
   one and two, supporting that part of the transfer's scope.

3. The dissertation discussion is fair to the accessible evidence. It
   acknowledges the prior stronger statement without alleging an error
   from damaged extraction or relying on an unverified stronger theorem.
   The introductory qualification is consistent with Section 9.

4. The Gram and infinite-family claims distinguish the substantive new
   statements from classical ingredients. The introduction does not claim
   fidelity concavity, matrix variational identities, quadratic matrix
   programming, or infinite aggregation in general as new. Section 7
   explains the difference from prior non-HHC and signed-equality examples.
   The stronger arbitrary-quadratic obstruction is explicitly restricted
   to conjunctions in the original variables and does not conflict with
   the finite lifted description.

5. The QMP comparison is accurate: Section 4.1 of the cited primary paper
   gives the stated sufficient replication threshold, which becomes
   r >= 3 for this three-constraint example. The manuscript does not infer
   the strict r = 2 result merely by replacing inequality signs or fixing
   a level after a different convexification result.

6. Approximation novelty is appropriately restricted to the prescribed
   cone and explicit dimension-independent bounds. The classical
   inverse-square exponent and objective-specific convex-duality result
   are credited. Neither the abstract nor discussion turns the result
   into an iteration complexity claim.

7. The abstract and discussion accurately summarize the manuscript's
   proved distinctions. Formal-verification language is restricted to
   named portions rather than implying that literature priority or the
   entire manuscript is mechanically checked. No unsupported broad
   “first” claim was found.

No manuscript file was edited. No project-wide check or CI inspection was
performed.
