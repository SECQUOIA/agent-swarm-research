# Stage 1, round 1 — independent review 5

## Verdict

**No major issues found. One valid minor literature-positioning correction is needed.** The foundational statements and proofs are mathematically sound in the stated bounded, equality-constrained setting. The stage is appropriately self-contained for its intended scope; the absent later sections are not treated as omissions in this review.

## Findings

1. **R5-S01-01 — minor: make the equality-model overlap with Khademnia–Davarnia explicit.** Location: `sections/01-foundations.tex`, lines 68–70, in the prior-work subsection: “Their model permits balance inequalities, whereas (1) imposes equalities.” The general framework indeed uses inequalities, but the cited paper's network specialization explicitly starts with equality balances represented as opposite inequality pairs. Its Section 3 says that the balance constraints are separated into two inequalities of opposite signs, with each incidence row duplicated with a negative sign. Thus the current contrast can suggest that the relevant predecessor's network results concern a different balance model, even though its principal network specialization already includes precisely the equality-flow setting used here. Please say that the general framework permits inequalities **and** its Section 3 represents equality balances by opposite pairs; the present paper exploits the underlying equality circulation space. This is minor because the surrounding text already credits the full disaggregation and general projection framework, and correcting this sentence does not invalidate a theorem or require a new argument. Evidence: repository source `literature/papers/khademnia2025-convexification-of-bilinear-terms-over/original.pdf`, Section 3 opening paragraph; the extracted passage is retained in `verification/reviewer5/stage01-round01/khademnia.txt`, lines 202–206.

No other necessary corrections were identified. In particular, I do not regard the sparse introduction or abstract as a defect at this foundations-only stage; their final integration is explicitly scheduled later.

## Mathematical checks actually performed

- Read all source statements and proofs in the frozen snapshot, including the preamble, introductory scope, references, and process scope.
- Checked both directions of simplex disaggregation, the claim of at most `m+1` graph points, and the distinction between the scaled constraint system at zero weight and multiplication of an empty polytope. The proof correctly implies nonemptiness from any positive state weight, so it also handles an empty flow polytope.
- Checked componentwise solvability of the incidence equations and the spanning-forest construction. Loops give zero columns and isolated vertices require zero balance; the stated component condition covers both.
- Checked the fundamental-cycle proof of block factorization, including parallel edges, individual loops, articulation vertices, and bridges. A fundamental cycle lies in a single cyclic block; extension by zero produces global circulations. The affine-product conclusion is valid even when some block domain is empty.
- Checked local state merging and proportional refinement when different blocks observe different labels. The reconstruction preserves the common global simplex weights, capacities, incidence equations, state sum, and observed products. Zero merged weight and zero individual weight are correctly handled.
- Checked the linear scaled-block form for reference flows outside capacity bounds. Its bounds become zero at zero weight, and scaling is exact at positive weight; no assumption that a deviation domain contains the origin is inadvertently used.
- Checked the cases `m=0`, no observations, no cyclic blocks, and capacity-induced lower-dimensional domains. No exceptional case contradicts the claims.
- Recomputed the one-dimensional reaggregation example: both original domains are `[0,1]`, whereas the aggregated system admits `q=2`. The Kis–Horváth Section 2, equation (7), reference does discuss precisely the failure of the common-matrix aggregate system to equal the hull in general.
- Confirmed the caution about adding arbitrary linear side constraints: intersection with a known hull is a valid relaxation, but convexification need not commute with intersection.

## Build and presentation checks

Built a **private copy** of the snapshot using the documented command:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The build succeeded and produced a seven-page PDF. The final log contained no undefined references, undefined citations, overfull/underfull boxes, or LaTeX warning lines. I visually inspected rendered pages 1, 5, and 7, covering the title and opening model, the local-state theorem, and the bibliography. Equations, theorem formatting, hyperlinks, and bibliography text were legible and remained inside the page boundaries. Evidence is retained under `verification/reviewer5/stage01-round01/`.

The notation is consistent at the conceptual level: `lambda_0` is the global residual state, the local starred state includes all globally unobserved labels for that block, and cycle rank is ambient rather than feasible affine dimension. The explicit explanations of these distinctions are useful for readers.

## Review limitations

This review does not establish novelty of later results, validate future computational claims, or independently check every bibliographic metadata field against a publisher. Direct source comparisons concentrated on the two citations used for the network-model distinction and the reaggregation boundary. No numerical theorem tests were needed for these elementary exact proofs. I did not read other current-round reports, coordinate judgments with other reviewers, modify manuscript sources, or build in the frozen snapshot.
