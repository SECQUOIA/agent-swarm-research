# Independent source inventory: represented-matroid spectral approximation sets

Date: 2026-09-22. This inventory freezes the obligations for topic 22. It
does not certify new Lean proofs or claim that implementation is complete.

## Sources and scope

The primary source is
[Spectral approximation sets for rationally represented matroid bases](../../../notes/research-20260912-represented-matroid-psd-approximation-set.md),
Sections 1–6. Section 7 supplies attribution, qualifications, and explicit
algebraic counterexamples; Section 8 gives an equivalent owner-count
construction. The
[historical independent mathematical review](../../../notes/research-20260912-represented-matroid-psd-independent-review.md)
checks the theorem and its bit complexity, but predates these Lean proofs.
Its exact Python checker deliberately uses exponential methods on small
fixtures; its success is not evidence of a polynomial implementation.

The related manuscript is
[paper-correlated-measurements](../../../paper-correlated-measurements/README.md).
Its main statement is `thm:matroid-spectral-set` in
[sections/03-approximation.tex](../../../paper-correlated-measurements/sections/03-approximation.tex).
The same section's criterion and reuse consequences are inherited by the
matroid theorem. The complete matroid proof and restriction witnesses are
in the section `app:matroid-proof` of
[appendices/approximation.tex](../../../paper-correlated-measurements/appendices/approximation.tex).
The introduction also states the result and its scope, and the discussion
warns that additive matroid atoms do not model arbitrary correlated history.
These are the paper locations that must remain consistent with the final
verification boundary. The earlier Gaussian-message and explicit-DAG
appendix material is outside this new implementation scope.

The source attributes the determinant profile method to Berstein et al.,
*Nonlinear Matroid Optimization and Experimental Design* (2008): signed
shifts in Lemma 4.1, positive support in Proposition 4.2, determinant and
interpolation in Lemmas 4.3–4.4, and deletion recovery in Lemma 2.1.
This inventory uses the supplied note and independent review for that
attribution; it does not perform a new literature-priority audit. Formal
verification must prove the needed identities and algorithms rather than
introduce those source results as new axioms.

The [37 frozen claims](CLAIMS.md) cover the original rational input,
actual feasible-base producer, all-target spectral sandwich, exact singular
ranges, cardinality, Turing bit complexity, criterion consequences, useful
explicit subclasses, and concrete limitations of the proof route. Priority,
practical runtime, general independence-oracle inputs, finite-field input
conversion, matroid intersection, arbitrary correlated information, and
simultaneous DAG-path and matroid constraints are not claimed. Other queued
topics are not authorized by this inventory.

## Input and output contract

The matroid is represented by an explicit rational `a` by `m` matrix `A`;
a column set is independent precisely when its columns are linearly
independent over the rationals. Each element and the prior carry a rational
symmetric PSD matrix of order `p`. The input accuracy is rational and in
`(0,1)`. Only `p` is fixed. In particular, `a`, `m`, and the matroid rank
`q` grow with the input.

The result is a finite set of actual original bases. For every original
base `B`, one returned base `Bhat` must satisfy both relative inequalities
with respect to `J(B)`. The representative does not vary with the quadratic
form direction. Neither fractional designs, bases of a smaller-rank
restriction, nor unattained integer profiles are admissible outputs.

The matroid always has a base. Rank `q=0` means its unique base is empty,
even when the prior information is nonzero. This differs from information
rank `r=0`, where PSD summands force the prior and all selected atoms to
be zero. The optional rank `q'=q-|F|` is a third quantity; `q'=0` returns
the forced set exactly and must not invoke a strictly positive residual
bound of the form `0 <= residual < q'h`.

## Equivalent owner forcing

The primary construction contracts the independent owner set after a
rank-preserving restriction. Its change-of-basis representation gives a
bijection between contracted bases and original bases contained in the
retained elements and containing the forced set.

