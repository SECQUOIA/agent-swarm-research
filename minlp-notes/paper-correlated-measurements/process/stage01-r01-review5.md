# Stage 1, independent review 5

Verdict: **No major issue found. Accept the foundations after the three minor clarifications below.** This is a Stage 1 verdict, not an assessment of the unwritten algorithms, experiments, or complete paper.

## Scope and independent checks

I read `sections/01-foundations.tex`, `macros.tex`, `references.bib`, the current PDF text, the coverage/source-access records, and the Stage 1 author handoff. I did not read another reviewer report. I visually inspected rendered PDF page 2; its table, mathematics, and paragraph layout are clear. I used the existing PDF without changing its build. Scratch files are confined to `verification/stage01-review5/`.

I checked the score and information derivation; augmented-information interpretation; block-inverse inflation and equality condition; both distinct conditional experiments; the marginal increment; the Kantorovich compression proof, prior treatment, rank refinement and design guarantees; and the source time-pattern decomposition. These arguments are correct under the stated fixed positive definite covariance and nonadaptive selection model. In particular, the A-optimality direction survives inversion correctly, and the common-kernel claim justifies using the same positive definite domain. The sharpness construction works, including rational approximation. The examples' numbers were independently checked with exact fractions (scratch `exact-check.txt`).

I also checked the relevant local Liu Section IV/Proposition 2 context, Wang's accepted-manuscript coefficient and criterion passages, Patan--Bogacka's fixed/parameter-dependent covariance context, the Moradi source's attribution of the classical inequality, and the immutable kinetics source code's construction of the cross-modality covariance. The manuscript credits the established selected-covariance model, weak-correlation agreement, and matrix inequality appropriately. The distinction between source versions and software and the limited scope of the source criticism are appropriate. Coverage includes a reasonable mapping of later developments; those future proofs and novelty comparisons remain future review obligations.

## MINOR 1: State when restriction to an estimable subspace preserves the statistical criterion

**Location:** `sections/01-foundations.tex:111–117`, especially “Alternatively, fix an estimable subspace in advance and restrict all matrices to it.”

An arbitrary subspace of estimable contrasts cannot in general be handled by simply compressing the information and then inverting it. Unknown nuisance parameters in its complement can affect the contrast variance. For example, let `J = [[2,1],[1,2]]` and let the selected contrast subspace be `span(e_1)`. It is estimable, but the variance is `(J^{-1})_11 = 2/3`, while inverting the restricted matrix gives `1/2`. The current sentence can be read as asserting equivalence to the immediately preceding contrast criterion.

**Correction:** Qualify the reduction to a declared reduced parameter model, or to a common supported/invariant information subspace with an orthonormal basis. If the complement remains an unknown nuisance parameter, say that one uses the appropriate contrast covariance/Schur complement rather than merely restricting `J`. A brief qualification is enough; no new theorem is needed here. This does not affect the full-parameter theorems presently written.

## MINOR 2: Make the corollary's inherited spectral assumptions explicit

**Location:** `sections/01-foundations.tex:299–314`.

The corollary states its feasible-family assumption but does not explicitly inherit the preceding proposition's `m I <= R <= M I` or identify `alpha` as its constant. Context makes the intended result evident and the proof is valid, but a reader quoting the corollary independently has an incomplete hypothesis/notation contract.

**Correction:** Begin “Under the assumptions of Proposition ... , with alpha as in (...), suppose ...”. The rank refinement can inherit `r_S` in the same sentence or by the existing reference. This is a presentation repair, not a mathematical change.

## MINOR 3: Identify which ratio has a supremum in the sharpness example

**Location:** `sections/01-foundations.tex:345–350`.

The text has just defined the achieved efficiency `1/b^2` approaching `1/alpha` from above, and then calls the bound “sharp as a supremum.” The worst efficiency is an infimum; the supremum applies to the reciprocal loss `b^2` or to the additive log loss. A reader could reasonably regard the current wording as reversing the extremum.

**Correction:** Say that the efficiency lower bound is sharp as an infimum, or state explicitly that the multiplicative loss approaches its supremum `alpha` (and log loss approaches `log alpha`). The example itself is correct.

## No further Stage 1 blocker

I found no unsupported positive novelty claim in this stage and no mathematical error that invalidates its substantive propositions. The provisional absence of an introduction, abstract, and later sections is intentional and is not a Stage 1 issue. Final submission review should ensure that the detailed foundations connect clearly to the later algorithms and that all computational certificate claims are independently supported there.