This implementation selects the source's alternative of retaining original
rows and adding a single
integer profile coordinate that counts forced owners. Restricting this
coordinate to `|F|` forces every owner, because bases are sets. This is an
equivalent construction whose proof must connect it to the same
original feasible family and establishes the displayed final cardinality
bound. The additional profile coordinate increases interpolation work but
not the number of retained owner-complete profiles at a fixed trial. The
forced contribution is common and can be subtracted exactly. An alternative
must not silently change the guarantee or assume a feasibility oracle.
The implementation does not claim to construct a contraction matrix.
Its full-base information degree bound is `2qLmax`; the common owner-complete
marker is fixed at `|F|`. Subtracting the shared forced profile identifies
the retained profiles with optional profiles and recovers the original
output bound. Interpolation uses `d+1` variables, still fixed when `p` is
fixed, rather than the contracted construction's `d` variables.

## Reuse and new proof obligations

The completed [topic 21 package](../21-dag-spectral/README.md) has useful
generic foundations despite its directory name. In particular,
`NormalizationComplete.exists_accepted_trial` applies to any selected
finite set of atoms: it gives a genuine enumerated trial, the normalized
identity floor, exact range, forced-owner bound, and target magnitude
bounds. It does not require that the selection is a DAG path.
`FactorInputData.cachedFactorData` connects actual cached rational
factorization to these interfaces. Normalization, signed-floor error,
spectral perturbation, kernel preservation, criterion comparisons, and
common-range pseudoinverse results can therefore be reused by proving the
appropriate base interfaces. There is no reason to duplicate these proofs.

The main new blocks are the represented-base model and rank safeguards;
determinant profile support; exact interpolation and actual deletion
recovery; variable-dimension rational linear algebra; and integration of
their execution and costs with the original-matrix normalization producer.
Suggested bounded modules follow those responsibilities, with separate
producer, correctness, cardinality, execution-cost, and headline layers
where their interfaces are stable. Documentation names alone do not imply
that such modules are already present or verified.

An important reuse limit is already visible in the code. Topic 21's
`RationalMatrixArithmetic.determinantBits` bounds a determinant by
`1 + n.factorial * (n*B+3)`, and its inverse bound derives from that.
`MatrixArithmeticTrace.determinantExpr` explicitly enumerates permutations;
its operation count is `n.factorial*(n+2)`. Those routines are compatible
with fixed information dimension `p`. They cannot supply polynomial work
or the needed polynomial encoding bound at variable matroid rank `q` or
variable interpolation-system dimension. New elimination or an equivalent
polynomial algorithm and sharper bit bounds are substantive obligations.

## Review risks

The source's independent mathematical review identifies no false theorem.
The central risks are lost hypotheses, assumed producers, or cost bounds
that no longer hold when matroid rank grows.

- Restriction must retain original rank. Deletion must retain the original
  row dimension even after columns are removed; recomputing a smaller
  rank can incorrectly accept a smaller set as a base.
- Forced owners are distinct elements, while selected factors remain
  distinct labels. Prior factors require no element. A removed forced
  owner invalidates the trial rather than disappearing from the condition.
- Positive squared minors have no cancellation over the rationals. An
  arbitrary modular reduction can erase a positive coefficient. Mixed
  determinants for two different representations can cancel.
- The maximum-volume basis is chosen separately for each target and only
  in the proof. Its real square roots are not algorithm inputs.
- Exact interpolation must be connected to computed determinant values.
  A formal coefficient sum over every base proves support but does not
  by itself prove the asserted algorithm or its complexity.
- Polynomial arithmetic-operation counts alone are insufficient. Input
  normalization, representation operations, grid monomials, determinant
  evaluation, interpolation, and deletion all need controlled operand
  bit lengths. Factorial costs cannot be hidden in a constant depending
  on `p` when their argument is `q` or the profile-grid size.
- Reusing scalar criterion inequalities must still select an actual
  returned base. Exact E comparisons need equality handling, and ordinary
  inverse-trace costs must keep the all-singular case explicit.

## Verification boundary

Completion requires a declaration-level coverage map for every frozen
claim, an independent review of the assembled statements and producer,
targeted warning-free Lean builds, axiom audit, and per-module kernel
replay with stable source hashes. Standard Lean foundational axioms may
be recorded; `sorry`, unproved custom axioms, and `native_decide` are not
substitutes for the requested verification.

No targeted Lean check was run as part of this inventory because it changes
only these scope documents. Project-wide verification and CI inspection
are excluded from local work. The mathematical source review, small exact
fixtures, Lean verification, and paper build are separate kinds of evidence
and must be reported separately.
